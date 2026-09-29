## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Missing IF2 convergence diagnostics — no trace plots to verify convergence")

**Findings classification:**
- ID 21.12.7: B — Missing IF2 convergence diagnostics; no trace plots of log-likelihood or parameter values vs. iteration (matches Human Issue #7)
- ID 21.12.8: A — No profile likelihoods or confidence intervals reported for POMP parameters
- ID 21.12.6: C — No ESS monitoring reported during particle filtering
- ID 21.12.5: C — Simulated data pfilter log-likelihood noted as very low but numerical value from L.pf1 not printed
- ID 21.12.1: C — AIC comparison across ARMA, GARCH, and POMP model classes lacks qualification about same-scale computation
- ID M1: C — Gaussian measurement model used despite heavy-tailed returns; Student-t not considered
- ID M2: C — Conclusion overstates model adequacy given unverified convergence and unassessed identifiability
- ID 21.12.4: C — Extreme sigma_eta values in pairs plot from some IF2 replicates are not commented on
- ID 21.12.10: C — Conclusion refers to "Nasdaq-500" three times; correct index is Nasdaq-100
- ID 21.12.11: C — ACF figure labeled "Nasdaq-100 Index return" but appears in ARMA residual diagnostics context; ambiguous whether raw returns or residuals

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 1 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
