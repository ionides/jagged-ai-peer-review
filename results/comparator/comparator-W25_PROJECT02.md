# Comparator Analysis — W25 Project 02

---

## Human Issues

1. Poisson noise (no overdispersion) in the main observation model. Subsequently, there is a nice analysis of how negative binomial noise is investigated but is found to be less necessary for a model having opponent covariates and momentum. Alternatively, the negative binomial model could imply that momentum is not necessary. Apparently, one team for one season is not enough to distinguish this. The authors recognize this. They appropriately investigate the question of whether momentum matters with an open mind, looking for the evidence both ways coming from the models and data.

2. The analysis is missing a benchmark, but does compare to alternative versions of the model.

3. Section/equation/figure numbers would be helpful.

4. The form of the model is not given any justification. Maybe this sort of social science does not have strong reasons to prefer one model over another; it could be just an empirical question. But the issue should be addressed.

5. A typo in the normal transition density model: $\phi x_{n-1}$ should be $x_n - \phi x_{n-1}$.

6. Future work could extend this to more teams. That extended analysis is beyond the reasonable scope of a 531 final project.

7. Note that the Tigers offensive skill ($X_n$) autoregresses toward 0 but we add a team-specific long-run average skill, $\mu$.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Primary Conclusion Depends on the Poisson Model, Which Is Strongly Outperformed by Negative Binomial")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Transition Density Formula Contains a Typo")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (Incorrect Sign Interpretation for gamma): A — covariate sign misinterpreted; human did not raise this
- Finding 2 (Profile Likelihood from suboptimal starting box): A — profile CI based on local not global MLE; human did not raise this
- Finding 3 (Optimal AR(1) parameters show no momentum): A — phi ~ -0.02 makes process effectively IID, conclusion misleading; human did not raise this
- Finding 4 (Transition Density Typo): B — exponent missing x_n term, density does not depend on x_n (matches Human Issue #5)
- Finding 5 (Primary Conclusion Depends on Poisson, Outperformed by NB): B — Poisson is poor fit relative to NB; conclusion not robust; NB yields no evidence for momentum (matches Human Issue #1)
- Finding 6 (NBin AR1 MLE worse than NBin Static): A — AR1 NB slightly worse than nested static NB, indicating convergence failure; human did not raise this
- Finding 7 (run_level hardcoded to "explore"): C — code cannot reproduce stored results; human did not raise this
- Finding 8 (Pairwise scatterplot mislabeled in Local Search section): C — presentation inconsistency; human did not raise this
- Finding 9 (Wilks approximation may not apply due to boundary parameter): C — boundary parameter issue with chi-squared df = 2; human did not raise this
- Finding 10 (No exploratory autocorrelation analysis before model construction): C — no ACF plot despite central research question being about temporal autocorrelation; human did not raise this
- Finding 11 (Code comment "log(mu) represents expected runs" incorrect): C — parameterization confusion in comment; human did not raise this
- Finding 12 (Inconsistent parameter_trans between files): C — minor inconsistency in initial POMP object; human did not raise this
- Finding 13 (No model adequacy assessment via simulation): C — no formal goodness-of-fit check at MLE; human did not raise this
- Finding 14 (Opponent strength uses season-wide future data): C — covariate construction violates causal structure; human did not raise this
- Finding 15 (nrow(opp_pitch_games > 0) incorrect code): C — logic error that happens to work in context; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Conclusion contradicts the sensitivity analysis — NB model fails to reject null while Poisson model does, yet paper asserts momentum is a material factor")
- Human Issue #2: covered (matched by finding: "No non-mechanistic benchmark")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Mathematical error in the transition density equation — x_n absent from exponent")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major Issue 1 (Mathematical error in transition density equation): B — x_n missing from exponent in Equation (1) (matches Human Issue #5)
- Major Issue 2 (LRT boundary violation): A — sigma=0 lies on boundary of parameter space, chi-squared approximation invalid
- Major Issue 3 (Duplicate vector in MLL computation): A — results_glob concatenated with itself instead of combining local and global search results
- Major Issue 4 (Conclusion contradicts sensitivity analysis): B — NB sensitivity analysis fails to reject null but Discussion asserts momentum is material (matches Human Issue #1)
- Major Issue 5 (Insufficient global search effort): A — only 5 starting points used (explore mode) on acknowledged complex likelihood surface
- Major Issue 6 (Look-ahead bias in covariate Z_n): A — full-season opponent ERA used as time-n covariate, including future games
- Minor: Profile likelihood omitted from main report: C — formal profile for phi computed in code but not shown in report
- Minor: No confidence intervals stated in text: C — only point estimates reported despite identifiability concerns
- Minor: No non-mechanistic benchmark: D — no ARIMA or IID comparison (matches Human Issue #2)
- Minor: phi to -1 finding not investigated: C — convergence to phi near -1 noted but not interpreted or checked for stability
- Minor: X_0=0 initial condition not sensitivity-tested: C — momentum fixed at zero at season start without sensitivity analysis
- Minor: Pairwise scatterplot mislabeling: C — figure labeled as local search results but code references global search output
- Minor: nrow(opp_pitch_games > 0) non-idiomatic: C — comparison operator applied inside nrow() rather than outside
- Minor: Comment error in blinded.Rmd: C — comment says "log(mu) represents expected runs" but mu is already the log-expected runs

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding #2 "Global MLE reveals AR(1) captures overdispersion not momentum"; note: finding #3 contradicts human's interpretation that NB analysis shows NB is less necessary)
- Human Issue #2: covered (matched by finding #1 "Absence of non-mechanistic benchmark")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding #4 "Mathematical error in AR(1) transition density")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (Absence of non-mechanistic benchmark): B — no non-mechanistic baseline compared against (matches Human Issue #2)
- Finding 2 (Global MLE reveals overdispersion not momentum): B — phi≈-0.012, large sigma indicate latent AR(1) absorbs overdispersion; NB sensitivity confirms this (matches Human Issue #1)
- Finding 3 (Primary conclusion contradicted by NB sensitivity): F — Doug says Poisson conclusion is an artifact and framing should be reversed; human says NB was found to be less necessary and the investigation is appropriately open-minded (contradicts Human Issue #1)
- Finding 4 (Mathematical error in AR(1) transition density): B — exponent written as -(φx_{n-1})² / 2σ² instead of -(x_n − φx_{n-1})² / 2σ² (matches Human Issue #5)
- Finding 5 (Profile likelihood seeded from wrong region): A — profile box restricted to sigma ∈ [0.003, 0.010], ~40 log-likelihood units below global MLE, rendering profile uninformative
- Finding 6 (Global search initialization anti-pattern): A — global replicates inherit cooled mif2 schedule from prior result object instead of fresh base pomp object
- Finding 7 (LRT at boundary of parameter space): A — sigma=0 is on boundary; Wilks' theorem requires interior null; chi-squared(2) approximation is not exact
- Finding 8 (No parameter estimates in main text): C — MLE values (phi, sigma, gamma, mu) never reported; readers cannot assess scientific plausibility
- Finding 9 (Computational details absent): C — particle count, IF2 iterations, and global replicate count not stated in main text
- Finding 10 (Covariate uses future data): C — opponent-strength covariate Z_n uses full 2024 season including post-game-n data; leakage not quantified
- Finding 11 (Coding bug in data processing): C — misplaced parenthesis in nrow() condition produces accidentally correct but fragile result
- Finding 12 (Redundant concatenation in MLL calculation): C — same vector concatenated with itself instead of combining local and global search results
- Finding 13 (Parameter transformation inconsistency between files): C — blinded.Rmd includes mu in log transform; Full_Code.Rmd standalone partrans excludes mu
- Finding 14 (Local search phi convergence not reconciled): C — local search finds phi≈-1, global finds phi≈-0.012; mechanistic explanation absent
- Finding 15 (Pairwise scatter mislabeled as local search): C — figure in Local Search section uses global search results (results_glob) not local search results

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "25.02.M1 — primary conclusion drawn from Poisson model; NB model shows no evidence for momentum")
- Human Issue #2: covered (matched by finding: "25.02.M6 — no comparison against a non-mechanistic benchmark")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "25.02.M5 — typographical error in latent transition density, x_n term missing")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- 25.02.M1: B — primary conclusion drawn from known-misspecified Poisson model; NB model eliminates evidence for momentum (matches Human Issue #1)
- 25.02.M2: A — likelihood ratio test does not account for Monte Carlo variability
- 25.02.M3: A — Wilks' approximation invalid at boundary of parameter space (sigma = 0)
- 25.02.M4: A — poor man's profile is not a proper profile likelihood; no CIs for any parameter
- 25.02.M5: B — typographical error in transition density equation, x_n term missing (matches Human Issue #5)
- 25.02.M6: B — no comparison against a non-mechanistic benchmark (matches Human Issue #2)
- 25.02.m1: C — computational settings (Np, Nmif, starts) not reported
- 25.02.m2: C — log-transform on mu implicitly constrains mu > 0
- 25.02.m3: C — fixed initial condition X_0 = 0 without sensitivity analysis
- 25.02.m4: C — Figure 2 simulated traces obscure the observed series
- 25.02.m5: C — dip in conditional log-likelihoods near Game 90 not discussed
- 25.02.m6: C — phi converging to approximately -1 not explained scientifically
- 25.02.m7: C — covariate Z_n uses season-level statistics introducing look-ahead bias

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 4 | 3 | 3 |
| B (AI major, human also found) | 2 | 2 | 3 | 3 |
| C (AI minor, human missed) | 9 | 7 | 8 | 7 |
| D (AI minor, human also found) | 0 | 1 | 0 | 0 |
| E (Human found, AI missed) | 5 | 4 | 4 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 1 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 0 | 5 | 2/7 = 29% | 4 | 9 | 13/15 = 87% |
| Charlie | 2 | 1 | 4 | 3/7 = 43% | 4 | 7 | 11/14 = 79% |
| Doug | 3 | 0 | 4 | 3/7 = 43% | 3 | 8 | 11/14 = 79% |
| Evan | 3 | 0 | 4 | 3/7 = 43% | 3 | 7 | 10/13 = 77% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: Section/equation/figure numbers would be helpful. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The form of the model is not given any justification. Maybe this sort of social science does not have strong reasons to prefer one model over another; it could be just an empirical question. But the issue should be addressed. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: Future work could extend this to more teams. That extended analysis is beyond the reasonable scope of a 531 final project. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: Note that the Tigers offensive skill ($X_n$) autoregresses toward 0 but we add a team-specific long-run average skill, $\mu$. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 7 human issues (57%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
