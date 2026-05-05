# Review: W25 PROJECT07
## *Dengue Fever in the U.S. States and Territories (2022–2023)*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (iterated filtering, mif2) with particle filter likelihood evaluation |
| **R packages used** | pomp, doFuture, doParallel, doRNG, forecast, denguedatahub (versions not pinned) |
| **Code publicly available** | Partial — Rmd provided in course submission; no external archive or DOI |
| **Data publicly available** | Yes — via `denguedatahub` R package (CDC data) |
| **Benchmark comparison included** | Yes — SARIMA(2,0,0)×(0,0,1)[53] used as benchmark |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 used for both SIRS and SEIR; some parameters fixed ad hoc without justification |
| 2 | Benchmark comparison | ~ | SARIMA benchmark present but comparison is informal and favors POMP models |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported, but no AIC or formal comparison table |
| 4 | Model diagnostics | ~ | ESS and conditional log-likelihoods shown for SIRS only; not for SEIR |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods; no confidence intervals for any parameter |
| 6 | Computational adequacy | ~ | Convergence traces shown; but computation is minimal (run_level=3 with Nglobal=20 for SIRS) |
| 7 | Forecast methodology | N/A | No forecasting objective stated |
| 8 | Model variations and nested comparisons | ~ | SIRS and SEIR compared qualitatively; no likelihood ratio test or AIC comparison between them |
| 9 | Stochasticity | ✓ | Both models use binomial transitions; negative binomial measurement model |
| 10 | Reproducibility and extendability | ~ | bake() used; no archived MLE parameter files as standalone CSVs; package versions absent |
| 11 | Corroboration with scientific knowledge | ~ | Some parameter values rationalized; N=4e9 in SIRS is biologically implausible |
| 12 | Measurement model specification | ~ | Negative binomial used; rho fixed at implausible values without justification |
| 13 | Initial conditions | ~ | Initial conditions partially estimated; fixed N not justified in SEIR |

---

## Summary

The paper models weekly travel-associated dengue cases in the U.S. (2022–2023) using two stochastic compartmental models — SIRS and SEIR — fit via particle filtering and iterated filtering (IF2), with a SARIMA benchmark. The authors implement seasonal transmission forcing, compare local and global parameter searches, and present visual trajectory comparisons. While the project demonstrates competent use of the `pomp` framework and appropriately includes a statistical benchmark, the analysis suffers from absent profile likelihoods, biologically implausible fixed parameters, inconsistent data filtering between the SIRS and SEIR models, and only informal model comparison. Neither model is formally shown to outperform the SARIMA benchmark, and no confidence intervals are reported for any parameter.

**Strengths:**
- Includes a SARIMA benchmark with AIC-based model selection, which is methodologically appropriate.
- Both compartmental models incorporate stochastic process noise (binomial transitions) and overdispersed measurement models (negative binomial).
- ESS and conditional log-likelihood diagnostics are shown for the SIRS model.
- bake() caching is used for computational reproducibility of expensive steps.
- Seasonal forcing is motivated by dengue biology and implemented in both models.

**Weaknesses:**
- No profile likelihoods or confidence intervals are computed for any parameter in either model.
- The SIRS model uses N=4e9 (four billion), far exceeding any plausible U.S. population, while the SEIR model uses N=3.2 million; neither is justified.
- Data construction differs between the two models (different filter conditions on the raw dataset), meaning the two models are not fit to the same data.
- The benchmark comparison is informal: log-likelihoods are reported but no AIC, likelihood ratio test, or formal comparison table between SIRS, SEIR, and SARIMA is presented.
- The SEIR global search is severely underpowered (Nglobal=100 for run_level=3 but the global search block uses `%dopar%` rather than `%dofuture%`, and `run_level` is re-declared mid-script inconsistently).

---

## Major Issues

### 1. No Profile Likelihoods or Confidence Intervals

Neither the SIRS nor the SEIR analysis computes profile likelihoods or reports any confidence intervals for parameter estimates. `Npoints_profile` and `Nreps_profile` are defined in the run-level blocks but never used — no profile likelihood code appears anywhere in the document. Without profiles, it is impossible to assess whether any parameter is identifiable from 106 weeks of data. Given that both models fix several parameters (N, rho in SIRS; N, k in SEIR) and estimate others, the identifiability of the estimated parameters under the fixed-parameter constraints is completely uncharacterized. Wheeler et al. (2024) emphasize profile likelihoods as essential for assessing identifiability; their absence here undermines all conclusions about parameter estimates.

**Fix:** Compute profile likelihoods for at least the key epidemiological parameters (beta/a/b, mu_IR, rho) in both models, report Monte Carlo Adjusted Profile (MCAP) confidence intervals, and discuss whether the profiles show evidence of identifiability or flat likelihood surfaces.

---

### 2. Biologically Implausible and Inconsistent Population Parameters

The SIRS model is initialized with `N=4e9` (four billion individuals) and later the global search fixes `N=3.25e8` (325 million) — the U.S. population. Neither value is explicitly justified in the text, and the initial value of four billion exceeds the entire U.S. population by more than tenfold. The reporting rate `rho=1e-7` used alongside N=4e9 implies that roughly 400 travelers per week are infected out of an effective pool of four billion, which has no epidemiological meaning for a travel-associated case series.

The SEIR model independently sets `N=3200000` (3.2 million) without explanation. This is inconsistent with the SIRS global search parameter of 3.25e8 and with any stated interpretation of N as the U.S. population.

These inconsistencies suggest that N and rho are being used as scale parameters calibrated numerically rather than as biologically interpretable quantities, which violates the interpretability goals of mechanistic modeling. Wheeler et al. (2024) flag implausible parameter estimates as evidence of model misspecification.

**Fix:** Justify the choice of N explicitly. If N represents a "susceptible traveler pool" rather than total U.S. population, state this clearly and provide a principled estimate. Ensure N and rho are consistent across models or explain the difference.

---

### 3. SIRS and SEIR Models Are Fit to Different Data

The SIRS model filters the raw CDC data using:
```r
cdc_casesby_week %>% filter(Travel.status == "All", Year %in% c(2022, 2023))
```

The SEIR model uses:
```r
data <- cdc_casesby_week
data <- data[637:nrow(data), ]
```

The row-index subsetting `[637:nrow(data), ]` is not equivalent to the year-and-travel-status filter used for SIRS. The raw dataset contains multiple travel statuses and years, so row 637 may not correspond to week 1 of 2022 for "All" travel status. As a result, the two models may be fit to different case series. The paper presents them as modeling the same phenomenon and compares their log-likelihoods directly, but this comparison is invalid if the data differ.

**Fix:** Use identical data extraction code for both models, verify the extracted series are equal (e.g., `identical(df_pomp$reports, meas$reports)`), and document the extraction logic clearly.

---

### 4. Informal and Incomplete Model Comparison

The paper's main conclusion is that "the log likelihoods of both the SIRS and SEIR model were close to the baseline of the SARIMA model." However, no formal comparison table is presented, and the comparison is misleading for several reasons: (a) SARIMA log-likelihood is reported as "approximately -445" without a precise value; (b) the SIRS and SEIR log-likelihoods are compared to this approximate figure without reporting standard errors alongside them; (c) no AIC values are computed for the mechanistic models to enable an apples-to-apples comparison with SARIMA's AIC-based model selection; (d) the two mechanistic models are not compared against each other via likelihood ratio test or AIC despite having the same observation model and nested model structure.

Wheeler et al. (2024) note that "log-likelihood or AIC values must be reported for any meaningful model comparison" and that visual comparisons alone are a weak measure. The conclusion that both mechanistic models perform well because their log-likelihoods are "close to" the SARIMA benchmark does not constitute a rigorous comparison.

**Fix:** Present a single comparison table with model name, number of estimated parameters, log-likelihood (with Monte Carlo SE), and AIC for SARIMA, SIRS, and SEIR. Use a likelihood ratio test for nested model comparisons (SEIR vs. SIRS is not nested, but both vs. SARIMA can be compared via AIC). Discuss what "close to" means in the context of model complexity differences.

---

### 5. Global Search Is Severely Underpowered for SIRS

The SIRS global search uses `Nglobal = switch(run_level, 2, 5, 20, 100)`, yielding only 20 search replicates at run_level=3. With 7 free parameters and a 7-dimensional search box, 20 random starting points is insufficient to characterize the global likelihood surface. The pairs plot for the global SIRS search (which should show 20 points) cannot meaningfully reveal the shape of the likelihood surface.

Additionally, the global search bake file is `paste0("global_sirs_",run_level,".rds")` which at run_level=3 is `"global_sirs_3.rds"`. The script reads `guesses` (20 rows) but the `mif2` inside the loop only runs `Nmif=50` iterations from each guess (using the `mf1` object from the local search), giving each guess only a single pass. This is insufficient for a global search; Wheeler et al. (2024) note that computational effort is a primary driver of whether a global search locates the true MLE.

**Fix:** Increase Nglobal to at least 100 for SIRS (consistent with the SEIR value). Run two passes of mif2 from each guess (as shown in the course notes pattern `mif2() |> mif2()`). Report the spread of top log-likelihoods across global search replicates to demonstrate convergence to a consistent maximum.

---

### 6. SEIR Particle Filter Diagnostics Missing

The SIRS section presents ESS and conditional log-likelihood diagnostics via `plot(sirs_pf)`, which is commendable. However, the SEIR section contains no equivalent diagnostics — no ESS plot, no conditional log-likelihood trace, and no assessment of filter health. Given that the SEIR model has an additional compartment (E) and different dynamics, the particle filter may behave differently, and its adequacy should be independently verified.

This is particularly important because the SEIR local search uses only `ncpu` replicates (typically 8 or fewer on a laptop), which may be insufficient to characterize the local likelihood surface reliably.

**Fix:** Add `pfilter` diagnostics for the SEIR model analogous to those presented for SIRS. Show ESS and conditional log-likelihoods at the initial parameters and at the MLE.

---

### 7. Fixed Parameters Not Justified for SEIR (k Fixed at 10)

In the SEIR model, the overdispersion parameter `k` is fixed at 10 throughout — in the local search, global search, and all simulations (`k=10` is hardcoded in every `simulate` and `coef` call). The value `k=10` is not explained or justified; there is no sensitivity analysis and no profile likelihood. Fixing an overdispersion parameter at an arbitrary value when the data show substantial variability can lead to biased estimates of all other parameters that affect the spread of the outcome distribution.

In contrast, the SIRS model estimates `k` (it appears in the parameter estimation search). This inconsistency is unexplained.

**Fix:** Either estimate `k` in the SEIR model (include it in `rw.sd`) or justify its fixed value with reference to external data or a sensitivity analysis. Remove `k` from `fixed_params` if it is being estimated, or add it if fixing is deliberate.

---

### 8. The "Pandemic Switch" in SIRS Is Not Scientifically Motivated

The SIRS model introduces a transmission shift at week 29 (labeled "pandemic week"), switching from parameter `a` to `b`. The authors state they set `a > b` because "the second peak after week 29 is larger than the first peak." However, the data covers 2022–2023, well into the post-pandemic period, and the use of the term "pandemic week" without any biological or epidemiological justification for a structural break at that specific week is ad hoc.

The model implies a permanent change in dengue transmission dynamics at a single calendar week (week 29 of the 106-week series, corresponding roughly to mid-July 2022), with no explanation of what epidemiological event this represents. This is a structural change to the model justified purely by visual inspection of the data, which risks overfitting.

**Fix:** Justify the "pandemic switch" biologically (e.g., a specific policy change, surveillance shift, or ecological event). If no justification exists, remove it or treat it as a sensitivity analysis. Alternatively, compare a model with the switch against one without it using a likelihood ratio test.

---

## Computational and Diagnostic Assessment

**Convergence:** The SIRS local search shows convergence traces across MIF2 iterations for all parameters, which is good. The SEIR local search also shows traces. However, neither model presents a scatter plot of final log-likelihoods across all global search replicates (only the best result is reported for SEIR), making it difficult to assess whether the global search consistently locates the same optimum.

**Particle filter:** ESS diagnostics are presented for the SIRS initial parameter filter. ESS occasionally dips near seasonal transitions, which the authors note. No equivalent diagnostics are shown for SEIR, which is a gap.

**Conditional log-likelihoods:** Per-time-step log-likelihoods are shown for the initial SIRS filter. These are not presented for the post-optimization parameters or for SEIR.

