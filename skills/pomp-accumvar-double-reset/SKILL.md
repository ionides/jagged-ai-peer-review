---
name: pomp-accumvar-double-reset
description: Detect cases where a POMP model manually resets an accumulator variable inside the rprocess Csnippet at integer time steps while also declaring the same variable in accumvars, causing a timing conflict that removes one observation period's accumulation before it can be evaluated by the measurement model — use when reviewing a POMP model that declares accumvars and contains an explicit H = 0 (or equivalent) reset inside its step function.
---

# POMP Accumulator Double-Reset Detector

## Purpose

POMP's `accumvars` mechanism resets declared accumulator variables to zero *after* the likelihood evaluation at each observation time, so that the accumulator reflects counts for only the current observation period. A common error is to also place an explicit reset (`H = 0`) inside the `rprocess` Csnippet, triggered at integer time steps (e.g., `if (fabs(fmod(t, 1.0)) < threshold) H = 0`). With sub-daily Euler steps (`delta.t = 1/7`), the first sub-step after each integer time t satisfies the condition, zeroing H at the *beginning* of the observation period rather than the end. This causes the accumulator to reflect only the sub-steps from the *previous* period that fall after the measurement time, rather than the full current period, producing a systematic measurement error and biasing the reporting-rate estimate.

This error is distinct from the accumulator semantic mismatch (wrong compartment flow accumulated), which is covered by `pomp-accumvar-semantic-audit`.

## When to Activate

Use this skill when:
- A POMP model declares one or more variables in `accumvars` (e.g., `accumvars = "H"`).
- The rprocess Csnippet or step function contains an explicit assignment `H = 0` (or `C = 0`, `Inc = 0`) inside a conditional block.
- The conditional is triggered at observation times (e.g., `if (fabs(fmod(t, 1.0)) < threshold)` for weekly data with `delta.t < 1`, or `if (t_int == obs_time)` for similar patterns).

Do not use this skill when:
- The reset is in `rinit` only (initial conditions), not in `rprocess`.
- The `accumvars` mechanism is not used (the accumulator is reset manually and no `accumvars` declaration is present — this is a different but potentially valid design).
- The Euler step size equals the observation interval (`delta.t = 1`), making the timing of manual and automatic resets identical.

## Procedure

### 1. Locate the accumvars declaration

Search for `accumvars = "H"` (or equivalent) in the `pomp()` call. Note all variable names declared.

### 2. Search the rprocess Csnippet for explicit resets

Search the Csnippet for assignments `H = 0`, `C = 0`, or `Inc = 0`. Note the condition under which the reset fires.

### 3. Determine the timing relative to measurement

Identify the observation interval (e.g., `times = 1:T` with integer times means observations at each integer). Determine `delta.t`. Evaluate whether the Csnippet condition `fabs(fmod(t, period)) < threshold` is triggered at the *start* or *end* of an observation window:

- The `accumvars` mechanism resets *after* the observation at time `t`.
- The Euler step at `t = k` (an integer) is the *first* step of the new observation period.
- If the Csnippet resets H at this step, the accumulation for the current period starts from zero (correct), but the reset happens *before* the Euler dynamics within this first sub-step are computed (also correct only if the reset is the *first* operation). This timing depends on the order of operations within the Csnippet.
- If the Csnippet resets H at the *last* sub-step before each integer time, the accumulation is cleared before the measurement model evaluates it — this is the error pattern.

In most cases with `delta.t = 1/7` and condition `fabs(fmod(t, 1.0)) < 1e-8`, the reset fires at t = 1, 2, 3, ..., which are exactly the observation times, and the Csnippet reset and the `accumvars` reset act on the same time points. The order of operations (Csnippet reset vs. measurement evaluation) determines whether the error is present.

### 4. Check for redundancy or conflict

If both the Csnippet reset and `accumvars` fire at the same observation times:
- The `accumvars` reset is the correct mechanism and should be the only one present.
- The Csnippet reset is redundant at best and conflicting at worst, depending on sub-step ordering.
- Flag this as a minor issue if the timing analysis shows no net effect, or a major issue if the timing removes a full observation period's accumulation.

### 5. Propose the fix

Remove the explicit `H = 0` reset from the Csnippet. Use `accumvars = "H"` as the sole reset mechanism, which is guaranteed by pomp to fire after the likelihood evaluation at each observation time.

## Limitations

- The severity of this error depends on sub-step ordering within the Euler integrator and the exact floating-point tolerance used in the `fmod` condition. In some implementations the error is zero (the Csnippet reset happens at t = 0 only, before any accumulation); in others it removes the first sub-step's contribution at every observation.
- Does not cover the case where `accumvars` is absent and the Csnippet reset is the sole mechanism — this may be intentional and is a different design choice.
- Does not replace the accumulator semantic audit (`pomp-accumvar-semantic-audit`); both checks should be applied when reviewing POMP accumulator variables.
