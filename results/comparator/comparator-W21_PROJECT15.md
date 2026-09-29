# Comparator Analysis — W21 Project 15

---

## Human Issues

1. Over-dispersed process noise might also help with fitting multiple waves (beyond the over-dispersed measurement model already used).

2. A time-varying measurement model would also make sense in the context of COVID.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Finding 1 (ARMA benchmark likelihood not comparable): A — ARMA Jacobian correction produces an incomparable likelihood to SEIR
- Finding 2 (mu_EI and mu_IR fixed without justification): A — both transition rates fixed at 0.1 with no sensitivity analysis
- Finding 3 (profile likelihood underpowered): A — profile uses fewer mif2 rounds than global search; CI based on only three above-threshold points
- Finding 4 (local search results suppressed via eval=FALSE): A — pairs plots and results table not rendered, preventing verification
- Finding 5 (initial state E=100, I=200 unjustified): A — ad hoc seeding values not estimated or profiled
- Finding 6 (tau ~0.09 not interpreted): A — overdispersion parameter MLE not discussed for epidemiological plausibility
- Finding 7 (measurement model notation sign error): C — positive exponent in text contradicts negative exponent in code
- Finding 8 (no convergence diagnostics beyond trace plots): C — no formal convergence metric or ESS from pfilter presented
- Finding 9 (piecewise beta breakpoints not epidemiologically motivated): C — date boundaries not linked to specific policy events
- Finding 10 (NCORES=1 negates parallelism): C — all %dopar% loops run serially; reproducibility note lacking
- Finding 11 (SARMA AIC table suppressed): C — model selection for SARMA cannot be verified by reader
- Finding 12 (no R0 or Rt discussed): C — time-varying beta values not translated into reproduction numbers
- Finding 13 (rho ~0.48 not externally validated): C — claimed "reasonable" without comparison to seroprevalence or ascertainment studies
- Finding 14 (measurement model conditioned on H, not incidence): C — H tracks recoveries, not new confirmed cases; systematic lag possible
- Finding 15 (no particle filter diagnostics): C — no effective sample size plots; filter collapse risk not assessed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "7-day weekly periodicity not incorporated into the SEIR model — recommends day-of-week effect in measurement model's reporting rate"; also touched on by finding: "SEIR model substantially outperformed by SARMA benchmark with no model revision — suggests incorporating a weekly effect in the measurement model as one remediation example")

