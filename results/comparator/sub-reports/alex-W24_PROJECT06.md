## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF/PACF interpretation is incorrect — standard ACF/PACF roles are reversed")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "log(likelihood()) output is misinterpreted — per-observation vs total log-likelihood conflated")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "log(likelihood()) output is misinterpreted — per-observation vs total log-likelihood conflated")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (Log-likelihood values not comparable across models): F — contradicts Human Issue #10 (human says rugarch's `likelihood()` returns log-likelihood; AI says it returns likelihood, not log-likelihood)
- Finding 2 (POMP global search does not explore meaningful parameter space): A — no matching human issue
- Finding 3 (Key parameters do not converge in MIF2): A — no matching human issue
- Finding 4 (Particle filter evaluated on simulated object, not real data): A — no matching human issue
- Finding 5 (ACF/PACF interpretation is incorrect): B — matches Human Issue #6
- Finding 6 (Time series frequency specification is incorrect): C — no matching human issue
- Finding 7 (POMP model description notational inconsistency): C — no matching human issue
- Finding 8 (No profile likelihood or confidence intervals for POMP parameters): C — no matching human issue
- Finding 9 (GARCH(4,1) under normal noise overfitted and not justified): C — no matching human issue
- Finding 10 (log(likelihood()) output is misinterpreted): D — matches Human Issues #10 and #13
- Finding 11 (No simulation-based model validation for POMP): C — no matching human issue
- Finding 12 (Data description vague and partially incorrect): C — no matching human issue
- Finding 13 (stew() files and caching not reproducible): C — no matching human issue
- Finding 14 (Pairs plot threshold of 300 log-likelihood units too broad): C — no matching human issue
- Finding 15 (Conclusions section understates model problems): C — no matching human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 1 |
