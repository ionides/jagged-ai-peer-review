# Peer Review: W24 Project 11
### NVIDIA Stock Price Analysis via ARMA, GARCH, and POMP Models

---

## Summary

This project fits three model families — ARMA, ARMA-GARCH, and a stochastic volatility POMP model — to daily log-returns of NVIDIA stock prices from January 2022 to April 2024. The paper follows a reasonable pedagogical arc: exploratory data analysis, ARMA model selection via AIC and likelihood ratio tests, GARCH model comparison, and a leverage-effect stochastic volatility model in the POMP framework. The ARMA-GARCH(1,1) with t-errors is selected as the best model based on log-likelihood.

Strengths include a well-motivated stochastic volatility model with explicit POMP representation, use of iterated filtering (IF2) at a reasonable run level, and a sensible model-building narrative. However, the project has several serious weaknesses: (1) the final log-likelihood comparison across models is statistically invalid because models use different observation distributions; (2) the global IF2 search is initialized from a previous mif2 result rather than the base pomp object, invalidating its claim to global coverage; (3) the initial particle filter is run on simulated data rather than real data, making its reported value incomparable to subsequent IF2 results; (4) no profile likelihoods are computed for any parameter; and (5) several methodological claims in the text contain factual errors. These issues collectively undermine the reliability of the conclusions.

---

## Major Issues

### 1. Global IF2 search anchored to local search result (invalidates global coverage claim)

In the global search chunk (lines 514-516), the `mif2()` call uses `if1[[1]]` as its first argument:

```r
if.box <- foreach(i=1:nv_Nreps_global,
  .packages='pomp',.combine=c) %dopar% mif2(if1[[1]],
    params=apply(nv_box,1,function(x)runif(1,x)))
```

The correct pattern is `mif2(nv.filt, params=...)`, where `nv.filt` is the base pomp object. By passing `if1[[1]]` (a previous mif2 result), all 80 global replicates inherit the internal IF2 state and cooling schedule of the local chain, which has already decayed to near-zero perturbation magnitude after 150 iterations. The new random starting values from the box are applied via `params=`, but the cooling schedule is fully depleted, meaning almost no parameter exploration occurs from those new starts. The reported "global maximum" is therefore not meaningfully different from the local search result, as the authors themselves note ("no significant improvement was observed compared to local search"). The fix is to replace `mif2(if1[[1]], ...)` with `mif2(nv.filt, ...)` in the global search loop. (See Wheeler et al. 2024 and pomp-global-search-init-audit skill.)

### 2. Initial particle filter evaluated on simulated data, not real data

The chunk at lines 430-434 evaluates the particle filter on `sim1.filt`, which is a pomp object constructed from a simulated realization of the model, not from the real NVIDIA log-return data:

```r
pf1 <- foreach(i=1:nv_Nreps_eval,
  .packages='pomp') %dopar% pfilter(sim1.filt, Np=nv_Np)
```

The log-likelihood from filtering simulated data is on an entirely different scale than the log-likelihood from filtering real data, because the two datasets are different. Any comparison of this "benchmark" value to subsequent IF2 log-likelihoods (which are computed on `nv.filt`, the real-data object) is invalid. The initial particle filter should be run on `nv.filt` at `params_test` to establish a real-data baseline. (See pomp-simdata-benchmark-error skill.)

### 3. Invalid cross-model log-likelihood comparison in the Conclusion

The Conclusion (line 550) states: "ARMA(0,0) give us the likelihood of 1092, the ARMA(0,0)-GARCH(1,1) model give us likelihood of 1120, while the POMP model ... give us likelihood of 1110." These three log-likelihoods cannot be numerically compared because they are computed under different observation models on (arguably) different transformations of the data:

- The ARMA(0,0) likelihood assumes Gaussian errors.
- The ARMA-GARCH-t likelihood uses a Student-t conditional distribution.
- The POMP measurement model (`dmeasure`) uses `dnorm(y, 0, exp(H/2), give_log)`, a Gaussian conditional on the latent log-volatility.

A direct numerical comparison of log-likelihoods across these three families is not valid and cannot be used to select a "best" model. A proper comparison would require evaluating all models under a common observation model, or using a proper scoring rule (e.g., CRPS). The ARMA-GARCH model's apparent superiority may be entirely an artifact of its heavier-tailed t-distribution absorbing the extreme log-returns that are poorly accommodated by the Gaussian POMP measurement model.

Additionally, there is an internal inconsistency: the text in the ARMA section reports a log-likelihood of 1087 for ARMA(0,0) (line 259), but the Conclusion reports 1092. The GARCH normal model is also reported as having likelihood 1092 (line 283), identical to the ARMA(0,0) value cited in the Conclusion — these appear to be different quantities accidentally given the same number.

### 4. No profile likelihoods; parameter identifiability not assessed

The project reports point estimates from the global search but presents no profile likelihoods for any parameter. Without profiles, it is impossible to assess whether parameters such as `sigma_nu`, `phi`, `sigma_eta`, or `mu_h` are identifiable from NVIDIA log-return data. The local search convergence traces (noted by the authors) show that `mu_h` and `H_0` do not converge. Combined with the global search finding that `sigma_nu` "stabilizes at 0" — a boundary value — this is strong evidence of potential non-identifiability or model misspecification that should be investigated via profile likelihoods and the MCAP procedure rather than simply noted in passing. (Wheeler et al. 2024, §Parameter identifiability.)

### 5. ADF test conclusion is inverted

Lines 157-158 state: "the test-statistic is about -7.16 and the p-value is less than 0.01, which suggest we keep the null hypothesis that our time series is stationary." This is incorrect. The null hypothesis of the Augmented Dickey-Fuller test is that a unit root is present (i.e., the series is non-stationary). A p-value below 0.01 provides strong evidence to reject the null, concluding in favor of stationarity — not that we "keep" a null of stationarity. The conclusion happens to be correct but the reasoning is backwards and should be corrected.

### 6. No benchmark comparison for the POMP model

The project does not compare the POMP stochastic volatility model against any non-mechanistic benchmark on the same footing. Even within the GARCH literature, a GARCH(1,1)-t is a strong benchmark for stochastic volatility models: both capture volatility clustering, but GARCH has a closed-form likelihood while the POMP model requires particle filtering. A meaningful evaluation would compute log-likelihoods for both models under the same observation model and data. As Wheeler et al. (2024) note, none of 32 cholera papers they reviewed performed such a comparison, and benchmark failures exposed important model deficiencies. For financial time series, the GARCH family constitutes the natural non-mechanistic benchmark.

### 7. No model diagnostics for the POMP model

The POMP section lacks all standard model diagnostics: no effective sample size (ESS) monitoring during particle filtering, no conditional log-likelihood plots by time step, no comparison of filtered trajectories to forward simulations from initial conditions, and no examination of the reconstructed latent log-volatility H_n for plausibility. The convergence traces shown (`plot(if1)`, `plot(if.box)`) indicate parameter traces but not the quality of the particle filter approximation. Without ESS monitoring, it is unknown whether the particle filter is degenerating silently, which would make all reported log-likelihoods unreliable. (Wheeler et al. 2024, §Model diagnostics.)

---

## Minor Issues

- **K-period log-return formula error (line 95):** The formula states r_t(k) = log(X_t / X_{t-1}), which is the 1-period return, not the k-period return. The correct expression for the k-period log return is log(X_t / X_{t-k}) = r_t + r_{t-1} + ... + r_{t-k+1}. The right-hand additive decomposition is correct but the left-hand equality with log(X_t/X_{t-1}) is wrong.

- **Hard-coded local file path (line 45):** `setwd("/Users/huanglingqi/Desktop/Stats 531 Final Project")` is a machine-specific absolute path that will cause the document to fail to render on any other system. All file paths should be relative to the project root, or the data file should be read directly with a relative path.

- **NVIDIA data file not included:** The dataset `NVDA.csv` is read from a local directory but is not present in the submitted project folder. Without this file, the document cannot be reproduced. The data should be included in the submission or downloaded programmatically.

- **Inconsistent log-likelihood values between sections:** The ARMA(0,0) log-likelihood is reported as approximately 1087 in the ARMA section (line 259) but as 1092 in the Conclusion (line 550). These should be reconciled, and if they differ due to a rerun, this should be noted.

- **GARCH(1,1) discarded for wrong reasons (lines 273-274):** The GARCH(1,1) model fitted with the `garch()` function uses Gaussian errors. The authors report coefficients (α₀=0.0011, α₁=0.0499, β₁=0.05) and discard the model because "p-values for three coefficients are greater than 0.1." However, β₁=0.05 seems implausibly small for a GARCH(1,1) applied to daily stock returns — typically β₁ > 0.8. This may indicate a fitting issue with the `garch()` function from the `tseries` package (known to be less reliable than `rugarch` or `fGarch`). The subsequent ARMA-GARCH via `fGarch::garchFit()` is more appropriate but the comparison should be made explicit.

- **Shapiro-Wilk test on residuals (line 256):** The Shapiro-Wilk test is reliable for sample sizes up to ~5000 observations. With ~540 daily observations, it is applicable, but the text should report the test statistic and p-value rather than just asserting non-normality.

- **ARMA(0,0) selected without acknowledging volatility clustering:** The Ljung-Box test on returns fails to reject independence (p≈0.325), which the authors use to justify ARMA(0,0). However, Ljung-Box on squared returns would test for ARCH effects. The decision to then fit a GARCH model is correct, but the logical path should explicitly note that while linear serial correlation is absent, conditional heteroskedasticity (nonlinear dependence) may still be present.

- **Missing root plot for ARMA(0,0):** The text discusses plotting roots for ARMA(0,1) and ARMA(1,0) (lines 198-214) but ARMA(0,0) has no AR or MA polynomial. The root plot is unnecessary for the selected model and the text should clarify this.

- **Convergence comment overstated (line 546):** The text states "sigma_nu stabilizes at 0" and "sigma_eta tends to converge around 5." A sigma_nu value at or near zero is a boundary estimate suggesting the leverage random walk G_n is nearly constant — this is scientifically important and should be interpreted in the context of whether leverage effects are present in NVIDIA stock, not simply reported as convergence.

- **Missing sessionInfo() or package version documentation:** No software version information is provided. Given that the `pomp` API has changed substantially across versions, this is a reproducibility concern.

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

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project11/Stats 531 Final Project.Rmd`
