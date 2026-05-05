# Peer Review: W25 Project 10
## "Daily Environmental Noise and Heart-Rate Variability"

---

## Summary

This project fits a linear-Gaussian partially observed Markov process (LG-POMP) to a pooled daily time series of heart-rate variability (SDNN) spanning November 2019 to December 2024 (n = 1,875 days), with environmental noise level (Leq) and physical activity (Energy) as observed covariates in the latent-state equation. The goal is to quantify the same-day effect of environmental noise on population-level HRV. The project includes an ARIMA(5,1,6) benchmark comparison and a linear regression baseline, and honestly reports that the POMP model fails to beat either benchmark. While the project demonstrates commendable honesty about its own failure and makes a genuine attempt at a two-stage IF2 optimization with convergence traces, the analysis suffers from a series of critical methodological and computational problems that undermine the validity of the reported estimates and prevent any confident scientific conclusion. The global search is fundamentally invalid due to a prior-mif2-result initialization error; the log-likelihood comparisons across models are made on incommensurable objects; parameter convergence is incomplete; no profile likelihoods or confidence intervals are presented; and the underlying data cannot be shared or reproduced. These issues compound to render the main stated findings — including the noise coefficient estimate — unreliable.

---

## Major Issues

### 1. Global Search Initialized from a Previous mif2 Result Object, Invalidating Global Coverage

In the Global Search code chunk, the first mif2 call within the foreach loop takes `mf1 <- mifs_local[[1]]` as its first argument:

```r
mf1 <- mifs_local[[1]]
...
mf1 |> mif2(params=c(guess, fixed_params)) |> mif2(Nmif=150) -> mf
```

This passes a previous IF2 result object (the first local-search chain) as the base object rather than the original `hrv_pomp` pomp object. As a result, every global replicate inherits the internal cooling schedule and IF2 state from `mifs_local[[1]]`, which has already spent 300 iterations converging toward the local solution. With the cooling fraction already near exhaustion, the 96 new starting guesses drawn from the box have very little functional IF2 exploration before perturbations shrink to near zero, effectively anchoring the "global" search near the local solution rather than exploring the full parameter box. (See the `pomp-global-search-init-audit` skill for the exact anti-pattern.) The fix is to replace `mf1` in the `mif2()` call with `hrv_pomp` (the raw pomp object), ensuring each global replicate starts fresh.

This error explains the dramatic discrepancy: the global search reports a best log-likelihood of -7,936 (shown in the HTML output), while the local search achieves -3,235. The authors themselves note the discrepancy and attribute it to insufficient iterations, but the initialization fault is a structural reason the global chains cannot escape the inherited cooling decay.

### 2. Log-likelihood Comparisons Are Made on Incommensurable Objects

The report directly compares:
- ARIMA(5,1,6) log-likelihood: -2,591, fitted to the **first-differenced** SDNN series (1,874 observations)
- Linear regression log-likelihood: -3,025, fitted to the **levels** SDNN series (1,875 observations) with noise and activity covariates
- POMP log-likelihood: -3,235, evaluated on the **levels** SDNN series (1,875 observations)

These likelihoods are not on the same scale. The ARIMA model is fitted to the differenced series, so its likelihood integrates over a different sample space than the POMP likelihood for the level series. A one-unit increase in the ARIMA log-likelihood does not correspond to the same improvement in predictive accuracy relative to the level-series models. The AIC comparison in the Conclusion section ("the POMP's much lower log-likelihood translates into a markedly worse AIC than either benchmark") is therefore invalid as stated: the ARIMA AIC cannot be directly compared to the POMP or regression AIC because the observation vectors differ. A valid benchmark comparison requires either (a) converting all likelihoods to the same scale via the Jacobian of the differencing transformation, or (b) using the ARIMA as a predictive model for the level series and evaluating its predictive likelihood on the same held-out observations as the POMP. See Wheeler et al. (2024), Practice 2: Benchmark comparison.

### 3. No Profile Likelihoods or Confidence Intervals for Any Parameter

No profile likelihoods are computed for any parameter, including the primary scientific quantity of interest — the noise coefficient b. The local-search trace plot (Figure 4) shows that b converges to a band around -0.30, but the width of that band and the true sampling uncertainty of the estimate are unknown without profile likelihoods. The authors report b ≈ -0.30 and interpret it as physiologically meaningful, but this is a point estimate from a non-converged local search (see Issue 4 below). Without profile likelihoods, there is no basis for stating that the noise-HRV relationship is "well identified by the data," as asserted on page 12. The MCAP procedure should be applied at minimum for b. See Wheeler et al. (2024), Practice 5: Parameter identifiability and uncertainty.

