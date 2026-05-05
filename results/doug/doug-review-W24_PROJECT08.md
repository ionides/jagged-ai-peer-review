# Peer Review: W24 Project 08
**King County COVID-19 Weekly Cases Analysis**

---

## Summary

This project analyzes weekly COVID-19 case counts in King County, Washington from January 2020 to March 2023 using three progressively complex models: an ARIMA(3,1,3) baseline, a SEIR POMP model, and a custom SVEIPR POMP model that adds vaccination, an asymptomatic compartment (P), and time-varying transmission and vaccination rates. The project demonstrates genuine effort in extending a standard compartmental framework and the SVEIPR model represents an ambitious attempt to capture policy-driven behavioral change through period-specific parameters. However, the work is undermined by a critical data-inconsistency bug (the SEIR model is fitted on Michigan data rather than King County data), a coding error in the reinfection transition, the global search anti-pattern that prevents true global exploration for the SVEIPR model, a substantially worse SVEIPR likelihood compared to SEIR, no benchmark comparison, no profile likelihoods, and a large number of unidentifiable multiplier parameters.

---

## Major Issues

### 1. SEIR Model Fitted on Wrong Dataset (Washtenaw County, Michigan)

The SEIR section contains a silent data-loading bug that invalidates all SEIR results. At line 176, the `sea_data` object is overwritten with:

```r
sea_data = full_data %>% filter(Admin2 == "Washtenaw", Province_State == "Michigan")
```

This loads data for Washtenaw County, Michigan (Ann Arbor area) instead of King County, Washington. The file `seattle_covid.csv` is then overwritten with the Michigan data, and the SEIR model — including both local search (best loglik = -1195.915) and global search (best loglik = -1194.489) — is fitted on this incorrect dataset. The `rm(list=ls())` at the start of the SVEIPR section causes a fresh reload of the correct King County data. As a result, the SEIR and ARIMA models are fitted on different datasets, and all SEIR parameter estimates and model comparisons reported in the paper are for Washtenaw County, not the stated King County target. This constitutes a fundamental validity failure for the entire SEIR analysis.

### 2. SVEIPR Global Search Uses the Anti-Pattern of Initializing from a Previous IF2 Result

At line 868, the code sets `mf1 <- mifs_local[[1]]` and then passes this previous IF2 result as the first argument to `mif2()` in every iteration of the global search loop:

```r
mf1 |> mif2(params = c(guess, fixed_params), Np = 2000, Nmif = 100) |> mif2(Nmif = 100)
```

This is the anti-pattern identified in Wheeler et al. (2024) and described in the `pomp-global-search-init-audit` skill: the global search inherits the cooling schedule from `mifs_local[[1]]`, which has already exhausted its perturbation budget after 200 IF2 iterations. The `params=c(guess, fixed_params)` argument nominally supplies a new starting point, but the cooling schedule inherited from `mf1` is near its final state, leaving very few effective IF2 iterations before perturbations shrink to near zero. The "global" search is therefore anchored near the local-search solution and cannot meaningfully explore the parameter box. The reported best loglik of -1376.675 for the global search may not represent a true global optimum. The fix is to replace `mf1 |> mif2(...)` with `pomp_model |> mif2(...)` in the global search loop.

### 3. SVEIPR Model Has Substantially Worse Likelihood than SEIR Despite Far Greater Complexity

The SVEIPR model achieves a best loglik of -1376.675 (global search), while the SEIR model achieves -1194.489 — a difference of approximately 182 log-likelihood units. Under AIC, the SVEIPR model adds approximately 24 free parameters (b1–b8, c1–c5, mu_SV, mu_EPI, mu_RS, mu_PR, gamma, alpha, tau, rho, eta) compared to SEIR, which would cost 48 AIC units. The net AIC disadvantage for SVEIPR is thus approximately 182×2 − 48 = 316 AIC units relative to SEIR. The paper presents the SVEIPR model as an improvement without acknowledging this stark quantitative inferiority. The authors attribute SVEIPR's better visual fit to "peaks" while ignoring the likelihood comparison. This contradiction must be addressed — either the SEIR fitted on the wrong data inflates its loglik, or SVEIPR is genuinely over-parameterized and under-fits the data. In either case, the comparison must be made honestly on the same dataset.

### 4. Coding Error: dN_RS Reinfection Transition Drawn from I Instead of R

In the SVEIPR `sepir_step` Csnippet (line 599), the reinfection flow from Recovered back to Susceptible is computed as:

```c
double dN_RS = rbinom(I, 1 - exp(-mu_RS * dt));
```

The first argument to `rbinom` should be `R` (the number of individuals at risk of reinfection), not `I`. Using `I` means the reinfection draw depletes from the infected compartment rather than from the recovered compartment. Furthermore, in the state-update block, `R` is incremented by `dN_PR + dN_IR` but is never decremented by `dN_RS`, meaning recovered individuals are never actually removed when reinfection occurs — only susceptibles are augmented. This coding error makes the reinfection mechanism internally inconsistent: the number of reinfections is drawn from the wrong pool, and the R compartment does not conserve mass. All results based on the SVEIPR model are affected by this bug.

### 5. No Benchmark Comparison Against a Non-Mechanistic Model

Neither the SEIR nor the SVEIPR model is compared against a non-mechanistic statistical benchmark (e.g., an auto-regressive negative binomial, or the ARIMA model fitted on the same data). While an ARIMA(3,1,3) is fitted, it is never compared to the POMP models quantitatively. Wheeler et al. (2024) demonstrate that mechanistic models that look visually reasonable can fail to beat simple benchmarks; without such a comparison it is impossible to assess whether the POMP models capture structure beyond what the ARIMA baseline already provides. The ARIMA log-likelihood should be reported and compared to the mechanistic model likelihoods on a common data and observation-model basis.

### 6. Parameter Identifiability Crisis: c4, b4, and Related Multipliers Are Unidentifiable

Inspection of the global search results shows severe non-identifiability among the period-specific multiplier parameters. The parameter `c4` (vaccination-rate multiplier for period 4) takes values ranging from 0.28 to 316.9 across runs within 10 loglik units of the MLE, with the best-fit value being 207.7. The parameters `b7` and `b8` (transmission multipliers for the Omicron period) range from 2.3 to 403.8 and 2.1 to 75.8 respectively at the same cutoff. These ranges are orders of magnitude wide with nearly flat likelihood, indicating that these parameters are not identified by the data. Profile likelihoods are not computed for any parameter, so no formal identifiability assessment is presented. Wheeler et al. (2024) emphasize that implausible or unconstrained parameter estimates should be interpreted as evidence of model misspecification rather than biological findings.

### 7. H Accumulator Only Tracks I→R Transitions, Excluding P→R

The SVEIPR model introduces a "P" (potentially infected, i.e., mildly symptomatic or asymptomatic) compartment as a distinct infectious stage. However, the accumulator variable H, which is linked to the reported cases via the measurement model, only accumulates transitions from I to R:

```c
H += dN_IR;
```

No contribution from P→R (`dN_PR`) is added to H. If the P compartment represents mildly symptomatic individuals who are also detected in surveillance, this omission underestimates the link between the model and the observed count data. Conversely, if only I→R cases are meant to be reported, the interpretation of the I compartment relative to P needs to be clarified in the text. The current setup is inconsistent with the stated purpose of the P compartment.

### 8. SEIR Global Search: 67 of 100 Runs Return NA Log-Likelihoods

The saved SEIR global search results (`seir_global.rds`) show that 67 of the 100 random starting points produced NA log-likelihoods, with 8 additional runs yielding log-likelihoods worse than -10,000. Only 33 runs produced finite, plausible results. This severe particle degeneracy — likely caused by the wide parameter box (Beta upper = 1000, which is physically implausible for weekly transmission) — means that the SEIR global search effectively explored only a small fraction of the intended parameter space. The paper does not report this degeneracy rate, leaving readers with a false impression of the global search's coverage. The box bounds should be scientifically motivated, and the degeneracy rate should be reported.

---

## Minor Issues

### 9. ARIMA Model Applied to Already-Differenced Data, Creating Double-Differencing

The data are first differenced in preprocessing (line 31: `differences <- diff(selected_observations)`), and then an `arima()` model with `order=c(3,1,3)` applies an additional difference internally. The result is ARIMA(3,1,3) fitted to already-differenced data, which is equivalent to fitting an ARIMA(3,2,3) on the original cumulative case counts. The text conflates the differencing steps and describes this incorrectly. The model selection table caption says "AIC Table for ARIMA Model" but the underlying data is already differenced weekly counts; the model order interpretation is confused throughout.

### 10. SVEIPR Measurement Model Uses Gaussian Approximation with No Justification

The SVEIPR `dmeas` Csnippet approximates the observation distribution with a discretized normal:

```c
double mean = rho * H;
double sd = sqrt(pow(tau * H, 2) + rho * H);
lik = pnorm(reports + 0.5, mean, sd, 1, 0) - pnorm(reports - 0.5, mean, sd, 1, 0);
```

This normal approximation is not motivated in the text, and no justification is provided for why it is preferable to a negative binomial measurement model (used in the SEIR submodel). Wheeler et al. (2024) recommend overdispersed count distributions (negative binomial) rather than Gaussian approximations for infectious disease case count data. The inconsistency between the SEIR measurement model (negative binomial, line 213) and the SVEIPR measurement model (Gaussian approximation) is not acknowledged.

### 11. Very High Loglik Standard Errors in SEIR Local Search Indicate Insufficient Particles

The SEIR local search evaluates log-likelihoods using `Np=2000` particles with 10 replicates. The saved `local_logliks.rds` shows loglik.se values up to 10.69 and a mean of 3.94. Standard errors above 1 log-likelihood unit indicate that the particle filter estimates are too noisy for reliable comparison and optimization; values above 2-3 units suggest serious particle degeneracy. The text does not report these standard errors or acknowledge the imprecision. For the SVEIPR model the standard errors are below 0.05, which is acceptable; the SEIR model's high standard errors may reflect the wrong-dataset bug (the Michigan data may differ in scale from what the parameter values expect).

### 12. Several Key Parameters Fixed Without Justification in SVEIPR Global Search

The SVEIPR global search fixes seven parameters: `Beta=1.01`, `mu_PR=0.93`, `mu_IR=0.98`, `mu_RS=0.5`, `alpha=0.4`, `N=2269675`, `mu_SV=0.5`. Of these, `mu_PR`, `mu_IR`, `mu_RS`, and `alpha` are biologically important: the recovery rates and the fraction routing through the asymptomatic pathway directly affect the epidemic dynamics. Fixing these at initial guesses without sensitivity analysis or likelihood-based justification may prevent the optimizer from finding a better fit and biases all reported estimates. No biological references are provided to justify these fixed values.

### 13. Poor Man's Profile Likelihood Used Instead of Proper Profile

The paper reports confidence intervals for gamma and eta by examining the range of values among global search runs with loglik above a threshold ("poor man's profile likelihood confidence interval"). This approach does not produce statistically valid confidence intervals: the set of runs that happen to have high loglik in a grid search is not equivalent to a profile likelihood. Genuine profile likelihood computation requires fixing each parameter at a grid of values and re-optimizing all remaining parameters at each grid point. Without proper profiles, the reported intervals for gamma and eta have no formal coverage guarantee.

### 14. Lack of Model Diagnostics (Conditional Log-Likelihoods, ESS Monitoring)

The paper does not present any model diagnostics beyond visual simulation overlays. Wheeler et al. (2024) recommend plotting conditional log-likelihoods over time to identify periods of poor fit, and monitoring effective sample size (ESS) during filtering. While the text mentions that "ESS around local peaks approaches 0," this is not formally documented with an ESS plot from the best-fit parameter values. Conditional log-likelihood plots would help identify whether the model fails specifically during the Omicron wave and would guide model refinement.

### 15. No Forecast or Policy Recommendation Despite Stated Goal

The introduction explicitly states that the goal is to "predict the number of infections in the future" and "give suggestions to government on making public policies." The paper contains no forecast, no out-of-sample evaluation, and no policy recommendations. The conclusion discusses model fit but makes no forward-looking claims. If forecasting was infeasible given the model's limitations, this should be acknowledged as a limitation; if it remains a goal, at minimum a discussion of how forecasts would be generated from the filtering distribution (Wheeler et al. 2024, Section on Forecasts) should be included.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/SVEIPR_results_run_level_3/lik_global_run_level_3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/SVEIPR_results_run_level_3/lik_local_run_level_3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/SVEIPR_results_run_level_3/global_search_run_level_3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/seir_global.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/local_logliks.rds`
