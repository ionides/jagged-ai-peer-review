# Ned-Clean Analysis — W25 Project 07

---

## Human Issues

1. SARIMA analysis would be better performed on a log scale.
2. The residuals from the SARIMA model are described as "white noise overall" — this is a weak interpretation. The tails are substantially longer than normal, one point could be considered an outlier, and the residuals have a slow trend.
3. Infectious disease data usually fits linear Gaussian assumptions better after a log transform; the team should carry out their linear data analysis on the log scale.
4. It would be worth understanding the parameter estimates for biological interpretation — how do they fit with known dengue epidemiology? The value rho=4×10^-5 might be a useful clue.
5. The two-year data period is limited; the full 2010–2023 dataset (perhaps aggregated to months) would give better understanding of inter-annual dynamics.
6. It is incorrect that "the oscillating pattern displayed in the ACF plots supports that the data is non-stationary."
7. An unclear assertion about model selection: SARIMA(1,0,1)×(0,0,1) has the same complexity and better AIC than the chosen model, so the reasoning is unclear.
8. The dataset contains "Travel-related cases," so modeling U.S. cases with an SIR-type model may be hard to interpret — the pattern could be driven by imported cases rather than local transmission.
9. The model supposes N=3.2×10^6 Americans are at risk — where does this figure come from?
10. Discussion of the homogeneous mixing assumption behind compartment models is requested.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF Interpretation Error — Oscillating Pattern Does Not Indicate Non-Stationarity Per Se")
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "Fundamental Mechanistic Mismatch: SIR-type Models Applied to Imported Case Data")
- Human Issue #9: covered (matched by finding: "Implausible Population Size N=4e9 in SIRS, Inconsistency Across Models")
- Human Issue #10: missed

**Findings classification:**
- Major#1 (SIR models applied to imported case data): B — matches Human Issue #8
- Major#2 (inconsistent data preparation across three models): A
- Major#3 (no profile likelihood or confidence intervals): A
- Major#4 (pandemic switch at week 29 poorly motivated): A
- Major#5 (implausible N=4e9/N=3.2M, inconsistency across models): B — matches Human Issue #9
- Major#6 (H accumulates recoveries, mislabeled as cumulative incidence): A
- Major#7 (SEIR global search claims 200 points but only 100 specified): A
- Major#8 (SEIR local search uses ncpu instead of Nlocal): A
- Minor#9 (mu_IR=0.8 implies unrealistically short infectious period): C
- Minor#10 (no ACF of SARIMA residuals — incomplete diagnostics): C
- Minor#11 (SARIMA period 53 vs POMP models period 52): C
- Minor#12 (no ODE formulation or R0 derivation for SEIR): C
- Minor#13 (SIRS global search loglik not explicitly reported): C
- Minor#14 (k fixed in SEIR but estimated in SIRS — non-comparable): C
- Minor#15 (oscillating ACF does not indicate non-stationarity): D — matches Human Issue #6

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
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
- Human Issue #6: covered (matched by finding: "ACF analysis concludes from oscillating ACF that series is non-stationary, but oscillating ACF is consistent with stationary seasonal AR process")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Biologically Implausible and Inconsistent Population Parameters — N=4e9 and N=3.2M unjustified")
- Human Issue #10: missed

**Findings classification:**
- Major#1 (no profile likelihoods or confidence intervals): A
- Major#2 (biologically implausible and inconsistent population parameters): B — matches Human Issue #9
- Major#3 (SIRS and SEIR models fit to different data): A
- Major#4 (informal and incomplete model comparison): A
- Major#5 (global search severely underpowered for SIRS — Nglobal=20): A
- Major#6 (SEIR particle filter diagnostics missing): A
- Major#7 (k fixed at 10 in SEIR not justified): A
- Major#8 (pandemic switch not scientifically motivated): A
- Minor: SARIMA log-likelihood reported as "approximately -445" without precise value: C
- Minor: SARIMA framing as benchmark confusingly stated: C
- Minor: run_level declared twice in script: C
- Minor: %dopar% vs %dofuture% mixing inconsistency: C
- Minor: color=531 in ggplot interpreted as numeric code: C
- Minor: SARIMA d=0 not justified; d=1 models not considered: C
- Minor: ACF oscillating pattern wrongly concluded as non-stationarity: D — matches Human Issue #6
- Minor: SEIR initial conditions fix E=10, I=70 without estimation or sensitivity: C
- Minor: ChatGPT disclosure lacks validation description: C
- Minor: theme ordering resets legend position (no effect): C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Reporting rate rho fixed at biologically implausible values without justification")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF analysis conclusion conflates pattern with non-stationarity")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "SEIR population size N implausibly small by two orders of magnitude")
- Human Issue #10: missed

**Findings classification:**
- Major#1 (SEIR model fitted on different dataset than SIRS): A
- Major#2 (global searches anchored to local-search mif2 chain — anti-pattern): A
- Major#3 (SEIR accumulator tracks recoveries, not new cases): A
- Major#4 (SEIR population size N=3.2M implausibly small): B — matches Human Issue #9
- Major#5 (invalid direct comparison of SARIMA and POMP log-likelihoods): A
- Major#6 (no profile likelihoods for any parameter): A
- Major#7 (rho fixed at biologically implausible value in SIRS; SEIR rho≈0.9 contradicts it): B — matches Human Issue #4
- Minor#8 (SEIR local search uses nbrOfWorkers() instead of Nlocal): C
- Minor#9 (SEIR simulations hardcode k=10 instead of optimized value): C
- Minor#10 (no ESS/pfilter diagnostic for SEIR before local search): C
- Minor#11 (SIRS run-level switch has 4 values for some parameters, 3 for others): C
- Minor#12 (SIRS model diagnostics beyond ESS missing — conditional log-likelihood not discussed): C
- Minor#13 (seasonal amplitude c logit-transformed, upper bound issue): C
- Minor#14 (no out-of-sample or forecasting evaluation): C
- Minor#15 (ACF analysis conclusion conflates oscillating pattern with non-stationarity): D — matches Human Issue #6

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Degenerate reporting rate rho≈0 in SIRS is unaddressed — rho=4e-5 effectively zero, not discussed")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ACF non-stationarity claim inconsistent with d=0 choice")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- 25.07.7 (SIRS model lacks stochastic transitions and measurement model): A
- 25.07.1 (SIRS log-likelihood not verified by replicated pfilter): A
- 25.07.2 (SEIR global search reveals severe identifiability failure; MLE biologically implausible — mu_IR=35.6): A
- 25.07.3 (no parameter uncertainty quantification for either model): A
- 25.07.4 (convergence not achieved in SIRS or SEIR local searches): A
- 25.07.8 (degenerate reporting rate rho≈0 in SIRS unaddressed): B — matches Human Issue #4
- 25.07.6 (pandemic switch unjustified and data-adaptive): A
- 25.07.I (section heading misspelling: "Explanatory" vs "Exploratory"): C
- 25.07.M1 (inconsistent seasonal period: 52 in POMP models vs 53 in SARIMA): C
- 25.07.M2 (ACF non-stationarity claim inconsistent with d=0 choice): D — matches Human Issue #6
- 25.07.M3 (large sma1 standard error not acknowledged): C
- 25.07.M4 (SEIR lacks ESS and filter diagnostic plots): C
- 25.07.M5 (ambiguous "2,000 particle-filtering replicates" in conclusion): C
- 25.07.M6 (no code or data archive): C
- 25.07.M7 (AI tool disclosure needs more specificity): C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 7 | 5 | 6 |
| B (AI major, human also found) | 2 | 1 | 2 | 1 |
| C (AI minor, human missed) | 6 | 9 | 7 | 7 |
| D (AI minor, human also found) | 1 | 1 | 1 | 1 |
| E (Human found, AI missed) | 7 | 8 | 7 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex:**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+7) = 3/10 = **0.30**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+6) / (6+2+6+1) = 12/15 = **0.80**

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+8) = 2/10 = **0.20**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+9) / (7+1+9+1) = 16/18 = **0.89**

**Doug:**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+7) = 3/10 = **0.30**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+7) / (5+2+7+1) = 12/15 = **0.80**

**Evan:**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+8) = 2/10 = **0.20**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+1+7+1) = 13/15 = **0.87**

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- **HI#1:** SARIMA analysis would be better on a log scale. (4 out of 4 reviewers missed)
- **HI#2:** Weak residual interpretation — tails longer than normal, outlier, slow trend. (4 out of 4 missed)
- **HI#3:** Log transform needed for linear data analysis. (4 out of 4 missed)
- **HI#5:** Two-year data period too limited; 2010–2023 dataset would improve inter-annual understanding. (4 out of 4 missed)
- **HI#7:** SARIMA model selection reasoning is unclear — SARIMA(1,0,1)×(0,0,1) has same complexity and better AIC. (4 out of 4 missed)
- **HI#10:** Discussion of homogeneous mixing assumption requested. (4 out of 4 missed)

Total consensus misses: 6 out of 10 human issues (60%).

### Unique finds per reviewer

Issues covered by exactly one reviewer that all others missed:

- **Alex only:** HI#8 (travel-related cases / SIR model mismatch — imported vs local transmission). All others missed.
- **Charlie only:** none
- **Doug only:** none
- **Evan only:** none

Note: HI#4 (biological interpretation of parameters / rho=4e-5) was covered by Doug and Evan but not Alex or Charlie. HI#6 (ACF non-stationarity error) was covered by all four reviewers. HI#9 (N=3.2×10^6 unjustified) was covered by Alex, Charlie, and Doug but not Evan.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major or Minor by every reviewer that the human did not mention:

All four reviewers raised the following concerns that the human did not:

- **No profile likelihoods / no confidence intervals for parameters** — raised as Major by Alex (Major#3), Charlie (Major#1), Doug (Major#6), Evan (25.07.3). (4 out of 4)
- **SEIR particle filter diagnostics missing (no ESS for SEIR)** — raised by Alex (Minor#10 — no ACF, related), Charlie (Major#6), Doug (Minor#10), Evan (25.07.M4). (4 out of 4, though Alex's framing differs slightly)
- **"Pandemic switch" at week 29 is unjustified** — raised as Major by Alex (Major#4), Charlie (Major#8), Evan (25.07.6). Doug does not raise this explicitly. (3 out of 4)
- **SIRS and SEIR models fit to different data** — raised as Major by Alex (Major#2), Charlie (Major#3), Doug (Major#1). Evan does not raise this. (3 out of 4)
- **ACF non-stationarity error** — raised by all four (Alex Minor#15, Charlie Minor, Doug Minor#15, Evan 25.07.M2). However, this matches Human Issue #6, so it is not AI-only.

Strict universal AI-only (raised by all 4 and not in human issues):

- **No profile likelihoods / confidence intervals** — 4 out of 4 reviewers. Count: 1 universal AI-only flag.
