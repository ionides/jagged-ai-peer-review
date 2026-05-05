# Peer Review: W24 Project 14 — Tuberculosis Incidence in the USA: ARIMA and POMP Analysis

---

## Summary

This project analyzes U.S. tuberculosis (TB) case data from 1953 to 2020 using two approaches: an ARIMA-based time series model and a POMP-based stochastic SEIRS compartmental model. The ARIMA section fits an ARIMA(0,1,5) model selected by AIC. The POMP section builds a stochastic SEIRS model with a time-varying transmission rate, gamma process noise, and a negative binomial measurement model, estimated using iterated filtering (mif2). The paper's main strength is its use of a mechanistic, partially observed model that explicitly accounts for under-reporting. However, the paper has severe methodological deficiencies: the global search was abandoned entirely, the single mif2 run provides no evidence of convergence, no benchmark comparison is made, no profile likelihoods are computed, model equations in the text are inconsistent with the code, reproducibility is compromised by a hardcoded absolute path and undefined helper functions, and the ARIMA model is selected but never diagnostically validated in the rendered output.

---

## Major Issues

### 1. No global search and no convergence evidence (Critical)

The entire optimization rests on a single mif2 call with `Nmif = 50` and `Np = 2000` from a single set of starting values. The authors explicitly acknowledge: "Due to time constraint it was not possible to run global search" and "Despite trying global search techniques, these efforts were omitted from the report due to encountered failures." No replicate mif2 runs from diverse starting points are shown, and no log-likelihood convergence trace from the single run is interpreted or discussed. The `plot(mif_out)` call will produce trace plots, but the text contains no commentary on whether the traces show convergence.

Without multiple restarts from diverse starting values converging to the same log-likelihood, there is no basis to claim that the reported parameter estimates or log-likelihood of -628.8447 are near the MLE. The entire downstream analysis (parameter interpretation, simulation) rests on an unverified, likely sub-optimal point. See Wheeler et al. (2024), §Computational adequacy: a large improvement in log-likelihood was attributed primarily to increasing computational effort, and convergence must be demonstrated via replicate searches.

**Fix:** Run at least 20 mif2 chains from diverse starting values (ideally drawn from a space-filling random search), plot the resulting log-likelihoods, and report the maximum across runs as the candidate MLE.

---

### 2. No non-mechanistic benchmark comparison (Critical)

The mechanistic SEIRS model is never compared against any non-mechanistic baseline. The ARIMA model fitted in the first section of the paper is never compared to the POMP model on a common quantitative scale (log-likelihood or AIC). The paper concludes that "the POMP model provides a more comprehensive approach" without any quantitative evidence. This comparison is the single most diagnostic check for whether a mechanistic model captures meaningful structure beyond what a simple statistical model achieves.

Wheeler et al. (2024) note that none of the 32 papers in their Haiti cholera review performed this comparison, and their own benchmark revealed that some models failed to beat an auto-regressive negative binomial. The same risk applies here.

**Fix:** Report the log-likelihood of the best-fitting ARIMA model and the best POMP model log-likelihood (from a proper global search) on the same data and measurement scale. Alternatively, fit an auto-regressive negative binomial model and compare via AIC.

---

### 3. Model equations inconsistent with code (Critical)

The written stochastic differential equations (lines 543–549) and the discrete-time binomial transition equations (lines 556–560) do not match the Csnippet implementation.

Specifically:

- The written ODE for S includes two terms: `- β(t) SI/N - dw(t) β SI/N`, implying both a deterministic and a stochastic component summed. The Csnippet code computes `foi = (Beta - Beta_t * (t - 1952)) * I / N` and then multiplies by `dw` (the gamma noise), meaning the noise is multiplicative on the entire force of infection, not additive. These are different models.
- The discrete-time equation for E (line 557) shows `E(t+δ) = E(t) + Binomial(S(t), 1 - exp(-μ_EI δ))`, which implies the new E entrants come from a binomial draw on S with rate μ_EI. This is wrong: the new E entrants should be the S→E transitions (`dN_SE`), and the E→I transitions should be subtracted. The code correctly computes `dN_SE` and `dN_EI` separately, but the equation is mis-stated.
- The H accumulator equation (line 560) uses `Binomial(I(t), 1 - exp(-μ_IR δ))`, which double-counts relative to the I→R transitions already drawn; the code correctly reuses `dN_IR` for both R and H updates.

