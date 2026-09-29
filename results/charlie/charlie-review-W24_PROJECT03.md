---
title: "Review: W24 Project 03"
subtitle: "*Analysis on Covid-19 Cases in Japan*"
format: pdf
---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) + replicated pfilter for likelihood evaluation |
| **R packages used** | pomp, forecast, ggplot2, doParallel, doRNG, doFuture |
| **Code publicly available** | Partial — code in project repository; data pulled from an external GitHub URL at runtime |
| **Data publicly available** | Yes — OWID COVID-19 dataset |
| **Benchmark comparison included** | No |

---

## POMP Checklist Scorecard

*✓ = satisfies practice, ~ = partially satisfies, ✗ = does not satisfy, N/A = not applicable*

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + logmeanexp used correctly; but two key biological parameters are fixed at incorrect values due to unit error |
| 2 | Benchmark comparison | ✗ | No non-mechanistic benchmark computed or compared |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported for SEIR searches; ARMA log-likelihood never stated; models fitted to different data windows |
| 4 | Model diagnostics | ~ | Trace plots shown for local search; no ESS monitoring; no conditional log-likelihood plots; pairs plots shown |
| 5 | Parameter identifiability and uncertainty | ~ | Profile only for ρ; β parameters never profiled; τ effectively fixed during profile computation |
| 6 | Computational adequacy | ~ | Final global search (350 mif2 iterations, 100 starts) is adequate; first global search uses only 22 iterations total per starting point |
| 7 | Forecast methodology | N/A | No SEIR forecasts presented |
| 8 | Model variations and nested comparisons | ✗ | No model variations tested; no nested likelihood comparisons |
| 9 | Stochasticity | ~ | Binomial process noise included; measurement model uses normal distribution rather than negative binomial |
| 10 | Reproducibility and extendability | ~ | Code available; data fetched from external URL; package versions not pinned; no sessionInfo() |
| 11 | Corroboration with scientific knowledge | ✗ | Unit error in μ_EI and μ_IR makes all biological interpretations invalid; implausibly high ρ not questioned |
| 12 | Measurement model specification | ~ | Discretized normal used without scientific motivation; negative binomial not considered |
| 13 | Initial conditions | ~ | S(0) estimated via η; E(0) = 100 and I(0) = 200 fixed arbitrarily without sensitivity analysis |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

This project applies two modeling approaches — SARIMA and a SEIR compartmental model via the pomp package — to weekly COVID-19 case counts in Japan. The ARMA component is fitted to the full 2020–2024 dataset, while the SEIR component is restricted to the pre-Omicron period (2020–2021) and uses a piecewise-constant contact rate β tied to policy events. Global likelihood optimization is performed using iterated filtering, and a profile likelihood is computed for the reporting probability ρ.

**Strengths:** The project applies likelihood-based inference correctly (IF2 + logmeanexp), uses appropriate replicated pfilter evaluation, shows trace plots as convergence diagnostics, and provides a scientifically motivated motivation for time-varying β. The final global search (100 starting points, 350 mif2 iterations per start) is computationally reasonable. The covariate-table mechanism for encoding policy interventions is correctly implemented.

**Weaknesses:** A fundamental unit inconsistency corrupts the biological interpretation of the fixed parameters μ_EI and μ_IR. No benchmark comparison is made between the SEIR model and any non-mechanistic alternative. The ARMA and SEIR analyses are conducted on different data windows, making no quantitative cross-model comparison possible. The profile likelihood for ρ is methodologically flawed because the nuisance parameter τ is effectively held fixed during optimization. Biologically implausible parameter estimates (R₀ on the order of hundreds to thousands) are reported without comment.

---

## Major Issues

### 1. Unit inconsistency in fixed biological parameters (CC-Yes: Error 1.3)

