# Peer Review: W25 Project 06
## "Investigating Hungarian Chickenpox Infections"

---

## Summary

This project models weekly chickenpox incidence in Hungary (2005–2015) using three approaches: an ARMA(4,4) model, a seasonally forced SEIRS model fitted via POMP (iterated filtering with particle filter likelihood), and a deep learning model combining Variational Mode Decomposition with N-BEATS. The core mechanistic contribution is the SEIRS model, which is biologically motivated and structurally reasonable. However, the POMP inference contains several critical implementation errors that collectively render all reported parameter estimates, log-likelihoods, and the profile likelihood invalid. The most serious problems are: (1) the measurement model reads only the last Euler sub-step's new infections rather than the weekly cumulative total, due to the absence of `accumvars`; (2) the population parameter N is set to approximately one-quarter of Hungary's actual population, producing a severely biased force-of-infection term; (3) the global search inherits the mif2 cooling state from the local search rather than starting fresh; (4) the seasonal amplitude `amp` is estimated without any parameter transformation constraint, yielding biologically implausible values exceeding 1.0; and (5) the profile likelihood is a pseudo-profile derived from global-search scatter, not from constrained optimization. These errors are compounding and undermine the mechanistic inference entirely.

---

## Major Issues

### 1. Missing `accumvars` causes measurement model to use only the last Euler sub-step

The Csnippet uses `NewEI = dN_EI` to track new E-to-I transitions at each Euler step, and the `dmeasure` and `rmeasure` Csnippets link observed case counts to `NewEI`. However, no `accumvars = "NewEI"` argument is passed to `pomp()`. With `delta.t = 1/7` weeks and observations at integer weekly times, there are 7 Euler sub-steps per observation interval. Without `accumvars`, `NewEI` is overwritten at every sub-step and the measurement model evaluates only the single sub-step immediately preceding the observation time, discarding six-sevenths of the weekly new-infection flow. This causes a systematic factor-of-7 undercount of modeled cases relative to the data, which is absorbed into inflated estimates of `rho` and distorted transition rates. The correct fix is to declare `accumvars = c("H", "NewEI")` in the `pomp()` call, which causes both variables to be summed across sub-steps and reset after each likelihood evaluation.

Additionally, `H` (which accumulates `dN_IR`, the I-to-R flow) is also never declared in `accumvars`, so it grows without bound from `t = 0` and the `emeas` Csnippet (`E_infection = rho * H`) produces an estimate that is a cumulative total of all recoveries since initialization, not a weekly count.

### 2. Population N is approximately one-quarter of Hungary's actual size, biasing the force of infection

The model fixes `N = 2267000`. Hungary's population during 2005–2015 was approximately 9.9–10.1 million. The value 2267000 is roughly 22% of the true population, which is not justified in the text. Because the force of infection is `Beta * I / N`, fixing N at 22% of its true value is equivalent to multiplying the effective transmission rate by a factor of 4.4. The global MLE for `Beta` is 100.4 per week. For chickenpox, R0 ≈ 8–10 and the mean generation interval is roughly 2 weeks, implying a biologically plausible Beta on the order of 4–5 per week; the estimated value of 100.4 is approximately 20 times too high. This discrepancy is quantitatively consistent with the factor of ~4.4 from the population error. The authors do not discuss this or compare estimated parameters to independent biological evidence (Wheeler et al. 2024, §11: Corroboration with scientific knowledge). N should either be set to the national total or modeled as a time-varying covariate.

### 3. Global search anti-pattern: initialized from a previous mif2 result, not the base pomp object

The global search code sets `mf1 <- mifs_local[[1]]` and then executes `mf <- mf1 %>% mif2(params = c(unlist(guess), fixed_params), ...)` for each global replicate. Passing a previous `mif2` result as the first argument to `mif2()` causes the global search to inherit the internal cooling schedule and state of the final local-search chain. Because `mifs_local[[1]]` has already run 100 IF2 iterations with `cooling.fraction.50 = 0.3`, its cooling schedule is near its terminal value; the global search replicates therefore perform very few functional IF2 iterations from the new random starting points before perturbations shrink to near zero. The "global search" is not genuinely global — it is anchored to the local-search solution. The fix is to replace `mf1` with the base `chickenSEIR` pomp object as the first argument to `mif2()` in the global loop (see `pomp-global-search-init-audit`).

### 4. Amplitude parameter `amp` estimated without transformation constraint, producing values exceeding 1

The `pomp()` call declares `logit = c("eta", "rho", "amp")` in `partrans`, which would restrict `amp` to the interval (0, 1). However, the local mif2 call overrides this with `partrans = parameter_trans(log = c("Beta", "mu_EI", "mu_IR", "k"), logit = c("eta", "rho"))`, which omits `amp`. Because the global search uses `mf1` (the local mif2 result) as its base object, it inherits this overridden `partrans`. Consequently, `amp` is estimated on the natural scale with no upper bound. All 20 local search results have `amp > 2.1` and all 100 global search results have `amp > 1.1` (maximum 1.76). With `amp > 1`, the seasonal forcing term `Beta_t = Beta * (1 + amp * cos(...))` becomes zero (guarded) during the off-season, implying complete cessation of transmission — a biologically extreme result. This transformation inconsistency should be corrected by ensuring `amp` is included in the `logit` entry of the `rw.sd`-level `partrans` call, or at minimum discussed as a model choice.

### 5. Profile likelihood is a pseudo-profile, not a genuine constrained optimization

The profile likelihood section explicitly describes implementing a "Poor Man's Profile" by filtering the global search scatter by `rho` values. The code confirms this: `rho_profile <- global_loglik_result %>% filter(is.finite(loglik)) %>% arrange(desc(loglik))` and the CI cutoff is applied directly to this scatter plot. No `profile_design()` call is present, no dedicated mif2 loop with `rho` excluded from `rw.sd` is run, and no constrained optimization at each rho grid point is performed. Applying a chi-squared cutoff (`ci_cutoff <- maxloglik - 4`, which itself deviates from the correct threshold of `maxloglik - 0.5 * qchisq(0.95, 1) = maxloglik - 1.92`) to this scatter produces a confidence interval with no valid statistical interpretation. Furthermore, only 1 point in the global search exceeds the correct chi-squared threshold, and only 3 exceed the relaxed threshold used; the reported CI is driven by extreme sparsity in the global search. A genuine profile likelihood requires fixing `rho` at each grid value, optimizing all remaining parameters via IF2 with `rho` excluded from `rw.sd`, and then applying the chi-squared cutoff to the resulting curve (see `pomp-pseudo-profile-audit`).

### 6. No benchmark comparison of POMP model against non-mechanistic baseline

The POMP mechanistic model is never quantitatively compared against the ARMA benchmark on a common basis. The paper reports ARMA log-likelihood as −3603.29 (Gaussian errors, original scale) and POMP log-likelihood as −3758.96 (negative binomial, original scale). These numbers are derived under different observation models and cannot be compared directly to assess relative model adequacy. Wheeler et al. (2024, §Benchmark comparison) recommend comparing the mechanistic model to a non-mechanistic benchmark such as an auto-regressive negative binomial — evaluated under the same observation model so log-likelihoods are directly comparable. Without such a comparison it is impossible to determine whether the SEIRS model captures any transmission dynamics beyond what a simple statistical model would achieve.

### 7. ODE equations claim demographic turnover but the Csnippet implements none

The model description lists differential equations that include `mu * N` (births) and `-mu * S` (deaths) in the dS compartment, and similarly for dE, dI, dR. The text states "we assume N remains approximately constant due to balanced demographic turnover." However, the `seir_step` Csnippet contains no birth or death terms: only `dN_SE`, `dN_EI`, `dN_IR`, `dN_RS` transitions are present. The total population `N` is fixed and the demographic terms `mu * N - mu * S` that would appear in a true open-population SEIR are absent. This discrepancy between the mathematical specification and the implemented code is a reproducibility failure (Wheeler et al. 2024, §10: Reproducibility and extendability; code-supplement-checklist, §Traceability). In practice, because 10-year birth/death effects are small, this is unlikely to materially change results, but the stated model and implemented model do not match.

