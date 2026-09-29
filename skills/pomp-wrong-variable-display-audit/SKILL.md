---
name: pomp-wrong-variable-display-audit
description: Detect cases where a POMP multi-model project computes a result for model N but then displays or reports the result variable from a prior model (e.g., prints sir_L_pf instead of sir2_L_pf), causing the rendered output to silently show values from the wrong model — use when reviewing a POMP project that fits multiple models sequentially and copy-pastes display chunks between model sections.
---

# POMP Wrong Variable Display Audit

## Purpose

In multi-model POMP workflows, an author typically fits model 1, computes its likelihood, prints it, then copies the chunk to fit model 2, updating the computation but forgetting to update the display call. The rendered HTML shows the model 1 likelihood under the model 2 section, with no warning or error. Any comparison of initial-guess likelihoods across models is invalid, because at least one reported value does not correspond to the model being described.

This error is distinct from:
- `pomp-artifact-audit`: covers discrepancies between pre-computed RDS artifacts and source code — here the artifact is an inline variable, not a file.
- `pomp-placeholder-result-audit`: covers fabricated values explicitly acknowledged as invented — here the value is genuine but belongs to the wrong model.
- `pomp-simdata-benchmark-error`: covers the wrong data object being passed to pfilter — here the computation is correct but the display references a prior result.

## When to Activate

Use this skill when:
- A POMP project fits two or more models sequentially within the same Rmd/Quarto document.
- Each model section contains a chunk that computes a result (e.g., `sir2_L_pf <- logmeanexp(...)`) and then a separate display call (e.g., `print(sir_L_pf)`).
- The display call uses a variable name that does not match the computation in the same chunk (e.g., the suffix `2` is missing from the print statement).

Do not use this skill when:
- Only a single model is fitted (no cross-model copy-paste risk).
- The display and computation variable names are identical within each chunk.
- The project uses a results table or CSV read-back to display values rather than inline print() calls.

## Procedure

### 1. Identify all result-computation assignments

For each model section, locate every line that assigns a likelihood or parameter result to a named variable:
- `m1_L_pf <- logmeanexp(...)`
- `sir2_L_pf <- ...`
- `seir_L_pf <- ...`

Note the exact variable name used in each assignment.

### 2. Locate the corresponding display calls

In the same chunk or immediately following code, find every `print()`, `cat()`, or inline display call that references a likelihood or parameter result variable.

### 3. Check for name mismatch between assignment and display

For each (assignment, display) pair within a model section:
- **Correct pattern**: The variable name in the display call matches the variable name assigned in step 1 for the same model (e.g., `sir2_L_pf` computed and `print(sir2_L_pf)` displayed).
- **Error pattern**: The display call references a variable from a different model (e.g., `sir2_L_pf` computed but `print(sir_L_pf)` displayed).

Flag any mismatch.

### 4. Assess the impact on reported comparisons

If a mismatch is detected:
- Identify which models are involved: which model's result is displayed and which model it should describe.
- Determine whether the document makes any cross-model likelihood comparison that depends on the mismatched value. If so, the comparison is invalid.
- Check whether the correct value is available (i.e., whether the correctly named variable was actually computed) and note what the true displayed value should be.

### 5. Check for the mismatch in write_csv calls

The same copy-paste error often affects CSV output calls (e.g., `write_csv("sir_lik.csv")` called inside a model-2 chunk that should write `"sir2_lik.csv"`). Verify that file names and variable names are consistent with the model being processed.

### 6. Report the finding

For each detected instance, report:
- The chunk name and the specific line where the mismatch occurs.
- The variable computed vs. the variable displayed.
- Which model's value was actually shown.
- The consequence: the rendered output silently presents results from the wrong model; cross-model comparisons based on the displayed values are invalid.
- The fix: update the display call to reference the correctly named variable for the current model.

## Limitations

- This skill requires side-by-side reading of assignment and display code within each chunk; it cannot be detected from the rendered HTML alone.
- In projects where variable names are identical across models (e.g., the author overwrites `L_pf` for each model in sequence), this error pattern does not apply — but such projects have a different risk (the prior model's result being silently overwritten before display).
- Does not cover the case where the computation itself is wrong (e.g., pfiltering with the wrong data object); that is covered by `pomp-simdata-benchmark-error`.
- The severity depends on whether the mismatched display is used in a formal model comparison. If the value is shown only for informal inspection and not cited in any conclusion, it may be a minor rather than major issue.
