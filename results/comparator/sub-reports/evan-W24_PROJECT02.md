## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "24.02.1 — ARIMA fit to first-differenced series vs POMP fit to undifferenced series makes log-likelihoods incomparable")
- Human Issue #6: missed
- Human Issue #7: covered (matched by findings: "24.02.4 — global search worse than local search is a clear diagnostic of optimization failure" and "24.02.5 — global search worse than local search, search is broken")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "24.02.4 — convergence inadequately demonstrated; recommends diverse starting points")
- Human Issue #10: covered (matched by finding: "24.02.1 — conclusion that ARIMA outperforms POMP is unsupported because comparison is invalid")
- Human Issue #11: covered (matched by finding: "24.02.2 — reported log-likelihoods including -205 likely from unreplicated pfilter or mif2 internal estimates; pfilter output shows -288.64 with SE 30.88")

**Findings classification:**
- 24.02.1: B — invalid ARIMA vs POMP log-likelihood comparison; ARIMA fit to differenced series, POMP to undifferenced; conclusion of ARIMA superiority unsupported (matches Human Issues #5 and #10)
- 24.02.2: B — mif2 likelihoods reported without replicated pfilter; SE ~31 log units renders estimates meaningless; -205 vs shown -288.64 discrepancy (matches Human Issue #11)
- 24.02.4: B — convergence inadequately demonstrated; 20-iteration trace plots; global search worse than local search; recommends diverse starting points (matches Human Issues #7 and #9)
- 24.02.3: A — no profile likelihoods or confidence intervals; scatter plot shows non-identifiable parameters
- 24.02.5: B — global search worse than local search; global search is broken or miscoded (matches Human Issue #7)
- 24.02.6: C — measurement model noise structure biologically unusual; logRho initialization at 3 unexplained
- 24.02.7: C — inconsistent notation alternating between log.CPUE and logCPUE
- 24.02.8: C — Figure 2.4 caption says ACF but displays PACF
- 24.02.11: C — ARIMA residuals not validated; no residual ACF shown
- 24.02.13: C — no parameter estimate table; best-found parameter values not reported
- 24.02.15: C — AIC table inconsistency; text states 204.48 but table shows 204.21

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 1 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
