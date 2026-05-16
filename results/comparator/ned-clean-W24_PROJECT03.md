# Ned-Clean Analysis — W24 Project 03

---

## Human Issues

1. The project is very similar to 531w21 project 15 and does not give full credit to the intellectual debt; much of the code and format is directly taken from that project without explanation, and this project is weaker and does not go beyond the source.
2. SARIMA seasonality: there is no particular reason to pick a SARIMA period; the report finds a period of ~4 weeks but writes equations with a period of 12 weeks.
3. The units of frequency on the periodogram are not specified but seem to be cycles per year, not per week; the peak corresponds to low-frequency behavior that might be modeled as trend.
4. The root plot shows some roots of the fitted ARMA are very close to the unit circle.
5. The AIC table shows some failures in maximization that are not pointed out, and the chosen model SARMA(1,0,5)x(1,0,1) is rather large for this situation.
6. The residual histogram is wrongly described as nearly normal; it has long tails.
7. The ARMA forecasts anticipate a new peak due to heterogeneity through time (sample variance varies considerably).
8. It may be hard to explain the waves without including the limited protection that infection with earlier strains provided against later strains (waning immunity / reinfection not modeled).
9. The time units on the time plot for the POMP model do not match dates, making it hard to see where the b_k terms switch over; the lag plot should also specify units of time.
10. The initial values of E and I are not discussed; in the code they are set to the same values used by 2024 project 15 without explanation.
11. Pay attention to units: observation times are coded in weeks, not days, so other time units must also be in weeks; mistakes arise because the project borrows from 2024 project 15 where times were in days.
12. Fixing mu_EI and mu_IR at 0.1/week (implying 10-week expected duration) is especially problematic given the unit mistake.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by Finding #10 — SARIMA B^12 vs period=4 notation inconsistency)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by Finding #1 — rate units mismatch, mu described as per-day applied with weekly delta.t)
- Human Issue #12: covered (matched by Finding #1 — same finding: fixing mu_EI=mu_IR=0.1 implies 10-week durations)

**Findings classification:**
- Finding #1 [Major] Rate units mismatch: B — mu_EI and mu_IR described as per-day applied with delta.t=1 week implies 10-week durations (matches Human Issues #11 and #12)
- Finding #2 [Major] Biologically implausible initial susceptible fraction eta (~3–9%): A — human did not raise eta implausibility (human raised E/I initial values, a distinct concern)
- Finding #3 [Major] Global Search 1 worse than local search — unexplained: A — human did not raise convergence issues
- Finding #4 [Major] Profile CI based on only 3 points above cutoff: A — human did not raise this
- Finding #5 [Major] Profile not anchored to globally-optimized parameter region: A — human did not raise this
- Finding #6 [Major] Simulation uses manually chosen parameters, not the MLE: A — human did not raise this
- Finding #7 [Major] b4 highly unstable / unidentified: A — human did not raise this
- Finding #8 [Moderate] SEIR covers only 46.8% of data, misses largest outbreaks: C — human did not raise data truncation asymmetry (human #8 is about waning immunity, a different concern)
- Finding #9 [Moderate] ARMA and SEIR never formally compared: C — human did not raise this
- Finding #10 [Moderate] SARIMA B^12 vs period=4 notation inconsistency: D — matches Human Issue #2
- Finding #11 [Moderate] Non-convergence in local search not addressed before proceeding: C — human did not raise this
- Finding #12 [Moderate] tau dramatically larger in best estimates than initial guess: C — human did not raise this
- Finding #13 [Minor] "Not Based on Local Search" label misleading: C — human did not raise this
- Finding #14 [Minor] Low particle count for likelihood evaluation in global searches: C — human did not raise this
- Finding #15 [Minor] Weekly subsampling imprecise (every 7th row vs. weekly aggregate): C — human did not raise this

Note: Alex uses three severity tiers (Major, Moderate, Minor). Moderate findings are treated as Minor (not Major) for A/B vs C/D classification, since the reviewer explicitly ranked them below Major.

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor/moderate, human missed) | 7 |
| D (AI minor/moderate, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

B+D+E = 2+1+9 = 12 (equals total human issues)

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by Minor Issue #9 — SARIMA equation uses B^12 but code implements period=4)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by Major Issue #8 — fixed initial conditions E=100, I=200 with no sensitivity analysis or justification)
- Human Issue #11: covered (matched by Major Issue #1 — unit inconsistency in mu_EI and mu_IR, per-day rates applied with weekly time step)
- Human Issue #12: covered (matched by Major Issue #1 — same finding: fixing mu=0.1 with weekly delta.t implies 70-day durations)

**Findings classification:**
- Major Issue #1: B — unit inconsistency in fixed epidemiological parameters (matches Human Issues #11 and #12)
- Major Issue #2: A — no benchmark comparison between ARMA and SEIR
- Major Issue #3: A — pervasive convergence failure across global searches
- Major Issue #4: A — global search box excludes the true MLE region
- Major Issue #5: A — profile likelihood unreliable and covers only one parameter
- Major Issue #6: A — no model diagnostics (ESS, conditional log-likelihoods)
- Major Issue #7: A — data handling: subsampling instead of aggregating weekly counts
- Major Issue #8: B — fixed initial conditions E=100, I=200 with no sensitivity analysis (matches Human Issue #10)
- Minor Issue #9: D — SARIMA equation uses B^12 but code implements period=4 (matches Human Issue #2)
- Minor Issue #10: C — convergence not achieved in local search for b4, eta, tau
- Minor Issue #11: C — global search 2 misleadingly labeled as "not based on local search"
- Minor Issue #12: C — conceptual error: log-likelihood normalization misconception
- Minor Issue #13: C — auto-installing packages violates reproducibility norms
- Minor Issue #14: C — sparse quantitative reporting of SEIR fit quality
- Minor Issue #15: C — rho CI interpreted without considering model misspecification

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

B+D+E = 3+1+8 = 12 (equals total human issues)

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed (Doug's minor bullet about period=4 vs 4.3 weeks addresses a different aspect than the human's concern about B^12 vs period=4 notation and no forcing frequency justification)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by Major Issue #8 — SEIR model cannot mechanistically explain multiple epidemic waves without waning immunity)
- Human Issue #9: missed
- Human Issue #10: missed (Doug does not raise E/I initial condition values specifically)
- Human Issue #11: covered (matched by Major Issue #3 — mu_EI and mu_IR fixed with wrong unit conversion; per-day rates not converted to per-week)
- Human Issue #12: covered (matched by Major Issue #3 — same finding: fixing at 0.1/week implies 10-week durations)

**Findings classification:**
- Major Issue #1: A — global searches perform worse than local search; best MLE never identified
- Major Issue #2: A — tau severely constrained in all searches except the profile
- Major Issue #3: B — mu_EI and mu_IR fixed with wrong unit conversion (matches Human Issues #11 and #12)
- Major Issue #4: A — no benchmark comparison between SEIR and SARIMA
- Major Issue #5: A — profile CI for rho rests on only three grid points
- Major Issue #6: A — b4 and b2 unidentifiable at likelihood optimum
- Major Issue #7: A — no model diagnostics (ESS, conditional log-likelihoods)
- Major Issue #8: B — SEIR model cannot explain multiple waves without waning immunity (matches Human Issue #8)
- Minor bullet (unit error in mu initialization): D — same underlying concern as Major #3; matches Human Issues #11 and #12 (these are already covered by B above; this minor re-statement is classified D to note the minor-level mention)
- Minor bullet (auto-installing packages): C
- Minor bullet (duplicate tidyverse call): C
- Minor bullet (registerDoParallel called twice): C
- Minor bullet (global_search_2.rds naming confusion): C
- Minor bullet (rho CI interpretation questionable): C
- Minor bullet (SARIMA period 4 vs 4.3 weeks): C
- Minor bullet (no convergence traces for global searches): C
- Minor bullet (measurement model description inconsistent): C
- Minor bullet (missing pomp package version): C
- Minor bullet (no RNG seeds for second global search): C
- Minor bullet (data truncation Dec 26 not Dec 31 as stated): C

Note: Human Issues #11 and #12 are covered by Major Issue #3 (B). The minor unit-error bullet re-states the same concern; Human Issues #11 and #12 are already marked covered and are not double-counted. D=0 for purposes of human recall (no human issue is covered exclusively by a minor finding).

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 11 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

B+D+E = 3+0+9 = 12 (equals total human issues)

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by Minor 24.03.5 — SARIMA equation uses B^12 but period=4 in code)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by Major M1 — initial conditions biologically implausible: E(0)=100, I(0)=200 with Japan's first case not until Jan 16, 2020 and week 1 showing 0 cases)
- Human Issue #11: covered (matched by Major 24.03.C — mu_EI and mu_IR appear to be expressed in day^-1 but applied in a weekly time-step model)
- Human Issue #12: covered (matched by Major 24.03.C — same finding: 0.1/week implies 10-week durations, inconsistent with COVID-19 biology)

**Findings classification:**
- 24.03.A [Major] Best MLE never identified; global search results inconsistent and unexplained: A
- 24.03.B [Major] Profile CI for rho logically invalid; epidemiological conclusion unsupported: A
- 24.03.C [Major] Rate parameters mu_EI and mu_IR unit inconsistency: B — matches Human Issues #11 and #12
- 24.03.D [Major] No convergence diagnostics for global searches: A
- M1 [Major] Initial conditions biologically implausible (E=100, I=200): B — matches Human Issue #10
- 24.03.4 [Major] No quantitative benchmark comparison between ARIMA and SEIR: A
- 24.03.3 [Minor] Simulation figures show results from global search 1, not best parameters: C
- 24.03.5 [Minor] SARIMA equation uses B^12 but model uses period=4: D — matches Human Issue #2
- 24.03.13 [Minor] Key references are Wikipedia articles: C
- 24.03.14 [Minor] mu_EI and mu_IR fixed throughout; sensitivity never assessed: C
- 24.03.6 [Minor] Truncated normal measurement model not justified vs negative binomial: C
- 24.03.N1 [Minor] Ljung-Box p=0.024 confirms residual autocorrelation but no alternative models explored: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

B+D+E = 3+1+8 = 12 (equals total human issues)

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 6 | 6 | 4 |
| B (AI major, human also found) | 2 | 3 | 3 | 3 |
| C (AI minor/moderate, human missed) | 7 | 6 | 11 | 5 |
| D (AI minor/moderate, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 9 | 8 | 9 | 8 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

**Alex:**
- Human Recall = (2 + 1) / (2 + 1 + 9) = 3 / 12 = 25.0%
- AI-Unique Rate = (6 + 7) / (6 + 2 + 7 + 1) = 13 / 16 = 81.3%

**Charlie:**
- Human Recall = (3 + 1) / (3 + 1 + 8) = 4 / 12 = 33.3%
- AI-Unique Rate = (6 + 6) / (6 + 3 + 6 + 1) = 12 / 16 = 75.0%

**Doug:**
- Human Recall = (3 + 0) / (3 + 0 + 9) = 3 / 12 = 25.0%
- AI-Unique Rate = (6 + 11) / (6 + 3 + 11 + 0) = 17 / 20 = 85.0%

**Evan:**
- Human Recall = (3 + 1) / (3 + 1 + 8) = 4 / 12 = 33.3%
- AI-Unique Rate = (4 + 5) / (4 + 3 + 5 + 1) = 9 / 13 = 69.2%

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Plagiarism / intellectual debt — project very similar to W21 project 15; code and format directly taken without full credit. (4 out of 4 reviewers missed)
- Human Issue #3: Periodogram frequency units not specified; peak seems to be cycles per year, not per week; corresponds to trend-level behavior. (4 out of 4 reviewers missed)
- Human Issue #4: Root plot shows some ARMA roots very close to the unit circle. (4 out of 4 reviewers missed)
- Human Issue #5: AIC table shows failures in maximization not pointed out; chosen model SARMA(1,0,5)x(1,0,1) is rather large. (4 out of 4 reviewers missed)
- Human Issue #6: Residual histogram wrongly described as nearly normal; it has long tails. (4 out of 4 reviewers missed)
- Human Issue #7: ARMA forecasts anticipate a new peak due to heterogeneity through time; sample variance varies considerably. (4 out of 4 reviewers missed)
- Human Issue #9: Time units on POMP time plot do not match dates; lag plot should specify units of time. (4 out of 4 reviewers missed)

Count: 7 out of 12 human issues were missed by every reviewer (58.3%).

### Unique finds per reviewer

For each reviewer, human issues that only that reviewer covered and all others missed:

- **Alex:** Human Issue #8 is covered only by Doug (not Alex). Human Issue #10 is covered by Charlie and Evan (not Alex). Human Issue #2 is covered by Alex, Charlie, and Evan. Human Issues #11 and #12 are covered by all four. Alex has no unique finds (issues covered by Alex and missed by all other three): examining — #2 covered by Alex, Charlie, Evan; #11, #12 covered by all four. Unique finds = 0.

- **Charlie:** Checking issues covered by Charlie but not by Alex, Doug, or Evan. Charlie covers #2, #10, #11, #12. #2 also covered by Alex, Evan. #10 also covered by Evan. #11, #12 covered by all. Unique finds = 0.

- **Doug:** Doug covers #8, #11, #12. #8 is covered only by Doug (Alex missed, Charlie missed, Evan missed). #11, #12 covered by all four. Unique finds = 1 (Human Issue #8).

- **Evan:** Evan covers #2, #10, #11, #12. #10 is covered by Evan and Charlie (not Alex, not Doug). Not unique to Evan alone. #2 covered by Alex, Charlie, Evan. #11, #12 covered by all. Unique finds = 0.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

Examining issues in A or C categories across all four reviewers:

- **No benchmark comparison between ARIMA and SEIR:** Alex (C — Moderate #9), Charlie (A — Major #2), Doug (A — Major #4), Evan (A — Major 24.03.4). All four raised this; human did not mention it.
- **Convergence failure / global searches performing worse than local search:** Alex (A — Major #3), Charlie (A — Majors #3 and #4), Doug (A — Majors #1 and #2), Evan (A — Major 24.03.A and 24.03.D). All four raised convergence problems; human did not mention them.
- **Profile likelihood problems (sparse points, unreliable CI):** Alex (A — Majors #4 and #5), Charlie (A — Major #5), Doug (A — Major #5), Evan (A — Major 24.03.B). All four raised profile likelihood issues; human did not mention them.
- **No model diagnostics (ESS, conditional log-likelihoods):** Alex does not explicitly raise this; Charlie (A — Major #6), Doug (A — Major #7), Evan (A — Major 24.03.D). Three of four raised this (not universal).

Universal AI-only flags (all four reviewers): 3 distinct themes.
1. No quantitative benchmark comparison between ARIMA and SEIR.
2. Convergence failure: global searches perform worse than local search; search box poorly calibrated.
3. Profile likelihood unreliable: based on very few points above cutoff; CI questionable.
