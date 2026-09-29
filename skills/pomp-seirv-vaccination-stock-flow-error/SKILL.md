---
name: pomp-seirv-vaccination-stock-flow-error
description: Detect two related errors in SEIRV-type POMP models where (1) the vaccinated compartment V is initialized to the incremental change in vaccination rate rather than the cumulative total stock, and (2) the vaccination rate parameter alpha is divided by population N in the hazard, producing a near-zero vaccination flow — use when reviewing a POMP COVID-19 or epidemic model that includes a vaccinated compartment and a vaccination rate parameter.
---

# POMP SEIRV Vaccination Stock-Flow Error Detector

## Purpose

POMP compartmental models that add a vaccinated compartment V to a standard SEIR structure (SEIRV models) require careful attention to two quantities: (1) the initial stock of vaccinated individuals at the start of the modeled period, and (2) the per-capita hazard of vaccination. Two distinct errors frequently co-occur in student projects modeling COVID-19 with vaccination:

**Error 1 — Stock-flow confusion in rinit**: The vaccinated compartment V is initialized using the *incremental change* in the vaccination rate between two dates (a flow, measured in percentage points) rather than the *cumulative total* fraction of the population vaccinated at the start of the period (a stock). For example, if the vaccination rate increased from 30.54% to 31.15% between March 30 and May 1, the author initializes `V = round(N * (0.3115 - 0.3054))` (approximately 0.6% of N) instead of `V = round(N * 0.3115)` (31.15% of N). The result is that V is initialized at roughly 1/50th of its true value, with the difference absorbed into R (computed as a residual), producing a dramatically incorrect susceptible fraction and corrupting all estimated compartment flows.

**Error 2 — Double-normalization of the vaccination hazard**: The per-step vaccination probability is defined as `1 - exp(-alpha / N * dt)`, where alpha is intended as a per-capita daily rate. Dividing by N produces a per-capita-squared rate (with units of 1/person/day), making the daily probability of vaccination approximately `alpha / N` (near zero for population-scale N). With N = 3e8 and alpha = 0.05, the daily vaccination probability per susceptible is approximately 1.67e-10, meaning essentially zero individuals are vaccinated per time step regardless of alpha's estimated value. The correct hazard for a per-capita rate alpha is `1 - exp(-alpha * dt)`.

These errors are distinct from:
- `pomp-covariate-compartment-underflow`: that skill covers a covariate driving a compartment negative during simulation.
- `pomp-residual-compartment-overflow`: that skill covers double-counting in a residual assignment.
- `pomp-static-population-audit`: that skill covers using a fixed N across a long time series.

Here the errors are in the initialization (confusing stock with flow) and in the hazard formulation (erroneously normalizing a per-capita rate by population size).

## When to Activate

Use this skill when:
- A POMP project adds a vaccinated compartment V to an SEIR-type model (SEIRV, SEIRDV, etc.).
- The `rinit` Csnippet initializes V using an expression involving the difference between two vaccination-rate percentages (e.g., `V = round(N * (p2 - p1))`), where `p1` and `p2` are both small fractions (both less than 1).
- The rprocess Csnippet defines a vaccination flow as `dN_SV = rbinom(S, 1 - exp(-alpha / N * dt))` or similar with a `/N` term in the hazard.

Do not use this skill when:
- The model correctly initializes V as `V = round(N * cumulative_vaccination_fraction)` where the cumulative fraction matches the documented vaccination prevalence at the start of the period.
- The hazard correctly omits the `/N` term: `dN_SV = rbinom(S, 1 - exp(-alpha * dt))`.
- The vaccination rate is modeled as a time-varying covariate (covariate_table) rather than a constant parameter.

## Procedure

### 1. Identify the V initialization in rinit

Read the `rinit` Csnippet. Find the assignment to V. Extract the numerical expression:
- Is it `round(N * fraction)` where `fraction` is the cumulative vaccination rate at the start of the period?
- Or is it `round(N * (p2 - p1))` where `p2 - p1` is a small increment (e.g., 0.006 rather than 0.31)?

