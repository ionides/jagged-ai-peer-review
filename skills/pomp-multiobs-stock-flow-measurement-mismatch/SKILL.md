---
name: pomp-multiobs-stock-flow-measurement-mismatch
description: Detect cases where a POMP model with multiple observation series has rmeasure and dmeasure that apply a stock variable (cumulative compartment count) and a flow variable (daily increment) asymmetrically across the two snippets for the same observation channel, causing the simulated data and likelihood to reflect different models — use when reviewing a POMP project with two or more observation variables where one snippet adds or subtracts a cumulative state compartment while the other uses the corresponding observed daily count.
---

# POMP Multi-Observation Stock/Flow Measurement Mismatch Detector

## Purpose

POMP models of infectious diseases sometimes track two observation series simultaneously (e.g., reported cases and deaths). When a model includes a cumulative compartment (e.g., `D` = total cumulative deaths) alongside an accumulator (e.g., `H` = new recoveries in the current observation window), it is possible to introduce an asymmetry between `rmeasure` and `dmeasure` that is not covered by the existing single-observation measurement model skills:

- `rmeasure` computes simulated cases as `rnorm(mean_cases, sd_cases) + D`, adding the cumulative deaths stock to the simulated flow-based case count.
- `dmeasure` evaluates the likelihood as `dnorm(cases - deaths, mean_cases, sd_cases)`, subtracting the observed daily death count (a flow) from the observed cases.

These two expressions are equivalent only if `D` (the cumulative deaths compartment in the particle state) equals the observed `deaths` variable (a daily flow) at every time step. In general they are not equal:
- `D` is a non-decreasing stock that grows throughout the epidemic.
- `deaths` (the observed variable) is a daily count that rises and falls with epidemic intensity.

This produces a mismatch where the simulated observation from `rmeasure` has a systematically different distribution than the density being evaluated in `dmeasure`, making the particle filter weights invalid and all IF2-estimated parameters unreliable.

This error is distinct from:
- `pomp-dmeas-rmeas-scale-inconsistency`: that skill covers different rescalings of the same state variable in a single-observation model.
- `pomp-dmeas-rmeas-moment-mismatch`: that skill covers different moment formulas for the same distributional family in a single-observation model.
- `pomp-inference-misuse`: that skill covers different distributional families between dmeas and rmeas.
- `pomp-covid-active-case-stock-flow-mismatch`: that skill covers the observation variable being a stock (active cases) while the accumulator tracks a flow.

Here the observation variable is correctly a flow (daily cases), but the rmeasure incorrectly adds a stock variable (`D`) to it, while dmeasure correctly subtracts a flow variable (observed deaths).

## When to Activate

Use this skill when:
- A POMP project defines both `rmeasure` and `dmeasure` for a model with two or more observation variables (e.g., cases and deaths).
- The model includes a cumulative compartment (e.g., `D` for total deaths, `R` for total recoveries) alongside an accumulator variable (e.g., `H` for new cases within the period).
- The `rmeasure` Csnippet adds or subtracts the cumulative compartment (stock) to one of the simulated observation variables.
- The `dmeasure` Csnippet adds or subtracts the corresponding observed daily count (flow) to compute the effective observation to evaluate the density against.

Do not use this skill when:
- The model has only a single observation series and no cumulative compartments appear in the measurement model.
- Both snippets use the same compartment (stock or flow) consistently for the same observation variable.
- The cumulative compartment appears only in the process model, not in the measurement snippets.

## Procedure

### 1. Identify all observation variables and compartments in the measurement model

Read the `rmeasure` and `dmeasure` Csnippets. List:
- All observed variables referenced (e.g., `cases`, `deaths`).
- All state compartments referenced (e.g., `H`, `D`, `R`, `I`).
- Whether each state compartment is a flow accumulator (declared in `accumvars` or reset at each observation time) or a cumulative stock (monotone increasing throughout the epidemic).

### 2. For each observation variable, compare how it is computed in rmeasure vs. how it is evaluated in dmeasure

For rmeasure:
- What expression defines the simulated value of each observed variable?
- Does it add or subtract a cumulative compartment?

For dmeasure:
- What expression is evaluated against the density function?
- Does it add or subtract an observed data column (which is a flow, measured at that time step)?

### 3. Check whether the rmeasure expression equals the dmeasure expression for the same particle state

Substitute concrete values to test consistency:
- Let `H = 500` (new recoveries today), `D = 10000` (cumulative deaths since epidemic start), `rho = 0.5`.
- Compute rmeasure's mean_cases and the additional term it adds (e.g., `mean_cases + D = 250 + 10000 = 10250`).
- Compute dmeasure's effective observation: if `cases = 5000` observed and `deaths = 50` observed deaths today, then `cases - deaths = 4950`.
- The density is evaluated at `cases - deaths = 4950` but the simulated expected value is `mean_cases + D = 10250`.

If these are of different orders of magnitude for typical epidemic states, the mismatch is severe.

### 4. Identify whether the mismatch is one-directional or bidirectional

- **One-directional**: only one observation variable has the stock/flow mismatch; the other is consistent.
- **Bidirectional**: both observation variables suffer from the mismatch.

Flag one-directional mismatches as major issues and bidirectional mismatches as critical issues.

### 5. Assess the impact on inference

If confirmed:
- The particle filter evaluates likelihoods for the dmeasure model (which computes a sensible quantity) while forward simulations come from the rmeasure model (which adds a large cumulative stock).
- Simulated trajectories will appear wildly different from the data (e.g., simulated cases inflated by the growing cumulative deaths stock), making visual goodness-of-fit assessments misleading.
- IF2 will converge to parameters that maximize the dmeasure log-likelihood, which may be reasonable, but all simulation-based outputs (predictions, residuals) will be invalid.
- The `rho` parameter and the variance parameter will absorb whatever scaling is needed, potentially at biologically implausible values.

### 6. Propose the fix

Identify the intended observation model and make both snippets consistent:
- If the intent is to model daily new cases with a Gaussian distribution centered on `rho * H`:
  - `rmeasure`: `cases = rnorm(rho * H, sd_cases)`; `deaths = D` (or whatever death model).
  - `dmeasure`: `lik = dnorm(cases, rho * H, sd_cases, give_log)` (no subtraction of deaths from cases).
- If the intent is to model `cases - deaths` (net new infections surviving):
  - `rmeasure`: `cases = rnorm(rho * H, sd_cases) + rnorm(death_mean, death_sd)` (simulate cases and deaths separately).
  - `dmeasure`: `lik = dnorm(cases - deaths, rho * H, sd_cases, give_log)`.

Ensure both snippets use the same stock-vs-flow variable for each term.

### 7. Report the finding

For each detected instance:
- Quote the specific lines in rmeasure and dmeasure that define the mismatched expressions.
- Provide a concrete numerical example at typical epidemic-peak state values showing the magnitude of the mismatch.
- State the consequence: simulations and likelihood evaluations reflect different models; all parameter estimates and goodness-of-fit plots are invalid.
- Propose the fix (see Step 6).

## Limitations

- This skill requires side-by-side reading of rmeasure and dmeasure in the context of the full state vector; it cannot be detected from rendered HTML output.
- If the epidemic duration is short, the cumulative stock `D` may be close to the daily count `deaths` near the epidemic peak, making the mismatch numerically mild even though it is conceptually present. Assess the magnitude with concrete values before flagging severity.
- Does not replace the other dmeas/rmeas consistency checks (`pomp-inference-misuse`, `pomp-dmeas-rmeas-moment-mismatch`, `pomp-dmeas-rmeas-scale-inconsistency`); all should be applied when reviewing multi-observation POMP measurement models.
- In some models, the death compartment is deliberately added to the simulated cases count to represent total burden. If the authors explicitly state this interpretation and the dmeasure is consistently specified, this is not an error. Only flag when the two snippets use inconsistent representations.
