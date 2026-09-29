---
name: pomp-prediction-wrong-params
description: Detect cases where a POMP project correctly computes and stores the MLE parameter vector but then passes a different (typically manually specified) parameter vector to the forward simulation or prediction call, causing reported forecasts to be based on arbitrary rather than estimated parameters — use when reviewing a POMP project that performs prediction or forecasting after a global search.
---

# POMP Prediction Wrong-Parameters Detector

## Purpose

A common POMP workflow computes the MLE by extracting the best-row of a global search result:

```r
params_maxlik = unlist(results_global[which.max(results_global$loglik),])
```

and then uses those parameters for forward simulation or prediction. A recurring error is to assign the MLE to a named variable (`params_maxlik`) but then pass a different, manually specified parameter vector (`params`) to the `simulate()` call used for prediction. Because both `params_maxlik` and `params` are valid named vectors that produce plausible-looking trajectories, the rendered output gives no indication that the wrong parameters were used. The resulting forecast has no valid statistical grounding: it reflects the author's initial parameter guess, not the likelihood-maximizing estimate.

This error is distinct from:
- `pomp-placeholder-result-audit`: that skill covers fabricated numbers; here, genuine computation occurred but the result was not used.
- `pomp-simulate-as-latent-state-inference`: that skill covers simulate() used for latent state visualization; here the error is in the prediction/forecasting call specifically.
- `pomp-forecast-from-initial-conditions`: that skill (if it exists) covers forecasting from estimated initial conditions rather than the filtering distribution; here the issue is which parameter vector is passed, not whether the filtering distribution is used.

## When to Activate

Use this skill when:
- A POMP project runs a global IF2 search and stores the MLE parameters in a named variable (e.g., `params_maxlik`, `best_params`, `mle_params`).
- The project subsequently calls `simulate()` or `forecast()` for prediction purposes.
- The `params=` argument in the simulation/forecast call is a different variable than the stored MLE (e.g., `params` vs. `params_maxlik`).
- The project presents the simulation output as a prediction or forecast based on estimated parameters.

Do not use this skill when:
- The simulation/forecast call correctly passes the MLE variable (e.g., `params=params_maxlik`).
- The project explicitly states that the forward simulation is illustrative and uses a fixed reference parameter set rather than the MLE.
- The simulation is a prior predictive check (before inference) where the MLE is not yet available.

## Procedure

### 1. Identify the MLE variable

Search the Rmd/R source for the global search result extraction:
```r
params_maxlik <- results_global[which.max(results_global$loglik), ]
# or
best_params <- coef(mifs_global[[which.max(logliks)]])
```
Note the variable name used to store the MLE.

### 2. Identify all downstream simulate() or forecast() calls

Search the source for `simulate(`, `forecast(`, or `pfilter(` calls that appear after the global search section. These may be inside or outside stew/bake blocks.

### 3. Check the params= argument of each call

For each simulation/forecast call, identify the `params=` argument:
- **Correct pattern**: `simulate(pomp_object, params=params_maxlik, ...)` — uses the MLE variable.
- **Error pattern**: `simulate(pomp_object, params=params, ...)` — uses a different (often previously defined) variable; `params` was likely defined earlier as the manual simulation guess.

If the error pattern is present, confirm that `params` (the variable actually passed) is a manually specified vector rather than derived from the MLE.

### 4. Assess the consequence for reported forecasts

If the error is confirmed:
- The reported forecast trajectories reflect the manual parameter guess, not the MLE.
- Any conclusion about future case counts, pandemic end dates, or policy-relevant quantities derived from the forecast is statistically invalid.
- Depending on how different `params` is from `params_maxlik`, the forecast may look very different from one based on the MLE — or may coincidentally look similar if the guess happened to be close to the MLE.

### 5. Check for consistent naming confusion throughout the document

Verify whether the variable `params` is reassigned at any point between the simulation-guess definition and the forecast call. In some projects, `params` is overwritten in a later chunk with the MLE values — in that case, the forecast may inadvertently be correct despite the misleading variable name.

### 6. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) of the `simulate()` or forecast call.
- The name of the MLE variable (e.g., `params_maxlik`) and the variable actually passed (e.g., `params`).
- The consequence: the forecast is not based on the MLE; all stated conclusions about the forecast are invalid.
- The fix: replace `params=params` with `params=params_maxlik` (after verifying the vector names match the pomp object's paramnames). If `params_maxlik` includes log-likelihood columns or other non-parameter columns, subset to the parameter names: `params=unlist(params_maxlik[paramnames(pomp_object)])`.

## Limitations

- This skill requires reading the source code; the rendered plot will look visually plausible regardless of which parameter vector was used.
- If the manual `params` guess happened to be close to the MLE (e.g., the simulation-guess was already well-calibrated), the practical impact on the forecast shape may be small — but the error should still be flagged because correctness is not guaranteed.
- Cannot detect this error when the MLE is directly extracted from the mif2 result via `coef(best_mif)` and passed inline to simulate — only detects the pattern where the MLE is stored in a named variable and a different named variable is passed.
- Does not replace the broader forecast methodology check (Wheeler et al. 2024, §Forecast methodology), which also requires that forecasts be conditioned on recent data via the filtering distribution, not just parameterized by the MLE.
