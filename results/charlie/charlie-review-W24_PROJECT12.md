---
title: "Review: W24 Project 12"
subtitle: "*Time Series Analysis of COVID-19 Cases in Kent County*"
---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | Iterated filtering (IF2) via `mif2`, particle filter (`pfilter`), profile likelihood |
| **R packages used** | pomp, forecast, tidyverse, doParallel, foreach, doRNG, kableExtra, readxl, lubridate |
| **Code publicly available** | Yes (Rmd, cached `.rds` bake files, Makefile in submission folder) |
| **Data publicly available** | Yes (`mi_covid.xlsx` included; public Michigan state source cited) |
| **Benchmark comparison included** | Yes — ARMA(2,1) on log(y+1)-transformed data with Jacobian correction |

---

## POMP Checklist Scorecard

*✓ = satisfies practice, ~ = partially satisfies, ✗ = does not satisfy, N/A = not applicable*

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ✓ | IF2 + replicated `pfilter`/`logmeanexp` pattern used correctly |
| 2 | Benchmark comparison | ~ | ARMA(2,1) with correct Jacobian correction; gap of 32.5 log-units misstated as "quite close" |
| 3 | Quantitative goodness-of-fit reporting | ~ | Loglik reported numerically; no AIC or other metric; gap to benchmark dismissed |
| 4 | Model diagnostics | ~ | ESS/conditional-loglik plot shown; failures noted narratively but not investigated |
| 5 | Parameter identifiability and uncertainty | ✗ | Only one of 13 parameters profiled; profile is sparse and self-described as "dubious" |
| 6 | Computational adequacy | ~ | Run_level=3 with Np=5000, Nmif=200; most local runs plateau far from best; no CPU-hours reported |
| 7 | Forecast methodology | N/A | No forecasting task |
| 8 | Model variations and nested comparisons | ✗ | No SEIR-vs-SEIRS nested test despite this being the paper's stated motivation |
| 9 | Stochasticity | ✓ | Gamma white noise on force of infection; discretized/censored-normal measurement model |
| 10 | Reproducibility and extendability | ~ | Code runs; MLE archived to `covid_params.csv`; no `sessionInfo()`/package pinning |
| 11 | Corroboration with scientific knowledge | ~ | µ_RS≈0 flagged as implausible but not followed up with nested test |
| 12 | Measurement model specification | ✓ | dmeasure/rmeasure Csnippets match the text formula exactly |
| 13 | Initial conditions | ~ | η estimated; no sensitivity check on N or I(1)=1 |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

This project fits a time-varying-β, time-varying-ρ SEIRS model to 212 weeks of weekly COVID-19 case counts in Kent County, Michigan (February 2020–March 2024) and evaluates it against a log-ARMA(2,1) benchmark. The authors demonstrate competent use of the course workflow: a properly Jacobian-corrected benchmark likelihood, thorough local and global IF2 searches at run_level=3, diagnostic pairs and trace plots, a profile likelihood for one parameter, and code that reproduces against cached `.rds` objects. However, the paper's most important analytical claim — that extending from SEIR to SEIRS is scientifically worthwhile — is never directly tested (no nested comparison, and the fitted µ_RS ≈ 0 is never used to trigger a structural revision). The SEIRS model falls 32.5 log-likelihood units short of the ARMA benchmark, yet the Conclusion describes this gap as "quite close." The single profiled parameter (ρ₃) is acknowledged by the authors themselves to rest on a "dubious" interval. Together these issues leave the paper's headline interpretations unsupported.

**Strengths:** Correct Jacobian-corrected ARMA benchmark; correct diagnosis of AIC-table optimizer failures; thorough IF2 search (run_level=3, 40 local + 200 global starts); final MLE parameters archived to a standalone CSV; code runs without errors against cached `.rds` files; measurement model in code matches the text.

**Weaknesses:** Largest gap — the SEIRS-vs-SEIR question the paper is built around is never resolved via a nested test or µ_RS profile; the 32.5-unit benchmark gap is misstated as small; only one parameter is profiled and that profile is sparse; local search convergence is poor for most replicates; no structural remediation is attempted despite identified filtering failures.

