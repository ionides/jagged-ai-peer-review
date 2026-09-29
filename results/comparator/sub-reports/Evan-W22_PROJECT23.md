## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "22.23.1 — Incomparable measurement models invalidate the model comparison")
- Human Issue #4: covered (matched by finding: "22.23.13 — 'Lowest log-likelihood = best model' is non-standard language")
- Human Issue #5: covered (matched by finding: "22.23.7 — No non-mechanistic benchmark")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "22.23.4 — SIR global search box excludes the local MLE region")
- Human Issue #11: missed

**Findings classification:**
- 22.23.1: B — Incomparable measurement models (SEIQR uses Q stock / dnorm vs. SIR/SEIR accumulator / dbinom) invalidate model comparison (matches Human Issue #3)
- 22.23.2: A — SEIQR force of infection missing division by N
- 22.23.3: A — SEIR uses weekly Euler step (delta.t=7) on daily data
- 22.23.4: B — SIR global search eta box [0.4, 0.6] excludes local MLE region [0.94, 0.96] (matches Human Issue #10)
- 22.23.7: B — No non-mechanistic (ARMA/SARIMA) benchmark fitted (matches Human Issue #5)
- 22.23.8: A — No profile likelihoods or confidence intervals reported
- 22.23.5: A — SEIQR declared best model despite non-converged mif2 trace plots
- 22.23.6: C — SEIR pairs plot erroneously plots SIR likelihood data (code bug)
- 22.23.9: C — mu_IR = 0.006 in SIR MLE implies 167-day infectious period, biologically implausible for Omicron
- 22.23.13: D — "Lowest log-likelihood = best model" is non-standard; should read "highest" (matches Human Issue #4)
- Diag (no ID): C — No per-time-point conditional log-likelihoods or ESS diagnostics reported

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
