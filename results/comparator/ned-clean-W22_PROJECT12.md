# Ned-Clean Analysis — W22 Project 12

---

## Human Issues

1. For the mechanistic model, one either has to analyze cases summed over weeks or to explicitly model the weekly periodicity.
2. Compare the mechanistic fit likelihoods to the ARMA benchmark.
3. For the ADF test, it is best not to present unprocessed R output. Better still, one could avoid the test entirely. ADF is only a test against a unit root hypothesis. Simply plotting the data would be better to detect a wider range of phenomena that might suggest a nonstationary model.
4. In the ARIMA model for the full data, the formula of the ARIMA is wrong. It should be the correct mathematical formula.
5. Fig 14 shows clearly how the initial values are inappropriately specified for the model, and also how the model fails to capture the weekday effect in the data. The model has to compensate for these shortcomings by having a large amount of noise.
6. The fixed choices E_0=30000 and I_0=15000 are not discussed — one must go to the code to find them. However, these unsuccessful choices critically affect all the other model-based analysis. Better to estimate them from data.
7. The model has measurement overdispersion, but no process noise.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Weekly seasonality identified but never modeled")
- Human Issue #2: covered (matched by finding: "No comparison of SEIR likelihood to a null or baseline")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "E and I initial conditions fixed at arbitrary values")
- Human Issue #7: missed

