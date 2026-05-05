# Peer Review: W24 Project 07 — Time Series Analysis of Apple Inc. (AAPL) Stock Price

## Summary

This project applies ARIMA/ARMA, GARCH variants, and a stochastic volatility POMP model to AAPL log returns from April 2020 to April 2024. The POMP model follows the Bretó (2014) leverage framework. The overall structure is reasonable, but there are numerous methodological, statistical, and presentation weaknesses detailed below.

---

## Weaknesses (Most Critical First)

### 1. Global Search Starts From a Single Local MIF2 Object (Critical Bug)

**Evidence:** In the global search code block, `if.box` is initialized using `mif2(if1[[1]], ...)` — that is, only the first object from the local search is used as the template for all 100 global starting points. This means the global search inherits the model specification and (most importantly) the parameter estimates of a single local run, rather than beginning truly fresh from the box. This defeats the purpose of a global search and likely introduces bias into the global likelihood surface. A correct implementation would restart from the `AAPL_filter` object, as is done in the local search.

### 2. Particle Filter Benchmark Uses Simulated Data, Not the Real Data (Critical Bug)

**Evidence:** The initial particle filter (`pf1`) is run on `sim1.filt`, which is constructed from a *simulated* dataset (`sim1.sim = simulate(sim1.sim, ...)`), not from the original AAPL returns. All subsequent local and global MIF2 runs are correctly applied to `AAPL_filter` (the real data), but the reported log-likelihood benchmark of -1501.19 is for simulated data. Comparing this benchmark to the MIF2 results on real data (log-likelihoods ~2650) is therefore meaningless and misleads the reader.

### 3. Log-Likelihood Values Are Implausibly High and Not Critically Examined

**Evidence:** The local search reports a maximum log-likelihood of 2650 and the global search 2655 for approximately 1000 observations of log returns. For a Gaussian observation model these values would imply extraordinarily tight fits and are atypically large compared to published analyses of comparable datasets. No sanity check (e.g., comparison with a simple Gaussian baseline) is performed. This strongly suggests a model specification error—possibly in the measurement model or the covariate setup—that inflates the likelihood.

### 4. Mismatch Between Benchmark Log-Likelihood (-1501) and MIF2 Results (~2650)

**Evidence:** The text states "We replicated the filtering process 20 times... obtained a log likelihood unbiased estimate of -1501.19." The local and global MIF2 log-likelihoods are then reported as ~2650, a difference of more than 4000 log-likelihood units. This enormous discrepancy is not discussed or explained. If it arose because the benchmark used simulated data (see Issue 2), this should be stated clearly. As written, it is deeply confusing and undermines trust in all reported results.

### 5. ARMA Grid Search Excludes ARMA(0,0) and Low-Order Models

**Evidence:** The grid search starts at `p_values <- c(1:4)` and `q_values <- c(1:4)`, so ARMA(0,0), ARMA(1,0), and ARMA(0,1) are never evaluated. The text concludes ARMA(1,1) is selected, but it is unclear whether the chosen model actually beats simpler alternatives like AR(1) or MA(1). The AIC-optimal model within the 4x4 grid is used, but the full table of AIC values is never displayed—only the minimum row is shown—preventing the reader from evaluating the choice.

### 6. GARCH Model Selection Uses Minimum (Not Maximum) Log-Likelihood

**Evidence:** The code for basic GARCH selects the best model by `min_value <- min(garch_table, na.rm = TRUE)`, where `garch_table` stores log-likelihood values. Log-likelihood should be *maximized*, not minimized. This inverts the selection criterion and likely leads to the worst-fitting model being labeled "best." The GARCH with t-distribution and apARCH sections correctly minimize AIC, making the error in the basic GARCH section more conspicuous.

### 7. Convergence Diagnostics Are Visually Poor and Insufficiently Discussed

**Evidence:** The MIF2 convergence diagnostic plots (both `local_d2.png` and `global_d2.png`) show that `sigma_nu` does not converge, `mu_h` spans a very wide range, and `phi` shows erratic behavior in the local search. The text acknowledges that "we can hardly say the log likelihood converges from the MIF2 convergence diagnostics plot" for local search, but the global convergence is described as "converges in just a few iterations," which contradicts the visual evidence in `global_d2.png` where `sigma_nu` and `phi` remain highly variable.

