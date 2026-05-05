# Ned-Clean Analysis — W21 Project 13

---

## Human Issues

1. The ODE model (deterministic skeleton) and the POMP model (stochastic) are not clearly related/explained; also, the SE rate is proportional to I+A+P in the stochastic version but only proportional to I in the skeleton — presumably a typo.
2. Overdispersion in the process model might also help — the binomial process noise seems too small to fit the data well.
3. Not all references are cited in the project.
4. The convergence plots show weak identifiability of some parameters; this should be noted explicitly.
5. There could have been more discussion of the presented results.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No profile likelihood or confidence intervals — identifiability unassessed; pairs plots not interpreted in terms of identifiability")
- Human Issue #5: missed

**Findings classification:**
- Major 1 (H accumulator tracks recoveries, not incidence): A — measurement model fundamentally misspecified
- Major 2 (Deaths in rmeasure/dmeasure inconsistent): A — rmeasure generates cases = X + D, dmeasure evaluates density of cases - deaths
- Major 3 (D is cumulative stock, used as daily deaths): A — D grows unboundedly, misrepresents daily death count
- Major 4 (rho logit-constrained but box allows rho > 1): A — improper search box for a reporting probability
- Major 5 (Intervention periods not aligned to calendar dates): A — day-index thresholds never mapped to actual policy events
- Major 6 (ARIMA/POMP likelihood comparison invalid): A — different observation models and data transformations; no complexity penalty
- Major 7 (Only 8 IF2 chains): A — insufficient for 16-parameter model
- Major 8 (alpha mislabeled and used inconsistently): A — "presymptomatic case portion" label is opposite of what code implements; estimated values conflict with cited literature
- Major 9 (nearbyint rounding bias in binomial splits): A — violates population conservation
- Major 10 (No profile likelihood or confidence intervals): B — matches Human Issue #4
- Minor 11 (ARIMA near-unit-circle roots not investigated): C — potential near-cancellation noted but not pursued
- Minor 12 (Spectrum analysis vague and unused): C — 150-day cycle identified but not incorporated or rigorously assessed
- Minor 13 (Convergence described without quantitative evidence): C — visual inspection only, no quantitative diagnostics
- Minor 14 (I_0=250 not justified; N not adjusted for initial infecteds): C — epidemiological justification absent
- Minor 15 (Observation model text describes weekly recovered cases; data is daily confirmed cases): C — disconnect between text description and implementation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No process noise in transmission — binomial demographic stochasticity insufficient for COVID overdispersion")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No profile likelihoods — identifiability unassessed; pairs plot hints at ridges but convergence claim unsupported")
- Human Issue #5: missed

**Findings classification:**
- Major 1 (H accumulator tracks recoveries not cases): A — semantic mismatch between accumulator and observed data
- Major 2 (dmeasure subtracts deaths inconsistently): A — cases - deaths compared to rho*H with no mechanistic justification
- Major 3 (Global search box allows rho > 1): A — invalid probability starting values for logit-constrained parameter
- Major 4 (No profile likelihoods): B — matches Human Issue #4
- Major 5 (No non-mechanistic benchmark comparison): A — ARIMA not a valid direct mechanistic benchmark; IID baseline absent
- Major 6 (ARIMA/POMP likelihood comparison invalid): A — different data transformations and observation models
- Major 7 (Placeholder text in intervention assumptions): A — "x-x and x-x" never filled in; day indices never mapped to calendar dates
- Minor 8 (Only 8 global search replicates): C — insufficient for 15-parameter model
- Minor 9 (Convergence plots as pre-generated PNG images): C — not inline-generated; reproducibility gap
- Minor 10 (No process noise in transmission): D — matches Human Issue #2
- Minor 11 (rw.sd = 0.01 uniformly for all parameters): C — may slow exploration of weakly identified parameters
- Minor 12 (Fixed initial conditions with no sensitivity analysis): C — I_0=250 not justified; no sensitivity check
- Minor 13 (H accumulator semantic mismatch also affects rmeasure; D stock vs daily flow): C — D cumulative added in rmeasure but daily deaths subtracted in dmeasure
- Minor 14 (ACF interpretation overstated for stationarity): C — no formal ADF test applied
- Minor 15 (AIC table may contain numerical instability for larger ARIMA models): C — Gaussian assumption violated for COVID count data

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
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No profile likelihoods — parameter identifiability not assessed")
- Human Issue #5: missed

**Findings classification:**
- Major 1 (Invalid direct ARIMA/POMP log-likelihood comparison): A — different observation models and data transformations; no complexity penalty
- Major 2 (H accumulator tracks recoveries not incident cases): A — rho absorbs biologically meaningless ratio
- Major 3 (Only 8 search replicates — computational inadequacy): A — insufficient diversity for 16-parameter space
- Major 4 (No profile likelihoods — identifiability not assessed): B — matches Human Issue #4
- Major 5 (ODE equation notation errors — destination vs source compartments): A — text uses R_t, D_t as rates where source compartment should appear; code correct
- Major 6 (Global search box for rho outside (0,1)): A — logit(1.5) undefined; invalid starting values
- Major 7 (No model diagnostics reported): A — no conditional log-likelihood, ESS, or simulation comparison
- Major 8 (Fixed and implausible initial conditions): A — I_0=250 not justified; no sensitivity analysis
- Major 9 (rmeasure/dmeasure inconsistency with D stock vs flow): A — D cumulative in state vs daily deaths in data
- Minor (Typo in file names — "greaklakes"): C — would cause read error if file renamed
- Minor (Spectral analysis disconnected from modeling): C — 150-day cycle identified but no seasonal component added
- Minor (Placeholder text in intervention assumptions): C — "x-x" intervals never filled in
- Minor (ACF interpretation phrasing backwards): C — substantive conclusion accidentally correct
- Minor (ARIMA near unit-circle roots not investigated): C — near-cancellation noted but simpler model not pursued
- Minor (Forecast methodology absent): C — no one-step-ahead simulation from filtering distribution
- Minor (No uncertainty quantification for parameter estimates): C — point estimates only, no CI
- Minor (No set.seed before parallel searches): C — exact reproduction impossible

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ID 21.13.2 — Parameter non-identifiability with no profile likelihoods; trace plots show spread; convergence claim unsupported")
- Human Issue #5: missed