---

## Major Issues

### 1. SEIRS model underperforms the ARMA benchmark by 32.5 log units; gap misstated as small and no structural revisions attempted

The Benchmark Comparison table reports log-likelihoods of −1371.5 (ARMA(2,1)) vs. −1404.0 (SEIRS), a difference of 32.5 units. The Conclusion states "the log-likelihood of our SEIRS model is quite close to that of the log-ARMA model," which is inaccurate. A 32.5-unit log-likelihood gap corresponds to an overwhelming likelihood ratio, not a marginal one.

Per course guidance (Ch. 17): "If the mechanistic model fits disastrously compared to the benchmark, our model is probably missing something important." The course-confirmed error (531-weakness-reference Error 1.15) is to respond to a poor-fitting model by increasing Np or Nmif rather than revising model structure. Here the authors have already run at run_level=3, so the computation is sufficient — the problem is structural. The paper identifies candidate causes (holiday reporting anomalies, possible model misspecification at specific time points from the ESS/conditional-loglik failures) but defers all remediation to "future work" without attempting a single structural fix. The authors should consider concrete alternatives: adding a holiday-period reporting covariate, testing whether two rather than three transmission-rate regimes are supported, or examining whether the importation rate ι is absorbing unexplained variation.

### 2. No nested SEIR vs. SEIRS comparison despite µ_RS ≈ 0 being the paper's central finding

The paper's stated scientific motivation is that the SEIRS extension (waning immunity) more accurately reflects COVID-19 biology. The optimal global parameters yield µ_RS ≈ 0.0006 week⁻¹, corresponding to a roughly 30-year immune duration. The authors themselves note: "we question its inclusion in the construction of our model because a recovery period of roughly 20 years is not intuitive." This observation directly motivates a nested likelihood-ratio test — fit a SEIR model (µ_RS=0) with the same IF2 protocol and compare via `2*(loglik_SEIRS − loglik_SEIR) ~ chi²_1`. Per POMP checklist items #5 and #8, implausible parameter estimates should be used to diagnose model misspecification or to test model variants, not left as a curiosity in the discussion. Without this test, the paper cannot support its claim that the SEIRS framework is an improvement, and indeed the near-zero µ_RS suggests the SEIRS extension provides little to no benefit.

### 3. Profile likelihood target parameter ρ₃ is perturbed during mif2, violating course standard

The profile computation uses the same `params_rw.sd` object as the global search. This object includes:

```r
rho3 = ifelse(data_weekly$week_num >= 125, 0.02, 0),
```

The course standard (531-conventions.md, Ch. 16, p57) is explicit: "The target parameter is NOT perturbed in mif2 during profile computation." When rho3 carries a nonzero `rw.sd` during the profile mif2, it drifts away from its intended grid starting value. The resulting profile evaluates the likelihood at whatever ρ₃ happens to land after 200 mif2 iterations, not at the intended grid values. The `group_by(round(rho3,5))` step at the end attempts to recover the profile by grouping on the final ρ₃ value, but since ρ₃ drifts freely, the final values need not cover the intended 0–1 range evenly. This likely contributes to the "only 4 points above the threshold" phenomenon the authors themselves identify. **Fix:** zero out rho3's random walk standard deviation in a profile-specific `rw.sd` specification.

### 4. Profile likelihood for ρ₃ is too sparse (11 points at run_level=3; standard is 30)

The profile grid is `seq(0, 1, by=0.1)`, yielding 11 distinct ρ₃ values. The course standard for run_level=3 is approximately 30 profile points (531-conventions.md). With only 11 starting values and only 4 of those producing likelihoods above the Wilks 95% threshold, the maximum of the profile is not clearly resolved and the CI endpoints (0.37 to 1.0) are unreliable. This is the course-confirmed error (531-weakness-reference Error 1.9, Major severity): "A profile likelihood must have enough points to clearly show the maximum and identify where the likelihood drops by the Wilks threshold." The authors note this explicitly ("may result in a dubious interval") but do not attempt to fix it. **Fix:** rerun the profile with ≥30 grid points, and also zero out the rho3 perturbation as noted in Issue 3.

