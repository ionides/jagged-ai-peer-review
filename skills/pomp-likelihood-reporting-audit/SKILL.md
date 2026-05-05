---
name: pomp-likelihood-reporting-audit
description: Use when reviewing a pomp project that saves likelihood results to CSV or RDS files and then prints or summarizes them in the narrative, to detect silent object-naming errors where the wrong likelihood object is printed — producing a narrative that contradicts the archived results without triggering any runtime error.
---

# pomp Likelihood Reporting Audit

## Purpose

In student and research POMP projects it is common to save likelihood estimates from pfilter or mif2 to external files (CSV, RDS) and later print or reference those objects in the narrative. A recurring silent error is printing the wrong R object — for example, printing `sir_L_pf` in the Model 3 summary chunk when `sir2_L_pf` was intended. Because both objects exist and are valid, R runs without error. The rendered HTML or PDF presents a number that looks plausible, but it belongs to a different model. When the authors then compare the printed values to draw conclusions about relative model fit, those conclusions are wrong.

This error is invisible to standard code review unless the reviewer independently checks the archived CSV/RDS values against the narrative claims.

## When to Activate

Use this skill when:
- A pomp project fits two or more competing model structures (e.g., SIR vs. SEIR vs. SIR with covariates).
- Each model produces a separately named likelihood object or CSV file (e.g., `sir_L_pf`, `seir_L_pf`, `sir2_L_pf` or `sir_lik.csv`, `seir_lik.csv`, `sir2_lik.csv`).
- The narrative contains printed likelihood values or model comparisons derived from those objects.
- The authors draw a conclusion about which model fits best based on the printed values.

Do not use this skill as a substitute for the full reproducibility audit in `guided-pomp-review` — it is a targeted check for a specific class of object-naming error in likelihood reporting.

## Procedure

### 1. Enumerate all model likelihood objects and their archived counterparts

Scan the Rmd/Qmd source for:
- All `pfilter` and `logmeanexp` calls that produce likelihood estimates, noting the variable names used (e.g., `sir_L_pf`, `seir_L_pf`).
- All `write_csv` or `saveRDS` calls that archive these estimates, noting the filename and the variable written.
- All `print`, `knitr::kable`, or inline R expressions that display likelihood values in the narrative.

Build a correspondence table: Model -> likelihood variable -> archived filename -> print/display call.

### 2. Read archived CSV/RDS files

Open every archived likelihood file (CSV, RDS, or similar). For each file, record:
- The model it was intended to represent (based on filename conventions and surrounding code context).
- The best (highest) log-likelihood value present.
- Any secondary columns such as `loglik.se`.

### 3. Cross-reference printed values against archives

For each `print` or display call identified in Step 1:
- Identify which variable is being printed.
- Look up that variable's value in the archived file for the same model.
- If the printed variable name does not match the model being discussed at that point in the narrative, flag as a potential object-naming error.

Common error pattern: a chunk labeled "Model 3 likelihood" contains `print(model1_L_pf)` rather than `print(model3_L_pf)`. The printed value is the Model 1 likelihood, but the surrounding text treats it as Model 3's.

### 4. Verify model ranking against archived values

After identifying the best log-likelihood from each model's archived file, rank the models by log-likelihood and compare this ranking to the authors' stated conclusion. If the ranking implied by the archives contradicts the ranking stated in the text:
- Identify which print/display call produced the incorrect value.
- Quote the offending line (e.g., `print(sir_L_pf)` in the Model 3 chunk).
- Compute the correct ranking from the archived files.
- Assess whether the incorrect ranking materially changes the paper's conclusions.

### 5. Check for overwrite hazards

Many student projects read a CSV, append new results, and write back to the same file within the same document. Verify:
- The read/append/write pattern is consistent and the final CSV reflects all runs.
- The variable used for printing was assigned after the pfilter run, not carried over from a previous chunk via a stale value.
- If `run_level` switches are present, confirm the archived CSV corresponds to the active run_level.

### 6. Summarize findings

For each error found:
- Quote the offending print or display call with its chunk label and line number.
- State the value actually printed vs. the correct value from the archive.
- Explain which model comparison or conclusion is affected.
- Propose the corrected print call.

## Limitations

- This skill requires access to archived output files (CSV, RDS). If the project does not save intermediate results to files, the audit must rely on the rendered HTML output instead, which requires reading the HTML to extract printed values.
- The skill detects object-naming errors in reporting, not errors in the likelihood computation itself (e.g., incorrect Csnippets or IF2 hyperparameters — see `pomp-csnippet-audit` and `pomp-if2-hyperparameter-audit` for those).
- In projects where all likelihood estimates are printed inline without archiving to files, this skill's cross-reference step cannot be applied. In that case, focus only on Step 1 (naming consistency) and Step 4 (whether any ranking claims are internally consistent with other printed values in the document).
- The skill assumes that the archived CSV files were generated by the code under review and have not been manually edited. If there is reason to suspect manual editing of output files, the audit must treat the CSV values as unverified.
