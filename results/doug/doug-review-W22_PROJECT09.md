# Peer Review: W22 Project 09
## Time Series Analysis of COVID-19 Cases in Washtenaw County

---

## Summary

This project applies an SEIR compartmental model with a time-varying contact rate to daily COVID-19 case counts in Washtenaw County, Michigan, from July 2021 to April 2022. The authors divide the time period at the onset of the Omicron variant (December 2021) and estimate two transmission rates, b1 and b2, using iterated filtering (IF2) in the `pomp` framework. A negative binomial and a SARIMA model are presented as non-mechanistic benchmarks. While the project demonstrates familiarity with the pomp workflow and correctly attempts a benchmark comparison, it suffers from a self-diagnosed convergence failure that is not properly acknowledged when downstream results are presented, a fundamentally invalid log-likelihood comparison between the SARIMA and POMP models, a global search initialization error that compromises the claimed global optimization, and several measurement-model and accumulator issues. The SEIR model fails to outperform the SARIMA benchmark, yet the conclusion does not engage seriously with this finding.

---

## Major Issues

### 1. Self-Diagnosed Non-Convergence Used to Draw Substantive Conclusions

In the local search section, the authors explicitly state: "There is fluctuation in the parameters that are not fixed. Additionally, our likelihood does not strictly increase as iterations proceed, which may indicate a problem." The global search traces similarly show poorly converged chains. Despite this explicit acknowledgment of convergence failure, the authors proceed to read off parameter estimates from the results table (interpreting b2 > b1 as evidence of Omicron's higher transmissibility), display simulation trajectories from the "optimal" parameters, and report a best log-likelihood of approximately -1547 as a substantive result. Per the `pomp-self-diagnosed-nonconvergence-audit` skill, every downstream parameter estimate, simulation plot, and model comparison is invalidated by the authors' own diagnosis. The conclusion that "the SEIR model fits the data well" cannot stand when the optimization is acknowledged not to have converged. The remedy is to substantially increase the number of particles, iterations, and search replicates from diverse starting points until convergence is demonstrated by stable log-likelihood traces.

### 2. Global Search Initialized from a Previous mif2 Result Object (Global Search Init Error)

In the `global` code chunk, the global search is launched as `mif1 %>% mif2(params=c(guess, fixed_params))`, where `mf1 <- mifs_local[[1]]` is the first local-search mif2 result object. Per the `pomp-global-search-init-audit` skill, passing a previous mif2 object as the first argument to the global search inherits the cooling schedule and internal IF2 state from the local chain rather than starting fresh from the base pomp object. This anchors the global search near the local-search solution, defeating the purpose of a global box search. The correct pattern is `washtenawSEIR %>% mif2(params=c(guess, fixed_params), ...)`, using the base pomp object. Because the global search is anchored to the local solution, the claimed "global maximum" of approximately -1547 is unreliable and may simply reflect the same local optimum found by the local search.

### 3. Invalid Direct Log-Likelihood Comparison Between SARIMA and SEIR Models

The authors compute a "corrected log-likelihood" of -1308.984 for the SARIMA(3,0,0)x(1,0,1)_7 model by subtracting the sum of log-transformed-plus-one case counts from the ARIMA log-likelihood (to approximately back-transform from the log scale). They then compare this directly to the SEIR model's log-likelihood of approximately -1547, concluding that "the SARIMA model captures the periodic phenomenon which the SEIR model may not take into account." Per the `sarima-baseline-audit` skill, this comparison is invalid: the SARIMA model is fitted to log(y+1)-transformed data under a Gaussian error structure, while the SEIR model is fitted to the original integer count data under a Gaussian measurement approximation (the dmeasure Csnippet uses a normal approximation, not a Poisson or negative binomial). The back-transformation correction is ad hoc and does not produce a comparable likelihood on the original count scale. The two log-likelihoods cannot be numerically compared to draw conclusions about relative model fit. A valid comparison would require both models to be evaluated under the same measurement model on the same data.

### 4. Accumulator Variable Accumulates Recoveries Rather Than New Infections

In the rprocess Csnippet, the accumulator H is updated as `H += dN_IR` (the flow from I to R, representing daily recoveries). The observed data (Cases) records daily confirmed new COVID-19 cases, which correspond to new detections entering the infectious compartment from exposure, not to recoveries. The measurement model then links Cases to rho*H, so rho estimates the ratio of daily confirmed cases to daily recoveries. This is a semantic mismatch: the SEIR model has no quarantine or detection compartment, so new confirmed cases most naturally correspond to new transitions from E to I (dN_EI) or new transitions from S to E (dN_SE), not to dN_IR. Per the `pomp-accumvar-semantic-audit` skill, this mismatch causes rho and mu_IR to absorb offsetting biases. The correct fix is to set `H += dN_EI` (or dN_SE) so that H tracks new infections. This issue, combined with the convergence failure, means that all reported parameter estimates (including the b1 < b2 finding) are unreliable.

### 5. Measurement Model Uses Normal Approximation Without Justification for Count Data

The dmeasure Csnippet implements `lik = pnorm(Cases+0.5, rho*H, sqrt((tau*H)^2 + rho*H), ...) - pnorm(Cases-0.5, ...)`, a normal approximation to the discrete count distribution via continuity correction. The rmeasure Csnippet uses `Cases = rnorm(rho*H, sqrt((tau*H)^2 + rho*H))`. While this Gaussian approximation is arguably defensible for large counts, it is not well-justified here: the dataset includes many small daily counts (especially during the July-November 2021 pre-Omicron period), and the normal approximation can assign non-negligible probability to negative cases. A standard negative binomial measurement model (as used in Wheeler et al. 2024 and the course notes) would be more appropriate and is consistent with the SEIR literature. Furthermore, when H=0 (which occurs when the particle filter collapses), the mean and SD of the normal are both zero, potentially causing numerical issues. The choice of Gaussian approximation is not discussed or justified in the text.

### 6. SARIMA Grid Search Period is Consistent with Data Frequency, but Back-Transformation is Mathematically Unjustified

The SARIMA grid search correctly specifies period=7 for the weekly (actually daily) data with a 7-day seasonal cycle. However, the back-transformation to obtain the "original scale log-likelihood" is computed as `arma30$loglik - sum(log_cases)`, where log_cases = log(1 + data$Cases). This adjustment applies a log-likelihood Jacobian correction for the log(y+1) transformation, but it is only valid if the transformation is exactly log(y) (not log(y+1)) and if the Gaussian assumption applies to the untransformed scale. The +1 offset introduces a non-trivial bias in the Jacobian, and the Gaussian model on log(y+1) does not correspond to any standard distribution on the original count scale. The reported "corrected log-likelihood" of -1308.984 is therefore not a valid quantity on the original observation scale, and the comparison to the SEIR model's log-likelihood is doubly invalid.

### 7. No Profile Likelihoods Computed; Parameter Identifiability Unassessed

No profile likelihoods are computed for any of the estimated parameters (b1, b2, rho, eta, mu_EI, tau). Without profile likelihoods, it is impossible to determine whether any parameter is identifiable from the data. The simultaneous fixing of mu_IR=0.2 without any sensitivity analysis is also unjustified: the recovery rate for COVID-19 varies substantially across populations and periods, and fixing it at an unchosen value may distort estimates of the remaining parameters. Per Wheeler et al. (2024) and POMP checklist item 5, profile likelihoods for key parameters (at minimum b1, b2, and rho) should be presented, with confidence intervals computed via the chi-squared cutoff or MCAP procedure.

### 8. Negative Binomial Benchmark Is Not Time-Resolved; Comparison Is Superficial

The negative binomial benchmark is a stationary model with no temporal structure: `dnbinom(data$Cases, size=exp(theta[1]), prob=exp(theta[2]))`. This treats all observations as i.i.d. draws from a single negative binomial distribution. The log-likelihood of -1652.252 is therefore a lower bound on what a reasonable time-series benchmark would achieve. The SEIR model beating a stationary i.i.d. model proves almost nothing about the model's ability to capture the actual temporal dynamics. Per Wheeler et al. (2024), the appropriate benchmark is a time-series model (e.g., ARIMA or auto-regressive negative binomial) that captures the autocorrelation structure. The SARIMA model (-1308.984, on an incomparable scale) actually beats the SEIR model, and this finding—which is the more diagnostic comparison—receives only a single sentence of discussion without grappling with its implications for model adequacy.

---

## Minor Issues

- **Fixed mu_IR without sensitivity analysis**: mu_IR is fixed at 0.2 (corresponding to a mean infectious period of 5 days) without citation or sensitivity analysis. For the Omicron period, evidence suggests shorter infectious periods. Sensitivity to this value should be reported.

- **Initial conditions inadequately justified**: E=30 and I=30 are described as "intuitive" values. The initial fraction eta (the susceptible fraction) is estimated, but E and I are hardcoded. Per POMP checklist item 13, sensitivity to initial conditions should be assessed, particularly since the data begins in the middle of a wave.

- **No convergence traces for global search**: The authors show convergence traces for the local search but not for the global search. For a claimed global search with 500 starting points, convergence traces from a representative subset of chains should be shown.

- **Simulation plot shows excessive variance without quantitative assessment**: The simulation envelopes from the optimal parameters are described as having "slightly large variance," but no quantitative measure (log-likelihood, coverage of the observed trajectory) is provided. This visual-only assessment is insufficient per Wheeler et al. (2024).

- **Duplicate description of Figure 1 text**: The paragraph "Figure 1 shows a time series plot smoothed by the Loess method..." appears twice in the paper (after Figure 2 in addition to after Figure 1). This appears to be a copy-paste error.

- **covariate_table counts not verified**: The covariate table sets `intervention=0` for the first 154 time points and `intervention=1` for the next 125 time points. The data spans from July 1, 2021 to April 6, 2022, which is 280 days total. 154 + 125 = 279, which is one day short of the 280 observations. This off-by-one discrepancy could cause a silent mismatch at the intervention boundary.

- **No reproducibility information**: No `sessionInfo()` is provided, and the `pomp` package version is not specified. The pomp API has changed across versions; results may not reproduce without version locking.

- **No ESS monitoring reported**: The particle filter effective sample size (ESS) is not reported for any filtering run. Persistent ESS collapse would indicate model-data mismatch or insufficient particles, and its absence from the report makes it impossible to assess filtering quality.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-covid-active-case-stock-flow-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project09/final_proj_531.Rmd`
