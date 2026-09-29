---
name: pomp-arima-double-invalid-comparison
description: Detect cases where a POMP project compares its log-likelihood to an ARIMA/SARIMA log-likelihood that was fitted on a materially shorter subset of the same dataset (different date filter), making the comparison doubly invalid due to both a dataset-length mismatch and an observation-model mismatch — use when a POMP project fits ARIMA on one date range and POMP on a wider range, then directly compares the resulting log-likelihoods.
---

# POMP vs. ARIMA Double-Invalid Comparison Detector

## Purpose

When a POMP project includes an ARIMA baseline and compares log-likelihoods, two distinct invalidity sources commonly coexist and compound each other:

1. **Observation-model mismatch**: the ARIMA uses a Gaussian likelihood on (possibly differenced) data; the POMP uses a different measurement model (e.g., negative binomial, truncated normal). Log-likelihoods from different observation models are not comparable. (Covered by `sarima-baseline-audit`.)

2. **Dataset-length mismatch within the same source dataset**: the ARIMA is fitted on a date-filtered subset of the data (e.g., `<= 2022-02-28`, yielding 90 rows), while the POMP is fitted on the full range (e.g., through `2022-03-31`, yielding 121 rows). The longer dataset produces a more negative log-likelihood purely because it sums over more observations, independent of model quality.

This second error is distinct from the multi-series length mismatch (`pomp-multi-series-length-mismatch`), which targets different named time series (e.g., two cities, two stocks). The current error arises from inconsistent date-filtering within a single series when switching between model types. It is also not detected by `sarima-baseline-audit` alone, which does not check for dataset-length consistency.

The compound effect: even if both errors individually produced manageable distortions, together they make the stated log-likelihood comparison entirely meaningless. The ARIMA's "better" log-likelihood is an artifact of (a) fewer observations and (b) a different model class, not superior fit to the data.

## When to Activate

Use this skill when:
- A POMP project fits an ARIMA or SARIMA model and a POMP mechanistic model to the **same underlying dataset** but with different date filters or row selections.
- The project presents a table or statement directly comparing the two log-likelihoods numerically and concludes that one model is better than the other.
- The ARIMA section and the POMP section load data separately (e.g., one filters to February, the other uses a pre-saved CSV covering March).

Do not use this skill when:
- Both models are fitted to the same date range and the same row count. In that case, only the observation-model mismatch (covered by `sarima-baseline-audit`) applies.
- The project does not make a direct numerical log-likelihood comparison (e.g., ARIMA is used only for EDA or spectrum analysis).
- The series have genuinely different durations for scientific reasons (e.g., the ARIMA needs a stationary pre-peak window while POMP covers the full epidemic). In that case, per-observation log-likelihood normalization should be used; flag if it is not.

## Procedure

### 1. Identify the ARIMA dataset

Locate the ARIMA fitting code. Find all date filters, `head()`, `tail()`, or row-selection calls applied to the raw data before `arima()` or `Arima()` is called. Record the number of observations (rows) used.

### 2. Identify the POMP dataset

Locate the POMP `pomp()` or `bake()`/`readRDS()` block. Identify the data source (inline filtering, or a pre-saved CSV). Record the number of rows or time steps in the pomp object.

### 3. Compare dataset lengths

If the two counts differ by more than a token amount (more than ~5% of the longer series), flag a dataset-length mismatch.

### 4. Identify the observation models

For ARIMA: Gaussian on the (possibly differenced) data.
For POMP: read the `dmeasure` Csnippet to identify the distributional family and scale.

If the families differ (almost always), flag an observation-model mismatch.

### 5. Assess the direction and magnitude of bias

For the dataset-length effect: the model fit to more observations will have a more negative log-likelihood, all else equal. Compute the approximate magnitude: if the per-observation log-likelihood is approximately `LL_per_obs`, then an extra `delta_n` observations shifts the total by roughly `delta_n * LL_per_obs`. If this shift is larger than the observed gap, the length difference alone explains the entire reported difference.

For the observation-model effect: Gaussian likelihoods on continuous data are not bounded below in the same way as discrete likelihoods on count data. Direct comparison is invalid regardless of magnitude.

### 6. Identify the stated conclusion and its invalidity

Quote the exact sentence(s) in the paper that interpret the log-likelihood comparison. Confirm that the conclusion (e.g., "ARIMA outperforms SEIR") rests solely on this invalid comparison.

### 7. Propose the fix

- Apply identical date filtering to both models (same start and end date, same row count).
- Either (a) use a common observation model for both models, or (b) replace the log-likelihood comparison with a proper scoring rule (CRPS, RMSE on the original scale) that does not require matching observation models.
- Alternatively, report the comparison as qualitative only, acknowledging that the two log-likelihoods are not directly comparable.

## Limitations

- Requires reading both the ARIMA and POMP data-loading code; the discrepancy is invisible from the rendered output.
- If the project uses a pre-saved CSV for the POMP data, the length must be inferred from the file's row count rather than the code filter.
- This skill does not evaluate the quality of either model independently — it only targets the invalidity of the cross-model comparison.
- Does not replace `sarima-baseline-audit` (observation-model mismatch) or `pomp-multi-series-length-mismatch` (cross-series length mismatch); all three should be applied when an ARIMA-vs-POMP comparison is present.
