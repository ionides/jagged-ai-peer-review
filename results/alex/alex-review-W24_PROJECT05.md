# Peer Review: W24 Project 05 — Modeling Flu Cases in Oklahoma

## Summary

This project applies time series methods to weekly influenza case counts in Oklahoma (2011–2015), sourced from the CDC FluView dashboard. The analysis proceeds from EDA and decomposition, through ARMA/SARIMA baseline models, to a SEIRS POMP model with sinusoidal forcing. The project is well-organized and demonstrates genuine effort in iterating through six rounds of global search. However, several methodological and technical issues undermine the reliability of the results and the interpretability of the conclusions.

---

## Weaknesses (most critical first)

### 1. [Major] Log-likelihood comparison between SARIMA and POMP is invalid

The central conclusion — that SARIMA outperforms the SEIRS POMP model because "the log-likelihood for the POMP model was much higher [in absolute value]" — rests on a direct numerical comparison of log-likelihoods from two incompatible models. The SARIMA log-likelihood is computed on the differenced, seasonally-differenced series and refers to a Gaussian likelihood on transformed data. The POMP log-likelihood is a particle-filter estimate of the marginal likelihood for the observed count data under a negative-binomial measurement model. These quantities are not on the same scale and cannot be compared as stated. The conclusion drawn from this comparison is therefore unfounded.

### 2. [Major] H accumulator is never reset between observation times

The `seirs_step` C-snippet increments `H` continuously (`H += dN_IR`) and the initial condition sets `H = 0`, but there is no reset of `H` at each observation time. In a standard pomp accumulator workflow the variable declared in `accumvars` is automatically zeroed at each observation time. The code does declare `H` in `accumvars = "H"`, so the reset should occur automatically. However, the `dmeasure` uses `H` directly as the expected count over the entire week, and `delta.t = 1/7` (one day). With 7 sub-steps per week, `H` accumulates recoveries over the week before being reset — this is correct only if the automatic reset is functioning properly. The project never verifies or discusses this, and the initial constant-Beta version of the model (lines 315–325 of blinded.Rmd) omits `accumvars` entirely in its first pomp construction (lines 344–356), which would cause `H` to grow without bound and invalidate that initial diagnostic.

### 3. [Major] SARIMA is fitted with period=12 instead of period=52

In the SARIMA grid-search function `get_aic_table_sarma` (lines 232–243), the seasonal period is hardcoded as `period=12` (monthly) rather than `period=52` (weekly), even though the data are weekly and the periodogram clearly identified a dominant cycle of 50 weeks. The final chosen model `sarima011` is then correctly refitted with `period=52` (line 254), but the AIC table used to select the seasonal orders (P, Q) was produced with the wrong period. The model selected from the misspecified table may not be the optimal weekly SARIMA specification.

### 4. [Major] No profile likelihoods; "poor man's profiles" cannot support inference

The project acknowledges it was unable to compute proper profile likelihoods. The poor man's profiles constructed from the pooled global search results are not a substitute: they aggregate points from six searches with very different bounding boxes and cooling schedules, and the profile is taken over a single parameter while all others vary freely. The resulting scatter cannot identify confidence intervals or assess parameter identifiability. In particular, mu_EI, mu_IR, and mu_RS show essentially flat profiles in the reported plots, suggesting these parameters are not well identified, yet no uncertainty is reported.

### 5. [Major] Sinusoidal forcing is imported from ChatGPT without epidemiological justification

The decision to introduce a sinusoidal forcing function for Beta is attributed entirely to a ChatGPT suggestion (line 391). No epidemiological literature or course material is cited to support this modeling choice. The functional form `Beta0 * (1 + amp * sin(2*pi*(t + phase)/52))` constrains `amp` to lie in (0,1) (via logit transformation), which prevents the possibility of a negative effective beta, but the biological interpretation of the amplitude and phase parameters is never discussed, nor is the choice of a sine versus cosine justified.

### 6. [Major] Estimated epidemiological parameters are not interpreted or validated

The final converged parameters (visible in seirs_lik.csv: mu_EI ≈ 0.55, mu_IR ≈ 1.1, mu_RS ≈ 0.07) imply a mean latent period of roughly 1.8 days, a mean infectious period of roughly 0.9 days, and a mean immunity period of roughly 14 days. These values are biologically implausible for influenza (typical latent period 1–4 days, infectious period 3–7 days, immunity lasting months to years). The authors do not discuss whether these estimates make epidemiological sense, which is a critical omission for a mechanistic model.

### 7. [Major] Arbitrary truncation of dataset without systematic justification

