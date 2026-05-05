# Ned-Clean Analysis — W21 Project 03

---

## Human Issues

1. The scatterplot for the SIR global search shows flat likelihood surface — some parameter combinations are unidentifiable — but this is a fact about the data, not a problem with maximization.
2. The ODE models written down do not perfectly match the POMP model implemented (the ODE is a deterministic skeleton, not identical to the POMP model).
3. The first SIRV model fits considerably better (8 units of log likelihood gained for two degrees of freedom); a likelihood ratio test is possible even without full identifiability.
4. The second SIRV model does not improve log likelihood; there is a coding bug — t^2 in the vaccination model is incorrectly included as dt^2 in the latent process model equations and code.
5. There could be benefits from running the code for longer (more particles/iterations), perhaps using the greatlakes cluster.
6. For the fitted models, it would be useful to calculate and discuss the R_0 values corresponding to the fitted parameters (e.g., R_0 = beta/mu_IR).

---

## Alex

**Coverage record:**
- Human Issue #1 (flat SIR likelihood surface, not a maximization problem): missed
- Human Issue #2 (ODE doesn't match POMP model): covered (matched by finding: "SIRV1 V-to-I transition hazard uses V instead of I — code-ODE mismatch")
- Human Issue #3 (SIRV1 fits better, LRT possible): covered (matched by finding: "SIR model dismissed by visual inspection, not likelihood comparison")
- Human Issue #4 (SIRV2 dt^2 coding bug): covered (matched by finding: "SIRV2 deterministic dN_SV can produce negative S — dt^2 formula issue")
- Human Issue #5 (run longer): covered (matched by finding: "Run level is set to 1 throughout — too few particles and iterations")
- Human Issue #6 (R_0 values): missed

