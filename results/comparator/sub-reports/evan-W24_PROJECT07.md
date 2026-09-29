## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH model selection inverted — min instead of max log-likelihood")
- Human Issue #7: covered (matched by finding: "Central conclusion unsupported by explicit quantitative comparison"; also matched by finding: "No explicit comparison table of log-likelihoods across model classes")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "ESS not monitored during particle filtering")
- Human Issue #11: missed

**Findings classification:**
- 24.07.M1: B — GARCH model selection inverted (min instead of max log-likelihood) (matches Human Issue #6)
- 24.07.M2: B — Central conclusion ("GARCH most effective") unsupported by explicit quantitative comparison (matches Human Issue #7)
- 24.07.M3: A — No profile likelihood; parameter identifiability not quantified
- 24.07.M5: A — run_level=3 uses only 1000 particles (same as run_level=2); convergence incomplete
- 24.07.M4r: D — No explicit comparison table of log-likelihoods across model classes (matches Human Issue #7)
- 24.07.M6: C — Initial conditions G_0=H_0=0 not justified
- 24.07.m1: C — Ljung-Box used as model selection criterion rather than diagnostic
- 24.07.new1: C — Live Yahoo Finance download creates reproducibility risk
- 24.07.new2: D — ESS not monitored during particle filtering (matches Human Issue #10)
- 24.07.m2: C — ACF "Lag 0.07" notation confuses fractional and integer lags

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
