# Ned-Clean Analysis — W25 Project 11

## Human Issues

1. Are the GARCH quantities called "likelihood" actually likelihoods, or just something similar?
2. The claim that sGARCH-norm achieves the lowest AIC despite having the lowest log-likelihood is stated incorrectly (30 units of log-likelihood would require ~30 additional parameters to not change AIC).
3. The t-distribution insights from GARCH models should be incorporated into the mechanistic (POMP) stochastic volatility model.
4. The conclusion that "ARMA modeling is crucial for capturing autocorrelation structures in financial time series" is not clearly supported — essentially no autocorrelation is found, yet the analysis moves to GARCH which assumes zero autocorrelation.
5. Most of this project is routine and could have been a midterm project; the stochastic volatility part is not well-developed — an existing model is used and weaknesses are not fixed.
6. Poor convergence in the local search is acknowledged but the authors still use only 1000 particles and 50 iterations; more particles and iterations should be tried.
7. Fig 3.1 caption reads "density of gold prices" (wrong label); also, a histogram of marginal values of a time series is usually not a good idea, especially when there is a trend.
8. The sample ACF of index prices is uninformative because the series is non-stationary (close to a random walk), not stationary as ACF assumes.
9. The reason given for choosing ARMA(1,1) is parsimony, but ARMA(1,0) and ARMA(0,1) have better AIC and more parsimony.
10. Quite a long time is spent on ARMA analysis given that it is discarded in favor of better models.
11. The raw close price was used instead of the adjusted close price; a stock split occurred on August 28, 2020, so the raw price does not accurately reflect market fluctuations, and the reported "major shift in 2020" is likely an artifact of the split.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Profile likelihood at insufficient resolution and too few particles")
- Human Issue #7: covered (matched by finding: "Density plot title hardcodes 'Gold Prices' for Apple data")
- Human Issue #8: covered (matched by finding: "No formal stationarity test for the log-return series")
- Human Issue #9: covered (matched by finding: "ARMA model selection logic does not match stated choice")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding #1 (implausible POMP parameters — sigma_eta and phi out of range): A — AI major, human missed
- Finding #2 (diagnostic mislabeled — eGARCH diagnostics presented as gjrGARCH): A — AI major, human missed
- Finding #3 (log-return computation applied to already log-transformed series): A — AI major, human missed
- Finding #4 (global search initialized from single local search chain): A — AI major, human missed
- Finding #5 (profile at insufficient resolution and too few particles): B — AI major, matches Human Issue #6
- Finding #6 (STL decomposition misapplied to stock price data): A — AI major, human missed
- Finding #7 (ARMA model selection logic does not match stated choice): B — AI major, matches Human Issue #9
- Finding #8 (density plot title "Gold Prices"): D — AI minor, matches Human Issue #7
- Finding #9 (GARCH vs POMP log-likelihood not on comparable bases): C — AI minor, human missed
- Finding #10 (pairs plot threshold too wide at 100 LL units): C — AI minor, human missed
- Finding #11 (no formal stationarity test for log-return series): D — AI minor, matches Human Issue #8
- Finding #12 (profile only for phi, other parameters ignored): C — AI minor, human missed
- Finding #13 (duplicate library imports): C — AI minor, human missed
- Finding #14 (acknowledgments section potentially blind-breaking): C — AI minor, human missed
- Finding #15 (section heading typo "Explorable Data Analysis"): C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Model selection rationale for GARCH internally inconsistent")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Insufficient computational effort for local and global POMP searches")
- Human Issue #7: covered (matched by finding: "Density plot title mislabeled")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major #1 (global search box excludes MLE region for mu_h): A — AI major, human missed
- Major #2 (global search initialized from previous mif2 result): A — AI major, human missed
- Major #3 (GARCH and POMP log-likelihoods not directly comparable): A — AI major, human missed
- Major #4 (diagnostics figure computed from wrong model — eGARCH not GJR-GARCH): A — AI major, human missed
- Major #5 (insufficient computational effort for local and global POMP searches): B — AI major, matches Human Issue #6
- Major #6 (profile likelihood range likely excludes global MLE for phi): A — AI major, human missed
- Major #7 (GARCH model selection rationale internally inconsistent): B — AI major, matches Human Issue #2
- Minor: figure numbering error: C — AI minor, human missed
- Minor: STL decomposition on non-stationary price level: C — AI minor, human missed
- Minor: density plot title mislabeled ("Gold Prices"): D — AI minor, matches Human Issue #7
- Minor: apple_params.csv polluted with earlier runs: C — AI minor, human missed
- Minor: profile uses %dofuture% while parallel backend is doParallel: C — AI minor, human missed
- Minor: no simulation-based model validation for POMP model: C — AI minor, human missed
- Minor: log-likelihood scale not discussed (40-unit difference between models): C — AI minor, human missed
- Minor: no acknowledgment that LL only comparable within same model class: C — AI minor, human missed
- Minor: redundant library calls: C — AI minor, human missed
- Minor: "Acknowledgments" misspelled as "Ackonwledgments": C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Log-likelihood comparison between GJR-GARCH and POMP not like-for-like — distributional mismatch; suggests adding t-distribution to POMP")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Computational settings run_level=2 with Nmif=50, Np=1000 is borderline")
- Human Issue #7: covered (matched by finding: "Density plot title mislabeled as 'Density Plot of Gold Prices'")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major #1 (global IF2 search initialized from previous mif2 result): A — AI major, human missed
- Major #2 (global search box excludes MLE region for mu_h): A — AI major, human missed
- Major #3 (profile likelihood Monte Carlo variance dominates the CI): A — AI major, human missed
- Major #4 (profile max exceeds global search max by 16 LL units — confirms global search failure): A — AI major, human missed
- Major #5 (simulated-data pfilter presented as real-data benchmark): A — AI major, human missed
- Major #6 (GARCH vs POMP log-likelihood not like-for-like due to distributional mismatch): B — AI major, matches Human Issue #3
- Major #7 (no non-mechanistic benchmark under same observation model): A — AI major, human missed
- Minor #8 (profile plot filtered by round(H_0, 2) rather than phi): C — AI minor, human missed
- Minor #9 (apple_params.csv contains stale entries from multiple runs): C — AI minor, human missed
- Minor #10 (computational settings run_level=2 is borderline): D — AI minor, matches Human Issue #6
- Minor #11 (inconsistency between stated best phi and parameter table): C — AI minor, human missed
- Minor #12 (missing profile likelihood for additional parameters): C — AI minor, human missed
- Minor #13 (notation inconsistency: psi in text vs theta in ARMA equation): C — AI minor, human missed
- Minor #14 (density plot title mislabeled): D — AI minor, matches Human Issue #7
- Minor #15 (missing sessionInfo() and no package version pinning): C — AI minor, human missed

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
- Human Issue #9: covered (matched by finding: "ARMA model selection contradicts AIC evidence — ARMA(1,1) chosen despite ARMA(3,4) having much lower AIC")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- ID 25.11.2 (ARMA model selection contradicts AIC evidence): B — AI major, matches Human Issue #9
- ID 25.11.3 (profile likelihood over phi too sparse to support reported CI): A — AI major, human missed
- ID 25.11.4 (sigma_eta near-non-identifiability not diagnosed): A — AI major, human missed
- ID M1 (mu_h shows extreme variability across runs — poorly identified): A — AI major, human missed
- ID 25.11.1 (cross-family LL comparison should note initialization assumptions): C — AI minor, human missed
- ID 25.11.6 (date anomaly in GARCH residual output — dates show 1970-1973): C — AI minor, human missed
- ID 25.11.11 (profile CI cutoff not stated): C — AI minor, human missed
- ID 25.11.13 (no forward simulation from fitted POMP model): C — AI minor, human missed
- ID M2 (no RNG seeds set): C — AI minor, human missed
- ID M3 (MC variability context for log-likelihood differences not discussed): C — AI minor, human missed

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
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 5 | 6 | 3 |
| B (AI major, human also found) | 2 | 2 | 1 | 1 |
| C (AI minor, human missed) | 6 | 8 | 6 | 6 |
| D (AI minor, human also found) | 2 | 1 | 2 | 0 |
| E (Human found, AI missed) | 7 | 8 | 8 | 10 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall (B+D)/(B+D+E) | AI-Unique Rate (A+C)/(A+B+C+D) |
|----------|---------------------------:|--------------------------------:|
| Alex | 4/11 = 0.364 | 11/15 = 0.733 |
| Charlie | 3/11 = 0.273 | 13/16 = 0.813 |
| Doug | 3/11 = 0.273 | 12/15 = 0.800 |
| Evan | 1/11 = 0.091 | 9/10 = 0.900 |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (E for all four reviewers):

- Human Issue #1: Are the GARCH quantities called "likelihood" actually likelihoods?
- Human Issue #4: The conclusion that "ARMA modeling is crucial for capturing autocorrelation" is not supported given essentially no autocorrelation is found.
- Human Issue #5: The project is routine (could have been a midterm project); the SV part is not well-developed.
- Human Issue #10: Quite a long time is spent on ARMA analysis given that it is discarded.
- Human Issue #11: Raw close price used instead of adjusted close price; stock split on August 28, 2020 distorts the data.

**Count: 5 out of 11 human issues were missed by all reviewers.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2 (AIC claim is mathematically incorrect): covered by Charlie only.
- Human Issue #3 (t-distribution should be incorporated into POMP): covered by Doug only.
- Human Issue #8 (ACF of price series uninformative — series non-stationary): covered by Alex only.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 1 |
| Doug | 1 |
| Evan | 0 |

### Universal AI-only flags

No finding was raised by all four reviewers while being missed by the human reviewer.
