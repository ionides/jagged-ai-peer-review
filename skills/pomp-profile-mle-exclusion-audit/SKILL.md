---
name: pomp-profile-mle-exclusion-audit
description: Use when a pomp project runs a structurally valid profile_design + foreach-mif2 sweep but the profiled parameter range is known or acknowledged to exclude the global MLE — producing a truncated profile that cannot support any confidence interval or identifiability conclusion, even though the code is mechanically correct and the plot appears well-formed.
---

# pomp Profile MLE Exclusion Audit

## Purpose

A profile likelihood is only statistically valid when the profiled parameter range contains the global MLE. A recurring failure mode occurs when the global search reveals that the MLE for a parameter is biologically implausible (e.g., a recovery rate of 150/day, or a transmission rate of 500), and the analyst responds by restricting the profile range to a biologically plausible subset (e.g., [0, 1]). The code is mechanically correct: `profile_design` is called, a foreach-mif2 sweep is run, a Wilks threshold line is drawn. But all profile points fall far below the global MLE log-likelihood, the threshold line lies above every plotted point, and no confidence interval can be read off. The analyst typically notes that the model is "misspecified" and moves on, but the profile has not contributed any evidence about identifiability — it has only confirmed that the model fits poorly when the parameter is constrained to the plausible range.

This failure mode is distinct from:
- Wrong design variable passed to iter() (covered by `pomp-profile-design-audit`)
- Domain truncation that excludes one mode in a multimodal landscape (covered by `pomp-profile-domain-audit`)
- Scatter approximation substituted for a real profile (covered by `pomp-profile-scatter-approximation-audit`)

The distinguishing feature here is that the truncation is acknowledged by the authors and motivated by biological plausibility rather than being an inadvertent error, yet the truncated profile is still reported as contributing meaningful evidence.

## When to Activate

Use this skill when:
- A pomp project runs a proper profile_design + foreach-mif2 sweep (mechanically correct code).
- The global search results show the MLE for the profiled parameter at a value outside the chosen profile range, or the text explicitly states that the optimizer prefers values outside the profiled range.
- The profile plot shows all points below the Wilks threshold, or the threshold is not visible in the plotted range.
- The authors interpret the result as confirmation of model misspecification rather than as a confidence interval.

Do not use this skill when the profile range covers the MLE and only a small number of points are below the threshold due to numerical noise.

## Procedure

### 1. Identify the global MLE for the profiled parameter

From the global search results (pairs plots, best_param table, or convergence traces), record:
- The value of the profiled parameter at the global MLE.
- The best log-likelihood achieved in the global search.

### 2. Identify the profile range

Find the `profile_design(param = seq(lo, hi, ...), ...)` call. Record lo and hi.

Ask: does the interval [lo, hi] contain the global MLE value from Step 1?

- If yes: the profile range is appropriate. This skill does not apply; evaluate with `pomp-profile-domain-audit` or `pomp-profile-design-audit` instead.
- If no: the profile range excludes the MLE. Continue to Step 3.

### 3. Assess the gap between the profile's best log-likelihood and the global MLE

From the profile results, identify `max(profile_loglik)`. Compare to `max(global_loglik)`. The difference `max(global_loglik) - max(profile_loglik)` measures how far below the global optimum the profile's best point lies.

- If the gap exceeds 5 log-likelihood units: the profile is operating in a region far from the optimum. Every profile point is well below the Wilks threshold and no confidence interval can be constructed. The profile is non-informative for identifiability.
- If the gap exceeds 50 units: the profile may be exploring a completely different likelihood mode or a degenerate region of parameter space. No meaningful inference is possible.

### 4. Evaluate what the truncated profile actually demonstrates

A profile restricted to a biologically plausible range, when the MLE is outside that range, demonstrates one of two things:

(a) **Model misspecification**: the model cannot achieve a high likelihood while constraining the parameter to plausible values, confirming that the model structure is wrong. This is a useful finding but it does not constitute a profile likelihood — it is a constrained likelihood evaluation.

(b) **Parameter confounding**: the plausible range for the parameter may interact with other parameters in ways that produce a flat or poorly defined constrained likelihood, masking whether the parameter is identifiable within the plausible range.

The reviewer should state which interpretation applies based on the shape of the profile within [lo, hi]: if the profile is flat (no clear maximum), it suggests (b); if it is monotone, it suggests (a).

### 5. State the consequence for reported conclusions

If the paper draws any inference from the truncated profile (e.g., "the parameter is poorly identified" or "the profile confirms misspecification"), evaluate whether that inference is supported:

- "The model is misspecified" is supported if the gap between the profile's best likelihood and the global MLE is large, and the global MLE is at a biologically implausible value. This conclusion does not require a valid profile — it follows from the global search alone.
- "The parameter is not identifiable within the plausible range" requires a profile restricted to that range, which is what was computed. This conclusion may be valid, but only if the profile optimizer successfully maximizes over nuisance parameters at each fixed value of the profiled parameter.
- "The confidence interval for the parameter is [a, b]" is not supported if the Wilks threshold line lies above all profile points. A confidence interval cannot be read off from a profile that never crosses the threshold.

### 6. Propose the correct analysis

Depending on the goal:

- **To assess model misspecification**: the global search result alone is sufficient. Report `max(global_loglik)` and compare to a benchmark. No profile is needed.
- **To assess identifiability within a constrained range**: reframe the analysis as a constrained likelihood profile and note that it characterizes the likelihood surface conditional on the parameter lying in [lo, hi]. Report the shape of this constrained profile (peak location, flatness) but do not draw Wilks confidence intervals.
- **To obtain a valid confidence interval**: restructure the model so that the MLE is biologically plausible (address the misspecification), then rerun the profile over a range that contains the revised MLE.

## Limitations

- This skill requires that the global MLE be identifiable from the output (global search results, best_param table, or convergence traces). If the global search itself is unconverged, the global MLE may not be reliably known.
- The distinction between model misspecification and parameter confounding (Step 4) is often ambiguous from the profile shape alone. Additional diagnostics (conditional log-likelihood plots, simulation checks) may be needed to distinguish them.
- This skill does not evaluate whether the model misspecification itself warrants major revision vs. minor revision. That judgment requires context about the scientific goals of the paper.
- When the profiled parameter has a hard physical upper bound (e.g., a probability must be in [0,1]) and the MLE lies at the boundary, this skill may misclassify a boundary MLE as an exclusion error. Check whether the MLE is at a constraint boundary before applying Step 3.
