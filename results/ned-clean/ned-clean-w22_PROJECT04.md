# Ned-Clean Analysis — W22 Project 04

---

## Human Issues

1. Best not to describe weekly periodicity as "seasonality" — seasonality corresponds to annual cycles.
2. Figure captions would be helpful; the blue line in simulations is presumably the data but is not described.
3. Diagnostics show difficulty explaining the resurgence at the end of the data (low effective sample size), but this may not be too critical.
4. The fits around the MLE have a very high reporting rate, close to 1 — how do you interpret that?
5. It would be good to compare the likelihood (AIC) between the mechanistic model and the ARMA benchmark; ARMA appears to do somewhat better.
6. Typo: "$I_t$: the number of recovered at time $t$" (should be $R_t$).
7. Spell checking: e.g., "pubilic", and "casual" for "causal".
8. The plot titled "differenced data" is differenced log data, but the adjacent ACF is for unlogged data — not apparent without studying source code.
9. Referencing observations by date rather than observation number would be easier to understand.

---

## Alex

**Coverage record:**
- Human Issue #1 (seasonality terminology): missed
- Human Issue #2 (figure captions/blue line): missed
- Human Issue #3 (diagnostics/resurgence/low ESS): missed
- Human Issue #4 (high rho interpretation): covered (matched by finding: "H accumulates dN_IR only; alpha-rho identifiability and rho near 1 not interpreted")
- Human Issue #5 (benchmark comparison): covered (matched by finding: "Likelihood benchmark comparison is missing")
- Human Issue #6 (I_t typo): covered (matched by finding: "Copy-paste error: I_t defined twice")
- Human Issue #7 (spell checking): missed
- Human Issue #8 (differenced data/ACF mismatch): missed
- Human Issue #9 (date vs observation number): missed

**Findings classification:**
- Finding 1 — dN_RS drawn from I instead of R [CRITICAL BUG]: A — fundamental implementation bug invalidating reinfection pathway
- Finding 2 — nearbyint split violates population conservation [CRITICAL BUG]: A — individuals created or destroyed at each step
- Finding 3 — H accumulates dN_IR only; alpha-rho identifiability not discussed [CRITICAL]: B — matches Human Issue #4 (reporting rate near 1 and its interpretation)
- Finding 4 — Time-varying beta with ad hoc breakpoints [MAJOR]: A — no justification or sensitivity analysis for breakpoints
- Finding 5 — Key parameters fixed without justification [MAJOR]: A — mu_PR, mu_IR, alpha, Beta fixed with no source cited
- Finding 6 — mu_RS fixed at local search value; circular reasoning [MAJOR]: A — global search inherits local optimum
- Finding 7 — No profile likelihood or confidence intervals [MAJOR]: A — no uncertainty quantification for any parameter
- Finding 8 — Likelihood benchmark comparison missing [MAJOR]: B — matches Human Issue #5 (POMP vs ARMA comparison)
- Finding 9 — Initial conditions hard-coded [MODERATE]: C — E=100, I=200, P=50 not estimated or justified
- Finding 10 — I_t defined twice (copy-paste error) [MODERATE]: D — matches Human Issue #6 (I_t typo)
- Finding 11 — Spectral analysis on non-stationary series [MODERATE]: C — apparent 7-day period may be artifact
- Finding 12 — Particle filter SE very large at starting point [MODERATE]: C — SE=78.32 at initial parameters
- Finding 13 — Global search uses only 10 starting points [MODERATE]: C — weak coverage of 9-dimensional space
- Finding 14 — SARIMA model selection incomplete [MINOR]: C — seasonal MA and higher-order terms not explored
- Finding 15 — Introduction data description mismatch [MINOR]: C — description does not match actual analysis window

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (seasonality terminology): missed
- Human Issue #2 (figure captions/blue line): missed
- Human Issue #3 (diagnostics/resurgence/low ESS): missed
- Human Issue #4 (high rho interpretation): covered (matched by finding: "H tracks recoveries — rho and alpha identifiability never discussed")
- Human Issue #5 (benchmark comparison): covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #6 (I_t typo): covered (matched by finding: "Typographical error: I_t defined twice")
- Human Issue #7 (spell checking): missed
- Human Issue #8 (differenced data/ACF mismatch): missed
- Human Issue #9 (date vs observation number): missed

