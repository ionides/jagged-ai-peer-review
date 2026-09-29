# Comparator Analysis — W24 Project 05

---

## Human Issues

1. Please give figures captions and numbers. For the time plot: show date, not just week number. For the frequency analysis: give units in the text and the plot.

2. Doing spectral analysis to detect the annual seasonality in this data is not necessary. One can do it as an exercise, but one could add appreciation that the conclusion was unsurprising after looking at the data.

3. The ARMA grid search is rather small - no more than 2 lags. Was that an intentional decision?

4. The fraction of the project devoted to ARMA and linear time series analysis is too large, considering that this analysis ends up being useful mostly as a benchmark for the mechanistic modeling.

5. Infectious disease dynamics, like many ecological systems, is better modeled by ARMA on a log scale.

6. Log likelihood for differenced models are not immediately comparable to those for the original data. One has to properly account for the transformation.

7. An interesting use of ChatGPT to propose consideration of a sinusoidal seasonal transmission.

8. In the initial pfilter, effective sample size (ESS) is always between 1990 and 2000, which is surprising. Perhaps the measurement model is extremely flat?

9. When describing the model parameter, the group misses discussion on the measurement model. Even though the readers can examine this in the code snippet they use, it can be useful for an understanding of their readers if they incorporate it in their report.

