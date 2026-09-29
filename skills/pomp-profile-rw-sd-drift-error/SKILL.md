---
name: pomp-profile-rw-sd-drift-error
description: Detect the anti-pattern of including the profiled parameter in rw.sd during a POMP profile likelihood IF2 search, which allows the parameter to drift away from its profile-grid value and renders the resulting profile curve and confidence interval invalid — use when reviewing a POMP project that constructs a profile likelihood via IF2 with a shared rw.sd definition.
---

# POMP Profile Likelihood rw.sd Drift Error Detector

## Purpose

A correct POMP profile likelihood over a target parameter (e.g., `rho3`) requires that parameter to be held fixed at each profile-grid value throughout the IF2 optimization. This is achieved by setting the parameter's `rw.sd` entry to zero in the profile mif2 call. A common error occurs when the profile mif2 call reuses the same `rw.sd` object defined for the global or local search, which assigns a non-zero perturbation to the profiled parameter. The parameter is then free to drift during IF2 iterations, producing a result that is not a profile likelihood — it is merely another unconstrained search seeded near the grid values. The saved artifact will contain far more unique values of the target parameter than the number of profile-grid points, and the resulting confidence interval is invalid.

This error is distinct from the profile-indexing error (wrong result object in pfilter step) and the profile-guess-stratification error (wrong `group_by` parameter at guess construction): those errors occur in a different stage of the profile workflow. This error occurs in the mif2 call itself.

## When to Activate

Use this skill when:
- A POMP project defines a `params_rw.sd` or `rw_sd(...)` object for the local/global IF2 search.
- A profile likelihood is computed by calling `mif2(..., rw.sd = params_rw.sd)` (or equivalent) where `params_rw.sd` is the same object used for the non-profile searches.
- The target parameter of the profile receives a non-zero `rw.sd` entry in `params_rw.sd` for at least some time points.

Do not use this skill when:
- The profile mif2 call constructs a separate `rw.sd` object that explicitly sets the profiled parameter's perturbation to zero.
- The project uses a deterministic skeleton and profile over a fixed parameter via `trajectory()` or `traj_objfun()`, where `rw.sd` does not apply.
- The project has only one `rw.sd` object and the profiled parameter is provably zero in it (e.g., the parameter was fixed in the original model and thus absent from `rw.sd`).

## Procedure

### 1. Identify the profiled parameter

Read the profile likelihood section to determine which parameter is the target (e.g., `rho3`, `beta`, `mu_IR`). Call it the **target parameter**.

### 2. Locate the rw.sd definition used in the profile mif2 call

Find the `mif2(...)` call inside the profile loop. Note the `rw.sd =` argument. Determine whether it is:
- A newly constructed `rw_sd(...)` object specific to the profile, or
- The same `rw.sd` object (`params_rw.sd`, `mf_rw.sd`, etc.) used in the local or global search.

### 3. Check whether the target parameter has a non-zero perturbation

In the `rw.sd` object, locate the entry for the target parameter. It may be time-varying (e.g., `rho3 = ifelse(week_num >= 125, 0.02, 0)`). Flag any case where the perturbation is non-zero for any time point.

- **Correct pattern**: `rw.sd = rw_sd(..., rho3 = 0, ...)` — perturbation explicitly set to zero for the profiled parameter.
- **Error pattern**: `rw.sd = params_rw.sd` where `params_rw.sd` contains `rho3 = ifelse(..., 0.02, 0)` — non-zero perturbation allowed during profile optimization.

### 4. Confirm the drift by inspecting the saved profile artifact

If the profile results are saved as an RDS or CSV file, load the artifact and check the number of unique values of the target parameter:

```r
prof <- readRDS("profile_results.rds")
cat("Unique target-parameter values:", length(unique(prof$rho3)), "\n")
cat("Expected (= number of profile grid points):", nrow(profile_design_grid), "\n")
```

If the number of unique values far exceeds the number of profile-grid points, the parameter drifted.

### 5. Assess the impact on the confidence interval

Because the target parameter is free to optimize, the profile curve reflects an unconstrained search rather than a profile. The confidence interval derived from this curve is not a profile-likelihood CI and does not have the correct coverage. Additionally, the reported CI bounds may be artificially wide or narrow depending on how the optimizer moved the parameter relative to the grid values.

### 6. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) of the profile mif2 call.
- The specific `rw.sd` entry that is non-zero for the profiled parameter.
- The consequence: the profile likelihood is invalid; reported confidence interval does not reflect the profile-likelihood CI.
- The fix: modify the profile mif2 call to use a `rw.sd` object in which the target parameter's perturbation is set to zero (e.g., add `rho3 = 0` to the `rw_sd(...)` call, or construct a separate profile-specific `rw.sd`).

## Limitations

- This skill requires reading the source code; the rendered profile plot may look visually plausible even when the parameter has drifted (the points may appear distributed across the profile axis because the optimizer found nearby values).
- If the target parameter receives a non-zero perturbation only for a small subset of time points (e.g., one out of 212 weeks), the practical impact may be small but the error is still present and should be flagged.
- Does not cover errors where the profiled parameter is fixed via `fixed_params` in a way that overrides `rw.sd`; that is the correct behavior and not an error.
- Does not replace the profile-indexing error check (`pomp-profile-indexing-error`) or the profile-guess-stratification check (`pomp-profile-guess-stratification-error`); all three should be applied when reviewing a POMP profile likelihood.
