## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "25.17.14 — Seasonal pattern unmodeled")
- Human Issue #4: covered (matched by finding: "25.17.6 — No mean-model baseline (ARMA/SARIMA)" and "25.17.14 — Seasonal pattern unmodeled")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- 25.17.1: A — mif2 internal log-likelihood likely used in AIC table; no replicated pfilter runs or Monte Carlo SEs reported
- 25.17.3: A — hard-coded regime windows introduce data-snooping bias, confounding the leverage hypothesis test
- 25.17.4: A — no profile likelihoods computed for any model parameter, leaving identifiability unassessed
- 25.17.6: B — no mean-model baseline (ARMA/SARIMA); STL decomposition reveals seasonality that should be addressed before variance modeling (matches Human Issue #4)
- 25.17.14: D — seasonal pattern identified in STL decomposition but not incorporated into any POMP model (matches Human Issues #3 and #4)
- 25.17.2: C — GARCH vs. SV likelihood scale comparison lacks explicit confirmation of matching normalizing conventions
- 25.17.M1: C — no simulation-based diagnostics for POMP models, unlike the QQ-plot and ACF provided for GARCH
- 25.17.M2: C — initial conditions G_0 = H_0 = 0 fixed without justification or sensitivity analysis

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
