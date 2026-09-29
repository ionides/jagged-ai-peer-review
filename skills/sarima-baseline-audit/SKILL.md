---
name: sarima-baseline-audit
description: Detect configuration mismatches in SARIMA/ARIMA baseline models used alongside POMP analyses — specifically, period misspecification in seasonal grid searches, inconsistencies between grid-search and final model configurations, and invalid direct log-likelihood comparisons between ARIMA-family and POMP models — use when a POMP project includes a SARIMA or ARIMA model as a baseline or benchmark.
---

# SARIMA Baseline Audit

## Purpose

POMP projects frequently fit an ARIMA or SARIMA model as a comparison baseline. Two systematic errors recur in this context that are not covered by the POMP-specific review skills:

1. **Period misspecification in the seasonal grid search**: the `period` argument in `arima()` or `auto.arima()` is set to the wrong value (e.g., `period=12` for weekly data instead of `period=52`), so the AIC-optimal orders selected from the grid do not apply to the final model specification.

2. **Invalid direct log-likelihood comparison between ARIMA and POMP models**: the ARIMA likelihood is evaluated under a Gaussian distribution on possibly differenced data, while the POMP likelihood is evaluated under a different observation model (e.g., negative binomial) on the original data. Direct numerical comparison of these values to conclude one model is "better" than the other is invalid.

## When to Activate

Use this skill when:
- A POMP project includes a SARIMA or ARIMA model fit via `arima()`, `Arima()`, or `auto.arima()`.
- The project presents an AIC grid search over seasonal or non-seasonal orders.
- The project explicitly compares the ARIMA/SARIMA log-likelihood to the POMP model log-likelihood numerically.
- The project concludes about relative model adequacy based on log-likelihood values from the two model families.

Do not use this skill when:
- No ARIMA/SARIMA model is present (pure POMP analysis).
- The ARIMA model is used only for EDA or pre-whitening, not as a benchmark.
- The comparison is made via a proper information criterion that accounts for different observation models (e.g., both models evaluated on the same data with the same measurement model).

## Procedure

### 1. Identify the seasonal period of the data

Read the data description to determine the sampling frequency (e.g., weekly = 52 per year, monthly = 12 per year, daily = 365 or 7 per week). Note the correct seasonal period.

### 2. Check the `period` argument in the grid search

Locate the AIC grid search code (typically a nested loop over `arima()` calls). Verify that the `seasonal = list(order = ..., period = P)` argument uses the correct period `P` for the data frequency.

- If `P` is wrong (e.g., 12 for weekly data), flag the entire grid search as invalid.
- Note whether the final model uses the same or different period — if different, flag the inconsistency explicitly.

### 3. Identify the observation model of each candidate model

For the ARIMA/SARIMA model: identify the error distribution (Gaussian by default in `arima()`), and whether the data is transformed (differenced, log-transformed, etc.).

For the POMP model: identify the measurement model in `dmeasure` (e.g., negative binomial, Poisson).

### 4. Assess whether the log-likelihood comparison is valid

A direct numerical comparison of log-likelihoods is valid only when both models are evaluated on the same untransformed data under the same observation model.

- If the observation models differ, flag the comparison as invalid.
- If one model uses differenced data and the other uses original counts, flag the comparison as invalid.
- Propose the correct fix: evaluate both models under a common observation model and data transformation, or use a proper scoring rule (e.g., CRPS on the original scale) that does not require matching likelihoods.

### 5. Check for directional errors in log-likelihood interpretation

Verify that the text correctly identifies that higher log-likelihood (less negative) corresponds to a better fit. Statements like "lower log-likelihood is a promising sign" or "the POMP model has a much higher log-likelihood, indicating it is worse" should be flagged and corrected.

## Limitations

- This skill covers configuration consistency and comparison validity only; it does not evaluate whether the SARIMA model is otherwise well-specified (residual diagnostics, stationarity testing, etc.).
- Does not apply when the ARIMA model is fitted in a Bayesian framework with an explicit likelihood that matches the POMP observation model.
- Cannot detect period misspecification when the data description is ambiguous about sampling frequency.
