---
name: pomp-profile-design-variable-mismatch
description: Detect cases where a POMP profile likelihood workflow constructs starting guesses via profile_design() into one variable but then iterates the profile IF2 search over a different (global-search) variable, causing the profile_design to be silently ignored and the resulting profile to reflect a re-run of the global search — use when reviewing a POMP project whose profile section contains both a profile_design() call and a foreach loop with iter() or similar iteration.
---

# POMP Profile Design Variable Mismatch Detector

## Purpose

A correct POMP profile likelihood workflow:
1. Calls `profile_design(target_param=grid, lower=..., upper=..., nprof=K)` to produce a starting-guess data frame (e.g., `guesses2`).
2. Iterates the IF2 search over that data frame: `foreach(guess=iter(guesses2, "row"), ...) %dopar% mif2(...)`.
3. Excludes the target parameter from `rw.sd` in the profile mif2 call.

A specific and silent failure occurs when step (2) iterates over the *original global-search guess object* (e.g., `guesses`) instead of the profile-design object (`guesses2`). Because both variables are valid data frames with the same column structure, the code compiles and runs without error. The profile_design result is computed but never used. The `stew()` or `foreach()` output reflects another unconstrained global search, not a profile likelihood. Any CI derived from the plot is invalid.

This error is distinct from `pomp-pseudo-profile-audit`, which covers the case where no `profile_design()` call exists at all. Here, profile_design IS called but its output is silently discarded due to a variable name mismatch in the iteration call.

## When to Activate

Use this skill when:
- A POMP project calls `profile_design(target_param=..., lower=..., upper=..., nprof=K)` and assigns the result to a variable (e.g., `guesses2`).
- The immediately following `foreach` or `stew` block iterates over a *different* variable (e.g., `iter(guesses, "row")` rather than `iter(guesses2, "row")`).
- The project presents the result as a profile likelihood and derives confidence intervals from it.

Do not use this skill when:
- The `foreach` correctly iterates over the profile_design result variable.
- No `profile_design()` call is present (use `pomp-pseudo-profile-audit` instead).
- The variable mismatch is in a non-profile context (e.g., two global searches using similar naming).

## Procedure

### 1. Locate the profile_design() call

Search the Rmd/R source for `profile_design(`. Note the variable name assigned to its output (e.g., `guesses2 <- profile_design(...)` or `profile_design(...) -> guesses2`).

### 2. Locate the profile IF2 search loop

Find the `foreach` or `stew` block that immediately follows the profile_design call and is labeled or described as the profile search. Identify the object being iterated: look for `iter(VAR, "row")` or `foreach(guess = VAR, ...)`.

### 3. Check whether the iterated object matches the profile_design output

- **Correct pattern**: `iter(guesses2, "row")` — iterates over the profile_design output.
- **Error pattern**: `iter(guesses, "row")` — iterates over the original global search guess object; the profile_design result `guesses2` is ignored.

If the error pattern is present, flag it.

### 4. Verify that rw.sd in the profile mif2 call does not fix the target parameter

Even if the correct variable were used, check whether the profiled parameter is excluded from `rw.sd` (set to 0 or omitted). If the rw.sd in the profile block omits the target parameter, the parameter would be free to drift even if guesses2 were iterated correctly. Document this as a compounding error (see also `pomp-profile-rw-sd-drift-error`).

### 5. Assess the impact on the profile plots and CIs

Since the profile IF2 search ran over the global-search guesses rather than the profile grid:
- The resulting parameter values have no systematic coverage of the target parameter's range.
- The profile plot is a scatter of global-search results, not a constrained likelihood surface.
- Chi-squared CI cutoffs applied to this scatter are statistically invalid.
- The profile_design result (`guesses2`) is wasted computation that does not contribute to any reported result.

### 6. Report the finding

For each detected instance, report:
- The code location of the `profile_design()` call and its output variable name.
- The code location of the `foreach`/`stew` block showing which variable is actually iterated.
- The consequence: profile_design output is silently ignored; the profile reflects a re-run of the global search; all reported CIs are invalid.
- The fix: replace `iter(guesses, "row")` with `iter(guesses2, "row")` in the profile search loop, and ensure the target parameter is excluded from `rw.sd` in the profile mif2 call.

## Limitations

- This skill requires side-by-side reading of the profile_design call and the iteration argument in the foreach block. It cannot be detected from the rendered HTML output.
- If the global-search guess object (`guesses`) and the profile_design object (`guesses2`) have different numbers of rows but the same column structure, the rendered profile plot will look different from a typical global-search scatter (because the iteration count differs), but will still not be a valid profile likelihood.
- Does not replace `pomp-pseudo-profile-audit` (no profile_design at all), `pomp-profile-rw-sd-drift-error` (profiled parameter free to drift), `pomp-profile-indexing-error` (wrong result object in pfilter step), or `pomp-profile-guess-stratification-error` (wrong group_by in guess construction). All applicable checks should be run when reviewing a POMP profile likelihood section.
