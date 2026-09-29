## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.04.M4 — Simulation plots lack labeled observed data overlay")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "22.04.3 — Profile likelihoods absent; no confidence intervals — calls out rho≈1 as needing scrutiny")
- Human Issue #5: covered (matched by finding: "22.04.2 — No quantitative SARIMA vs. POMP comparison")
- Human Issue #6: covered (matched by finding: "22.04.M1 — Notation error: R_t mislabeled as I_t")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- 22.04.1: A — Code bug: dN_RS drawn from I instead of R
- 22.04.2: B — No quantitative SARIMA vs. POMP comparison (matches Human Issue #5)
- 22.04.3: B — Profile likelihoods absent; no confidence intervals; calls out rho≈1 as needing justification (matches Human Issue #4)
- 22.04.4: A — mif2 log-likelihood not confirmed by replicated pfilter
- 22.04.5: A — Global search under-sampled (~5–10 points)
- 22.04.6: A — Initial conditions E, I, P hard-coded without justification
- 22.04.M1: D — Notation error: R_t mislabeled as I_t (matches Human Issue #6)
- 22.04.M2: C — mu_RS biological plausibility
- 22.04.M3: C — Gaussian measurement model allows negative counts
- 22.04.M4: D — Simulation plots lack labeled observed data overlay (matches Human Issue #2)
- 22.04.M5: C — SARIMA residuals show heteroscedasticity; log-transform not considered
- 22.04.M6: C — Seasonal differencing order D not stated
- 22.04.M7: C — Forward simulation vs. filtering distribution distinction not acknowledged

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
