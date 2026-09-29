## Evan

**Coverage record:**
- Human Issue #1: contradiction (AI 21.03.1 says computation is "critically insufficient" and "no conclusion... can be drawn from these results"; human says "not a problem with the maximization, which reliably gets within 5-10 log units of the maximum")
- Human Issue #2: covered (matched by finding: "SIRV1 vaccination transition probability S-dependence inconsistency — equation/code mismatch in the vaccination rate formula")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "SIRV1 outperforms SIRV2 in likelihood without explanation — SIRV2's unexplained underperformance")
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- 21.03.1: F — critically insufficient computation (contradicts Human Issue #1: AI says no conclusions can be drawn; human says maximization reliably gets within 5-10 log units)
- 21.03.2: A — no non-mechanistic benchmark comparison
- 21.03.3: A — forecast simulation uses starting-guess parameters, not MLE
- 21.03.4: A — accumulator H tracks recoveries rather than new infections
- 21.03.5: B — SIRV1 outperforms SIRV2 in likelihood without explanation (matches Human Issue #4)
- 21.03.6: C — profile likelihood for sigma has CI cutoff suppressed and too few points
- 21.03.7: D — SIRV1 vaccination transition probability has S-dependence inconsistency between equations and code (matches Human Issue #2)
- 21.03.M1: C — measurement model uses Binomial; overdispersion not considered
- 21.03.M2: C — EDA is limited; no ACF or log-scale examination
- 21.03.M3: C — computational settings hidden from rendered output
- 21.03.M4: C — minor writing errors ("agasinst", "EXISTING!")

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 1 |
