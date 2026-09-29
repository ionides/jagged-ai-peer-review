---
name: pomp-profile-guess-stratification-error
description: Detect the anti-pattern of constructing starting guesses for a POMP profile likelihood search by stratifying on the wrong parameter (e.g., grouping by rho instead of the profiled parameter mu_SV), which leaves the profile axis poorly covered and renders the resulting confidence interval unreliable — use when reviewing a POMP project that builds a profile likelihood by seeding IF2 runs from global-search results grouped by a parameter variable.
---

# POMP Profile Likelihood Guess Stratification Error Detector

## Purpose

A standard workflow for computing a POMP profile likelihood over a target parameter (e.g., `mu_SV`) seeds IF2 starting points by selecting high-likelihood rows from a previous global search, stratified by the target parameter's value. The stratification ensures that the profile search explores the full range of the target parameter. A recurring error is to stratify by the wrong parameter — for example, grouping by `round(rho, 2)` and keeping the top k rows per rho group. Because rho and mu_SV are not perfectly correlated, this stratification may leave large regions of the mu_SV axis without any starting point, producing a profile plot with gaps and a confidence interval that does not reflect the true profile.

This error is distinct from the profile-indexing error (using the wrong result object in the pfilter step): the current error occurs at the guess-construction stage, before any profile IF2 run is executed.

## When to Activate

Use this skill when:
- A POMP project constructs a profile likelihood by seeding IF2 runs from a subset of global-search results.
- The subsetting/filtering code uses `group_by(...)` followed by a `filter(rank(-loglik) <= k)` or `top_n(k, loglik)` call.
- The `group_by(...)` variable is not the parameter being profiled.

Do not use this skill when:
- The profile is constructed using `profile_design()` with an explicit grid over the target parameter — this function directly controls coverage of the target axis.
- The project performs no profile likelihood computation.
- The guesses are drawn from a uniform box (`runif_design`) rather than filtered from previous search results.

## Procedure

### 1. Identify the profiled parameter

Read the profile likelihood section. Determine which parameter is the stated subject of the profile (e.g., `mu_SV`, `Beta`, `rho`). Call this the **target parameter**.

### 2. Locate the guess-construction block

Find the code block that produces the starting guesses for the profile IF2 search. It typically looks like:

```r
read_csv("final_params.csv") |>
  group_by(cut = round(SOME_PARAM, 2)) |>
  filter(rank(-loglik) <= k) |>
  ungroup() |>
  select(-cut, -loglik, -loglik.se) -> guesses
```

### 3. Check whether `group_by` uses the target parameter

- **Correct pattern**: `group_by(cut = round(TARGET_PARAM, 2))` — stratifies on the same parameter being profiled, ensuring coverage across its range.
- **Error pattern**: `group_by(cut = round(OTHER_PARAM, 2))` — stratifies on a different parameter; coverage over the target axis is not guaranteed.

If the error pattern is present, flag it.

### 4. Assess the coverage gap

Examine (or request) the distribution of `TARGET_PARAM` values in the constructed `guesses` object. If the target parameter spans a narrow range in `guesses` relative to its range in `final_params.csv`, the profile will have gaps.

Also check: is `TARGET_PARAM` excluded from `rw.sd` in the profile IF2 call (correct, to fix it at the guess value)? If it is not excluded from `rw.sd`, the target parameter can drift away from the intended fixed value during optimization, further invalidating the profile.

### 5. Check reference likelihood for the CI computation

Verify that the confidence interval cutoff `max(loglik) - 0.5 * qchisq(df=1, p=0.95)` uses the global maximum log-likelihood (from the full parameter search), not just the maximum within the profile results. If the profile results have been merged back into the global results file (e.g., via `write_csv` that appends rows), the reference maximum may be inflated or deflated depending on ordering, producing an incorrect CI cutoff.

### 6. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) of the incorrect `group_by`.
- The consequence: the profile may lack starting points across the full range of the target parameter; reported CI bounds are unreliable.
- The fix: replace `group_by(cut = round(OTHER_PARAM, 2))` with `group_by(cut = round(TARGET_PARAM, 2))`, or switch to `profile_design()` for explicit grid-based coverage.

## Limitations

- This skill requires reading source code; the rendered profile plot may look superficially plausible even when the coverage is poor.
- If the target parameter and the stratification parameter are strongly correlated in the global search results, the error may have minimal practical impact — but it should still be flagged because the correctness depends on an unverified empirical relationship.
- Does not cover errors where the target parameter is included in `rw.sd` (allowed to drift during optimization); that is a separate issue also worth checking during profile review.
- Does not replace the full profile-indexing error check (covered by `pomp-profile-indexing-error/SKILL.md`); both checks should be applied when reviewing a POMP profile likelihood.
