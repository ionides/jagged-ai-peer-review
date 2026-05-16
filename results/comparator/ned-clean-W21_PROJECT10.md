# Ned-Clean Analysis — W21 Project 10

---

## Human Issues

1. There is an erroneous instantaneous drop in susceptibles evident when plotted, corresponding to a huge spike in cases — likely a reporting artifact from one facility catching up on numbers. It is unclear what was done about it.
2. The goal behind developing a range of models for vaccination counts (when vaccination is subsequently treated as a covariate input, not a response, for understanding cases) is not clearly explained.
3. There is a clear outlier in the cases — it is unclear what was done about it. Diagnostic plots are not shown, and such an outlier can be problematic for model development and fitting.
4. Too many significant figures in the table.
5. Why does the vaccination covariate not help explain the 2nd difference of COVID cases? This is not discussed.
6. The project did not get far into POMP modeling; simulated models have far less variability than the data, which likely explains why they cannot provide a statistical fit.
7. The graphic in the introduction contains microbiological details not needed for the project — either explain their role or leave them out.
8. Non-English captions on some graphs, other typos, and inconsistent abbreviations were distracting.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "No likelihood-based inference performed for any POMP model")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major #1 (No likelihood-based inference for any POMP model): B — matches Human Issue #6
- Major #2 (No parameter estimation — all hand-tuned): A — human did not raise no-estimation as a distinct concern beyond general POMP failure
- Major #3 (Bug in Model 3: N_SV drawn from I instead of S): A — human did not raise this
- Major #4 (Binomial measurement model causing -Inf log-likelihoods): A — human did not raise this
- Major #5 (Data window choice unexplained / potentially cherry-picked): A — human did not raise this
- Major #6 (Duplicate introduction section content): A — human did not raise this
- Major #7 (LRT degrees of freedom wrong): A — human did not raise this
- Major #8 (ARMA model applied to wrong data split): A — human did not raise this
- Minor #9 (Susceptible population calculation double-counts deaths): C — human did not raise this
- Minor #10 (Vaccination rate in Models 1 and 2 is hard-coded): C — human did not raise this
- Minor #11 (Model 2 uses `index` as state variable incorrectly): C — human did not raise this
- Minor #12 (Quadratic vaccination fit presented without residual diagnostics): C — human did not raise this
- Minor #13 (AIC table search reaches upper boundary without expanding): C — human did not raise this
- Minor #14 (No diagnostics for ARIMA models): C — human did not raise this
- Minor #15 (Live URL data downloads create reproducibility risk): C — human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "No likelihood-based inference performed on any POMP model")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major #1 (No likelihood-based inference performed on any POMP model): B — matches Human Issue #6
- Major #2 (No convergence diagnostics, no mif2 runs in main analysis): A — human did not raise this as a distinct concern
- Major #3 (Smoothed non-integer data fed to binomial measurement model): A — human did not raise this
- Major #4 (Mathematical specification of Model 3 inconsistent with code): A — human did not raise this
- Major #5 (LRT uses wrong degrees of freedom and mismatched data): A — human did not raise this
- Major #6 (No quantitative goodness-of-fit statistics for any model): A — human did not raise this
- Major #7 (No benchmark comparison for POMP model): A — human did not raise this
- Major #8 (H accumulator tracks recoveries but compared to new case reports): A — human did not raise this
- Minor #9 (Data duplication in Introduction and Section 2.1): C — human did not raise this
- Minor #10 (Vaccine constant V applied per Euler substep, not per day): C — human did not raise this
- Minor #11 (No residual diagnostics for ARIMA models): C — human did not raise this
- Minor #12 (Model selection ignores upper-boundary issue in AIC table): C — human did not raise this
- Minor #13 (ARIMA model applied to post-vaccination data after pre-vaccination selection, no justification): C — human did not raise this
- Minor #14 (Inconsistent parameter values between text and equations): C — human did not raise this
- Minor #15 (Data loaded from live external URLs): C — human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "No likelihood-based inference performed")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major #1 (No likelihood-based inference performed): B — matches Human Issue #6
- Major #2 (Binomial measurement model applied to accumulator H causes degenerate likelihood): A — human did not raise this
- Major #3 (Visual-only goodness-of-fit assessment): A — human did not raise this
- Major #4 (Vaccination subtraction can drive S below zero): A — human did not raise this
- Major #5 (Model 3 vaccination rate draws from wrong compartment): A — human did not raise this
- Major #6 (No benchmark comparison for POMP model): A — human did not raise this
- Major #7 (LRT applied to mismatched models, wrong degrees of freedom): A — human did not raise this
- Major #8 (No parameter identifiability assessment): A — human did not raise this
- Major #9 (Rolling-mean data misspecification in POMP models): A — human did not raise this
- Major #10 (`index` state variable not declared in partrans; linear vaccination unbounded): A — human did not raise this
- Minor: Data loading from external URLs: C — human did not raise this
- Minor: mu_IR not declared in partrans: C — human did not raise this
- Minor: Section 2.1 and Introduction duplicated: C — human did not raise this
- Minor: N population values inconsistent across models: C — human did not raise this
- Minor: No random seeds for reproducibility: C — human did not raise this
- Minor: Susceptible population formula double-counts recoveries: C — human did not raise this
- Minor: No convergence traces or ESS diagnostics: C — human did not raise this
- Minor: References use raw URLs rather than formal citations: C — human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "No likelihood-based inference performed")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major #1 / ID 21.10.8 (No likelihood-based inference performed): B — matches Human Issue #6
- Major #2 / ID 21.10.1+21.10.3 (Measurement model specification failures causing -Inf likelihoods): A — human did not raise this
- Major #3 / ID 21.10.2 (Model 3: vaccination draws from I not S): A — human did not raise this
- Major #4 / ID 21.10.9 (No benchmark comparison): A — human did not raise this
- Major #5 / unlabeled (Forward simulations are not goodness-of-fit evidence): A — human did not raise this
- Minor #6 / ID 21.10.5 (LRT degrees of freedom misstated): C — human did not raise this
- Minor #7 / ID 21.10.3 (mu_EI and mu_IR unit confusion): C — human did not raise this
- Minor #8 / unlabeled (Duplicate text in Introduction and Section 2.1): C — human did not raise this
- Minor #9 / unlabeled (Missing figure captions): C — human did not raise this (H8 is about non-English captions and typos, a distinct concern)
- Minor #10 / unlabeled (Set RNG seeds consistently): C — human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 7 | 9 | 4 |
| B (AI major, human also found) | 1 | 1 | 1 | 1 |
| C (AI minor, human missed) | 7 | 7 | 8 | 5 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 7 | 7 | 7 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+7) = 1/8 = 0.125
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+7) / (7+1+7+0) = 14/15 = 0.933

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+7) = 1/8 = 0.125
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+7) / (7+1+7+0) = 14/15 = 0.933

