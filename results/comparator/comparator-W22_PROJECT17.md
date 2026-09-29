# Comparator Analysis — W22 Project 17

---

## Human Issues

1. The conclusion that the sample ACF "indicated dependencies between the data" does not add much to the timeplot. Also, differencing is used as a way to make a stationary model more suitable, which is not quite the same thing as dependence.

2. "4 of the AR polynomial roots are inside the unit circle and one of the MA polynomial roots are inside the unit circle" does not seem to match the figure. Also, the figure shows inverse roots so they should be inside for invertibility and causality.

3. "most of the residual values stay close to the horizontal line y=0" suggesting a good fit of our model" is not a warranted conclusion. The residuals show heteroskedasticity and/or long tails, with some autocorrelation. Residuals are centered on zero by construction.

4. Probably, ARMA modeling on a log scale would fit better.

5. I(0)=270000 is a very large number of initial infected individuals. This is fixed in the code, rather than being estimated, which could cause problems with fitting other parameters.

6. The strong weekly cycle is not in the SEIR model. One could model weekly totals to avoid dealing with day-of-week effects.

7. Likelihoods are not quite comparable before and after differencing. This could explain all or some of the difference between the SARIMA and SEIR log likelihoods. Note that SEIR beats the ARMA likelihood.

8. The source of the data is unclear. The Kaggle link provided refers to something not updated since 2020-07-27. The authors say "the beginning of the pandemic in the US, 2021 June 5st" but that is not when the pandemic began. It is a reasonable date for the arrival of the delta variant, but the project makes no mention of this variant.

9. The model, with time-varying beta, made more sense in the analysis of a prior project which this project closely follows. At that time, the dynamics were driven by initial spread and social distancing interventions. More recently, variants and vaccination have been more critical.

