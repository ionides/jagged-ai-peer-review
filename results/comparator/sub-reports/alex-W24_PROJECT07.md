## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Seasonal Decomposition Applied to Financial Returns Is Inappropriate")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH Model Selection Uses Minimum (Not Maximum) Log-Likelihood")
- Human Issue #7: covered (matched by finding: "GARCH Conclusion Is Inconsistent With the Diagnostic Plots")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "POMP Model Parameter Transformation Is Incomplete")
- Human Issue #10: covered (matched by finding: "Filter Diagnostics Show Severe Particle Depletion")
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Global Search Starts From Single Local MIF2 Object): A — critical implementation bug; global search inherits a single local run instead of restarting fresh
- Finding 2 (Particle Filter Benchmark Uses Simulated Data): A — benchmark log-likelihood is computed on simulated, not real, data
- Finding 3 (Log-Likelihood Values Implausibly High): A — MIF2 log-likelihoods ~2650 are implausibly large and not sanity-checked
- Finding 4 (Mismatch Between Benchmark -1501 and MIF2 ~2650): A — >4000-unit discrepancy between benchmark and search results is unexplained
- Finding 5 (ARMA Grid Search Excludes Low-Order Models): A — grid starts at p,q=1 so ARMA(0,0)/AR(1)/MA(1) never evaluated
- Finding 6 (GARCH Model Selection Uses Minimum Log-Likelihood): B — selection criterion inverted (minimizing instead of maximizing log-likelihood), GARCH evaluation is incorrect (matches Human Issue #6)
- Finding 7 (Convergence Diagnostics Visually Poor and Insufficiently Discussed): A — sigma_nu does not converge; text claims global convergence contradicts visual
- Finding 8 (Filter Diagnostics Show Severe Particle Depletion): B — effective sample size collapses to near zero across many time points (matches Human Issue #10)
- Finding 9 (POMP Parameter Transformation Incomplete): B — phi near boundary (close to 1), near-unit-root behavior not flagged (matches Human Issue #9)
- Finding 10 (sigma_eta Anomalously Large in Local Search): A — sigma_eta ranges 0–30, physically implausible and uninvestigated
- Finding 11 (Seasonal Decomposition Inappropriate for Financial Returns): B — additive decomposition mis-specified for returns; adds no value (matches Human Issue #3)
- Finding 12 (ACF Lag Axis Misinterpreted): A — reported "lag 0.07" corresponds to ~18 days; authors do not recognize frequency scaling
- Finding 13 (GARCH Conclusion Inconsistent With Diagnostic Plots): B — no formal likelihood comparison between GARCH and POMP model is made (matches Human Issue #7)
- Finding 14 (Local Search Saves Wrong Variable to CSV): A — write.table references undefined variable local_results instead of r.if1
- Finding 15 (Excessive Reliance on Prior Course Material): A — POMP code borrowed from prior project with no novel contribution explained

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 5 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
