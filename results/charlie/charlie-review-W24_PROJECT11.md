# Peer Review: W24 Project 11
**Manuscript:** Stats 531 Final Project — NVIDIA Stock Price Analysis Using ARMA, GARCH, and POMP Models

---

## Summary

This project applies ARMA, GARCH, and POMP stochastic-volatility models to NVIDIA daily log-returns from January 2022 to April 2024. The authors perform exploratory data analysis, select an ARMA(0,0) model, fit several GARCH variants, and implement the leverage-effect stochastic volatility POMP model from Breto (2014) via iterated filtering (IF2). While the project is reasonably structured and covers multiple modeling frameworks, it suffers from critical methodological shortcomings in the POMP section: there is no benchmark comparison, parameter convergence is incomplete, the global search is improperly seeded from a single local-search replicate, profile likelihoods are absent, and the reported likelihoods are internally inconsistent. The code also embeds a hard-coded absolute path that prevents reproduction on any other machine.

---

## Major Issues

### 1. No non-mechanistic benchmark comparison (Wheeler et al. 2024, §Benchmark comparison)

The mechanistic stochastic-volatility POMP model is never compared against the GARCH model on a common, apples-to-apples basis. The Conclusion states that the POMP model achieves a log-likelihood of 1110 versus 1120 for ARMA(0,0)-GARCH(1,1)-t, and 1092 for ARMA(0,0). However, these numbers are not directly comparable: the ARMA/GARCH likelihoods are computed by `fGarch::garchFit` on the full series, while the POMP likelihood is evaluated via particle-filter log-mean-exp averaging on the same returns. No effort is made to verify that the observation models and data conditioning are identical across all three model families, so the cross-model comparison is invalid. Wheeler et al. (2024) emphasize that benchmark comparisons must be quantitatively rigorous and computed on the same observation model; the authors fail this standard.

### 2. Inconsistent log-likelihood figures across sections

The Conclusion states "ARMA(0, 0) give us the likelihood of 1092," yet the ARMA Model Selection section reports "the log-likelihood of the ARMA(0, 0) model, which is approximately 1087." The GARCH section describes a GARCH(1,1) with "likelihood of about 1596" but this model is then discarded; the ARMA(0,0)+GARCH(1,1)+normal model yields 1092, and the t-error variant yields 1120. These figures are scattered, contradictory, and never reconciled in a single comparison table. The absence of a clean, consolidated model-comparison table with AIC or log-likelihood on comparable scales makes it impossible for the reader to assess relative model performance.

### 3. Global search initialized from a single local-search replicate (Wheeler et al. 2024, §Computational adequacy)

The global search code is:
```r
if.box <- foreach(i=1:nv_Nreps_global,
  .packages='pomp',.combine=c) %dopar% mif2(if1[[1]],
    params=apply(nv_box,1,function(x)runif(1,x)))
```
Every global-search chain starts from `if1[[1]]` — the first of 15 local-search IF2 objects — rather than from a freshly constructed `pomp` object or from diverse replicates. This means all 80 global chains inherit the filter state (and potentially particle history) of a single local run, biasing the exploration of the parameter space and defeating the purpose of a box-based global search. The correct practice is to pass the base `nv.filt` object with `params = apply(nv_box, 1, function(x) runif(1, x))` so each chain starts from an independent draw from the box. See Wheeler et al. (2024) SI for the standard global-search template.

### 4. Incomplete convergence of key parameters (Wheeler et al. 2024, §Computational adequacy)

The authors acknowledge that `mu_h` and `H_0` do not converge in the local search, and describe mixed convergence in the global search ("some other parameters may not exhibit clear convergence"). Despite this, no additional iterations are attempted and the non-converged estimates are used as the final result. The log-likelihood traces shown by `plot(if1)` and `plot(if.box)` are not described or discussed in detail. Without evidence of convergence for all parameters, the reported MLE of 1111 (local) or its global counterpart cannot be trusted as near the true maximum. This is a validity-threatening deficiency as noted by Wheeler et al. (2024): "Reported likelihoods may not be near the MLE, undermining all downstream conclusions."

### 5. No profile likelihoods reported (Wheeler et al. 2024, §Parameter identifiability)

The project does not compute profile likelihoods for any parameter. Given that the authors themselves note non-convergence for `mu_h` and `H_0`, and that the POMP stochastic-volatility model is known to have near-flat likelihood surfaces in some directions, profile likelihoods are essential to assess identifiability. Without them, it is unknown whether any of the six parameters are well-identified by the NVIDIA return series. No confidence intervals are reported for any parameter estimate.

### 6. Hard-coded absolute path prevents reproducibility

Line 45 of the Rmd contains:
```r
setwd("/Users/huanglingqi/Desktop/Stats 531 Final Project")
data <- read.csv("NVDA.csv")
```
The data file `NVDA.csv` is not included in the project folder, and the absolute path is specific to the author's local machine. This means the code is not reproducible on any other system. According to the code-supplement checklist, relative paths must be used and all necessary data files must be included. The absence of `NVDA.csv` makes the entire analysis unreproducible from source.

### 7. Misidentification of ADF test conclusion (stationarity test interpretation error)

