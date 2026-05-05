---
name: pomp-seir-accumulator-convention
description: Use when reviewing a pomp SEIR (or similar compartmental) model for infectious disease where the observed data are new confirmed cases (incidence), to detect the silent mismatch where the accumulator variable tracks recoveries (dN_IR) or current prevalence (I) instead of new infections entering the observable state (dN_EI or dN_IR depending on the surveillance model), which produces a systematically lagged and misspecified observation process without any runtime error.
---

# pomp SEIR Accumulator Convention Audit

## Purpose

In student and research pomp projects for COVID-19 and other infectious diseases, reported case counts represent new confirmed infections — individuals who tested positive during a given observation interval (typically one day). The epidemiologically correct accumulator for such data is the flow of new individuals entering the symptomatic or infectious class (dN_EI in an SEIR model, or a separate detection compartment if one is modeled).

A recurring silent error is accumulating recoveries instead: `H += dN_IR`. Because confirmed cases do appear after recovery from the infectious class (in the sense that the model "counts" them), this assignment can seem plausible. However, it misspecifies the observation timing: an individual who enters I on day 1 and recovers on day 11 would be "counted" as a new case on day 11 under this convention, despite first being symptomatic and test-eligible on day 1. This introduces a systematic lag in the observation model equal to the infectious period, distorts all estimated duration parameters, and conflates incidence with a delayed proxy.

A related error is assigning the accumulator to a prevalence stock (`H = I`) rather than a flow — this is covered in `pomp-csnippet-audit`. This skill focuses specifically on the epidemiological question of which transition event the accumulator should track, which requires domain knowledge beyond syntactic correctness.

This error is invisible at runtime: the model compiles, simulations produce plausible trajectories, and the particle filter runs (or fails for unrelated reasons). It can only be caught by cross-referencing the accumulator update rule against the epidemiological definition of the observed data.

## When to Activate

Use this skill when:
- A pomp project fits an SEIR, SEIRD, SEIRV, or similarly structured compartmental model.
- The observed data represent new confirmed cases per interval (daily incidence, weekly incidence, or similar surveillance counts).
- The model defines an accumulator variable (typically H, cases, or reports) that is registered in `accumvars` and used as the size argument or mean in dmeas/rmeas.

Do not use this skill when:
- The observed data represent cumulative case totals (requires differencing the accumulator differently).
- The observed data represent hospitalized prevalence or ICU occupancy (stock variables, not incidence; a different observation model is appropriate).
- The model includes an explicit "detection" or "ascertainment" compartment that is separate from I and R — in that case, the accumulator should track the flow into the detection compartment, and the same logic applies at that level.

This skill is complementary to `pomp-csnippet-audit` (which checks stock-vs-flow syntax and dmeas/rmeas consistency) and does not replace it.

## Procedure

### 1. Identify the observed data type

Read the data description section of the manuscript or Rmd. Determine:
- Do the reported observations represent new cases per interval (incidence)?
- Do they represent active cases at a point in time (prevalence)?
- Do they represent cumulative totals?

For most COVID-19 case count datasets (NYT, JHU, OWID), the raw data are cumulative totals. Projects that difference the cumulative counts before fitting are working with incidence. Projects that fit the cumulative total directly require a different accumulator convention (typically cumulative flow rather than a reset accumulator).

### 2. Locate the accumulator update in the rprocess Csnippet

Find the rprocess Csnippet. Identify the line(s) that update the accumulator variable (registered in `accumvars`). Record:
- The transition being accumulated (e.g., `H += dN_SE`, `H += dN_EI`, `H += dN_IR`).
- The epidemiological meaning of that transition (S-to-E: new exposures; E-to-I: new infectious onset; I-to-R: recoveries).

### 3. Match accumulator transition to observation type

For incidence data (new confirmed cases per interval):
- The accumulator should track the transition that corresponds to case ascertainment. In most COVID-19 SEIR models without an explicit testing compartment, this is new infections entering the symptomatic/infectious class: `H += dN_EI`.
- If the model includes a testing or reporting delay compartment (e.g., S -> E -> I -> D_etected -> R), the accumulator should track the flow into the detected class.
- Accumulating recoveries (`H += dN_IR`) introduces a systematic lag equal to the infectious period. Flag as a major error.
- Accumulating new exposures (`H += dN_SE`) introduces a lag equal to the incubation period plus some infectious duration. Flag as a major error.

For prevalence data (e.g., hospitalized patients currently in hospital):
- A separate stock variable (not an accumulator) should be used, representing the current count in the relevant compartment (e.g., the H compartment if H represents current hospitalizations, not a flow).

### 4. Check the measurement model for consistency with the accumulator

After verifying the accumulator convention, confirm that the measurement model (dmeas/rmeas) treats H as the appropriate quantity:
- For incidence: H represents new detectable events per interval. A binomial draw `rbinom(H, rho)` or a negative binomial draw from mean `rho * H` is appropriate.
- A common secondary error is using H as the "size" argument in a binomial but accumulating into H at a sub-daily time step (delta.t < 1). Because accumvars resets H after each observation interval (not each sub-step), this is generally correct — but verify that delta.t and the accumvars reset are coordinated with the observation timing.

### 5. Assess impact on parameter estimates

If the accumulator tracks the wrong transition:
- The estimated reporting rate rho absorbs the timing discrepancy. It will be biased toward whatever value makes a shifted incidence curve match the shifted observation curve.
- The infectious period mu_IR will be biased because the observation process does not independently constrain it from the recovery process.
- The incubation period mu_EI may also be affected, because the peak of recoveries is shifted relative to the peak of new infections.
- State the direction and approximate magnitude of bias if determinable from the model structure.

### 6. Summarize findings

For each accumulator convention error found:
- Quote the offending Csnippet line (e.g., `H += dN_IR;`).
- State the epidemiological meaning of the transition being tracked.
- Explain why this does not correspond to the observation type (e.g., "confirmed cases reflect new symptom-onset events, not recovery events; recovery occurs approximately mu_IR^-1 days after symptom onset").
- Propose the corrected line (e.g., `H += dN_EI;` for new infections entering the infectious class).
- Identify which estimated parameters are likely biased as a result.

## Limitations

- This skill requires knowing the epidemiological definition of the observed data. If the data provenance is unclear (e.g., a column labeled "cases" that could be cumulative or incident), the audit cannot be completed without resolving the ambiguity first.
- The correct accumulator transition depends on the surveillance model. In settings where testing is delayed (e.g., results returned several days after specimen collection), neither dN_EI nor dN_IR may be the correct anchor — a dedicated ascertainment delay compartment is needed. This skill covers the common case where no such compartment is modeled.
- This skill addresses the transition tracked by the accumulator, not whether the model's overall compartment structure is appropriate for the disease. Structural model misspecification (e.g., omitting waning immunity, ignoring age structure) is outside scope.
- For models with multiple observation streams (e.g., cases and deaths), each accumulator must be evaluated separately. The presence of one correctly specified accumulator does not imply the others are correct.
