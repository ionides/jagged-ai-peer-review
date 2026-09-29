## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Tesla POMP uses a different dataset than Tesla GARCH, invalidating cross-model comparisons" and finding: "conclusion that POMP outperforms GARCH contradicted by Ford likelihoods")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "incomplete parenthetical question '(why we want to use log return instead of return?)' left in final submission")

**Findings classification:**
- Finding 1 (Tesla POMP uses different dataset): B — Tesla POMP fitted to only 364 of 1,258 observations, making cross-model comparisons invalid (matches Human Issue #5)
- Finding 2 (POMP conclusion contradicted by Ford likelihoods): B — Ford GARCH achieves higher log-likelihood than POMP, directly contradicting the conclusion (matches Human Issue #5)
- Finding 3 (promised AIC comparison never delivered): A — three-way AIC comparison across ARIMA, GARCH, and POMP promised in introduction but absent
- Finding 4 (computation does not match reported methodology): A — Ford global search described as 100 replicates at 2,000 particles but saved .rda files show 20 replicates at 1,000 particles
- Finding 5 (no profile likelihoods): A — neither Ford nor Tesla POMP includes profile likelihood computations
- Finding 6 (leverage formula typographical error): A — numerator and denominator of R_n formula are identical, evaluating to 1 for all G_n
- Finding 7 (normal GARCH and t-GARCH likelihoods use different normalization): A — cross-table comparison potentially invalid due to different normalization conventions and effective sample sizes
- Finding 8 (Tesla prediction plot uses Ford forecast uncertainty): C — Figure 10 uses ford_ahead[,2] instead of tesla_ahead[,2] for prediction bands
- Finding 9 (Tesla POMP figure captions say "Apple"): C — chunk at line 751 labels Tesla figures as Apple; figure numbering restarts
- Finding 10 (Tesla POMP searches use sequential rather than parallel execution): C — Tesla uses %do% while Ford uses %dopar%, substantially increasing runtime
- Finding 11 (no benchmark comparison for POMP models): C — ARMA(0,0) not retained as baseline for POMP log-likelihood comparison
- Finding 12 (citation numbering inconsistent): C — Breto (2014) cited as [2] but [2] refers to a different source; Breto (2014) never listed
- Finding 13 (decomposition of log returns misinterpreted as meaningful trend): C — classical additive decomposition on near-white-noise returns does not reflect genuine price trends
- Finding 14 (phi search box overly narrow given bimodal behavior): C — phi restricted to (0.95, 0.99) may miss second mode visible in pair plots
- Finding 15 (incomplete parenthetical question left in submission): D — "(why we want to use log return instead of return?)" is an unresolved author note (matches Human Issue #9)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
