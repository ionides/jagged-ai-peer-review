# Peer Review: W22 Project 17
## US COVID-19 Cases Analysis — SARIMA and SEIR Models

---

### Summary

This project applies SARIMA and SEIR models to daily US COVID-19 case counts from June 2021 through March 2022. The data covers two distinct waves (Delta and Omicron), and the authors address the structural break by introducing time-varying transmission and latency rates via seven piecewise-constant beta segments. The comparative framing — asking which model better captures the pandemic dynamics — is a reasonable research question. The SARIMA analysis is competently executed at a basic level. The SEIR analysis, however, contains several serious methodological and coding deficiencies: the global search is anchored to the local-search solution rather than exploring the parameter space independently; the model explicitly acknowledges non-convergence while continuing to draw substantive conclusions; the accumulator variable accumulates recoveries rather than new infections; the measurement model uses a normal approximation that can produce negative case counts; and no profile likelihoods or model diagnostics are presented. The log-likelihood comparison between SARIMA and SEIR, which forms the paper's main conclusion, is unreliable because the SEIR log-likelihood is from a non-converged, potentially mis-specified model.

---

### Major Issues

**1. Global search is anchored to the local-search solution, not a true global search**

In the `seir_global_mifs` chunk, the `mif2()` call in the global search loop takes `local_best` (the best result from `mifs_local`) as its first argument:

```r
local_best %>%
  mif2(
    params = c(apply(covid_box, 1, function(x) runif(1, x[1], x[2])), fixed_params),
    ...
  )
```

This passes a previous `mif2` result object as the first argument. While the `params=` argument supplies random draws from the box, the cooling schedule inherited from `local_best` is already at or near its final cooled state after `Nmif` iterations. This means the global search effectively starts from `local_best`'s parameter region with near-zero perturbations, not from the diverse starting points implied by the box. The "global search" is therefore a collection of near-duplicate local refinements from a single point, not a genuine exploration of the parameter space. The fix is to replace `local_best %>% mif2(...)` with `covidSEIR %>% mif2(...)` in the global search loop. See the `pomp-global-search-init-audit` skill and Wheeler et al. (2024) §Computational adequacy.

**2. Self-acknowledged non-convergence undermines all SEIR-based conclusions**

The conclusion section explicitly states: "Trajectory plots for some variables still do not show significant convergence." Despite this acknowledgment, the paper presents and interprets a table of best-fit parameter estimates, forward simulations from those parameters, and a log-likelihood comparison between SEIR and SARIMA. These results are all derived from a non-converged optimization and are therefore unreliable by the authors' own admission. The log-likelihood of -3684.733 reported for the SEIR model cannot be treated as a meaningful estimate of the model's maximum likelihood; it is a lower bound (at best) from a non-converged search. The main conclusion — "both SARIMA and SEIR models can well model COVID-19 daily cases" — is unsupported because the SEIR fit quality is unknown. Either computational effort must be substantially increased until genuine convergence is demonstrated, or all claims derived from the SEIR parameter estimates must be retracted. See the `pomp-self-diagnosed-nonconvergence-audit` skill.

**3. Accumulator variable accumulates recoveries rather than new infections**

The Csnippet increments `H` with `dN_IR` (individuals transitioning from I to R):

```c
H += dN_IR;
```

The measurement model then links observed daily cases to `rho * H`. But `dN_IR` represents daily recoveries, not daily new detections or new infections. Daily confirmed case counts record transitions into the infectious/detected pool (roughly `dN_EI` or `dN_SE`), not exits from it. This mismatch means the model is estimating the reporting rate of recoveries, not confirmed cases, which is a different epidemiological quantity. Because recoveries lag infections by the latency and infectious periods, the accumulator `H` is systematically shifted in time relative to what the data record, distorting all rate estimates. The fix is to accumulate `dN_EI` (exposed-to-infectious transitions, as a proxy for new cases) or `dN_SE` with an appropriate reporting lag. See the `pomp-accumvar-semantic-audit` skill.

**4. Measurement model uses a normal approximation with no lower bound enforcement**

The `dmeas` and `rmeas` Csnippets implement a normal distribution:

```c
double mean = rho * H;
double sd = sqrt(pow(tau * H, 2) + rho * H);
// dmeas: pnorm continuity-corrected
// rmeas: rnorm(...), rounded, clipped at 0
```

For small `H` values, this normal distribution has positive probability mass below zero. The `dmeas` snippet for `Cases > 0` uses `pnorm(Cases+0.5, ...) - pnorm(Cases-0.5, ...)`, which is appropriate, but when `Cases = 0` the formula `pnorm(Cases+0.5, ...)` instead of `pnorm(0.5, ...) - pnorm(-Inf, ...)` omits the left tail correction. More importantly, a negative-binomial measurement model would be more appropriate for overdispersed count data and is standard in POMP epidemic modeling (Wheeler et al. 2024, §Stochasticity). The normal approximation underestimates the probability of extreme counts and cannot produce zero cases without rounding, making it inappropriate for periods of very low transmission.

**5. Insufficient computational effort: run_level=2 with Np=1000, Nmif=100**

The project runs at `run_level=2` with `Np=1e3` particles, `Nmif=100` IF2 iterations, and only `Nreps_global=30` global search replicates. For a 13-parameter COVID SEIR model fitted to 298 time points, 1000 particles is marginal — particle filter variance is typically high enough to make individual log-likelihood evaluations noisy. The global search evaluation chunk uses only `Np=100` particles for the final likelihood evaluation:

```r
evals <- replicate(10, logLik(pfilter(mf, Np=100)))
```

This is severely inadequate: 100 particles for a model of this complexity produces log-likelihood estimates with Monte Carlo standard errors likely exceeding 5–10 units. The reported log-likelihood of -3684.733 with SE 0.0053 is therefore implausibly precise — this SE reflects only Monte Carlo variability across 10 replicates with 100 particles each, not the true estimation uncertainty. The number of particles should be at least 2000–5000 for stable likelihood evaluation at the global search stage. See Wheeler et al. (2024) §Computational adequacy.

**6. No benchmark comparison between SEIR and a non-mechanistic model**

The paper compares SEIR directly to SARIMA, with SARIMA serving as both the non-mechanistic benchmark and the primary comparison model. This is a reasonable framing, but the comparison is invalid because (a) the SEIR log-likelihood is from a non-converged optimization and (b) the SEIR and SARIMA log-likelihoods are not computed on a compatible basis — SARIMA uses a Gaussian likelihood while the SEIR uses a particle-filter-based likelihood with the normal approximation described above. There is no discussion of whether the likelihood values are comparable across the two model classes, nor any AIC-based comparison. The conclusion that SARIMA "has a higher log likelihood" than SEIR is stated as a model comparison but provides no evidence of the SEIR model's limitations beyond computational failure. See Wheeler et al. (2024) §Benchmark comparison.

**7. No profile likelihoods or parameter identifiability analysis**

The model has 11 free parameters (b1–b7, ei1, ei2, rho, tau) plus two fixed parameters (N, mu_IR). No profile likelihoods are computed for any parameter, so there is no evidence that these parameters are jointly identifiable from the data. With 7 piecewise-constant beta values and 2 piecewise-constant ei values, the model has very high flexibility relative to the data; many parameter combinations likely produce similar likelihoods. The estimated b5 = 0.15 appears identical to its starting value, suggesting the optimizer may not have moved this parameter meaningfully. Without profile likelihoods, the reported parameter estimates cannot be trusted to represent the MLE. See Wheeler et al. (2024) §Parameter identifiability.

**8. Initial conditions are fixed at biologically implausible values without justification**

