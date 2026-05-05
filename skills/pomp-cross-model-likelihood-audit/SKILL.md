---
name: pomp-cross-model-likelihood-audit
description: Use when reviewing a project that compares log-likelihoods or AIC values across ARMA, GARCH, and POMP (or other mixed model-class) fits to the same time series, to detect invalid cross-class likelihood comparisons where the models' likelihoods are not computed under a common observation model and therefore cannot be ranked numerically.
---

# pomp Cross-Model Likelihood Audit

## Purpose

A recurring error in financial time series projects (and other applied POMP analyses) is comparing log-likelihoods — or AIC values derived from them — across model classes (e.g., ARMA, GARCH, POMP stochastic volatility) as if they are numerically comparable. They are not: ARMA, GARCH, and POMP stochastic volatility models differ in their conditioning (unconditional vs. conditional on lagged squared residuals), their latent variable structure, and their effective observation models. A model with a higher log-likelihood is not necessarily a better fit to the data when the likelihoods are computed under different generative assumptions.

This error is non-obvious to students who correctly understand that AIC enables model comparison but do not recognize that AIC requires a common observation model (or at minimum, a common likelihood function computed on the same response variable with the same conditioning set).

This skill provides a targeted checklist for detecting and characterizing this class of error.

## When to Activate

Use this skill when:
- A project fits two or more model classes (e.g., ARMA + GARCH, GARCH + POMP, ARMA + POMP, or all three) to the same observed time series.
- The project presents a table or narrative comparing log-likelihoods or AIC values across those model classes.
- The project draws a conclusion about which model is preferred based on cross-class log-likelihood or AIC ranking.

Do not use this skill when comparing models within the same class (e.g., GARCH(1,1) vs. GARCH(4,2), or two competing POMP models). Within-class likelihood comparisons are valid when the models share the same observation model.

## Procedure

### 1. Identify all model classes being compared

List every model fit in the project and its class:
- ARMA/ARIMA: fit by `arima()`, likelihood is Gaussian unconditional likelihood of the observed series.
- GARCH: fit by `garch()` or `ugarchfit()`, likelihood is conditional on lagged squared observations; the initial observations are typically handled differently across implementations.
- POMP stochastic volatility (e.g., Breto 2014): fit by `mif2()` + `pfilter()`, likelihood is the marginal likelihood of the observed series integrated over the latent volatility path.

### 2. Check whether the likelihoods share a common observation model

For each pair of model classes being compared, ask:
- Do both likelihoods condition on the same information set at each time step?
- Do both use the same functional form for the observation distribution (e.g., both Gaussian, or different families)?
- Are both likelihoods evaluated on the same response variable (e.g., log-returns), or does one model a transformed variable?

If the answers differ across model classes, the log-likelihoods are not on a comparable scale. Flag the comparison as invalid.

Common incompatibility patterns:
- GARCH likelihoods are conditional on all lagged squared observations; ARMA likelihoods condition on lagged residuals from the mean model. These conditioning sets differ, so the numerical values are not comparable.
- POMP stochastic volatility models compute the marginal likelihood by integrating over the latent volatility path via a particle filter. This is a fundamentally different quantity from either the ARMA or GARCH conditional likelihood.
- Some GARCH implementations drop the first few observations for initialization; this further changes the effective sample size and makes numerical comparison invalid.

### 3. Check whether AIC is computed correctly within each class

Even setting aside cross-class comparability, verify within each model class:
- Is AIC computed as -2 * logLik + 2 * k, where k is the number of free parameters?
- For the POMP model specifically: is the maximum log-likelihood used (not the median from a stochastic search)? The median log-likelihood from multiple IF2 runs reflects optimization variability, not the model's best fit. Only the maximum is appropriate for AIC calculation.
- Are the degrees of freedom counted consistently? GARCH(p,q) has p+q+1 parameters; ARMA(p,q) has p+q+2 (including the intercept and variance); POMP models have however many parameters are estimated.

### 4. Assess what valid comparison exists

Identify whether any valid comparison is possible given the models fit:
- **Within-class comparisons** (e.g., GARCH(1,1) vs. GARCH(4,2)) are valid if fit to the same data under the same conditioning.
- **Out-of-sample predictive comparison**: one-step-ahead log-predictive scores computed on a held-out test set can be compared across model classes, because they all forecast the same quantity (the next observation) and the comparison is on equal footing.
- **Cross-validation** approaches similarly put all models on equal footing.

### 5. Characterize the error's impact on conclusions

Determine whether the invalid comparison affects the paper's main conclusion:
- If the paper uses the cross-class comparison only informally ("the POMP model appears competitive with GARCH"), the error is less severe.
- If the paper makes a specific claim ("by AIC, the POMP model is preferred over GARCH"), the conclusion is unsupported and this is a major error.
- If the paper uses the comparison to recommend a model for practical use (forecasting, risk management), the error has direct practical consequences.

### 6. Summarize findings

For each invalid cross-class comparison found:
- Name the models being compared and their model classes.
- Explain specifically why their likelihoods are not comparable (different conditioning, different observation model, etc.).
- Quote the specific claim in the text that relies on the invalid comparison.
- Propose an appropriate replacement (within-class comparison, out-of-sample evaluation, or qualified qualitative statement).

## Limitations

- This skill addresses likelihood comparability, not model misspecification within a class.
- The skill assumes the reviewer can identify the likelihood function being used by each model from the R code and package documentation. For less common packages, this may require consulting documentation.
- Some sophisticated treatments do construct a common observation model for ARMA and GARCH families (e.g., by casting both as special cases of a state-space model and computing a unified Kalman filter likelihood). This skill does not apply when such a unification is explicitly performed.
- This skill does not evaluate whether the POMP model is correctly specified or well-estimated — only whether the cross-class comparison is valid.
