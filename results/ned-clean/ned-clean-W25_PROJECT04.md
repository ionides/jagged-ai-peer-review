# Ned-Clean Analysis — W25 Project 04

---

## Human Issues

1. The introduction is brief and does not outline goals of the project or relevant background information.
2. The interpretation of ARMA residuals is poor — the residual time series shows extreme heteroskedasticity but is described as having "no clear patterns." The residual diagnostics suggest a logarithmic transformation should be considered. Residuals are also long-tailed compared to normal.
3. The roots on and close to the unit circle suggest poor stability, yet the conclusion that "the roots confirm stationarity and invertibility" is weak. Diagnostic plots are ignored.
4. The ARMA benchmark should be carried out as log-ARMA for situations where ARMA fits better on a log scale.
5. Reasoning about log-likelihood as a standalone argument for model quality is weak — log-likelihood is useful only to compare models (VAR section).
6. The Fig 5 residual plot explanation makes two incompatible points: first saying there is no pattern and then identifying one.
7. The report references a previous project but does not explain explicitly what was learned from it or what the authors' own creative innovations were.
8. It is not clear how the VAR model supports substantial conclusions.
9. Erratic use of boldface makes the text harder to read.
10. Incorrect reasoning: "ACF and PACF plots show strong autocorrelation and slow decay, indicating non-stationarity and the need for differencing." The usual motivation for sample ACF assumes a stationary model; differencing is only one way to build a non-stationary model.
11. Fig 1 needs a different scale for deceased — that line is not legible.
12. ARIMA(5,1,5) is a large model and not the model with lowest AIC. Models like ARIMA(1,1,3) or (1,1,4) are not considered.
13. VAR is described as "more transparent" and "easier to interpret" yet no useful interpretation is provided.
14. VAR diagnostics show longer than normal tails; a time plot would also reveal heteroskedasticity (not shown).
15. Authors should check whether using last week to predict this week is detectably worse (VAR fitted values).
16. Fig 4 has a typo in the time axis (runs 2024–2041).

---

## Alex

**Coverage record:**
- Human Issue #1 (brief intro): missed
- Human Issue #2 (ARMA residual interpretation / heteroskedasticity / log transform): missed
- Human Issue #3 (roots near unit circle — weak stationarity conclusion): covered (matched by Finding #12 — ARIMA(5,1,5) selected without checking near-cancellation of AR/MA roots; notes MA roots lie near unit circle and the inadequate response)
- Human Issue #4 (ARMA benchmark should be log-ARMA): missed
- Human Issue #5 (LL as standalone argument for VAR model quality): missed
- Human Issue #6 (Fig 5 residual plot — two incompatible points): missed
- Human Issue #7 (references previous project without explaining own contributions): missed
- Human Issue #8 (VAR does not support substantial conclusions): missed
- Human Issue #9 (erratic boldface): missed
- Human Issue #10 (incorrect ACF/PACF reasoning — non-stationarity and differencing): missed
- Human Issue #11 (Fig 1 scale for deceased): missed
- Human Issue #12 (ARIMA(5,1,5) not lowest AIC; simpler models not considered): missed
- Human Issue #13 (VAR claimed more transparent but no useful interpretation): missed
- Human Issue #14 (VAR diagnostics — long tails and no time plot): missed
- Human Issue #15 (VAR fitted values — check predictive edge): missed
- Human Issue #16 (Fig 4 time axis typo): missed

**Findings classification:**
- Finding #1 (R compartment missing dN_RS outflow — population not conserved): A — Critical/Major; human did not raise
- Finding #2 (H accumulates recoveries dN_IR rather than new infections): A — Major; human did not raise
- Finding #3 (Piecewise parameter notation — overlapping time intervals): A — Major; human did not raise
- Finding #4 (Profile LL for eta omits mu_IR from random walk — nuisance parameter frozen): A — Major; human did not raise
- Finding #5 (AIC/LL comparison between ARIMA and SEIRS methodologically invalid): A — Major; human did not raise
- Finding #6 (Time series objects specified with incorrect frequency): A — Major; human did not raise
- Finding #7 (VAR lag selection p=9 discards IC recommendations without justification): C — Moderate/Minor; human did not raise
- Finding #8 (VAR log-likelihood computed via approximation not matching true ML): C — Moderate/Minor; human did not raise
- Finding #9 (mu_RS fixed at 0.005 without epidemiological basis — circular justification): C — Moderate/Minor; human did not raise
- Finding #10 (Profile LL CIs computed with inconsistent filtering thresholds): C — Moderate/Minor; human did not raise
- Finding #11 (Initial I=1000 fixed without justification): C — Moderate/Minor; human did not raise
- Finding #12 (ARIMA(5,1,5) near-cancellation of AR/MA roots not checked): D — Moderate/Minor; matches Human Issue #3
- Finding #13 (Figure references internally inconsistent — chunk label offset): C — Minor; human did not raise (different from Human #16's time axis typo)
- Finding #14 (Global Search 2 not a systematic design — starts from previous profile): C — Minor; human did not raise
- Finding #15 (NegBinom parameterization uses unusual mean/variance form): C — Minor; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 15 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (brief intro): missed
- Human Issue #2 (ARMA residual interpretation / heteroskedasticity / log transform): missed
- Human Issue #3 (roots near unit circle — weak stationarity conclusion): missed
- Human Issue #4 (ARMA benchmark should be log-ARMA): missed
- Human Issue #5 (LL as standalone argument for VAR model quality): missed
- Human Issue #6 (Fig 5 residual plot — two incompatible points): missed
- Human Issue #7 (references previous project without explaining own contributions): missed
- Human Issue #8 (VAR does not support substantial conclusions): missed
- Human Issue #9 (erratic boldface): missed
- Human Issue #10 (incorrect ACF/PACF reasoning): missed
- Human Issue #11 (Fig 1 scale for deceased): missed
- Human Issue #12 (ARIMA(5,1,5) not lowest AIC; simpler models not considered): missed
- Human Issue #13 (VAR claimed more transparent but no useful interpretation): missed
- Human Issue #14 (VAR diagnostics — long tails and no time plot): missed
- Human Issue #15 (VAR fitted values — check predictive edge): missed
- Human Issue #16 (Fig 4 time axis typo): missed

