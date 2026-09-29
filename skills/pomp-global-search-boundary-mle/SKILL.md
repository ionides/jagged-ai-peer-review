---
name: pomp-global-search-boundary-mle
description: Detect cases where a POMP global IF2 search produces MLE parameter estimates that cluster at or near a box boundary, indicating the constraint is binding and the true unconstrained optimum likely lies outside the search space — use when reviewing a POMP project whose global search results show a parameter concentrated at one edge of its specified box range.
---

# POMP Global Search Boundary MLE Detector

## Purpose

In a POMP global IF2 search, starting parameters are drawn uniformly from a box and optimized via iterated filtering. When the true (unconstrained) MLE for a parameter lies outside the box, the optimizer cannot reach it and instead converges to the box boundary. The resulting MLE is a constrained optimum — not the global optimum — and all downstream conclusions (parameter estimates, profile likelihoods, CIs) are conditional on the artificial constraint imposed by the box. This error is silent: the optimization runs without error, the log-likelihood is plausible, and simulations from the boundary MLE may look visually reasonable.

The key diagnostic signature is that the top-ranked global search results all share nearly identical values for a particular parameter, and those values coincide with the upper or lower bound of the declared search box.

This error is distinct from:
- `pomp-global-search-box-misalignment`: that skill covers cases where the global search best log-likelihood is *lower* than the local search best, or where the saved artifact contains parameter values that have already drifted *outside* the stated box bounds. Here, the values are *within* the box but clustered at the boundary — the optimizer is stuck against a wall it cannot pass through.
- `pomp-global-search-box-domain-violation`: that skill covers box bounds that violate declared parameter transformation domains. Here, the bounds are within the transformation domain but artificially truncate the likelihood surface.
- `pomp-profile-range-misalignment`: that skill covers the profile grid not spanning the global MLE. This skill covers the global search box not spanning the unconstrained MLE.

## When to Activate

Use this skill when:
- A POMP project runs a global IF2 search by sampling starting parameters from a box (e.g., via `runif_design`).
- The saved global search result object (CSV or RDS) is available for inspection.
- Inspection of the top-ranked results reveals that one or more parameters have nearly identical values across all high-likelihood rows, with those values close to the stated upper or lower box bound.

Do not use this skill when:
- The global search results show parameter values spread across the interior of the box (far from boundaries), indicating the MLE is interior to the search space.
- The parameter's concentration at a boundary is explicitly motivated by the biology (e.g., the authors fix a parameter at its boundary for scientific reasons and discuss the constraint).
- The project uses `partrans = parameter_trans(log = ...)` for the parameter, in which case the boundary on the natural scale may not correspond to a boundary on the transformed scale used by IF2.

## Procedure

### 1. Locate the global search box definition

Read the `runif_design(lower = ..., upper = ...)` call or equivalent box definition. Record the lower and upper bounds for each parameter.

### 2. Load the global search result artifact

Read the saved result CSV or RDS file. For each parameter, compute:
- The range of values across all rows: `range(results$param_name, na.rm=TRUE)`.
- The values among the top-k rows by log-likelihood (e.g., top 10): `results[order(-results$loglik), ][1:10, "param_name"]`.

### 3. Check for boundary concentration in top results

For each parameter, compare the top-k values to the box bounds:
- **Error pattern**: All top-10 values of `tau` are within 5% of the upper box bound (e.g., tau_upper = 0.1 and all top values are 0.098–0.102).
- **Correct pattern**: Top values are spread across the interior of the box, well away from both boundaries.

A quantitative threshold: if more than 80% of the top-10 results have a parameter value within 5% of a box boundary, flag a potential boundary MLE.

### 4. Verify whether the MLE appears to be at the boundary

Check whether the single best-fit row (highest log-likelihood) has the parameter at or very near the boundary:
```r
best_row <- results[which.max(results$loglik), ]
cat("tau MLE:", best_row$tau, "  Upper bound:", tau_upper, "\n")
```
If `|MLE - bound| / bound < 0.05`, the MLE is at the boundary.

### 5. Assess whether the boundary is binding

A binding constraint means the optimizer is prevented from reaching a higher log-likelihood by the box limit. Evidence includes:
- The log-likelihood does not plateau as the parameter approaches the boundary; it continues to increase up to the boundary.
- A scatter plot of the parameter vs. log-likelihood shows a monotone increasing (or decreasing) trend ending abruptly at the boundary.

### 6. Assess the impact on downstream inference

If a binding constraint is confirmed:
- The reported MLE is a constrained estimator, not the global MLE.
- Profile likelihoods for other parameters, conditioned on the constrained MLE, are themselves conditioned on the wrong point.
- CIs for the boundary parameter cannot be computed within the current box.
- The reported log-likelihood is a lower bound on the true maximum log-likelihood.

### 7. Report the finding

For each detected boundary MLE:
- State the parameter name, its box bounds, and the MLE value relative to the boundary.
- Note that the reported log-likelihood is a constrained optimum, not the global MLE.
- Propose the fix: extend the box bound in the direction of the boundary by a factor of 2–5, re-run the global search, and check whether the MLE moves inward or continues to hug the new boundary. If the MLE stabilizes at an interior point, the unconstrained optimum has been found.

## Limitations

- This skill requires access to the saved global search result artifact and the box definition. It cannot be applied from the rendered HTML alone unless the MLE parameter table is shown with sufficient decimal precision.
- For parameters with log or logit transformations, the "boundary" on the natural scale may not produce a sharp constraint on the transformed scale used by IF2. In those cases, verify the issue on the transformed scale before flagging.
- A parameter near its boundary may reflect genuine biology (e.g., near-zero immunity loss) rather than a box constraint. Always compare the boundary value to biological plausibility before concluding the constraint is artificial.
- Does not replace the `pomp-global-search-box-misalignment` skill. Both should be applied: box-misalignment detects cases where IF2 drifted outside the box, while this skill detects cases where the MLE is stuck at the boundary from the inside.
