---
name: pomp-dmeas-rmeas-moment-mismatch
description: Detect cases where a POMP model's dmeasure and rmeasure Csnippets use the same distributional family but specify different moment functions (mean or variance) for that distribution, causing the likelihood evaluation and forward simulation to reflect different observation models despite no distributional family change — use when reviewing a POMP project with Gaussian or Poisson-approximation measurement models where standard deviation or variance expressions differ between the two snippets.
---

# POMP dmeas/rmeas Moment Mismatch Detector

## Purpose

The `pomp-inference-misuse` skill covers dmeasure/rmeasure inconsistency when different distributional families are used (e.g., `dnbinom` vs. `rbinom`). The `pomp-dmeas-rmeas-scale-inconsistency` skill covers the case where the same family is used but different linear rescalings of state variables produce different win/outcome probabilities. A third distinct failure mode occurs when both snippets use the same distributional family and the same state variable, but compute one of the distributional moments — typically the variance or standard deviation — via different mathematical expressions. Because no family change is visible, and simulations may still look superficially reasonable, this error is easy to miss in code review.

The canonical instance: dmeasure defines `sd_cases = sqrt(mean_cases * mean_cases)` (= |mean_cases|, coefficient of variation = 1) while rmeasure uses `sqrt(mean_cases)` (Poisson-like variance = mean). Both snippets use `dnorm`/`rnorm` with the same mean, but the variance differs by a factor of `mean_cases`. At large counts (e.g., daily COVID infections of 50,000), `sd_cases` in dmeasure evaluates to 50,000 while rmeasure uses sqrt(50,000) ≈ 224 — a factor of 224 discrepancy in the standard deviation, producing nearly flat dmeasure probabilities while rmeasure is highly concentrated.

## When to Activate

Use this skill when:
- A POMP project defines both `dmeasure` and `rmeasure` Csnippets using the same distributional family (both `dnorm`/`rnorm`, or both `dpois`/`rpois`).
- The snippets differ in how they compute the mean or variance/standard deviation parameter of that distribution.
- The difference in moment specification is non-trivial (ratio > 2 at typical state values).

Do not use this skill when:
- The distributional families differ between dmeasure and rmeasure (use `pomp-inference-misuse` instead).
- The snippets use the same family with rescaled state variables (use `pomp-dmeas-rmeas-scale-inconsistency` instead).
- Both snippets compute identical moment functions and differ only in calling the density vs. the random-draw variant (e.g., `dnorm(x, mu, sigma, give_log)` vs. `rnorm(1, mu, sigma)` with the same mu and sigma expressions).

## Procedure

### 1. Identify the distributional family used in each snippet

Read dmeasure and rmeasure side by side. Confirm both use the same family (e.g., both `dnorm`/`rnorm`, both `dpois`/`rpois`). If they differ, stop and apply `pomp-inference-misuse`.

### 2. Extract the moment expressions

For each snippet, identify:
- The expression for the **mean** parameter (e.g., `rho * H`, `mu_cases`).
- The expression for the **variance or standard deviation** parameter (e.g., `sqrt(rho * H)`, `sqrt(mean_cases * mean_cases)`, `tau * mean_cases`).

Write both expressions out explicitly.

### 3. Compare moment expressions symbolically

Check whether the mean expression and the variance/SD expression are identical across dmeasure and rmeasure:
- **Correct pattern**: Both use `mu = rho * H` and `sigma = sqrt(rho * H)`.
- **Error pattern**: dmeasure uses `sigma = sqrt(mu * mu)` = `|mu|` while rmeasure uses `sigma = sqrt(mu)`.

### 4. Verify numerically at representative state values

Substitute the expected range of the state variable (e.g., `H = 50000` for daily COVID counts) into both moment expressions:
- Compute the SD in dmeasure vs. rmeasure.
- If the ratio of SDs exceeds 2 at typical values, flag as a major error.
- Note the direction: if dmeasure SD > rmeasure SD, the likelihood will be artificially flat (near-uniform weights) and the particle filter will converge slowly or not at all; if dmeasure SD < rmeasure SD, the likelihood will be artificially sharp and may degenerate.

### 5. Assess the impact on inference

If the mismatch is confirmed:
- The particle filter weights are computed under dmeasure's moment specification.
- Forward simulations and reported prediction intervals use rmeasure's moment specification.
- IF2 converges to parameters that maximize the dmeasure likelihood, not the rmeasure model.
- Goodness-of-fit plots (overlaying simulations on data) reflect the rmeasure model, not the estimated model.
- All reported parameter estimates, log-likelihoods, and simulation comparisons are based on two different models simultaneously.

### 6. Check whether the author intended a specific statistical model

Read the text description of the measurement model. Determine whether:
- A Poisson approximation was intended (variance = mean → SD = sqrt(mean)).
- A normal-with-constant-CV model was intended (variance = mean^2 → SD = |mean|).
- A negative binomial was intended (should use `dnbinom_mu` / `rnbinom`).

The correct model depends on the scientific context. Flag the discrepancy regardless of intent; the implementation does not match the stated model in either case.

### 7. Report the finding

For each detected instance:
- Quote the specific variance/SD lines in each Csnippet.
- Provide a concrete numerical example of the SD ratio at typical state values.
- State the consequence: likelihood evaluation and simulation reflect different variance models; parameter estimates and fit assessments are invalid.
- Propose the fix: standardize the moment function across both snippets, using a scientifically motivated choice (Poisson, negative binomial, or constant-CV normal) and verifying consistency.

## Limitations

- This skill requires side-by-side code reading; it cannot be detected from the rendered HTML output.
- If the state variable in the moment expression has a very small expected range (e.g., counts near 1), the ratio of SDs may be close to 1 in practice, making the error negligible. Assess magnitude with numerical verification.
- Does not replace `pomp-dmeas-rmeas-scale-inconsistency` (state-variable rescaling in the probability function) or `pomp-inference-misuse` (different distributional families). All three should be applied when reviewing custom dmeas/rmeas Csnippets.
- In some models, intentional heteroscedasticity (e.g., variance proportional to the square of the mean for log-normal measurement error) is correct. Confirm that the discrepancy is unintentional before flagging.
