# Peer Review: W22 Project 12
## Modeling COVID-19 Cases in Michigan (SEIR POMP + ARIMA)

---

## Summary

This project models daily COVID-19 case counts in Michigan across two time periods: the full pandemic record (March 2020–April 2022) and the Omicron wave specifically (December 2021–April 2022). The authors fit ARIMA models to both windows and then build a stochastic SEIR POMP model for the Omicron wave, using a time-varying transmission rate (beta0/beta1) that shifts at a hard-coded breakpoint, and a Gaussian measurement model with overdispersion. A local IF2 search (20 chains, 50 iterations, 1000 particles) is followed by a global box search (400 starting points). The approach is reasonable in structure, and the authors sensibly restrict the POMP analysis to the single-variant Omicron period to avoid multi-variant complexity. However, the analysis contains several significant methodological and implementation errors that undermine the reliability of the reported parameter estimates and the validity of the global search, and it lacks benchmark comparison, profile likelihoods, and model diagnostics required to support the conclusions.

**Key strengths:** Likelihood-based inference via IF2 and particle filters is used; overdispersion is modeled; the motivation for focusing on the Omicron wave is clearly articulated; log-likelihood values are reported; the MLE parameters in the text match the saved artifact exactly.

**Key weaknesses:** Global search is initialized from a previous mif2 result (anti-pattern); the global search box excludes the MLE for at least one parameter (beta1); rho concentrates at the boundary; no profile likelihoods; no benchmark comparison; the dmeasure and rmeasure use different variance formulas; the accumulator H tracks recoveries (I→R) rather than new infections, which may not match reported-case data; the ARIMA section does not serve as a proper quantitative benchmark for the POMP model.

---

## Major Issues

### 1. Global search initialized from a previous mif2 result, not the base pomp object

In the global search code block, the first argument to `mif2()` is `mf1 <- mifs_local[[1]]` — a previously fitted mif2 chain from the local search — rather than the base `covidSEIR` pomp object. This is the canonical global-search-init-audit anti-pattern: the global search replicates inherit the cooling schedule of the already-converged local chain. Because the cooling schedule of `mf1` is at or near its terminal state after 50 iterations, the perturbations shrink to near zero almost immediately for every global replicate, regardless of the new random starting point drawn from the box. The global search is therefore effectively 400 copies of a local perturbation around the local-search MLE, not a genuine exploration of the full parameter box.

The fix is to replace `mf1` with `covidSEIR` (the original pomp object) as the first argument to every `mif2()` call inside the global search loop, while still passing the random `params=c(unlist(guess), fixed_params)` to set the starting point. This ensures each replicate begins from a fresh cooling schedule.

### 2. MLE for beta1 lies outside the global search box (binding box constraint)

The global search box sets beta1 in [0.15, 0.30], but the best-fit value recovered from the global search artifact is beta1 = 0.313 — outside the upper bound. Inspection of the global search artifact (global_search_.rds) confirms that 146 of the 400 runs have beta1 > 0.3, with values reaching 0.593. The MLE at 0.313 is therefore a constrained optimum produced by the optimizer drifting past the box boundary in the second mif2 call (which has no re-draw from the box). The true unconstrained MLE for beta1 may be higher, meaning the reported log-likelihood of -1155 is itself a lower bound on the achievable likelihood. The authors should extend the beta1 upper bound, re-run the global search with the corrected initialization (Issue 1 above), and verify that the new MLE is interior to the extended box.

### 3. Reporting rate rho concentrates at the boundary (rho → 1)

The global search box sets rho in [0.8, 1.0]. The best-fit rho = 0.995 is within 0.5% of the upper bound. Among the top 10 global search results, 9 have rho > 0.97. This suggests the data support rho = 1 (all cases are reported) or that the measurement model is misspecified: the overdispersion parameter psi is absorbing variance that a lower rho should be absorbing, and the optimizer pushes rho to its upper limit in compensation. An estimated rho near 1 is scientifically implausible for COVID-19 case reporting, where substantial under-reporting is well documented. The authors acknowledge lack of convergence in rho and psi but do not connect this to the boundary issue or consider whether the measurement model is misspecified. Profile likelihoods for rho are required to determine whether rho is truly unidentifiable or constrained artificially.