The text states that the transition rate from exposed to infectious is μ_EI = 1/(6.5 days) = 0.15 day⁻¹, and the removal rate is μ_IR ≈ 0.1 day⁻¹ based on CDC guidance. Both parameters are then fixed at 0.1 for all searches. However, the Euler process uses `delta.t = 1` passed to `euler(seir_step, delta.t = 1)`, where the time unit is one week (observations are sampled weekly, and `Time = row_number()` assigns integer weekly indices). At weekly time scale, μ_EI = 0.1 week⁻¹ implies a mean latency of 1/0.1 = 10 weeks (70 days), not 6.5 days. Similarly, μ_IR = 0.1 week⁻¹ implies a mean infectious period of 10 weeks (70 days), not 10 days. The correct values for the weekly model would be μ_EI ≈ 7/6.5 ≈ 1.08 week⁻¹ and μ_IR ≈ 7/10 = 0.7 week⁻¹.

This error propagates throughout the analysis. In the best global search result (loglik = −1083.8), the estimated contact rates are b1 = 96.6, b3 = 41.5, and the implied basic reproduction number for period 1 is b1/μ_IR = 96.6/0.1 = 966, which is biologically impossible. Many other high-likelihood parameter sets show b4 in the hundreds to thousands (e.g., b4 = 666, 351, 3043 in the top results from the final global search). These extreme values are direct consequences of the wrong rate scale. Because μ_EI and μ_IR are fixed rather than estimated, this error cannot self-correct.

To fix this: either re-parameterize the model with time in days (delta.t = 1/7) and keep μ_EI = 0.15 day⁻¹, or convert rates to week⁻¹ (μ_EI ≈ 1.08, μ_IR ≈ 0.7) and re-run all searches.

### 2. No benchmark comparison (CC-Yes: Error 1.6)

The project reports SEIR log-likelihoods ranging from −4219 (initial guess) to −1083 (final global search best) but never compares these to any non-mechanistic baseline. A simple IID negative binomial model or an ARMA model fitted to the same data window (2020–2021) would indicate whether the mechanistic model captures structure beyond what a simple statistical model achieves. The ARMA model fitted in the first section uses a different data window (2020–2024) and its log-likelihood is never reported in a form that could be used for comparison even on the common period.

Wheeler et al. (2024) note that none of 32 reviewed cholera papers included such a comparison, and that their negative binomial benchmark revealed that some models failed to beat it. The absence here means the added complexity of the SEIR model is unjustified on quantitative grounds.

To fix this: fit a negative binomial IID model to the 2020–2021 weekly counts and report its log-likelihood alongside the SEIR results. Optionally compare to the ARMA model evaluated on the restricted dataset.

### 3. ARMA and SEIR analyses fitted to different data windows, preventing any cross-model comparison

The SARIMA model is fitted to 222 weeks of data from 2020-01-05 to 2024-03-31, while the SEIR model is restricted to approximately 104 weeks ending 2021-12-31. The authors justify the truncation for the SEIR model by citing the emergence of the Omicron variant, which is scientifically reasonable. However, the consequence is that no quantitative comparison between the two approaches is possible: the ARMA log-likelihood is on a different dataset. The project's stated goal is to apply "two distinct yet complementary modeling approaches," but the analyses remain parallel without any synthesis.

To fix this: either (a) fit the ARMA model on the same 2020–2021 window and compare log-likelihoods, or (b) explicitly acknowledge that the two analyses address different questions and do not attempt cross-model comparison.

### 4. Profile likelihood for ρ effectively fixes τ during optimization, making it a conditional slice rather than a true profile (CC-Yes: Error 1.2)

At the profile likelihood section, the perturbation for τ is set to `rw.sd(..., tau = 0.0001, ...)`, which is orders of magnitude smaller than the perturbations used in global searches (tau up to 0.2 in search range). This extremely small random walk step size means mif2 will not explore τ away from its starting value during the profile computation. In practice, this means the reported "profile" for ρ holds τ approximately fixed and does not maximize over τ as a nuisance parameter at each ρ value. This produces a curve that is narrower than the true profile likelihood, yielding artificially optimistic confidence intervals. The resulting CI of [0.66, 0.93] for ρ cannot be trusted.

