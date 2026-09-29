# Comparator Analysis — W21 Project 13

---

## Human Issues

1. Section 2.2 presents an ODE model and then a POMP model including stochasticity, but does not explain the relationship between the two. The ODE model is the deterministic skeleton for the actual model used. Additionally, there is an inconsistency: the SE rate is correctly proportional to I+A+P in the stochastic version, but only proportional to I in the skeleton, which is presumably a typo.

2. Overdispersion in the process model might also help — the binomial process noise seems too small to fit the data well.

3. Not all references are cited in the project.

4. The convergence plots show weak identifiability of some parameters, and this should be noted.

5. There could have been more discussion of the presented results.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No profile likelihood or confidence intervals — pairs plots not interpreted for identifiability"; also matched by finding: "Convergence described without quantitative evidence")
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (H tracks recoveries, not incidence): A — accumulator H counts recoveries instead of new cases, invalidating measurement model
- Finding 2 (Deaths in rmeasure/dmeasure inconsistent): A — rmeasure and dmeasure are self-inconsistent in how death counts are handled
- Finding 3 (D is cumulative stock used as daily flow): A — D accumulates over the whole simulation but is used as a daily death count
- Finding 4 (rho improper constraint/prior): A — search box allows rho up to 2 but logit transform constrains it to (0,1)
- Finding 5 (Intervention periods by row index, not dates): A — intervention windows assigned by arbitrary index with no mapping to calendar events
- Finding 6 (ARIMA vs POMP likelihood comparison invalid): A — likelihoods evaluated on different scales with no complexity penalty
- Finding 7 (Only 8 IF2 chains): A — insufficient chains for a 16-parameter model given visible non-convergence in pairs plots
- Finding 8 (alpha mislabeled and inconsistent): A — alpha labeled "presymptomatic portion" but code routes higher alpha to asymptomatic compartment
- Finding 9 (nearbyint rounding bias): A — rounding alpha*k and (1-alpha)*k independently can violate population conservation
- Finding 10 (No profile likelihood or confidence intervals): B — pairs plots not interpreted for identifiability or correlation; no uncertainty quantification (matches Human Issue #4)
- Finding 11 (AIC selection without checking numerical stability): C — inverse roots near unit circle noted but not investigated further
- Finding 12 (Spectrum analysis vague and unused): C — dominant 150-day cycle identified but not incorporated or rigorously assessed
- Finding 13 (Convergence described without quantitative evidence): D — convergence declared by visual inspection only, no quantitative diagnostics (matches Human Issue #4)
- Finding 14 (I_0 = 250 not justified): C — no epidemiological basis given for initial infected count; initial population sum is N+250
- Finding 15 (Observation model text inconsistent with data): C — text describes weekly recovered cases but data is daily confirmed cases

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No process noise (environmental stochasticity) in transmission")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No profile likelihoods or confidence intervals — parameter identifiability entirely unassessed")
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (H accumulator tracks recoveries not cases): A — accumulator H sums dN_IR+dN_AR (recoveries) but is used as expected case count in measurement model
- Finding 2 (dmeasure subtracts deaths inconsistently): A — cases-deaths compared to rho*H (recoveries) has no mechanistic justification
- Finding 3 (rho > 1 allowed in global search box): A — search box sets rho in c(0,2) making infeasible starting values for a reporting rate
- Finding 4 (No profile likelihoods or CIs): B — parameter identifiability entirely unassessed; pairs plot insufficient substitute (matches Human Issue #4)
- Finding 5 (No non-mechanistic benchmark): A — POMP not compared against IID negative binomial or equivalent baseline
- Finding 6 (ARIMA/POMP likelihood comparison invalid): A — likelihoods evaluated on different data series and observation models, not directly comparable
- Finding 7 (Placeholder text in intervention periods): A — "x-x and x-x" never filled in; intervention periods not mapped to calendar dates
- Finding 8 (Only 8 global search replicates): C — too few replicates for 15-parameter model; standard is 40-100
- Finding 9 (Convergence plots as static PNG images): C — pre-generated images cannot be verified as coming from the described analysis
- Finding 10 (No process noise in transmission): D — binomial demographic stochasticity only; no environmental/overdispersion noise on Beta (matches Human Issue #2)
- Finding 11 (rw.sd = 0.01 uniformly for all parameters): C — uniform perturbation ignores parameter scale differences; below course standard of 0.02
- Finding 12 (Fixed initial conditions, no sensitivity analysis): C — I_0 = 250 unjustified and no sensitivity to alternative values shown
- Finding 13 (H accumulator mismatch also affects rmeasure): C — rmeas generates cases = rnorm(rho*H)+D, inconsistent with dmeas and misuses stock D vs. flow deaths
- Finding 14 (ACF interpretation overstated for stationarity): C — slow ACF decay cited for differencing without formal unit root test
- Finding 15 (AIC table may contain numerical instability): C — Gaussian ARIMA applied to non-Gaussian overdispersed counts without log-transform

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ODE equation notation errors in the text — Section 2.2 equations use destination rather than source compartments")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No profile likelihoods — pairs plot hints at identifiability issues but this is not assessed")
- Human Issue #5: missed

**Findings classification:**
- Major 1 (Invalid ARIMA-POMP log-likelihood comparison): A — direct comparison of ARIMA and POMP log-likelihoods is statistically invalid due to different observation models and parameter counts
- Major 2 (Accumulator H tracks recoveries not cases): A — accumulator variable H accumulates dN_IR + dN_AR (recoveries), not incident infections, causing systematic model misspecification
- Major 3 (Only 8 search replicates): A — global and local IF2 searches use only 8 replicates, insufficient for a 16-parameter model
- Major 4 (No profile likelihoods): B — no profile likelihoods computed; pairs plot hints at identifiability problems (especially collinearity of Beta and intervention scalars) but identifiability is not formally assessed (matches Human Issue #4)
- Major 5 (ODE equation notation errors): B — Section 2.2 transition rate equations use destination compartments instead of source compartments; Csnippet code is correct so this is a presentation error (matches Human Issue #1)
- Major 6 (Global search box for rho outside (0,1)): A — search box allows rho starting values above 1, which are invalid probability values and undefined on the logit scale
- Major 7 (No model diagnostics): A — no conditional log-likelihood plot, ESS, filtering trajectories, or simulation comparisons; convergence claim is unsupported
- Major 8 (Fixed and implausible initial conditions): A — I_0 = 250 and S_0 = N are hardcoded and not estimated or sensitivity-tested
- Major 9 (Measurement model inconsistency rmeasure/dmeasure): A — rmeas adds cumulative D to simulated cases while dmeas subtracts observed deaths, inconsistent if D is cumulative and deaths is a period count
- Minor (Typo in file names): C — code reads "greaklakes.csv" instead of "greatlakes.csv"
- Minor (Spectral analysis conclusion): C — 150-day cycle identified by spectrum analysis is disconnected from the ARIMA and POMP models, which include no seasonal component
- Minor (Model Assumption 1 placeholder text): C — Section 2.2.1 contains unfilled "x-x" placeholders for time intervals
- Minor (ACF interpretation): C — backwards phrasing about when to reject IID; substantive conclusion is accidentally correct
- Minor (ARIMA model diagnostic): C — inverse roots near unit circle noted but no simpler models investigated
- Minor (Forecast methodology absent): C — no forecasts or one-step-ahead simulations from the fitted POMP model
- Minor (No uncertainty quantification): C — only point estimates reported; no confidence or credible intervals for any parameter
- Minor (Reproducibility): C — no set.seed() before parallel searches; exact reproduction across machines is impossible

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ID 21.13.2 — parameter non-identifiability, trace plots show no convergence, no profile likelihoods reported")
- Human Issue #5: missed

**Findings classification:**
- ID 21.13.1: A — measurement model accumulates recoveries (dN_IR + dN_AR) rather than new cases; H tracks wrong quantity
- ID 21.13.2: B — parameter non-identifiability with no profile likelihoods; convergence claim unsupported by trace plots (matches Human Issue #4)
- ID 21.13.3: A — insufficient global search: only 8 starting points for a 15-dimensional parameter space
- ID 21.13.4: A — ARIMA-POMP log-likelihood comparison is not directly valid across different observation models and data transformations
- ID 21.13.5: A — mathematical description of I-compartment transitions inconsistent with code (conservation law violated in equations but correct in code)
- ID 21.13.M1: C — notation inconsistency for E-to-A/P rate (mu_EAP vs. mu_EI across text and code)
- ID 21.13.M2: C — placeholder text ("x-x") in intervention assumptions; day-count thresholds never mapped to calendar dates
- ID 21.13.M3: C — ESS dips at days ~75 and ~330 not discussed
- ID 21.13.M4: C — Normal measurement model can produce negative case counts; NegBin or Poisson with overdispersion recommended
- ID 21.13.M5: C — ARIMA residuals show heavy tails and ACF exceedances; no remedial action taken
- ID 21.13.M6: C — no sessionInfo() or pomp version reported
- ID 21.13.M7: C — typos ("Comparision", "paris plot") and incomplete bibliographic entries for references [6]–[11]

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 9 | 6 | 7 | 4 |
| B (AI major, human also found) | 1 | 1 | 2 | 1 |
| C (AI minor, human missed) | 4 | 7 | 8 | 7 |
| D (AI minor, human also found) | 1 | 1 | 0 | 0 |
| E (Human found, AI missed) | 4 | 3 | 3 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 4 | 1/5 = 20% | 9 | 4 | 13/15 = 87% |
| Charlie | 1 | 1 | 3 | 2/5 = 40% | 6 | 7 | 13/15 = 87% |
| Doug | 2 | 0 | 3 | 2/5 = 40% | 7 | 8 | 15/17 = 88% |
| Evan | 1 | 0 | 4 | 1/5 = 20% | 4 | 7 | 11/12 = 92% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: Not all references are cited in the project. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: There could have been more discussion of the presented results. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 5 human issues (40%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: Section 2.2 presents an ODE model and then a POMP model including stochasticity, but does not explain the relationship between the two. The ODE model is the deterministic skeleton for the actual model used. Additionally, there is an inconsistency: the SE rate is correctly proportional to I+A+P in the stochastic version, but only proportional to I in the skeleton, which is presumably a typo. (Covered only by Doug)
- Human Issue #2: Overdispersion in the process model might also help — the binomial process noise seems too small to fit the data well. (Covered only by Charlie)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 1 |
| Evan | 0 |
