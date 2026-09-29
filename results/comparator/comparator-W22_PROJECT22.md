# Comparator Analysis — W22 Project 22

---

## Human Issues

1. It would be interesting to see if a longer-tailed distribution for epsilon_n, such as t, fits better.

2. The global search suggests a bimodality: a collection of searches seem to reach a different and inferior region of parameter space. This is not scientifically critical - the second mode has much lower likelihood - but may help to understand numerical issues.

---

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

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Finding 1 (No Non-Mechanistic Benchmark): A — no IID or ARMA benchmark comparison provided
- Finding 2 (AIC Comparison GARCH vs. POMP Invalid): A — likelihoods from different models on different scales compared without qualification
- Finding 3 (No Profile Likelihoods): A — no profile likelihoods or confidence intervals for any POMP parameter
- Finding 4 (Inadequate Convergence Evaluation): A — parameters described as "still fluctuating" with no formal convergence resolution
- Finding 5 (Global Search Box Inconsistency): A — stated search box for Force Negative model differs from implemented code
- Finding 6 (Misinterpretation of sigma_nu Boundary): A — convergence to zero boundary treated as scientific confirmation rather than identifiability signal
- Finding 7 (run_level = 2 Throughout): C — final results run at preliminary-grade computational effort
- Finding 8 (Nreps_global = 20 Too Small): C — 20 global search replicates insufficient given convergence instability
- Finding 9 (Visual-Only Simulation Fit): C — model fit assessed only by visual overlay, no quantitative diagnostics
- Finding 10 (Train/Test Split Never Used): C — test set defined but never used for any evaluation
- Finding 11 (Dmeasure/Rproc Inconsistency): C — covariate-injection pattern not explained or verified
- Finding 12 (Simplified Model Not Formally Tested): C — no likelihood ratio test or explicit AIC table comparing nested models
- Finding 13 (Pairs Plot Threshold Inconsistency): C — local vs. global search pairs plots use different logLik cutoffs without explanation
- Finding 14 (GARCH tseries Non-Standard Likelihood): C — non-standard logLik convention of tseries not verified against POMP scale
- Finding 15 (No Consolidated Summary Table): C — log-likelihoods and AIC values scattered rather than collected in one comparison table

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
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Finding 1 (Global search anchored to prior IF2 result): A — global search initialization coding error invalidates global optimum claim
- Finding 2 (Self-diagnosed non-convergence): A — authors acknowledge convergence failures yet present results as final
- Finding 3 (No profile likelihoods): A — parameter identifiability not assessed
- Finding 4 (No benchmark comparison): A — no ARMA-family baseline comparison performed
- Finding 5 (Invalid AIC comparison GARCH vs POMP): A — cross-model log-likelihood comparison is invalid
- Finding 6 (AIC uses summary log-likelihood, not maximum): A — AIC computations conflate median/summary loglik with maximum
- Finding 7 (Model diagnostics absent): A — no ESS traces, no conditional log-likelihoods, no filtering diagnostics
- Finding 8 (Simplified model — forced simplification without LRT): A — leverage parameters dropped without formal likelihood ratio test
- Finding 9 (Simulations as visual evidence only): C — visual comparison insufficient as goodness-of-fit metric
- Finding 10 (Force-negative model ad hoc): C — fixed G = -0.05 is arbitrary and unjustified
- Finding 11 (Run level 2 marginal effort): C — Np = 1000, Nmif = 100 insufficient for final analysis
- Finding 12 (Parameter transformation for mu_h): C — mu_h not noted as estimated on natural scale
- Finding 13 (EDA lacks ACF/PACF of squared returns): C — standard volatility clustering diagnostics absent
- Finding 14 (Conclusion claims largest maximized log likelihood — unverified): C — rank ordering from non-converged chains is unreliable
- Finding 15 (References incomplete): C — self-citation and student project references lack transparency

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
- Human Issue #1: covered (matched by finding: "22.22.New2 — Normal measurement model not discussed in light of observed heavy tails; Student-t not considered")
- Human Issue #2: missed

**Findings classification:**
- 22.22.C1: A — No profile likelihoods or confidence intervals for any parameter
- 22.22.C2: A — No non-mechanistic benchmark comparison
- 22.22.C3: A — Convergence incomplete; key comparative claim within Monte Carlo noise
- 22.22.C4: C — AIC values not numerically reported for POMP models
- 22.22.C5: C — logLik SE not discussed relative to model comparison differences
- 22.22.C8: C — GARCH vs. POMP log-likelihood comparison not explicitly verified
- 22.22.C7: C — Train/test split defined but never used
- 22.22.New1: C — Conditional log-likelihood diagnostic not computed
- 22.22.New2: D — Normal measurement model not discussed in light of observed heavy tails; Student-t not considered (matches Human Issue #1)
- 22.22.C10: C — Force-negative model has arbitrary fixed G_0 = -0.05 without justification

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
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 7 | 6 | 8 | 3 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 8 | 9 | 7 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 2 | 2 | 2 | 1 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 0 | 2 | 0/2 = 0% | 7 | 8 | 15/15 = 100% |
| Charlie | 0 | 0 | 2 | 0/2 = 0% | 6 | 9 | 15/15 = 100% |
| Doug | 0 | 0 | 2 | 0/2 = 0% | 8 | 7 | 15/15 = 100% |
| Evan | 0 | 1 | 1 | 1/2 = 50% | 3 | 6 | 9/10 = 90% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: The global search suggests a bimodality: a collection of searches seem to reach a different and inferior region of parameter space. This is not scientifically critical - the second mode has much lower likelihood - but may help to understand numerical issues. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 1 out of 2 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: It would be interesting to see if a longer-tailed distribution for epsilon_n, such as t, fits better. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
