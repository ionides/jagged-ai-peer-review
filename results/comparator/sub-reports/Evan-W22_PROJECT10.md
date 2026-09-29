## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Normal measurement model in SEAPIRD inappropriate; contrasts with NB used in SIR")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "SEAPIRD N=500,000 vs SIR N=50,000,000 unexplained discrepancy")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- 22.10.1: A — ARMA model selection internally inconsistent (ARMA(4,4) has lower AIC but ARMA(3,3) selected)
- 22.10.2: A — MA roots nearly on unit circle indicating near non-invertibility
- 22.10.3: A — SEAPIRD fit on 7-day smoothed data while SIR/ARMA fit on raw data, invalidating central comparison
- 22.10.4: B — Normal measurement model in SEAPIRD inappropriate for count data; SIR correctly used negative binomial (matches Human Issue #3)
- 22.10.5: A — SIR local search MC standard error of 6.98 log-likelihood units is too large to support reliable comparison
- 22.10.6: A — SEAPIRD parameters severely non-identifiable; large discrepancies between local and global optima unexplored
- 22.10.8: A — No profile likelihoods or confidence intervals computed for any parameter
- 22.10.9: D — SEAPIRD population size N=500,000 vs SIR N=50,000,000; 100-fold difference unexplained (matches Human Issue #5)
- 22.10.10: C — Np and Nmif not reported in text
- 22.10.11: C — 7-day periodicity identified in spectral analysis but not incorporated into POMP models
- 22.10.12: C — ARMA residual diagnostics show heavy tails and autocorrelation; distributional mismatch not diagnosed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
