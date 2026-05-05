# Peer Review: W25 Project 05 — Analysis of Malaria Cases in Florida

---

## Summary

This project applies SARIMA and SEIR-based POMP models to monthly reported malaria cases in Florida (2006–2016). The SARIMA section is generally competent, but the POMP section contains several critical implementation errors, weak inferential choices, and methodological inconsistencies that substantially undermine the reliability of the results. The project is an admirable attempt to adapt an existing dengue model to malaria, but the adaptation introduces new problems without fully resolving them.

---

## Weaknesses (Most Critical First)

### 1. [Critical] Immigration model is never actually incorporated into the POMP object

The code in chunk `setup-immi` updates the R objects `paramnames` and `rproc` in memory, and sets new coefficients on `seir_spline_model` via `coef(seir_spline_model) <- c(...)`. However, there is no second `pomp(...)` call that rebuilds the model with the new `rproc` (containing `immigration_rate`) and updated `paramnames`. The original `seir_spline_model` was compiled against the old C-snippet and old `paramnames`. Setting coefficients does not recompile the process model. As a result, the "POMP Model with Immigration" local and global searches almost certainly ran using the original process model without immigration dynamics, invalidating the entire comparison between the two POMP models. This is the most serious technical error in the project.

### 2. [Critical] `lambda` is not multiplied by `dt` in the Euler step for `dSE`

In both `rproc` C-snippets (lines 373–375 and 570–572), the force of infection `lambda` absorbs the Gamma noise term `dW` (which already scales with `dt` through `rgammawn`), but the transition probability for `dSE` is `1 - exp(-lambda)` rather than `1 - exp(-lambda * dt)`. Since `lambda` is not separately multiplied by `dt`, the per-step transition probability for `S -> E` does not correctly scale with step size. This is a standard Euler-Multinomial bug that makes the model step-size dependent and gives inflated infection rates at small `dt`. The other transitions (`mu_EI`, `gamma`, `mu_H`, `r`) do use `dt` correctly.

### 3. [Critical] The SARIMA log-likelihood comparison (-96 vs -328) is not meaningful as stated

The text concludes there is "a significant scope for improvement" because the SARIMA log-likelihood is "-96" compared to the POMP log-likelihood of "-328." However, the SARIMA model was fitted on log-transformed counts (`log1p(Y)`), while the POMP model observes raw counts `Y`. These likelihoods are on different scales and with respect to different probability distributions; they cannot be directly compared numerically. No Jacobian adjustment is applied to convert the SARIMA log-likelihood to the scale of counts, nor is this acknowledged in the text. The conclusion drawn from this comparison is therefore unsupported.

### 4. [Major] `sigma_M` is defined and listed as an estimated parameter but is never used

The parameter `sigma_M = 0.3` appears in `paramnames` and in the coefficient table description ("Fixed measurement overdispersion"), and it appears in `par_trans` (where it is log-transformed). However, `rmeas` and `dmeas` use only a Poisson distribution with mean `rho * I + 1e-6` — `sigma_M` does not appear in either C-snippet. This is internally inconsistent: the model claims overdispersion but implements none. A negative binomial or compound Poisson measurement model would be needed to use `sigma_M` meaningfully.

### 5. [Major] Cumulative cases `C` accumulate `rho * dEI` but observations are linked to `I`

The state variable `C` is declared as an `accumvar` and incremented as `C += rho * dEI`, implying it tracks reported exposed-to-infectious transitions. But the measurement model links observations to `I` directly: `Y ~ Poisson(rho * I)`. These two representations are inconsistent — `C` is computed but never used in the measurement model, and its role in the model is unclear. This represents a conceptual disconnect between the state space and the observation model.

### 6. [Major] Population size `N_0 = 100000` is unrealistically small and not justified

Florida's population during 2006–2016 was approximately 18–20 million. Setting `N_0 = 100000` makes the model represent a small sub-population rather than the state, and this choice is never justified or discussed. Moreover, `N_0` is not perturbed in either local or global searches (it does not appear in `rw.sd`), so the model never explores whether a different population size improves fit. This fixed, unsupported value directly affects `lambda = beta * (I + epsilon) / N` and hence the entire transmission dynamics.

### 7. [Major] Birth rate `r = 0.135` is implausibly large and inconsistent with `mu_H`

