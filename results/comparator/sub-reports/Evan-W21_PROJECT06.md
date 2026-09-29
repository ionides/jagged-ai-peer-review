## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "21.06.3 — phi and sigma_eta identifiability: paper should not frame weak identifiability as a convergence problem but note profile likelihoods are needed to assess it")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "21.06.1 — AIC cross-class comparison needs qualification: POMP advantage over ARMA reflects modeling a richer feature, not just better optimization; models' differing scopes should be discussed")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "21.06.13 — Filtering-on-simulated-data section: text does not make clear the log-likelihood is from synthetic data, not real GME data; section needs explicit statement of purpose")

**Findings classification:**
- 21.06.5: A — MLE parameter estimates never reported in paper despite being written to CSV
- 21.06.14: A — No profile likelihoods or confidence intervals provided for any POMP parameter
- 21.06.4: A — Fixed leverage model (sigma_nu=0) never formally compared to stochastic leverage model
- 21.06.2: A — GARCH AIC table shows large non-monotone swings indicating numerical instability in higher-order fits
- 21.06.1: D — AIC cross-class comparison needs qualification; model scope differences should be discussed (matches Human Issue #7)
- 21.06.3: D — phi and sigma_eta slow convergence reflects weak identifiability, not a convergence problem; framing should change (matches Human Issue #5)
- 21.06.12: C — ARMA residual ACF shows significant correlations; specific lags should be named
- 21.06.13: D — Filtering-on-simulated-data section lacks explicit statement that log-likelihood is from synthetic data and why the section is there (matches Human Issue #10)
- ESS not monitored: C — Effective sample size during particle filtering never reported; filter degeneracy concern given GME's January 2021 spike
- Gaussian measurement model: C — dnorm measurement model may underfit heavy tails documented in QQ plots; Student-t alternative not discussed
- Typographical errors: C — "log-golatility" typo and inconsistent "loglikelihood"/"log-likelihood" usage

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