### 4. IF2 Optimization Has Not Converged: Log-likelihood Drifts Downward After Peak

The trace plots in Figure 4 clearly show that the log-likelihood peaks near iteration 10 at approximately -2,700 and then drifts downward to approximately -2,900 by iteration 300. The authors correctly identify this as "a hallmark of over-diffuse random-walk perturbations combined with Monte-Carlo noise in the particle filter," but this diagnosis is also a statement that the maximum log-likelihood value of -3,235 reported after the local search is substantially worse than the optimum found mid-run at -2,700. A particle-filter re-evaluation at the best mid-run parameter snapshot — not just the final snapshot — would be needed to recover the true local optimum. As presented, the best log-likelihood of -3,235 from the local search is an artifact of evaluating only the final-iteration parameters rather than the best-visited parameters across all iterations. This is a critical convergence failure. See Wheeler et al. (2024), Practice 6: Computational adequacy.

### 5. Data Cannot Be Shared; Analysis Is Not Reproducible

The underlying data are owned by Apple Inc. under a data-use agreement prohibiting distribution. All analyses were run inside Apple's secure VDI environment; neither the data file (`noise_hrv_531.csv`) nor the fully rendered HTML output can be exported. The report consists of annotated screenshots. This means:
- The code cannot be executed by any reader.
- The numerical results shown in screenshots cannot be verified.
- The intermediate `.rds` bake files (`hrv_local_search.rds`, `hrv_lik_local.rds`, `hrv_global_search.rds`) are not archived anywhere accessible.
- No synthetic or anonymized pseudo-data is provided as a substitute.

This is a complete reproducibility failure. See Wheeler et al. (2024), Practice 10: Reproducibility and extendability, and the Code-Supplement Checklist (Data Restrictions item).

### 6. Uniform rw.sd = 0.01 Applied to All Parameters Regardless of Scale Creates Mismatched Perturbations

In the local search, `rw.sd` is set to 0.01 uniformly for every parameter (a, b, c, d, sigma_proc, sigma_obs, X_0). However, `d` (the intercept that sets the long-run mean of SDNN) has a starting value of 41 and converges near 47–51, while `b` and `c` are on the order of 0.01–0.5. A fixed perturbation of 0.01 constitutes roughly 0.02% of the scale of `d`, making that parameter almost immobile from its starting value under random-walk perturbations of this size. Conversely, 0.01 is a large fraction of the scale of `sigma_proc` (which converges near 0.05–0.1). Parameters should be perturbed on scales proportional to their expected uncertainty; the uniform choice here will impede convergence for large-scale parameters while over-perturbing small-scale ones. This is consistent with the observed slow movement of `d` in Figure 4 (the chains spread over 42–52 without tightening). The fix is to set `rw.sd` for `d` to approximately 0.5–1.0, for `X_0` to approximately 0.5, and retain 0.01 for the unit-scale parameters.

### 7. Global Search Box Excludes X_0 and Fixes It at a Single Value

In the global search, `X_0` is excluded from the uniform box and instead fixed at 34 via `fixed_params = c(X_0=34)`. This means all 96 global chains start with the same initial latent state, which is inconsistent with a genuine global search. Sensitivity of the likelihood surface to `X_0` was noted in the local search (traces show meaningful movement in X_0 in Figure 4), so fixing it at a single value in the global search suppresses a dimension of uncertainty that the local search found informative. The global box should include a range for X_0 (e.g., 30 to 38).

### 8. Model Validation Through Simulation Inadequate: Only Three Pre-optimization Simulations Shown

Figure 3 shows three simulated trajectories from the initial guess parameters, which are unsurprisingly similar to the data range since the initial guess was chosen to match the empirical series. No simulation-based model validation is performed at the MLE: no simulations from the fitted model are overlaid against the observed SDNN, and no filtering-distribution simulations are presented. Simulation from the filtering distribution conditioned on the observed data would reveal whether the fitted model can reproduce the observed trajectory, as distinct from whether the data fall within the unconditional range of the process. The absence of any post-fit simulation diagnostics makes it impossible to assess model adequacy visually, compounding the lack of quantitative goodness-of-fit assessment. See Wheeler et al. (2024), Practice 4: Model diagnostics.

### 9. Pooling Across Individuals Destroys Within-Person Dynamics and Introduces Ecological Fallacy Risk

The motivation for pooling all participants into a single daily median/mean time series is stated as computational convenience (irregular missing data in individual records), but this aggregation creates a fundamental interpretive problem: the POMP model assumes a single latent state governing all participants simultaneously. In reality, individuals will have heterogeneous baseline HRV levels, noise exposures, and activity patterns. Pooling the SDNN median suppresses between-person variation; the estimated b is thus an ecological association rather than an individual-level causal effect. The descending trend in the SDNN series from 2019 to 2024 (Figure 1, approaching -2 ms over 5 years) may reflect cohort attrition (e.g., older participants added over time, participants dropping out) rather than a genuine physiological trend. No sensitivity analysis or robustness check addresses this concern, and the biological interpretation in the text does not acknowledge the ecological fallacy risk.

---

## Minor Issues

### 10. The AIC Table Is Computed on the Differenced Series but Presented as if It Were the Benchmark for the Level-Series POMP

The caption of Table 1 reads "AIC of ARIMA(p,1,q), where p,q are from 0 to 6" and the code applies `aic_table` to `d_sdnn_ts` (the differenced series). This is correct for ARIMA model selection but the subsequent comparison of these AIC values to the POMP model AIC is inconsistent; the issue of incommensurability (Major Issue 2) is compounded by the fact that this is never flagged in the text.

### 11. Log-likelihood Typo in Reported ARIMA Model

The code fits `arima(d_sdnn_ts, order=c(5,0,6))` (an ARMA(5,6) on the differenced series, which is equivalent to ARIMA(5,1,6) on levels), but the table caption reads "AIC of ARIMA(p,1,q)". This is consistent, but the code snippet on page 6 uses `order=c(5,0,6)` which corresponds to ARMA(5,0,6) — i.e., an MA(6) component with 5 AR lags and 0 differencing applied to the already-differenced series. The authors should clarify whether this is ARIMA(5,1,6) applied to levels or ARMA(5,6) applied to the once-differenced series; the two are equivalent but the notation in the text switches between them without acknowledgment.

### 12. Missing `pomp` Package Version and `sessionInfo()`

No `sessionInfo()` output is included, and the pomp package version is not pinned. The `pomp` API has changed substantially across versions; without a version specification, the code cannot be reproduced even in principle. An `renv` lockfile or at minimum `packageVersion("pomp")` output should be included. See Code-Supplement Checklist, Documentation (README) item.

### 13. Effective Sample Size of Particle Filter Not Monitored

The particle filter is run with Np = 5,000 in the local search and Np = 2,000 in the global search, but no ESS diagnostic is presented. For a 1,875-step time series with Gaussian observation noise, ESS collapse is unlikely, but the difference in Np between local and global searches (5,000 vs. 2,000) means the log-likelihood estimates from the two stages are not directly comparable. The authors use both to argue that the global search is worse than the local search, but particle-filter Monte Carlo noise with only 2,000 particles over 1,875 steps could account for several units of log-likelihood difference. See Wheeler et al. (2024), Practice 6; simulation checklist item 10.

### 14. Stationarity Claim Justified Only Visually; No Formal Test

The decision to first-difference the series is supported solely by the visual observation "it looks like there is a descending trend" (page 4) and "now it looks like there is no trend" (page 5). No formal unit-root test (ADF, KPSS) is applied to justify the differencing. For a 1,875-point series this is feasible and should be done. More importantly, the POMP model is fitted to the undifferenced (levels) series, while the ARIMA benchmark is fitted to the differenced series — meaning the differencing decision affects only the benchmark, not the POMP model, which has its own intercept and persistence parameter. The authors should clarify whether the trend in the original series is addressed by the POMP intercept `d` and the autoregressive parameter `a`, or whether first-differencing within the POMP state equation would improve fit.

### 15. Negligible sigma_proc Estimate Implies Degenerate Latent Structure

The local search trace for sigma_proc (Figure 4) shows nearly all chains collapsing to values near 0.05–0.1 by iteration 300, while sigma_obs inflates to roughly 1.0. The authors note this pattern but do not evaluate its scientific implications: when sigma_proc approaches zero, the latent state X_t becomes a deterministic function of covariates and X_0, and the POMP model collapses to a regression model. At this limit, the particle filter is evaluating essentially the same deterministic trajectory for all particles, and the reported likelihood improvement from using a POMP framework over regression disappears. This near-degenerate regime should be diagnosed explicitly via a likelihood ratio test comparing sigma_proc = 0 (constrained) against the fitted model, to determine whether the stochastic latent process adds any statistical value at all.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project10/blinded.pdf`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project10/Makefile`