These mathematical specification errors undermine the paper's scientific clarity and, per Wheeler et al. (2024) §Code and data supplements, constitute a reproducibility failure when code and text diverge.

**Fix:** Rewrite the mathematical specification to match the Csnippet code precisely.

---

### 4. No profile likelihoods or parameter identifiability assessment (Major)

With 13 parameters (Beta, Beta_t, mu_EI, mu_IR, mu_RS, rho, k, sigmaSE, S_0, E_0, I_0, R_0, N) fit to 68 annual observations, parameter identifiability is a serious concern. The paper presents no profile likelihoods, no confidence intervals, and no discussion of whether the estimated parameters are identifiable.

Several parameters are particularly suspect:
- `mu_EI = 129.3` implies an exposed-to-infectious period of approximately 0.008 years (about 3 days), which is implausibly short for TB (typical latency is weeks to months).
- `mu_RS = 33.8` implies immunity lasts approximately 11 days, again biologically implausible for TB.
- No comparison to literature values is provided.

Wheeler et al. (2024) §Parameter identifiability note that implausible MLE values (e.g., zero immunity loss rate) are evidence of model misspecification, not biological truths. The same interpretation applies here.

**Fix:** Compute profile likelihoods for at least the key epidemiological parameters (Beta, mu_EI, mu_IR, rho). Report 95% confidence intervals via MCAP. Compare estimated values to known TB natural history parameters.

---

### 5. ARIMA model selected but diagnostic model is never called (Major)

A `build_and_diagnose_model` function is defined (lines 390–450) but is never called in the document. The ARIMA model identified as "best" (ARIMA(0,1,5)) is never fitted, residual diagnostics are never produced, and the model is never shown to pass white-noise tests. The AIC comparison table is displayed, but the reader has no evidence that the chosen model is adequate or that residuals are uncorrelated.

**Fix:** Call `build_and_diagnose_model` on the selected ARIMA(0,1,5) model, display residual plots, ACF of residuals, and normality test results.

---

### 6. Hardcoded absolute path breaks reproducibility (Major)

Line 493 contains:
```
<img src="/Users/shreya/Desktop/Winter/stats_531/PROJECT2/seirs_draw.png" ...>
```
This is an absolute path to a local filesystem and will produce a missing image in any other environment. The SEIRS diagram is not included in the project files, making the HTML rendering incomplete for any reader other than the author.

**Fix:** Include the image file in the project directory and use a relative path, or remove the image and replace it with a LaTeX/TikZ or ASCII diagram.

---

### 7. `simulation_arima` and `simulation_sarima` functions are undefined (Major)

The `model_selection_table` function (lines 223–377) calls `simulation_arima` and `simulation_sarima` (lines 329–333), which are never defined anywhere in the document. The code only avoids a runtime error because `simulation_times = 0` is passed at the call site (line 382), causing the branch to be skipped. If a reviewer attempts to run the code with `simulation_times > 0`, it will error. The `simulated_ci_cover_0_table` results are therefore entirely absent. This is both a reproducibility failure and an incomplete analysis — the simulated confidence intervals were presumably intended to complement the Fisher-information intervals.

**Fix:** Define `simulation_arima` and `simulation_sarima`, or remove references to them and the corresponding table columns.

---

### 8. H compartment not reset between measurement times (Potential accumvar issue)

The process model uses `accumvars = 'H'` to ensure H is reset to zero at each observation time, which is correct for tracking incident cases per observation window. However, the initial condition in `seir_init` sets `H = 0` (line 666), which is correct. The concern is that with annual observations and a time step of 1/52 year (weekly), H accumulates all recoveries over 52 weekly steps before being reset. The measurement model then compares this accumulated H against the annual count `Number`. This architecture is correct but the paper provides no validation that the accumulation is happening as intended (e.g., a simple simulation check). Given the many model-building iterations in the code (including an earlier version where `accumvars` was absent), it is worth verifying explicitly.

**Fix:** Include a brief simulation check showing that the simulated annual `Number` values are of the right order of magnitude compared to observed counts.

---

### 9. Goodness-of-fit assessment is purely visual (Major)

The only goodness-of-fit assessment for the POMP model is a plot of 5 simulation trajectories overlaid on the data (lines 696–706), with the observation that the model "reasonably capture[s] the overall declining trend." No quantitative fit measure is reported, no AIC is computed, and the single reported log-likelihood of -628.8447 comes from before the mif2 run (it is the log-likelihood at the initial hand-picked parameter values, as `logLik(mif_out)` after a single non-converged run is also not properly interpreted).

