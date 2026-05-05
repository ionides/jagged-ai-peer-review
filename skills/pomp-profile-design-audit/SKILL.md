---
name: pomp-profile-design-audit
description: Use when reviewing a pomp project that calls profile_design() and passes the result to a foreach-mif2 loop, to detect the silent error where the loop iterates over the global search design instead of the profile design object — producing results that appear to be a profile likelihood but are actually a repeated global search.
---

# pomp Profile Design Audit

## Purpose

A recurring silent error in student POMP projects is constructing a `profile_design(...)` object for a profile likelihood search, then inadvertently iterating the `foreach`-`mif2` loop over the original global search design (e.g., `guesses`) instead of the profile design (e.g., `guesses2`). Because both objects are data frames of parameter grids and both produce valid IF2 output, R runs without error. The rendered document shows profile likelihood plots with a Wilks confidence interval cutoff, but the underlying results are a duplicate of the global search. Confidence intervals derived from this output are invalid.

This error is easy to introduce when adapting global-search template code for profiling: the only required change is swapping the variable name inside `iter(...)`, and this single-character edit is often omitted.

## When to Activate

Use this skill when:
- A pomp project calls `profile_design(param=seq(...), lower=..., upper=..., nprof=...)` and assigns the result to a variable (e.g., `guesses2`, `prof_design`).
- The project has a subsequent `foreach(guess=iter(..., "row"), ...) %dopar% { mif2(...) }` block intended to run the profile search.
- The project displays profile likelihood plots with a Wilks-threshold confidence interval.

Do not use this skill as a substitute for the full IF2 hyperparameter audit (`pomp-if2-hyperparameter-audit`) or the general convergence checks in `guided-pomp-review`. It is a targeted check for a single class of design-object substitution error.

## Procedure

### 1. Locate the profile_design call and record the assigned variable name

Find every `profile_design(...)` call in the document. For each, record:
- The variable name on the left-hand side of the assignment (e.g., `guesses2 <- profile_design(...)`).
- The parameter being profiled (the argument with a fixed sequence, e.g., `eta=seq(0.01, 0.1, length=40)`).
- The lower and upper bounds used for the nuisance parameters.

### 2. Find the foreach loop intended to use the profile design

Locate the `foreach` block that is structurally associated with the profile search (typically adjacent to or immediately following a `stew(file="results2.rda", {...})` wrapper). Record:
- The variable name inside `iter(..., "row")` — this is the object actually iterated over.
- The `.export` list, if parallel execution is used.

### 3. Check that the iterated variable matches the profile design object

Compare the variable name from Step 1 to the variable name from Step 2:
- If they match (e.g., both are `guesses2`): no error. Proceed to Step 4.
- If they differ (e.g., `iter(guesses, "row")` when the profile design is `guesses2`): flag as a critical error. The profile search is iterating over the wrong object. All downstream profile plots and confidence intervals are invalid.

### 4. Check that the profiled parameter is handled correctly in rw.sd

Examine the `rw.sd(...)` call inside the profile `mif2`:
- For a strict profile likelihood: the profiled parameter should not appear in `rw.sd` (it is fixed at each profile point and should not be perturbed). If it appears with non-negligible rw.sd, the profile is blurred — values of the profiled parameter will drift away from their design values during IF2.
- For a relaxed profile (acceptable in some contexts): the profiled parameter appears in `rw.sd` with a small value, and the optimizer is allowed to refine near each profile point. This should be explicitly acknowledged.

### 5. Verify the profiled parameter variable is exported to parallel workers

If the `foreach` loop uses `%dopar%`, check the `.export` argument:
- The profile design variable (e.g., `guesses2`) must appear in `.export` if it is not defined inside the loop body.
- The profiled parameter value at each design point is carried inside `guess` (the loop variable), so it does not need separate export — but verify this assumption by confirming `guess` is passed to `mif2(params=c(unlist(guess)), ...)`.

### 6. Verify profile plots display the profiled parameter on the x-axis

Examine the ggplot calls that produce profile likelihood figures:
- Confirm the x-axis maps to the profiled parameter (e.g., `aes(x=eta, y=loglik)`), not a different parameter.
- Confirm the confidence interval cutoff uses the correct Wilks formula: `maxloglik - 0.5 * qchisq(0.95, df=1)`.
- Confirm `maxloglik` is computed from the profile results object, not from the global search results.

### 7. Summarize findings

For each error found:
- Quote the offending `iter(...)` call with its variable name.
- Name the correct profile design variable that should have been used.
- Identify which profile plots and confidence intervals are affected.
- State the practical consequence: the reported CIs are intervals from a scatter of global-search points, not from an optimized profile, and are therefore wider, noisier, and potentially covering the wrong region of parameter space.
- Propose the corrected `iter(...)` call.

## Limitations

- This skill detects design-object substitution errors only. It does not evaluate whether the profile design itself is well-constructed (adequate number of profile points, appropriate range, correct parameter fixed).
- If the project uses a single design object for both global search and profiling (by filtering or subsetting it), the mismatch will not appear as a variable-name discrepancy. In that case, verify the filtering logic instead.
- This skill does not assess whether the Wilks approximation is appropriate for the model (it requires a well-identified, approximately quadratic likelihood surface near the MLE).
- Projects that cache profile results to `.rda` files and reload them may use a variable name that differs from the original profile design — verify by tracing from the stew block to the plot chunk.
