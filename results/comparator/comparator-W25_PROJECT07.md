# Comparator Analysis — W25 Project 07

---

## Human Issues

1. The SARIMA analysis has limitations, but is good enough to provide a reasonable benchmark for comparison to mechanistic models. SARIMA would be better on a log scale.

2. The novel mechanistic model is developed until it meets the benchmark and has somewhat plausible simulations and parameter values. More could be done, but this is already a nontrivial accomplishment.

3. The report says, "The residuals from the SARIMA model appear to be white noise overall." This is a weak interpretation. The tails are substantially longer than normal. One point could even be considered an outlier. The residuals have a slow trend.

4. Infectious disease data (like many other non-negative data types) usually fits linear Gaussian assumptions better after a log transform. We have seen this many times in class and in midterm projects. The team should carry out their linear data analysis on the log scale.

5. It would be worth trying to understand the parameter estimates, since that would lead to insights about what biological interpretation the fitted model is actually proposing. How do they fit with known dengue epidemiology? The value $\rho=4\times 10^{-5}$ might be a useful clue.

6. The two year data period is okay for studying high-frequency behavior, but the full 2010-2023 dataset (perhaps aggregated to months) would give better understanding of inter-annual dynamics.

7. It is incorrect that "The oscillating pattern displayed in the ACF plots supports that the data is non-stationary." The usual motivation for the sample ACF assumes a stationary model.

8. An unclear assertion, "By comparing the AIC values and model complexity, the most appropriate model is: SARIMA(2,0,0)×(0,0,1)". SARIMA(1,0,1)×(0,0,1) has the same complexity and better AIC, so the reasoning is unclear.

9. This dataset is called "Travel-related cases" so it may be that not much local transmission occurs in US. In that case, modeling US cases by an SIR model (or any extension of it) may be hard to interpret. The pattern could be driven not by US transmission but by a sinusoidal fluctuation in imported cases.

10. The model supposes that $N=3.2\times 10^6$ Americans are at risk of dengue. Where does this figure come from?

11. A referee requested discussion about the homogeneous mixing assumption behind compartment models. That is an interesting topic: that assumption motivates the model and guides its interpretation, but ultimately the statistical skill of the model is judged by its ability to fit the data regardless of fact that humans do not mix anything like homogeneously.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No ACF of SARIMA Residuals — claim of no strong autocorrelation is unsubstantiated; incomplete residual diagnostics")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "SIRS recovery rate mu_IR=0.8 implies biologically implausible infectious period; final estimated parameters not discussed in terms of biological plausibility")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "ACF Interpretation Error — oscillating ACF that decays is consistent with stationary seasonal ARMA, not evidence of non-stationarity")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Fundamental Mechanistic Mismatch — SIR-type models applied to imported case data, producing parameters with no epidemiological meaning")
- Human Issue #10: covered (matched by finding: "Implausible Population Size N=4e9 in SIRS, inconsistency across models including unexplained N=3.2 million in SEIR")
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Fundamental Mechanistic Mismatch — SIR models applied to imported case data): B — matches Human Issue #9
- Finding 2 (Inconsistent Data Preparation Across the Three Models): A — log-likelihoods invalid due to models fit on potentially different data
- Finding 3 (No Profile Likelihood or Confidence Intervals): A — Npoints_profile defined but never used; no uncertainty quantification
- Finding 4 (Poorly Motivated "Pandemic Switch" at Week 29 in SIRS): A — ad hoc threshold with no epidemiological justification
- Finding 5 (Implausible Population Size N=4e9, inconsistency across models): B — matches Human Issue #10
- Finding 6 (H Accumulates Recoveries Not New Infections — mislabeled as cumulative incidence): A — incorrect measurement equation and misleading code comment
- Finding 7 (SEIR Global Search Claims 200 Starting Points but Only 100 Specified): A — direct factual inconsistency between text and code
- Finding 8 (SEIR Local Search Uses ncpu Rather Than Nlocal): A — reproducibility undermined; far fewer runs than intended
- Finding 9 (SIRS Recovery Rate mu_IR=0.8 Implies Unrealistically Short Infectious Period): D — matches Human Issue #5
- Finding 10 (No ACF of SARIMA Residuals — Incomplete Residual Diagnostics): D — matches Human Issue #3
- Finding 11 (SARIMA Period Set to 53 Weeks, POMP Models Use 52): C — inconsistency in seasonal period across models, not discussed
- Finding 12 (No ODE Formulation or R0 Derivation for SEIR Model): C — asymmetric mathematical rigor across SIRS and SEIR
- Finding 13 (SIRS Global Search Loglik Not Explicitly Reported): C — unclear distinction between local and global search results for SIRS
- Finding 14 (k Fixed in SEIR but Estimated in SIRS — Non-Comparable Models): C — invalid log-likelihood comparison without AIC adjustment
- Finding 15 (ACF Interpretation Error — Oscillating Pattern Does Not Indicate Non-Stationarity): D — matches Human Issue #7

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Missing ACF for SARIMA residuals — text claims no strong autocorrelation without showing the ACF residual plot")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "SIRS rho fixed at epidemiologically implausible values — rho=4e-5 with N=3.25e8 implies ~5 million infections/week, scrutinizing rho biologically")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "ACF interpretation contradicts SARIMA specification — oscillating ACF is characteristic of a stationary seasonal process, not evidence of non-stationarity")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Biologically implausible and inconsistent N — N=3.2e6 for SEIR and other values are unjustified")
- Human Issue #11: missed

**Findings classification:**
- Major 1 (No profile likelihoods for any model parameter): A — neither SIRS nor SEIR computes profile likelihoods; profile variables defined but never used
- Major 2 (SIRS global search severely underpowered): A — Nglobal=20 and Nmif=50 for SIRS vs Nglobal=100 and Nmif=100 for SEIR; SIRS optimum may not have been found
- Major 3 (Biologically implausible and inconsistent N): B — N spans three orders of magnitude across models, none justified; SEIR N=3.2e6 specifically unjustified (matches Human Issue #10)
- Major 4 (SEIR overdispersion parameter k never estimated): A — k fixed at initial guess of 10 throughout SEIR despite being in log-transform list; no justification
- Major 5 (SEIR initial conditions E and I hard-coded): A — E=10 and I=70 hard-coded in rinit rather than estimated; SIRS correctly parameterizes all fractions
- Major 6 (SIRS rho fixed at epidemiologically implausible values): B — rho silently changes from 1e-7 to 4e-5 without explanation; both values imply implausible infection counts; directly engages rho=4e-5 as a biological red flag (matches Human Issue #5)
- Major 7 (No particle filter diagnostics for SEIR model): A — no ESS plot, no conditional log-likelihood trace for SEIR; asymmetric relative to SIRS
- Major 8 (Seasonal period inconsistency 52 vs 53): A — SARIMA uses period=53 but both POMP models use 52, introducing systematic phase drift
- Minor 1 (rw.sd values below course standard for SIRS): C — rw.sd=0.01 used vs course standard of 0.02; unexplained
- Minor 2 (ACF interpretation contradicts SARIMA specification): D — oscillating ACF cited as evidence of non-stationarity but fitted SARIMA has d=0, D=0; self-contradiction (matches Human Issue #7)
- Minor 3 (SEIR phi log-transform inappropriate for phase shift): C — phi forced positive by log-transform, different convention from SIRS phase parameter d; direct comparison impossible
- Minor 4 (Pandemic switch terminology and justification): C — "pandemic switch" term misleading for 2022-2023 travel-pattern break; structural break interpretation unclear
- Minor 5 (SEIR global search pairs plot 1000-unit range): C — filter retains results up to 1000 log-likelihood units below max, mixing optimal and catastrophically poor runs
- Minor 6 (SIRS pairs plot includes guess rows with NA log-likelihoods): C — NA rows from guesses may distort axis scaling in pairs plot
- Minor 7 (Missing ACF for SARIMA residuals): D — ACF of residuals omitted from SARIMA diagnostics; claim of "no strong autocorrelation" unsubstantiated (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Reporting rate rho fixed at biologically implausible values without justification")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "ACF analysis conclusion conflates oscillating pattern with non-stationarity")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "SEIR population size N is implausibly small by two orders of magnitude")
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (SEIR fitted on different dataset than SIRS): A — different dataset used for SEIR vs. SIRS, invalidating likelihood comparison
- Finding 2 (Global searches anchored to local-search mif2 chain): A — anti-pattern causing global search to not explore parameter space from fresh starts
- Finding 3 (SEIR accumulator tracks recoveries not new cases): A — H += dN_IR is semantic mismatch with reported case data
- Finding 4 (SEIR N implausibly small by two orders of magnitude): B — N=3.2 million vs. correct ~335 million (matches Human Issue #10)
- Finding 5 (Invalid comparison of SARIMA and POMP log-likelihoods): A — observation models are incompatible, making direct numeric comparison invalid
- Finding 6 (No profile likelihoods for any parameter): A — identifiability and confidence intervals cannot be assessed without profiles
- Finding 7 (Reporting rate rho fixed at biologically implausible values): B — rho=1e-7 is implausible for CDC travel surveillance and contradicted by SEIR estimate of ~0.9 (matches Human Issue #5)
- Finding 8 (SEIR local search uses nbrOfWorkers() instead of Nlocal): C — replicate count varies with execution environment
- Finding 9 (Post-local-search simulations hardcode k=10): C — optimized overdispersion parameter not used in post-search simulation blocks
- Finding 10 (No particle filter diagnostic for SEIR before local search): C — no ESS or conditional log-likelihood plot to verify filter health before IF2
- Finding 11 (SIRS run-level switch has 4 values for some parameters but only 3 levels): C — inconsistency in switch() definitions, Nglobal too small
- Finding 12 (SIRS model diagnostics beyond ESS): C — conditional log-likelihood panel not discussed
- Finding 13 (Seasonal amplitude c logit-transformed — inconsistency with upper bound of 1): C — logit upper bound issue in SEIR global box search
- Finding 14 (No out-of-sample or forecasting evaluation): C — models never used to generate forecasts or assess out-of-sample performance
- Finding 15 (ACF analysis conclusion conflates oscillating pattern with non-stationarity): D — oscillating ACF is characteristic of stationary seasonal ARMA, not non-stationarity (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: contradiction (AI says parameter values are biologically implausible/degenerate; human says the model has "somewhat plausible simulations and parameter values")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "degenerate reporting rate ρ ≈ 4×10^-5 in SIRS global search")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "ACF interpretation contradicts SARIMA choice")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "different N values across models invalidate log-likelihood comparison")
- Human Issue #11: missed

**Findings classification:**
- 25.07.1: B — Degenerate reporting rate ρ ≈ 4×10^-5 in SIRS global search (matches Human Issue #5)
- 25.07.2: B — Different N values across models (3.25×10^8 vs 3.2×10^6) invalidate log-likelihood comparison (matches Human Issue #10)
- 25.07.3: F — SEIR μ_IR = 35.6 is biologically implausible (contradicts Human Issue #2, which says parameter values are somewhat plausible)
- 25.07.5: A — Pandemic switch at week 29 is unjustified and untested
- 25.07.6: A — No profile likelihoods or confidence intervals for any parameter
- 25.07.7: C — SEIR k fixed at 10 throughout searches without disclosure
- 25.07.8: D — ACF interpretation ("supports non-stationarity") contradicts SARIMA choice with d=0, D=0 (matches Human Issue #7)
- M1: C — R0 derivation not connected to fitted parameter estimates
- Additional minor (sin/cos seasonal forcing discrepancy): C — SIRS uses sin() while SEIR uses cos() for seasonal forcing with no reconciliation
- Additional minor (SMA root): C — SMA root |z|=1.266 borderline invertibility not noted
- Additional minor (typos): C — Multiple manuscript typos noted
- Additional minor (ChatGPT reference): C — Reference [2] cites ChatGPT for AIC table functions without including generated code

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 6 | 5 | 2 |
| B (AI major, human also found) | 2 | 2 | 2 | 2 |
| C (AI minor, human missed) | 4 | 5 | 7 | 6 |
| D (AI minor, human also found) | 3 | 2 | 1 | 1 |
| E (Human found, AI missed) | 6 | 7 | 8 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 1 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 3 | 6 | 5/11 = 45% | 6 | 4 | 10/15 = 67% |
| Charlie | 2 | 2 | 7 | 4/11 = 36% | 6 | 5 | 11/15 = 73% |
| Doug | 2 | 1 | 8 | 3/11 = 27% | 5 | 7 | 12/15 = 80% |
| Evan | 2 | 1 | 7 | 3/10 = 30% | 2 | 6 | 8/11 = 73% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The SARIMA analysis has limitations, but is good enough to provide a reasonable benchmark for comparison to mechanistic models. SARIMA would be better on a log scale. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Infectious disease data (like many other non-negative data types) usually fits linear Gaussian assumptions better after a log transform. We have seen this many times in class and in midterm projects. The team should carry out their linear data analysis on the log scale. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The two year data period is okay for studying high-frequency behavior, but the full 2010-2023 dataset (perhaps aggregated to months) would give better understanding of inter-annual dynamics. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: An unclear assertion, "By comparing the AIC values and model complexity, the most appropriate model is: SARIMA(2,0,0)×(0,0,1)". SARIMA(1,0,1)×(0,0,1) has the same complexity and better AIC, so the reasoning is unclear. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: A referee requested discussion about the homogeneous mixing assumption behind compartment models. That is an interesting topic: that assumption motivates the model and guides its interpretation, but ultimately the statistical skill of the model is judged by its ability to fit the data regardless of fact that humans do not mix anything like homogeneously. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 11 human issues (45%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #9: This dataset is called "Travel-related cases" so it may be that not much local transmission occurs in US. In that case, modeling US cases by an SIR model (or any extension of it) may be hard to interpret. The pattern could be driven not by US transmission but by a sinusoidal fluctuation in imported cases. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