The dataset is trimmed to 2011–2015 (210 weeks) primarily because "the Great Lakes cluster was running slow" (line 63). Excluding the COVID-19 period is reasonable, but restricting to just 4 years rather than, e.g., 2011–2019 is not supported by any statistical or epidemiological argument. This choice limits the identifiability of the waning-immunity parameter mu_RS, which governs multi-year reinfection dynamics — a key feature of the SEIRS structure.

### 8. [Moderate] Initial state parameters fixed after local search without diagnostic support

After the local search, S0, E0, I0, R0, and k are fixed at locally-converged values for all six global searches (line 564). The justification given is that "they converged quickly," but the local search only ran 20 chains from a single starting point. Fixing these parameters without a formal sensitivity analysis or profile likelihood risks propagating a local artifact into all subsequent estimation.

### 9. [Moderate] ARMA grid search applied to the full seasonal time series (flu_ts) rather than the truncated subset (ok_flu)

The ARMA and SARIMA grid searches use `flu_ts <- ts(ok_flu$cases, ...)`, which is derived from `ok_flu` (the 2011–2015 subset). This is consistent. However, the full 2010–2024 dataset `flu` is read and displayed in the first plot, and the truncation is only applied afterwards. The ARMA section uses `flu_ts` (the truncated version) correctly, but the initial overview plot is unlabeled with respect to which rows correspond to which years, making reproducibility difficult.

### 10. [Moderate] Measurement model mismatch: dmeas uses H directly, but H is the cumulative weekly count

The measurement model is `dnbinom_mu(cases, k, rho * H, give_log)`. With `delta.t = 1/7` and 7 steps per week, `H` accumulates new recoveries (dN_IR) over the week. This is consistent with treating the weekly reported case count as a fraction `rho` of weekly recoveries. However, the paper never establishes that cases are defined as recoveries rather than new infections (dN_SE or dN_EI). Epidemiologically, reported ILI cases typically correspond to new symptomatic onsets (transitions out of E into I), not recoveries. Using dN_IR as the basis for observed cases introduces a systematic delay and potentially a different magnitude in the measurement model.

### 11. [Moderate] rw.sd values are uniform and small; no discussion of scale-appropriate perturbations

The random-walk standard deviations in `mif2` are set uniformly at 0.01 for all parameters on the transformed scale (line 90–94 of local R script). This ignores the very different scales and sensitivities of Beta0 (~2), phase (~-3 to 0), mu_IR (~1), and rho (~0.001). Small and uniform perturbations are unlikely to adequately explore the parameter space and may contribute to premature convergence.

### 12. [Moderate] "Poor man's profile" filtering inconsistency

For the poor man's profiles of mu_EI, mu_IR, and mu_RS (lines 946, 961, 980), the data are filtered to `mu_EI <= 1`, `mu_IR <= 10`, and `mu_RS <= 1` respectively, but no such filtering is applied when the final best parameters are selected from `params_new` in earlier global search tabs. This means the best-fit parameters used in the final simulation may come from regions of parameter space that are later excluded from the profiles, creating an internal inconsistency.

### 13. [Moderate] SARIMA seasonal period in the AIC table grid search uses B_{12} notation but period=12 in code

In the writeup (line 228), the SARIMA model is displayed with seasonal subscript $[52]$ implying weekly seasonality, yet the code passes `period=12`. This discrepancy between notation and code is confusing to readers and indicates the displayed AIC table does not correspond to the model described.

### 14. [Minor] The `eta` parameter appears in the initial parameter vector but is absent from the model

In the first (constant-Beta) SEIRS construction, `eta` is listed in `paramnames` (line 354) and set in the params vector (line 384), but it is never referenced in `seirs_step`, `seirs_rinit`, `seirs_dmeas`, or `seirs_rmeas`. The parameter is silently carried along without effect. This unused parameter is not explained.

### 15. [Minor] Reproducibility: `registerDoRNG(237835)` is set globally but the RNG state is not controlled per run-level

The RNG seed is set once (line 29 of Rmd, line 9 of each R script) but `bake()` with saved RDS files is only used in the local search scripts. The global search results are read from pre-saved CSV files, which means the reported likelihoods are not reproducible from the Rmd alone without re-running the Great Lakes scripts. The run_level variable in the Rmd is set to 3 (line 495), but the scripts use run_level 4 and 3 respectively — the connection between what was run on the cluster and what is displayed is not made explicit.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/great-lakes-seirs-global.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/great-lakes-seirs-local.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/ok-flu.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik_1.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik_6.csv`
