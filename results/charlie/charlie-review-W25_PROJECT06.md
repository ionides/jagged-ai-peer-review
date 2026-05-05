# Peer Review: W25 Project 06
## "Investigating Hungarian Chickenpox Infections"

---

## Summary

This project investigates weekly chickenpox case counts in Hungary (2005–2015) using three modeling frameworks: ARMA, a seasonally forced SEIRS-POMP model, and a deep-learning pipeline combining variational mode decomposition (VMD) with N-BEATS. The comparative scope is a genuine strength. However, the POMP component — the methodologically central contribution — contains several compounding implementation errors that invalidate its parameter estimates and the reported profile likelihood. Specifically, the local `mif2` call overrides the base `pomp` object's parameter transformations with an incomplete list, removing the logit constraint on the seasonal amplitude `amp` and the log constraint on the waning rate `omega`. This bug propagates into the global search (which inherits the broken `partrans` from the local result) and is confirmed by artifact inspection: all estimated `amp` values exceed 2.0, far outside the declared (0, 1) logit domain. Additionally, the profile likelihood for `rho` is a pseudo-profile — a filtered scatter of global-search results, not a dedicated profile IF2 search — making the reported confidence interval statistically invalid. The mathematical model specification in the text is inconsistent with the implemented Csnippet, and no quantitative benchmark comparison against the ARMA model is made on a common scale.

**Key strengths:** Combination of three modeling frameworks; use of negative binomial measurement model; some discussion of limitations; clear EDA.

**Key weaknesses:** `partrans` override bug invalidates all POMP parameter estimates; global search anchored to a corrupted local-search result; pseudo-profile CI; mathematical specification does not match code; no quantitative ARMA-vs-POMP comparison on a common observation model.

---

## Major Issues

### 1. `partrans` override in local `mif2` removes constraints on `amp` and `omega`

The base `pomp` object (chunk beginning at line 524) declares:
```
partrans = parameter_trans(
  log   = c("Beta", "mu_EI", "mu_IR", "k", "omega"),
  logit = c("eta", "rho", "amp")
)
```
The local `mif2` call (chunk `seir_local`, line 587) re-specifies:
```
partrans = parameter_trans(
  log   = c("Beta", "mu_EI", "mu_IR", "k"),
  logit = c("eta", "rho")
)
```
This new `partrans` argument **replaces** the base object's declaration entirely. `amp` loses its logit constraint and `omega` loses its log constraint. The IF2 optimizer is therefore free to drive `amp` beyond 1, which causes the seasonal forcing `Beta_t = Beta * (1 + amp * cos(...))` to become negative whenever `amp > 1` and the cosine reaches its minimum. The code guards against this with `if (Beta_t < 0) Beta_t = 0`, but the effective dynamics are biologically extreme: transmission is completely suppressed for part of the year.

Inspection of `mifs_local_1.rds` confirms the bug: all 20 local-search chains have final `amp` values between 2.1 and 2.8, far outside the declared (0, 1) domain. The global search results in `results_1.rds` show `amp` ranging from 1.12 to 1.76, all outside the logit constraint. The best-fit global parameters (loglik = −3758.96) include `Beta = 100.4` and `amp = 1.27`.

**Fix:** Remove the `partrans` argument from the `mif2` call entirely; the base object's declaration is automatically inherited. If the local `mif2` call must override `partrans` for any reason, it must include every parameter from the base declaration.

**Reference:** Wheeler et al. (2024), §Computational adequacy; `pomp-partrans-override-bug` skill.

---

### 2. Global search initialized from a corrupted local `mif2` result

At line 678 in the global search chunk (`seir_global`):
```r
mf1 <- mifs_local[[1]]
...
mf <- mf1 %>% mif2(params = c(unlist(guess), fixed_params), ...)
```
The first argument to `mif2()` is `mf1`, a previous `mif2` result object. Two distinct errors compound here:

(a) **Inherited broken `partrans`:** `mf1` carries the incomplete `partrans` from the local search (Issue 1), so the global search also runs without constraints on `amp` and `omega`.

(b) **Anchored initialization:** Passing a previous `mif2` result as the first argument inherits the cooling schedule of that chain. With `cooling.fraction.50 = 0.5` in the global call but a fully decayed schedule inherited from the local run, the effective exploration from the random starting points is severely curtailed.

The correct pattern is `mif2(chickenSEIR, params = c(unlist(guess), fixed_params), ...)` where `chickenSEIR` is the base `pomp` object. All global-search results reported in this project are affected by this error.

**Reference:** Wheeler et al. (2024), §Computational adequacy; `pomp-global-search-init-audit` skill.

---

### 3. Profile likelihood for `rho` is a pseudo-profile: CI is statistically invalid

The section "Profile Likelihood for Reporting Rate rho" (lines 780–813) constructs the profile by filtering the global search object `global_loglik_result` by log-likelihood value and plotting the result as a profile. No dedicated profile IF2 search is run:

- There is no `profile_design()` call.
- There is no foreach loop that fixes `rho` at grid values and optimizes the remaining parameters.
- There is no `rw.sd` construction that sets `rho = 0` to hold it fixed during optimization.

The code applies a cutoff of `maxloglik - 4` (a relaxed threshold, explicitly noted as deviating from the standard `0.5 * qchisq(df=1, p=0.95) ≈ 1.92`) to the global-search scatter and reads off `min_rho` and `max_rho`. This is a global-search scatter plot, not a profile likelihood curve. The chi-squared CI theorem requires that the curve plotted is the true profile, i.e., that at each fixed `rho` value the remaining parameters are optimized. That constrained optimization was never performed.

Additionally, the text (line 776) acknowledges "a clear peak in the likelihood surface near ρ ≈ 0.92," but inspection of `results_1.rds` shows that all 100 global-search results have `rho` values between 0.679 and 0.9997 — the scatter is sparse and the "profile" reflects sampling density from the global box, not a true profile.

**Fix:** Run a dedicated profile search using `profile_design(rho, lower=0.5, upper=1.0, nprof=20)` as starting points, with `rw.sd` setting `rho = 0` in the mif2 call. Evaluate log-likelihood at each result and apply the chi-squared threshold.

**Reference:** Wheeler et al. (2024), §Parameter identifiability; `pomp-pseudo-profile-audit` skill.

---

### 4. Mathematical model in text does not match the implemented Csnippet

The differential equations written in the SEIR Model Definition section (lines 451–462) include:

- $dS = \mu N - \beta(t) \cdot SI/N - \mu S$ (birth/death flux with rate $\mu$)
- $dI = \sigma E - \gamma I - \mu I + \lambda$ (importation term $\lambda$)

The text defines $\mu$ as birth/death rate and $\lambda$ as importation rate. Neither appears anywhere in the `seir_step` Csnippet. The code implements waning immunity ($\omega$, R→S transition) with no demographic birth-death flux and no importation. The section header says "SEIR" but the model includes R→S waning (`dN_RS = rbinom(R, 1 - exp(-omega * dt))`), making it an SEIRS model. The text acknowledges "SEIRS-type structures" in one sentence (line 464) but the equations and section title say SEIR.

This is a concrete reproducibility failure documented in Wheeler et al. (2024): when the mathematical description and code differ, readers cannot determine which represents the model that was actually fitted.

**Fix:** Replace the differential equations with a correct discrete-time stochastic specification that matches the Csnippet exactly. Update the section heading to SEIRS and remove $\mu$ (birth/death) and $\lambda$ (importation) from the parameter list.

**Reference:** Wheeler et al. (2024), §Reproducibility and extendability; code-supplement-checklist-pomp.md, Traceability section.

---

### 5. Best-fit `Beta = 100.4` is biologically implausible; no corroboration with independent evidence

The best global-search parameter estimate is `Beta = 100.4` per week. For a population of 2.267 million and an infectious period of about 2 weeks (`mu_IR ≈ 0.46`), this implies a basic reproduction number R₀ ≈ Beta/mu_IR ≈ 217. Published R₀ estimates for varicella are typically 3–10 in unvaccinated populations. The implausibly large `Beta` is a direct consequence of the `partrans` override bug (Issue 1): with `amp > 1`, the model periodically suppresses transmission to zero, and `Beta` inflates to compensate during the active season.

The paper does not compare any estimated parameter values against independent biological literature, which is required practice (Wheeler et al. 2024, §Corroboration with scientific knowledge).

**Fix:** Correct the `partrans` bug, rerun the optimization, and explicitly compare estimated `Beta`, `mu_EI`, `mu_IR`, and `rho` to published varicella natural history estimates.

---

### 6. `emeas` inconsistency with `dmeas`/`rmeas`

The `emeasure` Csnippet (line 521) computes expected observations as:
```c
E_infection = rho * H;
```
where `H` accumulates `dN_IR` (recoveries from I). But `dmeasure` and `rmeasure` both compute expected observations as `rho * NewEI`, where `NewEI = dN_EI` (E→I transitions). Furthermore, `H` is never declared in `accumvars`, so it accumulates all recoveries from t = 0 forward — it does not represent weekly counts. The `emeas` therefore computes a cumulative recovery count rather than a weekly new-infection count, which is the quantity used in `dmeas`/`rmeas`. This is an internal inconsistency: the expected value computed by `emeas` and the likelihood evaluated by `dmeas` are for different quantities.

**Fix:** Either (a) declare `H` in `accumvars` and change `emeas` to `E_infection = rho * H`, or (b) set `emeas` to `E_infection = rho * NewEI` to match `dmeas`/`rmeas`.

