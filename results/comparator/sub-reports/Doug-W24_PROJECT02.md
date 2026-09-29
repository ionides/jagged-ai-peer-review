## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "POMP never out-performs ARIMA benchmark; likelihoods not on same scale" and also by finding: "ARMA and POMP log-likelihoods not on same scale")
- Human Issue #6: covered (matched by finding: "KPSS test p-value truncation / null hypothesis semantics misstated")
- Human Issue #7: covered (matched by finding: "Global search critically underpowered — only 2 valid results" and also by finding: "Global search parameter space disconnected from local search region")
- Human Issue #8: covered (matched by finding: "Particle count for likelihood evaluation too small (Np=5)")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "POMP never out-performs ARIMA benchmark; likelihoods not on same scale")
- Human Issue #11: missed

**Findings classification:**
- M1 (POMP never out-performs ARIMA; likelihoods not on same scale; conclusion dismisses gap): B — POMP model never out-performs ARIMA; conclusion premature; likelihoods not comparable (matches Human Issues #5 and #10)
- M2 (Global search critically underpowered — only 2 valid results of 50): B — global search yields only 2 finite-likelihood results, confirming search is incomplete (matches Human Issue #7)
- M3 (Particle count too small, Np=5 in key evaluation): B — particle count far too small, producing unreliable likelihood estimates and particle depletion (matches Human Issue #8)
- M4 (No profile likelihoods; identifiability unassessed): A — no profile likelihoods computed for any of 12 parameters
- M5 (Bird equation uses fox noise term — model/equation inconsistency): A — bird dynamics equation uses W_t^F instead of W_t^B, inconsistent with code
- M6 (Measurement model states Negative Binomial but code uses Normal): A — text claims Negative Binomial measurement model; code implements Normal distribution
- M7 (Global search parameter space disconnected from local search region): B — global search range excludes local search MLE region, explaining why local beats global (matches Human Issue #7)
- M8 (IF2 convergence not demonstrated; only 50 iterations): A — trace plots show non-convergence at Nmif=50; no convergence evidence provided
- mn1 (Bibliography hard-coded to local path): C — bibliography YAML path is a local absolute path, preventing reproduction
- mn2 (Data path hard-coded): C — read_excel uses absolute local path despite data file being in project's data/ directory
- mn3 (Q_fit_bird_local_mifs.rds contains extra parameters not in Rmd model): C — artifact contains 20 parameters belonging to a different, undescribed model
- mn4 (ARMA and POMP log-likelihoods not on same scale): D — ARIMA fitted to differenced series; POMP on undifferenced logCPUE; comparison invalid without Jacobian adjustment (matches Human Issue #5)
- mn5 (eval=FALSE on global search chunk): C — global search chunk not executed from provided Rmd; results loaded from absolute local path
- mn6 (KPSS test p-value truncation / null hypothesis semantics misstated): D — p-value > 0.05 described as "proving" stationarity; KPSS null is stationarity so this merely fails to reject (matches Human Issue #6)
- mn7 (Parameter γ can produce negative predation rates if γ>1): C — model does not constrain γ ≤ 1; (1−γR_t) can be negative
- mn8 (No simulation-based model validation): C — no forward simulation or filtering distribution comparison; only diagnostic plot from arbitrary starting parameters
- mn9 (ACF section cross-reference error): C — text references wrong figure label; PACF caption reads "ACF of logCPUE"
- mn10 (Missing sessionInfo() and package version documentation): C — no R session info or package versions documented beyond passing mention of pomp version
- mn11 (Rodent covariate treated as known without uncertainty): C — peak rodent year derived from six sources over 140 years; uncertainty not discussed or propagated
- mn12 (Species name misspelling): C — Latin name written as Lapagos lapagos instead of Lagopus lagopus

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
