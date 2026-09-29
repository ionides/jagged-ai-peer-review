---
name: pomp-cross-model-param-reconciliation
description: Detect cases where two or more POMP models in the same paper claim to study the same system but use mutually irreconcilable values for shared parameters (e.g., reporting rate, population size, time period) without acknowledgment, making cross-model comparisons invalid — use when a paper fits multiple compartmental models to the same data and compares their likelihoods or parameter estimates.
---

# POMP Cross-Model Parameter Reconciliation Auditor

## Purpose

A paper may present multiple mechanistic models (e.g., SIRS and SEIR) as competing descriptions of the same epidemiological system and compare their log-likelihoods. For this comparison to be meaningful, the models must share the same data, the same observation model structure, and reconcilable values for parameters that both models define (e.g., total population N, reporting rate rho, time period). A recurring pattern in student projects is that one model fixes a parameter (e.g., rho = 1e-7) while another estimates it freely (e.g., rho ≈ 0.9), or one uses a correct population value while another uses a value off by two orders of magnitude — with neither discrepancy acknowledged. Because the models run without error and produce plausible-looking trajectories, this inconsistency is invisible without cross-reading both model sections.

This error is distinct from the dataset substitution error (wrong data used), the static population audit (fixed vs. time-varying N), and the invalid SARIMA-POMP LL comparison. It is specifically about internal contradiction *between* models in the same paper for the same system.

## When to Activate

Use this skill when:
- A paper fits two or more mechanistic compartmental models (e.g., SIR + SEIR, SIRS + SEIR, SIR + SIRV) to the same dataset.
- The paper compares the models' log-likelihoods or parameter estimates as if they are on equal footing.
- Both models define or estimate one or more shared parameters (N, rho, initial conditions, time span).

Do not use this skill when:
- Only a single mechanistic model is fitted (no cross-model comparison is made).
- The paper explicitly acknowledges and justifies differing assumptions across models (e.g., "Model 1 treats rho as fixed at the literature estimate; Model 2 estimates it freely").
- The models are applied to deliberately different datasets or subpopulations.

## Procedure

### 1. Identify the shared parameters across models

For each mechanistic model in the paper, note the values of:
- Total population N (fixed or estimated MLE)
- Reporting rate rho (fixed or estimated MLE)
- Data time span (start and end dates, number of observations)
- Observation model family (Poisson, negative binomial, Gaussian)
- Any other parameter that appears in both models with a biological interpretation (recovery rate, transmission rate)

### 2. Check for irreconcilable values

For each shared parameter, compare the values used or estimated across models:
- If one model fixes rho = 1e-7 and another estimates rho ≈ 0.9, these are irreconcilable.
- If N differs by more than a factor of 2 across models without explanation, flag it.
- If the data time span differs (different filtering or row-selection code), flag it.

Use the threshold: a ratio exceeding 10 for a shared parameter, or a differing data source, indicates a reconciliation failure.

### 3. Check whether discrepancies are acknowledged

Read the paper for any statement that explains differing assumptions across models (e.g., "SIRS fixes rho based on surveillance coverage; SEIR estimates it"). If no such statement exists, the discrepancy is unacknowledged.

### 4. Assess the impact on cross-model comparisons

If models are compared by log-likelihood and they differ in N, rho, or data:
- The log-likelihoods are not comparable because the effective observation model is different.
- Any statement like "SEIR achieves a higher log-likelihood than SIRS, indicating better fit" is invalid if the models differ in rho or N.
- Flag the cross-model comparison as invalid.

### 5. Report the finding

For each detected inconsistency, report:
- The specific parameter and the values used in each model.
- The location in the source code where each value is defined.
- Whether the discrepancy is acknowledged in the text.
- The consequence: cross-model LL comparisons are invalid; parameter estimates are not scientifically comparable.
- The fix: standardize shared parameters (same N, same rho treatment, same data) before comparing models, or explicitly justify differing assumptions.

## Limitations

- This skill requires reading both model sections carefully. It cannot be detected from the rendered HTML output unless parameter tables are shown.
- If models are intentionally designed with different assumptions (e.g., one assumes immunity waning, one does not), differences in rho or N may be scientifically motivated. Only flag cases where no justification is provided.
- Does not cover the case where both models use the same wrong parameter value — that would be caught by the static-population audit or accumvar semantic audit.
- Does not replace the dataset-substitution audit; that skill covers the data-source level, while this skill covers the parameter level.
