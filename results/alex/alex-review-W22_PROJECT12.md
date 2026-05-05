# Peer Review: Modeling COVID-19 Cases in Michigan
**Project:** W22 Project 12
**Reviewer:** Alex
**Date:** 2026-04-10

---

## Summary

This project models daily COVID-19 case counts in Michigan using ARIMA and SEIR POMP models. The authors first apply ARMA/ARIMA to the full dataset and to the Omicron sub-period (December 1, 2021 to April 13, 2022), then build a stochastic SEIR POMP model with a time-varying transmission rate for the Omicron wave. The effort covers data exploration, spectral analysis, model building, local and global likelihood searches, and a brief conclusion. While the scope is reasonable, there are substantial methodological, presentational, and inferential weaknesses throughout.

---

## Weaknesses (Most Critical First)

### 1. [Major] Hard-coded, unjustified threshold for beta switch (t > 33)

The Csnippet for `seir_step` switches the transmission rate from `beta0` to `beta1` at `t > 33` (day 33 of the Omicron sub-series), which corresponds approximately to January 3, 2022. This cutoff is hard-coded with no justification in the text, no sensitivity analysis, and no discussion of what biological or policy event it represents. A POMP model should either estimate the change-point or provide a clear epidemiological rationale. As implemented, the step-change is also biologically implausible (transmission does not change discontinuously overnight), and the choice of day 33 visually coincides with the peak of the Omicron wave but is not argued to be the peak; the authors simply say "around the inflection point." This is the single most consequential modeling decision and it receives no formal treatment.

### 2. [Major] mu_EI and mu_IR are fixed, not estimated -- and this is inadequately justified

The authors fix `mu_EI = 0.33` (mean latent period ~ 3 days) and `mu_IR = 0.14` (mean infectious period ~ 7 days) for the entire local and global search, treating them as known constants. In the text this is presented as a "reasonable assumption" based on CDC literature, but these parameters interact strongly with beta and rho in determining epidemic dynamics. Fixing them prevents the optimizer from exploring a key portion of parameter space and may artificially inflate identifiability of the remaining parameters. The project should at minimum show a profile likelihood over these parameters, or explain why fixing them is statistically valid given the data.

### 3. [Major] Measurement model inconsistency between dmeas and rmeas

The `dmeas` Csnippet computes the likelihood using a Normal approximation with standard deviation `sqrt(pow(psi * H, 2) + rho * H)`, while `rmeas` generates with `sqrt(pow(psi * rho * H, 2) + rho * (1-rho) * H)`. These are not the same variance formula: `dmeas` uses `psi * H` but `rmeas` uses `psi * rho * H`. This inconsistency means the particle filter evaluates a different distribution than what is simulated, which corrupts likelihood estimates and invalidates parameter inference. This is a code-level bug with direct consequences for all reported likelihoods.

### 4. [Major] Global search box does not include parameter space explored by local search

The global search box is stated as: `beta0 in [0.4, 0.6], beta1 in [0.15, 0.3], rho in [0.8, 1], eta in [0.3, 0.5], psi in [0.5, 0.95]`. The starting values used in the local search were `beta0=0.7, rho=0.5, psi=0.15`, which are outside the global search box. The text claims the box was "set a reasonable interval around the parameter estimates obtained from the local search," but the local search MLE (not the starting point) must be consulted. More importantly, `rho in [0.8, 1]` excludes the initial guess of 0.5, suggesting the local search converged to values near 1 for rho. If so, the upper boundary `rho=1` is hit repeatedly in the global search (the CSV shows many rows with rho > 0.99), suggesting the search box is miscalibrated and the MLE for rho is on the boundary -- a sign of model misspecification or over-reporting rate estimation problem, not properly diagnosed.

### 5. [Major] Particle filter standard error is very large at the initial guess

The authors report an unbiased log-likelihood of -1644.5 with standard error 4.77 at the starting parameter values, using Np=1000. A Monte Carlo SE of nearly 5 log-likelihood units is very large and indicates the particle filter is collapsing frequently at these parameter values. While the authors note this (implicitly, by using it only as a diagnostic), they do not increase Np before the local or global searches, where Np=1000 is used throughout. The final MLE has SE of 0.025, suggesting particle collapse is less of an issue there, but the intermediate search steps may have suffered from unreliable likelihood estimates that biased the optimization trajectory.

### 6. [Major] No profile likelihood or confidence intervals for any SEIR parameter

After completing the global search, the authors present only a pairs plot of likelihood surface and a table of the top parameter estimates. There are no profile likelihoods, no confidence intervals, and no formal uncertainty quantification for any estimated parameter. For a POMP analysis this is a critical omission: the pairs plot shows the rho-psi surface has no clear peak (the authors acknowledge "a lack of convergence"), but they do not follow up with profile likelihoods to understand the identifiability problem. Reporting MLEs without CIs provides no basis for epidemiological inference.

### 7. [Moderate] Local search uses only 20 chains with Nmif=50, which is insufficient

The local search runs 20 chains with Nmif=50 and cooling.fraction.50=0.5. For a 5-dimensional optimization (beta0, beta1, rho, eta, psi) with complex likelihood geometry, 50 iterations is very low and may not allow convergence, especially with a random walk standard deviation that includes `beta1 = rw.sd(0.015)` -- substantially smaller than for beta0 (0.05). The trace plots show the log-likelihood "seems to increase and converge around -1200," but 50 iterations is not enough to be confident of convergence. The global search then uses `mif2(Nmif=50)` as well, compounding this.

### 8. [Moderate] The ARIMA analysis conflates model selection with model validation

The authors select ARIMA(5,1,5) for both the full dataset and the Omicron sub-period using AIC, then immediately note residual non-normality and residual autocorrelation. These diagnostic failures are presented as a reason to prefer SEIR, but no attempt is made to address them within the ARIMA framework (e.g., SARIMA with period 7 given the confirmed weekly seasonality, or a log transformation). Applying a purely descriptive model like ARIMA to epidemic data is reasonable as a benchmark, but the comparison between ARIMA and SEIR is based on qualitative observation rather than any formal criterion, making the motivation for moving to SEIR methodologically weak.

### 9. [Moderate] Weekly seasonality is identified but never modeled

Both the full-period and Omicron spectral analyses clearly identify a 7-day periodic pattern in reported cases, and the authors acknowledge this is likely a reporting artifact. However, neither the ARIMA model (which would use a SARIMA with period 7) nor the SEIR model accounts for this periodicity. The overdispersion parameter psi is suggested as a way to absorb this variation, but overdispersion captures variance inflation, not autocorrelated weekly patterns. The failure to handle the weekly cycle undermines the fit of both model classes.

### 10. [Moderate] E and I initial conditions are fixed at arbitrary values

In `seir_rinit`, the initial conditions are set as `E = 30000` and `I = 15000` with no justification and without estimating them. These are free parameters that could substantially affect fit during the first few weeks of the Omicron wave. Fixing them at round numbers without sensitivity analysis is not defensible. The initial susceptible fraction eta is estimated but the seeding of E and I is not, creating an inconsistency.

### 11. [Moderate] Incomplete sentence in the text

The section "Seasonality Analysis / Omicron Data" contains the incomplete sentence: "Next, we explore patterns in the Omicron data, and notice a weekly ." This is a sentence fragment that was left unfinished, indicating the paper was not proofread before submission.

### 12. [Moderate] Figure 10 caption is incorrect

The caption for Figure 10 reads "Michigan Confirmed COVID-19 Daily Cases (black) and ARIMA(5, 1, 5) model fitted values (red)" but the title in the code says "Michigan COVID-19 Omicron Cases and fitted ARIMA(5,1,5) Model" -- Figure 10 is for the full dataset, not the Omicron subset, so the code title is also misleading. The caption should describe what is actually plotted (the full two-year dataset) and distinguish it clearly from Figure 12.

### 13. [Minor] Global search filter threshold is trivially permissive

The pairs plot filters results with `filter(loglik > max(loglik) - 100000)`, which is essentially no filter at all given that the range of log-likelihoods in the global search spans maybe 200 units. The standard practice is to filter to `max(loglik) - 10` or `max(loglik) - 20`. Using 100000 means all results including badly failing chains are shown, making the pairs plot less informative about the actual likelihood surface near the MLE.

### 14. [Minor] The data read from two sources inconsistently

The cleaned CSV `michigan_covid_clean_noNA.csv` is read at the top for EDA and ARIMA analysis, but then the raw Excel file `Data.xlsx` is re-read partway through the SEIR section. It is not explained why two separate data sources are needed, and the filtered SEIR dataset `cases` may differ from the `omicron` data frame used for ARIMA. This dual-source approach creates potential reproducibility concerns and should be unified into a single data pipeline.

### 15. [Minor] No comparison of SEIR likelihood to a null or baseline

The global search best log-likelihood is -1155. There is no baseline to compare this to -- for instance, the likelihood of the data under the fitted ARIMA model, or a null model, or a simpler SIR. Without such a comparison, it is impossible to assess whether the SEIR model provides a meaningful improvement in explanatory power. The ARIMA analysis also does not report log-likelihoods in a comparable form.

---

## Summary of Priority Issues

The most critical issues are the measurement model inconsistency between `dmeas` and `rmeas` (Issue 3), the unjustified hard-coded transmission switch threshold (Issue 1), the boundary behavior of rho in the global search (Issue 4), and the absence of any confidence intervals for SEIR parameters (Issue 6). These collectively undermine the reliability of the parameter estimates and the epidemiological conclusions drawn from them.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/new_global2.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/michigan_covid_clean_noNA.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/Makefile`
