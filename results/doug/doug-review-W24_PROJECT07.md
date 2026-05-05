# Peer Review: W24 Project 07
## Time Series Analysis of Apple Inc. (AAPL) Stock Price

---

## Summary

This project fits ARIMA, GARCH, and POMP (stochastic leverage) models to the daily log-returns of AAPL stock from April 2020 to April 2024. The POMP section applies iterated filtering (IF2) with a Bretó (2014)-style stochastic leverage model, reporting a local-search maximum log-likelihood of approximately 2650 and a global-search maximum of approximately 2655. While the project covers a reasonable breadth of modeling approaches and provides convergence diagnostics, it contains several critical methodological errors — most notably the global search initialization anti-pattern that invalidates the global optimum claim, a severe discrepancy between the particle-filter benchmark log-likelihood (−1501) and the local/global search reported values (2650/2655), an absence of any benchmark comparison, and the lack of profile likelihoods. These issues collectively undermine the validity of the quantitative conclusions.

---

## Major Issues

### 1. Global search initialized from a previous mif2 result object (anti-pattern)

In the global search code chunk, the `mif2()` call uses `if1[[1]]` — a previous IF2 result object — as its first argument:

```r
if.box <- foreach(i=1:AAPL_Nreps_global, .packages="pomp", .combine=c) %dopar%
  mif2(if1[[1]], params=apply(AAPL_box,1,function(x)runif(1,x)))
```

This is the anti-pattern documented in the `pomp-global-search-init-audit` skill. Passing a previous `mif2` result as the first argument causes the global search to inherit the internal IF2 state and cooling schedule from `if1[[1]]`, which is already at or near its final (decayed) cooling state after 100 iterations. The new random starting parameters from the box are applied, but the perturbation schedule has already cooled nearly to zero, so the optimizer performs little meaningful exploration from those new starting points. The reported global maximum of 2655 may simply replicate the local-search solution rather than reflecting a true global optimum. The correct pattern is `mif2(AAPL_filter, params=apply(AAPL_box,1,...))`, where `AAPL_filter` is the base `pomp` object.

**Fix:** Replace `mif2(if1[[1]], ...)` with `mif2(AAPL_filter, ...)` in the global search `foreach` loop, then rerun to verify whether the global maximum changes.

---

### 2. Irreconcilable log-likelihood discrepancy between particle filter benchmark and IF2 results

The particle filter evaluation on `sim1.filt` (a simulated dataset, not the real AAPL data) returns a log-likelihood of approximately −1501. However, the local search and global search report log-likelihoods of approximately 2650 and 2655, respectively. These values differ by over 4,000 units and have opposite signs, yet no explanation is provided. The most likely cause is that the initial particle filter evaluation is performed on `sim1.filt` (a simulated dataset generated from `params_test`) rather than on `AAPL_filter` (the actual data), while the IF2 searches are performed on `AAPL_filter`. The text treats all three values as if they are comparable benchmarks on the same model and data ("This could serve as an initial benchmark..."), which is misleading at best and an error in logic at worst. The values cannot be directly compared because they are evaluated on different datasets.

**Fix:** Clarify that the initial particle filter evaluation is on a simulated dataset. Re-run the initial particle filter on `AAPL_filter` at the test parameters so the values are on the same scale and provide a meaningful benchmark for the IF2 improvement.

---

### 3. No benchmark comparison against a non-mechanistic model

The POMP model's fit is never compared quantitatively to a non-mechanistic benchmark. The ARMA(1,1) and GARCH models are discussed descriptively, but no common likelihood or information criterion is reported that would allow a fair comparison of all three modeling approaches. Without such a comparison it is impossible to assess whether the mechanistic stochastic leverage POMP model captures meaningful structure beyond what the simpler GARCH models already explain. Wheeler et al. (2024) identify benchmark comparison as one of the most diagnostically valuable practices in POMP modeling. Given that GARCH-family models are specifically designed for financial volatility, the burden of proof is particularly high that the POMP model adds explanatory value.

**Fix:** Evaluate ARMA(1,1), GARCH(1,1)-t, and the POMP model on the same log-return series and report log-likelihood values under a common (or equivalent) observation model, or report AIC for each.

---

### 4. No profile likelihoods; parameter identifiability unaddressed

No profile likelihoods are computed for any parameter. The global pairs plot (global.png) shows that `sigma_eta` takes values across a very wide range (0 to ~30) and `sigma_nu` is concentrated near zero, yet these observations are not discussed in terms of identifiability. The local pairs plot also shows `sigma_eta` ranging from roughly 0 to 30 across the 20 local search replicates with no clear concentration near the MLE. The authors remark in passing that "`sigma_nu` > 0 is not supported" and that "`phi` doesn't show convergence (weakly identified)," but make no attempt to quantify the uncertainty or determine whether these parameters are identifiable. Wheeler et al. (2024, §Parameter identifiability) require profile likelihoods and confidence intervals (e.g., MCAP) for all key parameters.

**Fix:** Compute profile likelihoods for at least `phi`, `sigma_eta`, and `sigma_nu`. Report MCAP confidence intervals. Discuss whether the flat profile for `sigma_nu` indicates the model cannot distinguish this parameter from zero.

---

### 5. Computational adequacy is insufficient: only Np=1000 particles and Nmif=100 iterations

The reported settings at `run_level=3` are `Np=1000` and `Nmif=100`. For a daily financial return series of ~1000 observations, 1000 particles is borderline for a model with three state variables. The local-search ESS diagnostic (`local_d1.png`) shows ESS collapsing repeatedly to near zero throughout the filtering period, indicating substantial particle degeneracy. The global-search ESS diagnostic (`global_d1.png`) shows similar behavior. ESS collapse produces unreliable likelihood estimates and can cause IF2 to track noise rather than the true likelihood surface. Wheeler et al. (2024, §Computational adequacy) specifically note that increasing the number of particles was a primary driver of log-likelihood improvement in their analysis. The local search runs 20 replicates (`AAPL_Nreps_local=20`), which is reasonable, but the global search runs 100 replicates at only 1000 particles, which may be trading breadth for depth inappropriately.

**Fix:** Increase `Np` to at least 2000–5000 and verify that the reported log-likelihood is stable across independent particle filter evaluations. Report the standard error of the log-likelihood estimate from the particle filter replications as evidence of adequacy.

---

### 6. Measurement model uses deterministic observation equation without likelihood specification in text

The measurement model (rmeasure) is `y = Y_state`, a deterministic assignment. The dmeasure is `lik = dnorm(y, 0, exp(H/2), give_log)`, which evaluates the Gaussian likelihood for the observation given the state. This is internally consistent for a Gaussian observation model. However, the text does not write out the measurement model as a probability distribution anywhere in the model specification. The mathematical description only provides the process model equations. The reader cannot verify that the code implements what was intended without cross-referencing the Csnippets. Wheeler et al. (2024, §Measurement model specification) require the measurement model to be explicitly specified in the manuscript, not just implemented in code.

**Fix:** Add a line to the model specification stating that $Y_n | H_n \sim N(0, \exp(H_n/2))$, with the observation $y_n$ given by this distribution, making clear the Gaussian measurement assumption.

---

### 7. Local search variable naming error: `local_results` written instead of `r.if1`

In the local search code, the results are stored in `r.if1 = data.frame(...)` but the write.table call attempts to write `local_results`:

```r
write.table(local_results, file = "AAPL_params2.csv", ...)
```

The variable `local_results` is never defined in this code chunk. This would cause an error at runtime. The text then states "the maximum of estimated log likelihood is 2650" — this result must come from the pre-saved `mif1-3_2.rda` artifact rather than the inline code as written, since the inline code would fail. This discrepancy creates a reproducibility gap: the code chunk as written cannot produce the reported results.

**Fix:** Replace `local_results` with `r.if1` in the `write.table` call.

---

### 8. No model diagnostics: conditional log-likelihoods not examined

No conditional (per-time-step) log-likelihoods are plotted. The filter diagnostics plots (`local_d1.png`, `global_d1.png`) show ESS over time and a `cond.logLik` panel, but the conditional log-likelihood panel is present in the diagnostic output without being explicitly discussed. The authors do not identify any time periods where the model fits poorly, nor do they connect the ESS collapses to specific market events (e.g., the COVID volatility spike in 2020 or rate-hike volatility in 2022). Wheeler et al. (2024, §Model diagnostics) emphasize that conditional log-likelihood plots are essential for identifying model failures and guiding model development.

**Fix:** Explicitly plot and discuss per-observation conditional log-likelihoods. Identify the dates corresponding to ESS collapse and discuss whether they correspond to events outside the model's design scope.

---

### 9. Global search box is poorly specified for some parameters

The global search box specifies:
- `mu_h = c(-1, 0)` — but the local search finds best values between −8 and 4, far outside this range
- `sigma_eta = c(0.5, 1)` — but the local search pairs plot shows values from 0 to 30

