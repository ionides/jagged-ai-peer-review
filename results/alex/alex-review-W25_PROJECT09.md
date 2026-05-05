# Peer Review: NBA POMP-ELO (W25 Project 09)

---

## Summary

This project applies POMP methodology to model the Houston Rockets' "team strength" as a latent state, building on an ELO framework augmented with player Box Plus/Minus (BPM) covariates, home-court advantage, and fan attendance. Three POMP variants are proposed and compared against logistic regression and raw ELO baselines. While the topic is creative and the motivation is clear, the project suffers from several fundamental methodological flaws that undermine the validity of the results and conclusions.

---

## Weaknesses (Most Critical First)

### 1. [MAJOR] In-sample prediction used as the primary evaluation metric

The accuracy figures for all models (POMP, logistic regression, base ELO) are computed on the same 164 observations used for both model fitting and parameter estimation. There is no held-out test set, no cross-validation, and no out-of-sample evaluation. Reporting "Pred Acc" from simulations on training data is not a measure of predictive power; it measures in-sample fit. The conclusion that "POMP-ELO drastically improved its predictive power" is unsupported because no genuine prediction exercise was conducted. A proper evaluation would withhold at minimum one season's games and predict the other.

### 2. [MAJOR] Prediction accuracy computed from stochastic simulations rather than from expected win probabilities

The accuracy for POMP models is computed by averaging binary win predictions across 20 stochastic simulations (i.e., `mean(pred == actual)` over simulated `Win` draws). Because `Win` is a Bernoulli draw from `p_win`, each simulation independently generates a noisy binary outcome. Averaging accuracy over these noisy draws is not equivalent to comparing the model's win probability against the threshold 0.5, which is how the logistic regression and ELO baselines are evaluated. This inconsistency makes all model comparisons invalid: the POMP models are evaluated on a different (and more favorable) operational definition of "prediction."

### 3. [MAJOR] Critical code bug: Model 3 (Attendance) simulates from nba_pomp, not nba_pomp_att

At line 835, the "best parameter" simulation for the Attendance model uses `nba_pomp` (Model 1 object) rather than `nba_pomp_att`:

```r
nba_pomp |> simulate(
  params = c(beta1 = 1.84984, sigma = 5, home_court_avd = 89.33528, alpha = 0.5705353),
  ...
) -> sims_att_best
```

This means the reported accuracy for "Model Att" in the comparison table is identical to Model 1's result. The attendance model is never actually evaluated with its own optimized parameters or with its own POMP object. The conclusion regarding attendance effects is therefore entirely spurious.

### 4. [MAJOR] dmeas and rmeas are inconsistent with each other

The `dmeas` Csnippet computes the log-likelihood using a softmax formulation with explicit `max_val` normalization and home-court adjustment applied only to `team_score`. The `rmeas` Csnippet uses a different logistic formula where `home_court_avd` is added to or subtracted from the combined `(team_strength - opp_strength)` without dividing by 100 first. Because the measurement model used for likelihood evaluation (`dmeas`) is not the same model as that used for simulation (`rmeas`), parameter estimates from IF2 are for a model that is never actually simulated, and simulated predictions are from a model whose likelihood was never maximized.

### 5. [MAJOR] sigma (noise parameter) is fixed and excluded from optimization

`sigma` is set to a fixed value of 5 in both the local and global searches and is never included in `rw.sd`. No justification is given for why sigma = 5 is appropriate. Since sigma controls the magnitude of stochastic noise in team strength, fixing it arbitrarily truncates the parameter space and may prevent the optimizer from finding a meaningful optimum. A sensitivity analysis with respect to sigma, or at minimum a profile likelihood, is needed.

### 6. [MAJOR] Global search parameter bounds are poorly motivated and potentially off-scale

The global search for `home_court_avd` searches the interval [200, 250], but in simulations fixed at 40, and in the best-found parameter it is 89. The interval [200, 250] is far from both the initial guess of 40 and the apparent best value of 89. This means the global search is exploring a region that is inconsistent with prior knowledge, and the "best" parameter from the global search (home_court_avd = 89) lies outside the search box. It is unclear how this result was obtained; there may be additional local mif2 steps not shown, but this is not explained.

### 7. [MAJOR] No likelihood-based model comparison; log-likelihood values are not reported or discussed

The project never reports absolute log-likelihood values or uses them to compare models. The `results` and `results2` objects from the global search contain loglik columns, but the only output shown is the row with the maximum loglik. No likelihood ratio tests, AIC/BIC comparisons, or log-likelihood traces over IF2 iterations are discussed. For a POMP course project, comparing models via likelihood is the standard and expected approach, not accuracy of stochastic binary draws.

### 8. [MAJOR] ELO is used as the observed data for the latent state, not as the actual observation

The state variable `team_strength` is initialized at 1500 (ELO baseline) and is intended to mirror ELO, but the actual POMP observation is `Win` (binary game outcome). However, the simulations are plotted against `elo` as if ELO were the true state. ELO itself is a deterministic post-hoc calculation from observed wins and losses; it is not the true latent team strength. Validating model trajectories by visual comparison to a derived deterministic quantity (ELO) conflates the latent state with a specific estimation of it.

### 9. [MODERATE] t0 = 1 rather than t0 = 0; initialization issues with sequential ELO

The POMP object sets `t0 = 1` and `times = 1:164`, meaning the initial state at time 1 is the state just before the first observation. The ELO computation, however, already incorporates the first game result into `rockets_elo_df$elo`. This introduces a one-step indexing inconsistency: the ELO covariate at time 1 is the post-game ELO from game 1, not the pre-game ELO. Since the pre-game ELO is the relevant "opponent strength" for making predictions, this misalignment affects all 164 time steps.

### 10. [MODERATE] BPM covariates for the first several games have fewer than 5 games to average over, yet this is not formally documented or validated

The report states that for early games the average is over however many games have been played, but there is no explicit code shown for this calculation, and the BPM data is loaded from an Excel file without any verification that this averaging is correctly implemented. Given that the ELO computation starts fresh at 1500 for 2023-24 and carries into 2024-25, and there are 164 total games, the initialization choices and boundary conditions of the rolling window deserve explicit treatment.

### 11. [MODERATE] No convergence diagnostics or particle filter variance assessments

The IF2 traces for loglik are shown but never analyzed for convergence. The report mentions that Model 2 has "more noisy estimates," but provides no formal convergence check. The number of particles (Np = 1000) and number of IF2 iterations (Nmif = 20) are modest; no justification is given for their adequacy. Additionally, `loglik.se` is computed but never reported or discussed, making it impossible to assess uncertainty in the likelihood estimates.

### 12. [MODERATE] p_win is treated as a state variable rather than a derived quantity, causing conceptual confusion

`p_win` is stored as a state variable in `statenames` alongside `team_strength`. However, `p_win` is a deterministic function of `team_strength` and `opp_strength` at each time step and carries no additional state information. Including it as a state inflates the state dimension without benefit and conflates it with actually stochastic state components. More importantly, p_win is computed in `rproc` before the ELO post-game update, so it reflects the pre-game probability, which is then overwritten each step. This is used for the mean win probability plots, but its interpretation is never clearly stated.

### 13. [MODERATE] Hardcoded absolute file paths prevent reproducibility

The Rmd file contains absolute paths tied to a specific local machine:
- `/Users/nicholaskim/Documents/STAT-531/final/data/matchups.xlsx`
- `/Users/nicholaskim/Documents/STAT-531/final/data/BPM.xls`
- `/Users/nicholaskim/Documents/STAT-531/final/data/BPM-new.xlsx`

These paths will fail on any other machine. The data files are present in the `data/` subdirectory of the submission, so relative paths should have been used. This makes the project non-reproducible as submitted.

### 14. [MINOR] Logistic regression uses same data as POMP models but without proper train/test split, making the 64% baseline misleading

The logistic regression model is fit on all 164 games and its accuracy (64%) is in-sample. Similarly, ELO win probability is derived from the same sequence of games. Without a proper hold-out evaluation, the comparison of 64% (logistic) vs. higher POMP accuracy figures is not meaningful because all numbers reflect memorization of training data, not generalization.

### 15. [MINOR] The attendance POMP model's dmeas is never updated to include the attendance covariate

The `rmeas_att` Csnippet includes `log(attendance)` in the win probability formula, but `dmeas` (used for likelihood computation) is the same as in Models 1 and 2 and does not include attendance. This means IF2 parameter estimation for the attendance model optimizes a likelihood that does not reflect the attendance effect, even though `rmeas_att` applies it. The attendance-adjusted model therefore cannot be said to have been properly estimated via maximum likelihood.

---

## Summary of Critical Issues

The two most consequential problems are (1) the use of in-sample stochastic simulation accuracy as the sole evaluation metric, and (2) the bug that causes Model 3's evaluation to silently reuse Model 1's simulation object. Together these mean that neither the comparison table nor the conclusion ("POMP-ELO drastically improved its predictive power") can be taken at face value. A proper re-analysis would require a train/test split, a consistent comparison methodology based on expected win probabilities, and corrections to the dmeas/rmeas inconsistency and the attendance model evaluation.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project09/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project09/ref.bib`
