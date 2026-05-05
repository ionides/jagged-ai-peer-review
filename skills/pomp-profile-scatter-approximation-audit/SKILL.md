---
name: pomp-profile-scatter-approximation-audit
description: Use when a pomp project displays a profile likelihood plot by filtering high-likelihood points from a global search result rather than running a dedicated profile_design + foreach-mif2 sweep — a silent error that produces a visually plausible but statistically invalid profile and confidence interval.
---

# pomp Profile Scatter Approximation Audit

## Purpose

A recurring student error is approximating a profile likelihood by filtering global-search results to high-likelihood points, then plotting those points against the parameter of interest and drawing a Wilks threshold line. This produces a figure that looks like a profile likelihood but is not: the points are not constrained to optimize over nuisance parameters at each fixed value of the profiled parameter, the coverage of the profiled parameter's range is uncontrolled, and the Wilks CI derived from this scatter is statistically invalid. Because the error produces a plausible-looking plot without any runtime warning, it can pass unnoticed in peer review.

## When to Activate

Use this skill when:
- A pomp project shows a plot of loglik vs. a single parameter (e.g., rho, eta, mu_IR) with a horizontal Wilks threshold line and reports a CI from the intersection.
- The code producing this plot reads from a global-search results file (e.g., `read.csv("writeup_params.csv")`) rather than from a separate profile results file.
- The code includes `filter(loglik > max(loglik) - 10)` or similar before plotting, rather than grouping by fixed values of the profiled parameter.
- No `profile_design(...)` call appears in the document for the parameter being profiled.

Do not activate if the document contains an explicit `profile_design(param=seq(...))` call and a corresponding foreach-mif2 loop — that is a valid profile structure (evaluate it with `pomp-profile-design-audit` instead).

## Procedure

### 1. Identify the profile likelihood plot

Find every plot that displays loglik on the y-axis and a single parameter on the x-axis with a Wilks threshold line. Record:
- Which parameter is on the x-axis.
- Which data source is read for the plot (file name or object name).
- Any filter applied before plotting (e.g., loglik > max(loglik) - 10).

### 2. Trace the data source

Follow the data source back to its origin:
- If it comes from the same file used for the global search (e.g., `writeup_params.csv` also used for the pairs plot of global search results): this is a scatter-approximation profile. Flag immediately.
- If it comes from a separate file clearly labeled as profile results (e.g., `profile_rho.rds`, `profile_results.csv`): look for the `profile_design` call that generated it.

### 3. Verify profile_design is used (or absent)

Search the document for `profile_design(...)`:
- If absent: the profile is being approximated from scatter. Flag as a major error.
- If present: confirm it is called for the same parameter shown in the profile plot, and that the foreach-mif2 loop iterates over the profile design object (not the global search design). If the design object is present but the loop iterates over the wrong object, apply `pomp-profile-design-audit` instead.

### 4. Assess the consequence

For a scatter-approximation profile:
- The x-axis coverage of the profiled parameter is not systematic — the CI endpoints depend on where the global search happened to place high-likelihood points.
- Nuisance parameters are not re-optimized at each fixed value of the profiled parameter; they are simply whatever the global search found. This typically inflates the profile (makes it appear wider than the true profile) but can also create spurious narrow intervals if the global search concentrated near the MLE.
- The Wilks approximation requires that the profile is computed at the MLE of nuisance parameters for each fixed profiled-parameter value. Scatter approximation violates this requirement.
- Report: "The profile likelihood for [param] is approximated by filtering global-search points rather than by a profile_design sweep. The reported CI is not a valid profile CI."

### 5. Propose the correct implementation

Outline the corrected workflow:
1. Call `profile_design(param = seq(lower, upper, length = 40), lower = c(...), upper = c(...), nprof = 10)` to create a grid of starting points with param fixed at each profile value.
2. Run `foreach(guess = iter(profile_design_object, "row"), ...) %dopar% { mif2(params = c(unlist(guess), fixed_params), rw.sd = rw.sd_without_param, ...) }` — note that the profiled parameter should not appear in rw.sd.
3. Evaluate log-likelihood at each profile point with pfilter replicates.
4. Plot max loglik at each fixed param value vs. param, with a Wilks threshold.

## Limitations

- This skill cannot detect when a scatter approximation happens to give a numerically similar result to a proper profile — it flags the methodological error regardless of numerical outcome.
- For simple, well-identified models, the scatter approximation may produce an interval that is qualitatively similar to the true profile CI. The error is still present and should be noted, but the reviewer may choose to weight it as minor if the global search was well-executed and dense.
- This skill does not evaluate whether the profile's parameter range is appropriate or whether the Wilks approximation itself is valid for the model — those require separate assessment.
