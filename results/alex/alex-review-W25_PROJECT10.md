# Peer Review: Daily Environmental Noise and Heart-Rate Variability
**Semester:** W25 | **Project:** 10 | **Reviewer:** Alex

---

## Summary

This project investigates how daily environmental noise (Leq, dB(A)) affects heart-rate variability (SDNN, ms) using a pooled population-level daily time series spanning November 2019 to December 2024 (n = 1,875 days). A linear-Gaussian POMP (LG-POMP) model is specified with a single latent AR(1) state driven by noise and physical activity covariates, estimated via iterated filtering (MIF2). Benchmarks include an ARIMA(5,1,6) model and an OLS regression. The POMP model underperforms both benchmarks in log-likelihood terms, and the paper concludes that the current specification is exploratory.

---

## Weaknesses (Most Critical First)

### 1. [Major] POMP log-likelihood is worse than both benchmarks, yet no model revision is attempted

The maximized POMP log-likelihood from the local search is -3,235, compared to -2,591 for ARIMA(5,1,6) and -3,026 for OLS. The paper acknowledges this gap but defers all remediation to future work. A project that sets up a POMP model should iterate toward a competitive specification rather than stop at a demonstrably inferior fit. No alternative POMP formulations (e.g., AR(2) state, non-Gaussian measurement, log-normal observation) are actually tried, only mentioned as possibilities in the conclusion.

### 2. [Major] Global search produces a worse result than local search, with no adequate diagnosis

The global search returns a maximum log-likelihood of -7,936, whereas the local search reached -3,235. The discrepancy is enormous (roughly 4,700 log-likelihood units) and is glossed over with the observation that "150 MIF iterations and a relatively small particle count" may be the cause. No corrective run is performed. The global search result is therefore uninformative as a convergence diagnostic: it cannot confirm that the local search found a true optimum rather than a local mode. This is the most critical methodological gap.

### 3. [Major] Local search MIF2 traces show persistent non-convergence

Figure 4 shows that the log-likelihood rises steeply in the first ten iterations and then drifts downward, and parameters a, c, d, sigma_proc, and sigma_obs do not plateau. The paper acknowledges this but does not address it by, e.g., reducing the random-walk standard deviation, increasing Np, or running more iterations. Reporting results from a run that has demonstrably not converged undermines the validity of all downstream estimates.

### 4. [Major] Likelihood comparison across models is not on the same basis

The ARIMA log-likelihood (-2,591) is computed on the first-differenced series, while the POMP and OLS log-likelihoods are computed on the undifferenced series. These quantities are on different scales and cannot be directly compared with AIC or any information criterion. No Jacobian correction for the differencing transformation is applied, making the benchmark comparison invalid.

### 5. [Major] Pooling individual-level data into a single population-level series destroys the panel structure

Individual participants contribute measurements on different days with substantial missingness. By collapsing to daily population medians/means, the project eliminates between-subject heterogeneity and treats the result as if it were a single individual's time series. The POMP model has no mechanism to represent aggregation noise or varying panel composition over time. The long-run downward trend in SDNN visible in Figure 1 is most plausibly an artifact of changing participant enrollment (drop-outs, additions) rather than a genuine physiological decline, yet no panel-composition covariate or structural break is included.

### 6. [Major] Initial state X_0 is treated as a free parameter but fixed to 34 in the global search

In the local search X_0 is estimated (converging to 33-35 ms), but in the global search `fixed_params = c(X_0=34)` pins it at 34 while only the remaining six parameters are randomized. This asymmetry means the global search explores a lower-dimensional space than the local search, which partly explains but does not justify the large discrepancy in achieved log-likelihood. The decision is not explained or discussed.

### 7. [Major] No profile likelihood or confidence intervals are reported for any parameter

The paper reports a point estimate of b ≈ -0.30 as the key scientific result (noise coefficient), but provides no uncertainty quantification. For an LG-POMP with documented convergence difficulties, a profile likelihood over b is essential to assess whether the estimated effect is distinguishable from zero and whether the parameter is genuinely identified. This omission makes the central scientific claim unverifiable.

### 8. [Major] ARIMA model is selected on the differenced series but POMP is applied to the undifferenced series

The decision to difference is motivated by visual inspection of a trend. The POMP model addresses trend only through the AR(1) drift parameter a and intercept d, with no explicit trend component. If the observed downward trend is a unit root or slow drift, a stable AR(1) POMP will not capture it faithfully. The model specification and the ARIMA pre-processing step are therefore incompatible in their treatment of non-stationarity.

### 9. [Minor] Particle count in the global search (Np = 2,000) is materially lower than in the local search (Np = 5,000)

The global search uses Np = 2,000 particles and only 150 MIF iterations, while the local search uses Np = 5,000 and 300 iterations. The reduced settings are not justified and reduce the reliability of the global likelihood surface enough that the global result is effectively uninformative. The paper partially acknowledges this but does not report sensitivity to Np or Nmif.

### 10. [Minor] AIC table for ARIMA is computed on the differenced series with d hard-coded as 0

The `aic_table` function calls `arima(data, order=c(p,0,q))` on the pre-differenced object `d_sdnn_ts`, so it fits ARMA(p,q) models to the differenced series and labels the best model as ARIMA(5,1,6). The AIC values are therefore for the ARMA specification on the differenced series, not for ARIMA on the original series. While this is internally consistent, it is not stated clearly and may confuse readers.

### 11. [Minor] The OLS log-likelihood is back-computed from AIC rather than extracted directly

The code computes `logLik_lm <- -0.5*(aic_lm - 2*k)` rather than calling `logLik(hrv_lm)` directly. The formula is correct but unusual and introduces a potential off-by-one error if the definition of k (number of parameters) differs from what `AIC()` uses internally. The difference here is small but the approach is unnecessarily indirect.

### 12. [Minor] No simulation-based predictive check is performed

Figure 3 overlays three simulated trajectories on the data using the initial guess parameters. No analogous simulation from the MIF2-estimated parameters is shown, so it is impossible to assess whether the fitted model generates plausible HRV trajectories. A posterior predictive check or simulated envelope plot at the estimated parameter values is standard practice for POMP models.

### 13. [Minor] The data availability statement notes results were obtained in a proprietary VDI and cannot be reproduced externally

The entire analysis relies on data owned by Apple Inc. that cannot be shared, and the rendered HTML cannot be exported. This means the submitted PDF contains annotated screenshots rather than actual output, and no independent replication of any numerical result is possible. While the data-use restriction is legitimate, the project should have used a publicly available data set for a course submission, or at minimum ensured the code itself is fully self-contained and runnable on simulated data.

### 14. [Minor] Long-run equilibrium implied by the model is not discussed in terms of the noise effect

For the AR(1) state equation X_t = a X_{t-1} + b N_t + c A_t + d, the long-run mean is (b*N_bar + c*A_bar + d)/(1-a). With b ≈ -0.30 and a ≈ 0.20, a sustained 10 dB increase in mean noise would shift the long-run SDNN by approximately -0.30*10/(1-0.20) = -3.75 ms. This implied long-run effect is never computed or discussed, even though it is the more policy-relevant quantity.

### 15. [Minor] Random-walk standard deviations are uniform across all parameters at 0.01

All parameters use `rw.sd = 0.01` in the local search MIF2 run, without justification. Parameters operating on very different scales (e.g., d ≈ 47 vs. sigma_proc ≈ 0.1) need different perturbation sizes to explore the likelihood surface efficiently. The uniform choice likely contributes to the slow convergence of d and the erratic behavior of sigma_proc visible in Figure 4.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project10/blinded.pdf`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project10/Makefile`
