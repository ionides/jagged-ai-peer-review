# Comparator Analysis — W22 Project 19

---

## Human Issues

1. If you want to difference the data, 7-day differencing would remove the weekly periodicity. One could sum up cases over each week as another way to avoid dealing with day-of-week effects. This is simpler than the idea proposed in the conclusion of explicitly modeling day of week as a covariate.

2. Shapiro-Wilk test does not add much to the QQ plot here. The QQ plot tells you the nature of the non-normality (long tails both ends) which Shapiro-Wilk does not.

3. You reject the null hypothesis that the postulated model is reasonable, and then say "therefore, the model can be represented by ..." which is not a clear conclusion.

4. It could be worth estimating E(t_0) and/or I(t_0) rather than fixing them. The model seems to struggle at the start of the wave.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "7-day periodicity not incorporated into either model")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "hard-coded, unjustified initial conditions for E and I")

**Findings classification:**
- Finding 1 [Major — unfair log-likelihood comparison between ARIMA and SEIR]: A — raw log-likelihood comparison across models with different observational assumptions
- Finding 2 [Major — data subsetting inconsistency, title says March 31 but code filters to February 28]: A — ARIMA and SEIR fit to different time spans
- Finding 3 [Major — hard-coded E and I initial conditions]: B — E=6000 and I=15000 fixed, not estimated (matches Human Issue #4)
- Finding 4 [Major — mu_EI and mu_IR fixed without adequate justification]: A — fixed transition rates narrow uncertainty without justification
- Finding 5 [Major — profile likelihood for tau unreliable]: A — only two points above threshold, CI misreported as percentages
- Finding 6 [Major — global search finds beta2 < beta1, contradicting epidemiological motivation]: A — result contradicts stated biological rationale without resolution
- Finding 7 [Major — inadequate particle count and iteration count]: A — NP=1000 with unconverged local search
- Finding 8 [Moderate — ARIMA(4,1,4) selected despite near-cancellation of AR and MA roots]: C — near-unit-circle and nearly coincident roots signal lower effective order
- Finding 9 [Moderate — Shapiro-Wilk test rejection not acted upon]: C — SW result ignored, no transformation or alternative model considered
- Finding 10 [Moderate — 7-day periodicity not incorporated into either model]: D — weekly seasonal cycle unaddressed in both ARIMA and SEIR (matches Human Issue #1)
- Finding 11 [Moderate — covariate intervention split at day 17 fixed and not estimated]: C — transition date treated as known, no sensitivity analysis
- Finding 12 [Moderate — profile likelihood performed for tau only]: C — no profiles shown for beta1, beta2, rho, or eta
- Finding 13 [Minor — measurement model equation self-referential with notation error]: C — left-hand side H and distributional mean H_n are circular
- Finding 14 [Minor — ARIMA AIC table not fully visible in rendered output]: C — parsimony claim for ARIMA(4,1,4) unverifiable from output
- Finding 15 [Minor — acknowledgements note structural similarity to prior projects without methodological citation]: C — SEIR template not credited

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Initial conditions E = 6000 and I = 15000 fixed without justification or sensitivity analysis")

**Findings classification:**
- Finding 1 (Accumvar H never reset — structural bug): A — accumvar H is cumulative, invalidating all likelihoods
- Finding 2 (μ_EI and μ_IR fixed, not estimated): A — epidemiological transition rates fixed without identifiability assessment
- Finding 3 (Profile likelihood for τ has only two points above Wilks threshold): A — confidence interval for τ unreliable
- Finding 4 (Global search β₂ < β₁ at MLE contradicts model motivation): A — finding contradicts stated model motivation, not adequately addressed
- Finding 5 (ARIMA and SEIR log-likelihoods compared across different observation models): A — likelihoods for differenced vs. level observations are not comparable
- Finding 6 (Missing convergence diagnostics for global search): A — no evidence MLE was reached
- Finding 7 (rw.sd settings inconsistent with parameter transformations): C — τ perturbation substantially smaller than course standard
- Finding 8 (Spectral analysis misidentifies dominant period): C — code takes spectrum maximum without verifying actual frequency value
- Finding 9 (Initial conditions E = 6000 and I = 15000 fixed without justification): D — fixed initial infected compartments without estimation or sensitivity analysis (matches Human Issue #4)
- Finding 10 (Measurement model notation ambiguity — H reused): C — notation conflates latent accumulator and measurement variable
- Finding 11 (ARIMA(4,1,4) mechanical selection, near-cancelling roots unresolved): C — near-cancelling AR-MA roots indicate redundancy not addressed
- Finding 12 (Residual non-normality noted but not acted upon): C — no transformation or alternative model attempted
- Finding 13 (No non-mechanistic benchmark comparison for SEIR model): C — IID baseline log-likelihood not provided
- Finding 14 (Profile likelihood starting points drawn by rounding τ — non-uniform grid): C — grid determined by global search placement rather than pre-specified
- Finding 15 (Data subsetting inconsistency — end date differs between text and code): C — ARIMA and SEIR may be fitted to different data windows

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Residual normality rejected but conclusion unclear — Shapiro-Wilk rejects normality but conclusion states ARIMA fits well")
- Human Issue #4: covered (matched by finding: "Fixed and biologically unmotivated initial conditions for E and I")

**Findings classification:**
- Major 1 (Invalid log-likelihood comparison: different datasets and observation models): A — two models compared on different-length datasets with different observation models
- Major 2 (Accumulator variable tracks wrong epidemiological event): A — H accumulates dN_IR (recoveries) instead of dN_EI (new infections)
- Major 3 (Global search inherits cooling schedule from local search): A — mifs_local[[1]] passed as base object causes cooling to be near zero at global search start
- Major 4 (Profile likelihood neither globally seeded nor valid, 20-unit gap): A — profile maximum is 20.4 log-likelihood units below global MLE, making CI uninformative
- Major 5 (Profile CI displayed with incorrect units): A — tau values multiplied by 100 and displayed as percentages
- Major 6 (No valid benchmark comparison): A — ARIMA comparison invalidated by data-length and observation-model mismatches
- Major 7 (Fixed and biologically unmotivated initial conditions for E and I): B — E=6000 and I=15000 fixed without justification or sensitivity analysis (matches Human Issue #4)
- Major 8 (Key parameters mu_EI and mu_IR fixed without sensitivity analysis): A — wide cited ranges but no assessment of sensitivity to fixed values
- Major 9 (Global MLE contradicts key biological claim, not adequately addressed): A — beta2 < beta1 at global MLE contradicts Omicron being more contagious
- Minor: ARIMA model selection criterion: C — ARIMA(4,1,4) overparameterized with inverse roots near unit circle
- Minor: Residual normality rejected but conclusion unclear: D — Shapiro-Wilk rejects normality but conclusion states ARIMA fits well (matches Human Issue #3)
- Minor: Data description inconsistency: C — introduction says 121 days but EDA/ARIMA silently uses 90-day subset
- Minor: Profile starts stratified correctly but IF2 base object is wrong: C — group_by(cut=round(tau,2)) correct but mifs_local[[1]] base object renders profile invalid
- Minor: Measurement model notation inconsistency: C — subscript H_n reused on both sides of distributional statement
- Minor: No model diagnostics beyond visual fit: C — no conditional log-likelihood plots, ESS traces, or residual diagnostics for SEIR model
- Minor: No forecast methodology: C — no forecasting beyond observed period
- Minor: Computation level: C — NP=1000/NMIF=100 insufficient given 20-unit gap and initialization error

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.19.m3 — Shapiro-Wilk test redundant after QQ plot already shows non-normality")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "22.19.m1 — Initial conditions E=6000 and I=15000 hard-coded, not estimated")

**Findings classification:**
- 22.19.M1: A — ARIMA vs. SEIR log-likelihood comparison not scale-valid
- 22.19.M2: A — Profile likelihood for tau too sparse to yield valid CI
- 22.19.M3: A — Beta2 severely unstable across runs, consistent with non-identifiability
- 22.19.M4: A — Computational parameters NP, NMIF_S, NMIF_L never reported in manuscript
- 22.19.M5: A — No standard POMP diagnostics (ESS, conditional log-likelihoods) presented
- 22.19.M6: A — mu_EI and mu_IR fixed throughout with no sensitivity analysis
- 22.19.m1: D — Initial conditions E and I hard-coded, not estimated (matches Human Issue #4)
- 22.19.m2: C — Biological interpretation of Omicron contagiousness unsupported by unstable beta2
- 22.19.m3: D — Shapiro-Wilk test redundant after QQ plot shows non-normality (matches Human Issue #2)
- 22.19.m4: C — 90-day spectral peak misidentified as cyclic period rather than trend artifact
- 22.19.m5: C — All figures lack captions
- 22.19.m6: C — ARIMA(4,1,4) near-canceling roots suggest over-parameterization

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 6 | 8 | 6 |
| B (AI major, human also found) | 1 | 0 | 1 | 0 |
| C (AI minor, human missed) | 7 | 8 | 7 | 4 |
| D (AI minor, human also found) | 1 | 1 | 1 | 2 |
| E (Human found, AI missed) | 2 | 3 | 2 | 2 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 2 | 2/4 = 50% | 6 | 7 | 13/15 = 87% |
| Charlie | 0 | 1 | 3 | 1/4 = 25% | 6 | 8 | 14/15 = 93% |
| Doug | 1 | 1 | 2 | 2/4 = 50% | 8 | 7 | 15/17 = 88% |
| Evan | 0 | 2 | 2 | 2/4 = 50% | 6 | 4 | 10/12 = 83% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

(none)

Total consensus misses: 0 out of 4 human issues (0%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: If you want to difference the data, 7-day differencing would remove the weekly periodicity. One could sum up cases over each week as another way to avoid dealing with day-of-week effects. This is simpler than the idea proposed in the conclusion of explicitly modeling day of week as a covariate. (Covered only by Alex)
- Human Issue #2: Shapiro-Wilk test does not add much to the QQ plot here. The QQ plot tells you the nature of the non-normality (long tails both ends) which Shapiro-Wilk does not. (Covered only by Evan)
- Human Issue #3: You reject the null hypothesis that the postulated model is reasonable, and then say "therefore, the model can be represented by ..." which is not a clear conclusion. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 1 |
