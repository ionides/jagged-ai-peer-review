---
name: pomp-stochastic-dmeas-intermediate
description: Detect cases where a POMP dmeasure Csnippet uses a random-draw function (rbinom, rnorm, rpois, etc.) to compute an intermediate quantity that is then passed to a density function, making the conditional log-likelihood non-deterministic and invalidating all particle filter weights — use when reviewing a POMP project whose dmeasure Csnippet contains both a random-draw call and a density-evaluation call.
---

# POMP Stochastic Intermediate in dmeasure Detector

## Purpose

The particle filter requires that `dmeasure` returns a deterministic log p(y_t | x_t, θ) for each particle. If the Csnippet calls a random-draw function (e.g., `rbinom`, `rnorm`, `rpois`, `rexp`) to compute an intermediate variable, and then passes that variable into a density function (e.g., `dnorm`, `dpois`, `dnbinom`), the returned log-likelihood is a random variable rather than a deterministic function of the particle state. Every evaluation of the same particle with the same parameters and the same observation can return a different value. This means:

- Particle weights are random, not proper importance weights.
- The particle filter log-likelihood estimate is biased and inconsistent.
- IF2 convergence is not to the MLE of any well-defined model.
- The reported log-likelihood has no valid statistical interpretation.

This error is distinct from the `pomp-inference-misuse` pattern, which covers SSE-based optimization with non-particle-filter methods. The current pattern applies when mif2/pfilter IS used correctly as the inference engine, but the dmeasure itself is internally stochastic, corrupting all likelihood evaluations silently.

The canonical instance: a BVS-type compartmental model where `dmeasure` draws `Views = rbinom(N-S, prob)` (a stochastic intermediate) and then evaluates `dnorm(obs, Views*(1-exp(-mu)), Views*(1-exp(-mu))/10, 1)`. Each call to dmeasure with the same state returns a different `Views` and thus a different density value.

## When to Activate

Use this skill when:
- A POMP project defines a `dmeasure` Csnippet.
- The Csnippet contains a call to any random-draw function: `rbinom(`, `rnorm(`, `rpois(`, `rnbinom(`, `rexp(`, `rgamma(`, `runif(`, or similar.
- The result of the random-draw call is used as an argument to a density function (`dnorm`, `dpois`, `dnbinom`, `dbinom`, etc.) that computes the returned `lik` value.

Do not use this skill when:
- The `dmeasure` Csnippet contains only deterministic computations and density function calls (no random draws).
- The random-draw function appears only in an `rmeasure` Csnippet (which is the correct location for stochastic draws).
- The project uses a deterministic skeleton and the measurement model is evaluated analytically without random-draw intermediates.

## Procedure

### 1. Locate the dmeasure Csnippet

Read the `dmeasure` (or `bvs_dmeas`, `dmeas`, etc.) Csnippet string defined in the Rmd/R source.

### 2. Search for random-draw calls

Scan the Csnippet text for any of the following function calls:
- `rbinom(`, `rnorm(`, `rpois(`, `rnbinom(`, `rexp(`, `rgamma(`, `runif(`, `rhyper(`, `rgeom(`, `rnegbinom(`.

If none are found, stop — this error is not present.

### 3. Identify the density call that uses the random draw

Trace the result of the random-draw call through the Csnippet:
- Is the random draw stored in a local variable (e.g., `double Views = rbinom(...)`)?
- Is that variable subsequently used as an argument to a density function (e.g., `dnorm(obs, Views*rate, Views*rate/10, 1)`)?

If yes, the `lik` returned by `dmeasure` is a random variable.

### 4. Assess the impact

Confirm the inference method used in the project (mif2, pfilter, pmcmc):
- All particle-filter-based methods assume `dmeasure` is a deterministic function. A stochastic `dmeasure` means:
  - Different evaluations of the same particle produce different weights.
  - The particle filter cannot correctly track the filtering distribution.
  - IF2 perturbs parameters based on corrupted gradient signals.
  - The reported log-likelihood value has no statistical interpretation.
- Flag as a major error with critical consequences for all inference results.

### 5. Identify the correct fix

The stochastic quantity that was used as an intermediate in `dmeasure` should instead be:
- Marginalized out analytically if possible (compute the expected density over the random intermediate), or
- Moved to a latent state in `rprocess` so the particle state includes the formerly-intermediate quantity, allowing `dmeasure` to evaluate the density deterministically given the particle state.

For the canonical BVS case where `Views = rbinom(N-S, prob)` is an intermediate:
- Option A: Move `Views` into the state vector and compute it in `rprocess`. Then `dmeasure` reads the deterministic `Views` from the current particle state.
- Option B: Replace `rbinom(N-S, prob)` with its expected value `(N-S) * prob` in `dmeasure` (using a Poisson or normal approximation to the binomial), creating an approximate but deterministic density.

### 6. Report the finding

Report:
- The code location (Csnippet name and the specific random-draw and density-function lines).
- The consequence: `dmeasure` returns a different value on every call for the same (state, observation, parameter) triple; all particle filter weights, log-likelihoods, and IF2 convergence results are invalid.
- The fix (see Step 5).

## Limitations

- This skill requires reading the Csnippet source code; the error is invisible from rendered output.
- Some random draws inside `dmeasure` are intentional approximations that a reviewer might mis-flag (e.g., a Monte Carlo approximation to an intractable integral implemented inside dmeasure). In such cases, assess whether the approximation is documented and whether the Monte Carlo error is negligible — but even then, using R's random number state inside a density evaluation is generally fragile and should be flagged at minimum as a minor concern.
- The error may not affect results visibly if the random intermediate has low variance (e.g., a binomial with large N and probability near 0.5); in that case the stochastic dmeasure approximates its deterministic expected-value version. Assess severity by estimating the coefficient of variation of the intermediate at typical parameter values.
- Does not replace the `pomp-inference-misuse` skill (which covers stochastic SSE cost functions with non-pfilter optimizers) or the `pomp-dmeas-rmeas-moment-mismatch` skill (which covers deterministic but mismatched moment expressions). All three should be applied when reviewing custom dmeasure Csnippets.
