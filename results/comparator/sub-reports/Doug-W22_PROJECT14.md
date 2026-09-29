## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Non-Convergence of Both POMP Models Is Explicitly Acknowledged but Results Are Still Interpreted")
- Human Issue #5: covered (matched by finding: "Non-Convergence of Both POMP Models Is Explicitly Acknowledged but Results Are Still Interpreted")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Breto Global Search Initialized from Previous mif2 Result): A — global search inherits cooled perturbation schedule from prior IF2 chain, invalidating coverage claim
- Finding 2 (Breto Initial Particle Filter Evaluated on Simulated Data): A — pfilter run on sim1.filt not eth.filt, making the benchmark log-likelihood meaningless for real-data comparison
- Finding 3 (Heston rprocess Algebraically Misspecified): A — code applies sqrt(V) to autoregressive term, departing from stated equation phi*V
- Finding 4 (Non-Convergence of Both POMP Models Acknowledged but Results Still Interpreted): B — authors explicitly note convergence failures yet report and compare log-likelihood values as if they are MLEs (matches Human Issues #4 and #5)
- Finding 5 (No Profile Likelihoods or Confidence Intervals): A — key parameters estimated with no uncertainty quantification and no identifiability assessment
- Finding 6 (AIC Comparison Does Not Account for Monte Carlo Noise): A — exact GARCH/ARMA likelihoods compared to noisy POMP estimates without SE reporting
- Finding 7 (bake() Cache Double-Evaluation Pattern): A — same cache filename called twice; fragile code structure that would break if cache is cleared
- Finding 8 (Missing Model Diagnostics: No Conditional Log-Likelihoods, ESS Plots, or Simulation Envelopes): A — no conditional log-likelihoods, no ESS time series, no simulation envelopes overlaid on observed returns
- Finding 9 (Undefined Variable eth.sd_ivp in Breto rw.sd): C — dead code with typo in outer rw.sd definition; does not affect cached computation
- Finding 10 (Heston phi Search Box Spans (0,1) on logit-Transformed Scale): C — box effectively unconstrained on logit scale, inconsistent with text's implied constraint
- Finding 11 (Breto sigma_eta Search Box Implausibly Wide at 0.5–600): C — three-order-of-magnitude range not discussed; no check whether MLE is interior or boundary
- Finding 12 (Heston Local Search rw.sd Defined but Different Value Effectively Used): C — unused crypto_rw.sd_rp/ivp variables create confusion about which rw.sd was applied
- Finding 13 (Log-Likelihood Numbers Presented Without SE): C — bare integers reported in conclusion with no Monte Carlo standard errors
- Finding 14 (Stationarity Assessment Informal and Potentially Incorrect): C — stationarity asserted from visual inspection without any formal test
- Finding 15 (Missing References and Reproducibility Information): C — empty references section, no repository, no cached files, no tabulated MLE vectors

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