**Profile likelihoods:** None computed. `Npoints_profile` and `Nreps_profile` are defined but the profile likelihood code is absent from the document entirely. This is the single most critical missing element.

**Computational scale:** The SIRS global search uses 20 replicates with 50 MIF2 iterations and 1000 particles. The SEIR global search uses 100 replicates at similar settings. Total CPU hours are not reported. The computation is modest for a 106-observation time series with a simple model, but it is not clearly insufficient — the concern is the small number of global search replicates for SIRS.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file submitted to the course. There is no external archive (GitHub, Zenodo) with a DOI.

**Final parameters:** Intermediate CSV files (`sirs_lik.csv`) are written and read back within the script. However, the final MLE parameter vectors are not archived as standalone files; results depend on the bake RDS files being present in the working directory. The bake files are not submitted with the project.

**Model-code consistency:** The measurement model is `dnbinom_mu(reports, k, rho*H, give_log)` in both SIRS and SEIR. The text describes a negative binomial observation model with mean `rho*H`. This is consistent. However, the SEIR model hardcodes `k=10` in simulation calls while removing `k` from the search, creating a mismatch between the model as estimated and the model as simulated after the global search (the global search fixes `k` via `fixed_params = coef(measSEIR, c("N","k"))`, so this is internally consistent but the value is never justified).

**Package versions:** No `sessionInfo()` output is included. The `denguedatahub` package version is not specified; the row-index subsetting in the SEIR data construction `data[637:nrow(data),]` will break silently if the package is updated and the row count changes. The `pomp` version is not pinned.

**Auxiliary data:** Data is pulled from the `denguedatahub` package at run time. This is convenient but means results depend on the package version and the current CDC data, both of which may change.

**HPC reproducibility:** No cluster computing was used; analysis runs locally. This is acceptable for the scale of this project.

---

## Minor Issues

- The SARIMA log-likelihood is reported as "approximately -445" without a precise value. The actual value from `print(sarima)` should be cited exactly.
- The introduction states that both SARIMA and POMP models are fitted "to benchmark performance," but the SARIMA model is presented as the benchmark for the POMP models, not the reverse. The framing should be clarified.
- The `run_level` variable is declared twice in the SIRS section (lines ~339 and ~930), creating a risk of inconsistent settings if the document is partially re-run.
- The `%dopar%` operator is used in the SEIR global search while `%dofuture%` is used in the SIRS global search. These require different backend registrations and the mixing is inconsistent.
- The color `531` in the data plot (`geom_line(color = 531)`) will be interpreted as a numeric color code by ggplot2 rather than a meaningful named color; this appears to be a course in-joke but may produce unexpected rendering behavior.
- The SARIMA model selection table is computed over a grid that includes d=0 (no differencing) despite the ACF analysis suggesting non-stationarity. The choice of d=0 should be justified or d=1 models should also be considered.
- The ACF analysis concludes from oscillating ACF that the series is "non-stationary," but oscillating ACF is consistent with a stationary seasonal AR process. The stationarity interpretation is incorrect; a formal unit root test (ADF, KPSS) should be used.
- The SEIR initial conditions fix `E=10` and `I=70` as constants rather than estimating them, with no sensitivity analysis. For a 106-week series, initial conditions in 2022 may materially affect fit.
- References [2] acknowledges that two helper functions were generated with ChatGPT, which is appropriate to disclose; however no description of how those functions were validated is given.
- Several simulation plots use `theme(legend.position = c(0.2, 0.85))` followed immediately by `theme_minimal()`, which resets the legend position. The legend position customization has no effect.

---

## Recommendation

**Major Revision.**

The paper makes a reasonable attempt at mechanistic modeling of dengue fever dynamics using the `pomp` framework, with an appropriate benchmark comparison and stochastic model formulation. However, three critical deficiencies prevent acceptance in the current form: (1) the complete absence of profile likelihoods or confidence intervals for any parameter, making identifiability assessment impossible; (2) inconsistent data construction between the SIRS and SEIR models, which invalidates the head-to-head log-likelihood comparison that is central to the conclusion; and (3) biologically implausible and unjustified population parameters (N=4e9 for SIRS). These issues require substantive revision. The informal benchmark comparison and the underpowered SIRS global search also need to be addressed before the results can be considered reliable.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project07/blinded.Rmd`
