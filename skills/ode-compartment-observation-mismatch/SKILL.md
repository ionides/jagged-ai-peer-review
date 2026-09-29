---
name: ode-compartment-observation-mismatch
description: Detect cases where a deterministic ODE SIR/SEIR model is fitted by matching the wrong compartment (e.g., the currently-infectious I compartment) to the wrong type of observed data (e.g., cumulative reported cases), causing a monotonically-increasing data series to be matched against a hump-shaped compartment trajectory — use when reviewing a project that fits an ODE model to epidemic data via optim() or similar and plots the fitted compartment alongside observed counts.
---

# ODE Compartment-to-Observation Semantic Mismatch Detector

## Purpose

When fitting a deterministic ODE compartmental model (SIR, SEIR, etc.) to epidemic surveillance data, the choice of which model compartment to compare to observed data is critical. A common error is to match the `I(t)` compartment (currently infectious individuals — a prevalence measure that rises then falls) to cumulative reported cases (a monotonically increasing incidence measure). Because cumulative cases always increase while `I(t)` eventually decreases, these quantities are incommensurable: the best-fit parameters under RSS will produce a trajectory that peaks and falls even when the data has not yet peaked, or vice versa. The optimizer will still find a minimum, but the resulting parameter estimates reflect a compromise between two irreconcilable quantities rather than the true transmission dynamics.

This error is distinct from:
- `pomp-accumvar-semantic-audit`: that skill covers accumulating the wrong flow in a POMP accumulator variable. Here, the error occurs at the ODE level without a POMP accumulator.
- `pomp-inference-misuse`: that skill covers stochastic simulation-based cost functions in POMP. Here, the model is a deterministic ODE with a deterministic SSE cost.

The two observable manifestations are: (1) the visual plot shows the fitted compartment curve rising and falling while the observed cumulative data continues to rise — the curves can only cross once, and (2) the fitted model claims to predict a pandemic "peak" at a time that has already passed even though cumulative cases continued increasing afterward.

## When to Activate

Use this skill when:
- A project fits an ODE compartmental model to epidemic data via `optim()` or `nls()` minimizing a sum-of-squares or similar cost function.
- The cost function compares a model compartment (typically `I` or `I+E`) to an observed data column.
- The observed data is cumulative incidence (monotonically non-decreasing) while the model compartment being matched is a prevalence measure (rises then falls).
- The visual plot shows the model trajectory intersecting the data curve at most twice (once on the way up, once on the way down) while the data continues upward.

Do not use this skill when:
- The model correctly compares cumulative model incidence (`S(0) - S(t)` or the running sum of `dS/dt`) to cumulative reported cases.
- The model uses new daily cases (`-dS/dt` or the incidence flow `beta*S*I/N`) compared to new daily case counts.
- The project explicitly acknowledges the compartment-to-observation mapping and provides justification.

## Procedure

### 1. Identify the observed data type

Read the data description to determine whether the observation variable is:
- **Cumulative incidence**: total cases reported from epidemic start to time t (monotonically increasing).
- **New incident cases**: daily or weekly new case counts (non-monotone).
- **Prevalence**: number of currently active cases (non-monotone).

### 2. Identify which model compartment is used in the cost function

Locate the cost function (RSS or similar) in the source code. Identify which column of the ODE output is extracted and compared to the observed data. In R using `deSolve::ode()`, the output typically has columns named `time`, `S`, `I`, `R` (or `E`, `H`, etc.).

### 3. Check the semantic consistency

Compare the data type (Step 1) to the model compartment (Step 2):

| Data type | Correct compartment to match |
|-----------|------------------------------|
| Cumulative incidence | `S(0) - S(t)` = total removed from susceptible pool |
| New daily/weekly cases | Incidence flow `= beta*S*I/N * dt` over observation period |
| Current active cases (prevalence) | `I(t)` (or `I(t) + E(t)` for SEIR) |

- **Error pattern**: `I(t)` matched to cumulative incidence. Flag as major issue.
- **Error pattern**: `R(t)` matched to cumulative incidence when R counts only recovered (not cumulative removed). For a standard SIR where R = recovered + removed, `R(t)` may equal `S(0) - S(t) - I(t)` and still not equal cumulative cases due to the I compartment term.

### 4. Examine the visual output for the signature mismatch

In the rendered plot:
- Does the fitted compartment curve peak and then decline while the observed cumulative data continues to rise?
- Do the fitted curve and observed data intersect at most twice, with the data curve remaining above the fitted curve after the second crossing?

Both patterns confirm a semantic mismatch.

### 5. Assess the impact on parameter estimates

If the mismatch is confirmed:
- The transmission rate `beta` and recovery rate `gamma` are distorted to minimize the RSS between incommensurable quantities. The resulting estimates have no epidemiological interpretation.
- The predicted "peak" of the epidemic from the model reflects the optimized compromise between the rising and falling phases of `I(t)` against the monotonically rising cumulative data — not the true epidemic peak.
- All policy-relevant conclusions (e.g., "the virus reached its peak in February") derived from the fitted model are invalid.

### 6. Propose the fix

Specify the correct compartment or derived quantity to use:
- For cumulative reported cases: replace the RSS cost with `sum((dat$CumulativeCases - (N - S(t)))^2)` where `N - S(t)` is the total number of individuals ever infected.
- For new daily cases: add an incidence accumulator to the ODE system (e.g., `dC/dt = beta*S*I/N`) and compare `C(t) - C(t-1)` to the daily case count.

## Limitations

- This skill requires knowing the data type (cumulative vs. incident). For some surveillance systems, the data source description is ambiguous; in that case, inspect the data for monotonicity (cumulative data never decreases; incident data can).
- If the epidemic is still in its early rising phase at the time of fitting, the mismatch between `I(t)` and cumulative cases may be less visually obvious because both are increasing — but the extrapolation to a "peak" is still invalid.
- Does not cover the case where the correct compartment is matched but the data has a structural break (e.g., change in testing policy mid-series) — that is a data quality issue, not a model specification error.
- Does not replace the POMP checklist item 11 (corroboration with scientific knowledge); this skill focuses specifically on the compartment-to-observation semantic mismatch in deterministic ODE contexts.
