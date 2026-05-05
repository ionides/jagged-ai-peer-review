---
name: pomp-csnippet-audit
description: Use when auditing pomp rprocess/dmeas/rmeas Csnippets in a student or research project to detect silent implementation errors — specifically accumulator stock-vs-flow misuse, dmeas/rmeas distributional mismatches, and accumvars registration failures — that distort the likelihood without producing runtime errors.
---

# pomp Csnippet Audit

## Purpose

Silent implementation errors in pomp Csnippets can produce a syntactically valid, runnable model that nevertheless computes an incorrect likelihood. The most common failure mode is defining an accumulator variable as a stock (e.g., `H = I`) rather than a flow (e.g., `H += dN_EI`), which causes the same individual to appear in multiple observation-level trials. Because pomp does not validate Csnippet semantics, these errors go undetected by the package and can only be caught by manual code audit.

This skill provides a structured checklist for catching such errors during peer review or code audit.

## When to Activate

Use this skill when:
- Reviewing a pomp project that defines one or more accumulator variables in `rprocess` Csnippets.
- The measurement model (dmeas/rmeas) draws from a variable that is updated inside rprocess.
- There is any uncertainty about whether reported cases represent a flow (new events per interval) or a stock (cumulative or current count).

Do not use this skill as a substitute for reading the full model description — it is a targeted checklist for a specific class of implementation error.

## Procedure

### 1. Locate all accumulator variables

Find the `pomp()` call (or `pomp` object construction) and identify the `accumvars` argument. List every variable named there. If `accumvars` is absent, flag this immediately — any variable intended as a flow accumulator must appear in `accumvars` for pomp to reset it after each observation.

### 2. Check that accumulators are incremented, not assigned, in rprocess

For each accumulator variable `H` (or equivalent):
- Look at the rprocess Csnippet.
- If the snippet contains `H = <expression>` (assignment), this is a stock definition. Flag as a critical error.
- If the snippet contains `H += <expression>` or `H = H + <expression>`, this is a flow accumulation. This is correct.
- Common correct pattern: `H += dN_EI;` where `dN_EI` counts new transitions into the infectious or reported state during the time step.
- Common incorrect pattern: `H = I;` where `I` is the current prevalence stock.

### 2b. Check rprocess fidelity to stated SDE or difference equation (SDE-based models)

When the paper states a continuous-time SDE or discrete-time difference equation and the rprocess Csnippet is claimed to implement its discretization:

1. Write out the Euler-Maruyama (or stated) discretization of the SDE term by term.
2. Compare each term in the discretization against the corresponding expression in the Csnippet.
3. Flag any structural mismatches, including:
   - Applying a function (e.g., `sqrt`) to a term where none should appear, or omitting one that should be present. Example: a stated variance-space AR(1) `V = phi*V + ...` implemented as `V = phi*sqrt(V) + ...` quietly changes the model from a mean-reverting variance process to a mean-reverting standard-deviation process.
   - Confusing a variance-space AR(1) (`phi*V`) with a standard-deviation-space AR(1) (`phi*sqrt(V)`).
   - Incorrectly squaring or square-rooting the noise term (`sigma*dW` vs. `sigma^2*dW`).
   - Milstein correction terms present in the text but absent from the code (or vice versa).
4. Check any guard conditions (`if(V < 0) V = 0;` etc.) for logical correctness: verify the condition triggers on the correct sign, and that the replacement value (0 or `abs(V)` etc.) is consistent with the stated model's behavior at the boundary.
5. For stochastic volatility models specifically: confirm whether the latent state is variance (V) or log-variance (H = log(V)) throughout both the equation and the code — mixing the two is a common source of silent error.

This step is distinct from the dmeas/rmeas check (Step 3) because the error lives entirely in the rprocess Csnippet, produces no runtime error, and may not be detectable from convergence traces alone (both the stated model and the mis-implemented model can produce converging-looking IF2 runs).

### 2c. Check within-step update ordering for correlated latent processes

When the rprocess Csnippet models two latent state variables (e.g., G and H) that are intended to be correlated at each time step — such as a leverage model where a driving process G determines the correlation between return shocks and volatility shocks — verify that both are evaluated at a consistent point in time within the same Csnippet execution.

Specifically, inspect whether:
1. A noise term (e.g., omega) is drawn using the **pre-update** value of the driving process (e.g., `tanh(G)` before `G += nu`).
2. The driving process is then updated (`G += nu`).
3. The mean expression for the other latent state (e.g., H) uses the **post-update** value of the driving process.

If steps 1 and 3 use different values of the shared driving variable, the noise magnitude and the mean leverage term are evaluated at different time points. This is an asymmetry that may or may not match the stated model, but it is not the natural simultaneous-update discretization of a bivariate SDE. Flag this for clarification whenever the stated model does not explicitly specify the update ordering within a time step.

Common pattern that triggers this check:
```c
// omega uses G at time n-1
omega = rnorm(0, sigma_eta * sqrt(1-phi*phi) * sqrt(1-tanh(G)*tanh(G)));
// G is updated to time n
G += nu;
// leverage term in H update uses G at time n
H = mu_h*(1-phi) + phi*H + beta*tanh(G)*exp(-H/2) + omega;
```

This asymmetry is silent: the code compiles, the particle filter runs, and IF2 converges. It can only be caught by comparing the Csnippet execution order against the stated SDE or difference equation.

### 3. Verify dmeas and rmeas use the same distribution

Read both the `dmeasure` (dmeas) and `rmeasure` (rmeas) Csnippets side by side.
- Confirm they reference the same distributional family (e.g., both use negative binomial, or both use binomial).
- Confirm the parameters (size, probability, dispersion) are defined identically in both.
- A common mismatch: dmeas uses `dnbinom_mu(reports, k, rho*H, give_log)` while rmeas uses `rbinom(H, rho)`.
- Flag any discrepancy as a major error, because it means simulated data (from rmeas) and evaluated likelihoods (from dmeas) are drawn from different distributions.
- **Check guard conditions for logical correctness.** Some dmeas Csnippets include an `if`/`else` guard intended to truncate extreme observations (e.g., `if (cases <= 10*sd || cases >= -10*sd)`). Verify the boolean logic: an OR condition where one branch is always satisfied for the data type (e.g., `cases >= -10*sd` is always true when cases is non-negative) renders the guard vacuous — every observation passes through to the main likelihood evaluation, and the truncation is never applied. The practical effect is that the implemented dmeas computes an unconditional distribution while the text describes a truncated one. This is a mismatch between stated and implemented observation model. The fix is to use AND (`&&`) rather than OR (`||`), or to restructure the condition to bound from above only (e.g., `if (cases <= mean + 10*sd)`).

### 3b. Verify all parameters referenced in dmeas and rmeas appear in paramnames

After confirming distributional consistency (Step 3), check that every parameter name used inside dmeas and rmeas is declared in the `pomp()` call's `paramnames` argument:
- List all bare names inside the dmeas and rmeas function bodies (or Csnippets) that are not state variables (not in `statenames`) and not local variables.
- Confirm each such name appears in `paramnames`.
- A common failure: dmeas references a variable like `s`, `theta`, or `k` that was never added to `paramnames`. pomp will either throw a runtime error or silently read an uninitialized value, depending on version.
- Also verify that any parameter passed in a `simulate()` or `pfilter()` call but absent from `paramnames` is flagged — this indicates the model and the calling code are inconsistent about what parameters exist.

### 4. Verify the measurement model draws from a flow, not a stock

Confirm that the variable appearing in dmeas/rmeas (typically `H` or `cases`) represents new events within the observation interval (a flow), not the current count of individuals in a state (a stock).
- A stock variable (e.g., current number infected) can double-count individuals across observation periods.
- Ask: if an individual enters state I on day 1 and remains until day 5, does the observation on day 3 include that individual in H? If yes, and if H is used as the size argument to a binomial or negative-binomial draw, then days 1-5 all attempt to "report" the same person.

### 5. Check that initial value of accumulator is zero

In the `rinit` Csnippet, verify that all accumulator variables are initialized to 0. If initialized to a non-zero value, the first observation interval may over-count events.

### 6. Summarize findings

For each error found:
- Quote the offending line from the Csnippet.
- Explain the consequence (e.g., "H = I assigns prevalence stock to the accumulator; each individual infectious for k days is eligible to be reported k times, inflating the effective sample size and distorting rho").
- Propose the correct implementation.

## Limitations

- This skill addresses implementation errors only, not model misspecification (wrong compartment structure, wrong covariates, etc.).
- It assumes the pomp package is used directly via Csnippets; models constructed with high-level wrappers (e.g., spatPomp, epidemia) may have different conventions.
- It cannot detect errors in the underlying epidemiological logic (e.g., wrong transition rates) — only errors in how variables are tracked and measured.
- If the model uses a custom C file rather than inline Csnippets, the same logic applies but the audit requires reading the external file.