**Findings classification:**
- Issue 1 (beta switch t>33 hardcoded): A — unjustified hard-coded transmission switch threshold, human did not raise
- Issue 2 (mu_EI/mu_IR fixed, inadequately justified): A — fixed transition rates not estimated, human did not raise
- Issue 3 (dmeas/rmeas inconsistency): A — measurement model code inconsistency, human did not raise
- Issue 4 (global search box excludes local search space): A — search box miscalibration, human did not raise
- Issue 5 (particle filter SE very large at initial guess): A — large Monte Carlo SE at initial values, human did not raise
- Issue 6 (no profile likelihoods or CIs): A — no uncertainty quantification for SEIR parameters, human did not raise
- Issue 7 (local search Nmif=50 insufficient): A — insufficient IF2 iterations, human did not raise
- Issue 8 (ARIMA conflates selection with validation): C — ARIMA diagnostics failure not addressed, human did not raise
- Issue 9 (weekly seasonality identified but never modeled): D — weekly/weekday periodicity not handled in either model (matches Human Issue #1)
- Issue 10 (E and I initial conditions fixed at arbitrary values): D — E=30000 and I=15000 unjustified (matches Human Issue #6)
- Issue 11 (incomplete sentence in text): C — proofreading artifact, human did not raise
- Issue 12 (Figure 10 caption incorrect): C — mislabeled figure caption, human did not raise
- Issue 13 (global search filter trivially permissive): C — loglik filter threshold of 100000 is useless, human did not raise
- Issue 14 (data read from two sources inconsistently): C — dual data source reproducibility concern, human did not raise
- Issue 15 (no comparison of SEIR likelihood to null/baseline): D — no ARMA benchmark comparison (matches Human Issue #2)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No benchmark comparison to a non-mechanistic model")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Initial compartment values E=30000 and I=15000 fixed without justification")
- Human Issue #7: missed

**Findings classification:**
- Issue 1 (dmeas/rmeas inconsistent variance formulas): A — measurement model code inconsistency, human did not raise
- Issue 2 (H accumulates recoveries dN_IR, not new cases): A — structural accumulator misspecification, human did not raise
- Issue 3 (no profile likelihood computed): A — no identifiability analysis or CIs, human did not raise
- Issue 4 (global search uses only Nmif=50, insufficient computation): A — inadequate IF2 computational budget, human did not raise
- Issue 5 (mu_EI and mu_IR fixed without sensitivity analysis): A — fixed transition rates not evaluated, human did not raise
- Issue 6 (no benchmark comparison to non-mechanistic model): B — no ARMA benchmark (matches Human Issue #2)
- Issue 7 (beta switch t=33 hardcoded without justification): A — unjustified structural break, human did not raise
- Issue 8 (normal approximation for count data without checking): C — distributional mismatch for count data, human did not raise
- Issue 9 (Figure 10 label incorrect): C — mislabeled figure caption, human did not raise
- Issue 10 (scatterplot filter uses loglik > max - 100000): C — trivially permissive filter, human did not raise
- Issue 11 (initial compartment values E=30000, I=15000 fixed without justification): D — E_0/I_0 unjustified (matches Human Issue #6)
- Issue 12 (ACF plots labeled "Autocovariance function" incorrectly): C — terminology error, human did not raise
- Issue 13 (incomplete sentence in Omicron seasonality section): C — proofreading artifact, human did not raise
- Issue 14 (ARIMA model selection without cross-validation): C — ARIMA(5,1,5) selection inadequately validated, human did not raise
- Issue 15 (conclusion overstates SEIR model success): C — unsupported claim of superiority, human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No benchmark comparison between SEIR and non-mechanistic baseline")
- Human Issue #3: covered (matched by finding: "Stationarity test conclusion is incorrectly framed")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Issue 1 (global search initialized from previous mif2 result): A — global search anti-pattern, human did not raise
- Issue 2 (MLE for beta1 outside global search box): A — binding box constraint on beta1, human did not raise
- Issue 3 (rho concentrates at boundary rho→1): A — boundary MLE signals misspecification, human did not raise
- Issue 4 (dmeas/rmeas inconsistent variance formulas): A — measurement model code inconsistency, human did not raise
- Issue 5 (no benchmark comparison between SEIR and non-mechanistic baseline): B — no ARMA benchmark (matches Human Issue #2)
- Issue 6 (no profile likelihoods; identifiability unassessed): A — no uncertainty quantification, human did not raise
- Issue 7 (accumulator H tracks recoveries, not new detected cases): A — structural accumulator misspecification, human did not raise
- Issue 8 (hard-coded breakpoint for beta transition t>33): C — unjustified structural break, human did not raise
- Issue 9 (stationarity test conclusion incorrectly framed): D — ADF test misuse and incorrect framing (matches Human Issue #3)
- Issue 10 (AIC table caption mislabels Figure 10): C — mislabeled figure caption, human did not raise
- Issue 11 (particle filter SE large at initial parameter values): C — large Monte Carlo SE at initial values, human did not raise
- Issue 12 (same ARIMA order for both datasets without discussion): C — ARIMA(5,1,5) for both windows not discussed, human did not raise
- Issue 13 (no model diagnostics beyond pairs scatter plot): C — insufficient particle filter diagnostics, human did not raise
- Issue 14 (mu_EI and mu_IR fixed without sensitivity analysis): C — fixed transition rates not evaluated, human did not raise
- Issue 15 (no forecast or prediction from fitted model): C — no probabilistic forecast, human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.12.1 Missing benchmark comparison")
- Human Issue #3: covered (matched by finding: "22.12.6 ADF test applied to differenced series")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Initial compartment values E=30000, I=15000 not justified")
- Human Issue #7: missed

**Findings classification:**
- 22.12.1 (missing benchmark comparison): B — no ARMA benchmark comparison (matches Human Issue #2)
- 22.12.2 (measurement model inconsistency dmeas/rmeas): A — measurement model code inconsistency, human did not raise
- 22.12.3 (no profile likelihoods or CIs): A — no uncertainty quantification, human did not raise
- 22.12.7 (fixed mu_EI and mu_IR without sensitivity analysis): A — fixed transition rates not evaluated, human did not raise
- 22.12.5 (potential under-convergence in global search): C — insufficient Nmif iterations, human did not raise
- 22.12.6 (ADF test applied to differenced series): D — ADF test methodological issue (matches Human Issue #3)
- ESS collapse at end of time series: C — particle filter collapse near t=120-134, human did not raise
- Hard-coded regime change at t=33: C — unjustified structural break, human did not raise
- Initial compartment values E=30000, I=15000 not justified: D — E_0/I_0 unjustified (matches Human Issue #6)
- rho at boundary signals potential misspecification: C — boundary MLE signals misspecification, human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 6 | 3 |
| B (AI major, human also found) | 0 | 1 | 1 | 1 |
| C (AI minor, human missed) | 5 | 7 | 7 | 4 |
| D (AI minor, human also found) | 3 | 1 | 1 | 2 |
| E (Human found, AI missed) | 4 | 5 | 5 | 4 |

---

## Per-Reviewer Metrics

| Reviewer | B | D | E | Human Recall (B+D)/(B+D+E) | A | C | AI-Unique Rate (A+C)/(A+B+C+D) |
|----------|--:|--:|--:|---------------------------:|--:|--:|--------------------------------:|
| Alex | 0 | 3 | 4 | 3/7 = 0.43 | 7 | 5 | 12/15 = 0.80 |
| Charlie | 1 | 1 | 5 | 2/7 = 0.29 | 6 | 7 | 13/15 = 0.87 |
| Doug | 1 | 1 | 5 | 2/7 = 0.29 | 6 | 7 | 13/15 = 0.87 |
| Evan | 1 | 2 | 4 | 3/7 = 0.43 | 3 | 4 | 7/10 = 0.70 |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Weekly periodicity must be modeled or cases summed over weeks in the mechanistic model — missed by all 4 reviewers
- Human Issue #4: ARIMA formula in the text is wrong — missed by all 4 reviewers
- Human Issue #5: Fig 14 shows initial values inappropriately specified; model fails to capture weekday effect; model compensates with large noise — missed by all 4 reviewers
- Human Issue #7: The model has measurement overdispersion but no process noise — missed by all 4 reviewers

Count: 4 out of 7 human issues (4/7 = 0.57) were missed by every reviewer.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3 (ADF test misuse): covered by Doug (finding: stationarity test incorrectly framed) and Evan (finding: ADF test applied to differenced series) — covered by 2 reviewers, not a unique find for any single reviewer.
- Human Issue #2 (ARMA benchmark comparison): covered by all four reviewers — not a unique find.
- Human Issue #6 (E_0=30000, I_0=15000 not discussed): covered by Alex, Charlie, and Evan — not a unique find.

No human issue was covered by exactly one reviewer. Unique find count for each reviewer is 0.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

- dmeasure and rmeasure use inconsistent variance formulas: raised by Alex (Major), Charlie (Major), Doug (Major), Evan (Major) — all 4 reviewers flagged this; human did not mention it.
- No profile likelihoods computed for any parameter: raised by Alex (Major), Charlie (Major), Doug (Major), Evan (Major) — all 4 reviewers flagged this; human did not mention it.
- mu_EI and mu_IR fixed without sensitivity analysis: raised by Alex (Major), Charlie (Major), Doug (Minor), Evan (Major) — all 4 reviewers flagged this; human did not mention it (human issue #7 is about process noise, not the fixed transition rates).

Count: 3 universal AI-only flags.
