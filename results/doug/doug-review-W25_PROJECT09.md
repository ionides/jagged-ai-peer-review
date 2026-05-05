# Peer Review: W25 Project 09
## NBA POMP-ELO: A Stochastic System Approach to Modeling Team Strength and Predicting Games

---

## Summary

This project applies POMP methodology to NBA basketball, modeling the Houston Rockets' team strength as a latent state and using that state — embedded in an ELO-like update structure with a Bradley-Terry win-probability observation model — to predict game outcomes. Three model variants are presented: one with opponent ELO as a fixed covariate (Model 1), one where opponent strength is also a latent state (Model 2), and one that augments Model 1 with attendance as a modifier of home-court advantage (Model Att). Logistic regression and base ELO serve as non-POMP baselines. The project's central contribution is the creative formulation of sports ratings as a POMP problem.

The analysis has several genuine strengths: the motivating question is clearly stated, the ELO update equations are derived from first principles, and the mif2-based local and global searches are at least attempted. However, the project contains numerous severe methodological and code-level problems that undermine all its quantitative conclusions. The measurement models (dmeas/rmeas) are specified on incompatible scales, the global search box excludes the MLE found in the same document, model evaluation relies entirely on out-of-sample simulation accuracy computed on a stochastically generated binary outcome rather than on log-likelihood, no quantitative goodness-of-fit metric is reported, the Model 3 (attendance) best-parameter simulation uses the wrong pomp object, and the comparison between POMP models and baselines conflates the inference objective with prediction accuracy from a stochastic simulator. These failures make the paper's central empirical conclusion — that POMP-ELO "drastically improved" predictive power — unreliable.

---

## Major Issues

### 1. dmeas and rmeas implement different probability models on incompatible scales

The `dmeas` Csnippet divides `team_strength` and `opp_strength` by 100 before computing the Bradley-Terry probability, then evaluates `dbinom(Win, 1, p, give_log)`. The `rmeas` Csnippet uses the raw `team_strength` and `opp_strength` values (ELO scale, ~1500) directly in logistic-scale arithmetic without any division:

```c
// dmeas: divides by 100
double team_score = team_strength / 100.0;
double opp_score  = opp_strength  / 100.0;

// rmeas: uses raw values (~1500) in logistic expression
p = exp(home_court_avd + team_strength - opp_strength) / ...
```

Because ELO values near 1500 produce `exp(team_strength - opp_strength)` = `exp(0)` = 1 in `rmeas`, but `team_score = 15` in `dmeas`, the two snippets are computing win probabilities from entirely different numerical inputs. The particle filter evaluates `dmeas` for likelihood calculation while `rmeas` is used for forward simulation, so simulated trajectories and likelihood values reflect different models. This is a fundamental measurement-model inconsistency of the type flagged by Wheeler et al. (2024) as a concrete reproducibility failure, and it invalidates all likelihood evaluations, all IF2 estimates, and all simulation-based accuracy figures. Per the `pomp-inference-misuse` skill, this is a critical code error.

**Fix:** Standardize both snippets to the same scale. The simplest correction is to divide by 100 in `rmeas` as well, or to use the raw ELO scale consistently in both.

---

### 2. No log-likelihood or AIC reported; goodness-of-fit is purely visual and simulation-based

The paper does not report a single log-likelihood value for any POMP model. The IF2 convergence traces are shown, and best-row global-search results are printed (in a chunk whose output is included), but the log-likelihood at the MLE is never stated in the text, compared across models, or compared to any statistical threshold. Model comparison is done entirely via binary prediction accuracy computed from stochastic forward simulations. Wheeler et al. (2024) note that "visual comparisons alone are only a weak and informal measure of goodness-of-fit" — the same applies to simulation-based binary accuracy. Without log-likelihoods, it is impossible to assess whether the mechanistic model provides better statistical fit than the logistic regression baseline, or whether any two POMP variants are statistically distinguishable. Per POMP checklist item 3, this is a major deficiency.

**Fix:** Report the maximized log-likelihood (or AIC) for each POMP model and for the logistic regression (via its log-likelihood from `logLik(log_elo)`). Use likelihood ratio tests or AIC for model comparison. Retain prediction accuracy only as a secondary applied metric.

---

### 3. Global search box excludes the MLE found during that same search

For Model 1, the global search box is defined as:
```r
lower = c(beta1=0, home_court_avd=200, alpha=0)
upper = c(beta1=1, home_court_avd=250, alpha=1)
```
Yet the best-row result from the same search reports `home_court_avd = 89.33528` — a value more than twice below the lower bound of 200. This means the global search found its best solution by drifting far outside the declared box during IF2 iterations, which is accidental exploration rather than systematic coverage. The reported MLE is therefore not a result of genuine global search over the specified box, and the claim that a global search was conducted is not supported. The same misalignment occurs for Model 2 and for Model Att (same box definition, same solution at `home_court_avd ≈ 89` or `75`). Per the `pomp-global-search-box-misalignment` skill, this is a major issue.

**Fix:** Center the box on the values found in the local search (e.g., `home_court_avd` near 40–100 based on the fixed simulation parameters) or use a wider box. The current box covers [200, 250] which is far above the range where the model evidently achieves good fits.

---

### 4. Model 3 (attendance) best-parameter simulation uses the wrong pomp object

In the attendance section, the global search runs correctly on `nba_pomp_att`, but the subsequent "best parameter" simulation uses `nba_pomp` (the base Model 1 object without attendance in the covariate table):

```r
nba_pomp |> simulate(              # should be nba_pomp_att
  params = c(beta1 = 1.84984, ..., home_court_avd = 89.33528, ...),
  ...
) -> sims_att_best
```

The parameters used are also identical to the Model 1 best-row values, not the Model Att global search results. This means `errors_att` and the accuracy figure for "Model Att" in the comparison table are computed from Model 1 simulations, not Model 3. The attendance model was never actually evaluated at its own estimated parameters. Per the `pomp-dataset-substitution-audit` skill's principle of tracing which object feeds each result, this renders all conclusions about the attendance model invalid.

**Fix:** Replace `nba_pomp` with `nba_pomp_att` and use `results_att[which.max(results_att$loglik), ]` for the attendance model's best parameters.

---

### 5. Global search uses previous mif2 result object as the base rather than the raw pomp object

Both the Model 1 and Model Att global searches use `mf1 <- local_mifs[[1]]` (a previous mif2 result) as the first argument to the inner `mif2()` call:

```r
mf1 |>
  mif2(params=c(guess, fixed_params)) |>
  mif2(Nmif=20) -> mf
```

Per the `pomp-global-search-init-audit` skill, passing a previous mif2 result as the first argument causes the global search to inherit the cooling schedule from the local chain. The cooling at `mf1` is near its final decayed state after 20 IF2 iterations, so the global search restarts effectively perform very few functional IF2 iterations from the new random starting point. The reported "global" maximum may simply reflect the local-search neighborhood re-evaluated with different random seeds, not genuine global exploration. This compounds the box misalignment problem in Issue 3.

**Fix:** Replace `mf1 |> mif2(params=...)` with `nba_pomp |> mif2(params=..., Np=1000, Nmif=20, ...)` to ensure each global replicate starts from a fresh pomp object with a full cooling schedule.

---

### 6. No benchmark comparison against a non-mechanistic statistical model

The paper compares POMP models to logistic regression and base ELO, but neither is a time-series benchmark in the standard POMP-review sense (Wheeler et al. 2024, item 2). Logistic regression does not model the serial dependence in game outcomes, and ELO is itself a deterministic forerunner of the mechanistic model, not an independent statistical benchmark. An ARMA model for win probability, or an auto-regressive logistic model for binary game outcomes, would constitute a proper baseline for assessing whether the POMP model captures meaningful temporal structure. Without such a comparison — made on log-likelihood grounds, not prediction accuracy — there is no evidence that the stochastic latent-state model outperforms simpler time-series approaches.

**Fix:** Fit an AR(p) logistic regression on win outcomes (or a simpler logistic model with lagged ELO as a predictor) and compare log-likelihoods.

---

### 7. Computational adequacy is very low: Np=1000 and Nmif=20 with no convergence evidence

The local search uses Np=1000 particles and Nmif=20 mif2 iterations, and the global search runs two consecutive `mif2` calls of Nmif=20 (effectively 20 iterations from the inherited chain, per Issue 5). For a POMP model with 4–5 parameters, 20 IF2 iterations is typically far below convergence. The convergence traces shown in the figures are stated to be noisy for Models 1 and 2 (especially Model 2), and the text acknowledges "more noisy estimates" without investigating whether this is due to model misspecification or insufficient computation. The likelihood standard errors from `logmeanexp` are computed but not reported in the text, so Monte Carlo error in the likelihood estimates is unquantified. Per Wheeler et al. (2024) item 6 and POMP checklist, this is a major deficiency.

**Fix:** Increase Nmif to at least 100–200 and Np to at least 2000. Show convergence traces that have flattened. Report the loglik.se values and confirm they are small (< 0.5) before interpreting MLE estimates.

---

### 8. Prediction accuracy is evaluated on training data, not held-out games

All "prediction accuracy" figures are computed by simulating forward from fixed parameters and comparing simulated outcomes to the same 164 games used to fit the model. This is in-sample accuracy, not predictive accuracy. A model that simply memorizes the ELO ordering will achieve similar in-sample accuracy. The paper presents these figures as evidence that POMP-ELO is a better predictor than base ELO, but this comparison is invalid because: (a) ELO accuracy is also computed in-sample on the same 164 games, and (b) the POMP simulation accuracy is from a stochastic forward simulation, not from the filtering distribution conditioned on game-by-game data, so the comparison is not even on equal footing. No test-set evaluation or cross-validation is performed.

