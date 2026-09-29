---
name: pomp-profile-range-misalignment
description: Detect cases where a POMP profile likelihood grid range does not include the global MLE, causing the profile maximum and chi-squared CI to be artifacts of the grid boundaries rather than the true likelihood surface — use when reviewing a POMP project that computes a profile likelihood after a global search and the profile maximum lies at or near the boundary of the profiled parameter grid.
---

# POMP Profile Likelihood Range Misalignment Detector

## Purpose

A correct POMP profile likelihood requires that the grid of fixed parameter values spans a range that includes (or at least brackets) the global MLE. If the grid range is too narrow or offset, the profile maximum will be at or near a boundary, the chi-squared CI cutoff will be applied to an incomplete likelihood surface, and the reported CI bounds will be artifacts of the chosen range rather than reflections of the true uncertainty.

This error is distinct from the four other profile failure modes:
- `pomp-pseudo-profile-audit`: no profile IF2 search was run at all
- `pomp-profile-rw-sd-drift-error`: the profiled parameter is not fixed in `rw.sd`
- `pomp-profile-guess-stratification-error`: wrong `group_by` at guess construction
- `pomp-profile-indexing-error`: wrong result object used in the pfilter step

The current error occurs after a technically correct profile IF2 search has been run, but at a grid that excludes the region of interest.

## When to Activate

Use this skill when:
- A POMP project reports a profile likelihood for a parameter (e.g., `rho`) alongside a global search result.
- The profile grid is defined by a fixed `seq(lower, upper, length.out = n)` or similar.
- The profile maximum is at or near the boundary of the grid (i.e., the maximum log-likelihood occurs at the smallest or largest grid point).
- The global search reports a MLE for the same parameter that lies outside the profile grid range.

Do not use this skill when:
- The profile maximum is in the interior of the grid and the global MLE is consistent with the profile peak.
- The project explicitly states it is restricting the profile to a scientifically constrained range and justifies the bounds.
- The profile is constructed for diagnostic illustration only, with no CI claimed.

## Procedure

### 1. Identify the profiled parameter and its MLE from the global search

Read the global search section. Note the MLE estimate for the target parameter (e.g., `rho = 0.004` from the best row of the global search result object).

### 2. Identify the profile grid range

Locate the profile grid construction code, e.g.:
```r
rho = seq(0.02, 0.08, length.out = 25)
```
Note `lower` and `upper` of the grid.

### 3. Check whether the global MLE lies within the grid range

Compare the MLE from Step 1 to the range from Step 2:
- If MLE < lower or MLE > upper, flag a range misalignment.
- Compute the ratio: `(MLE) / (grid lower)` or `(grid upper) / (MLE)`. A ratio exceeding 2 indicates the MLE is far outside the grid.

### 4. Assess the consequence for the profile maximum and CI

If the global MLE is outside the profile grid:
- The profile maximum will be at the grid boundary closest to the MLE.
- The chi-squared cutoff `max(profile_loglik) - 1.92` applied to this truncated surface produces a CI that is biased toward the interior of the grid.
- The profile cannot confirm that the global MLE is the true optimum; it may be masking a higher-likelihood region outside the grid.

### 5. Check whether the profile log-likelihood at its maximum equals the global log-likelihood

The maximum of the profile likelihood should equal (within Monte Carlo error) the maximum of the global search likelihood. If the profile maximum is substantially lower than the global maximum, this confirms that the region containing the global optimum was not searched.

### 6. Report the finding

For each detected instance, report:
- The code location defining the profile grid range.
- The global MLE value and its position relative to the profile grid.
- The consequence: the profile maximum and CI are artifacts of the grid boundaries, not the true likelihood surface.
- The fix: extend the profile grid to bracket the global MLE (e.g., set `lower = MLE / 5` and `upper = MLE * 5` for a log-scale parameter, or use a range centered on the global MLE).

## Limitations

- This skill requires that both the global search results and the profile grid definition are visible in the source code or saved artifacts. If only the rendered profile plot is available, a boundary-maximum can be detected visually but the global MLE cannot be independently verified.
- In some cases the global MLE is implausible (e.g., due to a biologically implausible compensation mechanism) and the authors deliberately chose a more scientifically defensible grid range. If this choice is explicitly justified, it is not an error — but the CI should be reported as a conditional CI given the constrained range.
- Does not replace the other four profile failure mode checks; all five should be applied when reviewing a POMP profile likelihood.
