# Peer Review: W25 Project 12
## "Comparative Analysis of Volatility Models for Daily Gold Prices"

---

## Summary

This project fits three model families — ARIMA, GARCH (Gaussian and Student-t), and two POMP models (Heston stochastic volatility and a discrete regime-switching model) — to daily gold log returns from 2022–2024, comparing them via log-likelihood. The paper's main claim is that Student-t GARCH is the most efficient in-sample model, with the POMP frameworks adding interpretive value but only modest statistical gains. While the project demonstrates some methodological awareness (AIC-based model selection, profile likelihoods, convergence traces), it contains several critical errors that undermine the validity of its core claims: the regime-switching latent state plot is not data-conditioned inference, both profile likelihood computations use a single restart with a single particle filter evaluation and no confidence intervals are derived, the Heston MLE contains physically impossible parameter estimates that are dismissed without model-misspecification consideration, the log-likelihood comparison across model families is presented without AIC penalty, and no benchmark comparison against a simple non-mechanistic model is made in the POMP sense. Several additional methodological and presentational weaknesses are detailed below.

---

## Major Issues

### 1. Regime-switching latent state plot uses `simulate()` rather than the filtering distribution

In chunk `RS_plot` (line 830), the code calls `simulate(rs_model, params = coef(best_mif), nsim = 1, include.data = TRUE)` and then plots the resulting `regime` column as the "Inferred Regime Over Time." The surrounding text states: "The figure above visualizes the latent regime sequence *inferred* from the best-fit Regime-Switching model" and "The periods where Regime 2 dominates correspond to elevated market stress."

`simulate()` draws unconditionally from the prior process distribution given the fitted parameters — the resulting trajectory is statistically independent of the observed gold return data. It does not reflect what regime the market was actually in at any time. All substantive claims about which periods correspond to high or low volatility based on this plot are invalid. The correct approach is to run `pf <- pfilter(rs_model, params = coef(best_mif), Np = K)` and compute the particle-weighted fraction in Regime 2 at each time step from the filtering distribution (e.g., via `filter_traj()`), then plot this probability as the "estimated probability of being in the high-volatility regime." See Wheeler et al. (2024), §Model diagnostics.

### 2. Profile likelihoods use a single IF2 restart and a single particle filter evaluation — no confidence intervals are constructed

For both the Heston profile over `kappa` (chunk `heston_profile`, lines 590–615) and the RS profile over `log_sigma2` (chunk `RS_profile`, lines 852–876), the implementation runs exactly one `mif2()` call per grid point, starting from the MLE of the best global-search run (`modifyList(as.list(coef(best_mif)), ...)`), followed by a single `pfilter()` evaluation. No chi-squared CI cutoff is computed anywhere in the document.

This approach has two compounding problems. First, a single restart from the MLE provides no diversity: if the constrained likelihood surface has a different shape at grid values far from the MLE, the single chain may fail to reach the constrained optimum, yielding a profile that is artificially flat or drops too steeply. Second, a single `pfilter()` with Np = 5000 introduces Monte Carlo noise on the order of 1–3 log-likelihood units, which can dominate profile features at a 20-point grid. The resulting curves are therefore not valid profile likelihoods in the statistical sense. Critically, no confidence interval is extracted from either profile, so the profiles serve primarily as visual diagnostics — yet they are described as if they confirm identifiability ("this implies that kappa is a well-identified parameter"). Without computing a CI via `max(profile_loglik) - 0.5 * qchisq(df=1, p=0.95)` referenced against the global maximum, this claim is unsupported. The fix is to use `profile_design()` with a diverse starting box, run multiple (>=5) IF2 restarts per grid point, evaluate log-likelihood via `logmeanexp` over >= 10 replicated `pfilter()` calls, and apply the chi-squared threshold.

### 3. Negative `sigma` and `v0` in the Heston MLE are dismissed without model-misspecification consideration

The reported Heston MLE has `sigma` (volatility-of-volatility) = -0.0051 and `v_0` (initial variance) = -2.38e-5. Both of these parameters are constrained to be strictly positive by construction of the model: `sigma` appears as the coefficient of a noise term in the variance SDE and `v_0` is an initial variance. The Rmd code does not impose parameter transformations (no `partrans` declaration), so these estimates indicate that the optimizer landed at a boundary or found a degenerate solution. The text dismisses this with "they fall within acceptable ranges given the variability inherent in the particle filtering process," which is incorrect — negative variance parameters are not acceptable. In the Wheeler et al. (2024) framework (§Parameter identifiability), implausible parameter estimates at a boundary should be interpreted as evidence of model misspecification, not numerical noise. The authors should have applied log or logit transformations to variance parameters to enforce positivity, or flagged the result as evidence of a misspecified model. The downstream claim that the Heston model "achieved a strong fit" is undermined because the reported MLE is at a degenerate point.

