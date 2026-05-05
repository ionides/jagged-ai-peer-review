# Peer Review: W21 Project 15
**"An Analysis of COVID-19 Cases in Washtenaw County"**

---

## Summary

This project fits a time-varying SEIR model to daily COVID-19 confirmed case counts in Washtenaw County, Michigan (March–December 2020), using iterated filtering (mif2) within the pomp framework. The authors sensibly introduce a piecewise-constant contact rate beta to accommodate multiple epidemic waves and include a SARMA baseline comparison. Strengths include the use of likelihood-based inference, a presented profile likelihood for rho, and an honest acknowledgment that the SEIR model fails to beat the SARMA benchmark. However, the study has several methodological and computational weaknesses: the global search inherits the local-search mif2 object rather than a fresh pomp object; mu_EI and mu_IR are fixed without formal justification; the SARMA–SEIR log-likelihood comparison is invalid due to differing observation models; the profile rho confidence interval relies on only three points above the threshold; and several computational and reporting gaps are present. These issues collectively undermine the reliability of the reported MLE and profile CI.

---

## Major Issues

### 1. Global search initializes from a local-search mif2 result, not the base pomp object

In the global-search chunk (lines 438–465 of blinded.Rmd), the author writes:

```r
mf1 = mifs_local[[1]]
...
foreach(guess=iter(guesses, "row"), ...) %dopar% {
  mf = mf1 %>% mif2(params = c(unlist(guess), fixed_params), Nmif = NMIF_L) ...
```

Here `mf1` is the first element of `mifs_local`, itself a mif2 result from the local search. Passing a previous mif2 result object (rather than the original `covidSEIR` pomp object) as the first argument to mif2 causes the global search to inherit the cooling schedule of the local chain. At the point the global search starts, `mifs_local[[1]]` is already at the end of its cooling schedule (with `cooling.fraction.50 = 0.5` across 50 iterations), so the random-walk perturbations in the subsequent 7-stage global search start from an already-cooled state. This anchors the global search near the local-search solution rather than genuinely exploring the full parameter box. The claimed "global maximum" (-1,151.66) may not differ meaningfully from what the local search alone would have found. The fix is to replace `mf1 %>% mif2(params=..., Nmif=NMIF_L)` with `covidSEIR %>% mif2(params=..., Np=NP, Nmif=NMIF_L, cooling.fraction.50=0.5, rw.sd=params_rw.sd)` so that each global replicate begins from a fully fresh chain (Wheeler et al. 2024, §Computational adequacy).

### 2. Invalid direct log-likelihood comparison between SARMA and SEIR models

The paper compares the SEIR log-likelihood (-1,151.66) to the SARMA(3,3)x(1,1)_7 log-likelihood (-1,104.23) and concludes the SEIR model is outperformed. However, these log-likelihoods are not on the same scale. The SEIR likelihood is computed under a discretized-normal measurement model for daily raw counts. The SARMA likelihood is computed on log(1 + cases) under a Gaussian ARIMA model. The Jacobian adjustment `- sum(log_cases)` shown in the code (`arma33_s11$loglik - sum(log_cases)`) partially corrects for the log-transform, but the resulting value still reflects a Gaussian distribution on log-scale data, not discrete daily count data. Because the observation models differ, the log-likelihoods cannot be directly compared numerically — the comparison is not a valid model selection exercise. The authors should either (a) evaluate both models on the same data with the same observation model, or (b) use a proper scoring rule (e.g., CRPS) on the original scale that does not require matching distributional families (sarima-baseline-audit skill; Wheeler et al. 2024, §Benchmark comparison).

### 3. mu_EI and mu_IR fixed without formal identifiability justification

The incubation rate mu_EI and recovery rate mu_IR are fixed at 0.1 throughout the local search, global search, and profile likelihood. While the authors cite CDC guidance for plausible ranges, they offer no formal justification for fixing these parameters at a single value. Fixing these rates:
- Inflates apparent precision of other parameter estimates (b1–b5, rho, eta, tau), since their confidence regions are conditioned on fixed mu values.
- Prevents detection of collinearity between mu_EI, mu_IR, and the contact rates.
- Precludes any sensitivity analysis to show whether conclusions change with different fixed values.

At minimum, the paper should report estimates under alternative fixed values of mu_EI and mu_IR to assess sensitivity, or estimate them via the global search with appropriate profile likelihoods (Wheeler et al. 2024, §Parameter identifiability and uncertainty).

### 4. Profile likelihood for rho relies on only three points above the CI threshold

The profile section (lines 544–567) constructs a profile by running mif2 with rho fixed, seeding from the global search results stratified by `round(rho, 2)`. The rendered figure and the prose explicitly note "only three points are above the threshold." A confidence interval derived from three data points on a noisy profile curve is statistically unreliable:
- Monte Carlo noise in the pfilter evaluation (loglik.se values around 0.2–0.6 from the params CSV) can easily shift individual points above or below the chi-squared threshold, making the CI sensitive to noise rather than signal.
- The CI bounds [40.97%, 48.01%] span only about 3 percentage points of rho — an implausibly narrow and noise-sensitive range.

A robust profile requires approximately 20–30 grid points across the plausible range, each evaluated with logmeanexp over at least 10 particle filter replicates to reduce per-point SE to below 0.3 log-likelihood units (Wheeler et al. 2024, §Parameter identifiability and uncertainty).

### 5. Profile rho guess-stratification groups by rho but from all runs, not profile-specific design

In the profile chunk (lines 511–517), guesses are constructed by:
```r
guesses = read.csv(PARAMS_FILE) %>%
  group_by(cut = round(rho, 2)) %>%
  filter(rank(-loglik) <= 10) %>%
  ungroup() %>%
  select(-cut, -loglik, -loglik.se)
```
The stratification on `round(rho, 2)` is in principle correct for a rho profile. However, PARAMS_FILE accumulates results from all runs (id=1 for local, id=2 for global, id=3 for profile). If the profile results themselves are already appended to PARAMS_FILE before this read, the guess construction conflates earlier profile runs with global search results, potentially biasing coverage. More critically, the mif2 in the profile loop uses only 3 mif2 calls per guess (with decreasing cooling.fraction.50) — a total of `Nmif_L * 3 = 300` IF2 iterations with cooling — which may be insufficient to reach the constrained MLE at each rho grid value. Multiple independent restarts per grid point are strongly preferred (pomp-profile-single-restart-audit skill).

### 6. No model diagnostic tools applied (ESS, conditional log-likelihoods, filtering distribution)

The paper provides no diagnostic tools beyond visual inspection of forward simulations. Missing diagnostics include:
- Effective sample size (ESS) monitoring during particle filtering to detect particle degeneracy.
- Per-observation conditional log-likelihoods to identify time periods where the model fits poorly.
- A comparison of filtering-distribution simulations (conditioned on data) versus forward simulations from initial conditions, which would reveal whether the model dynamics are consistent with observed case patterns at each point in time.

These omissions make it impossible to assess where the model succeeds or fails mechanistically (Wheeler et al. 2024, §Model diagnostics).

---

## Minor Issues

### 7. Accumulator variable H tracks recoveries (I→R), not new infections

The Csnippet adds `H += dN_IR` (transitions from I to R), and the measurement model links `Cases ~ N(rho * H, ...)`. The data records newly confirmed COVID-19 cases — i.e., new infections entering the detected pool. Recoveries are not the same as newly reported cases, especially under a system where confirmations lag infection onset. While for a simple SEIR this ambiguity is commonly accepted (since dN_IR and new infections are proportional at steady state), the mismatch is non-trivial during epidemic surges and declines. The authors should confirm that the data records recoveries/removals rather than new detections, or revise H to track dN_EI (E→I transitions) for biological consistency (pomp-accumvar-semantic-audit skill).

### 8. rmeasure uses rnorm without enforcing integer rounding, potentially generating non-integer simulations

The rmeas Csnippet generates `Cases = rnorm(rho*H, sqrt(pow(tau*H,2)+rho*H))` and then rounds if positive: `Cases = nearbyint(Cases)`. However if `rho*H` is small and the draw is negative, Cases is set to 0.0 — which is correct. But the dmeas Csnippet evaluates the normal density at `Cases - 0.5` to `Cases + 0.5`, treating the observed count as a continuity-corrected integer. This is generally consistent, but the dmeas snippet does not explicitly check that the observed `Cases` is positive before computing `pnorm(Cases - 0.5, ...)` — when Cases = 0, the lower bound becomes -0.5, which is fine numerically. The implementation appears internally consistent but should be verified against any zero-count observations in the data.

