---
name: pomp-seir-conservation-identity-audit
description: Use when reviewing a pomp SEIR model where the R compartment is computed via a population conservation identity (R = pop - S - E - I) and the model adds a non-standard flow into R (e.g., vaccination, waning immunity), to detect the silent double-counting error where the flow is subtracted from S but also added explicitly to R, inflating the recovered pool and producing implausibly high R0 estimates without any runtime error.
---

# pomp SEIR Conservation Identity Audit

## Purpose

In standard SEIR POMP models adapted from published templates (e.g., King's measles model), the recovered compartment R is often computed not by explicitly tracking inflows and outflows, but via a population conservation identity:

```c
R = pop - S - E - I;
```

This works correctly for the standard model because R absorbs all individuals not in S, E, or I. When students extend such a model to add a new flow into R -- for example, vaccination moving individuals directly from S to R -- they typically subtract the flow from S correctly but then also add it explicitly to the R identity:

```c
S += births - trans[0] - trans[1] - vac;
R = pop - S - E - I + vac;   // INCORRECT: vac is already reflected in reduced S
```

Because S was already reduced by `vac`, the conservation identity `pop - S - E - I` already assigns those individuals to R. The additional `+ vac` term double-counts them, artificially inflating R. Over time, the spuriously large immune pool forces the optimizer to compensate by increasing R0 and other transmission parameters to maintain observed incidence levels. The error is silent: the code compiles and runs, simulations look qualitatively plausible, and particle filters converge. The only detectable symptom is an implausibly large MLE for R0 that the optimizer "explains away" as a consequence of low susceptibility.

## When to Activate

Use this skill when:
- A pomp SEIR (or SEIRV, SEIRD, or similar) model computes R via a conservation identity `R = pop - S - E - I` (or equivalent).
- The model adds a flow into R beyond the standard I-to-R recovery (e.g., vaccination, waning immunity of exposed individuals, birth-into-R assumptions).
- The estimated R0 from IF2 is substantially higher than epidemiologically expected values for the disease, and no other obvious explanation (e.g., identifiability failure, filter degeneracy) accounts for it.

Do not use this skill when R is updated via explicit accumulation (`R += dN_IR - dN_RX`), as in that case there is no conservation identity and the error pattern does not apply.

## Procedure

### 1. Identify whether R is computed via conservation identity or explicit accumulation

Read the rprocess Csnippet. Determine which pattern is used:
- **Conservation identity:** `R = pop - S - E - I;` (or with additional terms). The identity-based update is a single assignment using the total population.
- **Explicit accumulation:** `R += trans[4] - dN_RS;` where each flow is listed separately.

If the conservation identity is used, proceed with this skill. If explicit accumulation is used, stop -- this skill does not apply.

### 2. List all flows that move individuals into or out of S, E, and I

Read the Csnippet update lines for S, E, and I. For each, record every term that modifies the compartment:
- Inflows to S (births)
- Outflows from S (new exposures, natural mortality from S, vaccination)
- Inflows to E (new exposures)
- Outflows from E (latency completion, natural mortality from E)
- Inflows to I (latency completion)
- Outflows from I (recovery, natural mortality from I)

### 3. Identify any additional terms appended to the R conservation identity

Examine the line that computes R. Note any terms beyond `pop - S - E - I`:
- A `+ vac` term: vaccination was already removed from S, so it is already present in R via the identity.
- A `- dN_RS` term for waning immunity: if individuals are moved from R back to S in an earlier line, the identity already reflects this.
- A `+ births_to_R` term: if some births are assumed to enter R directly (e.g., maternally immune), check whether they are also absent from S births.

For each additional term, ask: was this quantity already absorbed into the conservation identity via its effect on S, E, or I?

### 4. Verify population consistency

After the update equations, compute the implied population:
```
S_new + E_new + I_new + R_new
```
Substitute the update expressions symbolically. If the result does not equal `pop` (or `pop + births - deaths` if pop is updated), there is a conservation violation. Identify which term is responsible.

### 5. Check whether `pop` is a fixed covariate or updated within the time step

If `pop` is a fixed covariate (not updated within each time step, as in many models using `covariate_table`), then:
- Natural mortality from S, E, I removes individuals from those compartments but does not reduce `pop`.
- The conservation identity then assigns the "ghost" individuals to R, inflating R.
- This is a known and deliberate simplification in some models (R absorbs mortality). If so, verify the model description explicitly acknowledges this.
- If `pop` should be updated (or if demographic turnover is substantial over the data period), flag the fixed-pop assumption as a potential source of drift.

### 6. Assess the impact on parameter estimates

If a double-counting error is found:
- The inflated R pool decreases the effective susceptible fraction, depressing the force of infection.
- To maintain observed incidence, the optimizer increases R0 (transmission rate).
- Other parameters that co-vary with R0 (gamma, amplitude, cohort) may also be distorted.
- Check whether the MLE for R0 substantially exceeds the epidemiologically expected range for the disease. If so, the double-counting is the most likely explanation.

### 7. Propose the correction

For a vaccination double-count of the form `R = pop - S - E - I + vac;`:
- The corrected line is simply `R = pop - S - E - I;`.
- No other lines need to change, because the vaccination flow already modifies S, and the identity automatically assigns those individuals to R.

For other error patterns (e.g., waning immunity moving individuals from R to S via `S += dN_RS` but then subtracting again in the identity), the correction depends on the specific flow structure.

## Limitations

- This skill detects double-counting errors in conservation-identity-based R updates only. It does not evaluate whether `pop` should be a fixed or dynamic quantity, which is a separate modeling assumption.
- The skill requires identifying the correct expected range for the disease's R0. If the epidemiological literature provides a wide range (e.g., 2--15), a moderately elevated MLE may not be diagnostic. The error is most clearly identifiable when the MLE exceeds the literature range by an order of magnitude.
- If the model has been deliberately parameterized such that R0 absorbs compensation for other model features (e.g., spatial aggregation, age structure), a high R0 MLE may be partially intentional. Read the model description carefully before attributing a high R0 solely to a double-counting error.
- This skill does not apply to models that compute R by a differential-equation-style explicit net-flow update, even if those updates contain errors.
