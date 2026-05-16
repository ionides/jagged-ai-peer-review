# Ned-Clean Analysis — W22 Project 22

## Human Issues

1. It would be interesting to see if a longer-tailed distribution for epsilon_n, such as t, fits better.
2. The global search suggests a bimodality (a collection of searches reaching a different and inferior region of parameter space) — this may help to understand numerical issues.

---

## Alex

**Coverage record:**
- Human Issue #1 (longer-tailed distribution / t-distribution): missed
- Human Issue #2 (bimodality in global search): missed

**Findings classification:**
- Finding 1 — AIC comparison GARCH vs POMP methodologically invalid: A
- Finding 2 — Simplified POMP not formally tested via LRT: A
- Finding 3 — No formal EDA diagnostics (ACF/PACF, stationarity tests, ARCH-LM): A
- Finding 4 — Particle filter likelihood estimates not sufficiently replicated (low Np, no SE table): A
- Finding 5 — Global search warm-start bias (anchored to if1[[1]]): A
- Finding 6 — Test set defined but never used: A
- Finding 7 — Force Negative model poorly motivated and scientifically questionable: A
- Finding 8 — No LRT or formal model selection between POMP variants [Moderate]: C
- Finding 9 — Global search box notation vs. actual box inconsistency [Moderate]: C
- Finding 10 — No profile likelihood or confidence intervals [Moderate]: C
- Finding 11 — GARCH residual diagnostics incomplete [Moderate]: C
- Finding 12 — Non-convergence acknowledged but not remediated [Moderate]: C
- Finding 13 — Negative AIC sign convention inconsistency [Minor]: C
- Finding 14 — Data provenance minor errors [Minor]: C
- Finding 15 — No simulation-based model validation [Minor]: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (longer-tailed distribution / t-distribution): missed
- Human Issue #2 (bimodality in global search): missed

**Findings classification:**
- Finding 1 — No non-mechanistic benchmark comparison [Major]: A
- Finding 2 — AIC comparison GARCH vs POMP not directly valid [Major]: A
- Finding 3 — No profile likelihoods for any parameter [Major]: A
- Finding 4 — Inadequate convergence — parameters "still fluctuating" without resolution [Major]: A
- Finding 5 — Global search starting box inconsistency in Force Negative model [Major]: A
- Finding 6 — Misinterpretation of sigma_nu convergence to zero as motivation to simplify [Major]: A
- Finding 7 — run_level = 2 throughout; final results are preliminary-grade [Minor]: C
- Finding 8 — Nreps_global = 20 is the minimum [Minor]: C
- Finding 9 — Initial simulation evaluated only visually [Minor]: C
- Finding 10 — Train/test split defined but never used [Minor]: C
- Finding 11 — Dmeasure inconsistent with Rproc (measurement model ambiguity) [Minor]: C
- Finding 12 — Simplified model not formally tested against original [Minor]: C
- Finding 13 — Pairs plots use different subsets across models [Minor]: C
- Finding 14 — GARCH likelihood from tseries may not be standard [Minor]: C
- Finding 15 — Conclusion lacks quantitative summary table [Minor]: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1 (longer-tailed distribution / t-distribution): missed
- Human Issue #2 (bimodality in global search): missed

