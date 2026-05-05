# Peer Review: W21 Project 10
## "Time Series Analysis of COVID-19 in Georgia"

---

## Summary

This project analyzes COVID-19 case trajectories and vaccination dynamics in Georgia using ARMA models and three variants of a stochastic SEIR model implemented in pomp. The authors incorporate vaccination as an external intervention into the SEIR framework — first as a constant removal rate, then with a linear trend term, and finally as a rate parameter — and use forward simulation to assess visual model fit. While the topic is timely and the effort to integrate vaccination dynamics into a mechanistic model is conceptually sound, the work has critical deficiencies. No likelihood-based inference is performed on the data: the models are calibrated entirely by manual parameter selection, and all fit assessment is visual. The particle filter was attempted (Appendix) but produced degenerate likelihoods (-Inf), which the authors did not resolve. As a consequence, no MLE, no profile likelihoods, no goodness-of-fit statistics, and no confidence intervals are reported. The ARMA analysis contains methodological errors in the LRT comparison. Several model specification issues — including a problematic vaccination implementation and a structural bug in Model 3 — further undermine the mechanistic interpretation.

---

## Major Issues

### 1. No Likelihood-Based Inference Performed

The entire POMP analysis (Models 1, 2, and 3) relies on manually selected parameter values and visual comparison to data. No `mif2()` optimization, no particle filter likelihood, and no formal parameter estimation is carried out in the main body of the report. The Appendix acknowledges that particle filter runs produced `-Inf` log-likelihoods, but the authors were unable to resolve this and explicitly state that "local and global search" remain "unsolved obstacles." Consequently, the primary purpose of building a POMP model — likelihood-based inference — is not achieved. All claimed parameter values are calibrated by eye. This violates the fundamental practice of likelihood-based inference (Wheeler et al. 2024, §1) and makes formal model comparison and uncertainty quantification impossible.

**Fix:** The authors must resolve the degenerate particle filter (likely caused by the binomial measurement model applied to a large-scale SEIR state; see Issue 2) and run `mif2()` with appropriate computational effort to obtain MLEs. All reported parameter values should derive from this optimization.

---

### 2. Binomial Measurement Model Applied to Accumulator State H Causes Degenerate Likelihood

The measurement model in all three POMP models uses `dbinom(reports, H, rho, give_log)` in `dmeasure` and `rbinom(H, rho)` in `rmeasure`. The `H` state is an integer accumulator of daily recoveries from the I compartment. For a binomial distribution, `H` must be a non-negative integer and must be at least as large as the observed `reports`. However, with a 7-day rolling mean applied to daily case data (producing fractional values), and with the Euler step size of `delta.t = 1/8`, the accumulated `H` at each observation time can frequently be very small or even zero relative to the observed reports, causing `dbinom(reports, H, rho)` to return zero probability (and log-likelihood of `-Inf`). This is the most likely cause of the `-Inf` log-likelihoods reported in the Appendix. The Appendix attempt to switch to `dnbinom(reports, H, rho)` is also misspecified: the R function `dnbinom` has signature `dnbinom(x, size, prob)`, where `size` is the dispersion parameter — placing `H` in the `size` position makes the size data-dependent, which is unusual and almost certainly unintended.

**Fix:** Use a negative binomial measurement model with a fixed or estimated dispersion parameter `k`: `lik = dnbinom_mu(reports, mu = rho * H, size = k, give_log)`. The observation should be linked to `rho * H` (expected reports), not to `H` as a size parameter. Both `dmeasure` and `rmeasure` must use consistent parameterizations.

---

### 3. Visual-Only Goodness-of-Fit Assessment

All three models are assessed purely by visual comparison of simulated trajectories to data. No log-likelihood values are computed or reported for the main models, no AIC comparisons are made, and no quantitative goodness-of-fit metrics are provided. Wheeler et al. (2024) explicitly note: "Visual comparisons alone are only a weak and informal measure of goodness-of-fit." The authors' characterization of Model 1 as "perfectly simulating" the peak and initial values based on visual inspection is not a valid scientific claim without quantitative support.

**Fix:** Report log-likelihood values for each model. If the particle filter degeneracy is resolved (Issue 2), compute `pfilter()` log-likelihoods at the manually selected parameter values as a minimum; ideally, optimize via `mif2()` and report the MLE log-likelihood alongside AIC for model comparison.

---

### 4. Vaccination Subtraction Can Drive S Below Zero (Critical Model Bug)

In Models 1 and 2, the susceptible compartment is updated as `S -= (dN_SE + 2500)` (Model 1) or `S -= (dN_SE + 2200 + index*4)` (Model 2). No check is made to ensure that `S` remains non-negative after this update. With `delta.t = 1/8`, the per-step removal is `2500/8` (for Model 1) from a vaccine term alone. As `S` decreases over time, the unconstrained subtraction will eventually drive `S` to negative values, producing nonsensical model dynamics (negative susceptible counts) and causing downstream binomial draw attempts with invalid arguments. This is a structural defect that would cause the particle filter to fail even if the measurement model were corrected.

**Fix:** Add a guard: `S = fmax(S - (dN_SE + V), 0)` and similarly for Model 2, or restructure vaccination as a binomial draw from S (as in Model 3) to ensure S remains non-negative by construction.

---

### 5. Model 3 Vaccination Rate Draws From Wrong Compartment

In Model 3, the vaccination flow is specified in the equations as `N_SV = binomial(I, 1-exp(-mu_SV*dt))`, yet the Csnippet correctly implements it as `double dN_SV = rbinom(S, 1-exp(-mu_SV*dt))`. The mathematical description uses `I` (the infectious compartment) as the base for vaccination draws, which is biologically meaningless — one cannot vaccinate from among the infectious. The inconsistency between the equation (line 544 in the Rmd: `N_{SV} = binomial(I, 1-exp(-\mu_{SV}*dt))`) and the code (which correctly uses `S`) represents a model-code discrepancy of the type Wheeler et al. (2024) highlight as a reproducibility failure. While the code is correct, the stated mathematical model is wrong and will mislead readers.

**Fix:** Correct the mathematical equation to `N_{SV} = \text{Binomial}(S, 1-\exp(-\mu_{SV}\cdot dt))` to match the Csnippet implementation.

---

### 6. No Benchmark Comparison for the POMP Model

No non-mechanistic statistical benchmark (e.g., ARMA, auto-regressive negative binomial) is compared against the POMP models. Wheeler et al. (2024) identify this as a key diagnostic: without such a comparison, "it is impossible to assess whether the mechanistic model captures meaningful structure beyond what a simple statistical model would achieve." The ARMA analysis in Section 3 models vaccination counts and COVID-19 cases separately and does not produce a forecast or likelihood for new daily cases in the POMP observation period. No attempt is made to compare the mechanistic model's fit to the ARMA fit on the same data.

**Fix:** Fit an ARMA or auto-regressive negative binomial model to the same 105-day daily case series used by the POMP models, compute its log-likelihood, and compare this to the POMP model log-likelihood. This comparison is required to establish that the mechanistic model adds predictive value.

---

### 7. Likelihood Ratio Test Applied to Mismatched Models

The LRT comparing model0 (ARIMA(1,1,1) for `people_fully_vaccinated`) to model1 (ARIMA(4,1,4) for `daily_vaccinations`) is invalid. These two models are fitted to different outcome variables: model0 uses `vaccine_data$daily_vaccinations` (line 188) while model1 uses `vaccine_data$daily_vaccinations` as well (line 189), but the AIC table was computed for `people_fully_vaccinated` (line 171). The coefficient table reported after the LRT (line 242) calls `model0$coef`, which is the ARIMA(1,1,1) for daily vaccinations — not for the model described in the AIC table. Furthermore, the test statistic is compared to a chi-squared distribution with 2 degrees of freedom (`pchisq(delta_ll, 2)`), but the difference in parameters between ARIMA(1,1,1) and ARIMA(4,1,4) is 6 parameters (3 AR + 3 MA), not 2. The degrees of freedom are incorrect.

**Fix:** Clarify which outcome variable each model is fitted to; refit consistently on the same outcome; and correct the LRT degrees of freedom to reflect the actual difference in number of parameters.

---

### 8. No Parameter Identifiability Assessment

No profile likelihoods or confidence intervals are computed for any parameters. With 6–7 free parameters and a 105-observation time series, identifiability is a real concern: beta, mu_EI, mu_IR, rho, and eta are potentially correlated, and the vaccine parameters add additional dimensions. The authors fix mu_IR = 0.09 (effectively fixing 1/infectious period = 11 days) and eta without estimation, but it is not clear these constraints are sufficient to ensure identifiability. Wheeler et al. (2024) emphasize that profile likelihoods should be computed for key parameters to assess whether they are identifiable. None are presented.

**Fix:** After resolving the particle filter degeneracy and running mif2, compute profile likelihoods for at least Beta, rho, and mu_EI.

---

