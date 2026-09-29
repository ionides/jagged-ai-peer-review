## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Presentation — missing reference list")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- 22.03.2: A — ARIMA vs POMP comparison is ungrounded; ARIMA log-likelihood never reported for comparison
- 22.03.3/22.03.4: A — dmeas contains stochastic draw and illegal likelihood clipping, making particle filter weights invalid
- 22.03.5: A — no convergence diagnostics (trace plots) shown for mif2 runs
- 22.03.6: A — no POMP parameter estimates reported
- 22.03.1: C — transformation pipeline ambiguity (log-differenced EDA vs ARIMA d=1)
- 22.03.7: C — AR root of 1.01363 near unit circle not discussed
- 22.03.8: C — R² reported but not a meaningful metric for ARIMA estimated by MLE
- 22.03.9: C — periodogram spike at Nyquist frequency left unexplained
- 22.03.10: C — total Twitch user base (N=41.5M) used as population size without justification
- 22.03.11: C — residual ACF prematurely described as white noise without Ljung-Box test
- Presentation-missing-reference: D — single citation "[1]" has no bibliography entry (matches Human Issue #5)
- Presentation-supplement-formatting: C — POMP supplement appears to be a browser-printed HTML file with local file path in header
- Unacknowledged-strength-forward-simulation: C — forward simulation trajectories qualitatively consistent with observed data not acknowledged as supporting evidence

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