The ARMA section states: "the p-value is less than 0.01, which suggest we keep the null hypothesis that our time series is stationary." This is precisely backwards. The ADF null hypothesis is that a unit root is present (non-stationarity); a p-value < 0.01 means we *reject* the null hypothesis and conclude the series is stationary, not that we "keep" it. While the substantive conclusion (the series is stationary) is correct, the logical description of the test is wrong and misleading. This error persists in the writeup as-is.

### 8. Ljung-Box test misinterpretation leads to incorrect modeling motivation

The authors use the Ljung-Box test (p = 0.325) to conclude that log-returns are independently distributed, and then proceed to fit ARMA, GARCH, and POMP models. However, the Ljung-Box test tests for autocorrelation in the mean; it is well known that financial returns can have negligible autocorrelation in levels but strong autocorrelation in squared returns (ARCH effects). The fact that the authors did not test for ARCH effects (e.g., McLeod-Li test or Ljung-Box on squared residuals) before motivating the GARCH model means the transition from ARMA to GARCH is poorly supported. The ARMA(0,0)+GARCH(1,1) model is introduced without first demonstrating the presence of conditional heteroskedasticity in the residuals.

### 9. GARCH(1,1) discarded on incorrect grounds

The authors discard a stand-alone GARCH(1,1) because "the coefficients of fitted model are not statistically significant." However, the standard GARCH model is not fit to log-returns directly in the conventional sense — the `garch()` function from the `tseries` package may differ from `garchFit()` from `fGarch`. Moreover, coefficient p-values for GARCH models are asymptotic and can be unreliable in small samples; the appropriate selection criterion is AIC or likelihood-ratio test, not individual t-tests. The authors then accept ARMA(0,0)+GARCH(1,1) from `fGarch` in the very next subsection without reconciling why the same GARCH structure becomes acceptable. This inconsistency is unexplained.

---

## Minor Issues

### 10. POMP model log-likelihood is lower than ARMA-GARCH but this is not adequately explained

The authors simply note that the POMP model's likelihood (1110-1111) is lower than ARMA(0,0)-GARCH(1,1)-t (1120) and accept the ARMA-GARCH as best. However, the stochastic volatility POMP model has more parameters and should in principle have a higher achievable log-likelihood. The fact that it does not may reflect insufficient optimization (issues 3 and 4 above) rather than a genuine model deficiency. This possibility is not discussed.

### 11. The `timing.box` variable contains a bug

The global search code has `timing.box <- .system.time["elapsed"]` (with a leading dot), whereas the local search uses `start_time <- system.time({...})`. The object `.system.time` is non-standard and will produce `NA` or an error in a fresh R session. This is a coding error that would prevent clean reproduction.

### 12. Particle filter evaluation uses simulated data, not observed data

The initial particle filter evaluation:
```r
pf1 <- foreach(i=1:nv_Nreps_eval, ...) %dopar% pfilter(sim1.filt, Np=nv_Np)
```
runs the filter on `sim1.filt`, which is a POMP object built from *simulated* data, not from the actual NVIDIA returns. The subsequent IF2 searches use `nv.filt` (real data). This evaluation step is therefore not measuring the model's fit to the observed data and is misleading; it also means the early reported particle filter diagnostics are not directly relevant to the actual estimation problem.

### 13. No effective sample size (ESS) diagnostics reported (simulation-study checklist, §10)

Particle filter ESS is never monitored or reported. For a 550-observation financial time series with 1500 particles at run level 3, ESS collapse is a genuine risk, especially given the heavy-tailed nature of NVIDIA returns. The simulation-study checklist requires ESS monitoring to confirm that the particle filter is not silently degenerating.

### 14. Missing `pomp` package version and `sessionInfo()`

No `sessionInfo()` output is provided, and the `pomp` package version is not recorded. The `pomp` API has changed substantially across versions. Without version pinning or an `renv` lockfile, the stochastic-volatility model code (which uses `covariate_table`, `Csnippet`, `parameter_trans`, `mif2`) may behave differently on current CRAN releases.

### 15. Notation inconsistency in POMP model definition

The model writeup defines $\beta_n = Y_n \sigma_\eta \sqrt{1 - \phi^2}$ and $\omega_n \sim N(0, \sigma^2_{\omega,n})$ with $\sigma^2_{\omega,n} = \sigma^2_\eta(1-\phi^2)(1-R_n^2)$, yet the `rproc1` C snippet computes `omega = rnorm(0, sigma_eta * sqrt(1-phi*phi) * sqrt(1-tanh(G)*tanh(G)))`. Squaring this standard deviation gives $\sigma^2_{\omega,n} = \sigma^2_\eta(1-\phi^2)(1-\tanh^2(G_n))$, which matches the text only if $R_n = \tanh(G_n)$. This substitution is implicit and not stated in the text, making the code harder to verify. The relationship $R_n = \tanh(G_n)$ (rather than the written $R_n = (\exp(2G_n)-1)/(\exp(2G_n)+1)$, which equals $\tanh(G_n)$) should be stated explicitly to confirm consistency.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project11/Stats 531 Final Project.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project11/Makefile`
