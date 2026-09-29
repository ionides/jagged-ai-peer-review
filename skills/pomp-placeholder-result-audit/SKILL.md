---
name: pomp-placeholder-result-audit
description: Detect cases where a POMP (or any statistical) project reports fabricated or placeholder numerical results — values that the author explicitly acknowledges were invented rather than computed — and assess the downstream impact on all conclusions that depend on those values — use when a manuscript contains self-annotated placeholder text alongside quantitative claims.
---

# POMP Placeholder Result Audit

## Purpose

A rare but severe reproducibility failure occurs when an author inserts placeholder numerical results (fabricated log-likelihoods, made-up parameter estimates, or illustrative numbers) into a draft manuscript and submits that draft without replacing the placeholders with actual computed values. Unlike computation errors (where wrong calculations produce wrong but genuinely computed numbers), this failure means the paper's quantitative claims have no computational basis at all. The error is typically self-announced — the author leaves an explanatory comment in the text such as "I made up these numbers based on typical patterns" or "swap in your actual values here" — but the comment is sometimes visible only in the rendered HTML or the source code, not as a clearly flagged caveat.

This failure is qualitatively different from:
- `pomp-artifact-audit`: artifact values conflict with the code (but the artifact exists)
- `pomp-closed-environment-reproducibility-audit`: results were computed but cannot be reproduced externally
- `pomp-simdata-benchmark-error`: the wrong dataset was used but a real computation was performed

Here, no valid computation underlies the reported numbers.

## When to Activate

Use this skill when:
- A project's source code or rendered HTML contains inline comments such as "I made up these numbers," "swap in your actual values," "placeholder — replace before submission," or similar self-annotations adjacent to numerical results.
- The reported quantitative results (log-likelihoods, parameter estimates, iteration counts) contain internal contradictions that suggest fabrication (e.g., the log-likelihood worsens but the text claims improvement, or the same quantity is reported differently in two locations).
- Parameter estimates or log-likelihood values are cited in multiple sections with conflicting values that cannot be reconciled by rounding.

Do not use this skill when:
- All reported numerical results are consistent across the document and no placeholder text is present.
- Discrepancies in reported values are minor (within Monte Carlo error for log-likelihoods) and plausibly caused by stochastic optimization.
- The author explicitly states results are illustrative (e.g., in a tutorial or worked-example context where fabricated values are pedagogically appropriate).

## Procedure

### 1. Scan for Self-Annotation Phrases

Search the Rmd/Quarto source and rendered HTML for phrases indicative of placeholder content:
- "made up," "fabricated," "placeholder," "example values," "swap in," "replace with," "illustrative"
- "based on typical patterns," "adjust as needed," "your actual values"
- Comment markers adjacent to numerical results: `# TODO`, `# FIXME`, `# replace`

### 2. Identify Which Results Are Affected

For each placeholder annotation found:
- List the specific numerical values labeled as fabricated (e.g., log-likelihood at specific iterations, final parameter estimates, convergence thresholds).
- Trace which conclusions in the paper depend on those values: CI claims, model adequacy assessments, interpretation of parameter estimates.

### 3. Check for Internal Contradictions

Regardless of self-annotation, scan all reported quantitative results for logical inconsistencies:
- **Log-likelihood direction**: does the text claim improvement while the reported value becomes more negative across iterations?
- **Parameter value consistency**: is the same parameter reported with different values in the Results table, the Discussion, and the Conclusion?
- **Count consistency**: does the claimed number of converged runs match the code's loop count or the number of rows in a displayed table?

Any contradiction is a strong secondary indicator of placeholder values even when no explicit self-annotation is present.

### 4. Assess the Scope of Invalidated Conclusions

Determine which sections of the paper can still be evaluated independently of the fabricated values:
- **Model specification**: Csnippets, paramnames, pomp() call structure — evaluable from code alone.
- **Optimization setup**: bounds, population size, iteration count — evaluable from code alone.
- **Goodness-of-fit claims**: entirely invalidated if the reported likelihood is fabricated.
- **Parameter interpretation**: partially evaluable if estimates appear in the code output (e.g., `print(params_est)`) but the surrounding narrative uses fabricated values.
- **Convergence evidence**: entirely invalidated.

### 5. Report the Finding

For each instance:
- Quote the exact placeholder annotation found in the source or rendered output.
- State which numerical values are affected.
- List every conclusion in the paper that depends on those values and is therefore unsupported.
- Flag as a major issue: a paper whose quantitative claims are acknowledged fabrications cannot be evaluated for model adequacy, parameter identifiability, or comparative fit.
- Propose the fix: re-run the optimization, replace all fabricated values with actual computed results, and verify internal consistency across all sections before submission.

## Limitations

- This skill requires reading source code and rendered output; self-annotation in a suppressed code chunk (`echo=FALSE`) may not be visible in the rendered HTML alone.
- Absence of self-annotation does not confirm that reported values are genuine — other skills (e.g., `pomp-artifact-audit`, `pomp-simdata-benchmark-error`) are needed to detect silent fabrication.
- In course-project contexts, placeholder text may reflect an incomplete draft rather than intentional misrepresentation; the fix (complete the computation) is the same regardless of intent, but the framing of the critique should note the distinction.
- Does not apply to Monte Carlo studies where "illustrative" parameter values are intentionally chosen for simulation purposes — the error pattern here is specifically fabricated *inference results* presented as genuine computations on real data.