### 4. dmeasure and rmeasure use inconsistent variance formulas

The dmeasure Csnippet computes `sd = sqrt(pow(psi * H, 2) + rho * H)`, while the rmeasure Csnippet computes `sd = sqrt(pow(psi * rho * H, 2) + rho * (1 - rho) * H)`. The text states the measurement model as `N(rho * H, rho*(1-rho)*H + (psi*rho*H)^2)`, which matches the rmeasure formula. The dmeasure formula uses `psi * H` instead of `psi * rho * H` in the overdispersion term. At the MLE (rho ≈ 0.995), the difference is negligible numerically (ratio ≈ 1.005 at all tested H values); however, the discrepancy means the likelihood evaluated by the particle filter does not match the stated mathematical model. More importantly, at different values of rho (e.g., early iterations with rho ≈ 0.5), the ratio is approximately `1/rho = 2`, producing a factor-of-2 difference in the overdispersion standard deviation between the two snippets. This is the pomp-dmeas-rmeas-moment-mismatch pattern: the particle weights are computed under a different measurement model than the one used for simulation. The dmeasure formula should be corrected to use `psi * rho * H` consistently with the text and rmeasure.

### 5. No benchmark comparison between the SEIR model and a non-mechanistic baseline

The ARIMA models fitted in the first section are not used as quantitative benchmarks for the SEIR model. The ARIMA log-likelihoods are evaluated under a Gaussian distribution on differenced data, while the SEIR model uses a Gaussian-approximation overdispersed count model on the original scale; the two log-likelihoods are not directly comparable. The paper concludes that the SEIR model is "much more explanatory" than ARIMA without any valid quantitative basis for this claim. Wheeler et al. (2024) identify benchmark comparison as a foundational practice: a non-mechanistic auto-regressive model fitted under the same observation model and data scale is required to establish whether the SEIR model captures meaningful structure beyond what a simple statistical model achieves. Without such a comparison, the claim of superior explanatory power is unsupported.

### 6. No profile likelihoods; parameter identifiability unassessed

No profile likelihoods are computed for any parameter. The pairs plot of global search results (Figure 18) shows a clear lack of convergence in rho and psi — the authors note this — but do not compute profile likelihoods to determine whether these parameters are identifiable. Given that rho is pinned near 1 and the text acknowledges that psi is also poorly constrained, the pair (rho, psi) may be jointly unidentifiable in this model: both can be varied jointly along a ridge of nearly equal likelihood. Profile likelihoods for at least rho and psi are required to assess identifiability and to support any confidence statements about parameter estimates. Per Wheeler et al. (2024), unidentifiable parameters may indicate model misspecification rather than data limitations.

### 7. Accumulator variable H tracks recoveries, not new detected cases

The Csnippet accumulates `H += dN_IR` (the flow from I to R), but the observation data records new confirmed COVID-19 cases. In the SEIR framework, a newly confirmed case corresponds to a person who has been detected — typically associated with the E→I transition (when they become symptomatic and test positive) rather than the I→R transition (recovery). Tracking recoveries in H forces the measurement model to link reporting-rate rho to the ratio of detected cases to recoveries per time step, rather than to the true detection rate. This will bias rho and any parameter that compensates for the mismatch. The standard SEIR accumulator for case counts should accumulate `dN_EI` or, if the model represents clinical confirmation, a separately modeled detection event. The authors should clarify what biological event the data records and verify that H accumulates the matching flow.

---

## Minor Issues

### 8. Hard-coded breakpoint for beta transition (t > 33) without justification or sensitivity analysis

The transmission rate shifts from beta0 to beta1 at time t = 33 (approximately January 2, 2022, counting from December 1, 2021), implemented as a hard-coded threshold in the Csnippet. No justification is given for why t = 33 was chosen as the breakpoint. This is not estimated from the data and no sensitivity analysis is presented for alternative breakpoints. At minimum, the authors should explain how t = 33 was determined and note it as a model assumption. A more rigorous treatment would either estimate the breakpoint as a parameter or fit models with several candidate breakpoints and compare via AIC.

### 9. Stationarity test conclusion is incorrectly framed

The ARIMA section applies the Augmented Dickey-Fuller (ADF) test and states that "the test result shows the rationality of using d=1." The ADF null hypothesis is the presence of a unit root (non-stationarity); a small p-value rejects the unit root, indicating stationarity — which would argue against differencing. The test is applied to the differenced series (case_diff), and rejection of the unit-root null on the differenced series supports that d=1 is sufficient (the differenced series is stationary), not that differencing is necessary in the first place. The prose should explicitly state what the test is testing and what the rejection implies. Additionally, only a single stationarity test is used; a KPSS test for corroboration is missing (per best practice).

### 10. AIC table caption mislabels Figure 10 description

The text above Figure 10 states "The result is shown in Figure # below" — the figure number was not filled in before submission. This is a proofreading error.

### 11. Particle filter standard error is large at initial parameter values

The initial particle filter evaluation reports a log-likelihood estimate of -1644.5 with a standard error of 4.77. A SE of 4.77 on a log-likelihood estimate is very large: it means the particle filter estimate is highly variable and 95% confidence intervals on the log-likelihood span roughly ±9 units. This indicates the initial parameter values place the model in a region of poor fit where the particle filter is struggling. While this improves dramatically near the MLE (SE = 0.025 at the global search best), the authors should note that Np = 1000 was insufficient at starting values and could be increased for stability across more of the parameter space.

### 12. ARIMA model is fitted to the full dataset and the Omicron subset using the same model order without discussion

The same ARIMA(5,1,5) specification is selected for both the full dataset (March 2020–April 2022) and the Omicron subset (December 2021–April 2022) based on AIC tables. The fact that the same orders emerge from both AIC tables is noted without comment. This coincidence deserves discussion: the Omicron data covers only ~135 days, and fitting a 10-parameter ARIMA(5,1,5) to ~135 observations risks overfitting. The residual diagnostics (Figures 11, 13) both show remaining autocorrelation, which is correctly identified but not resolved.

### 13. No model diagnostics beyond the pairs scatter plot

No conditional log-likelihood plots, effective sample size traces beyond the initial check, or filtering-distribution comparisons are presented. The particle filter check (Figure 15) shows ESS appears "adequate almost everywhere" but no specific values are cited and the ESS is only checked at the initial starting values, not at the MLE. Wheeler et al. (2024) recommend plotting conditional log-likelihoods to identify specific time periods of poor fit — this is especially important here because the weekly reporting artifact creates systematic periods of very high and very low case counts.

### 14. mu_EI and mu_IR are fixed throughout without sensitivity analysis

The exposure-to-infectious rate (mu_EI = 0.33) and the infectious-to-recovered rate (mu_IR = 0.14) are fixed as constants and never estimated. While fixing them simplifies the search, these rates interact with beta in determining R0, and the fixed values are justified only by citing their expected ranges for Omicron. No sensitivity analysis explores how the MLE for beta and rho changes if mu_EI or mu_IR vary within their plausible ranges. A minimum treatment would note the sensitivity of R0 to these assumptions.

### 15. No forecast or prediction from the fitted model; conclusions are primarily descriptive

The paper does not generate probabilistic forecasts from the fitted SEIR model despite having a fully fitted model. The conclusion that the SEIR model "seems reasonable" is supported only by visual overlay of 10 simulations on the data (Figure 17). Generating predictions from the filtering distribution (conditioning on observed data through April 2022 and simulating forward) would demonstrate the practical utility of the model and is a standard deliverable for applied POMP models. Per Wheeler et al. (2024) §7, forecasts should be conditioned on the filtering distribution rather than initial conditions.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-boundary-mle/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-moment-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/global_search_.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/lik_local.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project12/writeup_local_search.rds`
