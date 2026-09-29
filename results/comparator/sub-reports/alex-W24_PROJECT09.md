## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ARIMA fitting is applied to the wrong target variable — models conditional mean, not variance")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No formal likelihood ratio test between Breto model and no-leverage model")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Global search box bounds for the no-leverage model are implausibly wide")
- Human Issue #8: covered (matched by finding: "Definition of sigma_w^2 in the no-leverage model is stated but never verified; sigma_eta has different effective meanings across the two models")
- Human Issue #9: missed

**Findings classification:**
- Finding 1: A — Profile likelihood construction uses wrong particle filter object (if.box instead of if.prof)
- Finding 2: A — Likelihood comparison across models is not valid due to different data, parameterization, and sign conventions
- Finding 3: A — Periodogram applied to demeaned returns rather than squared/absolute returns (volatility proxy)
- Finding 4: B — ARIMA fitting applied to wrong target variable; models conditional mean not variance (matches Human Issue #2)
- Finding 5: A — No simulation-based model checking for the POMP Breto model
- Finding 6: B — No formal likelihood ratio test between Breto model and no-leverage model (matches Human Issue #4)
- Finding 7: B — Global search box bounds for the no-leverage model are implausibly wide, causing degenerate runs (matches Human Issue #7)
- Finding 8: C — Inconsistency in text-reported vs. output fGarch log-likelihood values
- Finding 9: C — ACF computed on demeaned returns rather than squared demeaned returns in the EDA
- Finding 10: C — Local search uses only a single starting point with no randomization
- Finding 11: C — run_level for the no-leverage model silently reduced to 2, creating unequal computational effort comparison
- Finding 12: C — Initial particle filter test applies to simulated data (sim1.filt) rather than real data (ndx.filt)
- Finding 13: C — No convergence diagnostics for the profile likelihood run
- Finding 14: D — Definition of sigma_w^2 never verified and sigma_eta not connected across the two models (matches Human Issue #8)
- Finding 15: C — Conclusion mischaracterizes the profile likelihood result as validation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
