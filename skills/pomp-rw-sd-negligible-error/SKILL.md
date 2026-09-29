---
name: pomp-rw-sd-negligible-error
description: Detect cases where a POMP IF2 search sets rw.sd perturbation sizes to numerically negligible constants (e.g., 2e-9) across all parameters, making IF2 perturbations effectively zero and producing no parameter movement — the opposite of the rw.sd-too-large error — use when reviewing a POMP project whose rw.sd values are orders of magnitude smaller than the parameter scales being optimized.
---

# POMP rw.sd Negligible-Value Error Detector

## Purpose

The `rw.sd` argument in `mif2()` controls the standard deviation of the random-walk perturbations applied to each parameter at each IF2 iteration. A distinct error from setting rw.sd too large (covered by `pomp-rw-sd-magnitude-error`) is setting rw.sd to a numerically negligible constant — such as `covid_rw.sd = 0.000000002` (2e-9) — across all parameters, regardless of the parameter scales. For parameters on scales of 0.001–10 (typical epidemiological rates), a perturbation SD of 2e-9 produces no effective movement per iteration. Combined with aggressive cooling (e.g., `cooling.fraction.50 = 0.00005`), the IF2 perturbations shrink from near-zero to essentially machine-zero within the first few iterations. The result is that every "global search" replicate evaluates the likelihood at approximately its random starting point, without any gradient-following optimization. The reported log-likelihoods and parameter estimates reflect the distribution of starting-point evaluations, not any optimization.

This error is distinct from:
- `pomp-rw-sd-magnitude-error`: that skill handles rw.sd set equal to the parameter starting values (too large). Here the error is rw.sd set to a tiny shared constant (too small).
- `pomp-global-search-init-audit`: that skill handles the wrong first argument to mif2.
- `pomp-profile-rw-sd-drift-error`: that skill handles non-zero rw.sd for the profiled parameter.

## When to Activate

Use this skill when:
- A POMP project defines a single shared `rw.sd` constant variable (e.g., `covid_rw.sd = 0.000000002`) and applies it uniformly to all parameters in `mif2()`.
- The shared rw.sd value is smaller than 1e-6, while the parameters being optimized span ranges of 1e-3 or larger.
- The convergence traces show flat lines from the first iteration with no visible parameter movement (confirming that no optimization is occurring).
- The project also sets `cooling.fraction.50` to a very small value (e.g., < 0.001), compounding the negligible perturbation by shrinking it to zero within a few iterations.

Do not use this skill when:
- The `rw.sd` values are individually calibrated per parameter and are in a reasonable range (e.g., 0.001–0.1 for unit-scale parameters).
- The rw.sd is small for a transformed parameter (log or logit scale) and the small value is appropriate given the expected uncertainty on that scale.
- The project is using a deterministic skeleton and least-squares rather than stochastic IF2.

## Procedure

### 1. Locate the rw.sd definition

Search the Rmd/R source for any variable assigned as a shared rw.sd scalar (e.g., `covid_rw.sd = ...`). Note the numerical value.

### 2. Identify the parameter scales being optimized

Read the search box or starting parameter values. Record the range of each parameter (e.g., `Beta1 ∈ (0, 0.001)`, `mu_ECa ∈ (0, 0.01)`). The minimum resolution needed to traverse the box is approximately (upper - lower) / Nmif.

### 3. Compare rw.sd to parameter scales

For each parameter:
- Compute the minimum meaningful perturbation: approximately (box_upper - box_lower) / Nmif.
- Compare to the actual rw.sd value.
- **Error pattern**: rw.sd < 1e-6 for a parameter spanning (0, 0.001) with Nmif = 100 → minimum meaningful perturbation ≈ 1e-5, which is 10x larger than the actual rw.sd.
- **Correct pattern**: rw.sd ≈ 1–10% of the parameter range (e.g., 1e-4 for Beta ∈ (0, 0.001)).

### 4. Check the cooling.fraction.50 interaction

Determine whether `cooling.fraction.50` compounds the problem:
- `cooling.fraction.50 = 0.00005` means perturbations are reduced to 0.005% of their initial value by iteration 50. Starting at rw.sd = 2e-9, the perturbation at iteration 50 is ≈ 1e-13 — well below machine precision for double-precision floating-point arithmetic.
- Flag as critical when `rw.sd * cooling.fraction.50 < 1e-12`, because at that point the perturbations are numerically zero for double-precision computation.

### 5. Inspect convergence traces

Examine the IF2 convergence trace plots:
- **Error signature**: All parameter traces are flat horizontal lines from iteration 1 to Nmif. The log-likelihood trace shows random scatter with no increasing trend. Between-replicate variance is nonzero (because starting points differ) but within-replicate variance is zero.
- **Correct signature**: Traces show high initial variance decreasing as the cooling schedule shrinks perturbations, converging toward a stable parameter region.

### 6. Assess impact on reported estimates

If negligible rw.sd is confirmed:
- The "optimization" is equivalent to a random search of the starting-point distribution, with no likelihood-gradient following.
- The best log-likelihood found reflects the starting-point that happened to have the highest likelihood, not the MLE.
- Reported parameter estimates are not MLEs; they are the best among the random starting points.
- All downstream conclusions (parameter interpretation, model comparison by log-likelihood) are invalid.

### 7. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) defining the shared rw.sd constant.
- The numerical value and the parameter scales it was applied to.
- The consequence: IF2 produces no meaningful optimization; reported likelihoods and parameter estimates are the best random starting points, not MLEs.
- The fix: replace the shared constant with individually calibrated rw.sd values approximately 2–5% of the expected parameter range for each parameter (e.g., `rw.sd = rw_sd(Beta1 = 2e-5, Beta2 = 2e-5, mu_ECa = 2e-4, ...)` for parameters in the range 0–0.001 to 0–0.01). Also set `cooling.fraction.50` to a reasonable value (0.1–0.5) to allow adequate parameter exploration before cooling.

## Limitations

- This skill detects the error from code structure (the rw.sd value relative to parameter scales). Convergence traces are required to confirm that no optimization occurred in practice.
- For parameters on the log or logit scale (via `partrans`), rw.sd applies to the transformed scale. A value of 2e-9 is still effectively zero on any transformed scale for typical epidemiological parameters, so the same diagnosis applies.
- If the project intentionally runs a "fixed-parameter evaluation" (no optimization) and explicitly states this, negligible rw.sd is not an error. Check whether the project describes the search as an optimization or as a parameter evaluation.
- Does not replace the full computational adequacy audit (Wheeler et al. 2024, item 6); this skill focuses specifically on the negligible-rw.sd failure mode, as distinct from the large-rw.sd failure mode covered by `pomp-rw-sd-magnitude-error`.