**Findings classification:**
- ID 21.13.1 (H accumulates recoveries, not cases): A — mean_cases = rho*H tracks wrong quantity; D (cumulative) added to simulated cases
- ID 21.13.2 (Parameter non-identifiability with no profile likelihoods): B — matches Human Issue #4
- ID 21.13.3 (Insufficient global search — only 8 starts for 15-dimensional space): A — insufficient diversity; convergence not established
- ID 21.13.4 (ARIMA-POMP likelihood comparison requires qualification): A — different observation models and data transformations
- ID 21.13.5 (Mathematical description inconsistent with code for I-compartment transitions): A — text draws dN_IR and dN_ID independently from full I; code correctly draws dN_ID from residual I - dN_IR
- M1 (Notation inconsistency for E-to-A/P rate): C — mu_EAP vs mu_EI vs mu_EI in code
- M2 (Placeholder text in intervention assumptions): C — "x-x and x-x" never filled; day indices not mapped to calendar dates
- M3 (ESS dips at days ~75 and ~330 not discussed): C — suggests model-data tension during early onset and December surge
- M4 (Normal measurement model can produce negative case counts): C — count-appropriate model (NegBin/Poisson) would be more appropriate
- M5 (ARIMA residuals show non-normality and possible seasonality): C — QQ-plot heavy tails; no remediation pursued
- M6 (Missing session info and software versions): C — R and pomp versions not reported
- M7 (Typos and incomplete references): C — references [6]–[11] missing author/journal/volume/page information

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
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 9 | 6 | 8 | 4 |
| B (AI major, human also found) | 1 | 1 | 1 | 1 |
| C (AI minor, human missed) | 5 | 7 | 8 | 7 |
| D (AI minor, human also found) | 0 | 1 | 0 | 0 |
| E (Human found, AI missed) | 4 | 3 | 4 | 4 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | B+D | B+D+E | Human Recall | A | C | A+B+C+D | AI-Unique Rate |
|----------|--:|--:|--:|----:|------:|-------------:|--:|--:|--------:|---------------:|
| Alex | 1 | 0 | 4 | 1 | 5 | 20.0% | 9 | 5 | 15 | 93.3% |
| Charlie | 1 | 1 | 3 | 2 | 5 | 40.0% | 6 | 7 | 15 | 86.7% |
| Doug | 1 | 0 | 4 | 1 | 5 | 20.0% | 8 | 8 | 17 | 94.1% |
| Evan | 1 | 0 | 4 | 1 | 5 | 20.0% | 4 | 7 | 12 | 91.7% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer (Alex, Charlie, Doug, Evan) failed to cover:

- Human Issue #1: ODE skeleton / stochastic POMP relationship not explained; SE rate discrepancy (proportional to I in skeleton vs I+A+P in stochastic) — presumably a typo.
- Human Issue #2: Overdispersion in the process model might help — binomial process noise seems too small. *(Note: Charlie covered this; the consensus miss is among Alex, Doug, and Evan only — see below.)*
- Human Issue #3: Not all references are cited in the project.
- Human Issue #5: There could have been more discussion of the presented results.

Strict consensus misses (all four reviewers missed): Human Issues #1, #3, and #5 — 3 out of 5 human issues (60%).

Human Issue #2 was missed by Alex, Doug, and Evan but covered by Charlie. Human Issue #4 was covered by all four reviewers.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Alex: none
- Charlie: Human Issue #2 (process overdispersion / binomial noise too small) — covered by Charlie only
- Doug: none
- Evan: none

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- H accumulator tracks recoveries, not incident cases (measurement model misspecified): raised as Major by Alex, Charlie, Doug, and Evan — 4 out of 4 reviewers.
- ARIMA/POMP log-likelihood comparison invalid (different observation models and data transformations): raised as Major by Alex, Charlie, Doug, and Evan — 4 out of 4 reviewers.
- No profile likelihoods / identifiability not assessed: raised as Major by all four reviewers — however, this matches Human Issue #4, so it is not a pure AI-only flag.
- Only 8 IF2 chains / insufficient global search: raised as Major by Alex, Charlie (minor), Doug, and Evan — Alex, Doug, Evan classified as Major; Charlie classified as Minor.
- Global search box allows rho > 1 (invalid for logit-constrained probability): raised as Major by Alex, Charlie, and Doug; not present in Evan. 3 out of 4 reviewers.
- rmeasure/dmeasure inconsistency (D stock vs daily flow): raised by Alex (Major 2+3), Charlie (Minor 13), Doug (Major 9), Evan (Major 1 partly) — all four reviewers touched this in some form.

Strictly universal AI-only Major flags (all four reviewers, not matching any human issue):

1. H accumulator tracks recoveries, not incident cases — raised as Major by all four reviewers. (4 out of 4)
2. ARIMA/POMP likelihood comparison is invalid due to different observation models/data transformations — raised as Major by all four reviewers. (4 out of 4)

Count: 2 universal AI-only Major flags.
