# Peer Review: W22 Project 19
**"An Analysis of the Omicron variant of COVID-19 Cases in Wayne County"**

---

## Summary

This project analyzes daily confirmed COVID-19 (Omicron variant) cases in Wayne County, Michigan from December 2021 through March 2022. The authors fit an ARIMA(4,1,4) model and an SEIR POMP model using iterated filtering (IF2) via `mif2`, then compare the two models by log-likelihood. While the project demonstrates familiarity with the pomp workflow and the SEIR framework, it contains several critical methodological errors that undermine nearly every quantitative conclusion: the two models are compared on materially different datasets; the accumulator variable tracks the wrong epidemiological event; the profile likelihood is seeded from a region far from the global optimum; and the global search inherits its cooling schedule from the local search. These compounding errors make the reported log-likelihoods, confidence intervals, and biological conclusions unreliable.

---

## Major Issues

### 1. Invalid log-likelihood comparison: different datasets and different observation models

The central quantitative conclusion of the paper -- that ARIMA(4,1,4) outperforms the SEIR model based on log-likelihood (-618.74 vs. -861.13) -- is doubly invalid.

First, the ARIMA model is fitted to `data_wayne1`, which is filtered to dates `<= 2022-02-28` (90 observations), while the SEIR model is fitted to `covid_wayne_winter.csv`, which spans December 1, 2021 through March 31, 2022 (121 observations). A log-likelihood is a sum over observations: adding 31 more observations to the SEIR dataset mechanically makes its log-likelihood more negative, independent of model quality. The 242-unit gap in log-likelihood between the two models is therefore dominated by this data-length difference, not model fit.

Second, even if both models were fitted to the same data, their log-likelihoods would not be directly comparable: the ARIMA model evaluates a Gaussian likelihood on differenced data, while the SEIR model evaluates a discretized normal likelihood on the original count scale. These are not nested models and do not share an observation model.

The authors should fit both models to the same 121-day dataset under a common or acknowledged observation model, or replace log-likelihood comparison with a proper scoring rule (e.g., CRPS on the original scale). See Wheeler et al. (2024), section on benchmark comparison.

### 2. Accumulator variable tracks the wrong epidemiological event

The SEIR model defines `H` as an accumulator variable (`accumvars = "H"`) that accumulates `dN_IR` -- transitions from the infectious compartment `I` to recovery (`H`). The measurement model then links `reports ~ Normal(rho * H, ...)`. However, the observed data records **new confirmed positive cases** -- epidemiologically, these are entries into the infectious compartment (transitions from `E` to `I`), not recoveries.

Accumulating recoveries (`dN_IR`) rather than new infections (`dN_EI`) creates a systematic mismatch between the observation process and what `H` represents. The reporting rate `rho` will be estimated to absorb the ratio of recoveries to true new case detections, not the true detection fraction. The transition rates `mu_IR` may also be distorted because the optimizer adjusts them to compensate. All parameter estimates and the fitted log-likelihood are unreliable as a result. The fix is to replace `H += dN_IR` with `H += dN_EI` in the `seir_step` Csnippet.

### 3. Global search inherits cooling schedule from local search (anti-pattern)

The global search is initialized using `mf1 <- mifs_local[[1]]` as the first argument to `mif2()` in the foreach loop:

```r
mf1 <- mifs_local[[1]]
...
mf = mf1 %>% mif2(params = c(unlist(guess), fixed_params), Nmif = NMIF_L) %>% ...
```

Passing a previous `mif2` result object as the base argument causes each global search replicate to inherit the internal IF2 state and cooling schedule from the completed local search chain. The cooling perturbations are therefore already at or near zero from the outset, meaning the global search performs very few effective parameter-space exploration steps from each new random starting point. The "global search" is effectively a collection of nearly-frozen local refinements anchored near the local search solution, not a genuine exploration of the parameter box. The fix is to replace `mif1` with the raw `covidSEIR` pomp object as the first argument to `mif2()` in the global search loop (Wheeler et al. 2024, section on computational adequacy).

### 4. Profile likelihood is neither globally seeded nor valid: 20-unit gap from global MLE

The profile likelihood over `tau` is seeded from `results_global` filtered by `round(tau, 2)`, and the IF2 base object is again `mifs_local[[1]]`. However, inspection of the saved artifacts reveals that the profile maximum log-likelihood is -881.56, while the global search maximum is -861.13 -- a gap of 20.4 log-likelihood units. This 20-unit deficit means the profile was never able to reach the globally optimal region of parameter space. Consequently:

- The profile curve does not represent the true profile log-likelihood surface.
- The chi-squared CI cutoff (applied at the profile maximum as reference) is computed at the wrong reference level. Using the correct global maximum as the reference, **zero** profile points exceed the CI threshold, making the confidence interval for `tau` entirely uninformative.
- The reported CI of [0.669, 0.706] (presented as [66.90%, 70.62%] in the text) is an artifact of the locally-seeded profile, not a reflection of the data's information about `tau`.

Furthermore, the global MLE for `tau` is 0.297, which falls below the lower end of the profile's coverage. The profile grid does not extend to the region where the global optimum lies. The CI should be recomputed after fixing the global search initialization issue (Issue 3) and re-running the profile from globally-seeded starting points.

### 5. Profile CI displayed with incorrect units (code bug)

The tau CI code formats the bounds as percentages via `sprintf("%.2f%%", 100 * min)` and `sprintf("%.2f%%", 100 * max)`. Since `tau` is a proportional noise scaling parameter (not a probability or rate), multiplying by 100 and appending "%" produces a nonsensical display. The reported CI "[66.90%, 70.62%]" in the HTML output is therefore misleading. The correct display should report the raw tau values (approximately 0.669 and 0.706) with appropriate units.

### 6. No comparison to a non-mechanistic benchmark on the same data

Per Wheeler et al. (2024), mechanistic models should be compared against non-mechanistic statistical benchmarks (e.g., ARIMA, auto-regressive negative binomial) to assess whether the mechanistic model captures meaningful structure. While an ARIMA model is included, the comparison is invalidated by the data-length and observation-model mismatches described above (Issue 1). There is no valid benchmark comparison in the paper, making it impossible to assess whether the SEIR structure provides any improvement over a simple time-series model.

### 7. Fixed and biologically unmotivated initial conditions for E and I

The initial exposed and infectious counts are fixed at `E = 6000` and `I = 15000` without justification, while only `eta` (the susceptible fraction) is estimated. For a model spanning an active epidemic peak, the initial values of `E` and `I` can substantially affect the peak timing and height of the simulated trajectory. The authors do not assess sensitivity to these fixed values, nor do they explain how 6,000 exposed and 15,000 infectious individuals on December 1, 2021 were determined. Wheeler et al. (2024) recommend either estimating initial conditions as parameters or demonstrating robustness to their choice.

### 8. Key epidemiological parameters mu_EI and mu_IR fixed without sensitivity analysis

The authors fix `mu_EI = 0.1` (mean latent period 10 days) and `mu_IR = 0.08` (mean infectious period 12.5 days) throughout all analyses. While they cite CDC guidance justifying these ranges, the ranges given in the text ([0.07, 0.5] for mu_EI, [0.07, 0.1] for mu_IR) are wide, and fixing values within these ranges can substantially affect the estimated transmission rates and the profile likelihood for other parameters. No sensitivity analysis over the fixed values is performed. The authors should either estimate these parameters or demonstrate that their choice of fixed values does not materially affect conclusions.

### 9. Global MLE contradicts the paper's key biological claim, and the contradiction is not adequately addressed

The paper's central biological motivation for the two-beta model is that the Omicron variant (active in the `beta2` period) should be more contagious than the earlier mixed-variant period (`beta1`). However, the global MLE yields `beta1 = 3.55` and `beta2 = 0.88` -- the opposite ordering. The authors acknowledge this: "the global search results in beta2 < beta1, indicating that the Omicron variant isn't contagious as expected." They then conclude that this is due to the model needing a longer tail, without considering model misspecification. This reversal of expected biological ordering is a strong signal of model misspecification (Wheeler et al. 2024, section on corroboration with scientific knowledge) and deserves more rigorous treatment -- either profile likelihoods for beta1 and beta2 separately to check identifiability, or explicit model diagnostics.

---

## Minor Issues

- **ARIMA model selection criterion**: The paper selects ARIMA(4,1,4) because it "gives fairly small AIC while not losing too much parsimony," but inspection of the AIC table should be used more systematically. With 90 observations and 8 AR/MA coefficients plus sigma, ARIMA(4,1,4) is overparameterized. The paper notes inverse roots near the unit circle, which suggests a smaller model would be more appropriate, but then proceeds with ARIMA(4,1,4) anyway.

- **Residual normality rejected but conclusion unclear**: The Shapiro-Wilk test rejects normality of ARIMA(4,1,4) residuals (p < 0.05), which is acknowledged, but no action is taken. The conclusion states that the ARIMA model fits well, which is inconsistent with this diagnostic failure.

- **Data description inconsistency**: The introduction states the data spans "12/01/2021 to 03/31/2022 (day 121)" but the EDA section's R code filters `data_wayne1` to `data_wayne$date <= '2022-02-28'` (90 days). The title, text, and SEIR dataset are internally consistent at 121 days, but the EDA and ARIMA analysis silently use a 90-day subset. This inconsistency is not mentioned anywhere in the paper.

- **Profile starts (guesses) are stratified correctly by tau, but the IF2 base object is wrong**: The profile code correctly uses `group_by(cut = round(tau, 2))` to stratify starting guesses by the profiled parameter. However, as noted in Issue 4, the base object (`mifs_local[[1]]`) and the large gap from the global MLE render the profile invalid regardless.

- **Measurement model notation inconsistency**: The text states the measurement model as `H = max(floor(H_n), 0)` where `H_n ~ N(rho*H_n, (tau*H_n)^2 + rho*H_n)`. The subscript `H_n` is reused on both the left and right sides of the distributional statement, which is circular. The correct notation should distinguish the latent count (e.g., `mu = rho * H_t`) from the observed count.

- **No model diagnostics beyond visual fit**: There are no conditional log-likelihood plots, effective sample size traces, or residual diagnostics for the SEIR model. Wheeler et al. (2024) recommend these as essential for understanding where and how the model succeeds or fails.

- **No forecast methodology**: No attempt is made to forecast beyond the observed period. While the paper's stated goal is analysis rather than forecasting, the omission means the practical utility of the model is not demonstrated.

- **Computation level**: With `NP = 1000` particles, `NMIF_L = 100` iterations, and `NREPS_EVAL = 20` replications, the computation is moderate. However, given the 20-unit gap between the profile maximum and global maximum, and the global-search initialization error, the computational setup is insufficient to guarantee convergence even at the local optimum.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-multi-series-length-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-ci-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/writeup_global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/writeup_profile_tau.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/writeup_local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/covid_wayne_winter.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/covid_data.csv`
