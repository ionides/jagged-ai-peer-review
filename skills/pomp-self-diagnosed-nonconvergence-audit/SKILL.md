---
name: pomp-self-diagnosed-nonconvergence-audit
description: Detect cases where a POMP project explicitly acknowledges in its text that IF2 failed to converge, yet continues to present and interpret parameter tables, simulation plots, and pairs plots derived from those non-converged chains as substantively meaningful — use when reviewing a POMP manuscript whose conclusion or diagnostic section contains an explicit convergence failure statement alongside downstream results.
---

# POMP Self-Diagnosed Non-Convergence Audit

## Purpose

A recurring failure pattern in POMP student projects occurs when the authors correctly identify that their IF2 optimization did not converge (e.g., "the likelihood waved between -7000 and -5000," "large variability in all parameters"), yet continue to display and interpret parameter estimates, simulation trajectories, and pairs plots derived from those non-converged chains. This is qualitatively different from:

- Projects where convergence failure is undetected (covered by computational adequacy in `guided-pomp-review/SKILL_pomp.md`).
- Projects that fabricate placeholder values (`pomp-placeholder-result-audit`).
- Projects where computation is merely insufficient but convergence is not explicitly rejected (`pomp-rw-sd-magnitude-error`).

The error here is rhetorical and evidentiary: the authors correctly diagnose the problem but draw unwarranted conclusions from results they acknowledge are unreliable. Every downstream claim about parameter values, goodness of fit, and model behavior is invalidated not by an external reviewer's judgment but by the authors' own statements.

## When to Activate

Use this skill when:
- A POMP project's text (in the diagnostic section, conclusion, or discussion) contains an explicit statement that IF2 did not converge, using phrases such as: "the likelihood does not look stable," "large variability in parameters," "the model failed to converge," "we are unable to achieve convergence."
- Despite this statement, the same document presents one or more of: a table of best-fit parameter estimates, simulation envelopes from the estimated parameters, a pairs plot of parameter-likelihood results, or quantitative conclusions about model fit (e.g., a stated best log-likelihood).
- The conclusion or abstract claims scientific results (e.g., "our model estimates transmission rate b1 = X") without caveating that these are derived from non-converged optimization.

Do not use this skill when:
- The project qualifies every downstream result with explicit non-convergence caveats (e.g., "these estimates are unreliable and reported only to illustrate the optimization setup").
- The convergence failure is described only in a limitations section added after all main claims, without those claims being retracted.
- The project identifies convergence failure for one submodel but reports converged results for a different, simpler submodel.

## Procedure

### 1. Locate the convergence failure statement

Search the text for phrases such as:
- "the likelihood does not look stable" / "likelihood is not stable"
- "does not converge" / "failed to converge" / "convergence issues"
- "large variability" in reference to parameter traces
- "we are unable to" in the conclusion of a POMP analysis

Record the exact quote, section, and page/chunk location.

### 2. Catalog all downstream results presented after the convergence failure statement

After locating the convergence failure acknowledgment, scan the remainder of the document for:
- Tables of best-fit parameter estimates.
- Simulation trajectory plots generated from `simulate(pomp_object, params = best_params, ...)`.
- Pairs plots of parameter-likelihood values.
- Explicit log-likelihood values cited as the "best" model fit.
- Any conclusion that interprets parameter estimates substantively (e.g., "the estimated vaccine efficacy of gamma = 0.7 suggests...").

List each such result with its code chunk location.

### 3. Check whether each downstream result is properly caveated

For each result identified in Step 2, determine whether the surrounding text:
- Explicitly states that the result is from a non-converged chain and therefore unreliable.
- Presents the result only as an illustration of the optimization setup, not as a substantive finding.
- Retracts or qualifies the result in the conclusion.

Flag any result that is presented without an accompanying non-convergence caveat as an instance of the error.

### 4. Assess the scope of invalidated conclusions

Determine which sections of the paper are affected by the self-diagnosed convergence failure:
- **Parameter estimates**: all parameter values from the best-fit row of non-converged results are unreliable; any biological interpretation (e.g., "the Delta transmission rate is 3x the original") is unsupported.
- **Simulation trajectories**: simulations from non-converged parameter estimates reflect a random visit to a high-likelihood region, not the MLE; they cannot be used to assess model adequacy.
- **Policy conclusions / counterfactual simulations**: if the stated research goal was a simulation study under different parameter values, those results are completely invalidated.
- **Log-likelihood comparisons**: a non-converged log-likelihood cannot be compared to an ARIMA or GARCH benchmark for model selection.

### 5. Report the finding

For each detected instance, report:
- The exact text of the convergence failure statement (with location).
- A list of results presented without convergence caveats (with code chunk locations).
- The consequence: the paper self-contradicts — it acknowledges convergence failure and then draws conclusions from the failed optimization; all such conclusions are unsupported by the authors' own evidence standard.
- The fix: either (a) substantially increase computational effort (more particles, more iterations, more replicates from diverse starts) until genuine convergence is demonstrated, then replace all non-converged results; or (b) restrict the paper's claims entirely to model specification and setup, removing all parameter estimates, simulation plots, and comparative claims that depend on the non-converged optimization.

## Limitations

- This skill requires both reading the text narrative (for the convergence failure statement) and reading the code/results (for non-caveated downstream results). It cannot be applied from code alone or from narrative alone.
- "Convergence" is a matter of degree. A project may state "the likelihood is somewhat variable" and still present results that are adequately converged for coarse inference. Apply judgment about the severity of the stated instability before flagging all results.
- This skill is primarily applicable in student/course-project contexts where authors may not have the computational resources to achieve convergence but still need to submit a complete report. The critique should be constructive, suggesting computational improvements rather than wholesale rejection.
- Does not replace the full computational adequacy audit (Wheeler et al. 2024, §Computational adequacy), which applies even when convergence failure is not explicitly acknowledged. Both checks should be applied when reviewing a POMP project's optimization section.
