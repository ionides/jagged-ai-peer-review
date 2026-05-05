---
name: pomp-profile-domain-audit
description: Use when reviewing a pomp project that runs a profile likelihood after a global search that reveals multimodality, to detect the silent error where the profile_design domain covers only one likelihood mode — producing a Wilks confidence interval that appears statistically valid but is actually conditional on a single basin and omits one or more alternative parameter regimes.
---

# pomp Profile Domain Audit

## Purpose

When a global IF2 search reveals multimodality (multiple distinct parameter combinations achieving similar log-likelihoods), the profile likelihood for a key parameter must span the full feasible range, including all identified modes. A recurring student error is to select the profile domain by inspecting global search results — e.g., `filter(logLik > max(logLik) - 10)` to define the `lower` and `upper` bounds for nuisance parameters — and then to profile the target parameter over only the range where one mode lives. The `profile_design` call and the Wilks cutoff are applied correctly within the truncated domain, so the code produces no error. The rendered CI looks precise. But it is a conditional CI: it characterizes uncertainty within one mode and says nothing about whether the other mode(s) are ruled out at the 95% level.

This error is more insidious than the wrong-variable error detected by `pomp-profile-design-audit` because the mechanics are all correct — only the choice of domain is wrong.

## When to Activate

Use this skill when:
- A pomp project's global search (or pairwise geometry plots, or convergence traces) reveals two or more distinct parameter clusters achieving log-likelihoods within, say, 10 units of the global maximum.
- The project subsequently runs a profile likelihood for a parameter whose MLE differs substantially between the identified modes.
- The profile domain for the target parameter does not extend to cover all modes.

Common trigger pattern: global search shows rho converging to two clusters (e.g., ~0.12 and ~0.90), but `profile_design(rho = seq(0.01, 0.50, length=30), ...)` covers only the low-rho mode.

Do not use this skill when the global search shows convergence to a single mode — in that case a well-chosen profile domain covering the neighborhood of the MLE is sufficient. This skill is specifically for the multimodal case.

## Procedure

### 1. Identify multimodality in the global search

Examine the global search results: convergence trace plots, pairwise geometry scatter plots, and the top-k parameter table. Ask:
- Do the top log-likelihoods cluster at two or more parameter combinations that are not simply due to label switching or periodicity?
- Does the target parameter (the one being profiled) take qualitatively different values across those clusters?
- Does the text acknowledge or explain the multimodality?

Record all identified modes: for each, note the approximate value of the profiled parameter and the log-likelihood.

### 2. Check the profile domain against all identified modes

Find the `profile_design(param = seq(lo, hi, length=n), ...)` call. Record `lo` and `hi`.

For each mode identified in Step 1:
- Does the value of the profiled parameter in that mode fall within [lo, hi]?
- If a mode has the profiled parameter outside [lo, hi], it is excluded from the profile. Flag this as a domain truncation error.

### 2b. Check whether the profile optimizer is initialized from the correct mode

Even when the profile parameter range nominally covers the global MLE, the profile may still be mode-conditional if the nuisance parameter optimizer is initialized from a local-search result rather than from global-search solutions.

Examine the `mif2(...)` call inside the profile loop:
- Is the base pomp object (the first argument) a local IF2 result such as `if1[[1]]`? If so, the optimizer starts from the local mode at every profile slice, even when the profiled parameter is at a value where the global mode is the relevant optimum.
- Is the `start` or `params` argument constructed from global search rows? If not, flag as a mode-conditional initialization error.

Common pattern triggering this error:
```r
mif2(if1[[1]],  # local search result used as base
     start = c(unlist(guesses[i,]), params_test),  # nuisance params from local mode
     ...)
```
Here `guesses` may span the correct phi range, but the nuisance parameters seeded from `params_test` or `if1[[1]]` anchor the optimizer near the local mode.

**Fix:** Initialize profile optimization at each profile slice from the global search row whose profiled-parameter value is closest to the current slice, rather than from a fixed local-search result.

### 3. Check whether the nuisance-parameter box covers all modes

The `lower` and `upper` arguments to `profile_design` constrain the nuisance parameters at each profile slice. If these bounds are derived from a filtered subset of the global search (e.g., `filter(logLik > max(logLik) - 10)`), and if one mode is excluded by this filter, then the nuisance-parameter optimizer cannot reach the excluded mode even at profile points where it would be relevant.

Trace how `lower` and `upper` are constructed:
- If they are derived from `range()` or `sapply(range)` applied to a filtered data frame, verify that all modes are represented in the filtered rows.
- If one mode's nuisance parameters fall outside the box, profile optimization at the corresponding profile-parameter values will converge to the wrong nuisance optimum.

### 4. Assess validity of the reported confidence interval

If any identified mode is outside the profile domain:

- The reported CI covers only the mode(s) within the domain. It is a conditional CI, not a marginal CI for the parameter.
- State the approximate log-likelihood of the excluded mode relative to the global maximum. If the difference is less than `0.5 * qchisq(0.95, df=1)` ≈ 1.92 units, the excluded mode is within the 95% Wilks region and the reported CI is missing a portion of the confidence set. If the difference is greater than 1.92 units, the excluded mode is ruled out at the 95% level and the CI is valid despite the truncation — but this must be verified, not assumed.
- Propose extending the profile domain to include all modes, or explicitly computing the likelihood at the excluded mode's parameter values to confirm it is outside the 95% confidence set.

### 5. Check for periodicity artifacts

Some parameters — particularly phase parameters (e.g., Phi in a seasonal contact rate) and parameters with support on a circle — produce artifactual multimodality because multiple values yield identical dynamics. Common examples:
- Phase Phi in `cos(2*pi*t/52 - Phi)` is periodic with period 2*pi; values Phi and Phi + 2*pi are identical.
- A parameter constrained to (0, 1) may appear bimodal near 0 and 1 due to boundary effects.

If multimodality is due to periodicity, document this, but note that the profile domain still must cover all non-redundant values. Reparameterizing to remove the periodicity is the preferred fix.

### 6. Summarize findings

For each domain truncation error:
- Quote the `profile_design` call with its `seq` bounds.
- Identify which mode is excluded and at what parameter value.
- Compute `max(globalLogLik) - logLik_excluded_mode` and compare to 1.92 to determine whether the excluded mode is inside or outside the 95% confidence set.
- State whether the reported CI is: (a) fully valid (excluded mode is outside the 95% set), (b) potentially invalid (excluded mode is near or within the 95% set), or (c) definitively invalid (excluded mode was never evaluated and its log-likelihood is unknown).
- Propose the corrected profile range.

## Limitations

- This skill requires that multimodality be visible in the global search output. If the global search is insufficiently dense and a second mode is missed entirely, this skill cannot detect it — the underlying problem is then computational inadequacy (covered in `guided-pomp-review` and `pomp-if2-hyperparameter-audit`).
- Determining whether an excluded mode is within the 95% Wilks set requires evaluating the likelihood at that mode. If the profile was never run there, this value is unknown and must be obtained by running additional particle filter evaluations.
- The Wilks approximation itself may be unreliable when the likelihood surface is irregular (non-quadratic near the MLE). This is a separate issue from domain truncation but is often co-present when multimodality occurs.
- Some apparent multimodality reflects parameter collinearity (a ridge), not true distinct modes. A ridge extending along a direction in parameter space looks bimodal in 2D projections (pairwise plots) but is not truly bimodal. Distinguish ridges (continuous paths of near-optimal likelihood) from distinct modes (separated by a likelihood valley) before applying this skill.
