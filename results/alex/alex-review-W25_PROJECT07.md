# Peer Review: W25 Project 07 — Dengue Fever in the U.S. States and Territories (2022–2023)

---

## Summary

This project fits SARIMA, SIRS, and SEIR models to weekly travel-associated dengue case counts in the U.S. (2022–2023) from the `denguedatahub` package. The project is well-structured and shows reasonable effort in model construction, but several critical methodological flaws undermine the validity of the compartmental models and make the conclusions unreliable.

---

## Weaknesses (Most Critical First)

### 1. [MAJOR] Fundamental Mechanistic Mismatch: SIR-type Models Applied to Imported Case Data

The data consist entirely of **travel-associated (imported) dengue cases**, not domestically transmitted ones. The authors filter with `Travel.status == "All"` (line 46) and explicitly state "imported infections remain persistent due to global travel." SIR/SIRS/SEIR models assume local transmission dynamics — S, I, R compartments interact via a force-of-infection term $\beta I/N$. For imported cases, there is no such local chain of transmission; cases are independent arrivals driven by travel volume and endemic conditions abroad. Applying a compartmental transmission model to imported case counts produces parameters (transmission rate $\beta$, recovery rate $\mu_{IR}$) that have no epidemiological meaning in this context. This is the most fundamental conceptual error in the project, and it invalidates the biological interpretation of all POMP model results.

### 2. [MAJOR] Inconsistent Data Preparation Across the Three Models

Three different data objects are created, each using a different filtering approach, which means the models may not all be fit to the same dataset:

- **SARIMA**: `dengue <- cdc_casesby_week %>% filter(Travel.status == "All", Year %in% c(2022, 2023))` (line 46) — correctly filters to "All" travel status and years 2022–2023.
- **SIRS**: `df <- cdc_casesby_week %>% filter(Year >= max(Year) - 1)` (line 325–327) — no `Travel.status` filter and uses a relative year filter. If the dataset has multiple travel status categories, this may include locally transmitted cases in addition to travel-associated ones, and may include records from years other than 2022–2023 if the data structure is non-standard.
- **SEIR**: `data <- cdc_casesby_week; data <- data[637:nrow(data), ]` (lines 776–777) — uses a hardcoded row index of 637 with no filter on `Travel.status` or `Year`. This is fragile, undocumented, and almost certainly does not match the 106-week 2022–2023 subset. The number of rows selected is not verified to correspond to the intended data range.

Because the three models are fit to potentially different data, the log-likelihood comparisons in the conclusion are invalid.

### 3. [MAJOR] No Profile Likelihood or Confidence Intervals — No Uncertainty Quantification

Despite defining `Npoints_profile` and `Nreps_profile` in the run-level settings (lines 345–346, 934–935), neither model computes a profile likelihood or provides confidence intervals for any parameter. This means there is no assessment of parameter uncertainty, identifiability, or whether estimated values are significantly different from biologically plausible ranges. The standard approach in POMP analyses is to produce profile likelihood plots and construct at least approximate 95% confidence intervals via the $\chi^2$ cutoff rule. The absence of this step is a major omission.

### 4. [MAJOR] Poorly Motivated "Pandemic Switch" at Week 29 in SIRS Model

The SIRS step function introduces a hard threshold at `pandemic__week = 29` (line 366), switching the baseline transmission rate from `a` to `b` after week 29. This is described as a "pandemic switch" (lines 305, 366, 668), but week 29 in a 2022–2023 time series corresponds to approximately mid-July 2022, which is not a recognizable epidemiological or policy boundary. The data cover 2022–2023, well after the acute COVID-19 pandemic period. The choice of week 29 appears to be driven purely by empirical fitting of the peak pattern (the authors acknowledge "we noticed that the second peak after week 29 is larger than the first peak"), not by any external event or biological process. This ad hoc feature is unexplained, undermines the interpretability of parameters `a` and `b`, and is absent from the SEIR model with no discussion of why it was dropped.

### 5. [MAJOR] Implausible Population Size N = 4e9 in SIRS Initial Parameters, with Inconsistency Across Models

The SIRS model is initialized with `N = 4e9` (4 billion people, line 428–431), then the global search fixes `N = 3.25e8` (325 million, the approximate US population, line 600). The SEIR model uses `N = 3200000` (3.2 million, line 856, 944, 1076), which is not explained — it is roughly the population of a single U.S. state. These three values span three orders of magnitude and are never reconciled or justified. Since `rho * H` in the measurement model scales with `N` through the dynamics, the reporting rate `rho` and the fitted case counts are deeply entangled with this choice. No sensitivity analysis is provided.

### 6. [MAJOR] H Accumulates Recoveries, Not New Infections — Mislabeled as "Cumulative Incidence"

In both the SIRS and SEIR models, `H += dN_IR` (lines 378, 801), meaning H accumulates individuals transitioning from I to R (recoveries). The comment on line 801 explicitly but incorrectly labels this as "Cumulative incidence (used for measurement)." Incidence refers to new infections (the S→I or S→E transition), not recoveries. While for simple SIR models the two flows are equal in expectation over long intervals, they differ within a time step and at the start of outbreaks. The measurement model `dnbinom_mu(reports, k, rho*H, ...)` then links reported cases to cumulative recoveries rather than cumulative new infections. This is a subtle but incorrect measurement equation that may cause bias, and the code comment is misleading.