---

## Minor Issues

- **SEIR vs. SEIRS mislabeling**: The model includes waning immunity (`omega`, `dN_RS` transitions from R back to S), making it an SEIRS model. The section title, state variable description, and most of the prose refer to it as "SEIR." This creates confusion about the model structure throughout.

- **Incorrect CI threshold for profile**: The code uses `ci_cutoff <- maxloglik - 4` with an inline comment "More relaxed than 0.5 * qchisq(df=1, p=0.95)." The correct 95% threshold is `maxloglik - 0.5 * qchisq(0.95, 1) ≈ maxloglik - 1.92`. Using −4 instead of −1.92 widens the interval by more than two likelihood units, further inflating the already-invalid pseudo-profile CI.

- **`amp` upper bound in global search exceeds logit domain**: The `runif_design` upper bound for `amp` is 0.4, which is within the logit domain (0, 1). But because the logit transform is not actually enforced (see Issue 4), this bound is not meaningful as a constraint. Once mif2 is called, `amp` can and does move far above 0.4 (reaching values > 2.1 in local search).

- **`mu_IR` lower bound in global search implies implausible infectious period**: The lower bound for `mu_IR` is 0.03 per week, corresponding to an infectious period of 33 weeks. Chickenpox has an infectious period of approximately 5–7 days (≈0.7–1 week), implying `mu_IR` should be near 7 (per week). The upper bound of 0.6 (1.7-week infectious period) is also substantially longer than biological expectation. The best-fit `mu_EI` of 0.136 implies a latent period of 7.4 weeks, which is nearly four times the known varicella incubation period of 10–21 days.

- **`H` accumulates recoveries, not cases; `emeas` gives a nonsensical cumulative total**: The `emeas` Csnippet computes `E_infection = rho * H`, where `H` accumulates `dN_IR` (I-to-R transitions) from `t = 0` without reset. The `emeas` output is therefore a running total of all recoveries since initialization scaled by `rho`, not the expected number of cases in the current week. This is used for the `emeasure` argument (expected measurement) and inflates rapidly over the 522-week series.

- **Deep learning evaluation methodology incompletely described**: The N-BEATS model achieves 2.5–3% MAPE, compared to 36.82% for ARMA. However, the Rmd writeup does not specify the train/validation/test split dates, the number of training epochs, the hyperparameter selection procedure, or whether the MAPE figures apply to the validation set, a test set, or in-sample. Without this information the comparison with ARMA (which uses in-sample MAPE on the full series) is not interpretable.

- **Duplicate `library(pomp)` call in setup chunk**: The setup chunk loads `library(pomp)` twice (lines 19–20). This is harmless but indicative of copy-paste editing without cleanup.

- **Auto-installing packages in non-interactive Rmd**: The POMP setup chunk uses `install.packages(to_install, ...)` within the document, which will install packages without user consent during rendering. This violates coding best practices (code-supplement-checklist, §Quality: "No auto-installing packages without user consent").

- **`plan(multicore)` may produce warnings or errors on Windows**: The code sets `plan(multicore)` for parallelism. `multicore` is unsupported on Windows (where `plan(multisession)` or `plan(cluster)` is required). A more portable choice would be `plan(multisession)` or a conditional check.

- **Log-ARMA and ARMA log-likelihoods described as "not directly comparable" but are compared by implication**: The paper notes the log-ARMA AIC (507.41) and linear ARMA AIC (7226.58) are "not directly comparable due to the change in data scale," then proceeds to contrast them for modeling insight. This acknowledged incomparability should apply equally to the ARMA-vs-POMP comparison, yet the paper does not address that the ARMA Gaussian likelihood and POMP NegBinom likelihood are also not directly comparable.

- **Population size not justified**: The value `N = 2267000` is stated without reference or explanation. Hungary's 2010 population was approximately 10 million. If the authors intended to model a specific subset (e.g., the reporting catchment for the 19 counties in the dataset), they should explicitly state the source and year of this figure.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/results_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/local_loglikes_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/mifs_local_1.rds`
