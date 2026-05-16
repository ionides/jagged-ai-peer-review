# Ned-Clean Analysis — W24 Project 13

---

## Human Issues

1. There is too much R output, including unexplained warning messages.
2. Non-English content is present; the reader cannot be expected to understand other languages in the context of this course.
3. The time plots would be more informative on a log scale; the sample ACF would also be more informative on the log of the data.
4. The three graphs at the beginning are confusing — they all have the same title, and it is not immediately obvious what the difference is between them (labels not all in English; unclear which shows all cases vs. first/second waves).
5. Aggregating cases over weeks can be a good way to avoid the weekly reporting pattern; otherwise it must be addressed explicitly in models or data analysis of daily data.
6. Preferring auto.arima because it also does other things (unexplained and presumably not understood) is a problematic way to pick statistical methodology.
7. The conclusions do not relate the ARIMA analysis to the POMP analysis; in fact they don't discuss ARIMA at all despite much of the report being spent on it; log-likelihoods should be compared (with care for differencing).
8. The ARIMA results are not always clear about which wave is under consideration; results for the first wave have little relevance for the subsequent analysis.
9. The SARIMA code sets frequency=52 rather than frequency=7 for 7 days in a week with daily data.
10. The fitted value plot for ARIMA can look over-optimistic, since even a simple model like "predict day n by the data on day n-1" would look similarly good.
11. The QQ-plot comments are incorrect: the QQ-plot shows the distribution of residuals, not the case data; the comment about using Poisson or negative binomial is therefore also incorrect.
12. Less time spent on ARIMA would allow more attention to the mechanistic modeling, which is more central to the conclusions.
13. In the local search results, the log-likelihood does not change much from the beginning of particle filtering — the search is not improving results much, parameters are not changing much; the statement that most parameters converge is incorrect.
14. A profile likelihood would be helpful to evaluate parameter estimates and assess whether parameters are accurately estimated.
15. Numbers and captions for figures would help the reader.
16. References should have name/title/year (e.g., APA format); all references should be cited in the text; the introduction has no references.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "auto.arima justification circular and unsupported")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "ts() frequency=52 misspecified for daily data")
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: covered (matched by finding: "no likelihood profile or uncertainty quantification")
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (Critical — R-language step function syntax errors / undefined variables): A — broken R prototype code; human did not raise
- Finding 2 (Critical — hard-coded absolute file path): A — reproducibility failure; human did not raise
- Finding 3 (Critical — measurement model misspecified: H accumulates recoveries): A — H tracks recoveries not quarantine entries; human did not raise
- Finding 4 (Critical — hard-coded intervention at t=125 unexplained): A — undocumented impulse; human did not raise
- Finding 5 (Major — fixed parameters mu_QR_o/b/r, k without justification): A — fixed parameters without justification; human did not raise
- Finding 6 (Major — local search uses %do% not %dopar%): A — sequential instead of parallel local search; human did not raise
- Finding 7 (Major — global search filter threshold of 1000 too permissive): A — loglik window of 1000 is enormous; human did not raise
- Finding 8 (Major — no likelihood profile or uncertainty quantification): B — matches Human Issue #14
- Finding 9 (Major — model description inconsistencies: Beta vs. Omicron labeling): A — compartment labeling inconsistent with epidemiological narrative; human did not raise
- Finding 10 (Major — SARIMA model selection: auto.arima justification circular): B — matches Human Issue #6
- Finding 11 (Moderate — ts() frequency=52 misspecified): D — matches Human Issue #9
- Finding 12 (Moderate — no simulation diagnostic plots after fitting): C — post-fit simulations absent; human did not raise
- Finding 13 (Moderate — Beta_or parameter unused in Csnippet): C — orphaned parameter; human did not raise
- Finding 14 (Minor — WARIMA term used inconsistently): C — terminology not formalized; human did not raise
- Finding 15 (Minor — data loading inconsistency: Google API vs. local CSV): C — data provenance not explained; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 13 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no quantitative comparison between SARIMA and POMP models")
- Human Issue #8: covered (matched by finding: "SARIMA model identified as WARIMA(4,1,1) but auto.arima returns different orders; unclear which model used")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "insufficient computational effort with no convergence justification")
- Human Issue #14: covered (matched by finding: "no profile likelihoods or confidence intervals")
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (Major — non-functional R prototype step function): A — broken code; human did not raise
- Finding 2 (Major — Beta_or declared but never used): A — orphaned parameter; human did not raise
- Finding 3 (Major — infection force driven by Q not I): A — epidemiologically backwards transmission; human did not raise
- Finding 4 (Major — no benchmark comparison against non-mechanistic model): B — matches Human Issue #7
- Finding 5 (Major — no profile likelihoods or confidence intervals): B — matches Human Issue #14
- Finding 6 (Major — insufficient computational effort / no convergence justification): B — matches Human Issue #13
- Finding 7 (Major — hard-coded absolute path): A — reproducibility failure; human did not raise
- Finding 8 (Major — three rate parameters fixed without justification): A — fixed parameters without justification; human did not raise
- Finding 9 (Minor — H tracks recoveries not case reports): C — accumulator mismatch; human did not raise
- Finding 10 (Minor — impulse at t=125 undocumented): C — undocumented ad hoc intervention; human did not raise
- Finding 11 (Minor — R_b described twice, R_o missing): C — notation/documentation inconsistency; human did not raise
- Finding 12 (Minor — SARIMA model vs auto.arima orders inconsistent; unclear which model used): D — matches Human Issue #8
- Finding 13 (Minor — stationarity claims inconsistent with SARIMA assumptions): C — heteroskedasticity acknowledged but not addressed; human did not raise
- Finding 14 (Minor — loglik filter of 1000 too permissive): C — filter extremely wide; human did not raise
- Finding 15 (Minor — no model diagnostics or forward simulation comparison): C — diagnostic plots absent; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 12 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "AIC table uses non-seasonal ARIMA — comparison with auto.arima is across non-comparable model classes")
- Human Issue #7: covered (matched by finding: "no quantitative comparison between SARIMA and POMP models")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "SARIMA period misspecification: frequency=52 for daily data")
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "insufficient computational effort — too few iterations and replicates")
- Human Issue #14: covered (matched by finding: "no profile likelihoods or confidence intervals")
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (Major — no quantitative comparison between SARIMA and POMP): B — matches Human Issue #7
- Finding 2 (Major — broken R-code step function): A — undefined variables, wrong argument signatures; human did not raise
- Finding 3 (Major — hard-coded absolute path): A — reproducibility failure; human did not raise
- Finding 4 (Major — no profile likelihoods or confidence intervals): B — matches Human Issue #14
- Finding 5 (Major — insufficient computational effort): B — matches Human Issue #13
- Finding 6 (Major — SARIMA period misspecification frequency=52): B — matches Human Issue #9
- Finding 7 (Major — H tracks recoveries not quarantine entries): A — accumulator variable mismatch; human did not raise
- Finding 8 (Major — no benchmark comparison against non-mechanistic model): A — separate from Finding 1; human #7 already matched; human did not separately raise non-mechanistic benchmark comparison
- Finding 9 (Major — model diagnostic checks absent): A — no ESS, no conditional loglik plots; human did not raise
- Finding 10 (Major — Beta_or in paramnames but never used): A — orphaned parameter; human did not raise
- Finding 11 (Minor — confusion about which strains are modeled): C — labeling inconsistency; human did not raise
- Finding 12 (Minor — %do% instead of %dopar% for local search): C — sequential local search; human did not raise
- Finding 13 (Minor — AIC table uses non-seasonal ARIMA, non-comparable to auto.arima): D — matches Human Issue #6
- Finding 14 (Minor — no reported log-likelihood values in text): C — best loglik not stated in prose; human did not raise
- Finding 15 (Minor — typographical and notational errors): C — typos and duplicate parameter definitions; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "AIC table minimum vs auto.arima choice not reconciled")
- Human Issue #7: covered (matched by finding: "no benchmark comparison — POMP vs SARIMA not compared quantitatively")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "non-convergent mif2 traces")
- Human Issue #14: covered (matched by finding: "no profile likelihoods or parameter uncertainty")
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (Major — transmission force driven by Q not I): A — epidemiologically backwards; human did not raise
- Finding 2 (Major — undisclosed hard-coded perturbation at t=125): A — undisclosed structural assumption; human did not raise
- Finding 3 (Major — no benchmark comparison): B — matches Human Issue #7
- Finding 4 (Major — no profile likelihoods or parameter uncertainty): B — matches Human Issue #14
- Finding 5 (Major — non-convergent mif2 traces): B — matches Human Issue #13
- Finding 6 (Minor — fixed parameters without justification): C — mu_QR and k fixed without epidemiological sources; human did not raise
- Finding 7 (Minor — code inconsistency between R prototype and Csnippet): C — untested R prototype; human did not raise
- Finding 8 (Minor — severe Monte Carlo variability, loglik.se up to 89.3): C — Np=2000 insufficient at some parameter settings; human did not raise
- Finding 9 (Minor — no ESS diagnostics): C — particle filter reliability unassessed; human did not raise
- Finding 10 (Minor — rho search range constraint [0.4,0.6] not justified): C — narrow range may prevent finding true MLE; human did not raise
- Finding 11 (Minor — biologically inconsistent initial conditions: I_o=0, Q_o=100): C — quarantined without infectious source; human did not raise
- Finding 12 (Minor — AIC table minimum vs auto.arima not reconciled): D — matches Human Issue #6

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 12 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 9 | 5 | 6 | 2 |
| B (AI major, human also found) | 2 | 3 | 4 | 3 |
| C (AI minor, human missed) | 4 | 6 | 4 | 6 |
| D (AI minor, human also found) | 1 | 1 | 1 | 1 |
| E (Human found, AI missed) | 13 | 12 | 11 | 12 |

---

## Per-Reviewer Metrics

- Human Recall = (B + D) / (B + D + E)
- AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 13 | 3/16 = 18.8% | 9 | 4 | 13/16 = 81.3% |
| Charlie | 3 | 1 | 12 | 4/16 = 25.0% | 5 | 6 | 11/15 = 73.3% |
| Doug | 4 | 1 | 11 | 5/16 = 31.3% | 6 | 4 | 10/15 = 66.7% |
| Evan | 3 | 1 | 12 | 4/16 = 25.0% | 2 | 6 | 8/12 = 66.7% |

---

## Cross-Reviewer Aggregation

### Consensus Misses

Human issues that every reviewer failed to cover (all four missed):

- Human Issue #1: Too much R output, including unexplained warning messages.
- Human Issue #2: Non-English content; reader cannot be expected to understand other languages.
- Human Issue #3: Time plots would be more informative on a log scale; ACF also more informative on log of data.
- Human Issue #4: Three graphs at beginning are confusing — same title, unclear difference (labels not in English, unclear which shows all cases vs. waves).
- Human Issue #5: Aggregating cases over weeks avoids weekly reporting pattern; otherwise must be addressed explicitly.
- Human Issue #8: ARIMA results not always clear about which wave; first-wave results have little relevance for subsequent analysis.
- Human Issue #10: Fitted value plot for ARIMA looks over-optimistic.
- Human Issue #11: QQ-plot comments incorrect — shows residual distribution not case data; Poisson/NB comment therefore also incorrect.
- Human Issue #12: Less time on ARIMA would allow more attention to mechanistic modeling.
- Human Issue #15: Numbers and captions for figures would help the reader.
- Human Issue #16: References should have name/title/year; all references should be cited; introduction has no references.

Total consensus misses: 11 out of 16 human issues (68.8%).

### Unique Finds Per Reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #9 (frequency=52 misspecification): covered only by Alex (D) and Doug (B). Not unique to one reviewer — covered by both Alex and Doug. Covered by neither Charlie nor Evan.

Reviewing more carefully — issues covered by exactly ONE reviewer:

- Human Issue #7 (conclusions don't relate ARIMA to POMP): covered by Charlie (B), Doug (B), Evan (B) — NOT unique.
- Human Issue #6 (auto.arima justification problematic): covered by Alex (B), Doug (D), Evan (D) — NOT unique.
- Human Issue #9 (frequency=52): covered by Alex (D), Doug (B) — NOT unique.
- Human Issue #8 (ARIMA results not clear about which wave): covered only by Charlie (D) — UNIQUE to Charlie.
- Human Issue #13 (local search not improving): covered by Charlie (B), Doug (B), Evan (B) — NOT unique.
- Human Issue #14 (profile likelihood): covered by Alex (B), Charlie (B), Doug (B), Evan (B) — NOT unique.

Summary: Only Human Issue #8 was covered by exactly one reviewer (Charlie).

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-Only Flags

Issues raised as Major by every reviewer that the human did not mention:

- Broken R prototype step function (undefined variables, wrong signatures): raised by Alex (A), Charlie (A), Doug (A) as Major; raised by Evan (C) as Minor. Raised as Major by 3 of 4 reviewers.
- Hard-coded absolute file path: raised by Alex (A), Charlie (A), Doug (A) as Major; not raised by Evan. Raised as Major by 3 of 4 reviewers.

Issues raised by all four reviewers (any severity) that the human did not mention:

- Broken R prototype: Alex (A/Critical), Charlie (A/Major), Doug (A/Major), Evan (C/Minor) — all four flagged this.
- Hard-coded absolute path: Alex (A/Critical), Charlie (A/Major), Doug (A/Major) — Evan did NOT flag this. Only 3 of 4.
- No profile likelihoods (already matched to Human #14 — not AI-only).
- Beta_or parameter unused: Alex (C/Moderate), Charlie (A/Major), Doug (A/Major) — Evan did NOT flag this. Only 3 of 4.

True universal AI-only flags (all four reviewers flagged, human missed):

- Broken R prototype step function: all four reviewers flagged this (as Major by Alex, Charlie, Doug; as Minor by Evan). Count: 1.

No other issue was flagged as a concern by all four reviewers while the human missed it.
