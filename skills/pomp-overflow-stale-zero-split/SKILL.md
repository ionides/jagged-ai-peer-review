---
name: pomp-overflow-stale-zero-split
description: Detect cases where a POMP rprocess Csnippet handles a compartment overflow by first setting the compartment to zero and then computing proportional splits using the already-zeroed variable, causing all split terms to evaluate to zero and silently zeroing downstream compartment flows — use when reviewing a POMP model whose step function contains an if-else overflow guard that assigns zero to a compartment before using it in proportional expressions.
---

# POMP Overflow-Guard Stale-Zero Split Detector

## Purpose

Compartmental POMP models sometimes guard against the event where the sum of outflows from a compartment exceeds the current compartment size (e.g., `dN_AR + dN_ASy > A`). A common manual overflow-handling pattern is:

```c
if ((dN_AR + dN_ASy) > A) {
  A = 0;
  R += nearbyint(A * (dN_AR / (dN_ASy + dN_AR)));   // BUG: A is already 0
  Sy += nearbyint(A * (dN_ASy / (dN_ASy + dN_AR))); // BUG: A is already 0
}
```

After `A = 0` is executed, every subsequent expression that multiplies by `A` evaluates to zero. The intended behavior — to split the pre-zeroing value of `A` proportionally between downstream compartments — requires saving the pre-zeroing value of `A` before the assignment. Without this, the overflow branch silently sends zero individuals to all downstream compartments, violating conservation: individuals "disappear" from A without entering any other compartment. This error does not produce a runtime warning, does not crash the simulation, and produces plausible-looking (but incorrect) trajectories because the overflow condition may be rare under typical parameter values.

This error is distinct from:
- `pomp-residual-compartment-overflow`: that skill covers a compartment exceeding its population bound due to a double-counted additive term. Here the error is within an overflow-guard block, not in the compartment assignment formula.
- `pomp-covariate-compartment-underflow`: that skill covers a covariate driving a compartment negative. Here the guard is triggered by stochastic outflows.
- `pomp-accumvar-semantic-audit`: that skill covers the wrong flow being accumulated. Here the flows are never computed (they evaluate to zero), not merely semantically mismatched.

## When to Activate

Use this skill when:
- A POMP rprocess Csnippet contains an if-else overflow guard of the form `if ((dN_AB + dN_AC) > X) { X = 0; ... }`.
- Inside the overflow branch, the code references the same variable `X` in expressions after the `X = 0` assignment (e.g., `R += nearbyint(X * fraction)`, `D += nearbyint(X * fraction)`).
- The intent (from context or comments) is to split the pre-zeroing value of `X` proportionally among the downstream compartments.

Do not use this skill when:
- The compartment variable is not read again inside the overflow branch after being zeroed.
- The overflow guard uses a saved copy of the pre-zeroing value (e.g., `double X_old = X; X = 0; R += nearbyint(X_old * fraction);`).
- The model uses `reulermultinom` or another pomp-native multinomial draw that handles conservation automatically, without manual overflow guards.

## Procedure

### 1. Identify overflow guard blocks in the rprocess Csnippet

Search the Csnippet for conditional blocks of the form:
```c
if ((dN_AB + dN_AC) > X) {
  X = 0;
  ...
}
```
List all variables that are zeroed inside if-blocks triggered by outflow-exceeds-compartment conditions.

### 2. Check whether the zeroed variable is read in expressions after the zeroing

Inside each overflow block, scan every expression that follows the `X = 0` line. Determine whether `X` appears on the right-hand side of any subsequent assignment:
```c
R += nearbyint(X * (dN_AR / (dN_ASy + dN_AR)));  // X is stale (zero) here
```

If yes, flag the bug.

### 3. Determine what value was intended

From context (comments, the else-branch, or the mathematical description in the text), determine what the intended splitting behavior is:
- The pre-zeroing value of `X` (call it `X_pre`) should be split proportionally by the ratio of outflow rates.
- `R += nearbyint(X_pre * (dN_AR / (dN_AR + dN_ASy)))` and `Sy += nearbyint(X_pre * (dN_ASy / (dN_AR + dN_ASy)))`.

### 4. Assess the impact on model dynamics

Determine when the overflow condition fires:
- If the overflow fires rarely (e.g., only during the initial transient), the bias is minimal and concentrated near t=0.
- If it fires regularly (e.g., whenever compartment size is small, which occurs on the tails of the epidemic), the bias compounds over time and affects the declining phase of the epidemic — precisely the region most informative for recovery-rate estimation.

Check whether the affected compartment flows feed into the measurement model. If so, the measurement model's expected observation is systematically underestimated during overflow events, biasing all rate parameters.

### 5. Propose the fix

Add a pre-zeroing copy of the variable before the zeroing assignment:
```c
if ((dN_AR + dN_ASy) > A) {
  double A_pre = A;  // save before zeroing
  A = 0;
  R += nearbyint(A_pre * (dN_AR / (dN_ASy + dN_AR)));
  Sy += nearbyint(A_pre * (dN_ASy / (dN_ASy + dN_AR)));
}
```

This correctly distributes all individuals from the compartment into downstream compartments and maintains population conservation.

### 6. Report the finding

For each detected instance:
- Quote the specific lines in the Csnippet showing `X = 0` followed by `X * (fraction)`.
- Explain that `X` evaluates to zero at these lines, causing the split to produce zero flows.
- Identify which downstream compartments receive zero instead of the intended proportional share.
- State when the overflow condition fires and how frequently, to assess the scope of bias.
- Provide the fix (saving `X_pre` before zeroing).

## Limitations

- This skill requires reading the Csnippet; the bug is invisible in rendered HTML output.
- If the overflow condition is never triggered at the estimated parameters (because compartments remain large throughout), the bug has no effect on the reported results — but the error is still present and would manifest under different parameter values.
- The proportional split logic itself (dividing by `dN_AR + dN_ASy`) may produce NaN when both outflows are zero. If this case is possible, an additional guard `if (dN_AR + dN_ASy > 0)` is needed around the proportional expression, separate from the overflow fix.
- Does not replace `pomp-accumvar-semantic-audit` or the full compartment-conservation audit; both should be applied when reviewing custom rprocess Csnippets with manual overflow guards.
