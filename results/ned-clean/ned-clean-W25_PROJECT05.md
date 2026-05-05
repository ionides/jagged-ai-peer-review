# Ned-Clean Analysis — W25 Project 05

---

## Human Issues

1. The SARIMA log-likelihood (-96) and POMP log-likelihood (-328) are improperly compared because the SARIMA is fitted to the log of the data and not adjusted for the transformation.
2. One could consider detrending rather than concluding "differencing the series will be advisable and possibly needed."
3. Using a periodogram to infer seasonality is overkill (and the periodogram does not show anything surprising).
4. SARIMA model AIC comparison does not take into account the loss of a datapoint when differencing; AIC is not perfectly comparable.
5. The SARIMA residual diagnostics show a good fit, but the report does not explain clearly that this is fitted to the log of the data.
6. It would be nice to have the Jacobian correction so that the SARIMA log-likelihood for log-data can be properly compared to the POMP log-likelihood for the raw data.
7. Two log-likelihoods claimed to both equal -332.02 are neither equal to -332.01 (they are -331.077 and -331.386) — a strange typo.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "SARIMA log-likelihood comparison not meaningful — SARIMA on log-transformed data, POMP on raw, no Jacobian adjustment")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: same finding #3 — "no Jacobian adjustment is applied to convert the SARIMA log-likelihood to the scale of counts")
- Human Issue #7: missed

**Findings classification:**
- Finding #1 (immigration model never incorporated): A — immigration rproc/paramnames updated but no second pomp() call; model ran without immigration dynamics
- Finding #2 (lambda not multiplied by dt): A — Euler step for dSE uses 1-exp(-lambda) not 1-exp(-lambda*dt), model is step-size dependent
- Finding #3 (SARIMA LL comparison not meaningful): B — SARIMA on log-transformed counts, POMP on raw counts, no Jacobian adjustment (matches Human Issues #1 and #6)
- Finding #4 (sigma_M defined but never used): A — sigma_M in paramnames and par_trans but absent from rmeas/dmeas; measurement remains Poisson
- Finding #5 (cumulative C inconsistency): A — C accumulates rho*dEI but dmeas observes rho*I; C never used in measurement model
- Finding #6 (N_0 = 100000 unrealistically small): A — Florida population ~18-20M; N_0 inflates force of infection by ~200x
- Finding #7 (r = 0.135 implausibly large): A — 13.5% monthly birth rate is biologically impossible; parameter not explored in local search
- Finding #8 (global_inits duplicate entries): A — c(base_params, c(...)) appends rather than overrides named entries; global search unreliable
- Finding #9 (no likelihood profile): A — no profile likelihoods, CIs, or uncertainty quantification for any parameter
- Finding #10 (B-spline not truly periodic): A — splines::bs() does not enforce boundary periodicity; pomp's periodic_bspline_basis() should be used
- Finding #11 (force of infection missing dt in equations): A — mathematical exposition shows stochastic differential form without dt; inconsistent with Euler code
- Finding #12 (mu_H labeled incorrectly): A — mu_H governs mortality across all compartments but is labeled "immunity loss duration"
- Finding #13 (AIC search grid too narrow): A — p_max=1, q_max=1, P=1, Q=1 only; no rationale for excluding higher orders
- Finding #14 (decompose() additive without justification): C — additive decomposition used on untransformed series despite noting non-constant variance
- Finding #15 (no formal SARIMA residual tests): C — only visual inspection; no Ljung-Box or Shapiro-Wilk applied

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 11 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 2 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Log-likelihood comparison between SARIMA and POMP models is not valid — different scales and observation models, Jacobian fix needed")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: same finding #2 — explicitly recommends converting to same likelihood scale, i.e., Jacobian-equivalent fix)
- Human Issue #7: missed

