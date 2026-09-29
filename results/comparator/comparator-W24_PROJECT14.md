# Comparator Analysis — W24 Project 14

---

## Human Issues

1. The background section is missing references.

2. Data whose scale varies considerably over time are often best plotted on a log scale.

3. Some ARIMA code is apparently taken from 531w24 midterm project 6 without credit. The smallest root table is a good idea to copy, but it would be better to give credit.

4. Regression with ARMA errors (looking to understand the time trend, perhaps with an exponential trend function) might be more insightful than differencing and fitting ARIMA.

5. The SEIR model equations do not perfectly match the implemented equations in the code.

6. The parameter values given as the result of the local search are the starting point for that search, as can be seen by looking at the convergence diagnostics. Considerably better likelihood values are obtained by the end of the local search.

7. The modeling and analysis is similar, but in many ways inferior, to a previous STATS 531 final project on tuberculosis (531w16 project 20). That project is cited, but it would have been better to acknowledge more fully what was learned from that paper, and make progress by contrasting that work with the different dataset in question here.

8. There is an inconsistency in log-likelihood values reported within the text and those shown in code outputs (-628.8447 and -629.6903), which raises concerns about the accuracy of the reported results.

9. SEIR has been successful for rapidly transmitted diseases but tuberculosis is different. Only those in poor housing, or with other risk factors, are typically at risk of TB, so treating S as the entire population may be problematic.

10. The report does not discuss the specification and estimation of initial state values. That can be established from the provided code, but should be in the report.

11. The model-based assessment does not get beyond basic iterated filtering to global maximization or profiles. Given the head-start acquired by building on a previous project, one can expect to get further.

12. Adding a diagram for the process model would help readers to easily understand your model.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Stochastic Model Equations Inconsistent with Implemented Code")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "No Global Parameter Search — Optimization is Effectively Absent"; also matched by finding: "No Likelihood Profile, Confidence Intervals, or Uncertainty Quantification for POMP Parameters")
- Human Issue #12: covered (matched by finding: "Broken Image Path in the Report")

**Findings classification:**
- Finding 1 (No Global Parameter Search): B — no global search performed, single local mif2 run insufficient (matches Human Issue #11)
- Finding 2 (H Compartment Accumulates Recoveries Not Infections): A — H accumulates dN_IR instead of new infections, biologically incorrect measurement model
- Finding 3 (Stochastic Model Equations Inconsistent with Code): B — written stochastic equations do not match the C-snippet actually used (matches Human Issue #5)
- Finding 4 (Population Size Fixed at 2023 Value): A — N=333,000,000 applied across 1953–2020 when population was roughly half that at the start
- Finding 5 (Implausible Biological Parameter Values): A — mu_EI ~129/yr implies 3-day TB latency; mu_RS ~34/yr implies 11-day immunity; not validated against literature
- Finding 6 (Measurement Model / accumvars): A — H reset via accumvars propagates the dN_IR error into the annual measurement; coherent structure but wrong quantity
- Finding 7 (No Likelihood Profile, CIs, or Uncertainty): B — no pfilter replicates, no profiles, no confidence intervals for any POMP parameter (matches Human Issue #11)
- Finding 8 (ARIMA Conflates Case Counts with Rate): A — model fitted to raw counts but figure displays rate; captions are inconsistent
- Finding 9 (Broken Image Path): D — SEIRS diagram referenced with absolute local path; will not render for any other reader (matches Human Issue #12)
- Finding 10 (ARIMA CI Code Never Defined): C — simulation_arima/simulation_sarima referenced but undefined; hidden by simulation_times=0
- Finding 11 (Incorrect Fisher CI Formula): C — diag(var.coef) returns variances not standard errors; CIs are wrong
- Finding 12 (No Convergence Diagnostics Interpreted): C — plot(mif_out) shown without any discussion of convergence or whether likelihood is still increasing
- Finding 13 (Simulation Plot Lacks Legend): C — legend removed with guides(color="none"); data vs. simulated trajectories indistinguishable
- Finding 14 (Duplicate and Redundant Code Blocks): C — seir_step and seir_rinit defined twice; earlier R versions silently overwritten by C-snippets
- Finding 15 (Missing/Anomalous Data Rows): C — year entries "1974 2" and "1979 3" and missing-value tokens not acknowledged in report

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by findings: "Written stochastic Euler equations are systematically incorrect and inconsistent with code" and "Stochastic Euler equations omit the RS waning immunity transition")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by findings: "No global search and absent convergence diagnostics" and "No profile likelihoods; parameter identifiability unassessed")
- Human Issue #12: covered (matched by finding: "Hardcoded local file path prevents rendering")

**Findings classification:**
- Finding 1 (No global search and absent convergence diagnostics): B — no global search/multiple mif2 chains run (matches Human Issue #11)
- Finding 2 (mif2 log-likelihood reported directly without replicated pfilter re-evaluation): A — mif2 internal likelihood used directly instead of pfilter re-evaluation
- Finding 3 (No non-mechanistic benchmark comparison): A — ARIMA and POMP log-likelihoods never compared
- Finding 4 (Written stochastic Euler equations systematically incorrect and inconsistent with code): B — equations show wrong parent pools, do not match Csnippet (matches Human Issue #5)
- Finding 5 (No profile likelihoods; parameter identifiability unassessed): B — no profiles computed for any of the 13 parameters (matches Human Issue #11)
- Finding 6 (No residual diagnostics for selected ARIMA(0,1,5)): C — build_and_diagnose_model defined but never called on selected model
- Finding 7 (Hardcoded local file path prevents rendering): D — SEIRS diagram references absolute path, does not appear in rendered HTML (matches Human Issue #12)
- Finding 8 (Population size fixed at 2023 value across all years 1953–2020): C — N=333,000,000 used throughout despite ~160M population in 1953
- Finding 9 (Fisher CI computation error in model_selection_table): C — diag(var.coef) used instead of sqrt(diag(var.coef)), producing incorrect CIs
- Finding 10 (Stochastic Euler equations omit the RS waning immunity transition): D — R(t+δ) equation missing inflow to S, another mismatch between equations and code (matches Human Issue #5)
- Finding 11 (Multiple redefinitions of seir_step obscure actual model): C — two dead-code R definitions precede the Csnippet actually used
- Finding 12 (Figure 2 caption incorrect): C — caption says "cases and deaths" but figure shows rates per 100,000
- Finding 13 (Intermediate R-based measurement model uses wrong observation variable): C — R-based dmeas uses Rate while final POMP object uses Number
- Finding 14 (ARIMA model selection rationale not adequately explained): C — AIC table shown but minimum cell not identified, near-unit MA root not discussed
- Finding 15 (Visual goodness-of-fit presented as primary model validation): C — conclusion based solely on visual comparison of 5 simulated trajectories

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ARIMA fitted to unlogged counts, log transform preferable given wide dynamic range")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "force-of-infection equation inconsistent between text and Csnippet"; also matched by finding: "discrete stochastic transition equations inconsistent with stated ODE system")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "no assessment of initial condition sensitivity, values not discussed for plausibility")
- Human Issue #11: covered (matched by finding: "no global parameter search performed"; also matched by finding: "no profile likelihoods or confidence intervals for any parameter")
- Human Issue #12: covered (matched by finding: "hard-coded absolute path to external image file — diagram will not render for any reader")

**Findings classification:**
- Finding 1 (accumulator tracks recoveries not new infections): A — semantic mismatch between H accumulator and reported TB incidence counts
- Finding 2 (no global parameter search): B — no global search performed, estimates unreliable (matches Human Issue #11)
- Finding 3 (no benchmark comparison): A — POMP model never compared quantitatively to ARIMA or other baseline
- Finding 4 (no profile likelihoods or CIs): B — no uncertainty quantification for any of 13 parameters (matches Human Issue #11)
- Finding 5 (force-of-infection inconsistent between text and Csnippet): B — narrative uses mu_IR label for foi, Csnippet defines foi differently (matches Human Issue #5)
- Finding 6 (fixed population N ignores demographic change): A — N fixed at 333M for 1953–2020, inflating transmission rate estimates
- Finding 7 (measurement model Rate vs Number mismatch across code blocks): A — intermediate R-function uses Rate, final Csnippet uses Number; different measurement models
- Finding 8 (discrete stochastic equations inconsistent with stated ODE): B — written difference equations omit time-varying Beta_t term present in Csnippet (matches Human Issue #5)
- Finding 9 (single mif2 convergence trace without discussion): C — biologically implausible mu_EI and mu_RS values not flagged
- Finding 10 (ARIMA caption says incidence rate, model fitted to counts; log scale issue): D — log transform preferable given wide dynamic range of counts (matches Human Issue #2)
- Finding 11 (hard-coded absolute path to external image): D — diagram will not render for any reader other than author (matches Human Issue #12)
- Finding 12 (ARIMA model selection on AIC alone, simulation_times=0, root near unit circle): C — adequacy checks computed but not discussed, smallest root 1.05
- Finding 13 (no goodness-of-fit beyond single log-likelihood value): C — -628.8447 reported with no context, no comparison to saturated model or AIC
- Finding 14 (ESS not monitored during particle filtering): C — particle degeneracy not assessed with Np=2000 and 13 parameters
- Finding 15 (no assessment of initial condition sensitivity): D — initial proportions estimated but plausibility not discussed (matches Human Issue #10)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "24.14.4 — notation collision: mu_IR used for both force of infection and recovery rate, creating an equation-level inconsistency")
- Human Issue #6: covered (matched by finding: "24.14.2 — single mif2 run with trace plots still trending at iteration 50; reported parameter values are effectively starting-point values")
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "24.14.1 — mif2 internal log-likelihood reported directly without replicated pfilter; the −628.8447 figure is a noisy, biased estimate")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "24.14.2 — single mif2 run with no global search across starting points; convergence never established")
- Human Issue #12: missed

**Findings classification:**
- 24.14.1: B — mif2 log-likelihood reported without replicated pfilter (matches Human Issue #8)
- 24.14.2: B — single mif2 run; convergence not established; parameters still trending at final iteration (matches Human Issues #6 and #11)
- 24.14.3: A — simulations exceed observed data by two orders of magnitude; authors incorrectly claim model captures trend
- 24.14.5: A — no quantitative comparison of ARIMA and POMP log-likelihoods
- 24.14.7: A — fixed population N uses 2023 U.S. value for 1953–2020 data, biasing transmission parameter throughout
- 24.14.8: A — estimated parameters imply biologically implausible latent and infectious periods for TB; not flagged
- 24.14.4: D — notation collision: mu_IR defined as both force of infection in equations and recovery rate in parameter list (matches Human Issue #5)
- 24.14.6: C — ARIMA model selection chose higher-AIC model (0,1,5) over lower-AIC model (3,1,4) without documented rationale
- 24.14.9: C — ESS collapses to near zero during 1975–1990 HIV-era resurgence period; not discussed
- 24.14.10: C — residual diagnostics for the selected ARIMA(0,1,5) model not shown in manuscript
- Reproducibility: C — no sessionInfo(), package version pins, or RNG seeds; multiple unused versions of model code not removed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 2 | 4 | 4 |
| B (AI major, human also found) | 3 | 3 | 4 | 2 |
| C (AI minor, human missed) | 6 | 8 | 4 | 4 |
| D (AI minor, human also found) | 1 | 2 | 3 | 1 |
| E (Human found, AI missed) | 9 | 9 | 7 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 1 | 9 | 3/12 = 25% | 5 | 6 | 11/15 = 73% |
| Charlie | 3 | 2 | 9 | 3/12 = 25% | 2 | 8 | 10/15 = 67% |
| Doug | 4 | 3 | 7 | 5/12 = 42% | 4 | 4 | 8/15 = 53% |
| Evan | 2 | 1 | 8 | 4/12 = 33% | 4 | 4 | 8/11 = 73% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The background section is missing references. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: Some ARIMA code is apparently taken from 531w24 midterm project 6 without credit. The smallest root table is a good idea to copy, but it would be better to give credit. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Regression with ARMA errors (looking to understand the time trend, perhaps with an exponential trend function) might be more insightful than differencing and fitting ARIMA. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: The modeling and analysis is similar, but in many ways inferior, to a previous STATS 531 final project on tuberculosis (531w16 project 20). That project is cited, but it would have been better to acknowledge more fully what was learned from that paper, and make progress by contrasting that work with the different dataset in question here. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: SEIR has been successful for rapidly transmitted diseases but tuberculosis is different. Only those in poor housing, or with other risk factors, are typically at risk of TB, so treating S as the entire population may be problematic. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 12 human issues (42%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: Data whose scale varies considerably over time are often best plotted on a log scale. (Covered only by Doug)
- Human Issue #6: The parameter values given as the result of the local search are the starting point for that search, as can be seen by looking at the convergence diagnostics. Considerably better likelihood values are obtained by the end of the local search. (Covered only by Evan)
- Human Issue #8: There is an inconsistency in log-likelihood values reported within the text and those shown in code outputs (-628.8447 and -629.6903), which raises concerns about the accuracy of the reported results. (Covered only by Evan)
- Human Issue #10: The report does not discuss the specification and estimation of initial state values. That can be established from the provided code, but should be in the report. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 2 |
| Evan | 2 |
