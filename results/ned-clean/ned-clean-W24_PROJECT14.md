# Ned-Clean Analysis — W24 Project 14

---

## Human Issues

1. The background section is missing references.
2. Data whose scale varies considerably over time are often best plotted on a log scale.
3. Some ARIMA code is apparently taken from a midterm project without credit.
4. Regression with ARMA errors might be more insightful than differencing and fitting ARIMA.
5. The SEIR model equations do not perfectly match the implemented equations in the code.
6. The parameter values given as the result of the local search are the starting point for that search (convergence not established; better likelihood values obtained by end of search).
7. The modeling and analysis is similar to but inferior to a previous STATS 531 project on TB; the prior work should be acknowledged more fully.
8. There is an inconsistency in log-likelihood values reported in the text vs. code outputs (-628.8447 and -629.6903).
9. SEIR treats S as the entire population, which may be problematic for TB (only those with specific risk factors are typically at risk).
10. The report does not discuss specification and estimation of initial state values.
11. The model-based assessment does not get beyond basic iterated filtering to global maximization or profiles.
12. Adding a diagram for the process model would help readers.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: Major 3 — stochastic model equations inconsistent with code)
- Human Issue #6: covered (matched by finding: Major 1 — no global search, single local run, convergence not established)
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: Major 7 — no likelihood profile, confidence intervals, or uncertainty quantification)
- Human Issue #12: covered (matched by finding: Minor 9 — broken image path; diagram not visible to readers)

**Findings classification:**
- Major 1 (no global parameter search): B — matches Human Issue #6
- Major 2 (H accumulates recoveries not infections): A — H compartment semantic mismatch
- Major 3 (stochastic equations inconsistent with code): B — matches Human Issue #5
- Major 4 (population fixed at 2023 value): A — systematic bias in transmission parameters
- Major 5 (implausible biological parameter values not validated): A — mu_EI ~3 days, mu_RS ~11 days
- Major 6 (H not reset / accumvar propagation of error from Major 2): A — elaboration of accumvar semantic mismatch
- Major 7 (no profile likelihoods, no CI, no uncertainty quantification): B — matches Human Issue #11
- Major 8 (ARIMA conflates raw case count with rate; caption inconsistency): A — ARIMA applied to tb_num but caption says "incidence rate"
- Minor 9 (broken image path; diagram not visible): D — matches Human Issue #12
- Minor 10 (undefined simulation_arima / simulation_sarima functions): C — undefined helper functions
- Minor 11 (incorrect Fisher CI formula: variance used instead of SD): C — diag(var.coef) instead of sqrt(diag(var.coef))
- Minor 12 (convergence diagnostics shown but not interpreted): C — plot(mif_out) not discussed
- Minor 13 (simulation plot lacks legend and data reference): C — actual data vs simulated not clearly labeled
- Minor 14 (duplicate and redundant code blocks): C — seir_step defined twice
- Minor 15 (anomalous/missing rows in data not addressed): C — "1974 2" and "1979 3" year fields silently dropped

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: Minor 10 — ARIMA fitted to raw unlogged counts; log transform preferable for data with large dynamic range)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: Major 3 — model equations inconsistent with code)
- Human Issue #6: covered (matched by finding: Major 1 — no global search, no convergence evidence)
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: Minor 15 — no assessment of initial condition sensitivity; initial proportions not discussed for plausibility)
- Human Issue #11: covered (matched by finding: Major 4 — no profile likelihoods or parameter identifiability assessment)
- Human Issue #12: covered (matched by finding: Major 6 — hardcoded absolute path; SEIRS diagram cannot render for any reader)

**Findings classification:**
- Major 1 (no global search, no convergence evidence): B — matches Human Issue #6
- Major 2 (no non-mechanistic benchmark comparison): A — ARIMA and POMP never compared quantitatively
- Major 3 (model equations inconsistent with code): B — matches Human Issue #5
- Major 4 (no profile likelihoods or identifiability assessment): B — matches Human Issue #11
- Major 5 (ARIMA diagnostic function defined but never called): A — build_and_diagnose_model unused
- Major 6 (hardcoded absolute path breaks reproducibility): B — matches Human Issue #12
- Major 7 (simulation_arima and simulation_sarima undefined): A — undefined helper functions
- Major 8 (H compartment accumulates recoveries not infections): A — accumvar semantic mismatch
- Minor 9 (single mif2 convergence trace shown without discussion): C — implausible parameter values not flagged
- Minor 10 (ARIMA caption mismatch + log transform not considered): D — matches Human Issue #2
- Minor 11 (hardcoded absolute path — duplicate of Major 6): C — same image path issue already captured in Major 6
- Minor 12 (ARIMA selection based on AIC alone; smallest root 1.05): C — no ARIMA adequacy checks shown
- Minor 13 (no goodness-of-fit quantification beyond single log-likelihood): C — single log-likelihood without context
- Minor 14 (ESS not monitored during particle filtering): C — no ESS diagnostics reported
- Minor 15 (no assessment of initial condition sensitivity): D — matches Human Issue #10

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: Minor 10 — ARIMA fitted to unlogged raw counts; log transform preferable)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: Major 5 — force-of-infection equation inconsistent between text and Csnippet)
- Human Issue #6: covered (matched by finding: Major 2 — no global parameter search; single mif2 run from one starting point)
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: Minor 15 — no assessment of initial condition sensitivity; plausibility of S_0, E_0, I_0, R_0 not discussed)
- Human Issue #11: covered (matched by finding: Major 4 — no profile likelihoods or confidence intervals for any parameter)
- Human Issue #12: covered (matched by finding: Minor 11 — hardcoded absolute path; diagram not visible)

**Findings classification:**
- Major 1 (H accumulates recoveries not infections): A — dN_IR used instead of dN_SE or dN_EI
- Major 2 (no global parameter search; estimates unreliable): B — matches Human Issue #6
- Major 3 (no benchmark comparison against non-mechanistic model): A — ARIMA and POMP never compared
- Major 4 (no profile likelihoods or confidence intervals): B — matches Human Issue #11
- Major 5 (force-of-infection equation inconsistent between text and Csnippet): B — matches Human Issue #5
- Major 6 (fixed population N = 333,000,000 throughout 1953-2020): A — systematic bias; population was ~160M in 1953
- Major 7 (intermediate R model uses Rate, final Csnippet uses Number — measurement model duplication): A — Rate vs Number mismatch between code versions
- Major 8 (discrete stochastic transition equations inconsistent with ODE): A — written difference equations do not match Csnippet implementation
- Minor 9 (single mif2 convergence trace without discussion): C — implausible mu_EI and mu_RS not flagged
- Minor 10 (ARIMA caption mismatch + log transform not considered): D — matches Human Issue #2
- Minor 11 (hardcoded absolute path; diagram not portable): D — matches Human Issue #12
- Minor 12 (ARIMA model selection AIC alone; smallest root 1.05): C — no ARIMA adequacy checks; near unit-circle root
- Minor 13 (no goodness-of-fit quantification for POMP beyond single log-likelihood): C — no AIC, no comparison to ARIMA likelihood
- Minor 14 (ESS not monitored during particle filtering): C — no ESS diagnostics
- Minor 15 (no assessment of initial condition sensitivity): D — matches Human Issue #10

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: 24.14.2 — single mif2 run; convergence not established)
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: 24.14.1 — mif2 log-likelihood reported without replicated pfilter; proper likelihood evaluation not performed)
- Human Issue #12: missed

**Findings classification:**
- 24.14.1 (mif2 log-likelihood reported without replicated pfilter): B — matches Human Issue #11
- 24.14.2 (single mif2 run; convergence not established): B — matches Human Issue #6
- 24.14.3 (simulations inconsistent with data by two orders of magnitude): A — simulated trajectories reach 600,000+ vs observed <30,000
- 24.14.5 (no quantitative benchmark comparison): A — ARIMA and POMP log-likelihoods never compared
- 24.14.7 (fixed population N = 333,000,000 for 1953-2020 data): A — systematic bias in transmission parameters
- 24.14.8 (biologically implausible parameter values unchecked): A — mu_EI ~2.8 days, mu_RS ~11 days for TB
- 24.14.4 (notation collision: mu_IR used for both force of infection and recovery rate): C — naming inconsistency in equations
- 24.14.6 (ARIMA model selection: lowest-AIC model not chosen; rationale undocumented): C — ARIMA(3,1,4) has lower AIC than selected ARIMA(0,1,5)
- 24.14.9 (ESS near-zero around 1975-1985 not discussed): C — filter losing track during HIV-era TB resurgence
- 24.14.10 (no residual diagnostics shown for selected ARIMA model): C — build_and_diagnose_model output absent
- Reproducibility (no sessionInfo, multiple code versions of seir_step): C — reproducibility concerns from redundant code

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 10 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 5 | 5 | 4 |
| B (AI major, human also found) | 3 | 4 | 3 | 2 |
| C (AI minor, human missed) | 6 | 5 | 4 | 5 |
| D (AI minor, human also found) | 1 | 2 | 3 | 0 |
| E (Human found, AI missed) | 8 | 6 | 6 | 10 |

---

## Per-Reviewer Metrics

| Reviewer | B | D | E | Human Recall (B+D)/(B+D+E) | A | C | AI-Unique Rate (A+C)/(A+B+C+D) |
|----------|--:|--:|--:|---------------------------:|--:|--:|--------------------------------:|
| Alex | 3 | 1 | 8 | 33.3% | 5 | 6 | 73.3% |
| Charlie | 4 | 2 | 6 | 50.0% | 5 | 5 | 62.5% |
| Doug | 3 | 3 | 6 | 50.0% | 5 | 4 | 60.0% |
| Evan | 2 | 0 | 10 | 16.7% | 4 | 5 | 81.8% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (E for all four reviewers):

1. Human Issue #1 — The background section is missing references.
3. Human Issue #3 — Some ARIMA code is apparently taken from a midterm project without credit.
4. Human Issue #4 — Regression with ARMA errors might be more insightful than differencing and fitting ARIMA.
7. Human Issue #7 — The modeling and analysis is similar to but inferior to a previous STATS 531 project on TB; the prior work should be acknowledged more fully.
8. Human Issue #8 — There is an inconsistency in log-likelihood values reported in the text vs. code outputs (-628.8447 and -629.6903).
9. Human Issue #9 — SEIR treats S as the entire population, which may be problematic for TB (only those with specific risk factors are typically at risk).

**Count: 6 out of 12 human issues were missed by all four reviewers.**

### Unique finds per reviewer

No human issue was covered exclusively by a single reviewer. Every issue that was covered by any reviewer was covered by at least two reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

1. **Effective sample size (ESS) not monitored during particle filtering.** All four reviewers flag that no ESS diagnostics are reported, that ESS collapse would indicate model-data mismatch, and that the choice of Np = 2000 is unjustified. The human review does not mention ESS at all.

**Count: 1 universal AI-only flag.**