### 5. Only one of thirteen parameters profiled; identifiability of key parameters unassessed

Profile likelihoods are computed only for ρ₃. The model has 13 free parameters (b1, b2, b3, ρ₁, ρ₂, ρ₃, µ_EI, µ_IR, µ_RS, η, τ, σ_SE, ι). The local and global pairs plots reveal ridges (b1, b2, b3 are positively correlated; ρ₁ and ρ₂ form a ridge), and µ_RS is at a biological boundary. Per POMP checklist #5, profile likelihoods should be computed for parameters whose identifiability is in question. Without profiles for at least µ_RS (the parameter motivating the whole model extension) and for any of the three transmission rates, the paper cannot report meaningful confidence intervals or assess whether the data support separate values of b1, b2, and b3.

### 6. Local search convergence: most runs plateau far from the best result

The text states that local search loglik traces "increase before plateauing around a log-likelihood of roughly −1,500," while the best local result is −1413.6 — approximately 86 log-likelihood units better. This large spread among 40 replicates (31 of 40 runs apparently stuck at ~−1500 while 1 reached −1413.6) indicates severe difficulty in the optimization landscape. Per POMP checklist #6, convergence evidence requires multiple searches reaching *similar* terminal likelihoods; a 86-unit spread among replicates is not consistent with convergence. While the global search later finds −1404.0 (9.6 units further), the fact that most searches fail to approach the apparent MLE raises the concern that even −1404.0 may not be near the true maximum of this 13-parameter likelihood. The global search convergence is described in terms of pairs-plot geometry only; no global-search trace plots analogous to the local-search trace plots are shown.

### 7. No convergence traces shown for the global search

The local search displays loglik and parameter trace plots across mif2 iterations for all 40 replicates (Figure local-diag). The global search displays only `plot(global_mifs)`, which in the pomp package plots the particle-filter ESS and conditional log-likelihood over time for a single mif2 object — this is a time-series diagnostic, not a convergence diagnostic. No analogue of the local-search trace plots (loglik vs. mif2 iteration, for all 200 global-search replicates) is shown. Per course conventions and POMP checklist #6, the loglik panel consistently converging upward across runs is the required evidence of convergence (531-conventions.md: "the loglik panel should be consistently converging upward across runs"). Omitting this display for the analysis stage that produces the paper's reported MLE is a gap in the convergence documentation. (This is Error 1.8 in 531-weakness-reference, Major severity.)

---

## Computational and Diagnostic Assessment

**Convergence:** Local search (40 replicates, Nmif=200, Np=5000) shows loglik converging in the trace plots, but most runs plateau ~86 units below the best result, indicating the optimization landscape is difficult and most replicates are stuck in suboptimal regions. Global search (200 starts) improves by only 9.6 units over the best local result; no convergence traces (loglik vs. iteration) are shown for the global runs.

**Particle filter:** ESS and conditional log-likelihood over time are shown via `plot(global_mifs)` for one mif2 object. "Points of failure" are visible but not quantified (no count of collapsed weeks, no numeric ESS threshold). The minimum ESS from the initial parameter exploratory pfilter is computed in an `include=FALSE` chunk and not reported.

**Conditional log-likelihoods:** Shown only via the generic `plot()` diagnostic for a single mif2 object; not isolated in a dedicated figure with date annotations, despite visible failures around the holiday season.

**Profile likelihoods:** Only ρ₃ is profiled, with 11 grid points, a perturbed target parameter, and a self-described "dubious" interval. No profiles for µ_RS, b1/b2/b3, ι, or σ_SE.

**Computational scale:** No CPU-hours, wall-clock time, or cluster specification reported, despite `Sys.getenv('SLURM_NTASKS_PER_NODE')` indicating HPC use. Readers cannot assess whether additional computation (wider search box, more profile points) was infeasible.

---

## Reproducibility Assessment

