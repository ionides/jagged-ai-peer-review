---
name: pomp-partrans-undeclared-param
description: Detect cases where a POMP model extension adds new parameters (e.g., tau, amplitude) to paramnames without declaring any transformation for them in partrans, leaving those parameters on their natural scale during IF2 and allowing them to drift outside their implied domain — use when reviewing a POMP project that extends a base model with additional parameters and uses a partrans declaration copied from the base model.
---

# POMP Parameter Transformation Undeclared-Parameter Detector

## Purpose

When authors extend a base POMP model (e.g., adding a Student-t degrees-of-freedom parameter `tau` or a regime-amplitude parameter `amplitude` to a base SV model), they typically copy the base model's `parameter_trans()` call and add the new parameters to `paramnames`. If the new parameters have implicit domain constraints (e.g., `tau > 0`, `amplitude > 0`, or `tau ∈ (1, 60)`), but are not added to the `partrans` declaration, they receive the identity transformation during IF2. This means:

1. IF2 random-walk perturbations can push the parameter outside its domain (e.g., `tau < 0`).
2. Hard clamps in the Csnippet (e.g., `nearbyint(tau) < 1 ? 1 : tau`) prevent runtime crashes but introduce a non-smooth boundary that the optimizer cannot respect, distorting convergence.
3. The reported MLE for the unconstrained parameter may be at a boundary artifact rather than a genuine interior optimum.

This error is distinct from `pomp-partrans-override-bug`, which covers cases where a `mif2()` call supplies its own `partrans` argument that omits parameters already declared in the `pomp()` call. Here, the `pomp()` call itself is the source of the omission — no override is involved; the parameters simply were never added to the declaration.

## When to Activate

Use this skill when:
- A POMP project extends a base model by adding one or more new parameters to `paramnames` (e.g., `tau`, `amplitude`, `nu_df`, `lambda`, `kappa`).
- The new parameters have an implied positivity or boundedness constraint (e.g., degrees of freedom must be > 0, amplitudes are meant to be positive).
- The `partrans = parameter_trans(...)` declaration in the `pomp()` call is copied from the base model and does not include the new parameters.
- The Csnippet contains a clamp or `nearbyint` guard that compensates for the missing constraint.

Do not use this skill when:
- The new parameters are intentionally unconstrained (e.g., a mean parameter that can be any real number).
- All new parameters with domain constraints are explicitly declared in `partrans` with appropriate transformations.
- The project uses `pomp-partrans-override-bug` (which handles mif2-level overrides, not pomp-level omissions).

## Procedure

### 1. Identify the paramnames list

Read the `paramnames` argument in the `pomp()` call (or the `N_rp_names`, `N_ivp_names` vectors that feed into it). List every parameter by name.

### 2. Read the partrans declaration

Locate the `parameter_trans(log = c(...), logit = c(...))` call. List every parameter with a declared transformation.

### 3. Compute the undeclared set

Take the set difference: parameters in `paramnames` that are absent from any transformation family in `partrans`. For each undeclared parameter, note:
- Its name.
- Any domain constraint implied by its biological/mathematical role (e.g., `tau = df > 0`, `phi ∈ (0,1)`, `amplitude > 0`).
- Whether the Csnippet contains a compensating clamp (e.g., `nearbyint(tau) < 1 ? 1 : tau`).

### 4. Flag undeclared constrained parameters

For each parameter with an implied constraint that lacks a `partrans` entry:
- **Error pattern**: `tau` appears in `paramnames` and is clamped to `(1, 60)` in the Csnippet, but `partrans` contains only `log=c("sigma_eta","sigma_nu"), logit="phi"`.
- **Correct pattern**: `parameter_trans(log=c("sigma_eta","sigma_nu","tau"), logit="phi")`.

Note: a `log` transform for a lower-bounded-at-zero parameter, or a `logit` transform with scaling for a (a, b)-bounded parameter, is the standard fix.

### 5. Assess the impact on IF2 convergence

For each flagged parameter:
- Determine the rw.sd value assigned to the parameter. A large rw.sd relative to the parameter's natural scale (e.g., `rw.sd_tau = 1` for `tau = 5`) means IF2 will frequently attempt values outside the domain.
- Examine the convergence trace for the parameter: flat or high-variance traces for a constrained parameter with no transformation are a diagnostic signature.
- If the parameter is clamped in the Csnippet, note that the optimizer sees a flat likelihood surface near the clamp boundary, which can distort the MLE and artificially compress confidence intervals.

### 6. Report the finding

For each detected instance, report:
- The parameter name and its implied constraint.
- The code location of the `parameter_trans()` call that omits the transformation.
- The Csnippet clamp (if present) that compensates but does not fix the underlying issue.
- The consequence: IF2 can explore out-of-domain values, convergence may be distorted, and the reported MLE for the unconstrained parameter may be at a clamp boundary rather than an interior optimum.
- The fix: add the appropriate transformation to `parameter_trans()` (e.g., `log = c("tau", "amplitude")` for positive parameters).

## Limitations

- This skill requires reading both the paramnames list and the partrans declaration carefully. The error is invisible from convergence plots alone unless the parameter exhibits the characteristic flat/clamp boundary pattern.
- Parameters that are intentionally unconstrained (real-valued) should not be flagged. The skill requires domain knowledge to determine whether a parameter has an implicit constraint.
- If the IF2 rw.sd for the undeclared parameter is small enough that the parameter rarely leaves its domain during a typical run, the practical impact may be negligible. However, the error should still be flagged because correctness is not guaranteed across all runs and starting values.
- Does not replace `pomp-partrans-override-bug`, which covers the mif2-level override case. Both skills should be applied when reviewing POMP models with custom `partrans` declarations.