**Findings classification:**
- Finding 1 (tau rw.sd too small, effectively not estimated): A — tau perturbation size set 200× too small, rendering tau optimization ineffective
- Finding 2 (profile likelihood for rho too sparse): A — only three points above Wilks threshold, CI invalid
- Finding 3 (mu_EI and mu_IR fixed without profiling or sensitivity analysis): A — two key epidemiological parameters fixed with no identifiability check
- Finding 4 (SEIR outperformed by SARMA by ~47 log-likelihood units with no model revision): A — large benchmark gap unaddressed; model revision not attempted
- Finding 5 (global search convergence diagnostics absent): A — no trace plots for global search, pairs plot insufficient
- Finding 6 (no model diagnostics beyond unconditional forward simulation): A — no conditional log-likelihoods per time step, no ESS monitoring
- Finding 7 (profile likelihood computed only for rho; b1–b5 and eta not profiled): A — identifiability of contact rate segments unverified
- Finding 8 (ARMA model selection code not rendered; benchmark AIC unverifiable): A — four eval=FALSE chunks suppress AIC table computation
- Finding 9 (local search results table and pairs plot not rendered): C — suppressed via eval=FALSE, numerical results invisible to readers
- Finding 10 (E(0) and I(0) fixed without sensitivity): C — initial compartment values not estimated or profiled
- Finding 11 (initial pfilter uses fewer particles than rest of analysis): C — Np=500 vs NP=1000, SE of 25.50 suggests inadequate particle count
- Finding 12 (optimal tau at boundary of search domain): C — tau MLE at 0.1012 against upper bound of 0.1, expanded search not attempted
- Finding 13 (R compartment not tracked; population conservation unverifiable): C — S+E+I+H does not equal N, no sanity check possible
- Finding 14 (7-day weekly periodicity not incorporated into SEIR model): D — recommends day-of-week effect in measurement model's reporting rate (matches Human Issue #2)
- Finding 15 (Gaussian measurement model choice not discussed): C — no justification for truncated normal over negative binomial

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Finding 1 (Global search init from local mif2 object): A — global search inherits cooled mif2 rather than fresh pomp object
- Finding 2 (Invalid SARMA–SEIR log-likelihood comparison): A — log-likelihoods not on same scale due to differing observation models
- Finding 3 (mu_EI and mu_IR fixed without identifiability justification): A — fixing transition rates inflates precision of other estimates
- Finding 4 (Profile rho based on only three points above threshold): A — statistically unreliable CI from three noisy profile points
- Finding 5 (Profile rho guess-stratification conflates all run ids): A — PARAMS_FILE accumulation biases profile coverage
- Finding 6 (No model diagnostic tools applied): A — ESS, conditional log-likelihoods, and filtering distributions all absent
- Finding 7 (Accumulator H tracks recoveries not new infections): C — semantic mismatch between H and confirmed cases data
- Finding 8 (rmeasure non-integer rounding with small rho*H): C — dmeas/rmeas internally consistent but needs verification against zero-count data
- Finding 9 (Initial conditions E=100, I=200 fixed without estimation): C — no sensitivity analysis for hard-coded initial infected counts
- Finding 10 (rho CI reference max may come from profile not global search): C — PARAMS_FILE not filtered to id==2 before computing cutoff
- Finding 11 (Computational effort at run_level=2 insufficient): C — loglik.se up to 0.62 at MLE with no evidence doubling NP is safe
- Finding 12 (SARMA grid search eval=FALSE, hiding model selection): C — actual model selection not reproduced during document compilation
- Finding 13 (No discussion of tau boundary-hugging): C — tau at upper bound suggests measurement model needs more overdispersion
- Finding 14 (IID negative binomial benchmark trivially easy to beat): C — temporal dependence alone explains the improvement over IID
- Finding 15 (Conclusion overstates model fit quality): C — SEIR is 47 log-likelihood units worse than SARMA; conclusion does not acknowledge failure

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- 21.15.M2: A — profile likelihood for rho is too sparse to support the reported CI
- 21.15.M3: A — no convergence diagnostics for the global search
- 21.15.M4: C — ARMA benchmark comparison: Jacobian correction for log-transform not explained in text
- 21.15.M1: C — sensitivity of fixed mu_EI and mu_IR not reported
- 21.15.M5: C — fixed initial conditions E_0=100, I_0=200 without sensitivity analysis
- 21.15.m7: C — run-level parameters (Np, Nmif, NREPS, NSTART) not stated in text
- 21.15.m8: C — effective sample size from particle filter not reported
- 21.15.m14: C — truncated normal measurement model used without justification or comparison to negative binomial
- 21.15.new1: C — no profile likelihoods for any of the five beta parameters
- 21.15.new2: C — figures show forward simulations from MLE, not filtering-distribution-conditioned simulations
- 21.15.m6: C — pathological divergence of b3/b4 in local search traces not discussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 8 | 6 | 2 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 9 | 6 | 9 | 9 |
| D (AI minor, human also found) | 0 | 1 | 0 | 0 |
| E (Human found, AI missed) | 2 | 1 | 2 | 2 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 0 | 2 | 0/2 = 0% | 6 | 9 | 15/15 = 100% |
| Charlie | 0 | 1 | 1 | 1/2 = 50% | 8 | 6 | 14/15 = 93% |
| Doug | 0 | 0 | 2 | 0/2 = 0% | 6 | 9 | 15/15 = 100% |
| Evan | 0 | 0 | 2 | 0/2 = 0% | 2 | 9 | 11/11 = 100% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Over-dispersed process noise might also help with fitting multiple waves (beyond the over-dispersed measurement model already used). (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 1 out of 2 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: A time-varying measurement model would also make sense in the context of COVID. (Covered only by Charlie)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |
