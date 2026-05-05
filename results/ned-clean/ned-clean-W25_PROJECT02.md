# Ned-Clean Analysis — W25 Project 02

---

## Human Issues

1. The analysis is missing a non-mechanistic benchmark comparison.
2. Section/equation/figure numbers would be helpful.
3. The form of the model is not given any justification; why one parameterization was chosen is not addressed.
4. A typo in the transition density formula: the exponent should be -(x_n - phi*x_{n-1})^2 / (2*sigma^2), not -(phi*x_{n-1})^2 / (2*sigma^2).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding #4 — "Transition Density Formula Contains a Typo")

**Findings classification:**
- Finding 1 (Incorrect sign interpretation for gamma): A — Major; AI finds the writeup incorrectly states negative gamma means less scoring against stronger pitching, when the correct sign is positive
- Finding 2 (Profile likelihood from suboptimal starting box): A — Major; AI finds profile is seeded from local search region (~40 log-likelihood units below global MLE), making the profile and its CI uninformative
- Finding 3 (AR(1) params show no momentum): A — Major; AI finds phi≈-0.02 and sigma≈0.58 means the latent state is essentially i.i.d. noise (random effects), not momentum
- Finding 4 (Transition density typo): B — Major; matches Human Issue #4
- Finding 5 (Primary conclusion rests on Poisson outperformed by NB): A — Major; AI finds the Poisson model is 41 log-likelihood units worse than NB static, so the primary inference is drawn from a poorly-fit model
- Finding 6 (NBin AR1 MLL slightly worse than NBin static): A — Major; AI finds AR1 NB MLL (-396.461) is slightly below static NB (-396.458), indicating convergence failure in the NB global search
- Finding 7 (run_level hardcoded to "explore"): C — Minor (Moderate); AI finds code cannot reproduce stored results because nseq=5 vs stored nseq=500
- Finding 8 (Pairwise scatterplot mislabeled as local search): C — Minor (Moderate); AI finds figure in Local Search section uses global search results
- Finding 9 (Wilks approximation at boundary): C — Minor (Moderate); AI finds sigma=0 is a boundary condition and chi-squared(2) is an approximation
- Finding 10 (No ACF/autocorrelation analysis in EDA): C — Minor (Moderate); AI finds EDA shows only time series plot and five-number summary, no ACF
- Finding 11 (Code comment incorrectly describes log(mu)): C — Minor (Moderate); AI finds comment conflates mu with log(mu) in parameterization
- Finding 12 (Inconsistent parameter_trans): C — Minor; AI finds partrans differs between blinded.Rmd and Full_Code.Rmd initial object
- Finding 13 (No model adequacy assessment): C — Minor; AI finds no simulation from fitted model at MLE estimates for adequacy check
- Finding 14 (Opponent strength uses future data): C — Minor; AI finds Z_n constructed using full-season data including post-game-n observations
- Finding 15 (nrow(opp_pitch_games > 0) code bug): C — Minor; AI finds incorrect code that happens to work in this context but is fragile

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding #2 — "Missing non-mechanistic benchmark comparison")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding #1 — "Typographical error in transition density equation")

