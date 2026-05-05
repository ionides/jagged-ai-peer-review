# Ned-Clean Analysis — W22 Project 07

---

## Human Issues

1. Model is missing a normal error in the term Y_n = exp{H_n/2} * epsilon_n.
2. Based on the GARCH analysis, one might try epsilon_n having a t distribution rather than normal. The effective sample size plot also suggests that — there are some jumps that are large outliers under a normal model.
3. A simpler stochastic volatility model might be worth trying before advancing to stochastic volatility with leverage.
4. Conclusion: "improvements of log likelihood were not significant" moving from normal to t GARCH seems wrong — make a likelihood ratio test.
5. Conclusion: "The POMP models perform much better than the GARCH for both Ford and Tesla" does not seem to be supported by the likelihoods. But it looks like the Tesla POMP model was fitted to a reduced length time series (for practical reasons of finishing the analysis) which is not described in the report.
6. An AIC table for ARMA(p,q) is mentioned but not shown.
7. "Other models with competitive AIC values are not invertible or causal, with polynomial roots inside of the unit circle" seems implausible, since arima() will never fit roots inside the unit circle.
8. Plotting simulations from the mechanistic models would allow us to visually assess the fitted models.
9. Typo: "(why we want to use log return instead of return?)" should be deleted.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by Finding 7: "POMP model description inconsistent — Y_n equation deterministic but code implements normal distribution")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by Finding 1: "Tesla POMP uses only 365 observations while Ford uses all 1,258")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by Finding 9: "incomplete sentence left in introduction")

