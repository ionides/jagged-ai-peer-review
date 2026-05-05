---
name: pomp-dmeas-give-log-sentinel-audit
description: Use when reviewing a pomp dmeas Csnippet that contains a guard condition returning a numeric sentinel (e.g., lik = 0) for invalid parameter or state values, to detect the silent error where the sentinel value is not conditioned on give_log — assigning probability 1 instead of probability 0 to the observation when give_log=TRUE.
---

# pomp dmeas give_log Sentinel Audit

## Purpose

In pomp, the dmeas Csnippet receives a `give_log` argument that controls whether it should return the probability density (give_log=FALSE) or the log-density (give_log=TRUE). Guard conditions that assign a hard-coded `lik = 0` when parameter or state values are invalid behave differently under these two modes:

- When give_log=FALSE: `lik = 0` means probability zero. This kills the particle weight, which is the intended behavior.
- When give_log=TRUE: `lik = 0` means log-probability zero, i.e., probability **one**. This **upweights** particles with invalid parameters, which is the opposite of the intended behavior.

Because the particle filter always calls dmeas with give_log=TRUE, a guard that sets `lik = 0` unconditionally will incorrectly assign maximum weight to particles with invalid configurations such as negative dispersion parameters, negative accumulator values, or similar. The code runs without error; the particle filter runs; IF2 may even converge. The error is entirely silent.

## When to Activate

Use this skill when:
- A pomp project's dmeas Csnippet contains an `if`/`else` guard condition.
- The guard assigns a fixed numeric value (0, -1e10, or similar) to `lik` when the condition triggers.
- The assignment does not condition on `give_log`.

Do not use this skill when the guard is handled with the correct conditional form (`lik = give_log ? R_NegInf : 0.0;`) — that is the correct pattern and this skill does not apply.

## Procedure

### 1. Locate the dmeas Csnippet and identify guard conditions

Read the full dmeas body. Identify every `if`/`else` branch that triggers before or instead of the main density evaluation.

### 2. Check whether each guard assignment is conditioned on give_log

For each guard that assigns a fixed value to `lik`:
- If the assignment is `lik = give_log ? R_NegInf : 0.0;` — this is correct. No issue.
- If the assignment is `lik = 0;` unconditionally — flag as a sentinel error. When give_log=TRUE, this assigns log-probability 0 (probability 1) to particles with invalid parameters.
- If the assignment is `lik = -1e10;` or another large negative number — flag as a partial fix. This approximates -Inf when give_log=TRUE but is not the correct sentinel for non-log mode (should be 0.0).

### 3. Assess whether parameter transformations reduce the severity

Check the `partrans` argument in the pomp() call:
- If k and rho are estimated on the log scale (log=c("k", "rho")), they will always be positive after back-transformation. A guard `if (k < 0 || rho < 0)` will never trigger in practice during IF2.
- However, accumulator variables (H) are not transformed and can become zero or negative if the model is evaluated at extreme parameter values or if numerical precision errors occur during the Euler step.
- Even if the guard never triggers in a well-configured run, it will trigger during debugging or at degenerate starting values, producing misleading results.

### 4. Propose the corrected guard

The standard pattern is:

```c
if (k <= 0 || rho <= 0 || H < 0)
  lik = give_log ? R_NegInf : 0.0;
else
  lik = dnbinom_mu(reports, k, rho*H, give_log);
```

or equivalently, remove the guard on k and rho and rely on parameter transformations to enforce positivity, checking only H:

```c
if (H < 0)
  lik = give_log ? R_NegInf : 0.0;
else
  lik = dnbinom_mu(reports, k, rho*H, give_log);
```

### 5. Summarize findings

For each problematic guard found:
- Quote the offending lines.
- State the consequence: particles with invalid configurations receive log-likelihood 0 (probability 1) when give_log=TRUE, corrupting the particle weights.
- Propose the corrected assignment.

## Limitations

- This skill addresses sentinel value errors in dmeas guard conditions only. It does not evaluate the logical correctness of the guard condition itself (OR vs. AND errors are covered by `pomp-csnippet-audit`).
- In practice, the error may never trigger if parameter transformations keep all parameters in the valid range during IF2. However, the incorrect guard still represents a latent bug that will manifest during debugging, manual evaluation, or at degenerate starting values.
- This skill does not detect cases where the guard is absent entirely (no protection for invalid states) — that is a different issue covered by `pomp-csnippet-audit`.
