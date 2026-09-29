---
name: pomp-profile-indexing-error
description: Detect the anti-pattern of evaluating a POMP profile likelihood by extracting parameters from the wrong result object (e.g., the box-search object instead of the profile-search object), causing the profile likelihood plot to reflect a different computation than intended — use when reviewing a POMP project that constructs a profile likelihood after a global box search.
---

# POMP Profile Likelihood Indexing Error Detector

## Purpose

A common POMP workflow constructs a profile likelihood by (1) running a box global search (`if.box`), (2) running a separate profile IF2 search (`if.prof`) over a grid of fixed values for the target parameter, and (3) evaluating the log-likelihood at the profile-search parameter estimates. A recurring copy-paste error is to evaluate the log-likelihood using `coef(if.box[[i]])` instead of `coef(if.prof[[i]])` in the likelihood evaluation step. Because the box-search object has already been computed and is in scope, and the loop index `i` is shared with the profile loop, this error compiles and runs silently. The resulting "profile likelihood" plot reflects box-search parameters re-evaluated at a higher particle count, not a true profile over the target parameter.

## When to Activate

Use this skill when:
- A POMP project runs a profile IF2 search (e.g., via `foreach(i=1:nrow(guesses)) %dopar% mif2(...)` over a `profile_design()` grid) and stores the result in a variable such as `if.prof`.
- The project also has a prior global box search stored in a variable such as `if.box`.
- The project evaluates log-likelihood in a subsequent `foreach` loop using `pfilter(ndx.filt, params=coef(...[[i]]), ...)`.

Do not use this skill when:
- The project has only one IF2 result object in scope (no risk of mis-indexing).
- The profile likelihood is constructed using a dedicated `profile_design`-based helper that encapsulates both the search and evaluation in the same loop.
- The project uses `traj_objfun` or deterministic profile methods that do not involve a separate pfilter evaluation step.

## Procedure

### 1. Identify the profile search loop

Search the Rmd/R source for a `foreach` (or similar parallel loop) that calls `mif2(...)` with a `params=` argument drawn from `guesses[i,]` or a `profile_design()` result. Note the variable name assigned to the result (e.g., `if.prof`).

### 2. Identify the likelihood evaluation loop

Locate the subsequent `foreach` loop that calls `pfilter(pomp_obj, params=coef(X[[i]]), ...)` and stores results in `L.prof`. Note the variable `X` passed to `coef()`.

### 3. Check whether the correct result object is used

- **Correct pattern**: `coef(if.prof[[i]])` — extracts parameters from the profile-search result.
- **Error pattern**: `coef(if.box[[i]])` — extracts parameters from the box-search result, ignoring the profile optimization entirely.

If the error pattern is present, flag it as a major issue.

### 4. Assess the impact on conclusions

If the error is confirmed:
- The plotted "profile likelihood" shows box-search parameters re-evaluated, not the profile over the fixed parameter.
- Reported confidence intervals derived from the profile plot are invalid.
- Pair plots labeled as "profile" results actually show the box-search distribution.

### 5. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line).
- The consequence: profile likelihood plot and derived confidence intervals are not valid profile likelihoods.
- The fix: replace `coef(if.box[[i]])` with `coef(if.prof[[i]])` in the evaluation loop, ensuring the index `i` runs over the profile search results.

## Limitations

- This skill requires reading the source code; it cannot be detected from the rendered HTML output alone, because the profile plot may look visually plausible even when the wrong object is indexed.
- In some projects, the profile search and box search may have the same number of replicates, making the index mismatch less obvious from the plot shape alone.
- Does not cover errors where the profile parameter is not held fixed during the search (e.g., `sigma_eta` is included in `rw.sd` when it should be excluded for a profile over `sigma_eta`).
