# Peer Review: W25 Project 08
## Netflix Returns Analysis — POMP Volatility Model

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) via pomp R package |
| **R packages used** | pomp, rugarch, forecast, quantmod, doParallel, doRNG |
| **Code publicly available** | Yes — Git repo (blinded.rmd, pomp_final.Rmd, saved .rda and .csv files) |
| **Data publicly available** | Yes — Yahoo Finance via quantmod (downloaded at runtime) |
| **Benchmark comparison included** | Partial — GARCH/GJR-GARCH vs. POMP AIC compared verbally; no ARMA benchmark vs. POMP |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | logmeanexp used correctly; but rw.sd applied on natural scale for sigma_nu/sigma_eta without confirming transformation scope |
| 2 | Benchmark comparison | ~ | GARCH compared to POMP verbally; no formal ARMA benchmark table |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported; AIC computed but cross-model comparison table missing |
| 4 | Model diagnostics | ~ | ESS and conditional log-likelihoods discussed but not shown as standalone plots |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods; weak identifiability acknowledged but not quantified |
| 6 | Computational adequacy | ~ | run_level=2, 20 replicates; two likelihood clusters indicate optimizer did not converge globally |
| 7 | Forecast methodology | ✗ | Holdout set created but never evaluated; no out-of-sample test |
| 8 | Model variations and nested comparisons | ✗ | No model variants compared; no nested tests |
| 9 | Stochasticity | ✓ | SV model includes process noise and leverage; dmeasure uses normal distribution |
| 10 | Reproducibility and extendability | ~ | .rda and .csv archived; pomp version not pinned |
| 11 | Corroboration with scientific knowledge | ~ | mu_h ≈ -7.8 and mu_h ≈ -9.5 noted but not interpreted against financial volatility literature |
| 12 | Measurement model specification | ✗ | Text description conflicts with code (sigma_nu misidentified as observation noise) |
| 13 | Initial conditions | ~ | G_0 and H_0 estimated but sensitivity not assessed |

---

## Summary

This project analyzes daily NFLX log-return volatility using rolling statistics, GARCH, GJR-GARCH, and a stochastic volatility POMP model, benchmarking NFLX against SPY. The project demonstrates familiarity with the POMP workflow, uses correct logmeanexp aggregation, and structures both local and global IF2 searches. However, the model specification in the main writeup incorrectly describes sigma_nu as entering the measurement equation when the actual code places it only in the leverage process; the global parameter search box excludes the apparent MLE region for key parameters; no profile likelihoods are computed despite acknowledged identifiability concerns; and a holdout set built at the start is never used for out-of-sample evaluation.