### 8. Filter Diagnostics Show Severe Particle Depletion

**Evidence:** Both `local_d1.png` and `global_d1.png` show "effective sample size" frequently collapsing to near zero across many time points, with "cond log-lik" exhibiting enormous negative spikes. This indicates severe particle impoverishment and suggests the particle filter is failing for substantial portions of the time series. This is a fundamental validity issue for the MIF2 results but is never discussed in the text.

### 9. POMP Model Parameter Transformation Is Incomplete

**Evidence:** The `partrans` applies `log` to `sigma_eta` and `sigma_nu` and `logit` to `phi`, but does not constrain `mu_h`, `G_0`, or `H_0`. While `mu_h` and the initial value parameters may be unconstrained in principle, omitting them from the transformation documentation and not discussing the parameter space raises questions. More critically, `phi` is the AR coefficient for log-volatility and should satisfy |phi| < 1 for stationarity; the logit transform enforces (0,1), which is appropriate, but the pairwise plots show phi values very close to 1.0 (near the boundary), which can cause near-unit-root behavior in H and should be flagged.

### 10. sigma_eta Values in Local Search Are Anomalously Large

**Evidence:** The local pairwise scatter plot (`local.png`) shows `sigma_eta` ranging from roughly 0 to 30. The model specifies `sigma_eta` as a volatility-of-volatility parameter and values this large are physically implausible for financial log returns and inconsistent with the cited Bretó (2014) framework. The text does not flag this as a warning sign or investigate whether these correspond to degenerate solutions.

### 11. Seasonal Decomposition Applied to Financial Returns Is Inappropriate

**Evidence:** The code applies `decompose(data_lr)` to the log returns with `frequency = 253` (approximate number of trading days per year). Additive seasonal decomposition assumes deterministic, repeating seasonal patterns—a well-known mis-specification for financial return series. The authors do not find seasonal patterns (as expected), but presenting this analysis adds no value and could mislead readers about the appropriateness of seasonal models for returns.

### 12. ACF Lag Axis Is Misinterpreted

**Evidence:** The text states "we do observe a peak at Lag 0.07" when discussing the ACF plot. An ACF lag of 0.07 in R's default plotting (with `frequency = 253`) corresponds to approximately lag 18 in absolute time units (0.07 × 253 ≈ 18 days), not a lag of 0.07. The authors do not recognize or explain this scaling, nor do they identify what the actual lag number is, leading to an incorrect interpretation of the autocorrelation structure.

### 13. GARCH Conclusion Is Inconsistent With the Diagnostic Plots

**Evidence:** The conclusion states "the GARCH model proved to be the most effective in forecasting volatility." However, the diagnostic Q-Q plots for all three GARCH variants (basic, apARCH, t-distribution) show heavy-tailed residuals with substantial departures from normality, and the authors themselves describe each as "not a good fit." No formal likelihood comparison is made between GARCH variants and the POMP model. The conclusion is therefore not supported by the evidence presented.

### 14. Local Search Saves Wrong Variable to CSV

**Evidence:** In the local search code block, the line `write.table(local_results, file = "AAPL_params2.csv", ...)` references `local_results`, which is never defined in the code. The actual result data frame is named `r.if1`. This would cause a runtime error if the `eval=FALSE` block were executed; the global search correctly uses `r.box`.

### 15. Excessive Reliance on Prior Course Material Without Independent Contribution

**Evidence:** The project explicitly states "The codes in this part are borrowed from [3] and [4]" (course notes and a prior year's project) for both the local and global search sections. Reference [4] is a W22 project that applied essentially the same Bretó (2014) leverage model to a similar stock. The POMP model structure, parameter names, Csnippet implementations, and search setup are nearly identical to those references. The project does not explain what novel analysis or extension it contributes beyond applying the same code to a different ticker and date range.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project07/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project07/local.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project07/local_d1.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project07/local_d2.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project07/global.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project07/global_d1.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project07/global_d2.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project07/Makefile`