**Findings classification:**
- Major 1 (Invalid LL comparison between ARIMA and SEIRS): A — Major; human did not raise
- Major 2 (Biologically implausible b3 in SEIRS Model 1): A — Major; human did not raise
- Major 3 (Profile LL for eta uses incorrect stratification variable): A — Major; human did not raise
- Major 4 (Unjustified removal of highest-LL profile result in rho2): A — Major; human did not raise
- Major 5 (No non-mechanistic benchmark on raw counts): A — Major; human did not raise
- Major 6 (Near boundary optimum not adequately explored; bimodal mu_IR): A — Major; human did not raise
- Major 7 (Initial conditions violate closed-population assumption): A — Major; human did not raise
- Major 8 (Piecewise beta notation error — overlapping time intervals): A — Major; human did not raise
- Minor: Commented-out vaccine data code in EDA section: C — Minor; human did not raise
- Minor: Figure-caption mismatch (Figure 4/5 label confusion): C — Minor; human did not raise (different from Human #16's time axis typo)
- Minor: VAR log-likelihood manually computed: C — Minor; human did not raise
- Minor: mu_RS limitation statement is ambiguous: C — Minor; human did not raise
- Minor: Profile scripts use inconsistent group-by variables (copy-paste error): C — Minor; human did not raise
- Minor: No pomp/R package version information: C — Minor; human did not raise
- Minor: Global Search 2 has half the starting points of Global Search 1: C — Minor; human did not raise
- Minor: ARIMA frequency argument inconsistent with weekly data: C — Minor; human did not raise
- Minor: No out-of-sample holdout evaluation: C — Minor; human did not raise
- Minor: b3 outside stated global search range: C — Minor; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 16 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1 (brief intro): missed
- Human Issue #2 (ARMA residual interpretation / heteroskedasticity / log transform): missed
- Human Issue #3 (roots near unit circle — weak stationarity conclusion): covered (matched by Finding #13 — ARIMA(5,1,5) near non-invertibility; notes MA roots near boundary and paper does not follow up on why ARIMA(5,1,5) is preferred despite the invertibility concern)
- Human Issue #4 (ARMA benchmark should be log-ARMA): missed
- Human Issue #5 (LL as standalone argument for VAR model quality): missed
- Human Issue #6 (Fig 5 residual plot — two incompatible points): missed
- Human Issue #7 (references previous project without explaining own contributions): missed
- Human Issue #8 (VAR does not support substantial conclusions): missed
- Human Issue #9 (erratic boldface): missed
- Human Issue #10 (incorrect ACF/PACF reasoning): missed
- Human Issue #11 (Fig 1 scale for deceased): missed
- Human Issue #12 (ARIMA(5,1,5) not lowest AIC; simpler models not considered): missed
- Human Issue #13 (VAR claimed more transparent but no useful interpretation): missed
- Human Issue #14 (VAR diagnostics — long tails and no time plot): missed
- Human Issue #15 (VAR fitted values — check predictive edge): missed
- Human Issue #16 (Fig 4 time axis typo): missed

**Findings classification:**
- Finding #1 (All profile likelihoods are pseudo-profiles — profiled parameter never fixed): A — Major; human did not raise
- Finding #2 (Profile guess stratification wrong for all profile computations): A — Major; human did not raise
- Finding #3 (Global search initialization inherits cooling schedule from local search chain): A — Major; human did not raise
- Finding #4 (H accumulates recoveries rather than new infections): A — Major; human did not raise
- Finding #5 (Invalid LL and AIC comparison between ARIMA and SEIRS): A — Major; human did not raise
- Finding #6 (mu_RS fixed at biologically implausible value, no sensitivity analysis): A — Major; human did not raise
- Finding #7 (No non-mechanistic statistical benchmark for SEIRS): A — Major; human did not raise
- Finding #8 (Piecewise interval definition — typographical error with overlapping intervals): C — Minor; human did not raise
- Finding #9 (Time series frequency set incorrectly for ARIMA analysis): C — Minor; human did not raise
- Finding #10 (rho2 profile drops highest-LL row without justification): C — Minor; human did not raise
- Finding #11 (Initial I=1000 not justified): C — Minor; human did not raise
- Finding #12 (VAR log-likelihood manually computed using approximation): C — Minor; human did not raise
- Finding #13 (ARIMA(5,1,5) near non-invertibility — parsimony ignored): D — Minor; matches Human Issue #3
- Finding #14 (Figure cross-referencing errors — caption/label numbering): C — Minor; human did not raise (different from Human #16's time axis typo)
- Finding #15 (ChatGPT use disclosure lacks specificity): C — Minor; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 15 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (brief intro): missed
- Human Issue #2 (ARMA residual interpretation / heteroskedasticity / log transform): missed
- Human Issue #3 (roots near unit circle — weak stationarity conclusion): missed
- Human Issue #4 (ARMA benchmark should be log-ARMA): missed
- Human Issue #5 (LL as standalone argument for VAR model quality): missed
- Human Issue #6 (Fig 5 residual plot — two incompatible points): missed
- Human Issue #7 (references previous project without explaining own contributions): missed
- Human Issue #8 (VAR does not support substantial conclusions): missed
- Human Issue #9 (erratic boldface): missed
- Human Issue #10 (incorrect ACF/PACF reasoning): missed
- Human Issue #11 (Fig 1 scale for deceased): missed
- Human Issue #12 (ARIMA(5,1,5) not lowest AIC; simpler models not considered): missed
- Human Issue #13 (VAR claimed more transparent but no useful interpretation): missed
- Human Issue #14 (VAR diagnostics — long tails and no time plot): missed
- Human Issue #15 (VAR fitted values — check predictive edge): missed
- Human Issue #16 (Fig 4 time axis typo): missed

**Findings classification:**
- C1 (AIC comparison ARIMA vs SEIRS requires qualification): A — Major; human did not raise
- C2 (Phase boundary overlap — model specification ill-defined): A — Major; human did not raise
- C3 (Global search convergence diagnostics absent): A — Major; human did not raise
- C4 (ESS not shown for final fitted parameter estimates): A — Major; human did not raise
- C5 (Final LL values not confirmed as replicated pfilter estimates): A — Major; human did not raise
- C6 (mu_RS fixed without sensitivity analysis): A — Major; human did not raise
- C7 (Near-zero b3 in Model 1 contradicts third-wave mechanistic attribution): A — Major; human did not raise
- C8 (Profile likelihoods missing for b3, rho_3 in Model 2, and mu_EI): C — Minor; human did not raise
- C9 (NegBinom parameterization should be clarified): C — Minor; human did not raise
- C10 (Initial compartment allocations E0, I0, R0 not stated): C — Minor; human did not raise
- MS3 (Global search range for b3 inconsistent with best result): C — Minor; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 16 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 8 | 7 | 7 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 8 | 10 | 8 | 4 |
| D (AI minor, human also found) | 1 | 0 | 1 | 0 |
| E (Human found, AI missed) | 15 | 16 | 15 | 16 |

---

## Per-Reviewer Metrics

- **Human Recall** = (B + D) / (B + D + E)
- **AI-Unique Rate** = (A + C) / (A + B + C + D)

| Reviewer | B+D | B+D+E | Human Recall | A+C | A+B+C+D | AI-Unique Rate |
|----------|----:|------:|-------------:|----:|--------:|---------------:|
| Alex | 1 | 16 | 6.3% | 14 | 15 | 93.3% |
| Charlie | 0 | 16 | 0.0% | 18 | 18 | 100.0% |
| Doug | 1 | 16 | 6.3% | 15 | 16 | 93.8% |
| Evan | 0 | 16 | 0.0% | 11 | 11 | 100.0% |

---

## Cross-Reviewer Aggregation

### Consensus Misses

Human issues that every reviewer failed to cover (missed by Alex, Charlie, Doug, and Evan):

1. The introduction is brief and does not outline goals of the project or relevant background information.
2. The interpretation of ARMA residuals is poor — extreme heteroskedasticity described as "no clear patterns"; log transformation not considered; long-tailed residuals.
4. The ARMA benchmark should be carried out as log-ARMA for situations where ARMA fits better on a log scale.
5. Reasoning about log-likelihood as a standalone argument for model quality is weak (VAR section).
6. The Fig 5 residual plot explanation makes two incompatible points.
7. The report references a previous project but does not explain what was learned or what the authors' own innovations were.
8. It is not clear how the VAR model supports substantial conclusions.
9. Erratic use of boldface makes the text harder to read.
10. Incorrect reasoning about ACF/PACF, non-stationarity, and the need for differencing.
11. Fig 1 needs a different scale for deceased — that line is not legible.
12. ARIMA(5,1,5) is a large model and not the model with lowest AIC; simpler models not considered.
13. VAR is described as more transparent and easier to interpret yet no useful interpretation is provided.
14. VAR diagnostics show longer than normal tails; no time plot shown.
15. Authors should check whether using last week to predict this week is detectably worse.
16. Fig 4 has a typo in the time axis (runs 2024–2041).

**Count: 15 out of 16 human issues were missed by all four reviewers.**

(Human Issue #3 — roots near unit circle and weak stationarity conclusion — was covered by Alex and Doug, but missed by Charlie and Evan.)

### Unique Finds Per Reviewer

Human issues covered by only one reviewer and missed by all others:

- Human Issue #3 (roots near unit circle): covered by Alex and Doug — not a unique find for either one alone.

No human issue was covered uniquely by exactly one reviewer.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-Only Flags

Issues raised as Major by every reviewer that the human did not mention:

The following Major AI findings appear across all four reviewers:

- **Invalid log-likelihood / AIC comparison between ARIMA and SEIRS models** (raised as Major by Alex [Finding #5], Charlie [Major 1], Doug [Finding #5], Evan [C1])
- **mu_RS fixed at biologically implausible value without sensitivity analysis** (raised as Major by Alex [Finding #9 — Moderate], Charlie [implicit in minor], Doug [Finding #6], Evan [C6])

Note: The LL comparison issue is universal across all four reviewers. The mu_RS issue is universal for Doug and Evan as Major; Alex rates it Moderate and Charlie rates it Minor. Adjusting for strict Major-only universality:

**Strictly universal AI Major flags (all four reviewers raise as their own Major):**
- Invalid log-likelihood/AIC comparison between ARIMA and SEIRS models: raised explicitly as Major by Charlie, Doug, and Evan; rated as a Major finding (AIC comparison) by Alex as well (Finding #5). **Count: 1 universal AI-only major flag.**

Additional near-universal AI flags (3 of 4 reviewers, not the human):
- H accumulates recoveries instead of new infections (Alex, Charlie [implicit in model spec], Doug — not in Evan as named finding)
- No non-mechanistic benchmark on raw counts (Charlie, Doug — not Alex or Evan as explicit major)
