## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Gaussian HMM AR(1) Model Is Acknowledged to Be Misspecified But No Resolution Is Provided — decreasing log-likelihood during IF2 iterations is identified as a classical signature of model misspecification")

**Findings classification:**
- Major Issue 1 (Global Search Anti-Pattern): A — prior mif2 result passed as first argument to mif2 in global search, anchoring near local optimum
- Major Issue 2 (Pseudo-Profile Likelihoods): A — no constrained IF2 optimization run; scatter plots of global-search results used in place of true profile likelihoods; chi-squared CIs statistically invalid
- Major Issue 3 (Initial Particle Filter on Simulated Data): A — AR-HMM initial particle filter evaluated on simulated data (sim1.filt) rather than real data
- Major Issue 4 (Heston Box Contains Undeclared Parameter sigma_nu): A — sigma_nu present in global search box but absent from heston_paramnames, creating silent mismatch
- Major Issue 5 (No Non-Mechanistic Benchmark): A — no comparison of POMP models against a simple non-mechanistic benchmark on a common likelihood scale
- Major Issue 6 (Inadequate Computational Effort for Heston): A — only 2,000 particles used for 9-dimensional Heston model; SE of log-likelihood not reported
- Major Issue 7 (AR-HMM Misspecification Unresolved): B — log-likelihood increases then decreases during IF2 iterations, identified as classical signature of model misspecification; model still included in formal comparison (matches Human Issue #1)
- Major Issue 8 (Model Comparison Table Mixes Incompatible Log-Likelihoods): A — ARMA, GARCH, and POMP log-likelihoods placed in same table without acknowledging incompatible observation models
- Major Issue 9 (Pairs Plot Typo): A — column name "01" is a typo for "p1" in the Gaussian HMM pairs plot call
- Minor Issue (eta missing from partrans): C — eta not given logit transform in t-HMM partrans despite being in (0,1)
- Minor Issue (single simulation for MLE validation): C — only nsim=1 trajectory used for visual MLE validation in t-HMM and Heston
- Minor Issue (last iteration estimator lacks justification): C — "last iteration estimator" used as heuristic when likelihood trace is non-monotone without formal statistical justification
- Minor Issue (no model diagnostics beyond visual simulation): C — conditional log-likelihood plots and ESS traces computed but not interpreted to identify model failure periods
- Minor Issue (data aggregation choice not validated): C — 97.5th percentile aggregation to 12-hour windows not compared to alternatives
- Minor Issue (missing sessionInfo and package versions): C — no R or package version record; reproducibility undermined
- Minor Issue (Heston non-standard log-volatility parameterization): C — Euler discretization uses exp(-Z) in mean-reversion term rather than standard Heston SDE form; justification not provided

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |
