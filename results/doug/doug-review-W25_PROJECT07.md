# Peer Review: W25 Project 07
## "Dengue Fever in the U.S. States and Territories (2022–2023)"

---

## Summary

This project fits three models — SARIMA(2,0,0)×(0,0,1)[53], SIRS, and SEIR — to weekly travel-associated dengue case counts reported in the United States from 2022 to 2023 (106 observations). The SIRS model introduces a two-phase transmission rate with a seasonal sine term, while the SEIR model introduces an exposed compartment with cosine seasonal forcing. Both mechanistic models are estimated via IF2 (mif2) with a negative-binomial measurement model, and the paper concludes that both POMP models achieve log-likelihoods comparable to the SARIMA benchmark (~-445), with the SIRS reaching approximately -440.

A genuine strength is that the paper undertakes two separate compartmental models and fits both with IF2 rather than resorting to ad hoc calibration. The particle filter ESS diagnostic for the SIRS model is shown, and convergence traces are presented. However, the analysis suffers from several critical methodological and coding errors that undermine nearly all quantitative conclusions: the SEIR model is fitted to a different dataset than the SIRS model, the global searches for both models inherit internal state from a previous local-search mif2 chain rather than starting from the raw pomp object, the SEIR accumulator tracks recoveries rather than new cases, population size N in the SEIR model is implausibly small by two orders of magnitude, the SARIMA log-likelihood is compared numerically to POMP log-likelihoods under incompatible observation models, and no profile likelihoods are computed for any parameter in either model. These issues collectively prevent the stated conclusions from being supported.

---

## Major Issues

### 1. SEIR model fitted on a different dataset than the SIRS model

The SIRS data-loading block (lines ~45–51) correctly filters `cdc_casesby_week` to `Year %in% c(2022, 2023)`. The SEIR section (lines ~776–782) uses an entirely different filtering strategy:

```r
data <- cdc_casesby_week
data  <- data[637:nrow(data), ]
data$Week <- seq(1, nrow(data))
```

This row-index slice does not guarantee alignment with the years 2022–2023; it depends on the exact ordering and length of the `cdc_casesby_week` data frame. As a result, the SEIR model is most likely fitted on a different time period than the SIRS model. The two models' log-likelihoods are then compared (Conclusion section) as if they were fitted on the same data — which they were not. All SEIR parameter estimates, likelihoods, and the "SEIR vs. SARIMA" comparison are invalid until this is corrected. Per the `pomp-dataset-substitution-audit` skill, this class of copy-paste filter error is a critical failure that does not produce any runtime warning.

**Fix:** Replace the row-index slice with the same `filter(Year %in% c(2022, 2023))` call used in the SIRS section. Verify that both models see identical data before comparing their likelihoods.

---

### 2. Both global searches are anchored to the local-search mif2 chain (anti-pattern)

In the SIRS section (lines ~610–626), the global search is structured as:

```r
mf1 <- mifs_local[[1]]
foreach(guess=iter(guesses,"row"), ...) %dofuture% {
  mf1 |> mif2(params=c(guess, fixed_params)) |> mif2(Nmif=Nmif) -> mf
  ...
}
```

The same pattern appears in the SEIR global search (lines ~1083–1100):

```r
mf1 <- local_mifs[[1]]
foreach(guess=iter(guesses,"row"), ...) %dopar% {
  mf1 |> mif2(params=c(guess, fixed_params)) |> mif2(Nmif=Nmif) -> mf
  ...
}
```

Passing a previous `mif2` result object (`mf1`) as the first argument to `mif2()` causes the global search to inherit the cooling schedule and internal IF2 state of the local chain. Because `mf1` has already run `Nmif` iterations and its perturbation magnitudes have decayed nearly to zero, each "global" replicate starts from a random parameter draw but performs very few functional IF2 iterations before the perturbations collapse — anchoring the result near the local-search solution. The claimed "global search" does not explore the parameter space from genuinely fresh starts. Per the `pomp-global-search-init-audit` skill, this is a well-documented anti-pattern.

**Fix:** Replace `mf1 |> mif2(params=..., ...)` with `base_pomp_object |> mif2(params=..., ...)` in both global search loops, where `base_pomp_object` is the original `pomp()` call result (`dfSIRS` or `measSEIR`), not a previous mif2 result.

---

### 3. SEIR accumulator variable tracks recoveries, not new cases

In the SEIR rprocess Csnippet (lines ~785–802):

```
H += dN_IR;  // Cumulative incidence (used for measurement)
```

`dN_IR` is the flow from I to R — that is, recoveries. The observation data (`reports`) consists of newly reported dengue cases, which correspond to new infections (entries into the infectious compartment, i.e., `dN_EI`) or at least newly symptomatic individuals, not recoveries. Accumulating recoveries in H and linking reported counts to `rho * H` via the measurement model is a semantic mismatch: the reporting rate `rho` no longer estimates the fraction of new infections that are reported; it absorbs the ratio of recoveries to new cases, and the estimated transition rates compensate accordingly. Per the `pomp-accumvar-semantic-audit` skill, this distorts all SEIR parameter estimates and invalidates policy conclusions derived from the model.