The global search box is substantially narrower than the region visited by the local search for `mu_h` and much narrower than the estimated range for `sigma_eta`. If the global maximum is outside the box, the global search cannot find it. The fact that the global maximum (2655) is only marginally better than the local maximum (2650) could reflect this constraint rather than genuine convergence to a global optimum.

**Fix:** Expand the global search box to encompass the full range of values producing high log-likelihoods in the local search. In particular, `mu_h` should range at least from −10 to 2 and `sigma_eta` should have an upper bound well above 1.

---

### 10. Initial conditions not estimated or assessed for sensitivity

Initial conditions `G_0` and `H_0` are set to fixed values of 0 in `params_test` and included in the search box as `G_0 = c(-2, 2)` and `H_0 = c(-1, 1)`. No sensitivity analysis is performed on these choices, and no justification is given for the initialization range. Wheeler et al. (2024, §Initial conditions) document that initialization strategy affected AIC by ~72 units for one of their models. The text dismisses `H_0` in passing ("doesn't play an important role"), but this claim is unsupported without a systematic assessment.

**Fix:** At minimum, verify the sensitivity of the reported log-likelihood to plausible alternative initial condition values. Alternatively, include `H_0` and `G_0` in the profile likelihood computations to formally assess their impact.

---

## Minor Issues

- **Decomposition applied to financial log-returns**: The `decompose()` function (multiplicative/additive seasonal decomposition) is applied to the log-return series, which is non-seasonal and stationary. This decomposition is not meaningful for log-returns and the plot serves no analytical purpose. The ACF result that "there is no seasonality" makes the decomposition even more puzzling since the conclusion is reached before the decomposition is applied.

- **GARCH model selection criterion inconsistency**: The basic GARCH grid search uses `logLik.garch()` and selects the model with the minimum log-likelihood value (higher log-likelihood is better; minimum is worse). The code explicitly selects `min_value` and `min_index`, which would select the worst-fitting model. The asymmetric GARCH and t-GARCH searches correctly use minimum AIC. The basic GARCH selection is therefore inconsistent and likely wrong.

- **Selective log-likelihood table**: The project does not collect log-likelihood values for all GARCH variants into a single comparison table. The reader must mentally compare numbers spread across multiple narrative sections.

- **`run_level` at 3 but Np only 1000**: The run-level table shows `AAPL_Np = switch(run_level, 100, 1e3, 1e3)`, so run levels 2 and 3 both use 1000 particles. There is no high-effort configuration that increases the particle count — the highest run level does not provide additional computational resources relative to run level 2, only more replicates.

- **CatGPT citation for LaTeX**: The text cites "CatGPT [2]" (clearly ChatGPT) for writing LaTeX equations. This is not a valid academic citation and raises concerns about the intellectual contribution to the mathematical notation in the paper. The reference should be removed and the standard ARMA model equations written by the authors.

- **Data potentially non-reproducible at render time**: The data are retrieved live via `getSymbols("AAPL", ...)` from Yahoo Finance at render time. Historical Yahoo Finance data can change as corporate actions or adjustments are applied retroactively, meaning a re-render may not produce identical data. No archived snapshot of the data is provided.

- **Conclusion does not connect to quantitative results**: The conclusion states "the GARCH model proved to be the most effective in forecasting volatility" but no formal forecasting comparison is presented in the paper. The ARMA model is compared visually via a forecasting plot, but no GARCH or POMP forecast is shown. This conclusion is unsupported.

- **No `sessionInfo()` or package version documentation**: No session information is provided, making it difficult to verify that the code will run correctly with current package versions. The `pomp` API has changed across versions and results may not reproduce.

- **`phi` parameter transform inconsistency**: The `params_test` vector initializes `phi = expit(4) ≈ 0.982` and uses `logit="phi"` in `partrans`. This means `phi` is constrained to (0,1) by the logit transform, which is appropriate for an AR(1) coefficient. However, the global search box specifies `phi = c(0.95, 0.99)` on the original (not transformed) scale, which is correct given that `mif2` will transform internally. This is consistent, but the text should clarify this to avoid confusion.

- **References 3 and 4 are course materials and student projects**: Two of the six references (references [3] and [4]) are a course notes PDF and a previous student project report. These are not peer-reviewed sources for the methods being applied. The original Bretó (2014) paper is correctly cited for the model, but the implementation methodology should cite Ionides et al. (2006/2015) for IF2 rather than course slides.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/pf1-3.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/mif1-3_2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/local.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/local_d1.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/local_d2.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/global.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/global_d1.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/global_d2.png`