**Findings classification:**
- Finding #1 (POMP underperforms SARIMA with no resolution): A — gap of 230+ LL units acknowledged but dismissed; no diagnostic follow-up provided
- Finding #2 (LL comparison not valid — different scales): B — SARIMA on log1p, POMP on raw Poisson; likelihoods not directly comparable; Jacobian fix recommended (matches Human Issues #1 and #6)
- Finding #3 (sigma_M defined but never used in dmeas/rmeas): A — sigma_M in paramnames and par_trans but dmeas/rmeas implement plain Poisson; reproducibility failure
- Finding #4 (C accumulates dEI but dmeas observes I): A — fundamental mismatch between accumvar tracking and measurement model; C is dead weight
- Finding #5 (no profile likelihoods; identifiability not assessed): A — global search scatter plots are not profile likelihoods; no CIs computable
- Finding #6 (computational effort insufficient; same LL suspicious): A — 20 replicates sparse for 12-parameter model; local and immigration models both converge to -332.02, suggesting optimizer not exploring space
- Finding #7 (global_inits duplicate entries): A — c() appends rather than overrides; global search effectively 20 replicates of local search
- Finding #8 (r = 0.135 biologically implausible): A — 162% annual birth rate impossible; inconsistent with global search initialization range
- Finding #9 (measurement uses I/prevalence not incidence — minor): C — monthly reports are incidence not stock; rho*I conflates flow and stock
- Finding #10 (SARIMA grid too narrow): C — only 16 models searched; claim of "best model" valid only within restricted space
- Finding #11 (periodogram frequency axis labeling misleading): C — spec.pgram returns cycles/month not cycles/year as labeled; 0.0888 corresponds to ~11.26-month period
- Finding #12 (invertibility check does not verify near-boundary): C — Mod(roots)>1 checked but proximity to boundary not assessed; sma1 may be near -1
- Finding #13 (no ESS monitoring): C — no effective sample size reported; filter degeneracy not ruled out
- Finding #14 (simulation comparison purely visual): C — no summary statistics computed; coverage of observed data by simulation envelope not quantified
- Finding #15 (session info not reported): C — no sessionInfo() or package versions; pomp API changes make reproducibility uncertain

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Invalid comparison between SARIMA and POMP log-likelihoods — different observation models, different data scales")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: same finding #1 — "ARIMA model performs differencing internally, altering the effective data further" as a second reason the comparison is invalid)
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: same finding #1 — fix requires evaluating both models under a common observation model or using proper scoring rules)
- Human Issue #7: missed

**Findings classification:**
- Finding #1 (invalid SARIMA vs POMP LL comparison): B — SARIMA on log-transformed, POMP on raw; differencing alters data; valid comparison requires same observation model (matches Human Issues #1, #4, and #6)
- Finding #2 (measurement model inconsistent — C vs I): A — C declared in accumvars and updated via dEI but dmeas observes I; C never read by measurement
- Finding #3 (no non-mechanistic benchmark on same scale): A — SARIMA comparison invalid; no Poisson/NB benchmark on raw counts fitted
- Finding #4 (inadequate global search scale): A — 20 starting points insufficient for 14+ parameter model; standard practice requires 200-400 replicates
- Finding #5 (no profile likelihoods or CIs): A — global scatter plots are not profiles; no identifiability assessment possible
- Finding #6 (no convergence diagnostics — no LL traces): A — parameter trace plots shown but no LL traces across iterations; convergence not demonstrated
- Finding #7 (measurement model lacks overdispersion — sigma_M never used): A — sigma_M in paramnames/par_trans but absent from dmeas/rmeas; Poisson underestimates uncertainty
- Finding #8 (accumulator C declared but never read by dmeas): A — C resets to 0 at each observation time but measurement links to I; C is dead code
- Finding #9 (population dynamics implausible — N_0=100k, r=0.135): A — 200-fold population error; birth rate of 100%+ per year; transmission parameters uninterpretable
- Finding #10 (global search initialization error — duplicate names): A — c(base_params, c(...)) creates duplicate parameter entries; random initialization silently ignored; global search is effectively local search
- Minor: notation error in SARIMA equation (B operator omitted): C — (1+theta_1)(1+Theta_1*B^12) should be (1+theta_1*B)(1+Theta_1*B^12)
- Minor: AIC grid search narrow: C — p,q in {0,1} only; optimal order not guaranteed
- Minor: no Ljung-Box or formal residual test for SARIMA: C — visual ACF inspection only; autocorrelation may be missed near significance threshold
- Minor: epsilon semantics ambiguous: C — epsilon/N may dominate force of infection when I~0 in non-endemic setting; not discussed
- Minor: no convergence traces for local search: C — trace plots shown only for global search; local search convergence unverifiable
- Minor: simulation from best_local uses wrong parameter vector length: C — slicing by index rather than name is fragile; may accidentally include loglik columns
- Minor: no acknowledgment of model limitations for imported malaria: C — constant immigration rate may be poor approximation for heterogeneous travel-linked importation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "25.05.1 — Invalid SARIMA vs POMP likelihood comparison — SARIMA on log1p, POMP on raw integer counts")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: same finding 25.05.1 — suggests fitting count-data baseline or explicitly acknowledging scales differ; Jacobian-equivalent fix)
- Human Issue #7: missed

