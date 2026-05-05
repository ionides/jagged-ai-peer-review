# Peer Review: W22 Project 12 — Modeling COVID-19 Cases in Michigan

## Summary

This project fits ARIMA and SEIR POMP models to daily COVID-19 case counts in Michigan, with the primary mechanistic analysis focused on the Omicron wave (December 2021 – April 2022). The ARIMA section covers both the full time-series and the Omicron subset; the SEIR section introduces a two-phase transmission parameter (beta0 before day 33, beta1 after) to capture the behavioral response to the outbreak. The global search finds a best log-likelihood of approximately -1155. While the project demonstrates familiarity with the pomp workflow, it has serious deficiencies in measurement-model correctness, parameter identifiability, computational adequacy, and profile-likelihood reporting that undermine the validity of the conclusions.

---

## Major Issues

### 1. Dmeasure and rmeasure use inconsistent variance formulas (measurement model error)

The mathematical specification (Equation for dC/dt) gives the variance as:

    rho*(1-rho)*H + (psi*rho*H)^2

but the dmeasure Csnippet computes:

    double sd = sqrt(pow(psi * H, 2) + rho * H);

The first term `pow(psi * H, 2)` omits the factor `rho^2` (it should be `pow(psi * rho * H, 2)`), and the second term `rho * H` omits the `(1-rho)` factor. Separately, the rmeasure Csnippet uses yet another formula:

    sqrt(pow(psi * rho * H, 2) + rho * (1 - rho) * H)

which matches the mathematical statement but differs from dmeasure. This inconsistency between dmeasure and rmeasure means the particle filter is evaluating a likelihood under a different measurement distribution than the one used to simulate data. This invalidates all reported likelihoods and all downstream conclusions.

Wheeler et al. (2024) emphasize that the measurement model in code must match the mathematical description; here neither dmeasure nor rmeasure matches consistently.

**Fix:** Align dmeasure to use `sd = sqrt(pow(psi * rho * H, 2) + rho * (1 - rho) * H)`, matching the stated mathematical model and the rmeasure implementation.

---

### 2. H accumulates recoveries (dN_IR) but the measurement model conditions on H as reported cases

The model adds `dN_IR` to the accumulator `H` in the process model (`H += dN_IR`), which tracks the flow into the recovered compartment. But `H` is then used in dmeasure and rmeasure as the mean of reported cases, implying reported cases = new recoveries rather than new infections or confirmed positives. Epidemiologically, COVID-19 case reports correspond to confirmed infections (transitions from E to I, or newly symptomatic), not to recoveries. Using dN_IR as the observation mean is a structural misspecification: it delays the peak by the entire infectious period and produces the wrong relationship between transmission parameters and observed data.

**Fix:** Track new infections (dN_EI) in the accumulator H, or track newly symptomatic individuals, to match what the surveillance data actually measure.

---

### 3. No profile likelihood computed for any parameter

The project performs only local and global searches and presents a scatterplot matrix of the likelihood surface. No profile likelihoods are computed for any parameter. Without profile likelihoods, it is impossible to assess parameter identifiability or report confidence intervals. The scatterplot matrix itself shows clear lack of convergence in rho and psi (acknowledged in the text), yet no formal identifiability analysis is performed.

This is a course-confirmed error (Error 1.9 / POMP Checklist item 5): profile likelihoods are a required component of the analysis. The absence means no uncertainty quantification is possible for any parameter estimate.

**Fix:** Compute profile likelihoods for at least the key parameters (beta0, beta1, rho, eta) following the course standard (5–30 profile points at run_level 2–3), and report confidence intervals.

---

### 4. Global search uses only a single mif2 pass with Nmif=50, then a second mif2 with default Nmif

