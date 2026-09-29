# Peer Review: W25 Project 14
## Influenza Case Trends in Nova Scotia: Capturing the Seasonal Behavior

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) with particle filter likelihood evaluation |
| **R packages used** | pomp, tidyverse, doFuture, doParallel, doRNG |
| **Code publicly available** | Partial — R scripts and pre-computed RDS files in project directory |
| **Data publicly available** | Yes — Nova Scotia lab-confirmed influenza cases CSV included |
| **Benchmark comparison included** | No — ARIMA and POMP sections are separate with no joint log-likelihood comparison |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + replicated pfilter used for SEIRS/SIR; single-run pfilter in conclusion comparison |
| 2 | Benchmark comparison | ✗ | ARIMA analyzed but never compared to POMP by log-likelihood |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported per section; final comparison is unreliable (see Issue 3) |
| 4 | Model diagnostics | ~ | Trace plots and ESS shown for SEIRS and SIRS; SIR has none |
| 5 | Parameter identifiability and uncertainty | ~ | Profile likelihood for rho only; CI is degenerate |
| 6 | Computational adequacy | ~ | run_level=3 for SEIRS; SIR and SIRS use fewer replicates |
| 7 | Forecast methodology | N/A | No forecasting attempted |
| 8 | Model variations and nested comparisons | ~ | SIR, SIRS, SEIRS compared; final comparison is flawed |
| 9 | Stochasticity | ~ | Process noise via binomial Euler; NegBin measurement for SIR/SEIRS; SIRS uses Poisson |
| 10 | Reproducibility and extendability | ~ | RDS files included; no sessionInfo or package versions |
| 11 | Corroboration with scientific knowledge | ~ | Some parameter interpretation; biologically implausible SIRS population size |
| 12 | Measurement model specification | ~ | NegBin for SIR/SEIRS; Poisson for SIRS; inconsistent |
| 13 | Initial conditions | ~ | Estimated as fractions for SEIRS; fixed N in SIRS at wrong population size |

---

## Summary

This project applies time series methods to weekly lab-confirmed influenza case counts in Nova Scotia (2014–2019, ~261 observations). The authors perform EDA with spectral analysis, fit ARIMA models to differenced data, and then develop three POMP compartmental models of increasing biological complexity: SIR, SIRS, and SEIRS. The SEIRS model achieves the best log-likelihood (-586.6) and the authors conclude it is the most appropriate framework for capturing Nova Scotia influenza dynamics.

**Strengths:** The progression from SIR to SIRS to SEIRS is well-motivated; the SEIRS model correctly uses negative binomial overdispersion and is implemented with HPC-scale iterated filtering (run_level=3, 100 global starting points). Pre-computed RDS files are archived, enabling reproduction of downstream results without re-running expensive optimization. ESS diagnostics and convergence trace plots are shown for the SEIRS and SIRS models.

**Weaknesses:** The project contains several critical flaws. The SIRS model is parameterized with N = 3.25×10^8 (approximately the US population) rather than Nova Scotia's ~969,400, rendering all SIRS parameter estimates nonsensical. The final model comparison in the conclusion uses a single unreplicated particle filter call per model and produces an impossible positive log-likelihood (+19,821) for the SIRS model. No log-likelihood comparison between the ARIMA model and any POMP model is ever made, so the claim that mechanistic modeling adds value over a simple benchmark is unsubstantiated. The profile likelihood CI for rho is degenerate (a single-point interval with min = max = 0.001769433).

---

## Major Issues

### 1. No non-mechanistic benchmark comparison (CC-Yes Error 1.6)

The project performs a separate ARIMA analysis and a separate POMP analysis, but never compares them numerically. The conclusion presents log-likelihoods only across the three POMP models (SIR, SIRS, SEIRS) and does not include the ARIMA log-likelihood. Without a benchmark comparison, there is no evidence that the mechanistic model adds value over a simple statistical model. The course explicitly taught this validation step (Q11-01), and Wheeler et al. (2024) note that none of the reviewed Haiti cholera papers performed such a comparison — a gap they identify as a systematic weakness in the field. The authors should compute the log-likelihood of their chosen ARIMA model on the same observed data and the same scale as the POMP models, then compare directly.

### 2. SIRS model uses US population size (N = 3.25×10^8) instead of Nova Scotia population

