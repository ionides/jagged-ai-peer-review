## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "leverage and no-leverage models compared at incomparable computational levels")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "declining log-likelihood during local search misdiagnosed as overfitting")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major 1 (profile likelihood code evaluates global search parameters): A — profile logLik evaluation loop draws from if.box instead of if.prof, invalidating the CI
- Major 2 (incomparable computational run levels for leverage vs. no-leverage): B — leverage and no-leverage models fitted at run_level=3 vs. run_level=2 (matches Human Issue #4)
- Major 3 (declining log-likelihood misdiagnosed as overfitting): B — paper attributes declining local-search trajectory to overfitting rather than model misspecification (matches Human Issue #6)
- Major 4 (profile design uses only 100 of 600 starting points): A — loop bound of 100 covers only ~2–3 sigma_eta values out of 40 designed
- Major 5 (profile CI upper bound at boundary of search range): A — upper CI bound of 1 lies outside searched range [0.5, 0.95], indicating sigma_eta is not identified from above
- Minor: text misquotes its own numerical output: C — text reports max log-likelihood as 3483 when output shows 43483
- Minor: tseries::garch log-likelihood normalization not verified: C — normalization difference between tseries and fGarch not reconciled before comparison
- Minor: no formal AIC/LRT comparison for nested leverage/no-leverage models: C — raw log-likelihood comparison used without chi-squared test for 2 additional parameters
- Minor: no simulation-based goodness-of-fit from fitted model: C — only pre-fitting simulation shown; no forward simulations from MLE overlaid on observed returns
- Minor: initial pfilter applied to simulated data, not real data: C — initial likelihood test uses sim1.filt (simulated returns) rather than actual NASDAQ data
- Minor: spectral analysis applied to returns rather than squared returns: C — periodogram of demeaned returns tests conditional-mean autocorrelation rather than volatility cycles
- Minor: no profiles for phi, mu_h, or sigma_nu: C — only sigma_eta is profiled; identifiability of other key parameters unassessed
- Minor: model selection criteria switch between ARIMA and GARCH sections: C — AIC used for ARMA(5,5) selection but significance used for ARMA+GARCH order reduction
- Minor: stew cache files absent from repository: C — .rda cache files not submitted; reproduction requires multi-hour HPC re-run

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
