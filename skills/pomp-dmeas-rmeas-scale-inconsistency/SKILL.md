---
name: pomp-dmeas-rmeas-scale-inconsistency
description: Detect cases where a POMP model's dmeasure and rmeasure Csnippets apply different numerical rescalings to state variables before computing win/outcome probabilities, causing the likelihood evaluation and forward simulation to reflect different effective models despite using the same distributional family — use when reviewing a POMP project with a custom Bradley-Terry or logistic observation model.
---

# POMP dmeas/rmeas Scale Inconsistency Detector

## Purpose

The `pomp-inference-misuse` skill covers the case where `dmeasure` and `rmeasure` use different distributional families (e.g., `dnbinom` vs. `rbinom`). A related but distinct error occurs when both snippets use the same distributional family (e.g., both use `dbinom`/`rbinom` with a logistic-type probability), but apply different linear rescalings to state variables before computing the probability. Because the particle filter uses `dmeasure` for likelihood evaluation and `rmeasure` for forward simulation, any difference in the computed probability between the two snippets means the model that is estimated and the model that is simulated are different. This error is invisible without side-by-side code comparison and produces no runtime warning.

The canonical instance arises in Bradley-Terry-style POMP models for sports or competition outcomes, where one Csnippet divides state variables by a normalizing constant (e.g., `team_score = team_strength / 100.0`) while the other uses raw values (e.g., `exp(team_strength - opp_strength)`), producing win probabilities from entirely different numerical inputs.

## When to Activate

Use this skill when:
- A POMP project defines a custom `dmeasure` and `rmeasure` that compute a probability (e.g., win probability, detection probability) as a nonlinear function of one or more continuous state variables.
- The probability function involves an exponentiation or logistic transform of the state variable (e.g., `exp(team_score)` or `1 / (1 + pow(10, diff/400))`).
- The state variables are on a large numerical scale (e.g., ELO ratings ~1500, population counts ~1e6) where a factor-of-100 rescaling changes the computed probability substantially.

Do not use this skill when:
- Both snippets apply identical transformations to state variables and differ only in whether they call the density or random-draw variant (e.g., `dbinom` vs. `rbinom` with the same `p`).
- The `pomp-inference-misuse` skill already covers the inconsistency (different distributional families).
- The measurement model is a standard epidemiological negative binomial or Poisson form where no manual rescaling of state variables is performed.

## Procedure

### 1. Identify the probability computation in dmeasure

Read the `dmeas` Csnippet. Identify:
- All state variables that appear in the probability expression.
- Any rescaling applied to those variables (e.g., division by a constant, logarithm, exponentiation).
- The final expression for `p` (or `lik`) as a function of rescaled state variables.

### 2. Identify the probability computation in rmeasure

Read the `rmeas` Csnippet. Perform the same identification:
- All state variables in the probability expression.
- Any rescaling applied.
- The final expression for `p`.

### 3. Compare the two probability expressions

Check whether `dmeas` and `rmeas` compute the same probability for the same state variable values:
- **Correct pattern**: Both snippets apply identical rescaling and produce numerically identical `p` for any given state.
- **Error pattern**: One snippet divides state by a constant (e.g., `team_score = team_strength / 100.0`) while the other uses the raw state value in the logistic expression; or one snippet uses a log-scale transform that the other omits.

To verify, substitute a concrete state value (e.g., `team_strength = 1500`, `opp_strength = 1500`) into both formulas and compute `p` numerically. If the two values differ, the snippets are inconsistent.

### 4. Assess the magnitude of the inconsistency

Compute the difference in win probability between `dmeas` and `rmeas` at typical state values:
- If the typical state is in the range [1400, 1600] (ELO scale) and `dmeas` divides by 100 (scale ~15) while `rmeas` does not (scale ~1500), the logistic expression `exp(diff)` will be near 1 in `dmeas` (diff ≈ 0) but exp(±100) in `rmeas` for any imbalance — producing probabilities near 0.5 in `dmeas` and near 0 or 1 in `rmeas`. This is a severe inconsistency.
- If the rescaling difference is minor (e.g., a factor of 1.01), the practical impact may be negligible. Flag as major only when the probability discrepancy at typical states exceeds 0.1.

### 5. Check the home-court advantage term

If a home-court advantage parameter (`hca`, `home_court_avd`) also receives different treatment in the two snippets (e.g., added directly in one and divided by 100 in the other), document this separately as an additional inconsistency.

### 6. Assess the impact on inference

If the inconsistency is confirmed:
- The particle filter's likelihood evaluation (via `dmeas`) is computing probabilities for a different model than the forward simulations (via `rmeas`).
- IF2 will converge to the MLE of the `dmeas` model, not the `rmeas` model.
- Forward simulations from the estimated parameters will not correspond to the fitted model.
- Prediction accuracy computed from forward simulations is evaluating a different model than was estimated, making accuracy figures and model comparisons invalid.

### 7. Report the finding

For each detected instance, report:
- The code location (chunk name) and the specific lines defining `p` in each snippet.
- A concrete numerical example demonstrating the probability discrepancy at typical state values.
- The consequence: likelihood evaluation and forward simulation reflect different models; all parameter estimates, log-likelihoods, and simulation-based predictions are invalid.
- The fix: ensure both snippets apply identical transformations to state variables before computing `p`. Typically this means adding the same `/100.0` rescaling (or removing it from both) and checking that the `home_court_avd` term is treated identically.

## Limitations

- This skill requires side-by-side code reading; the inconsistency is invisible from the rendered output.
- Requires numerical verification at concrete state values to assess severity; asymptotic or symbolic analysis alone may not reveal the magnitude of the discrepancy.
- Does not replace the `pomp-inference-misuse` skill, which covers distributional family inconsistencies. Both should be applied when reviewing custom dmeas/rmeas Csnippets.
- In some models, `dmeas` and `rmeas` legitimately differ in how they handle boundary cases (e.g., zero counts) while computing the same probability in the generic case; confirm the main probability expression is identical before flagging.
