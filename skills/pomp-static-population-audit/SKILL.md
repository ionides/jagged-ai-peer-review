---
name: pomp-static-population-audit
description: Detect cases where a POMP model of a long historical time series fixes total population N to a single modern census value rather than using a time-varying covariate, causing systematic bias in all rate parameters proportional to the ratio of true historical population to the fixed value — use when reviewing a POMP infectious-disease model fitted to multi-decade data.
---

# POMP Static Population Audit

## Purpose

POMP compartmental models of infectious disease define force-of-infection terms of the form `Beta * I / N`, where `N` is the total population. For models fitted to short time series (a few years), fixing `N` to a single observed value introduces negligible bias. For models spanning multiple decades, however, the true population can change by a factor of two or more. Using a fixed modern census value for `N` across a 50–70 year historical series systematically inflates or deflates the effective per-capita contact rate, distorting `Beta` and any other rate that is normalized by population size. The effect is not self-correcting: the optimizer will absorb the population error into `Beta` and potentially other parameters rather than exposing it as a model misfit.

This error is distinct from dataset substitution (wrong unit), accumulator mismatch (wrong flow), or measurement model misspecification. It is a covariate-design failure that affects the process model.

## When to Activate

Use this skill when:
- A POMP infectious-disease model is fitted to annual or similarly coarse time-series data spanning 20 or more years.
- The model includes a population size parameter `N` that appears in the force of infection (e.g., `Beta * I / N`).
- The value of `N` is fixed as a scalar constant (e.g., assigned directly in `params` or hardcoded in the Csnippet) rather than provided as a covariate varying with time.

Do not use this skill when:
- The time series spans fewer than 10 years and the population change is negligible (< 10%).
- The model already uses a time-varying population covariate loaded from a demographic table.
- The population is treated as a model parameter to be estimated from the data and the authors discuss whether the estimated value corresponds to a plausible historical average.

## Procedure

### 1. Identify the population value used in the model

Search the Rmd/R source for the assignment of `N` in the `params` vector or in a fixed-params declaration. Note the numerical value.

### 2. Identify the time span of the data

Read the data description to determine the start year, end year, and total span of the time series. Note the sampling frequency (annual, monthly, weekly).

### 3. Compare N to historical population data

Look up (or approximate from context) the actual population of the modeled unit at the start of the data series. Compare it to the value used in the model:
- If the ratio (model N) / (actual historical N) exceeds 1.5 or is below 0.75 for any substantial portion of the series, flag the issue.
- Compute the approximate bias factor: `Beta_apparent / Beta_true ≈ N_model / N_actual`. For a two-fold population error, `Beta` is biased by a factor of 2.

### 4. Assess whether the authors acknowledge the limitation

Check the paper for any discussion of the fixed-N assumption. If the authors note it as a limitation but do not quantify the potential bias, flag it as a minor issue. If the authors do not mention it at all and the bias factor exceeds 1.5, flag it as a major issue.

### 5. Check whether other rate parameters absorb the bias

Examine the estimated values of `Beta` and related rate parameters. If `Beta` is implausibly large or small relative to literature values for the disease, this may indicate population error rather than a true biological transmission rate. Note whether the authors compare parameter estimates to independent biological evidence (as required by POMP checklist §11).

### 6. Propose the fix

Recommend that the authors replace the fixed scalar `N` with a time-varying population covariate loaded from demographic data (e.g., census estimates or interpolated series). In pomp, this is done via the `covar` argument with a `covariate_table()` specifying population by year. If full demographic data is unavailable, a linear interpolation between census years is an acceptable approximation, and its sensitivity should be assessed.

## Limitations

- This skill requires external knowledge of the historical population of the modeled unit. If the reviewer does not have access to approximate census figures, the magnitude of the bias cannot be assessed precisely.
- For models where `N` appears only in the initial condition (e.g., `S = round(N * S_0)`) but not in the force-of-infection denominator, the bias mechanism differs and this skill's Step 3 calibration does not apply directly.
- If `N` is estimated as a free parameter via likelihood maximization (not fixed), this is a different issue: the optimizer may estimate an effective N that compensates for the missing time-variation. This is still a model misspecification but the direction of bias is less predictable.
- Does not replace the full POMP checklist §11 (Corroboration with scientific knowledge), which covers a broader range of implausible parameter estimates.
