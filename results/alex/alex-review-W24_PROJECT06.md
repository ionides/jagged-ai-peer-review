# Peer Review: W24 Project 06 — Volatility Analysis of NASDAQ

---

## Summary

This project fits several time series models — ARMA, GARCH (normal and t-distributed), ARMA-GARCH, and a POMP stochastic volatility model — to NASDAQ log returns over a five-year period (April 2019 to April 2024). The POMP component follows the Bretó (2014) leverage-effect stochastic volatility framework closely modeled after course notes. The project is readable but has a number of significant methodological, inferential, and presentational deficiencies detailed below.

---

## Weaknesses (Most Critical First)

### 1. Log-likelihood Values Are Not Comparable Across Models (Major)

The report compares ARMA(4,4) log-likelihood (3324.91), GARCH(4,1) normal log-likelihood (3476.55), GARCH(1,1)-t log-likelihood (3538.77), ARMA(4,4)+GARCH(1,1) log-likelihood (3550.09), and POMP log-likelihood (3510) as if they are directly comparable. They are not. The `rugarch` `likelihood()` function returns the *likelihood* (not log-likelihood), and `log(likelihood(...))` returns the log of the total likelihood only if `likelihood()` itself returns the summed likelihood. More critically, the ARMA log-likelihood from `arima()` is in a different scale/normalisation than those from `rugarch`. No verification is provided that all likelihoods are evaluated on the same observations using the same normalisation convention. The conclusion that ARMA+GARCH beats the POMP model therefore rests on an apples-to-oranges comparison.

### 2. POMP Global Search Does Not Explore a Meaningful Parameter Space (Major)

The global search box defined for the POMP model is:
- `sigma_nu` in (0.005, 0.05)
- `mu_h` in (-1, 0)
- `phi` in (0.95, 0.99)
- `sigma_eta` in (0.5, 1)

These ranges are extremely narrow and are chosen based on the local search, which itself was initialised from a single fixed starting point (`params_test`). The local search summary reports that `mu_h` converges to approximately -10 and `sigma_eta` ranges up to 50, yet the global search box contradicts these findings by using (-1, 0) and (0.5, 1) respectively. The global search therefore does not qualify as a genuine global search and likely misses better regions of the likelihood surface.

### 3. Key Parameters Do Not Converge in MIF2 (Major)

The authors acknowledge that `H_0` and `mu_h` do not converge in the MIF2 filter convergence plots. Despite this, no corrective action is taken: no re-parameterization, no extended cooling schedule, no additional iterations, and no revised parameter box is proposed. Non-convergence of `mu_h` is particularly consequential because it is a core structural parameter (the long-run mean of log-volatility). Presenting final parameter estimates and likelihood values under non-convergence without remediation is a significant inferential flaw.

### 4. Particle Filter Evaluation Is Run on a Simulated Object, Not the Real Data Object (Major)

In the particle filtering step, `pf1` is computed on `sim1.filt`, which is the POMP object constructed from a *simulated* trajectory (`sim1.sim`), not on `NADQ.filt` which contains the actual observed data. The subsequent local MIF2 is correctly run on `NADQ.filt`, but the initial particle filter likelihood evaluation step is therefore not a meaningful likelihood evaluation on the real data and its reported value is misleading.

### 5. ACF/PACF Interpretation Is Incorrect (Major)

The report states: "The number of significant spikes in the ACF plot is 1, hence, we can assume that the AR term has value 1. Likewise, the number of significant spikes in the PACF plot is 4. Hence, it can be inferred that the MA term is 4." This reverses the standard interpretation: the ACF is used to identify the MA order (trailing off or cutting off after q lags), while the PACF is used to identify the AR order (cutting off after p lags). The stated logic is backwards and leads to incorrect model identification reasoning, even if the final AIC table is consulted for selection.

### 6. Time Series Frequency Specification Is Incorrect (Minor/Moderate)

The data are daily stock prices and the log returns are at daily frequency. However, the code sets `ts(time_series_data$Log_Return, start = c(2019, 4), frequency = 1)`. Setting `frequency = 1` means the series is treated as annual data with no sub-annual structure. This does not affect subsequent `arima()` fitting (which ignores frequency for ARMA), but it means the axis labels on the time series plot are meaningless, and any seasonal considerations (which the authors acknowledge as a limitation) are made impossible by the data structure.

