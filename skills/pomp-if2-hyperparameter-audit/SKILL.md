---
name: pomp-if2-hyperparameter-audit
description: Use when reviewing a pomp project that calls mif2 to verify that rw.sd, cooling.fraction.50, Np, and Nmif are set to values that permit meaningful optimization — specifically to detect near-zero rw.sd or cooling.fraction.50 that freeze the optimizer and silently invalidate all IF2 results.
---

# pomp IF2 Hyperparameter Audit

## Purpose

Iterated filtering (IF2 via `mif2`) requires hyperparameters — `rw.sd`, `cooling.fraction.50`, `Np`, and `Nmif` — to be set within ranges that allow the optimizer to explore parameter space. When these values are misconfigured (especially rw.sd near zero or cooling.fraction.50 near zero), IF2 is effectively disabled: the perturbation magnitude collapses immediately, parameters cannot move from their starting values, and the reported log-likelihood reflects the starting point rather than any optimized value. This failure is silent: the code runs without error, convergence trace plots look "stable" (because nothing is moving), and the results appear numerical. A reviewer without awareness of IF2 mechanics can mistake a frozen-optimizer artifact for genuine convergence.

This skill provides a targeted checklist for detecting misconfigured IF2 hyperparameters during peer review or code audit.

## When to Activate

Use this skill when:
- A pomp project calls `mif2` with explicit `rw.sd`, `cooling.fraction.50`, `Np`, or `Nmif` arguments.
- The reported log-likelihoods from IF2 appear suspiciously identical across starting points, or the convergence traces show parameters that do not move across iterations.
- A single variable such as `covid_rw.sd` or `cooling_frac` is set and then passed into multiple `mif2` calls — a pattern that risks applying an incorrect value to all searches simultaneously.

Do not use this skill as the sole computational adequacy check — it complements, but does not replace, the convergence-trace and ESS checks in `guided-pomp-review`.

## Procedure

### 1. Locate all mif2 calls and extract hyperparameters

Find every `mif2(...)` call in the document. For each, record:
- `rw.sd(...)`: the perturbation standard deviation for each estimated parameter
- `cooling.fraction.50`: the fraction of the initial rw.sd remaining after 50 IF2 iterations
- `Np`: number of particles
- `Nmif`: number of IF2 iterations

If any of these are defined as variables (e.g., `covid_rw.sd <- 0.002`), trace the variable definition and verify the value used at the call site.

### 2. Check rw.sd for non-negligible values

For each parameter listed in `rw.sd(...)`:
- Values on the order of 0.01–0.1 on the log or logit scale are typical for epidemiological parameters.
- Values below 1e-4 are extremely small and warrant scrutiny.
- Values below 1e-6 are essentially zero: the optimizer cannot distinguish them from no perturbation. Flag as a critical error.
- Check whether the perturbation is applied on the transformed scale (log, logit) or the natural scale. A value of 0.002 on the log scale is reasonable; 0.002 on a parameter whose natural range spans 1–1,000,000 is insufficient.

Common error pattern: a variable like `covid_rw.sd <- 0.000000002` is defined once and passed to all parameters in all `mif2` calls simultaneously, freezing every parameter in every search.

### 3. Check cooling.fraction.50 for plausible values

- Standard values used in course examples and published POMP analyses range from 0.3 to 0.8.
- Values below 0.01 cause the perturbation magnitude to collapse to near zero within the first few iterations.
- Values below 1e-3 are effectively zero cooling: the optimizer degenerates to a particle filter with a single fixed parameter vector after 1-2 iterations. Flag as a critical error.

Check: after `Nmif` iterations, the effective perturbation is approximately `rw.sd * cooling.fraction.50^(Nmif/50)`. Compute this and verify it is non-negligible (greater than, say, 1e-4 on the transformed scale).

### 4. Check Np (number of particles) for adequacy

- For a model with T observation times, Np should be large enough that the particle filter does not degenerate (effective sample size collapsing to 1 or 2 particles).
- As a rough guideline: Np >= 500 for simple models (2-3 compartments, T < 100), Np >= 2000 for moderate models (4-6 compartments, T ~ 200-500), Np >= 10000 for complex or spatiotemporal models.
- Np=100 is a pilot-run value only; flag any production search that uses Np=100 or fewer.
- Note: if Np used during IF2 differs from Np used for final likelihood evaluation (a common and valid practice), verify both are reported and the evaluation Np is substantially larger.

### 5. Check Nmif (number of IF2 iterations) for adequacy

- Nmif < 50 is insufficient for all but the simplest models; flag as a critical error.
- Nmif in the range 100-500 is typical for well-configured analyses.
- Verify that convergence traces (log-likelihood and parameter values vs. iteration) are shown. If traces are not shown, flag as a reporting failure independent of the Nmif value.

### 6. Cross-check run_level switches

Many student and research projects define a `run_level` variable that switches between a fast pilot configuration (small Np, Nmif) and a production configuration. Verify:
- Which run_level is active in the final document.
- Whether the active run_level corresponds to the computational scale claimed in the text.
- Whether different models within the same document use different run_levels inconsistently (e.g., one model at run_level=2, another at run_level=1).

### 7. Assess convergence traces against hyperparameter configuration

After checking the numerical values, examine any convergence trace plots:
- If rw.sd is near zero, parameters should appear essentially flat across iterations. A flat convergence trace under near-zero rw.sd indicates optimizer failure, not convergence.
- If rw.sd is reasonable but traces are still flat, this may indicate a genuinely flat likelihood surface (identifiability problem) or filter degeneracy (too few particles). These require different responses.
- Distinguish between: (a) parameters that converge to a stable value from diverse starting points (good), (b) parameters that appear flat because rw.sd is zero (bad — frozen optimizer), and (c) parameters that are highly variable across runs (bad — non-convergence or non-identifiability).

### 8. Summarize findings

For each problematic hyperparameter configuration found:
- Quote the offending line (e.g., `covid_rw.sd <- 0.000000002`).
- Compute the practical consequence (e.g., "effective perturbation after 10 iterations = 2e-9 * 0.00005^(10/50) = 2e-9 * 0.007 ≈ 1.4e-11, functionally zero").
- State which IF2 searches are affected.
- Propose corrected values with brief justification.

## Limitations

- This skill addresses hyperparameter misconfiguration only, not model misspecification or Csnippet implementation errors (see `pomp-csnippet-audit` for those).
- The "reasonable range" for rw.sd depends on the parameterization. Parameters estimated on the natural scale (not log or logit) may appropriately use smaller rw.sd values if their natural range is narrow.
- Frozen-optimizer diagnosis requires observing the trace plots alongside the numerical hyperparameters; a flat trace alone is not definitive evidence of a frozen optimizer without checking rw.sd.
- This skill does not evaluate whether the parameter search box (initial ranges) is appropriate; that is a separate modeling concern.
