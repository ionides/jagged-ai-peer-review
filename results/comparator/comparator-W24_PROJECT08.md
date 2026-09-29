# Comparator Analysis — W24 Project 08

---

## Human Issues

1. ARMA modeling would be more successful on the log scale.

2. The residual plot for ARMA shows dramatic heteroskedasticity. When the authors say "We can observe certain stationarity and good fit for this model," they are failing to see the information in the plot.

3. Early figures are numbered, but later figures are missing numbers and captions.

4. Reviewers did not find much to criticise with this project. It only has small novelty relative to previous class projects, but combining a bit of novelty with careful technique meets the requirements of a strong course project.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ARIMA(3,1,3) selected despite non-normal residuals — suggests log transformation as remedy")
- Human Issue #2: covered (matched by finding: "ARIMA(3,1,3) selected despite non-normal residuals — heavy-tailed residuals, no diagnostic follow-up, authors do not investigate")
- Human Issue #3: missed
- Human Issue #4: contradiction (AI says critical data-contamination bug and multiple MAJOR code errors substantially undermine validity; human says little to criticize, careful technique meets requirements of a strong course project)

**Findings classification:**
- Finding 1 (MAJOR: SEIR section fitted to Washtenaw County data instead of King County): F — contradicts Human Issue #4 (human says careful technique/good project; AI identifies critical data-contamination bug invalidating reported results)
- Finding 2 (MAJOR: SVEIPR has strictly worse log-likelihood than SEIR with no discussion): A — no corresponding human issue
- Finding 3 (MAJOR: Double differencing in ARIMA section): A — no corresponding human issue
- Finding 4 (MAJOR: Bug in SVEIPR reinfection transition — wrong compartment): A — no corresponding human issue
- Finding 5 (MAJOR: Euler step size too coarse in SVEIPR): A — no corresponding human issue
- Finding 6 (MAJOR: SVEIPR log-likelihood comparison internally inconsistent): A — no corresponding human issue
- Finding 7 (MODERATE: Observation accumulator H only counts symptomatic transitions): C — no corresponding human issue
- Finding 8 (MODERATE: Vaccine uptake multiplier c4 takes epidemiologically implausible values): C — no corresponding human issue
- Finding 9 (MODERATE: SEIR poorly identified — extreme parameter values in global search): C — no corresponding human issue
- Finding 10 (MODERATE: Claimed profile likelihood CIs are not actually computed): C — no corresponding human issue
- Finding 11 (MODERATE: SVEIPR local search does not estimate several key parameters): C — no corresponding human issue
- Finding 12 (MODERATE: ARIMA(3,1,3) selected despite non-normal residuals, no diagnostic follow-up): D — matches Human Issues #1 and #2
- Finding 13 (MINOR: SEIR reported log-likelihood value inconsistent with stored data): C — no corresponding human issue
- Finding 14 (MINOR: SVEIPR initial conditions fixed at implausibly large values): C — no corresponding human issue
- Finding 15 (MINOR: Bibliography contains duplicate entries and an irrelevant citation): C — no corresponding human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "QQ-plot shows severe tail deviation; log transformation not explored")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: contradiction (Charlie says major revision required with multiple critical bugs; human says little to criticize and the project meets requirements for a strong course project)

