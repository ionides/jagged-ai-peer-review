# Ned-Clean Analysis — W22 Project 09

---

## Human Issues

1. Further diagnostic analysis could investigate which data points are problematic for the mechanistic model to explain (e.g., using effective sample size).
2. A bug has led to a collection of identical points reported for the global search.
3. The conclusion b2 > b1 may not be statistically significant; a profile likelihood or likelihood ratio test should be used.
4. The initial values E0 = 30, I0 = 30 may be questionable; they could be parameterized similarly to S as in lecture notes Ch 17.
5. The local search shows issues: the log likelihood diverges with iterations; possible investigation via particle filter diagnostics and ESS; problematic model assumptions could be state initializations and/or process overdispersion; reducing random walk size may help.
6. The report does not specify the measurement model.
7. The report closely follows a previous project (cited); less is done here (no profile), conclusions are less carefully drawn, and the model is less fully described (measurement model omitted).
8. The style of references is informal.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No profile likelihood or confidence intervals for any parameter")
- Human Issue #4: covered (matched by finding: "Initial exposed population E=30 is hardcoded and not justified")
- Human Issue #5: covered (matched by finding: "Likelihood non-convergence acknowledged but not addressed")
- Human Issue #6: covered (matched by finding: "Measurement model uses a Normal approximation; text does not specify the distribution, only the moments")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (H accumulator tracks recoveries not new infections): A — structural mis-specification of accumulator; human did not raise
- Major 2 (SEIR loglik outperformed by SARIMA): A — loglik gap flagged as under-discussed; human did not raise as standalone issue
- Major 3 (mu_IR fixed without justification): A — recovery rate fixed without citation or sensitivity; human did not raise
- Major 4 (No profile likelihood or confidence intervals): B — matches Human Issue #3
- Major 5 (Likelihood non-convergence not addressed): B — matches Human Issue #5
- Major 6 (Normal measurement model allows negative counts): B — matches Human Issue #6
- Moderate 7 (Global search single mif2 pass per starting point): A — inadequate convergence for global search; human did not raise
- Moderate 8 (Covariate split date inconsistent with code): A — date arithmetic error; human did not raise
- Moderate 9 (rho=0.9 initial guess implausibly high): A — biologically implausible reporting rate; human did not raise
- Moderate 10 (ARMA loglik correction and benchmark comparison flawed): A — comparison validity questioned; human did not raise
- Moderate 11 (E=30 hardcoded and not justified): D — matches Human Issue #4
- Moderate 12 (EDA caption text repeated verbatim): C — editing error; human did not raise
- Minor 13 (cahce=TRUE typo): C — misspelling in chunk headers; human did not raise
- Minor 14 (mu_SI notation incorrect for S-to-E rate): C — notational ambiguity; human did not raise
- Minor 15 (Vaccination and waning immunity ignored): C — model limitation not discussed; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "No Model Diagnostics Beyond Visual Simulation Comparison" — mentions ESS traces)
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No Profile Likelihoods for Any Parameter")
- Human Issue #4: covered (matched by finding: "Initial Conditions: E and I Fixed Without Justification")
- Human Issue #5: covered (matched by finding: "Non-Monotone Likelihood During Local Search Is Noted But Not Addressed")
- Human Issue #6: covered (matched by finding: "Measurement Model Uses Normal Approximation Instead of Count Distribution; text specifies only moments")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (Global search single mif2 pass): A — convergence inadequacy in global search; human did not raise
- Major 2 (mu_IR fixed without biological justification): A — unjustified fixed parameter; human did not raise
- Major 3 (No profile likelihoods for any parameter): B — matches Human Issue #3
- Major 4 (SARIMA loglik comparison Jacobian issue): A — Jacobian correction noted as actually correct but gap is understated; human did not raise
- Major 5 (Non-monotone likelihood in local search not addressed): B — matches Human Issue #5
- Major 6 (Normal approximation measurement model): B — matches Human Issue #6
- Major 7 (H accumulator tracks recoveries not new cases): A — structural accumulator error; human did not raise
- Minor 8 (Initial conditions E/I fixed without justification): D — matches Human Issue #4
- Minor 9 (Benchmark gap undercharacterized as "slightly higher"): C — magnitude of loglik gap understated; human did not raise this as standalone issue
- Minor 10 (Global search box for b1/b2 includes zero): C — degenerate lower bound; human did not raise
- Minor 11 (No model diagnostics beyond visual simulation): D — matches Human Issue #1
- Minor 12 (Covariate split hard-coded without robustness check): C — split date sensitivity not explored; human did not raise
- Minor 13 (Local search uses only 20 replicates from same start): C — limited local search exploration; human did not raise
- Minor 14 (Missing sessionInfo and package version documentation): C — reproducibility gap; human did not raise
- Minor 15 (Caption for Figure 1 repeated verbatim): C — copy-paste error; human did not raise

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
- Human Issue #1: covered (matched by finding: "No ESS monitoring reported")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No Profile Likelihoods Computed; Parameter Identifiability Unassessed")
- Human Issue #4: covered (matched by finding: "Initial conditions inadequately justified")
- Human Issue #5: covered (matched by finding: "Self-Diagnosed Non-Convergence Used to Draw Substantive Conclusions")
- Human Issue #6: covered (matched by finding: "Measurement Model Uses Normal Approximation Without Justification for Count Data")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (Self-diagnosed non-convergence used to draw conclusions): B — matches Human Issue #5
- Major 2 (Global search initialized from previous mif2 result): A — faulty global search init pattern; human did not raise
- Major 3 (Invalid direct loglik comparison SARIMA vs SEIR): A — comparison on incompatible scales; human did not raise
- Major 4 (Accumulator tracks recoveries not infections): A — structural accumulator error; human did not raise
- Major 5 (Normal approximation not justified for count data): B — matches Human Issue #6
- Major 6 (SARIMA back-transformation mathematically unjustified): A — Jacobian correction invalid; human did not raise (note: Doug and Major 3 both address SARIMA comparison; assigned separately)
- Major 7 (No profile likelihoods; identifiability unassessed): B — matches Human Issue #3
- Major 8 (Negative binomial benchmark not time-resolved): A — benchmark choice inadequate; human did not raise
- Minor: Fixed mu_IR without sensitivity analysis: C — unjustified fixed parameter; human did not raise
- Minor: Initial conditions inadequately justified (E=30, I=30): D — matches Human Issue #4
- Minor: No convergence traces for global search: C — diagnostic gap; human did not raise as distinct from local search issue
- Minor: Simulation plot shows excessive variance without quantitative assessment: C — visual-only assessment insufficient; human did not raise
- Minor: Duplicate description of Figure 1 text: C — copy-paste error; human did not raise
- Minor: covariate_table counts not verified (off-by-one): C — potential silent mismatch; human did not raise
- Minor: No reproducibility information (sessionInfo): C — version documentation absent; human did not raise
- Minor: No ESS monitoring reported: D — matches Human Issue #1

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ESS Not Monitored")
- Human Issue #2: covered (matched by finding: "Duplicate Rows in Global Search Table and Loglik Discrepancy")
- Human Issue #3: covered (matched by finding: "Parameter Non-Identifiability: b2 and mu_EI — conclusion that b2 > b1 cannot be supported")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Local Search Non-Convergence Seeding Global Search")
- Human Issue #6: covered (matched by finding: "Gaussian Measurement Model and Negative Count Clamping — choice not justified in text")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- ID 22.09.1 (Duplicate rows in global search; loglik discrepancy): B — matches Human Issue #2
- ID 22.09.2 (Local search non-convergence seeding global search): B — matches Human Issue #5
- ID 22.09.3 (Parameter non-identifiability: b2 and mu_EI): B — matches Human Issue #3
- ID 22.09.4 (Implausible reporting rate rho ~ 0.97): A — biologically implausible rho; human did not raise
- ID 22.09.5 (H accumulator semantics — recoveries not infections): A — structural accumulator error; human did not raise
- ID 22.09.6 (Large initial pfilter Monte Carlo SE not discussed): C — numerical diagnostic gap; human did not raise
- ID 22.09.7 (Gaussian measurement model and negative count clamping): D — matches Human Issue #6
- ID 22.09.8 (SARIMA likelihood scale note): C — comparison scale subtlety; human did not raise
- ID 22.09.9 (ESS not monitored): D — matches Human Issue #1
- ID 22.09.10 (mu_IR fixed without citation): C — unjustified fixed parameter; human did not raise
- ID 22.09.11 (Extreme simulation variance in Figure 8): C — large spread not discussed; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 4 | 5 | 2 |
| B (AI major, human also found) | 3 | 3 | 3 | 3 |
| C (AI minor, human missed) | 4 | 6 | 6 | 4 |
| D (AI minor, human also found) | 1 | 2 | 2 | 2 |
| E (Human found, AI missed) | 4 | 3 | 3 | 3 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (3+1) / (3+1+4) = 4/8 = 0.500
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+4) / (7+3+4+1) = 11/15 = 0.733

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (3+2) / (3+2+3) = 5/8 = 0.625
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+6) / (4+3+6+2) = 10/15 = 0.667

**Doug**
- Human Recall = (B+D) / (B+D+E) = (3+2) / (3+2+3) = 5/8 = 0.625
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+6) / (5+3+6+2) = 11/16 = 0.688

**Evan**
- Human Recall = (B+D) / (B+D+E) = (3+2) / (3+2+3) = 5/8 = 0.625
- AI-Unique Rate = (A+C) / (A+B+C+D) = (2+4) / (2+3+4+2) = 6/11 = 0.545

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer:

- Human Issue #7: The report closely follows a previous project (cited); less is done here (no profile), conclusions are less carefully drawn, model less fully described.
- Human Issue #8: The style of references is informal.

Count: 2 out of 8 human issues (25%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2 (Bug leading to identical points in global search): covered only by Evan (ID 22.09.1). Alex, Charlie, and Doug missed it.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

1. H accumulator variable tracks recoveries (dN_IR) rather than new infections (dN_SE or dN_EI) — raised as Major by Alex, Charlie, Doug, and Evan.
2. mu_IR fixed without citation or sensitivity analysis — raised by all four reviewers (Major by Alex and Charlie; Minor by Doug and Evan).
3. SARIMA log-likelihood comparison is methodologically problematic (incompatible scales, invalid Jacobian, or gap severely understated) — raised by all four reviewers.

Count: 3 universal AI-only flags.
