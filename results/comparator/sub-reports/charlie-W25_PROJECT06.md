## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Log-ARMA vs. linear-ARMA MAPE comparison is not valid — MAPE on log scale and raw scale have no common interpretation")
- Human Issue #3: covered (matched by finding: "Three-model comparison uses incompatible metrics and data — POMP is never assigned a MAPE or out-of-sample metric")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "POMP model substantially underperforms ARMA benchmark by ~156 log-lik units with no acknowledgment")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Log-ARMA vs. linear-ARMA MAPE comparison is not valid — MAPE on log scale and raw scale have no common interpretation")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (POMP underperforms ARMA by 156 log-lik units, unacknowledged): B — matches Human Issue #6
- Finding 2 (Profile likelihood for ρ is not a true profile; wrong Wilks cutoff): A — no human issue raised this
- Finding 3 (`ivp()` mis-applied to non-IVP parameters in `rw.sd`): A — no human issue raised this
- Finding 4 (Text model contradicts code — births, deaths, importation absent from implementation): A — no human issue raised this
- Finding 5 (Three-model comparison uses incompatible metrics and data): B — matches Human Issue #3
- Finding 6 (`emeas` uses cumulative H, inconsistent with `dmeas`/`rmeas` using NewEI): A — no human issue raised this
- Finding 7 (No SARIMA considered despite prominent 52-week seasonality): A — no human issue raised this
- Finding 8 (`omega` absent from `rw.sd` in global search): C — no human issue raised this
- Finding 9 (Profile CI degenerate under correct Wilks threshold): C — no human issue raised this
- Finding 10 (Cooling fraction 0.3 departs from course standard without justification): C — no human issue raised this
- Finding 11 (Initial SEIR parameter values biologically implausible for chickenpox): C — no human issue raised this
- Finding 12 (Log-ARMA vs. linear-ARMA MAPE comparison invalid): D — matches Human Issues #2 and #9
- Finding 13 (`loglik.se < 10` filter excessively permissive): C — no human issue raised this
- Finding 14 (Redundant/inconsistent `partrans` re-specified inside local search `mif2`): C — no human issue raised this
- Finding 15 (Duplicate `library(pomp)`; auto-install without consent): C — no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