An `r = 0.135` per month would imply a population growing by ~13.5% per month, which is biologically impossible for humans. If interpreted as an annual rate, 13.5% per year is still far above typical human birth rates (~1–1.5% per year for Florida). This parameter is also never explored in the local search (absent from `rw.sd` in the initial local search) and is set to `runif(1, 0, 0.001)` in the global search, suggesting the authors themselves recognized after the fact that it should be near zero. The initial value and its impact on model dynamics during the early search are not discussed.

### 8. [Major] The `global_inits` construction uses `c(base_params, c(...))`, creating duplicate parameter entries

In the global search, `global_inits` is built by combining `base_params` (the full current coefficient vector, including `b_1` through `b_5`, `g`, etc.) with a second list that overrides the same parameter names. In R, `c()` on named vectors with duplicate names does not replace but appends, creating duplicate entries. When `mif2` receives this parameter vector, the behavior is undefined or will use the first occurrence. The global search parameter initialization is therefore unreliable, meaning the purported exploration of parameter space may not have been executed correctly.

### 9. [Major] No likelihood profile or parameter uncertainty quantification is provided

The project performs local and global searches but presents no likelihood profiles, confidence intervals, or profile likelihood plots for any parameter. The trace plots are shown only to diagnose convergence but no attempt is made to characterize the uncertainty of estimated parameters (e.g., `rho`, `mu_EI`, `gamma`, `immigration_rate`). For a POMP analysis, this is a significant gap in the inferential framework.

### 10. [Moderate] The periodic B-spline is not truly periodic

The `periodic.bspline.basis` function uses `splines::bs()` evaluated at `t %% period`, which maps time onto the period interval. However, `splines::bs()` does not enforce periodicity at the boundary — the spline value at `t %% period = 0` will generally not equal the value at `t %% period = 12`. The `pomp` package provides `periodic_bspline_basis()` specifically for this purpose. Using a non-periodic spline for seasonality modeling undermines the motivation for using splines over a simple sinusoidal forcing.

### 11. [Moderate] The force of infection is missing the `* dt` in the mathematical equations

In the model equations (line 304), the force of infection is written as:

```
lambda(t) = exp(...) * (I(t) + epsilon) / N(t) * dW(t)
```

This is the stochastic differential form, which does not include a `dt` multiplier. Yet in the Euler step, the correct Euler-Multinomial approximation requires the hazard to be multiplied by `dt`. The mathematical exposition and the code are inconsistent about whether and how `dt` enters, contributing to the dimensionally ambiguous implementation noted in weakness 2.

### 12. [Moderate] `mu_H` is described as "natural death rate" but labeled "Mean duration of immunity loss"

In the coefficient table and code comments, `mu_H = 1/900` is described as "Mean duration of immunity loss ~900 days (~2.5 years)." However, in the model equations, `mu_H` governs `dSM`, `dEM`, `dIM`, and `dRM` — deaths from all compartments — making it the natural death (mortality) rate, not an immunity waning rate. These are distinct biological quantities. There is no waning immunity (R->S) flow in the model structure, so the comment is simply incorrect.

### 13. [Moderate] AIC model search grid is too narrow

The SARIMA model search considers only `p_max = 1`, `q_max = 1`, `P = 1`, `Q = 1`, restricting the search to a 4x4 grid. No rationale is given for excluding higher-order models, and the ACF analysis shows significant correlations at many lags beyond lag 1. The text calls this search comprehensive and selects SARIMA(0,1,1)(0,1,1)[12] as the best model, but this conclusion is only valid within the restricted grid.

### 14. [Minor] The `decompose()` function uses an additive decomposition without justification

The STL-like decomposition is performed using `decompose(monthly_ts)`, which defaults to an additive model. The text notes possible non-constant variance and then proceeds to use a log transformation, but the decomposition plot itself uses the untransformed series. Performing decomposition on the original scale while also discussing non-constant variance is slightly inconsistent.

### 15. [Minor] No formal residual diagnostic tests for SARIMA are conducted

The residual analysis for SARIMA is limited to visual inspection of the residual plot, ACF, and Q-Q plot. No Ljung-Box test or formal normality test (e.g., Shapiro-Wilk) is applied to corroborate the visual assessments. Given that the authors describe the fit as "excellent," formal tests would strengthen this claim.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project05/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project05/Makefile`
