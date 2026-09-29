---
name: pomp-profile-ci-direction-error
description: Detect cases where a POMP project reverses the profile likelihood CI inclusion direction — claiming that points above the chi-squared threshold line are problematic or outside the CI, when in fact points above the threshold are inside the 95% CI — use when reviewing a POMP project that plots a profile likelihood with a horizontal cutoff and makes a prose claim about which points are inside or outside the confidence interval.
---

# POMP Profile Likelihood CI Direction Error Detector

## Purpose

The standard POMP profile likelihood confidence interval (CI) for parameter θ consists of all values of θ for which the profile log-likelihood exceeds the cutoff:

```
max(logLik) - 0.5 * qchisq(df=1, p=0.95)
```

Points **above** this horizontal cutoff line are **inside** the 95% CI; points **below** the cutoff are **outside** the CI (i.e., excluded). A recurring student error is to invert this interpretation, describing points above the threshold as suspicious, cautionary, or indicative of a problem, and treating points below the threshold as the region of confidence. This error is invisible from the plot itself (the plot is drawn correctly) but appears in the prose interpretation surrounding the figure. Readers who trust the text without re-reading the formal definition will draw the opposite conclusion about which parameter values are supported by the data.

This error is distinct from:
- `pomp-loglik-direction-error`: that skill covers confusing "lower is better" vs. "higher is better" in model comparisons. Here the direction of model comparison is not the issue — the issue is specifically about the CI inclusion region relative to the threshold line.
- `pomp-pseudo-profile-audit`: that skill covers the absence of a genuine profile search. Here a profile was computed but its plot is misinterpreted.
- `pomp-profile-rw-sd-drift-error`, `pomp-profile-indexing-error`, etc.: those skills cover computation errors in the profile search. Here the computation may be correct; only the interpretation is wrong.

## When to Activate

Use this skill when:
- A POMP project displays a profile likelihood plot with a horizontal red (or colored) cutoff line drawn at `max(logLik) - 0.5 * qchisq(df=1, p=0.95)`.
- The surrounding prose makes a claim about which points (above or below the cutoff) are inside the 95% CI, or describes points above the cutoff as "cautionary," "problematic," or "uncertain."

Do not use this skill when:
- The prose correctly identifies the CI as the set of θ values with profile log-likelihood *above* the cutoff.
- The plot is labeled as a scatter plot rather than a profile likelihood and no CI interpretation is made.
- The project uses a different convention (e.g., a profile deviance plot where the axis is negated, so the CI is correctly below a cutoff).

## Procedure

### 1. Locate the profile likelihood plot and its interpretation

Search the rendered document and Rmd source for the code that plots profile log-likelihood against a parameter, with a horizontal cutoff line. Identify the surrounding prose sentences that describe the CI.

### 2. Identify the stated CI inclusion direction

Read the prose. Determine whether the text states or implies:
- **Correct pattern**: "the 95% CI consists of values for which the profile log-likelihood exceeds the cutoff" — or equivalent language indicating that the CI is above the threshold.
- **Error pattern**: "points above the threshold are concerning / cautionary / need caution" or "the CI is below the threshold" — indicating the CI is inverted.

### 3. Verify the cutoff computation in code

Confirm the cutoff formula:
```r
geom_hline(yintercept = max(results$logLik) - 0.5 * qchisq(df=1, p=0.95))
```
If the formula is correct (positive cutoff shift, not negative), then the horizontal line is in the right place and the error is purely interpretive.

### 4. Assess the impact on conclusions

Determine what parameter range is actually supported by the data (above the cutoff) and what range the text claims is supported (below the cutoff). If the parameter is near the boundary of the box (e.g., φ near 1), the correct interpretation may be that the CI is one-sided or unbounded above, while the incorrect interpretation may instead describe only the lower tail as supported.

### 5. Check for additional confusion with parameter scale

Verify that the profiled parameter is plotted on the correct scale (e.g., natural scale after `partrans`, not the logit-transformed internal scale). If the axis shows values outside the natural parameter range (e.g., φ < 0 when φ must be in (0,1) via logit transform), flag this as an additional error — it suggests the profiled parameter's transformed value is being plotted directly.

### 6. Report the finding

For each detected instance, report:
- The exact prose sentence(s) that invert the CI direction.
- The correct interpretation: the 95% CI for θ is the set of θ values for which the profile log-likelihood exceeds `max(logLik) - 0.5 * qchisq(df=1, p=0.95)`, i.e., points **above** the horizontal line.
- The consequence: any stated parameter range (e.g., "φ is bounded below by 0.95") may be incorrect — re-reading the plot with the correct interpretation may yield a different or uninformative CI.
- The fix: revise the prose to correctly state the CI direction, and restate which parameter values are included in (vs. excluded from) the confidence set.

## Limitations

- This skill detects interpretation errors in the prose; the plot itself may be correctly constructed. It cannot be triggered from plot inspection alone — the prose must be read.
- If the profile log-likelihood is essentially flat (all points above or all points below the cutoff), the CI direction error does not change the substantive conclusion (the CI is either everything or nothing). Flag the error regardless, but note the practical impact may be zero.
- Does not replace computational profile diagnostics (`pomp-profile-rw-sd-drift-error`, `pomp-profile-pre-global-seed-error`, etc.); all applicable profile checks should be run when reviewing a POMP profile likelihood.
- In some projects, the profile plot is drawn using a negated log-likelihood (profile deviance), in which case "below" the cutoff is correct. Confirm the axis label before applying this skill.
