# Peer Review: W25 Project 08
## Netflix Returns Analysis Using POMP and GARCH Models

---

## Summary

This project analyzes daily log-returns of Netflix (NFLX) stock relative to the S&P 500 ETF (SPY) from 2015 to 2022 using a progression of models: EDA, ARIMA, GARCH(1,1), GJR-GARCH, and a stochastic volatility (SV) model implemented via POMP. The SV model follows Breto (2014) with a leverage-driven latent volatility process estimated by IF2. The project is well-structured and covers a broad range of methods. However, it has serious weaknesses in global search design (the search box excludes the optimal phi region), in model comparison (the claim that POMP beats GARCH is stated but not formally demonstrated), in identifiability analysis (no profile likelihoods), in notation (the measurement model is misdescribed in the submitted Rmd), and in several interpretive errors. A draft note is also left in the final submission.

---

## Major Issues

### 1. Global search box for phi excludes the optimal parameter region

The global IF2 search specifies `phi = c(0.9, 0.999)` as the search box. However, inspection of the saved artifacts shows that the highest-likelihood solutions for NFLX have phi approximately 0.62 to 0.89 — entirely outside the lower bound of this box. Seven of the 20 local-search replicates (the ones that found the better mode) converged to phi in this range. The global search can only reach this region if IF2 drifts below 0.9 from its initial random draw inside [0.9, 0.999]. Only 5 out of 20 global replicates did so. The global search best log-likelihood (4619.8) is 3 units below the local search best (4622.8), confirming that the global search did not outperform the local search and that the box was misspecified. The paper's claim that the global search "broadly explores the parameter landscape and increasing robustness against local maxima traps" is therefore not supported for NFLX.

**Fix:** Extend the phi box to cover [0.5, 0.999] or a range centered on the local-search MLE. For a properly logit-transformed parameter the box should be specified in logit units or derived from inspection of the local-search distribution.

---

### 2. Measurement model misdescription in the submitted document

Section 6.1 of `blinded.rmd` writes the measurement innovation as $\epsilon_n \sim N(0, \sigma_\nu)$, implying that the observation variance is $\sigma_\nu$. This is inconsistent with the actual code in `pomp_final.Rmd`, which correctly writes $\epsilon_n \sim N(0, 1)$ and implements `dmeasure` as `dnorm(y, 0, exp(H/2), give_log)`. In the model, $\sigma_\nu$ controls only the leverage-driver process $G_n$, not the measurement equation. The blinded document therefore presents a materially different model specification than was actually estimated, making the submitted analysis misleading to readers.

**Fix:** In `blinded.rmd`, correct the measurement equation to $\epsilon_n \sim N(0,1)$ and clarify that $\sigma_\nu$ is the standard deviation of the $G_n$ process noise only.

---

### 3. No benchmark comparison for the POMP model

The paper presents ARIMA and GARCH models and a POMP model but does not include a formal quantitative comparison of all models in a single table. Section 8.1 claims that "maximum log-likelihood values obtained were higher than those of both GARCH and GJR-GARCH models," but no unified AIC table is presented; the GARCH comparison table in Section 4.3 only compares GARCH(1,1) vs. GJR-GARCH, not vs. the POMP model. Without reporting the GARCH log-likelihoods alongside the POMP log-likelihood (4622.8 for NFLX, AIC = -9234), readers cannot assess whether the claimed superiority holds. A good GARCH(1,1) model routinely achieves likelihoods that differ from POMP-SV by only tens of units. Per Wheeler et al. (2024), mechanistic models must be compared quantitatively to non-mechanistic benchmarks.

**Fix:** Add a table showing log-likelihood and AIC for ARIMA, GARCH(1,1), GJR-GARCH, and POMP-SV for both NFLX and SPY.

---

### 4. No profile likelihoods — parameter identifiability not quantified

The paper acknowledges "weaker identifiability" for NFLX but provides no profile likelihoods or confidence intervals for any parameter. The pairs plots show parameter clouds but cannot distinguish a flat likelihood surface from a broad identifiable region. Wheeler et al. (2024) identify profile likelihood computation as essential for assessing identifiability. The artifacts confirm the identifiability concern: 13 of 20 local-search replicates converge to the phi = 1 boundary (bimodal likelihood), and sigma_eta ranges from 0.78 to 1506.8 across replicates, indicating severe unidentifiability near phi = 1.

**Fix:** Compute profile likelihoods for phi and sigma_eta using `profile_design()`. Report MCAP confidence intervals. The flat profile for sigma_eta near the phi = 1 mode is itself an informative diagnostic.

---

### 5. No model diagnostics (conditional log-likelihoods, ESS, simulation comparisons)

Despite using a particle filter, the paper presents no per-observation conditional log-likelihood plots, no effective sample size (ESS) monitoring, and no comparison of filter-conditioned simulations to observed data. The text mentions that "ESS and conditional log-likelihoods are stable at a moderate level for most data points, with few correlated dips at some isolated time points," but no figures showing these diagnostics appear in the submitted document. Wheeler et al. (2024) demonstrate that such diagnostics are essential for understanding where a model fails (e.g., around earnings shocks) and for motivating model extensions.

**Fix:** Plot conditional log-likelihoods over time and highlight periods of model misfit (e.g., the April 2022 subscriber-loss shock). Plot ESS over the filter run. Overlay filtering-distribution simulations against the observed series.

---

### 6. Holdout set defined but never evaluated

The paper defines `nflx_holdout` and `spy_holdout` (January 2023 to April 2025) at the top but never uses them. The ARIMA forecast produces 30-day forward predictions without evaluating against actual holdout observations, and the POMP model does not generate filtered forecasts from the holdout period. Given that one of the stated research goals is assessing predictive capability, the absence of any held-out evaluation is a serious omission. No RMSE, MAPE, or coverage metrics are reported.

**Fix:** Evaluate ARIMA forecasts against observed holdout returns. For the POMP model, generate forecasts from the filtering distribution conditioned on training data (per Wheeler et al. 2024, §Forecast methodology) and evaluate calibration on the holdout period.

---

### 7. Insufficient computational effort — global search fails to improve on local search for NFLX

With `run_level = 2` (Np = 1000, Nmif = 100, Nreps_global = 20), the global search achieves a best log-likelihood of 4619.8, which is 3.0 units below the local-search best (4622.8). A properly executed global search should match or exceed the local-search likelihood. The gap indicates that the global search is computationally insufficient and/or that the phi box misspecification (Issue 1) prevented the optimizer from finding the true optimum. Only 5 of 20 global replicates escaped the phi = 1 trap. At run_level = 3 (Nreps_global = 100, Nmif = 200), a better coverage of the parameter space would be expected. Wheeler et al. (2024) emphasize that "insufficient computation can make a good model look bad."

**Fix:** Increase run_level to 3 or expand the phi box as noted in Issue 1. Report convergence traces showing all global replicates reaching similar log-likelihoods before accepting results.

---

### 8. ACF interpretation error in Section 3.1

Section 3.1 states: "The ACF plots show slow decay for both series, which is characteristic of non-stationary series." This claim is incorrect in context. The ACF is computed on log returns (already a stationary series as confirmed by the ADF test and explicitly confirmed by the authors). Slow ACF decay in a stationary returns series is not evidence of non-stationarity; it is evidence of autocorrelation or, in the context of financial returns, potentially volatility clustering in the squared series. The subsequent statement "these diagnostics confirm that log returns are already stationary and do not require further differencing" contradicts the earlier ACF interpretation.

**Fix:** Correct the ACF interpretation to note that moderate autocorrelation in stationary log returns may indicate ARMA structure (which motivates ARIMA modeling) and that slow decay in squared returns would indicate ARCH effects (motivating GARCH).

---

## Minor Issues

### 9. Notation inconsistency in Section 6.2 (initialization values)

Section 6.2 states that sigma_nu is initialized at $\exp(-5)$, but the code shows `sigma_nu = exp(-6)`. This is a minor inconsistency between text and code but should be corrected for accuracy.

### 10. Unfinished draft note left in Section 8.2

Section 8.2 contains the following unedited placeholder: "Add direct discussions of how we expanded on the previous projects." This draft note was not removed before submission and should be replaced with substantive text.

### 11. Reference [11] used for two different works

Reference [11] is cited in Section 6 as "STATS 531 Winter 22 Project 7" (the source of the POMP code) and again in Section 8.2 as "Project 7, Winter 2024: Analysis of Apple Stock Price." These are different papers assigned the same reference number. The references section (line 1074) defines [11] as the W24 project, making the Section 6 citation inaccurate.

Additionally, Reference [12] (listed as "Project 11, Winter 2024: NVIDIA Stock Price Analysis") has a URL pointing to `project07/blinded.html` instead of `project11/blinded.html`.

### 12. ARIMA residual description uses implausible units

Section 5.2 states: "Extreme outliers, including negative residuals exceeding -100 points, highlight the stock's erratic return movements." The ARIMA model is fitted on log returns (scale approximately -0.5 to +0.5), so residuals of -100 are impossible. This appears to be a carryover from a prior version of the analysis applied to price levels.

### 13. Beta standard error formula is incorrect

The 95% confidence interval for beta in Section 7.4 is computed as:
`se = sqrt(var(NFLX) / (n * var(SPY)))`.
The correct OLS standard error for the slope uses the residual variance, not the total variance of NFLX: `se = sqrt(residual_var / (n * var(SPY)))`. The formula used overestimates the standard error when NFLX and SPY are correlated, producing a wider CI than is statistically warranted.

### 14. STL decomposition applied to non-stationary prices

Section 3.2 applies STL decomposition to closing prices (non-stationary) rather than returns. While the authors acknowledge this choice, decomposing a trending series with frequency=252 can produce trend and seasonal components that reflect the non-stationarity rather than genuine periodicity. The stated seasonal period (252 trading days) does not correspond to a natural seasonal cycle for stock prices.

### 15. First log-return set to zero rather than NA

The code computes `log_return = c(0, diff(log(Close)))`, setting the first observation's return to 0. This is technically incorrect; the first return should be `NA` since no prior price exists. Including this zero biases the sample mean slightly toward zero and adds a spurious observation to the ADF test and ARIMA fitting.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
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

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/blinded.rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/pomp_final.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/nflx_params_local.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/nflx_params_global.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/spy_params_local.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/spy_params_global.csv`
