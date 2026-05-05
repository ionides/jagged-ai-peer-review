---
name: pomp-internal-compartment-role-audit
description: Use when reviewing a pomp model that adds non-standard compartments beyond S/E/I/R (e.g., dead-not-buried, funeral, hospitalized, quarantined) to detect the silent error where an internal compartment is updated as a per-step flow (assignment from a transition count) but subsequently used as a stock in a rate expression — producing a model that compiles and runs but misrepresents the biological dynamics of the extended compartment.
---

# pomp Internal Compartment Role Audit

## Purpose

Extended compartmental models for diseases like Ebola (SEIRDF), Cholera (SIWR), or COVID-19 (SEIQR) add compartments beyond the standard SEIR structure to represent biologically relevant states — funerals, water reservoirs, quarantine, dead-not-yet-buried individuals. These compartments often have a dual character: they receive individuals from a flow (e.g., daily deaths flowing into a funeral compartment) and also act as a stock that drives future transitions (e.g., the number of ongoing funerals driving susceptible exposure).

A silent misspecification occurs when the Csnippet updates such a compartment via assignment from a per-step transition count (`F = round(dN_DF)`) but then uses it in a rate expression that assumes stock-like persistence (`rbinom(F_size * F, 1 - exp(-Beta2 / F_size * dt))`). Under the assignment convention, F represents only funerals beginning at this exact time step and resets to zero when no deaths occur. The biological reality is that funerals persist for multiple days (the duration of burial rites), so the stock should accumulate deaths over a biologically plausible window and decay at a rate corresponding to funeral duration.

This error does not trigger a runtime warning. Simulations will run and produce trajectories, but the non-standard compartment is effectively marginalized: on most time steps, the per-step assignment produces F = 0 and the extended transmission pathway is switched off.

## When to Activate

Use this skill when:
- A pomp model extends the standard SEIR structure with a compartment that represents a persistent biological state (e.g., dead-not-buried, funeral congregation, water reservoir, quarantine ward).
- The rprocess Csnippet updates this compartment with an assignment (`C = round(dN_XY)`) rather than an accumulation (`C += dN_XY`) or a differential equation (`C += dN_XY - dN_YZ`).
- A subsequent rate expression in the same Csnippet multiplies or conditions on the current value of that compartment as a stock (e.g., `rbinom(C * size_factor, ...)`).

Do not use this skill for the measurement accumulator H — that case is covered by `pomp-csnippet-audit` and `pomp-seir-accumulator-convention`.

## Procedure

### 1. Identify all non-standard compartments

Read the statenames argument of the pomp() call. List all compartment names beyond S, E, I, R. For each, identify its biological interpretation from the model description.

### 2. Classify each compartment as flow, stock, or hybrid

For each non-standard compartment C:
- **Flow**: C represents events occurring at this time step only (e.g., new deaths today). Correct update: `C = dN_XY` (reset each step). Correct downstream use: nowhere in the same step's rate expressions (only in dmeas if C is the measurement accumulator).
- **Stock**: C represents individuals currently in the state (e.g., individuals currently in funeral rites). Correct update: `C += dN_XY - dN_YZ` (net inflow minus outflow). Correct downstream use: in rate expressions as a population size or force-of-infection multiplier.
- **Hybrid**: C is assigned a flow value but used downstream as a stock — this is the error pattern.

### 3. Cross-reference each compartment's update rule against its downstream uses

For each non-standard compartment C:
- Find all lines in the Csnippet where C appears on the right-hand side of an expression (downstream uses).
- Compare: if C is updated by assignment (`C = ...`) but used as a stock in a rate expression, flag as a hybrid error.
- Quote both the update line and the downstream use line.

### 4. Assess the biological consequence of the misspecification

For each flagged compartment:
- Estimate the fraction of time steps where the compartment would be zero under the assignment convention (equal to the fraction of steps with no relevant transition occurring).
- State the effect on the associated transmission pathway: if C is frequently zero, the pathway is effectively disabled.
- Compare to the intended biological role: if funerals are supposed to persist for several days, but F resets to zero after one step, the funeral transmission route is drastically underrepresented.

### 5. Propose the correct implementation

For each flagged compartment:
- If the compartment should be a stock with persistence: implement as a differential equation with inflow from the transition and outflow at a biologically motivated rate. Example for a funeral compartment with mean duration 1/mu_F days: `F += dN_DF - dN_FO` where `dN_FO = rbinom(F, 1 - exp(-mu_F * dt))`.
- If the compartment should be a pure flow (events this step only): remove it from downstream rate expressions and ensure it is not used as a stock.

### 6. Check whether the compartment should be in accumvars

If the compartment is intended as a measurement accumulator (used in dmeas/rmeas), verify it appears in `accumvars`. If it is an internal stock (not directly observed), verify it does not appear in `accumvars` (which would reset it after each observation, destroying its memory).

## Limitations

- This skill requires understanding the biological interpretation of each compartment, which must come from the model description and the literature. Without knowing whether F represents "active funerals" (stock) or "funerals initiated today" (flow), the audit cannot classify the error.
- In models with very short time steps (delta.t << 1 day), a per-step assignment may approximate a stock if transitions are dense enough. Assess whether the time step is short enough to make this approximation valid before flagging.
- This skill does not address whether the compartment's biological interpretation is appropriate for the disease — only whether the code implementation is consistent with that interpretation.
- Models using ODEs (deterministic process models) instead of Euler-multinomial Csnippets have equivalent issues but require reading the derivative expressions rather than Csnippet assignments.
