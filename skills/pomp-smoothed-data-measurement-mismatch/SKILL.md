---
name: pomp-smoothed-data-measurement-mismatch
description: Detect cases where a POMP project applies a moving-average or rolling-mean transformation to raw count data and then feeds the smoothed (non-integer, autocorrelated) values directly to a discrete measurement model (binomial or Poisson), producing a systematic mismatch between the data type and the distributional family of the measurement model — use when reviewing a POMP project whose data preprocessing includes rollmean(), filter(), or similar smoothing before the pomp() call.
---

# POMP Smoothed-Data / Measurement-Model Mismatch Detector

## Purpose

POMP projects analyzing infectious disease count data frequently preprocess raw case counts with a moving-average smoother (e.g., `rollmean(dat$cases, 7)`) before passing the result as the `data` argument to `pomp()`. The smoothed series has two properties that are incompatible with standard discrete measurement models:

1. **Non-integer values**: A 7-day rolling mean of integer case counts produces fractional values. Passing fractional values to `dbinom(x, size, prob)` or `dpois(x, lambda)` in `dmeasure` may return zero or NA because these functions require integer `x`, causing the particle filter to return `-Inf` log-likelihoods at every observation time.

2. **Autocorrelation**: The rolling mean introduces serial correlation between consecutive observations. Even if the measurement model is evaluated at rounded integer values, the independence assumption underlying the factored likelihood `prod(p(y_t | x_t))` is violated, producing likelihood estimates that do not correspond to any valid statistical model.

This failure is distinct from:
- `pomp-inference-misuse`: that skill covers stochastic simulation-based cost functions and dmeas/rmeas distributional family inconsistencies.
- `pomp-accumvar-semantic-audit`: that skill covers accumulating the wrong compartment flow.
- `pomp-dmeas-rmeas-scale-inconsistency`: that skill covers rescaling differences between dmeas and rmeas.

Here the issue is at the data level: the data transformation and the measurement model are incompatible.

## When to Activate

Use this skill when:
- A POMP project calls `rollmean()`, `filter()`, `smooth()`, `zoo::rollmean()`, or similar before the `pomp()` call.
- The smoothed result is assigned as the `data` argument (or as a column in the data frame passed to `pomp()`).
- The `dmeasure` Csnippet uses `dbinom`, `dpois`, or `dnbinom` — distributions that require integer-valued observations.
- The project reports degenerate particle filter likelihoods (`-Inf`) that are not explained by other model defects.

Do not use this skill when:
- The project uses raw (unsmoothed) count data as the observation series.
- The smoothed data is used only for visualization or exploratory analysis, not as the `data` argument to `pomp()`.
- A Gaussian measurement model is used, which can accommodate continuous observations (though autocorrelation still violates independence).
- The project explicitly acknowledges the smoothing-induced mismatch and adopts a measurement model appropriate for continuous autocorrelated data.

## Procedure

### 1. Identify the data preprocessing pipeline

Read the data preparation code that precedes the `pomp()` call. Search for:
- `rollmean(`, `filter(`, `zoo::rollmean(`, `TTR::SMA(`, `stats::filter(`
- Any other smoothing or averaging operation applied to the case count column.

Note the window width (e.g., 7 for a 7-day mean) and whether the result replaces or supplements the raw counts.

### 2. Identify which data column is passed to pomp()

Locate the `pomp()` call (or the `data.frame` / `tibble` that feeds into it). Determine which column is the `reports` (or equivalent observation) variable:
- Is it the raw count column, or the smoothed column?
- Is the smoothed column given the same name as the original (e.g., `dat$reports <- rollmean(...)`)? This is the most dangerous pattern because no renaming signals the substitution.

### 3. Check the measurement model for integer requirements

Read the `dmeasure` Csnippet. Identify the distribution used:
- `dbinom(x, size, prob)`: requires `x` to be a non-negative integer ≤ `size`.
- `dpois(x, lambda)`: requires `x` to be a non-negative integer.
- `dnbinom(x, size, mu)` or `dnbinom_mu`: requires `x` to be a non-negative integer.

If any of these is used and the observations are smoothed, flag the mismatch.

### 4. Check whether degenerate likelihoods are reported

Scan the Appendix or results section for:
- Reports of `-Inf` log-likelihoods from `pfilter()`.
- Convergence traces that remain flat at the minimum possible value.
- Author comments noting that the particle filter "fails" or produces unreasonable results.

If degenerate likelihoods are reported without a clear explanation, the smoothed-data mismatch is a primary candidate cause.

### 5. Assess the autocorrelation impact on the likelihood

Even if the fractional-value problem is resolved (e.g., by rounding the rolling mean), note that the factored likelihood `prod(p(y_t | x_t))` is only valid when observations are conditionally independent given the latent state. A rolling mean of window width W introduces correlation of length W-1 between consecutive observations. This means the POMP likelihood underestimates the true uncertainty, and standard errors derived from it are too small. Flag this as a theoretical concern even if the degenerate-likelihood problem is resolved by other means.

### 6. Propose the fix

Provide concrete remediation options:
- **Preferred fix**: Use raw daily case counts as the observation variable. The POMP measurement model is designed to handle the noise in raw counts via the distributional family and dispersion parameter.
- **Alternative fix**: If smoothing is desired for visual clarity, keep the raw counts as the observation variable for model fitting, and display a smoothed version of the fitted trajectories in figures.
- **Gaussian alternative**: If the project insists on using smoothed observations, switch to a Gaussian measurement model (`dmeasure` using `dnorm(reports, mu=rho*H, sd=sigma, give_log)`) that can accommodate continuous values, and discuss the autocorrelation limitation.

### 7. Report the finding

For each detected instance:
- Cite the code line where the rolling mean is applied and the column name passed to `pomp()`.
- State the measurement distribution used in `dmeasure` and why it requires integer inputs.
- Note whether degenerate likelihoods were observed and whether this mismatch is the likely cause.
- Provide the fix (raw data or Gaussian measurement model).

## Limitations

- Some implementations of `dnbinom` in C accept non-integer `x` via interpolation (the underlying C code uses the gamma function). In that case, the mismatch does not produce `-Inf` but the likelihood values are still not the intended negative-binomial probabilities for integer counts. This subtlety requires inspecting the actual C behavior rather than the R-level documentation.
- The autocorrelation concern applies broadly; this skill does not quantify its impact on specific parameter estimates, only flags its presence.
- Does not replace the full POMP measurement model specification check (SKILL_pomp.md §12); this skill focuses specifically on the data-transformation/distributional-family incompatibility.
- Cannot detect cases where the smoothing is applied in a separate script before the Rmd is run and the smoothed data is read from a CSV; in that case, only the data file inspection reveals the transformation.
