---
name: pomp-artifact-audit
description: Programmatically load and inspect pre-computed POMP result objects (RDS, RDA files) to detect silent parameter name mismatches, unidentifiable parameters, and inconsistencies between saved artifacts and the source code narrative — use when a POMP project loads pre-computed results rather than rerunning inference inline.
---

# POMP Artifact Audit

## Purpose

When a POMP project stores its computational results in a pre-computed file (`.rds`, `.rda`, `.RData`) and loads it at render time rather than running inference inline, the source code and the saved artifact can diverge silently. This skill provides a systematic procedure for cross-checking the artifact against the narrative to catch naming mismatches, unidentifiable parameters, and discrepancies between the stated model and the results that were actually computed.

## When to Activate

Use this skill when:
- An Rmd/Quarto project loads results via `readRDS()`, `load()`, or equivalent at the top of the document rather than computing them inline.
- The project reports parameter estimates, log-likelihoods, or confidence intervals derived from a saved object.
- The POMP parameter names in the Csnippet code need to be verified against the column names in the result object.

Do not use this skill when:
- The analysis is run fully inline (no pre-saved result objects).
- The result file is not accessible for inspection (e.g., not included in the project folder).
- The project is not a POMP inference analysis (e.g., a pure simulation study with no parameter estimation).

## Procedure

### 1. Identify Pre-Computed Artifacts

Scan the Rmd/Quarto source for `readRDS`, `load`, `readRDS`, or similar calls. Note the file names and the variable names they are assigned to.

### 2. Load and Inspect the Artifact

Using R (via a Bash call), load the artifact and extract:
- Column names (for data frames / matrices)
- Dimensions
- Range and distribution of each parameter column
- Maximum log-likelihood value
- Any columns that are in the artifact but not in the source code parameter list, or vice versa

```r
x <- readRDS("path/to/result.rds")
cat("Colnames:", colnames(x), "\n")
cat("Dim:", dim(x), "\n")
cat("Max loglik:", max(x$loglik, na.rm=TRUE), "\n")
print(summary(x))
```

### 3. Cross-Check Parameter Names

Compare the column names in the artifact against:
- The `paramnames` argument in the `pomp()` call
- The variable names in the Csnippets (`statenames`, transition rate names)
- Any column renames applied in the analysis code (e.g., `colnames(result)[5] <- "mu_PR"`)

Flag any column that exists in the artifact under a different name than what the source code Csnippet defines. Document whether the rename is explained in the text or silently applied.

### 4. Check for Unidentifiable Parameters

For each parameter column, examine the range of values across all search runs relative to the variation in log-likelihood:
- If a parameter varies by orders of magnitude while log-likelihood is nearly constant, the parameter is likely unidentifiable.
- Compare the spread of parameter values at loglik > (max_loglik - 1.92) vs. the full range — a very wide spread at the CI cutoff indicates non-identification.

### 5. Verify Best-Fit Values Against the Text

Confirm that the parameter values reported as the MLE in the text match those from `result[which.max(result$loglik), ]` in the artifact. Discrepancies indicate either a display error or that a different result object was used than the one provided.

### 6. Check for Model-Code Discrepancies

Using the identified best-fit parameters, verify that the mathematical equations in the text are consistent with what the Csnippets implement. Pay particular attention to:
- Which state variable appears in the transition rate (e.g., `N` vs. `R` in the force of infection analog)
- Whether the measurement model in the Csnippet matches the distributional specification in the text

## Limitations

- Requires R to be available in the review environment to execute inspection code.
- Cannot detect discrepancies in models where the artifact was generated from code not present in the Rmd (e.g., a separate script run on a cluster).
- Does not replace a full reproducibility audit — it checks consistency between the artifact and the Rmd, not whether the artifact itself is correct.
- For very large result objects, loading them may be slow; use `str()` or `head()` in that case.
