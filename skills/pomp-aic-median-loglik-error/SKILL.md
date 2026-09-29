---
name: pomp-aic-median-loglik-error
description: Detect cases where a POMP project computes AIC using the median (or mean) log-likelihood across IF2 replicates instead of the maximum, producing an AIC value that is larger (worse) than the correct AIC and invalidating model selection conclusions — use when reviewing a POMP project that reports AIC alongside a summary() of log-likelihoods from a multi-replicate IF2 or pfilter search.
---

# POMP AIC Median Log-Likelihood Error Detector

## Purpose

AIC is defined as -2 * logLik + 2k, where logLik is the *maximum* log-likelihood (or its best estimate). In multi-replicate POMP IF2 searches, the analyst has access to a distribution of log-likelihood estimates across replicates — one per mif2 chain. A common error is to report the *median* (or mean) of this distribution in summary() output, then use that median value to compute AIC. Because the median is always less than or equal to the maximum for a set of non-identical values, the resulting AIC is inflated (worse) compared to the correct AIC based on the MLE. This makes the POMP model appear less competitive than it actually is relative to ARMA or GARCH baselines, and the reported AIC cannot be used for valid model selection.

This error is distinct from:
- `pomp-loglik-direction-error`: that skill covers directional misinterpretation (claiming "lower log-likelihood is better"). Here the direction of interpretation is correct, but the wrong summary statistic (median vs. max) is used.
- `pomp-placeholder-result-audit`: that skill covers fabricated values. Here the value is genuinely computed but is the wrong summary of the distribution.

## When to Activate

Use this skill when:
- A POMP project reports AIC for a stochastic model (one fitted via IF2 or pfilter with multiple replicates).
- The project uses `summary(r.if1$logLik)` or `summary(r.box$logLik)` to display log-likelihoods and then references the "median" value in the AIC computation.
- The AIC reported for the POMP model equals -2 * (median logLik from summary output) + 2k rather than -2 * max(logLik) + 2k.
- The AIC value for the POMP model is consistent with the median but not the maximum of the log-likelihood distribution (which can be verified if the summary statistics are shown).

Do not use this skill when:
- Only a single particle filter or IF2 run is performed and there is no distribution of log-likelihood estimates to summarize.
- The project correctly uses `max(logLik)` or the best log-likelihood from the search to compute AIC.
- The project uses `logmeanexp()` to compute the log-likelihood estimate (this is the correct Monte Carlo averaging approach for a single run with multiple particle filter replications, and is different from taking the median over multiple IF2 chains).

## Procedure

### 1. Locate the AIC computation for the POMP model

Search the Rmd/R source and conclusion text for explicit AIC computations for the POMP model. Identify the formula used: is it `-2 * logLik_value + 2 * k`?

### 2. Identify the log-likelihood value used in the AIC formula

Determine which specific value was used as `logLik_value`:
- Was it drawn from `summary(r.if1$logLik)` or `summary(r.box$logLik)`? If so, note whether the text references "median," "mean," "max," or "1st Qu." etc.
- Was it drawn from `max(r.box$logLik)` or `max(L.if1[,1])`?

### 3. Check consistency between stated value and summary statistics

If the project shows the full `summary()` output of log-likelihoods, extract the maximum and median from that output. Compute:
- Correct AIC: `-2 * max_logLik + 2 * k`
- Reported AIC: the value stated in the text

If the reported AIC matches `-2 * median_logLik + 2 * k` but not `-2 * max_logLik + 2 * k`, the error is confirmed.

### 4. Assess the magnitude of the error

Compute the discrepancy: `AIC_reported - AIC_correct = -2 * (median_logLik - max_logLik)`. Because median <= max for any set of values, the reported AIC is greater than or equal to the correct AIC. A discrepancy of more than 2 AIC units is practically significant for model selection. Larger discrepancies (e.g., > 10 units) could reverse model selection conclusions.

### 5. Check whether the error affects model selection conclusions

Determine which models are being compared. If the inflated AIC for the POMP model is still the best (lowest) among all candidates, the model selection conclusion is robust. If the inflated AIC makes the POMP model appear second-best to a simpler model (e.g., GARCH), re-computing with the correct AIC might reverse the conclusion.

### 6. Report the finding

For each detected instance, report:
- The code location or prose statement where the median log-likelihood was used in AIC computation.
- The correct AIC value based on `max(logLik)`.
- The magnitude of the discrepancy.
- Whether the model selection conclusion (best model by AIC) is affected.
- The fix: replace `median(r.box$logLik)` with `max(r.box$logLik)` in the AIC formula, and update all reported AIC values accordingly.

## Limitations

- This skill requires identifying the specific numerical value used in the AIC formula. If the project does not show the full `summary()` output, it may not be possible to determine whether the median or maximum was used.
- In some projects the median and maximum of the log-likelihood distribution are close (e.g., when all replicates converge well), making the error practically negligible. The check in Step 4 identifies when the discrepancy is material.
- Does not cover the case where `logmeanexp()` is used to estimate the log-likelihood from multiple particle filter runs on the same parameters — that is the statistically correct approach (the log of the mean likelihood estimator) and is not an error.
- Does not replace the `pomp-loglik-direction-error` skill; both should be applied when reviewing POMP model comparisons by AIC or log-likelihood.
