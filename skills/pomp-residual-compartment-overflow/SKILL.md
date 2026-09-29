---
name: pomp-residual-compartment-overflow
description: Detect cases where a POMP rprocess Csnippet computes one compartment as the population residual (e.g., R = pop - S - E - I) and then adds an extra term to it (e.g., + vac, + immigrants) that was already subtracted from another compartment, causing the total compartment sum to exceed the true population and violating conservation — use when reviewing a POMP model that adds a vaccination or immigration term to a residual compartment assignment.
---

# POMP Residual Compartment Overflow Detector

## Purpose

Compartmental POMP models frequently track one compartment (typically R, the recovered class) as the population residual: `R = pop - S - E - I`. This assignment enforces exact population conservation without needing to explicitly track deaths or waning immunity in R. A recurring error occurs when an author modifies this residual formula by appending an additional flow term — most commonly vaccination — to produce `R = pop - S - E - I + vac`. Because vaccinated individuals are simultaneously subtracted from S in the same Euler step, the `vac` quantity has already been removed from the S compartment before R is computed. Adding `vac` again on the right-hand side of R's assignment double-counts these individuals, causing the total N to grow by `vac` at every observation step:

```
S_new + E_new + I_new + R_new = (S_new + E_new + I_new) + (pop - S_new - E_new - I_new + vac) = pop + vac
```

This is biologically incorrect. The force-of-infection denominator `pop` is now smaller than the actual total compartment count, distorting transmission rates. The susceptible fraction is also incorrect because the inflated R reduces the apparent susceptible pool. All parameter estimates — especially R0, rho, and the vaccination rate — are unreliable.

This error is distinct from:
- `pomp-static-population-audit`: that skill covers using a fixed N across a long series. Here the issue is that the total of compartments dynamically exceeds N.
- `pomp-covariate-compartment-underflow`: that skill covers a covariate making a compartment go negative. Here the compartment is positive but inflated.
- `pomp-accumvar-semantic-audit`: that skill covers the wrong compartment flow being accumulated. Here the error is in the compartment state itself, not the accumulator.

## When to Activate

Use this skill when:
- A POMP rprocess Csnippet computes one compartment as the population residual using the pattern `R = pop - S - E - I` (or analogous for other compartments).
- The same Csnippet also defines a vaccination, immigration, or waning-immunity flow that is subtracted from another compartment (e.g., `S -= vac`) in the same step.
- The residual formula is augmented with a `+ vac` (or similar) term: `R = pop - S - E - I + vac`.

Do not use this skill when:
- R is tracked as a differential state (e.g., `R += trans[4] + vac - mu*R`) rather than as a residual assignment.
- The additional term in the residual formula represents deaths entering from outside the system (net immigration), provided the population denominator `pop` is correspondingly updated.
- The model explicitly allows population growth (e.g., an open population model where pop is itself a covariate), and the author acknowledges that total N increases over the simulation period.

## Procedure

### 1. Identify the residual compartment assignment

Search the rprocess Csnippet for assignments of the form:
```c
R = pop - S - E - I;
```
or in multi-variant models:
```c
R = pop - S - E1 - E2 - I1 - I2;
```
Note all terms on the right-hand side.

### 2. Identify extra additive terms in the residual

Check whether the residual assignment includes any term that is also subtracted from another compartment in the same Euler step. Common patterns:
- `R = pop - S - E - I + vac;` combined with `S -= vac;`
- `R = pop - S - E - I + immigrants;` combined with external immigration subtraction.

If such a term exists, flag it as a candidate for double-counting.

### 3. Verify the double-counting by population accounting

Compute the algebraic sum `S_new + E_new + I_new + R_new` symbolically. If the result equals `pop + vac` (or `pop + extra_term`) rather than `pop`, the conservation violation is confirmed.

### 4. Assess the impact on parameter estimates

When total N exceeds pop by a cumulative amount proportional to vac:
- The force of infection `beta * I / pop` uses a denominator smaller than the true total count, inflating the effective transmission rate. This will drive R0 estimates upward.
- The apparent susceptible fraction (S / pop) is smaller than the true fraction if the extra individuals in R dilute the susceptible pool. This compounds the R0 distortion.
- The reporting rate rho absorbs whatever scaling mismatch results from the inflated population.

### 5. Identify the correct fix

Two correct approaches:

**Option A — track vaccination as a flow into R:**
```c
// Remove the + vac from the residual, track R explicitly:
S += births - trans[0] - trans[1] - vac;
E += trans[0] - trans[2] - trans[3];
I += trans[2] - trans[4] - trans[5];
R = pop - S - E - I;  // pop is conserved; vac is already reflected via S reduction
```

This approach relies on the residual to maintain conservation; vaccinated individuals flow from S to R through the conservation equation.

**Option B — track R as a differential state:**
```c
double dR_vac = vac;
double dR_recovery = trans[4];
double dR_death = mu * R * dt;  // or reulermultinom for R deaths
S += births - trans[0] - trans[1] - dR_vac;
E += trans[0] - trans[2] - trans[3];
I += trans[2] - trans[4] - trans[5];
R += dR_vac + dR_recovery - dR_death;
```

This approach removes the residual assignment entirely and tracks all flows explicitly.

### 6. Report the finding

For each detected instance, report:
- The specific line in the Csnippet with the augmented residual.
- The compartment from which the extra term was already subtracted.
- The algebraic proof that total N = pop + extra_term.
- The consequence: force-of-infection denominator is misspecified; all rate parameters are distorted.
- The fix (Option A or B above).

## Limitations

- This skill requires symbolic population accounting; it cannot be detected from the rendered HTML output (the model runs without error and produces plausible-looking simulations).
- In some models, `pop` itself is updated at each step (e.g., births increment pop before the residual assignment). In that case, the residual formula may be intentionally different from the static-N version; confirm that `pop` update semantics are consistent before flagging.
- If vac is typically very small relative to pop (e.g., vac ≈ 100 out of N ≈ 10^7), the practical impact on parameter estimates may be small. However, the conceptual error is present regardless and should be flagged.
- Does not replace the full POMP checklist §9 (Stochasticity) or §11 (Corroboration with scientific knowledge); those checks address whether parameter estimates are plausible given the (possibly distorted) model output.
