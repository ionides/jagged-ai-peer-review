## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Missing forward simulation from best-fit parameters — initial simulation uses test params and is much more volatile than data; no post-fit simulation shown")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Missing forward simulation from best-fit parameters — initial simulation uses test params and is much more volatile than data; no post-fit simulation shown")
- Human Issue #7: covered (matched by findings: "No convergence diagnostics presented" and "No ESS monitoring reported")

**Findings classification:**
- Major Issue 1 (Invalid cross-model AIC comparison): A — AIC comparison across ARMA, GARCH, and POMP is invalid due to different likelihood scales and Monte Carlo noise
- Major Issue 2 (AIC from noisy max log-likelihood): A — per-chain log-likelihood uses only 20 PF replicates; max() selects chain with largest Monte Carlo noise, biasing AIC
- Major Issue 3 (Global IF2 initialized from previous mif2 result): A — global search passes if1[[1]] as first argument, inheriting decayed cooling schedule instead of starting fresh
- Major Issue 4 (Simulated-data PF result presented as real-data benchmark): A — particle filter on simulated data (sim1.filt) misleadingly compared to real-data fit
- Major Issue 5 (No convergence diagnostics): B — no log-likelihood vs. iteration or parameter trace plots for local or global IF2 searches (matches Human Issue #7)
- Major Issue 6 (No profile likelihoods or CIs): A — no profile likelihoods computed for any parameter; identifiability unassessed
- Major Issue 7 (No non-mechanistic benchmark comparison): A — ARMA and GARCH are not true non-mechanistic baselines; no formal LRT or uncertainty-aware AIC comparison
- Major Issue 8 (Erroneous POMP superiority claim): A — POMP AIC advantage of ~109 units reported without log-likelihood SE or acknowledgment of Monte Carlo variance
- Minor: Inconsistent index name (Nasdaq-100 vs Nasdaq-500): C — conclusion section refers to "Nasdaq-500" three times; straightforward factual error
- Minor: Parameter initialization discrepancy: C — text states phi=0.95 but code sets phi=0.995
- Minor: mu_h/G_0/H_0 partrans: C — G_0 and H_0 left untransformed; optimizer may drift outside search box bounds
- Minor: No ESS monitoring: D — ESS not reported or plotted for any particle filter run (matches Human Issue #7)
- Minor: rproc2.sim vs rproc2.filt not explained: C — split between simulation and filter process snippets is unexplained
- Minor: Global search box constructed from local-search pairs plot alone: C — only 20 local replicates; phi box (0.95, 0.99) may be too narrow
- Minor: No sessionInfo() or package version documentation: C — package versions not recorded; reproducibility at risk
- Minor: Missing forward simulation from best-fit parameters: D — no simulation from fitted MLE shown; initial simulation acknowledges over-volatility but no post-fit comparison provided (matches Human Issues #3 and #6)
- Minor: No financial interpretability of estimated parameters: C — claims parameters are "easier to interpret" but provides no interpretation of specific MLE values

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