**Fix:** Change `H += dN_IR` to `H += dN_EI` (accumulate newly infectious individuals, i.e., departures from the E compartment) or `H += dN_SE` (new exposures), depending on what the CDC surveillance data records. For reported dengue cases, `H += dN_EI` is typically the correct choice.

---

### 4. SEIR population size N is implausibly small by two orders of magnitude

The SEIR model uses `N = 3200000` (3.2 million). The paper describes the data as travel-associated dengue cases from "U.S. States and Territories," implying the at-risk population is the full U.S. population (~335 million). A value of 3.2 million is inconsistent by a factor of roughly 100. This directly biases the force-of-infection term `Beta * I / N`: with an artificially small N, the per-contact transmission rate `Beta` is inflated by a factor of ~100 to compensate, producing a biologically uninterpretable estimate. The initial conditions `eta * N = 0.1 * 3.2M = 320,000 susceptibles` are also implausible for a national model.

By contrast, the SIRS model uses `N = 3.25e8` (325 million), which is the correct order of magnitude. The inconsistency is never acknowledged or justified, and the SEIR `Beta` estimates cannot be compared meaningfully to any reference values.

**Fix:** Set `N = 3.25e8` (or the same value used in the SIRS model) and re-estimate initial conditions and transmission rates accordingly. Alternatively, treat `N` as a fixed covariate reflecting the effective travel-exposed population and justify its value with reference to census or travel data.

---

### 5. Invalid direct comparison of SARIMA and POMP log-likelihoods

The paper repeatedly compares the SARIMA log-likelihood (~-445) to the SIRS and SEIR log-likelihoods (-440 and approximately -445, respectively), concluding that "the log likelihoods of both the SIRS and SEIR model were close to the baseline of the SARIMA model, which is a desirable feature." This comparison is invalid. The SARIMA model is fitted under a Gaussian observation model on the original count series; the POMP models use a negative-binomial measurement model. Because the observation distributions differ, the two log-likelihood values are on incompatible scales and cannot be directly compared. Per the `sarima-baseline-audit` skill, a valid comparison requires both models to be evaluated under the same observation model and on the same (potentially transformed) data. The conclusion that "close log-likelihoods" is "desirable" misinterprets what benchmark comparison means: the POMP model should ideally exceed the benchmark substantially, suggesting it captures mechanistic structure the ARMA model cannot.

**Fix:** Evaluate both models under a common scoring rule (e.g., CRPS on the original scale), or use the SARIMA model only as a qualitative reference rather than claiming numeric comparability. Acknowledge explicitly that the log-likelihood scales are incompatible.

---

### 6. No profile likelihoods for any parameter in either model

Neither the SIRS nor the SEIR section computes a profile likelihood for any parameter. Without profile likelihoods, it is impossible to assess whether parameters are identifiable from the 106-week time series, and no confidence intervals are reported for any parameter. This is particularly concerning for the SIRS model, which has 10 free parameters (a, b, c, d, mu_IR, mu_RS, k, S_0, I_0, R_0) and only 106 observations, and the SEIR model, which has at least 7 free parameters. The reporting rate `rho` is fixed at `1e-7` in the SIRS model without statistical justification. Per Wheeler et al. (2024) and POMP checklist §5, profile likelihoods are necessary to determine whether the data support the complexity of the fitted models.

**Fix:** Compute profile likelihoods for at least the key epidemiological parameters (transmission rate, recovery rate, and reporting rate) using `profile_design()` with the profiled parameter excluded from `rw.sd`. Report Monte Carlo Adjusted Profile (MCAP) confidence intervals.

---

### 7. Reporting rate rho fixed at biologically implausible values without justification

In the SIRS model, `rho` is fixed at `1e-7` and declared as a `fixed_param`. This reporting rate of 0.0000001 means that for every 10 million new infections, only 1 is reported. For a model of U.S. travel-associated dengue cases, where the CDC actively tracks imported cases, such an extreme underreporting factor is scientifically implausible. The paper states "we fixed N and rho based on surveillance coverage" but provides no citation or quantitative justification. Furthermore, the SEIR model estimates `rho` freely and converges to values near 0.9 (near-perfect reporting), which contradicts the SIRS assumption completely. This fundamental inconsistency between the two models is never acknowledged or explained.

**Fix:** Either estimate `rho` in the SIRS model via likelihood maximization, or justify the fixed value with reference to CDC surveillance coverage estimates. Discuss why SIRS and SEIR yield such drastically different implied reporting rates.

---

## Minor Issues

### 8. SEIR local search uses nbrOfWorkers() replicates instead of Nlocal

The SEIR local search chunk (lines ~946–957) runs:

```r
foreach(i=seq_len(ncpu), ...) %dofuture%
```

This ties the number of IF2 replicates to the number of available cores rather than the `Nlocal` parameter defined in the run-level settings (Nlocal = 20 at run_level = 3). The result is that the number of local search replicates varies with the execution environment and may be inconsistent across runs. The SIRS model correctly uses a fixed count (`foreach(i=1:20, ...)`). Convergence assessment requires a reproducible, fixed number of replicates.

