---
name: pomp-accumvar-semantic-audit
description: Detect cases where a POMP model's accumulator variable (accumvars) tracks the wrong compartment flow relative to what the observation data records, causing a systematic mismatch between the measurement model and the data — use when reviewing a POMP project that uses an accumulator variable linked to reported case counts.
---

# POMP Accumulator Variable Semantic Audit

## Purpose

POMP models of infectious disease counts commonly define an accumulator variable (e.g., `H`) that is reset at each observation time and accumulates one or more compartment flows. The measurement model then links observed case counts to this accumulator (e.g., `reports ~ NegBin(rho * H, k)`). A recurring error is to accumulate the wrong flow: for example, accumulating recoveries from quarantine (`dN_QR`) rather than new entries into quarantine (`dN_IQ`), when the observation data records newly detected (quarantined) cases. Because both flows are plausible aggregations, this error does not produce a runtime warning, and simulations may still produce trajectories that superficially resemble the data — masking the mismatch.

This error distorts parameter estimates: `rho` absorbs the ratio of recoveries to true detections, and transition rates may shift to compensate. Profile likelihoods and any policy conclusions derived from the model are unreliable.

## When to Activate

Use this skill when:
- A POMP project defines an accumulator variable `H` (or `C`, `Inc`, etc.) in `accumvars`.
- The accumulator is linked to reported case counts in the measurement model (e.g., `mu = rho * H` in `dmeasure`).
- The model includes multiple compartment flows (e.g., infection, quarantine entry, quarantine exit/recovery) any of which could plausibly be accumulated.

Do not use this skill when:
- The accumulator variable clearly tracks only one flow (e.g., a simple SIR model where `H` can only accumulate `dN_IR`).
- The paper explicitly justifies the choice of which flow to accumulate with reference to the data-generating mechanism.
- No accumulator variable is used (e.g., the measurement model links directly to a state compartment such as `I`).

## Procedure

### 1. Identify the accumulator variable and what it accumulates

Read the Csnippet or R step function. Locate all lines of the form `H += ...` (or `C += ...`, `Inc += ...`). Note each compartment flow being accumulated.

### 2. Identify what the observation data records

Read the data description and the measurement model. Determine what epidemiological event the observed count represents:
- Newly detected / confirmed infections (entries into a detection or quarantine compartment)?
- Recoveries or hospitalizations (exits from an infectious compartment)?
- Deaths?
- Some combination (e.g., daily test positives)?

### 3. Check whether the accumulated flow matches the observation event

Compare the flows accumulated in `H` against the identified observation event:
- **Correct pattern**: `H += dN_SI` for confirmed new infections in an SIR, or `H += dN_IQ` (entries to quarantine) when data records newly quarantined cases.
- **Error pattern**: `H += dN_QR` (exits from quarantine / recoveries) when data records newly confirmed cases entering quarantine; or `H += dN_IR` (recoveries) when data records new infections.

Flag any case where the accumulated flow is the biological complement of what the data records.

### 4. Assess the impact on parameter estimates

If a mismatch is found:
- Explain which parameter(s) absorb the mismatch. Typically `rho` (the reporting rate) will be estimated near the ratio of recoveries to infections per time step, not the true reporting fraction.
- Note that transition rates out of the mismatched compartment may also be distorted, because the optimizer shifts them to improve the log-likelihood under the wrong measurement model.
- Flag all downstream parameter estimates, confidence intervals, and policy conclusions as potentially unreliable.

### 5. Propose the fix

Identify the correct flow to accumulate based on the data-generating process. For example:
- If data = new confirmed (quarantined) cases: `H += dN_IQ_o + dN_IQ_b`
- If data = new infectious cases (not quarantined): `H += dN_SI_o + dN_SI_b`

Specify the exact line in the Csnippet to change.

## Limitations

- This skill requires biological domain knowledge to determine what the observation data records. For novel diseases or non-standard surveillance systems, the correct accumulation may be ambiguous; in such cases, flag the issue as a potential concern and request clarification from the authors.
- Simulations from an incorrectly specified model may still look visually similar to the data if the mismatched flow has similar dynamics to the correct flow. Visual plausibility does not confirm semantic correctness.
- Does not cover cases where the entire measurement model is misspecified (e.g., wrong distribution family) — those are covered by the `pomp-inference-misuse` skill and the POMP checklist item on measurement model specification.
- Does not apply to spatial POMP models where accumulation is per spatial unit; the same logic applies but must be checked unit by unit.