10. There is a sign mistake in the Binomial transition probability expression which may have been inherited from a prior cited project. It is okay to borrow from cited past projects, but one should borrow critically.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "AIC-selected ARIMA(5,5) has roots outside unit circle making model non-causal and non-invertible")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Log-likelihood comparison between SARIMA and SEIR is invalid — SARIMA evaluated on differenced data, SEIR on raw series")
- Human Issue #8: covered (matched by finding: "Data source reproducibility issue — Kaggle snapshot version not specified")
- Human Issue #9: covered (matched by finding: "References to prior projects without independent validation of suitability for current data and variants")
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (S(0)=N, no recovered population): A — S initialized to full US population, ignoring prior infections and vaccination
- Finding 2 (Accumulator H conflates recoveries with new cases): A — measurement model tracks recoveries rather than incident infections
- Finding 3 (SARIMA vs. SEIR log-likelihood comparison invalid): B — SARIMA likelihood on differenced data, SEIR on raw; not directly comparable (matches Human Issue #7)
- Finding 4 (Np=100 too small in global search): A — only 100 particles for final likelihood evaluation, unreliable MLE
- Finding 5 (Convergence absent, no remediation): A — authors acknowledge non-convergence but take estimates anyway
- Finding 6 (Gap in beta time-period specification): A — 28-day window Nov 12–Dec 8 unaccounted for in stated formulas
- Finding 7 (mu_IR fixed without justification): A — recovery rate fixed at 0.1 with no reference or sensitivity analysis
- Finding 8 (SARIMA formula typographical error): C — epsilon_n appears twice on RHS; symbol p reused for seasonal and non-seasonal AR orders
- Finding 9 (High-order ARIMA(5,5) causality/invertibility issues): D — 4 AR and 1 MA roots outside unit circle; model accepted without correction (matches Human Issue #2)
- Finding 10 (Normal approximation for count data): C — normal used for case counts without justification or comparison to negative binomial
- Finding 11 (b5 inconsistency between text and code): C — text states b5=1.5, code sets b5=0.15, factor-of-10 discrepancy
- Finding 12 (Global search box for tau far from starting value): C — search box [0.2, 0.4] while initial tau=0.001
- Finding 13 (No profile likelihood or CIs for SEIR parameters): C — only point estimates reported after global search
- Finding 14 (Data source reproducibility): D — Kaggle snapshot version/date unspecified, raw CSV date range differs from stated range (matches Human Issue #8)
- Finding 15 (Prior project borrowed without independent validation): D — model structure from W21 Project 15 used without justifying suitability for different time period and variants (matches Human Issue #9)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SARIMA non-causal and non-invertible; roots inside unit circle not remediated")
- Human Issue #3: covered (matched by finding: "QQ-plot heavy tails acknowledged but not addressed")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "initial conditions violate population conservation; S+E+I > N; implausible susceptible pool including I=270,000")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "direct log-likelihood comparison between SARIMA and SEIR is invalid due to differencing")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (measurement model accumulates recoveries): A — H += dN_IR accumulates recoveries rather than new infections, causing temporal displacement
- Finding 2 (initial conditions violate population conservation): B — S+E+I > N and implausible susceptible pool (matches Human Issue #5)
- Finding 3 (no profile likelihood): A — no profile likelihoods or confidence intervals computed for any SEIR parameter
- Finding 4 (SARIMA non-causal and non-invertible): B — roots inside unit circle acknowledged but model retained without remediation (matches Human Issue #2)
- Finding 5 (invalid SARIMA–SEIR log-likelihood comparison): B — SARIMA likelihood conditions on fewer observations due to differencing (matches Human Issue #7)
- Finding 6 (rw.sd 10x below standard): A — rw.sd = 0.002 for b1–b7 instead of 0.02, hampering IF2 exploration
- Finding 7 (text–code mismatch for b5): C — b5 listed as 1.5 in text but 0.15 in code
- Finding 8 (covariate period for b5 inconsistent): C — text says 13-day b5 window but code implements 40-day window
- Finding 9 (global search uses Np=100 vs Np=1000): C — hardcoded Np=100 in global search pfilter vs Np=1000 in local search
- Finding 10 (no non-mechanistic benchmark): C — no IID or autoregressive baseline comparison for SEIR
- Finding 11 (convergence incomplete but not addressed): C — convergence failure noted but no corrective action taken
- Finding 12 (no model diagnostics for SEIR fit): C — no ESS plot, no conditional log-likelihood trace reported
- Finding 13 (find_best_local uses unreliable mif2 log-likelihood): C — mif2 internal log-likelihood used for selection despite perturbations in final iteration
- Finding 14 (mu_IR fixed without justification): C — mean recovery time fixed at 10 days with no citation or sensitivity analysis
- Finding 15 (QQ-plot non-normality not addressed): D — heavy tails in SARIMA residuals noted but no remediation attempted (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SARIMA model not invertible or causal, roots outside unit circle")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "initial conditions fixed at biologically implausible values, including I=270,000 and S=N")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no benchmark comparison — SARIMA and SEIR log-likelihoods not on compatible basis")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (global search anchored to local-search solution): A — genuine global search not performed; human did not raise this
- Finding 2 (self-acknowledged non-convergence undermines SEIR conclusions): A — non-convergence acknowledged but conclusions drawn anyway; human did not raise this
- Finding 3 (accumulator variable accumulates recoveries not new infections): A — H += dN_IR is a model misspecification; human did not raise this
- Finding 4 (measurement model normal approximation with no lower bound enforcement): A — inappropriate for overdispersed count data; human did not raise this
- Finding 5 (insufficient computational effort, Np=1000, Nmif=100): A — run_level=2 inadequate for 13-parameter model; human did not raise this
- Finding 6 (SARIMA and SEIR log-likelihoods not on compatible basis, comparison invalid): B — matches Human Issue #7
- Finding 7 (no profile likelihoods or parameter identifiability analysis): A — 11 free parameters with no profiles; human did not raise this
- Finding 8 (initial conditions fixed at biologically implausible values): B — matches Human Issue #5
- Finding 9 (SARIMA model not invertible or causal, roots outside unit circle): D — matches Human Issue #2
- Finding 10 (AIC table via two sequential searches, not joint): C — sequential ARIMA then SARIMA selection; human did not raise this
- Finding 11 (covariate coding gap November 12 to December 8, 2021): C — unassigned period in piecewise table; human did not raise this
- Finding 12 (global search evaluation uses Np=100 inconsistent with local search Np=1000): C — inconsistent particle count across evaluations; human did not raise this
- Finding 13 (N listed twice with conflicting values in parameter table): C — proofreading error in starting points section; human did not raise this
- Finding 14 (no model diagnostics, ESS not monitored, no conditional log-likelihood plots): C — particle filter diagnostics absent; human did not raise this
- Finding 15 (no reproducibility info, no sessionInfo or package versions): C — code supplement deficiency; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Ljung-Box rejection not reconciled with adequacy claim")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "ID 22.17.6 — initial conditions implausible for mid-pandemic start")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "ID 22.17.1 — SARIMA vs SEIR likelihood comparison requires qualification")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- ID 22.17.2: A — measurement model accumulates recoveries (dN_IR) instead of new infections
- ID 22.17.3: A — SARIMA model selection contradicts the reported AIC table
- ID 22.17.6: B — initial conditions implausible (S=N, R=0) for mid-pandemic start date (matches Human Issue #5)
- ID 22.17.4: A — no profile likelihood; identifiability not assessed
- ID 22.17.7: A — incomplete convergence but strong adequacy conclusions drawn
- ID 22.17.1: B — SARIMA vs SEIR likelihood comparison invalid due to different data transformations (matches Human Issue #7)
- Np=100 for global search: C — low particle count for final likelihood evaluations
- Nm/Nreps values not stated: C — computational parameters not reported in text
- Simulation trajectories overshoot: C — trajectories reach 1.5M daily cases vs observed 800K maximum
- Ljung-Box rejection not reconciled: D — Ljung-Box strongly rejects white-noise residuals yet paper claims adequacy (matches Human Issue #3)
- Figure caption numbering errors: C — captions reference non-existent figure numbers inherited from source project
- Normal measurement model negative counts: C — Normal distribution can yield negative case counts

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 3 | 6 | 4 |
| B (AI major, human also found) | 1 | 3 | 2 | 2 |
| C (AI minor, human missed) | 5 | 8 | 6 | 5 |
| D (AI minor, human also found) | 3 | 1 | 1 | 1 |
| E (Human found, AI missed) | 6 | 6 | 7 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 3 | 6 | 4/10 = 40% | 6 | 5 | 11/15 = 73% |
| Charlie | 3 | 1 | 6 | 4/10 = 40% | 3 | 8 | 11/15 = 73% |
| Doug | 2 | 1 | 7 | 3/10 = 30% | 6 | 6 | 12/15 = 80% |
| Evan | 2 | 1 | 7 | 3/10 = 30% | 4 | 5 | 9/12 = 75% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The conclusion that the sample ACF "indicated dependencies between the data" does not add much to the timeplot. Also, differencing is used as a way to make a stationary model more suitable, which is not quite the same thing as dependence. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Probably, ARMA modeling on a log scale would fit better. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The strong weekly cycle is not in the SEIR model. One could model weekly totals to avoid dealing with day-of-week effects. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: There is a sign mistake in the Binomial transition probability expression which may have been inherited from a prior cited project. It is okay to borrow from cited past projects, but one should borrow critically. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 10 human issues (40%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #8: The source of the data is unclear. The Kaggle link provided refers to something not updated since 2020-07-27. The authors say "the beginning of the pandemic in the US, 2021 June 5st" but that is not when the pandemic began. It is a reasonable date for the arrival of the delta variant, but the project makes no mention of this variant. (Covered only by Alex)
- Human Issue #9: The model, with time-varying beta, made more sense in the analysis of a prior project which this project closely follows. At that time, the dynamics were driven by initial spread and social distancing interventions. More recently, variants and vaccination have been more critical. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 2 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
