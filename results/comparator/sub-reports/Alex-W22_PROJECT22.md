## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Finding 1 [Major] AIC Comparison Invalid: A — AIC comparison between GARCH and POMP is methodologically invalid due to incompatrable likelihood scales
- Finding 2 [Major] Simplified POMP Not Genuine POMP: A — simplified model with sigma_nu=0 eliminates latent state dynamics, no LRT performed
- Finding 3 [Major] No Formal Diagnostic Tests: A — no stationarity tests, ACF/PACF, or ARCH-LM tests on raw data
- Finding 4 [Major] Particle Filter Not Sufficiently Replicated: A — Nreps_eval=10 and Np=1000 too low; Monte Carlo error not reported across models
- Finding 5 [Major] Global Search Warm-Start Bias: A — all global search chains seeded from a single converged mif2 object rather than fresh starts
- Finding 6 [Major] Test Set Never Used: A — test set partitioned at the start but never referenced in analysis
- Finding 7 [Major] Force Negative Model Poorly Motivated: A — G fixed at -0.05 produces negligible leverage effect; model scientifically questionable
- Finding 8 [Moderate] No LRT Between POMP Variants: C — no likelihood ratio test between full and simplified POMP models
- Finding 9 [Moderate] Global Search Box Inconsistency: C — stated search box for Force Negative model contradicts narrower box used in code
- Finding 10 [Moderate] No Profile Likelihood: C — only point estimates reported; no confidence intervals for key parameters
- Finding 11 [Moderate] GARCH Residual Diagnostics Incomplete: C — no ACF/PACF of squared residuals or Ljung-Box test after GARCH fitting
- Finding 12 [Moderate] Non-Convergence Not Remediated: C — convergence plots show non-convergence but run_level 3 parameters are never used
- Finding 13 [Minor] Negative AIC Sign Convention: C — garch_aic function produces negative AIC values inconsistent with displayed log-likelihoods
- Finding 14 [Minor] Data Provenance Errors: C — minor errors in stated date range; observation counts not made explicit
- Finding 15 [Minor] No Simulation-Based Validation: C — single simulated trajectory used instead of percentile envelopes or formal simulation check

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
