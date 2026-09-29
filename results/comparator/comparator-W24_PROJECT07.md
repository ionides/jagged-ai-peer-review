# Comparator Analysis — W24 Project 07

---

## Human Issues

1. The introduction has no references, and only weak motivation. It would be good to clarify the practical goal of fitting a model, and to relate the data analysis to that goal.

2. The report is written like a preliminary investigation, including irrelevant unformatted R output and not much text.

3. The time series decomposition is not well explained. What does "seasonality" mean here?

4. ADF test is not designed for situations with time-varying sample variance, since neither the model used as a null hypothesis, nor the alternative model used to motivate the test statistic, have that feature.

5. ARMA modeling is known to be a poor choice for financial markets, so it is not worth dedicating a substantial fraction of the project effort to it.

6. The GARCH AIC values are clearly measuring something different from the standard definition of AIC used for the ARMA AIC table. So, what are the numbers being presented?

7. A natural way to combine the different analysis sections would be to compare log-likelihood or AIC for the different models under consideration. That would involve resolving the problem of what the code calculates for the number called AIC for GARCH.

8. The asymmetric GARCH (AGARCH) is not defined.

9. A curious feature of the likelihood search for the POMP model is that a small fraction of searches find higher likelihood with φ around 0.9, whereas most searches find φ very close to 1. This could be noted and discussed, even if there was no time to resolve it.

10. The conclusions should be thoughtful about limitations as well as pointing out the positive results. For a course project, on a short timescale, there are bound to be weaknesses. Here, for example, the effective sample size is sometimes rather small. One solution would be to add long tails (t, not normal) to the stochastic volatility model, just as was done for GARCH.

11. References should have titles, authors and dates, in a standard format such as APA. There should also be more citations in the text.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Seasonal Decomposition Applied to Financial Returns Is Inappropriate")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH Model Selection Uses Minimum (Not Maximum) Log-Likelihood")
- Human Issue #7: covered (matched by finding: "GARCH Conclusion Is Inconsistent With the Diagnostic Plots")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "POMP Model Parameter Transformation Is Incomplete")
- Human Issue #10: covered (matched by finding: "Filter Diagnostics Show Severe Particle Depletion")
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Global Search Starts From Single Local MIF2 Object): A — critical implementation bug; global search inherits a single local run instead of restarting fresh
- Finding 2 (Particle Filter Benchmark Uses Simulated Data): A — benchmark log-likelihood is computed on simulated, not real, data
- Finding 3 (Log-Likelihood Values Implausibly High): A — MIF2 log-likelihoods ~2650 are implausibly large and not sanity-checked
- Finding 4 (Mismatch Between Benchmark -1501 and MIF2 ~2650): A — >4000-unit discrepancy between benchmark and search results is unexplained
- Finding 5 (ARMA Grid Search Excludes Low-Order Models): A — grid starts at p,q=1 so ARMA(0,0)/AR(1)/MA(1) never evaluated
- Finding 6 (GARCH Model Selection Uses Minimum Log-Likelihood): B — selection criterion inverted (minimizing instead of maximizing log-likelihood), GARCH evaluation is incorrect (matches Human Issue #6)
- Finding 7 (Convergence Diagnostics Visually Poor and Insufficiently Discussed): A — sigma_nu does not converge; text claims global convergence contradicts visual
- Finding 8 (Filter Diagnostics Show Severe Particle Depletion): B — effective sample size collapses to near zero across many time points (matches Human Issue #10)
- Finding 9 (POMP Parameter Transformation Incomplete): B — phi near boundary (close to 1), near-unit-root behavior not flagged (matches Human Issue #9)
- Finding 10 (sigma_eta Anomalously Large in Local Search): A — sigma_eta ranges 0–30, physically implausible and uninvestigated
- Finding 11 (Seasonal Decomposition Inappropriate for Financial Returns): B — additive decomposition mis-specified for returns; adds no value (matches Human Issue #3)
- Finding 12 (ACF Lag Axis Misinterpreted): A — reported "lag 0.07" corresponds to ~18 days; authors do not recognize frequency scaling
- Finding 13 (GARCH Conclusion Inconsistent With Diagnostic Plots): B — no formal likelihood comparison between GARCH and POMP model is made (matches Human Issue #7)
- Finding 14 (Local Search Saves Wrong Variable to CSV): A — write.table references undefined variable local_results instead of r.if1
- Finding 15 (Excessive Reliance on Prior Course Material): A — POMP code borrowed from prior project with no novel contribution explained

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 5 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "decompose() applied to daily log returns without justification")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH model selection selects worst-fitting model — tseries reports non-standard likelihood values and min() used instead of max()")
- Human Issue #7: covered (matched by finding: "no quantitative comparison between ARMA, GARCH, and POMP model likelihoods")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "no simulation-based model validation — ESS occasionally drops to single digits")
- Human Issue #11: covered (matched by finding: "references given as bare URLs rather than bibliographic citations")

**Findings classification:**
- Major Issue 1 (initial pfilter benchmark on simulated data): A — pfilter computed on sim1.filt (simulated data) rather than real AAPL returns, making the stated baseline meaningless
- Major Issue 2 (factual discrepancy on replicates/particles): A — text claims 20 replicates with 2000 particles; code uses 10 and 1000
- Major Issue 3 (GARCH model selection selects worst-fitting model): B — tseries reports non-standard likelihood values; min() used instead of max(), likely selecting the worst GARCH specification (matches Human Issue #6)
- Major Issue 4 (no profile likelihoods or confidence intervals): A — no profile likelihoods computed for any POMP parameter; sigma_eta and sigma_nu ranges are wide with no confidence bounds
- Major Issue 5 (no quantitative cross-model comparison): B — no log-likelihood or AIC comparison across ARMA, GARCH, and POMP; stated conclusion unsupported (matches Human Issue #7)
- Major Issue 6 (convergence failure acknowledged but not addressed): A — local search shows sigma_eta and H_0 still drifting at iteration 100 with no structural revision or increased computation
- Major Issue 7 (sigma_nu and sigma_eta near zero, scientific interpretation absent): A — near-zero estimates suggesting leverage collapse not discussed or tested against a reduced model
- Minor: no simulation-based model validation: D — ESS drops to single digits around time 400 and 800; no simulated trajectory overlays computed (matches Human Issue #10)
- Minor: decompose() applied to daily log returns without justification: D — log returns have no physical seasonality at frequency 253; component is plotted but never discussed (matches Human Issue #3)
- Minor: run_level=3 set but uses run_level=2 parameter values: C — Np=1000 and Nmif=100 at run_level=3 match run_level=2 defaults, not run_level=3 standard (Np=5000, Nmif=200)
- Minor: ARIMA section title but ARMA model fitted: C — d=0 in the fitted model; section heading is inconsistent with the specification
- Minor: references given as bare URLs rather than bibliographic citations: D — references [1]–[4] and [6] lack author, title, and date (matches Human Issue #11)
- Minor: acknowledgment of AI tool for LaTeX writing: C — reference [2] cites "CatGPT" for LaTeX; appropriateness under course policy should be clarified
- Minor: ARMA grid search excludes p=0 or q=0: C — pure AR or pure MA models not considered; best AIC from restricted grid may be suboptimal
- Minor: AIC comparison within basic GARCH grid omitted: C — log-likelihoods compared without complexity penalty; AIC would be more appropriate for model selection within the GARCH family

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Decomposition applied to financial log-returns")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH model selection criterion inconsistency")
- Human Issue #7: covered (matched by finding: "No benchmark comparison against a non-mechanistic model"; also matched by finding: "Selective log-likelihood table")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "No profile likelihoods; parameter identifiability unaddressed")
- Human Issue #10: covered (matched by finding: "Computational adequacy is insufficient")
- Human Issue #11: missed

**Findings classification:**
- Major 1 (global search anti-pattern): A — global search initialized from previous mif2 result object invalidates global optimum claim
- Major 2 (log-likelihood discrepancy): A — particle filter benchmark of −1501 irreconcilable with IF2 results of ~2650/2655
- Major 3 (no benchmark comparison): B — no common log-likelihood or AIC reported across ARMA, GARCH, and POMP models (matches Human Issue #7)
- Major 4 (no profile likelihoods): B — no profile likelihoods computed; phi and sigma_nu identifiability unaddressed despite pair-plot evidence (matches Human Issue #9)
- Major 5 (computational adequacy): B — ESS collapses to near zero repeatedly with only Np=1000 particles, indicating particle degeneracy (matches Human Issue #10)
- Major 6 (measurement model not in text): A — dmeasure specifies Gaussian observation model but no probability distribution is written out in the manuscript
- Major 7 (variable naming error): A — write.table calls undefined variable local_results instead of r.if1, causing reproducibility gap
- Major 8 (no conditional log-likelihoods): A — per-time-step conditional log-likelihoods not discussed or used to diagnose model failures
- Major 9 (global search box too narrow): A — mu_h box c(−1,0) excludes the range −8 to 4 found by local search; sigma_eta box c(0.5,1) far too narrow
- Major 10 (initial conditions not assessed): A — G_0 and H_0 fixed without sensitivity analysis or justification
- Minor: Decomposition applied to financial log-returns: D — decompose() is meaningless for non-seasonal log-returns; "no seasonality" conclusion makes decomposition puzzling (matches Human Issue #3)
- Minor: GARCH model selection criterion inconsistency: D — basic GARCH grid search uses logLik.garch() and selects minimum (worst-fitting) model, inconsistent with AIC used elsewhere (matches Human Issue #6)
- Minor: Selective log-likelihood table: D — log-likelihood values for GARCH variants not collected into a single comparison table (matches Human Issue #7)
- Minor: run_level 3 same as level 2: C — run_level=3 does not increase particle count beyond Np=1000, providing no additional computational resources
- Minor: CatGPT citation: C — "CatGPT [2]" is not a valid academic citation for LaTeX equation writing
- Minor: Data non-reproducible at render time: C — live getSymbols() call means re-renders may produce different data without an archived snapshot
- Minor: Conclusion unsupported: C — concludes GARCH is best for forecasting but no formal forecasting comparison is presented
- Minor: No sessionInfo(): C — no session information or package version documentation provided
- Minor: phi transform note: C — global search box for phi is on original scale while logit transform is used internally; consistent but unexplained
- Minor: References 3 and 4 are course materials: C — two of six references are course notes and a student project, not peer-reviewed sources

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH model selection inverted — min instead of max log-likelihood")
- Human Issue #7: covered (matched by finding: "Central conclusion unsupported by explicit quantitative comparison"; also matched by finding: "No explicit comparison table of log-likelihoods across model classes")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "ESS not monitored during particle filtering")
- Human Issue #11: missed

**Findings classification:**
- 24.07.M1: B — GARCH model selection inverted (min instead of max log-likelihood) (matches Human Issue #6)
- 24.07.M2: B — Central conclusion ("GARCH most effective") unsupported by explicit quantitative comparison (matches Human Issue #7)
- 24.07.M3: A — No profile likelihood; parameter identifiability not quantified
- 24.07.M5: A — run_level=3 uses only 1000 particles (same as run_level=2); convergence incomplete
- 24.07.M4r: D — No explicit comparison table of log-likelihoods across model classes (matches Human Issue #7)
- 24.07.M6: C — Initial conditions G_0=H_0=0 not justified
- 24.07.m1: C — Ljung-Box used as model selection criterion rather than diagnostic
- 24.07.new1: C — Live Yahoo Finance download creates reproducibility risk
- 24.07.new2: D — ESS not monitored during particle filtering (matches Human Issue #10)
- 24.07.m2: C — ACF "Lag 0.07" notation confuses fractional and integer lags

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 10 | 5 | 7 | 2 |
| B (AI major, human also found) | 5 | 2 | 3 | 2 |
| C (AI minor, human missed) | 0 | 5 | 7 | 4 |
| D (AI minor, human also found) | 0 | 3 | 3 | 2 |
| E (Human found, AI missed) | 6 | 6 | 6 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 5 | 0 | 6 | 5/11 = 45% | 10 | 0 | 10/15 = 67% |
| Charlie | 2 | 3 | 6 | 5/11 = 45% | 5 | 5 | 10/15 = 67% |
| Doug | 3 | 3 | 6 | 5/11 = 45% | 7 | 7 | 14/20 = 70% |
| Evan | 2 | 2 | 8 | 3/11 = 27% | 2 | 4 | 6/10 = 60% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The introduction has no references, and only weak motivation. It would be good to clarify the practical goal of fitting a model, and to relate the data analysis to that goal. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: The report is written like a preliminary investigation, including irrelevant unformatted R output and not much text. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: ADF test is not designed for situations with time-varying sample variance, since neither the model used as a null hypothesis, nor the alternative model used to motivate the test statistic, have that feature. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: ARMA modeling is known to be a poor choice for financial markets, so it is not worth dedicating a substantial fraction of the project effort to it. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The asymmetric GARCH (AGARCH) is not defined. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 11 human issues (45%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #11: References should have titles, authors and dates, in a standard format such as APA. There should also be more citations in the text. (Covered only by Charlie)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |
