---
name: pomp-aic-mc-noise-audit
description: Detect cases where a POMP project presents AIC comparisons between the POMP model and deterministic-likelihood models (GARCH, ARMA, SARIMA) without reporting the Monte Carlo standard error of the POMP log-likelihood, rendering the AIC difference statistically uninterpretable — use when a project compares POMP AIC to GARCH or ARMA AIC and claims superiority based on the numerical difference alone.
---

# POMP AIC Monte Carlo Noise Audit

## Purpose

GARCH, ARMA, and SARIMA models have exact (analytically computed) log-likelihoods. POMP stochastic models use particle filter estimates of the log-likelihood, which are subject to Monte Carlo noise. When a project compares AIC values from these two model families and concludes that the POMP model is "better" by a given AIC margin, the conclusion is only valid if the AIC margin substantially exceeds the Monte Carlo noise in the POMP log-likelihood estimate.

Two compounding sources of Monte Carlo noise are present in a typical POMP AIC:

1. **Within-chain noise**: Each IF2 chain's final log-likelihood is estimated by `logmeanexp` over `Nreps_eval` particle filter replicates. If `Nreps_eval` is small (< 10), the per-chain log-likelihood SE is on the order of 1–5 units for typical financial return models.

2. **Selection bias across chains**: The AIC uses `max(logLik)` over all IF2 replicates. Taking the max of noisy estimates selects the chain with the largest positive noise realization, biasing the AIC optimistically by an amount that grows with the number of chains and the per-chain SE.

Together, these effects mean that a POMP AIC advantage of fewer than ~5–10 units over a deterministic model may lie entirely within Monte Carlo noise. The paper's conclusion that the POMP model is superior may not be statistically justified.

This error is distinct from:
- `pomp-aic-median-loglik-error`: that skill covers using the median (wrong statistic) rather than the maximum log-likelihood in the AIC formula. Here, `max()` is used correctly, but the max itself is a noisy estimator.
- `sarima-baseline-audit`: that skill covers mismatched observation models or invalid period specifications in SARIMA. Here the observation models may match, and the issue is purely about MC noise.
- `pomp-loglik-direction-error`: that skill covers directional misinterpretation of log-likelihood values. Here the direction is correct but the precision is overstated.

## When to Activate

Use this skill when:
- A POMP project reports AIC for both a stochastic POMP model (fitted via particle filter + IF2) and a deterministic-likelihood model (GARCH, ARMA, or SARIMA, fitted via `arima()`, `garch()`, or `Arima()`).
- The project states or implies that the POMP model is superior based on a numerical AIC advantage.
- The POMP AIC is computed from `max(logLik)` across IF2 replicates without reporting the SE of the log-likelihood.
- The AIC advantage of POMP over the deterministic model is less than 20 units (below this threshold, Monte Carlo noise may explain the entire gap).

Do not use this skill when:
- The POMP log-likelihood SE is explicitly reported (via `logmeanexp(..., se=TRUE)`) and the AIC advantage clearly exceeds 2 × SE.
- The project acknowledges that the AIC comparison is approximate due to MC noise and does not make strong model-selection claims.
- The AIC advantage of POMP exceeds 50 units, making the noise-driven explanation implausible.

## Procedure

### 1. Identify the AIC values reported for each model

Record the exact AIC reported for:
- The deterministic-likelihood model (GARCH, ARMA, SARIMA): this is an exact value with no MC noise.
- The POMP model: note the formula used. Is it `-2 * max(r.box$logLik) + 2 * k` or `-2 * median(r.box$logLik) + 2 * k`? (If median, also apply `pomp-aic-median-loglik-error`.)

### 2. Compute the claimed AIC advantage

Compute `AIC_deterministic - AIC_POMP`. A positive value means POMP appears better. Note the magnitude.

### 3. Assess the per-chain log-likelihood SE

Locate the `logmeanexp(replicate(Nreps_eval, logLik(pfilter(...))), se=TRUE)` call that produces each chain's log-likelihood estimate. Read the SE from the second element of the returned vector. If the SE is not reported, flag that it is missing.

For typical financial log-return models with N ≈ 1258 observations, a Gaussian measurement model, and `Np = 2000` particles, expected per-chain log-likelihood SE is approximately 0.5–2 units per chain.

### 4. Assess selection bias from taking the max across chains

If there are `K` IF2 chains, the maximum of K noisy log-likelihood estimates has an expected upward bias of approximately `SE × Φ^{-1}(K/(K+1))` relative to the true MLE, where `Φ^{-1}` is the standard normal quantile function. For K = 20 chains and SE = 1.5 units, the expected max bias is approximately 2–3 log-likelihood units, corresponding to an AIC bias of 4–6 units.

### 5. Compare the AIC advantage to the combined noise

If `AIC_advantage < 2 × (per-chain SE) + selection_bias_estimate`, the AIC advantage is potentially explained by Monte Carlo noise alone. Flag this as a major issue.

### 6. Check whether the observation models are comparable

Verify that both models are evaluated on the same data (same observations, same transformation). For financial log-return data:
- ARMA: Gaussian observation model for demeaned returns.
- GARCH: Gaussian conditional distribution for same series.
- POMP SV: Gaussian observation model `dnorm(y, 0, exp(H/2))` for same series.

If all three use Gaussian distributions on the same untransformed data, the log-likelihoods are on a comparable scale and the AIC comparison is conceptually valid — but the MC noise issue in Step 5 still applies.

If the models differ in observation distribution (e.g., POMP uses Student-t while ARMA uses Gaussian), the log-likelihoods are not directly comparable. Flag this as a separate issue (see `sarima-baseline-audit` for SARIMA-specific guidance).

### 7. Report the finding

For each detected instance, report:
- The AIC values and claimed advantage.
- The per-chain log-likelihood SE (if reported) or its absence.
- The estimated MC bias from max-selection across chains.
- Whether the AIC advantage likely exceeds MC noise.
- The consequence: the model selection conclusion may not be statistically supported; the POMP model may not genuinely outperform the deterministic model by the claimed margin.
- The fix: report `logmeanexp(replicate(Nreps_eval, logLik(pfilter(...))), se=TRUE)` for the best-chain parameters, report the SE alongside the AIC, and compare the AIC advantage to twice the SE before claiming model superiority. For stronger evidence, use the best-chain parameters and run an additional `logmeanexp` over a larger number of particle filter replicates (e.g., 50 rather than 20) to reduce the SE before reporting the final AIC.

## Limitations

- The expected max-selection bias formula in Step 4 assumes independent, identically normally distributed per-chain log-likelihood estimates. In practice, the estimates are not exactly independent (chains that converge to the same region will be correlated) and may not be normal; the formula gives an approximation only.
- If the project uses `Np = 5000` or more particles, the per-chain SE may be small enough (< 0.5 units) that the MC noise concern is minor even for modest AIC advantages (10+ units).
- This skill does not apply when the AIC advantage is large (> 50 units), as MC noise alone cannot plausibly explain a gap of that magnitude.
- Does not replace the `pomp-aic-median-loglik-error` skill or the broader computational adequacy check (Wheeler et al. 2024, §6); it focuses specifically on the MC noise in the AIC comparison between POMP and deterministic models.