**Code availability:** Rmd, Makefile, image asset, and raw data (`mi_covid.xlsx`) all present in the submission folder. No external repository or DOI (not required for course projects per 531-conventions.md).

**Final parameters:** Accumulated to `covid_params.csv` via write_csv at multiple stages — satisfies POMP checklist item 10. MLE vectors can be read without re-running optimization.

**Model-code consistency:** Verified by reading the Csnippets against the mathematical description. The dmeasure/rmeasure correctly implement the censored-normal formula (mean = ρ(t)H, variance = (τH)² + ρ(t)H). The covariate breakpoints (weeks 54, 72 for β; weeks 54, 125 for ρ) match the stated date ranges. No text/code discrepancy found.

**Package versions:** No `sessionInfo()`, no `renv`/`packrat` lockfile, and no explicit pomp version statement. The pomp API has changed substantially across versions; without version pinning, reproduction is not guaranteed on future releases.

**Auxiliary data:** All inputs present in the submission folder; no external covariate files needed.

**HPC reproducibility:** No SLURM or PBS job-submission scripts; no node/memory/walltime specifications. Exact computational environment is not documented.

---

## Minor Issues

- The `Nsim` parameter is set to 500 at run_level=3 but is never used; the actual simulation figures use `nsim=20` (initial) and `nsim=5` (final). Five simulations is low for visually assessing the spread of model trajectories.

- The measurement model is described as "discretized normal distribution, truncated at zero" but the Csnippet implements a *censored* (not truncated) formulation: the probability mass for sub-zero outcomes is added to the bin at reports=0 without renormalizing. This is a standard course pattern (matching the measles case study) but the terminology in the text is imprecise.

- The β(t) and ρ(t) piecewise functions have different breakpoints (β changes at weeks 54 and 72; ρ changes at weeks 54 and 125). The choice to use *different* breakpoints is not discussed or justified; if both processes are responding to the same epidemiological events, the asymmetry requires explanation.

- The reported ρ₃ > ρ₂ in the optimal parameters contradicts the authors' stated hypothesis ("we suspect a higher reporting rate" in interval 2 than interval 3). The authors note this but offer no explanation. A plausible driver (home testing supplanting official reporting in 2022–2024) should be discussed.

- No `sessionInfo()` output or package-version documentation anywhere in the report or supplement, making exact reproduction uncertain across pomp versions.

- The AIC-table maximization failures (Section "AIC Table") are correctly identified as optimizer failures, a strength. However, the authors do not attempt to resolve these via multiple starting points (e.g., arima2::arima), so the chosen ARMA(2,1) benchmark is based on a fit that triggered a convergence warning (though the practical impact appears minimal based on the loglik values).

- The initial guess for ι is 10, while the final MLE is approximately 200—an order of magnitude difference. No comment on this discrepancy appears before the global-search results section, leaving the reader uncertain whether this is expected or surprising.

- No sensitivity analysis for fixed parameters N=659,000 or I(1)=1 (POMP checklist item 13).

---

## Recommendation

**Major Revision.** The project correctly implements the course's IF2 workflow and produces reproducible results, but three structural gaps prevent it from supporting its key claims: (1) the central SEIRS-vs-SEIR question is unresolved (no nested test, µ_RS ≈ 0 not acted upon); (2) the 32.5-unit benchmark gap is understated as "quite close" with no structural fix attempted; and (3) the single profiled parameter has a sparse, methodologically flawed profile that the authors themselves call "dubious." Before this analysis can be presented as complete, it requires at minimum: a nested SEIR comparison or µ_RS profile; a corrected profile likelihood for ρ₃ with ≥30 grid points and rho3's rw.sd zeroed out during the profile mif2; and a candid discussion of what the benchmark gap implies about model adequacy.

---

## Files Consulted

**Skill files (Skills/guided-pomp-review/):**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`

**Skill files (Skills/531_references/):**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files (projects_Material/project/final_project_W24/project12/):**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project12/blinded.html`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project12/Makefile`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project12/seirs_figure.png`
