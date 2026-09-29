---
name: pomp-covid-active-case-stock-flow-mismatch
description: Detect cases where a POMP project constructs the observation variable as Confirmed - Deaths - Recovered from a cumulative COVID dataset, yielding active case counts (a stock), then links it to an accumulator variable tracking daily compartment flows (a flow), creating a stock-vs-flow mismatch that invalidates the likelihood and all parameter estimates — use when reviewing a POMP project fitted to COVID case data derived from cumulative-column subtraction.
---

# POMP COVID Active-Case Stock-Flow Mismatch Detector

## Purpose

COVID-19 datasets from sources such as Johns Hopkins, Kaggle, and Our World in Data typically report cumulative totals for Confirmed, Deaths, and Recovered. A common project error is to compute the observation variable as:

```r
data$cases <- data$Confirmed - data$Deaths - data$Recovered
```

This expression yields the number of **currently active infections** — a stock variable that counts how many people are sick on a given day. Because Confirmed, Deaths, and Recovered are all cumulative, their difference is the current prevalence, not a daily incidence flow.

The POMP measurement model is then written to compare this active-case stock to an accumulator variable `H` that is reset at each observation time and accumulates daily compartment flows (e.g., `H += dN_IR` for new recoveries, or `H += dN_EI` for new detections). This creates a stock-vs-flow mismatch:

- The **data** represents a snapshot of how many people are currently infected.
- The **accumulator** represents a count of events that occurred within the current observation period.

These two quantities have different units, different dynamics, and different magnitudes. The parameter `rho` absorbs whatever scaling is needed to make the likelihood numerically large, but at biologically implausible values. All downstream parameter estimates, likelihood values, and model comparisons are unreliable.

This error is distinct from:
- `pomp-accumvar-semantic-audit`: that skill covers cases where the data is a flow variable but the wrong flow is accumulated (e.g., recoveries instead of new detections). Here the data itself is not a flow at all.
- `pomp-smoothed-data-measurement-mismatch`: that skill covers applying rolling means before passing data to pomp. Here the data transformation is a stock-level subtraction, not a smoothing operation.

## When to Activate

Use this skill when:
- A POMP project works with COVID-19 (or similar cumulative-column) data.
- The observation variable is computed as `Confirmed - Deaths - Recovered` or an equivalent subtraction of cumulative columns.
- The POMP model uses an accumulator variable (`accumvars`) to link compartment flows to the observation.
- The measurement model links the accumulator to the observation: `reports ~ NegBin(rho * H, k)`.

Do not use this skill when:
- The observation variable is computed as the daily increment: `diff(Confirmed)` or `Confirmed[t] - Confirmed[t-1]`.
- The POMP measurement model links directly to a state compartment (e.g., `rho * I`) without using an accumulator.
- The dataset provides pre-processed daily new case counts (not cumulative totals) so that subtraction of cumulative columns is not involved.

## Procedure

### 1. Identify how the observation variable is constructed

Read the data preprocessing code. Search for lines of the form:
```r
data$cases <- data$Confirmed - data$Deaths - data$Recovered
data$active <- data$total_cases - data$total_deaths - data$total_recovered
```

Check whether `Confirmed`, `Deaths`, and `Recovered` are cumulative (non-decreasing) or daily increments (could decrease). In standard COVID datasets from Johns Hopkins, WHO, or Kaggle, these are cumulative.

To confirm: print the first few rows and check whether `Confirmed` is monotonically non-decreasing. If so, the subtraction yields active cases (a stock), not new cases (a flow).

### 2. Identify the accumulator variable and what it accumulates

Read the Csnippet rprocess and find `H += ...` (or equivalent). Note which compartment flows are summed into H.

Common error patterns:
- `H += dN_IR_o + dN_IR_b` — accumulates daily recoveries (flow) compared to active cases (stock).
- `H += dN_EI` — accumulates daily new exposures (flow) compared to active cases (stock).

Both are mismatches when the data is a stock variable.

### 3. Assess the direction of the mismatch

Determine the approximate magnitude of the mismatch:
- Active cases (stock): at any time t, roughly equal to the total infectious compartment `I_o + I_b + ...`.
- New recoveries per day (flow H from `dN_IR`): approximately `mu_IR × I`, which is much smaller for typical recovery rates.
- New detections per day (flow H from `dN_EI`): approximately `mu_EI × E`, also smaller than the total active-case stock.

The stock variable is always larger than the daily flow by approximately 1/rate (e.g., if recovery rate is 0.05/day, the stock is ~20× the daily flow). The `rho` parameter will absorb this ratio, but the dynamics differ: the stock declines when recoveries exceed new infections, while the daily recovery flow is always non-negative and does not reflect the stock's trajectory faithfully.

### 4. Determine the correct observation variable

If the data source provides cumulative columns, the correct observation variable for a POMP accumulator is the **daily increment**:
```r
data$new_cases <- c(NA, diff(data$Confirmed))
# or subtract deaths/recoveries if only new confirmed is desired:
data$new_cases <- c(NA, diff(data$Confirmed - data$Deaths - data$Recovered))
# but note: new active cases = new_Confirmed - new_Deaths - new_Recovered
```

Alternatively, if the model's observation variable is intended to be current active cases, the measurement model should compare to the current state variable (e.g., `rho * (I_o + I_b)`) directly, without using an accumulator.

### 5. Report the finding

For each detected instance:
- Cite the code line where `Confirmed - Deaths - Recovered` (or equivalent) is computed.
- Confirm that the columns are cumulative (monotone non-decreasing).
- State which compartment flow H accumulates.
- Explain the magnitude and direction of the mismatch.
- Note that `rho` cannot correct for the difference in dynamics between a stock and a flow.
- Propose the fix: use `diff(Confirmed)` for daily new cases, or link the measurement model directly to the infectious state compartment.

## Limitations

- This skill requires checking whether the source columns are cumulative or daily. Some datasets (e.g., aggregated reports) provide daily counts directly; in that case, `Confirmed - Deaths - Recovered` may not yield active cases.
- In some epidemic models, the data truly is a stock variable (e.g., hospital bed occupancy). In that case, the measurement model should link directly to the corresponding stock compartment, not use an accumulator. This is a valid design and not an error.
- The mismatch may not produce degenerate likelihoods (the particle filter will still run), making it undetectable from rendered output alone. Code reading is required.
- Does not replace `pomp-accumvar-semantic-audit`, which should be applied in addition to this skill when the data is a flow variable.