10. The conclusions correctly point out the preliminary nature of the findings. The mechanistic model has some promising features, but does not (yet) explain the data better than an ARIMA model.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "log-likelihood comparison between SARIMA and POMP is invalid — SARIMA log-likelihood is on differenced data and not comparable to POMP marginal likelihood")
- Human Issue #7: contradiction (AI says sinusoidal forcing from ChatGPT is a Major weakness lacking epidemiological justification; human says it is an interesting use of ChatGPT)
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (Log-likelihood comparison invalid): B — SARIMA log-likelihood on differenced data cannot be directly compared to POMP log-likelihood (matches Human Issue #6)
- Finding 2 (H accumulator never reset): A — H accumulator in constant-Beta version omits accumvars, potentially growing without bound
- Finding 3 (SARIMA period=12 instead of 52): A — AIC table for seasonal order selection used wrong period
- Finding 4 (No profile likelihoods): A — poor man's profiles from pooled global search results cannot support parameter inference
- Finding 5 (Sinusoidal forcing from ChatGPT without justification): F — AI labels it a Major weakness; human calls it an interesting use of ChatGPT (contradicts Human Issue #7)
- Finding 6 (Estimated parameters not interpreted or validated): A — implied latent and infectious periods are biologically implausible but never discussed
- Finding 7 (Arbitrary truncation of dataset): A — restriction to 2011–2015 unjustified statistically or epidemiologically
- Finding 8 (Initial state parameters fixed without diagnostic support): C — local search had only 20 chains from one starting point; no sensitivity analysis
- Finding 9 (ARMA grid search dataset scope): C — overview plot unlabeled by year; truncation applied after initial display
- Finding 10 (Measurement model mismatch — dmeas uses H): C — cases measured via recoveries (dN_IR) rather than new infections introduces systematic delay
- Finding 11 (rw.sd values uniform and small): C — uniform 0.01 perturbations ignore different scales of Beta0, phase, mu_IR, rho
- Finding 12 (Poor man's profile filtering inconsistency): C — filtering thresholds in profiles inconsistent with best-parameter selection used earlier
- Finding 13 (SARIMA notation vs. code discrepancy): C — writeup shows seasonal subscript [52] but code passes period=12
- Finding 14 (eta parameter unused): C — eta appears in paramnames and params vector but is never referenced in any model snippet
- Finding 15 (Reproducibility/RNG seed not controlled per run): C — global search results read from pre-saved CSV files, not reproducible from Rmd alone

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: contradiction (AI says ChatGPT-sourced model structure is a weakness lacking citation; human says it was an interesting use)
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: contradiction (AI says conclusion overstates certainty; human says conclusions correctly point out the preliminary nature of the findings)

**Findings classification:**
- Finding 1 (SARIMA Grid Search Wrong Seasonal Period): A — Major; the SARIMA AIC grid search used period=12 instead of period=52, invalidating model selection
- Finding 2 (Profile Likelihoods Absent): A — Major; "poor man's profiles" are likelihood slices, not proper profiles; no valid uncertainty quantification
- Finding 3 (H Accumulator Tracks Recoveries Not New Infections): A — Major; accumulator increments dN_IR instead of dN_EI, misaligning observation model with clinical presentation
- Finding 4 (No Convergence Trace Plots for Global Search): A — Major; global search mif2 runs have no trace plots, leaving convergence unverified
- Finding 5 (Unused Parameter eta): A — Major; eta appears in paramnames and parameter vectors but is never referenced in any Csnippet
- Finding 6 (logmeanexp SE Not Reported for pf_local): C — Minor; pf_local log-likelihood reported without Monte Carlo standard error
- Finding 7 (Biological Plausibility of Estimated Parameters Not Checked): C — Minor; final parameter estimates not compared against known flu biology
- Finding 8 (SARIMA Residual Diagnostics Incomplete): C — Minor; no Ljung-Box test; residual autocorrelation assessed only visually
- Finding 9 (Data Restriction Partly Computationally Motivated): C — Minor; restricting data to 2011–2015 justified partly by cluster slowness rather than scientific criteria
- Finding 10 (ChatGPT Model Structure Without Literature Citation): F — contradiction; AI flags absence of literature citation as a weakness (contradicts Human Issue #7)
- Finding 11 (Local Search Non-Convergence Dismissed Too Quickly): C — Minor; non-convergence of parameters in local search dismissed without follow-up analysis
- Finding 12 (Phase Parameter Not Constrained for Periodicity): C — Minor; unconstrained phase creates infinite identical modes, causing artificial multimodality in profiles
- Finding 13 (rw.sd = 0.01 Is Half Course Standard): C — Minor; perturbation size unjustifiably halved relative to course standard of 0.02
- Finding 14 (No Sensitivity Analysis of Particle Count): C — Minor; Np=2000 used throughout with no sensitivity check against a smaller Np
- Finding 15 (Conclusion Overstates Certainty): F — contradiction; AI says conclusion rests on shaky foundations and should be more measured (contradicts Human Issue #10)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 2 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Invalid log-likelihood comparison between SARIMA and POMP")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major 1 — Invalid log-likelihood comparison between SARIMA and POMP: B (matches Human Issue #6)
- Major 2 — SARIMA grid search uses incorrect seasonal period (period=12 instead of 52): A
- Major 3 — Reporting rate (rho) estimate is biologically implausible (~0.0013): A
- Major 4 — Key parameters poorly identified, no profile likelihoods computed: A
- Major 5 — No valid benchmark comparison for POMP model: A
- Major 6 — Log-likelihood direction misstated in local search narrative: A
- Minor 1 — SARIMA model text uses B_12 inconsistently with final model at period=52: C
- Minor 2 — rw.sd for phase parameter is extremely small (0.01): C
- Minor 3 — k and initial conditions fixed during global search: C
- Minor 4 — Phantom eta parameter in initial SEIRS model: C
- Minor 5 — Inconsistency between claimed (750) and actual (1,354) search count: C
- Minor 6 — No quantitative goodness-of-fit summary for POMP simulations: C
- Minor 7 — Rationale for restricting data to 2011–2015 requires stronger justification: C
- Minor 8 — Decomposition section misstates seasonal period as daily/weekly rather than annual: C
- Minor 9 — No discussion of model limitations beyond parameter estimation issues: C
- Minor 10 — Total computational cost not reported: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ID 24.05.7 — conclusion treats non-comparable likelihoods as directly comparable; SARIMA fitted to doubly-differenced series, POMP to original counts")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- ID 24.05.1: A — possible wrong seasonal period in SARIMA (period=12 vs. 52 weeks)
- ID 24.05.2: A — global search log-likelihoods likely taken from mif2 output rather than replicated pfilter evaluations
- ID 24.05.3: A — parameters mu_IR and mu_RS span orders of magnitude at comparable likelihoods; severe identifiability problem
- ID 24.05.4: A — profile likelihoods absent; no parameter confidence intervals computed
- ID 24.05.7: B — conclusion directly compares SARIMA (differenced, Gaussian) and POMP (original counts, negative binomial) log-likelihoods without methodological justification (matches Human Issue #6)
- ID 24.05.6: C — best-fit immune period (~13 weeks) is implausibly short relative to published influenza natural history
- ID 24.05.8: C — unused parameter eta in initial paramnames vector
- ID 24.05.12: C — loglik.se from replicated pfilter is computed but never reported in text
- ID 24.05.13: C — fixed parameter values (S0, E0, I0, R0, k) and rationale for fixing them are not stated
- ID 24.05.NEW1: C — result RDS/CSV files not archived in submission
- ID 24.05.NEW2: C — no per-chain convergence trace plots shown for any global search

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 5 | 5 | 4 |
| B (AI major, human also found) | 1 | 0 | 1 | 1 |
| C (AI minor, human missed) | 8 | 8 | 10 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 8 | 8 | 9 | 9 |
| F (Human-AI contradiction) | 1 | 2 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 8 | 1/9 = 11% | 5 | 8 | 13/14 = 93% |
| Charlie | 0 | 0 | 8 | 0/8 = 0% | 5 | 8 | 13/13 = 100% |
| Doug | 1 | 0 | 9 | 1/10 = 10% | 5 | 10 | 15/16 = 94% |
| Evan | 1 | 0 | 9 | 1/10 = 10% | 4 | 6 | 10/11 = 91% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Please give figures captions and numbers. For the time plot: show date, not just week number. For the frequency analysis: give units in the text and the plot. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: Doing spectral analysis to detect the annual seasonality in this data is not necessary. One can do it as an exercise, but one could add appreciation that the conclusion was unsurprising after looking at the data. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: The ARMA grid search is rather small - no more than 2 lags. Was that an intentional decision? (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The fraction of the project devoted to ARMA and linear time series analysis is too large, considering that this analysis ends up being useful mostly as a benchmark for the mechanistic modeling. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: Infectious disease dynamics, like many ecological systems, is better modeled by ARMA on a log scale. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: In the initial pfilter, effective sample size (ESS) is always between 1990 and 2000, which is surprising. Perhaps the measurement model is extremely flat? (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: When describing the model parameter, the group misses discussion on the measurement model. Even though the readers can examine this in the code snippet they use, it can be useful for an understanding of their readers if they incorporate it in their report. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 7 out of 10 human issues (70%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
