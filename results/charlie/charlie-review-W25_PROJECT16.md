# Peer Review: W25 Project 16
## "Analyzing Whooping Cough with ARMA and POMP"

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2), particle filter (pfilter) for POMP; ARIMA and ARCH via rugarch for classical |
| **R packages used** | pomp, rugarch, FinTS, forecast, doParallel, doFuture, foreach |
| **Code publicly available** | Yes (git repo submission) |
| **Data publicly available** | Partial — CDC NNDSS data used; auxiliary files (births, deaths, vaccination) included in repo |
| **Benchmark comparison included** | Partial — ARCH vs. SEIR POMP comparison is attempted but methodologically compromised |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + replicated pfilter used correctly; logmeanexp applied properly |
| 2 | Benchmark comparison | ~ | ARCH vs. POMP comparison attempted but invalid due to different data transformations |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported but comparison is problematic |
| 4 | Model diagnostics | ~ | Trace plots shown for SIR and main SEIR; trace plots for comparison SEIR are commented out |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods; no confidence intervals for any parameter |
| 6 | Computational adequacy | ~ | Global searches with Np=5000, nseq=500, Nmif=100; moderate effort |
| 7 | Forecast methodology | N/A | No forecasting performed |
| 8 | Model variations and nested comparisons | ~ | SIR and SEIR compared; SEIRV attempted; no formal likelihood ratio test |
| 9 | Stochasticity | ~ | Stochastic process model with negative binomial measurement; overdispersion k fixed |
| 10 | Reproducibility and extendability | ~ | bake() caching used; no renv; sessionInfo absent |
| 11 | Corroboration with scientific knowledge | ~ | Implausible SIR parameters noted qualitatively but not formally |
| 12 | Measurement model specification | ✗ | Accumulator H tracks I→R transitions, not S→I new infections; epidemiologically atypical |
| 13 | Initial conditions | ~ | Eta estimated; E, I, H initialized to fixed non-zero constants without justification |

---

## Summary

This project applies ARMA, ARCH, SIR, and SEIR models to weekly whooping cough case counts for five East North Central states (2017–2025), with a focus on the large 2024 outbreak. The authors correctly identify and implement IF2 with replicated pfilter evaluation, appropriately use logmeanexp for likelihood aggregation, and pursue a genuinely interesting modeling challenge involving epidemic dynamics, missing data, and covariate incorporation. However, the project has several significant methodological weaknesses: the primary ARCH-vs.-POMP comparison is invalid because the two models are fit to different data transformations; no profile likelihoods are computed, leaving all parameters without confidence intervals or formal identifiability assessment; and the accumulator in both compartmental models tracks recoveries (I→R) rather than new infections, which is epidemiologically atypical for a disease where cases are diagnosed at onset of illness.

**Strengths:** Proper use of logmeanexp for likelihood aggregation; bake() caching for reproducibility of expensive computations; honest acknowledgment of model limitations; engagement with real covariate data (vaccination, births, deaths); multiple model structures explored; global search with reasonable computational effort (Np=5000, nseq=500 starting points).

**Weaknesses:** Invalid likelihood comparison between ARCH (differenced data) and SEIR POMP (original data); no profile likelihoods for any parameter; measurement model accumulator tracks the wrong transition; missing convergence diagnostics for the version of the model used in the key comparison; and no confidence intervals reported for any estimated parameter.

---

## Major Issues

### 1. Invalid likelihood comparison between ARCH and SEIR POMP models

The core comparison in the paper compares the ARCH model log-likelihood (−1203) against the SEIR POMP log-likelihood (−1442), concluding that "the ARCH model demonstrated superior performance." The authors justify this by noting that "first differencing is a linear transformation with a constant Jacobian." This justification is insufficient for two reasons.

First, the ARCH model is fit to the differenced series `pertussis_diff` (Δy_t = y_t − y_{t−1}), while the SEIR POMP model is fit to the original case count series y_t. These are not the same data. The standard course principle that likelihoods across model classes are comparable (MT2 Q4-01) applies only when both models are evaluated on the same observed sequence. The Jacobian of a simple difference transform for continuous densities is indeed 1, but here the underlying data are discrete counts (not continuous), and the ARCH model imposes a Gaussian distribution on the differenced counts — a misspecification that makes the likelihood scale non-equivalent to the POMP likelihood on the original count data.

Second, the SEIR POMP model fit to original data (ll = −1442) is being compared to an ARCH model fit to a different data object that also uses linearly interpolated values for the 2022 gap (from `interpolated_cases.csv`), while the SEIR POMP treats those weeks as missing via the ISNA check. The two models therefore differ in both the data transformation and the handling of missing observations.

This comparison should either be abandoned or restructured by fitting an ARMA-class model directly to the original count data (e.g., a negative-binomial INGARCH) on the same observations used for the POMP model, enabling a valid apples-to-apples comparison. As stated in 531-conventions.md, likelihoods from different model classes ARE comparable — but only for the same data. (Error 2.2, CC-Yes, Major.)

### 2. No profile likelihoods computed; no confidence intervals reported

Neither the SIR nor the SEIR model includes profile likelihood computations for any parameter. As a result, the project cannot formally assess whether any parameter is identifiable from the data, and no confidence intervals are reported for beta, mu_IR, eta, rho, or k. The authors note qualitatively that mu_IR appears not to be identifiable in the SIR global search pairs plot, but this observation is informal. For parameters like rho (reporting rate) and eta (initial susceptible fraction), identifiability is directly relevant to interpreting whether the model reveals anything about the 2024 outbreak dynamics.

Profile likelihoods require optimizing over all other parameters at each fixed value of the target parameter (not merely slicing through the likelihood at fixed values). The course explicitly tested this distinction (Q10-02). Without profiles, the reported point estimates are unverified and the biological interpretation of any parameter is unsupported.

To address this, compute profile likelihoods for at least the key parameters (rho, eta, base_beta, outbreak_beta) using the course standard approach: fix the target parameter on a grid of at least 20–30 values (run_level=3) and re-optimize over remaining parameters at each grid point. (Error 1.9, CC-Yes, Major.)

### 3. Measurement model accumulator tracks recoveries, not new infections

In both the SIR and SEIR models, the accumulator variable H is updated as `H += dN_IR` (transitions from I to R), and the measurement model predicts reported cases as proportional to H. This means the model conceptualizes reported cases as proportional to the number of people leaving the infectious compartment — i.e., recoveries.

For pertussis (whooping cough), cases are reported when diagnosed, which typically occurs during or shortly after onset of symptoms — that is, when individuals enter the infectious compartment (transitions S→I in SIR, or E→I in SEIR), not when they leave it. The standard POMP compartmental approach for disease surveillance data is to accumulate new infections: `H += dN_SI` (SIR) or `H += dN_EI` (SEIR). Using I→R transitions systematically shifts the predicted timing of the outbreak peak relative to the observed data, since H captures "resolved" cases rather than "incident" cases. This measurement model mismatch contributes to poor model fit and may be partially responsible for the simulations failing to capture the outbreak surge.