**Findings classification:**
- Finding 1 [MAJOR]: B — Tesla POMP uses only 365 obs while Ford uses all 1,258 (matches Human Issue #5)
- Finding 2 [MAJOR]: A — POMP vs GARCH comparison invalid because log-likelihoods are not comparable (Human Issue #5 already counted via Finding 1)
- Finding 3 [MAJOR]: A — Bug in Tesla GARCH prediction plot: Ford's predicted volatility used for Tesla
- Finding 4 [MAJOR]: A — Model equation for R_n algebraically equals 1 due to typographical error
- Finding 5 [MAJOR]: A — Ford global search references missing file and uses wrong run_level object
- Finding 6 [MAJOR]: A — Ford and Tesla POMP run at different computational scales (sequential vs parallel)
- Finding 7 [MAJOR]: B — POMP model description inconsistent: Y_n written as deterministic but code implements Y_n ~ N(0, exp(H/2)) (matches Human Issue #1)
- Finding 8 [MINOR]: C — Tesla POMP section duplicates figure captions from a different project ("Apple")
- Finding 9 [MINOR]: D — Incomplete sentence "(why we want to use log return instead of return?)" left in document (matches Human Issue #9)
- Finding 10 [MINOR]: C — GARCH model selection criteria inconsistently applied across model variants
- Finding 11 [MINOR]: C — Weak identifiability of mu_h and H_0 rationalized rather than addressed
- Finding 12 [MINOR]: C — Ford global search convergence discussion references wrong figure number
- Finding 13 [MINOR]: C — Decomposition applied to non-stationary log returns and interpreted as meaningful trend
- Finding 14 [MINOR]: C — References section labeled "Scholarships" instead of "References"
- Finding 15 [MINOR]: C — YAML header contains typo disabling table of contents numbering

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by Major Issue 1: "Tesla POMP uses different dataset than Tesla GARCH, invalidating all cross-model comparisons for Tesla")
- Human Issue #6: covered (matched by Major Issue 3: "Promised AIC comparison across ARIMA, GARCH, and POMP never delivered")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by Minor Issue 15: "Incomplete sentence and informal language in the text")

**Findings classification:**
- Major 1 [MAJOR]: B — Tesla POMP uses different dataset than Tesla GARCH (matches Human Issue #5)
- Major 2 [MAJOR]: A — Conclusion that POMP outperforms GARCH contradicted by Ford likelihoods (Human Issue #5 already counted via Major 1)
- Major 3 [MAJOR]: B — Promised three-way AIC comparison across ARIMA, GARCH, and POMP never delivered (matches Human Issue #6)
- Major 4 [MAJOR]: A — Ford global search actual computation does not match reported methodology
- Major 5 [MAJOR]: A — No profile likelihoods reported for any parameter
- Major 6 [MAJOR]: A — Typographical error in leverage function formula: R_n evaluates to 1 for all G_n
- Major 7 [MAJOR]: A — Normal GARCH and t-GARCH log-likelihoods compared without noting different normalization conventions
- Minor 8 [MINOR]: C — Tesla prediction plot (Figure 10) uses Ford forecast uncertainty, not Tesla's
- Minor 9 [MINOR]: C — Figure captions in Tesla POMP section misidentify stock as "Apple"
- Minor 10 [MINOR]: C — Tesla local and global POMP searches use sequential execution rather than parallel
- Minor 11 [MINOR]: C — No benchmark comparison for POMP models
- Minor 12 [MINOR]: C — Citation numbering internally inconsistent (Breto 2014 not in reference list)
- Minor 13 [MINOR]: C — Decomposition of log returns treated as revealing meaningful trends
- Minor 14 [MINOR]: C — Global search box for phi is overly narrow given bimodal behavior
- Minor 15 [MINOR]: D — Incomplete sentence "(why we want to use log return instead of return?)" left in final submission (matches Human Issue #9)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by Major Issue 2: "Tesla POMP uses only last 365 observations; Ford POMP uses all 1,258")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by minor issue: "No model diagnostics specific to the POMP stochastic leverage model")
- Human Issue #9: covered (matched by minor issue: "Unresolved sentence fragment in introduction")

**Findings classification:**
- Major 1 [MAJOR]: A — Initial particle-filter benchmark evaluated on simulated data, not real data
- Major 2 [MAJOR]: B — Tesla POMP uses only last 365 observations; Ford uses all 1,258 (matches Human Issue #5)
- Major 3 [MAJOR]: A — Tesla global IF2 search incorrectly initialized from previous mif2 result
- Major 4 [MAJOR]: A — Claim that POMP outperforms GARCH is not supported (Human Issue #5 already counted via Major 2)
- Major 5 [MAJOR]: A — Non-convergence acknowledged but results interpreted as substantively meaningful
- Major 6 [MAJOR]: A — No benchmark comparison between POMP and non-mechanistic baseline
- Major 7 [MAJOR]: A — No profile likelihoods or confidence intervals for any parameter
- Major 8 [MAJOR]: A — Particle count and computational settings inadequate; archived files contradict reported methodology
- Minor: Unresolved sentence fragment in introduction — D (matches Human Issue #9)
- Minor: Figure caption mismatch in Tesla section — C
- Minor: Wrong-dataset prediction for Tesla GARCH (Ford ahead used for Tesla plot) — C
- Minor: Tesla model description refers to "Apple" — C
- Minor: ARMA model selection not connected to GARCH (no ARCH test) — C
- Minor: No model diagnostics specific to POMP stochastic leverage model — D (matches Human Issue #8)
- Minor: mu_h not properly log-transformed in partrans — C
- Minor: Reference [2] cited as Breto (2014) but listed as course lecture notes — C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by M2: "Cross-model conclusion contradicted by paper's own numbers")
- Human Issue #6: covered (matched by m2: "ARMA AIC table absent from report body")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by m4: "Inline authoring note not removed")

**Findings classification:**
- M1 [MAJOR]: A — Baseline pfilter run on simulated data, not actual returns
- M2 [MAJOR]: B — Cross-model conclusion that POMP outperforms GARCH contradicted by paper's own likelihoods (matches Human Issue #5)
- M3 [MAJOR]: A — Tesla prediction figure uses Ford volatility bands due to variable naming error
- M4 [MAJOR]: A — No profile likelihoods or confidence intervals
- M5 [MAJOR]: A — Measurement model architecture (rmeasure/dmeasure design) unexplained
- m1 [MINOR]: C — R_n formula typeset as 1 (LaTeX transcription error)
- m2 [MINOR]: D — ARMA AIC table absent from report body (matches Human Issue #6)
- m3 [MINOR]: C — Global search initializes from local search object, limiting exploration
- m4 [MINOR]: D — Inline authoring note "(why we want to use log return instead of return?)" not removed (matches Human Issue #9)
- m5 [MINOR]: C — Ford uses 1,000 particles vs Tesla's 2,000 at run_level=3; uneven computational investment undiscussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 5 | 7 | 4 |
| B (AI major, human also found) | 2 | 2 | 1 | 1 |
| C (AI minor, human missed) | 7 | 6 | 6 | 3 |
| D (AI minor, human also found) | 1 | 1 | 2 | 2 |
| E (Human found, AI missed) | 6 | 6 | 6 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex:**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+6) = 3/9 = 0.333
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+7) / (5+2+7+1) = 12/15 = 0.800

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+6) = 3/9 = 0.333
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+6) / (5+2+6+1) = 11/14 = 0.786

**Doug:**
- Human Recall = (B+D) / (B+D+E) = (1+2) / (1+2+6) = 3/9 = 0.333
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+6) / (7+1+6+2) = 13/16 = 0.813

**Evan:**
- Human Recall = (B+D) / (B+D+E) = (1+2) / (1+2+6) = 3/9 = 0.333
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+3) / (4+1+3+2) = 7/10 = 0.700

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer (0 out of 4 reviewers covered them):

- Human Issue #2: Suggestion to try t distribution for epsilon_n in the POMP/SV model; effective sample size plot suggests heavy tails. (4 out of 4 reviewers missed)
- Human Issue #3: Suggestion to try a simpler stochastic volatility model before advancing to stochastic volatility with leverage. (4 out of 4 reviewers missed)
- Human Issue #4: The claim "improvements of log likelihood were not significant" moving from normal to t GARCH is wrong; a likelihood ratio test should be made. (4 out of 4 reviewers missed)
- Human Issue #7: The claim that other ARMA models have roots inside the unit circle is implausible since arima() never fits such roots. (4 out of 4 reviewers missed)

Total consensus misses: 4 out of 9 human issues.

### Unique finds per reviewer

Human issues covered by exactly one reviewer (all others missed):

- Human Issue #1 (missing epsilon_n in measurement equation): covered only by Alex.
- Human Issue #8 (plotting simulations from mechanistic model): covered only by Doug.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

1. **Tesla GARCH prediction plot bug:** The Tesla GARCH forecast figure (Figure 10) uses Ford's predicted volatility (`ford_ahead[,2]`) instead of Tesla's (`tesla_ahead[,2]`) for the confidence band, making the Tesla forecast figure incorrect. Raised by all four reviewers (Alex as Major, Charlie as Minor, Doug as Minor, Evan as Major).

Total universal AI-only flags: 1.
