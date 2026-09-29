# Comparator Analysis — W25 Project 09

---

## Human Issues

1. dmeas and rmeas are not quite consistent. dmeas does not subtract home advantage (i.e., give it to the opponents) when playing away.

2. It would be nice to present likelihoods as well as predictive scores. Likelihood provides tools such as likelihood ratio test and AIC to assess how the improvement in prediction (on a training set) compares.

3. This project is relatively light on diagnostic investigations. How would one assess outliers, over-dispersion, or other possibilities for improved model specification? The baseline models already successfully demonstrate no major model misspecification.

4. The report does not place the project securely into the context of other 531 projects (or a broader literature, but that is beyond expectations for a final project). The topic is original, but the report should say this and the team should say what they learned from previous projects, as requested in the assignment description.

5. One referee commented that classic Elo already adds about 100 points for home court. This could be useful information if the project is developed further.

6. The code could readily be run on different teams, which would be interesting without much extra work. However, in practice, each new dataset often needs individualized attention to its particular features.

7. BPM (Box Plus-Minus) should be defined at first use. This is good practice for all acronyms even if you suspect the reader may be familiar with them.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by findings: "dmeas and rmeas are inconsistent with each other" [Finding 4] and "attendance POMP model's dmeas never updated to include attendance covariate" [Finding 15])
- Human Issue #2: covered (matched by finding: "No likelihood-based model comparison; log-likelihood values are not reported or discussed" [Finding 7])
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (In-sample prediction as primary evaluation metric): A — no held-out test set; in-sample accuracy reported as predictive power
- Finding 2 (Accuracy from stochastic simulations vs. expected win probabilities): A — inconsistent operational definition of "prediction" across model types
- Finding 3 (Code bug: Model 3 simulates from nba_pomp, not nba_pomp_att): A — attendance model evaluation is silently reusing Model 1's object
- Finding 4 (dmeas and rmeas inconsistent with each other): B — different formulas for softmax vs. logistic with home-court adjustment (matches Human Issue #1)
- Finding 5 (sigma fixed and excluded from optimization): A — no justification for sigma = 5; truncates parameter space
- Finding 6 (Global search bounds poorly motivated and off-scale for home_court_avd): A — search interval [200, 250] is far from both initial guess and best-found value
- Finding 7 (No likelihood-based model comparison; log-likelihood values not reported): B — no LRT, AIC, or log-likelihood traces used for comparison (matches Human Issue #2)
- Finding 8 (ELO used as observed data for latent state): A — conflates deterministic post-hoc ELO with true latent team strength
- Finding 9 (t0 = 1 rather than t0 = 0; initialization indexing issues): C — one-step misalignment between POMP object and ELO covariate
- Finding 10 (BPM covariates for early games not formally documented or validated): C — boundary conditions of rolling BPM window not shown in code
- Finding 11 (No convergence diagnostics or particle filter variance assessments): C — IF2 traces shown but not analyzed; loglik.se never discussed
- Finding 12 (p_win treated as state variable rather than derived quantity): C — conceptual confusion; inflates state dimension without benefit
- Finding 13 (Hardcoded absolute file paths prevent reproducibility): C — paths tied to a specific local machine
- Finding 14 (Logistic regression in-sample baseline misleading): C — 64% accuracy is in-sample; comparison to POMP is not meaningful
- Finding 15 (Attendance POMP model's dmeas never updated to include attendance covariate): D — dmeas/rmeas inconsistency for attendance effect; same underlying issue as dmeas not matching rmeas (matches Human Issue #1)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by findings: "home_court_avd is on inconsistent scales in dmeas vs. rmeas" and "Away-game case is handled asymmetrically between dmeas and rmeas")
- Human Issue #2: covered (matched by findings: "Model comparison uses in-sample prediction accuracy, not log-likelihood" and "No likelihood-based benchmark comparison")
- Human Issue #3: covered (matched by findings: "No simulation from the filtering distribution" and "Convergence diagnostics are shown but not interpreted")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (home_court_avd inconsistent scales in dmeas vs. rmeas): B — scale inconsistency between dmeas and rmeas is a distinct manifestation of the same underlying dmeas/rmeas inconsistency concern (matches Human Issue #1)
- Finding 2 (away-game handled asymmetrically between dmeas and rmeas): B — directly identifies that dmeas does not subtract home advantage for away games, matching Human Issue #1 precisely
- Finding 3 (Model 3 accuracy evaluation silently uses Model 1): A — coding bug causing Model 3 to be evaluated using Model 1 parameters; not raised by human
- Finding 4 (attendance has no effect on likelihood in Model 3): A — dmeas_att never defined so attendance enters rmeas but not the likelihood; not raised by human
- Finding 5 (latent ELO update uses simulated win, not observed Win): A — structural design flaw in rproc causing particle degeneracy; not raised by human
- Finding 6 (no profile likelihoods computed): A — concerns parameter identifiability and confidence intervals; distinct from Human Issue #2's model-comparison concern
- Finding 7 (model comparison uses in-sample prediction accuracy, not log-likelihood): B — directly matches Human Issue #2's call for likelihood-based (AIC/LRT) rather than predictive-score comparisons (matches Human Issue #2)
- Finding 8 (prediction accuracy computed in-sample): A — out-of-sample evaluation concern not raised by human
- Finding 9 (hard-coded absolute local file paths): A — reproducibility failure; not raised by human
- Finding 10 (no likelihood-based benchmark comparison): B — matches Human Issue #2's underlying concern that likelihoods should be used to assess model improvement rather than prediction accuracy alone (matches Human Issue #2)
- Finding 11 (sigma fixed without justification): C — parameter fixing without sensitivity analysis; not raised by human
- Finding 12 (global search parameter space excludes the MLE): C — search box misconfiguration; not raised by human
- Finding 13 (no simulation from filtering distribution): D — filtering simulations are a model diagnostic tool; matches Human Issue #3's concern about light diagnostic investigation (matches Human Issue #3)
- Finding 14 (p_win stored as redundant state variable): C — design inefficiency; not raised by human
- Finding 15 (convergence diagnostics shown but not interpreted): D — failure to interpret diagnostic output matches Human Issue #3's concern about inadequate diagnostic investigation (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
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
- Human Issue #7: missed

**Findings classification:**
- Major Issue 1 (dmeas/rmeas scale inconsistency): B — dmeas divides by 100 while rmeas uses raw ELO values, making the two snippets compute win probabilities from incompatible inputs (matches Human Issue #1)
- Major Issue 2 (no log-likelihood or AIC): B — no log-likelihood value reported for any POMP model; comparison relies entirely on binary prediction accuracy from stochastic simulations (matches Human Issue #2)
- Major Issue 3 (global search box excludes MLE): A — the declared box for home_court_avd is [200, 250] yet the best-row result shows home_court_avd ≈ 89, outside that box
- Major Issue 4 (Model 3 attendance uses wrong pomp object): A — attendance best-parameter simulation calls nba_pomp (Model 1) instead of nba_pomp_att, using Model 1 parameters
- Major Issue 5 (global search initialises from previous mif2 result): A — inner mif2 call inherits the decayed cooling schedule of the local chain rather than starting fresh
- Major Issue 6 (no time-series benchmark comparison): A — logistic regression and ELO are not time-series baselines; no AR-logistic or ARMA-type model is compared on log-likelihood grounds
- Major Issue 7 (computational adequacy — Np=1000, Nmif=20): A — particle count and IF2 iterations are too low; convergence is not demonstrated and Monte Carlo error is unquantified
- Major Issue 8 (prediction accuracy evaluated on training data): A — all accuracy figures use the same 164 games used for fitting; no held-out test set or cross-validation
- Major Issue 9 (sigma fixed without justification): A — sigma=5 is held fixed in all runs without sensitivity analysis; affects likelihood surface and identifiability of other parameters
- Major Issue 10 (rw.sd values equal starting-point values): A — perturbation SD of 40 for home_court_avd and 0.5 for beta1 are far too large, causing IF2 chains to diffuse rather than converge
- Minor: hard-coded absolute paths: C — data loading uses /Users/nicholaskim/Documents/... making analysis non-reproducible on other machines
- Minor: p_win declared as state variable unnecessarily: C — p_win is a derived quantity reset each step; carrying it in statenames adds overhead without benefit
- Minor: Model 2 simulation uses nba_pomp instead of nba_pomp2: C — Model 2 post-search evaluation calls simulate on the Model 1 object, which lacks opp_strength as a state and beta2 as a parameter
- Minor: ELO covariate and data column confusion: C — elo column is in the data frame but used only for plotting; no clear statement distinguishes it from the latent team_strength state
- Minor: attendance logistic regression accuracy compared against wrong dataset: C — mean(pred_win_att == bpm$Win) evaluates against the non-attendance dataset rather than bpm_att$Win
- Minor: no parameter uncertainty or confidence intervals: C — only MLE point estimates are reported; profile likelihoods and likelihood-based CIs are entirely absent
- Minor: conclusion overstates evidence: C — claims "drastically improved predictive power" while measurement model is inconsistent, wrong objects are used for simulation, and evaluation is in-sample only

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

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by findings: "25.09.2 — dmeas and rmeas implement materially different win-probability formulas" and "Minor-scale — rmeas uses raw ELO scale; dmeas rescales by /100")
- Human Issue #2: covered (matched by finding: "25.09.5 — log-likelihood computed but never used; model selection rests entirely on prediction accuracy")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- 25.09.1: A — sigma is fixed at 5.00 throughout all searches, never optimized
- 25.09.2: B — dmeas and rmeas implement materially different win-probability formulas (matches Human Issue #1)
- 25.09.3: A — Model Att global search table is numerically identical to Model 1, indicating copy-paste
- 25.09.5: B — log-likelihood computed but never used; model selection rests entirely on prediction accuracy; AIC/LRT not applied (matches Human Issue #2)
- 25.09.4: A — Base ELO prediction accuracy reported as 57.93% in text but 66.46% in table
- 25.09.6: A — sim_win drawn inside rproc and used for state update before actual observation is incorporated
- 25.09.7: A — no confidence intervals or profile likelihoods computed for any parameter
- 25.09.8: A — only 20 mif2 iterations used; several parameters have not stabilized
- Minor-scale: D — rmeas uses raw ELO scale; dmeas rescales by /100, giving home_court_avd different quantitative meaning in each (matches Human Issue #1)
- Minor-pwin: C — p_win stored as state variable despite being a deterministic function of other states
- Minor-plusign: C — OPP equation has stray plus sign on line 312
- Minor-eloeq: C — ELO update equation displayed does not match the correct formula implemented in code
- Minor-partrans: C — Model 2 partrans may not include log = c("alpha"), unlike Model 1
- Minor-seed: C — no set.seed() calls; results not exactly reproducible
- Minor-software: C — R version and pomp version not reported
- Minor-captions: C — figure captions absent for Figures 003, 004, 011, 012, 013
- Minor-prose: C — repeated words and typographical errors throughout ("there is there is", "A a", etc.)
- Minor-insample: C — prediction accuracy figures appear to be in-sample with no training/test split noted

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 6 | 8 | 6 |
| B (AI major, human also found) | 2 | 4 | 2 | 2 |
| C (AI minor, human missed) | 6 | 3 | 7 | 9 |
| D (AI minor, human also found) | 1 | 2 | 0 | 1 |
| E (Human found, AI missed) | 5 | 4 | 5 | 5 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 5 | 2/7 = 29% | 6 | 6 | 12/15 = 80% |
| Charlie | 4 | 2 | 4 | 3/7 = 43% | 6 | 3 | 9/15 = 60% |
| Doug | 2 | 0 | 5 | 2/7 = 29% | 8 | 7 | 15/17 = 88% |
| Evan | 2 | 1 | 5 | 2/7 = 29% | 6 | 9 | 15/18 = 83% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #4: The report does not place the project securely into the context of other 531 projects (or a broader literature, but that is beyond expectations for a final project). The topic is original, but the report should say this and the team should say what they learned from previous projects, as requested in the assignment description. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: One referee commented that classic Elo already adds about 100 points for home court. This could be useful information if the project is developed further. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The code could readily be run on different teams, which would be interesting without much extra work. However, in practice, each new dataset often needs individualized attention to its particular features. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: BPM (Box Plus-Minus) should be defined at first use. This is good practice for all acronyms even if you suspect the reader may be familiar with them. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 7 human issues (57%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: This project is relatively light on diagnostic investigations. How would one assess outliers, over-dispersion, or other possibilities for improved model specification? The baseline models already successfully demonstrate no major model misspecification. (Covered only by Charlie)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |
