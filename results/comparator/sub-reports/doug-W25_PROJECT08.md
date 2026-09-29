## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ACF interpretation error — authors describe ACF as showing non-stationary patterns then conclude stationarity, a self-contradiction that reflects the same faulty stationarity reasoning")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no benchmark comparison — no AIC table comparing ARIMA/GARCH/POMP"; also matched by finding: "no model diagnostics including conditional log-likelihoods of individual observations")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (Global search box for phi excludes optimal parameter region): A — Major; not raised by humans
- Finding 2 (Measurement model misdescription in submitted document): A — Major; not raised by humans
- Finding 3 (No benchmark comparison for the POMP model): B — Major; no AIC table comparing ARIMA, GARCH, GJR-GARCH, and POMP-SV (matches Human Issue #7)
- Finding 4 (No profile likelihoods — parameter identifiability not quantified): A — Major; not raised by humans
- Finding 5 (No model diagnostics — conditional log-likelihoods, ESS, simulation comparisons): B — Major; absence of per-observation conditional log-likelihoods and ESS monitoring (matches Human Issue #7)
- Finding 6 (Holdout set defined but never evaluated): A — Major; not raised by humans
- Finding 7 (Insufficient computational effort — global search fails to improve on local search): A — Major; not raised by humans
- Finding 8 (ACF interpretation error in Section 3.1): B — Major; ACF described as showing non-stationary patterns for an already-stationary series, then contradicted by authors' own stationarity conclusion — same faulty stationarity reasoning as human issue (matches Human Issue #1)
- Finding 9 (Notation inconsistency in Section 6.2 — sigma_nu initialization): C — Minor; not raised by humans
- Finding 10 (Unfinished draft note left in Section 8.2): C — Minor; not raised by humans
- Finding 11 (Reference [11] used for two different works; Reference [12] URL mismatch): C — Minor; not raised by humans
- Finding 12 (ARIMA residual description uses implausible units): C — Minor; not raised by humans
- Finding 13 (Beta standard error formula is incorrect): C — Minor; not raised by humans
- Finding 14 (STL decomposition applied to non-stationary prices): C — Minor; not raised by humans
- Finding 15 (First log-return set to zero rather than NA): C — Minor; not raised by humans

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
