---
name: pomp-covariate-compartment-underflow
description: Detect cases where a POMP rprocess Csnippet subtracts a covariate value (e.g., daily vaccinations, immigration, deaths from external cause) from a compartment without a non-negativity guard, allowing the compartment to go negative when the covariate exceeds the current compartment size — use when reviewing a POMP model that incorporates a time-varying covariate as a direct additive or subtractive flow on a state compartment.
---

# POMP Covariate Compartment Underflow Detector

## Purpose

POMP compartmental models sometimes incorporate time-varying covariates as direct flows into or out of compartments. A common example is vaccination, where a covariate `IM` representing daily newly-fully-vaccinated individuals is subtracted from the susceptible compartment S at each time step (`S -= dN_SE + IM`). If `IM` can ever exceed the current susceptible count (S - dN_SE), the Euler step produces a negative compartment value. Negative compartment values are biologically nonsensical and cause cascading errors: subsequent binomial or negative-binomial draws from a negative size argument are undefined (or silently return 0), the particle filter degenerates, and likelihood estimates are corrupted.

This error is distinct from:
- `pomp-static-population-audit`: that skill covers using a fixed N across a long time series. Here the issue is the Euler step producing negative values dynamically.
- `pomp-accumvar-semantic-audit`: that skill covers the wrong compartment flow being accumulated. Here the issue is the size of an external covariate flow exceeding the available compartment stock.
- `pomp-global-search-box-domain-violation`: that skill covers parameter domain violations at initialization. Here the violation occurs dynamically during forward simulation.

## When to Activate

Use this skill when:
- A POMP rprocess Csnippet subtracts a covariate from a compartment (e.g., `S -= IM`, `S -= dN_SE + IM`, `R += IM`).
- The covariate is time-varying and loaded from a `covariate_table()` — so its value at any given time step depends on external data, not the model state.
- The covariate is unbounded by the current compartment size (i.e., no `min(IM, S)` or equivalent guard is applied before subtraction).
- The covariate can realistically exceed the compartment size at some time steps (e.g., during peak vaccination rollout, when most remaining susceptibles are vaccinated in a short period).

Do not use this skill when:
- The covariate is a rate (not a count), multiplied by the compartment size before subtracting (e.g., `S -= sigma * IM * S`), which is self-limiting.
- The code includes an explicit clamp or guard (e.g., `double depart = fmin(IM, S - dN_SE); S -= dN_SE + depart;`).
- The covariate is always much smaller than the compartment size for the entire simulated time range (e.g., a small immigration flow into a large population with short series).

## Procedure

### 1. Identify covariate-driven compartment flows

Read the rprocess Csnippet. Search for lines of the form:
```c
S -= IM;
S -= dN_SE + IM;
R += IM;
```
or equivalently any additive adjustment to a compartment using a covariate variable (a variable that appears in the covariate_table but not in paramnames or statenames).

### 2. Confirm the covariate is unbounded relative to the compartment

Check the covariate_table definition and the raw covariate data:
- What is the maximum value of the covariate over the time series?
- What is the minimum value of the affected compartment (e.g., S) expected during the model run?
- If max(covariate) > expected_min(S), underflow is possible.

For vaccination covariates applied to S: near the end of the vaccination campaign, S may have shrunk to a small number while the daily vaccination rate remains high (many of the newly vaccinated may already be in R from natural infection). This makes underflow likely in the late time steps.

### 3. Check for a non-negativity guard

Search the Csnippet for guards such as:
```c
double net_depart = fmin(IM, S - dN_SE);
S -= dN_SE + net_depart;
R += dN_IR + net_depart;
```
If no such guard is present, flag the underflow risk.

### 4. Assess the impact on model output

If negative compartment values can occur:
- Binomial draws `rbinom(S, prob)` with S < 0 are undefined in C (the R implementation of `rbinom` returns `NaN` or 0 for negative size, but behavior may vary across compilers).
- The particle filter likelihood `dbinom(reports, H, rho)` will be evaluated at NaN states, producing -Inf log-likelihoods or NaN.
- Particle degeneracy: particles that hit negative states are assigned zero weight, degrading the effective sample size and potentially causing filter collapse.
- IF2 convergence: the optimizer may avoid parameter regions where underflow frequently occurs, biasing parameter estimates toward regions where S stays positive — not necessarily the biologically correct region.

### 5. Propose the fix

Recommend adding a non-negativity guard at the covariate flow step. For a vaccination scenario:
```c
double actual_IM = fmin(IM, fmax(S - dN_SE, 0.0));
S -= dN_SE + actual_IM;
R += dN_IR + actual_IM;
```
This ensures that at most the available susceptibles are vaccinated per step, and the compartment size remains non-negative. Note: if `IM` represents external data on vaccinated persons, capping it introduces a discrepancy between the covariate and the modeled flow — this should be noted as a model limitation.

### 6. Report the finding

For each detected instance, report:
- The Csnippet line where the uncapped covariate is subtracted.
- The covariate variable name and its data source.
- Whether the covariate value can realistically exceed the compartment size during the simulation.
- The consequence: negative compartment values corrupt the particle filter, bias parameter estimates, and may produce silent NaN likelihoods.
- The fix: add an explicit non-negativity guard capping the covariate flow at the available compartment stock.

## Limitations

- Assessing whether underflow actually occurs requires knowledge of the covariate magnitude and the expected compartment trajectory at the estimated parameters. If the reviewer does not have access to the covariate data or the simulation output, the risk can only be flagged as potential rather than confirmed.
- For models where compartments are on a very large scale (e.g., S ~ 10 million) and covariates are small (e.g., daily vaccination counts ~ 1,000), the underflow risk is negligible even without a guard; apply judgment based on the ratio of covariate to compartment size.
- Does not cover cases where the process model uses stochastic draws (e.g., `rbinom(S, prob)`) that are themselves bounded by S — those are inherently self-limiting and cannot produce negative values from the stochastic draw alone, only from a subsequent deterministic covariate subtraction.
- Does not replace the `pomp-static-population-audit` skill (which addresses fixed-N bias) or the `pomp-accumvar-semantic-audit` skill (which addresses the wrong flow being tracked).
