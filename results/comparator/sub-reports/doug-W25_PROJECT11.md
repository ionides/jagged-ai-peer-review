## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Log-likelihood comparison between GJR-GARCH and POMP is not like-for-like due to t vs. Gaussian distributional mismatch")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Computational settings run_level=2 with Nmif=50, Np=1000 is borderline; more particles and iterations needed")
- Human Issue #7: covered (matched by finding: "Density plot title mislabeled as 'Density Plot of Gold Prices'")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Global IF2 search initialized from previous mif2 object): A — incorrect initialization of global search from stale IF2 chain rather than base pomp object
- Finding 2 (Global search box excludes region containing MLE for mu_h): A — box set to mu_h in (-1,0) but MLE is at -8.58, outside the box
- Finding 3 (Profile likelihood Monte Carlo variance dominates CI): A — profile uses Np=100 so SE up to 9.3 units exceeds chi-squared threshold of 1.92 units
- Finding 4 (Profile maximum substantially exceeds global search maximum): A — 16.2-unit discrepancy between profile max and global search max confirms global search failure
- Finding 5 (Simulated-data particle filter result presented as real-data benchmark): A — pfilter run on simulated data, not real AAPL data, making the comparison invalid
- Finding 6 (Log-likelihood comparison between GJR-GARCH and POMP not like-for-like): B — GJR-GARCH uses t-distribution while POMP uses Gaussian; conflates model structure with distributional choice (matches Human Issue #3)
- Finding 7 (No non-mechanistic benchmark under same observation model): A — sGARCH-norm and POMP achieve nearly equal log-likelihoods but the implication is not discussed
- Finding 8 (Profile likelihood plot filtered by round(H_0, 2) rather than phi): C — grouping variable uses H_0 instead of the profiled parameter phi
- Finding 9 (apple_params.csv contains stale entries from multiple runs): C — CSV accumulates implausible logLik > 8000 values from earlier exploratory runs
- Finding 10 (Computational settings run_level=2 with Nmif=50, Np=1000 borderline): D — authors acknowledge poor convergence; run_level=3 (Nmif=100, Np=2000) needed (matches Human Issue #6)
- Finding 11 (Inconsistency between stated best phi and parameter table): C — global search gives phi ~0.9 but profile CI is (0.959, 0.99)
- Finding 12 (Missing profile likelihood for additional parameters): C — only phi is profiled; sigma_nu, sigma_eta, mu_h also need profiles
- Finding 13 (Notation inconsistency: psi in prose but theta in ARMA equation): C — MA parameters called psi in text but theta_j in displayed equation
- Finding 14 (Density plot title mislabeled as "Density Plot of Gold Prices"): D — ggplot code title not updated from template/different dataset (matches Human Issue #7)
- Finding 15 (Missing sessionInfo() and no package version pinning): C — no sessionInfo() output and no renv snapshot in supplement

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