### 7. The POMP Model Description Contains Notational Inconsistency (Minor/Moderate)

In the model description section, `beta_n` is defined in the text as `beta_n = Y_n * sigma_eta * sqrt(1 - phi^2)`, suggesting it is indexed by time. However, in the Csnippet `rproc1`, `beta` is computed as `beta = Y_state * sigma_eta * sqrt(1 - phi*phi)` and used inside the same step, which is actually `beta_{n-1}` (using the previous state value of `Y_state`). The exposition does not clarify this timing convention and could mislead readers about the model's dynamics.

### 8. No Profile Likelihood or Confidence Intervals for POMP Parameters (Minor/Moderate)

The report provides no profile likelihood analysis and no uncertainty quantification for any of the estimated POMP parameters. Given that MIF2 convergence is already problematic, there is no sense of the reliability of point estimates. A pairs plot is shown but log-likelihood values span a range of 300 units (the threshold used is `max(logLik) - 300`), which is an unusually wide window that obscures parameter identifiability.

### 9. GARCH(4,1) Under Normal Noise Is Overfitted and Not Justified (Minor/Moderate)

The AIC-selected GARCH model under normal noise is GARCH(4,1), which is an unusual order. The report does not discuss whether the GARCH(4,1) model satisfies stationarity and positivity constraints (which become increasingly difficult to satisfy as p increases). No parameter estimates or standard errors for the GARCH(4,1) model are shown, making it impossible to assess whether the model is well-identified.

### 10. The `log(likelihood(...))` Output Is Misinterpreted (Minor/Moderate)

For GARCH(4,1) normal, the report states: "This model has a likelihood of 3476.553 and a log likelihood of 8.1538." The value 8.1538 is the *per-observation* log-likelihood (infocriteria scale in rugarch), not the total log-likelihood. Similarly for other GARCH models. Claiming these as the log-likelihood and comparing them with the ARMA log-likelihood of 3324.91 (which is a total) conflates two incompatible quantities.

### 11. No Simulation-Based Model Validation for POMP (Minor)

The project includes a single simulation from the initial parameter guess to show that the model does not fit well at the test parameters. However, after fitting via MIF2, there is no simulation from the estimated parameters to check whether the fitted POMP model can reproduce key features of the data (volatility clustering, heavy tails, autocorrelation in squared returns). This is a standard diagnostic step in POMP-based volatility analysis that is absent here.

### 12. Data Description Is Vague and Partially Incorrect (Minor)

The introduction states this project analyzes "NASDAQ" but the data file `NDAQ.csv` contains prices for the ticker NDAQ (Nasdaq, Inc. — the company itself), not the NASDAQ Composite Index. The price range (~$29 to ~$63) and volume are consistent with NDAQ stock, not the Composite (which trades in the thousands). This distinction matters: modeling a single company's stock rather than a broad market index changes the interpretation and scope of the analysis entirely, but the distinction is never acknowledged.

### 13. `stew()` Files and Caching Are Not Reproducible Without Saved `.rda` Files (Minor)

The code uses `stew()` to cache intermediate computation results in `.rda` files (`pf1_3.rda`, `mif1_3.rda`, `box_eval_3.rda`). These files are not included in the submitted project folder. Any reader attempting to reproduce the analysis must re-run the full MIF2 computations, which is only possible if the SLURM environment or equivalent computing infrastructure is available. No seed is set globally before the MIF2 runs (only inside `doRNG`), and the overall reproducibility of the numerical results is not guaranteed.

### 14. Pairs Plot Threshold of 300 Log-Likelihood Units Is Too Broad (Minor)

The pairs plots for both local and global searches use a threshold of `max(logLik) - 300` to subset the data. A window of 300 log-likelihood units is extremely permissive — it includes trajectories that are far from optimal — and obscures the structure near the mode. A more informative threshold would typically be 10 to 20 units.

### 15. Conclusions Section Understates Model Problems (Minor)

The conclusions acknowledge that "some of the estimated parameters do not converge" but describe this as something that "needs to be done to enhance the performance," framing it as a future improvement rather than a fundamental problem with the current analysis. The non-convergence of core parameters like `mu_h` means the reported maximum likelihood of 3510 for the POMP model is not reliable, and the comparison with GARCH/ARMA-GARCH models cannot be considered valid. This should be stated explicitly.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project06/blinded.rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project06/NDAQ.csv`
