# Final AI Review: NBA POMP-ELO (w25, Project 09)

---

## Overall Assessment

This project makes an imaginative connection between the classical ELO rating system and the POMP framework, applying particle-filter-based inference to Houston Rockets game outcomes over two NBA seasons. The core framing — treating team strength as a noisy latent state driven by recent player performance momentum — is coherent and motivated. Three model variants are explored, local and global iterated filtering searches are run, and multiple non-mechanistic baselines are provided. However, the inferential conclusions are compromised by a set of concrete, correctable problems: the process-noise parameter sigma is apparently held fixed at an arbitrary value throughout optimization; the density evaluator (dmeas) and simulator (rmeas) implement materially different measurement models; the Model Att global search appears to be a copy-paste of Model 1's results rather than a distinct optimization; and log-likelihood, which is the appropriate criterion for model comparison, is computed but never used — all conclusions instead rest on prediction accuracy. Together, these issues mean that the numerical results as presented cannot be taken at face value. The project demonstrates genuine engagement with POMP methodology and a creative application domain, but requires substantial revision of both the optimization setup and the model comparison before its conclusions can be considered reliable.

---

## Key Strengths

**25.09.10 — Multiple model variants exploring genuine design questions**
The paper defines three structurally distinct POMP models: opponent ELO as a fixed covariate, opponent ELO as a second stochastic state, and an attendance-modulated home-court advantage parameter. These represent real modeling decisions rather than superficial variations, and the comparisons illuminate the tradeoff between state complexity and estimation stability.

**25.09.11 — Multiple starting points in global search**
The trace plots show multiple colored chains launched from different starting points, indicating that the global search was implemented with the correct multi-start logic. This is the right approach for avoiding local optima.

**Interpretable model structure**
The mean-reverting regularization term alpha*(TS - 1500) prevents unbounded growth of the latent state, which is a thoughtful design choice that reflects domain knowledge about the ELO scale.

---

## Major Points

**ID: 25.09.1**
**Concern:** Sigma is never optimized — it is fixed at 5.00 throughout all local and global searches.
**Why it matters:** Sigma controls the magnitude of process noise, which is the central mechanism distinguishing POMP-ELO from deterministic ELO. Fixing it at an arbitrary value means the reported MLE estimates and log-likelihoods correspond to a partially constrained model whose noise level was not chosen by the data. All quantitative conclusions about model fit and parameter estimates are conditional on this unjustified fixed value.
**Severity:** Major
**Suggested author action:** Include sigma in the `mif2` parameter vector with a reasonable box constraint (e.g., 1 to 50). Re-run local and global searches. Report the optimized sigma alongside a profile likelihood over sigma to assess identifiability of the noise level.

---

**ID: 25.09.2**
**Concern:** The density evaluator `dmeas` and the simulator `rmeas` implement materially different win-probability formulas.
**Why it matters:** The particle filter weights particles using `dmeas` and generates simulated observations using `rmeas`. When these compute different probabilities for the same state, the filter is incoherent — it scores particles under one model and generates predictions under another. This invalidates both the reported log-likelihoods (used for inference) and the simulated prediction accuracies (used for comparison).
**Severity:** Major
**Suggested author action:** Unify `dmeas` and `rmeas` to use the same probability formula. The `dmeas` log-sum-exp form (dividing by 100) is the cleaner version; rewrite `rmeas` to use the same scaled Bradley-Terry formula. Verify that `give_log` is handled correctly in `dmeas`.

---

**ID: 25.09.3**
**Concern:** The Model Att global search table is numerically identical to the Model 1 result, indicating it was not actually run as a separate optimization.
**Why it matters:** If Model Att was not re-optimized, its reported accuracy (71%) and parameter estimates are meaningless as evidence of the attendance effect. The paper's conclusion that attendance adds value to the model cannot be supported.
**Severity:** Major
**Suggested author action:** Re-run the global search for `nba_pomp_att` separately, save the resulting parameter estimates and log-likelihood, and compare them to Model 1 using AIC.

---

**ID: 25.09.5**
**Concern:** Model 2 is declared the best model based on a 1.4 percentage-point accuracy advantage, while its log-likelihood is approximately 9 units worse than Model 1 (Model 1: -97.3; Model 2: -106), implying ΔAIC ≈ 18 in favor of Model 1 after penalizing Model 2's extra parameter.
**Why it matters:** Prediction accuracy on the same 164 training games is a poor model-selection criterion — it does not penalize complexity and a 1.4 pp difference over 164 binary outcomes is within normal sampling variation. Log-likelihood and AIC are the appropriate tools for comparing nested models. By these criteria, Model 1 is clearly preferred.
**Severity:** Major
**Suggested author action:** Use AIC (or likelihood ratio test for nested models) as the primary model selection criterion. Report ΔAIC for each model pair. Retain prediction accuracy as a supplementary metric but do not use it for formal model selection.

