---
name: pomp-loglik-direction-error
description: Detect cases where a POMP (or any statistical) project inverts the log-likelihood direction in model comparisons, claiming that a "lower" or "smallest" log-likelihood indicates the best model fit — use when a project reports log-likelihood values for multiple models and states a conclusion about which model fits best.
---

# POMP Log-Likelihood Direction Error Detector

## Purpose

Log-likelihood values are typically negative for probabilistic models on discrete or continuous count data. Higher log-likelihood (i.e., less negative, closer to zero) indicates better model fit. A recurring student error is to state that the model with the "lowest" or "smallest" log-likelihood is the best fit — inverting the interpretation. This error does not affect which model is identified as best (the ranking is correct) but demonstrates a misunderstanding of the statistical framework and misleads readers. A secondary variant occurs when a positive log-likelihood value is reported without recognition that it signals a numerical error in the model specification (e.g., a Poisson measurement model with near-zero expected counts on data that is mostly zero, caused by an incorrect population parameter).

This error is related to but distinct from the stationarity-test-conclusion-audit skill, which catches inversions of null-hypothesis directions in unit-root tests.

## When to Activate

Use this skill when:
- A project reports log-likelihood values for two or more competing models.
- The project states a conclusion about which model fits best using the word "lowest," "smallest," "minimum," or equivalent to describe the preferred model's log-likelihood.
- A reported log-likelihood value is positive, which is anomalous for standard Poisson, negative binomial, or Gaussian measurement models on typical epidemiological count data.

Do not use this skill when:
- The project correctly identifies the model with the highest (least negative) log-likelihood as the best fit.
- The project uses AIC (which is negatively defined as -2 * loglik + 2k) and correctly identifies the model with the lowest AIC as best — this is a different direction convention.
- The project uses a scoring rule where lower values indicate better fit (e.g., CRPS, RMSE).

## Procedure

### 1. Identify all reported log-likelihood values and model comparisons

Search the text for numerical log-likelihood values reported for multiple models. Note the sign and magnitude of each value.

### 2. Check the stated direction of preference

Identify the sentence that states which model is best based on log-likelihood. Check whether it uses:
- **Correct pattern**: "highest log-likelihood," "largest log-likelihood," "best log-likelihood," or equivalent phrasing implying that more positive (or less negative) is better.
- **Error pattern**: "lowest log-likelihood," "smallest log-likelihood," "minimum log-likelihood" used to identify the best model.

If the error pattern is present, flag it.

### 3. Check for positive log-likelihood anomalies

For each reported log-likelihood value, assess whether it is plausible:
- For a Poisson or negative binomial measurement model on count data: the log-likelihood per observation is bounded above by approximately 0 (for perfect predictions). Over N observations, the total log-likelihood should be negative and on the order of -N to -3N for typical epidemiological data.
- A positive total log-likelihood (e.g., +19821 for 262 weekly observations) is anomalous and signals a model specification error, most commonly:
  - A Poisson measurement model with expected counts near zero caused by a drastically wrong population N, causing `dpois(0, ~0) ≈ 1` and contributing near-zero log-likelihood for the many zero-count weeks.
  - A denominator error in the force of infection that makes all transitions near zero.
  - A numerical overflow or NaN returned by logLik() that is silently treated as a finite number.

Flag any positive log-likelihood as a critical error requiring investigation of the model specification.

### 4. Check for consistency between stated direction and model ranking

Even when the prose direction is wrong, verify that the model actually identified as "best" has the numerically highest log-likelihood. If the model with the highest numerical log-likelihood is correctly identified despite the wrong directional language, note that the substantive conclusion is correct but the explanation is wrong. If an anomalous value (e.g., a positive LL from a broken model) is cited as evidence of the worst fit while the prose direction is inverted, the conclusion may be doubly confused.

### 5. Report the finding

For each detected instance, report:
- The specific sentence with the incorrect directional language.
- The correct interpretation: higher log-likelihood (more positive / less negative) indicates better fit.
- Whether any reported log-likelihood values are anomalously positive and what the likely cause is.
- The consequence: readers unfamiliar with the convention may be misled, and any policy or model selection conclusion that depends on the direction statement is expressed incorrectly.
- The fix: replace "lowest" / "smallest" with "highest" / "largest" when describing log-likelihood preference; investigate and correct any positive log-likelihood values.

## Limitations

- This skill addresses only the prose direction of the comparison, not whether the log-likelihoods are computed correctly or are comparable across models.
- AIC comparisons are a legitimate convention where lower is better — do not flag AIC comparisons as errors.
- In some Bayesian frameworks, negative log-posterior densities are used as loss functions where lower is better; check which framework the project uses before applying this skill.
- Does not replace the `pomp-cross-model-param-reconciliation` skill, which assesses whether the log-likelihood values from different models are actually comparable (same data, same observation model). Both skills should be applied when reviewing multi-model comparisons.
