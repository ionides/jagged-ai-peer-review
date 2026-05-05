# Peer Review: W24 Project 01
## "A Latent Process of Democracy since 1800"

---

## Summary

This project applies a POMP (Partially Observed Markov Process) framework to model the global spread of democracy from 1800 to 2020. The authors construct an SPRN compartmental model inspired by game-theoretic theories of democratization (Acemoglu and Robinson 2006), in which sovereign states transition from a pool of autocracies (S) through elite-dominated periods (P), revolutionary threats (R), into negotiated democracies (N). The annual increment of democracies (delta Z(t)) is modeled as a negative binomial observation. The authors run a global search with 200 IF2 restarts and compare the POMP model against regression benchmarks.

The project shows genuine engagement with POMP methodology and the political science literature, and the inclusion of a benchmark comparison is commendable. However, the analysis contains multiple serious flaws: a critical discrepancy between the mathematical model description and the implemented code; a saved results file with parameter names inconsistent with the described model; a flawed approach to profile likelihood and confidence intervals; a fundamental structural issue with the state space that prevents the model from capturing the growing number of sovereign states; and several methodological weaknesses in diagnostics and inference. These issues collectively undermine confidence in the reported parameter estimates and substantive conclusions.

---

## Major Issues

### 1. Critical mismatch between model description and implemented code

The text (Section 2.1) states that the transition rate from S to P is governed by the expected value `beta * R(t) / zeta(t)`, where `R(t)` represents revolutionary threats and `zeta(t) = S(t)` is the covariate. However, the implemented `sprn_step` Csnippet reads:

```c
double dN_SP = rbinom(S, 1-exp(-Beta * N/tot_sov * dt));
```

The code uses `N` (the negotiation/democracy compartment, a stock that only accumulates) rather than `R` (revolutionary threats) in the numerator. It also uses `tot_sov` (the covariate from `covar.csv`) rather than the compartment `S` in the denominator. This means the transition mechanism actually implemented is not what the text describes. The rate of new elites emerging increases as democracies accumulate, which is the opposite of the theoretical mechanism (revolution drives democratization, not prior democracy). This discrepancy materially affects what is being estimated and the substantive interpretation of all results. Per Wheeler et al. (2024), model-code consistency is a fundamental reproducibility requirement.

### 2. Saved results (RDS file) appear to be from a different model

The archived results file `Level 2.5.rds` contains a column named `mu_IR` (column 5), which the analysis renames to `mu_PR` at line 287 (`colnames(result)[5] <- "mu_PR"`). The name `mu_IR` is characteristic of an SEIR-type epidemic model (I = Infected, R = Recovered), while the described SPRN model uses `mu_PR` (P = powerful elites to R = revolutionary threats). Furthermore, the range of this column spans five orders of magnitude (0.030 to 5,530), far exceeding the upper search bound of 100 specified in `runif_design`. This strongly suggests the RDS file was saved from a different model run, potentially with a different parameterization, rather than from the SPRN model described. The rename silently masks this discrepancy. All parameter estimates and confidence intervals derived from this file are therefore of uncertain validity.

### 3. Profile likelihood not computed; confidence intervals are invalid

The paper describes and displays "profile likelihood confidence intervals" (Section 2, Figure 4) and applies the Wilks theorem cutoff (`maxlog - 0.5 * qchisq(df=1, p=0.95)`). However, the underlying plot is a scatter of the global search results (one loglik value per random starting point), not a true profile likelihood. A profile likelihood requires fixing each parameter at a grid of values and re-optimizing over all remaining parameters for each fixed value. Applying a chi-squared cutoff to a global search scatter does not produce valid confidence intervals. As a result, the claimed parameter identifiability evidence and confidence intervals in the paper are unsupported. The paper even notes that `mu_PR` (mu_IR) ranges widely with near-zero correlation with loglik, which is a sign of non-identifiability, but this is not discussed appropriately. Profile likelihoods should be computed via `profile_design()` combined with separate `mif2` runs at each fixed value, per Wheeler et al. (2024), Section on parameter identifiability.

### 4. Structural flaw: state S cannot accommodate new sovereign states

The model initializes `S = 23` (matching the 23 sovereign states in 1800) and allows S to decrease as states transition to P. However, the number of sovereign states grows from 23 in 1800 to approximately 195 by 2020, as confirmed by the covariate `tot_sov`. The model provides no mechanism for new sovereign states to enter the system. Once the initial 23 states have all transitioned through the pipeline, `S = 0` and no further democratization is possible. This contradicts both the data (ongoing new democracies throughout the period) and the theoretical motivation. The covariate `tot_sov` is used in the denominator of the S-to-P transition but never used to replenish S. This is a fundamental structural misspecification that likely drives the simulation overprediction noted in the probes analysis.

### 5. Observation model inconsistency: stock vs. flow mismatch

The observation model specifies `E[delta Z(t)] = rho * N(t)`, where `N(t)` is the cumulative (stock) count of negotiated democracies. However, `delta Z(t)` is a flow variable (new democracies per year). As `N(t)` accumulates over 221 years to approximately 154, the expected annual new democracies `rho * N` grows to approximately 10 by the end of the period, whereas the observed mean of `delta Z(t)` is only 0.69 per year. The model should instead measure against the flow `dN/dt` (the rate of transitions into N), not the stock `N` itself. This mismatch is the root cause of the simulation overprediction documented in Figure 7. An appropriate fix would use a within-period accumulator variable (as in SEIR models where new infections per observation period are tracked via an accumulator, then reset) rather than the compartment stock.

### 6. No convergence diagnostics for IF2

The paper reports running 200 IF2 chains with 200 iterations and 2,000 particles. No convergence traces (log-likelihood vs. iteration number) are presented. Without these traces, it is impossible to assess whether the optimization has converged, whether the cooling schedule was appropriate, or whether additional iterations would improve the estimates. The pairs plots of global search results (Figures 3–4) are informative but cannot substitute for convergence traces. The random walk size of 0.02 applied uniformly to all parameters (on their natural scales) is also not justified, as parameters span different scales (e.g., `Beta` at ~0.26 vs. `mu_IR` at ~0.03). Per Wheeler et al. (2024), convergence diagnostics are an essential component of computational adequacy.

### 7. Non-identifiability of mu_PR not acknowledged

The column `mu_IR` (presented as `mu_PR`) ranges from 0.030 to 5,530 across 200 runs, with a correlation of only -0.06 with the loglikelihood. This near-zero correlation over five orders of magnitude is a strong indicator that `mu_PR` is unidentifiable from the data — the model fit is essentially independent of this parameter's value. The paper does not acknowledge this non-identifiability. Instead, it interprets the confident estimates of other parameters as evidence that "the parameter estimates are well identified" (Section 2). This conclusion cannot be drawn from a global search scatter, and it fails entirely for `mu_PR`. Unidentifiable parameters should be discussed as a potential model misspecification, consistent with Wheeler et al. (2024) guidance on parameter identifiability.

---

## Minor Issues

### 8. AIC for IID model uses incorrect number of parameters

The AIC for the IID negative binomial model is computed as `AIC.iid <- 2 - 2 * log.iid`, implying one free parameter. The IID NB model fitted by `optim(c(0,-5), nb_lik)` estimates two parameters (log-size and log-prob). The correct formula is `AIC.iid <- 4 - 2 * log.iid`. This is a minor error (difference of 2 AIC units) but understates the penalty for the IID model.

### 9. Duplicate figure caption variable (cap_fig7)

The variable `cap_fig7` is assigned twice: once for "Figure 7. Simulation Plot" (line ~432) and once for "Figure 7. Probes Plot" (line ~457). Both figures also share the caption number "Figure 7," which conflicts with the figure numbering in the text. The probes plot should be labeled Figure 8. The duplicate assignment in R means the second assignment overwrites the first; neither figure will display the intended caption.

### 10. Mathematical formula contains a typographical error

The equation for the S-to-P transition in the text (Section 2.1) reads: `N_SP(t+delta) + N_SP(t) + Binomial[...]`. The `+` connecting the left side to the right side should be `=`. This appears to be a copy-paste artifact from a difference equation formulation.

### 11. Benchmark comparison conclusion is imprecise

The paper states that "negative binomial regression performs better as opposed to POMP." By raw loglikelihood, the NB regression is only marginally better (-210.62 vs -211.85, a difference of ~1.2 units). Given that the loglikelihood SE for the POMP estimate is ~0.02, the POMP loglikelihood estimate is subject to additional Monte Carlo uncertainty (across particle filter runs) not present in the GLM. The difference may not be statistically meaningful. The paper should either argue this more carefully or acknowledge that the POMP model is approximately competitive with NB regression in raw likelihood, while being penalized by AIC for additional parameters.

### 12. Parameter search design is mislabeled

The design matrix generated by `runif_design(...)` is stored as `profile_design` (line 268), but it is a global search (random uniform) design, not a profile design. The variable name creates confusion with actual profile likelihood computation and contributes to the misrepresentation in Section 2 where the global search scatter is described as a "profile likelihood confidence interval."

### 13. No model diagnostics beyond probes

The diagnostic section (Section 2.2) includes only forward simulations and probes. Missing diagnostics include: (a) effective sample size (ESS) monitoring during particle filtering, (b) conditional log-likelihood plots to identify periods of poor fit, and (c) filtering-distribution simulations (conditioned on observed data) contrasted with unconditioned forward simulations. Per Wheeler et al. (2024), these tools are standard for identifying specific sources of model misspecification.

### 14. Initial conditions are all fixed, not estimated

All initial compartment values (S=23, P=1, R=2, N=1) are fixed constants, not estimated parameters. The paper does not assess sensitivity to these choices. Wheeler et al. (2024) note that initial condition choices affected AIC by ~72 units in one example model. Given the structural issue with S not growing, the choice of initial S is especially consequential and should at minimum be justified or subjected to sensitivity analysis.

### 15. Reproducibility: no RNG seed documentation for the mif2 run

While the global search design is generated with `set.seed(531)`, the parallel `mif2` computation uses `doFuture` and `doRNG` without explicit documentation of which seed or seed strategy was applied to the full parallel computation. The `doRNG` version is recorded in the RDS attributes, but no explicit seed value for the parallel run is set or documented in the Rmd. This limits exact reproducibility. Per Wheeler et al. (2024) and the code supplement checklist, particle filter seeds should be recorded per run.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project01/Level 2.5.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project01/df_dems.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project01/covar.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project01/Makefile`
