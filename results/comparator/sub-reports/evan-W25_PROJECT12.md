## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "25.12.2 — AIC value for ARIMA stated in text does not match the table or the log-likelihood")

**Findings classification:**
- 25.12.1: A — physically impossible Heston parameter estimates (sigma < 0, v0 < 0); not raised by human
- 25.12.2: B — AIC value for ARIMA(2,0,2) stated in text is inconsistent with both the table and the log-likelihood (matches Human Issue #9)
- 25.12.3: A — GARCH specification mislabeled in final comparison table (Table 5 says GARCH(1,3) but Section 4 selects GARCH(1,1)); not raised by human
- 25.12.4: A — kappa profile flat on the left, no lower confidence bound determinable despite claim of identifiability; not raised by human
- 25.12.5: A — sigma_2 profile shows two local maxima with a valley, inconsistent with reliable profiling; not raised by human
- 25.12.6: A — logit inversion error (p11 computed incorrectly) and resulting near-random regime switching; not raised by human
- 25.12.7: A — ESS not monitored or reported for particle filter; not raised by human
- 25.12.8: A — no confidence intervals reported for any parameter; not raised by human
- 25.12.M3: A — introduction promises predictive accuracy evaluation but only in-sample log-likelihoods are presented; not raised by human
- 25.12.10: C — Heston trace plots interpreted as "strong convergence" without noting algorithm converged to a physically inadmissible region; not raised by human
- 25.12.11: C — number of pfilter replicates and logmeanexp aggregation not stated; not raised by human
- 25.12.12: C — ARMA(2,2) selected in Section 3 but Section 4 twice refers to ARMA(1,1)+GARCH(1,1); not raised by human
- Notation/presentation: C — LaTeX rendering error in GARCH-t variance equation, inconsistent figure numbering, Wikipedia reference, y-axis label cut off; not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
