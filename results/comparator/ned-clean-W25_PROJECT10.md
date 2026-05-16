# Ned-Clean Analysis — W25 Project 10

---

## Human Issues

1. Diagnostic plots to explore why the POMP model is not fitting well are missing; likelihood anomaly diagnostics (e.g., as in the measles case study from Chapter 18) would have helped explain the poor fit.
2. The decreasing log-likelihood with iteration indicates model misspecification; the proposed solution (more particles or smaller random walk step size) will not fix this — the problem is that as random walk step size reduces, the model no longer fits well.
3. The report does not place the project in the context of other 531 projects or a broader literature; the team should say what they learned from previous projects, as requested in the assignment description.
4. When AIC suggests a very large ARIMA such as (5,1,6), this may signal the need for alternative model specifications (e.g., fitting a trend instead).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Local search MIF2 traces show persistent non-convergence — LL rises then drifts downward")
- Human Issue #3: missed
- Human Issue #4: missed

**Findings classification:**
- Finding 1 (POMP LL worse than benchmarks, no revision attempted): A — AI major, human missed
- Finding 2 (Global search worse than local, no adequate diagnosis): A — AI major, human missed
- Finding 3 (Local search MIF2 traces show non-convergence; LL rises then drifts down): B — AI major, human also found (matches Human Issue #2)
- Finding 4 (Likelihood comparison invalid — differenced vs. undifferenced series): A — AI major, human missed
- Finding 5 (Pooling individual data into population-level series destroys panel structure): A — AI major, human missed
- Finding 6 (X_0 treated asymmetrically between local and global searches): A — AI major, human missed
- Finding 7 (No profile likelihood or confidence intervals for any parameter): A — AI major, human missed
- Finding 8 (ARIMA/POMP incompatible treatment of non-stationarity): A — AI major, human missed
- Finding 9 (Particle count in global search lower than local search, not justified): C — AI minor, human missed
- Finding 10 (AIC table computed on differenced series, d hard-coded as 0): C — AI minor, human missed
- Finding 11 (OLS LL back-computed from AIC rather than extracted directly): C — AI minor, human missed
- Finding 12 (No simulation-based predictive check at MLE): C — AI minor, human missed
- Finding 13 (Data proprietary, not reproducible externally): C — AI minor, human missed
- Finding 14 (Long-run equilibrium implied by model not discussed): C — AI minor, human missed
- Finding 15 (Uniform rw.sd = 0.01 for all parameters regardless of scale): C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "IF2 Optimization Has Not Converged — LL drifts downward after peak")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "AIC Grid Search Uses Differenced Data Without Justification — trend-stationary alternative noted")

**Findings classification:**
- Finding 1 (Global search initialized from previous mif2 result object): A — AI major, human missed
- Finding 2 (LL comparisons on incommensurable objects — differenced vs. levels): A — AI major, human missed
- Finding 3 (No profile likelihoods or CIs for any parameter): A — AI major, human missed
- Finding 4 (IF2 optimization not converged — LL drifts downward after peak): B — AI major, human also found (matches Human Issue #2)
- Finding 5 (Data cannot be shared, analysis not reproducible): A — AI major, human missed
- Finding 6 (Uniform rw.sd = 0.01 for all parameters regardless of scale): A — AI major, human missed
- Finding 7 (Global search box excludes X_0, fixes it at single value): A — AI major, human missed
- Finding 8 (Model validation through simulation inadequate — only pre-optimization simulations): A — AI major, human missed
- Finding 9 (Pooling across individuals — ecological fallacy risk): A — AI major, human missed
- Finding 10 (Differencing not formally justified; trend-stationary alternative more efficient): D — AI minor, human also found (matches Human Issue #4)
- Finding 11 (ARIMA notation inconsistency — ARMA(5,6) vs ARIMA(5,1,6)): C — AI minor, human missed
- Finding 12 (Missing pomp package version and sessionInfo()): C — AI minor, human missed
- Finding 13 (ESS of particle filter not monitored): C — AI minor, human missed
- Finding 14 (Stationarity claim justified only visually, no formal test — distinct from finding 10 in focus on POMP model's handling): C — AI minor, human missed
- Finding 15 (Negligible sigma_proc implies degenerate latent structure): C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Computational Adequacy — Local Search Convergence is Incomplete; LL trace decreases after peaking")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "AIC Grid Search Uses Differenced Data Without Justification — deterministic trend alternative noted")

**Findings classification:**
- Finding 1 (Global search dramatically underperforms local search — global MLE unreliable): A — AI major, human missed
- Finding 2 (Invalid LL comparison between ARIMA and POMP models): A — AI major, human missed
- Finding 3 (No profile likelihoods — parameter identifiability completely unassessed): A — AI major, human missed
- Finding 4 (Process-noise vs measurement-noise trade-off indicates model misspecification): A — AI major, human missed
- Finding 5 (Computational adequacy — local search convergence incomplete; LL drops after peak): B — AI major, human also found (matches Human Issue #2)
- Finding 6 (No benchmark comparison on a common scale): A — AI major, human missed
- Finding 7 (Reproducibility severely compromised — data cannot be shared): A — AI major, human missed
- Finding 8 (AIC grid search uses differenced data without justification; deterministic trend alternative noted): D — AI minor, human also found (matches Human Issue #4)
- Finding 9 (ARIMA order notation inconsistency): C — AI minor, human missed
- Finding 10 (Simulation from initial guess shows no trend despite data trend): C — AI minor, human missed
- Finding 11 (Pairs plot based on invalid global search results): C — AI minor, human missed
- Finding 12 (Conclusion's AIC comparison mixes values from incompatible models): C — AI minor, human missed
- Finding 13 (Linear regression LL computed incorrectly for comparison purposes): C — AI minor, human missed
- Finding 14 (Physical activity covariate Energy dropped without analysis): C — AI minor, human missed
- Finding 15 (No out-of-sample or forecast evaluation): C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "C4 — Differencing not justified by formal test; deterministic trend alternative noted")

**Findings classification:**
- C1 (No profile likelihood or CI for noise coefficient b): A — AI major, human missed
- C2 (Benchmark comparison between incommensurable likelihoods — ARIMA differenced vs. POMP levels): A — AI major, human missed
- C3 (Global search discrepancy unexplained — undermines reported MLE): A — AI major, human missed
- M1 (Ecological fallacy risk from population-level pooling): A — AI major, human missed
- C4 (Differencing not justified by formal test; deterministic trend alternative noted): D — AI minor, human also found (matches Human Issue #4)
- C5 (No ESS monitoring; near-zero sigma_proc suggests filter degeneracy): C — AI minor, human missed
- C6 (No simulation-based model check at MLE): C — AI minor, human missed
- C7 (X_0 treated asymmetrically between local and global searches): C — AI minor, human missed
- C8 (AIC table caption mislabeled): C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 8 | 6 | 4 |
| B (AI major, human also found) | 1 | 1 | 1 | 0 |
| C (AI minor, human missed) | 7 | 5 | 7 | 4 |
| D (AI minor, human also found) | 0 | 1 | 1 | 1 |
| E (Human found, AI missed) | 3 | 2 | 2 | 3 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall | AI-Unique Rate |
|----------|-------------:|---------------:|
| Alex | (1+0)/(1+0+3) = 1/4 = 25.0% | (7+7)/(7+1+7+0) = 14/15 = 93.3% |
| Charlie | (1+1)/(1+1+2) = 2/4 = 50.0% | (8+5)/(8+1+5+1) = 13/15 = 86.7% |
| Doug | (1+1)/(1+1+2) = 2/4 = 50.0% | (6+7)/(6+1+7+1) = 13/15 = 86.7% |
| Evan | (0+1)/(0+1+3) = 1/4 = 25.0% | (4+4)/(4+0+4+1) = 8/9 = 88.9% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- **Human Issue #1** (Missing diagnostic plots / likelihood anomaly diagnostics for poor POMP fit): missed by Alex, Charlie, Doug, and Evan.
- **Human Issue #3** (Report does not place project in context of other 531 projects or broader literature): missed by Alex, Charlie, Doug, and Evan.

Count: 2 out of 4 human issues (50%) were missed by all reviewers.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2 (decreasing LL with iteration = misspecification; proposed solutions won't help): covered by Alex, Charlie, and Doug — not a unique find for any single reviewer.
- Human Issue #4 (large ARIMA suggests alternative model specifications): covered by Charlie, Doug, and Evan — not a unique find for any single reviewer.

No human issue was covered by exactly one reviewer to the exclusion of all others.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- **Invalid / incommensurable log-likelihood comparison** (ARIMA evaluated on differenced series vs. POMP on levels): raised as Major by Alex (Finding 4), Charlie (Finding 2), Doug (Finding 2), and Evan (C2).
- **No profile likelihood or confidence intervals for any parameter**: raised as Major by Alex (Finding 7), Charlie (Finding 3), Doug (Finding 3), and Evan (C1).
- **Global search produces far worse result than local search / global MLE unreliable**: raised as Major by Alex (Finding 2), Charlie (Finding 1), Doug (Finding 1), and Evan (C3).
- **Pooling individual-level data into population-level series / ecological fallacy risk**: raised as Major by Alex (Finding 5), Charlie (Finding 9), Doug (not as standalone major but present in context), and Evan (M1).

Note: The pooling/ecological fallacy concern is raised explicitly as Major by Alex, Charlie, and Evan; Doug raises it within the context of Issue 4 (model misspecification) rather than as a standalone finding. Counting only issues where all four reviewers independently flagged it as Major:

Confirmed universal AI-only Major flags (all four reviewers): 3
1. Incommensurable log-likelihood comparison (ARIMA differenced vs. POMP levels)
2. No profile likelihood or confidence intervals for any parameter
3. Global search far worse than local search / global MLE unreliable

Count: 3 universal AI-only Major flags.
