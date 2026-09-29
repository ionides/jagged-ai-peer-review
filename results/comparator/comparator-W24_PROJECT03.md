# Comparator Analysis — W24 Project 03

---

## Human Issues

1. The project is very similar to 531w21 project 15. It references that project once, but does not give full credit to the intellectual debt. Much of the code and the format of the report is directly taken from that project, without explanation. The model turns out to be more satisfactory for the situation of 2024 project 15. This project not only fails to go beyond the analysis of its source project, it is weaker and does not pay full credit to the source.

2. Usually, we only use seasonality in ARMA when there is a known forcing frequency (e.g., one year). Here, there is no particular reason to pick a SARIMA period. The report finds a period of about 4 weeks and then writes equations with a period of 12 weeks.

3. The units of frequency on the periodogram are not specified but seem to be cycles per year, not per week. So, the peak frequency is 0.23 per year, corresponding to low-frequency behavior that might be modeled as trend in an ARMA context.

4. The root plot shows some roots of the fitted ARMA are very close to the unit circle.

5. The AIC table shows some failures in maximization that are not pointed out: SARMA(2,0,4)×(1,0,1) to SARMA(3,0,4)×(1,0,1) and SARMA(3,0,3)×(1,0,1) to SARMA(4,0,3)×(1,0,1), for example. The model that is chosen, SARMA(1,0,5)×(1,0,1), is rather large for this situation.

6. The residual histogram is wrongly described as nearly normal. It has long tails.

7. The ARMA forecasts anticipate a new peak. That is because of heterogeneity through time — for example, the sample variance of the data varies considerably through time.

8. It may be hard to explain the waves without including the limited protection that infection with earlier strains provided against later strains.

9. The time units on the time plot for the POMP model does not match dates, so it is hard to see where the b_k terms switch over. The lag plot should also specify units of time.

10. The initial values of E and I are not discussed. In the code, they are set to the same values used by 2024 project 15, without explanation.

11. Pay attention to units. The observation times are coded in weeks, not days. So, other time units must also be in weeks for consistency. The mistakes arising here may be because the project borrows heavily from 2024 project 15, for which the observation times were coded in days.

12. Fixing μ_EI and μ_IR at 0.1/week (i.e., a 10 week expected duration) is especially problematic given the unit mistake.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SARIMA notation inconsistency: B^12 in equations but period=4 in code")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "Rate units mismatch: transition rates treated as per-week despite being described as per-day")
- Human Issue #12: covered (matched by finding: "Rate units mismatch: transition rates treated as per-week despite being described as per-day")

