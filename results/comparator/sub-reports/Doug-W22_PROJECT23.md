## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Fixed initial conditions are not estimated or assessed for sensitivity")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "SEIQR measurement model links to Q (stock) without an accumulator, confounding the observation")
- Human Issue #4: covered (matched by finding: "Conclusion incorrectly describes log-likelihood direction")
- Human Issue #5: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Global search box excludes the MLE region (SIR model)")
- Human Issue #11: missed

**Findings classification:**
- Major 1 (SEIQR rprocess omits N-normalization in force of infection): A — no matching human issue
- Major 2 (Log-likelihoods on incommensurable scales, cannot be compared): A — no matching human issue
- Major 3 (SEIQR measurement model links to Q stock without accumulator): B — (matches Human Issue #3)
- Major 4 (Non-convergence acknowledged but results interpreted substantively): A — no matching human issue
- Major 5 (SEIR Euler step size delta.t=7 inconsistent with daily data): A — no matching human issue
- Major 6 (SEIR local search pairs plot displays SIR data): A — no matching human issue
- Major 7 (No non-mechanistic benchmark comparison): B — (matches Human Issue #5)
- Major 8 (Global search box excludes MLE region — eta range mismatch): B — (matches Human Issue #10)
- Major 9 (No profile likelihoods or confidence intervals): A — no matching human issue
- Minor: Population size discrepancy in introduction: C — no matching human issue
- Minor: SEIQR global search uses %do% instead of %dopar%: C — no matching human issue
- Minor: SEIR partrans in mif2 call redundant and potentially inconsistent: C — no matching human issue
- Minor: Fixed initial conditions not estimated or assessed for sensitivity: D — (matches Human Issue #1)
- Minor: No model diagnostics beyond visual inspection: C — no matching human issue
- Minor: Conclusion incorrectly describes log-likelihood direction: D — (matches Human Issue #4)
- Minor: Computational effort is low and not justified: C — no matching human issue
- Minor: No assessment of model adequacy for the full pandemic period: C — no matching human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
