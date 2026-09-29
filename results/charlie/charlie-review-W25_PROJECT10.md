# Review: W25 Project 10

## Paper Metadata

| Field | Details |
|-------|---------|
| **Title** | Daily Environmental Noise and Heart-Rate Variability |
| **Inference method** | MIF2 (iterated filtering via `mif2`), particle filter (`pfilter`) |
| **R packages used** | pomp, tidyverse, doParallel, doRNG, foreach, knitr |
| **Code publicly available** | No — analysis performed inside Apple Inc.'s secure VDI; HTML output cannot be exported |
| **Data publicly available** | No — proprietary Apple Inc. data under research-use agreement |
| **Benchmark comparison included** | Yes — ARIMA(5,1,6) and linear regression |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | MIF2 used correctly in principle; but declining loglik means terminal likelihood is not at MLE |
| 2 | Benchmark comparison | ~ | Benchmarks included but compared across differently-transformed data (see Issue 2) |
| 3 | Quantitative goodness-of-fit reporting | ~ | Loglikelihoods reported but the reported POMP value is from a non-converged run |
| 4 | Model diagnostics | ~ | Trace plots shown; no simulation-based post-fit diagnostics or ESS monitoring |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods, no confidence intervals |
| 6 | Computational adequacy | ✗ | Loglik declines after iteration ~10; optimizer never converged; global search far below local |
| 7 | Forecast methodology | N/A | No forecasts attempted |
| 8 | Model variations and nested comparisons | ✗ | No alternative model structures tested |
| 9 | Stochasticity | ~ | Process and measurement noise included; overdispersion not assessed |
| 10 | Reproducibility and extendability | ✗ | Data proprietary and inaccessible; analysis unverifiable; screenshots only |
| 11 | Corroboration with scientific knowledge | ~ | Noise coefficient sign discussed; other parameters not checked against literature |
| 12 | Measurement model specification | ~ | Gaussian assumed; acknowledged as potentially wrong but not examined |
| 13 | Initial conditions | ~ | X_0 estimated as parameter; no sensitivity analysis |

---

## Summary

This project fits a linear-Gaussian partially observed Markov process (LG-POMP) to a proprietary daily pooled dataset of heart-rate variability (SDNN, n = 1,875 days) and two covariates (daily environmental noise Leq and physical activity Energy), aiming to quantify the instantaneous suppressive effect of noise on HRV at the population level. The model is compared informally against an ARIMA(5,1,6) benchmark and a linear regression. The project demonstrates genuine methodological ambition and clear scientific motivation.

**Strengths:** The research question is well-framed and the LG-POMP model is elegantly specified. The author correctly uses `logmeanexp` to aggregate replicated particle filter runs, shows trace plots for convergence diagnosis, and acknowledges the model's shortcomings honestly in the conclusion. The identification of the model as linear-Gaussian is a sophisticated observation that could support future Kalman filter implementation.

**Weaknesses:** The optimizer demonstrably fails to converge — the log-likelihood peaks near −2700 in early iterations and declines to −3235 by the final iteration, so the reported MLE is not the true MLE. The ARIMA benchmark is fit to the differenced series while the POMP model is fit to the original series, making the key comparative log-likelihoods non-comparable. No profile likelihoods or confidence intervals are reported for any parameter. The data and full output are inaccessible due to Apple Inc. proprietary restrictions, making the analysis unverifiable.

---

## Major Issues

### 1. Convergence failure: log-likelihood declines after iteration ~10 throughout the mif2 run

The trace plot (Figure 4) shows the log-likelihood peaking near ℓ ≈ −2700 within the first ten iterations and then drifting downward to approximately −3100 by iteration 300. The replicated pfilter evaluation at the final iterate gives −3235.17 — substantially worse than the early peak. This is a clear convergence failure: the reported MLE is at least 500 log-likelihood units below the best likelihood visited during the search.

The author correctly diagnoses this as arising from "over-diffuse random-walk perturbations combined with Monte-Carlo noise in the particle filter" and proposes three remedies (smaller rw.sd, more particles, fixing σ_proc). However, none of these remedies are implemented. The analysis is reported as if the terminal likelihood of −3235 is the MLE, when in fact the optimizer abandoned the best solution it found. This is a major flaw that invalidates downstream model comparisons: the POMP model's true MLE (at least −2700, possibly better) would substantially change the performance picture relative to the benchmarks. [CC-Yes; Error 1.8 — Missing convergence diagnostics for iterated filtering; Error 1.5 — Declining likelihood during iterated filtering]

*Fix:* Re-run with a smaller cooling fraction (e.g., cooling.fraction.50 = 0.1), reduce rw.sd to 0.005 or smaller, or switch to the Kalman filter (see Issue 5) to obtain an exact and noiseless likelihood. Stop mif2 at the iteration of the peak loglik, and report the likelihood at that point rather than at the terminal iterate.

---

### 2. ARIMA benchmark fitted to the differenced series; POMP model fitted to the original series — log-likelihoods are not comparable

The ARIMA(5,0,6) model is fitted to `d_sdnn_ts` (the first-differenced series, 1,874 observations), producing a log-likelihood of −2591.27. The POMP model is fitted to the original `sdnn` column (1,875 observations). A Gaussian linear regression is also fitted to the original (undifferenced) series, giving −3025.71. These three likelihoods are for different data — differenced vs. undifferenced, and in some cases different numbers of observations — and cannot be compared directly. The conclusion states "a purely empirical ARIMA(5, 1, 6) model fitted to the same differenced series achieved ℓ_max^ARIMA ≈ −2591" and then compares it in the same sentence to the POMP's −3235, which is the likelihood of the undifferenced data. This comparison is invalid.

Likelihoods from different model classes applied to *the same data* are directly comparable (course convention; MT2 Q4-01), but likelihoods computed on *different data* are not. The AIC values reported in the AIC table on page 6 are for ARMA models on the differenced data and similarly cannot be used to benchmark POMP on the undifferenced data. [CC-Yes; Error 2.2 — AIC comparison between ARIMA and POMP without noting non-comparability; here the problem is more fundamental because the data differ]

*Fix:* Either (a) fit the ARIMA model to the original undifferenced series as `arima(sdnn_ts, order=c(5,1,6))`, which produces a likelihood on the same data as the POMP model, or (b) fit a POMP model that internally includes the differencing as part of the observation equation, ensuring all likelihoods are for the same observed data.

---

### 3. POMP fits substantially worse than the linear regression benchmark, yet no structural revision is attempted

Even setting aside the ARIMA comparability problem, comparing likelihoods on the same undifferenced data: the linear regression achieves −3025.71 and the POMP achieves −3235.17. The POMP model has strictly more parameters and dramatically more computational effort, yet fits substantially worse than a simple regression by approximately 209 log-likelihood units. The author concludes that "the present model specification does not yet capture the dominant structure in the data," but does not revise the model before reporting. When the mechanistic model fits disastrously compared to even the weakest benchmark, the correct diagnostic step is to examine residuals and revise the model structure — not to retain the failed model and defer revision to future work. [CC-Yes; Error 1.15 — Increasing Np/Nmif as the first response when POMP fits poorly vs. benchmark; Error 1.6 — Not comparing to a non-mechanistic benchmark (present but ignored in model development)]

*Fix:* Investigate why the POMP underperforms. Likely candidates include: (a) the first-order AR dynamics are insufficient for daily SDNN which has longer-range structure; (b) the Gaussian measurement model is misspecified (log-normal may fit better); (c) the process noise σ_proc near zero is absorbing all variance into measurement error, effectively collapsing the model to a static regression. Each of these should be examined before declaring results.

---

### 4. No profile likelihoods and no confidence intervals for any parameter

The parameter estimates (a ≈ 0.2, b ≈ −0.30, c ≈ 0.1, d ≈ 47–51, σ_proc ≈ 0, σ_obs ≈ 1, X_0 ≈ 34) are reported only as MLE point estimates from the trace plots, with no uncertainty quantification. No profile likelihoods are computed for any parameter. The author mentions "profile the likelihood on a much finer grid with a larger particle set" as future work. Without profiles, it is impossible to assess whether any parameter is identifiable. The trace plots themselves reveal strong collinearity between a, d, σ_proc, and σ_obs (acknowledged in the text), which profile likelihoods would formally characterize. The key scientific parameter b (noise effect on HRV) is reported with no confidence interval, so the main conclusion — that noise suppresses HRV by roughly 0.3 ms per dB — is unsupported by any formal uncertainty quantification. [CC-Yes; Error 1.9 — Profile likelihood too sparse to identify the maximum; Checklist #5 — Parameter identifiability and uncertainty]

*Fix:* Compute profile likelihoods for at least b (the noise effect) and a (the persistence parameter) using `mif2` at a fixed grid of target parameter values. Report MCAP-based or Wilks-based 95% confidence intervals. Note that switching to the Kalman filter (Issue 5) would make profile computation much faster.

---

### 5. The LG-POMP model admits exact Kalman filter likelihood evaluation; using a particle filter introduces avoidable Monte Carlo noise

The model is explicitly identified as a linear-Gaussian partially observed Markov process. For this model class, the Kalman filter delivers the exact likelihood in closed form — no Monte Carlo approximation is required. By instead using `pfilter` (a particle filter), the analysis introduces stochastic likelihood evaluation noise at every step of the optimization and at every pfilter call. This noise directly causes the likelihood-decline problem in Issue 1: the optimizer cannot distinguish between a genuine decrease in likelihood and a large negative Monte Carlo fluctuation, so the cooling schedule causes it to drift away from the optimum. None of the computational difficulties diagnosed in Issues 1, 4, and 6 would exist if the Kalman filter were used.

*Fix:* Implement the Kalman filter likelihood for this LG-POMP model, which can be done analytically in closed form or using the `KFAS` or `dlm` packages. This would allow exact MLE via gradient-based optimization, profile likelihoods computed in seconds rather than hours, and reliable confidence intervals.

---

### 6. Global search result (−7936) is far below local search result (−3235); the global search cannot validate the local optimum

The global search (Np = 2000, Nmif = 150, 96 chains) produces a maximum log-likelihood of −7936.22 — approximately 4,700 log-likelihood units below the local search result of −3235.17. The author attributes this to the global search being "scored at the terminal parameter vector" and using "a relatively small particle set," but this explanation does not salvage the comparison. If the global search reliably identifies the neighbourhood of the true optimum, its terminal likelihoods should be within reasonable Monte Carlo error of the local search value, not 4,700 units below. A gap of this magnitude means the global search has not converged at all, and the claim that "the high-likelihood points cluster in the same (a, b, c, d, σ_obs) neighbourhood found by the local search" does not resolve the discrepancy. The global search cannot serve as a validation that no better solution exists elsewhere in the parameter space. [CC-Yes; Error 1.8 — Missing convergence diagnostics; Checklist #6 — Computational adequacy]

*Fix:* Increase Np and Nmif for the global search to values where the global terminal likelihoods are within a few units of the local result. Alternatively, use the global search only for initialising local runs, and validate the local result via several independently seeded local searches achieving similar terminal likelihoods.

---

### 7. Autoregressive coefficient a fails to converge in the local search

The trace plot (Figure 4) shows a "drifts steadily upward from near zero toward 0.2–0.25 without ever plateauing" through 300 mif2 iterations. The author characterises this as expected because a is weakly identified, but weak identifiability leads to spread across multiple converged runs at a well-defined likelihood maximum — it does not produce a parameter that continues to trend upward throughout the full run. A trend through the entire run is evidence that the optimiser has not finished climbing; it signals that 300 iterations were insufficient for this parameter, not merely that the likelihood surface is flat around a converged value. [CC-Yes; Error 1.8 — Missing convergence diagnostics; see course note: what to look for is loglik converging upward, not parameter continuing to trend]

*Fix:* Increase Nmif until a stops trending, or adopt a schedule in which Nmif is determined adaptively by monitoring the loglik improvement per iteration. If switching to the Kalman filter as in Issue 5, this problem disappears.

---

### 8. Data, analysis, and outputs are inaccessible; review is based on annotated screenshots

The data-availability statement confirms that the underlying data is proprietary Apple Inc. property. The HTML notebook was generated inside Apple's VDI and cannot be exported. The submitted artefact is a PDF of annotated screenshots of the R Markdown console output and plots. This means no aspect of the analysis can be independently verified: the numerical results, the code execution, the completeness of the output, and the correctness of any figure are all unauditable. The screenshots substitute for but do not replace a reproducible analysis. Furthermore, no synthetic or anonymised dataset is provided that would allow readers to exercise the code structure. [Checklist #10 — Reproducibility and extendability]

*Fix:* Request an exemption from Apple's data-sharing policy for a de-identified or aggregated dataset, or construct a synthetic dataset with statistical properties similar to the original that can be distributed alongside the code. At minimum, provide a complete, executable Rmd file that runs on the synthetic data.

---

## Computational and Diagnostic Assessment

**Convergence:** The loglik trace climbs steeply in the first ten iterations to approximately −2700, then drifts downward to approximately −3100 by iteration 300. This pattern is the opposite of convergence. Multiple chains (48) are run but they all exhibit the same declining trajectory, meaning replication of the failure does not rescue the analysis. The author correctly identifies the cause but does not implement any fix.

**Particle filter:** Np = 5000 for the local search and 2000 for the global search. The particle count is reasonable for local search but insufficient for the global search given the discrepancy in terminal likelihoods. No effective sample size (ESS) monitoring is shown.

**Conditional log-likelihoods:** Not reported. Per-time-step log-likelihoods would help diagnose which periods of the 2019–2024 data are driving the poor fit (e.g., COVID-19 era behavioural changes or Apple Watch uptake effects).

**Profile likelihoods:** Not computed. This is the most critical missing diagnostic for this report.

**Computational scale:** The local search with 48 chains × Np 5000 × Nmif 300 is substantial, implying a well-resourced computing environment. However, the computational effort is wasted because the optimizer diverges from the best solution it found.

---

## Reproducibility Assessment

**Code availability:** Not publicly available. All code executed within Apple's secure VDI.

**Final parameters:** Not archived separately. Parameter values are visible in trace plot axes and text but not in a downloadable file.

**Model-code consistency:** The mathematical model (Equations 1–2) matches the Csnippet code shown on page 9. The measurement model uses `dnorm(sdnn, X, sigma_obs, give_log)`, consistent with Y_t = X_t + ε_t, ε_t ~ N(0, σ_obs²).

**Package versions:** Not reported. `sessionInfo()` output is absent. The `pomp` API is version-sensitive and without a pinned version, the code cannot be confirmed reproducible on current CRAN.

**Auxiliary data:** The covariate table (`covar_df`) is constructed from the same proprietary CSV as the observations, so it is equally inaccessible.

**HPC reproducibility:** The code uses SLURM environment variable `SLURM_NTASKS_PER_NODE`, confirming HPC use, but no SLURM job scripts or environment specifications are provided.

---

## Minor Issues

- The decision to difference the SDNN series is made by visual inspection ("It looks like there is a descending trend") with no formal stationarity test and no consideration of whether the trend is deterministic (trend + ARMA noise) rather than stochastic (unit root). A downward trend in long-term HRV data could plausibly reflect COVID-19 pandemic effects or increasing Apple Watch adoption over 2019–2024, neither of which would be well-modelled by differencing. [CC-Yes; Error 2.1 — Treating differencing and detrending as equivalent]

- No simulation-based post-fit diagnostics are shown. Figure 3 shows forward simulations from initial parameter guesses only. After fitting, there should be a comparison of simulated trajectories (from the filtering distribution or from the MLE parameters) to the observed data, to assess whether the model reproduces the data's range, seasonal amplitude, and autocorrelation structure.

- The Gaussian measurement model (Y_t = X_t + ε_t, ε_t ~ N(0, σ_obs²)) is applied to SDNN values (a strictly positive quantity measured in milliseconds). No justification is given for the Gaussian assumption, no QQ-plot of residuals is shown, and no overdispersion check is performed. The author notes in the conclusion that log-normal vs. Gaussian observation models should be compared; this should be part of the initial analysis, not deferred to future work.

- The loglik computation for the linear regression (`logLik_lm <- -0.5*(aic_lm - 2*k)`) is algebraically correct given the AIC definition, but it relies on R's `AIC()` using the standard normalisation. The computation is correct but non-transparent; reporting `logLik(hrv_lm)` directly would be clearer.

- The `rw.sd` for all parameters is set to 0.01, which is half the course-standard value of 0.02 (Ch 15, p31). While smaller perturbations can improve stability in principle, combined with 300 iterations and a cooling fraction of 0.5, the perturbation schedule may be insufficient to adequately explore the parameter space in early iterations where broader exploration is most needed. The author proposes "reducing random-walk step sizes" as a fix for the declining likelihood, but the step sizes are already small; the more likely fix is reducing the total number of iterations or the cooling rate.

- The paired scatter plot (Figure 5) shows loglik values from the global search spanning from approximately −11,000 to −8,000. The range of these likelihoods — all far below the local search value of −3,235 — provides additional evidence that the global search is uninformative about the true MLE. The clustering of high-loglik points in a particular (a, b, c, d, σ_obs) region should be interpreted cautiously when "high" means −8,000 to −9,000 rather than near −3,235.

- The model conflates between-person heterogeneity with within-day measurement noise in σ_obs. Since observations are daily medians aggregated across participants, σ_obs captures both individual-level HRV variation across people and sensor noise. The pooling design masks between-person dynamics, and the model parameters (particularly b, the noise effect) estimate a population-average effect that may differ substantially from individual-level effects. The conclusion briefly acknowledges this but no sensitivity analysis is presented.

---

## Recommendation

**Major Revision.** The analysis as submitted does not achieve a reliable MLE: the optimizer's trajectory demonstrates that the best likelihood found (approximately −2700) is substantially better than the reported value (−3235), and the key parameter a has not converged after 300 iterations. No uncertainty quantification (profile likelihoods or confidence intervals) is provided for any parameter, including the primary scientific quantity of interest (the noise effect b). The benchmark comparison is invalidated by fitting the ARIMA and POMP models to different data. The proprietary data restriction makes the analysis unverifiable. Before this work can be considered complete, the authors must: (1) achieve genuine convergence of the optimizer, ideally by switching to the Kalman filter for this LG-POMP model; (2) report profile likelihood confidence intervals for b; (3) ensure all compared log-likelihoods are evaluated on the same data; and (4) provide a reproducible analysis environment (even if using a synthetic dataset).

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project10/blinded.pdf` (all 16 pages, read as images)
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project10/Makefile`
