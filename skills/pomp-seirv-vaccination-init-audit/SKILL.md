---
name: pomp-seirv-vaccination-init-audit
description: Use when reviewing a pomp SEIRV or similar model that initializes the vaccinated compartment V from a reported population vaccination percentage, to detect the silent error where the Csnippet uses a daily rate change or a percentage-of-a-percentage instead of the cumulative vaccination fraction, producing an initial V value orders of magnitude smaller than the stated value without any runtime error.
---

# pomp SEIRV Vaccination Initialization Audit

## Purpose

When students adapt SEIRV compartmental models from COVID-19 or similar disease contexts, they typically initialize the vaccinated compartment V by citing an external source for the population vaccination percentage. A recurring silent implementation error occurs when the Csnippet arithmetic uses the daily change in vaccination rate (e.g., `N*(0.5945-0.5935)`) or a percentage-of-a-percentage (e.g., `N*0.3*0.01`) rather than the cumulative fraction (e.g., `N*0.5945`). The resulting V is 10 to 1000 times smaller than stated, the susceptible fraction is correspondingly inflated, and all transmission and vaccine-related parameter estimates are distorted. The error produces no runtime warning or error; simulations appear visually plausible because the particle filter compensates through other parameters.

## When to Activate

Use this skill when:
- A pomp SEIRV (or SEIRDV, SEIQRV, or similar) model initializes a vaccinated compartment V inside an rinit Csnippet.
- The text cites a specific vaccination percentage from an external source (e.g., "31.15% of the population was vaccinated").
- The Csnippet uses arithmetic involving that percentage to compute the initial V value.

Do not apply when V is estimated as a free parameter from the data rather than fixed from external vaccination statistics.

## Procedure

### 1. Locate the rinit Csnippet and the V initialization line

Find the rinit Csnippet. Identify the line that sets V (e.g., `V = nearbyint(N*0.3*0.01);`).

### 2. Extract the claimed vaccination percentage from the text

Find the paragraph where the authors state the vaccination level used for initialization (e.g., "31.15% were vaccinated on 2021-05-01").

### 3. Compute the expected V value

Multiply the stated percentage by N: expected_V = N * (percentage / 100) if stated as a percent, or N * fraction if stated as a decimal (e.g., "0.3115").

### 4. Evaluate the Csnippet arithmetic

Substitute numerical values into the Csnippet expression for V and compute the result. Compare against expected_V from Step 3.

Common error patterns:
- `N*0.3*0.01` when the intended value is `N*0.31`: the extra `*0.01` scales down by a factor of 100.
- `N*(0.5945-0.5935)` when the intended value is `N*0.5945`: the subtraction computes the one-day change in rate rather than the cumulative rate.
- `N*pct/100/100` with a double percentage conversion: the percentage is first stored as a whole-number percent (e.g., 31.15) and then divided by 100 twice.

### 5. Check the R (recovered) compartment for downstream effects

If V is initialized incorrectly, the residual R compartment (often computed as `R = N - S - E - I - V - H`) will absorb the error. Verify whether the R initialization is plausible given the expected V value. An R that is implausibly large or negative at t=0 is a secondary symptom of the V initialization error.

### 6. Assess downstream impact on parameter estimates

When V is much smaller than the true vaccinated population:
- The susceptible fraction S is inflated.
- To match observed incidence despite the larger susceptible pool, the optimizer decreases Beta (transmission rate) or increases mu_IR (recovery rate).
- Conversely, the vaccination removal rate alpha will be poorly identified because V is too small to generate a meaningful V->E or V->R flow.
- For models with vaccine-breakthrough pathways (e.g., V-to-E via sigma*Beta), sigma will be unidentifiable because dN_VE is negligible when V is near zero.

### 7. Summarize findings

For each discrepancy found:
- Quote the Csnippet line.
- State the computed value and the expected value.
- Identify the factor by which they differ.
- State which parameters are most likely distorted.
- Propose the corrected expression.

## Limitations

- This skill addresses initialization-scale errors only, not whether the SEIRV model structure itself is appropriate for the disease or time period.
- If V is initialized from a covariate table (not a fixed Csnippet expression), the audit requires tracing the covariate data rather than evaluating Csnippet arithmetic.
- For models where the vaccinated compartment includes multiple dose categories (e.g., partially vs. fully vaccinated), the initialization check becomes more complex; this skill addresses the common single-V case only.
