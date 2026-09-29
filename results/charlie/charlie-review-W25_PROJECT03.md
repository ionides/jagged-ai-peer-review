# Review: W25 PROJECT03
## *Flu Cases in Michigan*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) via iterated filtering, local and global search |
| **R packages used** | pomp, forecast, ggplot2, doParallel, doRNG |
| **Code publicly available** | Yes — Git repository (no separate DOI archive) |
| **Data publicly available** | Yes — CDC FluView (flu_michigan.csv included in repo) |
| **Benchmark comparison included** | Yes — ARMA and SARMA compared to POMP by log-likelihood (but comparison is invalid; see Major Issue 1) |

---

## POMP Checklist Scorecard

*checkmark = satisfies practice, ~ = partially satisfies, x = does not satisfy, N/A = not applicable*

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2 used correctly; but profile and local-search likelihood evaluation are noisy (single pfilter) |
| 2 | Benchmark comparison | ~ | ARMA/SARMA comparison attempted but invalid (different response variables) |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported but comparison is not apples-to-apples |
| 4 | Model diagnostics | x | Only visual simulation comparison; no ESS monitoring, no conditional log-likelihoods |
| 5 | Parameter identifiability and uncertainty | ~ | Profile likelihood attempted but too sparse, single pfilter per point, only 4 of 8 parameters covered |
| 6 | Computational adequacy | ~ | Global search uses only 10 starts; no convergence traces for global search |
| 7 | Forecast methodology | N/A | No forecasting conducted |
| 8 | Model variations and nested comparisons | x | No alternative model structures tested |
| 9 | Stochasticity | checkmark | Binomial transitions with exponential probabilities; negative binomial measurement model |
| 10 | Reproducibility and extendability | ~ | Code present; data path in Rmd is incorrect; no package version pinning |
| 11 | Corroboration with scientific knowledge | x | No R0 or epidemiological parameter interpretation |
| 12 | Measurement model specification | ~ | H tracks I->R flow (recoveries) rather than E->I flow (new cases); introduces unmotivated lag |
| 13 | Initial conditions | checkmark | Population-proportion initialization estimated as parameters |

---

## Summary

The paper applies ARMA, SARMA, and a SEIRS POMP model to weekly influenza case counts in Michigan (2023–2025), asking whether POMP can effectively capture flu dynamics. The SEIRS model incorporates a cosine seasonal transmission function, is fitted via iterated filtering (mif2), and profile likelihoods are attempted for four parameters. The reported log-likelihood improvement from ARMA to POMP is substantial, but the comparison is confounded by the two model classes being fitted to different transformations of the data (differenced vs. original). Additional major flaws include noisy single-pfilter profile likelihood evaluation, too-sparse profile grids yielding collapsed singleton CIs, and absent convergence diagnostics for the global search.

**Strengths:**
- Coherent modeling pipeline from data exploration through POMP inference
- Correct use of logmeanexp in the global search likelihood evaluation
- Negative binomial measurement model appropriately accounts for overdispersion
- Thoughtful acknowledgment of computational limitations in the profile analysis
- Well-structured report with clear section organization

**Weaknesses:**
- The ARMA/SARMA–POMP log-likelihood comparison is not valid (different response variables)
- Profile likelihood evaluation relies on a single noisy pfilter call per grid point with no logmeanexp
- Profile grids are too sparse (10 points) and the resulting singleton CIs are misinterpreted
- No convergence trace plots or diagnostics for the global search
- rw.sd for rho (0.00001) is orders of magnitude below the course standard (0.02)

---

## Major Issues

### 1. Log-likelihood comparison between ARMA/SARMA and POMP is not valid

The comparison table in Section 5 places ARMA log-likelihood (-497.31), SARMA log-likelihood (-495.40), and SEIRS log-likelihood (-375.79) side by side and concludes a "substantial improvement" from the mechanistic model. However, the ARMA and SARMA models are fitted to `diff_flu_ts` (the first-differenced series), while the POMP model is fitted to the original `flu_data$cases`. These are different response variables. Log-likelihoods are only directly comparable when both models are evaluated against the same observed data. An ARMA model fitted to the first-differenced series gives the joint density of week-to-week *changes* in cases, not of the case counts themselves, so the two likelihoods measure goodness-of-fit to different quantities. The correct approach is to either (a) fit an ARIMA(0,1,1) model to the original case counts in a single call, or (b) compute the likelihood of a chosen ARIMA specification on the original (undifferenced) series and compare that to the POMP likelihood. As written, the main conclusion in Section 7.1 — that the SEIRS model "significantly outperformed" ARMA/SARMA — cannot be supported.

### 2. Profile likelihood uses a single pfilter run per grid point (no logmeanexp)

In Section 6, each profile likelihood value is evaluated with a single `pfilter` call at Np = 5000: `profile_amp$loglik[i] <- logLik(pf)`. The particle filter is a stochastic estimator; each run produces a different log-likelihood estimate with non-negligible Monte Carlo variance. The course-standard method (as implemented correctly in the global search) is `logmeanexp(replicate(N, logLik(pfilter(...))), se=TRUE)`. With a single noisy estimate per grid point, the apparent shape of the profile curve reflects Monte Carlo noise as well as the true likelihood surface. The Wilks cutoff for a 95% CI is approximately 1.92 log-likelihood units below the maximum. If the Monte Carlo standard error is on the order of 1 log unit (typical for Np = 5000 on a 110-observation dataset), the noise is comparable to the threshold, making the CI endpoints unreliable. The singleton CIs reported for phase and rho are very likely an artifact of this noise rather than genuine identifiability information (see also Major Issue 3).

### 3. Profile likelihood too sparse: 10 grid points per parameter

Each profile is computed over only 10 grid points. The course standard at run_level = 3 is 30 points; at run_level = 2 it is 5 points. Ten points is between these levels, but combined with the single-pfilter noise described above, 10 points is insufficient to reliably identify the profile maximum and the CI endpoints. The profile for `amp` covers a range of only 0.2 units (MLE ± 0.1), and the profile for `phase` covers ± 10 weeks. With only 10 equally spaced points in each range, the CI is determined by which adjacent points bracket the cutoff — a procedure that is sensitive to Monte Carlo noise at each point. Specifically, the collapsed CIs [2.7, 2.7] for phase and [0.00015, 0.00015] for rho suggest the cutoff is exceeded between consecutive grid points in both directions, which could simply mean the curvature of the true profile at those points is not resolved by 10 equally spaced evaluations. The authors attribute these results to "limited identifiability" and "poor identifiability" respectively (Section 6.2) without acknowledging that a denser, replicated profile is needed to support this conclusion.

### 4. rw.sd for rho is orders of magnitude below course standard

The perturbation standard deviation for `rho` is set as `rho = 0.00001` in `rw_sd`. The `rho` parameter has logit partrans, meaning optimization is performed on the logit scale. In pomp's mif2, perturbations are applied on the transformed (estimation) scale. The MLE value of rho is approximately 0.00015, so logit(rho) ≈ -8.8. A perturbation of 0.00001 standard deviations on the logit scale is approximately zero — rho would effectively be frozen at its starting value throughout the iterated filtering run. The course standard is rw.sd = 0.02 on the transformed scale. If rho is not being meaningfully perturbed, the MLE reported for rho reflects the starting value rather than a likelihood-maximized estimate, which undermines the profile likelihood and the comparison in Section 5. The correct fix is to use `rho = 0.02` as the rw.sd (on the logit scale), consistent with course conventions.

### 5. Local search: single pfilter per mif2 run used to select the best result

In the local search (Section 4.2), each of the 10 mif2 runs is evaluated with a single pfilter run to obtain its log-likelihood:

```r
lik_local <- lapply(mif_local, function(mf) {
  pf <- pfilter(mf, Np = 2000)
  c(coef(mf), loglik = logLik(pf))
})
```

The run with the highest single-run log-likelihood is then selected as the best parameter set. Because each particle filter evaluation is stochastic, the "best" run may simply be the one with the luckiest draw, not the one that achieved the highest true log-likelihood. The correct approach is to replicate the pfilter evaluation for each run and use logmeanexp to obtain stable estimates before comparing. The global search section correctly uses `logmeanexp(replicate(10, logLik(pfilter(mf, Np = 2000))), se = TRUE)`, but this good practice is absent from the local search selection step.

### 6. No convergence trace plots for the global search

Section 4.3 reports the global search results (10 starting points, 100 Nmif iterations) and identifies a best log-likelihood of -375.77, but no trace plots are shown for the global search. Trace plots of log-likelihood across mif2 iterations from multiple starting values are the standard diagnostic for verifying that the optimizer has converged to a consistent maximum. Without these, there is no evidence that the global search converged rather than terminating at disparate local optima. The local search does include trace plots, but the global search — which is more important for validating the MLE — lacks them entirely.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots are provided for the local search (Section 4.2), which is good. However, no trace plots are shown for the global search (Section 4.3), which is the more consequential run. The discussion mentions that the global search produced a "slightly better log-likelihood (-375.77 versus -375.83)" but without convergence traces, it is unclear whether either search reached the true MLE.

**Particle filter:** The local search uses Np = 1000 for mif2 and Np = 2000 for pfilter evaluation. The global search uses Np = 1000 for mif2 and Np = 2000 for replicated pfilter evaluation. The profile likelihood uses Np = 5000 for a single pfilter call. No ESS monitoring is reported at any stage. Given the Michigan population size (N ≈ 10^7) and the small fraction infected, particle filter degeneracy is a real risk that should be documented.

**Conditional log-likelihoods:** Not reported. There is no plot of per-observation log-likelihoods across the time series. This diagnostic would be particularly informative for identifying whether the model captures the large spike around week 110 (2024-2025 season).

**Profile likelihoods:** Attempted for four parameters (amp, Beta0, phase, rho), but compromised by single pfilter evaluation per point and too-few grid points (10). Three of the four parameters have not been profiled (mu_EI, mu_IR, mu_RS, k), so identifiability of the bulk of the model parameters is unknown.

**Computational scale:** Total computational effort is not reported. Given run_level-2-scale parameters (Np=1000, Nmif=100, 10 starts), the analysis appears to be preliminary-grade. For a final project, run_level = 3 with Np = 5000 and at least 20 global starts is more appropriate.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file within the Git repository. No separate archive with a DOI is provided, which is acceptable for a course project.

**Final parameters:** The best global parameter vector is printed in the Rmd output and available in the R session. Parameters are not saved as a separate CSV or RDS file, so reproducing Section 6 without re-running the full optimization is not straightforward.

**Model-code consistency:** The measurement model (`dnbinom_mu(cases, k, rho * H, give_log)`) uses H, which accumulates `dN_IR` (I→R transitions, i.e., recoveries). The text and model equations describe the model as tracking epidemic dynamics, and cases are described as "new infections" in the introduction. However, H counts recoveries, not infections, introducing an implicit delay of approximately 1/mu_IR ≈ 0.56 weeks. This is a discrepancy between the narrative and the code, though with weekly data and a short infectious period the practical effect may be small.

**Package versions:** No `sessionInfo()` output, no `renv` lockfile, and no pinned package versions. The `pomp` package has undergone API changes across major versions; results may not reproduce on a different installed version.

**Data file path:** The code reads `data <- read.csv("../Data/flu_michigan.csv")` but the data file `flu_michigan.csv` is located in the project03 directory alongside the Rmd, not in a parent `Data/` directory. This path will fail if the Rmd is knitted from its own directory. The Makefile or the correct relative path should be verified.

**Auxiliary data:** Only the main case count CSV is needed and is included. No covariate matrices or spatial structure are required for this model.

---

## Minor Issues

- **Spectral period vs. SARMA period inconsistency:** The frequency analysis (Section 2.2) identifies a dominant period of approximately 60 weeks (frequency ≈ 0.0167 cycles/week). The SARMA model in Section 3.2 uses a seasonal period of 52 weeks, corresponding to an annual cycle. The report does not acknowledge or reconcile this discrepancy. If the data truly exhibits a 60-week dominant cycle, using period=52 in the SARMA model requires justification. The discrepancy likely arises from the short time span (≈ 2.25 years), which makes 52-week periodicity difficult to distinguish from 60-week periodicity.

- **Singleton CIs for phase and rho attributed to identifiability:** Section 6.2 interprets the singleton CIs as indicating "limited identifiability" and "poorly identifiable" parameters. Given that these CIs arise from a single noisy pfilter call per 10-point grid, the more likely explanation is Monte Carlo variance in the profile, not a genuine likelihood property. The claim that "the data contains insufficient information about the seasonal timing" is not supported by the evidence presented.

- **H accumulates I→R flow rather than E→I flow:** The accumulator variable H is incremented by `dN_IR` (recoveries) in the step function. In most SEIR model implementations and course examples, H is used to track new infections (the E→I flow, `dN_EI`), since reported influenza cases correspond to individuals becoming symptomatic. Using recoveries introduces an additional delay of approximately 1/mu_IR ≈ 0.56 weeks on average. With weekly data this is a small but biologically unmotivated shift that should be noted and justified.

- **Global search uses only 10 starting points:** The global search samples 10 random starting points for a 13-parameter model. The course standard for run_level = 2 is Nreps_global = 20 and for run_level = 3 is 100. With only 10 starts in a high-dimensional space, the search may miss the global maximum. The slight log-likelihood improvement over the local search (0.06 log units) is well within Monte Carlo noise, suggesting the two searches may be finding similar optima rather than the global MLE.

- **No biological parameter interpretation:** The fitted parameter estimates (Beta0 ≈ 3.77, mu_EI ≈ 0.9, mu_IR ≈ 1.8 per week) are reported but not interpreted in biologically meaningful terms. For example: mean incubation period ≈ 1/mu_EI ≈ 1.1 weeks ≈ 7.8 days (epidemiologically, influenza incubation is ~2 days, suggesting possible model misspecification or unit issues); mean infectious period ≈ 1/mu_IR ≈ 0.56 weeks ≈ 3.9 days (plausible); the basic reproduction number R0 = Beta0/mu_IR ≈ 2.1 (plausible for seasonal flu). Computing and comparing these to independent epidemiological knowledge (Wheeler et al. 2024, item 11) would substantially strengthen the analysis.

- **Profile likelihood covers only 4 of 8+ estimated parameters:** Profile likelihoods are computed for amp, Beta0, phase, and rho, but not for mu_EI, mu_IR, mu_RS, or k. The identifiability and uncertainty of the remaining four parameters are completely unknown. The authors acknowledge this limitation, but since mu_EI and mu_IR govern the core transmission dynamics, their profiles are arguably more important than phase and rho.

- **rw.sd for phase may be too small for global search:** The phase parameter has rw.sd = 0.1 (in natural units of weeks). In the global search, phase is initialized uniformly over [0, 52] weeks from the MLE. With Nmif = 100 iterations and cooling.fraction.50 = 0.5, the effective random walk displacement over 100 steps is roughly 0.1 × sqrt(100) × cooling_adjustment ≈ 0.5–1 week. If the starting value is far from the optimal phase, the optimizer may not be able to travel far enough to find the true MLE for phase, contributing to poor global search performance for this parameter.

- **Missing model diagnostics:** Beyond forward simulations, no model diagnostics are presented. Effective sample size (ESS) traces from the particle filter, conditional log-likelihood plots by week, or filtering-distribution simulations would help identify specific periods (e.g., the large 2024-2025 spike around week 110) where the model may be misspecified.

- **Data path error may prevent reproduction:** The Rmd reads from `../Data/flu_michigan.csv` but the file exists at the project level. This will cause a file-not-found error when knitting from the project directory. The path should be corrected to `"flu_michigan.csv"` or a relative path consistent with the project structure.

---

## Recommendation

**Major Revision.**

The project demonstrates a solid understanding of the POMP framework and implements a reasonable SEIRS model for influenza dynamics. However, several methodological issues materially affect the validity of the reported conclusions. The most critical are: (1) the log-likelihood comparison between ARMA/SARMA and POMP is not valid because the models are fitted to different data transformations; (2) profile likelihoods are evaluated with a single noisy particle filter run per grid point rather than the required replicated logmeanexp; and (3) the profile grid is too sparse (10 points) to support valid CI determination, rendering the identifiability conclusions in Section 6 unreliable. Additional issues — particularly the absence of convergence diagnostics for the global search, the near-zero effective rw.sd for rho, and the missing model diagnostics — further undermine confidence in the parameter estimates. Addressing items 1–4 above is required for the analysis to reach an acceptable standard.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project03/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project03/flu_michigan.csv` (existence confirmed, not fully read)
