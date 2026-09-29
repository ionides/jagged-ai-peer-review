## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by findings: "local search convergence not achieved: ~100 log-unit spread" and "Nmif=50 below run_level=2 standard of 100 iterations")
- Human Issue #7: covered (matched by finding: "density plot title says 'Gold Prices' instead of 'Apple Stock Prices'")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "ARMA model selection narrative inconsistent; AIC table not shown to verify ARMA(1,1) is parsimony-optimal")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (GARCH diagnostics on eGARCH, not gjrGARCH): A — diagnostics run on wrong model; invalidates entire diagnostic section for chosen model
- Finding 2 (Profile Np=100 vs Np=1000 in main analysis): A — profile likelihood evaluated with ten times fewer particles than main analysis
- Finding 3 (Profile CI upper bound truncated at search boundary): A — CI upper bound of 0.99 equals the grid maximum; true upper bound may exceed it
- Finding 4 (Log-likelihood comparison across different datasets): A — GARCH fitted to raw log-returns, POMP fitted to mean-centered log-returns; values not comparable
- Finding 5 (Local search convergence not achieved: ~100 log-unit spread): B — matches Human Issue #6
- Finding 6 (Profile too sparse: only 10 grid points): A — fewer than 5 points above Wilks cutoff; CI not credibly bounded
- Finding 7 (Duplicate "Figure 4.2" caption): C — same caption number used for two different figures
- Finding 8 (Density plot title says "Gold Prices"): D — matches Human Issue #7
- Finding 9 (Pairs plot threshold 100 log units): C — filter includes all runs; obscures parameter structure near optimum
- Finding 10 (Simulation code ignores simulated data): C — sapply never uses sim argument; misrepresents what was computed
- Finding 11 (Profile only for phi; other parameters not assessed): C — identifiability of mu_h, sigma_eta, sigma_nu not assessed
- Finding 12 (ARMA model selection narrative inconsistent): D — matches Human Issue #9
- Finding 13 (Nmif=50 below run_level=2 standard): D — matches Human Issue #6
- Finding 14 (No out-of-sample evaluation): C — no rolling-window or train/test split despite stated forecasting goal
- Finding 15 (ARMA notation inconsistency): C — psi in description, theta_j in equation; inconsistent throughout Section 4

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
