---
name: pomp-global-search-box-misalignment
description: Detect cases where the POMP global IF2 search box excludes the region containing the global MLE, causing the global search to underperform the local search and making any "global maximum" claim unreliable — use when reviewing a POMP project that reports a global search best log-likelihood below the local search best, or whose parameter box does not span the MLE found by the local search.
---

# POMP Global Search Box Misalignment Detector

## Purpose

A correct POMP global IF2 search should initialize parameter vectors uniformly from a box that brackets the global MLE. If the box for any parameter is constructed using prior assumptions that exclude the true MLE region, the global search can only reach the better region if IF2 perturbs the parameters outside their initial bounds during optimization. This is accidental rather than systematic exploration, and the claimed "global" coverage is invalid.

The diagnostic signature is:
- The global search best log-likelihood is lower (worse) than the local search best log-likelihood.
- Inspection of the saved global search artifacts shows that the highest-likelihood solutions have parameter values outside the specified box bounds.
- Only a small fraction of global replicates (e.g., 5 out of 20) found the high-likelihood region.

This error is distinct from:
- `pomp-global-search-init-audit`: that skill handles the wrong first argument to mif2 (previous mif2 result vs. pomp object). Here the first argument is correct; the box range is the problem.
- `pomp-global-search-param-override-bug`: that skill handles the duplicate-name c() concatenation bug at parameter construction time.
- `pomp-profile-range-misalignment`: that skill handles the profile likelihood grid range, not the global search box.

## When to Activate

Use this skill when:
- A POMP project runs a global IF2 search by sampling starting parameters from a box (e.g., `apply(nflx_box, 1, runif)` or `runif_design`).
- The global search best log-likelihood is lower than the local search best log-likelihood (after accounting for Monte Carlo noise; a gap of more than ~2 units is suspicious).
- The saved global search artifact contains high-likelihood parameter values outside the stated box bounds for one or more parameters.
- The project interprets the global search as having found the global MLE when in fact the optimizer drifted to good solutions not covered by the box.

Do not use this skill when:
- The global search clearly outperforms the local search (global best > local best), indicating adequate box coverage.
- The box is defined to intentionally restrict to a scientifically constrained range and the authors acknowledge this.
- Only one search stage (local or global) is run; a comparison between stages requires both.

## Procedure

### 1. Compare global and local search log-likelihoods

Load the saved local and global search result files (CSV or RDA artifacts). Compare:
```r
max(global_results$logLik, na.rm=TRUE)  # global best
max(local_results$logLik, na.rm=TRUE)   # local best
```
If the global best is more than ~2 units below the local best, flag a potential box misalignment.

### 2. Identify the parameter values at the global best

Extract the best-row parameters from the global search:
```r
global_results[which.max(global_results$logLik), ]
```
For each parameter, compare the MLE value to the stated box bounds.

### 3. Check whether any MLE parameter values lie outside the box bounds

For each dimension of the box, verify:
- Is the global MLE value within [box_lower, box_upper]?
- If the MLE is outside the box, note the direction (above upper bound or below lower bound) and the ratio.

### 4. Check what fraction of global replicates found the high-likelihood region

Count the proportion of global replicates that converged to parameter values in the region near the true MLE (e.g., within 5 log-likelihood units of the best):
```r
sum(global_results$logLik > max(global_results$logLik) - 5) / nrow(global_results)
```
If fewer than 50% of replicates are within 5 units of the best, the search was poorly covering the space.

### 5. Identify whether high-likelihood solutions required drifting outside the box

Check whether the high-likelihood global replicates have parameter values that were inside or outside the box at initialization. Because starting values are drawn uniformly from the box, any solution with a parameter outside the box necessarily drifted there during IF2 optimization — which is accidental, not systematic.

### 6. Verify with the local search

Compare the local search best parameters to the box bounds. If the local search (started from a single informed guess) finds solutions outside the box range, this confirms that the box was specified too narrowly and the prior assumption was wrong.

### 7. Report the finding

For each misaligned parameter, report:
- The stated box bounds.
- The local search MLE value for that parameter.
- The global search MLE value for that parameter.
- The fraction of global replicates that reached the high-likelihood region.
- The consequence: the "global maximum" reflects accidental IF2 drift, not systematic box exploration; the reported global MLE may not be reliable.
- The fix: extend the box to include the region identified by the local search (e.g., set box bounds to [local_MLE * 0.5, local_MLE * 2] for positive parameters, or center the box on the local MLE with a generous radius).

## Limitations

- This skill requires access to both the saved local and global search artifacts and the box definition in the source code.
- If the local search itself is poorly converged (e.g., all local replicates stuck in a local optimum), the local MLE may not represent the true global MLE, and comparing to it may be misleading.
- Some IF2 drift outside the initial box is expected and benign for parameters with wide flat regions; this skill is most relevant when the drift is systematic and the box excludes the primary mode.
- Does not replace the `pomp-global-search-init-audit` check; both should be applied when reviewing a POMP global search.
