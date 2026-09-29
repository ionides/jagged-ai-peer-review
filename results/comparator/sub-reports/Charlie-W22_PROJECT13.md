## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Factor-of-14 scaling in measurement model is unjustified for daily data")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Lack of quantitative comparison between California and Texas models")
- Human Issue #7: covered (matched by finding: "Texas initial likelihood evaluated with California parameters (code-order bug)")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Insufficient computation: local search at debugging-level settings")

**Findings classification:**
- Finding 1 (pseudo-profile likelihood): A — profile likelihood is a likelihood slice from global search scatter, not a true optimization over nuisance parameters
- Finding 2 (global search box misaligned): A — lower bound for b4 set at 700 while MLE converges near 221
- Finding 3 (Texas pfilter uses California params): B — code-order bug causes Texas starting-value likelihood to be evaluated with California parameters (matches Human Issue #7)
- Finding 4 (insufficient computation): B — local search run at run_level=1 with 50 particles and 5 iterations (matches Human Issue #10)
- Finding 5 (global search code absent from Rmd): A — reproducibility failure; actual global search computation not present in displayed code
- Finding 6 (no benchmark comparison): A — no non-mechanistic baseline fitted to either state
- Finding 7 (factor-of-14 scaling unjustified): B — phi=14 multiplier borrowed from a weekly-data project, unexplained and distorts parameter interpretation for daily data (matches Human Issue #4)
- Finding 8 (rho described at wrong transition): C — text says reporting occurs at E→I but code accumulates I→R transitions
- Finding 9 (Texas rw.sd specifies extra params): C — b3 and b4 listed in rw.sd but not in Texas model's paramnames
- Finding 10 (tau perturbation effectively zero): C — rw.sd of 0.0001 on log scale effectively fixes tau during filtering
- Finding 11 (fixed epidemiological parameters without sensitivity analysis): C — mu_EI and mu_IR fixed throughout with no sensitivity check
- Finding 12 (no model diagnostics): C — no ESS plots, no conditional log-likelihood plots, no filtering-distribution comparison
- Finding 13 (profile likelihood only for rho): C — contact-rate parameters b1–b4 have no uncertainty quantification despite weak identifiability
- Finding 14 (lack of quantitative comparison between CA and TX): D — no formal comparison of log-likelihoods, contact rates, or reporting rates across states (matches Human Issue #6)
- Finding 15 (policy-effect interpretation not grounded in identifiability): C — conclusion about CDC guideline effect not supported given unquantified identifiability of b3 and b4

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
