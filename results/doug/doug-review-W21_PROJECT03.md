# Peer Review: W21 Project 03
## "Investigation of Vaccination Effect on Covid-19 in California"

---

## Summary

This project investigates the effect of COVID-19 vaccination on case counts in California (January–April 2021) using three progressively complex compartmental models: a basic SIR, a first SIRV model (estimated vaccination rate), and a second SIRV model (externally calibrated vaccination rate using a quadratic fit). The authors apply IF2 via `mif2()` for likelihood-based inference, which is the appropriate approach. The project is motivated by a substantive epidemiological question and represents a genuine attempt to use mechanistic POMP modeling. However, the analysis is compromised by a critical accumulator variable semantic mismatch that is present in all three models, by a global search initialization anti-pattern that prevents genuine global coverage, by insufficient computational effort, by a prediction step that uses the wrong parameter vector, and by the absence of any non-mechanistic benchmark comparison. These issues collectively undermine the validity of all reported parameter estimates, model comparisons, and the pandemic "end date" forecast.

---

## Major Issues

### 1. Accumulator variable H tracks recoveries, not new infections (all three models)

In all three rprocess step functions, the accumulator variable H is updated as `H <- H + dN_IR`, which accumulates the I→R (recovery) flow. However, the observed data column `New_Report` represents newly confirmed (detected) COVID-19 cases — new infections entering the I compartment from S, i.e., `dN_SI`. The measurement model `dbinom(x=New_Report, size=H, prob=rho, log=log)` therefore links reported new cases to recoveries, not infections. These two quantities have completely different dynamics: recoveries lag infections by roughly the infectious period, and their ratio (dN_IR/dN_SI) over a short interval is not a fixed reporting fraction. The reporting rate parameter `rho` will be estimated to compensate for this mismatch, producing biologically meaningless estimates. All three models share this error.

The fix is to change `H <- H + dN_IR` to `H <- H + dN_SI` in each step function, so that the accumulator tracks new infections. This is also consistent with the standard SIR POMP model formulation in which new daily cases are proportional to new S→I transitions, not I→R transitions. (See Wheeler et al. 2024, §Measurement model specification; see also POMP course lecture notes.)

### 2. Global search initialized from previous mif2 result, not the base pomp object

In all three global searches, the code sets `mf1 <- mifs_local[[1]]` and then calls `mf1 %>% mif2(params=c(unlist(guess), fixed_params)) %>% mif2(Nmif=options_Nmif)`. Passing a previous mif2 result object as the first argument to `mif2()` causes the new call to inherit the internal IF2 state — specifically the cooling schedule — from the local search chain. By the time `mifs_local[[1]]` was constructed, its cooling schedule had already decayed to near its minimum. The subsequent global search therefore applies near-zero perturbations from the first iteration, effectively preventing exploration of the box. The claimed "global search" is in fact 100 copies of a locally perturbed search anchored near the local-search solution. Any statement that the global search found a "global maximum" is unsupported by the code.

The fix is to replace `mf1 %>% mif2(params=c(unlist(guess), fixed_params))` with `covidSIRV2 %>% mif2(params=c(unlist(guess), fixed_params), Np=options_Np, Nmif=options_Nmif, ...)` (using the base pomp object as the first argument). This applies equally to all three model sections. (See Wheeler et al. 2024, §Computational adequacy.)

### 3. Prediction step uses initial manual parameter guess, not the MLE

At the prediction stage, the code correctly extracts the MLE: `params_maxlik = unlist(results_global[which.max(results_global$loglik),])`. However, the forward simulation for the pandemic-end forecast uses `params=params`, which is the manually specified initial guess `c(Beta=0.01, Sigma=0.01, mu_IR=0.04, mu_VR=0.9, rho=0.3, eta=0.9, N=N)` defined in the simulation chunk, not `params=params_maxlik`. The forecast trajectories therefore reflect the authors' initial guess about parameter values, not the likelihood-maximizing estimates. The conclusion that "the pandemic will end before July 2021" has no valid statistical grounding.

The fix is to replace `params=params` with `params=params_maxlik[paramnames(covidSIRV2)]` in the simulate call used for forecasting. The `params_maxlik` vector likely includes `loglik` and `loglik.se` columns that must be stripped before passing to simulate.

### 4. Grossly insufficient computational effort (run_level = 1 throughout)

The document sets `run_level = 1` throughout, which corresponds to `Np=100`, `Nmif=10`, `Neval=2`, `Nglobal=10`, `Nlocal=10`. For an epidemic model with 87 observations, 100 particles is far below what is needed for a stable particle filter likelihood estimate. At `Np=100`, particle degeneracy is likely at almost every observation time step. With `Nmif=10` iterations, the IF2 algorithm has barely begun to explore the likelihood surface. The local search log-likelihood single-evaluation uses `logmeanexp` over a single pfilter call (`logmeanexp` of one value is just that value), providing no Monte Carlo averaging. All reported log-likelihoods, parameter estimates, and profile likelihood results are computed from a test-level run that is not suitable for scientific conclusions. The production run levels (run_level=2 or 3) would require `Np=1000–5000` and `Nmif=100–200`. (See Wheeler et al. 2024, §Computational adequacy.)

### 5. No non-mechanistic benchmark comparison

None of the three mechanistic models is compared against a non-mechanistic statistical benchmark (e.g., ARMA, auto-regressive negative binomial, or even a simple regression on a time trend). Without such a comparison, it is impossible to assess whether the mechanistic models capture meaningful structure beyond what a purely statistical model would achieve. The text dismisses the SIR model on the basis of non-convergence of the pairs plot, and moves to the SIRV models, but never quantifies whether any model outperforms a simple benchmark. The claim that vaccination is effective because sigma is small cannot be validated without such a comparison. (See Wheeler et al. 2024, §Benchmark comparison.)

### 6. Profile likelihood for sigma allows the profiled parameter to drift (rw.sd error)

In the profile likelihood section for sigma, the mif2 call uses `rw.sd = rw.sd(Beta=0.01, rho=0.02, eta=0.02, mu_IR=0.02, mu_VR=0.02)`. The profiled parameter `Sigma` is absent from the `rw.sd` specification, which means it receives a non-zero perturbation equal to whatever is inherited from the model defaults — or alternatively, it is treated as fixed because it is not in `rw.sd`. However, the initialization via `profile_design(Sigma=seq(0.001,0.5,length=20), ...)` places Sigma at specific grid values, and because Sigma is omitted from `rw.sd`, it actually does receive zero perturbation (the correct behavior for profiling). But the profile starting guesses are paired via `nprof=10` replicates drawing the *other* parameters from a box — the authors use `profile_design()` correctly. A secondary issue: the CI cutoff line `geom_hline(color="red", yintercept=ci.cutoff)` is commented out in the plot code, so the formal 95% CI boundary is not displayed. The authors acknowledge sigma's weak identifiability from the profile but cannot formally state a CI without the cutoff line.

The fix is to uncomment the `geom_hline` call so the CI boundary appears in the figure, and ensure the profile is re-run at adequate computational scale (see Issue 4).

### 7. SIRV model 1: incorrect force of infection on vaccinated compartment

In the first SIRV model's step function, the probability of V→I transition is specified as `prob = 1 - exp(-Sigma * Beta * V / N * delta.t)`. This uses V (vaccinated count) in the denominator-equivalent force-of-infection term, but V should not appear there: the force of infection on vaccinated individuals should be proportional to the infectious population I, not to V itself. The correct formulation, consistent with the ODE `dV/dt = -sigma*beta/N * V * I`, would be `prob = 1 - exp(-Sigma * Beta * I / N * delta.t)`. This code-level error means the stochastic model being fitted does not correspond to the stated ODE, and parameter estimates from this model have no mechanistic interpretation. Note that the second SIRV model correctly uses `dN_VI <- rbinom(n=1, size=V, prob=1-exp(-Sigma*Beta*I/N*delta.t))`.

### 8. Forecast is not conditioned on the filtering distribution

The pandemic-end prediction is generated by calling `simulate()` on a pomp object that includes the future time points, starting from the estimated initial conditions at t=0. This is a forward simulation from the initial state, not from the filtering distribution (the distribution of the latent state conditioned on all 87 observed data points). Forecasts generated in this way ignore all information in the data about the current state of the epidemic and are equivalent to forward simulations from the estimated parameters at the beginning of the study period. Appropriate forecasting requires running the particle filter through the observed data to obtain the filtering distribution at Day 87, then simulating forward from that distribution. (See Wheeler et al. 2024, §Forecast methodology.)

---

## Minor Issues

- **Log-likelihood single-evaluation in local search**: The local search likelihood evaluation uses `pfilter(Np=options_Np) %>% logLik() %>% logmeanexp()`, which applies `logmeanexp` to a single value and provides no variance reduction. The evaluation should use `replicate(options_Neval, pfilter(...) %>% logLik()) %>% logmeanexp(se=TRUE)` to obtain a proper Monte Carlo average and its standard error.

- **Possible negative initial compartment R**: The initial R compartment in SIRV models is `round(N*(1-eta)-I0-V0)`. With N=39368, eta=0.9, I0=2727 (thousand), and V0=90 (thousand), R = round(39368*0.1 - 2727 - 90) = round(3937 - 2817) = 1120 thousand, which is positive at the initial guess. However, if eta approaches 1 and V0 is large, R could become negative. This should be guarded against in the rinit function.

- **SIRV2 vaccination rate formula inconsistency**: The model text states the vaccination rate is `2.88*dt + 1.89*t*dt + 0.95*dt^2`, but the quadratic fit reported is `85.79 + 2.88*Day + 0.95*Day^2` (R^2=0.999). The derivative of the fitted model with respect to Day is `2.88 + 1.90*t` (not 1.89*t). The code uses `sum(coef(fit)[c(2,3)] * c(delta.t, 2*D*delta.t + delta.t^2))`, which correctly takes the derivative of the quadratic (ignoring the constant term, whose derivative is zero). The discrepancy of 1.89 vs. 1.90 in the text is a minor rounding inconsistency.

- **No effective sample size diagnostics**: The particle filter effective sample size (ESS) is not monitored or reported for any model. ESS collapse is a warning sign of particle degeneracy, which is especially likely at `Np=100`. (See Wheeler et al. 2024, §Model diagnostics.)

- **No corroboration with scientific knowledge**: The estimated parameter values (transmission rates, recovery rates, vaccine efficacy) are never compared to independent epidemiological literature values. A recovery rate mu_IR on the scale estimated should correspond to an infectious period on the order of days; this should be checked against known COVID-19 natural history.

- **Goodness-of-fit is assessed only visually**: The conclusion that "the SIRV model does better" is based on the paired plots and verbal description of likelihood improvement, with no formal quantitative comparison (e.g., AIC table). Visual comparisons are insufficient for scientific conclusions about model adequacy. (See Wheeler et al. 2024, §Quantitative goodness-of-fit.)

- **Population scaling unit inconsistency**: The project divides all counts by 1000 ("the unit we use is thousand") but does not explicitly note whether the reported population N=39368 is in the same units as the data. The code sets N=39368 (thousands of people), I0=round(df$Active[1]/1000), and V0=round(df$People_Fully_Vaccinated[1]), so the unit is consistent, but this should be stated explicitly.

- **Typo in conclusion**: "EXISTING!" at the end of the forecast section (line 600) is a draft artifact that should be removed.

- **References**: The reference list cites "Masaaki, Ishikawa (2012)" but the text attributes the model to "Masaaki's paper 2021." The year discrepancy should be reconciled.

---

## Files Consulted

**Skill files:**
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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-boundary-mle/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-covariate-compartment-underflow/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-moment-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-domain-violation/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project03/blinded.Rmd`
