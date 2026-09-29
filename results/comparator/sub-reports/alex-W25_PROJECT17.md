## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 7: "No EDA beyond visual inspection — STL seasonality identified at end as diagnostic rather than at the start; seasonality should have been detected and discussed before model fitting")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding 15: "Hypothesis framing tied to regulatory narrative is weakly supported — evidence chain tenuous, conclusion overstates the strength of evidence for regulation limiting leverage")
- Human Issue #8: covered (matched by finding 5: "No parameter transformations for tau and amplitude; positivity constraints not enforced — tau can go negative or to zero without log transformation")

**Findings classification:**
- Finding 1 (Hard-coded regime-shift windows — data snooping): A — Major finding; human did not raise it
- Finding 2 (Missing daily data file prevents reproducibility): A — Major finding; human did not raise it
- Finding 3 (AIC selection inconsistency with final GARCH model fit): A — Major finding; human did not raise it
- Finding 4 (GARCH model labeling error T-GARCH(3,1) vs T-GARCH(1,3)): A — Major finding; human did not raise it
- Finding 5 (No parameter transformations for tau/amplitude; positivity not enforced): B — Major finding (matches Human Issue #8)
- Finding 6 (Leftover development comments in submitted code): C — Minor finding; human did not raise it
- Finding 7 (No EDA beyond visual inspection; seasonality found late not early): D — Minor finding (matches Human Issue #3)
- Finding 8 (AIC penalty adequacy — 1.4-unit difference not decisive): C — Minor finding; human did not raise it
- Finding 9 (Regime-amplitude parameter not consistently identified across models): C — Minor finding; human did not raise it
- Finding 10 (Rw.sd for tau disproportionately large relative to other parameters): C — Minor finding; human did not raise it
- Finding 11 (Equation 4 notation inconsistency between base and t-distribution models): C — Minor finding; human did not raise it
- Finding 12 (No simulation-based diagnostics for final SV models): C — Minor finding; human did not raise it
- Finding 13 (Filtered log-likelihood for simulated data is misleading): C — Minor finding; human did not raise it
- Finding 14 (Demeaning formula mismatch between equation and code): C — Minor finding; human did not raise it
- Finding 15 (Hypothesis framing tied to regulatory narrative weakly supported): D — Minor finding (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
