## Evan

**Coverage record:**
- Human Issue #1: covered (matched by findings: "25.09.2 — dmeas and rmeas implement materially different win-probability formulas" and "Minor-scale — rmeas uses raw ELO scale; dmeas rescales by /100")
- Human Issue #2: covered (matched by finding: "25.09.5 — log-likelihood computed but never used; model selection rests entirely on prediction accuracy")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- 25.09.1: A — sigma is fixed at 5.00 throughout all searches, never optimized
- 25.09.2: B — dmeas and rmeas implement materially different win-probability formulas (matches Human Issue #1)
- 25.09.3: A — Model Att global search table is numerically identical to Model 1, indicating copy-paste
- 25.09.5: B — log-likelihood computed but never used; model selection rests entirely on prediction accuracy; AIC/LRT not applied (matches Human Issue #2)
- 25.09.4: A — Base ELO prediction accuracy reported as 57.93% in text but 66.46% in table
- 25.09.6: A — sim_win drawn inside rproc and used for state update before actual observation is incorporated
- 25.09.7: A — no confidence intervals or profile likelihoods computed for any parameter
- 25.09.8: A — only 20 mif2 iterations used; several parameters have not stabilized
- Minor-scale: D — rmeas uses raw ELO scale; dmeas rescales by /100, giving home_court_avd different quantitative meaning in each (matches Human Issue #1)
- Minor-pwin: C — p_win stored as state variable despite being a deterministic function of other states
- Minor-plusign: C — OPP equation has stray plus sign on line 312
- Minor-eloeq: C — ELO update equation displayed does not match the correct formula implemented in code
- Minor-partrans: C — Model 2 partrans may not include log = c("alpha"), unlike Model 1
- Minor-seed: C — no set.seed() calls; results not exactly reproducible
- Minor-software: C — R version and pomp version not reported
- Minor-captions: C — figure captions absent for Figures 003, 004, 011, 012, 013
- Minor-prose: C — repeated words and typographical errors throughout ("there is there is", "A a", etc.)
- Minor-insample: C — prediction accuracy figures appear to be in-sample with no training/test split noted

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
