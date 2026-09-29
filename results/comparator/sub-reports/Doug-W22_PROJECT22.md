## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Finding 1 (Global search anchored to prior IF2 result): A — global search initialization coding error invalidates global optimum claim
- Finding 2 (Self-diagnosed non-convergence): A — authors acknowledge convergence failures yet present results as final
- Finding 3 (No profile likelihoods): A — parameter identifiability not assessed
- Finding 4 (No benchmark comparison): A — no ARMA-family baseline comparison performed
- Finding 5 (Invalid AIC comparison GARCH vs POMP): A — cross-model log-likelihood comparison is invalid
- Finding 6 (AIC uses summary log-likelihood, not maximum): A — AIC computations conflate median/summary loglik with maximum
- Finding 7 (Model diagnostics absent): A — no ESS traces, no conditional log-likelihoods, no filtering diagnostics
- Finding 8 (Simplified model — forced simplification without LRT): A — leverage parameters dropped without formal likelihood ratio test
- Finding 9 (Simulations as visual evidence only): C — visual comparison insufficient as goodness-of-fit metric
- Finding 10 (Force-negative model ad hoc): C — fixed G = -0.05 is arbitrary and unjustified
- Finding 11 (Run level 2 marginal effort): C — Np = 1000, Nmif = 100 insufficient for final analysis
- Finding 12 (Parameter transformation for mu_h): C — mu_h not noted as estimated on natural scale
- Finding 13 (EDA lacks ACF/PACF of squared returns): C — standard volatility clustering diagnostics absent
- Finding 14 (Conclusion claims largest maximized log likelihood — unverified): C — rank ordering from non-converged chains is unreliable
- Finding 15 (References incomplete): C — self-citation and student project references lack transparency

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
