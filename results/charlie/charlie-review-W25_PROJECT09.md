# Peer Review: NBA POMP-ELO: A Stochastic System Approach to Modeling Team Strength and Predicting Games
**Reviewer:** Charlie  
**Semester/Project:** W25 / Project 09  

---

## Summary

The paper proposes a POMP-ELO framework that models Houston Rockets team strength as a latent state variable, augmenting the classical ELO rating system with BPM-based covariates, a Bradley-Terry win probability, and a mean-reverting noise process. Three model variants are compared against logistic regression and base ELO baselines on 164 games across the 2023-24 and 2024-25 seasons. While the problem framing is creative and the use of the `pomp` package for sports prediction is novel, the paper contains several fundamental methodological errors that invalidate its principal claim that POMP-ELO substantially outperforms its baselines. Most critically, the dmeasure and rmeasure Csnippets compute win probability from incompatible numerical scales, meaning the likelihood being optimized and the simulations used for accuracy evaluation reflect entirely different models. Additional problems include a global search whose parameter box excludes the local-search MLE, rw.sd values set equal to parameter starting magnitudes, a hard-coded absolute file path that prevents reproducibility, and no quantitative goodness-of-fit reporting (log-likelihood or AIC). The accuracy comparisons in the Model Comparison section are therefore uninterpretable as stated.

---

## Major Issues

### 1. dmeasure and rmeasure compute win probability on incompatible numerical scales

The `dmeas` Csnippet divides `team_strength` and `opp_strength` by 100.0 before computing the Bradley-Terry win probability (lines 298-310 of blinded.Rmd), while `rmeas` uses the raw state values directly (lines 313-322). With `team_strength` and `opp_strength` on the ELO scale (~1500), the `dmeas` probability is computed from scores of approximately 15, where the softmax produces values near 0.5 for any balanced matchup; `rmeas` feeds raw values near 1500 into the same expression, where `exp(team_strength - opp_strength)` saturates to 0 or 1 for any non-zero imbalance. Furthermore, `home_court_avd` is divided by 100 in `dmeas` but used at full scale in `rmeas`. Concretely, at `team_strength = 1550, opp_strength = 1500, home_court_avd = 89` (the reported MLE): `dmeas` computes `p ≈ exp(15.89)/(exp(15.89)+exp(15.0)) ≈ 0.70`, while `rmeas` computes `p ≈ exp(1550+89-1500)/(1+exp(1550+89-1500)) ≈ 1.0`. The particle filter optimizes the `dmeas` model; all simulations and all reported accuracy figures are produced by the `rmeas` model. These are different models. All model comparison results, simulation accuracy figures, and parameter estimates are therefore invalid as evidence for the paper's central claim.

**Fix:** Make `dmeas` and `rmeas` apply identical rescaling to state variables before computing the win probability. The simplest approach is to remove the `/100.0` division from `dmeas` and apply a consistent rescaling (e.g., divide all three quantities by 400, matching ELO convention) in both snippets.

---

### 2. Global search parameter box excludes the local-search MLE for home_court_avd

The global search box sets `home_court_avd` in `[200, 250]` for all three models (lines 556-560, 614-618, 805-809). However, the local search converges to `home_court_avd ≈ 89` for Model 1 (the value used in subsequent simulations at line 585) and `≈ 76` for Model 2 (line 642). Both of these values lie far below the box lower bound of 200. Any global search replicate that happens to find `home_court_avd ≈ 89` must have drifted there via IF2 perturbations starting from values 2-3× larger — an accidental drift, not systematic coverage. The stated "global maximum" for each model is therefore not a reliable global optimum. This also means the global best log-likelihood cannot be meaningfully compared to the local search best, and the best parameter vectors reported from the global search are not trustworthy.

**Fix:** Center the global search box on the local MLE for each parameter. For `home_court_avd`, set the box to `[20, 200]` or `[0, 300]` to span both the local MLE and plausible alternatives.

---

### 3. rw.sd values are set equal to parameter starting values

