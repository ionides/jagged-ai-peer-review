# Comparator Analysis — W25 Project 11

---

## Human Issues

1. Are the GARCH quantities called "likelihood" actually likelihoods or just something similar? See Quiz 2, Q12-02.

2. "despite having the lowest log-likelihood, sGARCH-norm achieves the lowest AIC due to its simpler structure": this doesn't look right, because 30 units of log likelihood would require an additional 30 parameters if it is not to have a higher AIC.

3. The t distribution can be used for stochastic volatility models just as readily as for GARCH models. It is good for non-mechanistic and mechanistic models to challenge each other for new ideas. But, the insights from them can and should be included in the mechanistic models.

4. The conclusion, "ARMA modeling is crucial for capturing autocorrelation structures in financial time series" is not clearly supported. Essentially no autocorrelation is found, and then the analysis moves on to GARCH models which assume the autocorrelation is zero.

5. Most of this project could have been done as a midterm project. There are many past midterm and final projects doing similar things, so the analysis is quite routine. The stochastic volatility part is not well developed: an existing model is used, and weaknesses are not fixed.

6. Although the author acknowledges the poor convergence in the local search, they have decided to use 1000 particles with 50 iterations. Maybe it's worth trying more particles and more iterations (something like 5000 particles and 100 iterations). This way, they may be able to see if it's the problem with particle filtering or if there is model misspecification.

7. Fig 3.1 has a caption "density of gold prices". Also, a histogram of marginal values of a time series is usually not a good idea. When the time series has a trend, it is an especially poor choice.

8. The sample ACF of index prices is uninformative. This plot estimates autocorrelation for a stationary time series, but the time plot (and common knowledge of investments) suggests that it is close to a random walk, which is non-stationary.

9. The reason given for choosing ARMA(1,1) is parsimony, but (1,0) and (0,1) have better AIC and more parsimony.

10. Quite a long time is spent on ARMA considering that it gets discarded in favor of better models.

11. The team decided to use the close price rather than the adjusted close price. On August 28, 2020, a stock split occurred, which would cause the raw close price not accurately to reflect market fluctuations. The report's observation that "a major shift occurred in 2020, marked by a rapid surge in prices and increased volatility" is likely due to the use of the raw closing price as affected by the stock split.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Profile Likelihood Is Computed at Insufficient Resolution and With Too Few Particles")
- Human Issue #7: covered (matched by finding: "Density Plot Title Hardcodes 'Gold Prices' for Apple Data")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "ARMA Model Selection Logic Does Not Match Stated Choice")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (POMP Parameter Values Are Implausible): A — phi ~= 1 and anomalously large sigma_eta suggest boundary convergence, not addressed by human
- Finding 2 (Inconsistency Between Stated Model and Diagnostic Evaluation): A — diagnostics run on eGARCH but attributed to gjrGARCH, not addressed by human
- Finding 3 (Log-Return Computation Applied to Already Log-Transformed Series): A — "+1" offset artifact in POMP input series vs. ARMA/GARCH series, not addressed by human
- Finding 4 (Global Search Initialized Only From a Single Local Search Chain): A — mif2(if1[[1]],...) biases global search, not addressed by human
- Finding 5 (Profile Likelihood Computed at Insufficient Resolution and Too Few Particles): B — Np=100 in profile likelihood is insufficient for reliable CI (matches Human Issue #6)
- Finding 6 (STL Decomposition Is Misapplied to Stock Price Data): A — STL assumes stable seasonal period, invalid for financial prices, not addressed by human
- Finding 7 (ARMA Model Selection Logic Does Not Match Stated Choice): B — ARMA(1,1) choice poorly justified; code and text inconsistent on model selection (matches Human Issue #9)
- Finding 8 (Density Plot Title Hardcodes "Gold Prices" for Apple Data): D — copy-paste title error in Figure 3.1 (matches Human Issue #7)
- Finding 9 (Log-Likelihood Comparison Between GARCH and POMP Not on Comparable Bases): C — MC error in POMP estimate not reported; GARCH vs. POMP gap smaller than noise
- Finding 10 (Pairs Plot Threshold Is Too Wide — 100 log-likelihood units): C — conventional threshold is 20 units, not addressed by human
- Finding 11 (No Formal Stationarity Test for Log-Return Series): C — no ADF/KPSS test for log-returns, not addressed by human
- Finding 12 (Profile Likelihood Computed Only for phi): C — no profiles for sigma_eta, mu_h, sigma_nu, not addressed by human
- Finding 13 (Duplicate Library Imports): C — several libraries imported twice, minor code quality issue
- Finding 14 (Acknowledgments Contain Potentially Blind-Breaking Self-References): C — references "Project 11" from W24, not addressed by human
- Finding 15 (Section Heading Typo "Explorable Data Analysis"): C — typo for "Exploratory Data Analysis", not addressed by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by findings: "local search convergence not achieved: ~100 log-unit spread" and "Nmif=50 below run_level=2 standard of 100 iterations")
- Human Issue #7: covered (matched by finding: "density plot title says 'Gold Prices' instead of 'Apple Stock Prices'")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "ARMA model selection narrative inconsistent; AIC table not shown to verify ARMA(1,1) is parsimony-optimal")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (GARCH diagnostics on eGARCH, not gjrGARCH): A — diagnostics run on wrong model; invalidates entire diagnostic section for chosen model
- Finding 2 (Profile Np=100 vs Np=1000 in main analysis): A — profile likelihood evaluated with ten times fewer particles than main analysis
- Finding 3 (Profile CI upper bound truncated at search boundary): A — CI upper bound of 0.99 equals the grid maximum; true upper bound may exceed it
- Finding 4 (Log-likelihood comparison across different datasets): A — GARCH fitted to raw log-returns, POMP fitted to mean-centered log-returns; values not comparable
- Finding 5 (Local search convergence not achieved: ~100 log-unit spread): B — matches Human Issue #6
- Finding 6 (Profile too sparse: only 10 grid points): A — fewer than 5 points above Wilks cutoff; CI not credibly bounded
- Finding 7 (Duplicate "Figure 4.2" caption): C — same caption number used for two different figures
- Finding 8 (Density plot title says "Gold Prices"): D — matches Human Issue #7
- Finding 9 (Pairs plot threshold 100 log units): C — filter includes all runs; obscures parameter structure near optimum
- Finding 10 (Simulation code ignores simulated data): C — sapply never uses sim argument; misrepresents what was computed
- Finding 11 (Profile only for phi; other parameters not assessed): C — identifiability of mu_h, sigma_eta, sigma_nu not assessed
- Finding 12 (ARMA model selection narrative inconsistent): D — matches Human Issue #9
- Finding 13 (Nmif=50 below run_level=2 standard): D — matches Human Issue #6
- Finding 14 (No out-of-sample evaluation): C — no rolling-window or train/test split despite stated forecasting goal
- Finding 15 (ARMA notation inconsistency): C — psi in description, theta_j in equation; inconsistent throughout Section 4

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Log-likelihood comparison between GJR-GARCH and POMP is not like-for-like due to t vs. Gaussian distributional mismatch")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Computational settings run_level=2 with Nmif=50, Np=1000 is borderline; more particles and iterations needed")
- Human Issue #7: covered (matched by finding: "Density plot title mislabeled as 'Density Plot of Gold Prices'")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Global IF2 search initialized from previous mif2 object): A — incorrect initialization of global search from stale IF2 chain rather than base pomp object
- Finding 2 (Global search box excludes region containing MLE for mu_h): A — box set to mu_h in (-1,0) but MLE is at -8.58, outside the box
- Finding 3 (Profile likelihood Monte Carlo variance dominates CI): A — profile uses Np=100 so SE up to 9.3 units exceeds chi-squared threshold of 1.92 units
- Finding 4 (Profile maximum substantially exceeds global search maximum): A — 16.2-unit discrepancy between profile max and global search max confirms global search failure
- Finding 5 (Simulated-data particle filter result presented as real-data benchmark): A — pfilter run on simulated data, not real AAPL data, making the comparison invalid
- Finding 6 (Log-likelihood comparison between GJR-GARCH and POMP not like-for-like): B — GJR-GARCH uses t-distribution while POMP uses Gaussian; conflates model structure with distributional choice (matches Human Issue #3)
- Finding 7 (No non-mechanistic benchmark under same observation model): A — sGARCH-norm and POMP achieve nearly equal log-likelihoods but the implication is not discussed
- Finding 8 (Profile likelihood plot filtered by round(H_0, 2) rather than phi): C — grouping variable uses H_0 instead of the profiled parameter phi
- Finding 9 (apple_params.csv contains stale entries from multiple runs): C — CSV accumulates implausible logLik > 8000 values from earlier exploratory runs
- Finding 10 (Computational settings run_level=2 with Nmif=50, Np=1000 borderline): D — authors acknowledge poor convergence; run_level=3 (Nmif=100, Np=2000) needed (matches Human Issue #6)
- Finding 11 (Inconsistency between stated best phi and parameter table): C — global search gives phi ~0.9 but profile CI is (0.959, 0.99)
- Finding 12 (Missing profile likelihood for additional parameters): C — only phi is profiled; sigma_nu, sigma_eta, mu_h also need profiles
- Finding 13 (Notation inconsistency: psi in prose but theta in ARMA equation): C — MA parameters called psi in text but theta_j in displayed equation
- Finding 14 (Density plot title mislabeled as "Density Plot of Gold Prices"): D — ggplot code title not updated from template/different dataset (matches Human Issue #7)
- Finding 15 (Missing sessionInfo() and no package version pinning): C — no sessionInfo() output and no renv snapshot in supplement

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "ID 25.11.2 — ARMA model selection contradicts AIC evidence; ARMA(1,1) chosen citing parsimony despite AIC favoring other models")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- ID 25.11.2: B — ARMA model selection contradicts AIC evidence (matches Human Issue #9)
- ID 25.11.3: A — Profile likelihood over phi too sparse to support reported CI
- ID 25.11.4: A — sigma_eta near-non-identifiability not diagnosed
- ID M1: A — mu_h shows extreme variability across runs indicating poor identifiability
- ID 25.11.1: C — Cross-family log-likelihood comparison should note initialization assumptions
- ID 25.11.6: C — Date anomaly in GARCH residual output (dates show 1970–1973 instead of 2020–2025)
- ID 25.11.11: C — Profile CI cutoff criterion not stated
- ID 25.11.13: C — No forward simulation from fitted POMP model
- ID M2: C — No RNG seeds set for stochastic computations
- ID M3: C — MC variability context for log-likelihood differences not discussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 10 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 5 | 6 | 3 |
| B (AI major, human also found) | 2 | 1 | 1 | 1 |
| C (AI minor, human missed) | 7 | 6 | 6 | 6 |
| D (AI minor, human also found) | 1 | 3 | 2 | 0 |
| E (Human found, AI missed) | 8 | 8 | 8 | 10 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 8 | 3/11 = 27% | 5 | 7 | 12/15 = 80% |
| Charlie | 1 | 3 | 8 | 3/11 = 27% | 5 | 6 | 11/15 = 73% |
| Doug | 1 | 2 | 8 | 3/11 = 27% | 6 | 6 | 12/15 = 80% |
| Evan | 1 | 0 | 10 | 1/11 = 9% | 3 | 6 | 9/10 = 90% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Are the GARCH quantities called "likelihood" actually likelihoods or just something similar? See Quiz 2, Q12-02. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: "despite having the lowest log-likelihood, sGARCH-norm achieves the lowest AIC due to its simpler structure": this doesn't look right, because 30 units of log likelihood would require an additional 30 parameters if it is not to have a higher AIC. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The conclusion, "ARMA modeling is crucial for capturing autocorrelation structures in financial time series" is not clearly supported. Essentially no autocorrelation is found, and then the analysis moves on to GARCH models which assume the autocorrelation is zero. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: Most of this project could have been done as a midterm project. There are many past midterm and final projects doing similar things, so the analysis is quite routine. The stochastic volatility part is not well developed: an existing model is used, and weaknesses are not fixed. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The sample ACF of index prices is uninformative. This plot estimates autocorrelation for a stationary time series, but the time plot (and common knowledge of investments) suggests that it is close to a random walk, which is non-stationary. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: Quite a long time is spent on ARMA considering that it gets discarded in favor of better models. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: The team decided to use the close price rather than the adjusted close price. On August 28, 2020, a stock split occurred, which would cause the raw close price not accurately to reflect market fluctuations. The report's observation that "a major shift occurred in 2020, marked by a rapid surge in prices and increased volatility" is likely due to the use of the raw closing price as affected by the stock split. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 7 out of 11 human issues (64%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: The t distribution can be used for stochastic volatility models just as readily as for GARCH models. It is good for non-mechanistic and mechanistic models to challenge each other for new ideas. But, the insights from them can and should be included in the mechanistic models. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |
