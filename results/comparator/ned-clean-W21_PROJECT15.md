# Ned-Clean Analysis — W21 Project 15

---

## Human Issues

1. The strong weekly pattern may be the missing piece for getting a mechanistic model to beat an ARMA benchmark (the model does not address or incorporate weekly periodicity).
2. Over-dispersed process noise might also help with model fit (it is absent from the current model).
3. A time-varying measurement model would also make sense in the context of COVID (it is absent from the current model).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- Major 1 (ARMA benchmark likelihood incomparable to SEIR likelihood): A — invalid log-likelihood comparison due to differing observation models and scales
- Major 2 (mu_EI and mu_IR fixed without justification): A — both transition rates fixed at 0.1 with no sensitivity analysis or profile likelihood
- Major 3 (profile likelihood for rho underpowered): A — only three points above chi-squared threshold; CI unreliable
- Major 4 (local search results suppressed with eval=FALSE): A — local search table and pairs plots not rendered; key diagnostics missing
- Major 5 (initial states E=100, I=200 ad hoc): A — no estimation or sensitivity analysis for initial conditions
- Major 6 (tau estimated ~0.09 but not interpreted): A — overdispersion parameter value not discussed in context of measurement model
- Minor 7 (measurement model notation sign error): C — text has positive exponent in binomial probability; code correctly has negative sign
- Minor 8 (no convergence diagnostics beyond trace plots): C — no formal convergence metric; local search pairs plots suppressed
- Minor 9 (piecewise beta breakpoints not epidemiologically motivated): C — date boundaries for beta regimes not linked to documented policy events
- Minor 10 (NCORES=1 means serial execution): C — parallelization negated; reproducibility impaired
- Minor 11 (SARMA AIC table suppressed): C — model selection results hidden; reader cannot verify SARMA(3,3)x(1,1)_7 choice
- Minor 12 (no discussion of R0 or Rt): C — estimated beta values not translated into epidemiologically interpretable reproduction numbers
- Minor 13 (rho ~0.48 claimed reasonable without external validation): C — no comparison to seroprevalence or ascertainment studies
- Minor 14 (measurement model applied to H tracking recoveries, not incidence): C — semantic mismatch between accumulator and observed case definition
- Minor 15 (no formal model diagnostics — ESS): C — no effective sample size plots or particle filter diagnostics presented

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "SEIR fails to beat SARMA; 7-day seasonal cycle should have motivated model revision")
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- Major 1 (SEIR fails to beat SARMA; no structural revision attempted): B — identifies the weekly/seasonal cycle as the key gap and flags failure to address it (matches Human Issue #1)
- Major 2 (rho profile CI based on only three points above threshold): A — profile is statistically unreliable; CI not robustly determined
- Major 3 (rw.sd for tau negligibly small; tau cannot be optimized by mif2): A — perturbation too small to bridge gap from starting value to MLE
- Major 4 (MLE for tau lies at global search box boundary): A — optimizer pushed tau to its upper bound; true MLE not found
- Major 5 (mu_EI and mu_IR fixed without profile or identifiability assessment): A — no formal justification; sensitivity not assessed
- Major 6 (profile CI construction conflates profile and global search results): A — profile envelope built from all run types, not profile-specific runs
- Minor 7 (local search results hidden from report): C — table and pairs plots set to eval=FALSE
- Minor 8 (no model diagnostics beyond forward simulation): C — no ESS, conditional log-likelihoods, or filtering distribution comparisons
- Minor 9 (beta break dates appear post-hoc): C — not linked to documented policy events with citations
- Minor 10 (no model structure comparisons using likelihood): C — no LRT or AIC comparing alternative beta specifications
- Minor 11 (initial conditions unexplained 300-person discrepancy): C — S+E+I at t=0 implies ~90% already recovered, which is implausible
- Minor 12 (SARMA AIC value inconsistent with reported log-likelihood): C — AIC of 231.698 is on log-transformed scale, not original scale
- Minor 13 (measurement model undefined when H=0): C — degenerate normal distribution when accumulator is zero
- Minor 14 (single-core execution for 500-start global search): C — total computation time not reported; adequacy cannot be assessed
- Minor 15 (no parameter uncertainty beyond rho): C — no profile likelihoods for beta parameters, eta, or tau

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- Major 1 (global search initializes from local-search mif2 result, inheriting cooled state): A — cooling schedule inherited from local search; global search not genuinely exploring parameter space
- Major 2 (invalid direct log-likelihood comparison between SARMA and SEIR): A — different observation models and data scales; comparison is not a valid model selection exercise
- Major 3 (mu_EI and mu_IR fixed without formal identifiability justification): A — fixes inflate precision of other estimates; collinearity not assessed
- Major 4 (profile likelihood for rho relies on only three points above CI threshold): A — CI statistically unreliable; profile curve noisy near maximum
- Major 5 (profile rho guess-stratification conflates all run types): A — profile guesses drawn from all run IDs (local, global, profile combined)
- Major 6 (no model diagnostic tools applied — ESS, conditional log-likelihoods): A — no particle filter diagnostics or filtering distribution comparisons
- Minor 7 (accumulator H tracks recoveries, not new infections): C — semantic mismatch between dN_IR and confirmed case definition
- Minor 8 (rmeasure uses rnorm without integer enforcement verification): C — implementation appears consistent but should be verified against zero-count observations
- Minor 9 (initial conditions E=100, I=200 fixed without estimation or sensitivity): C — hard-coded values not profiled over; early dynamics may be sensitive
- Minor 10 (rho CI uses global-search max as reference without explicit filtering): C — code should filter to id==2 before computing reference maximum
- Minor 11 (computational effort at run_level=2 may be insufficient): C — loglik.se up to 0.62 for MLE; doubling NP not tested
- Minor 12 (SARMA model selection run with eval=FALSE): C — AIC grid search hidden; reproducibility not guaranteed
- Minor 13 (no discussion of tau parameter estimates): C — tau near box boundary not noted; no profile for tau
- Minor 14 (IID negative binomial comparison trivially easy to beat): C — low-bar benchmark; SARMA is the informative comparison
- Minor 15 (conclusion overstates model fit quality): C — SEIR outperformed by SARMA by 47 log-units; conclusion does not acknowledge this failure

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- M2 (profile likelihood for rho too sparse to support reported CI): A — only 3 points above threshold; CI bounds determined by single observations
- M3 (no convergence diagnostics for global search): A — no trace plots for global search runs; convergence to MLE not verifiable
- M4 (ARMA benchmark comparison: Jacobian correction not explained in text): C — correction is applied in code but not described; readers may question validity
- M1 (sensitivity of fixed mu_EI and mu_IR not assessed): C — defensible given external evidence but no sensitivity runs reported
- M5 (fixed initial conditions E_0=100, I_0=200 without sensitivity analysis): C — narrative justification only; no sensitivity or estimation
- m7 (run-level parameters not reported in text): C — Np, Nmif, NREPS_EVAL not stated; computational adequacy cannot be assessed
- m8 (ESS not reported): C — particle degeneracy not monitored; early epidemic dynamics may produce low ESS
- m14 (truncated normal measurement model lacks justification): C — negative binomial is standard; no comparison or explicit justification provided
- new1 (no profiles for beta parameters): C — five contact-rate parameters are central scientific result but have no CIs
- new2 (forward simulation vs. filtering distribution): C — figures show unconditional forward simulations, not filtering-distribution-conditioned diagnostics
- m6 (pathological divergence in local search traces not discussed): C — b3 reaching ~100 in some chains not acknowledged in text

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 5 | 6 | 2 |
| B (AI major, human also found) | 0 | 1 | 0 | 0 |
| C (AI minor, human missed) | 9 | 9 | 9 | 9 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 3 | 2 | 3 | 3 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall = (B+D)/(B+D+E) | AI-Unique Rate = (A+C)/(A+B+C+D) |
|----------|-----------------------------:|----------------------------------:|
| Alex | 0/3 = 0.00 | 15/15 = 1.00 |
| Charlie | 1/3 = 0.33 | 14/15 = 0.93 |
| Doug | 0/3 = 0.00 | 15/15 = 1.00 |
| Evan | 0/3 = 0.00 | 11/11 = 1.00 |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: Over-dispersed process noise might help with model fit — missed by all 4 reviewers.
- Human Issue #3: A time-varying measurement model would make sense in the COVID context — missed by all 4 reviewers.

**2 out of 3 human issues are consensus misses (missed by all reviewers).**

Human Issue #1 was covered by Charlie only (all other reviewers missed it).

### Unique finds per reviewer

| Reviewer | Unique finds (human issues covered by this reviewer alone) |
|----------|-----------------------------------------------------------:|
| Alex | 0 |
| Charlie | 1 (Human Issue #1: weekly pattern as missing fix) |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer (all 4) that the human did not mention:

1. Profile likelihood for rho is underpowered / too sparse — all 4 reviewers flagged this (Alex Major 3, Charlie Major 2, Doug Major 4, Evan Major M2).
2. mu_EI and mu_IR are fixed without adequate justification or sensitivity analysis — all 4 reviewers flagged this (Alex Major 2, Charlie Major 5, Doug Major 3, Evan Minor M1).
3. Initial conditions E_0=100, I_0=200 are fixed without estimation or sensitivity analysis — all 4 reviewers flagged this (Alex Major 5, Charlie Minor 11, Doug Minor 9, Evan Minor M5).
4. No particle filter diagnostics (effective sample size / ESS) presented — all 4 reviewers flagged this (Alex Minor 15, Charlie Minor 8, Doug Major 6, Evan Minor m8).

**4 universal AI-only flags identified.**
