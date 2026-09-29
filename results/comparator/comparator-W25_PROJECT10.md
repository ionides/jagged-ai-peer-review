# Comparator Analysis — W25 Project 10

---

## Human Issues

1. The mechanistic model falls quite a long way short of the non-mechanistic benchmarks (ARMA and plain regression), indicating problems with the model. More diagnostic plots are needed to explore why the proposed dynamic model structure is not fitting well, for example looking at the likelihood anomalies as in Chapter 18 (the measles case study).

2. The decreasing log-likelihood with iteration is an indication of model misspecification. The proposed solution to use more particles or reduce random walk step size will not help — the problem is exactly that as the random walk step size reduces, the model no longer fits so well.

3. The report does not place the project securely into the context of other 531 projects or a broader literature. The topic is original, but the report should say this, and the team should say what they learned from previous projects, as requested in the assignment description.

4. When AIC suggests a very large ARIMA such as (5,1,6), the data are sometimes indicating a need to think of alternative model specifications — for example, fitting a trend.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "POMP log-likelihood is worse than both benchmarks, yet no model revision is attempted")
- Human Issue #2: contradiction (AI says the decreasing log-likelihood traces indicate non-convergence fixable by tuning; human says it indicates model misspecification and that more particles or smaller rw.sd will not help)
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ARIMA model is selected on the differenced series but POMP is applied to the undifferenced series — incompatible treatment of non-stationarity/trend")

**Findings classification:**
- Finding 1 (POMP worse than benchmarks, no revision attempted): B — POMP log-likelihood is worse than both benchmarks (matches Human Issue #1)
- Finding 2 (global search far worse than local search): A — global search produces a result ~4,700 log-likelihood units below local search with no adequate diagnosis
- Finding 3 (local search MIF2 traces show persistent non-convergence): F — Alex attributes the decreasing log-likelihood to non-convergence and implies tuning (reduce rw.sd, increase Np, more iterations) would fix it; human says it indicates model misspecification and those fixes will not help (contradicts Human Issue #2)
- Finding 4 (likelihood comparison not on the same basis — differenced vs undifferenced): A — ARIMA log-likelihood is on the differenced series, POMP/OLS on undifferenced; direct AIC comparison invalid
- Finding 5 (pooling individual data destroys panel structure): A — between-subject heterogeneity and changing enrollment artifact not addressed
- Finding 6 (X_0 fixed in global search but free in local search): A — asymmetry in parameter space searched is unexplained
- Finding 7 (no profile likelihood or confidence intervals): A — key noise coefficient b has no uncertainty quantification
- Finding 8 (ARIMA on differenced, POMP on undifferenced — incompatible non-stationarity treatment): B — stable AR(1) POMP will not capture a unit root or slow drift (matches Human Issue #4)
- Finding 9 (Np = 2,000 in global search vs 5,000 in local search): C — reduced particle count makes global surface uninformative; sensitivity not reported
- Finding 10 (AIC table computed on differenced series with d hard-coded as 0): C — ARMA(p,q) on differenced series labeled as ARIMA(5,1,6) without clear statement
- Finding 11 (OLS log-likelihood back-computed from AIC rather than extracted directly): C — correct formula but unnecessarily indirect and risks off-by-one in k
- Finding 12 (no simulation-based predictive check from estimated parameters): C — only initial-guess simulations shown; no fitted-parameter envelope plot
- Finding 13 (data in proprietary VDI; results not externally reproducible): C — submitted PDF contains screenshots; no independent replication possible
- Finding 14 (long-run equilibrium effect of noise not computed or discussed): C — policy-relevant implied effect (~-3.75 ms per 10 dB) never derived
- Finding 15 (uniform rw.sd = 0.01 across all parameters regardless of scale): C — parameters on very different scales need different perturbation sizes

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by findings: "POMP fits substantially worse than the linear regression benchmark, yet no structural revision is attempted" and "no simulation-based post-fit diagnostics shown")
- Human Issue #2: contradiction (Charlie says declining loglik is convergence failure and proposes reducing rw.sd as the fix; human says it indicates model misspecification and reducing rw.sd will not help)
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "differencing decision made by visual inspection with no consideration of whether trend is deterministic vs. stochastic")

**Findings classification:**
- Major 1 (convergence failure — loglik declines after iteration ~10): F — contradicts Human Issue #2 (human says declining loglik signals model misspecification and proposed solutions won't help; Charlie calls it convergence failure and recommends reducing rw.sd as the fix)
- Major 2 (ARIMA on differenced series, POMP on original — likelihoods non-comparable): A — not raised by any human issue
- Major 3 (POMP worse than linear regression, no structural revision attempted): B — matches Human Issue #1
- Major 4 (no profile likelihoods, no confidence intervals): A — not raised by any human issue
- Major 5 (LG-POMP admits exact Kalman filter; particle filter introduces avoidable MC noise): A — not raised by any human issue
- Major 6 (global search −7936 far below local search −3235): A — not raised by any human issue
- Major 7 (AR coefficient a fails to converge in local search): A — not raised by any human issue
- Major 8 (data and analysis inaccessible; screenshots only): A — not raised by any human issue
- Minor: differencing decided by visual inspection; no consideration of deterministic trend: D — matches Human Issue #4
- Minor: no simulation-based post-fit diagnostics: D — matches Human Issue #1
- Minor: Gaussian measurement model for SDNN (strictly positive) with no justification: C — not raised by any human issue
- Minor: loglik computation for linear regression non-transparent: C — not raised by any human issue
- Minor: rw.sd already small; author proposes reducing further but step sizes already small: C — not raised by any human issue
- Minor: global scatter plot range (−11,000 to −8,000) provides additional evidence global search uninformative: C — not raised by any human issue
- Minor: sigma_obs conflates between-person heterogeneity with within-day measurement noise: C — not raised by any human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by findings: "Process-Noise vs. Measurement-Noise Trade-off Indicates Potential Model Misspecification" and "No Benchmark Comparison on a Common Scale")
- Human Issue #2: covered (matched by finding: "Process-Noise vs. Measurement-Noise Trade-off Indicates Potential Model Misspecification"; note: "Computational Adequacy — Local Search Convergence is Incomplete" contradicts the human's diagnosis)
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "AIC Grid Search Uses Differenced Data Without Justification for Differencing")

**Findings classification:**
- Finding 1 (Global Search Dramatically Underperforms Local Search): A — global MLE unreliable due to box misalignment and insufficient compute; no human issue raises this
- Finding 2 (Invalid Log-Likelihood Comparison Between ARIMA and POMP): A — ARIMA LL evaluated on differenced series is incomparable to POMP LL on level series; no human issue raises this specific invalidity claim
- Finding 3 (No Profile Likelihoods — Parameter Identifiability Unassessed): A — absence of profile likelihoods and MCAP CIs; no human issue raises this
- Finding 4 (Process-Noise vs. Measurement-Noise Trade-off Indicates Potential Model Misspecification): B — sigma_proc collapses toward zero, model may be equivalent to linear regression, recognized sign of model misspecification (matches Human Issues #1 and #2)
- Finding 5 (Computational Adequacy — Local Search Convergence is Incomplete): F — attributes decreasing log-likelihood to over-diffuse rw.sd and treats calibrating rw.sd as the fix; contradicts Human Issue #2, which says the decreasing log-likelihood is model misspecification and that reducing rw.sd will not help
- Finding 6 (No Benchmark Comparison on a Common Scale): B — both ARIMA and regression comparisons are methodologically invalid, leaving no valid benchmark; matches Human Issue #1's concern that the mechanistic model cannot be adequately benchmarked
- Finding 7 (Reproducibility Severely Compromised): A — data under Apple NDA, analysis behind VDI firewall, only screenshots available; no human issue raises this
- Finding 8 (AIC Grid Search Uses Differenced Data Without Justification for Differencing): D — no formal stationarity test supports the differencing decision; trend-stationarity vs. difference-stationarity distinction unaddressed (matches Human Issue #4)
- Finding 9 (ARIMA Notation Confusion — ARMA(5,6) vs. ARIMA(5,1,6)): C — representation ambiguity confuses whether d=1 is applied once or twice; no human issue raises this
- Finding 10 (Simulation from Initial Guess Shows No Trend): C — simulated trajectories lack the systematic downward trend visible in the data; no human issue raises this
- Finding 11 (Pairs Plot Based on Invalid Global Search Results): C — Figure 5 parameter estimates are far from MLE, making identifiability inference unreliable; no human issue raises this
- Finding 12 (Conclusion's AIC Comparison Mixes Incompatible Models): C — AIC conclusion presumes log-likelihoods on a common scale when they are not; no human issue raises this
- Finding 13 (Linear Regression Benchmark Log-Likelihood Computed Incorrectly for Comparison): C — lm() LL is actually on the same scale as POMP measurement model but this valid comparison is not highlighted; no human issue raises this
- Finding 14 (Physical Activity Covariate Dropped Without Analysis): C — Energy coefficient c is diffuse and poorly identified but receives no interpretation; no human issue raises this
- Finding 15 (No Out-of-Sample or Forecast Evaluation): C — no held-out data evaluated for predictive accuracy; no human issue raises this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: C4 — differencing not justified by formal test; slow secular decline could be modeled with a trend rather than differencing)

**Findings classification:**
- C1: A — no profile likelihood or confidence interval for the noise coefficient b (Major)
- C2: A — benchmark comparison between incommensurable likelihoods (ARIMA on differenced series vs. POMP on level series) (Major)
- C3: A — global search discrepancy (-7936 displayed vs. -5244 claimed vs. -3235 local optimum) is unexplained and undermines the reported MLE (Major)
- M1: A — ecological fallacy risk from population-level pooling; causal inference not warranted (Major)
- C4: D — differencing not justified by formal unit-root test; deterministic trend may be more appropriate (matches Human Issue #4)
- C5: C — no ESS monitoring; near-zero sigma_proc suggests potential filter degeneracy (Minor)
- C6: C — no simulation-based model check at MLE; forward simulations use initial-guess parameters, not the fitted MLE (Minor)
- C7: C — X_0 treated asymmetrically between local and global searches without disclosure (Minor)
- C8: C — AIC table caption mislabeled as ARIMA(p,1,q) when models are ARMA(p,q) on already-differenced series (Minor)

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
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 6 | 4 | 4 |
| B (AI major, human also found) | 2 | 1 | 2 | 0 |
| C (AI minor, human missed) | 7 | 5 | 7 | 4 |
| D (AI minor, human also found) | 0 | 2 | 1 | 1 |
| E (Human found, AI missed) | 1 | 1 | 1 | 3 |
| F (Human-AI contradiction) | 1 | 1 | 1 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 0 | 1 | 2/3 = 67% | 5 | 7 | 12/14 = 86% |
| Charlie | 1 | 2 | 1 | 2/3 = 67% | 6 | 5 | 11/14 = 79% |
| Doug | 2 | 1 | 1 | 3/4 = 75% | 4 | 7 | 11/14 = 79% |
| Evan | 0 | 1 | 3 | 1/4 = 25% | 4 | 4 | 8/9 = 89% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: The report does not place the project securely into the context of other 531 projects or a broader literature. The topic is original, but the report should say this, and the team should say what they learned from previous projects, as requested in the assignment description. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 1 out of 4 human issues (25%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: The decreasing log-likelihood with iteration is an indication of model misspecification. The proposed solution to use more particles or reduce random walk step size will not help — the problem is exactly that as the random walk step size reduces, the model no longer fits so well. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |
