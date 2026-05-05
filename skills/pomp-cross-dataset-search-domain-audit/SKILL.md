---
name: pomp-cross-dataset-search-domain-audit
description: Use when reviewing a pomp project that fits the same model structure to two or more distinct time series (e.g., separate disease variants, geographic regions, or time periods) using a shared global-search starting-point box, to detect the silent error where the common box fails to cover the MLE for one or more datasets — causing the optimizer to extrapolate outside the design region and producing unreliable parameter estimates for those datasets.
---

# pomp Cross-Dataset Search Domain Audit

## Purpose

When the same mechanistic model is fit separately to multiple time series (different disease variants, locations, or periods), students frequently reuse the same global-search starting-point box for all datasets. If the true MLE for one dataset lies outside the shared box, the global search for that dataset produces starting points that are all on the same side of the optimum. The optimizer may still find a good value by extrapolating from the best `mif2` run (`mf1 <- mifs_local[[1]]`), but the search is no longer "global" in the intended sense: all 100+ random starting points are systematically displaced from the true optimum, and the optimizer's ability to find the MLE depends on luck and the quality of the local-search seed rather than on a properly designed global search.

This error is silent: the code runs, the global search produces a valid-looking pairs plot and a top-k parameter table, and the MLE is reported in the text. The problem is only detectable by comparing the reported MLE to the stated search bounds.

## When to Activate

Use this skill when:
- A pomp project fits the same model structure to two or more distinct time series and labels them as separate analysis targets (e.g., two disease variants, two countries, two time periods).
- The global-search starting-point box (`runif_design` bounds or equivalent) is defined once and used for all datasets, or the bounds are defined separately but are identical or nearly identical across datasets.
- The reported MLE for at least one dataset falls outside the stated search bounds for one or more parameters.

Do not use this skill when each dataset's starting-point box is individually tailored based on exploratory analysis of that dataset. This skill specifically addresses shared-box reuse across datasets with potentially different parameter scales.

## Procedure

### 1. Enumerate all datasets and their separate model fits

Identify every time series being fit and the corresponding model object, local-search result, and global-search result. For each, record:
- The dataset name and time span.
- The local-search starting parameters (from `pomp(..., params=c(...))` or equivalent).
- The global-search box: `lower` and `upper` bounds in `runif_design(lower=..., upper=...)`.
- The best global-search MLE and its log-likelihood.

### 2. Check whether the global-search box covers the MLE for each dataset

For each dataset and each estimated parameter:
- Compare the MLE value to the `lower` and `upper` bounds.
- If MLE < lower or MLE > upper: flag as an out-of-box MLE. The global search for this dataset was not sampling near the true optimum.
- Note: the MLE can fall outside the box if the `mf1` base object (from local search) carries parameter values that IF2 refines beyond the starting-point range. Flag this pattern explicitly — the global search is functioning as an extended local search, not a true global search.

### 3. Assess the consequence for parameter estimates and comparisons

For each out-of-box MLE:
- State which parameter is out of range and by how much (e.g., "MLE Beta = 389 but box upper = 100, a factor of ~4 outside the search region").
- Assess whether the global search is effectively sampling a different region of parameter space than the optimum. If all 100 starting points are concentrated in Beta ∈ [1, 100] while the true optimum is at Beta = 389, only the local-search seed at Beta ≈ 224 (from the local search) is near the optimum, and the global search provides essentially no new information for this dataset.
- Identify whether any downstream conclusions (parameter comparisons across datasets, profile likelihoods) depend on the problematic dataset's estimates. If so, escalate to a major issue.

### 4. Check whether the profile likelihood box inherits the search domain problem

When profile likelihoods are computed after a global search, the nuisance-parameter box for the profile is often derived from the filtered global-search results (e.g., `sapply(range, ...)` over rows with loglik > max - 10). If the global search was dominated by the local-search seed rather than the random starting points, this box will be artificially narrow and centered on the local seed's parameter values. Check:
- Whether the profile nuisance-parameter box is derived from the global-search results.
- Whether those results are dominated by the local-search seed (check if the top-k rows from the global search all have similar parameter values to the local-search MLE, rather than spanning the global-search box).

### 5. Propose corrected search boxes

For each dataset with an out-of-box MLE:
- Recommend constructing the starting-point box by (a) running a pilot local search, (b) inspecting the convergence traces, and (c) setting the global-search box to be at least 2-3x wider than the local search's apparent convergence range, centered on the local-search MLE.
- Alternatively, recommend running the global search on the log or logit scale of parameters, where the natural range is more uniform across datasets.
- For cross-dataset comparisons, recommend verifying that each dataset's global search is genuinely sampling near its optimum before comparing MLEs.

### 6. Check log-likelihood comparability across datasets

When comparing log-likelihoods across datasets with different time spans or different numbers of observations:
- Log-likelihoods are not directly comparable across datasets of different length: a dataset with twice as many observations will produce approximately twice the log-likelihood (in magnitude) even for equally good fits.
- Verify whether the text makes direct numerical comparisons of log-likelihoods across datasets. If so, flag as an invalid comparison — the correct quantity for comparing fit quality across datasets of different size is the per-observation log-likelihood (total log-likelihood divided by number of observations) or a proper information criterion.

## Limitations

- This skill requires knowing the MLE for each dataset, which is only available if the global-search results are archived in RDS or CSV files that can be read. If results are not archived, the audit must rely on values reported in the rendered document.
- A large out-of-box MLE may still represent a reliable estimate if the local-search seed happened to start near the true optimum and IF2 converged there from a single starting point. However, this cannot be verified without replicate global searches, and the reliability of a single-seed estimate is always lower than a properly designed multi-start search.
- This skill addresses the experimental design of the global search, not the quality of the IF2 optimization within each starting point. Even a well-designed global search box can fail to find the MLE if Np or Nmif are too small — that is covered by `pomp-if2-hyperparameter-audit`.
- For models with high-dimensional parameter spaces (more than 6-8 estimated parameters), the global search box problem is harder to diagnose from a simple MLE-vs-bounds comparison, because the MLE is a point in a high-dimensional space and may appear within bounds on marginal projections while being outside the box in joint space.
