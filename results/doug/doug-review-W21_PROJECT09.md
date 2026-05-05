# Peer Review: W21 Project 09 — Utah COVID-19 SIR Model

## Summary

This project applies ARIMA and SIR-family models to Utah COVID-19 seven-day rolling average case counts from March 2020 through April 2021. The ARIMA component is executed competently and provides a reasonable baseline. However, the POMP-based SIR analysis is almost entirely commented out: the author explicitly acknowledges computational failures with the particle filter, provides no converged likelihood estimates, and falls back on a deterministic ODE SIR model fitted by minimizing residual sum of squares (RSS) on cumulative cases using `optim`. The measurement model in the pomp object contains a severe distributional mismatch between `dmeasure` and `rmeasure`. No likelihood-based inference is completed, no benchmark comparison is made, no uncertainty is quantified, and no convergence diagnostics are shown. The concluded claim that the "SIR model shows the cycle of the virus better than the pomp model" is unsupported because neither model was properly estimated.

---

## Major Issues

### 1. POMP inference is entirely absent — all mif2/pfilter code is commented out

The entire IF2 local search, global search, and likelihood evaluation code (lines 212–273 in the Rmd) is commented out. The author states: "After a certain number of numerics, R struggled calculating the log-likelihood statistic... This is the best model that it calculated." No log-likelihood, no parameter estimates from IF2, and no convergence diagnostics are presented. The only POMP output shown is a forward simulation from two manually chosen parameter sets. This means the core claim of fitting a POMP model to the data is not substantiated. Per Wheeler et al. (2024), parameters must be estimated by maximizing the likelihood, not by visual inspection of simulations.

**Fix:** Complete the particle filter and IF2 inference pipeline with adequate particle counts (Np >= 1000) and at least 20 replicate searches. Report log-likelihoods and convergence traces.

---

### 2. Severe dmeasure/rmeasure distributional mismatch

The `dmeasure` function uses `dnbinom(x=count, mu=s, size=theta)` where `s` is a state variable (appearing nowhere in `statenames` or `paramnames`) and `theta` is also undeclared. The `rmeasure` function uses `rbinom(n=1, size=H, prob=rho)`. These are entirely different distributions: `dmeasure` specifies a negative binomial with mean `s` and overdispersion `theta`, while `rmeasure` specifies a binomial with size `H` and success probability `rho`. As documented in the `pomp-inference-misuse` skill, this means the likelihood evaluated by the particle filter and the forward simulations reflect different models. Neither `s` nor `theta` are declared in `paramnames`, so `s` would default to zero in C, making `dnbinom(x, mu=0, size=0)` almost certainly produce degenerate likelihood values. This explains why the particle filter crashed for the author.

**Fix:** Align `dmeasure` and `rmeasure` to use the same distribution family and parameters. A consistent negative binomial specification would be: `dmeasure = dnbinom(x=count, mu=rho*H, size=theta, log=log)` and `rmeasure = rnbinom(n=1, mu=rho*H, size=theta)`, with both `rho` and `theta` declared in `paramnames`.

---

### 3. Deterministic ODE SIR fitted by RSS on cumulative cases — not a POMP model

The main mechanistic model presented (the "SIR Process" section) uses `deSolve::ode()` with `optim()` minimizing residual sum of squares between the ODE's infected compartment `I` and cumulative reported cases. This is not the same as the POMP SIR object defined earlier. Fitting a deterministic ODE to cumulative cases by RSS: (a) treats cumulative counts as if they are the infected compartment `I` (which tracks currently infected individuals, not cumulative cases), (b) ignores observation noise and overdispersion, (c) provides no likelihood-based uncertainty quantification, and (d) is not comparable to the ARIMA log-likelihood. Per Wheeler et al. (2024), fitting a deterministic model to stochastic data distorts parameter estimates because unmodeled stochastic variation is absorbed by other parameters.

**Fix:** If a deterministic model is used, at minimum specify a measurement model and compute the residual likelihood on the appropriate scale. Alternatively, use a stochastic POMP SIR with proper particle filter inference.

---

### 4. No benchmark comparison between mechanistic and non-mechanistic models

The ARIMA(5,2,4) model is fitted in the first section and the SIR model in the second, but no quantitative comparison is made between them. The author states only that "the SIR model seems to show the cycle of the virus better than the POMP model I was able to achieve." This visual impression is not a quantitative comparison. Per Wheeler et al. (2024), mechanistic models must be compared against non-mechanistic benchmarks using log-likelihood or AIC to assess whether the mechanistic model captures meaningful structure. Without this comparison, it is impossible to judge whether the SIR model offers any improvement over ARIMA(5,2,4).

**Fix:** Evaluate the ARIMA and POMP models on the same data and observation scale and compare log-likelihoods. Note that direct comparison requires that both models use the same observation model (e.g., Gaussian on differenced data for ARIMA vs. negative binomial on original counts for POMP may not be directly comparable).

---

### 5. No quantitative goodness-of-fit for the mechanistic model

The final SIR model assessment is entirely visual: three plots of cumulative incidence vs. fitted ODE curves are shown with no reported RSS value, no R-squared, no AIC, and no log-likelihood. Wheeler et al. (2024) state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The text claims "the model still isn't a perfect fit" but provides no quantification of how imperfect.

**Fix:** Report at minimum the RSS and/or AIC from the `optim()` call (`Opt$value`). For a proper POMP model, report the log-likelihood from the particle filter.

---

### 6. Model fitted to cumulative cases, but POMP object observes daily new cases