**Findings classification:**
- 25.05.1 (invalid SARIMA vs POMP LL comparison): B — SARIMA on log1p continuous variable, POMP on raw integer counts; different observation distributions and scales; conclusion about inferiority does not follow (matches Human Issues #1 and #6)
- 25.05.4 (no profile likelihoods; scatter plots not profiles): A — scatter plots show endpoint parameter values from 20 runs, not re-optimized profiles; no CIs computable
- 25.05.5 (unconverged parameter traces): A — log-likelihood trace still increasing at iteration 100; reported estimates are lower bounds, not stable MLEs
- 25.05.2 (sigma_M declared but no effect in code): C — sigma_M in paramnames but absent from dmeas C-snippet; measurement equidispersed Poisson
- 25.05.6 (sma1 = -1.000 at invertibility boundary): C — coefficient at boundary may indicate overdifferencing; "invertible" check technically true but boundary case warrants discussion
- 25.05.7 (r biologically implausible): C — r=0.135 month^{-1} implies 13.5% monthly growth (~4-fold annually); likely transcription from source paper with different time units
- 25.05.10 (SARIMA equation notation error): C — (1+theta_1)(1+Theta_1*B^12) omits B from non-seasonal MA polynomial
- M-1 (ESS not monitored): C — effective sample size not reported; filter degeneracy not ruled out given small Np=1000 in local search

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 11 | 8 | 9 | 2 |
| B (AI major, human also found) | 2 | 2 | 3 | 2 |
| C (AI minor, human missed) | 2 | 7 | 7 | 5 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 5 | 5 | 4 | 5 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 2 | 0 | 5 | 28.6% (2/7) | 11 | 2 | 86.7% (13/15) |
| Charlie | 2 | 0 | 5 | 28.6% (2/7) | 8 | 7 | 88.2% (15/17) |
| Doug | 3 | 0 | 4 | 42.9% (3/7) | 9 | 7 | 84.2% (16/19) |
| Evan | 2 | 0 | 5 | 28.6% (2/7) | 2 | 5 | 77.8% (7/9) |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: One could consider detrending rather than concluding "differencing the series will be advisable and possibly needed." — missed by all 4 reviewers
- Human Issue #3: Using a periodogram to infer seasonality is overkill (the periodogram does not show anything surprising). — missed by all 4 reviewers
- Human Issue #5: The SARIMA residual diagnostics do not explain clearly that the analysis is fitted to the log of the data. — missed by all 4 reviewers
- Human Issue #7: Two log-likelihoods both claimed to equal -332.02 are neither equal to -332.01 (they are -331.077 and -331.386) — a numerical reporting error. — missed by all 4 reviewers

Consensus miss count: 4 out of 7 human issues (57%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #4 (AIC not comparable after differencing — datapoint loss): covered only by Doug; missed by Alex, Charlie, Evan.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- No profile likelihoods / parameter uncertainty quantification: raised as Major by Alex (finding #9), Charlie (finding #5), Doug (finding #5), Evan (25.05.4). Present in all 4 reviewers.
- sigma_M declared but never used in measurement model (Poisson instead of overdispersed): raised as Major by Alex (#4), Charlie (#3), Doug (#7) and as Minor by Evan (25.05.2). Three of four raise it as Major; Evan raises it as Minor. All four flag it.
- Population size N_0 = 100,000 unrealistically small / r = 0.135 biologically implausible: raised as Major by Alex (#6, #7), Charlie (#8), Doug (#9) and as Minor by Evan (25.05.7). All four flag population/demographic implausibility.
- Global search initialization creates duplicate parameter entries: raised as Major by Alex (#8), Charlie (#7), Doug (#10). Not raised by Evan. Three of four flag this.

Universal AI-only flags (all 4 reviewers): 2 issues — no profile likelihoods; sigma_M declared but unused.
Near-universal (3 of 4 reviewers as Major): population implausibility; global search initialization bug.