**Strengths:**
- Correctly uses logmeanexp aggregation and replicated pfilter evaluation (rather than averaging on log scale or trusting mif2's internal loglik)
- parameter_trans correctly applies log and logit transformations for sigma_eta, sigma_nu, and phi
- The stochastic volatility leverage model is well-motivated and implemented in C snippets
- Both local and global searches are run with 20 replicates each, and convergence trace plots are produced
- Archived .rda and .csv parameter files allow evaluation without re-running optimization

**Weaknesses:**
- Measurement equation description in the main writeup incorrectly introduces sigma_nu as observation noise; code uses dnorm(y, 0, exp(H/2)) with no sigma_nu in dmeasure
- Global search box restricts mu_h to [-1, 0] and phi to [0.9, 0.999], but the apparent MLE has mu_h ≈ -7.8 and phi ≈ 0.757 for NFLX — the box excludes the optimum
- No profile likelihoods computed despite flat likelihood surfaces
- Holdout set (2023–2025) created but never used
- Unfinished editorial text embedded in Section 8.2

---

## Major Issues

### 1. Measurement Model Text–Code Mismatch: sigma_nu Misidentified as Observation Noise

The blinded.rmd Section 6.1 writes the measurement equation as Y_n = exp{H_n/2} * epsilon_n, with "epsilon_n ~ N(0, sigma_nu)" described as "a noisy measurement." This implies sigma_nu is the observation noise standard deviation. However, the actual dmeasure C snippet in pomp_final.Rmd is `lik = dnorm(y, 0, exp(H/2), give_log)`, which corresponds to epsilon_n ~ N(0,1) with no sigma_nu. The parameter sigma_nu appears exclusively in the state equation as the innovation SD of the G_n leverage random walk: `nu = rnorm(0, sigma_nu); G += nu`.

The same Section 6.1 later correctly states "nu_n ~ N(0, sigma_nu^2), with sigma_nu governing the variability of the leverage process," directly contradicting the measurement equation description two paragraphs earlier. The model as coded is a standard stochastic volatility model (epsilon_n ~ N(0,1) in dmeasure); sigma_nu is purely a state-process parameter, not an observation noise parameter. This internal inconsistency would mislead any reader trying to replicate or extend the analysis, and is exactly the type of code–text discrepancy documented as a concrete reproducibility failure in Wheeler et al. (2024). The measurement equation in the main text must be corrected to match the code.

### 2. Global Search Box Excludes the Apparent MLE Region

The global search initializes mu_h uniformly from [-1, 0] and phi from [0.9, 0.999]. Yet the local search (starting from informed initial values) consistently finds the MLE at mu_h ≈ -7.8 and phi ≈ 0.757 for NFLX, and mu_h ≈ -9.5 and phi ≈ 0.939 for SPY. For NFLX, both the optimal mu_h (-7.8) and phi (0.757) lie entirely outside the global search box boundaries. For SPY, mu_h = -9.5 also lies far outside [-1, 0].

This means none of the 20 global search replicates started from a region near the apparent optimum. The global search's purpose is to verify the local optimum by approaching it from diverse directions; here, the box is too narrow and misplaced to serve that purpose. It is not surprising that the global search fails to improve on the local search — the global replicates must traverse a very large parameter distance before reaching the optimum. The result is that the comparison between local and global searches provides no useful evidence of convergence to a global maximum. The global search box should be expanded to include the MLE region found by the local search: at minimum, mu_h should range to at least -12 and phi should range from 0.5 or lower for NFLX.

### 3. No Profile Likelihoods Despite Acknowledged Identifiability Problems (CC-Yes: Error 1.9)

The project acknowledges "weaker identifiability" and "flat likelihood surface" for NFLX, and identifies that sigma_nu and sigma_eta show "substantial variability across replicates." Examining the archived parameter CSVs confirms this: among the 20 NFLX global runs, sigma_eta ranges from 0.9 to 679 and logLik_se reaches 10.5 for some runs, meaning individual log-likelihood estimates span ±20 log-units. Despite these warning signs, no profile likelihoods are computed for any parameter.

This is a course-confirmed error (W25 Q10-02). Without profiles, it is impossible to determine which parameters are identifiable and which are not, confidence intervals cannot be constructed, and the reported point estimates may be on a flat ridge where many parameter combinations yield similar likelihoods. The project notes "potential benefits from additional data or parameter profiling" in the limitations, but this should be treated as a required analysis step, not an optional future improvement. At minimum, profile likelihoods for phi and sigma_eta — the most influential parameters — should be computed.

### 4. NFLX Optimizer Stuck in Local Maxima; Convergence Not Demonstrated

The text explicitly states that the NFLX local search "converges into two groups, indicating the existence of traps for local maxima." The logLik gap between these two groups is approximately 17 units (4605 vs. 4622), far larger than the Monte Carlo SE of ~0.85, confirming these are distinct modes and not Monte Carlo noise. The global search, despite starting from diverse (if poorly positioned) initial values, achieves a maximum of 4619.8, below the local search maximum of 4622.8. Neither search demonstrates that the reported best parameters are the global MLE. For a 6-parameter model, IF2 with 20 replicates at run_level=2 may be insufficient for a multimodal surface. The project should either run additional replicates from the vicinity of the local maximum cluster, or acknowledge clearly that the reported parameters may not be the global MLE and that inference about parameter values is correspondingly uncertain.

### 5. Holdout Set Created but Never Evaluated

In Section 2.1, the project explicitly creates `nflx_holdout` and `spy_holdout` covering 2023–2025, and Section 8.3 lists "uncertainty propagation" as a limitation of ARIMA forecasts. Yet neither the POMP model nor the GARCH models are ever evaluated on the holdout data. The project uses 2023–2025 data only in Section 7 (the market comparison, using the full `NFLX` and `SPY` symbols re-downloaded without the training cutoff). The holdout set is simply discarded. Since a primary claim of the project is that POMP better captures volatility dynamics, out-of-sample log-likelihood or density forecasts on the holdout period would be the most meaningful test of this claim. In-sample AIC comparisons favor more flexible models mechanically and do not establish forecasting value.

---

## Computational and Diagnostic Assessment

**Convergence:** Two distinct likelihood clusters appear in NFLX local search convergence traces, signaling multiple local maxima. The global search does not escape these. For SPY, convergence appears cleaner with a single dominant cluster. Convergence traces are shown for all replicates (correct practice).

**Particle filter:** Np = 1000 at run_level=2 is course-standard and defensible. ESS and conditional log-likelihoods are mentioned in the text but do not appear as standalone diagnostic plots — they are described as part of the mif2 output. Several NFLX global runs have logLik_se > 5 (one reaches 10.52), indicating that 1000 particles is insufficient for some parameter combinations and that those likelihoods should not be taken as reliable estimates.

**Conditional log-likelihoods:** Referenced in text descriptions ("few correlated dips at some isolated time points") but not presented as explicit per-time-step log-likelihood plots. These would be especially valuable given the known extreme events (2022 subscriber loss crash) in the training data.

**Profile likelihoods:** None computed. See Major Issue 3.

**Computational scale:** run_level=2 with 20 replicates per search; CPU-hours not reported. Given the multimodality found, additional computation (run_level=3 or more replicates) would be appropriate.

---

## Reproducibility Assessment

**Code availability:** Both blinded.rmd and pomp_final.Rmd are available; .rda and .csv files archive the fitted results. The separation of the pomp specification into a separate file (pomp_final.Rmd) that is not directly rendered in the main report makes verification harder.

**Final parameters:** Archived in .csv files (nflx_params_global.csv, etc.). Good practice.

**Model-code consistency:** The measurement model description in blinded.rmd conflicts with the actual dmeasure code. See Major Issue 1.

**Package versions:** pomp version not pinned (no renv or sessionInfo() provided). The pomp API has changed substantially across versions and results may not reproduce on current CRAN releases.

**Auxiliary data:** Data is downloaded at runtime from Yahoo Finance; there is no guarantee the Yahoo Finance API will return identical data in future runs (adjusted prices may be retroactively revised). A static CSV of the training data should be archived.

**HPC reproducibility:** Parallel execution uses all detected cores; no cluster job scripts needed for this scale.

---

## Minor Issues

- **Unfinished editorial text in Section 8.2:** A blockquote reads "We extended the analysis beyond classical GARCH by incorporating asymmetric volatility modeling. Add direct discussions of how we expanded on the previous projects." This is a visible editorial placeholder that was not completed before submission.

- **Incorrect URL in Reference 12:** Reference [12] ("Project 11, Winter 2024: NVIDIA Stock Price Analysis") links to https://ionides.github.io/531w24/final_project/project07/blinded.html — the same URL as Reference [11] (Project 7, W24 Apple). This is a copy-paste error.

- **ACF description inconsistency in Section 3.1:** The text states "The ACF plots show slow decay for both series, which is characteristic of non-stationary series," then immediately concludes "these diagnostics confirm that log returns are already stationary." Slow decay in the ACF of log returns would contradict stationarity; financial log returns typically exhibit near-zero ACF. The description appears to have been written for a non-return series (e.g., raw prices) and was not updated to match the actual plot of log returns.

- **Cross-model AIC comparison lacks a summary table:** Section 8.1 asserts verbally that "the maximum log-likelihood values obtained were higher than those of both GARCH and GJR-GARCH models." The GARCH and POMP AIC values are computed in the code but never placed in a common comparison table with the POMP model's AIC. A single table with model, number of parameters, log-likelihood, and AIC for GARCH(1,1), GJR-GARCH, and POMP would substantiate this claim. The statement "it only has 3 more parameters" is also ambiguous — GARCH(1,1) with mean has 4 parameters, GJR-GARCH with skewed-t has approximately 7; the POMP model has 6. The number of additional parameters depends on which model is the reference.

- **First observation set to zero:** Both blinded.rmd and pomp_final.Rmd compute `c(0, diff(log(nflx_train$Close)))`, prepending an artificial zero as the first log return. This zero enters the POMP covariate table and the likelihood computation. Setting the first return to NA (or simply dropping it) would be preferable to avoid contaminating the likelihood with a deterministic zero return.

- **Large Monte Carlo SEs in several global search runs not discussed:** The text reports only the Monte Carlo SE of the best-likelihood run (≈0.82 for NFLX). In the archived nflx_params_global.csv, seven runs have logLik_se > 2, and one has logLik_se = 10.52. These high-SE runs indicate that 1000 particles is insufficient for those parameter values, and the reported logLik for those runs is unreliable. The discussion should note which runs are trustworthy and which are not, rather than relying on picking the best logLik from a table where many entries are noisy.

- **Auto-installing packages without user consent:** The packages chunk at the start of blinded.rmd runs `install.packages(pkg)` inside a loop for any missing package. This modifies the user's R environment without consent and can fail silently in restricted environments.

- **pomp version not pinned:** The pomp package API has changed substantially across versions. Without pinning the version (e.g., via renv), the code may not reproduce correctly on current CRAN releases.

---

## Recommendation

**Major Revision.** The core POMP analysis contains a model description error that misidentifies the role of sigma_nu, a global search design flaw that prevents meaningful exploration of the parameter space, and no profile likelihood analysis despite explicit acknowledgment of identifiability concerns. These issues collectively undermine confidence in the reported parameter estimates and the AIC comparisons. The holdout set built at the start is never used, missing the most compelling test of the POMP model's utility. The analysis should be revised to: (1) correct the measurement equation description to match the code; (2) redesign the global search box to include the MLE region; (3) compute profile likelihoods for at minimum phi and sigma_eta; and (4) evaluate held-out density forecasts on the 2023–2025 period.

---

## Files Consulted

**Skill files:**
- /Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md
- /Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md
- /Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md
- /Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd
- /Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md
- /Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md
- /Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md

**Project files:**
- /Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project08/blinded.rmd
- /Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project08/pomp_final.Rmd
- /Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project08/nflx_params_global.csv
- /Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project08/nflx_params_local.csv
- /Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project08/spy_params_global.csv
- /Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project08/spy_params_local.csv