To fix this: set tau's rw.sd to a value consistent with the full global search (e.g., 0.02 on log scale) so that τ is genuinely optimized at each fixed ρ value.

### 5. Profile likelihood computed only for ρ; scientifically central β parameters never profiled

Only one parameter (the reporting probability ρ) receives a profile likelihood analysis. The four time-varying contact rates b1–b4 are the scientifically central parameters of the model — they represent the effective transmission rates across distinct epidemic phases — yet their identifiability is never assessed. The pairs plots from the global search show substantial spread in b1 through b4 values across high-likelihood parameter sets (e.g., b4 ranges from 7 to 3042 in the top results of the final global search), which strongly suggests these parameters are poorly identified. Without profile likelihoods, no confidence intervals can be stated for these parameters and the authors' claim of "narrow variability" in the parameter space is not supported.

To fix this: compute profile likelihoods for at least b1 and b4 (the first and last policy phases), which bound the epidemic's start and end, and report associated confidence intervals.

### 6. Reported second global search is worse than the first by ~900 log-likelihood units, but described as "not significantly better"

The "Second Global Search Results Based on Local Search" (mifs_global, global_search_results.rds) achieves a best log-likelihood of −4457.8. The "First Global Search Results Based on Local Search" achieves −3531.9. A difference of approximately 926 log-likelihood units is enormous — orders of magnitude beyond Monte Carlo noise. The text states this result "is not significantly better than the log likelihood of the previous local and global search," which is misleading: −4457.8 is substantially *worse* than −3531.9, not comparable. This indicates the second global search failed to find good parameter values (due to its extremely narrow search ranges and tiny perturbation sizes), and the authors appear not to have recognized the direction of the difference.

The same search also uses rw.sd values as small as 0.0001 for b1 and b2, which is far too small for the IF2 algorithm to make meaningful parameter moves. These values effectively freeze the contact rate parameters during optimization.

To fix this: use perturbation sizes consistent with the final global search (≥0.02 on log scale) and use a wider search box that encompasses parameter regions suggested by the other searches.

### 7. First global search uses only 22 total mif2 iterations per starting point

The "Based on Local Search" global search chains mif2 with Nmif = 10, 2, 2, 2, 2, 2, 2 = 22 total iterations per starting point across 500 starting values. The course standard for a meaningful global search is Nmif = 100 (run_level=2) or 200 (run_level=3). At 22 iterations, the optimizer cannot have converged, and the best log-likelihood of −3531.9 is likely not near the true maximum. Indeed, the subsequent "not based on local search" global search with 350 iterations per start (100 starts) achieves −1083.8, an improvement of ~2448 log-likelihood units. The results from the first global search should not be interpreted as indicative of the model's optimal fit.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots from the local search (10 runs, Nmif = 50) are shown and described as converging. The log-likelihood panel shows upward trends, which is encouraging. However, the local search uses only 10 replicate runs and Nmif = 50, which is at the lower bound of course standards. The final global search (100 starts, 350 iterations) is more convincing and finds a substantially better likelihood.

**Particle filter:** No ESS monitoring is presented at any stage. The Np values used vary across searches: Np = 500 for initial evaluation, Np = 1000 for final evaluation of the "not based on local search" global search (which is the best search). Using Np = 500 for the initial parameter evaluation is modest given the model complexity, but the subsequent use of Np = 10000 for the local search evaluation (200 replicates) and Np = 10000 for the second global search evaluation is more thorough.

**Conditional log-likelihoods:** No per-time-step log-likelihood plot is presented. Given the complex multi-peak structure of the data, such plots would be valuable for identifying which epidemic phases the model fits poorly.

**Profile likelihoods:** A profile for ρ is computed with 40 grid points and 5 starting values per point. The number of grid points is adequate to show the profile shape. However, as noted in Major Issue 4, the profile for ρ effectively fixes τ and should not be trusted. No profiles are shown for β parameters.

**Computational scale:** Total CPU cost is not reported. The final global search (100 starts × 350 mif2 iterations × Np = 1000) is moderate in scale.

---

## Reproducibility Assessment

**Code availability:** Code is included inline in the Quarto document. The analysis uses `bake()` with RDS files for caching, which is good practice. RDS files are present in the submission.

**Final parameters:** The best parameter vectors are presented in HTML tables but are not archived in a standalone CSV or RDS file for easy access. The baked RDS files (global_search_2.rds, etc.) contain the optimization results and serve as implicit archives.

**Model-code consistency:** The measurement model in code (discretized normal distribution) matches the mathematical description in the text.

**Package versions:** No `sessionInfo()` output is provided and no `renv` or equivalent version-locking is used. The `pomp` package API has changed across versions; results may not reproduce exactly on a different installation.

**Auxiliary data:** The dataset is fetched at runtime from a public GitHub URL (`raw.githubusercontent.com/LiangqiTang/531-final-project/main/owid-covid-data.csv`). If this URL becomes unavailable the analysis cannot be reproduced without additional steps.

**Auto-installation:** The preamble uses `if (!require("pkg")) install.packages("pkg")` for all dependencies. This silently installs packages without user consent and is a coding practice red flag.

---

## Minor Issues

- The ARMA analysis is applied to raw weekly case counts that span from near-zero to over 300,000 without any transformation. For highly right-skewed count data, a log or square-root transformation is typically recommended before fitting Gaussian ARMA; the project does not consider this. (CC-Yes: Error 2.5)

- The Ljung-Box test for the SARIMA residuals rejects the null of white noise, indicating residual autocorrelation. The authors note this ("there's correlation between the residual in the model, which kind of violates the model assumption") but take no remedial action — no revised model is attempted and no consequence for inference is discussed.

- The justification for the SARIMA seasonal period of 4 weeks rests on a spectral peak at frequency 0.2311 week⁻¹, corresponding to a period of 4.33 weeks. Rounding this to 4 is not discussed, and the scientific basis for a ~monthly cycle in COVID-19 incidence is not provided.

- The discretized normal measurement model is used without scientific motivation. For disease count data, a negative binomial measurement model is the course-standard approach and provides explicit overdispersion. The choice of normal here is never justified.

- E(0) = 100 and I(0) = 200 are fixed as initial exposed and infectious counts without justification or sensitivity analysis. Given that the epidemic was just beginning in January 2020 in Japan (likely close to zero cases), these values are arbitrary. Only η (the susceptible fraction) is estimated.

- The simulation presented after the "not based on local search" global search uses manually specified parameters (b1 = 60, b2 = 0.06, b3 = 40, b4 = 600) that do not correspond to the reported MLE (b1 = 96.6, b2 = 1.2, b3 = 41.5, b4 = 7.3) or to any single table row. The relationship between these values and the optimization results is not explained.

- The profile likelihood pairs plot is described as showing "very decentralized distribution, especially for η, τ and ρ," which would normally suggest that these parameters are not well-identified from the data. However, this observation is immediately followed by a confidence interval report without acknowledging the tension between a flat profile and a finite CI.

---

## Recommendation

Major Revision. The analysis contains a fundamental unit inconsistency (Major Issue 1) that renders the biological interpretation of all fitted parameters invalid. This error should be corrected before any scientific conclusions are drawn. Additionally, the absence of a benchmark comparison (Major Issue 2), the incomparability of the ARMA and SEIR analyses due to different data windows (Major Issue 3), and the flawed profile likelihood (Major Issue 4) together prevent a valid assessment of model adequacy. The authors demonstrate familiarity with the pomp workflow and IF2 methodology, which is a solid foundation. Correcting the time-unit error, fitting both models to a common data window, and computing profiles for the β parameters would substantially strengthen the work.

---

## Files Consulted

### Skill files

- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

### Project files

- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project03/blinded.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project03/blinded.html`
