# Peer Review: W24 Project 02
## "Investigating the alternative prey hypothesis with the POMP framework"

---

### Summary

This project applies the POMP framework to model willow ptarmigan population dynamics in Norway using 142 years of harvest data (1872-2012), motivated by the alternative prey hypothesis. The model draws on a modified Lotka-Volterra system with fox and bird population states and a rodent covariate. An ARIMA baseline is also fit. The writeup is readable and the scientific motivation is interesting, but the POMP implementation has serious technical deficiencies that undermine the analysis.

---

## Weaknesses (prioritized by severity)

### 1. MAJOR: POMP model log-likelihood is worse than the ARIMA baseline, with no adequate explanation

The global search yields a best log-likelihood of -176.3, the local search yields approximately -134, and the ARIMA(0,1,5) baseline yields -99.32. These are not comparable — the ARIMA is fit to differenced data while the POMP model is fit to the level series — yet the authors directly compare these values and treat the discrepancy as a computational resource problem ("we limit the parameter space to save the running time"). This is a fundamental methodological error. The log-likelihoods cannot be compared on equal footing without accounting for the Jacobian of the differencing transformation. The conclusion that "ARMA model is fitting the data better" based on this comparison is not validly supported.

### 2. MAJOR: Fox population is a latent state with no data, making the model unidentifiable

The model posits two latent states: log fox population (logF) and log bird population (logB). Only logCPUE, a proxy for bird abundance, is observed. Fox population density is never observed and no fox data is incorporated. With only a single observation equation linking logCPUE to logB, there is effectively no data to inform the fox state. The model is severely underidentified: with 12 parameters and a single observation per time point, the fox dynamics are unconstrained by the data, and the filter is fitting noise. The authors acknowledge the particle degeneracy issue but do not connect it to this structural identifiability problem.

### 3. MAJOR: Particle filter uses Np=5 for likelihood evaluation after mif2

In the local search section, log-likelihood evaluation after a single mif2 run uses only `Np=5` particles:

```r
foreach (i=1:10, .combine=c, ...) %dofuture% {
  mif2_out |> pfilter(Np=5)
} -> pf
```

Five particles is an extremely small number, producing highly variable and unreliable likelihood estimates. The resulting log-likelihood of -205 (SE=3.14) is essentially meaningless given this variance. The global and local search scripts use larger Np (100-500), but the summary statistics reported in the narrative rely on this inadequate evaluation.

### 4. MAJOR: Same noise process W_t^F is applied to both fox and bird equations

In both Equations (1) and (2), the stochastic term is labeled $W_t^F$. The bird equation in the text reads:

$$\log B_{t+dt} = \log B_t + dt(\alpha + \beta \exp(\log F_t)[1 - \gamma R_t])W_t^F$$

However, in the actual code the bird step uses `dwB = rgammawn(sigmaB, dt)` independently of `dwF`. This is an inconsistency between the mathematical presentation and the implementation. If the intention is that fox and bird dynamics share a noise source, the code is wrong; if the bird has independent noise, the equation notation is wrong and the biological interpretation changes.

### 5. MAJOR: Negative binomial measurement model stated but normal distribution implemented

The text states: "The measurement model $Y(t)$ is our ptarmigan count proxy, logCPUE, $y(t) = \text{Negative Binomial}(mean=\rho\beta_t, \sigma)$." The actual code uses a normal distribution:

```r
rmeas: logCPUE = rnorm(logB - logRho, sigma_obs)
dmeas: lik = dnorm(logCPUE, logB - logRho, sigma_obs, give_log)
```

This is a direct contradiction between the stated model and the implemented model. The negative binomial is appropriate for count data but logCPUE is a continuous log-transformed variable, so the normal may be more defensible in practice — but the description must match the implementation.

### 6. MAJOR: logCPUE is removed from the pomp object during model setup

In the code, `bird1 <- bird |> dplyr::select(-R)` selects only the columns not including R, keeping year and logCPUE. However, the covariate table construction uses `bird |> dplyr::select(year, R)`. This appears correct, but the `obs_names` argument is set inline within the `pomp()` call using `<-` assignment (`obs_names <- c("logCPUE")`) rather than a named argument. This is a code error: the `obs_names` argument to `pomp()` is not a valid argument and will be silently ignored or cause unexpected behavior; the correct argument is `obsnames`. The observed variable name is set implicitly by the column name in the data, but this makes the code misleading and unreliable.

### 7. MAJOR: Global search range is extremely narrow and biologically unmotivated

The global search uses a very tight uniform design:

```r
lower = c(alpha=0, Beta=0, ..., a=7, b=2, logF_0=0.4, logB_0=1.6, ...)
upper = c(alpha=0.1, Beta=0.1, ..., a=8, b=3, logF_0=0.5, logB_0=1.7, ...)
```

The range for `alpha` (birth rate) is 0 to 0.1, and for `Beta` (predation) is 0 to 0.1, while from the local search `a` is fixed near 7-8. These ranges are not derived from biological knowledge or from the local search results. The global search is not genuinely global — it is a narrow refinement around an ad hoc region, and critically it uses `fixed_params <- coef(mif2_out)` to fix all parameters not listed in the `guesses`, which means most parameters are held at the single mif2 result rather than being varied.

### 8. MAJOR: Local search convergence diagnostics are presented only as static images with absolute file paths

The convergence trace plots are included as image embeds via absolute local paths (`/Users/ruojunliu/Desktop/...`), making the report non-reproducible on any other machine. All local search code is set to `eval=FALSE`, so the plots are pre-generated figures. There is no way to verify the convergence results from the submitted materials. The `.rds` files (`local_search.rds`, `Q_fit_bird_local_mifs.rds`) suggest some results were saved, but these are not connected to the narrative in the report.

### 9. MINOR: Parameter transformation applies log transform to parameters that can be negative or zero

The parameter transformation applies `log` to all 12 parameters including `alpha`, `Beta`, `gamma`, `b`, `c`, `a`. While constraining these to be positive may be biologically motivated, the model does not discuss this constraint. Notably, `beta` in the bird equation represents a mortality term, so `logB += ... - Beta*exp(logF)*...` with Beta forced positive is correct, but `alpha` representing bird birth rate is also forced positive. The gamma parameter, representing predation efficiency reduction, is also log-transformed, yet the term `(1 - gamma*R)` could become negative if `gamma > 1`, which the log-transform does not prevent since gamma could still be large.

### 10. MINOR: The `logRho` parameter naming and use is confused

The parameter is named `logRho` and initialized as `logRho = 3`, but it enters the measurement equation as `logCPUE ~ N(logB - logRho, sigma_obs)`. This means logRho acts as an additive offset in log space (i.e., a scaling factor between bird population and CPUE). However, the text describes $\rho$ as the mean of the negative binomial, and the equation $mean = \rho \beta_t$ mixes multiplicative and additive interpretations. The parameter transformation applies `log` to `logRho`, meaning the actual parameter used internally is `exp(logRho)`, further compounding confusion about its interpretation.

### 11. MINOR: ARIMA model selection has a label error in the text

The text states "Figure \@ref(fig:trend), the partial correlation dies out after 5 lags" but the correct reference should be to Figure \@ref(fig:pacf). This is a copy-paste error that affects the readability of the correlation analysis section.

### 12. MINOR: Only 2 rows appear in bird_params_middle.csv, suggesting the global search nearly failed

The saved global search results file `bird_params_middle.csv` contains only 2 rows of finite log-likelihood results (out of 50 guesses). The code filters `filter(is.finite(loglik))`, meaning 48 of 50 starting guesses resulted in non-finite likelihoods (likely -Inf). This is a very high failure rate for the particle filter and indicates the model is numerically fragile across most of the parameter space, yet this is not discussed.

### 13. MINOR: No profile likelihood or confidence intervals are computed for any parameter

The analysis jumps from local/global search directly to a conclusion without ever computing profile likelihoods, confidence intervals, or any measure of parameter uncertainty. For a POMP model with 12 parameters, some assessment of identifiability and uncertainty is essential, particularly given the identifiability concerns noted above.

### 14. MINOR: The `dt=1/52` step size (weekly) is not justified

The Euler step size `delta.t=1/52` simulates weekly dynamics for annual data. While small step sizes can improve Euler accuracy, this dramatically increases computation cost and is not discussed. For a model with annual observations and annual covariates (rodent peak years), a weekly step size introduces sub-annual dynamics that cannot be informed by or validated against data.

### 15. MINOR: Bibliography file path is hardcoded to an absolute local path

The YAML header contains `bibliography: /Users/ruojunliu/Desktop/references.bib`, which will fail on any machine other than the author's. The image embeds similarly use absolute paths throughout. The report as submitted cannot be rendered by any other user.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project02/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project02/bird_params_middle.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project02/README.md`