### 9. POMP Models Applied to Only 105 Observations of Rolling-Mean Data

The data used for the POMP models (`dat`) is a 7-day rolling mean of daily cases over days 299–409 of the pandemic (January–April 2021). Applying a rolling mean transforms the data: the smoothed observations are not independent draws from the stated binomial measurement model, as the rolling mean introduces autocorrelation. The `rollmean` function is applied and the result is directly fed as the `reports` column to the pomp object. This means the measurement model `reports ~ Binomial(H, rho)` is misspecified: the rolling-mean observations are continuous and autocorrelated, not integer-valued and independent. This creates a fundamental mismatch between the data and the measurement model.

**Fix:** Use original daily case counts (not rolling means) as the observation series, or adopt a measurement model that accounts for the smoothing-induced autocorrelation.

---

### 10. `index` State Variable in Model 2 Not Declared in partrans; Linear Vaccination Term Is Unbounded

In Model 2, `index` is used as a state variable that increments by 1 at each Euler step (`index += 1` in the Csnippet). With `delta.t = 1/8`, over 105 observation days, `index` reaches approximately `105 * 8 = 840`. The vaccination subtraction from S becomes `2200 + index * 4`, which at the end of the series reaches `2200 + 840 * 4 = 5560` per Euler step, or `5560 * 8 = 44,480` per day. The authors state this approach "might lead to an early stop," but do not note that the linear term becomes unrealistically large. More critically, `index` is declared in `statenames` but the vaccine slope `c` (written as the constant 4 in the code) is hardcoded rather than estimated, and `c` does not appear in `paramnames`. This prevents optimization of the vaccination slope.

**Fix:** Either use the actual vaccination covariate (interpolated vaccination counts) as a pomp covariate table rather than an internal state, or estimate the slope as a free parameter in paramnames. Hardcoding the slope precludes likelihood-based optimization.

---

## Minor Issues

- **Data loading from external URLs**: Sections 3 and 4 each reload the raw data from GitHub URLs (`raw.githubusercontent.com`) rather than using local files. This makes reproducibility contingent on external URL stability and network access at render time. The introduction states local files (`us-states.csv`, `us_state_vaccinations.csv`) are available, but the modeling sections re-download from the internet.

- **mu_IR not declared in partrans**: In all three models, `mu_IR` appears in `paramnames` and in the rprocess Csnippet, but is not included in `partrans = parameter_trans(log=c("Beta","mu_EI"), logit=c("rho","eta"))`. Because `mu_IR` is a rate (must be positive), it should receive a `log` transformation in partrans. Without this, IF2 could push mu_IR to negative values during optimization.

- **Section 2.1 and Introduction are duplicated**: The data description (sources, sample size, filtering) is stated identically in both the Introduction (pp. 1–2) and Section 2.1 (pp. 2–3). This adds approximately one page of verbatim repetition.

- **N population values inconsistent across models**: Model 1 uses `N = 10610000`; Model 2 uses `N = 10610000`; Model 3 simulation uses `N = 10620000`; the introduction states the 2019 census estimate is 10.62 million. These small discrepancies suggest copy-paste inconsistencies that were not reconciled. Per the `pomp-cross-model-param-reconciliation` skill, shared parameters should be identical across models.

- **No random seeds for reproducibility in main models**: While `set.seed(10000)` is used before the simulation calls, the seeds are set inside the `simulate()` call blocks. The models themselves have no fixed seed for the particle filter or any future optimization. Reproducibility requires seeds to be documented for all stochastic computations (code supplement checklist).

- **Susceptible population formula double-counts recoveries**: The EDA section computes `susceptible = population - fully_vaccinated - deaths - cases`, where `cases` is cumulative reported cases (including both recovered and deceased). This formula may double-subtract deaths (once through `deaths` and once through `cases` which includes fatal cases). The authors should clarify whether `cases` includes or excludes deaths in the NYT dataset.

- **No convergence traces or ESS diagnostics**: Even the Appendix particle filter runs show only a `plot(pf)` call, which would produce ESS and conditional log-likelihood diagnostic plots — but these plots are not included in the rendered document. Including them would have been informative for diagnosing the degeneracy.

- **References use raw URLs rather than formal citations**: All references are listed as raw URLs rather than formatted bibliographic entries. A single Wikipedia URL is cited as the basis for the R0 = 3.5 claim (Reference [6] links to a clinical paper, but [4] links to course notes without a permanent identifier). These should be replaced with proper citations.

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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-design-variable-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/ode-compartment-observation-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project10/blinded.Rmd`
