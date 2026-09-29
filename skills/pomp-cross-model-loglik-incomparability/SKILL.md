---
name: pomp-cross-model-loglik-incomparability
description: Detect cases where a POMP project fits multiple models using different observation-model families (e.g., Binomial vs. Gaussian, Poisson vs. Normal) and then directly compares their log-likelihoods to select the best model, producing an invalid comparison because the likelihoods are computed under different probability measures — use when reviewing a multi-model POMP paper whose models differ in dmeasure distributional family.
---

# POMP Cross-Model Log-Likelihood Incomparability Detector

## Purpose

When a paper fits multiple competing mechanistic models to the same dataset and selects among them by log-likelihood or AIC, the comparison is only valid if all models use the same observation-model family evaluated on the same data. A recurring error in projects that progressively complexify their models (e.g., SIR → SEIR → SEIQR) is to change the measurement model distributional family between models — for example, using a Binomial dmeasure for the simpler models and a Gaussian dmeasure for the more complex model — and then directly comparing log-likelihoods as if they were on the same scale. Because different distributional families define probability over different sample spaces (discrete integers vs. continuous reals), their log-densities are not comparable: a Gaussian likelihood on count data can be orders of magnitude higher (less negative) than a Binomial likelihood on the same data without reflecting better fit, because the Gaussian density integrates to one over the reals rather than summing to one over the integers.

This error is distinct from:
- `pomp-cross-model-param-reconciliation`: that skill detects irreconcilable values for shared parameters (N, rho) across models; it does not check whether the observation-model families are compatible.
- `pomp-inference-misuse`: that skill detects dmeas/rmeas inconsistency *within a single model*. Here the inconsistency is *across models* being compared.
- `pomp-arima-double-invalid-comparison`: that skill detects ARIMA vs. POMP log-likelihood comparisons on datasets of different length. Here all models fit the same dataset but use different distributional families.

## When to Activate

Use this skill when:
- A POMP paper fits two or more mechanistic models (e.g., SIR, SEIR, SEIQR, or variants) to the same dataset.
- The models use different distributional families in their `dmeasure` Csnippets (e.g., one uses `dbinom`, another uses `dnorm` or `dpois`).
- The paper directly compares log-likelihood values across all models to identify the "best" model.

Do not use this skill when:
- All models use the same observation-model family (e.g., all use Negative Binomial or all use Binomial), even if the parameterization differs. In that case, the log-likelihoods are comparable and this skill does not apply.
- The paper reports log-likelihoods only for descriptive purposes within each model's own section and does not perform a cross-model comparison.
- The paper explicitly acknowledges the incomparability and restricts formal model selection to the subset of models with matching observation models.

## Procedure

### 1. List all models and their dmeasure families

For each model fitted in the paper:
- Read the `dmeasure` (or `dmeas`) Csnippet.
- Identify the distributional family: `dbinom`, `dnbinom`, `dpois`, `dnorm`, `dlnorm`, `dnbinom_mu`, etc.
- Note whether an accumulator variable (from `accumvars`) or a stock compartment is used as the size/mean argument.

### 2. Check whether all models use the same family

Compare the family across all models:
- **Comparable**: all models use the same distributional family (e.g., all `dbinom` with different accumulator variables).
- **Incomparable**: one or more models use a different family (e.g., SIR and SEIR use `dbinom`, SEIQR uses `dnorm`).

Flag any case where the families differ.

### 3. Verify that the paper compares log-likelihoods across the incomparable models

Confirm that the paper:
- Tabulates or mentions log-likelihood values for all models.
- States a conclusion about which model fits best based on these values (e.g., "SEIQR has the best log-likelihood").

If no cross-model comparison is made, do not flag this as an error — models with different families can still be reported individually.

### 4. Assess the direction and magnitude of the bias

Determine which model has the superficially higher (less negative) log-likelihood:
- Gaussian log-densities on count data are typically much higher than Binomial log-probabilities for the same data, because the Gaussian density is not bounded above by 0 (it can be positive for concentrated distributions on continuous data).
- A Poisson likelihood is bounded above by 0 (log p ≤ 0 for each observation), whereas a Gaussian likelihood evaluated at the mean can exceed 0 when the standard deviation is small.

Estimate whether the reported log-likelihood gap between models is plausibly explained by the family change alone, independent of model quality.

### 5. Identify the specific conclusion that is invalidated

Quote the specific sentence in the paper that uses the cross-model log-likelihood comparison to conclude which model is best. State explicitly that this conclusion cannot be supported because the log-likelihoods are not on the same scale.

### 6. Propose the fix

Provide concrete remediation options:
- **Preferred**: Standardize all models to use the same observation-model family before comparing log-likelihoods. The choice of family should be scientifically motivated (e.g., Binomial for overdispersed count data with a reporting rate).
- **Alternative**: Restrict the formal model comparison to the subset of models with matching families (e.g., compare SIR vs. SEIR using Binomial, and report the SEIQR model's Gaussian log-likelihood only for illustrative purposes with a clear caveat).
- **Scoring-rule alternative**: Replace log-likelihood comparison with a proper scoring rule (e.g., CRPS, RMSE on the original count scale) that does not require matching distributional families.

### 7. Report the finding

For each detected instance, report:
- The model name and dmeasure family for each model in the comparison.
- The log-likelihood values reported and the conclusion drawn.
- The explanation of why the comparison is invalid (different probability measures; Gaussian likelihood not bounded above by 0 on count data).
- The fix.

## Limitations

- This skill requires reading all `dmeasure` Csnippets across models. If Csnippets are defined in separate scripts not shown in the main document, the inconsistency may not be detectable from the Rmd alone.
- In some models, a Gaussian likelihood is a deliberate and acknowledged approximation to a discrete likelihood (e.g., for large counts). If the authors explicitly justify and discuss this approximation and do not claim the Gaussian log-likelihood is directly comparable to a Binomial log-likelihood, the situation is more nuanced — flag as a minor concern rather than a major error.
- The severity of the error depends on how different the log-likelihood scales are. For very large counts where the Gaussian and Binomial agree closely, the comparison may be approximately valid. For small or sparse count data, the discrepancy can be orders of magnitude.
- Does not replace `pomp-cross-model-param-reconciliation`, which should be applied in addition to detect parameter-value inconsistencies between models.
- Does not replace `pomp-inference-misuse`, which should be applied to check within-model dmeas/rmeas consistency.
