## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Primary Conclusion Depends on the Poisson Model, Which Is Strongly Outperformed by Negative Binomial")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Transition Density Formula Contains a Typo")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (Incorrect Sign Interpretation for gamma): A — covariate sign misinterpreted; human did not raise this
- Finding 2 (Profile Likelihood from suboptimal starting box): A — profile CI based on local not global MLE; human did not raise this
- Finding 3 (Optimal AR(1) parameters show no momentum): A — phi ~ -0.02 makes process effectively IID, conclusion misleading; human did not raise this
- Finding 4 (Transition Density Typo): B — exponent missing x_n term, density does not depend on x_n (matches Human Issue #5)
- Finding 5 (Primary Conclusion Depends on Poisson, Outperformed by NB): B — Poisson is poor fit relative to NB; conclusion not robust; NB yields no evidence for momentum (matches Human Issue #1)
- Finding 6 (NBin AR1 MLE worse than NBin Static): A — AR1 NB slightly worse than nested static NB, indicating convergence failure; human did not raise this
- Finding 7 (run_level hardcoded to "explore"): C — code cannot reproduce stored results; human did not raise this
- Finding 8 (Pairwise scatterplot mislabeled in Local Search section): C — presentation inconsistency; human did not raise this
- Finding 9 (Wilks approximation may not apply due to boundary parameter): C — boundary parameter issue with chi-squared df = 2; human did not raise this
- Finding 10 (No exploratory autocorrelation analysis before model construction): C — no ACF plot despite central research question being about temporal autocorrelation; human did not raise this
- Finding 11 (Code comment "log(mu) represents expected runs" incorrect): C — parameterization confusion in comment; human did not raise this
- Finding 12 (Inconsistent parameter_trans between files): C — minor inconsistency in initial POMP object; human did not raise this
- Finding 13 (No model adequacy assessment via simulation): C — no formal goodness-of-fit check at MLE; human did not raise this
- Finding 14 (Opponent strength uses season-wide future data): C — covariate construction violates causal structure; human did not raise this
- Finding 15 (nrow(opp_pitch_games > 0) incorrect code): C — logic error that happens to work in context; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