---

### 7. No quantitative comparison between ARMA and POMP models on a common scale

The paper proposes a "comparative analysis across traditional statistical time series models (ARMA), mechanistic epidemic modeling (POMP)" but the comparison is qualitative. The ARMA log-likelihood (−3603.29 under Gaussian) and POMP log-likelihood (best −3758.96 under negative binomial) are evaluated under different observation models on different response scales. Direct comparison of these numbers would be invalid (Wheeler et al. 2024, §Benchmark comparison), and the paper avoids doing so — but it also provides no valid quantitative comparison.

A proper benchmark test would fit an ARMA-type model with a negative binomial observation distribution (e.g., an auto-regressive negative binomial) to the same data and compare log-likelihoods. Alternatively, both models can be compared on a common predictive scoring rule (e.g., CRPS). Without this, the paper cannot support any claim about whether the mechanistic model captures meaningful structure beyond a statistical baseline.

**Reference:** Wheeler et al. (2024), §Benchmark comparison.

---

### 8. `start_params` undefined in local search code

The local `mif2` chunk (line 589) references `params = start_params`, but `start_params` is never defined in any visible code chunk in the document. The `chickenSEIR` object was initialized with default `params` at line 536, but `start_params` as a separate object is absent. This is a reproducibility failure: readers cannot determine the starting parameter values for the local search from the code as written.

**Fix:** Add `start_params <- coef(chickenSEIR)` (or an explicit definition) before the local search chunk.

---

## Minor Issues

### 9. All `rw.sd` entries use `ivp()` only; `omega` is not perturbed

Both the local and global search use:
```r
rw.sd = rw_sd(Beta=ivp(0.05), mu_EI=ivp(0.05), mu_IR=ivp(0.05),
              eta=ivp(0.02), rho=ivp(0.02), amp=ivp(0.05), phi=ivp(1), k=ivp(0.1))
```
The `omega` parameter (waning immunity rate) is entirely absent from `rw.sd` in both searches, meaning it is never perturbed by IF2 and remains at its starting value throughout optimization. The text in the Global Search section claims `omega` is among the parameters explored over the box bounds `[0.002, 0.01]`, but since `omega` receives no perturbation, the global search samples `omega` values only at initialization; they are not optimized. This is inconsistent with the claimed global exploration.

### 10. Ljung-Box degrees of freedom not corrected for estimated ARMA parameters

The Ljung-Box test at lag 20 uses 20 degrees of freedom (line 261), but the ARMA(4,4) model has 8 estimated AR/MA parameters plus an intercept. The effective degrees of freedom should be reduced by the number of estimated parameters (Box and Pierce, 1970; Ljung and Box, 1978). Using the uncorrected degrees of freedom makes the test anti-conservative for the ARMA(4,4) residuals.

### 11. Deep learning validation uses only 2-step ahead forecast accuracy

The N-BEATS model is evaluated on a 2-step (2-week) ahead forecast with MAPE of 2.5–3.0%. No out-of-sample test set split strategy is described: which weeks form the validation set? How many total observations are in validation vs. training? Without this, the 2.5% MAPE figure cannot be assessed for overfitting. Given 1220 input features and a relatively short training series (522 weeks), the risk of data leakage or overfitting is substantial.

### 12. AIC table comparison between linear and log-ARMA models is correctly noted as invalid but still computed

The paper correctly states that the AIC values 7226.58 (linear) and 507.41 (log-transformed) "are not directly comparable due to the change in data scale." However, the text still reports them side by side in a way that could mislead readers who do not notice the disclaimer. No Jacobian correction for the log transform is applied. The comparison should either be omitted or the log model should be evaluated by transforming predictions back to the original scale and computing a likelihood on the original counts.

### 13. `library(pomp)` called twice in setup chunk

Line 19-20 of the setup chunk calls `library(pomp)` twice consecutively. This is cosmetically redundant but does not affect results.

### 14. Convergence trace plot uses `melt()` from reshape2 without explicit import

The trace plot chunk (line 611) calls `melt()`, which requires the `reshape2` package (or `tidyr::pivot_longer`). The package is not loaded in the setup or POMP setup chunk. While the code loads `tidyverse` (which does not export `melt`), this may silently fail or produce unexpected behavior depending on which other packages are loaded. The supplement should explicitly load `reshape2` or replace `melt()` with `pivot_longer()`.

### 15. No `sessionInfo()` or package version documentation

The supplement does not record R version, `pomp` version, or any other package versions. The `pomp` API has changed substantially across versions. Results may not reproduce on current CRAN releases without version pinning via `renv` or similar. The Python requirements file (`requirements.txt`) lists packages without version pins as well.

**Reference:** Code-supplement-checklist-pomp.md, Documentation section.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/mifs_local_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/local_loglikes_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/results_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project06/requirements.txt`