**Findings classification:**
- Finding 1 — Global search anchored to local IF2 result; invalid global optimum [Major]: A
- Finding 2 — Self-diagnosed non-convergence treated as final estimates [Major]: A
- Finding 3 — No profile likelihoods; parameter identifiability not assessed [Major]: A
- Finding 4 — No benchmark comparison against non-mechanistic model [Major]: A
- Finding 5 — Invalid AIC comparison between GARCH and POMP [Major]: A
- Finding 6 — AIC computation uses summary log-likelihood, not maximum [Major]: A
- Finding 7 — Model diagnostics absent (no cond.logLik, ESS, filtering distribution) [Major]: A
- Finding 8 — Simplified POMP forced simplification without statistical test [Major]: A
- Finding 9 — Simulations presented as evidence of fit — visual comparison only [Minor]: C
- Finding 10 — Force-negative model interpreted without scientific justification [Minor]: C
- Finding 11 — Computational parameters at run level 2 [Minor]: C
- Finding 12 — Parameter transformation for mu_h not discussed [Minor]: C
- Finding 13 — EDA section lacks ACF/PACF of squared returns [Minor]: C
- Finding 14 — Conclusion claims simplified POMP has largest logLik — unverified [Minor]: C
- Finding 15 — References section incomplete [Minor]: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (longer-tailed distribution / t-distribution): covered (matched by finding: "Normal measurement model not discussed in light of heavy tails — motivates Student-t")
- Human Issue #2 (bimodality in global search): missed

**Findings classification:**
- 22.22.C1 — No profile likelihoods or confidence intervals [Major]: A
- 22.22.C2 — No non-mechanistic benchmark comparison [Major]: A
- 22.22.C3 — Convergence incomplete; key comparative claim within Monte Carlo noise [Major]: A
- 22.22.C4 — AIC values not numerically reported for POMP models [Minor]: C
- 22.22.C5 — logLik SE not discussed relative to model comparison differences [Minor]: C
- 22.22.C8 — GARCH vs POMP log-likelihood comparison not explicitly verified [Minor]: C
- 22.22.C7 — Train/test split defined but never used [Minor]: C
- 22.22.New1 — Conditional log-likelihood diagnostic not computed [Minor]: C
- 22.22.New2 — Normal measurement model not discussed in light of heavy tails [Minor]: D (matches Human Issue #1)
- 22.22.C10 — Force-negative model has arbitrary fixed G_0 = -0.05 without justification [Minor]: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 8 | 3 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 8 | 9 | 7 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 2 | 2 | 2 | 1 |

---

## Per-Reviewer Metrics

- **Alex:** Human Recall = (B+D)/(B+D+E) = (0+0)/(0+0+2) = 0/2 = **0.00**; AI-Unique Rate = (A+C)/(A+B+C+D) = (7+8)/(7+0+8+0) = 15/15 = **1.00**
- **Charlie:** Human Recall = (0+0)/(0+0+2) = 0/2 = **0.00**; AI-Unique Rate = (6+9)/(6+0+9+0) = 15/15 = **1.00**
- **Doug:** Human Recall = (0+0)/(0+0+2) = 0/2 = **0.00**; AI-Unique Rate = (8+7)/(8+0+7+0) = 15/15 = **1.00**
- **Evan:** Human Recall = (0+1)/(0+1+1) = 1/2 = **0.50**; AI-Unique Rate = (3+6)/(3+0+6+1) = 9/10 = **0.90**

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- Human Issue #2: The global search suggests a bimodality (a collection of searches reaching a different and inferior region of parameter space) — missed by all 4 reviewers.

Count: 1 out of 2 human issues (50%).

**Unique finds per reviewer:** Human issues covered by only one reviewer and missed by all others.

- Human Issue #1 (longer-tailed distribution): covered only by Evan (missed by Alex, Charlie, Doug).

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

The following concerns appear in all four reviewers' findings and were not raised by the human:

1. No profile likelihoods computed for any POMP parameter.
2. No non-mechanistic benchmark comparison (ARMA or i.i.d. baseline).
3. Invalid AIC/log-likelihood comparison between GARCH and POMP models.
4. Parameter non-convergence acknowledged but results treated as final / no remediation.
5. Global search methodology flawed (warm-start from local IF2 result or box inconsistency).
6. Train/test split defined but never used.
7. Force-negative model lacks scientific justification for its constraint.
8. Simplified model adopted without formal statistical test (LRT).
9. Simulation-based model validation is visual only.
10. Computational effort at run_level = 2 insufficient for final results.

Count: 10 universal AI-only flags.