**Fix:** Hold out the last season (or last 20 games) for evaluation. Compare all models on the same held-out period using proper scoring rules or calibrated probability forecasts, not just binary accuracy.

---

### 9. sigma is fixed throughout and never estimated or justified

The parameter `sigma` (process noise standard deviation) is declared in `paramnames` and held fixed at 5 throughout — it is extracted via `fixed_params <- coef(nba_pomp, c("sigma"))` and excluded from all `rw.sd` calls. A value of 5 ELO points per game is chosen arbitrarily and its sensitivity is never assessed. Because sigma controls the amount of stochastic variation in team strength, it directly affects the likelihood surface and the identifiability of other parameters. Fixing it without justification means the reported MLE values for beta1, alpha, and home_court_avd are conditional on an unjustified sigma, and the model may be under- or over-dispersed relative to the data. Per POMP checklist item 9 (stochasticity) and item 5 (identifiability), this should be flagged.

**Fix:** Either estimate sigma via IF2 alongside the other parameters, or conduct a sensitivity analysis by repeating the optimization at sigma = 1, 5, 10 and reporting how much the MLE for other parameters changes.

---

### 10. rw.sd values are set to the parameter starting values, not appropriate perturbation sizes

In all `rw.sd` calls, the perturbation sizes equal the starting-point values of the parameters:
```r
rw.sd = rw_sd(beta1=0.5, home_court_avd=40, alpha=0.05)
```
This is unusual: `rw.sd` specifies the standard deviation of the IF2 random-walk perturbations, not the initial parameter values. For `home_court_avd`, a perturbation SD of 40 (nearly the entire starting value) means the parameter will be perturbed by on the order of ±80 ELO points each iteration — an enormous perturbation that will cause IF2 to explore far outside any reasonable region. For `beta1 = 0.5` the perturbation is equal to the starting value, again very large relative to the parameter scale. The IF2 algorithm requires perturbation sizes comparable to the expected MLE uncertainty, not to the parameter magnitude itself. Oversized perturbations cause the parameter chain to diffuse rather than converge.

**Fix:** Set `rw.sd` to small values (e.g., 0.02–0.05 for beta1, 1–5 for home_court_avd, 0.001–0.01 for alpha) and verify convergence by inspecting whether traces decrease and stabilize.

---

## Minor Issues

- **Hard-coded absolute paths**: The data loading code contains absolute paths (`/Users/nicholaskim/Documents/...`), making the analysis non-reproducible on any other machine. All paths should be relative to the project root.

- **p_win is declared as a state variable but is not a population quantity**: `p_win` is stored as a state variable via `statenames` and is reset each time step. Because it is a derived quantity (a function of the current `team_strength` and `opp_strength`) rather than an accumulated flow, it does not need to be in `statenames` and accumulates no meaningful sequential information. Including it in `statenames` increases computational overhead without benefit and adds a spurious state to the particle filter.

- **Model 2 best-parameter simulation uses nba_pomp (Model 1 object) instead of nba_pomp2**: In the Model 2 post-search evaluation, `nba_pomp |> simulate(...)` is called with Model 2's best parameters, but `nba_pomp` does not have `opp_strength` as a state or `beta2` as a parameter. This is either a silent error or a coding oversight; at minimum, `nba_pomp2` should be used.

- **ELO is provided both as a covariate and as a data column, creating potential confusion**: The data frame passed to `pomp()` contains an `elo` column (the Rockets' own ELO) as a data variable, but it is used only for plotting, not in the model. This creates a risk of confusion between the latent `team_strength` state and the `elo` covariate. The paper would benefit from a clear statement that `elo` is carried along for plotting purposes only.

- **The attendance logistic regression accuracy is compared against `bpm$Win` but uses `bpm_att` for model fitting**: The line `mean(pred_win_att == bpm$Win)` evaluates the attendance-augmented logistic regression against the `bpm` dataset (the non-attendance dataset). If the row order of `bpm` and `bpm_att` differs, this produces incorrect accuracy. The correct target should be `bpm_att$Win`.

- **No parameter uncertainty or confidence intervals**: The paper reports MLE point estimates from the global search but provides no confidence intervals for any parameter. Profile likelihoods are entirely absent. Without uncertainty quantification, there is no basis for concluding that any parameter is reliably estimated from this dataset. Per POMP checklist item 5, profile likelihoods or at minimum likelihood-based confidence intervals should be reported for the key parameters (beta1, home_court_avd, alpha).

- **The conclusion overstates the evidence**: The conclusion claims POMP-ELO has "drastically improved predictive power" relative to ELO. Given the measurement-model inconsistency (Issue 1), the wrong object used in simulation (Issue 4), the training-set-only evaluation (Issue 8), and the absence of log-likelihood reporting (Issue 2), this conclusion is not supported by the analysis as presented.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project09/blinded.Rmd`
