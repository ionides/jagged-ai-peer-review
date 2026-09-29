## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "22.22.New2 — Normal measurement model not discussed in light of observed heavy tails; Student-t not considered")
- Human Issue #2: missed

**Findings classification:**
- 22.22.C1: A — No profile likelihoods or confidence intervals for any parameter
- 22.22.C2: A — No non-mechanistic benchmark comparison
- 22.22.C3: A — Convergence incomplete; key comparative claim within Monte Carlo noise
- 22.22.C4: C — AIC values not numerically reported for POMP models
- 22.22.C5: C — logLik SE not discussed relative to model comparison differences
- 22.22.C8: C — GARCH vs. POMP log-likelihood comparison not explicitly verified
- 22.22.C7: C — Train/test split defined but never used
- 22.22.New1: C — Conditional log-likelihood diagnostic not computed
- 22.22.New2: D — Normal measurement model not discussed in light of observed heavy tails; Student-t not considered (matches Human Issue #1)
- 22.22.C10: C — Force-negative model has arbitrary fixed G_0 = -0.05 without justification

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |
