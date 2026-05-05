# Peer Review: W21 Project 13
## "An Investigation into COVID-19 in California"

---

## Summary

This paper fits an ARIMA(4,1,3) model and a seven-compartment SEAPIRD POMP model to daily COVID-19 case counts in California from January 2020 to April 2021. The SEAPIRD model extends the standard SEIR framework by adding asymptomatic (A) and presymptomatic (P) compartments and six time-varying intervention scalars on the transmission rate. The paper is a genuine effort to fit a mechanistic model to a complex epidemic, and the use of intervention covariates is conceptually motivated. However, the analysis suffers from several serious methodological flaws: the ARIMA-POMP log-likelihood comparison is statistically invalid, the accumulator variable tracks recoveries rather than incident cases (mismatching the observation data), the global and local searches are far too sparse to identify the MLE reliably, no profile likelihoods are computed, and several ODE equations in the text contain notation errors. The conclusion that the POMP model outperforms ARIMA due to a higher log-likelihood is not supported by the analysis as conducted.

---

## Major Issues

### 1. Invalid direct comparison of ARIMA and POMP log-likelihoods

The paper compares the ARIMA(4,1,3) log-likelihood (-4091) to the POMP model log-likelihood (-3792) and concludes that the POMP model "performed better" (Conclusion section). This comparison is statistically invalid for two reasons:

- The ARIMA likelihood is evaluated under a Gaussian distribution on first-differenced data, while the POMP likelihood is evaluated under a Normal measurement model on the original daily case counts. The two likelihoods are not on the same scale and cannot be directly compared.
- The ARIMA model uses 7 parameters, while the SEAPIRD model uses 16. Even if the observation models were comparable, AIC or a penalized criterion must be used rather than raw log-likelihood.

The paper acknowledges the difference in parameter counts in passing ("The arima model had a log likelihood of -4091 using 7 parameters") but draws the comparison anyway. See Wheeler et al. (2024) §Model comparison for best practices on benchmark comparisons. Fix: compare the models using AIC, or evaluate both on the same untransformed data under the same observation model (e.g., a Gaussian approximation to the raw case counts for both).

### 2. Accumulator variable H tracks recoveries, not incident cases

The rprocess Csnippet accumulates `H += dN_IR + dN_AR` — that is, transitions from I to R plus transitions from A to R. The measurement model then links observed *cases* to `rho * H`. However, `dN_IR + dN_AR` represents recovered individuals, not newly confirmed (detected) infections. The California CDC surveillance data used here records *newly reported confirmed cases*, which correspond to incident infections entering the symptomatic compartment I (or a detection event), not recoveries. Linking cases to recoveries causes the reporting rate `rho` to absorb the ratio of recoveries to infections per time step, which is a biologically meaningless quantity. This is a systematic model misspecification that distorts all parameter estimates. Fix: accumulate `H += dN_PI` (new entries into the symptomatic infected compartment I from P), which corresponds to newly symptomatic and thus newly confirmable cases.

### 3. Computational inadequacy: only 8 search replicates

Both the local search (chunk `lik_local.rds`) and global search (chunk `mifs_global.rds`) use only 8 parallel IF2 replicates (`foreach(i=1:8, ...)`). Wheeler et al. (2024) and standard practice recommend at minimum 20–50 replicates for a model with 16 parameters, and many more for difficult surfaces. With 8 replicates, there is insufficient diversity to identify whether the optimization has converged to the global MLE or a local optimum. The convergence diagnostic (pairs plot) shows parameter scatter but with only 8 points it cannot distinguish convergence from coincidence. Fix: increase both searches to at least 20 replicates, and preferably run a second-stage global search from a tighter box around the best solutions found in the first pass.

### 4. No profile likelihoods — parameter identifiability not assessed

No profile likelihoods are computed for any parameter. With 16 estimated parameters (Beta, six intervention scalars c_1–c_6, five transition rates, alpha, rho, tau) and a complex model, unidentifiability is a serious concern. In particular, the intervention scalars c_1–c_6 and Beta are collinear — only their products matter for the force of infection, so there is likely a ridge in the likelihood surface along constant `Beta * c_i`. The pairs plot hints at this (the cluster of red points), but without profiles the claim that the global search "appears to converge" (Fit Analysis section) is unsupported. Fix: compute profile likelihoods for at least Beta, rho, alpha, and one representative intervention scalar. See Wheeler et al. (2024) §Parameter identifiability.

### 5. ODE equation notation errors in the text

The mathematical description of the model (Section 2.2) lists transition rates using the destination compartment rather than the source:

- `dN_PI/dt = mu_PI * R_t` — should be `mu_PI * P_t` (rate of transfer from P)
- `dN_IR/dt = mu_IR * R_t` — should be `mu_IR * I_t`
- `dN_ID/dt = mu_ID * D_t` — should be `mu_ID * I_t`
- `dN_AR/dt = mu_AR * R_t` — should be `mu_AR * A_t`

The Csnippet code is correct (e.g., `rbinom(P, 1 - exp(-mu_PI * dt))`), so this is a presentation error, but it demonstrates confusion in the model description and would mislead a reader trying to understand the model structure. Fix: correct the differential equation text to use the source compartment.

### 6. Global search box for rho allows values outside (0, 1) on the natural scale

