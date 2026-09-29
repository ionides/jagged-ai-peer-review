---
name: pomp-orphan-paramname-audit
description: Detect cases where a POMP model lists a parameter in paramnames that is never referenced in any Csnippet (rprocess, rmeasure, dmeasure, rinit), causing IF2 to perturb a ghost parameter with no effect on the likelihood surface and wasting optimization effort — use when reviewing a POMP project whose paramnames vector appears larger than what the Csnippets require.
---

# POMP Orphan paramnames Detector

## Purpose

The `paramnames` argument in a `pomp()` call declares the complete set of parameters that the model uses. IF2 (`mif2()`) perturbs all parameters listed in `rw.sd` based on this declaration. If `paramnames` includes a parameter that is never referenced in any Csnippet — neither `rprocess`, `rmeasure`, `dmeasure`, nor `rinit` — the optimizer perturbations on that parameter have no effect on the model output. The likelihood surface is flat in that parameter direction regardless of its value, and the optimizer wastes computational effort perturbing it without ever improving the fit. The parameter also appears in pairs plots and convergence traces, creating misleading scatter that suggests the parameter is being estimated when it is in fact unidentified by construction.

This error is distinct from:
- `pomp-partrans-undeclared-param`: that skill covers parameters in `paramnames` that lack a `partrans` entry (wrong transformation). Here, the parameter has no role in the model at all.
- `pomp-accumvar-semantic-audit`: that skill covers accumulator variables tracking the wrong compartment flow. Here, the issue is an entirely unused parameter name.

## When to Activate

Use this skill when:
- A POMP project defines a `paramnames` vector with multiple entries.
- The `paramnames` vector appears longer than the set of parameters explicitly referenced in the Csnippets.
- The project's initialization history suggests incremental development where parameters were added or renamed and old entries were not cleaned up (e.g., `ini_positive` and `ini_positive_remained` coexisting in `paramnames` when only one appears in the Csnippets).

Do not use this skill when:
- All parameters in `paramnames` appear in at least one Csnippet.
- The project uses R-level (non-Csnippet) process or measurement functions, where parameter references are not in a Csnippet text and a string search would produce false negatives.
- The parameter is used only in a covariate table or fixed_params vector but is intentionally excluded from Csnippets (e.g., a population size used only in initialization).

## Procedure

### 1. Extract the paramnames vector

Read the `pomp()` call and record every name listed in `paramnames`.

### 2. Collect all Csnippet code

Identify and read all Csnippet strings: the `rprocess` Euler step, `rinit`, `rmeasure`, and `dmeasure` snippets.

### 3. Check each paramnames entry against the Csnippets

For each parameter name in `paramnames`, search for it as a literal token in the concatenated Csnippet text.

- **Correct pattern**: The parameter name appears at least once in one of the Csnippets.
- **Error pattern**: The parameter name does not appear in any Csnippet. It is an orphan — declared but never used.

Note: use whole-word matching to avoid false positives (e.g., `ini_positive` as a prefix of `ini_positive_remained`).

### 4. Check whether the orphan parameter appears in rw.sd

Locate the `rw.sd = rw_sd(...)` call in `mif2()`. Determine whether the orphan parameter receives a non-zero perturbation. If so, IF2 perturbs it at every iteration without any effect on the likelihood, wasting computation and adding noise to parameter-space diagnostics.

### 5. Assess the impact on pairs plots and convergence traces

An orphan parameter with a non-zero `rw.sd` will appear as a flat, high-variance column in the pairs plot (the likelihood is constant regardless of its value) and as a random-walk trace in the convergence plot. This can be mistaken for a weakly identifiable parameter, when in fact it is completely unidentified by construction.

### 6. Report the finding

For each orphan parameter detected:
- State the parameter name.
- Confirm it is absent from all Csnippets.
- Note whether it receives a non-zero `rw.sd`.
- Report the consequence: the optimizer perturbs a parameter with no model effect; pairs-plot and trace-plot output for that parameter is uninterpretable.
- Propose the fix: either (a) remove the parameter from `paramnames` and `rw.sd` if it is genuinely unused, or (b) add it to the appropriate Csnippet if it was accidentally omitted from the model code.

## Limitations

- This skill requires string-level search of Csnippet text. Parameters referenced via R-level functions (non-Csnippet `rprocess`) would not be found by this search; the skill should not be applied when the model uses R-level step functions.
- Some parameters are intentionally passed through `paramnames` for use only in `covariate_table()` construction or other auxiliary roles outside the Csnippets. In those cases the parameter is not an orphan even though it does not appear in Csnippet code; context reading is required to confirm.
- Does not replace the `pomp-partrans-undeclared-param` skill; both should be applied when reviewing POMP models with complex `paramnames` declarations.