The SIRS pomp object is constructed with `N = 3.25e8` (line 636 of blinded.Rmd), which is approximately the 2019 United States population. The study region is Nova Scotia, whose population is approximately 969,400 — a factor of ~335 smaller. The SEIRS model (and the real-world context described in the text) correctly uses N = 969400. The force of infection term `beta * I / N` in the SIRS model is therefore ~335 times too small for any given I, making all density-dependent transmission parameters estimated by this model biologically meaningless. Every parameter value reported for the SIRS model (a, b, rho, mu_IR, mu_RS) must be interpreted against this inflated population denominator and cannot be compared to the SIR or SEIRS parameter estimates.

### 3. Single unreplicated pfilter used for final model comparison; impossible positive log-likelihood (CC-Yes Error 1.4)

The conclusion's model comparison (lines 1351–1357) computes each model's log-likelihood with a single `pfilter` call:

```r
loglik_sir  <- logLik(pfilter(mif_sir, Np = 2000))
loglik_seir <- logLik(pfilter(mif_seirs, Np = 2000))
loglik_sirs <- logLik(pfilter(mif_sirs, Np = 2000))
```

No `logmeanexp` aggregation over replicates is applied. Each of these is a noisy Monte Carlo estimate; comparing single runs can reverse the relative ordering of models purely due to sampling noise. The course explicitly requires replicated pfilter + logmeanexp for reliable log-likelihood comparison (Q9-02). Furthermore, the reported SIRS log-likelihood of +19,821.71 is physically impossible: a properly specified Poisson measurement model for non-negative count data cannot produce a positive total log-likelihood of this magnitude over 261 observations. This value indicates either a code failure or a corrupted model object, and it invalidates the conclusion's model ranking.

### 4. Wrong index used to extract best SIRS model in conclusion

In the conclusion code (lines 1343–1347), `best_index` is taken from the SIR section:

```r
mif_sir  <- local_fits[[best_index]]         # best_index = SIR best fit (1–5)
mif_sirs <- local_mifs_sirs[[best_index]]    # uses SIR index for SIRS — wrong
best_index <- which.max(unlist(local_ll_seir[, "loglik"]))
mif_seirs <- local_mifs_seir[[best_index]]
```

`local_mifs_sirs` contains 10 local SIRS fits (Nlocal=10), but the index used to select among them is derived from the SIR model's 5 fits. No `which.max` over SIRS local log-likelihoods is ever computed. This means `mif_sirs` does not necessarily contain the best SIRS local fit, and the SIRS log-likelihood reported in the conclusion is from an arbitrary SIRS chain rather than the best-found chain. This contributes to the implausible SIRS log-likelihood of +19,821.71.

### 5. No convergence trace plots for SIR model iterated filtering (CC-Yes Error 1.8)

The SIRS section (lines 762–779) and the SEIRS section (loaded from seirs_ls.RDS) both present mif2 trace plots demonstrating parameter and likelihood convergence. The SIR section shows no trace plots at all — the local search is summarized only by a table of final log-likelihoods and a visual comparison of simulated vs. observed cases. Without trace plots, there is no evidence that the SIR optimizer converged to a stable likelihood region or that the five local runs achieved comparable terminal log-likelihoods. The course teaches trace plots as the minimum standard for convergence assessment (Q10-01, Q10-03).

### 6. Profile likelihood confidence interval is degenerate

The 95% CI computed for the reporting rate rho has `min = max = 0.001769433` — a single-point interval (lines 1331–1333 of blinded.Rmd). Only one value of rho satisfies the Wilks threshold `max(loglik) - 1.92`, meaning the profile either has too few rho values near the maximum to bracket a meaningful interval, or the rho grid is misaligned relative to the actual MLE. The authors themselves note that "the reporting rate from our best-fit parameters (0.001132336) lies outside the 95% confidence interval," acknowledging that the global search maximum and the profile maximum are inconsistent — a sign that the profile is not adequately covering the parameter space. A valid profile must have enough distinct rho values to bracket both endpoints of the Wilks interval.

### 7. Inconsistent measurement models across POMP models undermine cross-model comparison

The SIR model uses negative binomial measurement (`dnbinom_mu`, line 293), the SEIRS model uses negative binomial (`dnbinom_mu`, line 1144), but the SIRS model uses Poisson measurement (`dpois`, line 610). The Poisson model has no overdispersion parameter, which is a known inadequacy for weekly disease count data. More critically, the log-likelihoods from Poisson and negative binomial measurement models are not on the same scale for the same data: they represent different probability models and cannot be directly compared without acknowledging that the log-likelihood differences reflect both model fit and distributional assumptions. The conclusion compares log-likelihoods across all three models as if they were computed under equivalent assumptions, which they are not.

---

## Minor Issues

- **Log-likelihood comparison direction misstated (conclusion):** The text states "SEIRS model performs best, with the lowest value of -590.46" (line 1358). This is backwards: in log-likelihood, higher is better. -590.46 is the highest (least negative) among the three POMP models, indicating the best fit, not the lowest. The SIRS model with loglik +19,821.71 is described as having "a much higher value," which the authors appear to interpret as worse — but they provide no explanation for why a positive loglik is treated as evidence of poor fit.

- **Inconsistent observation count:** Two consecutive sentences in the EDA section report different sample sizes: "The dataset contains 262 observations" followed immediately by "We have 261 observations in our dataset." The data filtered from 2014-09-06 to 2019-09-07 produces one of these counts; a definitive statement with verification is needed.

- **Unit error in data summary:** The text states "the median being 1 cases per day" (EDA section), but the data are weekly counts. The correct statement is 1 case per week. This error propagates to the interpretation of the distribution.

- **ARIMA differencing lacks unit root justification:** The authors observe gradual ACF decay and immediately proceed to difference the series, concluding d=1 is needed. No ADF test or structural break analysis is performed to distinguish a unit root process from a trend-stationary process. For seasonal disease data, the choice between differencing and detrending has implications for model validity.

- **H accumulator tracks recoveries rather than symptom onset:** In both the SIR model (`cases = dN_IR`, line 282) and the SEIRS model (`H += dN_IR`, line 1132), the observation proxy accumulates I→R transitions (recoveries). Influenza cases are clinically reported at symptom onset, which corresponds to the E→I transition in the SEIRS model (`dN_EI`). Using recoveries introduces a systematic lag of approximately 1/mu_IR weeks relative to reported onset. For weekly data with mu_IR ≈ 2 per week (half-week infectious period), this lag is small but biologically inconsistent with the stated purpose.

- **SIRS global search uses only 3 pfilter replicates for likelihood evaluation:** In the SIRS global search code (line 956 of blinded.Rmd), `ll_vals <- replicate(3, logLik(pfilter(mf, Np = 1000)))`. The SEIRS and SIR analyses use 10 and 5 replicates respectively. Three replicates with Np=1000 produces higher Monte Carlo variance in the log-likelihood estimates, making the SIRS global search results less reliable than those from the other models.

- **No package versions or sessionInfo provided:** The project provides no `sessionInfo()` output, no `renv.lock`, and no explicit version pins for `pomp` or other packages. The `pomp` API has changed substantially across CRAN versions; results may not reproduce on a different installation. As noted in the POMP code supplement checklist, pomp and spatPomp version pinning is essential for reproducibility.

- **Duplicate and inconsistent data loading across sections:** The data file `Lab-confirmed_Influenza_Cases.csv` is loaded and filtered independently in at least three separate code chunks (SIR, SIRS, SEIRS sections), using slightly different column renaming conventions (`cases_obs` for SIR, `cases` for SIRS/SEIRS, `week` vs `time` as the time variable). While each POMP object uses its own consistently named columns, the repeated loading makes it harder to audit data consistency across models and creates a maintenance risk if filtering criteria are ever changed.

---

## Recommendation

**Major Revision.** The project demonstrates a sound conceptual approach — progressing from SIR to SEIRS with seasonal forcing, using HPC-scale iterated filtering, and archiving pre-computed results. However, several critical issues must be addressed before the analysis is reliable:

1. The SIRS model must be corrected to use Nova Scotia's population (N ≈ 969,400) and its results re-evaluated.
2. The conclusion's model comparison must use replicated pfilter + logmeanexp, and must correctly extract each model's best-found fit.
3. A log-likelihood comparison between the chosen ARIMA model and the best POMP model must be added to substantiate the claim that mechanistic modeling adds value.
4. The profile likelihood must be recomputed over a designed rho grid with enough points to produce a non-degenerate CI, or the authors must acknowledge its limitations explicitly.
5. Convergence trace plots must be shown for the SIR model's iterated filtering.

---

## Files Consulted

**Skill files:**

- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**

- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project14/seirs_gs.R`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project14/seirs_ls.R`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project14/seirs_pf.R`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project14/influenza_params.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project14/sirs_lik.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project14/README`