Wheeler et al. (2024) state: "Visual comparisons alone are only a weak and informal measure of goodness-of-fit." Five simulation trajectories are insufficient to assess calibration.

**Fix:** Report the log-likelihood after filtering (using `pfilter` with multiple replicates) at the fitted parameters. Compute AIC and compare to the ARIMA baseline.

---

### 10. Population fixed at 2023 value; acknowledged but not addressed (Minor/Moderate)

The population N is fixed at 333,000,000 (the 2023 U.S. population), yet the data spans 1953–2020. The U.S. population in 1953 was approximately 160 million, roughly half the current value. This means the transmission rate Beta and the initial fractions S_0, I_0, E_0, R_0 are fitting to incorrect population sizes throughout the time series. The authors acknowledge this in the "Further Investigation" section but do not address it. Because force of infection is `Beta * I / N`, underestimating N by up to a factor of 2 for earlier years will produce systematically biased Beta estimates.

**Fix:** Either use yearly U.S. population estimates as a covariate (available from Census Bureau data), or at minimum perform a sensitivity analysis with the mean population over the study period.

---

### 11. Stochastic model equations label mislabeled (Minor)

The deterministic ODE system (lines 542–549) is labeled "Stochastic Model" in the section heading. It is the mean-field (deterministic) approximation of the process, not the stochastic model itself. The discrete-time binomial transitions that follow (lines 554–560) represent the actual stochastic model. This labeling is misleading.

**Fix:** Rename the ODE block to "Deterministic mean-field equations" or "ODE approximation" and label the binomial transitions as the stochastic process model.

---

### 12. Fisher confidence interval computation is incorrect (Minor)

The `model_selection_table` function computes "Fisher CI" as:
```r
fisher_ci_low <- pc_model$coef - 1.96 * diag(pc_model$var.coef)
fisher_ci_high <- pc_model$coef + 1.96 * diag(pc_model$var.coef)
```
`diag(pc_model$var.coef)` returns the diagonal of the variance-covariance matrix, which gives the variances, not the standard errors. The correct standard errors are `sqrt(diag(pc_model$var.coef))`. This means all reported Fisher confidence intervals are dramatically miscalculated (using variance instead of SD in the margin of error). The `fisher_ci_cover_0_table` results are therefore unreliable.

**Fix:** Replace `diag(pc_model$var.coef)` with `sqrt(diag(pc_model$var.coef))` throughout the interval computation.

---

### 13. ARIMA applied to raw counts without scale justification (Minor)

The ARIMA model is applied to `tb_num`, the raw case counts (ranging from ~84,000 in 1953 to ~7,000 in 2020). No transformation is applied. For count data with such a large dynamic range and clear heteroscedasticity (variance likely scales with level), a log-transform or Box-Cox transform would typically be considered. The spectral analysis and AIC model selection are both performed on the raw untransformed series, yet the heteroscedasticity is not discussed.

**Fix:** At minimum, plot and discuss the residual variance over time to assess whether heteroscedasticity is present; consider whether a log-transformed series would be more appropriate for ARIMA modeling.

---

### 14. mif2 random walk standard deviation is uniform across all parameters (Minor)

All parameters in the mif2 call (line 729) are given a random walk standard deviation of 0.02, regardless of parameter scale or transformation. While parameters are log- or logit-transformed via `partrans`, the magnitude 0.02 is applied uniformly. In practice, some parameters (such as the initial fractions S_0, E_0, I_0 under barycentric transformation) may need different perturbation magnitudes. No justification or sensitivity analysis for the choice of rw.sd values is provided.

**Fix:** Provide brief justification for the rw.sd choices, or note that tuning these values was not performed and represents a limitation.

---

### 15. Missing: particle filter diagnostics and effective sample size (Minor)

No effective sample size (ESS) diagnostics are reported for the particle filter. ESS collapse during filtering would indicate that the model is incompatible with the data (or that the particle count is insufficient), but neither is checked. The `Np = 2000` choice is not justified, and no sensitivity to particle count is assessed.

**Fix:** Report ESS traces from the final pfilter run. Verify that ESS does not collapse to near zero at any time point.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project14/TB_data_usa.csv`