**Fix:** Replace `seq_len(ncpu)` with `seq_len(Nlocal)` to match the SIRS model and the run-level settings.

---

### 9. Post-local-search SEIR simulations hardcode k=10 instead of using the optimized value

In the SEIR simulation blocks following the local and global searches (lines ~1000, ~1029, ~1122, ~1148), `k` is hardcoded at 10:

```r
params = c(Beta = max_row$Beta, ..., k = 10)
```

The overdispersion parameter `k` is estimated during the IF2 search, yet the post-search simulations do not use the optimized value. This means the simulation trajectories displayed as "model fit under optimized parameters" do not actually reflect the MLE — the overdispersion (and hence the width of the credible bands) is misspecified.

**Fix:** Replace `k = 10` with `k = max_row$k` in all post-search simulation blocks.

---

### 10. No particle filter diagnostic (ESS) for SEIR before local search

The SIRS section presents ESS and conditional log-likelihood plots (pfilter output) to verify filter health before proceeding to IF2 optimization. The SEIR section omits this diagnostic entirely. Without confirming that the particle filter is healthy at the chosen initial parameters, there is no basis for trusting the convergence of the SEIR local or global search.

**Fix:** Add a `pfilter()` call at the initial SEIR parameter values with a `plot()` of the resulting object to display ESS and per-observation log-likelihoods, analogous to the SIRS section.

---

### 11. SIRS run-level switch has 4 values for some parameters but only 3 run levels

The run-level settings block (lines ~339–347) defines:

```r
Np <- switch(run_level, 100, 1e3, 1e3, 2e3)
```

This provides 4 values for `Np` but only 3 for `Nlocal`, `Nglobal`, and others. R's `switch()` for integers uses positional matching, so providing extra values is harmless, but the inconsistency suggests the run-level definitions were not carefully maintained. At run_level = 3, `Nglobal = 20` for the SIRS model, which is very few replicates for a global search with 7 free parameters.

**Fix:** Standardize all `switch()` calls to use the same number of levels, and increase `Nglobal` to at least 100 for run_level = 3.

---

### 12. SIRS model does not present model diagnostics beyond ESS

The SIRS section presents a particle filter ESS plot and convergence traces from the local search, but no per-observation conditional log-likelihood plot is discussed for diagnosing periods of poor fit. The ESS diagnostic is noted briefly ("ESS occasionally dips"), but the conditional log-likelihood panel — shown in the pfilter plot — is not discussed. Wheeler et al. (2024) §Model diagnostics emphasizes that per-observation log-likelihoods are essential for identifying where the model fails.

**Fix:** Add a discussion of the conditional log-likelihood panel from the pfilter output. Identify any weeks with systematically low conditional log-likelihood and consider whether the model structure is adequate for those periods.

---

### 13. Seasonal amplitude c in SIRS is logit-transformed, restricting it to (0, 1) — inconsistency with model

The SIRS `partrans` declares `logit = c("rho", "c")`, restricting `c` (seasonal amplitude) to (0, 1). The sinusoidal transmission model uses `1 + c * sin(...)`, so the amplitude must lie in (0, 1) for the transmission rate to remain positive. However, the model text states `c ∈ [0, 1)` as an assumption, and the initial simulation uses `c = 0.4`. This is internally consistent. What is inconsistent is that the `c` amplitude in the SEIR model (`a` in the SEIR Csnippet) is also declared with `logit` but its value in the global box search is allowed up to 1 (`upper = c(a = 1, ...)`). A value of exactly 1 with logit transformation would require an infinite logit argument. The upper bound should be slightly below 1.

---

### 14. No out-of-sample or forecasting evaluation

The project fits models to the full 2022–2023 period (106 weeks) with no held-out test set and no forecasting exercise. The stated motivation references "rising international mobility" and policy relevance, but the fitted models are never used to generate forecasts or assess out-of-sample performance. Per Wheeler et al. (2024) §Forecast methodology, models used for policy should be evaluated on their forecasting performance via simulation from the filtering distribution.

---

### 15. ACF analysis conclusion conflates pattern with non-stationarity

The EDA section states "the oscillating pattern displayed in the [ACF] plots supports that the data is non-stationary," while also noting "the lack of significant partial autocorrelation at higher lags suggests that higher-order AR terms are unnecessary." No formal stationarity test (ADF, KPSS) is performed. The ACF pattern described (sinusoidal oscillation, gradual damping) is characteristic of a stationary seasonal ARMA process, not a non-stationary one. A non-stationary process would exhibit ACF that decays very slowly or not at all, not an oscillating pattern. The conclusion drawn (non-stationarity) is not supported by the evidence presented.

**Fix:** Perform ADF or KPSS tests on the raw series and correctly interpret the hypothesis test direction (ADF: small p-value rejects unit root, supporting stationarity; KPSS: small p-value rejects stationarity). The SARIMA(2,0,0)×(0,0,1)[53] fit with d=0 already implies the authors treated the series as stationary in practice.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project07/blinded.Rmd`