### 9. Initial conditions E=100, I=200 fixed without estimation or sensitivity analysis

The initial infected counts E=100 and I=200 are justified by a narrative argument about an early outbreak from external travelers, but they are not estimated and no sensitivity analysis is presented. The initial exposed fraction eta is estimated, but the absolute numbers E and I at t=0 are hard-coded. Given that the study covers 306 days, the early period dynamics may be sensitive to these values. The authors should either estimate E_0 and I_0 within the search, or present a sensitivity analysis (Wheeler et al. 2024, §Initial conditions).

### 10. rho confidence interval uses global-search max as reference, not a separately verified maximum

The CI cutoff is computed as `max(all$loglik) - 0.5 * qchisq(df=1, p=0.95)` where `all` reads from PARAMS_FILE and includes all run ids. If the profile has generated and appended its own results to PARAMS_FILE before this read, the maximum loglik used as reference may come from a profile run rather than the global search MLE. The paper states the global MLE is -1,151.66, but the PARAMS_FILE first row shows -1,151.656, so this appears consistent. Nevertheless, the code should explicitly filter to global-search results (e.g., `filter(id == 2)`) before computing the reference maximum to prevent inadvertent reference to a profile or local-search value.

### 11. Computational effort at run_level=2 may be insufficient for reliable inference

At run_level=2, the global search uses NP=1000 particles, NMIF_L=100 iterations per stage (7 stages), and NREPS_EVAL=20 replicates for likelihood evaluation. With 8 parameters being searched (b1–b5, rho, eta, tau) and 500 starting points, the per-replicate particle count of 1000 is at the lower end for a 306-observation time series with a 5-phase model. The loglik.se values in PARAMS_FILE range from 0.12 to 0.62, with the MLE row showing SE=0.62 — a relatively high SE for the single best point. No evidence is presented that doubling NP would not materially change the reported MLE or profile CI (Wheeler et al. 2024, §Computational adequacy).

### 12. SARMA model selection grid uses correct period=7 but is run with eval=FALSE, hiding the search

The AIC grid search (lines 596–623) is marked `eval = FALSE` in the code chunks, meaning the search over ARMA orders is not actually run during document compilation. The user instead hard-codes the final model as SARMA(3,3)x(1,1)_7. While the code is visible, there is no guarantee that the code correctly corresponds to the model selection that was actually performed. The grid search should be run inline (or the full AIC table presented) for reproducibility.

### 13. No discussion of tau parameter estimates or their epidemiological meaning

The measurement model includes tau as a dispersion parameter controlling overdispersion: `sd = sqrt((tau*H)^2 + rho*H)`. The MLE value of tau from PARAMS_FILE is approximately 0.099–0.101 — very close to its upper box bound of 0.1. This boundary-hugging suggests the optimizer pushed tau to its maximum allowed value, potentially indicating the model requires more overdispersion than the box permits. The paper does not discuss this finding or present a profile for tau.

### 14. Model comparison against naive IID negative binomial is correct but trivially easy to beat

The paper presents a negative binomial IID model (log-likelihood = -1,464.861) as a first benchmark. Since the IID model has no temporal dependence structure, beating it is a very low bar. The SEIR model improves by ~313 log-likelihood units simply by capturing trend — this says almost nothing about whether the mechanistic SEIR structure is preferable to a non-mechanistic time series model. The SARMA baseline (which captures temporal dependence without mechanistic structure) is the more informative comparison, and it is the one the SEIR model fails to beat.

### 15. Conclusion overstates model fit quality

The conclusion states "the global search results and simulations based on the MLE show that our model can fit the data pretty well." However, the SEIR MLE log-likelihood (-1,151.66) is worse than the SARMA benchmark (-1,104.23) by approximately 47 log-likelihood units — a very large gap. The mechanistic model is outperformed by a purely statistical model with a 7-day seasonal cycle. The conclusion should explicitly note this failure and discuss what model extensions (e.g., weekly reporting patterns, stochastic beta) might address it.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-mc-noise-audit/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project15/pomp_cache/writeup_params.csv`