### 7. [MAJOR] SEIR Global Search Claims 200 Starting Points but Only 100 Are Specified

The text states "using 200 random initial parameter sets" (line 1065), but `Nglobal` at run level 3 is set to 100 (line 933: `Nglobal <- switch(run_level, 2, 5, 100)`), and `nseq = Nglobal` (line 1081). This is a direct factual inconsistency between the text and the code. Additionally, the SIRS global search has `Nglobal = 20` at run level 3 (line 342), which is a sparse coverage of a 7-dimensional parameter space.

### 8. [MAJOR] SEIR Local Search Uses Number of CPU Cores Rather Than Nlocal

The SEIR local search runs `foreach(i=seq_len(ncpu), ...)` (lines 945–947), where `ncpu = nbrOfWorkers()`, rather than using the pre-defined `Nlocal = 20` (line 932). On a machine with fewer cores (e.g., 4 or 8), this results in far fewer MIF2 runs than intended and than the SIRS local search (which explicitly uses 20 runs, line 486). The number of local search starts is not reported in the writeup, preventing reproducibility assessment.

### 9. [MINOR] SIRS Recovery Rate mu_IR = 0.8 Implies Unrealistically Short Infectious Period for Dengue

The initial SIRS parameter `mu_IR = 0.8` per week (line 428) corresponds to a mean infectious period of 1.25 weeks (~9 days). While dengue infectious duration is broadly cited as 4–10 days (consistent with this estimate), the recovery rate estimated after global search converges to values in the range of 2–10 per week (line 605 upper bound). A recovery rate of 10/week implies a mean infectious period of only 0.7 days, which is biologically implausible. The final estimated parameters are not discussed in terms of biological plausibility, and this upper bound of the search box is not justified.

### 10. [MINOR] No ACF of SARIMA Residuals — Incomplete Residual Diagnostics

The residual analysis for the SARIMA model includes a time series plot, histogram, and Q-Q plot (lines 219–225), but does not include a residual ACF plot or a formal test such as the Ljung-Box test. Without a residual ACF, the claim that residuals "show no strong autocorrelation" (line 229) is unsubstantiated. The presence of remaining autocorrelation would indicate model inadequacy that cannot be detected from visual inspection of the residual time series alone.

### 11. [MINOR] SARIMA Period Set to 53 Weeks Despite Seasonal Forcing Period of 52 Weeks in POMP Models

The SARIMA model uses period = 53 (lines 102, 126, 147, 196) based on the observation that the dataset has 53 weeks per year, which is correct for the ARMA model. However, both POMP models use a hard-coded period of 52 (line 369: `/52`, line 787: `double period = 52`), creating an inconsistency in how annual seasonality is defined across the three models. The SEIR model documentation also states $T = 52$ (line 755). This discrepancy is not discussed or justified.

### 12. [MINOR] No ODE Formulation or R0 Derivation for the SEIR Model

The SIRS model receives a detailed deterministic ODE analysis including disease-free equilibrium, basic reproduction number $R_0 = \beta/\gamma$, and endemic equilibrium (lines 264–300). The SEIR model section (lines 719–772) provides only the stochastic transition equations and does not derive the corresponding $R_0$, DFE, or endemic equilibrium. This asymmetry in mathematical rigor across the two models makes the comparative analysis structurally uneven.

### 13. [MINOR] SIRS Global Search Loglik Not Explicitly Reported

The SIRS global search section (lines 629–703) prints the best parameter vector but never explicitly states the maximum log-likelihood value achieved. In contrast, the SEIR global search reports `-446.79` explicitly. The conclusion mentions the SIRS achieved `-440` (line 1187), but this corresponds to the local search description in the trace plot text (line 517), not a formal post-optimization particle filter evaluation. The distinction between local and global search results for SIRS is unclear.

### 14. [MINOR] k (Overdispersion) Fixed in SEIR but Estimated in SIRS Creates Non-Comparable Models

The SEIR model fixes `k = 10` throughout (lines 856, 944, 1076: `fixed_params <- coef(measSEIR, c("N","k"))`), while the SIRS model estimates k and reports convergence to values of 7–11 (line 517). Since k controls the dispersion of the negative-binomial observation model, fixing it arbitrarily at 10 rather than estimating it may inflate the SEIR log-likelihood or produce overconfident fits. More importantly, comparing log-likelihoods between models with different numbers of free parameters without penalty (e.g., AIC) is not valid.

### 15. [MINOR] ACF Interpretation Error — Oscillating Pattern Does Not Indicate Non-Stationarity Per Se

The text states "The oscillating pattern displayed in the plots supports that the data is non-stationary" (line 79). This is not quite correct: an oscillating ACF that decays to zero is consistent with a stationary seasonal ARMA process (as the authors themselves acknowledge on line 80–81 when they discuss the damped oscillations). Non-stationarity would manifest as an ACF that does not decay. The text makes a contradictory claim by later asserting the data is consistent with a stationary SARIMA process. The seasonal differencing order D = 0 in the chosen model is also consistent with stationarity.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project07/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project07/blinded.html`
