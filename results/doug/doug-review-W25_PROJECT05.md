# Peer Review: W25 Project 05
## Analysis of Malaria Cases in Florida

---

## Summary

This project analyzes monthly malaria case counts in Florida (2006–2016) using both SARIMA and POMP-based SEIR models. The authors fit a SARIMA(0,1,1)(0,1,1)[12] model to log-transformed monthly counts and then adapt a dengue SEIR model with periodic B-splines and process noise from Subramanian et al. (2020) to the same data. They extend the SEIR model by adding an immigration parameter to capture imported infections, which is epidemiologically motivated given that malaria is locally eradicated in Florida. Strengths include a clear biological motivation for the immigration extension, use of mif2/pfilter for proper likelihood-based inference, and an appropriate process noise structure. However, the POMP analysis suffers from severe methodological gaps: the measurement model is misspecified relative to what the text describes, no non-mechanistic benchmark is compared against the POMP model, the global search is inadequate in scale (20 replicates, 100 iterations), no profile likelihoods are computed, no convergence evidence is presented, and the comparison between SARIMA and POMP log-likelihoods is invalid due to differing observation models and data transformations.

---

## Major Issues

### 1. Invalid comparison between SARIMA and POMP log-likelihoods

The paper concludes (p. final section) that the SARIMA model fits much better than the POMP model based on log-likelihoods of approximately −96 vs. −328. This comparison is statistically invalid for at least two reasons. First, the SARIMA model is fitted to log-transformed case counts (`log1p(Y)`) under a Gaussian assumption, while the POMP models are fitted to the original count scale under a Poisson observation model. These likelihoods are evaluated under different observation models on different data scales and cannot be compared numerically. Second, the ARIMA model performs differencing internally, altering the effective data further. A valid comparison requires either evaluating both models under a common observation model on the identical untransformed data, or using proper scoring rules such as CRPS. This is a central conclusion of the paper and it rests on an invalid comparison. See the sarima-baseline-audit skill criteria.

### 2. Measurement model is inconsistent between text and code

The paper states the observation model is Poisson-distributed on rho * I_t (the infectious compartment at the current time point). However, the cumulative case accumulator `C` is declared in `accumvars` and updated inside rprocess as `C += rho * dEI`. The dmeasure and rmeasure Csnippets (`dmeas` and `rmeas`) are written as `dpois(Y, rho * I + 1e-6, give_log)` and `rpois(rho * I + 1e-6)`, respectively — linking observations directly to the current `I` compartment level, not to the period-specific cumulative incidence `C`. There is thus a fundamental mismatch: the accumulator tracks new exposures progressing through latency (proportional to dEI), but the measurement model links observations to the stock of current infecteds I. For malaria case reports, which typically reflect newly detected or diagnosed cases, the accumulator approach linking to dEI is epidemiologically more defensible than linking to I. The inconsistency means the likelihood evaluation does not match the stated model equations and should be corrected.

### 3. No non-mechanistic benchmark comparison

The POMP models are not compared to any non-mechanistic statistical benchmark evaluated on the same data and scale. The SARIMA comparison is invalid (Issue 1 above), and no auto-regressive negative binomial or Poisson benchmark is fitted on the original count scale to provide an objective baseline for the POMP models. Without such a comparison, it is impossible to assess whether the mechanistic model captures structure beyond what a simple empirical time-series model achieves. Wheeler et al. (2024) identify this as the single most important diagnostic check, noting that none of the 32 papers in their Haiti cholera review provided one.

### 4. Inadequate global search scale

The global search uses only 20 random starting points with 100 IF2 iterations (`Np = 2000`). For a model with 14 estimated parameters plus 5 spline coefficients, 20 replicates provides extremely sparse coverage of the parameter space. Standard practice for models of this complexity requires at least 200–400 global search replicates. The text acknowledges that the model may be stuck in a local optimum, but then dismisses this after finding only a marginal improvement — a conclusion that cannot be trusted given the sparse search. The reported best log-likelihood of approximately −328 may be substantially above the true MLE.

### 5. No profile likelihoods or confidence intervals

No profile likelihoods are computed for any parameter. Without profile likelihoods, it is impossible to assess whether parameters such as rho, g, immigration_rate, sigma_P, or the spline coefficients b_1–b_5 are identifiable from the data. The global search scatter plots (parameter vs. log-likelihood) shown in the paper are treated implicitly as informal profile plots but are not profile likelihoods — they are unconstrained scatter plots from a sparse global search and have no valid statistical interpretation for confidence intervals. This makes all stated or implied parameter estimates unreliable (Wheeler et al. 2024, Section on Parameter Identifiability).

### 6. No convergence diagnostics

While trace plots of parameters across IF2 iterations are shown, the paper does not show log-likelihood traces across iterations for either the local or global search. Without log-likelihood traces, it is unclear whether the optimizer converged or whether the reported log-likelihood values are near the true maximum. The paper correctly notes that "the model is weakly identifiable" based on parameter non-convergence in the trace plots, but does not investigate this further or interpret it in terms of model misspecification.

### 7. Measurement model lacks overdispersion

