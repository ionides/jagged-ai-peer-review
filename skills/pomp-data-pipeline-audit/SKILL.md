---
name: pomp-data-pipeline-audit
description: Use when reviewing a pomp project that reads raw data, applies transformations (reversal, differencing, log, subsetting, unit conversion), and then passes a derived series to the pomp model, or when a project fits separate pomp models to multiple groups or assets and compares results across them — to detect silent errors where the series passed to pomp differs from the series analyzed in EDA, or where two models being compared are fit to datasets of different lengths, producing consistent-looking output with no runtime error.
---

# pomp Data Pipeline Audit

## Purpose

A recurring silent error in student POMP projects occurs when raw data are transformed in multiple steps before modeling, and the variable passed to the `pomp()` constructor is not the same object displayed in EDA plots or described in the text. Because R does not enforce referential transparency across chunks, a variable used in EDA and a differently-processed variable used in modeling can coexist without any error. The rendered document looks consistent, but the model is fitted to different data than described.

Common manifestations:
- Raw price vector used in EDA plots; log-differenced and reindexed version passed to pomp.
- Row-reversed data frame used for EDA; original (unreversed) order passed to pomp (or vice versa).
- A subset of dates used in EDA; full series or a different subset passed to pomp.
- Demeaned returns computed twice with slightly different means (e.g., once from the raw vector, once from a ts object), with different variables used in EDA vs. modeling.

## When to Activate

Use this skill when:
- A pomp project reads raw data and applies two or more transformation steps (reversal, differencing, log, subsetting, demeaning, unit conversion) before constructing the pomp object.
- EDA plots use variable names that differ from the variable passed to the `data=` argument of `pomp()`.
- The document reports that returns, residuals, or transformed values are "computed as X" in the text but the code shows those values derived from a different intermediate object.
- A project fits separate pomp models to two or more groups or assets (e.g., two stocks, two countries) and compares log-likelihoods or parameter estimates across them — in this case, also verify that all pipelines use the same sample window and sample length.

Do not apply this skill as a replacement for reading the model description carefully — it is a targeted audit of data-variable provenance.

## Procedure

### 1. Identify the raw data object and all derived objects

Read every data-loading and transformation chunk. For each variable assigned from data operations, record:
- Variable name
- What transformation was applied (reversal, differencing, log, subsetting, demeaning)
- Which chunk created it

Build a provenance table: raw file -> intermediate objects -> final objects.

### 2. Identify the variable passed to pomp

Find every `pomp(data=...)` or `pomp(data=data.frame(...))` call. Record:
- The variable name or expression used as the data argument
- Which row(s) of the provenance table this corresponds to

### 3. Identify variables used in EDA

Find every plot, ACF, summary, or model fitting call (including ARMA and GARCH fits) in sections before the POMP model. Record the variable names used.

### 4. Cross-reference EDA variables against the pomp data variable

For each EDA variable identified in Step 3:
- Does it correspond to the same intermediate object as the pomp data variable?
- If not, trace both back to the raw data and identify where they diverge.
- Common divergence points: one variable is reversed and the other is not; one is demeaned using a different mean; one includes more or fewer observations.

**For comparative multi-group or multi-asset studies (additional check):** If the document fits pomp models to two or more groups (e.g., two stocks, two geographic units), build a separate provenance table for each group's pipeline and compare:
- Do all pipelines load from the same date range?
- Do all pipelines apply `tail()`, `head()`, or other subsetting operations? If one does and another does not, the resulting models are fit to different sample sizes and their log-likelihoods and parameter estimates cannot be directly compared.
- Does each pipeline demean using its own group-specific mean (correct) or a pooled mean (potentially incorrect)?

A common silent error pattern: one asset's section adds `TeslaData = tail(TeslaData, 365)` while the other asset's section uses the full series. The rendered document shows numerically plausible output for both, but all cross-asset log-likelihood or parameter comparisons are invalid.

### 5. Verify chronological ordering

For time series data:
- Confirm that the variable passed to pomp runs in ascending chronological order (earliest observation first, matching the time index in the pomp object).
- If row-reversal code is present, verify it is applied consistently to all downstream objects.
- Compute `diff(log(...))` or the equivalent transformation explicitly and check whether the resulting series has the same length, mean, and variance as described in the text.

### 6. Check length consistency

Verify that all objects used in modeling have the same length:
- The data vector passed to pomp
- Any covariate time series
- The time index

Length mismatches usually trigger a runtime error, but off-by-one errors (e.g., from `diff()` reducing length by 1) may not, and can cause silent misalignment between observations and covariates.

### 7. Summarize findings

For each discrepancy found:
- Name the two variables that diverge.
- State the point in the pipeline where they diverge.
- Explain the practical consequence (e.g., "ARMA is fitted to reversed returns; POMP model is fitted to correctly ordered returns; conclusions about relative model fit are not comparable").
- Propose the correction.

## Limitations

- This skill requires carefully reading the data-cleaning code across multiple chunks. For documents with many intermediate objects, the provenance table can become large.
- If the document uses `eval=FALSE` for expensive chunks and loads results from a cached `.RData` file, the variable names in the cached file may not match the names in the `eval=FALSE` code, making provenance difficult to trace.
- The skill does not evaluate whether the transformation itself is statistically appropriate (e.g., whether log returns are the right quantity to model) — only whether the same transformation is applied consistently throughout the document.
