---
name: pomp-rprocess-equation-code-discrepancy
description: Detect cases where the algebraic form of the state-transition equation stated in the text (e.g., phi*V_{n-1} in the mean-reversion term) differs from the Csnippet implementation (e.g., phi*sqrt(V)), causing the estimated model to differ from the described model — use when reviewing a POMP project whose rprocess Csnippet contains a mathematical transformation of the state variable that does not match the corresponding equation in the paper's methods section.
---

# POMP rprocess Equation-Code Discrepancy Detector

## Purpose

When a POMP project specifies a state-space model, the rprocess Csnippet must implement exactly the transition density described by the mathematical equations in the methods section. A subtle and silent error occurs when the functional form of the state variable in the Csnippet's mean structure differs from the text. For example:

- Text describes: `V_n = (1 - phi) * theta + phi * V_{n-1} + sqrt(V_{n-1}) * omega_n`
- Code implements: `V = theta*(1 - phi) + phi*sqrt(V) + sqrt(V)*omega;`

The code applies `sqrt(V)` to the autoregressive term (`phi*sqrt(V)`) rather than `phi*V`, introducing a square-root nonlinearity in the conditional mean that is not stated or motivated in the text. The model that is estimated is therefore not the model that is described, and all parameter estimates, likelihood values, and interpretations are for the unnamed code model rather than the stated text model.

This error is distinct from:
- `pomp-rprocess-wrong-hazard-variable`: that skill covers using the wrong state variable (V vs. I) in a compartmental force-of-infection term. Here, the variable is correct but the functional form (linear vs. square-root) differs between text and code.
- `pomp-dmeas-rmeas-scale-inconsistency`: that skill covers differences between dmeasure and rmeasure. Here, the discrepancy is within rprocess itself, between the text equation and the Csnippet.
- `pomp-population-text-code-discrepancy`: that skill covers a transcription error in a fixed parameter value (N). Here, the discrepancy is in the functional form of the transition equation, not a single parameter value.

The error is invisible at runtime because the Csnippet is syntactically valid and produces plausible output. It can only be detected by carefully reading the text equation and the Csnippet side-by-side and checking that every state variable appears with the same functional transformation in both.

## When to Activate

Use this skill when:
- A POMP project defines a continuous-valued state variable (e.g., V, H, G for stochastic volatility; S, I for epidemic models) in rprocess.
- The project's methods section contains an explicit difference equation or discretized SDE for the state variable.
- The rprocess Csnippet contains nonlinear transformations of the state variable (e.g., `sqrt(V)`, `log(V)`, `exp(V)`, `tanh(G)`) in a position that does not match the stated equation.

Do not use this skill when:
- The Csnippet implements a standard epidemic compartmental model (SIR/SEIR/SIRV) using binomial draws — those have well-established textbook forms and the appropriate skill is `pomp-rprocess-wrong-hazard-variable`.
- The project explicitly notes a deliberate simplification or approximation relative to the stated continuous-time model (e.g., "we apply the square-root approximation to improve numerical stability").
- No explicit mathematical equation is given in the text; the Csnippet is the sole specification.

## Procedure

### 1. Extract the stated state-transition equation from the text

Read the methods section and identify every explicitly stated difference equation or discretized SDE. For each continuous state variable `X`, record:
- The conditional mean of `X_n` given `X_{n-1}`: the function `f(X_{n-1})` such that `E[X_n | X_{n-1}] = f(X_{n-1})`.
- The noise term: the standard deviation `g(X_{n-1})` multiplied by a noise draw.
- The functional forms of `f` and `g` (e.g., `f(V) = (1-phi)*theta + phi*V`, `g(V) = sqrt(V)`).

### 2. Read the rprocess Csnippet

Locate the Csnippet that implements the state update. For each continuous state variable `X`:
- Identify the deterministic (mean) component of the update.
- Identify the stochastic component.
- Note the functional transformation applied to the previous state value (e.g., `sqrt(V)`, `V`, `log(V)`).

### 3. Compare the functional forms term by term

For each term in the stated equation, check whether the same term appears in the Csnippet with the same functional form:

| Text term | Expected code term | Actual code term | Match? |
|-----------|-------------------|------------------|--------|
| `(1-phi)*theta` | `theta*(1 - phi)` | `theta*(1 - phi)` | Yes |
| `phi * V_{n-1}` | `phi*V` | `phi*sqrt(V)` | **No** |
| `sqrt(V_{n-1}) * omega` | `sqrt(V)*omega` | `sqrt(V)*omega` | Yes |

Flag any row where the actual code term does not match the expected code term.

### 4. Assess the magnitude of the discrepancy

Determine the practical difference between the stated and implemented models:
- At typical state values (from the data scale or fitted parameter range), compute the numerical difference between the stated mean and the implemented mean.
- Example: if `phi = 0.9` and typical `V = 0.0004` (hourly return variance), then:
  - Stated mean component: `phi * V = 0.9 * 0.0004 = 0.00036`
  - Implemented mean component: `phi * sqrt(V) = 0.9 * 0.02 = 0.018`
  - Ratio: 50x — a major discrepancy that fundamentally changes the model's dynamics.

Flag as a major issue if the ratio exceeds 2 at typical state values.

### 5. Check whether the discrepancy affects model stability

For stochastic volatility models, the Heston variance process requires `V > 0` for `sqrt(V)` to be real. If the Csnippet applies `sqrt(V)` to the mean term but the stated model does not, the boundary behavior of the process changes: the implemented model's mean is pulled toward the boundary faster or slower than the stated model. Check whether the project includes an explicit non-negativity guard (e.g., `if(V < 0) { V = 0; }`) and whether that guard is consistent with the stated model.

### 6. Verify consistency of the measurement model

Check that the measurement model (`dmeasure`/`rmeasure`) is consistent with the implemented rprocess, not just the stated equation. If the measurement model expects the latent state on a particular scale (e.g., `dnorm(y, 0, sqrt(V), give_log)` expects `V > 0`), verify that the rprocess produces states on that scale under the implemented (not the stated) dynamics.

### 7. Report the finding

For each detected discrepancy, report:
- The specific text equation and the specific Csnippet line where the discrepancy occurs.
- A numerical example showing the magnitude of the difference at typical state values.
- The consequence: the estimated model is not the stated model; all parameter estimates, log-likelihoods, and model comparisons are for an undescribed model.
- The fix: correct the Csnippet to match the stated equation (e.g., change `phi*sqrt(V)` to `phi*V`), or update the text to describe the model that is actually implemented and provide scientific justification for the nonlinear mean structure.

## Limitations

- This skill requires side-by-side reading of the mathematical methods and the Csnippet. It cannot be detected from rendered HTML output.
- The comparison requires knowing the intended mapping from math notation to code variable names (e.g., that `V_{n-1}` maps to the C variable `V` inside the Csnippet's update step). This is usually clear from context but may require reading the `statenames` argument.
- For models where a nonlinear mean is intentional (e.g., a square-root diffusion model for which both text and code are consistent), this skill does not apply. It applies only when the text and code disagree.
- Does not replace the full rprocess verification (POMP checklist §9, stochasticity); this skill focuses specifically on algebraic mismatches between text equations and Csnippet implementations.