### 4. Log-likelihood comparison across model families is not AIC-adjusted

Table 5 ranks five model specifications by raw log-likelihood: ARIMA (2,0,2), GARCH(1,3)-Normal, GARCH(1,3)-t, Heston POMP, and RS POMP. The text uses this table to conclude that Student-t GARCH is "the most efficient in-sample choice." However, the models have very different numbers of parameters: ARIMA(2,0,2) has 5 free parameters; GARCH(1,3)-Normal adds 5 more; GARCH(1,3)-t adds one more for the tail index; the Heston model has 5 parameters; the RS model has 6. The RS model, which narrowly achieves the highest raw log-likelihood (2539.7 vs. GARCH-t at 2543.4), actually has fewer parameters than GARCH(1,3)-t. An AIC comparison (2k - 2*loglik) would change the ranking and could reverse the authors' conclusion. The authors compute AIC for the ARIMA grid search (Table 1) and reference GARCH AIC values earlier in the paper but revert to raw log-likelihood for the final comparison table. The correct approach is to present AIC values for all models in Table 5 so the comparison accounts for parameter complexity.

### 5. No non-mechanistic benchmark for the POMP models (Wheeler et al. 2024, §Benchmark comparison)

The paper claims POMP models provide "additional insights" over ARIMA and GARCH. However, neither the Heston nor the RS model is compared to a non-mechanistic autoregressive benchmark in a way that isolates the latent-state structure as the source of improvement. The ARIMA model in this paper is underdispersed (it fails to capture ARCH effects as shown by the ACF of squared residuals), making it a weak benchmark. A proper comparison would include a GARCH-class model with the same number of parameters as each POMP model evaluated on the same data — or an auto-regressive model for squared returns — to isolate what the latent-state structure adds beyond the GARCH already captures. Wheeler et al. (2024) specifically note that mechanistic models should be compared to auto-regressive benchmarks to determine whether the mechanistic structure captures meaningful additional signal.

### 6. Heston profile is evaluated against `heston_model` rather than the constrained model object

In chunk `heston_profile` (lines 593–611), the `mif2()` call constructs a modified pomp object:
```r
mif_fit <- mif2(
  pomp(heston_model, params = modifyList(as.list(coef(best_mif)), as.list(fixed_params))),
  ...
)
pf <- pfilter(heston_model, params = coef(mif_fit), Np = 5000)
```
The `pfilter()` call evaluates log-likelihood on `heston_model` (the original pomp object) using `coef(mif_fit)`. Because `kappa` was excluded from `rw.sd` in the profile `mif2()` call, `coef(mif_fit)` will retain the fixed `kappa` value embedded in the constrained object's parameters. However, it is not guaranteed that the `kappa` stored in `coef(mif_fit)` equals the grid value, since the constrained object was initialized via `modifyList` on the full parameter vector, and `mif2()` may reassign parameters. The safer and standard approach is to pass the constrained pomp object directly to `pfilter()` (i.e., `pf <- pfilter(pomp(heston_model, params = coef(mif_fit)), Np = 5000)` or to verify that the evaluated `kappa` in `coef(mif_fit)` matches the grid value at each iteration.

---

## Minor Issues

### 7. Log-likelihood comparison between ARIMA and POMP models requires identical observation models and data

The text compares ARIMA log-likelihood (2525.8) directly to GARCH and POMP log-likelihoods (2528–2543) in Table 5. While all models in this study are fitted to the same log-return series with a Gaussian observation model, the ARIMA log-likelihood from R's `arima()` is a conditional log-likelihood that conditions on the initial observations for the AR and MA components. For ARIMA(2,0,2), this discards the contribution of the first 2 observations. The GARCH and POMP likelihoods may or may not condition on initial observations in the same way. The paper should clarify whether all five models are evaluated on exactly the same N observations, or acknowledge the potential small discrepancy.

### 8. Discussion references "a common 2025 hold-out" but no out-of-sample evaluation is performed

In Section 7 (line 998), the text criticizes Project 11 for an inconsistent training window, stating "fitting both classes on the full 2022–2024 span and scoring them on a common 2025 hold-out keeps the playing field level." However, no out-of-sample evaluation on a 2025 hold-out is actually performed in this paper. The comparison in Table 5 is entirely in-sample. This statement creates a false impression of methodological rigor that does not exist in the analysis. Either the out-of-sample evaluation should be implemented or the claim should be removed.

### 9. Effective sample size not monitored; particle degeneracy cannot be ruled out

