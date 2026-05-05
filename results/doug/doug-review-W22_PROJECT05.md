# Peer Review: W22 Project 05
## "An Inquiry into the Effects of Vaccination on COVID-19 Cases using Compartment Models"

---

## Summary

This project attempts to model daily US COVID-19 cases from April 19, 2021 through April 15, 2022 using a SVEIQRD compartment model within the POMP framework, with the stated goal of simulating counterfactual vaccination scenarios. The authors first fit an ARIMA(1,1,2) baseline and an ARMA-GARCH model (which fails to converge), then develop a 7-compartment stochastic POMP model with a time-varying transmission rate to account for Delta and Omicron variants. While the mechanistic model structure is thoughtfully designed and the compartment transitions are biologically motivated, the project suffers from severe computational inadequacy (the IF2 search fails to converge), absence of any profile likelihood or parameter identifiability analysis, no benchmark comparison between the POMP model and a non-mechanistic baseline, no goodness-of-fit quantification, and the stated simulation study goal is never realized. The authors acknowledge convergence failure in the conclusion but proceed to present results as if the model were adequately estimated.

---

## Major Issues

### 1. Complete absence of benchmark comparison

The mechanistic SVEIQRD model is never compared against any non-mechanistic statistical benchmark using a quantitative measure (log-likelihood or AIC). The authors fit an ARIMA(1,1,2) and describe it as inadequate based on visual residual diagnostics and the failure of ARMA-GARCH to converge, but they never compute a comparable log-likelihood for the ARIMA model on the original count scale and compare it to the POMP log-likelihood. Without such a comparison it is impossible to assess whether the SVEIQRD model captures meaningful epidemiological structure beyond what a simple time-series model achieves. Wheeler et al. (2024) emphasize that such comparisons are the single most diagnostic check for mechanistic models, and none of the 32 papers in their Haiti cholera review performed one either — this paper replicates that oversight. The fix is to evaluate the ARIMA model's log-likelihood under the same Gaussian or negative-binomial measurement model on the original data and compute AIC for direct comparison.

### 2. IF2 convergence failure is acknowledged but results are presented regardless

The authors explicitly state (local search diagnostics section): "In the diagnostic plot, the likelihood does not look very stable, waving between -7000 and -5000." and (conclusion): "Given the failure of our model to converge, we are unable to make a definitive simulation study." Despite acknowledging non-convergence, the paper continues to display best-fit parameter tables, simulation plots, and a pairs plot as if these represent valid inference. Non-converged IF2 chains do not yield reliable parameter estimates, log-likelihoods, or simulations — all such downstream results are statistically meaningless without demonstrated convergence. The fix is either to substantially increase computational effort (more particles, more iterations, more replicates) until convergence is achieved, or to restrict claims to the model structure only and not report any parameter estimates.

### 3. Computational effort is grossly inadequate and reporting is incomplete

At run level 1 (the lowest level, triggered when fewer than 8 cores are available) the code uses only 50 particles, 5 IF2 iterations, and 5 evaluation replicates. Even at run level 3 (maximum, 8+ cores), the configuration is 500 particles, 200 iterations, and 40 evaluation replicates. For a 7-parameter epidemiological SEIR-type model fitted to ~360 observations, 500 particles with 200 iterations is marginal; with 14 free parameters (b1, b2, b3, nu, gamma, mu_EI, mu_IQ, kappa, mu_QR, mu_QD, rho, chi, phi, psi), it is likely insufficient. Moreover, the local search is run with only 8 replicates regardless of run level, providing no evidence that multiple independent chains converge to the same region. Wheeler et al. (2024) note that convergence evidence requires "multiple searches from different starting points reaching similar likelihoods." The fix is to run at least 20 local replicates and present a scatter plot of converged log-likelihoods to demonstrate that a stable maximum has been found.

### 4. No profile likelihood or confidence intervals for any parameter

No profile likelihood is computed for any parameter, and no confidence intervals are reported. With 14 free parameters, the model is at risk of severe non-identifiability. The pairs plot of local and global search results is described as "sparse" by the authors themselves, which is a diagnostic signal of identifiability problems. Without profile likelihoods, it is unknown whether b1, b2, b3 (three separate transmission rates), nu (vaccination rate), and gamma (vaccine efficacy) are jointly identifiable from daily case counts alone. Wheeler et al. (2024) specifically flag zero estimated immunity loss rates and zero human-to-human transmission as signals of model misspecification rather than biological truth — this project's parameters could exhibit the same problem. The fix is to compute 95% profile likelihood confidence intervals (using Monte Carlo Adjusted Profile) for at least the three transmission rate parameters and vaccine efficacy gamma.

### 5. The primary research question is never answered

The stated goal is to "simulate different vaccine adoption scenarios" to answer "what if the vaccine rollout post April 19 was faster or slower?" This simulation study is completely absent from the final report. The conclusion explicitly acknowledges this: "Given the failure of our model to converge, we are unable to make a definitive simulation study." The paper therefore fails to address its own research question. This is a fundamental incompleteness in the project.

### 6. Measurement model: dmeasure uses a poorly specified Gaussian with an asymmetric condition

The `model_dmeas` Csnippet defines the likelihood as `lik = dnorm(cases, mean, sd, 0) + tol` but only when `cases <= 10*sd || cases >= -10*sd`. This condition is always true (since `cases >= -10*sd` holds for any non-negative case count and any positive sd), so the outer `else` branch that returns `tol` is dead code. More critically, the measurement model uses a truncated normal approximation to a discrete count process. The model description text says the observation is `round(C_N)^+` where `C_N ~ N(chi*H, (rho*H)^2 + chi*H)`, but the dmeasure evaluates the continuous normal density on discrete count data without correcting for discretization. A standard negative binomial or zero-inflated Poisson measurement model would be more appropriate and statistically principled for daily COVID-19 case counts.