---

**ID: 25.09.4**
**Concern:** Base ELO prediction accuracy is reported as 57.93% in the text but 66.46% in the comparison table.
**Why it matters:** This 8.5 pp discrepancy changes the narrative — if Base ELO achieves 66.46%, it is competitive with all logistic regression variants, and the POMP gains are more modest than the text implies. If 57.93% is correct, the table is wrong. Either way, the comparison table cannot be trusted.
**Severity:** Major
**Suggested author action:** Identify the source of the discrepancy (different prediction thresholds? different seasons? different ELO initialization?), correct the table, and add a note explaining what each accuracy value represents.

---

**ID: 25.09.6**
**Concern:** Inside `rproc`, a simulated game outcome (`sim_win`) is drawn from the current win probability and used immediately to update `team_strength` within the same process step. The observed outcome `Win` is then evaluated against `dmeas` separately.
**Why it matters:** In a standard POMP hidden Markov model, the observation is external to the process equation. Here the process generates an internal pseudo-observation and uses it for state evolution before the actual observation is incorporated via filtering. This means the latent state has already incorporated a random game result that may differ from the observed result — a structural inconsistency that makes the particle filter's weighting semantically problematic.
**Severity:** Major
**Suggested author action:** Move the ELO update based on game outcome out of `rproc` and into a deterministic covariate (since the actual game result is observed), or carefully document why drawing `sim_win` inside `rproc` is the intended design and how it relates to the filtering operation.

---

**ID: 25.09.7**
**Concern:** No confidence intervals or profile likelihoods are computed for any parameter.
**Why it matters:** Parameter point estimates (beta1 ≈ 1.85, alpha ≈ 0.571, home_court_avd ≈ 89) carry substantive interpretations (momentum effect, mean reversion rate, home advantage magnitude). Without uncertainty quantification, it is impossible to know whether these estimates are informative or whether the data can distinguish them from zero or from alternative values.
**Severity:** Major
**Suggested author action:** Compute profile likelihoods for at least the key parameters (beta1, alpha, home_court_avd) using the course-standard profile likelihood approach with a fixed grid. Report 95% confidence intervals using the MCAP or chi-squared cutoff.

---

**ID: 25.09.8**
**Concern:** Local and global searches use only 20 mif2 iterations. Several parameters (beta1, home_court_avd in Model 2) have not stabilized by the final iteration.
**Why it matters:** MLE estimates obtained from insufficiently converged searches are not the true MLEs — they are upper bounds at best. The reported log-likelihoods and parameter values may not represent the model's actual optimum.
**Severity:** Major
**Suggested author action:** Increase `Nmif` to at least 100 (run_level=2) or 200 (run_level=3). Verify convergence by showing that chains from different starting points have reached the same region by the final iteration. The trace plots show the requisite structure — just extend the runs.

---

## Minor Points

**Measurement model: rmeas uses raw ELO scale; dmeas rescales by /100.**
These different scalings mean that even if the formulas were otherwise aligned, `home_court_avd` would have very different quantitative meaning in each snippet. Report which scale is intended and apply it consistently.

**p_win stored as state variable without justification.**
p_win is a deterministic function of team_strength and opp_strength at each step. Storing it as a state variable adds no information and increases the particle filter's state dimension. Remove it as a state and compute it on the fly in dmeas/rmeas as needed.

**OPP equation has a stray plus sign:** Line 312 reads `+ - alpha(OPP_n - 1500)`.

**ELO update equation (line ~67)** writes `TS = TS ± K·E_S` but the standard ELO formula updates by `K*(1 - E_S)` for a win. The code implements the correct formula but the displayed equation does not match. Correct the equation.

**Model 2's `partrans` does not appear to include `log = c("alpha")`** in the visible model specification code, unlike Model 1. Verify that the alpha positivity constraint is enforced for all models.

**No `set.seed()` calls visible.** Results are not exactly reproducible.

**Software versions not reported.** State R version and pomp version.

**Figure captions are absent.** Figures 003, 004, 011, 012, 013 show win probability traces with colored lines but no legend or caption explaining what each line represents.

**Prose errors:** "there is there is" (Introduction), "A a crucial player", "we we're unable to", "similarly improvements", "did due compared". Proofread before final submission.

**Text says the model was tested on 164 games** spanning two seasons. It would be worth noting whether the parameter search used all 164 games or a training/test split, since the prediction accuracy figures appear to be in-sample.