The fix is to replace `H += dN_IR` with `H += dN_SI` (SIR) or `H += dN_EI` (SEIR), corresponding to the transition that best represents the moment of detection in the surveillance system. (POMP Checklist Item #12, Major.)

### 4. Missing convergence diagnostics for the SEIR model used in the ARCH comparison

The SEIR model that produces the comparison log-likelihood of −1442 (the "SEIR Model for ARCH Comparison" section) has its local search trace plots commented out in the code (lines 1134–1141 of blinded.Rmd). This means there is no graphical evidence that the iterated filtering converged for the exact model instance driving the primary comparison result. The reader cannot verify whether the optimizer reached a stable neighborhood of the MLE or whether −1442 is a reliable estimate of the optimized likelihood.

The main SEIR model (not the comparison variant) does show trace plots, but these apply to a slightly different model (with one additional data point). The comparison variant's optimization diagnostics are entirely absent from the rendered output.

To address this, the trace plots for the comparison SEIR model should be rendered and included. At minimum, the log-likelihood panel of the mif2 trace should be shown to confirm convergence. (Error 1.8, CC-Yes, Major.)

### 5. SEIR model consistently fails to capture the outbreak without structural revision

Both the main SEIR global search and the comparison SEIR global search produce simulations that "fail to capture the surge in reported whooping cough cases." The authors correctly acknowledge this failure but treat it only as motivation for future work (births/deaths, better vaccination data), without pursuing iterative model revision.

When a mechanistic model's simulations systematically underperform — even after a 500-point global search from diverse starting values — the appropriate response is to diagnose what structural feature the model is missing. In this case, candidates include: (a) the measurement model accumulating the wrong transition (Issue 3 above), (b) the overdispersion parameter k being fixed at an unjustified value (see Issue 9), (c) the outbreak start time being hard-coded rather than estimated, and (d) the absence of waning immunity (pertussis immunity wanes substantially over 5–10 years, which would affect the susceptible pool). The paper does not systematically work through these possibilities.

Per Error 1.15 (CC-Yes), when the POMP model fits substantially worse than a simpler benchmark, the right first step is to revise model structure — not accept the poor fit and move on. (Error 1.15, CC-Yes, Major.)

---

## Computational and Diagnostic Assessment

**Convergence:** The SIR local search trace plots are shown and the log-likelihood panel appears to converge upward across 50 mif2 iterations. The main SEIR local search also shows trace plots with apparent convergence. However, as noted in Issue 4, the comparison SEIR variant's trace plots are absent. For the global searches, the pairs plots provide some evidence that the optimizer explored the parameter space, but convergence diagnostics (log-likelihood vs. iteration traces for representative runs) are not shown for the global search phase.

**Particle filter:** Replicated pfilter evaluation uses Np=2000 for local searches and Np=5000 for global searches with 10 replicates each, combined via logmeanexp — this is correct course practice. The reported standard errors (loglik.se) are small in the shown outputs, suggesting adequate Monte Carlo precision. ESS is not reported, but this omission is minor.

**Conditional log-likelihoods:** Per-time-step log-likelihoods are not plotted. These would be informative for identifying which time periods (e.g., the 2024 surge) the model fails to explain. Their absence limits diagnostic insight.

**Profile likelihoods:** Not computed for any parameter. This is a major gap as described in Issue 2.

**Computational scale:** The global search uses nseq=500 starting points with Nmif=100 and Np=5000 per evaluation. This is a reasonable effort for a student project. Total CPU time is not reported, which is a minor omission.

---

## Reproducibility Assessment

**Code availability:** Code is included in the submission via the blinded.Rmd file. The bake() calls cache expensive computations to .rds files, which are present in the data/ subdirectory — this is good practice.

**Final parameters:** The best-fit parameter vectors are written to CSV files (whoop_truncated_params_SIR.csv), and the archived .rds files allow rerunning downstream analysis without re-optimizing. This partially satisfies the reproducibility standard.

**Model-code consistency:** The measurement model accumulator (H += dN_IR) is not described in the mathematical specification — the text presents the standard transition equations but does not explicitly state that reported cases are proportional to I→R transitions. This is a specification gap that should be clarified (and likely corrected per Issue 3).

**Package versions:** No sessionInfo() output or renv lockfile is present. Given that pomp's API has changed across versions, results may not be exactly reproducible on a different version.

**Auxiliary data:** All auxiliary data files (births, deaths, vaccination, population) are included in the data/ directory. This is good practice.

**RNG seeds:** Seeds are set for the simulations and bake() calls use per-job seeds via .options.future. This is adequate for approximate reproducibility.

---

## Minor Issues

- **Vaccination data from one state extrapolated to five.** The vaccination coverage used for all five East North Central states comes from Michigan county immunization report cards only. The text notes this limitation but provides no sensitivity analysis. Vaccination hesitancy patterns vary significantly by state, and Indiana and Wisconsin had notably different vaccination coverage trajectories during this period. The assumption of uniform coverage across states is not validated.

- **Overdispersion parameter k fixed without justification.** In the SIR model, k=10 is fixed; in the SEIR, k=5 is fixed. Neither value is estimated or motivated by data. An incorrectly fixed k can cause the measurement model to systematically under- or over-report uncertainty, affecting the particle filter and the reported log-likelihoods. The authors should either include k in the optimization or justify the fixed value by reference to exploratory analysis.

- **Missing data treatment for POMP not stated in text.** The SEIR model handles NA observations via `(ISNA(Cases)) ? 0 : dnbinom_mu(...)`, contributing 0 to the log-likelihood for missing weeks. This is a legitimate approach (treating missing as unobserved) but is never mentioned in the text. The reader has no way to know how the ~127 missing weeks are handled without reading the C snippet.

- **Initial H value set to 1 instead of 0 in SEIR.** In `seir_rinit`, H is initialized to 1 (`H = 1`). The accumulator H should be initialized to 0 at t0 since it accumulates transitions within each observation interval and is reset at each observation. Starting with H=1 biases the first predicted observation.

- **Hard-coded outbreak start time (week 332) not estimated or validated.** The breakpoint between `base_beta` and `outbreak_beta` is fixed at week 332 (April 2024) based on visual inspection of the data. This parameter is not estimated within the model, nor is sensitivity to this choice assessed. Misspecification of the breakpoint could shift the estimated base_beta and outbreak_beta substantially.

- **Unused variable `pertussis_diff_adjusted` in ARCH code.** The variable `pertussis_diff_adjusted <- pertussis_diff[-1]` is created at line 293 but the subsequent `ugarchfit` call uses `data = pertussis_diff` (not `pertussis_diff_adjusted`). While the lengths are equal (both have length(df$Cases)−1), this dead variable suggests the code was modified mid-development and creates unnecessary confusion about which series the model was actually fit to.

- **Differencing applied without formal stationarity test.** The ARMA section differences the pertussis series without first testing whether the series has a unit root (e.g., via ADF or KPSS test). The pertussis time series from 2017–2025 has a clear outbreak in 2024 but otherwise low endemic levels — this is more consistent with a trend-stationary or epidemic-driven process than a unit-root process. If the true data-generating process is trend-stationary, differencing introduces an MA unit root and produces a misspecified model (Error 2.1). At minimum, a formal test or discussion of this choice is warranted.

- **SIR global search parameters are biologically implausible but not fully discussed.** The best SIR global search parameters include beta=259 (per week, far above typical values for pertussis) and mu_IR=6.92 per week (implying an average infectious period of about 1 day, vs. the known pertussis infectious period of 1–3 weeks). The authors note that mu_IR is not identifiable but do not discuss whether these estimates indicate model misspecification beyond the identifiability issue. Per Wheeler et al. (2024) and POMP checklist item #11, implausible parameter estimates should be interpreted as signs of model misspecification and discussed accordingly.

- **ARMA section describes ARMA(2,4) as selected despite convergence problems.** The text notes the selected model "experienced convergence problems" but still uses it for the log-likelihood comparison with ARCH. A model with numerical convergence issues may not reliably represent the local maximum of the likelihood, and multiple starting points (e.g., using arima2::arima) would help confirm the reported log-likelihood. This is relevant to the validity of the ARCH vs. ARMA comparison on the differenced series (Error 2.15).

---

## Recommendation

This project demonstrates genuine engagement with the course material and addresses an interesting real-world problem. The correct use of logmeanexp, bake() caching, replicated pfilter evaluation, and global search with diverse starting points reflect solid implementation skills. However, the work has four issues that should be addressed before the conclusions can be trusted: the ARCH-vs.-POMP likelihood comparison is methodologically invalid as written; no profile likelihoods are computed; the measurement model accumulates the wrong compartmental transition; and the key comparison model lacks convergence diagnostics. Major revision is required to address these issues.

**Priority fixes:**
1. Remove or restructure the ARCH-vs.-POMP likelihood comparison to use the same data for both models.
2. Add profile likelihoods for at least rho, eta, and one beta parameter in the SEIR model.
3. Correct the accumulator to `H += dN_EI` (SEIR) so reported cases correspond to new infections, not recoveries; re-run and re-report all downstream results.
4. Uncomment and include the convergence trace plots for the comparison SEIR model.

---

## Files Consulted

**Skill files — guided-pomp-review:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`

**Skill files — 531_references:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files — W25 Project 16:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project16/data/interpolated_cases.csv`
