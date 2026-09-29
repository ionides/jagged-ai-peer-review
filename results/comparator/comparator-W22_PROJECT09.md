# Comparator Analysis — W22 Project 09

---

## Human Issues

1. Further diagnostic analysis could investigate which data points are problematic for the mechanistic model to explain (e.g., using effective sample size) which might lead to insights on ways to get improved understanding in future.

2. A bug has led to a collection of identical points reported for the global search.

3. The conclusion $b_2>b_1$ may not be statistically significant. One could make a suitable profile likelihood, or equivalently a likelihood ratio test.

4. The initial values for the state variables $E_0 = 30$, $I_0 = 30$ may be questionable. As an alternative, the initial states for $E$ and $I$ could be parameterized similarly to $S$, as in lecture notes Ch 17.

5. The local search shows issues. The log likelihood diverges with iterations. Possibly, the authors could plot particle filters diagnostic and look at ESS, which might give clues what is going wrong. Problematic model assumptions could be state initializations and/or process overdispersion. It is also possible that reducing the random walk size would change the local search trends.

6. The report does not specify the measurement model.

7. The report closely follows https://ionides.github.io/531w21/final_project/project15/blinded.html. This project is cited, so it is not a major problem. The updated data leads to new considerations. However, when so much of the groundwork is already prepared, one may hope the project will go further. If anything, less is done here, since the previous project also calculated a profile. Also, the conclusions are less carefully drawn and the model is less fully described - it is identical when it appears in both, but this article omits to describe the measurement model. If the authors had explained better the close relationship to this previous project, they might have realized that they should make their own contribution larger.

