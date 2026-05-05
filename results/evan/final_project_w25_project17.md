# Final AI Review
## Project: final_project_w25 / project17
## Title: Time Series Analysis of New York Harbor Conventional Gasoline Regular Spot Price

---

## Overall Assessment

This project applies stochastic volatility (SV) models to monthly log returns of New York Harbor gasoline spot prices, with the goal of testing whether leverage effects are attenuated in regulated commodity markets. The POMP pipeline is executed competently: simulation studies, local and global searches, convergence traces, and ESS monitoring are all present. The authors extend the Breto (2014) SV model with a Student-t observation distribution — a non-trivial and correctly implemented modification — and include a T-GARCH benchmark. The Discussion section shows genuine scientific self-awareness, particularly in acknowledging the regime-shift hard-coding as a fundamental limitation. However, several methodological gaps prevent the main conclusion from being well-established: the leverage comparison is confounded by data-snooped regime windows, profile likelihoods are absent for all parameters, no mean-model baseline is provided, and the log-likelihood values in the AIC table may not have been computed via replicated pfilter runs with reported Monte Carlo uncertainty.

## Key Strengths

- **Full POMP pipeline executed (25.17.9):** Simulation, local search, global search, pair plots, and ESS monitoring are all present, demonstrating methodological competence. The comparison of ESS before and after the model modification provides a concrete diagnostic signal.
- **Student-t observation model correctly implemented (25.17.12):** The dmeasure includes the Jacobian term `- (H/2)`, indicating careful attention to the log-density derivation for the scaled-t model.
- **T-GARCH benchmark included (25.17.11):** The paper directly compares the SV model to a GARCH benchmark, satisfying a key course expectation.
- **Self-critical Discussion (25.17.10):** The authors identify the regime-shift hard-coding as a "serious mistake" and propose a principled alternative (Weibull-based event timing). This level of self-reflection is valuable.

## Major Points

**25.17.3 — Hard-coded regime windows confound the leverage hypothesis test**
*Severity: Major*

The "amplitude" parameter modifying mu_h during t ∈ [262,275] and t ∈ [400,410] is applied to both the with-leverage and without-leverage models. These windows were chosen by visually inspecting the data being analyzed, introducing data-snooping bias. As a result, the AIC difference of 1.4 between the two models cannot cleanly be attributed to the leverage mechanism: the regime modification itself was tailored to the observed extremes. The central scientific conclusion — that leverage is attenuated in gasoline prices — rests on this comparison and therefore cannot be considered definitively established.

*Suggested author action:* For the leverage comparison, either (a) use the original Breto specification vs. a basic SV without regime modification, or (b) treat the window boundaries as estimated parameters. Present modified models as an exploratory extension only.

**25.17.4 — No profile likelihoods for any model parameter**
*Severity: Major*

Profile likelihoods are absent for all three POMP models. The text infers from the global search pair plots that sigma_nu approaches zero (Section 2.3.4), but this inference is unreliable without a formal profile. Pair plots show the joint distribution of filter estimates across mif2 runs, not likelihood profiles. Without profiles for sigma_nu, phi, tau, and amplitude, the identifiability of these parameters is unassessed and no confidence intervals can be reported.

*Suggested author action:* Compute profile likelihoods for at least sigma_nu (directly relevant to the leverage hypothesis) and tau (degrees of freedom). A profile for sigma_nu approaching zero would provide direct statistical support for the leverage-attenuation claim.

**25.17.1 — mif2 internal log-likelihood likely used in AIC table**
*Severity: Major*

The log-likelihoods in the AIC comparison table (437.1 for modified SV with leverage; 434.8 without leverage) are reported without Monte Carlo standard errors and without an explicit statement that they come from replicated pfilter runs on best mif2 parameters. The simulation-stage evaluations do report SEs (e.g., 0.079 and 3.38e-6), but these are for simulated data, not the actual data used in the AIC table. The mif2 internal likelihood is a biased estimate because particle perturbations inflate effective noise.

*Suggested author action:* For each model, extract the best parameter vector from the global search, run pfilter 10–20 times, compute logmeanexp, report the result with Monte Carlo SE, and use this value in the AIC table.

**25.17.6 — No mean-model baseline (ARMA/SARIMA)**
*Severity: Major*

The T-GARCH model captures conditional heteroskedasticity but is not a mean-model baseline. To establish that the stochastic volatility framework adds explanatory power over a linear model for the returns, an ARMA or SARIMA model should be fit and compared. Figure 19 (STL decomposition) reveals a strong seasonal pattern in the log returns. If significant mean-model structure is present, this should be captured before modeling the variance process.

*Suggested author action:* Examine ACF/PACF of the demeaned log returns, fit ARMA(p,q) models, and report AIC values.

## Minor Points

**25.17.14 — Seasonal pattern unmodeled**
*Severity: Minor*

Figure 19 (STL decomposition) shows a clear seasonal component with roughly annual periodicity in the gasoline log returns. This seasonal variation is not incorporated into any of the POMP models. The residual autocorrelation in the GARCH model at lags 1–2 (Figure 18) may partially reflect this unmodeled seasonality. Future work should consider a seasonal ARMA baseline or a seasonally-adjusted return series as input.

**25.17.2 — GARCH vs. SV likelihood scale: verification recommended**
*Severity: Minor*

The paper compares GARCH and SV log-likelihoods without explicitly verifying that both use the same normalizing convention for the t-distribution. The SV dmeasure correctly includes the Jacobian, and standard GARCH packages also compute full log-likelihoods. The comparison is likely valid, but a one-line statement confirming the software convention would strengthen the comparison.

**25.17.M1 — No simulation-based POMP model diagnostics**
*Severity: Minor*

GARCH residuals are diagnosed via QQ-plot and ACF (Figure 18), but no equivalent diagnostic is provided for the POMP models. Simulating from the fitted POMP model and comparing to the observed returns (e.g., simulation envelopes on quantiles) would help assess whether the SV model is adequately capturing the conditional distribution of returns.

**25.17.M2 — Initial conditions G_0 = H_0 = 0 unjustified**
*Severity: Minor*

Initial conditions for the latent states are fixed at zero without justification or sensitivity analysis. In SV models the initial log-volatility can affect early-sample inference, particularly when the data begin in a period of unusual volatility. A brief sensitivity check or a statement justifying why H_0 = 0 is appropriate for this dataset would strengthen the analysis.
