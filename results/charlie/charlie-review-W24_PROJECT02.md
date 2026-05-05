# Review: W24 PROJECT02
## *Investigating the alternative prey hypothesis with the POMP framework*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (iterated filtering via `mif2`) with particle filter |
| **R packages used** | pomp v5.6, doParallel, doFuture, doRNG, foreach |
| **Code publicly available** | Partial — Rmd source available in submission; uses hard-coded local paths |
| **Data publicly available** | Yes — hosted on Dryad (link placeholder in text) |
| **Benchmark comparison included** | Yes — ARIMA(0,1,5) included, but comparison is methodologically invalid (see Major Issue 1) |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 used, but particle count is critically low (Np=5 in one key evaluation) |
| 2 | Benchmark comparison | ~ | ARIMA benchmark present but log-likelihoods are not comparable across models |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported but with significant caveats around comparability |
| 4 | Model diagnostics | ~ | ESS and conditional log-likelihood plotted for initial guess; no diagnostics at MLE |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods, no confidence intervals |
| 6 | Computational adequacy | ✗ | Np=5 for likelihood evaluation; global search underperforms local search; convergence not demonstrated |
| 7 | Forecast methodology | N/A | No forecasting task stated |
| 8 | Model variations and nested comparisons | ✗ | Single model specification; no nested comparisons |
| 9 | Stochasticity | ✓ | Gamma noise included in both state equations |
| 10 | Reproducibility and extendability | ✗ | Hard-coded absolute paths; no package pinning; final parameters not independently archived |
| 11 | Corroboration with scientific knowledge | ✗ | Parameter estimates not compared to biological literature |
| 12 | Measurement model specification | ~ | Normal measurement model used; no overdispersion; mismatch between text description and measurement model formulation |
| 13 | Initial conditions | ~ | Initial conditions estimated; sensitivity not assessed |

---

## Summary

This project applies the POMP framework to model willow ptarmigan population dynamics in Southeastern Norway from 1872 to 2012, with the goal of examining the alternative prey hypothesis. The authors build a stochastic Lotka-Volterra-style process model with fox, rodent, and bird population states, fit it via iterated filtering (IF2), and compare the resulting log-likelihood against an ARIMA(0,1,5) baseline. While the ecological motivation is clear and the use of POMP in this non-epidemiological domain is novel, the analysis is severely undermined by critically inadequate computation (Np=5 for log-likelihood evaluation), a methodologically invalid ARIMA-versus-POMP log-likelihood comparison, a global search that is demonstrably misconfigured and produces results worse than the local search, and an absence of profile likelihoods, model diagnostics at the MLE, or parameter uncertainty quantification. The paper's main quantitative conclusions rest on these flawed computations and cannot be accepted in their current form.

**Strengths:**
- Interesting non-standard ecological application of POMP; the alternative prey hypothesis provides a scientifically motivated process model structure
- Stochastic process model with gamma noise in both state equations is appropriate
- An ARIMA baseline is included, which is a good instinct even though the comparison is not properly executed
- Some particle filter diagnostics (ESS, conditional log-likelihood) are reported for the initial parameter guess

**Weaknesses:**
- The ARIMA and POMP log-likelihoods are not comparable (different observation models, differenced vs. original data); the central comparative claim is invalid
- Particle count of Np=5 used for log-likelihood evaluation renders all reported POMP likelihoods unreliable
- Global search underperforms local search by 42 log-likelihood units, indicating severe box misalignment and/or structural bugs in the search procedure
- No profile likelihoods or confidence intervals; no model diagnostics at the fitted MLE
- Hard-coded local file paths prevent any external reproduction

---

## Major Issues

### 1. Invalid ARIMA-versus-POMP log-likelihood comparison

The paper's central conclusion — "the ARIMA model is fitting the data better" (Section 3.2) — rests on comparing the ARIMA(0,1,5) log-likelihood of -99.32 directly to the POMP model log-likelihood of -134 (local search) and -176.3 (global search). This comparison is methodologically invalid on two grounds.

First, the ARIMA model is fitted to first-differenced log-CPUE using a Gaussian error model, while the POMP model is fitted to the original (undifferenced) log-CPUE series using a Normal observation model. These are different observation models on different transformations of the data; their log-likelihoods are not on the same scale and cannot be compared numerically.

Second, even if both were on the original scale, the POMP likelihood accounts for the full joint distribution of observations given the latent process, while the ARIMA likelihood marginalizes over the latent structure entirely. A joint log-likelihood of -134 for a 142-observation series is not intrinsically worse than an ARIMA log-likelihood of -99 — these numbers have different interpretations.

