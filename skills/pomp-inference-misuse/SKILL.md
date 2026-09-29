---
name: pomp-inference-misuse
description: Detect and diagnose cases where a POMP project substitutes stochastic simulation-based cost functions (e.g., SSE from a single nsim=1 draw) for proper particle-filter likelihood evaluation, and cross-check dmeasure/rmeasure Csnippets for distributional inconsistency — use when reviewing inline POMP code that performs parameter optimization.
---

# POMP Inference Misuse Detector

## Purpose

Student and practitioner POMP projects frequently commit two related but distinct errors that undermine all downstream conclusions:

1. **Stochastic cost function abuse**: using a single stochastic simulation draw to compute a cost (e.g., SSE, RMSE) and then minimizing that cost with a deterministic optimizer (Nelder-Mead, GenSA, optim). Because the cost function is itself stochastic, the optimizer is chasing noise, results are not reproducible, and the minimum found has no statistical interpretation.

2. **dmeas/rmeas distributional inconsistency**: the `dmeasure` Csnippet uses one distribution (e.g., `dnbinom`) while the `rmeasure` Csnippet uses a different or mis-parameterized distribution (e.g., `rbinom`), causing simulated data and evaluated likelihoods to be drawn from different models.

This skill provides a systematic code-reading procedure to detect both failure modes quickly during manuscript review.

## When to Activate

Use this skill when:
- An Rmd/Quarto POMP project defines a `cost_function` or objective that calls `simulate()` with `nsim=1` (or any small fixed number) and computes a deterministic metric against observed data.
- The project uses non-particle-filter optimizers (`optim`, `nlminb`, `GenSA`, `DEoptim`, `nloptr`) on a POMP model.
- The `dmeasure` and `rmeasure` Csnippets are defined in the same project and use different R/C function families (e.g., `dnbinom` vs. `rbinom`, `dpois` vs. `rnbinom`).

Do not use this skill when:
- The project uses `mif2()`, `pfilter()`, `pmcmc()`, or other particle-filter-based inference — these are correct approaches and this skill's error patterns do not apply.
- The project is a pure simulation study with no parameter estimation.
- The project uses a deterministic skeleton and least-squares on the deterministic trajectory (a legitimate, if limited, approach) — this is distinct from stochastic simulation SSE.

## Procedure

### 1. Locate the optimization call

Search the Rmd/R source for calls to `optim(`, `GenSA(`, `nlminb(`, `DEoptim(`, `nloptr(`, or any other optimizer that is not `mif2` or `pmcmc`. Note the function name passed as `fn =` or equivalent.

### 2. Inspect the cost function body

Read the cost function body. Check for:
- A call to `simulate(pomp_object, nsim=K, ...)` where K is small (typically 1).
- Computation of SSE, RMSE, MAE, or similar between `sim$observations` and `data$observations`.
- **Flag**: if the cost function calls `simulate()` with a stochastic process model, the function value is a random variable. Any optimizer minimizing this is minimizing noise.

### 3. Check for particle filter likelihood evaluation

Confirm whether the project calls `pfilter()` or `logLik(pfilter(...))` anywhere. If not, and if the model has a stochastic `rprocess`, the project has no valid likelihood evaluation.

### 4. Inspect dmeasure and rmeasure Csnippets

Read both Csnippets side by side. For each, identify:
- The distributional family (e.g., `dnbinom` / `rnbinom`, `dpois` / `rpois`, `dbinom` / `rbinom`).
- The parameterization (e.g., `dnbinom_mu` vs. `dnbinom`; `mu =` vs. `prob =`).

Flag any of the following:
- `dmeasure` uses `dnbinom(x, size, prob, ...)` but `rmeasure` uses `rbinom(n, size, prob)` — these are entirely different distributions.
- `dmeasure` uses `dnbinom_mu` (mu parameterization) but `rmeasure` uses `rnbinom` (prob parameterization) with no conversion.
- The `size` parameter in `dmeasure` is set to the state variable I (e.g., `dnbinom(cases, I, rho, ...)`) — this makes size data-dependent and scales the variance with the state in an unusual way that is rarely intended.

### 5. Check parameter count consistency

Verify that all parameters appearing in `dmeasure` and `rmeasure` Csnippets are listed in `paramnames`. Missing parameters default silently to zero in pomp Csnippets, causing hard-to-detect errors.

### 6. Assess reproducibility of optimization

Determine whether:
- A random seed is set before the optimizer call and the seed is stable across the full execution context.
- Multiple independent runs from different starting points are performed and compared.
- Convergence is assessed by examining whether runs from different starts reach similar objective values.

If the cost function is stochastic (Step 2), note that setting a seed does not resolve the fundamental problem — it only freezes one noisy realization.

### 7. Summarize findings

For each detected failure mode, report:
- The specific code location (chunk name and approximate line).
- The statistical consequence (e.g., "optimizer minimizes a random variable; reported parameter estimates have no statistical interpretation").
- The fix (e.g., "replace SSE cost function with `logLik(pfilter(pomp_object, params=params, Np=2000))`").

## Limitations

- This skill reads code statically; it cannot detect failures that only manifest at runtime (e.g., numerical overflow in Csnippets, particle degeneracy).
- It does not assess whether the particle filter itself is run with sufficient particles — that is covered by the computational adequacy check in `guided-pomp-review/SKILL_pomp.md`.
- If the project uses a deterministic skeleton (`ode()` or `trajectory()`) rather than `simulate()`, SSE minimization may be a legitimate (if suboptimal) fitting approach; apply this skill's flags with reduced severity in that case.
- Does not replace the full POMP review checklist — it focuses specifically on the inference-mechanism and measurement-model-consistency failure modes.
