# Ned-Clean Analysis — W25 Project 09

---

## Human Issues

1. dmeas and rmeas are inconsistent: dmeas does not apply home advantage subtraction (to opponents) when playing away.
2. Likelihoods are not reported; the project should present likelihoods (and tools like likelihood ratio test and AIC) in addition to predictive scores.
3. The project is light on diagnostic investigations (outliers, over-dispersion, other model misspecification possibilities).
4. The report does not place the project in the context of other 531 projects or explain what was learned from previous projects (as requested in the assignment description).
5. Classic Elo already adds ~100 points for home court — this relevant context is not mentioned.
6. BPM (Box Plus-Minus) is not defined at first use.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "dmeas and rmeas are inconsistent")
- Human Issue #2: covered (matched by finding: "No likelihood-based model comparison; log-likelihood not reported")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- In-sample prediction as primary evaluation metric: A — no held-out test set, all accuracy figures computed on training data
- Prediction accuracy from stochastic simulations, inconsistent comparison methodology: A — POMP accuracy computed differently from logistic/ELO baselines, making comparisons invalid
- Model 3 code bug (nba_pomp instead of nba_pomp_att): A — attendance model evaluated using wrong pomp object
- dmeas and rmeas inconsistent: B — measurement model inconsistency (matches Human Issue #1)
- sigma fixed and excluded from optimization: A — no justification for sigma=5, no sensitivity analysis
- Global search bounds poorly motivated (home_court_avd box [200,250] vs actual ~89): A — box far from apparent MLE
- No likelihood-based model comparison; log-likelihood not reported: B — matches Human Issue #2
- ELO used as observed data for latent state validation: A — ELO is a derived deterministic quantity, not the true latent state
- t0=1 indexing inconsistency with ELO covariate: C — one-step misalignment between ELO covariate and POMP time index
- BPM covariates boundary conditions for early games not documented: C — rolling window initialization not verified
- No convergence diagnostics or particle filter variance assessments: C — IF2 traces not analyzed; loglik.se not reported
- p_win treated as state variable rather than derived quantity: C — inflates state dimension without benefit
- Hardcoded absolute file paths prevent reproducibility: C — paths tied to author's local machine
- Logistic regression in-sample accuracy — baseline misleading: C — 64% baseline is in-sample fit, not predictive
- Attendance dmeas never updated to include attendance covariate: C — IF2 for attendance model optimizes wrong likelihood

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "dmeasure and rmeasure compute win probability on incompatible numerical scales")
- Human Issue #2: covered (matched by finding: "No quantitative goodness-of-fit reporting (no log-likelihood or AIC)")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- dmeasure/rmeasure incompatible scales: B — win probability computed on different numerical inputs in dmeas vs rmeas (matches Human Issue #1)
- Global search box excludes local-search MLE for home_court_avd: A — box [200,250] far from MLE at ~89
- rw.sd values set equal to parameter starting values: A — enormously large perturbations cause IF2 to diffuse rather than converge
- Global search initialized from previous mif2 result rather than base pomp object: A — inherits near-zero cooling schedule, undermining global exploration
- No quantitative goodness-of-fit reporting (no log-likelihood or AIC): B — matches Human Issue #2
- No non-mechanistic statistical benchmark: A — logistic regression and ELO are not independent time-series benchmarks
- Hard-coded absolute file paths prevent reproducibility: A — paths tied to author's local machine
- Simulation-based accuracy evaluated against incorrect reference outcomes in Model 2 and Model Att: A — wrong pomp object and wrong ground truth used
- sigma fixed but undiscussed: C — no justification for sigma=5, role relative to ELO scale not discussed
- p_win stored as state variable, no inferential purpose: C — deterministic function of current state, adds no information
- Bradley-Terry probability formula in text differs from dmeas implementation: C — text equation and code implementation mathematically different for away games
- ELO initial condition set with malformed date: C — as.Date(10/24/2023) evaluates 10/24/2023 as division, not a date string
- Only 20 IF2 iterations used: C — far below standard practice; perturbations have already decayed by final iteration
- Prediction accuracy mixes in-sample and out-of-sample metrics: C — all accuracy figures computed on same 164-game training set
- Typos and grammatical issues: C — "there is there an underlying truth," "Attendence," "did due compared"

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "dmeas and rmeas implement different probability models on incompatible scales")
- Human Issue #2: covered (matched by finding: "No log-likelihood or AIC reported; goodness-of-fit is purely visual and simulation-based")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- dmeas and rmeas implement different probability models on incompatible scales: B — matches Human Issue #1
- No log-likelihood or AIC reported; goodness-of-fit purely visual/simulation-based: B — matches Human Issue #2
- Global search box excludes the MLE found during that same search: A — home_court_avd box [200,250] vs best value ~89
- Model 3 (attendance) best-parameter simulation uses wrong pomp object: A — nba_pomp used instead of nba_pomp_att
- Global search uses previous mif2 result as base rather than raw pomp object: A — inherits decayed cooling schedule, not genuine global search
- No benchmark comparison against non-mechanistic statistical model: A — logistic regression and ELO are not independent time-series benchmarks
- Computational adequacy very low: Np=1000 and Nmif=20 with no convergence evidence: A — insufficient iterations; loglik.se computed but not reported
- Prediction accuracy evaluated on training data, not held-out games: A — in-sample accuracy not a valid predictive metric
- sigma fixed throughout, never estimated or justified: A — arbitrary value; conditional MLE unreliable
- rw.sd values set to parameter starting values: A — perturbation SD equal to starting value; causes IF2 diffusion
- Hard-coded absolute paths: C — paths tied to author's local machine
- p_win as state variable, not a population quantity: C — deterministic derived quantity; unnecessary in statenames
- Model 2 best-parameter simulation uses nba_pomp (Model 1 object) instead of nba_pomp2: C — silent error in Model 2 evaluation
- ELO provided as both covariate and data column, creating confusion: C — unclear whether elo column is used in model or only for plotting
- Attendance logistic regression accuracy compared against wrong dataset: C — mean(pred_win_att == bpm$Win) should use bpm_att$Win
- No parameter uncertainty or confidence intervals: C — no profile likelihoods; no basis for concluding parameters are reliably estimated
- Conclusion overstates evidence: C — "drastically improved predictive power" unsupported given measurement inconsistency and in-sample evaluation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "25.09.2 — dmeas and rmeas implement materially different win-probability formulas")
- Human Issue #2: covered (matched by finding: "25.09.5 — Model 2 declared best based on accuracy while log-likelihood and AIC favor Model 1")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- 25.09.1 — sigma never optimized, fixed at 5.00: A — central mechanism of POMP-ELO not estimated; MLE conditional on unjustified value
- 25.09.2 — dmeas and rmeas implement materially different win-probability formulas: B — matches Human Issue #1
- 25.09.3 — Model Att global search table numerically identical to Model 1 (not re-run as separate optimization): A — attendance model was never independently estimated
- 25.09.4 — Base ELO accuracy discrepancy: 57.93% in text vs 66.46% in table: A — 8.5 pp discrepancy changes narrative; comparison table untrustworthy
- 25.09.5 — Model 2 declared best based on accuracy while ΔAIC≈18 favors Model 1: B — AIC/log-likelihood is the correct criterion; matches Human Issue #2
- 25.09.6 — sim_win drawn inside rproc and used for ELO update before actual observation incorporated via filtering: A — structural inconsistency in POMP design
- 25.09.7 — No confidence intervals or profile likelihoods for any parameter: A — point estimates uninterpretable without uncertainty quantification
- 25.09.8 — Only 20 mif2 iterations; parameters not stabilized by final iteration: A — MLE estimates unreliable
- Minor: rmeas uses raw ELO scale while dmeas rescales by /100 (same topic as 25.09.2, not double-counted): C — additional detail on scale inconsistency
- Minor: p_win stored as state variable without justification: C — deterministic derived quantity; unnecessary state dimension
- Minor: Stray plus sign in OPP equation: C — typographical error in model equation
- Minor: ELO update equation in text does not match code (K*E_S vs K*(1-E_S)): C — displayed equation differs from code implementation
- Minor: Model 2 partrans does not include log="alpha": C — alpha positivity constraint may not be enforced for all models
- Minor: No set.seed() calls: C — results not exactly reproducible
- Minor: Software versions not reported: C — R version and pomp version not stated
- Minor: Figure captions absent: C — win probability trace figures have no legend or caption
- Minor: Prose errors: C — "there is there is," "A a crucial player," "we we're unable to," etc.
- Minor: In-sample accuracy note: C — prediction accuracy figures appear to be in-sample

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 6 | 8 | 6 |
| B (AI major, human also found) | 2 | 2 | 2 | 2 |
| C (AI minor, human missed) | 7 | 7 | 7 | 9 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 4 | 4 | 4 | 4 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall | AI-Unique Rate |
|----------|-------------:|---------------:|
| Alex | 2/6 = 33.3% | 13/15 = 86.7% |
| Charlie | 2/6 = 33.3% | 13/15 = 86.7% |
| Doug | 2/6 = 33.3% | 15/17 = 88.2% |
| Evan | 2/6 = 33.3% | 15/17 = 88.2% |

Human Recall = (B+D) / (B+D+E)
AI-Unique Rate = (A+C) / (A+B+C+D)

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (4 out of 6):

- Human Issue #3: The project is light on diagnostic investigations (outliers, over-dispersion, other model misspecification possibilities).
- Human Issue #4: The report does not place the project in the context of other 531 projects or explain what was learned from previous projects.
- Human Issue #5: Classic Elo already adds ~100 points for home court — this relevant context is not mentioned.
- Human Issue #6: BPM (Box Plus-Minus) is not defined at first use.

### Unique finds per reviewer

Human issues covered by only one reviewer (all others missed): none. Issues #1 and #2 were covered by all four reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention (3 issues):

1. In-sample prediction used as the sole evaluation metric (no held-out test set or cross-validation). All four reviewers flagged this as a major weakness of the model comparison.
2. sigma is fixed at an arbitrary value (5) throughout all optimization runs with no justification, sensitivity analysis, or profile likelihood. All four reviewers identified this as undermining the reported MLE estimates.
3. p_win is stored as a state variable (in statenames) despite being a deterministic function of team_strength and opp_strength at each step. All four reviewers noted this as unnecessary and potentially confusing.