**Findings classification:**
- Finding 1 (Transition density typographical error): B — Major; matches Human Issue #4
- Finding 2 (Missing non-mechanistic benchmark comparison): B — Major; matches Human Issue #1
- Finding 3 (Insufficient computational effort for global search): A — Major; AI finds 40-unit log-likelihood spread across global search starting points, indicating non-convergence
- Finding 4 (LRT conclusion not robust, Wilks conditions not verified): A — Major; AI finds LRT reverses completely under NB model and sigma=0 is a boundary condition invalidating Wilks' theorem
- Finding 5 (Profile only for phi; identifiability unresolved for gamma, sigma, mu): A — Major; AI finds no profile likelihoods or confidence intervals for other key parameters
- Finding 6 (Parameter transformation inconsistency between files): A — Major; AI finds blinded.Rmd and Full_Code.Rmd define partrans differently for the pomp object
- Finding 7 (Data leakage in opponent-strength covariate): A — Major; AI finds Z_n uses full-season pitcher statistics including post-game-n data
- Finding 8 (Scatterplot mislabeled as local search): C — Minor; AI finds scatterplot labeled under Local Search actually plots global search results
- Finding 9 (nrow code bug): C — Minor; AI finds incorrect parenthesis placement in fallback condition
- Finding 10 (Non-standard density notation, no search bound justification): C — Minor; AI finds model equation uses non-standard PMF notation and no argument is given for parameter search bounds
- Finding 11 (X_0=0 fixed, no sensitivity analysis): C — Minor; AI finds initial condition assumes neutral momentum without verification
- Finding 12 (Poor man's profile not explained): C — Minor; AI finds limitations of the poor man's profile not described to readers
- Finding 13 (No RNG seed reported): C — Minor; AI finds set.seed calls not shown in main report, preventing reproducibility verification
- Finding 14 (Wilks finite-sample calibration): C — Minor; AI finds no parametric bootstrap to calibrate LRT null distribution for series of length 162
- Finding 15 (Missing sessionInfo and package versions): C — Minor; AI finds no sessionInfo() or pinned package environment in supplement

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding #1 — "Absence of a non-mechanistic benchmark")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding #4 — "Mathematical error in AR(1) transition density")

**Findings classification:**
- Finding 1 (No non-mechanistic benchmark): B — Major; matches Human Issue #1
- Finding 2 (Global MLE reveals overdispersion not momentum): A — Major; AI finds phi≈-0.012 and sigma≈0.574 mean the latent AR(1) is absorbing overdispersion, confirmed by NB sensitivity analysis
- Finding 3 (Primary conclusion contradicted by sensitivity analysis): A — Major; AI finds Poisson LRT p<0.001 reverses to p=1 under NB, and NB is the more credible observation model
- Finding 4 (Mathematical error in AR(1) transition density): B — Major; matches Human Issue #4
- Finding 5 (Profile seeded from local optimum region — uninformative): A — Major; AI finds profile sigma box is [0.003, 0.010], far from global MLE sigma=0.574, making the profile invalid
- Finding 6 (Global search initialization anti-pattern): A — Major; AI finds mif2 called on a previous mif2 result object inheriting a cooled perturbation schedule, making global search effectively local
- Finding 7 (LRT at boundary of parameter space): A — Major; AI finds sigma=0 on boundary violates Wilks' theorem conditions
- Finding 8 (No parameter estimates or CIs in main text): C — Minor; AI finds MLE values for phi, sigma, gamma, mu never stated in paper
- Finding 9 (Computational details absent): C — Minor; AI finds Np, Nmif, number of global starts not reported
- Finding 10 (Covariate uses future data): C — Minor; AI finds Z_n uses full 2024 season data including games after game n
- Finding 11 (nrow coding bug): C — Minor; AI finds element-wise comparison applied to full data frame inside nrow()
- Finding 12 (Redundant concatenation in MLL calculation): C — Minor; AI finds same vector concatenated with itself twice in max() call
- Finding 13 (Parameter transformation inconsistency): C — Minor; AI finds partrans differs between blinded.Rmd display and Full_Code.Rmd execution
- Finding 14 (Local search phi convergence unexplained): C — Minor; AI finds phi≈-1 in local search vs phi≈-0.012 in global search discrepancy not resolved
- Finding 15 (Pairwise scatter mislabeled): C — Minor; AI finds scatterplot in Local Search section uses global search results

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by M6 — "No comparison against a non-mechanistic benchmark")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by M5 — "Typographical error in the latent transition density")

**Findings classification:**
- M1 (Conclusion from known-misspecified Poisson model): A — Major; AI finds primary conclusion uses Poisson when the paper's own cited literature and NB sensitivity analysis favor NB
- M2 (LRT does not account for Monte Carlo variability): A — Major; AI finds log-likelihood estimates from particle filtering subject to MC noise of unknown magnitude, making the LRT statistic unreliable
- M3 (Wilks approximation invalid at boundary): A — Major; AI finds sigma=0 is a boundary constraint and chi-squared(2) approximation is not formally correct
- M4 (Poor man's profile, no CIs for any parameter): A — Major; AI finds Figure 7 is upper envelope of global search, not a proper profile; no CIs provided
- M5 (Transition density typo): B — Major; matches Human Issue #4
- M6 (No non-mechanistic benchmark): B — Major; matches Human Issue #1
- m1 (Computational settings not reported in main text): C — Minor; AI finds Np, Nmif, number of random starts absent from main paper
- m2 (Log-transform on mu constrains mu>0): C — Minor; AI finds parameter transformation implicitly constrains mu to be positive without documentation
- m3 (Fixed X_0=0, no sensitivity): C — Minor; AI finds initial condition assumes neutral momentum without justification or check
- m4 (Figure 2 simulated traces difficult to read): C — Minor; AI finds many overlapping blue simulated traces obscure the observed series
- m5 (Dip in conditional log-likelihoods near Game 90 not discussed): C — Minor; AI finds localized drop in conditional log-likelihood not identified or explained
- m6 (phi converges to approximately -1 in local search, not discussed): C — Minor; AI finds scientifically implausible alternating AR(1) pattern at local optimum not addressed
- m7 (Covariate Z_n uses future data): C — Minor; AI finds look-ahead bias in opponent-strength covariate acknowledged only in Discussion

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 5 | 5 | 4 |
| B (AI major, human also found) | 1 | 2 | 2 | 2 |
| C (AI minor, human missed) | 9 | 8 | 8 | 7 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 3 | 2 | 2 | 2 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Recall = (B+D) / (B+D+E)
AI-Unique Rate = (A+C) / (A+B+C+D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 3 | 1/4 = 25.0% | 5 | 9 | 14/15 = 93.3% |
| Charlie | 2 | 0 | 2 | 2/4 = 50.0% | 5 | 8 | 13/15 = 86.7% |
| Doug | 2 | 0 | 2 | 2/4 = 50.0% | 5 | 8 | 13/15 = 86.7% |
| Evan | 2 | 0 | 2 | 2/4 = 50.0% | 4 | 7 | 11/13 = 84.6% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: Section/equation/figure numbers would be helpful. (missed by all 4 reviewers)
- Human Issue #3: The form of the model is not given any justification; why one parameterization was chosen is not addressed. (missed by all 4 reviewers)

Count: 2 out of 4 human issues (50%) were missed by every reviewer.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1 (missing benchmark): covered by Charlie, Doug, and Evan — not unique to any single reviewer
- Human Issue #4 (transition density typo): covered by all four reviewers — not unique to any single reviewer
- Human Issue #1 is covered by Charlie, Doug, Evan but NOT Alex → Alex uniquely misses #1; no unique coverage by Alex
- Human Issue #4 is covered by all four

Alex uniquely covered: none (Alex is the only one who missed Human Issue #1 among reviewers; but no human issue is covered only by Alex)

Checking unique coverage:
- Alex covers: Human Issue #4 only
- Charlie covers: Human Issues #1 and #4
- Doug covers: Human Issues #1 and #4
- Evan covers: Human Issues #1 and #4

Human Issue #4 is covered by all four — not unique to any reviewer.
Human Issue #1 is covered by Charlie, Doug, Evan but missed by Alex — not a unique find for any of them since all three share it.

No human issue is covered by exactly one reviewer. Unique finds per reviewer = 0 for all.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- The primary conclusion rests on the Poisson model which is contradicted by the negative binomial sensitivity analysis (Alex finding #5, Charlie finding #4, Doug finding #3, Evan M1): all four reviewers raise this as a major concern the human did not flag explicitly.
- The Wilks approximation is invalid because sigma=0 is a boundary condition (Alex finding #9 — rated Moderate, Charlie finding #4, Doug finding #7, Evan M3): Charlie, Doug, and Evan flag this as Major; Alex flags it as Moderate. Three of four raise it as Major; all four mention it.
- The profile likelihood is seeded from a suboptimal region and is uninformative (Alex finding #2, Charlie finding #5 partially, Doug finding #5, Evan M4): Alex, Doug flag this directly as Major; Charlie frames it as computational effort; Evan frames it as poor man's profile not being proper. The specific profile-seeding problem is flagged as Major by Alex and Doug; related concerns appear in Charlie and Evan.

Issues raised as Major by all four reviewers and missed by human:
1. The primary scientific conclusion is based on the Poisson model and reverses under the negative binomial, yet the Poisson result is presented as primary — making the main conclusion fragile or invalid. (Alex #5, Charlie #4, Doug #3, Evan M1)

Issues raised as Major by at least three reviewers and missed by human:
2. The Wilks approximation is applied when sigma=0 is a boundary of the parameter space, violating the theorem's conditions. (Alex #9 [Moderate], Charlie #4, Doug #7, Evan M3)
3. The profile likelihood for phi is constructed from a starting region far below the global MLE, rendering it uninformative. (Alex #2, Doug #5; partially in Charlie #3 and Evan M4)

Universal AI-only Major flags (all four): 1 issue (Poisson conclusion fragility).

Universal AI-only flags (all four, any severity): 1 confirmed; boundary/Wilks and profile issues come close but are classified differently across reviewers.

Count of universal AI-only Major flags: 1