Compare the resulting V value to the reported vaccination prevalence in the text:
- If the text states X% of the population was vaccinated, V should be approximately `N * X/100`.
- If the computed V is smaller than this by a factor of > 10, flag as a stock-flow confusion error.

### 2. Compute the magnitude of the initialization error

Calculate the correct V (stock) and the initialized V (flow-based):
- **Correct V**: `N * cumulative_fraction` (e.g., `3e8 * 0.31 = 93,000,000`).
- **Initialized V**: `N * delta_fraction` (e.g., `3e8 * 0.006 = 1,800,000`).
- **Error factor**: correct / initialized (e.g., 93,000,000 / 1,800,000 ≈ 52).

If the error factor exceeds 10, flag as a major issue. Note that the residual compartment (typically R) absorbs the missing individuals, so R is inflated by the same amount.

### 3. Check the vaccination hazard in rprocess

Read the rprocess Csnippet. Find the line computing the vaccination flow:
- Does it have the form `rbinom(S, 1 - exp(-alpha / N * dt))`?
- If `/N` is present, compute the daily vaccination probability at the starting parameter value:
  `p = 1 - exp(-alpha_init / N)` where alpha_init is the starting value used in the simulation.
- If `p < 1e-6` (i.e., essentially zero), flag as a double-normalization error.

### 4. Verify the impact on model dynamics

If both errors are present:
- V is initialized near zero rather than at the true vaccinated count.
- V grows at a negligible rate per time step (near-zero flow from S to V).
- The vaccinated compartment is effectively dormant throughout the simulation.
- The parameter alpha is non-identifiable: any value of alpha produces nearly identical dynamics because the vaccination flow is near zero regardless.
- The model reduces in practice to a standard SEIR without vaccination, even though vaccination was the scientific motivation for the SEIRV extension.

### 5. Check whether the R residual is plausible

If V is severely under-initialized, the R compartment (often computed as a residual `R = round(N*(1-eta) - E - I - H - V)`) will be inflated by the amount of true V that is not in V. Check whether this produces a plausible initial epidemic state:
- Is R approximately equal to N * cumulative_prior_infection_fraction?
- Or does it encompass both recovered individuals AND the ~90%+ of vaccinated population, making the R compartment a mixture of biologically distinct groups?

If R absorbs both true recovered and true vaccinated individuals, the model cannot distinguish protection from natural infection from protection from vaccination, undermining the motivation for the SEIRV extension.

### 6. Report the findings

For each detected instance, report:
- The specific line in rinit where V is initialized, and the computed value.
- The correct value (using the stated cumulative vaccination fraction from the text).
- The specific line in rprocess containing the double-normalized hazard, and the computed daily probability.
- The consequence: V is dormant; alpha is non-identifiable; the SEIRV model reduces to SEIR; the R compartment conflates recovered and vaccinated individuals.
- The fix: (a) set `V = round(N * cumulative_fraction)` in rinit; (b) change the hazard to `rbinom(S, 1 - exp(-alpha * dt))` in rprocess.

## Limitations

- This skill requires knowledge of the documented vaccination prevalence at the start of the modeled period. If the paper does not state this value, the magnitude of the initialization error cannot be computed precisely — but the pattern `V = round(N * (p2 - p1))` where both p1 and p2 are small fractions is still sufficient to flag the issue.
- In some models, `p2 - p1` intentionally represents a *daily* vaccination rate (the fraction newly vaccinated on a given day), not a cumulative difference. In that case the initialization to a flow quantity may be intentional; confirm by checking whether the text explicitly says "daily rate" or "cumulative fraction."
- The double-normalization error (dividing alpha by N in the hazard) does not apply if the model defines alpha in units of vaccinations-per-day-per-total-population (i.e., with N already incorporated into the units). In that case the `/N` is correct. This interpretation is unusual but should be checked against the paper's parameter definitions.
- Does not replace the full POMP checklist §11 (Corroboration with scientific knowledge) check on whether parameter estimates match independent biological evidence.