**Findings classification:**
- Finding 1 (Rate units mismatch): B — transition rates μ_EI and μ_IR treated as per-week but described as per-day, implying 10-week durations (matches Human Issues #11 and #12)
- Finding 2 (Implausible eta): A — initial susceptible fraction of 3–9% is biologically impossible for a novel pathogen
- Finding 3 (Global Search 1 worse than local search): A — non-monotone likelihood trajectory across searches never investigated
- Finding 4 (Profile CI from only 3 points): A — 95% CI for rho derived from only 3 filtered estimates above the chi-squared cutoff
- Finding 5 (Profile not anchored to MLE region): A — profile for rho uses local-search base model far from globally-optimized parameter region
- Finding 6 (Simulation uses manually chosen parameters): A — final simulation uses hand-picked values inconsistent with the stated MLE
- Finding 7 (Highly unstable b4): A — b4 ranges from 0.97 to 3042 across top solutions; effectively unidentified, never discussed
- Finding 8 (SEIR covers only 46.8% of data): C — model truncated at 2021, missing largest Japanese COVID waves
- Finding 9 (ARMA and SEIR never formally compared): C — no AIC/BIC comparison, no residual analysis for SEIR, no synthesis
- Finding 10 (SARIMA notation inconsistency B^12 vs period=4): D — equations use B^12 but code implements period=4 (matches Human Issue #2)
- Finding 11 (Non-convergence in local search): C — b4, eta, tau still varying at final iteration; not addressed before proceeding to global search
- Finding 12 (tau 12-fold increase never discussed): C — initial tau=0.05 grows to ~0.60 at MLE; sign of process misspecification, never interpreted
- Finding 13 (Misleading section title): C — "Not Based on Local Search" section still uses mifs_local[[1]] as base object
- Finding 14 (Low particle count): C — global searches use Np=1000 vs Np=10000 in profile; mixing precision levels
- Finding 15 (Weekly subsampling imprecise): C — every-7th-row sampling risks date misalignment with stated period start

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: contradiction (AI says peak frequency is 0.2311 week⁻¹ corresponding to a period of 4.33 weeks; human says the units seem to be cycles per year, so 0.23/year corresponds to low-frequency behavior, not a ~4-week cycle)
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "E(0) = 100 and I(0) = 200 fixed without justification or sensitivity analysis")
- Human Issue #11: covered (matched by finding: "unit inconsistency in fixed biological parameters — time unit is weeks but μ_EI and μ_IR treated as day⁻¹ values")
- Human Issue #12: covered (matched by finding: "unit inconsistency in fixed biological parameters — time unit is weeks but μ_EI and μ_IR treated as day⁻¹ values")

**Findings classification:**
- Major Issue 1 (unit inconsistency in μ_EI and μ_IR): B — time unit is weeks but rates fixed as if days, making 10-week latency/infectious periods (matches Human Issues #11 and #12)
- Major Issue 2 (no benchmark comparison): A — no non-mechanistic baseline computed or compared
- Major Issue 3 (ARMA and SEIR on different data windows): A — no quantitative cross-model comparison possible
- Major Issue 4 (profile likelihood fixes τ via rw.sd = 0.0001): A — conditional slice rather than true profile, CI for ρ untrustworthy
- Major Issue 5 (β parameters never profiled): A — central contact rate parameters b1–b4 have no profile likelihoods or confidence intervals
- Major Issue 6 (second global search worse than first, described as "not significantly better"): A — −4457.8 vs −3531.9 is a ~926 unit degradation, not comparable
- Major Issue 7 (first global search uses only 22 total mif2 iterations): A — far below course standard; best likelihood of −3531.9 not near true maximum
- Minor (ARMA on raw counts without transformation): C — right-skewed counts up to 300,000 fitted without log or square-root transform
- Minor (Ljung-Box rejects white noise; no remedial action): C — residual autocorrelation acknowledged but no revised model attempted
- Minor (SARIMA period: rounding 4.33 to 4 not discussed; no scientific basis for monthly cycle): F — Charlie states frequency is 0.2311 week⁻¹ giving 4.33-week period; human says units appear to be cycles per year so 0.23/year is low-frequency trend-like behavior (contradicts Human Issue #3)
- Minor (discretized normal measurement model without scientific motivation): C — negative binomial not considered
- Minor (E(0) = 100, I(0) = 200 fixed without justification): D — initial exposed and infectious counts arbitrary, no sensitivity analysis (matches Human Issue #10)
- Minor (simulation uses manually specified parameters not corresponding to MLE): C — b1=60, b2=0.06, b3=40, b4=600 vs reported MLE unexplained
- Minor (profile pairs plot shows "decentralized" distribution but CI reported without acknowledging tension): C — flat profile contradicts finite CI claim

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "SEIR model cannot mechanistically explain multiple epidemic waves without waning immunity")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "mu_EI and mu_IR fixed; unit conversion wrong — 0.1/week should be ~1.08/week"; also matched by finding: "Unit error in mu_EI and mu_IR initialization")
- Human Issue #12: covered (matched by finding: "mu_EI and mu_IR fixed; unit conversion wrong — 0.1/week should be ~1.08/week"; also matched by finding: "Unit error in mu_EI and mu_IR initialization")

**Findings classification:**
- Major 1 (Global searches worse than local; best MLE never identified): A — no human issue raised this
- Major 2 (Tau severely constrained in all searches except profile): A — no human issue raised this
- Major 3 (mu_EI and mu_IR fixed; unit conversion wrong, 0.1/week should be ~1.08/week): B — matches Human Issues #11 and #12
- Major 4 (No benchmark comparison between SEIR and SARIMA): A — no human issue raised this
- Major 5 (Profile CI for rho rests on only three grid points): A — no human issue raised this
- Major 6 (b4 and b2 unidentifiable at likelihood optimum): A — no human issue raised this
- Major 7 (No model diagnostics: ESS, conditional log-likelihoods, filtering checks): A — no human issue raised this
- Major 8 (SEIR cannot explain multiple waves without waning immunity): B — matches Human Issue #8
- Minor: Unit error in mu_EI and mu_IR initialization: D — matches Human Issues #11 and #12
- Minor: Inappropriate auto-installing of packages: C — no human issue raised this
- Minor: Duplicate library(tidyverse) call: C — no human issue raised this
- Minor: registerDoParallel() called twice with conflicting arguments: C — no human issue raised this
- Minor: global_search_2.rds referenced but not discussed in text: C — no human issue raised this
- Minor: rho CI interpretation questionable (reporting rate 66–93% implausibly high): C — no human issue raised this
- Minor: SARIMA seasonal period 4 weeks but spectral peak at ~4.3 weeks: C — no human issue raised this
- Minor: No convergence traces for global searches: C — no human issue raised this
- Minor: Measurement model description slightly inconsistent (rmeasure vs dmeasure): C — no human issue raised this
- Minor: Missing pomp package version: C — no human issue raised this
- Minor: No RNG seeds before second global search: C — no human issue raised this
- Minor: Data truncation at Dec 26 not Dec 31 as stated: C — no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 11 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "24.03.5 — SARIMA equation uses B^12 but period=4 in code; should be B^4")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "M1 — initial conditions E(0)=100, I(0)=200 biologically implausible and unjustified")
- Human Issue #11: covered (matched by finding: "24.03.1 — µ_EI and µ_IR expressed in day⁻¹ but applied in weekly model, implying 10-week sojourn times")
- Human Issue #12: covered (matched by finding: "24.03.1 — µ_EI and µ_IR expressed in day⁻¹ but applied in weekly model, implying 10-week sojourn times")

**Findings classification:**
- 24.03.7: A — best MLE never identified; three global searches return results differing by >2,400 log-likelihood units with no reconciliation
- 24.03.2: A — profile CI for ρ is logically invalid because it excludes the MLE from global search 3; epidemiological conclusion unsupported
- 24.03.1: B — µ_EI and µ_IR appear to be in day⁻¹ but applied in a weekly time-step model, implying ~10-week sojourn times inconsistent with COVID-19 biology (matches Human Issues #11 and #12)
- 24.03.12: A — no convergence diagnostics (trace plots) shown for any of the three global searches
- M1: B — initial conditions E(0)=100 and I(0)=200 are biologically implausible and unjustified (matches Human Issue #10)
- 24.03.4: A — no quantitative benchmark comparison between SARIMA and SEIR on a common metric
- 24.03.3: C — simulation figures display results from global search 1 (loglik=−3531.9) rather than the best-fitting global search 3 result
- 24.03.5: D — SARIMA seasonal lag in the written equation is B^12 but the model uses period=4; should be B^4 (matches Human Issue #2)
- 24.03.13: C — key references (ARMA, SIR/SEIR, ACF/PACF, etc.) are Wikipedia articles rather than textbooks
- 24.03.14: C — µ_EI and µ_IR are fixed throughout and no sensitivity analysis is provided
- 24.03.6: C — truncated normal measurement model is not justified over a negative binomial
- 24.03.N1: C — Ljung-Box test p=0.024 confirms residual autocorrelation but no alternative models are explored

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 6 | 6 | 4 |
| B (AI major, human also found) | 1 | 1 | 2 | 2 |
| C (AI minor, human missed) | 7 | 5 | 11 | 5 |
| D (AI minor, human also found) | 1 | 1 | 1 | 1 |
| E (Human found, AI missed) | 9 | 8 | 9 | 8 |
| F (Human-AI contradiction) | 0 | 1 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 9 | 3/12 = 25% | 6 | 7 | 13/15 = 87% |
| Charlie | 1 | 1 | 8 | 3/11 = 27% | 6 | 5 | 11/13 = 85% |
| Doug | 2 | 1 | 9 | 3/12 = 25% | 6 | 11 | 17/20 = 85% |
| Evan | 2 | 1 | 8 | 4/12 = 33% | 4 | 5 | 9/12 = 75% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The project is very similar to 531w21 project 15. It references that project once, but does not give full credit to the intellectual debt. Much of the code and the format of the report is directly taken from that project, without explanation. The model turns out to be more satisfactory for the situation of 2024 project 15. This project not only fails to go beyond the analysis of its source project, it is weaker and does not pay full credit to the source. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The root plot shows some roots of the fitted ARMA are very close to the unit circle. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: The AIC table shows some failures in maximization that are not pointed out: SARMA(2,0,4)×(1,0,1) to SARMA(3,0,4)×(1,0,1) and SARMA(3,0,3)×(1,0,1) to SARMA(4,0,3)×(1,0,1), for example. The model that is chosen, SARMA(1,0,5)×(1,0,1), is rather large for this situation. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The residual histogram is wrongly described as nearly normal. It has long tails. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: The ARMA forecasts anticipate a new peak. That is because of heterogeneity through time — for example, the sample variance of the data varies considerably through time. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: The time units on the time plot for the POMP model does not match dates, so it is hard to see where the b_k terms switch over. The lag plot should also specify units of time. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 6 out of 12 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #8: It may be hard to explain the waves without including the limited protection that infection with earlier strains provided against later strains. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |
