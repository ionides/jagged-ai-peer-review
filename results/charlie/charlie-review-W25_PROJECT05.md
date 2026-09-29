# Peer Review: W25 Project 05
## *Analysis of Malaria Cases in Florida*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) via the `pomp` R package; replicated pfilter for likelihood evaluation |
| **R packages used** | `pomp`, `forecast` (Arima), `foreach`, `doFuture`, `ggplot2`, `tidyverse` |
| **Code publicly available** | Yes — submitted as part of course repository |
| **Data publicly available** | Yes — Project Tycho (CC BY 4.0), DOI: 10.25337/T7/ptycho.v2.0/US.61462000 |
| **Benchmark comparison included** | No (no non-mechanistic benchmark for POMP evaluation) |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 used with replicated pfilter, but see Issues 3, 7 |
| 2 | Benchmark comparison | ✗ | No ARMA or IID benchmark at the POMP scale; SARIMA comparison is on a different observation scale |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported, but SARIMA/POMP comparison is methodologically invalid |
| 4 | Model diagnostics | ✗ | No ESS monitoring; no conditional log-likelihood plots; visual comparisons only |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods; no confidence intervals; scatter plots misrepresent identifiability |
| 6 | Computational adequacy | ~ | Global search with 20 starts and Nmif=100 is reasonable but poorly constructed (see Issue 7) |
| 7 | Forecast methodology | N/A | No forecasts attempted |
| 8 | Model variations and nested comparisons | ✗ | Immigration model tested but never actually implemented; no formal comparison |
| 9 | Stochasticity | ~ | Process noise (Gamma white noise) is included; measurement model is Poisson despite σ_M declared as overdispersion |
| 10 | Reproducibility and extendability | ~ | Code present; but critical bugs prevent reproduction of intended analysis |
| 11 | Corroboration with scientific knowledge | ✗ | Parameter units are inconsistent with described biology; implausible values not flagged |
| 12 | Measurement model specification | ✗ | Code and text disagree; σ_M never used; ε value in code differs from parameter |
| 13 | Initial conditions | ~ | Initial compartments specified; N_0 = 100,000 unjustified for Florida |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

This project fits SARIMA and SEIR-based POMP models to monthly malaria case counts in Florida (2006–2016) from Project Tycho. The SARIMA analysis is well structured, and the use of a biologically motivated SEIR model with B-spline forcing is a reasonable design choice for a seasonally driven disease. However, the paper suffers from several critical implementation errors: the "immigration model" is never actually built into the pomp object (the rprocess is never updated), rendering the central biological claim unsupported; rate parameters described in days are applied in a monthly time-unit model, producing biologically implausible latent and infectious periods; and a declared overdispersion parameter (σ_M) is never used in the measurement model while the implemented code differs from the stated formula. The likelihood comparison between SARIMA and the POMP models conflates AIC and log-likelihood and compares values computed on different observation scales.

**Strengths:** The biological motivation for adapting the dengue SEIR model with splines is clearly articulated. The SARIMA analysis is competent, including log transformation, seasonal differencing, AIC model selection, invertibility check, and residual diagnostics. The use of replicated pfilter with logmeanexp for likelihood evaluation is correct.

**Weaknesses:** The immigration model is not implemented (critical code bug); rate parameters have unit inconsistencies making all biology-based interpretations unreliable; the measurement model code contradicts the text; the SARIMA-POMP likelihood comparison is methodologically invalid; no profile likelihoods or confidence intervals are produced; no benchmark comparison is made at the POMP scale.

---

## Major Issues

### 1. Immigration model is never actually implemented in the pomp object

This is the most critical error in the paper. In the `setup-immi` chunk, the authors redefine the R variable `rproc` to a new Csnippet that includes immigration dynamics. However, they never call `pomp(...)` again to rebuild `seir_spline_model` with this new process model. The only update applied to `seir_spline_model` is `coef(seir_spline_model) <- c(...)`, which only updates the parameter vector. The `rprocess` slot of `seir_spline_model` still holds the old Csnippet from the initial model, which contains no immigration term.

When `mif2(seir_spline_model, ...)` is called in the immigration local search, `immigration_rate` is in the parameter vector but is not referenced by the active C code. The `pomp` package silently ignores the unreferenced parameter and runs the original SEIR model, which explains the identical log-likelihood of -332.02 for both models. The claim "POMP model with immigration yields the same likelihood (-332.02)" and the biological conclusion that "introducing an immigration parameter in the SEIR framework was the right call" are both based on a model that was never computed.

**Fix:** After defining the new `rproc`, reconstruct the pomp object: `seir_spline_model_immi <- pomp(seir_spline_model, rprocess = euler(rproc_immi, delta.t = 1/24))` before fitting.

---

### 2. Rate parameters described in days are applied in a monthly time-unit model

The POMP model time unit is months: `monthly_all$time = 1:132` for 132 monthly observations, and the spline period is `period = 12` (months). All rate parameters must therefore be per month. However, the parameter descriptions state:

- `mu_EI = 1/25.2` — "Progression rate from exposed to infectious (1/latent period), 25.2 days"
- `gamma = 1/20.5` — "Recovery rate, 1/infectious period, ~20.5 days"

In a monthly model, `mu_EI = 1/25.2` implies an average E→I latent period of 25.2 months (~2.1 years), not 25.2 days. Similarly, `gamma = 1/20.5` implies an infectious period of 20.5 months (~1.7 years). The biologically correct values in monthly units would be approximately `mu_EI ≈ 30/14 ≈ 2.14` per month (for a ~14-day latent period) and `gamma ≈ 30/20.5 ≈ 1.46` per month. The values used are off by a factor of approximately 30. This is Error 1.3 (inconsistent units between latent process and measurement model), which the course explicitly tested and classified as Major severity. All biological interpretations of the fitted parameters are unreliable.

**Fix:** Divide all day-scale rates by 30.44 (average days per month) to convert to per-month units, or document clearly that the time unit is days and adjust the data and spline period accordingly.

---

### 3. Measurement model code contradicts the mathematical description; σ_M is declared but never used

The paper states the measurement model as `Y_t ~ Poisson(ρ I_t + ε)` where `ε` is "small background risk pressure" parameterized as `epsilon = 1`. The parameter table also lists `σ_M = 0.3` as "Fixed measurement overdispersion." Neither statement matches the implemented code:

- The `rmeas` Csnippet uses `rpois(rho * I + 1e-6)` and `dmeas` uses `dpois(Y, rho * I + 1e-6, give_log)`. The hardcoded constant `1e-6` is used, not the parameter `epsilon` (= 1).
- `sigma_M = 0.3` appears in `paramnames` and is initialized, but it is referenced nowhere in `rmeas`, `dmeas`, or `rproc`. It has no effect on the model.

A Poisson model has variance equal to its mean. Using `sigma_M` as overdispersion (e.g., in a negative binomial) would substantially change the likelihood surface and fitted parameters. The discrepancy between the stated measurement model (which mentions overdispersion) and the implemented model (pure Poisson with a mismatched ε value) constitutes a reproducibility failure consistent with the pattern documented in Wheeler et al. (2024). This is also a violation of POMP checklist item #12 (measurement model specification).

**Fix:** Decide whether the model should be Poisson (remove `sigma_M`, use `epsilon` correctly) or negative binomial (implement overdispersion using `sigma_M`). Ensure the mathematical statement and the C snippets agree.

---

### 4. Cumulative cases accumulator C is tracked but never used in the observation model

The model defines `accumvars = "C"` and updates `C += rho * dEI` in `rproc`, accumulating a fraction of E→I transitions. However, the measurement model observes `rpois(rho * I + 1e-6)`, which uses the current stock of infectious individuals I, not the accumulator C. These are different quantities: C records cumulative reported incidence, while I is prevalence. The paper does not clarify which quantity `Y` is supposed to represent (new monthly cases, which would correspond to flow, or current count, which would correspond to I). Given that the data consists of monthly reported case counts (new cases per month), observations from C would be more appropriate. As implemented, C is computed and discarded.

**Fix:** If Y represents new monthly cases, use `dmeas` based on C (and reset C at each observation time). If Y represents a stock, remove the accumulator and clarify the biological interpretation.

---

### 5. No profile likelihoods and no confidence intervals

The paper presents scatter plots of loglik vs. parameter values from the global search (the "parameter-loglik-plots" chunk) but does not compute profile likelihoods. A profile likelihood requires maximizing the likelihood over all nuisance parameters at each fixed value of the target parameter. The scatter plots show the raw distribution of optimization results across starting points, which is a slice (fixed starting-point scatter), not a profile. This is Error 1.2 (computing a likelihood slice instead of a profile), explicitly tested in course quiz Q10-02 and classified as Major severity. Without profile likelihoods, no confidence intervals are available for any POMP parameter, and the identifiability of the model cannot be assessed. The claim of "weak identifiability" in the conclusion is based on scatter in parameter values rather than examination of the likelihood surface.

**Fix:** Compute proper profile likelihoods for at least the key parameters (e.g., `rho`, `mu_EI`, `gamma`, `immigration_rate`) following the course standard: fix target parameter, optimize all others via mif2 at each grid point, and evaluate using replicated pfilter.

---

### 6. SARIMA AIC and POMP log-likelihood are compared on different scales

The conclusion states: "as seen in the difference in likelihoods between the SARIMA model (-96) and the POMP models (-328), there is a significant scope for improvement in the mechanistic models." This comparison is invalid on two counts.

First, -96 is the AIC of the SARIMA model, not its log-likelihood. AIC = -2·loglik + 2k; for SARIMA(0,1,1)(0,1,1)[12] with k = 2, the log-likelihood is approximately (-96 − 4)/(−2) = 50, not -96.

Second, the SARIMA is fit to `log1p(Y)` (the log-transformed series), while the POMP model is fit to raw counts Y. These likelihoods are densities evaluated on different observation scales and are not directly comparable without a Jacobian correction. This is Error 2.2 (AIC comparison between ARIMA and POMP without noting non-comparability), tested in quiz Q4-05/Q11-01.

If the intent is to benchmark the POMP model against a simpler model on the same data and scale, the appropriate comparison would be to fit a negative binomial or Poisson ARMA model directly to the raw count data Y and compare log-likelihoods.

**Fix:** Either fit a benchmark model on the same observation scale (raw counts) or explicitly note that the SARIMA and POMP likelihoods are not comparable and refrain from drawing conclusions based on their numerical difference.

---

### 7. Global search starting points are incorrectly constructed due to duplicate parameter names

In the global search, `global_inits` is constructed as `c(base_params, c(b_1 = runif(1, -2, 2), ...))`. Since `base_params` already contains `b_1`, `b_2`, ..., `b_5`, `g`, `rho`, `sigma_P`, etc., the resulting vector has duplicate names. In R, when a named vector contains duplicate names and is subscripted (or passed to a function that extracts by name), the first matching element is returned. The `pomp` package extracts parameters by name from the `params` argument to `mif2`; it will use the first occurrence, which comes from `base_params`, not from the intended random initialization. As a consequence, the "global" search is effectively a local search from the same fixed starting point, merely with different random seeds for the stochastic optimizer. This likely explains why the global search yields only "marginal" improvement over the local search. The diversity of starting points — the entire purpose of global search — is defeated.

**Fix:** Build `global_inits` by updating `base_params` with the new values using named assignment: start from a copy of `base_params`, then set `params["b_1"] <- runif(1, -2, 2)`, etc.

---

### 8. No benchmark model comparison for POMP

No non-mechanistic benchmark (e.g., ARMA, Poisson regression, negative binomial regression on raw counts) is compared against the POMP models. The course explicitly taught (quiz Q11-01, Error 1.6) that comparing a mechanistic model to such a benchmark is a necessary validation step. Without it, there is no way to assess whether the SEIR structure adds explanatory value over a simple statistical model. Given that the POMP log-likelihood is approximately -332 while the model has numerous parameters, an IID negative binomial fit to the raw counts could plausibly achieve a competitive log-likelihood. The paper cannot support its biological conclusions without this baseline.

**Fix:** Fit an ARMA or negative binomial model to the raw monthly case counts Y and report the log-likelihood for direct comparison with the POMP models.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots from the global search are shown for all parameters and loglik together. The paper claims the loglik "seems to be converging to -328," but the relevant diagnostic — a clear, separate loglik panel showing consistent upward convergence across all 20 runs to a common plateau — is not shown or discussed explicitly. The parameter panels show substantial spread, which is expected for weakly identified parameters, but the convergence criterion should be terminal loglik agreement across runs, not visual impressions.

**Particle filter:** The particle count is Np = 2000 for local search evaluation and Np = 4000 for global search evaluation (both using 10 replications with logmeanexp). These are reasonable. However, no ESS monitoring is performed at any point. ESS collapse during filtering is a key diagnostic for identifying time periods of poor model-data agreement, and its absence means the paper has no information about where the model fails.

