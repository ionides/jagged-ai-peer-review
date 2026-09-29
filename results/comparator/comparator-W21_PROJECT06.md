# Comparator Analysis — W21 Project 06

---

## Human Issues

1. Motivation was somewhat unclear: explain the relationship between studying volatility and understanding the GameStop story.

2. All the models used are stationary, and the WallStreetBets intervention is perhaps temporary, so there might be room for improvement on these business-as-usual financial models. For example, perhaps volatility might increase with increasing stock price when there is a deliberate manipulation of the stock price, and this is the opposite of the usual pattern.

3. Make sure the text explains what is going on: usually, we only show code and computer output that is part of the story explained in the text.

4. In Conclusions: compare the maximized log likelihood, not the median log likelihood from a stochastic search.

5. If some parameters are weakly identified, that is not necessarily a problem for the model: it just means that those parts of the model are not so important.

6. The maximized likelihood may be more relevant than the median when doing multiple searches to numerically maximize the likelihood.

7. The assumptions and purposes of the different models could be discussed more, to put the maximized likelihoods and other results in context.

8. In the global search, the convergence points form two clusters, most clearly seen in log likelihood vs $\mu_h$.

9. Show returns with a mean, and don't also show demeaned returns which is visually almost identical.

10. Some sections are short on motivation: if you have a section on filtering simulated data, you should explain briefly why it is there, and what you learn from it.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "anomalous event (short squeeze) without special modeling treatment")
- Human Issue #3: covered (matched by finding: "simulation comparison plot text does not match code"; also matched by "pairs plots shown but not discussed meaningfully")
- Human Issue #4: missed
- Human Issue #5: contradiction (AI says non-convergence of H_0 and sigma_nu is a serious problem for inference; human says weakly identified parameters are not necessarily a problem)
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (near-verbatim replication of course slides): A — no human issue matches
- Finding 2 (global search box inconsistent with local search results): A — no human issue matches; human issue #8 identifies two clusters in global search (different specific claim)
- Finding 3 (AIC comparison across ARMA/GARCH/POMP invalid): A — no human issue matches
- Finding 4 (non-convergence largely ignored; declared success anyway): F — contradicts Human Issue #5 (human says weak identification is not necessarily a problem; AI says non-convergence of H_0 and sigma_nu is a serious problem)
- Finding 5 (particle filter LL as point estimate without Monte Carlo error): A — no human issue matches; human issues #4 and #6 concern max vs. median, a distinct specific claim
- Finding 6 (ARMA residual ACF not investigated): A — no human issue matches
- Finding 7 (GARCH(4,2) selected without justification): A — no human issue matches
- Finding 8 (simulation comparison plot text does not match code): D — matches Human Issue #3
- Finding 9 (covaryt covariate table setup fragile): C — no human issue matches
- Finding 10 (no likelihood ratio test between nested models): C — no human issue matches
- Finding 11 (pairs plots shown but not discussed meaningfully): D — matches Human Issue #3
- Finding 12 (ARMA(1,3) not the overall AIC minimum): C — no human issue matches
- Finding 13 (anomalous event without special modeling treatment): D — matches Human Issue #2
- Finding 14 (conclusion misstates log-likelihood values): C — no human issue matches
- Finding 15 (heavy reliance on past student projects not disclosed): C — no human issue matches

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "tanh(G) code not explained in text"; also matched by finding: "pairs plots shown but not interpreted")
- Human Issue #4: covered (matched by finding: "AIC for POMP uses median log-likelihood, not maximum")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "AIC for POMP uses median log-likelihood, not maximum")
- Human Issue #7: covered (matched by finding: "no non-mechanistic IID benchmark — ARMA addresses mean, not volatility")
- Human Issue #8: covered (matched by finding: "pairs plots shown but not interpreted — multi-modality in mu_h undiscussed")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "initial test simulation mismatch insufficiently explained")

**Findings classification:**
- Major 1 (Direct AIC comparison across ARMA/GARCH/POMP invalid): A — cross-model AIC normalization not verified
- Major 2 (Profile likelihoods entirely absent): A — no profiles computed for any POMP parameter
- Major 3 (Incomplete convergence acknowledged but not addressed): A — H_0 and sigma_nu non-convergence ignored before conclusions
- Major 4 (Global search starts from if1[[1]], not best replicate): A — arbitrary starting replicate inherited for all global runs
- Major 5 (Insufficient particle count Np=2,000 at run_level=3): A — below standard 5,000 for non-Gaussian series
- Major 6 (GARCH tseries::garch non-standard log-likelihood): A — normalization of tseries log-likelihood unverified
- Minor 7 (No non-mechanistic IID benchmark): D — identifies that ARMA serves the mean not volatility, matching Human Issue #7 (assumptions/purposes of models underdiscussed)
- Minor 8 (ARMA AIC table lacks convergence discussion): C — numerical stability of optimizer not checked
- Minor 9 (Simulation-based model diagnostics absent): C — no post-fitting simulated trajectory comparison
- Minor 10 (Initial test simulation mismatch insufficiently explained): D — matches Human Issue #10 (sections on simulated data need motivation and explanation of what is learned)
- Minor 11 (ARMA residual ACF inadequately explained — seasonality misattributed): C — explanation misleading but no human issue matches
- Minor 12 (Pairs plots shown but not interpreted — multi-modality undiscussed): D — matches Human Issues #8 (two clusters visible in log-likelihood vs mu_h) and #3 (output shown without narrative explanation)
- Minor 13 (AIC for POMP computed from median log-likelihood, not maximum): D — matches Human Issues #4 and #6 (use maximized likelihood, not median)
- Minor 14 (tanh(G) leverage code not explained in text): D — matches Human Issue #3 (only show code that is part of the story explained in the text)
- Minor 15 (ARMA(1,3) written equation missing epsilon_{n-3} term): C — typographical error, no human issue matches

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 5 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No Discussion of Model Limitations Regarding the Unprecedented Price Spike")
- Human Issue #3: covered (matched by finding: "Simulated-Data Particle Filter Presented Without Clear Benchmark Qualification")
- Human Issue #4: covered (matched by finding: "AIC Calculation for POMP Model Appears to Use Median Log-Likelihood")
- Human Issue #5: contradiction (Doug says non-convergence of H_0 and sigma_nu is a major problem requiring substantial remediation; human says weakly identified parameters are not necessarily a problem for the model)
- Human Issue #6: covered (matched by finding: "AIC Calculation for POMP Model Appears to Use Median Log-Likelihood")
- Human Issue #7: covered (matched by finding: "Invalid Cross-Model Log-Likelihood Comparison")
- Human Issue #8: covered (matched by finding: "Global Search Box for mu_h Is Inconsistently Narrow")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Simulated-Data Particle Filter Presented Without Clear Benchmark Qualification")

**Findings classification:**
- Finding 1 (Simulated-Data Particle Filter Presented Without Clear Benchmark Qualification): B — Major; simulated-data filter section is not clearly explained or motivated (matches Human Issues #3 and #10)
- Finding 2 (Global IF2 Search Initialized from Previous mif2 Result): A — Major; global search uses if1[[1]] as base object, inheriting a near-exhausted cooling schedule that invalidates the global coverage claim
- Finding 3 (No Benchmark Comparison Against a Non-Mechanistic Model): A — Major; no volatility benchmark fitted on the same data and observation model to contextualize the POMP log-likelihood
- Finding 4 (Invalid Cross-Model Log-Likelihood Comparison): B — Major; ARMA, GARCH, and POMP log-likelihoods are not comparable because they condition on different data transformations and observation models (matches Human Issue #7)
- Finding 5 (No Profile Likelihoods for Key Parameters): A — Major; profile likelihoods absent for all structural parameters, leaving identifiability unassessed
- Finding 6 (Non-Convergence Acknowledged but Not Remediated): F — Major; Doug treats non-convergence of H_0 and sigma_nu as a critical problem requiring substantial remediation (contradicts Human Issue #5, which says weakly identified parameters are not necessarily a problem)
- Finding 7 (Quantitative Model Adequacy Assessment Is Incomplete): A — Major; no conditional log-likelihoods per time point, no ESS traces, and the simulation shown uses pre-optimization parameters
- Finding 8 (Pairs Plot Subset Criterion Differs Between Local and Global Searches): C — Minor; different log-likelihood cutoffs (20 vs. 10 units) make visual comparison of the two pairs plots uninformative
- Finding 9 (AIC Calculation for POMP Model Appears to Use Median Log-Likelihood): D — Minor; AIC is computed from the median rather than the maximum log-likelihood (matches Human Issues #4 and #6)
- Finding 10 (Conclusion Incorrectly Claims Good Fit Because Log-Likelihood Converges Quickly): C — Minor; convergence of the optimizer is a computational diagnostic, not evidence of model adequacy
- Finding 11 (Missing rw.sd Justification): C — Minor; uniform rw.sd = 0.02 applied to parameters on different scales with no justification
- Finding 12 (Global Search Box for mu_h Is Inconsistently Narrow): D — Minor; global box for mu_h is c(-1, 0) while local search starts at -5, potentially explaining bimodal clustering visible in log-likelihood vs mu_h (matches Human Issue #8)
- Finding 13 (Stationarity of Log-Returns Not Formally Tested): C — Minor; no ADF/KPSS test reported despite unusual spike in January 2021
- Finding 14 (Model Equation Notation Error): C — Minor; beta_n uses Y_n in the text equation but the implementation passes the previous observed return via covariate covaryt
- Finding 15 (No Discussion of Model Limitations Regarding the Unprecedented Price Spike): D — Minor; the Breto (2014) model lacks jump components and the paper does not address whether smooth log-volatility dynamics are appropriate for the WallStreetBets shock (matches Human Issue #2)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "21.06.3 — phi and sigma_eta identifiability: paper should not frame weak identifiability as a convergence problem but note profile likelihoods are needed to assess it")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "21.06.1 — AIC cross-class comparison needs qualification: POMP advantage over ARMA reflects modeling a richer feature, not just better optimization; models' differing scopes should be discussed")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "21.06.13 — Filtering-on-simulated-data section: text does not make clear the log-likelihood is from synthetic data, not real GME data; section needs explicit statement of purpose")

**Findings classification:**
- 21.06.5: A — MLE parameter estimates never reported in paper despite being written to CSV
- 21.06.14: A — No profile likelihoods or confidence intervals provided for any POMP parameter
- 21.06.4: A — Fixed leverage model (sigma_nu=0) never formally compared to stochastic leverage model
- 21.06.2: A — GARCH AIC table shows large non-monotone swings indicating numerical instability in higher-order fits
- 21.06.1: D — AIC cross-class comparison needs qualification; model scope differences should be discussed (matches Human Issue #7)
- 21.06.3: D — phi and sigma_eta slow convergence reflects weak identifiability, not a convergence problem; framing should change (matches Human Issue #5)
- 21.06.12: C — ARMA residual ACF shows significant correlations; specific lags should be named
- 21.06.13: D — Filtering-on-simulated-data section lacks explicit statement that log-likelihood is from synthetic data and why the section is there (matches Human Issue #10)
- ESS not monitored: C — Effective sample size during particle filtering never reported; filter degeneracy concern given GME's January 2021 spike
- Gaussian measurement model: C — dnorm measurement model may underfit heavy tails documented in QQ plots; Student-t alternative not discussed
- Typographical errors: C — "log-golatility" typo and inconsistent "loglikelihood"/"log-likelihood" usage

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 6 | 4 | 4 |
| B (AI major, human also found) | 0 | 0 | 2 | 0 |
| C (AI minor, human missed) | 5 | 4 | 5 | 4 |
| D (AI minor, human also found) | 3 | 5 | 3 | 3 |
| E (Human found, AI missed) | 7 | 4 | 2 | 7 |
| F (Human-AI contradiction) | 1 | 0 | 1 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 3 | 7 | 2/9 = 22% | 6 | 5 | 11/14 = 79% |
| Charlie | 0 | 5 | 4 | 6/10 = 60% | 6 | 4 | 10/15 = 67% |
| Doug | 2 | 3 | 2 | 7/9 = 78% | 4 | 5 | 9/14 = 64% |
| Evan | 0 | 3 | 7 | 3/10 = 30% | 4 | 4 | 8/11 = 73% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Motivation was somewhat unclear: explain the relationship between studying volatility and understanding the GameStop story. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: Show returns with a mean, and don't also show demeaned returns which is visually almost identical. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 10 human issues (20%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #5: If some parameters are weakly identified, that is not necessarily a problem for the model: it just means that those parts of the model are not so important. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
