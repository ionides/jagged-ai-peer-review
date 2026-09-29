# Comparator Analysis — W22 Project 11

---

## Human Issues

1. The outlier removal decisions seem reasonable. However, the county data reveal that some of these outliers are shared across counties, which makes it harder to explain them as data collection or processing errors.

2. The MIF2 diagnostics show that some of the searches essentially failed (green and cyan in the local search). It might be clearer to remove them from subsequent analysis.

3. It would be useful to compare to an ARMA or log-ARMA benchmark likelihood, to give some indication of whether substantial additional changes are required reach the point of having a mechanistic model with good statistical fit.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "outliers removed without statistical justification")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "no comparison to a baseline model")

**Findings classification:**
- Finding 1 [R update equation incorrect]: A — R recovered-compartment update equation is wrong, yielding a residual rather than a genuine Markov state
- Finding 2 [iota goes negative]: A — iota is unconstrained and the MLE uses a negative value, which is epidemiologically impossible
- Finding 3 [implausible R0]: A — local MLE gives R0 ~ 83 and global MLE gives R0 = 202, far outside the accepted chickenpox range
- Finding 4 [outliers removed without justification]: B — six data points removed solely by visual inspection with no statistical test or citation (matches Human Issue #1)
- Finding 5 [global search R0 range narrower than local result]: A — global search bounds R0 in [6,14] while local search converged to R0 ~ 83, creating an unresolved inconsistency
- Finding 6 [alpha fixed vs. perturbed contradiction]: A — alpha is excluded from estpars but still appears in rw.sd, creating a code/specification contradiction
- Finding 7 [no baseline model comparison]: B — no reference log-likelihood, SARIMA, or simpler model comparison is reported (matches Human Issue #3)
- Finding 8 [single simulation replicate]: A — model evaluation uses nsim=1, preventing any assessment of predictive uncertainty
- Finding 9 [vaccination implementation conflates recovery]: A — vaccination flow is applied only to newborns via birth rate, conflating vaccination with recovery
- Finding 10 [duplicate rows in CSV]: C — cpox_params_1.csv contains many exact duplicate rows, inflating the apparent number of independent search evaluations
- Finding 11 [cooling fraction too aggressive]: C — cooling.fraction.50 = 0.1 reduces perturbations to 10% after 50 iterations, leaving too little exploration
- Finding 12 [initial parameters borrowed from Birmingham measles without justification]: C — sigma, gamma, amplitude, alpha, iota, psi, sigmaSE taken directly from a measles calibration without chickenpox-specific justification
- Finding 13 [rho calculation is circular]: C — rho is derived by dividing total cases by total births, which conflates incidence with birth cohort size
- Finding 14 [implausible global MLE values unremarked]: C — global simulation uses gamma = 922 and iota = -0.43 but these epidemiologically impossible values are not discussed
- Finding 15 [seasonality windows copied from measles]: C — English school-term windows from a measles case study are applied without adaptation to Hungarian chickenpox

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "outlier removal not adequately justified — no formal criterion given")
- Human Issue #2: covered (matched by finding: "large Monte Carlo standard error in several local search likelihood evaluations, signaling failed runs")
- Human Issue #3: covered (matched by finding: "no non-mechanistic benchmark comparison")

**Findings classification:**
- Finding 1 (biologically implausible MLE parameters from global search): A — R0=202, gamma=922, iota=-0.429 accepted uncritically
- Finding 2 (negative iota used as best-fit parameter): A — implementation bug; iota enters force-of-infection expression without non-negativity constraint
- Finding 3 (global search loglik lower than local search, unresolved): A — gap of ~77 log-likelihood units with no corrective action
- Finding 4 (no non-mechanistic benchmark comparison): B — matches Human Issue #3
- Finding 5 (no formal profile likelihoods; identifiability not assessed): A — "poor man's profile" for vr only, no profiles for R0, rho, gamma
- Finding 6 (cooling fraction 0.1 is very aggressive): A — perturbations effectively zero before search completes; not justified
- Finding 7 (large Monte Carlo SE in local search evaluations): B — matches Human Issue #2
- Finding 8 (R0 from local search also biologically implausible at 82.67): C — flagged in Discussion but not diagnosed or constrained
- Finding 9 (outlier removal not adequately justified): D — matches Human Issue #1
- Finding 10 (global search fixes initial conditions rather than estimating them): C — introduces potentially large bias in global likelihood surface
- Finding 11 (simulation diagnostics use only one trajectory): C — nsim=1 cannot reveal model's predictive uncertainty
- Finding 12 (iota lacks log transformation in partrans): C — duplicate angle on the same bug as Finding 2; optimizer can silently reach negative values
- Finding 13 (no ARIMA/spectral analysis baseline for EDA): C — about EDA framing, not benchmark likelihood comparison
- Finding 14 (eval=FALSE code blocks reference undefined objects): C — reproducibility issue; objects from prior eval=FALSE blocks would not exist at runtime
- Finding 15 (vaccination implementation may double-count individuals): C — population balance S+E+I+R=pop should be verified

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Outlier removal without formal justification — no quantitative criterion, analysis not shown robust to inclusion")
- Human Issue #2: covered (matched by finding: "Local search cooling fraction very aggressive — non-converged chains visible in trace plots")
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison — no ARIMA/SARIMA/auto-regressive baseline provided")

**Findings classification:**
- Finding 1 (Population conservation violated in R compartment): A — R = pop - S - E - I + vac double-counts vaccinated individuals, inflating population at every step
- Finding 2 (Global search box severely misaligned with MLE): A — declared box excludes actual MLE by factor 10–60 in several parameters
- Finding 3 (Global search initialized from previous mif2 result): A — anti-pattern: mf1 passed instead of base pomp object, cooling schedule near-expired at start
- Finding 4 (Global search performs worse than local by 77 LL units): A — gap of 77.4 log-likelihood units renders global "best parameters" unreliable
- Finding 5 (Negative iota / potential NaN in force of infection): A — iota=-0.43 with non-integer alpha causes pow(negative, non-integer)=NaN in C
- Finding 6 (No non-mechanistic benchmark comparison): B — no ARIMA/SARIMA/auto-regressive baseline (matches Human Issue #3)
- Finding 7 (No profile likelihoods computed): A — no genuine profile likelihoods for any of the 11 estimated parameters
- Finding 8 (Implausible parameter estimates not interrogated): A — R0=82.7 is ~8x literature value; sigma implies 3.2-day incubation vs known 10-21 days
- Finding 9 (Seasonality windows copied from UK measles without verification): A — English school-calendar windows applied to Hungarian data without checking Hungarian calendar
- Finding 10 (Initial conditions inconsistent across searches): C — global search fixes S_0/E_0/I_0/R_0 from local result while local search estimates them, making likelihoods non-comparable
- Finding 11 (Outlier removal without formal justification): D — no prespecified quantitative criterion; authors remove six points without robustness check (matches Human Issue #1)
- Finding 12 (Measurement model uses normal approximation to negative binomial): C — pnorm/rnorm used instead of dnbinom_mu/rnbinom, problematic for small counts
- Finding 13 (rho initialized from cases/births ratio): C — incorrect initialization rationale, though rho is subsequently estimated via IF2
- Finding 14 (Local search cooling fraction very aggressive): D — cooling.fraction.50=0.1 leads to near-zero perturbations by final iteration; non-converged chains visible (matches Human Issue #2)
- Finding 15 (Global evaluation table presents biologically incoherent parameters): C — gamma=922 implies 0.4-day recovery, vr=0.62 contradicts stated low-vaccination motivation, no caveats given

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "C8 — outlier removal without documented criterion; neither provides a rationale distinguishing data error from genuine extreme event")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "C1 — no non-mechanistic benchmark; explicitly calls for ARMA/SARIMA comparison")

**Findings classification:**
- C1: B — no non-mechanistic benchmark (matches Human Issue #3)
- C2: A — biologically implausible parameter estimates (R0=82–202, sigma implying ~3-day latent period)
- C3: A — no proper profile likelihood or confidence intervals
- C4: A — global search maximum 77 log-likelihood units below local search maximum
- C5: A — single forward simulation draw; no quantitative goodness-of-fit metric
- C6: A — initial conditions fixed in global search without justification
- C7: C — negative iota allowed in optimization, causing potential numerical instability
- C8: D — outlier removal without documented criterion (matches Human Issue #1)
- C9: C — run_level used for reported results not stated in text
- C10: C — measurement model choice (normal approximation) not justified
- M1: C — vaccine effectiveness 0.92 hardcoded, confounds with estimated vr

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 7 | 5 | 8 | 5 |
| B (AI major, human also found) | 2 | 2 | 1 | 1 |
| C (AI minor, human missed) | 6 | 7 | 4 | 4 |
| D (AI minor, human also found) | 0 | 1 | 2 | 1 |
| E (Human found, AI missed) | 1 | 0 | 0 | 1 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 0 | 1 | 2/3 = 67% | 7 | 6 | 13/15 = 87% |
| Charlie | 2 | 1 | 0 | 3/3 = 100% | 5 | 7 | 12/15 = 80% |
| Doug | 1 | 2 | 0 | 3/3 = 100% | 8 | 4 | 12/15 = 80% |
| Evan | 1 | 1 | 1 | 2/3 = 67% | 5 | 4 | 9/11 = 82% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

(none)

Total consensus misses: 0 out of 3 human issues (0%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
