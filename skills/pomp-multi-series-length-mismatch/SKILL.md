---
name: pomp-multi-series-length-mismatch
description: Detect cases where a POMP project fits models to two or more separate time series of materially different lengths (e.g., due to tail() truncation or different date filtering) and then directly compares the resulting log-likelihoods or parameter estimates as though the models are comparable — use when reviewing a POMP project that claims to compare model fit across multiple distinct series (e.g., two stocks, two cities) but loads or preprocesses each series independently.
---

# POMP Multi-Series Length Mismatch Detector

## Purpose

When a project fits a POMP model to two or more distinct time series (e.g., two stocks, two geographic regions), the log-likelihood of each model is a function of that series' length, distributional characteristics, and the parameter values. Directly comparing log-likelihoods across series of different lengths is invalid: a shorter series will typically produce a smaller-magnitude (or even positive) log-likelihood even for a well-fitted model, while a longer series produces a more negative value. Any conclusion about relative model quality, volatility, or fit that rests on cross-series log-likelihood comparison is statistically meaningless.

This error commonly arises from:
- Applying `tail(data, N)` or `head(data, N)` to one series but not another before constructing the pomp object.
- Filtering one series to a sub-period for "convenience" or to avoid a market regime change, then forgetting to apply the same filter to the other series.
- Copy-pasting a model-fitting block from a reference (e.g., a course example with a short dataset) without updating the data length.

## When to Activate

Use this skill when:
- A project fits POMP (or ARIMA/GARCH) models to two or more separate named time series (e.g., two stock tickers, two epidemiological regions).
- Each series has a separate data-loading or data-transformation block.
- The project makes a cross-series comparison of log-likelihoods, AIC, parameter estimates, or model-implied quantities (e.g., volatility, transmission rate).

Do not use this skill when:
- Only a single series is analyzed.
- The project explicitly uses a common observation window for all series (same start date, same end date, same frequency) and applies the same data transformation to each.
- The project compares nested models on the same series (within-series comparison), not across different series.

## Procedure

### 1. Identify all data-loading blocks

Scan the Rmd/R source for all `read.csv`, `read_csv`, `readRDS`, `tail()`, `head()`, `filter()`, or `subset()` calls that define the input dataset for each named series. Note the number of rows (or the implied length after filtering) for each.

### 2. Compute or estimate the effective series length for each model

For each series:
- Check whether `tail(data, N)` or `head(data, N)` is applied, and if so, what N is.
- Check whether a date filter (e.g., `filter(date >= "2020-01-01")`) reduces the series.
- Compute or estimate the final number of observations passed to the pomp object.

If any two series have materially different lengths (more than ~10% difference), flag for further analysis.

### 3. Check whether cross-series log-likelihood comparisons are made

Search the text and code for:
- Explicit statements comparing log-likelihoods across the two series (e.g., "Series A has log-likelihood X while Series B has Y, so A fits better").
- AIC comparisons that use log-likelihoods from different series.
- Comparative conclusions about parameter estimates that assume equivalent information content.

### 4. Assess the sign and magnitude of reported log-likelihoods

For a Gaussian observation model on a mean-zero series with variance σ² and length N, the expected log-likelihood at reasonable parameters is approximately:
- −(N/2) × log(2π) − (N/2) × log(σ²) − N/2

For daily financial log-returns (σ² ≈ 0.001–0.002), this is roughly −1.5N to −2.0N. A positive log-likelihood or one far from this range suggests a dataset length mismatch (shorter series, or evaluation on simulated data).

If one series has a positive or anomalously small-magnitude log-likelihood compared to what the stated series length would predict, confirm by checking the actual data length in the code.

### 5. Assess the impact on conclusions

For each cross-series comparison that is based on mismatched series lengths:
- The relative log-likelihood difference is dominated by the length difference, not model quality.
- Any conclusion about which series is "better fit" or "more volatile" based on log-likelihood is invalid.
- Parameter estimates remain internally valid for each series, but cannot be compared directly if the inference used different amounts of data.

### 6. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) where each series is loaded or truncated.
- The effective length of each series.
- The cross-series comparison that is invalidated.
- The consequence: log-likelihood values are not comparable across series of different lengths; all stated comparative conclusions are statistically invalid.
- The fix: apply identical date filtering and data preprocessing to both series before fitting any model, so that both models are trained on the same observation window and have the same number of observations.

## Limitations

- This skill requires reading the data-loading code; it cannot be detected from the rendered output alone.
- If the series have different lengths but the project does not make any cross-series log-likelihood comparison (e.g., it only compares within-series nested models), the length mismatch may be acceptable and should not be flagged as a major error.
- In some domains (e.g., comparing two epidemics with naturally different durations), unequal series lengths are scientifically motivated. In that case, the project should use per-observation log-likelihoods or AIC-normalized metrics. Flag if this normalization is not done.
- Does not replace the `pomp-simdata-benchmark-error` skill, which covers the case where a simulated dataset is substituted for real data. Both should be applied when reviewing multi-series POMP projects.
- Does not replace the `pomp-dataset-substitution-audit` skill, which covers geographic filter copy-paste errors within a single multi-unit dataset.
