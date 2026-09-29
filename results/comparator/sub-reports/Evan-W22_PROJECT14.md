## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "22.14.3 — Severe ESS Collapse / Gaussian Measurement Model, suggesting t-distributed measurement model")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "22.14.4 — Breto Model Non-Convergence")
- Human Issue #5: covered (matched by finding: "22.14.5 — Heston Local Search: Declining MIF2 Log-Likelihood Trace")
- Human Issue #6: covered (matched by finding: "Missing figure captions — none of the 23 figures have descriptive captions")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- 22.14.3 (Severe ESS Collapse / Gaussian Measurement Model): B — pervasive ESS collapse indicates Gaussian noise misspecification; recommends t-distributed model (matches Human Issue #1)
- 22.14.4 (Breto Model Non-Convergence): B — sigma_eta drifts to extreme values, chains not converged after 200 iterations (matches Human Issue #4)
- 22.14.5 (Heston Local Search Declining Trace): B — loglik declines monotonically during local search, opposite of expected pattern (matches Human Issue #5)
- 22.14.6 (No Profile Likelihoods or Confidence Intervals): A — no profile likelihoods computed for any parameter in either model
- 22.14.M2 (V_0 Non-Convergence in Heston): A — initial condition V_0 still spreading after 200 MIF2 iterations, not identified
- 22.14.1r (Cross-Model Likelihood Comparison): C — comparison of raw log-likelihoods across garchFit and pomp not explicitly justified
- 22.14.M3 (ARMA Model Selection): C — ARMA(4,4) fits better by ~14.6 AIC units but AR(4) selected "for simplicity" without acknowledgment
- 22.14.13 (Reproducibility): C — no sessionInfo() or R package version information provided
- Typographical errors: C — "Simple Sotchastic Volatility," "Comparsion," "time-seris" should be corrected
- Missing figure captions: D — none of the 23 figures have descriptive captions (matches Human Issue #6)
- Citation quality: C — Heston model cited via Wikipedia instead of original Heston 1993 source

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
