---
name: pomp-partrans-override-bug
description: Detect the anti-pattern of supplying a `partrans = parameter_trans(...)` argument directly to a `mif2()` call that omits one or more parameter transformations declared in the base `pomp()` object, silently removing constraints on those parameters and allowing them to be estimated outside their declared domain — use when reviewing a POMP project where the mif2 call includes its own `partrans` argument.
---

# POMP Parameter Transformation Override Bug Detector

## Purpose

A `pomp()` object carries a `partrans` slot that declares how each parameter is transformed for internal optimization (e.g., `log` for positive parameters, `logit` for parameters in (0, 1)). When `mif2()` is called with an explicit `partrans = parameter_trans(...)` argument, that new `partrans` **replaces** — not extends — the one in the base pomp object. Any parameter omitted from the new `partrans` declaration is treated as untransformed (identity) during the IF2 search.

This is a silent failure: the `mif2()` call runs without error, but the parameter constraint is removed. Estimates for the omitted parameter can then drift outside its declared domain (e.g., `amp > 1` when `logit` was declared) and remain there for all subsequent operations that inherit the `mif2` result (e.g., a global search that uses the local `mif2` result as its base object via the `pomp-global-search-init-audit` anti-pattern).

The most common version is a local mif2 call that declares `partrans` for a subset of parameters to fix a numerical issue, forgetting to carry over all parameters from the pomp-level declaration.

## When to Activate

Use this skill when:
- A POMP project declares `partrans` in the `pomp()` call (e.g., `parameter_trans(log = c("Beta", ...), logit = c("rho", "amp", ...))`).
- One or more `mif2()` calls in the same project also supply their own `partrans = parameter_trans(...)` argument.
- The set of parameters listed in the `mif2`-level `partrans` is a strict subset of those in the `pomp`-level `partrans`.

Do not use this skill when:
- The `mif2()` call supplies no `partrans` argument (it correctly inherits the pomp-object's declaration).
- The `mif2`-level `partrans` includes every parameter that the `pomp`-level `partrans` includes (no omission).
- The project uses only the `pomp()`-level `partrans` and calls `mif2()` without overriding it.

## Procedure

### 1. Identify the `partrans` in the `pomp()` call

Search the Rmd/R source for the `pomp()` constructor call. Locate the `partrans = parameter_trans(...)` argument. Record every parameter listed under `log = c(...)`, `logit = c(...)`, or other transformation families.

### 2. Locate every `mif2()` call that supplies a `partrans` argument

Search for `mif2(` calls. For each one, check whether a `partrans =` argument is present.

### 3. Compare parameter lists

For each `mif2`-level `partrans`, compare its listed parameters to those from Step 1:
- **Correct**: Every parameter in the `pomp`-level `partrans` is also in the `mif2`-level `partrans` with the same transformation.
- **Error pattern**: One or more parameters from the `pomp`-level `partrans` are absent from the `mif2`-level `partrans`. Those parameters receive identity transformation during IF2 and can leave their declared domain.

List all omitted parameters by name.

### 4. Verify that estimates exceed the declared domain

Load the saved artifact (local or global search results) and check the range of the omitted parameters:
- For a parameter declared with `logit` but omitted from `mif2` `partrans`: values outside (0, 1) confirm the bug.
- For a parameter declared with `log` but omitted: negative values confirm the bug.

```r
result <- readRDS("results.rds")
cat("Range of amp:", range(result$amp, na.rm=TRUE), "\n")
# Values > 1 with logit declaration confirm the override bug.
```

### 5. Assess propagation through the global search

If the global search uses the local mif2 result as its base object (see `pomp-global-search-init-audit`), the override `partrans` from the local mif2 is inherited by the global search. Confirm that the global search results also show out-of-domain values for the omitted parameter.

### 6. Assess the impact on parameter estimates and model behavior

For each omitted parameter, determine the biological or mathematical consequence of estimating it without the declared constraint:
- `amp` without logit: can exceed 1, causing the seasonal forcing to suppress transmission to exactly zero during the off-season (if the model guards against negative transmission rates). Report whether the model explicitly handles `Beta_t < 0` (e.g., with a clamp to zero) and whether the resulting dynamics are still interpretable.
- A rate parameter without `log`: can become negative, producing undefined probability transitions.

Flag as a major issue if the omitted parameter's estimate is outside its declared domain.

### 7. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) of the `mif2()` call with the overriding `partrans`.
- Which parameters are omitted and what their declared transformation was.
- The confirmed range of estimates in the saved artifact.
- The biological/statistical consequence (e.g., "amp > 1 allows complete suppression of transmission in off-season; estimates are biologically extreme and inconsistent with the declared logit constraint").
- The fix: either (a) remove the `partrans` argument from the `mif2()` call entirely (so it inherits the `pomp`-level declaration), or (b) include all parameters from the `pomp`-level `partrans` in the `mif2`-level `partrans`.

## Limitations

- This skill requires reading both the source code and the saved artifacts to confirm out-of-domain values. In some cases the optimizer may not have moved the omitted parameter outside its domain even without a constraint, making the bug latent rather than manifest.
- If the omitted parameter's natural-scale estimates happen to remain within the declared domain despite the missing constraint (e.g., `amp` stays below 1 by chance), the bug is still present and should be flagged, because the absence of the constraint means no guarantee the parameter will remain in-domain on different data or with different starting values.
- Does not replace the `pomp-global-search-init-audit` check: if the global search also uses the local mif2 result as its base object, both bugs compound each other and both should be reported.
- Does not cover the case where `partrans` is consistent but the declared transformation domain is itself incorrect (e.g., declaring `logit` for a parameter that should be unrestricted).
