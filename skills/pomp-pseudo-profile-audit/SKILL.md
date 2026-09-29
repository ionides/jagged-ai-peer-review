---
name: pomp-pseudo-profile-audit
description: Detect cases where a POMP project presents global-search scatter plots as profile likelihood curves by filtering and grouping global-search results without ever running a profile-specific IF2 optimization, causing chi-squared confidence intervals derived from those plots to be statistically invalid — use when reviewing a POMP project that displays parameter-vs-loglik plots with CI cutoff lines but shows no separate profile_design or profile mif2 call.
---

# POMP Pseudo-Profile Likelihood Detector

## Purpose

A correct POMP profile likelihood for parameter θ requires: (1) constructing a grid of fixed θ values, (2) running IF2 optimization over all other parameters with θ held fixed at each grid point, and (3) evaluating the log-likelihood at the resulting parameter estimates. A recurring error is to skip steps (1) and (2) entirely: the author filters the global-search result object by a log-likelihood range, groups by rounded values of θ, selects top rows per group, and plots the result as a profile. Applying a chi-squared CI cutoff (max(loglik) − 0.5 × qchisq(df=1, p=0.95)) to this scatter plot produces confidence intervals that have no valid statistical interpretation, because the optimization at each θ value was not constrained to fix θ.

This error is distinct from the three other profile failure modes:
- `pomp-profile-indexing-error`: the wrong result object is used in the pfilter step
- `pomp-profile-guess-stratification-error`: the wrong parameter drives the `group_by` at guess construction
- `pomp-profile-rw-sd-drift-error`: the profiled parameter is not fixed in `rw.sd` during profile IF2

The current error occurs earlier: no profile IF2 search is ever executed.

## When to Activate

Use this skill when:
- A POMP project displays one or more parameter-vs-loglik plots with a horizontal CI cutoff line, described as "profile likelihood" or used to derive confidence intervals.
- The project also has a global (box) search result object (e.g., `global_search.rds`, `if.box`).
- The Rmd/R source shows no `profile_design()` call, no separate foreach loop with a fixed target-parameter grid, and no `mif2(...)` call where the target parameter is excluded from `rw.sd`.

Do not use this skill when:
- The project explicitly runs a separate profile IF2 search (even if imperfect — other profile skills apply in that case).
- The parameter-vs-loglik plot is explicitly labeled as a global-search scatter plot rather than a profile likelihood.
- The project uses a deterministic skeleton and computes a profile via `traj_objfun()` with a fixed parameter; this is a valid (if limited) approach.

## Procedure

### 1. Identify the variable used to construct the profile plots

Search the Rmd/R source for the code that produces parameter-vs-loglik plots. Note:
- The data object used (e.g., `profile_results`, `results`).
- Whether the data object is assigned directly from the global search (e.g., `profile_results <- read_rds("global_search.rds")`).

### 2. Confirm no separate profile IF2 search exists

Search the source for:
- `profile_design(` — would indicate a proper profile grid setup.
- A foreach loop with `mif2(...)` where the loop variable is a fixed value of the target parameter, not a generic random guess.
- Any `rw.sd` construction that explicitly sets the profiled parameter's perturbation to zero.

If none of these appear, the project has no true profile likelihood computation.

### 3. Check the plot construction code

Identify whether the "profile" is constructed by:
```r
results |>
  filter(loglik > max(loglik) - K) |>
  group_by(round(target_param, d)) |>
  filter(rank(-loglik) < n) |>
  ungroup() |>
  ggplot(aes(x = target_param, y = loglik)) + ...
```
This pattern is a scatter-plot filter of the global search, not a profile likelihood. The `group_by` + `filter(rank(-loglik) < n)` step selects the top-n rows per rounded parameter bin from the global search, which is not equivalent to constrained optimization at each grid point.

### 4. Assess the validity of any reported CI

If a horizontal cutoff line is drawn at `max(loglik) - 0.5 * qchisq(df=1, p=0.95)` on these plots:
- The CI is derived from the profile likelihood theorem, which requires that the plotted curve is the true profile likelihood.
- Because no constrained optimization was performed, the plotted curve is not the profile likelihood, and the CI is invalid.
- Flag as a major issue: any stated parameter range or confidence interval derived from these plots must be recomputed using a genuine profile likelihood search.

### 5. Report the finding

For each detected instance, report:
- The code location (variable assignment and plot chunk) showing that `profile_results` is the global search object.
- The absence of a profile_design or profile IF2 loop.
- The consequence: plotted curves are global-search scatter plots; chi-squared CI cutoffs are not statistically valid; reported confidence intervals are unreliable.
- The fix: run a dedicated profile search using `profile_design(target_param, ...)` to fix the parameter at a grid of values, optimize all other parameters via IF2 at each grid point (with target_param excluded from `rw.sd`), evaluate log-likelihood at each result, then apply the chi-squared threshold.

## Limitations

- This skill requires reading the source code; the rendered HTML plots may look visually similar to valid profile likelihood curves.
- In some cases the global-search scatter approximates the true profile reasonably well (especially if the global search had very dense coverage), so the practical impact on CI bounds may be small. However, the error should always be flagged because correctness is not guaranteed.
- Does not replace the three other profile skills (`pomp-profile-indexing-error`, `pomp-profile-guess-stratification-error`, `pomp-profile-rw-sd-drift-error`), which apply when a profile IF2 search was actually run but with errors in the setup or evaluation step.
