# Ned-Clean Analysis — W22 Project 01

---

## Human Issues

1. Fig 1 caption says "Blue line" but should read "red line."
2. Notation issue: Y_n models the return R_n = log(y_n) - log(y_{n-1}) rather than the data y_n directly; clearer notation would have Y_n model y_n.
3. ARIMA models with different levels of integration (D != 0) do not have directly comparable likelihoods.
4. The ARIMA models can capture the strong weekly periodicity (people play more on weekends), but GARCH and stochastic volatility cannot unless that periodicity is incorporated; comparison is unfair without addressing this.
5. No rationale for why a stochastic leverage model is suitable for game play data; applying it seems like an exercise in running code developed for a different situation.
6. A model (and/or exploratory analysis) linking game growth to COVID incidence is missing, given the introduction discusses an interaction with COVID levels.
7. More details about the Steam platform data would help readers.
8. The decomposition into trend + noise + cycles is unsuccessful because "noise" is actually weekly periodicity; bandpass filter frequencies are not relevant to this data; goal and purpose of decomposition is not explained.
9. The choice of p=5, q=5 in GARCH(p,q) is not explained.
10. The pairs plot for the stochastic leverage model section seems sparse; the team could try logLik > max(logLik) - 40 instead of logLik > max(logLik) - 20.
11. The conclusion about divergence of mu_h and sigma_eta is wrong; the convergence box plot shows both parameters converge well.
12. In Fig 1, the grey interval described as a "95% confidence interval" is unclear; what model or method generates it?

---

## Alex

**Coverage record:**
- Human Issue #1 (Fig 1 caption blue→red): missed
- Human Issue #2 (Y_n notation): missed
- Human Issue #3 (incomparable likelihoods): covered (matched by finding: "Incomparable log-likelihoods invalidate the model comparison table")
- Human Issue #4 (weekly periodicity not in GARCH/SV): missed
- Human Issue #5 (no rationale for leverage model): covered (matched by finding: "Applying a financial leverage model to gaming data lacks justification")
- Human Issue #6 (no COVID linkage model): missed
- Human Issue #7 (Steam data details): missed
- Human Issue #8 (decomposition unsuccessful/unexplained): missed
- Human Issue #9 (GARCH p=5,q=5 unexplained): covered (matched by finding: "GARCH model label says (5,5) but only GARCH(1,1) is actually fitted")
- Human Issue #10 (pairs plot sparse): missed
- Human Issue #11 (wrong convergence conclusion): contradiction (Alex says non-convergence is real and not remedied; human says the authors' conclusion of non-convergence is wrong and the box plot shows convergence IS achieved)
- Human Issue #12 (95% CI in Fig 1 unclear): missed

**Findings classification:**
- Finding 1 [Major] — Incomparable log-likelihoods invalidate comparison: B (matches Human Issue #3)
- Finding 2 [Major] — Model named "Fixed Leverage" but implements Stochastic Leverage: A
- Finding 3 [Major] — Particle filter uses simulated data instead of real observations: A
- Finding 4 [Major] — No profile likelihood or confidence intervals for POMP parameters: A
- Finding 5 [Major] — Non-convergence acknowledged but not remedied: F (contradicts Human Issue #11; human says convergence IS achieved per box plot, Alex says it is not)
- Finding 6 [Major] — GARCH model label says (5,5) but only GARCH(1,1) fitted: B (matches Human Issue #9)
- Finding 7 [Major] — Figure number skips from 5 to 7: A
- Finding 8 [Moderate/Minor] — Applying financial leverage model to gaming data lacks justification: D (matches Human Issue #5)
- Finding 9 [Moderate/Minor] — ARIMA model selection ignores SARIMA result: C
- Finding 10 [Moderate/Minor] — Missing values never documented or handled: C
- Finding 11 [Moderate/Minor] — Legend color mismatch in simulation plot: C
- Finding 12 [Moderate/Minor] — ARIMA applied to already-demeaned series with additional differencing: C
- Finding 13 [Moderate/Minor] — Twitch viewership data collected but never used: C
- Finding 14 [Minor] — Section "Source" discloses heavy structural borrowing: C
- Finding 15 [Minor] — Equation label inconsistency R_b vs R_n: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (Fig 1 caption blue→red): missed
- Human Issue #2 (Y_n notation): missed
- Human Issue #3 (incomparable likelihoods): covered (matched by finding: "Incorrect log-likelihood adjustment for the ARIMA model distorts the summary table")
- Human Issue #4 (weekly periodicity not in GARCH/SV): missed
- Human Issue #5 (no rationale for leverage model): missed
- Human Issue #6 (no COVID linkage model): covered (matched by finding: "Research question and modeling strategy are misaligned")
- Human Issue #7 (Steam data details): missed
- Human Issue #8 (decomposition unsuccessful/unexplained): missed
- Human Issue #9 (GARCH p=5,q=5 unexplained): covered (matched by finding: "GARCH model mislabeled and log-likelihood potentially affected")
- Human Issue #10 (pairs plot sparse): missed
- Human Issue #11 (wrong convergence conclusion): contradiction (Charlie says global search non-convergence is real and conclusion is drawn from unconverged results; human says convergence IS achieved per box plot)
- Human Issue #12 (95% CI in Fig 1 unclear): missed

**Findings classification:**
- Issue 1 [Major] — Research question and modeling strategy misaligned: B (matches Human Issue #6)
- Issue 2 [Major] — Incorrect log-likelihood adjustment for ARIMA distorts table: B (matches Human Issue #3)
- Issue 3 [Major] — No profile likelihoods or confidence intervals: A
- Issue 4 [Major] — Global search convergence not achieved; conclusion drawn from non-converged results: F (contradicts Human Issue #11; human says convergence IS achieved, Charlie says it is not)
- Issue 5 [Major] — GARCH model mislabeled: B (matches Human Issue #9)
- Issue 6 [Major] — No benchmark comparison appropriate for mechanistic model: A
- Issue 7 [Major] — Unnecessary differencing of already-stationary series: A
- Issue 8 [Minor] — SARIMA comparison abandoned without full justification: C
- Issue 9 [Minor] — No simulation-based goodness-of-fit diagnostic: C
- Issue 10 [Minor] — H_0 non-convergence not adequately addressed: C
- Issue 11 [Minor] — Summary table values inconsistent with code output: C
- Issue 12 [Minor] — Causal language used without causal identification: C
- Issue 13 [Minor] — Data subsetting inconsistency: C
- Issue 14 [Minor] — Figure 5 label has typos ("noice", "circle"): C
- Issue 15 [Minor] — Local search sim1.filt vs. sim1.filt2 distinction unclear: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1 (Fig 1 caption blue→red): missed
- Human Issue #2 (Y_n notation): missed
- Human Issue #3 (incomparable likelihoods): covered (matched by finding: "Invalid cross-model log-likelihood comparison")
- Human Issue #4 (weekly periodicity not in GARCH/SV): missed
- Human Issue #5 (no rationale for leverage model): missed
- Human Issue #6 (no COVID linkage model): covered (matched by finding: "No connection between motivating question and model")
- Human Issue #7 (Steam data details): missed
- Human Issue #8 (decomposition unsuccessful/unexplained): missed
- Human Issue #9 (GARCH p=5,q=5 unexplained): covered (matched by minor finding: "GARCH model misspecification in text vs. code")
- Human Issue #10 (pairs plot sparse): missed
- Human Issue #11 (wrong convergence conclusion): contradiction (Doug says non-convergence of most parameters is real; human says convergence IS achieved per box plot)
- Human Issue #12 (95% CI in Fig 1 unclear): missed

**Findings classification:**
- Issue 1 [Major] — Invalid cross-model log-likelihood comparison: B (matches Human Issue #3)
- Issue 2 [Major] — Global IF2 search initialized from previous mif2 result: A
- Issue 3 [Major] — Non-convergence of most parameters in both searches: F (contradicts Human Issue #11; human says convergence IS achieved, Doug says it is not)
- Issue 4 [Major] — No profile likelihoods; identifiability unassessed: A
- Issue 5 [Major] — Conclusion inverts model ranking on log-likelihood: A
- Issue 6 [Major] — No benchmark comparison appropriate for mechanistic model: A
- Issue 7 [Major] — No connection between motivating question and model: B (matches Human Issue #6)
- Issue 8 [Major] — Filtering on simulated data for initial particle filter evaluation: A
- Minor: GARCH model misspecification in text vs. code: D (matches Human Issue #9)
- Minor: Seasonal ARIMA period not used in final model: C
- Minor: ARIMA log-likelihood adjustment unexplained and non-standard: C
- Minor: Initial simulation comparison uses wrong series (log_df vs log_df2): C
- Minor: No ESS monitoring: C
- Minor: Pairs plot uses log-transformed sigma_nu in global but raw in local: C
- Minor: Research question not answered (causal language): C
- Minor: Figure numbering gap: C
- Minor: Computational cost not reported: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1 (Fig 1 caption blue→red): missed
- Human Issue #2 (Y_n notation): missed
- Human Issue #3 (incomparable likelihoods): covered (matched by finding: "22.01.1 — Invalid log-likelihood comparison across model classes")
- Human Issue #4 (weekly periodicity not in GARCH/SV): missed
- Human Issue #5 (no rationale for leverage model): missed
- Human Issue #6 (no COVID linkage model): missed
- Human Issue #7 (Steam data details): missed
- Human Issue #8 (decomposition unsuccessful/unexplained): missed
- Human Issue #9 (GARCH p=5,q=5 unexplained): covered (matched by finding: "22.01.G — GARCH model name, equation, and code are inconsistent")
- Human Issue #10 (pairs plot sparse): missed
- Human Issue #11 (wrong convergence conclusion): contradiction (Evan says non-convergence is real and MLE is invalid; human says convergence IS achieved per box plot)
- Human Issue #12 (95% CI in Fig 1 unclear): missed

**Findings classification:**
- 22.01.1 [Major] — Invalid log-likelihood comparison across model classes: B (matches Human Issue #3)
- 22.01.2 [Major] — Best benchmark model not used; AIC difference misread: A
- 22.01.4 [Major] — Differencing of already-stationary series without justification: A
- 22.01.8 [Major] — Non-convergence acknowledged but MLE reported as valid: F (contradicts Human Issue #11; human says convergence IS achieved, Evan says it is not)
- 22.01.3 [Major] — sigma_nu at or near zero (parameter boundary): A
- 22.01.6 [Major] — No profile likelihoods or confidence intervals: A
- 22.01.G [Minor] — GARCH model name, equation, and code inconsistent: D (matches Human Issue #9)
- 22.01.5 [Minor] — Filtering step on simulated data not clearly labeled: C
- 22.01.M1 [Minor] — ESS not monitored during particle filtering: C
- 22.01.M2 [Minor] — Causal language without causal identification: C
- 22.01.M3 [Minor] — Title typo "Pandamic": C
- 22.01.M4 [Minor] — No sensitivity analysis for box search bounds: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 4 | 3 | 5 | 4 |
| B (AI major, human also found) | 2 | 3 | 2 | 1 |
| C (AI minor, human missed) | 7 | 8 | 8 | 5 |
| D (AI minor, human also found) | 1 | 0 | 1 | 1 |
| E (Human found, AI missed) | 8 | 8 | 8 | 9 |
| F (Human-AI contradiction) | 1 | 1 | 1 | 1 |

---

## Per-Reviewer Metrics

Recall denominator = B + D + E (F excluded).

**Alex:**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+8) = 3/11 = 0.27
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+7) / (4+2+7+1) = 11/14 = 0.79

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = (3+0) / (3+0+8) = 3/11 = 0.27
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+8) / (3+3+8+0) = 11/14 = 0.79

**Doug:**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+8) = 3/11 = 0.27
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+8) / (5+2+8+1) = 13/16 = 0.81

**Evan:**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+9) = 2/11 = 0.18
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+5) / (4+1+5+1) = 9/11 = 0.82

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (all four missed or contradicted):

- Human Issue #1: Fig 1 caption says "Blue line" but should read "red line." — missed by all 4 (4 out of 4)
- Human Issue #2: Y_n notation issue — missed by all 4 (4 out of 4)
- Human Issue #4: Weekly periodicity not captured by GARCH/SV models — missed by all 4 (4 out of 4)
- Human Issue #5: No rationale for stochastic leverage being suitable for game play — missed by Alex (missed), Charlie (missed), Doug (missed), Evan (missed) — missed by all 4 (4 out of 4)
- Human Issue #7: More details about Steam platform data needed — missed by all 4 (4 out of 4)
- Human Issue #8: Decomposition unsuccessful/unexplained — missed by all 4 (4 out of 4)
- Human Issue #10: Pairs plot for stochastic leverage section too sparse — missed by all 4 (4 out of 4)
- Human Issue #11: Wrong conclusion on convergence — contradicted by all 4 (not "missed" but universally contradicted; all reviewers agreed convergence failed, while human says it succeeded) (4 out of 4 contradictions)
- Human Issue #12: 95% CI in Fig 1 is unclear — missed by all 4 (4 out of 4)

Summary: 8 issues missed by all reviewers (Issues 1, 2, 4, 5, 7, 8, 10, 12); 1 issue contradicted by all reviewers (Issue 11).

Total consensus misses (missed + universally contradicted): 9 out of 12 human issues.

### Unique finds per reviewer

Human issues covered by exactly one reviewer (others all missed or contradicted):

- Human Issue #6 (COVID linkage): covered by Charlie (B) and Doug (B); covered by 2 reviewers, not a unique find.
- Human Issue #3 (incomparable likelihoods): covered by all four; not unique.
- Human Issue #9 (GARCH p=5,q=5): covered by all four; not unique.
- Human Issue #5 (no rationale for leverage): covered only by Alex (D). Charlie, Doug, Evan all missed it.

Unique finds:
- Alex: Human Issue #5 (no rationale for leverage model in gaming context) — 1 unique find
- Charlie: none
- Doug: none
- Evan: none

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- No profile likelihoods / confidence intervals for POMP parameters: raised as Major by Alex (Finding 4), Charlie (Issue 3), Doug (Issue 4), Evan (22.01.6) — all 4 reviewers, human missed. (4 out of 4)

Issues raised by at least 3 reviewers as Major that the human missed:
- Non-convergence acknowledged but not remedied (as a methodological failure requiring action): raised as Major by Alex, Charlie, Doug, Evan — but this is the contradiction item (Human Issue 11), so it is classified F, not A.
- No connection between motivating question and model / COVID linkage missing: raised as Major by Charlie (Issue 1) and Doug (Issue 7); raised indirectly but not as Major by Alex or Evan — not universal.

Universal AI-only Major flags count: 1 (no profile likelihoods)
