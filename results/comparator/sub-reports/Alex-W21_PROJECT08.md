## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Gaussian HMM AR(1) likelihood goes up then down during MIF2, root cause is degenerate measurement via covariate trick")

**Findings classification:**
- Finding 1 (Log-Likelihood Not Comparable Across Models): A — log-likelihoods incomparable because Heston and AR(1) HMM use covariate filtering on a different probability space
- Finding 2 (t-HMM rprocess Uses euler() Instead of discrete_time()): A — structural mismatch makes t-HMM incomparable to Gaussian HMM
- Finding 3 (Gaussian HMM AR(1) Measurement Equation Is Trivial): B — authors note likelihood goes up then down in MIF2; Alex identifies root cause as degenerate covariate-trick measurement (matches Human Issue #1)
- Finding 4 (Heston Euler Discretization Incorrect for Log-Variance): A — code equations inconsistent with stated SDE; rho near 1.0 signals misspecification
- Finding 5 (No Formal Profile Likelihood CIs): A — only "poor man's" profile CIs used; no profiles for t-HMM or Heston
- Finding 6 (Pairs Plot Typo Silently Drops Parameter): C — `01` numeric literal used instead of `p1`; p1 omitted from diagnostic plot
- Finding 7 (Global Search Very Low Particle Count): C — Np=200 for Gaussian HMM global search vs. 1000-20000 elsewhere
- Finding 8 (AIC Parameter Count for ARMA+GARCH Wrong): C — parameter count listed as 6, should be 8
- Finding 9 (97.5th Percentile Aggregation Unjustified): C — no sensitivity analysis for choice of percentile or 12-hour window
- Finding 10 (HMM Transition Probabilities Confusingly Named): C — p0 is off-diagonal transition; prose interpretation potentially reversed
- Finding 11 (t-HMM dmeasure Unusual Coding Pattern): C — give_log passed as integer to dt(); correct but merits documentation
- Finding 12 (Heston Global Search Box Has Non-Existent Parameter): C — sigma_nu in search box not in heston_paramnames; silently ignored
- Finding 13 (Only 1-3 Simulations Shown): C — too few trajectories for predictive-envelope assessment
- Finding 14 (No Residual Diagnostics Beyond Visual): C — no PIT histograms, ACF of residuals, or systematic ESS discussion
- Finding 15 (Reference Numbering Error): C — entry [4] duplicated; subsequent numbers off by one

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |
