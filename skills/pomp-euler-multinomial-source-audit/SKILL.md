---
name: pomp-euler-multinomial-source-audit
description: Use when reviewing a pomp project with a multi-compartment Euler-multinomial rprocess Csnippet to detect the silent error where a transition draw samples the wrong source compartment (e.g., rbinom(I, ...) for an R-to-S transition), which produces a valid-running model that misrepresents population flows and violates conservation without any runtime error.
---

# pomp Euler-Multinomial Source Compartment Audit

## Purpose

In Euler-multinomial rprocess Csnippets, each transition draw takes the form `dN_XY = rbinom(X, 1-exp(-rate*dt))`, where X is the source compartment. A silent error occurs when the wrong compartment is passed as the first argument — for example, `dN_RS = rbinom(I, 1-exp(-mu_RS*dt))` when the intended transition is from R to S. The code compiles, simulates, and runs the particle filter without error. However, the transition dynamics are misspecified: R-to-S transitions are drawn from I, which may have a very different population size and can drive S into negative territory or inflate transition counts beyond what R contains.

This error is distinct from the stock-vs-flow accumulator error (covered by `pomp-csnippet-audit`) and from the wrong-transition-tracked-by-accumulator error (covered by `pomp-seir-accumulator-convention`). It is specifically about using the wrong compartment as the size argument in an otherwise syntactically correct Euler-multinomial draw.

## When to Activate

Use this skill when:
- A pomp project uses Euler-multinomial rprocess Csnippets with three or more compartments.
- The model includes transitions between non-adjacent compartments (e.g., R-to-S waning immunity, V-to-S vaccine waning, Q-to-S quarantine release, or P-to-R asymptomatic recovery in a SEPIR model).
- Any transition in the Csnippet involves a compartment that is not the immediately preceding compartment in the standard SEIR chain.

Do not use this skill as a substitute for the accumulator audit (`pomp-csnippet-audit`) or the accumulator convention audit (`pomp-seir-accumulator-convention`) — all three should be applied when reviewing a new pomp Csnippet.

## Procedure

### 1. List all transitions defined in the model description

From the model text, diagram, or differential equations, extract every intended transition as a triple: (source compartment, destination compartment, rate parameter). Example:

| Transition | Source | Destination | Rate |
|-----------|--------|-------------|------|
| S to E    | S      | E           | Beta |
| E to I    | E      | I           | mu_EI|
| I to R    | I      | R           | mu_IR|
| R to S    | R      | S           | mu_RS|

### 2. For each transition, locate the corresponding draw in the Csnippet

Scan the rprocess Csnippet and match each biological transition X->Y to its Csnippet line, typically of the form:
`double dN_XY = rbinom(COMP, 1-exp(-rate*dt));`

Note: the variable name `dN_XY` may not always follow the X->Y convention; use the rate parameter and surrounding context to identify which biological transition each line represents.

### 3. Verify that COMP matches the source compartment X

For each transition:
- If COMP == X: correct.
- If COMP != X: flag as a source compartment error. Record the offending line, the intended source compartment, the actual compartment used, and the biological consequence.

Pay particular attention to transitions that skip compartments (e.g., R-to-S) or that reuse rate parameter names that appear in multiple places — these are the highest-risk lines.

### 4. Check compartment update equations for conservation

After verifying all source compartments, check that each compartment's net update in the Csnippet equals inflows minus outflows as specified in the model:
- Each compartment should be decremented by all outgoing transitions and incremented by all incoming transitions.
- If a compartment update does not include a term that should be present (e.g., R is not decremented by dN_RS), this signals either a missing update line or a misidentified transition draw.

Violations of conservation provide a secondary diagnostic for source compartment errors: if R grows without bound while S is being replenished, and dN_RS is drawn from I, the conservation check will reveal the inconsistency even if the source compartment error is subtle.

### 5. Assess the consequence of the misspecification

For each flagged error, assess the likely impact on model dynamics and parameter estimates:
- State which compartment was sampled instead of the intended one.
- Estimate the typical size difference between the correct and incorrect source compartments (e.g., "during the epidemic peak, I may be 10x smaller than R, so dN_RS is 10x underestimated").
- State which estimated parameters are likely biased as a result (e.g., if R-to-S draws from I, the effective waning immunity rate is confounded with the infectious prevalence).

### 6. Summarize findings

For each error:
- Quote the offending Csnippet line (e.g., `double dN_RS = rbinom(I, 1-exp(-mu_RS*dt));`).
- State the intended and actual source compartment.
- Explain the consequence.
- Propose the corrected line (e.g., `double dN_RS = rbinom(R, 1-exp(-mu_RS*dt));`).

## Limitations

- This skill requires knowing the intended biological transitions, which must come from the model description or diagram. If the description is ambiguous or absent, the audit cannot determine the correct source compartment without additional biological context.
- In models with very small compartment sizes, source compartment errors may produce implausible simulation outputs (negative compartment counts) that are detectable without this skill. In large-N models, the error may be numerically mild in some periods even though the model dynamics are misspecified.
- This skill does not detect errors in the rate parameter values themselves (e.g., using mu_IR where mu_RS was intended), only errors in the source compartment size argument. A separate review of rate parameter assignments is needed.
- The skill addresses one-compartment-draws-from-another errors. It does not cover Euler-multinomial splitting errors (where a single outflow from one compartment is split across multiple destinations) — those require a different audit focused on the `reulermultinom` function or equivalent.