The paper states (Section 5.1) "convergence diagnostics and effective sample size trajectories did not indicate particle degeneracy or instability," but no ESS plots are presented anywhere in the document. ESS monitoring is a standard diagnostic for particle filter adequacy (Wheeler et al. 2024, §Computational adequacy; simulation checklist §10). The claim about ESS should either be supported with a plot or removed. Given the small variance parameters in the Heston model (theta ≈ 8e-5), there is genuine risk of particle filter degeneracy that should be empirically assessed.

### 10. The regime-switching model's transition probability p_11 ≈ 0.52 implies near-random switching, not "persistence"

The text (line 821–824) describes the RS model as having "asymmetric transition structure where the high-volatility regime is more persistent" based on p_11 ≈ 0.52 and p_22 ≈ 0.80. However, p_11 ≈ 0.52 is essentially a coin flip — the low-volatility regime has virtually no persistence (expected duration = 1/(1-0.52) ≈ 2 days). The text describes this as "low-volatility regime" behavior without noting that this near-random transition is anomalous. Coupled with the simulate()-based regime plot that shows "frequent switching," this suggests the model may be poorly identified or the low/high regime labels may be inverted. This should be flagged as a potential model misspecification or identifiability concern (Wheeler et al. 2024, §Parameter identifiability).

### 11. GARCH AIC values in Table 3 are inconsistent with those cited in the text

Table 3 reports GARCH(1,3)-Normal AIC of approximately -5046.13 (text: "GARCH(1,3) has the lowest AIC value of -5046.13"). Table 5 reports GARCH(1,3)-Normal log-likelihood as 2528.7, which would correspond to AIC = 2*k - 2*2528.7. With k=10 parameters (ARMA(2,2) + GARCH(1,3) + mean + intercept), AIC ≈ 20 - 5057.4 = -5037.4. The figures are inconsistent. Additionally, Table 5 lists "GARCH(1,3)" under both the Normal and Student-t rows, but the text (line 355) states the authors decided to proceed with GARCH(1,1) after the diagnostic comparison — yet Table 5 uses GARCH(1,3). The final chosen model should be clearly identified and used consistently.

### 12. Figure numbering collision: two "Figure 3" plots

The paper uses "Figure 3" for both the log-return time series (line 128, chunk using `log_return_df`) and the ACF of squared log returns (line 249). This duplication makes it impossible to identify which figure the text refers to in several places.

### 13. The rw.sd for the Heston local search has `mu = 0.0005` matching the starting value for `mu`, a potential rw.sd magnitude issue

In chunk `heston_local` (line 497), `rw_sd_vals <- rw_sd(mu = 0.0005, ...)` and the starting value for `mu` is also `0.0005`. While this is a borderline case (the other parameters have rw.sd values much smaller than their starting values), having `rw.sd` equal to the starting value for `mu` means the drift perturbation is 100% of the starting estimate, which is very large for a drift parameter in this context. The starting value for `kappa` is 2.0 and `rw.sd` for kappa is 0.05 (2.5%), which is reasonable. For `mu`, the perturbation should be calibrated to approximately 1–5% of the expected MLE range, not equal to the starting value.

### 14. No model diagnostics beyond trace plots and QQ plots

The paper presents QQ plots and convergence traces for the POMP models but does not show: (a) simulated trajectories overlaid on the observed data to assess forward-simulation adequacy; (b) conditional log-likelihoods over time to identify periods of poor fit; (c) comparison of summary statistics between simulated and observed data (e.g., distribution of absolute returns, autocorrelation of squared returns). These diagnostics are standard in POMP analysis (Wheeler et al. 2024, §Model diagnostics) and would help assess whether the Heston or RS model provides a genuinely better description of the data structure beyond likelihood value.

### 15. Typos and unclear terminology

- Section 2.2 heading: "Stationairty" should be "Stationarity."
- Line 354: "We therefore proceed with the parsimonious ARMA(1,1)+GARCH(1,1) model" — but the model used throughout is ARMA(2,2), not ARMA(1,1). The text switches terminology inconsistently, sometimes calling the mean equation "ARMA(1,1)" (lines 345, 354, 356) and other times ARMA(2,2) (Table 4, line 255). This likely reflects an earlier draft where ARMA(1,1) was used and the switch to ARMA(2,2) was incompletely propagated.
- Line 266: "AMIRA(2, 0, 2)" should be "ARIMA(2, 0, 2)."
- The reference to "Project 16 (Winter 2022)" in Section 5.1 (line 447) as a methodological guide is unusual citation practice for an academic paper; the cited project's methodology should be described directly.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project12/data.csv`