### 7. dmeasure and rmeasure use inconsistent normal parameterizations

The `model_dmeas` Csnippet computes `sd = sqrt(pow(rho*H,2) + chi*H) + tol`, while `model_rmeas` computes `sd = sqrt(pow(rho*H,2) + chi*H + tol)` (the tolerance is inside the square root in rmeasure but outside in dmeasure). This is a minor but genuine discrepancy: in dmeasure, `sd` can equal `tol = 1e-10` when H = 0, which can produce near-zero density values; in rmeasure, `sd` is always positive due to the tol inside the root. While numerically negligible in most cases, this inconsistency means the density evaluation and forward simulation use slightly different standard deviations, undermining the correspondence between the model being estimated and the model being simulated.

### 8. Global search uses run-level-dependent particle counts with no reported level

The code automatically selects run level (1, 2, or 3) based on available cores, but the rendered report never states which run level was actually used during the global search. A reader examining the results cannot determine whether 50 or 500 particles were used, which particles per run level constitutes an order-of-magnitude difference in approximation quality. The reported best global log-likelihood of -5677.496 is presented without any associated Monte Carlo standard error, making it impossible to assess reliability. The fix is to report the run level, the number of particles, and the log-likelihood standard error alongside all reported likelihood values.

### 9. Global search initialization: local search result may be passed to global mif2

The global search code calls `mif2(model, params = c(apply(covid_box, 1, ...)))` where the first argument is `model` (the base pomp object). This is structurally correct. However, the global search box construction for several parameters (N, initial_V, last_week_cases, initial_Q, initial_R, initial_D) uses scalar values rather than two-column ranges. When `apply(covid_box, 1, function(x) runif(1, x[1], x[2]))` is applied to a row with a single value (not two columns), `runif(1, x, x)` returns exactly that value — these fixed parameters are not randomized across replicates. This is appropriate for truly fixed parameters, but the authors do not explicitly acknowledge that these six parameters are being held fixed in the global search. The phi and psi ranges (0.15–0.25 and 0.45–0.55) are also extremely narrow, essentially fixing these initial-condition parameters near their hand-chosen starting values rather than exploring them broadly.

### 10. No model diagnostics beyond convergence traces

The paper presents no conditional log-likelihood plots, no effective sample size plots, no comparison of simulated summary statistics against observed data, and no analysis of reconstructed latent states (S, E, I, V trajectories). The only diagnostic tools employed are the IF2 convergence traces and pairs plots of parameter estimates. Wheeler et al. (2024) demonstrate that conditional log-likelihood plots were essential for discovering model misspecification in the Haiti cholera context. For a COVID model with three distinct transmission regimes (original, Delta, Omicron), per-period conditional log-likelihoods would immediately reveal which regime is responsible for the convergence failure.

---

## Minor Issues

### 11. Compartment model contains a likely typo in E(t) equation

The model equations state `E(t) = E(0) + N_SE(t) + N_SV(t) - N_EI(t)`. Vaccinated individuals (N_SV) should not flow directly into E — they flow from S to V, and from V to E via N_VE. The correct expression should include N_VE (vaccinated individuals who become exposed) rather than N_SV. The Csnippet code correctly implements `E += dN_SE + dN_VE - dN_EI` (line 569), but the mathematical writeup conflates N_SV and N_VE, suggesting a transcription error in the equations.

### 12. S(0) definition is circular

The initial condition definition states `S(0) = N - V(0) - S(0) - E(0) - I(0) - Q(0) - R(0) - D(0)`, which has S(0) appearing on both sides of the equation. This is clearly a typo (the second S(0) on the right side should presumably be 0 or omitted), but it undermines confidence in the mathematical presentation.

### 13. ARIMA model selection ignores weekly seasonality

The ARMA tables grid search uses `season_period = 7` but the authors state "incorporation of seasonal terms were not necessary and caused convergence issues," then proceed to select ARIMA(1,1,2) without seasonal terms. For daily COVID-19 data, weekly reporting cycles are well-documented (fewer tests processed on weekends), and a proper SARIMA(p,1,q)(P,0,Q)[7] model should be considered. The reported AIC table only covers non-seasonal models.

### 14. ARMA-GARCH model failure is treated as evidence of model inadequacy without diagnostic investigation

The paper reports that ARMA-GARCH models produce "non-invertible Hessian matrix" and concludes the approach is inadequate. No investigation is performed into why the Hessian is non-invertible (possible causes: wrong model order, data scaling, poor starting values, boundary estimates). The ARMA-GARCH convergence failure is presented as motivation for POMP, but without diagnosing its cause, the inference that POMP is necessary rather than just the GARCH initialization being poorly specified is unsupported.

### 15. References are formatted inconsistently and contain unprofessional citations

References 16–23 are either Stack Overflow posts, GitHub repository links, or direct links to other student projects from previous semesters (references 17–23 cite five prior-year course projects by URL). Citing other student projects as if they were citable sources is methodologically inappropriate. The code adaptation from prior projects (acknowledged for "global search method" in the text) should instead reference the original pomp package and IF2 methodology papers.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stochastic-dmeas-intermediate/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project05/blinded.Rmd`
