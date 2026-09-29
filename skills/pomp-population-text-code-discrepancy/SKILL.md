---
name: pomp-population-text-code-discrepancy
description: Detect cases where a POMP project documents one population size N in the text description but uses a numerically different value in the code, causing the force-of-infection scaling to be wrong and invalidating all parameter estimates — use when a POMP project models two or more geographic units and the code N values differ from those stated in the methods or data description.
---

# POMP Population Text-Code Discrepancy Detector

## Purpose

In POMP compartmental models, the force of infection includes the term `Beta * I / N`, making N a direct scaling factor for the transmission rate. When a paper studies multiple geographic units (countries, states, cities), each unit requires its correct population size. A recurring error — particularly in projects that copy and adapt code between units — is to state the correct N in the text (e.g., "Sierra Leone population: 16,190,280") while the code uses a different value (e.g., `N=6190280`) due to a transcription error such as a dropped digit, a decimal point shift, or a copy-paste from a different unit.

Unlike the `pomp-static-population-audit` skill (which handles temporal bias from using a single fixed N across a long time series), this error is a simple code-text disagreement within a single analysis unit. The result is that the effective Beta estimated from the data is biased by the ratio of the true N to the coded N — which can be a factor of 2 or more if a digit is dropped from a 7-8 digit population figure.

This error is distinct from:
- `pomp-static-population-audit`: that skill covers temporal variation in N for long time series. Here, the issue is a transcription error between text and code for a fixed time window.
- `pomp-cross-model-param-reconciliation`: that skill covers N inconsistencies across models of the same system. Here, the inconsistency is between the text documentation and the code for a single model.

## When to Activate

Use this skill when:
- A POMP project models two or more geographic units (e.g., countries, states) in parallel sections of the same document.
- Each unit's population size N is stated in the methods text or data description.
- The code uses a hardcoded `N` value in `params` or `fixed_params` that can be compared against the stated value.
- The project copies and adapts code from one unit to another with minimal modification.

Do not use this skill when:
- Only a single geographic unit is modeled (no cross-unit copying risk, though a single-unit discrepancy is still possible).
- N is estimated as a free parameter (not fixed in code) — in that case the text value is an initial guess, not the model's N.
- The discrepancy is smaller than 5% (negligible bias on Beta).

## Procedure

### 1. Extract the stated N values from the text

Read the methods, data description, or introduction. For each geographic unit, record the population size stated in prose (e.g., "Guinea population 10,628,972; Sierra Leone population 16,190,280").

### 2. Extract the coded N values from the source

Search the Rmd/R source for each unit's `params = c(... N=..., ...)` or `fixed_params = c(N=..., ...)`. Record the numerical value used in code for each unit.

### 3. Compare text values to coded values

For each unit, compute the ratio: `N_code / N_text`. Flag any discrepancy where:
- The ratio is outside [0.95, 1.05] — a more than 5% deviation.
- The digit count differs (e.g., 7 digits vs. 8 digits) — strongly suggestive of a dropped digit.

### 4. Identify the source of the discrepancy

Common transcription error patterns:
- **Dropped leading digit**: 16,190,280 → 6,190,280 (ratio ≈ 0.38; factor ~2.6 bias on Beta).
- **Unit mismatch**: value in thousands vs. actual count (e.g., 10,629 vs. 10,628,972).
- **Copy-paste from another unit**: Guinea's N pasted into Sierra Leone's code block.

### 5. Quantify the bias on Beta

The effective transmission rate is proportional to `Beta * I / N`. If the coded N is wrong by factor r = N_code / N_true, then the estimated Beta is biased by factor 1/r:

- `Beta_estimated ≈ Beta_true * (N_true / N_code) = Beta_true / r`

Compute the bias factor and report it. A factor exceeding 1.5 constitutes a major issue that invalidates parameter comparisons between units.

### 6. Check whether the comparison between units is invalidated

If the paper compares parameter estimates or confidence intervals across geographic units, and N is wrong for one unit, the comparison is invalid. Specifically:
- Confidence intervals for Beta in the unit with the wrong N are biased and cannot be compared to intervals from other units.
- Any conclusion that "transmission rates are similar across units" based on overlapping CIs is not supported if one unit's Beta scale is distorted.

### 7. Report the finding

For each detected discrepancy, report:
- The unit name, the text-stated N, and the coded N.
- The discrepancy ratio and the implied bias factor on Beta.
- Any cross-unit conclusions that are invalidated by the discrepancy.
- The fix: update the coded N to match the correct population value and re-run all parameter estimation and profile likelihood computations for that unit.

## Limitations

- This skill requires reading both prose and code; it cannot be detected from rendered HTML output.
- If the paper cites a specific demographic source for N and the code value differs from that source, the code is clearly wrong. If no source is cited in prose, the text value itself may be in error and should be verified against census data before concluding which value is correct.
- For population values that are plausible for a different administrative subdivision of the same country (e.g., a province vs. the whole country), the "discrepancy" may be intentional. Check whether the study scope is explicitly defined as sub-national.
- Does not cover the case where both text and code use the same wrong N — that is covered by `pomp-static-population-audit`.