The fix is to evaluate both models on a common basis. One valid approach is to evaluate the ARIMA model on the original (undifferenced) log-CPUE using the same Gaussian observation model as the POMP measurement model, computing `logLik(arima(data$logCPUE, order=c(0,0,0)))` versus the POMP model. Alternatively, use a proper scoring rule (e.g., CRPS on original observations) that does not require matching likelihoods. Until this is corrected, all comparative conclusions are unsupported. See Wheeler et al. (2024) §Benchmark comparison, and the sarima-baseline-audit guidance.

---

### 2. Critically inadequate particle count for log-likelihood evaluation

In the local search code chunk (lines ~393-398), after a single `mif2` run, the log-likelihood is evaluated using Np=5 particles:

```r
foreach (i=1:10, .combine=c, .options.future=list(seed=652643293)) %dofuture% {
  mif2_out |> pfilter(Np=5)
} -> pf
logLik(pf) -> ll
print(logmeanexp(ll, se=TRUE))
```

Five particles is far below any defensible minimum for a 12-parameter model applied to 142 observations. A particle filter with Np=5 will experience catastrophic degeneracy in nearly every time step, producing a log-likelihood estimate with Monte Carlo standard error likely exceeding 10-20 log-likelihood units. The reported local search log-likelihood of -205 (SE=3.14) for a single mif2 run, and the stated -134 for the 20-chain foreach loop, are both derived from computations using Np far too small to be trusted. The global search uses Np=500 for final evaluation (line ~509), which is more reasonable, but even there only 50 starting points are used and the search is severely constrained (see Major Issue 3).

All reported POMP log-likelihoods in the paper are potentially artifactual. As a minimum, Np should be set to at least 1000 (and ideally 2000-5000 for a model of this complexity) before any log-likelihood is reported as evidence of model fit. Wheeler et al. (2024) note that insufficient computation is the primary cause of misleadingly poor POMP performance relative to simple baselines.

---

### 3. Global search severely underperforms local search: evidence of box misalignment and structural flaws

The global search yields a best log-likelihood of -176.3, which is 42 units worse than the local search result of -134. This is a diagnostic signature of a misconfigured global search (see pomp-global-search-box-misalignment skill). Examining the global search box:

```r
lower = c(alpha = 0, Beta = 0, gamma = 0, a = 7, b = 2, c = 0.5,
          sigma_obs = 0, logF_0 = 0.4, logB_0 = 1.6,
          sigmaF = 0, sigmaB = 0.02, logRho = 0.3)
upper = c(alpha = 0.1, Beta = 0.1, gamma = 0.1, a = 8, b = 3, c = 1,
          sigma_obs = 1, logF_0 = 0.5, logB_0 = 1.7,
          sigmaF = 0.1, sigmaB = 0.04, logRho = 0.5)
```

The local search starting point uses `a = 1`, yet the global search box forces `a` into [7, 8]. The best global result has `a = 1.43` (from `bird_params_middle.csv`) — a value well outside the lower bound of 7. This means the IF2 optimization had to drift `a` from somewhere in [7, 8] all the way down to ~1.4, relying on accidental perturbation rather than systematic exploration. The box for `b` presents the same problem: starting value is 2, but the box puts `b` in [2, 3]. The initial conditions box ([0.4, 0.5] for logF_0 and [1.6, 1.7] for logB_0) is extremely narrow (width 0.1), while the best global result has logF_0 = 0.86 and logB_0 = 2.91, both well outside these ranges.

Additionally, the global search code calls `mif2(params=c(guess, fixed_params))` where `fixed_params = coef(mif2_out)`. Because `guess` contains the same parameter names as `fixed_params`, this creates a duplicate-name concatenation. In R, `c()` appends without deduplication, so each combined vector contains every parameter twice. Whether pomp uses the first or last occurrence determines whether `guess` or `fixed_params` values are actually used — in either case, the intended override is unreliable. See the pomp-global-search-param-override-bug skill for the full diagnosis.

Furthermore, the global search is initialized from `mf1 <- mifs_local[[1]]` (a previous mif2 result) rather than the base pomp object `mod`. This anchors the cooling schedule to the local search chain, potentially causing near-zero perturbations from the start of the global search. See the pomp-global-search-init-audit skill. The combination of these three issues (box misalignment, duplicate-name override, wrong initialization object) renders the global search results unreliable.

---

### 4. Measurement model text-code inconsistency

The text (Section 2, Methods) states: "The measurement model $Y(t)$ is our ptarmigan count proxy, log-CPUE, $y(t) = \text{Negative Binomial}(\text{mean}=\rho\beta_t, \sigma)$". However, the actual measurement model implemented in the code is:

