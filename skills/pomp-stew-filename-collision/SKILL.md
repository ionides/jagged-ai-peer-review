---
name: pomp-stew-filename-collision
description: Detect cases where a POMP project uses the same stew() or bake() cache filename for two different computations (e.g., a broad global search and a narrowed-box follow-up search), causing the second computation to be silently skipped and stale results from the first computation to be used in its place — use when reviewing a POMP project that runs multiple sequential IF2 searches with stew() and claims improvement from a second search.
---

# POMP stew() Filename Collision Detector

## Purpose

The `stew()` function (and its equivalent `bake()`) in the `pomp` ecosystem caches computation results to a named file. If the file already exists on disk, `stew()` skips the computation and loads from the existing file. This design is intended to avoid re-running expensive computations, but it creates a silent failure when two distinct computations — such as a broad global search and a subsequent narrowed-box search — are written to the same filename. In that case, the second `stew()` call loads the first search's results without any warning. The document renders normally, the new variable is populated with old data, and any reported improvement or confirmation from the "second" search is fabricated.

This failure is distinct from:
- `pomp-global-search-init-audit`: that skill covers using a previous mif2 result as the first argument to mif2 (wrong initialization), not file caching.
- `pomp-global-search-box-misalignment`: that skill covers box ranges that exclude the MLE; here the box range is correct but the computation never runs.
- `pomp-profile-pre-global-seed-error`: that skill covers CSV accumulation ordering; this skill covers cache-file naming.

## When to Activate

Use this skill when:
- A POMP project calls `stew()` or `bake()` more than once in the same document.
- Two or more `stew()` / `bake()` calls use the same filename (or a filename that evaluates to the same string at runtime, e.g., `paste0("box_eval_bitcoin_", run_level, ".rda")` used twice with the same `run_level`).
- The project claims that a second search produces different, improved, or confirmatory results compared to the first.

Do not use this skill when:
- All `stew()` / `bake()` calls in the document use distinct filenames.
- The repeated filename is intentional (e.g., multiple sections that should all use the same cached result, with the computation only needing to run once).
- The project explicitly notes that it is loading previously cached results and does not claim to be running a new computation.

## Procedure

### 1. Identify all stew() and bake() calls

Search the Rmd/R source for all `stew(file = ..., {...})` and `bake(file = ..., {...})` calls. For each call, record:
- The evaluated filename (substituting any variable values, e.g., `run_level`).
- The variable(s) assigned inside the call.
- The computation being performed (e.g., "broad global search", "narrowed-box search", "profile search").

### 2. Check for duplicate filenames

Compare the evaluated filename list. If any two `stew()` / `bake()` calls share the same filename, flag the collision.

- Note which call appears first in document order (and thus writes the file).
- Note which call appears second (and thus loads from the pre-existing file without running).

### 3. Assess the consequence for reported results

For the second (non-executing) `stew()` call:
- Determine which variable(s) are loaded from the stale cache.
- Identify every downstream analysis that uses those variables: summary statistics, convergence plots, parameter pairs plots, log-likelihood comparisons, and any text narrative that claims "the second search found...".
- All such results reflect the first search's computation, not the second's.

### 4. Check whether the narrative claims improvement from the second search

If the text states that the second search confirmed the global maximum, improved the log-likelihood, or revealed a different parameter region, these claims are unsupported — the second search never ran.

### 5. Verify by comparing results

If the cached artifacts are available, check whether the variable populated by the second `stew()` call is identical to the variable populated by the first:
```r
identical(r.box, r.box.new)  # should be FALSE if searches ran; TRUE indicates collision
```
Identical results between two searches with different boxes confirm the collision.

### 6. Report the finding

For each detected collision:
- Cite the two `stew()` call locations (chunk names and approximate line numbers).
- State the shared filename.
- Identify which results are affected and which narrative claims are invalidated.
- The fix: assign a unique filename to each distinct computation, e.g., `"box_eval_bitcoin_narrow_3.rda"` for the narrowed-box search.

## Limitations

- This skill requires reading the source code; the rendered HTML shows no indication that `stew()` loaded from cache rather than rerunning.
- If the two computations would have produced identical results anyway (e.g., the parameter space was the same despite different stated box bounds), the practical impact is zero — but the code is still incorrect and should be fixed.
- Does not apply when the same filename is used across separate Rmd sessions with intermediate file deletion (e.g., if the author deleted the `.rda` file between runs). Code inspection alone cannot detect this case; the presence of the file at render time must be assumed.
- Does not replace the `pomp-global-search-init-audit` skill; both should be applied when reviewing multi-stage global searches.
