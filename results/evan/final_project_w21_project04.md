# Final AI Review: w21 Project 04
# Extended Analysis on the U.S. 10-Year Treasury Bond Yield

---

## Overall Assessment

This project applies a stochastic leverage POMP model (Bretó 2014 style) to monthly U.S. 10-year Treasury Bond yield changes (1990–2021) and compares it against GARCH(1,1), with a complementary analysis of the yield-CPI relationship. The core mechanistic modeling pipeline is executed correctly: `logmeanexp` is used to combine particle filter replicates, the filtering and simulation rprocesses are properly separated, and the global search is run at run_level = 3 on HPC with Np = 2000 and Nmif = 200. The complementary CPI analysis uses appropriate tools (LRT, spectral coherence). However, three standard POMP workflow components are absent — convergence trace plots, profile likelihoods, and an ARMA benchmark — which together prevent any conclusion about whether the stochastic leverage model is well-identified or whether its added complexity over linear alternatives is warranted. Addressing these gaps is essential for the analysis to be scientifically complete.

---

## Key Strengths

**S1 — Correct likelihood aggregation.** `logmeanexp` is applied consistently to combine particle filter replicate log-likelihoods, which is the correct approach and avoids the common averaging-on-the-natural-scale error.

**S2 — Adequate computation.** Run_level = 3 with Np = 2000, Nmif = 200, and yield_Nreps_global = 100 starting values on Great Lakes provides a solid global search. The 10-minute wall time for 100 randomized starts is reasonable.

**S3 — Correct filtering/simulation separation.** The code maintains separate `rproc.filt` (conditions on covariate `covaryt`) and `rproc.sim` (generates `Y_state` stochastically), which is the essential POMP distinction for likelihood evaluation vs. forward simulation.

**S4 — Appropriate complementary analysis.** The LRT (ARIMA with/without CPI covariate on HP-detrended data) and squared coherence plot are methodologically sound tools for assessing the yield-CPI association.

---

## Major Points

**ID: 21.04.4 — Missing convergence diagnostics**
- Concern: No mif2 trace plots are shown. The pairs plots provided only show the post-filtering parameter distribution; they do not show whether the log-likelihood or parameters converged over iterations.
- Why it matters: Without trace plots it is impossible to determine whether the reported MLE of –25.71 reflects genuine convergence or premature stopping. If the likelihood is still increasing at iteration 200, the estimate is unreliable.
- Severity: Major
- Suggested author action: Add `plot(if1[[1]])` (or equivalent for a representative chain) showing log-likelihood, sigma_nu, mu_h, phi, sigma_eta vs. mif2 iteration. Confirm that the trace has flattened before the final iteration.

**ID: 21.04.5 — No profile likelihoods; parameter identifiability not addressed**
- Concern: The global search pairs plot (logLik > max – 10) shows substantial spread in multiple parameters, particularly `phi` (clustered near the upper boundary at 0.99) and `sigma_nu`. This pattern is consistent with a ridge in the likelihood surface — weak identifiability. No profile likelihoods are computed, and no confidence intervals are reported.
- Why it matters: If parameters are weakly identified, the MLE coordinates are unreliable and economic interpretation is not possible. The conclusion that the POMP model is preferred "due to the possibility of interpretation" is undermined if parameters cannot be identified.
- Severity: Major
- Suggested author action: Compute profile likelihoods for at least `phi` and `sigma_eta` (the primary volatility parameters). Use MCAP to construct 95% confidence intervals. If profiles are flat, discuss this as a limitation.

**ID: 21.04.9 — No ARMA/ARIMA benchmark**
- Concern: The paper compares the POMP model only to GARCH(1,1). No ARMA/ARIMA model is fit to `yield_diff` as a non-mechanistic benchmark.
- Why it matters: ARMA models provide the standard linear baseline for financial return series. If an ARMA(1,1) achieves a similar log-likelihood to the 6-parameter stochastic leverage model, the mechanistic model's additional complexity is not warranted. The GARCH comparison alone is not sufficient because GARCH is also a latent-variable model.
- Severity: Major
- Suggested author action: Fit ARMA(p,q) models to `yield_diff` using `auto.arima` or a manual AIC table. Compare log-likelihoods and AIC with the POMP result. Note that ARMA and POMP likelihoods for the same data are directly comparable.

---

## Minor Points

**ID: 21.04.1 — Likelihood comparison incomplete (AIC absent; MC SE unreported for MLE)**
- The comparison of –33.89 (GARCH, 3 parameters) vs. –25.71 (POMP, 6 parameters) does not account for parameter count. AIC for GARCH ≈ 73.8 vs. AIC for POMP ≈ 63.4 — the conclusion likely holds, but AIC should be computed and reported. Additionally, the Monte Carlo SE for the best POMP log-likelihood (–25.71) is not reported; the simulation-data experiment reports SE = 0.034 (adequate), but this should be confirmed for the real-data global search result.
- Severity: Minor
- Suggested author action: Report AIC for both models; extract and report SE from the `logLik_se` column of `r.box`.

**ID: M1 — Normal measurement model not evaluated against fat-tailed alternatives**
- Financial return series (including yield changes) commonly exhibit excess kurtosis. The Normal measurement model may underfit tail events. No diagnostic of the residual distribution is provided.
- Severity: Minor
- Suggested author action: Plot a QQ-plot of the standardized residuals (observed `yield_diff` divided by fitted `exp(H/2)`). If heavy tails are apparent, note a Student-t measurement model as a potential extension.

**ID: M2 — No economic interpretation of fitted volatility path**
- The model reconstructs a log-volatility series H_t. The paper does not plot this series or check whether it aligns with known periods of Treasury market stress (e.g., 2008 financial crisis, 2013 taper tantrum, March 2020 COVID shock).
- Severity: Minor
- Suggested author action: Plot the filtering distribution of H_t over time and annotate major financial events. This would substantiate the claim that the model is "interpretable."

**ID: 21.04.6 — HP filter lambda = 100 not standard for monthly data**
- The standard HP filter penalty for monthly data is lambda ≈ 14,400 (Ravn and Uhlig 2002). Lambda = 100 produces a smoother trend and may misclassify medium-frequency cycles as trend, which affects the CPI association analysis.
- Severity: Minor
- Suggested author action: Justify lambda = 100 or present a sensitivity check with lambda = 14,400.

**ID: 21.04.13 — No sessionInfo or package versions**
- Reproducibility is limited without recording the R and package versions used.
- Severity: Minor
- Suggested author action: Add `sessionInfo()` to the end of the Rmd.

**ID: 21.04.11 — Title typo**
- "Yied" should be "Yield."
- Severity: Minor
- Suggested author action: Correct the title.