```r
Csnippet("logCPUE = rnorm(logB - logRho, sigma_obs);") -> rmeas
Csnippet("lik = dnorm(logCPUE, logB - logRho, sigma_obs, give_log);") -> dmeas
```

This is a Gaussian (Normal) observation model on log-CPUE, not a Negative Binomial on counts. The text description is entirely inconsistent with the code. This discrepancy means that either (a) the text is wrong and the implementation uses a Gaussian measurement model, or (b) the code is wrong and the intended Negative Binomial model was never implemented. Wheeler et al. (2024) document this exact class of error as a major reproducibility failure. Regardless of which is intended, the paper as submitted cannot be evaluated for model adequacy because the implemented and described models differ.

Additionally, the Gaussian observation model on log-CPUE — if intentional — lacks overdispersion and uses a single noise parameter `sigma_obs` shared across all observations. Given the 142-year span of the data with substantial non-stationarity, this is almost certainly too restrictive.

---

### 5. No parameter identifiability assessment or confidence intervals

No profile likelihoods are computed and no confidence intervals are reported for any parameter. With 12 parameters in the process model, several of which have overlapping roles in the Lotka-Volterra dynamics (e.g., the interaction between `gamma`, `c`, `Beta`, and `b`), identifiability is a serious concern. The local search pairs plot (Figure local_search_2) is described as showing "little to no apparent linear correlation," which the authors treat as a positive sign, but a scattered cloud in the pairs plot can also indicate non-convergence or flat likelihood surfaces rather than uncorrelated well-identified parameters.

Profile likelihoods should be computed for at least the key ecological parameters (`gamma`, `alpha`, `Beta`) using multiple IF2 restarts from a broad box at each grid value, with log-likelihood evaluated via logmeanexp over >= 10 particle filter replicates. Without these, it is unknown whether any parameter in the model is identifiable from 142 annual observations. Wheeler et al. (2024) note that boundary estimates (e.g., MLE at zero for a rate parameter) are evidence of model misspecification rather than biological truths.

---

### 6. No model diagnostics at the fitted MLE

Particle filter diagnostics (ESS and conditional log-likelihood) are shown only for the initial parameter guess (Figure pf1). No diagnostics are presented at the locally or globally fitted parameter estimates. The ESS plot for the initial guess correctly identifies particle degeneracy, but without an analogous plot at the MLE, there is no way to assess whether the fitted model resolved this degeneracy or whether it persists. Persistent ESS collapse at the MLE would indicate model-data mismatch that would invalidate the fitted likelihood.

The authors should run `pfilter(mod, params=best_params, Np=2000)` and display the resulting ESS and conditional log-likelihood traces. Periods of low ESS at the MLE identify specific time periods where the model fails to explain the data, which is critical diagnostic information given the known structural breaks in ptarmigan abundance during this 142-year record.

---

### 7. Partial convergence evidence and inadequate optimization

The convergence traces from the local search (Figure local_search_1) show that several parameters — specifically `log(B_0)` and `sigma_F` — have not converged after 50 IF2 iterations. The authors acknowledge this: "not all parameters show signs of convergence, such as log(B_0), sigma_F." A non-converged IF2 chain means the reported log-likelihood is not near the MLE; downstream parameter estimates and all goodness-of-fit comparisons are unreliable.

The local search uses only 20 replicates at Np=1000 for Nmif=50. For a 12-parameter model with apparent convergence difficulties, this is insufficient. The global search uses only 50 starting points with Nmif=100 (inferred from code), which is minimal. Best practice (Wheeler et al. 2024, §Computational adequacy) involves running multiple searches from diverse starting points until the best log-likelihoods across independent runs agree to within Monte Carlo error. No evidence of this convergence criterion being checked is provided.

---

## Computational and Diagnostic Assessment

**Convergence:** Not demonstrated. The convergence traces (local_search_1.png) show non-convergence for at least two parameters. No global search convergence traces are shown. Multiple searches show substantial variation in final log-likelihoods (range from -134 to -205 just in the local search), indicating the optimizer has not found a stable region.

**Particle filter:** ESS monitored at initial guess only (Figure pf1). The initial ESS shows persistent low values ("particle degeneracy issue" acknowledged by authors). No ESS diagnostics at MLE. The critically low Np=5 used in one key evaluation is a severe flaw.

**Conditional log-likelihoods:** Shown for initial guess only. Fluctuating conditional log-likelihoods noted but not interpreted in terms of specific time periods of poor fit.

**Profile likelihoods:** Not computed. This is a critical gap given 12 parameters with potentially collinear roles.