The rinit function sets `S = N = 334,515,015`, `E = 200,000`, `I = 270,000`, `H = 0` at the start of the analysis period (June 2021). Setting S = N implies zero prior immunity at the start of June 2021, which is biologically implausible — by June 2021, approximately 40% of the US population had been vaccinated or infected. The authors cite a prior SEIR paper for the E and I initial values, but do not account for the recovery compartment or prior immunity. The incorrect S(0) = N forces the model to compensate through the beta parameters, distorting all transmission rate estimates. See Wheeler et al. (2024) §Initial conditions.

---

### Minor Issues

**9. SARIMA model is not invertible or causal, and this is acknowledged but not addressed**

The paper correctly identifies that the fitted SARIMA(5,1,5)×(2,1,1)_7 model has roots outside the unit circle, making it non-invertible and non-causal. This is a serious diagnostic failure — a non-invertible model has an undefined MA representation and the conditional forecasts are unreliable. The appropriate response is to restrict the model order or use a different parameterization, not simply to proceed with the analysis. The paper notes the problem ("indicating the model is not invertible and not causal") but draws no conclusion from it.

**10. AIC table for SARIMA is computed with two separate searches that may not be comparable**

The non-seasonal ARIMA AIC table and the seasonal SARIMA AIC table are computed sequentially: first ARIMA(p,1,q) for p,q in 0:5, then SARIMA(5,1,5)×(P,1,Q)_7 for P,Q in 0:2. The ARIMA selection is used to fix p=5, q=5 before the seasonal search begins. This sequential selection does not account for the interaction between seasonal and non-seasonal components and may not find the globally optimal SARIMA specification. A joint search or a model-averaging approach would be more rigorous.

**11. Covariate intervention coding has a gap (November 12 to December 8, 2021)**

The piecewise covariate table covers:
- Periods 1–4: June 5 to November 11, 2021
- Period 5: December 9 to December 21, 2021

There is a gap from November 12 to December 8, 2021, which is not assigned to any period in the table (the table has 30+28+62+40+40+15+83 = 298 entries total, but the beta definitions jump from period 4 (b4) ending November 11 to period 5 (b5) starting December 9). The text does not describe what happens to the model during this gap period. This may cause misalignment between the covariate and the data time indices.

**12. Global search evaluation uses 10 replicates with Np=100, inconsistent with the local search evaluation**

The local search evaluation (`seir_local_search` chunk) uses `Nreps_eval=20` replicates with `Np=1e3`, while the global search evaluation uses `replicate(10, logLik(pfilter(mf, Np=100)))`. The dramatically lower particle count in the global evaluation (100 vs. 1000) makes the global log-likelihood estimates far noisier than the local estimates, undermining the log-likelihood comparison between local and global search results. This inconsistency should be corrected by using the same Np across all evaluation steps.

**13. The starting parameter text table contains an error: N is listed twice**

In the "Choosing starting points" section, the parameter list states both "N = 334,515,015" (the US population) and "N = 367,601 (fixed)" in the same bulleted list. The second value appears to be an error — it may be a leftover from a different dataset or a previous version of the model. The code correctly uses `pop_us = 334515015`. This inconsistency suggests insufficient proofreading.

**14. No model diagnostics (conditional log-likelihoods, ESS monitoring)**

Beyond the convergence trace plots, no particle-filter diagnostics are presented. The effective sample size (ESS) is not monitored, so it is impossible to assess whether the particle filter is degenerating during the Omicron wave (where case counts spike dramatically). Conditional log-likelihood plots would identify specific time periods where the model fails. These diagnostics are important for a model applied to a dataset with two distinct epidemic waves. See Wheeler et al. (2024) §Model diagnostics.

**15. Reproducibility: no session information, package versions, or total compute time reported**

The Rmd file does not include `sessionInfo()` output, package version numbers, or any indication of total computation time. The pomp and doParallel package versions are not recorded. Given that the pomp API has changed across versions, the code may not reproduce on current CRAN releases. The Makefile is present but does not document the reproduction workflow. See the code supplement checklist.

---

### Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-boundary-mle/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project17/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project17/us1.csv`
