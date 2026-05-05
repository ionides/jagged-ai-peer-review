# Peer Review: W24 Project 14
## Tuberculosis Incidence in the U.S. — ARIMA and POMP Analysis

---

## Summary

This project analyzes annual U.S. tuberculosis (TB) case counts from 1953 to 2020 using two modeling approaches: an ARIMA time-series model and a SEIRS-compartment POMP model. The ARIMA section is methodologically careful, including an AIC-based model selection table, root diagnostics, and residual checks. The POMP section sets up a stochastic SEIRS model in C via Csnippets and incorporates a time-varying transmission rate and gamma white noise for process stochasticity. A negative binomial measurement model is specified. The authors are transparent about the limitations of their work and explicitly acknowledge that a global search was not completed.

The analysis has notable strengths in the ARIMA component and in the clarity of the POMP model motivation, but the POMP inference component is severely incomplete: no global search is performed, no profile likelihoods are computed, no benchmark comparison is made, and the accumulator variable is semantically mismatched to the observation data. Several structural issues in the compartment dynamics and measurement equations further undermine the conclusions.

---

## Major Issues

### 1. Accumulator variable tracks recoveries, not new infections

The Csnippet rprocess accumulates `H += dN_IR` — the flow from I to R, i.e., recoveries. However, `dmeasure` links the observed count `Number` (annual reported TB cases) to `rho * H` via a negative binomial distribution. Annual reported TB cases represent newly diagnosed infections entering the system, not individuals who have already recovered. The accumulator should track `dN_SE` (or `dN_EI`) — new exposures or new infectious-stage entries — not recoveries. This semantic mismatch causes the reporting-rate parameter `rho` to absorb the ratio of annual recoveries to true incidence, and all estimated transition-rate parameters are distorted to compensate. The consequence is that reported parameter estimates, simulated trajectories, and any model-fit interpretation are unreliable. (See: POMP checklist §12, Measurement model specification; POMP accumulator semantic audit.)

### 2. No global parameter search performed — reported estimates are unreliable

The authors explicitly state: "As a future scope, we aim to try global search method to find the best parameters. Due to time constraint it was not possible to run global search." The single `mif2` call uses a single fixed starting point with `Np = 2000` and `Nmif = 50`. Without a global search from diverse random starting points, there is no basis for claiming the reported log-likelihood of −628.8447 or the reported parameter vector is near the MLE. The parameter box is never explored. All parameter estimates and conclusions about the POMP model's adequacy are invalidated by this omission. (See: POMP checklist §6, Computational adequacy; Wheeler et al. 2024.)

### 3. No benchmark comparison against a non-mechanistic model

The POMP model is never compared quantitatively against a statistical baseline. While an ARIMA(0,1,5) model is fitted earlier in the report, no log-likelihood or AIC comparison between the ARIMA model and the POMP model is presented. Without such a comparison, it is impossible to assess whether the mechanistic SEIRS model captures structure beyond what a simple time-series model achieves. Wheeler et al. (2024) note that none of the 32 papers in their review performed this comparison, and their auto-regressive negative binomial benchmark revealed that some mechanistic models failed to beat it. (See: POMP checklist §2, Benchmark comparison.)

### 4. No profile likelihoods or confidence intervals for any parameter

The report presents no profile likelihoods and no uncertainty quantification for any of the 13 model parameters. It is therefore unknown whether any parameter is identifiable from these 68 annual observations. Given the large number of parameters relative to the data length, unidentifiability is a serious concern. The rate parameters `mu_EI = 128.9` and `mu_RS = 33.8` in particular are implausibly large on a per-year scale (mu_EI = 128.9 /year implies mean latency of roughly 2.8 days; mu_RS = 33.8 /year implies immunity loss in roughly 11 days) and may reflect optimization pathology rather than biological signal. (See: POMP checklist §5, Parameter identifiability and uncertainty.)

### 5. Force-of-infection equation is inconsistent between the text and the Csnippet

The narrative states the transmission rate is modified as `mu_IR = (β − β_t · (t − 1952)) · I · S / N · dγ/dt`, using the label `mu_IR` for the force of infection (a naming collision with the recovery rate also called `mu_IR`). The Csnippet defines `foi = (Beta - Beta_t * (t - 1952)) * I / N` and applies it as the rate for the S→E transition (`dN_SE`). The text equations (lines ~544–548) show a separate S→E ODE involving `dw(t) · β · SI/N`, but the discrete stochastic equations (lines ~556–561) are inconsistent: `dN_SE` uses only `dw(t) · β · I/N · δt` without the time-varying `β_t` term. This creates a discrepancy between the stated model and the implemented model. (See: POMP checklist §12, code-supplement-checklist §Traceability.)

### 6. Fixed population N ignores 70 years of U.S. demographic change

The total population `N` is fixed at 333,000,000 (the 2023 U.S. population) for the entire period 1953–2020. The U.S. population in 1953 was approximately 160 million — roughly half the 2023 value. Using the wrong population denominator inflates the effective transmission rate and biases the reported per-capita contact rate, distorting all parameters that depend on `I/N`. The authors acknowledge this limitation in the "Further Investigation" section but treat it as a minor future improvement rather than a substantial bias in the current analysis. (See: POMP checklist §11, Corroboration with scientific knowledge.)

### 7. Measurement model fits incidence counts but pomp object uses Rate as observation variable in one code block

An intermediate R-function SEIR block (lines ~621–635) defines `seir_dmeas` operating on `Rate`, while the subsequent Csnippet block (lines ~669–691) defines `seir_dmeas` operating on `Number` and creates the actual model object `TBseir_C` used for all inference. The `pomp()` call sets `obsnames = 'Number'`. The data object passed to `pomp()` is `data` which contains both `Year` and `Number` columns (cases counts). The Rate-based version is silently overwritten. The mismatch means the intermediate R-function object (`TBseir`) and the final C-snippet object (`TBseir_C`) correspond to different measurement models. Only `TBseir_C` appears in inference, but the duplication creates unnecessary confusion and reproducibility risk.

### 8. Discrete stochastic transition equations are inconsistent with the stated ODE system

The stated stochastic difference equations (lines ~556–561) show `dN_SE = Binom(S, 1 − exp(−dw · β · I/N · δ))` — using only a constant `β` without the time-varying `β_t` correction and without the `fmin` clamping shown in the Csnippet. Meanwhile, the Csnippet uses `foi = (Beta − Beta_t · (t − 1952)) · I/N` with gamma white noise applied as `dN_SE = rbinom(S, 1 − exp(−dw · foi · dt))`. The written-out difference equations do not match the implemented Csnippet. Readers cannot verify the model from the text alone. (See: POMP checklist §12; code-supplement-checklist §Traceability.)

---

## Minor Issues

### 9. Single mif2 convergence trace shown without discussion

The `plot(mif_out)` output is shown, but no interpretation of the convergence traces is provided. The traces for `mu_EI` and `mu_RS` plateau at values that imply sub-week biological time scales (mu_EI ≈ 129/year), which is biologically implausible for TB (mean latency typically 2–12 weeks). The authors do not flag these values as suspicious or interpret them as potential evidence of model misspecification. (See: POMP checklist §4, Model diagnostics.)

### 10. ARIMA model fit on case counts but AIC table caption says "incidence rate"

The AIC table caption reads "AIC of some ARIMA models (incidence number)" while the smallest-root table caption reads "Smallest roots of ARIMA models (incidence rate)." The model is fitted to `tb_num` (the raw case counts), not the incidence rate. The incidence rate caption is misleading. Additionally, the ARIMA model is fitted to the unlogged counts, which may be inappropriate given the wide dynamic range (84,304 in 1953 to 7,174 in 2020 — more than a 10-fold decline). A log transform is typically preferable for count data with such strong trends and heteroscedasticity.

### 11. Hard-coded absolute path to external image file

Line ~493 embeds `src="/Users/shreya/Desktop/Winter/stats_531/PROJECT2/seirs_draw.png"`. This path is author-specific and non-portable. The diagram will not render for any other reader and fails the basic platform-independence requirement of a reproducible supplement. (See: code-supplement-checklist §Platform Independence.)

### 12. ARIMA model selection based on AIC alone without model adequacy checks being shown

The model selection table includes AIC values and smallest roots, but the `simulation_times = 0` argument in the `model_selection_table()` call (line ~382–386) disables the bootstrap CI coverage check for the final selection step. The residual normality and ACF diagnostic tables are computed but not discussed in the narrative. The selected model ARIMA(0,1,5) has a smallest root of 1.05, which is very close to the unit circle and may indicate near-cancellation.

### 13. No goodness-of-fit quantification for the POMP model beyond a single log-likelihood value

The report states the best log-likelihood found is −628.8447 but provides no context: no comparison to the saturated model, no AIC, no comparison to the ARIMA log-likelihood (which is evaluated under a different observation model and therefore not directly comparable without adjustment). A single log-likelihood number without context does not constitute a quantitative goodness-of-fit assessment. (See: POMP checklist §3, Quantitative goodness-of-fit reporting.)

### 14. Effective sample size not monitored during particle filtering

No ESS diagnostics are reported. Given that `Np = 2000` is used for a model with 13 parameters, particle degeneracy is a real concern, particularly in the early decades of the 1950s–1960s where TB incidence was high and rapidly declining. Persistent ESS collapse would indicate model-data mismatch or insufficient particles. (See: POMP checklist §4, Model diagnostics; simulation checklist §10.)

### 15. No assessment of initial condition sensitivity

Initial proportions `S_0, E_0, I_0, R_0` are estimated as parameters via a barycentric transformation, but the report does not discuss the plausibility of the estimated values (`S_0 = 0.754, R_0 = 0.245` implies roughly 75% susceptible in 1952 with 24.5% having recovered immunity, at a time when TB had been endemic for decades). No sensitivity analysis is performed. Wheeler et al. (2024) document that initialization choice can shift AIC by ~72 units. (See: POMP checklist §13, Initial conditions.)

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
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
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project14/TB_data_usa.csv`
