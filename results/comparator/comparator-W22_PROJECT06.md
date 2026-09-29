# Comparator Analysis — W22 Project 06

---

## Human Issues

1. The analysis is quite similar to the referenced source (project14 from W21). The data are different, but the model and analysis follow a similar trajectory. It would have been better to discuss explicitly the relationship to that previous work.

2. Signs in the "conservation of mass" flow equations are wrong. For example, we should have $S(t)=S(t_0)- N_{SE}(t)$.

3. The report does not describe the measurement model. From the code, one can see that the `dnbinom` specification is incorrect, since it uses a parameterization corresponding to a binomial distribution.

4. The process model does not include overdispersion (as described in Chapter 17) which might cause problems matching the variability in the data.

5. A benchmark (perhaps log-ARMA) would help to establish the goodness of fit of the model, or identify misspecification issues.

6. Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R expressions.

7. In the code, the authors set $E(0) = 14$ and $I(0) = 7$ but did not explain this setting in the report. This may be done to match by eye, but it should be explained and the decision could have consequences for the conclusions.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Negative Binomial Measurement Model Is Misspecified")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Initial Values for E and I Are Hardcoded Without Justification")

**Findings classification:**
- Finding 1 [Major] Negative Binomial Measurement Model Is Misspecified: B — H used as dispersion parameter instead of mean; rho/H roles inverted (matches Human Issue #3)
- Finding 2 [Major] Conditional Likelihood Assigns Zero to Zero-Count Observations: A — dmeas returns only tol for zero-count weeks, discarding valid likelihood information
- Finding 3 [Major] Inconsistency Between Stated and Analyzed Time Period: A — stated 1966-1967 window conflicts with code constructing 10-year series then truncating to 105 rows
- Finding 4 [Major] Parameters mu_EI and mu_IR Are Fixed Without Justification: A — transition rates fixed at biologically implausible values with no citation or sensitivity analysis
- Finding 5 [Major] Parameter Transformation Is Incomplete: A — b2 amplitude lacks non-negativity constraint; log transforms omitted for rate parameters
- Finding 6 [Major] eta Profile Does Not Reach the Confidence Interval Cutoff: A — flat profile indicates unidentifiability yet paper reports CI bounds as valid
- Finding 7 [Major] Global Search Starts All Chains from mifs_local[[1]] Only: A — all 60 global chains inherit algorithmic settings from single local run
- Finding 8 [Moderate] rho Profile Range Inconsistent with Global Search Results: C — profile boundary validity not visually confirmed; narrow CI not validated
- Finding 9 [Moderate] Decomposition Analysis Confuses Trend with Vaccine Efficacy: C — data predates MMR vaccine introduction by at least one year
- Finding 10 [Moderate] R0 Calculation Uses Wrong Formula and Wrong Compartment: C — L/A heuristic used instead of model-derived formula; flow labeled Delta N_{SI} instead of Delta N_{SE}
- Finding 11 [Moderate] Comment Left in Published Document: C — section title with authorial uncertainty left verbatim in rendered HTML
- Finding 12 [Moderate] Initial Values for E and I Are Hardcoded Without Justification: D — E=14 and I=7 fixed with no epidemiological reasoning or sensitivity analysis (matches Human Issue #7)
- Finding 13 [Minor] Contradictions in Reported eta CI Bounds Between Rmd and HTML: C — Rmd text states (0.19%, 0.24%) while HTML table shows (0.24%, 0.25%)
- Finding 14 [Minor] Data Imputation Uses Sequential Forward Filling With Potential Edge Cases: C — consecutive missing values produce cascading imputation bias
- Finding 15 [Minor] Comment in Text Uses Incorrect Direction of Bivariate Association: C — b1-b2 ridge reflects structural identifiability issue, not noted as such

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

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Sign Errors in the State Equation Presentation")
- Human Issue #3: covered (matched by finding: "Measurement Model Parametrization Unexplained and Non-Standard")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No Benchmark Comparison")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Initial Conditions E=14 and I=7 Fixed Without Justification")

**Findings classification:**
- Finding 1 (Force-of-Infection Discrepancy Between Text and Code): A — text uses E but code uses I in force of infection; no human issue raised this
- Finding 2 (Sign Errors in State Equation Presentation): B — wrong signs in S and R equations (matches Human Issue #2)
- Finding 3 (Measurement Model Parametrization Unexplained and Non-Standard): B — dnbinom parameterization non-standard/incorrect and unexplained (matches Human Issue #3)
- Finding 4 (Global Search Uses Only mifs_local[[1]] as Starting Template): A — single fixed local run template used for all global search; no human issue raised this
- Finding 5 (eta Profile Fails to Identify the Maximum; CI Is Invalid): A — eta profile never reaches Wilks threshold yet CI is still reported; no human issue raised this
- Finding 6 (Flow Rates Fixed Without Literature Justification): A — mu_EI and mu_IR fixed at biologically implausible values with no justification; no human issue raised this
- Finding 7 (No Benchmark Comparison): B — no ARMA or other benchmark fit provided (matches Human Issue #5)
- Finding 8 (No Model Diagnostics): A — no conditional log-likelihood plot or ESS monitoring; no human issue raised this
- Finding 9 (Data Truncation Unexplained): C — 501 weeks truncated to 105 without explanation; no human issue raised this
- Finding 10 (rho Profile CI Implausibly Narrow): C — CI width of 0.69pp is suspiciously narrow given Monte Carlo noise; no human issue raised this
- Finding 11 (run_level = 2 with Potentially Insufficient Global Search): C — global search trace plots show non-convergence; no human issue raised this
- Finding 12 (Initial Conditions E=14 and I=7 Fixed Without Justification): D — hardcoded initial compartment counts not motivated (matches Human Issue #7)
- Finding 13 (Typo in Data Description "1996-1975"): C — typo for 1966-1975; no human issue raised this
- Finding 14 (Pairs Plot Comment Left in Draft State): C — internal draft note not removed before submission; no human issue raised this
- Finding 15 (Conclusion Overstates Model Fit): C — conclusion claims SEIR fits well without resolving open validity issues; no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: contradiction (AI says NB measurement model is commendable; human says dnbinom specification is incorrect, using a binomial parameterization)
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Fixed parameters (mu_EI, mu_IR) lack justification and sensitivity analysis")

**Findings classification:**
- Major 1 (Global search initialization anti-pattern): A — mifs_local[[1]] as first mif2 argument exhausts cooling schedule, invalidating global search
- Major 2 (Global search demonstrably inadequate): A — profile searches find substantially better log-likelihoods than declared global maximum
- Major 3 (Accumulator H tracks I→R instead of E→I): A — systematic mismatch between accumulator and observation process
- Major 4 (Implausible R0 ~4,872): A — estimated parameters imply biologically extreme intrinsic R0 with no discussion
- Major 5 (No non-mechanistic benchmark): B — no SARIMA or similar baseline provided (matches Human Issue #5)
- Major 6 (Profile CI for eta misreported and poorly converged): A — text states no CI reached but artifact shows two points above cutoff; reported CI bounds inconsistent
- Major 7 (Profile searches use profile-maximum as CI reference): A — both profiles use max within-profile loglik rather than robust global MLE as chi-squared reference
- Major 8 (Fixed parameters mu_EI, mu_IR lack justification): B — fixed rate parameters have no cited source and no sensitivity analysis; same underlying concern as unexplained fixed initial conditions (matches Human Issue #7)
- Minor: Text-code discrepancy in force-of-infection formula: C — text uses E/N in force of infection but code correctly uses I/N
- Minor: Incorrect eta initial value calculation: C — stated rationale (12,460×2÷15,717,204) yields 0.00159, not the stated 0.0023
- Minor: Data loaded from external URL: C — reproducibility risk from live URL dependency
- Minor: SE of logLik large (SD=2.3): C — 1,000 particles insufficient for reliable likelihood evaluation at MLE
- Minor: Global search box for eta is very narrow: C — 30% range despite local search finding values outside the box
- Minor: Convergence traces not discussed quantitatively: C — qualitative description only, no between-chain diagnostics
- Minor: No model diagnostics: C — no conditional log-likelihoods or ESS diagnostics presented
- Minor: Plot comment left in code: C — draft note "(not sure if we need to inclue this part)" left in submission
- Strength (Negative Binomial measurement model described as commendable): F — AI praises the NB measurement model as commendable; human says the dnbinom specification is incorrect, using a binomial parameterization (contradicts Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.06.2 — incorrect signs in compartment equations")
- Human Issue #3: contradiction (AI says dnbinom is appropriate and correctly implemented; human says dnbinom specification is incorrect)
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "22.06.1 — no benchmark comparison")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "22.06.5 — fixed mu_EI and mu_IR without justification or sensitivity analysis")

**Findings classification:**
- 22.06.1: B — no benchmark comparison provided (matches Human Issue #5)
- 22.06.3: A — unidentified eta profile; reported CI is statistically invalid
- 22.06.5: B — mu_EI and mu_IR fixed without justification or sensitivity analysis (matches Human Issue #7)
- 22.06.6: A — no particle filter diagnostics (ESS or conditional log-likelihood traces)
- 22.06.2: D — incorrect signs in compartment equations (matches Human Issue #2)
- 22.06.4: C — rho profile optimization quality; apparent gap below global maximum
- 22.06.7: C — rho parametrization in dnbinom not explained in text
- 22.06.8: C — vaccine timeline factual error (data precedes MMR program)
- 22.06.9: C — inconsistency between text and Table 4 for eta CI values
- M1: C — rho serves double-duty as reporting rate and dispersion parameter without explanation
- M2: C — short two-cycle data window limits seasonal parameter reliability; not discussed as limitation
- Key Strength (Negative binomial measurement model): F — AI states dnbinom is "appropriate" and "implemented correctly"; human says the dnbinom specification is incorrect (contradicts Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 5 | 6 | 2 |
| B (AI major, human also found) | 1 | 3 | 2 | 2 |
| C (AI minor, human missed) | 7 | 6 | 8 | 6 |
| D (AI minor, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 5 | 3 | 4 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 1 | 1 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 5 | 2/7 = 29% | 6 | 7 | 13/15 = 87% |
| Charlie | 3 | 1 | 3 | 4/7 = 57% | 5 | 6 | 11/15 = 73% |
| Doug | 2 | 0 | 4 | 2/6 = 33% | 6 | 8 | 14/16 = 88% |
| Evan | 2 | 1 | 3 | 3/6 = 50% | 2 | 6 | 8/11 = 73% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The analysis is quite similar to the referenced source (project14 from W21). The data are different, but the model and analysis follow a similar trajectory. It would have been better to discuss explicitly the relationship to that previous work. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The process model does not include overdispersion (as described in Chapter 17) which might cause problems matching the variability in the data. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R expressions. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 7 human issues (43%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
