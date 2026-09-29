# Peer Review: W25 Project 09
## NBA POMP-ELO: A Stochastic System Approach to Modeling Team Strength and Predicting Games

---

## Summary

This project proposes a POMP-based extension of ELO ratings — "POMP-ELO" — to model the Houston Rockets' team strength as a latent state across two NBA seasons (164 games). Three model variants are introduced: one treating opponent strength as a covariate (Model 1), one treating opponent strength as a second latent state (Model 2), and one augmenting Model 1 with a fan-attendance modifier on home-court advantage (Model 3). Baselines include base ELO and logistic regression. The primary comparison criterion is in-sample prediction accuracy derived from stochastic forward simulations.

The project's core concept — embedding ELO dynamics inside a POMP latent-state framework — is creative and scientifically motivated. However, the analysis has multiple critical flaws. The measurement model (dmeas) and the simulation model (rmeas) are inconsistent in both parameter scale and functional form, making the likelihood function and all downstream inference invalid as specified. Model 3's evaluation contains a coding bug that silently substitutes Model 1 for Model 3 throughout. Profile likelihoods are absent, the primary model comparison relies on in-sample prediction accuracy rather than log-likelihood, and the code is non-reproducible due to hard-coded local file paths. These issues collectively undermine the validity of the reported conclusions.

---

## Major Issues

### 1. home_court_avd is on inconsistent scales in dmeas vs. rmeas

In `dmeas` (lines 297--311), `home_court_avd` is divided by 100 before use:

```c
double hca = home_court_avd / 100.0;
if (home == 1) { team_score += hca; }
```

In `rmeas` (lines 313--322), `home_court_avd` is used at its raw scale:

```c
p = exp(home_court_avd + team_strength - opp_strength) / ...
```

Because `dmeas` controls likelihood evaluation and `rmeas` controls simulation, the parameter `home_court_avd` has a completely different effect in the two components. The global search MLE finds `home_court_avd ≈ 89`, which corresponds to an effect of 0.89 in `dmeas` but an enormous logit shift of 89 in `rmeas`. All parameter estimates, log-likelihoods, and simulated win probabilities are therefore computed under incompatible measurement models. This is a course-confirmed error type (Wheeler et al. 2024, measurement model specification).

**Fix:** Ensure that `home_court_avd` appears at the same scale in both `dmeas` and `rmeas`. Either divide by 100 consistently, or remove the division and retrain from scratch.

---

### 2. Away-game case is handled asymmetrically between dmeas and rmeas

In `rmeas`, when `home == 0`, `home_court_avd` is explicitly subtracted from the home team's (opponent's) logit:

```c
p = exp(team_strength - (opp_strength + home_court_avd)) / ...
```

In `dmeas`, when `home == 0`, no adjustment is made — team_score is left unmodified. The opponent does not receive a home-court boost in the likelihood. This means `dmeas` and `rmeas` implement structurally different models for away games. The likelihood function does not match the simulation even at a qualitative level for the away-game case.

**Fix:** Apply a symmetric home-court adjustment in `dmeas`: when `home == 0`, subtract `hca` from `team_score` or add it to `opp_score`.

---

### 3. Model 3 accuracy evaluation silently uses Model 1 (coding bug)

The code block at lines 835--858 that computes Model 3's best-parameter accuracy calls `nba_pomp |> simulate(...)` with Model 1's MLE parameters (`beta1 = 1.84984, home_court_avd = 89.33528, alpha = 0.5705353`). It does not use `nba_pomp_att` or Model 3's optimized parameters. As a result, the "Model Attendance" row in the comparison table is identical to a re-evaluation of Model 1. Model 3's accuracy is entirely fictional as reported.

**Fix:** Replace the simulation call with `nba_pomp_att |> simulate(params = c(...))` using the best parameters found by Model 3's global search.

---

### 4. Attendance has no effect on the likelihood function in Model 3

The `nba_pomp_att` object (lines 715--736) specifies `dmeasure = dmeas`. The original `dmeas` does not reference `attendance` in any way. Therefore, attendance has no effect on the log-likelihood, parameter estimation, or filtering in Model 3. The only place attendance appears is in `rmeas_att`, which is used for simulation. The model is described as capturing an attendance effect on home-court advantage, but no such effect is estimated or scored by the likelihood.

Additionally, no `dmeas_att` is defined anywhere in the code. This means there is no corrected measurement model available.

**Fix:** Define a `dmeas_att` that mirrors the functional form of `rmeas_att`, incorporating `log(attendance)` in the win probability calculation. Use this in `nba_pomp_att`.

---

### 5. The latent ELO update uses a simulated win (sim_win), not the observed Win

Within `rproc` (and `rproc2`), the ELO update to `team_strength` is based on an internally simulated game outcome:

```c
int sim_win = rbinom(1, p_win);
if (sim_win == 1) { team_strength += ...; }
else              { team_strength -= ...; }
```

The observed `Win` is used only in `dmeas` for reweighting. This means team_strength evolves based on a hypothetical sequence of game outcomes rather than the actual game history. When `sim_win ≠ Win`, team_strength is updated in the wrong direction. The particle filter must correct this through importance weights, but particles that repeatedly simulate wrong outcomes will have strongly degraded weights, producing rapid particle degeneracy over a 164-game season. The latent state does not represent ELO computed from actual outcomes — a critical design flaw for this application.

**Fix:** Either restructure the model so that the observed `Win` enters the ELO update (which is not possible in standard POMP rproc), or acknowledge this limitation explicitly and assess particle degeneracy via effective sample size plots. A more appropriate design might treat the ELO-computed-from-actual-wins as a covariate rather than updating it stochastically.

---

### 6. No profile likelihoods are computed

Profile likelihoods are not computed for any parameter in any model. This means parameter identifiability cannot be assessed, no confidence intervals are reported, and it is unknown whether the parameters (`beta1`, `alpha`, `home_court_avd`) are jointly or marginally identifiable from 164 binary observations. Given that `sigma` is fixed at 5 without justification, and that `beta1`'s MLE falls outside the global search box (discussed in Issue 12), identifiability is particularly uncertain here (Error 1.9, CC-Yes; Wheeler et al. 2024, §Parameter identifiability).

**Fix:** Compute profile likelihoods for at least `beta1` and `alpha` using the course-standard procedure. Report confidence intervals.

---

### 7. Model comparison uses in-sample prediction accuracy, not log-likelihood

The final model comparison (lines 948--975) ranks models exclusively by in-sample prediction accuracy computed from stochastic forward simulations. Log-likelihood values are available from the global search output but are not compared across models in any structured way. Prediction accuracy from stochastic simulations is an unreliable comparison criterion: it conflates the model's calibration with the stochastic noise of random simulations, and it does not penalize model complexity. Log-likelihood or AIC is the appropriate criterion for comparing these models (Wheeler et al. 2024, §Quantitative goodness-of-fit reporting).

**Fix:** Report the best log-likelihood (and loglik.se) for each model from the global search as the primary comparison criterion. AIC values penalizing for number of estimated parameters should also be reported.

---

### 8. Prediction accuracy is computed in-sample

All reported prediction accuracies — including those for POMP models — are computed on the same 164 games used to fit the models. In-sample accuracy is expected to be higher than out-of-sample accuracy and cannot support the claim that "POMP-ELO has drastically improved [ELO's] predictive power." The logistic regression comparison is also in-sample. No held-out test set or cross-validation is employed. The improvement over base ELO cannot be attributed to the POMP model's structure without out-of-sample evaluation.

**Fix:** Reserve at least a final third of the season as a test set, or use rolling one-step-ahead forecasting to produce out-of-sample predictions for all models.

---

### 9. Hard-coded absolute local file paths (reproducibility failure)

Three data-loading calls use absolute local paths (lines 56, 156, 672):

```r
matchups <- read_excel("/Users/nicholaskim/Documents/STAT-531/final/data/matchups.xlsx")
bpm      <- read_excel("/Users/nicholaskim/Documents/STAT-531/final/data/BPM.xls")
bpm_att  <- read_excel("/Users/nicholaskim/Documents/STAT-531/final/data/BPM-new.xlsx")
```

These paths do not exist on any machine other than the authors'. The Rmd cannot be knitted by any reviewer. Data files are present in the repository's `data/` subdirectory, but the code never references them. This is a complete reproducibility failure (Wheeler et al. 2024, §Reproducibility and extendability; code-supplement checklist).

**Fix:** Replace all absolute paths with relative paths pointing to the `data/` directory (e.g., `read_excel("data/matchups.xlsx")`).

---

### 10. No likelihood-based benchmark comparison

The POMP models are compared only to logistic regression and base ELO using prediction accuracy. No non-mechanistic time-series or probabilistic baseline (ARMA, auto-regressive logistic, IID Bernoulli) is compared using log-likelihood. Without a likelihood-based benchmark, it is impossible to determine whether the POMP model's complexity is statistically justified. A simple Bernoulli model with a constant win probability would provide a minimal baseline (Error 1.6, CC-Yes).

**Fix:** Fit at least one non-mechanistic model (e.g., logistic regression or a GLM with time-varying win probability) and compare log-likelihoods with the POMP model.

---

## Minor Issues

### 11. sigma is fixed without justification

The parameter `sigma` (process noise standard deviation) is fixed at 5 and excluded from both local and global search via `fixed_params <- coef(nba_pomp, c("sigma"))`. No rationale is given for this choice. The value 5 is set by initial conditions, not from any prior evidence or sensitivity analysis. Fixing `sigma` may introduce model misspecification that affects all other parameter estimates.

**Fix:** Either estimate `sigma` jointly with other parameters, or justify the fixed value with a sensitivity analysis showing results are stable across a range of `sigma` values.

---

### 12. Global search parameter space excludes the MLE

For Models 1 and 2, the global search box restricts `beta1` and `beta2` to `[0, 1]`. The reported MLE values are `beta1 = 1.84984` (Model 1) and `beta2 = 2.479902` (Model 2) — both lie well above the upper bound. The search relies on mif2's random walk to escape the initial box, which may not occur reliably with only 20--40 mif2 iterations. The global search may systematically underexplore regions where the true global optimum lies. Similarly, `home_court_avd` is initialized from `[200, 250]` but the MLE is approximately 89, far below the lower bound.

**Fix:** Expand the search box for `beta1` and `beta2` to at least `[0, 3]`, and for `home_court_avd` to include the range `[50, 150]`. Confirm by running a second global search with the expanded box and verifying that terminal log-likelihoods are no worse.

---

### 13. No simulation from the filtering distribution

The simulation-based diagnostics shown (e.g., simulations over fixed or MLE parameters) are all unconditional forward simulations from the initial state. No simulations from the filtering distribution (conditioning on all observed game outcomes up to each time step) are presented. Filtered simulations are the appropriate tool for assessing how well the model tracks the actual season trajectory, and are particularly important here given the structural concern in Issue 5 (Wheeler et al. 2024, §Model diagnostics).

---

### 14. p_win stored as a redundant state variable

`p_win` is stored as a latent state in `statenames`, but it is a deterministic function of `team_strength` and `opp_strength` computed within `rproc` at each step. Storing it as a state wastes particle memory and adds no information beyond what team_strength already encodes. More confusingly, `p_win` is the pre-ELO-update win probability, making its use in the traceplot comparison (lines 1003--1006) potentially misleading.

---

### 15. Convergence diagnostics are shown but not interpreted

Trace plots for local searches are displayed for all three models but are not interpreted in the text. For Model 2, the authors note that parameter estimates are "noisy" but do not assess whether the log-likelihood panel shows consistent upward convergence across all runs — which is the primary convergence criterion per course standards. At Nmif=20, convergence is not guaranteed, and the plots should be explicitly evaluated.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project09/blinded.Rmd`