**Findings classification:**
- Major 1 (wrong county data in SEIR): A — SEIR section silently uses Washtenaw County data instead of King County, invalidating all SEIR results
- Major 2 (conservation violation in SVEIPR): A — reinfection transition draws from wrong compartment (I instead of R) and R is never decremented, causing artificial population growth
- Major 3 (no profile likelihoods): A — neither SEIR nor SVEIPR computes profile likelihood curves; only an informal "poor man's profile" is used
- Major 4 (over-differencing in ARIMA): A — data already consists of first differences but ARIMA is fit with d=1, effectively fitting to second differences
- Minor 1 (vaccination rate non-standard): C — SVEIPR vaccination rate is proportional to prevalence, which is epidemiologically non-standard and unjustified
- Minor 2 (global search bounds exceeded): C — best SVEIPR parameters b7=16.2 and b8=18.7 exceed the stated upper design bounds of 15.0 without explanation
- Minor 3 (dmeas/rmeas inconsistency): C — rmeas clamps negative counts to 0 but dmeas does not account for this clamping, creating an inconsistency between simulator and evaluator
- Minor 4 (SEIR convergence with wrong county): C — claim that SEIR local search converges is moot since the analysis uses wrong-county data
- Minor 5 (fixed parameters not estimated): C — several key SVEIPR rate parameters are fixed without justification against independent clinical evidence
- Minor 6 (ARIMA log-likelihood not reported): C — only AIC is reported for ARIMA; the log-likelihood is not extracted, preventing informal cross-model comparison
- Minor 7 (poor man's profile CIs inadequate): C — marginal scatter-plot ranges used as CIs depend on starting-point distribution rather than the Wilks 95% threshold
- Minor 8 (initial conditions not justified): C — SVEIPR initialized at E=1000, I=500, P=500 without justification or sensitivity analysis
- Minor 9 (QQ-plot tail deviation / log transformation): D — QQ-plot of ARIMA residuals shows severe tail deviation; log transformation not explored (matches Human Issue #1)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: contradiction (AI identifies 8 major issues including a fundamental data-validity failure — SEIR fitted on wrong dataset — directly contradicting the human's assessment of "careful technique" and "not much to criticise")

**Findings classification:**
- Finding 1 (SEIR fitted on wrong dataset): F — directly contradicts Human Issue #4's claim of "careful technique / strong course project" (constitutes a fundamental validity failure)
- Finding 2 (SVEIPR global search anti-pattern): A — SVEIPR global search inherits exhausted cooling schedule from prior IF2 run, preventing true global exploration
- Finding 3 (SVEIPR worse likelihood than SEIR): A — SVEIPR loglik ~182 units worse than SEIR despite far greater complexity, not acknowledged by authors
- Finding 4 (coding error dN_RS drawn from I instead of R): A — reinfection transition uses wrong compartment, R never decremented, mass not conserved
- Finding 5 (no benchmark comparison): A — ARIMA model never compared quantitatively to POMP models
- Finding 6 (parameter identifiability crisis): A — c4, b7, b8 and related multipliers range over orders of magnitude near MLE, no profile likelihoods computed
- Finding 7 (H accumulator excludes P→R): A — accumulator only tracks I→R transitions, omitting P→R contribution, inconsistent with stated purpose of P compartment
- Finding 8 (SEIR global search 67/100 runs return NA): A — severe particle degeneracy unreported, false impression of global search coverage
- Finding 9 (ARIMA applied to already-differenced data, double-differencing): C — data differenced in preprocessing then ARIMA(3,1,3) differences again; model order interpretation confused throughout
- Finding 10 (SVEIPR Gaussian approximation measurement model): C — normal approximation used without justification; inconsistent with SEIR's negative binomial measurement model
- Finding 11 (high loglik SEs in SEIR local search): C — loglik SE up to 10.69, mean 3.94, indicating insufficient particles; not reported in text
- Finding 12 (key parameters fixed without justification in SVEIPR): C — mu_PR, mu_IR, mu_RS, alpha fixed at initial guesses with no biological references or sensitivity analysis
- Finding 13 (poor man's profile likelihood instead of proper profile): C — CI from range of high-loglik runs is not a valid profile likelihood; no formal coverage guarantee
- Finding 14 (lack of model diagnostics): C — no conditional log-likelihood plots over time, no formal ESS monitoring from best-fit parameters
- Finding 15 (no forecast despite stated goal): C — introduction promises predictions and policy recommendations; paper contains neither

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: misc-1 — "Figures 19-21 lack axis labels and captions")
- Human Issue #4: contradiction (AI Overall Assessment explicitly says the work "is undermined by a critical bug" and raises seven major issues; human says "did not find much to criticise")

**Findings classification:**
- 24.08.1: A — critical bug in reinfection (R→S) Csnippet draws from I instead of R
- 24.08.2: A — SVEIPR log-likelihood ~183 units worse than SEIR, unexplained
- 24.08.3: A — seven parameters fixed at ad hoc values without justification
- 24.08.5: A — profile likelihood CIs lack stated threshold and formal meaning
- 24.08.6: A — Gaussian measurement model used in SVEIPR without justification
- 24.08.7: A — data differencing pipeline confusion; possible double-differencing in ARIMA
- 24.08.8: A — biologically implausible mu_IR = 5.33/week (~1.3 day infectious period)
- 24.08.9: C — convergence described as "successful" despite many chains collapsing
- 24.08.4: C — ARIMA and POMP log-likelihoods not comparable across data transformations
- 24.08.13: C — run_level variable undocumented in rendered output
- misc-1: D — Figures 19-21 lack axis labels and captions (matches Human Issue #3)
- misc-2: C — SVEIPR initial conditions (E=1000, I=500, P=500) implausible for Jan 2020
- Overall Assessment: F — AI says work is undermined by a critical bug and multiple major gaps; human says not much to criticise (contradicts Human Issue #4)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 4 | 7 | 7 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 8 | 8 | 7 | 4 |
| D (AI minor, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 1 | 2 | 3 | 2 |
| F (Human-AI contradiction) | 1 | 1 | 1 | 1 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 1 | 1 | 2/3 = 67% | 5 | 8 | 13/14 = 93% |
| Charlie | 0 | 1 | 2 | 1/3 = 33% | 4 | 8 | 12/13 = 92% |
| Doug | 0 | 0 | 3 | 0/3 = 0% | 7 | 7 | 14/14 = 100% |
| Evan | 0 | 1 | 2 | 1/3 = 33% | 7 | 4 | 11/12 = 92% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

(none)

Total consensus misses: 0 out of 4 human issues (0%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: The residual plot for ARMA shows dramatic heteroskedasticity. When the authors say "We can observe certain stationarity and good fit for this model," they are failing to see the information in the plot. (Covered only by Alex)
- Human Issue #3: Early figures are numbered, but later figures are missing numbers and captions. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
