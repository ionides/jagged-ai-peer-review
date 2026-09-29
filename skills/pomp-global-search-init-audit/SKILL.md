---
name: pomp-global-search-init-audit
description: Detect the anti-pattern of initializing a POMP global IF2 search from a previous mif2 result object rather than the base pomp object, which anchors the global search to the local-search solution and invalidates the search's claim to global coverage — use when reviewing POMP code that performs a two-stage local-then-global IF2 optimization.
---

# POMP Global Search Initialization Audit

## Purpose

A common two-stage POMP optimization workflow runs a local IF2 search from a fixed starting point, then runs a global search by sampling starting parameters from a box. A recurring error is to initialize the global search by calling `mif2(if1[[i]], params=...)` (using a previous IF2 result as the first argument) instead of `mif2(base_pomp_object, params=...)`. This error causes the global search to inherit the internal state and cooling schedule from the local chain, anchoring it near the local-search solution rather than exploring the full parameter box from fresh starts. The reported "global maximum" may therefore be the same local optimum dressed up as a global search.

## When to Activate

Use this skill when:
- A POMP project performs a two-stage optimization: a local IF2 search (e.g., `mif2(pomp_object, params=fixed_start, ...)`) followed by a global box search (e.g., `mif2(..., params=apply(box, 1, runif))`).
- The global search `mif2()` call passes a previous `mif2` result object (e.g., `if1[[1]]`, `mif_local`) as its first argument rather than the original `pomp` object.

Do not use this skill when:
- The project runs only a single-stage IF2 search.
- The global search explicitly uses the base `pomp` object as the first argument to `mif2()` (this is the correct pattern).
- The project uses PMCMC or other non-IF2 inference methods where this anti-pattern does not apply.

## Procedure

### 1. Locate the local IF2 search

Search the Rmd/R source for `mif2(` calls. Identify the first argument: is it a `pomp` object or a previous `mif2` result? Note the variable name used.

### 2. Locate the global box search

Find the second `mif2(` call block (typically inside a `foreach` loop over `NADQ_Nreps_global` or similar). Identify:
- The first argument passed to `mif2()`.
- The `params=` argument — is it drawn from a box via `apply(box, 1, runif)` or similar?

### 3. Check whether the first argument is a raw pomp object or a previous mif2 result

- **Correct pattern**: `mif2(pomp_object, params=apply(box, 1, runif), Np=..., Nmif=..., ...)`
  - Starts each global replicate fresh from the raw pomp object with a new random starting point.
- **Anti-pattern**: `mif2(if1[[1]], params=apply(box, 1, runif), Np=..., Nmif=..., ...)`
  - Passes a previous IF2 chain as the object; new `params=` are applied but the cooling schedule and internal IF2 state from `if1[[1]]` are inherited.

Flag the anti-pattern as a major issue if present.

### 4. Assess the impact on the reported global maximum

If the anti-pattern is detected:
- Note that the global search replicates all share the cooling schedule of `if1[[1]]`, which is typically at or near its final cooling state after `Nmif` iterations. This means the global search effectively performs very few functional IF2 iterations from the new random start before the perturbations shrink to near zero.
- The reported "global maximum" log-likelihood may not differ meaningfully from the local-search result, and the pairs plot of the global search may show clustering near the local-search solution rather than broad coverage of the box.

### 5. Verify convergence trace interpretation

Check whether the convergence traces (`plot(if.box)`) show genuine parameter movement across iterations, or flat traces from near the first iteration (indicating the cooling schedule inherited from the previous chain has already decayed to near zero).

### 6. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line).
- The consequence: global search anchored to local-search solution; reported global maximum may not represent a true global optimum.
- The fix: replace `mif2(if1[[1]], ...)` with `mif2(base_pomp_object, ...)` in the global search loop, where `base_pomp_object` is the original `pomp()` call result.

## Limitations

- This skill applies only to IF2-based POMP optimization. The analogous issue in PMCMC (using a warmed-up chain as the start of a new chain from a different starting point) exists but has different implications.
- The anti-pattern may have negligible practical impact if `if1[[1]]` happened to start at a bad point and the box search genuinely explores the new starting locations — but this cannot be verified without access to the cooling schedule metadata, so the issue should be flagged regardless.
- Does not replace a full computational adequacy audit (covered by the POMP-specific checklist in `guided-pomp-review/SKILL_pomp.md`).
