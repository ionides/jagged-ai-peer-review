# Comparator Analysis — W24 Project 06

---

## Human Issues

1. The report is written as a working draft not a completed project. There is too much R code and raw output presented, and too little explanation or motivation for what is done.

2. The project has weak motivation. It seems like a very standard task, comparing two models, which has been done many times before, including in DATASCI/STATS 531.

3. In the introduction, the data source/citation and time frame of their analysis should be included. The data is from 4/15/2019 to 4/12/2024, but this is not clear unless you look at the dataset.

4. The introduction could provide definitions for volatility and log-returns in case the audience is unfamiliar with financial analyses.

5. Some of the Data section plots are not discussed.

6. "The number of significant spikes in the ACF plot is 1, hence, we can assume that the AR term has value 1. Likewise, the number of significant spikes in the PACF plot is 4. Hence, it can be inferred that the MA term is 4." Here, both the counting and the reasoning are incorrect.

7. The ADF test is not designed for situations with time-varying sample variance, since neither the model used as a null hypothesis, nor the alternative model used to motivate the test statistic, have that feature.

8. The Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test was not covered in class, so it is especially appropriate to include a full definition and citation.

9. "Data is stationary" should better be written as "data can appropriately be modeled as stationary". Stationarity is a property of models, not data.

10. garch is not well explained. The `rugarch` package returns the log-likelihood using the `likelihood()` function. The authors should have figured out that the numbers only make sense if that is how it is.

11. It is not clear what the quantity called AIC is. It is not the usual definition, minus twice the log-likelihood plus twice the number of parameters.

12. The stochastic volatility model could also have longer than Gaussian tails for the returns, and the ESS and conditional log-likelihood plots seem to confirm that. It would be interesting to look at the likelihood anomalies between the stochastic volatility model and the t-garch.

13. There is no reference to previous 531 projects. Project 6 is rather similar to project 7, which credits a 531w22 project. The 2022 project is much better done, and avoids problems such as misunderstanding of log-likelihood shared by both 2024 projects 6 and 7.

14. Numbered figures and captions would help the reader.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF/PACF interpretation is incorrect — standard ACF/PACF roles are reversed")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "log(likelihood()) output is misinterpreted — per-observation vs total log-likelihood conflated")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "log(likelihood()) output is misinterpreted — per-observation vs total log-likelihood conflated")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (Log-likelihood values not comparable across models): F — contradicts Human Issue #10 (human says rugarch's `likelihood()` returns log-likelihood; AI says it returns likelihood, not log-likelihood)
- Finding 2 (POMP global search does not explore meaningful parameter space): A — no matching human issue
- Finding 3 (Key parameters do not converge in MIF2): A — no matching human issue
- Finding 4 (Particle filter evaluated on simulated object, not real data): A — no matching human issue
- Finding 5 (ACF/PACF interpretation is incorrect): B — matches Human Issue #6
- Finding 6 (Time series frequency specification is incorrect): C — no matching human issue
- Finding 7 (POMP model description notational inconsistency): C — no matching human issue
- Finding 8 (No profile likelihood or confidence intervals for POMP parameters): C — no matching human issue
- Finding 9 (GARCH(4,1) under normal noise overfitted and not justified): C — no matching human issue
- Finding 10 (log(likelihood()) output is misinterpreted): D — matches Human Issues #10 and #13
- Finding 11 (No simulation-based model validation for POMP): C — no matching human issue
- Finding 12 (Data description vague and partially incorrect): C — no matching human issue
- Finding 13 (stew() files and caching not reproducible): C — no matching human issue
- Finding 14 (Pairs plot threshold of 300 log-likelihood units too broad): C — no matching human issue
- Finding 15 (Conclusions section understates model problems): C — no matching human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF and PACF roles reversed in preliminary model identification")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Confusion between log-likelihood and likelihood in the GARCH benchmarks")
- Human Issue #11: missed
- Human Issue #12: contradiction (AI says no ESS trace or conditional log-likelihood plots exist in the report; human says ESS and conditional log-likelihood plots seem to confirm longer tails)
- Human Issue #13: missed
- Human Issue #14: missed

**Findings classification:**
- Major 1 (global search box excludes local-search optimal region): A — global search box disjoint from parameter region identified as optimal by local search
- Major 2 (no profile likelihoods or confidence intervals): A — no profile likelihoods computed for any POMP parameter
- Major 3 (no post-fit model diagnostics, no ESS or conditional log-likelihood plots): F — contradicts Human Issue #12 (human says ESS and conditional log-likelihood plots exist and confirm longer tails; AI says no such plots are present)
- Major 4 (GARCH log-likelihood/likelihood confusion): B — rugarch `likelihood()` returns log-likelihood; authors take a second log and report it as "log likelihood" (matches Human Issue #10)
- Major 5 (ACF and PACF roles reversed): B — ACF used to infer AR order and PACF to infer MA order, reversing the standard diagnostic roles (matches Human Issue #6)
- Major 6 (sigma_eta range up to 50 not interpreted as misspecification): A — essentially unbounded parameter estimate not flagged or investigated
- Major 7 (non-convergence of mu_h and H_0 not investigated): A — non-convergence noted but treated as a computational limitation rather than a signal of model misspecification
- Minor: pairs plot threshold too permissive (300 log units): C — threshold far exceeds the Wilks 95% confidence region; no diagnostic value added
- Minor: demeaned_returns does not subtract the mean: C — variable name promises transformation that does not occur; code-text mismatch
- Minor: stated global maximum 3510 does not match printed summary output: C — text value inconsistent with rendered HTML summary maxima
- Minor: Nreps_local = 20 at run_level=3 same as run_level=2: C — not scaled up as course reference table suggests
- Minor: no AIC reported for POMP model: C — fair parsimony comparison with benchmark models requires AIC for POMP
- Minor: only one POMP model structure tried: C — no leverage-free variant tested despite four benchmark structural variants
- Minor: no README or sessionInfo: C — exact reproduction on different pomp/rugarch versions not guaranteed
- Minor: Limitations section vague with no concrete corrective steps: C — "broader parameters selection" without actionable specifics
- Minor: "Model Discription" typo: C — should be "Description"
- Minor: all five references are bare URLs or book-title strings: C — no full bibliographic information

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: contradiction (Doug says motivation is "appropriate financial time series context"; human says motivation is weak and the task is standard)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF/PACF interpretation reversed — AR/MA identification rules confused")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: contradiction (Doug says rugarch's `likelihood()` returns the likelihood and 8.1538 is the log-likelihood; human says rugarch's `likelihood()` returns the log-likelihood, so 3476.553 is the log-likelihood)
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed

**Findings classification:**
- Major Issue 1 (invalid direct log-likelihood comparison across model families): A — invalid log-likelihood comparison across ARMA, GARCH, and POMP model families due to incompatible observation models
- Major Issue 2 (non-convergence of mu_h and H_0 left unresolved): A — acknowledged non-convergence of two key parameters dropped without remediation
- Major Issue 3 (no profile likelihoods or parameter uncertainty): A — no profile likelihoods or confidence intervals; pairs plot threshold -300 too wide to be informative
- Major Issue 4 (global search initialized from if1[[1]] only): A — global box search restarts from a single prior local-search run instead of fresh starting points
- Major Issue 5 (likelihood evaluation inconsistency between sim1.filt and NADQ.filt): A — discrepancy between base objects used for initial filtering vs. mif2/likelihood evaluation not explained
- Major Issue 6 (misinterpretation of GARCH likelihood output): F — Doug says rugarch's `likelihood()` returns the likelihood (3476.553), making 8.1538 the log-likelihood; human says `likelihood()` returns the log-likelihood, so 3476.553 is the log-likelihood (contradicts Human Issue #10)
- Motivation adequate (Strengths section — "appropriate financial time series context"): F — Doug explicitly asserts motivation is appropriate; human says motivation is weak (contradicts Human Issue #2)
- Minor: typo "Model Discription": C — spelling error in section heading
- Minor: ACF/PACF interpretation reversed: D — AR order suggested by PACF and MA by ACF, not the other way around (matches Human Issue #6)
- Minor: ARMA(4,4) overfitting risk not discussed: C — high parameter count relative to simpler alternatives not addressed
- Minor: sigma_nu converges near zero (possible model misspecification): C — boundary value suggesting leverage random walk may be degenerate, not discussed
- Minor: pairs plot threshold logLik > max - 300 too wide: C — standard threshold for 95% CI is max - 1.92; -300 includes nearly all searched points
- Minor: variable naming NADQ vs. NASDAQ: C — inconsistent ticker/variable naming throughout
- Minor: references cited only as URLs: C — peer-reviewed citations should replace URL-only references
- Minor: frequency=1 for daily financial data: C — ts() call treats data as annual, not daily
- Minor: QQ-plot reference line non-standard: C — plots theoretical quantiles against themselves rather than standard reference line
- Minor: beta_n formula inconsistency between text and code: C — text uses observed Y_n; code uses latent state Y_state

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 2 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Data description is incomplete — exact date range, number of observations, and data source not stated")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF/PACF order interpretation is reversed")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Likelihood-scale confusion — rugarch `likelihood()` returns log-likelihood; applying `log()` to it yields meaningless ~8.15")
- Human Issue #11: covered (matched by finding: "GARCH and ARMA AIC tables are on different scales — per-observation vs total")
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed

**Findings classification:**
- 24.06.1: B — Likelihood-scale confusion invalidates the central model comparison; rugarch `likelihood()` returns log-likelihood but paper applies `log()` again, producing ~8.15 (matches Human Issue #10)
- 24.06.2: A — Non-convergence of mu_h and H_0 invalidates POMP likelihood as a final estimate
- 24.06.3: A — sigma_eta is severely non-identifiable in the global search
- 24.06.5: A — No profile likelihoods or confidence intervals reported for any POMP parameter
- 24.06.4: D — ACF/PACF order interpretation is reversed (ACF used for AR, PACF used for MA) (matches Human Issue #6)
- 24.06.5b: D — GARCH and ARMA AIC tables are on different scales (per-observation vs total) without noting the difference (matches Human Issue #11)
- 24.06.13: C — No forward simulation from fitted POMP model shown
- 24.06.10b: D — Data description incomplete; exact date range, observation count, and data source not stated in text (matches Human Issue #3)
- 24.06.6: C — Code export typo: `'if'` (reserved keyword) included in foreach export argument

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
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 3 | 4 | 5 | 3 |
| B (AI major, human also found) | 1 | 2 | 0 | 1 |
| C (AI minor, human missed) | 9 | 10 | 9 | 2 |
| D (AI minor, human also found) | 1 | 0 | 1 | 3 |
| E (Human found, AI missed) | 11 | 11 | 11 | 10 |
| F (Human-AI contradiction) | 1 | 1 | 2 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 11 | 3/14 = 21% | 3 | 9 | 12/14 = 86% |
| Charlie | 2 | 0 | 11 | 2/13 = 15% | 4 | 10 | 14/16 = 88% |
| Doug | 0 | 1 | 11 | 1/12 = 8% | 5 | 9 | 14/15 = 93% |
| Evan | 1 | 3 | 10 | 4/14 = 29% | 3 | 2 | 5/9 = 56% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The report is written as a working draft not a completed project. There is too much R code and raw output presented, and too little explanation or motivation for what is done. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The introduction could provide definitions for volatility and log-returns in case the audience is unfamiliar with financial analyses. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: Some of the Data section plots are not discussed. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: The ADF test is not designed for situations with time-varying sample variance, since neither the model used as a null hypothesis, nor the alternative model used to motivate the test statistic, have that feature. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test was not covered in class, so it is especially appropriate to include a full definition and citation. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: "Data is stationary" should better be written as "data can appropriately be modeled as stationary". Stationarity is a property of models, not data. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #14: Numbered figures and captions would help the reader. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 7 out of 14 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: In the introduction, the data source/citation and time frame of their analysis should be included. The data is from 4/15/2019 to 4/12/2024, but this is not clear unless you look at the dataset. (Covered only by Evan)
- Human Issue #11: It is not clear what the quantity called AIC is. It is not the usual definition, minus twice the log-likelihood plus twice the number of parameters. (Covered only by Evan)
- Human Issue #13: There is no reference to previous 531 projects. Project 6 is rather similar to project 7, which credits a 531w22 project. The 2022 project is much better done, and avoids problems such as misunderstanding of log-likelihood shared by both 2024 projects 6 and 7. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 2 |
