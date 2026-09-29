---
name: pomp-simdata-benchmark-error
description: Detect the anti-pattern of evaluating an initial particle-filter likelihood on a simulated pomp object (e.g., sim1.filt) instead of the real-data pomp object, and then presenting that value alongside IF2-search likelihoods on real data as if they are comparable benchmarks — use when reviewing a POMP project that follows a teaching-template workflow with a separate simulation object.
---

# POMP Simulated-Data Benchmark Error Detector

## Purpose

POMP teaching examples and course templates commonly construct two pomp objects: one for filtering real data (`data_filter`) and one for filtering a simulated dataset (`sim1.filt`). The simulated object is used to verify that the particle filter runs before committing to expensive IF2 optimization. A recurring student error is to report the log-likelihood from the simulated-data particle filter run as if it were a benchmark for the real-data model, then compare it numerically to IF2 log-likelihoods that were computed on the real-data object. Because the simulated and real datasets are different, the two log-likelihood values are on completely different scales and cannot be compared.

This error manifests as an anomalous numerical discrepancy — often thousands of log-likelihood units — between the "initial benchmark" value and the IF2 search results, with no explanation provided in the text.

## When to Activate

Use this skill when:
- A POMP project constructs a simulated pomp object (e.g., via `simulate()` followed by `pomp(sim1.sim, covar=..., rprocess=rproc.filt, ...)`) and evaluates `pfilter()` on it.
- The project reports the resulting log-likelihood as an "initial benchmark" or starting point for comparison with IF2-search results.
- The reported initial benchmark log-likelihood and the IF2-search log-likelihoods differ by an unusually large amount (e.g., more than a few hundred units, or have opposite signs).

Do not use this skill when:
- The project explicitly labels the initial particle filter run as a check on simulated data (not a benchmark on real data).
- The initial particle filter and the IF2 search both use the same data object.
- The discrepancy is explained in the text (e.g., "we first evaluate on simulated data to verify the filter, then evaluate on real data").

## Procedure

### 1. Identify the initial particle filter call

Search the Rmd/R source for the first `pfilter()` call outside of an IF2 loop. Note the pomp object passed as its first argument.

### 2. Trace the object's origin

Determine whether the object passed to `pfilter()` is:
- The real-data pomp object (constructed from actual observations), or
- A simulated pomp object (constructed by passing `sim1.sim` or equivalent to `pomp()` and overriding `rprocess` with the filter process).

If the object was created from a `simulate()` call, flag it as a candidate for this error.

### 3. Check whether the reported log-likelihood is presented as a real-data benchmark

Read the narrative surrounding the particle filter result. Determine whether the text:
- Describes the value as an "initial benchmark," "starting point," or "reference value" for the model on the real data.
- Compares the value directly to IF2-search log-likelihoods without acknowledging the different datasets.

If yes, flag the discrepancy.

### 4. Compute the expected sign and magnitude

Approximate the expected log-likelihood for the real data at reasonable parameter values. For a daily financial log-return series of length N under a Gaussian measurement model, the log-likelihood should be approximately −N/2 × log(2π) − N/2, which is negative and on the order of −N. A reported value that is positive or has the wrong order of magnitude relative to −N is a strong indicator of dataset substitution.

### 5. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line).
- The likely cause: the particle filter was evaluated on a simulated dataset, not the real data.
- The consequence: the reported "benchmark" is not on the same scale as the IF2-search results; the comparison is invalid.
- The fix: re-run the initial particle filter on the real-data pomp object (e.g., `AAPL_filter`) at the test parameters, and report that value as the baseline.

## Limitations

- Cannot be detected purely from the saved artifact; requires reading the source code to identify which object is passed to `pfilter()`.
- In some projects the simulated-data pfilter and real-data IF2 results are on similar scales by coincidence; magnitude checks alone are insufficient — the object provenance must be traced.
- Does not apply to projects that compute both a simulated-data diagnostic run and a real-data run and present them separately; only the misrepresentation of the simulated-data result as a real-data benchmark is the error.
