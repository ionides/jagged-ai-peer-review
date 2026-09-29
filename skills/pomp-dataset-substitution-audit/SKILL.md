---
name: pomp-dataset-substitution-audit
description: Detect silent dataset substitution bugs in POMP (or any time-series) projects where a data-loading block is copy-pasted across sections and the geographic or unit filter is changed, causing one or more models to be fitted on a different dataset than the one described in the paper — use when reviewing a project that fits multiple models sequentially and re-reads or re-filters the data between sections.
---

# POMP Dataset Substitution Audit

## Purpose

Student and practitioner POMP projects frequently fit multiple models in sequence (e.g., ARIMA, then SEIR, then a custom extension). When moving between model sections, authors often copy a data-loading block from an earlier section and modify the filter criteria to experiment with a different location or unit — then forget to revert it. Because the substituted data is structurally similar (same column names, same date range), the model runs without error and produces plausible-looking but entirely wrong estimates. The rendered HTML output gives no indication that the wrong dataset was used.

This skill provides a targeted code-reading procedure to detect this class of silent error.

## When to Activate

Use this skill when:
- A project describes analysis of a specific geographic unit or subject (e.g., "King County, Washington") in its title and introduction.
- The project fits multiple models in separate Rmd/Quarto sections.
- Each model section contains a data-loading or data-filtering code block that selects rows by a geographic or unit identifier (e.g., `filter(Admin2 == "...", Province_State == "...")`).
- The analysis uses a large multi-unit dataset (e.g., a national surveillance file with rows for every county or state) as the source.

Do not use this skill when:
- The project loads data from a single-unit file (e.g., a CSV already filtered to one location) with no inline filtering.
- All model sections share a single data-loading block defined at the top of the document.
- The project explicitly states it is comparing multiple geographic units.

## Procedure

### 1. Identify the Stated Target Unit

Read the title, abstract, and introduction to determine the specific geographic unit, entity, or subject the analysis claims to study.

### 2. Locate Every Data-Loading or Data-Filtering Block

Scan the Rmd/R source for:
- `read.csv`, `read_csv`, `readRDS`, or equivalent calls.
- `filter(...)` calls that select rows by a unit identifier.
- Assignments to `data`, `sea_data`, `df`, or equivalent variable names that appear in model-fitting code.

Note the line number and variable name of each occurrence.

### 3. Check Every Filter for Consistency with the Stated Target

For each data-loading or filtering block, verify that the filter criteria match the stated target unit. Flag any block where:
- The `Admin2`, `Province_State`, `county`, `state`, `country`, or equivalent field does not match the stated target.
- The variable name is the same as one used in a previous correct section (e.g., `sea_data`) but the filter has been changed.

### 4. Trace Which Data Object Is Used in Each Model

For each model-fitting call (`pomp()`, `arima()`, `lm()`, etc.), trace backwards to determine which data object it uses:
- Is the model fitted on the correctly filtered data?
- Has a global variable been overwritten between sections with a different dataset (e.g., `sea_df` reassigned)?
- Does a `rm(list=ls())` or `rm(...)` call between sections cause a later block to silently re-read data?

### 5. Cross-Check Reported Results for Plausibility

If a substitution is suspected, compare the reported parameter estimates or log-likelihoods across models. A sudden large change in scale or in the best-fit transmission rate that is not explained by model complexity may indicate that different models were fitted on different datasets.

### 6. Report the Finding

For each detected substitution, report:
- The code location (line number and chunk name) of the incorrect filter.
- Which model(s) are affected.
- The consequence: all parameter estimates, likelihoods, and conclusions for the affected model(s) apply to the wrong unit and are invalid for the stated target.
- The fix: change the filter criteria to match the stated target, re-run the affected models, and re-evaluate all reported results.

## Limitations

- This skill requires reading source code; it cannot detect substitution bugs from the rendered HTML output alone.
- In projects with very similar datasets across units (e.g., two counties with similar epidemic trajectories), plausibility checks in Step 5 may not reveal the substitution — code inspection is always required.
- Does not cover the case where the entire dataset is wrong (e.g., the wrong CSV file is loaded) rather than the filter within a correct multi-unit file; that case requires checking the filename against the data description.
- Does not replace a full data-provenance audit; it specifically targets the copy-paste filter-change failure mode.