**Findings classification:**
- Finding 1 (Accumulator H tracks dN_IR not dN_SI — fundamental misspecification): A — MAJOR, human missed
- Finding 2 (Prediction simulation uses initial-guess params, not MLE): A — MAJOR, human missed
- Finding 3 (SIRV1 V-to-I hazard uses V instead of I): B — MAJOR (matches Human Issue #2)
- Finding 4 (SIRV1 S-to-V hazard density-dependent, inconsistent with ODE): A — MAJOR, human issue #2 already matched by finding 3
- Finding 5 (Run level = 1, too few particles/iterations): B — MAJOR (matches Human Issue #5)
- Finding 6 (Profile: Sigma not held fixed in first mif2 call): A — MAJOR, human missed
- Finding 7 (SIRV2 dN_SV can produce negative S, dt^2 formula): B — MAJOR (matches Human Issue #4)
- Finding 8 (Local search uses single pfilter, no replication): C — MODERATE treated as Minor, human missed
- Finding 9 (CI cutoff for sigma computed but not plotted): C — MODERATE treated as Minor, human missed
- Finding 10 (Active cases as I(0) conflates active with true infectious): C — MODERATE treated as Minor, human missed
- Finding 11 (Vaccine efficacy ">80%" not supported by analysis): C — MODERATE treated as Minor, human missed
- Finding 12 (SIR dismissed by visual inspection, no formal LRT or AIC): D — MODERATE treated as Minor (matches Human Issue #3)
- Finding 13 (Vaccination regression uses same data as POMP model): C — MINOR, human missed
- Finding 14 (Prediction plots show 5 simulations, text claims 10): C — MINOR, human missed
- Finding 15 (SIRV1 global search filter threshold 1000 units, too wide): C — MINOR, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (flat SIR likelihood surface, not a maximization problem): missed
- Human Issue #2 (ODE doesn't match POMP model): covered (matched by finding: "SIRV model 1 incorrect force of infection on vaccinated compartment — uses V instead of I")
- Human Issue #3 (SIRV1 fits better, LRT possible): covered (matched by finding: "Goodness-of-fit assessed only visually — no AIC table or formal comparison")
- Human Issue #4 (SIRV2 dt^2 coding bug): missed
- Human Issue #5 (run longer): covered (matched by finding: "Grossly insufficient computational effort — run_level=1 throughout")
- Human Issue #6 (R_0 values): missed

**Findings classification:**
- Finding 1 (Accumulator H tracks recoveries, not new infections): A — MAJOR, human missed
- Finding 2 (Global search initialized from previous mif2, not base pomp object): A — MAJOR, human missed
- Finding 3 (Prediction uses initial manual guess, not MLE): A — MAJOR, human missed
- Finding 4 (Grossly insufficient computational effort, run_level=1): B — MAJOR (matches Human Issue #5)
- Finding 5 (No non-mechanistic benchmark comparison): A — MAJOR, human missed
- Finding 6 (Profile sigma allows drift — rw.sd error): A — MAJOR, human missed
- Finding 7 (SIRV1 incorrect force of infection, uses V instead of I): B — MAJOR (matches Human Issue #2)
- Finding 8 (Forecast not conditioned on filtering distribution): A — MAJOR, human missed
- Finding M1 (Log-likelihood single-evaluation in local search, no replication): C — MINOR, human missed
- Finding M2 (Possible negative initial compartment R): C — MINOR, human missed
- Finding M3 (SIRV2 vaccination rate formula inconsistency, 1.89 vs 1.90): C — MINOR, human missed
- Finding M4 (No effective sample size diagnostics): C — MINOR, human missed
- Finding M5 (No corroboration with scientific knowledge): C — MINOR, human missed
- Finding M6 (Goodness-of-fit assessed only visually, no AIC table): D — MINOR (matches Human Issue #3)
- Finding M7 (Population scaling unit inconsistency): C — MINOR, human missed
- Finding M8 (Typo "EXISTING!" in conclusion): C — MINOR, human missed
- Finding M9 (References year discrepancy, 2012 vs 2021): C — MINOR, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1 (flat SIR likelihood surface, not a maximization problem): missed
- Human Issue #2 (ODE doesn't match POMP model): covered (matched by finding: "SIRV model 1 incorrect force of infection on vaccinated compartment — uses V instead of I")
- Human Issue #3 (SIRV1 fits better, LRT possible): covered (matched by finding: "Goodness-of-fit assessed only visually — no AIC table or formal comparison")
- Human Issue #4 (SIRV2 dt^2 coding bug): missed
- Human Issue #5 (run longer): covered (matched by finding: "Grossly insufficient computational effort — run_level=1 throughout")
- Human Issue #6 (R_0 values): missed

**Findings classification:**
- Finding 1 (Accumulator H tracks recoveries, not new infections): A — MAJOR, human missed
- Finding 2 (Global search initialized from previous mif2, not base pomp object): A — MAJOR, human missed
- Finding 3 (Prediction uses initial manual guess, not MLE): A — MAJOR, human missed
- Finding 4 (Grossly insufficient computational effort, run_level=1): B — MAJOR (matches Human Issue #5)
- Finding 5 (No non-mechanistic benchmark comparison): A — MAJOR, human missed
- Finding 6 (Profile sigma allows drift — rw.sd error): A — MAJOR, human missed
- Finding 7 (SIRV1 incorrect force of infection, uses V instead of I): B — MAJOR (matches Human Issue #2)
- Finding 8 (Forecast not conditioned on filtering distribution): A — MAJOR, human missed
- Finding M1 (Log-likelihood single-evaluation in local search, no replication): C — MINOR, human missed
- Finding M2 (Possible negative initial compartment R): C — MINOR, human missed
- Finding M3 (SIRV2 vaccination rate formula inconsistency, 1.89 vs 1.90): C — MINOR, human missed
- Finding M4 (No effective sample size diagnostics): C — MINOR, human missed
- Finding M5 (No corroboration with scientific knowledge): C — MINOR, human missed
- Finding M6 (Goodness-of-fit assessed only visually, no AIC table): D — MINOR (matches Human Issue #3)
- Finding M7 (Population scaling unit inconsistency): C — MINOR, human missed
- Finding M8 (Typo "EXISTING!" in conclusion): C — MINOR, human missed
- Finding M9 (References year discrepancy, 2012 vs 2021): C — MINOR, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (flat SIR likelihood surface, not a maximization problem): missed
- Human Issue #2 (ODE doesn't match POMP model): covered (matched by finding: "21.03.7 — SIRV1 S-to-V transition probability S-dependence inconsistency with ODE")
- Human Issue #3 (SIRV1 fits better, LRT possible): missed
- Human Issue #4 (SIRV2 dt^2 coding bug): missed
- Human Issue #5 (run longer): covered (matched by finding: "21.03.1 — Critically insufficient computation")
- Human Issue #6 (R_0 values): missed

**Findings classification:**
- 21.03.1 (Critically insufficient computation, run_level=1): B — MAJOR (matches Human Issue #5)
- 21.03.2 (No non-mechanistic benchmark comparison): A — MAJOR, human missed
- 21.03.3 (Forecast simulation uses starting-guess params, not MLE): A — MAJOR, human missed
- 21.03.4 (Accumulator H tracks recoveries rather than new infections): A — MAJOR, human missed
- 21.03.5 (SIRV1 outperforms SIRV2 in likelihood without explanation): A — MAJOR, human missed
- 21.03.6 (Profile CI cutoff suppressed, too sparse): C — MINOR, human missed
- 21.03.7 (SIRV1 S-to-V S-dependence inconsistency with stated ODE): D — MINOR (matches Human Issue #2)
- 21.03.M1 (Binomial measurement model, overdispersion not considered): C — MINOR, human missed
- 21.03.M2 (EDA limited, no ACF or log-scale examination): C — MINOR, human missed
- 21.03.M3 (Computational settings hidden from rendered output): C — MINOR, human missed
- 21.03.M4 (Minor writing errors — typos): C — MINOR, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 4 | 6 | 6 | 4 |
| B (AI major, human also found) | 3 | 2 | 2 | 1 |
| C (AI minor, human missed) | 7 | 8 | 8 | 5 |
| D (AI minor, human also found) | 1 | 1 | 1 | 1 |
| E (Human found, AI missed) | 2 | 3 | 3 | 4 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (3+1) / (3+1+2) = 4/6 = 0.667 (66.7%)
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+7) / (4+3+7+1) = 11/15 = 0.733 (73.3%)

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+3) = 3/6 = 0.500 (50.0%)
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+8) / (6+2+8+1) = 14/17 = 0.824 (82.4%)

**Doug**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+3) = 3/6 = 0.500 (50.0%)
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+8) / (6+2+8+1) = 14/17 = 0.824 (82.4%)

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+4) = 2/6 = 0.333 (33.3%)
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+5) / (4+1+5+1) = 9/11 = 0.818 (81.8%)

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer:

- Human Issue #1 (flat SIR likelihood surface as a data property, not a maximization problem): missed by Alex, Charlie, Doug, Evan
- Human Issue #6 (calculate and discuss R_0 values for fitted parameters): missed by Alex, Charlie, Doug, Evan

Count: 2 out of 6 human issues (33.3%) were missed by all reviewers.

### Unique finds per reviewer

A "unique find" is a human issue covered by exactly one reviewer while all others missed it.

- Human Issue #4 (SIRV2 dt^2 coding bug): covered only by Alex (Charlie, Doug, Evan missed it)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer (as Major or Minor) that the human did not mention:

1. Accumulator H tracks recoveries (dN_IR) instead of new infections (dN_SI) — raised as Major by all four reviewers (Alex finding 1, Charlie finding 1, Doug finding 1, Evan 21.03.4)
2. Prediction simulation uses initial-guess parameters instead of MLE — raised as Major by all four reviewers (Alex finding 2, Charlie finding 3, Doug finding 3, Evan 21.03.3)

Count: 2 universal AI-only flags.
