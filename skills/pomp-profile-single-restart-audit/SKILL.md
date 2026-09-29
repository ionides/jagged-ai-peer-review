---
name: pomp-profile-single-restart-audit
description: Detect cases where a POMP profile likelihood is computed using a single IF2 restart per grid point (starting from the MLE) with a single pfilter evaluation and the profile-maximum rather than the global-maximum as the CI reference, causing Monte Carlo noise to dominate the profile curve and CI bounds to be statistically invalid — use when reviewing a POMP project that constructs a profile by looping over a grid but runs only one mif2 and one pfilter call per grid point.
---

# POMP Profile Likelihood Single-Restart Audit

## Purpose

A correct POMP profile likelihood requires that at each profile grid value for the target parameter, the optimizer finds the **constrained maximum** over all other parameters. In practice, this requires multiple IF2 restarts from diverse starting points at each grid value (or use of `profile_design()` with a broad box). A common shortcut — especially in course-project contexts where students follow simplified homework examples — is to run a single IF2 chain starting from the current MLE for every grid point, then evaluate with a single `pfilter()` call. This approach has three compounding problems:

1. **Single restart from MLE**: Starting every profile point from the full MLE provides no diversity. If the constrained likelihood surface at a grid value distant from the MLE has a different shape, the single chain may fail to reach the constrained optimum, causing the profile to be artificially flat or to drop too steeply.

2. **Single pfilter evaluation**: A single particle filter evaluation introduces substantial Monte Carlo noise (~1–5 log-likelihood units for typical epidemic models). With only 10 grid points and no replicated evaluations, the profile curve is dominated by noise rather than signal, and CI bounds computed via `which(loglik >= cutoff)` are sensitive to individual noisy evaluations.

3. **CI reference uses profile maximum instead of global maximum**: The chi-squared CI cutoff should be `global_max_loglik - 0.5 * qchisq(df=1, p=0.95)`. Using the profile maximum instead (as done when computing `max(profile_amp$loglik) - qchisq(0.95,1)/2`) is valid only if the profile maximum equals the global maximum within Monte Carlo error. If the profile was seeded from a suboptimal starting point or has noise, this condition fails silently.

This error pattern is distinct from the other profile failure modes:
- `pomp-pseudo-profile-audit`: no profile IF2 search was run at all
- `pomp-profile-rw-sd-drift-error`: the profiled parameter is not fixed in rw.sd
- `pomp-profile-guess-stratification-error`: wrong group_by at guess construction
- `pomp-profile-indexing-error`: wrong result object in pfilter step
- `pomp-profile-pre-global-seed-error`: CSV contains only pre-global results
- `pomp-profile-range-misalignment`: grid range excludes global MLE

Here, the profile IF2 search is structurally correct (profiled parameter excluded from rw.sd, grid constructed over the target parameter), but the computational execution is inadequate: one restart, one evaluation.

## When to Activate

Use this skill when:
- A POMP project defines a profile likelihood via a for-loop (or foreach loop) over a grid of fixed parameter values.
- Inside the loop, there is exactly one `mif2()` call per grid point (no inner loop over multiple restarts).
- The `mif2()` starting parameters are drawn from a single point (typically `MLE_params` with the profiled parameter overwritten), not from a diverse box.
- The log-likelihood evaluation inside the loop is a single `pfilter()` call (not `logmeanexp` over multiple replicates).
- The CI cutoff is computed as `max(profile_loglik) - 0.5 * qchisq(df=1, p=0.95)` using the profile maximum, not the global search maximum.

Do not use this skill when:
- The profile loop contains an inner loop over multiple restarts from diverse starting points at each grid value.
- The log-likelihood is evaluated via `logmeanexp(replicate(K, logLik(pfilter(...))), se=TRUE)` with K >= 5.
- The project uses `profile_design()` and seeds IF2 from a high-likelihood box (the diversity comes from the box, not the single point).
- The profile is explicitly described as a diagnostic illustration only, with no CI claimed.

## Procedure

### 1. Locate the profile loop

Search the Rmd/R source for a for-loop or foreach loop with a grid variable (e.g., `amp_grid`, `beta_grid`, `seq(lower, upper, length.out=N)`). Identify what is stored per grid point.

### 2. Count the number of mif2 calls per grid point

Inside the loop body, count how many `mif2()` calls are made. If exactly one, flag as potential single-restart issue.

### 3. Identify the starting parameters for mif2

Determine what `params=` is passed to the `mif2()` call:
- **Single-restart pattern**: `params_prof <- MLE_params; params_prof[target] <- grid[i]; mif2(..., params=params_prof)` — all restarts start from the MLE, just with the target parameter forced to the grid value.
- **Multi-restart pattern**: Starting parameters drawn from a box or from diverse high-likelihood rows of a previous global search.

### 4. Count pfilter calls per grid point

Identify whether the log-likelihood evaluation is:
- A single `logLik(pfilter(..., Np=K))` call — flag as noisy single evaluation.
- `logmeanexp(replicate(J, logLik(pfilter(...))), se=TRUE)` with J >= 5 — this is adequate.

### 5. Check the CI reference point

Locate the cutoff computation: `cutoff <- max(profile_loglik) - 0.5 * qchisq(df=1, p=0.95)`.
- If `max(profile_loglik)` is the maximum within the profile results, check whether it matches the global search maximum (within a few log-likelihood units of Monte Carlo error, typically < 2).
- If the profile maximum is more than ~3 units below the global maximum, flag the CI reference as incorrect.

### 6. Assess the impact on reported CIs

Identify any "singleton" CIs (where the CI collapses to a single grid point) or unusually narrow CIs (spanning fewer than 2 grid intervals) as likely artifacts of Monte Carlo noise rather than genuine precision. A singleton CI on a 10-point grid is almost always caused by a single noisy pfilter evaluation being above the cutoff while its neighbors are not — this has no statistical interpretation.

### 7. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) of the profile loop.
- The number of restarts per grid point (expected: 1, flagged).
- Whether pfilter is replicated (expected: no, flagged).
- Whether the CI reference uses profile max vs. global max.
- The consequence: Monte Carlo noise dominates the profile; singleton or narrow CIs are artifacts; reported CIs are not valid profile-likelihood CIs.
- The fix: Use `profile_design()` seeded from a high-likelihood box, run multiple IF2 restarts per grid value, evaluate log-likelihood via `logmeanexp` over >= 10 replicates, and apply the chi-squared cutoff against the global search maximum.

## Limitations

- This skill detects the single-restart pattern from code structure alone; it cannot determine whether the single restart happened to find the constrained optimum in a specific case (which would reduce the practical severity).
- If the global search was also very sparse (e.g., 10 replicates), the "global maximum" reference point may itself be unreliable — in that case, both the global search and the profile need more computation.
- Does not replace other profile failure mode checks; all applicable skills should be applied when reviewing a POMP profile likelihood.
- In rare cases where the likelihood surface is very smooth and unimodal, a single restart from the MLE may be adequate — but this cannot be verified without additional diagnostics and should still be flagged.