**Findings classification:**
- Issue 1 — dN_RS draws from I instead of R [Critical]: A — fundamental compartment bug
- Issue 2 — R compartment never decreases; population conservation violated [Critical]: A — R grows monotonically
- Issue 3 — H tracks recoveries (dN_IR) not new infections; rho-alpha identifiability [Critical]: B — matches Human Issue #4 (high rho and its interpretation)
- Issue 4 — eta missing from parameter transformation [Major]: A — eta can escape [0,1] during perturbation
- Issue 5 — No profile likelihoods computed [Major]: A — no identifiability assessment or confidence intervals
- Issue 6 — Parameters fixed without statistical justification [Major]: A — mu_PR, mu_IR, alpha, Beta, mu_RS fixed ad hoc
- Issue 7 — No non-mechanistic benchmark comparison [Major]: B — matches Human Issue #5 (POMP vs ARMA)
- Issue 8 — Insufficient global search replicates (10 runs) [Major]: A — too few for 9-dimensional space
- Issue 9 — I_t defined twice [Major]: B — matches Human Issue #6 (I_t typo)
- Issue 10 — AIC comparison not addressed on common scale [Minor]: C — both likelihoods reported separately but not compared
- Issue 11 — Spectral frequency/period calculation not shown [Minor]: C — 0.13 cycles/day inversion not documented
- Issue 12 — mu_EPI convergence problem acknowledged but not addressed [Minor]: C — noted and ignored
- Issue 13 — Initial conditions for E, I, P fixed without justification [Minor]: C — E=100, I=200, P=50 arbitrary
- Issue 14 — SARIMA residuals not fully interpreted [Minor]: C — non-normality dismissed; no Ljung-Box test
- Issue 15 — Intervention indicator gap at time step 35 [Minor]: C — unassigned time step creates one-day anomaly

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1 (seasonality terminology): missed
- Human Issue #2 (figure captions/blue line): missed
- Human Issue #3 (diagnostics/resurgence/low ESS): covered (matched by finding: "Model diagnostics — ESS not examined; particle fails between time 110 and 120")
- Human Issue #4 (high rho interpretation): covered (matched by finding: "rho near 1 interpretation" minor bullet)
- Human Issue #5 (benchmark comparison): covered (matched by finding: "No benchmark comparison against non-mechanistic model")
- Human Issue #6 (I_t typo): covered (matched by finding: "Typo in state variable description" minor bullet)
- Human Issue #7 (spell checking): missed
- Human Issue #8 (differenced data/ACF mismatch): missed
- Human Issue #9 (date vs observation number): missed

**Findings classification:**
- Major 1 — Critical rprocess bug: dN_RS draws from I instead of R: A — fundamental compartment error
- Major 2 — No benchmark comparison against non-mechanistic model: B — matches Human Issue #5 (POMP vs ARMA)
- Major 3 — Direct comparison of SARIMA and POMP log-likelihoods is invalid: A — different observation models on different data scales
- Major 4 — No profile likelihoods; parameter identifiability not assessed: A — pairs plots cannot substitute for profile likelihood
- Major 5 — Multiple key parameters fixed without scientific justification: A — no sources cited, no sensitivity analysis
- Major 6 — Insufficient computational scale; convergence not demonstrated: A — 10 replicates too few; mu_EPI shows convergence problem
- Major 7 — Accumulator H tracks wrong flow (dN_IR instead of new infections): A — systematic mismatch between observation model and data
- Major 8 — Normal approximation with potentially non-positive support: A — particle degeneracy when H=0
- Major 9 — Global search fixes mu_RS at local search value; circular: A — unresolved identifiability suppressed by fixing
- Major 10 — Model diagnostics (ESS) not examined: B — matches Human Issue #3 (low ESS / diagnostic difficulty)
- Minor — Typo: I_t duplicated: D — matches Human Issue #6 (I_t typo)
- Minor — Intervention indicator gap at time 35: C — one-day anomaly in transmission schedule
- Minor — rho near 1 interpretation: D — matches Human Issue #4 (high rho near 1)
- Minor — No out-of-sample validation or forecast: C — fitted model not used to project forward
- Minor — Initial conditions largely fixed (E, I, P): C — sensitivity not assessed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (seasonality terminology): missed
- Human Issue #2 (figure captions/blue line): covered (matched by finding: "22.04.M4 — Simulation plots lack labeled observed data overlay")
- Human Issue #3 (diagnostics/resurgence/low ESS): missed
- Human Issue #4 (high rho interpretation): covered (matched by finding: "22.04.3 — Profile likelihoods absent; rho ≈ 1 cannot be distinguished from artifact without CIs")
- Human Issue #5 (benchmark comparison): covered (matched by finding: "22.04.2 — No quantitative SARIMA vs. POMP comparison")
- Human Issue #6 (I_t typo): covered (matched by finding: "22.04.M1 — Notation error: R_t mislabeled as I_t")
- Human Issue #7 (spell checking): missed
- Human Issue #8 (differenced data/ACF mismatch): missed
- Human Issue #9 (date vs observation number): missed

