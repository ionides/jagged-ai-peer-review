---
name: pomp-rw-sd-magnitude-error
description: Detect cases where a POMP IF2 search sets rw.sd perturbation sizes equal to or proportional to parameter starting values rather than to appropriate uncertainty scales, causing parameter diffusion instead of convergence — use when reviewing a POMP project whose rw.sd values match the params starting values.
---

# POMP rw.sd Magnitude Error Detector

## Purpose

The `rw.sd` argument in `mif2()` controls the standard deviation of the random-walk perturbations applied to each parameter at each IF2 iteration. A common error is to copy parameter starting values directly into `rw.sd`, producing perturbation sizes equal to (or a fixed fraction of) the parameter's initial magnitude. For parameters on large scales (e.g., `home_court_avd = 40`, `beta = 500`), this produces perturbation SDs that are so large relative to the likelihood surface that the IF2 chain diffuses across the entire parameter space rather than converging to the MLE. Convergence traces appear flat and noisy throughout, and the reported "converged" log-likelihood may reflect a random walk through the parameter space rather than a genuine optimum.

This error is distinct from:
- `pomp-global-search-init-audit`: that skill handles the wrong first argument to mif2 (previous mif2 result vs. pomp object)
- `pomp-global-search-param-override-bug`: that skill handles duplicate-name c() concatenation
- `pomp-global-search-box-misalignment`: that skill handles box ranges that exclude the MLE
- `pomp-profile-rw-sd-drift-error`: that skill handles non-zero rw.sd for the profiled parameter

Here the issue is specifically that rw.sd values are set to the parameter starting magnitudes, producing perturbations far too large for stable convergence.

## When to Activate

Use this skill when:
- A POMP project defines `rw.sd = rw_sd(param1=v1, param2=v2, ...)` in an `mif2()` call.
- The values `v1`, `v2`, ... match or are proportional to the starting-parameter values used in `coef(pomp_object) <- c(param1=v1, ...)` or in a prior `simulate()` call.
- The convergence traces show flat, high-variance parameter chains that do not decrease from the starting values.

Do not use this skill when:
- The `rw.sd` values are small (e.g., 0.01–0.1 for unit-scale parameters) and clearly calibrated to the expected MLE uncertainty rather than to the parameter magnitude.
- The project explicitly states it used a warm-up run to calibrate rw.sd values from an empirical covariance matrix.
- The parameter is on a transformed (log or logit) scale and the rw.sd is appropriate for that scale.

## Procedure

### 1. Locate the rw.sd definition

Search the Rmd/R source for `rw_sd(` or `rw.sd = ` inside `mif2()` calls. Record all parameter-perturbation pairs.

### 2. Locate the starting-parameter definition

Find the `coef(pomp_object) <-` or `params = c(...)` block that precedes the mif2 call. Record the starting values for each parameter that appears in `rw.sd`.

### 3. Compare rw.sd values to starting-parameter magnitudes

For each parameter with a non-zero rw.sd entry:
- **Error pattern**: `rw.sd` value equals or is a substantial fraction (> 50%) of the starting-parameter value. Example: `coef <- c(beta1=0.5, home_court_avd=40, alpha=0.05)` followed by `rw.sd=rw_sd(beta1=0.5, home_court_avd=40, alpha=0.05)`.
- **Correct pattern**: `rw.sd` values are small relative to the parameter scale, typically 1–10% of the expected MLE value for that parameter (e.g., `rw.sd=rw_sd(beta1=0.02, home_court_avd=2, alpha=0.005)`).

Flag any case where the rw.sd value equals the starting value.

### 4. Inspect convergence traces

Examine the convergence trace plots for each parameter with the flagged rw.sd values:
- **Error signature**: Parameter traces are high-variance and flat from start to finish, with no visible decrease in variance or convergence to a stable value. The log-likelihood trace likewise shows large variance without a clear asymptote.
- **Correct signature**: Traces show high initial variance that decreases across iterations (as the cooling schedule reduces perturbations), converging to a stable region near the MLE.

If the traces are flat and noisy, confirm the rw.sd magnitude error is causing diffusion.

### 5. Assess the impact on reported MLE estimates

If large rw.sd values are confirmed:
- The IF2 cooling schedule reduces perturbations geometrically, so by the final iteration the perturbations may have shrunk to near zero regardless of the initial rw.sd. However, early iterations with very large perturbations can push parameters far from the starting point, and the cooling schedule may not bring them back to a good region.
- The reported "best log-likelihood" from the convergence traces may reflect a transient noisy visit to a high-likelihood region, not a stable MLE.
- Multiple chains may show very different final parameter values (high between-chain variance), indicating non-convergence.

### 6. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) of the `mif2()` call.
- The specific parameter-perturbation pairs where rw.sd equals the starting value.
- The consequence: parameter chains diffuse rather than converge; reported MLE values may not be near the true optimum.
- The fix: replace large rw.sd values with small calibrated values, typically 2–5% of the expected parameter range. Empirical calibration can be done by running a short pilot mif2 with moderate rw.sd values and setting final rw.sd to the empirical SD of the converged parameter distribution.

## Limitations

- This skill detects the error from code structure and trace plots. It cannot determine whether the large rw.sd caused the optimization to fail in a specific case — only that it is a likely cause of non-convergence when the traces are flat.
- For parameters on log or logit scale (via `partrans`), the rw.sd applies to the transformed scale. A large rw.sd on the log scale (e.g., 0.5) may be reasonable; this skill should be applied with awareness of which scale the perturbation operates on.
- If `cooling.fraction.50` is set very low (e.g., 0.01), the cooling schedule decays so quickly that even large initial rw.sd values shrink to near zero within a few iterations, partially mitigating the error. However, this also means the optimizer has very little time to explore, so it still fails — just for a different reason.
- Does not replace the full computational adequacy audit (Wheeler et al. 2024, item 6); this skill focuses specifically on the rw.sd calibration failure mode.
