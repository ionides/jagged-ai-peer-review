## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Decomposition applied to financial log-returns")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH model selection criterion inconsistency")
- Human Issue #7: covered (matched by finding: "No benchmark comparison against a non-mechanistic model"; also matched by finding: "Selective log-likelihood table")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "No profile likelihoods; parameter identifiability unaddressed")
- Human Issue #10: covered (matched by finding: "Computational adequacy is insufficient")
- Human Issue #11: missed

**Findings classification:**
- Major 1 (global search anti-pattern): A — global search initialized from previous mif2 result object invalidates global optimum claim
- Major 2 (log-likelihood discrepancy): A — particle filter benchmark of −1501 irreconcilable with IF2 results of ~2650/2655
- Major 3 (no benchmark comparison): B — no common log-likelihood or AIC reported across ARMA, GARCH, and POMP models (matches Human Issue #7)
- Major 4 (no profile likelihoods): B — no profile likelihoods computed; phi and sigma_nu identifiability unaddressed despite pair-plot evidence (matches Human Issue #9)
- Major 5 (computational adequacy): B — ESS collapses to near zero repeatedly with only Np=1000 particles, indicating particle degeneracy (matches Human Issue #10)
- Major 6 (measurement model not in text): A — dmeasure specifies Gaussian observation model but no probability distribution is written out in the manuscript
- Major 7 (variable naming error): A — write.table calls undefined variable local_results instead of r.if1, causing reproducibility gap
- Major 8 (no conditional log-likelihoods): A — per-time-step conditional log-likelihoods not discussed or used to diagnose model failures
- Major 9 (global search box too narrow): A — mu_h box c(−1,0) excludes the range −8 to 4 found by local search; sigma_eta box c(0.5,1) far too narrow
- Major 10 (initial conditions not assessed): A — G_0 and H_0 fixed without sensitivity analysis or justification
- Minor: Decomposition applied to financial log-returns: D — decompose() is meaningless for non-seasonal log-returns; "no seasonality" conclusion makes decomposition puzzling (matches Human Issue #3)
- Minor: GARCH model selection criterion inconsistency: D — basic GARCH grid search uses logLik.garch() and selects minimum (worst-fitting) model, inconsistent with AIC used elsewhere (matches Human Issue #6)
- Minor: Selective log-likelihood table: D — log-likelihood values for GARCH variants not collected into a single comparison table (matches Human Issue #7)
- Minor: run_level 3 same as level 2: C — run_level=3 does not increase particle count beyond Np=1000, providing no additional computational resources
- Minor: CatGPT citation: C — "CatGPT [2]" is not a valid academic citation for LaTeX equation writing
- Minor: Data non-reproducible at render time: C — live getSymbols() call means re-renders may produce different data without an archived snapshot
- Minor: Conclusion unsupported: C — concludes GARCH is best for forecasting but no formal forecasting comparison is presented
- Minor: No sessionInfo(): C — no session information or package version documentation provided
- Minor: phi transform note: C — global search box for phi is on original scale while logit transform is used internally; consistent but unexplained
- Minor: References 3 and 4 are course materials: C — two of six references are course notes and a student project, not peer-reviewed sources

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