**Conditional log-likelihoods:** Not reported. Per-observation log-likelihoods are among the most useful diagnostics for identifying model deficiencies (Wheeler et al. 2024, §Model diagnostics); their absence is a meaningful gap.

**Profile likelihoods:** Not computed. See Major Issue 5.

**Computational scale:** Not reported. CPU-hours or equivalent are not mentioned. The local search uses Nmif = 50 with 10 starts; the global search uses Nmif = 100 with 20 starts. These are within the run_level=2 range and appear adequate for a preliminary analysis, though the incorrectly constructed global search (Issue 7) limits the value of the global component.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file and data is included. The analysis can nominally be re-run.

**Final parameters:** No archived MLE parameter vectors are provided separately from the optimization code. Readers must re-run the full optimization to evaluate the reported likelihoods.

**Model-code consistency:** The measurement model in the text uses `ε` (epsilon = 1) but the code uses the hardcoded constant `1e-6`. The parameter `σ_M` is described as "Fixed measurement overdispersion" but is never referenced in the measurement code. See Major Issue 3.

**Package versions:** No `sessionInfo()` output or `renv` lockfile is provided. The `pomp` API has changed across versions; readers cannot verify which version was used.

**Auxiliary data:** The Project Tycho CSV file is included in the submission directory. Covariate tables (B-spline basis) are constructed programmatically within the Rmd and do not require external files.

---

## Minor Issues

- **Periodogram x-axis mislabeled (Error 2.8):** The `spec.pgram` call labels the x-axis as `"Frequency (cycles per year)"`, but with monthly data the native frequency unit is cycles per month. The paper correctly identifies the dominant period as approximately 12 months (at frequency ≈ 0.0888), but the x-axis label is inconsistent with the stated unit. The label should read "cycles per month."

- **SARIMA model equation notation error:** The equation `(1+θ₁)(1+Θ₁B¹²)εₜ` is missing the backshift operator in the first factor. The correct notation is `(1+θ₁B)(1+Θ₁B¹²)εₜ`.

- **Population size N_0 = 100,000 not justified:** Florida's population during 2006–2016 was approximately 18–20 million. The choice of N_0 = 100,000 is not explained. Using a representative sub-population is sometimes acceptable, but the effect on parameter estimates (especially ρ and the transmission coefficients) should be acknowledged.

- **Birth rate r = 0.135/month is biologically implausible:** The initial value `r = 0.135` in a monthly model corresponds to a ~14% monthly birth rate (>100% annually). The global search constrains `r ∈ [0, 0.001]` but never questions the initial value. No justification for any value of r is provided.

- **σ_M parameter is listed in the parameter table as "Fixed measurement overdispersion" but is never used:** This creates the false impression that the measurement model accounts for overdispersion. If σ_M is not used, it should not appear in the parameter table or description.

- **No formal model comparison between initial and immigration models:** The paper states that immigration "explains the model fit better" but no likelihood ratio test, AIC comparison, or even a clear statement of both models' log-likelihoods is provided. The identical loglik (-332.02) in the local search actually suggests no improvement.

- **Causal language in conclusions (Error 2.10):** The conclusion states "introducing an immigration parameter... supports the assumption that the force of infection is coming from outside Florida." This is causal language applied to a fitted model that did not in fact include immigration (Issue 1). Even were the model correctly implemented, observational model fit does not establish a causal mechanism.

---

## Recommendation

**Major Revision.** The paper has a clear scientific motivation and a coherent analytical plan: SARIMA for time-series characterization, followed by a mechanistic SEIR model with seasonal B-spline forcing and an immigration extension. The SARIMA component is well executed. However, the POMP component contains multiple critical errors that, taken together, mean the primary mechanistic analysis is unreliable: the immigration model is never actually implemented (the rprocess is never updated), rate parameters have unit inconsistencies of factor ~30, the measurement model code contradicts the text, profile likelihoods are absent, and the global search is incorrectly constructed. The biological conclusions rest entirely on the immigration model, which was not computed. Revision must address Major Issues 1–3 at minimum before the POMP results can be interpreted.

---

## Files Consulted

**Skill files — guided-pomp-review:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`

**Skill files — 531_references:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project05/Malaria Counts USA 1951-2017/README.txt`
