# Ned-Clean Analysis — W24 Project 07

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
9. A curious feature of the likelihood search for the POMP model is that a small fraction of searches find higher likelihood with phi around 0.9, whereas most searches find phi very close to 1. This could be noted and discussed, even if there was no time to resolve it.
10. The conclusions should be thoughtful about limitations as well as pointing out the positive results. For a course project, on a short timescale, there are bound to be weaknesses. Here, for example, the effective sample size is sometimes rather small. One solution would be to add long tails (t, not normal) to the stochastic volatility model, just as was done for GARCH.
11. References should have titles, authors and dates, in a standard format such as APA. There should also be more citations in the text.

---

## Alex

Note: Alex's review has a single "Weaknesses (Most Critical First)" section with no explicit Major/Minor split. All findings are treated as Major since no Minor section exists.

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Seasonal Decomposition Applied to Financial Returns Is Inappropriate")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH Model Selection Uses Minimum (Not Maximum) Log-Likelihood")
- Human Issue #7: covered (matched by finding: "GARCH Conclusion Is Inconsistent With the Diagnostic Plots")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Filter Diagnostics Show Severe Particle Depletion")
- Human Issue #11: missed

**Findings classification:**
- Alex #1 (Global search init anti-pattern): A — global search inherits state from local mif2 object; human missed
- Alex #2 (Particle filter benchmark uses simulated data): A — benchmark log-lik evaluated on simulated data, not real AAPL data; human missed
- Alex #3 (Log-likelihood values implausibly high): A — reported log-likelihoods of ~2650 not sanity-checked; human missed
- Alex #4 (Mismatch between benchmark log-lik and MIF2 results): A — 4000-unit discrepancy unexplained; human missed
- Alex #5 (ARMA grid excludes ARMA(0,0)): A — low-order models excluded from grid search; human missed
- Alex #6 (GARCH model selection uses minimum log-likelihood): B — inverted selection criterion matches Human Issue #6
- Alex #7 (Convergence diagnostics visually poor): A — sigma_nu and phi non-convergence not addressed; human missed
- Alex #8 (Filter diagnostics show ESS collapse): B — severe particle depletion matches Human Issue #10
- Alex #9 (POMP parameter transformation incomplete): A — mu_h, G_0, H_0 unconstrained; phi near boundary; human missed
- Alex #10 (sigma_eta anomalously large): A — sigma_eta 0–30 range not flagged; human missed
- Alex #11 (Seasonal decomposition inappropriate for financial returns): B — decompose() misapplied matches Human Issue #3
- Alex #12 (ACF lag axis misinterpreted): A — lag 0.07 misread; human missed
- Alex #13 (GARCH conclusion inconsistent with diagnostics): B — no formal likelihood comparison across models matches Human Issue #7
- Alex #14 (Local search saves wrong variable to CSV): A — local_results undefined; human missed
- Alex #15 (Excessive reliance on prior course material): A — no novel contribution; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 11 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

Note: Charlie has explicit "Major Issues" (7 items) and "Minor Issues" (bullet list). Two minor bullets duplicate major issues (decomposition, GARCH selection) and are excluded from counting.

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: Charlie Major #7 "Decomposition of Non-Seasonal Data Is Methodologically Inappropriate")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: Charlie Major #4 "Erroneous Model Selection in Basic GARCH Section")
- Human Issue #7: covered (matched by finding: Charlie Major #1 "No Unified Quantitative Comparison Across Model Families")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: Charlie Major #6 "POMP Model Uses Only Gaussian Measurement Noise Despite Heavy Tails")
- Human Issue #11: missed

**Findings classification:**
- Charlie Major #1 (No unified quantitative comparison): B — no log-lik/AIC table across ARMA, GARCH, POMP matches Human Issue #7
- Charlie Major #2 (IF2 non-convergence for key parameters): A — phi and sigma_eta non-convergence not remediated; human missed
- Charlie Major #3 (Absence of profile likelihoods): A — no profile likelihoods; identifiability unresolved; human missed
- Charlie Major #4 (Erroneous GARCH model selection): B — min instead of max log-likelihood matches Human Issue #6
- Charlie Major #5 (Global search box inconsistency for sigma_eta): A — search box [0.5,1] inconsistent with results [0,30]; human missed
- Charlie Major #6 (Gaussian measurement noise; no t-distribution): B — heavy tails not addressed in POMP model matches Human Issue #10
- Charlie Major #7 (Decomposition of non-seasonal data): B — decompose() on financial returns matches Human Issue #3
- Charlie Minor: Selective log-likelihood table: C — GARCH variants not in single table; human missed
- Charlie Minor: run_level=3 same Np as run_level=2: C — no high-effort configuration; human missed
- Charlie Minor: CatGPT citation for LaTeX: C — AI tool cited as reference; human missed
- Charlie Minor: Data non-reproducible at render time: C — live Yahoo Finance download; human missed
- Charlie Minor: Conclusion does not connect to quantitative results: C — "GARCH most effective" unsupported; human missed
- Charlie Minor: No sessionInfo(): C — package versions undocumented; human missed
- Charlie Minor: phi parameter transform inconsistency: C — phi scale in box vs. transform; human missed
- Charlie Minor: References 3 and 4 are course materials: C — non-peer-reviewed references for methods; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

Note: Doug has explicit "Major Issues" (10 items) and "Minor Issues" (bullet list).

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: Doug Minor "Decomposition applied to financial log-returns")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: Doug Minor "GARCH model selection criterion inconsistency")
- Human Issue #7: covered (matched by finding: Doug Major #3 "No benchmark comparison against a non-mechanistic model")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: Doug Minor "Conclusion does not connect to quantitative results")
- Human Issue #11: missed

**Findings classification:**
- Doug Major #1 (Global search initialized from previous mif2 result): A — anti-pattern; human missed
- Doug Major #2 (Irreconcilable log-likelihood discrepancy): A — benchmark vs MIF2 values ~4000 units apart; human missed
- Doug Major #3 (No benchmark comparison): B — no common log-lik across model families matches Human Issue #7
- Doug Major #4 (No profile likelihoods): A — parameter identifiability unaddressed; human missed
- Doug Major #5 (Computational adequacy insufficient): A — Np=1000 and Nmif=100 too low; human missed
- Doug Major #6 (Measurement model not described in text): A — Gaussian assumption implicit; human missed
- Doug Major #7 (Local search variable naming error): A — local_results undefined; human missed
- Doug Major #8 (No model diagnostics discussed): A — ESS collapses not connected to market events; human missed
- Doug Major #9 (Global search box poorly specified): A — mu_h and sigma_eta box too narrow; human missed
- Doug Major #10 (Initial conditions not estimated or assessed): A — H_0=G_0=0 sensitivity not tested; human missed
- Doug Minor: Decomposition inappropriate: D — decompose() on financial log-returns matches Human Issue #3
- Doug Minor: GARCH selection criterion inconsistency: D — min log-likelihood instead of max matches Human Issue #6
- Doug Minor: Selective log-likelihood table: C — GARCH variants not in single table; human missed
- Doug Minor: run_level=3 same Np as run_level=2: C — no high-effort particle count; human missed
- Doug Minor: CatGPT citation for LaTeX: C — AI tool cited as reference; human missed
- Doug Minor: Data non-reproducible at render time: C — live Yahoo Finance download; human missed
- Doug Minor: Conclusion does not connect to quantitative results: D — "GARCH most effective" unsupported matches Human Issue #10
- Doug Minor: No sessionInfo(): C — package versions undocumented; human missed
- Doug Minor: phi parameter transform inconsistency: C — phi scale in box vs. transform; human missed
- Doug Minor: References 3 and 4 are course materials: C — non-peer-reviewed references; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: Evan M1 "GARCH model selection inverted")
- Human Issue #7: covered (matched by finding: Evan M2 "Central conclusion unsupported by quantitative comparison")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: Evan new2 "ESS not monitored during particle filtering")
- Human Issue #11: missed

**Findings classification:**
- Evan M1 (GARCH model selection inverted — min not max): B — inverted selection criterion matches Human Issue #6
- Evan M2 (Conclusion unsupported by quantitative comparison): B — no log-lik table across model classes matches Human Issue #7
- Evan M3 (No profile likelihood; identifiability unquantified): A — profile likelihoods absent; human missed
- Evan M5 (run_level=3 only 1000 particles; convergence incomplete): A — same Np at run levels 2 and 3; human missed
- Evan M4r (No explicit log-likelihood comparison table): C — closely related to M2 but HI #7 already matched; human missed as standalone
- Evan M6 (Initial conditions G_0=H_0=0 not justified): C — sensitivity analysis absent; human missed
- Evan m1 (Ljung-Box misused as model selection criterion): C — diagnostic used as selection tool; human missed
- Evan new1 (Live Yahoo Finance download creates reproducibility risk): C — data not archived; human missed
- Evan new2 (ESS not monitored during particle filtering): D — particle degeneracy concerns matches Human Issue #10
- Evan m2 (ACF "Lag 0.07" notation confuses fractional and integer lags): C — ACF axis scaling misread; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 11 | 3 | 9 | 2 |
| B (AI major, human also found) | 4 | 4 | 1 | 2 |
| C (AI minor, human missed) | 0 | 8 | 7 | 5 |
| D (AI minor, human also found) | 0 | 0 | 3 | 1 |
| E (Human found, AI missed) | 7 | 7 | 7 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (4+0) / (4+0+7) = 4/11 = 36.4%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (11+0) / (11+4+0+0) = 11/15 = 73.3%

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (4+0) / (4+0+7) = 4/11 = 36.4%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+8) / (3+4+8+0) = 11/15 = 73.3%

**Doug**
- Human Recall = (B+D) / (B+D+E) = (1+3) / (1+3+7) = 4/11 = 36.4%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (9+7) / (9+1+7+3) = 16/20 = 80.0%

**Evan**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+8) = 3/11 = 27.3%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (2+5) / (2+2+5+1) = 7/10 = 70.0%

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer (all four: Alex, Charlie, Doug, Evan):

1. Human Issue #1: No references in introduction; weak motivation for fitting a model.
2. Human Issue #2: Report written like a preliminary investigation; unformatted R output; insufficient text.
4. Human Issue #4: ADF test not designed for time-varying sample variance.
5. Human Issue #5: ARMA modeling is a poor choice for financial markets; too much project effort devoted to it.
8. Human Issue #8: The asymmetric GARCH (AGARCH) is not defined.
9. Human Issue #9: Bimodal phi behavior in likelihood search (small fraction finding phi~0.9 vs majority near 1) not noted or discussed.
11. Human Issue #11: References lack titles, authors, and dates in standard format; insufficient in-text citations.

**Count: 7 out of 11 human issues were missed by all four reviewers.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- HI 3 (decomposition/seasonality): Covered by Alex, Charlie, and Doug — not unique to any one.
- HI 6 (GARCH AIC values): Covered by Alex, Charlie, Doug, and Evan — not unique.
- HI 7 (compare log-lik/AIC across models): Covered by Alex, Charlie, Doug, and Evan — not unique.
- HI 10 (conclusions/ESS/t-distribution): Covered by Alex, Charlie, Doug, and Evan — not unique.

No reviewer has a unique find (a human issue covered only by that reviewer).

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as AI-only (human missed) by every reviewer: None. No single AI-only finding was raised by all four reviewers simultaneously.

The closest common AI-only finding across three of the four reviewers is "no profile likelihoods" (Charlie A, Doug A, Evan A; Alex does not raise this explicitly), and "global search initialization problems" (Alex A, Doug A; Charlie and Evan address related but distinct global-search concerns).
