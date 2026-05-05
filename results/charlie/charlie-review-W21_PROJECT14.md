# Peer Review: W21 Project 14 — Mumps SEIR POMP Model

## Summary

This project applies an SEIR POMP model with a seasonal contact rate to 100 weeks of mumps case data from Michigan (September 1971 to September 1973), sourced from Project Tycho. The authors motivate the SEIR structure by the ~17-day mumps incubation period and explain the seasonal cosine forcing of the transmission rate. Iterated filtering via `mif2` is used for likelihood maximization, and a profile likelihood for the reporting rate rho is constructed. While the report demonstrates a reasonable command of the POMP workflow, several significant methodological problems undermine the reliability of the results: the measurement model uses a non-standard and likely incorrect negative binomial parameterization; key parameters are fixed without uncertainty quantification; no benchmark comparison is made; and the goodness-of-fit assessment is purely visual with a single simulation.

---

## Major Issues

### 1. Incorrect Negative Binomial Parameterization in Measurement Model (Major)

The `dmeas` Csnippet uses `dnbinom(cases, H, rho, give_log)`, where H is the accumulator variable counting weekly recoveries and rho is the reported reporting rate. In R's `dnbinom(x, size, prob)` convention, this sets `size = H` and `prob = rho`. This means:

- The implied mean of observed cases is `H * (1 - rho) / rho`, not `rho * H`. For rho ~ 0.12, the mean prediction is approximately `7.3 * H` — roughly seven times the number of recoveries in that week, which is mechanistically incoherent.
- H is serving as the dispersion ("size") parameter of the negative binomial rather than as the signal being reported. This conflates the latent count (as a variance control parameter) with the observation mean in a way that is not the standard reporting-delay model used in POMP disease modeling.
- The typical parameterization would use `H` as the expected number of true cases and a separate overdispersion parameter, e.g., `dnbinom(cases, size = phi, mu = rho * H, give_log = 1)`, with phi controlling overdispersion.
- Similarly, `rmeas` uses `rnbinom(H, rho)`, which generates observations with mean `H*(1-rho)/rho` — inconsistent with the interpretation of rho as a reporting probability.

This parameterization error means all fitted parameters (especially rho and b1) are not interpretable as described, and the inferred CI for rho (11.14%–14.52%) does not estimate the reporting probability it is claimed to estimate. [POMP checklist item 12: Measurement model specification; SKILL_pomp.md]

---

### 2. No Benchmark Comparison (Major)

The SEIR POMP model is never compared against any non-mechanistic benchmark (e.g., ARMA, auto-regressive negative binomial, or IID negative binomial). The conclusion states that "mumps cases of Michigan in the 1970s can be well modeled by an SEIR pomp model," but without a benchmark this claim cannot be substantiated. A simple ARMA or negative binomial regression may achieve a similar or higher log-likelihood, in which case the added structural complexity of the SEIR model would require additional justification.

Wheeler et al. (2024) note that none of the 32 papers in their Haiti cholera review performed such a comparison, and that benchmark comparisons exposed important model failures. The course quiz (Q11-01) explicitly tested this as Error 1.6. [SKILL_pomp.md checklist item 2; 531-weakness-reference.md Error 1.6]

---

### 3. Goodness-of-Fit Assessed Only by Single-Run Visual Simulation (Major)

The final model assessment is based on a single forward simulation from either local or global best parameters (Figures 7 and 11). A single stochastic realization is a very weak basis for assessing model adequacy. The simulation may happen to look reasonable or poor purely by chance. Best practice (Wheeler et al. 2024) requires at least multiple simulations to show the distribution of outcomes, or a quantitative goodness-of-fit statistic such as the log-likelihood relative to a benchmark. No formal goodness-of-fit numbers are reported to support the qualitative conclusion in the Conclusion section. [SKILL_pomp.md checklist item 3]

---

### 4. Fixed Parameters Without Sensitivity Analysis or Uncertainty Propagation (Major)

Three parameters are fixed without being estimated: `N = 8881826`, `mu_EI = 0.412`, and `mu_IR = 0.714`. While N is reasonably justified by census data, the rate parameters mu_EI and mu_IR are presented as known constants derived from biological ranges, but:

- `mu_EI = 0.412` per week implies a mean latent period of `1/0.412 ≈ 2.43` weeks (~17 days). The text claims the incubation period is "approximately 17 days," but this is actually the upper range; typical estimates are 12–25 days with high individual variability.
- `mu_IR = 0.714` per week implies a mean infectious period of `1/0.714 ≈ 1.4` weeks (~10 days), but the text says individuals can spread the virus "for over a week," which is imprecise.
- No sensitivity analysis is performed to show how the results change if these fixed values are varied within their biological plausible ranges.
- Fixing epidemiologically uncertain parameters at point values inflates apparent precision of estimated parameters and artificially narrows the profile likelihood CI for rho.

Per Wheeler et al. (2024), initial conditions and fixed parameters should be examined for sensitivity. [SKILL_pomp.md checklist item 13]

---

### 5. Profile Likelihood Only for One Parameter; No CIs for Others (Major)

Profile likelihoods and confidence intervals are computed only for rho. No identifiability assessment is presented for b1, b2, Phi, or eta, despite these being the key epidemiological and transmission parameters estimated from data. The pairwise plots (Figures 6, 9) show potential ridge-like correlations between b1 and eta, which the authors themselves note as a "trade-off effect." This collinearity suggests the parameters may not be individually identifiable, and profile likelihoods for each would be needed to verify this. Without such checks, the point estimates cannot be trusted to represent unique optima. [SKILL_pomp.md checklist item 5; 531-weakness-reference.md Error 1.9]

---

### 6. Global Search Initialized from Only a Single Local Search Result (Major)

The global search in `mumps.R` and `blinded.Rmd` calls `mif2(mifs_local[[1]], ...)` for every global replicate, inheriting the mif2 tuning parameters from only the first local search result. This means all 60 global replicates share the same base mif2 settings. While the starting parameters are drawn randomly from the global box, the mif2 settings (Np, Nmif, cooling.fraction.50, rw.sd) are all inherited from a single local run. A more robust approach would either pass the settings explicitly or cycle through multiple local mif2 objects. More critically, this means the number of mif2 iterations in the global search defaults to whatever Nmif the first local search used, which may not have been designed for global exploration. [SKILL_pomp.md checklist item 6]

---

## Minor Issues

### 7. No Model Diagnostics (ESS, Conditional Log-Likelihood, Filtering Distribution)

No diagnostic plots beyond the mif2 trace plots are presented. The effective sample size (ESS) from particle filtering is not monitored or displayed. Conditional log-likelihood plots (per-observation log-likelihoods over time) would reveal which time periods the model fits poorly. Filtering-distribution comparisons (conditioning on observed data versus forward simulation from initial conditions) would help assess whether the model's fitted structure matches the data's dynamics. Wheeler et al. (2024) used conditional log-likelihood plots to discover model misspecification. [SKILL_pomp.md checklist item 4]

---

### 8. R Compartment Not Tracked; Population Conservation Not Verified

The state vector is `c("S", "E", "I", "H")` — the Recovered compartment R is absent. H is an accumulator that resets each week. The true recovered count is implicitly N - S - E - I, but this is never computed or checked. Because the model ignores demography, it should be verified that S + E + I + R = N throughout the simulation. Without R tracked explicitly, it is impossible to verify this conservation property. If R were tracked, it would also enable biologically interpretable summaries (e.g., final attack rate). [SKILL_pomp.md checklist item 11]

---

### 9. Conclusion Overstates Model Adequacy

The conclusion states "we can now say that mumps cases of Michigan in the 1970s can be well modeled by an SEIR pomp model." This assertion is not supported by the evidence presented. The only basis offered is a single visual simulation (Figure 11) that "looks promising." With no benchmark comparison, no formal goodness-of-fit statistic, and the measurement model issues described in Issue 1, this conclusion cannot stand as written. The conclusion should be restated as a qualified finding, acknowledging the limitations listed in the Limitations section more prominently. [SKILL_pomp.md general criteria]

---

### 10. Trace Plots Show Slow or Incomplete Convergence for Eta in Global Search

The global trace plots (Figure 8) show that eta does not clearly converge to a consistent value — multiple trajectories remain spread across a wide range. The authors acknowledge this ("eta seems to have more variability") for the local search, and Figure 8 shows similar patterns globally. The pairs plot (Figure 9) shows that b1 and eta are correlated. This is suggestive of a likelihood ridge (weak identifiability), which should be quantified via a profile likelihood for eta rather than left as an informal observation. [531-conventions.md, POMP: iterated filtering diagnostics; SKILL_pomp.md checklist item 5]

---

### 11. Global Search Box May Be Too Wide for b1 and b2

The global search box sets `b1 = c(0, 5)` and `b2 = c(0, 5)`. Since Beta = exp(b1 + b2 * cos(...)), with b1=5 and b2=5 the transmission rate peaks at exp(10) ≈ 22026 per week, which is epidemiologically unreasonable for a human disease. Starting a fraction of replicates from such extreme values may explain the "cliff-like" shape of likelihoods seen in Figure 8 and reduces search efficiency in the plausible region. Tightening the box based on the local search results (as the profiling box-construction step attempts for the profile) would have been more efficient for the global search as well. [SKILL_pomp.md checklist item 6]

---

### 12. Profile Construction Has Only 15 Replicates Per Rho Value (nprof = 15)

The profile uses `nprof = 15` guesses per rho value with 30 rho grid points, yielding 450 total mif2 runs. While this is within run_level=2 norms, the scatter in the profile plot (Figure 12) is noticeable. More critically, each profile point undergoes only two sequential mif2 calls — the second inheriting Nmif from the first (100 iterations) plus 40 more. Given the apparent ridges and poor mixing seen in the global search, the profile may not fully maximize over nuisance parameters at each rho value, producing a profile that is too narrow (CI too wide or too narrow depending on direction of bias). [531-weakness-reference.md Error 1.2; SKILL_pomp.md checklist item 5]

---

### 13. Initial Conditions for E and I Are Hard-Coded, Not Estimated

The `seir_init` snippet hard-codes `E = 20` and `I = 10` as fixed starting values regardless of the fitted parameter vector. Only the susceptible fraction eta is estimated. The choice of E=20 and I=10 at week 0 (September 1971) is not biologically justified nor checked for sensitivity. If the epidemic is near its trough in September 1971, these values may be far from the true initial conditions and could distort parameter estimates, particularly for the early-wave dynamics. [SKILL_pomp.md checklist item 13; 531-conventions.md: "Initial conditions can be treated as fixed or as estimated parameters — both are acceptable"]

---

### 14. Only One Parameter Profile Presented Despite CI Claims

The text offers confidence intervals only for rho. Given the biological relevance of the incubation and infectious period rates (which are fixed) and the seasonality parameters b1, b2, and Phi (which are estimated but not profiled), the report provides an incomplete picture of parameter uncertainty. At minimum, a profile for eta (which shows the most variability and a known collinearity with b1) would help validate the identifiability claims implicit in the global search discussion. [SKILL_pomp.md checklist item 5]

---

### 15. No ARIMA/Classical Time Series Analysis

The report goes directly from EDA to the SEIR POMP model without any classical time series analysis. While POMP-only projects are acceptable, examining the autocorrelation structure (ACF/PACF) or fitting a simple ARIMA or SARIMA model to the log-transformed counts would have provided a useful reference point for the data's temporal structure, aided in justifying the seasonal period of 52 weeks, and served as the benchmark required for POMP model validation. [531-conventions.md: "Benchmark comparison is encouraged but not required"; SKILL_pomp.md checklist item 2]

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project14/mumps.R`
