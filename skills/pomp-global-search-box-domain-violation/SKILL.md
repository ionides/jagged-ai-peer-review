---
name: pomp-global-search-box-domain-violation
description: Detect cases where a POMP global IF2 search box specifies starting-value ranges that violate the domain of declared parameter transformations (e.g., rho > 1 for a logit-transformed probability, or negative values for a log-transformed rate), causing invalid starting points to be drawn before the transformation is applied — use when reviewing a POMP project whose global search box and partrans declarations are defined separately.
---

# POMP Global Search Box Domain Violation Detector

## Purpose

POMP models declare parameter transformations via `parameter_trans(log = c(...), logit = c(...))` in the `pomp()` call. During a global IF2 search, starting parameters are drawn from a box using `runif(1, lower, upper)` on the *natural* (untransformed) scale, then passed to `mif2()`. If the box bounds are set outside the domain of the declared transformation — for example, `rho = c(0, 2)` for a logit-transformed probability that requires rho in (0, 1) — the starting values drawn from the box can violate the transformation domain. Values of rho > 1 have no valid logit representation, and values of rho = 0 or 1 produce -Inf or +Inf on the logit scale.

This error is distinct from:
- `pomp-global-search-box-misalignment`: that skill covers boxes whose valid range excludes the region containing the MLE. Here, the box range itself is invalid for the declared transformation.
- `pomp-partrans-undeclared-param`: that skill covers parameters that lack a transformation declaration. Here, the transformation IS declared, but the box violates its domain.
- `pomp-global-search-param-override-bug`: that skill covers c() concatenation creating duplicate names.

## When to Activate

Use this skill when:
- A POMP project declares `partrans = parameter_trans(logit = c("rho", ...), log = c("Beta", ...))` in the `pomp()` call.
- The global search box (`covid_box`, `nflx_box`, etc.) specifies bounds for a logit-transformed parameter outside (0, 1) (e.g., `rho = c(0, 2)`, `alpha = c(-0.1, 1.1)`), or bounds for a log-transformed parameter that include zero or negative values (e.g., `mu_IR = c(-0.5, 10)`).
- Starting parameters are drawn from the box using `runif(1, lower, upper)` on the natural scale.

Do not use this skill when:
- The box bounds for logit-transformed parameters are strictly within (0, 1) and bounds for log-transformed parameters are strictly positive.
- The project applies its own clamping before passing starting values to mif2 (e.g., `pmax(pmin(x, 0.999), 0.001)` for logit parameters).
- The starting parameters for the global search are specified on the transformed (log or logit) scale rather than the natural scale.

## Procedure

### 1. Identify the partrans declaration

Read the `parameter_trans(log = c(...), logit = c(...))` argument in the `pomp()` call. Produce two lists:
- `logit_params`: parameters declared with logit transformation (must be in (0, 1) on natural scale).
- `log_params`: parameters declared with log transformation (must be > 0 on natural scale).

### 2. Locate the global search box definition

Find the box definition (e.g., `covid_box <- rbind(Beta = c(0, 2), rho = c(0, 2), ...)`). For each parameter row, note the lower and upper bounds.

### 3. Check bounds for logit-transformed parameters

For each parameter in `logit_params`, verify that the box lower bound is > 0 and the upper bound is < 1:
- **Error pattern**: `rho = c(0, 2)` — upper bound > 1, invalid for logit transformation.
- **Error pattern**: `alpha = c(0, 1)` — boundary values 0 and 1 produce -Inf and +Inf on the logit scale; bounds should be, e.g., c(0.001, 0.999).
- **Correct pattern**: `rho = c(0.001, 0.999)` — strictly within the logit domain.

### 4. Check bounds for log-transformed parameters

For each parameter in `log_params`, verify that the box lower bound is > 0:
- **Error pattern**: `mu_IR = c(0, 10)` — lower bound of 0 produces -Inf on the log scale.
- **Correct pattern**: `mu_IR = c(0.001, 10)` — lower bound is strictly positive.

### 5. Assess the impact on the global search

If domain-violating bounds are confirmed:
- Starting values drawn from the invalid region (e.g., rho = 1.5) cannot be transformed by the logit function and will produce NaN or error in the IF2 step.
- In some pomp versions, NaN parameter values are silently replaced by the starting parameter value or cause the replicate to fail without warning, effectively reducing the number of functional global search replicates.
- The reported global search coverage of the parameter space is incomplete: replicates that start in the invalid region contribute no useful optimization.

### 6. Report the finding

For each detected domain violation, report:
- The parameter name.
- The declared transformation (log or logit).
- The box bounds that violate the domain.
- The consequence: starting values outside the transformation domain produce NaN or -Inf; those search replicates fail or fall back to default values, reducing effective coverage.
- The fix: tighten box bounds to the valid domain (e.g., `rho = c(0.001, 0.999)` for logit; `mu_IR = c(1e-6, 10)` for log).

## Limitations

- This skill requires cross-checking the box definition against the partrans declaration. It cannot be detected from the rendered HTML output.
- Some pomp versions may handle out-of-domain starting values gracefully by projecting them back into the valid domain; in that case the error is latent rather than manifest.
- If the number of global search replicates is large (> 50) and only a few fall in the invalid region, the practical impact on the reported global maximum may be small — but the error should still be flagged because correctness depends on the empirical distribution of uniform draws from the box.
- Does not replace the `pomp-global-search-box-misalignment` skill; that skill handles the case where valid starting values are drawn from a region that excludes the MLE. Both should be applied when reviewing POMP global searches.