**Doug**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+7) = 1/8 = 0.125
- AI-Unique Rate = (A+C) / (A+B+C+D) = (9+8) / (9+1+8+0) = 17/18 = 0.944

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+7) = 1/8 = 0.125
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+5) / (4+1+5+0) = 9/10 = 0.900

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- Human Issue #1: Erroneous instantaneous drop in susceptibles / spike in cases (reporting artifact) — missed by all 4 reviewers
- Human Issue #2: Goal behind vaccination modeling not clearly explained — missed by all 4 reviewers
- Human Issue #3: Clear outlier in cases, unclear what was done, no diagnostic plots — missed by all 4 reviewers
- Human Issue #4: Too many significant figures in the table — missed by all 4 reviewers
- Human Issue #5: Vaccination covariate not helping explain 2nd difference of COVID cases, not discussed — missed by all 4 reviewers
- Human Issue #7: Introductory graphic contains unnecessary microbiological details — missed by all 4 reviewers
- Human Issue #8: Non-English captions, typos, inconsistent abbreviations — missed by all 4 reviewers

Count: 7 out of 8 human issues were consensus misses.

**Unique finds per reviewer:** Human issues covered by exactly one reviewer and missed by all others.

- Human Issue #6 (POMP not far enough, simulated models less variable) was covered by all four reviewers. No human issue was covered by exactly one reviewer and missed by all others.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

All four reviewers raised the following concerns that the human did not raise:

1. Model 3: vaccination transition draws from the infectious compartment (I) instead of the susceptible compartment (S) — a fundamental compartment error
2. LRT degrees of freedom are wrong (ARIMA(1,1,1) vs. ARIMA(4,1,4) has 6 parameter difference, not 2)
3. Duplicate content between the Introduction and Section 2.1

Count: 3 universal AI-only flags.
