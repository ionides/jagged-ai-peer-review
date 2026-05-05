# Ned-Clean Analysis — W22 Project 06

---

## Human Issues

1. The analysis is closely similar to a prior referenced project (https://ionides.github.io/531w21/final_project/project14/blinded.html); the relationship to that previous work should have been discussed explicitly.
2. Signs in the "conservation of mass" flow equations are wrong (e.g., S(t) should subtract N_SE(t), not add it).
3. The measurement model is not described in the report; additionally, the dnbinom specification in the code is incorrect (uses a binomial parameterization rather than the standard negative binomial with mean rho*H).
4. The process model does not include overdispersion (as described in Chapter 17), which might cause problems matching the variability in the data.
5. A benchmark (e.g., log-ARMA) would help establish goodness of fit or identify misspecification.
6. Numbers are hard-coded in the Rmd document rather than referenced using inline R expressions.
7. Initial conditions E(0)=14 and I(0)=7 are set in the code but not explained in the report; this should be explained as it may have consequences for conclusions.

---

## Alex

**Coverage record:**
- Human Issue #1 (analysis similar to prior project): missed
- Human Issue #2 (sign errors in flow equations): missed
- Human Issue #3 (measurement model not described; dnbinom incorrect): covered (matched by finding: "Negative Binomial Measurement Model Is Misspecified")
- Human Issue #4 (process model lacks overdispersion): missed
- Human Issue #5 (no benchmark): missed
- Human Issue #6 (numbers hard-coded): missed
- Human Issue #7 (E(0)=14, I(0)=7 not explained): covered (matched by finding: "Initial Values for E and I Are Hardcoded Without Justification")

**Findings classification:**
- Finding 1 (Negative Binomial Measurement Model Is Misspecified): B — dnbinom misspecified with H as dispersion (matches Human Issue #3)
- Finding 2 (Conditional Likelihood Assigns Zero to Zero-Count Observations): A — truncating zero-count contributions biases the filter
- Finding 3 (Inconsistency Between Stated and Analyzed Time Period): A — 1966-1967 claim vs. 105-week code window inconsistency
- Finding 4 (Parameters mu_EI and mu_IR Fixed Without Justification): A — transition rates fixed at biologically implausible values with no citation
- Finding 5 (Parameter Transformation Is Incomplete): A — b2 amplitude lacks non-negativity constraint in parameter_trans
- Finding 6 (eta Profile Does Not Reach CI Cutoff): A — profile is flat; reported CI bounds are meaningless
- Finding 7 (Global Search Starts All Chains from mifs_local[[1]] Only): A — cooling schedule inherited from a single local run biases global search
- Finding 8 (rho Profile Range Inconsistent with Global Search): C — profile range not verified to bracket CI cutoff on both sides
- Finding 9 (Decomposition Confuses Trend with Vaccine Efficacy): C — data predates MMR vaccine by at least one year
- Finding 10 (R0 Calculation Uses Wrong Formula): C — L/A heuristic used instead of SEIR-derived R0=beta/mu_IR
- Finding 11 (Comment Left in Published Document): C — draft section title and commented-out code left in rendered HTML
- Finding 12 (Initial Values E=14, I=7 Hardcoded Without Justification): D — initial compartment counts fixed without motivation (matches Human Issue #7)
- Finding 13 (Contradictions in eta CI Bounds Between Rmd and HTML): C — text states (0.19%, 0.24%) but table shows (0.24%, 0.25%)
- Finding 14 (Data Imputation Uses Sequential Forward Filling): C — cascading imputation bias if consecutive missing values occur
- Finding 15 (Bivariate Association Comment Incorrect): C — b1-b2 ridge indicates structural identifiability issue, not mere correlation

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
- Human Issue #1 (analysis similar to prior project): missed
- Human Issue #2 (sign errors in flow equations): covered (matched by finding: "Sign Errors in the State Equation Presentation")
- Human Issue #3 (measurement model not described; dnbinom incorrect): covered (matched by finding: "Measurement Model Parametrization Unexplained and Non-Standard")
- Human Issue #4 (process model lacks overdispersion): missed
- Human Issue #5 (no benchmark): covered (matched by finding: "No Benchmark Comparison")
- Human Issue #6 (numbers hard-coded): missed
- Human Issue #7 (E(0)=14, I(0)=7 not explained): covered (matched by finding: "Initial Conditions E=14 and I=7 Fixed Without Justification")

**Findings classification:**
- Finding 1 (Force-of-Infection Discrepancy Between Text and Code): A — text uses E in force of infection, code uses I; inconsistency in SEIR structure (Major)
- Finding 2 (Sign Errors in the State Equation Presentation): B — S and R equations have reversed signs (matches Human Issue #2) (Major)
- Finding 3 (Measurement Model Parametrization Unexplained and Non-Standard): B — dnbinom uses H as dispersion; non-standard and unjustified (matches Human Issue #3) (Major)
- Finding 4 (Global Search Uses Only mifs_local[[1]]): A — single local template biases global search diversity (Major)
- Finding 5 (eta Profile Fails to Identify Maximum; CI Invalid): A — profile range too narrow; no valid CI can be constructed (Major)
- Finding 6 (Flow Rates Fixed Without Literature Justification): A — mu_EI=0.08 implies 12.5-week latent period, biologically implausible (Major)
- Finding 7 (No Benchmark Comparison): B — no ARMA or regression baseline provided (matches Human Issue #5) (Major)
- Finding 8 (No Model Diagnostics): A — no ESS, conditional log-likelihood, or filtering distribution checks (Major)
- Finding 9 (Data Truncation Unexplained): C — 105-week subset from 501-week dataset not explained in text (Minor)
- Finding 10 (rho Profile CI Implausibly Narrow): C — 0.69 percentage-point width suspicious given Monte Carlo noise (Minor)
- Finding 11 (run_level=2 with Potentially Insufficient Global Search): C — trace plots show non-convergence; computational adequacy not established (Minor)
- Finding 12 (Initial Conditions E=14 and I=7 Fixed Without Justification): D — hardcoded initial compartment values not motivated (matches Human Issue #7) (Minor)
- Finding 13 (Typo in Data Description): C — "1996-1975" should be "1966-1975" (Minor)
- Finding 14 (Pairs Plot Comment Left in Draft State): C — section header contains unresolved internal note (Minor)
- Finding 15 (Conclusion Overstates Model Fit): C — conclusion not supported given unresolved profile and measurement model issues (Minor)

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
- Human Issue #1 (analysis similar to prior project): missed
- Human Issue #2 (sign errors in flow equations): missed
- Human Issue #3 (measurement model not described; dnbinom incorrect): missed
- Human Issue #4 (process model lacks overdispersion): missed
- Human Issue #5 (no benchmark): covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #6 (numbers hard-coded): missed
- Human Issue #7 (E(0)=14, I(0)=7 not explained): missed

**Findings classification:**
- Finding 1 (Global search initialization anti-pattern): A — mifs_local[[1]] as template exhausts cooling before new starts can explore (Major)
- Finding 2 (Global search demonstrably inadequate): A — profile searches find solutions 2.7–5.2 log-likelihood units better than global max (Major)
- Finding 3 (Accumulator H tracks I→R instead of E→I): A — H accumulates recoveries rather than new infections; systematic mismatch with surveillance data (Major)
- Finding 4 (Implausible intrinsic R0 ~ 4,872): A — fitted b1, b2, mu_IR imply biologically implausible R0 with no discussion (Major)
- Finding 5 (No non-mechanistic benchmark comparison): B — no SARIMA or autoregressive baseline provided (matches Human Issue #5) (Major)
- Finding 6 (Profile CI for eta misreported): A — profile is noisy, two points above cutoff are non-contiguous, text CI contradicts table (Major)
- Finding 7 (Profile uses profile-maximum as CI reference): A — noisy profile max used instead of robustly estimated global max (Major)
- Finding 8 (Fixed parameters mu_EI, mu_IR lack justification): A — mu_EI=0.08 implies 12.5-week latent period; no citation or sensitivity analysis (Major)
- Minor: text-code discrepancy (E vs I in force of infection): C — text writes E, code uses I in force of infection (Minor)
- Minor: incorrect eta initial value calculation: C — stated calculation yields 0.0023 but actual arithmetic gives 0.00159 (Minor)
- Minor: data loaded from external URL: C — reproducibility depends on external repository stability (Minor)
- Minor: SE of logLik large (SD=2.3): C — Np=1000 insufficient for reliable likelihood evaluation at MLE (Minor)
- Minor: global search box for eta very narrow: C — eta box (0.002, 0.0026) narrower than local search range found (Minor)
- Minor: convergence traces not discussed quantitatively: C — discussion of trace plots is qualitative only (Minor)
- Minor: no model diagnostics: C — no ESS, conditional log-likelihood, or filtering distribution comparisons (Minor)
- Minor: plot comment left in code: C — draft note "(not sure if we need to inclue this part)" not removed (Minor)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (analysis similar to prior project): missed
- Human Issue #2 (sign errors in flow equations): covered (matched by finding: "22.06.2 — Incorrect signs in compartment equations")
- Human Issue #3 (measurement model not described; dnbinom incorrect): covered (matched by finding: "22.06.7 — rho parametrization in dnbinom not explained")
- Human Issue #4 (process model lacks overdispersion): missed
- Human Issue #5 (no benchmark): covered (matched by finding: "22.06.1 — No benchmark comparison")
- Human Issue #6 (numbers hard-coded): missed
- Human Issue #7 (E(0)=14, I(0)=7 not explained): missed

**Findings classification:**
- 22.06.1 (No benchmark comparison): B — no non-mechanistic baseline log-likelihood provided (matches Human Issue #5) (Major)
- 22.06.3 (Unidentified eta profile; CI statistically invalid): A — profile flat, no visible peak; reported CI contradicts paper's own acknowledgment (Major)
- 22.06.5 (Fixed parameters mu_EI and mu_IR without justification): A — no citation for fixed values; no sensitivity analysis conducted (Major)
- 22.06.6 (No particle filter diagnostics): A — no ESS plots or conditional log-likelihood traces provided (Major)
- 22.06.2 (Incorrect signs in compartment equations): D — S(t)=S(0)+N_SE and R(t)=R(0)-N_IR have reversed signs (matches Human Issue #2) (Minor)
- 22.06.4 (rho profile optimization quality): C — profile max slightly below global max; gap may reflect Monte Carlo noise (Minor)
- 22.06.7 (rho parametrization in dnbinom not explained): D — rho as success probability controls both mean and variance; not interpreted (matches Human Issue #3) (Minor)
- 22.06.8 (Vaccine timeline factual error): C — paper claims 1966-1967 data covers MMR program start, but MMR began in 1969 (Minor)
- 22.06.9 (Inconsistency between text and Table 4 eta CI values): C — text reports (0.19%, 0.24%) while table shows (0.24%, 0.25%) (Minor)
- M1 (rho double-duty as reporting rate and dispersion): C — negative binomial parametrization means rho governs both mean and variance simultaneously (Minor)
- M2 (Short data window limits seasonal parameter reliability): C — only two epidemic cycles; limitation not discussed in paper (Minor)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 5 | 7 | 3 |
| B (AI major, human also found) | 1 | 3 | 1 | 1 |
| C (AI minor, human missed) | 7 | 6 | 8 | 5 |
| D (AI minor, human also found) | 1 | 1 | 0 | 2 |
| E (Human found, AI missed) | 5 | 3 | 6 | 4 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+5) = 2/7 = 28.6%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+1+7+1) = 13/15 = 86.7%

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (3+1) / (3+1+3) = 4/7 = 57.1%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+6) / (5+3+6+1) = 11/15 = 73.3%

**Doug**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+6) = 1/7 = 14.3%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+8) / (7+1+8+0) = 15/16 = 93.8%

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+2) / (1+2+4) = 3/7 = 42.9%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+5) / (3+1+5+2) = 8/11 = 72.7%

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer (all four failed to cover):

- Human Issue #1: Analysis closely mirrors a prior course project; the explicit relationship was never discussed. (missed by Alex, Charlie, Doug, Evan)
- Human Issue #4: The process model does not include overdispersion as taught in Chapter 17. (missed by Alex, Charlie, Doug, Evan)
- Human Issue #6: Numbers are hard-coded in the Rmd rather than referenced via inline R expressions. (missed by Alex, Charlie, Doug, Evan)

Count: 3 out of 7 (42.9%)

### Unique finds per reviewer

No human issue was covered by exactly one reviewer. Every human issue that was covered at all was covered by at least two reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

1. **eta profile CI is invalid** — all four reviewers flagged that the profile likelihood for eta is flat over the search range, making the reported confidence interval meaningless. (Alex Major #6, Charlie Major #5, Doug Major #6, Evan Major 22.06.3)

2. **Fixed parameters mu_EI and mu_IR lack biological justification** — all four reviewers identified that fixing mu_EI=0.08 (implying a 12.5-week latent period) and mu_IR=0.4 without citation or sensitivity analysis is a critical weakness. (Alex Major #4, Charlie Major #6, Doug Major #8, Evan Major 22.06.5)

Count: 2 universal AI-only flags