**Computational scale:** CPU cost mentioned only qualitatively ("more than 8 hours on Great Lakes"). No particle counts or iteration counts reported for the cluster runs. No HPC job scripts or environment specifications provided.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file but uses hard-coded absolute paths that are specific to the author's local machine (e.g., `/Users/ruojunliu/Desktop/STATS 531 - Time Series/pomp_final/`). The bibliography path is also hard-coded (`/Users/ruojunliu/Desktop/references.bib`). The document cannot be compiled without modifying these paths.

**Final parameters:** The file `bird_params_middle.csv` contains only 2 rows (best and second-best global search results), suggesting only 2 out of 50 global replicates produced finite log-likelihoods — the remaining 48 produced `-Inf` and were filtered out by `filter(is.finite(loglik))`. This is a severe sign of model instability. Final parameter estimates from the local search are referenced but not archived as a standalone file.

**Model-code consistency:** The measurement model described in the text (Negative Binomial) does not match the code (Gaussian). This is a critical inconsistency (Wheeler et al. 2024).

**Package versions:** pomp v5.6 is mentioned in passing, but no `sessionInfo()` output or `renv` lockfile is provided. Package versions for `doParallel`, `doFuture`, `doRNG`, and others are not specified.

**Auxiliary data:** The Dryad link for the bird data is a placeholder (empty parentheses in the Rmd). The `data/bird_data.xlsx` file appears to be present in the submission folder.

**HPC reproducibility:** Great Lakes cluster was used but no SLURM job scripts or environment specs are provided. Computation is nominally possible but practically unreproducible without this information.

---

## Minor Issues

- The PACF caption (line 145) reads "ACF of logCPUE" — should be "PACF of logCPUE."
- The body text (line 151) references "Figure \@ref(fig:trend)" when describing the PACF, but the PACF is in Figure \@ref(fig:pacf). This is a cross-reference error.
- "Lotka-Volterra" is misspelled as "Lotka-Voltera" throughout (lines 232, 547).
- Line 541: "As a result, he log-likelihood produced" — "he" should be "the."
- The Rmd title references `Lapagos lapagos` as the Latin name for willow ptarmigan; the correct binomial is *Lagopus lagopus*.
- Line 279 gives an initial parameter guess of `log(F_0) = 1` but the actual code (line 349) sets `logF_0 = 1` and `logB_0 = 2`, inconsistently with the stated `log(B_0) = 1` in text.
- The process model equations (Eq. 1 and 2) both use `W_t^F` as the noise term for both fox and bird state equations, but the code defines separate `dwF` and `dwB` noise terms. Eq. 2 should use `W_t^B`.
- The global search stores results to `bird_params_middle2.csv` in the code (line 523) but the loaded artifact is `bird_params_middle.csv` (line 529) — these are different files, and it is unclear which computation produced the archived results.
- No discussion of why logF and logB are used as state variables (log-scale SDE) rather than F and B directly; the stochastic differential equations as written mix the log-scale dynamics with multiplicative gamma noise in a way that should be explicitly justified.
- The `partrans` in the `pomp()` call specifies `log` transformation for all 12 parameters including `logF_0`, `logB_0`, and `logRho` — applying a `log` transform to a parameter that is already on the log scale means the optimizer searches on the log-log scale, which may cause numerical difficulties and is likely unintended.

---

## Recommendation

**Major Revision / Reject and Resubmit.** The paper has a scientifically interesting motivation and a reasonable model structure for the ecological question, but the analysis is not yet in a state that supports its conclusions. The central comparative claim (ARIMA fits better than POMP) rests on an invalid log-likelihood comparison between models with different observation models on different data transformations. The POMP results themselves are unreliable due to critically low particle counts (Np=5), a global search that produces results 42 units worse than the local search due to systematic box misalignment and parameter override bugs, and non-convergence of key parameters. The text-code inconsistency in the measurement model (Negative Binomial described, Gaussian implemented) is a reproducibility failure that must be resolved before any further analysis is evaluated. Profile likelihoods and parameter uncertainty quantification are absent entirely.

The work should be revised by: (1) correcting the measurement model to be consistent between text and code; (2) rerunning the POMP inference with adequate particle counts (Np >= 1000 for intermediate evaluations, >= 2000 for final log-likelihood assessment); (3) correcting the global search box to span the regions identified by the local search; (4) fixing the global search initialization to use the base pomp object rather than a previous mif2 result; (5) computing profile likelihoods for the key ecological parameters; and (6) providing a valid basis for the ARIMA-vs-POMP comparison. Until these issues are addressed, the paper cannot be recommended for publication.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project02/bird_params_middle.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project02/README.md`
