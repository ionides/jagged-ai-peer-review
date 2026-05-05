# Peer Review: W25 Project 11
## Time Series Analysis of Apple Stock Price

---

## Summary

This project compares two volatility modeling frameworks — ARMA-GARCH variants (sGARCH, EGARCH, GJR-GARCH) and a discrete-time stochastic volatility POMP model — applied to Apple Inc. (AAPL) daily log-returns from January 2020 to early 2025. The paper is well-structured and covers both a classical econometric pipeline (ACF analysis, model selection by AIC, residual diagnostics) and a state-space approach with IF2-based parameter estimation, local and global searches, and a profile likelihood for the persistence parameter phi. Key strengths include thorough GARCH diagnostics, clear mathematical exposition of the stochastic volatility model, and an honest acknowledgment of POMP model limitations.

However, the POMP analysis suffers from several critical methodological errors: the global search box excludes the region containing the global MLE for mu_h by more than an order of magnitude; the global search uses a previous mif2 result as its first argument rather than the base pomp object; the GARCH and POMP log-likelihoods are compared as if they were on the same scale when they are computed on different data transformations (mean-subtracted vs. non-mean-subtracted); and the diagnostics figure for GJR-GARCH is actually computed from the eGARCH model. These errors collectively undermine the central comparative conclusion.

---

## Major Issues

### 1. Global search box excludes the region containing the global MLE for mu_h

The global search box is defined as `mu_h = c(-1, 0)` (blinded.Rmd, line 735). However, the best parameter set returned by the global search has `mu_h = -8.58` (verified from `box_eval_2.rda`), which lies more than 8 units below the box's lower bound of -1. The profile likelihood data in `eta_profile.rds` further confirms that mu_h at the profile maximum is approximately -8.7.

This means the global search could only reach the high-likelihood region by IF2 drifting the parameter far outside the specified box during optimization — an accidental escape rather than systematic coverage. Only one replicate out of 50 reached a log-likelihood above 3285 (matching the best value of 3288.956); the others cluster around 3200-3260, confirming poor coverage. The reported "global maximum" does not represent a reliable global optimum.

The fix is to extend the mu_h box to bracket the region identified by the local search, for example `mu_h = c(-12, 0)`.

### 2. Global search initialized from a previous mif2 result rather than the base pomp object

The global search code (blinded.Rmd, line 766) calls `mif2(if1[[1]], params=apply(apple_box,1,function(x)runif(1,x)))`, using `if1[[1]]` (the first mif2 result from the local search) as the first argument. The correct pattern for a global search is `mif2(apple.filt, params=...)`, where `apple.filt` is the base pomp object. Passing a previous mif2 result inherits the cooling schedule from the completed local chain, so the perturbation scale at the start of the global search is already at or near its terminal cooling state. The new random starting parameters are effectively explored with near-zero perturbations, making the global search a weak reseeding of the local chain rather than genuine box-wide exploration. This compounds the box misalignment issue (Issue 1) and further reduces confidence in the reported global MLE.

### 3. GARCH and POMP log-likelihoods are not directly comparable

The comparison table in the Analysis section reports:
- sGARCH_norm: 3289.09
- GJR-GARCH: 3328.37
- POMP model: 3288.55

The GARCH models are fitted to `na.omit(df$log_return)` (the raw log returns), while the POMP model is fitted to `deMeanRtn` (the mean-subtracted log returns). Although the numerical difference between mean-subtracted and non-mean-subtracted returns is small, the GARCH models include an explicit ARMA mean component (`armaOrder = c(1,1)`), while the POMP measurement equation is `Y_n = exp(H_n/2) * epsilon_n` with zero mean. The log-likelihoods of these models are defined over different distributional families and different normalizations of the data. Presenting these values in the same table and concluding that GJR-GARCH fits better conflates two non-comparable likelihood scales. A valid comparison would require fitting both model families to identical data with the same observation model structure, or computing out-of-sample predictive likelihoods on a held-out set.

### 4. Diagnostics figure mislabeled and computed from wrong model

The diagnostic analysis in Section 5 (GARCH) states "Based on all these observations, gjrGARCH successfully captures volatility clustering" and the figure is captioned "Figure 5.1: gjrGARCH Diagnostics Plots." However, the code at line 465 sets `model_to_test <- models[["eGARCH_std"]]` and passes this to `garch_residual_diagnostics()`. The diagnostics — skewness, kurtosis, ARCH-LM test, Ljung-Box tests, and all plots — are computed from the eGARCH model, not from the GJR-GARCH model. The authors state they "selected gjrGARCH for further analysis" but then validate the wrong model. The conclusion that gjrGARCH adequately captures volatility clustering is not supported by the diagnostics shown.

### 5. Insufficient computational effort for both local and global POMP searches

The local search uses `Np=1000` particles, `Nmif=50` iterations, and `Nreps_local=50` replicates. The global search uses the same settings with `Nreps_global=50` replicates. From the convergence diagnostics (Figure 6.1), the authors themselves observe that "the parameter values across different runs vary significantly," and from the global search results only one replicate approaches the best log-likelihood. The log-likelihood spread across local-search replicates is reported as "approximately 100 log units" — a range of 100 log-likelihood units indicates the optimization has not converged (well-converged chains should cluster within a few units of the true MLE). With 1000 particles and 50 iterations, the likelihood estimates are also subject to non-trivial Monte Carlo noise. Wheeler et al. (2024) demonstrate that "large improvement in log-likelihood was primarily attributed to increasing the computational effort." The authors acknowledge these limitations but do not attempt to quantify whether their best-reported log-likelihood is near the true MLE.

### 6. Profile likelihood range likely excludes the global MLE for phi

The profile likelihood is computed over `phi = seq(0.85, 0.99, length=10)`. The global search produces two qualitatively different solutions: the best result has `phi = 0.91`, while several other results have `phi ≈ 0.9999` with `sigma_eta > 20`. The fact that many global search replicates converged to the phi ≈ 1 boundary suggests there may be a second local optimum near phi = 1. The profile range (0.85–0.99) does not include the phi ≈ 0.9999 region, so the reported confidence interval cannot speak to whether the model is identifiable across the full persistence range. Additionally, the profile uses only 10 phi grid points and 15 replicates per point (150 total evaluations), which is quite sparse. The profile maximum of 3305.177 exceeds the global search best of 3288.956 by approximately 16 log-likelihood units, which is unexpected: the global search should achieve a log-likelihood at least as high as the profiled maximum. This discrepancy suggests the global search did not adequately explore the phi ≈ 0.91 region with the optimal mu_h value, consistent with the box misalignment in Issue 1.

### 7. Model selection rationale for GARCH is internally inconsistent

The authors state (Section 4) that they choose GJR-GARCH over sGARCH-norm because the goal is "to capture the financial volatility dynamics" rather than forecast accuracy. However, sGARCH-norm achieves the lowest AIC — the standard metric for balancing fit and parsimony — while GJR-GARCH achieves the highest log-likelihood. The argument that GJR-GARCH captures dynamics better because it has higher log-likelihood contradicts the AIC-based selection used for ARMA model choice earlier in the same paper. The paper does not report AIC values for the asymmetric GARCH models (EGARCH, GJR-GARCH), so readers cannot verify whether the complexity penalty offsets the log-likelihood gain. If AIC were consistently applied, sGARCH-norm would be the preferred model.

---

## Minor Issues

- **Figure numbering error**: Two figures are labeled "Figure 4.2" — the ACF plot of log returns (line 142) and the ARMA diagnostics plot (line 230). The second should be numbered 4.3 or higher.

- **STL decomposition applied to non-stationary price level**: The STL decomposition in Figure 3.2 is applied to `1 + log(Close)`, which retains the trend and is non-stationary. STL decomposition is designed to separate trend, seasonality, and remainder from a series that may be non-stationary in level, but the resulting "seasonality" component should be interpreted with caution for a stock price series — there is no a priori reason to expect a periodic seasonal component with frequency 260 (trading days per year), and the seasonality detected may be spurious. The authors conclude "the seasonal pattern is not very obvious," which is correct but the decomposition adds little to the analysis.

- **Density plot title mislabeled**: The code for Figure 3.1 sets the title to "Density Plot of Gold Prices" (line 88) when it should read "Apple Stock Price." This is a copy-paste artifact.

- **apple_params.csv is polluted with results from earlier runs**: The csv file contains 40 rows at the top with log-likelihoods in the 8000–9000 range (inconsistent with the analysis run at run_level=2), followed by repeated duplicate blocks of rows from multiple append operations. While the analysis does not read from this file (results come from the cached .rda files), the csv is listed as a supplementary artifact and is misleading to anyone attempting to reproduce the analysis.

- **Profile likelihood uses `%dofuture%` while parallel backend is `doParallel`**: The profile computation at line 886 uses `%dofuture%` but the registered backend at line 633 is `doParallel` (via `registerDoParallel`). This may cause the profile to run sequentially rather than in parallel, or may trigger a fallback to a default future plan. The `doFuture` package is loaded (line 36) but no `plan()` call is made to set up a future backend. A `plan(multisession)` or `plan(cluster)` call is needed for `%dofuture%` to run in parallel.

- **No simulation-based model validation for POMP model**: The paper does not produce forward simulations from the fitted POMP model to check whether simulated trajectories resemble the observed log-return series. The evaluation code (lines 810–850) generates simulations but only uses them as a vehicle to re-run the particle filter — the simulated data are never plotted or compared to the observed series. Wheeler et al. (2024) emphasize simulation-based diagnostics as essential for assessing model adequacy.

- **Log-likelihood scale not discussed**: The comparison table reports log-likelihoods of approximately 3288–3328 across all models, but the authors do not acknowledge that a difference of ~40 log-likelihood units between GJR-GARCH and sGARCH-norm is large (corresponds to a likelihood ratio test p-value that is effectively zero). This suggests the normal-distribution assumption in sGARCH-norm is strongly rejected by the data, yet the paper treats the choice as a trade-off between AIC and log-likelihood rather than a statistical rejection.

- **No acknowledgment that log-likelihood values can only be compared within the same model class**: The comparison table places GARCH log-likelihoods (computed via the rugarch package using exact normal/t-distribution densities) alongside the POMP log-likelihood (estimated via particle filter with Monte Carlo noise). The POMP log-likelihood estimate has standard error ~0.44 (from evaluation.rds), so the numerical comparison is approximate. This should be noted.

- **Redundant library calls**: `library(forecast)` is called twice at lines 37 and 39; `library(ggplot2)` is called twice at lines 34 and 43. These are minor code quality issues.

- **"Acknowledgments" is misspelled as "Ackonwledgments"** in the section header.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/references.bib`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/apple_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/evaluation.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/eta_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/box_eval_2.rda`