**Findings classification:**
- 22.04.1 — Code bug: dN_RS drawn from I instead of R [Major]: A — reinfection pathway not correctly implemented
- 22.04.2 — No quantitative SARIMA vs. POMP comparison [Major]: B — matches Human Issue #5 (benchmark comparison)
- 22.04.3 — Profile likelihoods absent; rho ≈ 1 and eta ≈ 0.9 uninterpretable without CIs [Major]: B — matches Human Issue #4 (high rho interpretation)
- 22.04.4 — mif2 log-likelihood not confirmed by replicated pfilter [Major]: A — biased estimate used as absolute measure
- 22.04.5 — Global search under-sampled (~5-10 points) [Major]: A — one extreme outlier (b1 ≈ 4000) signals optimizer escape
- 22.04.6 — Initial conditions E, I, P hard-coded without justification [Major]: A — affects early dynamics and Beta/b1 estimates
- 22.04.M1 — R_t mislabeled as I_t [Minor]: D — matches Human Issue #6 (I_t typo)
- 22.04.M2 — mu_RS biological plausibility (0.65-day reinfection interval) [Minor]: C — implies implausibly rapid reinfection
- 22.04.M3 — Gaussian measurement model allows negative counts [Minor]: C — negative binomial more appropriate
- 22.04.M4 — Simulation plots lack labeled observed data overlay [Minor]: D — matches Human Issue #2 (figure captions/blue line)
- 22.04.M5 — SARIMA residuals show heteroscedasticity; log-transform not considered [Minor]: C — variance heterogeneity during peak
- 22.04.M6 — Seasonal differencing order D not stated [Minor]: C — D value never specified in text
- 22.04.M7 — Forward simulation vs. filtering distribution not distinguished [Minor]: C — stronger test of fit not conducted

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 6 | 8 | 4 |
| B (AI major, human also found) | 2 | 3 | 2 | 2 |
| C (AI minor, human missed) | 6 | 6 | 3 | 5 |
| D (AI minor, human also found) | 1 | 0 | 2 | 2 |
| E (Human found, AI missed) | 6 | 6 | 5 | 5 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall | AI-Unique Rate |
|----------|-------------:|---------------:|
| Alex | 3/9 = 0.333 | 12/15 = 0.800 |
| Charlie | 3/9 = 0.333 | 12/15 = 0.800 |
| Doug | 4/9 = 0.444 | 11/15 = 0.733 |
| Evan | 4/9 = 0.444 | 9/13 = 0.692 |

- Human Recall = (B + D) / (B + D + E)
- AI-Unique Rate = (A + C) / (A + B + C + D)

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (4 out of 9):

- Issue #1: Best not to describe weekly periodicity as "seasonality" — missed by all four reviewers.
- Issue #7: Spell checking ("pubilic", "casual" for "causal") — missed by all four reviewers.
- Issue #8: The "differenced data" plot uses differenced log data but the adjacent ACF uses unlogged data — missed by all four reviewers.
- Issue #9: Referencing observations by date rather than observation number — missed by all four reviewers.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Issue #2 (figure captions / unlabeled blue line): covered only by Evan (M4).
- Issue #3 (diagnostics / low ESS at resurgence): covered only by Doug (Major 10).

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 1 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention (5 issues):

1. The `dN_RS` transition in the rprocess Csnippet draws from compartment I instead of R, breaking the reinfection pathway that is the model's central biological motivation.
2. No profile likelihoods are computed for any parameter, making it impossible to assess identifiability or report valid confidence intervals.
3. Multiple key parameters (mu_PR, mu_IR, alpha, Beta, and mu_RS) are fixed without scientific justification, literature citations, or sensitivity analysis.
4. The global search uses too few replicates (10 starting points) to reliably explore a high-dimensional parameter space, with no convergence evidence.
5. Initial conditions for E, I, and P are hard-coded as arbitrary round numbers without estimation or sensitivity analysis.