The observation model uses a Poisson distribution throughout. For monthly disease surveillance counts, which typically exhibit substantial overdispersion relative to Poisson (due to reporting variation, clustering, surveillance changes), a negative binomial measurement model is generally more appropriate. The paper includes a `sigma_M` parameter in `paramnames` and in parameter transformations, suggesting overdispersion was considered, but it is not actually incorporated into `dmeasure` or `rmeasure`. The Poisson measurement model will produce artificially high likelihoods for near-zero counts and underestimate uncertainty. Wheeler et al. (2024) recommend negative binomial observation models as standard practice.

### 8. Accumulator variable C is declared in accumvars but used incorrectly

The variable `C` is declared in `accumvars = "C"` in the pomp object, meaning pomp will automatically reset it to zero after each observation time. However, the measurement model links observations to `I` (not to `C`), so the accumulated value of `C` is never used in likelihood evaluation or simulation of observations. The accumulator is therefore dead code — it accumulates but is never read by dmeasure/rmeasure. This either means the intended model (Poisson on rho*C) was not implemented as planned, or the accumvars declaration is unnecessary and should be removed. Either way, the code does not implement the model as described.

### 9. Population dynamics specification is implausible for a ten-year US state dataset

The model fixes `N_0 = 100,000` as the initial population of Florida for a 10-year model, and also includes birth and death dynamics (`r = 0.135`, `mu_H = 1/900`). The actual population of Florida is approximately 19–21 million during 2006–2016. Using N_0 = 100,000 introduces a 200-fold population error. The force of infection `lambda = beta * (I + epsilon) / N` is consequently severely inflated: with N = 100,000 instead of ~20,000,000, the per-capita force of infection is 200 times larger, which distorts the transmission coefficient beta by the same factor. Furthermore, the birth rate r = 0.135 per month corresponds to an annual birth rate of over 100%, which is biologically impossible. These values render all estimated transmission parameters uninterpretable relative to known malaria biology. See the pomp-static-population-audit skill criteria.

### 10. Global search parameter box initialization error

In the global search code, `global_inits` is constructed as `c(base_params, c(...))` where `base_params` contains the current model coefficients and the second vector contains overrides for specific parameters. In R, when two named vectors are concatenated with `c()`, duplicate names are retained — the second set of values appended to the end do not override the first. As a result, the global starting parameter vectors contain duplicate entries for every parameter that appears in both `base_params` and the override vector (b_1 through b_5, g, rho, sigma_P, mu_EI, gamma, r, epsilon, mu_H, immigration_rate). When coef() later processes these parameters, only the first occurrence of each name is typically used, meaning the global search starting values are actually the fixed base_params values for all overridden parameters — the random initialization has no effect. The global search is therefore not a genuine global search but effectively 20 replicates of the local search.

---

## Minor Issues

- **Notation error in SARIMA equation**: The model equation is written as `(1+theta_1)(1+Theta_1*B^12) * epsilon_t` without correct use of the backshift operator. The non-seasonal MA polynomial should be `(1 + theta_1 * B)`, not `(1 + theta_1)`. This is a typographical error that makes the equation incorrect as written.

- **AIC grid search is narrow**: The SARIMA grid search explores only p, q in {0, 1} and P, Q in {0, 1}. The justification for this narrow range is not given. A standard grid search for a monthly series with obvious seasonality would typically explore p, q up to 3 or 4 to ensure the optimal order is found.

- **No Ljung-Box or formal residual test for SARIMA**: The paper relies on visual ACF inspection of residuals to conclude "no autocorrelation." A formal Ljung-Box test at multiple lags would provide stronger evidence. Visual ACF inspection alone may miss autocorrelation at lags outside the plotted range or near the significance threshold.

- **sigma_M is not used in the model**: The parameter `sigma_M` appears in `paramnames` and `parameter_trans` but is never referenced in `dmeasure`, `rmeasure`, or `rprocess`. This dead parameter adds to the apparent model complexity without providing any function. If measurement overdispersion was intended, sigma_M should be incorporated into the observation model.

- **Birth rate r = 0.135 is biologically implausible**: A per-month birth rate of 13.5% implies population doubling in roughly 5 months. Florida's annual birth rate is approximately 0.012 per year (~0.001 per month). The parameter value is off by two orders of magnitude and should be based on actual demographic data.

- **epsilon semantics are ambiguous**: The `epsilon` parameter appears in the force of infection as `(I + epsilon) / N`. With N = 100,000 and epsilon = 1, this is a negligible background term. However, the authors describe it as a "background risk pressure" without connecting it to any epidemiological mechanism. With I values that can be 0 or near-zero in a non-endemic setting, this term may dominate the force of infection when local infections are absent — but this is not discussed.

- **No convergence traces for local search**: Trace plots are shown only for the global search. The local search trace plots (or log-likelihood curves) are not presented, making it impossible to assess whether the local search converged before the global search began.

- **Simulation from best_local uses wrong parameter vector length**: In the simulation code (`sim_list <- simulate(seir_spline_model, params = unlist(best_local[1, 1:length(coef(seir_spline_model))]))`), the number of columns in best_local includes loglik and loglik.se at the end, so slicing to `length(coef(seir_spline_model))` may or may not correctly exclude those columns depending on the ordering. This is fragile code that should explicitly select parameter columns by name rather than by index.

- **No acknowledgment of model limitations for imported malaria**: The immigration parameter captures all imported cases as a constant-rate Poisson process. Imported malaria cases in Florida are likely heterogeneous in time (linked to travel patterns, origin countries, seasons), and a constant immigration rate may be a poor approximation. The paper does not discuss this limitation.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
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
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project05/blinded.Rmd`
