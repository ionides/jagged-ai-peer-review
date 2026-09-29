## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Finding 1 (Global search init from local mif2 object): A — global search inherits cooled mif2 rather than fresh pomp object
- Finding 2 (Invalid SARMA–SEIR log-likelihood comparison): A — log-likelihoods not on same scale due to differing observation models
- Finding 3 (mu_EI and mu_IR fixed without identifiability justification): A — fixing transition rates inflates precision of other estimates
- Finding 4 (Profile rho based on only three points above threshold): A — statistically unreliable CI from three noisy profile points
- Finding 5 (Profile rho guess-stratification conflates all run ids): A — PARAMS_FILE accumulation biases profile coverage
- Finding 6 (No model diagnostic tools applied): A — ESS, conditional log-likelihoods, and filtering distributions all absent
- Finding 7 (Accumulator H tracks recoveries not new infections): C — semantic mismatch between H and confirmed cases data
- Finding 8 (rmeasure non-integer rounding with small rho*H): C — dmeas/rmeas internally consistent but needs verification against zero-count data
- Finding 9 (Initial conditions E=100, I=200 fixed without estimation): C — no sensitivity analysis for hard-coded initial infected counts
- Finding 10 (rho CI reference max may come from profile not global search): C — PARAMS_FILE not filtered to id==2 before computing cutoff
- Finding 11 (Computational effort at run_level=2 insufficient): C — loglik.se up to 0.62 at MLE with no evidence doubling NP is safe
- Finding 12 (SARMA grid search eval=FALSE, hiding model selection): C — actual model selection not reproduced during document compilation
- Finding 13 (No discussion of tau boundary-hugging): C — tau at upper bound suggests measurement model needs more overdispersion
- Finding 14 (IID negative binomial benchmark trivially easy to beat): C — temporal dependence alone explains the improvement over IID
- Finding 15 (Conclusion overstates model fit quality): C — SEIR is 47 log-likelihood units worse than SARMA; conclusion does not acknowledge failure

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