The global search box specifies `rho = c(0, 2)` (`covid_box` definition). Since `rho` has a logit transformation declared in `partrans`, IF2 operates on the logit-transformed scale. However, the starting parameters are drawn as `runif(1, 0, 2)` on the natural scale and then passed to mif2, which means starting values of rho > 1 (e.g., rho = 1.5) are illegal probability values. While the logit transform would convert valid starting points, a starting value of rho = 1.5 has no valid logit representation (logit is only defined on (0, 1)). This can cause the global search to crash or to silently treat boundary-violating starting points in undefined ways. Fix: restrict the box to `rho = c(0.001, 0.999)` to ensure all starting values are valid probabilities.

### 7. No model diagnostics reported

The paper presents three convergence plots (referenced as external PNG files) and states "it appears the POMP model has converged" (Section 2.2.4), but provides no:
- Conditional log-likelihood plot (per-observation log-likelihood over time, used to identify periods of poor fit)
- Effective sample size (ESS) over the particle filter run
- Comparison of filtering distribution trajectories to forward simulations
- Summary statistics comparing simulated datasets to observed data

Without these diagnostics, there is no basis for the convergence claim, and there is no assessment of where or how the model fails to fit the data. Wheeler et al. (2024) §Model diagnostics describes these as essential for published POMP analyses.

### 8. Fixed and implausible initial conditions

The model fixes initial conditions as `I_0 = 250` (hardcoded in `seapird_init`) and `S_0 = N = 39,512,223`. These are not estimated as parameters. The choice of I_0 = 250 is not justified with reference to surveillance data or literature, and given the sensitivity of epidemic trajectories to initial conditions, this could substantially affect parameter estimates. More critically, fixing S_0 = N assumes the entire California population is susceptible on day 1 (January 22, 2020), which is plausible but not verified. Fix: treat I_0 as a free parameter estimated via MLE, and assess sensitivity of results to the initial conditions.

### 9. Measurement model inconsistency between rmeasure and dmeasure

The `rmeas` Csnippet computes `cases = rnorm(rho * H, sqrt(tau * rho * H * (1 - rho))) + D`, while the `dmeas` Csnippet evaluates `dnorm(cases - deaths, rho * H, sqrt(tau * rho * H * (1 - rho)))`. The two are equivalent only if `deaths = D` in the data at every time step (since D in the state is the cumulative death count, not period deaths). The `rmeas` adds `D` to the simulated cases as a whole-epidemic cumulative, while `dmeas` subtracts the observed death *count* (which is a different daily or period quantity depending on how the data is structured). If `deaths` in the data is a daily death count but `D` in the state is cumulative, the measurement model is inconsistent between simulation and evaluation. Fix: clarify whether D is a period accumulator or a cumulative state, and ensure the add/subtract in rmeas and dmeas use the same quantity.

---

## Minor Issues

- **Typo in file names**: The code reads `local_results_greaklakes.csv` (note the typo "greaklakes" instead of "greatlakes"). This suggests the file was generated with this misspelling, which would cause a read error if the file were renamed. Minor but should be corrected.

- **Spectral analysis conclusion**: The spectrum analysis identifies a 150-day cycle as "dominant frequency." The authors correctly note that 442 days of data is insufficient to confirm seasonality, but the entire spectrum analysis section is then disconnected from the modeling — there is no seasonal component in either the ARIMA or POMP model despite the spectral finding.

- **Model Assumption 1 placeholder text**: Section 2.2.1, Assumption 1 reads "We assume lockdown measures across California from x-x and x-x scales the force of the invention coefficient..." — the time intervals are left as "x-x", suggesting this text was not completed before submission.

- **ACF interpretation**: The paper states "less than 95% of lags fall outside the band, we would not reject the null hypothesis that residuals are IID." This phrasing is backwards: Ljung-Box/visual ACF convention flags residuals as non-IID when *more than* 5% of lags exceed the band. However, the two significant lags (6 and 22) out of many shown do suggest near-IID behavior, so the substantive conclusion is correct if accidentally so.

- **ARIMA model diagnostic**: The paper notes that one inverse AR root and some inverse MA and AR roots are at the edge of the unit circle, suggesting a smaller model, but proceeds with ARIMA(4,1,3) regardless. The failure to investigate simpler models (e.g., the near-cancellation of AR and MA roots) leaves model selection incomplete.

- **Forecast methodology absent**: The paper makes no forecasts from the fitted POMP model. While not strictly required, the analysis would benefit from at least a one-step-ahead simulation from the filtering distribution to demonstrate the model's predictive utility. As stated in Wheeler et al. (2024) §Forecast methodology, stochastic POMP models have a natural advantage in forecasting via the filtering distribution.

- **No uncertainty quantification**: Point estimates are reported for all parameters (best row from the global search), but no confidence intervals, credible intervals, or bootstrap estimates are provided for any parameter. This makes the parameter estimates uninterpretable scientifically.

- **Reproducibility**: The analysis uses `bake()` caching with files `lik_local.rds`, `local_results.rds`, `mifs_global.rds` (implied), and `global_search.rds`. These files are present in the submitted folder, which is good. However, no `set.seed()` is called before the parallel searches, making exact reproduction across machines impossible.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-design-variable-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/ode-compartment-observation-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/hp-filter-lambda-misspecification/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-mc-noise-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project13/blinded.Rmd`