The global search code runs `mif2(params=c(unlist(guess), fixed_params))` (using mf1's settings, Nmif=50) and then immediately `mif2(Nmif=50)` — a total of 100 mif2 iterations from a random starting point. The local search itself only uses Nmif=50. For a model with 5 free parameters and ~133 observations, this level of computation may be insufficient to reliably reach the global MLE. The loglik traces from the local search show convergence around -1200, while the global search reaches -1155 — a gap of ~45 log units — suggesting that the local search with Nmif=50 was not reaching the true optimum. No evidence is presented that further computation would not improve the result.

Per Wheeler et al. (2024), the single largest improvement in log-likelihood in their analysis "was primarily attributed to increasing the computational effort in numerical maximization." Without a convergence check (e.g., multiple independent global searches reaching the same terminal likelihood), the MLE may not be reliable.

**Fix:** Run the global search with more iterations (at minimum Nmif=100 as the course run_level=2 standard), and verify that multiple runs converge to the same maximum log-likelihood.

---

### 5. Fixed parameters mu_EI and mu_IR are not estimated and no sensitivity analysis is performed

The authors fix mu_EI = 0.33 and mu_IR = 0.14 throughout the entire analysis and do not perturb them in the random walk. No sensitivity analysis is conducted to assess how the fitted likelihoods and other parameter estimates change with different fixed values. For COVID-19/Omicron, the infectious period is known to vary substantially across studies; fixing these parameters without sensitivity analysis may distort the estimates of beta0, beta1, rho, and eta.

Furthermore, fixing nuisance parameters at literature-derived values rather than estimating them or profiling over them violates the principle that profile likelihoods should be computed even for "fixed" parameters when they are uncertain.

**Fix:** Either estimate mu_EI and mu_IR (letting them vary with appropriate random walk), or conduct a sensitivity analysis by re-fitting at several plausible values (e.g., mu_EI in [0.25, 0.5]) and comparing resulting likelihoods.

---

### 6. No benchmark comparison to a non-mechanistic model

The project fits both ARIMA and SEIR models but does not perform a quantitative likelihood comparison between them. The conclusion states the SEIR model is "much more explanatory than using ARIMA," but no log-likelihood or AIC values from the ARIMA models are reported or compared to the SEIR log-likelihood of -1155. Without this comparison it is impossible to judge whether the mechanistic model adds value over the statistical alternative.

This is a course-confirmed error (Error 1.6): benchmark comparison is explicitly taught as a validation tool. An IID (negative binomial) model would provide the weakest meaningful benchmark.

**Fix:** Report the ARIMA log-likelihoods for the Omicron dataset alongside the SEIR log-likelihood, and include at least an IID negative-binomial comparison to anchor the scale.

---

### 7. The time-varying beta switch at t=33 is hardcoded without justification or estimation

The model sets `if(t>33) { Beta = beta1; }` — a sharp, deterministic switch on day 33 of the Omicron wave. This value appears to have been chosen visually (the authors note it corresponds to "around the inflection point") but it is not estimated as a parameter and no sensitivity analysis is conducted over the switch time. A hardcoded, unestimated structural break that determines which transmission rate applies to each observation is a form of ad hoc calibration that can artificially inflate the apparent fit and makes the model non-identifiable in the usual sense.

**Fix:** Either estimate the switch time as a parameter (with appropriate prior or constraint), profile over it, or replace the sharp switch with a smooth sigmoid function for beta(t) and estimate the midpoint and slope.

---

## Minor Issues

### 8. Measurement model uses a normal approximation for count data without checking adequacy

The measurement model uses a Gaussian approximation for what is inherently count data. For small H (near the tail of the Omicron wave), the normal approximation will assign non-negligible probability to negative case counts, and the rounding via `nearbyint` in rmeasure does not resolve this for dmeasure. The authors note that simulations show "much higher variance than actual data," which may partly reflect this distributional mismatch. A negative binomial measurement model is standard for COVID case counts and would be more appropriate.

---

### 9. AIC table labels the model plots incorrectly (Figure 10)

The caption for Figure 10 reads "Michigan COVID-19 Omicron Cases and fitted ARIMA(5,1,5) Model" but the code (`arima(case, ...)`) fits the full dataset, not the Omicron subset. This is a labeling error that creates confusion about which dataset is being modeled.

---

### 10. The scatterplot matrix filter uses `loglik > max(loglik) - 100000`

When plotting the likelihood surface (Figure 18), the filter condition `filter(loglik > max(loglik) - 100000)` retains essentially all results since no runs have loglik differing by 100,000 units. This filter does nothing and appears to be a copy-paste artifact from a template where the threshold should be something like `max(loglik) - 10` or `max(loglik) - 50`. The resulting plot is not a meaningful depiction of the high-likelihood region.

**Fix:** Use a threshold such as `max(loglik) - 50` to focus the pairs plot on the high-likelihood region and make identifiability patterns visible.

---

### 11. Initial compartment values E=30000 and I=15000 are fixed without justification

The rinit Csnippet fixes E=30000 and I=15000 at time zero. These values are not motivated by data or estimated as parameters. On December 1, 2021, Michigan was reporting roughly 4,000–8,000 daily cases; 15,000 infected individuals at initialization (before scaling by rho) is plausible but not justified. Sensitivity to these fixed initial conditions is not assessed.

Per Wheeler et al. (2024), initial conditions can substantially affect model fit (up to ~72 AIC units in their analysis). At minimum, a brief sensitivity check should be reported.

---

### 12. ACF plots are labeled "Autocovariance function" but display autocorrelation

Figures 6 and 8 are labeled "Autocovariance function" (both in the text and as the figure captions), but the R function `acf()` by default returns autocorrelations (normalized, dimensionless), not autocovariances. This is a terminology error.

---

### 13. The text contains an incomplete sentence in the Omicron seasonality section

The sentence "Next, we explore patterns in the Omicron data, and notice a weekly ." is incomplete — it ends with "weekly" followed by a period, with no noun completing the thought. This appears to be a drafting artifact.

---

### 14. ARIMA model selection defaults to ARIMA(5,1,5) for both full and Omicron data without cross-validation or out-of-sample assessment

The project selects ARIMA(5,1,5) for both datasets based purely on in-sample AIC. With p+q=10 parameters and weekly seasonal structure present in the data (period 7 detected in the spectrum), a SARIMA model would be more appropriate. The authors acknowledge weekly patterns but do not attempt a seasonal ARIMA even though the spectral analysis clearly identifies a 7-day cycle. Given that ARIMA(5,1,5) then fails residual diagnostics (ACF of residuals shows autocorrelation), the model selection step does not lead to a model that passes diagnostics, and the authors do not investigate why or attempt alternatives.

---

### 15. The conclusion overstates the success of the SEIR model

The conclusion states the SEIR model is "much more explanatory than using ARIMA" and that "with these parameters, the model is better able to capture the weekly variance." However, Figure 17 (the final simulation plot) shows that simulated trajectories have substantially higher variance than the data, and the authors themselves note this. No quantitative comparison supports the claim that the SEIR model outperforms ARIMA. Given the measurement model inconsistency identified in Issue 1, the reported log-likelihood cannot be taken at face value, making any such comparison unreliable.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/new_global2.csv`