All three mif2 local searches use `rw.sd=rw_sd(beta1=0.5, home_court_avd=40, alpha=0.05)` (lines 504, 533, 786-787), which exactly match the starting parameter values `c(beta1=0.5, home_court_avd=40, alpha=0.05)`. For `home_court_avd`, the perturbation SD equals the starting value of 40, which is enormous relative to any plausible MLE uncertainty — this causes the IF2 chain to diffuse across parameter space rather than converge to the MLE. Appropriate rw.sd values should be approximately 2-5% of the expected MLE value (e.g., `rw.sd=rw_sd(beta1=0.01, home_court_avd=1, alpha=0.002)`). The convergence traces shown in the paper, while not visible in the code, likely show flat high-variance parameter chains consistent with this failure mode. Per Wheeler et al. (2024), computational adequacy requires evidence that parameter estimates have converged, which is not demonstrated here.

**Fix:** Set rw.sd values to approximately 1-5% of the expected MLE for each parameter. Run a short pilot mif2 to calibrate rw.sd from the empirical SD of a preliminary converged distribution.

---

### 4. Global search initialized from a previous mif2 result rather than the base pomp object

In all three global searches (lines 563-577, 622-636, 813-826), the global search calls `mf1 |> mif2(params=c(guess,fixed_params)) |> mif2(Nmif=20)` where `mf1` is `local_mifs[[1]]` — the first result from the local IF2 search. Passing a previous mif2 result as the first argument to the global mif2 call inherits the internal cooling schedule from the local chain, which is at or near its final (near-zero perturbation) state. This anchors all global search replicates near the local-search solution rather than exploring the full parameter box from fresh starts. The reported global maximum may simply reflect the local optimum re-discovered from nearby starting points, not a genuine global search. The correct pattern is `mif2(nba_pomp, params=c(guess,fixed_params), ...)` using the base pomp object as the first argument.

**Fix:** Replace `mf1 |> mif2(params=...)` with `nba_pomp |> mif2(params=..., Np=1000, Nmif=50, ...)` in the global search loop, using the original pomp object so each replicate starts with a fresh cooling schedule.

---

### 5. No quantitative goodness-of-fit reporting (no log-likelihood or AIC comparison)

The paper presents no log-likelihood values, AIC, or other quantitative goodness-of-fit metrics in the Model Comparison section. The only comparisons offered are simulation-based prediction accuracy rates, which as noted in Issue 1 are computed from the rmeas model rather than the dmeas model being fitted. Wheeler et al. (2024) state explicitly that "visual comparisons alone are only a weak and informal measure of goodness-of-fit," and the same applies to simulation accuracy evaluated from a misspecified measurement model. Without log-likelihood values (which are printed by the mif2 traces and pfilter calls already in the code), it is impossible to formally compare models or assess whether the POMP models represent any improvement over the baselines.

**Fix:** Report the best log-likelihood (with standard error) for each model from the pfilter replicate evaluations already computed in the code. Use these to compute AIC for each model and include a formal comparison table.

---

### 6. No non-mechanistic statistical benchmark

The paper's stated goal is to show that POMP-ELO improves over ELO and logistic regression. However, neither baseline is a proper non-mechanistic statistical benchmark in the sense of Wheeler et al. (2024): both baselines are constructed from the same BPM and ELO covariates as the POMP models, and there is no comparison to a standard time-series benchmark (ARMA, auto-regressive negative binomial, or even a null model). Furthermore, the logistic regression and ELO baselines are evaluated at in-sample prediction accuracy, while no out-of-sample or holdout evaluation is performed. The claim that "POMP has resulted in far better performance" (line 994) is not supported without a proper statistical baseline comparison. Per Wheeler et al. (2024, §Benchmark comparison), mechanistic models should be compared against non-mechanistic statistical benchmarks quantitatively.

**Fix:** Add an auto-regressive baseline (e.g., logistic regression on lagged win outcomes) as a proper time-series benchmark. Evaluate all models on a held-out test set (e.g., the last 20 games of the 2024-25 season) rather than in-sample accuracy.

---

### 7. Hard-coded absolute file paths prevent reproducibility

The data loading uses absolute paths tied to the author's local filesystem: `/Users/nicholaskim/Documents/STAT-531/final/data/matchups.xlsx` (line 55), `/Users/nicholaskim/Documents/STAT-531/final/data/BPM.xls` (line 155), and `/Users/nicholaskim/Documents/STAT-531/final/data/BPM-new.xlsx` (line 672). These paths will fail on any machine other than the author's. The data files are present in the project `data/` subfolder, but the code does not use relative paths to reference them. Per the code supplement checklist, relative paths (or paths relative to the project root) are required for reproducibility.

**Fix:** Replace all absolute paths with relative paths such as `read_excel("data/matchups.xlsx")` and ensure the Rmd knits correctly from the project directory.

---

### 8. Simulation-based accuracy evaluated against incorrect reference outcomes in Model 2 final evaluation

At line 641-663, the code simulates `sims2_best` from `nba_pomp` (Model 1's pomp object, not `nba_pomp2`). This means Model 2's best-parameter simulation is actually run using Model 1's structure. Additionally, the `true_win` reference at line 648 is drawn from `sims1` (the initial fixed-parameter simulation from Model 1) rather than from the actual outcome data. The Model 2 accuracy figure reported in the Model Comparison section is therefore computed from the wrong model and the wrong ground truth. The same issue appears in the attendance model evaluation at lines 834-857, where `nba_pomp` (Model 1) is used instead of `nba_pomp_att`.

**Fix:** For Model 2's post-global-search evaluation, use `nba_pomp2 |> simulate(params=c(best_params_model2, sigma=5), ...)` and extract true outcomes from the observed data directly (e.g., `bpm$Win`) rather than from a prior simulation object.

---

## Minor Issues

- **sigma is fixed but undiscussed:** The parameter `sigma` (process noise SD) is fixed at 5 throughout all models and never estimated or profiled. There is no justification for this value, and fixing it to an arbitrary value while estimating other parameters undermines identifiability. The role of sigma relative to the ELO scale (~1500) should at minimum be discussed; on the raw ELO scale a sigma of 5 is small, but on the /100-rescaled `dmeas` scale it would be 0.05.

- **p_win is stored as a state variable but serves no inferential purpose:** `p_win` is listed in `statenames` and initialized but is never used in the dmeasure, and its inclusion in the state vector increases the dimension of the latent state without benefit. This is harmless but unnecessary.

- **Bradley-Terry probability formula in text differs from dmeas implementation:** The text equation at line 250 shows `p = exp(hca*I(Home=1) + team_1) / (exp(hca*I(Home=1)+team_1)+exp(hca*I(Home=0)+team_2))`, but the dmeas Csnippet at line 308 implements `p = exp(team_score - max_val) / (exp(team_score - max_val) + exp(opp_score - max_val))` with opp_score receiving no home advantage term. These are mathematically different when Home=0 (away game). The text description and code implementation should be reconciled.

- **ELO initial condition set with malformed date:** The `initial` data frame at line 142 uses `as.Date(10/24/2023, format="%m/%d/%y")` where `10/24/2023` is evaluated as a division (`10/24/2023 ≈ 0.000496`) before `as.Date()` sees it, not as a date string. The resulting initial date is January 1, 1970 plus ~0 days, not October 24, 2023. This corrupts the ELO initialization plot, though it does not affect the POMP analysis since the time index is constructed separately.

- **Only 20 IF2 iterations used:** Both local and global searches use `Nmif=20` iterations, which is unusually low for IF2. Standard practice (and Wheeler et al. 2024) suggests at least 50-100 iterations to achieve convergence, particularly for the global search where starting points are far from the MLE. The cooling schedule with `cooling.fraction.50=0.5` means the perturbations halve in 10 iterations, so at 20 iterations the cooling has already decayed substantially. With only 20 iterations and large initial rw.sd (see Issue 3), convergence is unlikely.

- **Prediction accuracy comparison mixes in-sample and out-of-sample metrics:** The logistic regression, POMP, and ELO accuracies are all computed on the same 164-game training set. In-sample accuracy is an optimistic estimate of predictive performance; the logistic regression has 3 free parameters fit to these exact 164 observations, giving it a natural in-sample advantage. A meaningful comparison would use cross-validation or a held-out test set.

- **Typos and grammatical issues:** "there is there an underlying truth" (line 34, doubled phrase); "TS can grow to always be bigger than Opponent Strength as it can grow to be larger" (line 239, awkward doubling); "Attendence" in section heading at line 667; "due" vs "do" confusion at line 862 ("How did these POMP models due compared to").

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project09/blinded.Rmd`
