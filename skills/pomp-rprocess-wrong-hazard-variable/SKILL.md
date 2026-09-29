---
name: pomp-rprocess-wrong-hazard-variable
description: Detect cases where a POMP rprocess step function specifies the hazard rate of a compartment transition using the wrong state variable (e.g., using V instead of I in the force-of-infection term for V→I transitions in an SIRV model), causing the stochastic transition probabilities to be inconsistent with the stated ODE system — use when reviewing a POMP compartmental model with multiple infection pathways or cross-compartment interactions.
---

# POMP rprocess Wrong Hazard Variable Detector

## Purpose

In POMP compartmental models with multiple infection pathways (e.g., SIRV, SVEIR, SEIRD), the hazard rate for each transition must reference the correct state variable. A recurring error in student SIRV projects is to specify the V→I transition probability using V (the vaccinated count) in the hazard rate rather than I (the infectious count):

```r
# Error: uses V instead of I in force of infection on vaccinated
dN_VI <- rbinom(n=1, size=V, prob=1-exp(-Sigma*Beta*V/N*delta.t))

# Correct: force of infection on V is proportional to I
dN_VI <- rbinom(n=1, size=V, prob=1-exp(-Sigma*Beta*I/N*delta.t))
```

In an SIRV model where vaccinated individuals can be (partially) infected, the biological mechanism is mass-action mixing: vaccinated individuals encounter infected individuals at a rate proportional to I/N. The `size` argument of `rbinom` is correctly V (we draw from the vaccinated pool), but the rate at which each vaccinated individual transitions to I depends on I, not V. Using V in the hazard rate creates a self-enhancing (or self-suppressing) transition that is disconnected from the actual infectious compartment, producing a dynamics that does not correspond to the stated differential equations.

This error does not produce a runtime warning because the code is syntactically valid. Simulations still produce plausible-looking trajectories when the two compartments have similar magnitudes, masking the inconsistency.

## When to Activate

Use this skill when:
- A POMP project defines a compartmental model with multiple infection pathways (e.g., SIRV, SVEIR, SEIQ, SEIRD, SVIR).
- At least one transition involves a compartment being infected by external contact (i.e., the `size` of the binomial draw is one compartment, but the hazard rate should depend on a different compartment representing the infectious pool).
- The rprocess step function specifies `prob = 1 - exp(-rate * X / N * delta.t)` where `X` is a state variable — verify that `X` is the infectious compartment (typically I or E+I), not the compartment being depleted (the `size` argument).

Do not use this skill when:
- The model has only one infection pathway (standard SIR/SEIR) where the force of infection is unambiguously `Beta * I / N`.
- The transition is not infection-driven (e.g., recovery I→R, waning immunity R→S) and the hazard rate appropriately depends only on parameters, not on other compartments.
- The authors explicitly describe a non-standard force-of-infection formulation and justify it scientifically.

## Procedure

### 1. Identify all infection-driven transitions in the rprocess

Read the rprocess Csnippet or R step function. List every `rbinom` (or `reulermultinom`, `rpois`, etc.) call that represents an infection event — i.e., a transition where an individual moves from a non-infectious compartment to an infectious or exposed compartment. For each call, note:
- The `size` argument (which compartment is being depleted).
- The `prob` argument (what drives the transition rate).

### 2. Identify the intended force of infection from the stated ODE

Read the differential equations stated in the text. For each infection-driven transition, extract the force-of-infection term. Standard mass-action mixing produces terms of the form `(Beta / N) * S * I` (or `(Sigma * Beta / N) * V * I` for partially immune vaccinated individuals). The force of infection always depends linearly on the **infectious** compartment I (or E+I for SEIR-type models).

### 3. Cross-check the hazard variable in the rprocess against the ODE

For each infection-driven transition:
- The `size` argument should match the compartment that is depleted (e.g., `size=V` for V→I transitions).
- The hazard rate in `prob = 1 - exp(-rate * X / N * delta.t)` should have `X = I` (the infectious compartment), regardless of which compartment's members are at risk.

**Error pattern**: `dN_VI <- rbinom(n=1, size=V, prob=1-exp(-Sigma*Beta*V/N*delta.t))` — uses `V` in the hazard, so the transition rate increases as more people are vaccinated, independent of the infectious pool size.

**Correct pattern**: `dN_VI <- rbinom(n=1, size=V, prob=1-exp(-Sigma*Beta*I/N*delta.t))` — uses `I` in the hazard, so vaccination reduces the probability of transition (because V→I depends on infectious contacts, not on vaccinated pool size).

Flag any case where the state variable in the hazard rate is the same as the `size` compartment when the transition is driven by external infection.

### 4. Verify consistency with the stated model equations

Confirm that the stated ODE matches the code:
- ODE: `dV/dt = ... - (sigma*beta/N) * V * I * dt` implies the transition probability `1 - exp(-Sigma*Beta*I/N*delta.t)` applied to a pool of size V.
- Code: If `prob = 1-exp(-Sigma*Beta*V/N*delta.t)`, the effective ODE would be `dV/dt ~ -(Sigma*Beta*V^2/N)`, which is a quadratic-in-V term not in the stated model.

### 5. Assess the impact on parameter estimates

If the wrong variable is in the hazard:
- The fitted `Sigma` and `Beta` parameters absorb the model misspecification. For example, if V >> I (most people vaccinated, few infected), using V instead of I inflates the force-of-infection term, so the optimizer will drive `Sigma` toward zero to compensate.
- Any conclusion about vaccine efficacy derived from the estimated `Sigma` is invalid.
- The profile likelihood for `Sigma` reflects the interaction between the wrong hazard specification and the data, not the true vaccine efficacy.

### 6. Check all other models in the paper for the same error

Multi-model papers often build SIRV variants iteratively. If the first SIRV model has the wrong hazard variable but the second SIRV model corrects it, the comparison between the models' likelihoods reflects both the model structure difference and the code error. Flag this cross-model inconsistency explicitly.

### 7. Report the finding

For each detected instance, report:
- The rprocess chunk and the specific `rbinom` call with the error.
- The correct state variable that should appear in the hazard rate, citing the stated ODE.
- The consequence: the stochastic process model is inconsistent with the stated ODE; parameter estimates (especially vaccine efficacy parameters) are invalid.
- The fix: replace the wrong variable with the correct infectious compartment variable in the hazard rate expression.

## Limitations

- This skill requires cross-reading the ODE statements in the text against the rprocess code. It cannot be detected from the rendered HTML output.
- In some models, the force of infection genuinely depends on multiple compartments simultaneously (e.g., SEIR where both E and I contribute to transmission). In those cases, the combined term is correct and should not be flagged.
- For spatially structured models, the force of infection may involve aggregate terms across spatial units; the same principle applies (hazard should depend on the total infectious pool, not on the susceptible/vaccinated compartment).
- Does not replace the `pomp-accumvar-semantic-audit` skill, which covers the wrong compartment flow being accumulated. Both skills should be applied when reviewing POMP models with vaccination compartments.