8. The style of references is informal.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No profile likelihood or confidence intervals — explicitly notes the b1/b2 difference cannot be assessed as statistically meaningful")
- Human Issue #4: covered (matched by finding: "Initial E=30 hardcoded and not justified relative to data")
- Human Issue #5: covered (matched by finding: "Likelihood non-convergence acknowledged but not addressed")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (H tracks recoveries not infections): A — fundamental accumulator mis-specification; no human issue raises this
- Finding 2 (SEIR outperformed by SARIMA): A — mechanistic model worse than non-mechanistic benchmark; not raised by human
- Finding 3 (mu_IR fixed without justification): A — recovery rate hardcoded, no sensitivity analysis; not raised by human
- Finding 4 (No profile likelihood or CIs): B — no uncertainty quantification, b1/b2 difference cannot be assessed (matches Human Issue #3)
- Finding 5 (Likelihood non-convergence not addressed): B — log-likelihood diverges in local search, no remedial action (matches Human Issue #5)
- Finding 6 (Measurement model Normal approximation): A — Gaussian model allows negative counts; human issue #6 flags absence of measurement model description in text, not its appropriateness
- Finding 7 (Global search single mif2 pass): C — only one mif2 round per starting point; not raised by human
- Finding 8 (Covariate split date inconsistency): C — off-by-one day error and misleading "first half" description; not raised by human
- Finding 9 (rho=0.9 implausibly high): C — initial reporting probability not epidemiologically justified; not raised by human
- Finding 10 (ARMA benchmark comparison flawed): C — log-likelihood scales not comparable between SARIMA and SEIR; not raised by human
- Finding 11 (E=30 hardcoded and unjustified): D — initial exposed compartment arbitrary and not varied in global search (matches Human Issue #4)
- Finding 12 (EDA caption repeated verbatim): C — editing error, same text appears twice; not raised by human
- Finding 13 (Typo cahce=TRUE): C — misspelling disables chunk caching; not raised by human
- Finding 14 (Wrong notation mu_SI): C — S-to-E rate mislabeled as mu_SI; not raised by human
- Finding 15 (Vaccination/waning immunity ignored): C — no discussion of vaccination or Omicron reinfection during study period; not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "No Model Diagnostics Beyond Visual Simulation Comparison — no ESS traces computed")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No Profile Likelihoods for Any Parameter")
- Human Issue #4: covered (matched by finding: "Initial Conditions: E and I Fixed Without Justification")
- Human Issue #5: covered (matched by finding: "Non-Monotone Likelihood During Local Search Is Noted But Not Addressed")
- Human Issue #6: covered (matched by finding: "Measurement Model Uses Normal Approximation Instead of Count Distribution — text does not specify the approximating distribution")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (Global Search One mif2 Pass): A — global search convergence inadequacy due to single mif2 pass per starting value
- Finding 2 (mu_IR Fixed): A — mu_IR fixed at 0.2 without biological justification or sensitivity analysis
- Finding 3 (No Profile Likelihoods): B — no profile likelihoods for any parameter (matches Human Issue #3)
- Finding 4 (SARIMA Jacobian): A — SARIMA log-likelihood comparison and scale mismatch inadequately addressed
- Finding 5 (Non-Monotone Likelihood): B — non-monotone likelihood during local search noted but not addressed (matches Human Issue #5)
- Finding 6 (Measurement Model Normal Approximation): B — measurement model uses normal approximation and text does not formally specify the distribution (matches Human Issue #6)
- Finding 7 (H Accumulator): A — H accumulator tracks recoveries rather than new infections, invalidating rho interpretation
- Finding 8 (Initial Conditions): D — E_0 and I_0 fixed as "intuitive values" without justification or estimation (matches Human Issue #4)
- Finding 9 (Benchmark Gap Undercharacterized): C — 238 log-likelihood unit gap described as "slightly higher" without adequate discussion
- Finding 10 (Global Search Box Includes Zero): C — lower bounds for b1 and b2 include zero, causing potential numerical problems
- Finding 11 (No Model Diagnostics): D — no ESS traces or per-time-point diagnostics to identify problematic periods (matches Human Issue #1)
- Finding 12 (Covariate Split Hard-Coded): C — Delta/Omicron intervention split date hard-coded without sensitivity check
- Finding 13 (Local Search 20 Replicates): C — local search uses only 20 replicates from the same starting point
- Finding 14 (Missing sessionInfo): C — no sessionInfo() or package version documentation
- Finding 15 (Caption Repeated): C — figure caption text repeated verbatim in the body

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "No ESS monitoring reported — ESS not reported for any filtering run, preventing assessment of filtering quality and model-data mismatch")
- Human Issue #2: covered (matched by finding: "Global Search Initialized from a Previous mif2 Result Object — anchors global search near local solution, compromising the claimed global optimization")
- Human Issue #3: covered (matched by finding: "No Profile Likelihoods Computed — without profiles for b1, b2, rho it is impossible to assess whether b2>b1 is statistically significant")
- Human Issue #4: covered (matched by finding: "Initial conditions inadequately justified — E=30 and I=30 described as 'intuitive' without sensitivity analysis")
- Human Issue #5: covered (matched by finding: "Self-Diagnosed Non-Convergence Used to Draw Substantive Conclusions — local search log-likelihood does not strictly increase yet estimates are reported as definitive"; also matched by finding: "No ESS monitoring reported")
- Human Issue #6: covered (matched by finding: "Measurement Model Uses Normal Approximation Without Justification — Gaussian approximation is not discussed or justified in the text")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (Self-Diagnosed Non-Convergence): B — authors acknowledge convergence failure yet proceed to draw parameter estimates and model conclusions (matches Human Issue #5)
- Major 2 (Global Search Init Error): B — global search initialized from a previous mif2 result, inheriting cooling schedule and anchoring near local solution rather than exploring the box (matches Human Issue #2)
- Major 3 (Invalid Log-Likelihood Comparison SARIMA vs SEIR): A — SARIMA fitted to log(y+1)-transformed data under Gaussian errors; SEIR fitted to original count data; direct numerical comparison is invalid
- Major 4 (Accumulator Variable Accumulates Recoveries): A — H += dN_IR tracks recoveries rather than new infections, causing semantic mismatch between H and the observed case counts
- Major 5 (Measurement Model Uses Normal Approximation): B — Gaussian continuity-correction approximation is not discussed or justified in the report text (matches Human Issue #6)
- Major 6 (SARIMA Back-Transformation Mathematically Unjustified): A — log(y+1) Jacobian correction is invalid, making the "corrected log-likelihood" of -1308.984 not a valid quantity on the original scale
- Major 7 (No Profile Likelihoods Computed): B — no profiles for b1, b2, rho, or other parameters; identifiability unassessed and b2>b1 conclusion unverifiable (matches Human Issue #3)
- Major 8 (Negative Binomial Benchmark Not Time-Resolved): A — i.i.d. stationary negative binomial sets a trivially low bar; SARIMA model outperforms SEIR but receives minimal discussion
- Minor: Fixed mu_IR without sensitivity analysis: C — mu_IR fixed at 0.2 without citation or sensitivity analysis; Omicron evidence suggests shorter infectious periods
- Minor: Initial conditions inadequately justified: D — E=30 and I=30 described as "intuitive" without sensitivity analysis (matches Human Issue #4)
- Minor: No convergence traces for global search: C — convergence traces shown for local search but not for any of the 500 global search chains
- Minor: Simulation plot shows excessive variance without quantitative assessment: C — visual-only description of "slightly large variance" with no quantitative coverage measure
- Minor: Duplicate description of Figure 1 text: C — paragraph describing Figure 1 appears twice, appearing to be a copy-paste error
- Minor: covariate_table counts not verified (off-by-one): C — 154+125=279, one day short of the 280-observation span, potential silent boundary mismatch
- Minor: No reproducibility information: C — no sessionInfo() or pomp version specified
- Minor: No ESS monitoring reported: D — ESS not reported for any filtering run; persistent collapse would indicate model-data mismatch or insufficient particles (matches Human Issues #1 and #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ESS Not Monitored — ESS not reported or plotted; flag periods of consistently low ESS")
- Human Issue #2: covered (matched by finding: "Duplicate Rows in Global Search Table and Loglik Discrepancy")
- Human Issue #3: covered (matched by finding: "Parameter Non-Identifiability: b2 and mu_EI — profile likelihoods needed; b2>b1 conclusion unsupported")
- Human Issue #4: missed
- Human Issue #5: covered (matched by findings: "Local Search Non-Convergence Seeding Global Search" and "ESS Not Monitored — ESS not reported or plotted; flag periods of consistently low ESS")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- 22.09.1: B — Duplicate rows in global search table and loglik discrepancy with pair plot (matches Human Issue #2)
- 22.09.2: B — Local search non-convergence used to seed global search; trace plot diverges (matches Human Issue #5)
- 22.09.3: B — b2 and mu_EI effectively unidentified; profile likelihoods needed; b2>b1 conclusion unsupported (matches Human Issue #3)
- 22.09.4: A — Implausible reporting rate rho~0.97 signals model misspecification; not examined
- 22.09.5: A — H accumulator increments dN_IR instead of dN_EI, producing a time-shifted measurement of incidence
- 22.09.6: C — Initial pfilter Monte Carlo SE of 1510 not acknowledged
- 22.09.7: C — Gaussian measurement model clamps negative values in rmeas but assigns nonzero density to negatives in dmeas
- 22.09.8: C — SARIMA and SEIR likelihoods not on identical scales even after Jacobian correction
- 22.09.9: D — ESS not monitored or plotted; filter degeneracy undetected (matches Human Issues #1 and #5)
- 22.09.10: C — mu_IR fixed at 0.2 without clinical citation; single value used across Delta and Omicron periods
- 22.09.11: C — Extreme simulation variance in Figure 8 not discussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 4 | 4 | 2 |
| B (AI major, human also found) | 2 | 3 | 4 | 3 |
| C (AI minor, human missed) | 8 | 6 | 6 | 5 |
| D (AI minor, human also found) | 1 | 2 | 2 | 1 |
| E (Human found, AI missed) | 5 | 3 | 2 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 5 | 3/8 = 38% | 4 | 8 | 12/15 = 80% |
| Charlie | 3 | 2 | 3 | 5/8 = 62% | 4 | 6 | 10/15 = 67% |
| Doug | 4 | 2 | 2 | 6/8 = 75% | 4 | 6 | 10/16 = 62% |
| Evan | 3 | 1 | 4 | 4/8 = 50% | 2 | 5 | 7/11 = 64% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #7: The report closely follows https://ionides.github.io/531w21/final_project/project15/blinded.html. This project is cited, so it is not a major problem. The updated data leads to new considerations. However, when so much of the groundwork is already prepared, one may hope the project will go further. If anything, less is done here, since the previous project also calculated a profile. Also, the conclusions are less carefully drawn and the model is less fully described - it is identical when it appears in both, but this article omits to describe the measurement model. If the authors had explained better the close relationship to this previous project, they might have realized that they should make their own contribution larger. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The style of references is informal. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 8 human issues (25%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
