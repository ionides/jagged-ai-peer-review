# Ned-Clean Analysis — W24 Project 06

---

## Human Issues

1. The report is written as a working draft — too much raw R code and output, too little explanation or motivation.
2. The project has weak motivation; comparing two models is a standard task done many times before in STATS 531.
3. The introduction lacks a data source/citation and time frame of analysis.
4. The introduction does not define volatility and log-returns for readers unfamiliar with financial analyses.
5. Some Data section plots are not discussed.
6. The ACF/PACF interpretation is incorrect: both the counting and the reasoning are wrong.
7. The ADF test is not appropriate for data with time-varying sample variance.
8. The KPSS test is not covered in class and lacks a full definition and citation.
9. "Data is stationary" should be written as "data can appropriately be modeled as stationary"; stationarity is a property of models, not data.
10. GARCH is not well explained; the rugarch likelihood() function returns the log-likelihood, and the AIC definition is unclear.
11. The quantity called AIC is not the usual definition (minus twice the log-likelihood plus twice the number of parameters).
12. The stochastic volatility model could have longer-than-Gaussian tails; the likelihood anomalies between the stochastic volatility model and t-GARCH would be interesting to investigate.
13. There is no reference to previous 531 projects; Project 6 is similar to project 7 and the better 2022 project.
14. Numbered figures and captions would help the reader.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF/PACF interpretation is incorrect — reversed logic")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Log-likelihood values not comparable across models")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed

**Findings classification:**
- Major Issue 1 (log-likelihood not comparable): B — likelihood/log-likelihood confusion and scale mismatch (matches Human Issue #10)
- Major Issue 2 (POMP global search does not explore meaningful space): A — global search box contradicts local search results
- Major Issue 3 (H_0 and mu_h do not converge, no corrective action): A — non-convergence acknowledged but left unresolved
- Major Issue 4 (particle filter on simulated object, not real data): A — pf1 computed on sim1.filt rather than NADQ.filt
- Major Issue 5 (ACF/PACF interpretation reversed): B — counting and reasoning are wrong (matches Human Issue #6)
- Minor Issue 6 (frequency=1 incorrect for daily data): C — time series frequency specification error
- Minor Issue 7 (notational inconsistency beta_n vs beta): C — timing convention for beta not clarified in exposition
- Minor Issue 8 (no profile likelihood or confidence intervals): C — no uncertainty quantification for POMP parameters
- Minor Issue 9 (GARCH(4,1) overfitted, not justified): C — unusual order not discussed for stationarity/positivity constraints
- Minor Issue 10 (log(likelihood) output misinterpreted): C — per-observation vs total log-likelihood conflated
- Minor Issue 11 (no simulation-based model validation for POMP): C — no post-fit simulation diagnostic
- Minor Issue 12 (NDAQ vs NASDAQ confusion): C — data described as NASDAQ but ticker is for Nasdaq Inc., not the index
- Minor Issue 13 (stew() files not reproducible without .rda files): C — intermediate .rda files not included in submission
- Minor Issue 14 (pairs plot threshold of 300 too broad): C — extremely permissive window obscures parameter structure
- Minor Issue 15 (conclusions understate model problems): C — non-convergence framed as future improvement rather than fundamental flaw

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 12 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF/PACF interpretation reversed — ACF guides MA order, PACF guides AR order")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Likelihood values compared across incompatible scales")
- Human Issue #11: covered (matched by finding: "GARCH AIC cannot be compared to ARMA AIC due to per-observation scaling")
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed

**Findings classification:**
- Major Issue 1 (likelihood values on incompatible scales): B — likelihood/log-likelihood scale mismatch across model families (matches Human Issue #10)
- Major Issue 2 (POMP does not outperform, no remediation): A — failure to investigate why POMP underperforms GARCH
- Major Issue 3 (no profile likelihoods or confidence intervals): A — no uncertainty quantification for POMP parameters
- Major Issue 4 (computational adequacy insufficient and undocumented): A — pairs plot window too wide; IF2 convergence not demonstrated
- Major Issue 5 (notational inconsistency beta_n vs beta): A — model equations ambiguous between time-indexed and scalar beta
- Major Issue 6 (global search box inconsistent with local search results): A — mu_h optimal near -10 but box restricted to (-1, 0)
- Major Issue 7 (ACF/PACF interpretation reversed): B — spike-counting heuristic identifies wrong orders and logic is backwards (matches Human Issue #6)
- Major Issue 8 (no POMP model diagnostics — ESS, conditional log-likelihoods): A — no particle filter diagnostics after fitting
- Major Issue 9 (GARCH AIC not comparable to ARMA AIC due to per-observation scaling): B — per-observation vs total AIC conflated (matches Human Issue #11)
- Minor: Typo "Model Discription": C — spelling error in section title
- Minor: Global search variable name bug ('if' exported): C — reserved keyword in export list
- Minor: Stationarity test conclusion confusingly phrased: C — ADF p-value truncation not clearly explained
- Minor: Missing parameter transformation check: C — mu_h estimated on untransformed scale without justification
- Minor: No random seed for ARMA/GARCH sections: C — reproducibility gap for deterministic model fits
- Minor: References inadequate (Wikipedia, repeated citations): C — inappropriate citations for statistical methods
- Minor: Initial filter likelihood estimate not discussed: C — L.pf1 value unexplained and appears to use simulated data
- Minor: Local search pairs plot window too wide: C — 300-unit window obscures parameter structure near MLE
- Minor: Conclusion states 3510 but output shows 3513: C — minor inconsistency in reported global maximum

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF/PACF interpretation reversed")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Misinterpretation of GARCH likelihood output")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed

**Findings classification:**
- Major Issue 1 (invalid direct log-likelihood comparison across model families): A — broader comparison invalidity argument beyond H10 scope
- Major Issue 2 (non-convergence of mu_h and H_0 left unresolved): A — convergence failure acknowledged but no action taken
- Major Issue 3 (no profile likelihoods or parameter uncertainty): A — pairs plot threshold 300 units too wide; no CIs
- Major Issue 4 (global search initialized from if1[[1]] only): A — subtle misuse of mif2 anchors global search near local solution
- Major Issue 5 (likelihood evaluation discrepancy between sim1.filt and NADQ.filt): A — inconsistency not explained
- Major Issue 6 (misinterpretation of GARCH likelihood output): B — log(likelihood()) yields per-observation value; confusion between likelihood and log-likelihood (matches Human Issue #10)
- Minor: Typo "Model Discription": C — spelling error in section title
- Minor: ACF/PACF interpretation reversed: D — AR/MA identification logic backwards (matches Human Issue #6)
- Minor: ARMA(4,4) overfitting not discussed: C — risk of overfitting relative to simpler GARCH(1,1) not commented on
- Minor: sigma_nu near zero (boundary value): C — possible model misspecification or parameter degeneracy
- Minor: Pairs plot threshold too wide: C — 300-unit window vs standard ~2-unit window for 95% CI
- Minor: NADQ vs NASDAQ variable naming: C — minor inconsistency in variable names
- Minor: References inadequate: C — URLs and partial citations rather than peer-reviewed sources
- Minor: frequency=1 for daily data: C — treats data as annual, makes axis labels misleading
- Minor: QQ-plot is non-standard: C — reference line plotted incorrectly
- Minor: beta_n in text uses Y_n but code uses Y_state: C — inconsistency between text notation and code implementation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 12 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Data description incomplete — date range, observations, data source not stated")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF/PACF order interpretation reversed")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Likelihood-scale confusion invalidates central model comparison")
- Human Issue #11: covered (matched by finding: "GARCH and ARMA AIC tables on different scales")
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed

**Findings classification:**
- 24.06.1 (likelihood-scale confusion invalidates central model comparison): B — rugarch likelihood() output treated as raw likelihood; log() applied yielding meaningless number (matches Human Issue #10)
- 24.06.2 (non-convergence of mu_h and H_0 invalidates POMP likelihood): A — reported log-likelihood is lower bound, not MLE; comparison unreliable
- 24.06.3 (sigma_eta severely non-identifiable in global search): A — parameter ranges from 0 to 100+ with no concentration; profile likelihood needed
- 24.06.5 (no profile likelihoods or confidence intervals): A — point estimates without uncertainty bounds; pairs plot at -300 threshold is uninformative
- 24.06.4 (ACF/PACF interpretation reversed): D — PACF informs AR order, ACF informs MA order, not the reverse (matches Human Issue #6)
- 24.06.5b (GARCH and ARMA AIC tables on different scales): D — GARCH AIC is per-observation while ARMA AIC is total; not noted in text (matches Human Issue #11)
- 24.06.13 (no forward simulation from fitted POMP model): C — post-fit simulation diagnostic absent
- 24.06.10b (data description incomplete): D — exact date range, number of observations, data source not stated (matches Human Issue #3)
- 24.06.6 (code export typo — 'if' keyword): C — reserved keyword in foreach export list; possible silent error

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 2 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 10 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 3 | 6 | 5 | 3 |
| B (AI major, human also found) | 2 | 3 | 1 | 1 |
| C (AI minor, human missed) | 10 | 9 | 9 | 2 |
| D (AI minor, human also found) | 0 | 0 | 1 | 3 |
| E (Human found, AI missed) | 12 | 11 | 12 | 10 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall | AI-Unique Rate |
|----------|-------------:|---------------:|
| Alex | 2/14 = 14.3% | 13/15 = 86.7% |
| Charlie | 3/14 = 21.4% | 15/18 = 83.3% |
| Doug | 2/14 = 14.3% | 14/16 = 87.5% |
| Evan | 4/14 = 28.6% | 5/9 = 55.6% |

- Human Recall = (B + D) / (B + D + E)
- AI-Unique Rate = (A + C) / (A + B + C + D)

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (10 out of 14):

1. H1 — The report is written as a working draft; too much raw R code, too little explanation.
2. H2 — Weak motivation; comparing models is a standard task done many times in STATS 531.
4. H4 — No definitions for volatility and log-returns for unfamiliar readers.
5. H5 — Some Data section plots are not discussed.
7. H7 — The ADF test is not appropriate for time-varying sample variance.
8. H8 — The KPSS test lacks a full definition and citation.
9. H9 — "Data is stationary" should be "data can appropriately be modeled as stationary."
12. H12 — The SV model could have longer-than-Gaussian tails; likelihood anomalies between SV and t-GARCH deserve investigation.
13. H13 — No reference to previous 531 projects; Project 6 is similar to the 2022 project.
14. H14 — Numbered figures and captions would help the reader.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Alex: 0
- Charlie: 0
- Doug: 0
- Evan: 1 (H3 — introduction lacks data source/citation and time frame)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention (2 total):

1. Non-convergence of mu_h and H_0 left unresolved — all four reviewers (Alex Major Issue 3, Charlie Major Issue 2, Doug Major Issue 2, Evan 24.06.2) flagged that the authors acknowledge non-convergence but take no corrective action, making the reported POMP log-likelihood unreliable.
2. No profile likelihoods or parameter uncertainty quantification — all four reviewers (Alex Minor Issue 8, Charlie Major Issue 3, Doug Major Issue 3, Evan 24.06.5) noted the absence of profile likelihoods and confidence intervals for POMP parameters.