The POMP object is built using `Seven.day.Average` (daily new case rolling averages) as the observation. The deterministic ODE SIR is initialized with `I = dat$Cumulative.Cases[1]` and fitted to `dat$Cumulative.Cases` — the cumulative incidence. These are two distinct data types. The infected compartment `I` in a standard SIR model represents current infections, not cumulative cases. Matching `I(t)` to cumulative `C(t)` is biologically incorrect: the cumulative curve monotonically increases while `I(t)` rises and falls. The visual match in the plot (the red `I` curve rises and then falls, while the blue cumulative points continue to rise) demonstrates this mismatch explicitly — the model is being fit to data it cannot represent.

**Fix:** Either fit the ODE to new daily cases by computing dI/dt as the flow into I, or accumulate total infections and compare to cumulative data. In a proper POMP model, `H` (the accumulator variable) counts new infections per observation period, linked to reported new cases.

---

### 7. Parameter identifiability and uncertainty not assessed

No profile likelihoods, confidence intervals, or standard errors are reported for any parameters. The recovery rate `mu_IR = 1/15` is fixed by cross-correlation analysis without acknowledgment that this is a strong assumption, and no sensitivity analysis is performed. The parameters `beta = 0.0088` and `gamma = 0.0458` from the ODE fit are reported without any uncertainty. Per Wheeler et al. (2024), profile likelihoods should be computed for key parameters to assess identifiability.

**Fix:** Compute profile likelihoods for at least `beta`, `gamma`, and the reporting rate `rho`. Report confidence intervals via the Monte Carlo Adjusted Profile (MCAP) method.

---

### 8. Recovery rate estimated by lagged cross-correlation — ad hoc calibration

The recovery rate `mu_IR = 1/15` is estimated by finding which lag maximizes cross-correlation between new cases and new recoveries. While this is a creative approach, it is an ad hoc calibration that does not account for uncertainty in the lag estimate, does not propagate that uncertainty into the model, and does not constitute likelihood-based inference. The cross-correlation plot shows noisy patterns with no clear dominant lag — using lag 15 as a point estimate from a noisy cross-correlation function understates the parameter uncertainty substantially.

**Fix:** Estimate `mu_IR` jointly with other parameters via likelihood maximization. If a literature-based prior is preferred, use a Bayesian approach that propagates prior uncertainty.

---

### 9. No model diagnostics presented

No conditional log-likelihood plots, no effective sample size monitoring from the particle filter, and no residual analysis are presented. The filtering distribution is never compared to forward simulations. The only diagnostic shown is the ARIMA residual check (via `checkresiduals`). Per Wheeler et al. (2024), diagnostic tools must be applied to understand where and how the model succeeds or fails.

**Fix:** For the ARIMA model, the `checkresiduals` output is adequate. For the SIR model, plot residuals from the ODE fit over time. For a properly implemented POMP model, plot per-observation log-likelihoods and monitor effective sample size.

---

### 10. Forecast methodology absent

No forecasts are made from either model. The conclusion states that "the virus is beginning to be in decline" based on a visual interpretation of the fitted curves — this is not a formal forecast. Per Wheeler et al. (2024), forecasts should be generated from the filtering distribution (conditioning on all observed data), propagating parameter uncertainty into forecast intervals.

**Fix:** Generate forward simulations from the fitted model conditioned on all available data to produce probabilistic forecasts with uncertainty bands.

---

## Minor Issues

### 11. ARIMA model order selection uses d=2 throughout the grid search without justification

The AIC table grid search fixes `d=2` for all (p,q) combinations (`arima(data1, order=c(p,2,q))`). Differencing twice is unusual for epidemiological count data and suggests possible over-differencing. The stationarity of the seven-day average series after one difference should be assessed (e.g., via ADF or KPSS test) before committing to d=2. No stationarity tests are reported.

---

### 12. The parameter `s` in `dmeasure` is not declared and is not a state variable

In the `sir_dcovid` function, `dnbinom(x=count, mu=s, size=theta)` uses `s` as the mean of the negative binomial. However, `s` is not listed in `statenames=c("S","I","R","H")` nor in `paramnames=c("Beta","mu_IR","N","eta","rho")`. In C, undeclared variables default to zero, so `dnbinom(x, mu=0, size=0)` is evaluated. The parameter `theta` similarly appears in `dmeasure` but not in `paramnames`. This is the proximate cause of the particle filter crashing.

---

### 13. Initial population fractions produce biologically implausible initialization

The `rinit` function sets `S = round(N*eta)` with eta defaulting to 0.05, and `R = round(N*(1-eta))`, meaning 95% of Utah's population (approximately 3.1 million people) is initialized as recovered at the start of the pandemic (March 2020). This is epidemiologically implausible: in March 2020 essentially no one had recovered from COVID-19. The initialization should have `S ≈ N`, `I` small, and `R = 0`.

---

### 14. ACF interpretation is vague and incorrect

The text states "there is no clear lag pattern, as there is not a better ACF than the unadjusted or lagged data." The ACF of the seven-day rolling average shows clear and sustained autocorrelation at many lags (the bars extend far outside the confidence bounds), which is the standard signature of a non-stationary or slowly decaying autocorrelation structure. The conclusion that "no further data adjustments were done" appears to be based on a misreading of the ACF plot.

---

### 15. Prose contains several typographical and grammatical errors

Multiple words are misspelled throughout: "diognostics" (diagnostics), "acurate" (accurate), "succeptable" (susceptible), "dieseas" (disease), "acf" (ACF), "caluclating" (calculating), "numerics" (likely meant "numerical optimization"). The text also uses inconsistent capitalization for "SIR" vs. "Sir." These issues do not affect the analysis but detract from readability.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
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
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project09/blinded.Rmd`
