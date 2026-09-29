---
name: pomp-global-search-param-override-bug
description: Detect the anti-pattern of constructing POMP global search starting parameters via c(base_params, c(overrides)) in R, which appends duplicate names rather than overriding them, silently making the global search start from the same fixed point for every replicate — use when reviewing a POMP project that builds a global search box by concatenating a base parameter vector with override values.
---

# POMP Global Search Parameter Override Bug Detector

## Purpose

A common POMP global search workflow attempts to randomize starting parameters by constructing each replicate's parameter vector as `c(base_params, c(b_1 = runif(...), b_2 = runif(...), ...))`. In R, the `c()` function concatenates named vectors without deduplication: if `base_params` already contains elements named `b_1`, `b_2`, etc., the result is a vector with duplicate names — the override values are appended at the end, not substituted in place. Because pomp's `coef()` and `mif2()` typically use the first occurrence of each named parameter, the override values are silently ignored. The global search is therefore not a genuine global search: every replicate starts from the same fixed `base_params` values, producing 20 (or however many) copies of what is effectively a local search.

This error is distinct from the global-search-init-audit error (using a previous mif2 result as the first argument to mif2): that error anchors the cooling schedule, while this error silently defeats parameter randomization at the initialization stage.

## When to Activate

Use this skill when:
- A POMP project constructs global search starting parameters using `c(base_params, c(param1 = runif(...), param2 = runif(...), ...))` or `c(base_params, list(...))` inside a `replicate()` or `lapply()` call.
- `base_params` is extracted from `coef(seir_model)` or assigned as a named vector that already contains the parameters being "overridden."
- The project claims to perform a global search over a parameter box but reports log-likelihoods that are identical or nearly identical across all replicates, or that match the local search exactly.

Do not use this skill when:
- The global search constructs starting parameters using `apply(box, 1, runif)` or `sobolDesign()` or `runif_design()` directly, which generate fresh named vectors without any base_params inheritance.
- The project explicitly uses `modifyList(as.list(base_params), overrides)` or `base_params[names(overrides)] <- overrides` for correct in-place replacement.
- The project stores starting parameters in a matrix or data frame with one row per replicate and passes them via `params = box[i, ]` — this pattern avoids the duplicate-name issue entirely.

## Procedure

### 1. Locate the global search parameter construction code

Search the Rmd/R source for the global search starting-parameter block. It typically appears inside `replicate(N, {...})` or `lapply(1:N, function(i) {...})` feeding into a `foreach` loop.

### 2. Identify the base parameter vector

Determine whether a `base_params` (or equivalent) vector is defined before the override block:
- Is it assigned from `coef(pomp_object)` or as a hardcoded named vector?
- Does it already contain the parameters that the override block attempts to randomize?

### 3. Check for the duplicate-name concatenation pattern

Examine the combining expression:
- **Error pattern**: `c(base_params, c(b_1 = runif(1, -2, 2), b_2 = runif(1, -2, 2), ...))`
  - In R, `c(x, y)` for two named vectors appends `y` after `x`. If both contain `b_1`, the result has two elements named `b_1`. The first one (from `base_params`) is retained by pomp.
- **Correct pattern**: Use `modifyList(as.list(base_params), list(b_1 = runif(1,-2,2), ...))` then `unlist()`, or construct the parameter vector from scratch without inheriting `base_params`.

To confirm the error, check: `length(global_inits[[1]])` vs. `length(base_params)`. If the override vector has K parameters and base_params has P parameters, and all K appear in base_params, then each replicate vector has length P + K instead of P — the duplicates are appended.

### 4. Verify the effective starting values

If a seed is set before `replicate()`, run the first replicate manually and check:
```r
params_1 <- global_inits[[1]]
cat("b_1 occurrences:", sum(names(params_1) == "b_1"), "\n")
cat("first b_1 value:", params_1["b_1"], "\n")
cat("last b_1 value:", tail(params_1[names(params_1) == "b_1"], 1), "\n")
```
If the first occurrence equals the base_params value and the last occurrence equals the intended random value, the bug is confirmed.

### 5. Assess the impact on the global search

If the bug is confirmed:
- All global search replicates begin from the same `base_params` starting point; the "random" overrides are appended but not used.
- The "global search" is effectively N copies of the local search from a fixed start.
- The reported best log-likelihood from the global search reflects a local optimum, not a global optimum.
- Any claimed improvement in log-likelihood from local to global search is either zero (if both use the same base_params) or reflects Monte Carlo noise across identical starting conditions.

### 6. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) of the `c(base_params, c(...))` expression.
- Confirmation that `base_params` already contains the overridden parameter names.
- The consequence: the global search is not global; reported best log-likelihood is from a local optimum.
- The fix: replace `c(base_params, c(overrides))` with `modifyList(as.list(base_params), list(overrides))` followed by `unlist()`, or build the parameter vector from scratch using `c(fixed_params, random_params)` where `fixed_params` does not contain the parameters being randomized.

## Limitations

- This skill requires reading both the source code and understanding R's `c()` semantics for named vectors. It cannot be detected from the rendered HTML output.
- If `base_params` does not already contain the overridden parameter names (e.g., `immigration_rate` is new and not in the original `coef()` output), then `c(base_params, c(immigration_rate = runif(...)))` is correct — only duplicate names are a problem.
- In some pomp versions or calling patterns, the parameter vector may be matched by position rather than by name; in that case the duplicate-name error may have a different effect. Always verify the actual behavior by checking which values the mif2 call uses.
- Does not replace the pomp-global-search-init-audit skill; both should be applied when reviewing global searches.
