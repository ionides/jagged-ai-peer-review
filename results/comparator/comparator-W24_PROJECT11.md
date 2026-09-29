# Comparator Analysis — W24 Project 11

---

## Human Issues

1. The introduction reads like ChatGPT. The conclusion also reads like it has been edited by ChatGPT. A tell-tale sign is sweeping statements made in elaborate language which are not well supported or linked to specific results from the project. According to the rules of the course, ChatGPT is allowed but should be properly attributed as a source.

2. ADF test is not designed for situations with time-varying sample variance, since neither the model used as a null hypothesis, nor the alternative model used to motivate the test statistic, have that feature.

3. Ljung-Box is also of borderline relevance. The null assumes independence, whereas time-varying variance suggests a model should have a lack of independence even if it is uncorrelated — GARCH and stochastic volatility both have that property.

4. The following sentence does not make sense: "Having verified both the stationarity and independence of the data, we can now proceed to the next stage: selecting an appropriate ARMA model." If we really want a stationary, independent model, the only possible ARMA model is ARMA(0,0). Later, the group claim that models which are not independent (e.g., GARCH and stochastic volatility) fit the data better, highlighting the flaw in the reasoning.

5. ARMA(0,0)+GARCH seems to be indistinguishable from GARCH, since there is no ARMA component. So, is the difference only the software used to fit the model? That could use some explanation and investigation.

6. The stated GARCH log-likelihood seems far too high, and is much higher than the stated ARMA(0,0)+GARCH log-likelihood. Such inconsistencies should be noted, and ideally resolved.

7. ARMA(0,0) here is an independent, identically distributed (iid) Gaussian model. It would be helpful to remind the reader of that.

8. The conclusions contain some thoughtful reasoning, but also have logical flaws. The explanation, "This aligns with the efficient market theory, emphasizing the importance of market unpredictability to prevent arbitrage opportunities," is true of stochastic volatility and GARCH as well as an iid model.

9. Since GARCH is white noise (following the definition provided by the group, with white noise interpreted in the weak sense) the ARMA + GARCH model is in fact ARMA, just non-Gaussian ARMA.

10. The authors did not provide the data with their report, so they do not meet the reproducibility expectations for the final project. Also, they have some absolute rather than relative file references.

11. In the "Exploratory Data Analysis" section, authors don't explain the huge jump on 2023/05/25 and its potential influence on their model fitting. As can be seen in their data plot, the close price on 2023/05/24 is 305 and the next day close price increases to 379, which is a considerable surge. This may be the reason for low ESS in their POMP model at time 340 (roughly). In section "POMP Model - Local Search", there is a great decrease in ESS, probably suggesting a bad fit on 2023/05/25.

12. In their GARCH analysis, they find the residuals following a t-distribution are more reasonable, but in their POMP model, they still build the model using normal distribution.

13. In the filter diagnostics that plotted effective sample size and conditional likelihood for the last iteration of their filtering process, there is a clear spike around time 340, as well as a smaller spike around 510. It would have been useful to mention this spike, even if it turns out to be irrelevant in their modeling. Is there something of note that happens around those time points in the data? Or is this something worth adjusting the model to account for?

14. The authors could have benefitted by paying attention to peer review on previous similar projects for this course, e.g., https://ionides.github.io/531w22/final_project/project07/comments.html.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH(1,1) Discarded for Wrong Reason — 1596 GARCH likelihood never reconciled with 1120 for same model class")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Hardcoded Absolute File Path Prevents Reproducibility")
- Human Issue #11: contradiction (AI says there are no ESS trace plots; human says ESS trace plots exist and show a clear spike around time 340)
- Human Issue #12: missed
- Human Issue #13: contradiction (AI says there are no ESS trace plots; human says ESS trace plots exist and show spikes at time 340 and 510)
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (ADF Test Conclusion Is Statistically Incorrect): A — inverted null hypothesis direction and retain/reject confusion; human #2 raises a different ADF criticism (wrong model assumption for time-varying variance), so no match
- Finding 2 (Likelihood Values Are Inconsistent Between Sections): A — ARMA(0,0) conclusion (1092) vs body (1087.62), POMP 1111 vs 1110; human #6 specifically concerns the implausibly high GARCH 1596, which is finding 8's territory, not this
- Finding 3 (Global Search Box Contradicts Reported Convergence Values): A — sigma_eta and mu_h converge outside their declared search bounds
- Finding 4 (GARCH Definition Contains a Notational Error): A — sigma_n incorrectly called iid white noise
- Finding 5 (Section Header Mislabeled as "ARIMA Model Selection"): C — should be "ARMA Model Selection"
- Finding 6 (LRT Test Statistics Computed But Not Reported): C — test stat values and p-values absent from output
- Finding 7 (Global Search Uses Only a Single Starting Chain): C — warm-starting from if1[[1]] defeats the purpose of global search
- Finding 8 (GARCH(1,1) Discarded for Wrong Reason): D — different normalization between garch() and garchFit(); 1596 vs 1120 inconsistency never reconciled (matches Human Issue #6)
- Finding 9 (Root Interpretation for Causality/Invertibility Is Confused): C — inside/outside unit circle convention reversed
- Finding 10 (k-Period Log-Return Formula Contains a Typographical Error): C — t_{t-1} typo; left-hand side is 1-period not k-period return
- Finding 11 (Hardcoded Absolute File Path Prevents Reproducibility): D — setwd() with absolute path; reproducibility concern (matches Human Issue #10)
- Finding 12 (Conclusion Incorrectly Attributes Lower Likelihood to ARMA(0,0)): C — 1092 in conclusion vs 1087.62 in ARMA section; same instance as finding 2 but no human issue covers this specific inconsistency
- Finding 13 (Global Search Box for phi Is Overly Narrow Without Justification): C — phi constrained to [0.95, 0.99] without diagnostic justification
- Finding 14 (No Discussion of POMP Model Simulation or Diagnostic Checks): F — claims no ESS trace plots exist, but human issues #11 and #13 describe existing ESS trace plots with visible spikes at time 340 and 510 (contradicts Human Issues #11 and #13)
- Finding 15 ("Daily Log Volatility" Statistic Is Mislabeled): C — quantity is standard deviation, not log volatility

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 10 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "tseries::garch() vs fGarch::garchFit() normalization discrepancy explains the ~500 log-unit gap between the two GARCH-related fits")
- Human Issue #6: covered (matched by finding: "tseries::garch() vs fGarch::garchFit() normalization discrepancy explains the ~500 log-unit gap between the two GARCH-related fits")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "hard-coded absolute file path prevents reproducibility")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (No profile likelihood): A — no profile likelihoods computed for any POMP parameter; parameter identifiability not assessed
- Finding 2 (Convergence failure not addressed): A — mu_h and H_0 convergence failures acknowledged but not diagnosed or resolved
- Finding 3 (Wrong log-likelihood in conclusion): A — conclusion labels 1092 as the ARMA(0,0) log-likelihood when 1087.62 is correct; 1092 belongs to ARMA(0,0)+GARCH normal
- Finding 4 (Hard-coded file path): B — setwd() with absolute local path prevents reproducibility (matches Human Issue #10)
- Finding 5 (ADF null hypothesis misstated): A — text says "keep the null hypothesis that time series is stationary" but ADF null is non-stationarity
- Finding 6 (Minimum-AIC model not selected): A — ARMA(2,2) has lower AIC than ARMA(0,0) but is never discussed or justified against
- Finding 7 (tseries vs fGarch normalization discrepancy): B — tseries::garch() uses a non-standard likelihood convention producing ~1596 vs fGarch's 1092, explaining the large gap and the "software difference" question (matches Human Issues #5 and #6)
- Finding 8 (No simulation-based POMP diagnostics): C — fitted stochastic volatility model never simulated forward for model checking
- Finding 9 (sigma_nu converges to 0): C — leverage effect effectively absent but not interpreted; boundary estimate not examined via profile likelihood
- Finding 10 (Global search box excludes high-likelihood region): C — sigma_eta MLE ~5 from local search lies outside the global search box of (0.5, 1)
- Finding 11 (Likelihood comparisons across packages not verified): C — arima(), garchFit(), and pfilter() likelihoods compared without confirming consistent normalization conventions
- Finding 12 (ARIMA vs ARMA section title): C — section called "ARIMA Model Selection" but no differencing is applied
- Finding 13 (LRT statistics not shown): C — test statistics and chi-squared p-values omitted; reader cannot verify LRT application
- Finding 14 (GARCH dismissed on p-values): C — simple GARCH(1,1) discarded based on coefficient p-values rather than AIC/likelihood framework used elsewhere
- Finding 15 (Shapiro-Wilk on raw residuals): C — normality test applied to heteroskedastic raw GARCH residuals rather than standardized residuals

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "ARMA(0,0) selected without acknowledging volatility clustering — Ljung-Box on squared returns would test for ARCH effects")
- Human Issue #4: covered (matched by finding: "ADF test conclusion is inverted — reasoning is backwards, saying 'keep null of stationarity' when the null is unit root")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Invalid cross-model log-likelihood comparison in Conclusion"; also matched by finding: "Inconsistent log-likelihood values between sections")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Hard-coded local file path"; also matched by finding: "NVIDIA data file not included")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: contradiction (AI says no ESS monitoring or conditional log-likelihood plots exist; human says the project does include filter diagnostics plotting ESS and conditional likelihood, but the spike around time 340 was not discussed)
- Human Issue #14: missed

**Findings classification:**
- Major 1 (Global IF2 search anchored to local mif2 result): A — global search passes if1[[1]] instead of base pomp object, depleting cooling schedule before new starts are explored
- Major 2 (Particle filter evaluated on simulated data): A — benchmark log-likelihood computed on simulated data rather than real NVIDIA returns, making it incomparable to IF2 results
- Major 3 (Invalid cross-model log-likelihood comparison): B — models use different observation distributions so numerical LL comparison is invalid; also identifies internal GARCH/ARMA LL discrepancy (matches Human Issue #6)
- Major 4 (No profile likelihoods): A — no profile likelihoods computed for any parameter; sigma_nu at boundary and non-converging parameters not investigated via MCAP
- Major 5 (ADF test conclusion inverted): B — text says "keep the null hypothesis that our time series is stationary" when ADF null is unit root (non-stationary); reasoning is backwards (matches Human Issue #4)
- Major 6 (No benchmark comparison for POMP model): A — POMP model not compared to GARCH(1,1)-t or any other benchmark on a common footing
- Major 7 (No model diagnostics for POMP model): F — claims no ESS monitoring or conditional log-likelihood plots by time step exist; contradicts Human Issue #13, which states that the project does include filter diagnostic plots showing ESS and conditional likelihood with a visible spike at time 340
- K-period log-return formula error: C — formula for k-period return gives the 1-period return on the left-hand side
- Hard-coded local file path: D — setwd() uses machine-specific absolute path (matches Human Issue #10)
- NVIDIA data file not included: D — NVDA.csv not present in submission; document cannot be reproduced (matches Human Issue #10)
- Inconsistent log-likelihood values between sections: D — ARMA(0,0) LL reported as 1087 in ARMA section but 1092 in Conclusion (matches Human Issue #6)
- GARCH(1,1) discarded for wrong reasons: C — beta coefficient implausibly small, possibly a fitting issue with the tseries::garch() function
- Shapiro-Wilk test on residuals: C — test statistic and p-value not reported, only conclusion of non-normality stated
- ARMA(0,0) selected without acknowledging volatility clustering: D — Ljung-Box on returns alone does not rule out ARCH effects; squared-return test omitted (matches Human Issue #3)
- Missing root plot for ARMA(0,0): C — root plot is unnecessary for ARMA(0,0) since it has no AR or MA polynomials; text should clarify this
- Convergence comment overstated: C — sigma_nu stabilizing at zero is a boundary estimate with scientific implications for leverage effects, not simply a convergence report
- Missing sessionInfo() or package versions: C — no software version documentation despite substantial pomp API changes across versions

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 4 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "m3 — numerical inconsistency in reported log-likelihoods")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "m4 — ESS degeneracy near time ~300–350 not discussed")
- Human Issue #12: covered (matched by finding: "M3 — POMP measurement model uses Gaussian errors despite evidence for heavy-tailed errors")
- Human Issue #13: covered (matched by finding: "m4 — ESS degeneracy near time ~300–350 not discussed")
- Human Issue #14: missed

**Findings classification:**
- M1: A — POMP model not identified along key parameters (sigma_nu collapses, sigma_eta has extreme spread, phi fails to converge)
- M2: A — No profile likelihoods or confidence intervals for POMP parameters
- M3: B — POMP measurement model uses Gaussian errors despite GARCH section establishing heavy-tailed errors are needed (matches Human Issue #12)
- m1: C — ADF test null hypothesis direction stated backwards ("keep the null" when p < 0.01 should mean "reject the null")
- m2: C — ARMA(2,2) has better AIC than selected ARMA(0,0) but is not discussed
- m3: D — Numerical inconsistency in reported log-likelihoods across sections (matches Human Issue #6)
- m4: D — ESS degeneracy near time ~300–350 (May 2023 extreme return) not discussed (matches Human Issues #11 and #13)
- m5: C — Typographical error in k-period log-return equation
- m6: C — Forecasting stated as a goal in introduction but not attempted in analysis

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 10 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 5 | 4 | 2 |
| B (AI major, human also found) | 0 | 2 | 2 | 1 |
| C (AI minor, human missed) | 8 | 8 | 6 | 4 |
| D (AI minor, human also found) | 2 | 0 | 4 | 2 |
| E (Human found, AI missed) | 10 | 11 | 9 | 10 |
| F (Human-AI contradiction) | 1 | 0 | 1 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 2 | 10 | 2/12 = 17% | 4 | 8 | 12/14 = 86% |
| Charlie | 2 | 0 | 11 | 3/14 = 21% | 5 | 8 | 13/15 = 87% |
| Doug | 2 | 4 | 9 | 4/13 = 31% | 4 | 6 | 10/16 = 62% |
| Evan | 1 | 2 | 10 | 4/14 = 29% | 2 | 4 | 6/9 = 67% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The introduction reads like ChatGPT. The conclusion also reads like it has been edited by ChatGPT. A tell-tale sign is sweeping statements made in elaborate language which are not well supported or linked to specific results from the project. According to the rules of the course, ChatGPT is allowed but should be properly attributed as a source. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: ADF test is not designed for situations with time-varying sample variance, since neither the model used as a null hypothesis, nor the alternative model used to motivate the test statistic, have that feature. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: ARMA(0,0) here is an independent, identically distributed (iid) Gaussian model. It would be helpful to remind the reader of that. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The conclusions contain some thoughtful reasoning, but also have logical flaws. The explanation, "This aligns with the efficient market theory, emphasizing the importance of market unpredictability to prevent arbitrage opportunities," is true of stochastic volatility and GARCH as well as an iid model. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: Since GARCH is white noise (following the definition provided by the group, with white noise interpreted in the weak sense) the ARMA + GARCH model is in fact ARMA, just non-Gaussian ARMA. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #14: The authors could have benefitted by paying attention to peer review on previous similar projects for this course, e.g., https://ionides.github.io/531w22/final_project/project07/comments.html. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 6 out of 14 human issues (43%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: Ljung-Box is also of borderline relevance. The null assumes independence, whereas time-varying variance suggests a model should have a lack of independence even if it is uncorrelated — GARCH and stochastic volatility both have that property. (Covered only by Doug)
- Human Issue #4: The following sentence does not make sense: "Having verified both the stationarity and independence of the data, we can now proceed to the next stage: selecting an appropriate ARMA model." If we really want a stationary, independent model, the only possible ARMA model is ARMA(0,0). Later, the group claim that models which are not independent (e.g., GARCH and stochastic volatility) fit the data better, highlighting the flaw in the reasoning. (Covered only by Doug)
- Human Issue #5: ARMA(0,0)+GARCH seems to be indistinguishable from GARCH, since there is no ARMA component. So, is the difference only the software used to fit the model? That could use some explanation and investigation. (Covered only by Charlie)
- Human Issue #11: In the "Exploratory Data Analysis" section, authors don't explain the huge jump on 2023/05/25 and its potential influence on their model fitting. As can be seen in their data plot, the close price on 2023/05/24 is 305 and the next day close price increases to 379, which is a considerable surge. This may be the reason for low ESS in their POMP model at time 340 (roughly). In section "POMP Model - Local Search", there is a great decrease in ESS, probably suggesting a bad fit on 2023/05/25. (Covered only by Evan)
- Human Issue #12: In their GARCH analysis, they find the residuals following a t-distribution are more reasonable, but in their POMP model, they still build the model using normal distribution. (Covered only by Evan)
- Human Issue #13: In the filter diagnostics that plotted effective sample size and conditional likelihood for the last iteration of their filtering process, there is a clear spike around time 340, as well as a smaller spike around 510. It would have been useful to mention this spike, even if it turns out to be irrelevant in their modeling. Is there something of note that happens around those time points in the data? Or is this something worth adjusting the model to account for? (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 2 |
| Evan | 3 |
