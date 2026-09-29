# Final AI Review: STATS 531 W24 Project 11
# NVIDIA Stock Price Analysis — ARMA, GARCH, and POMP Models

---

## Overall Assessment

This project applies ARMA, GARCH, and stochastic volatility POMP models to NVIDIA daily log-returns, with the goal of capturing volatility dynamics. The effort is commendable: the stochastic volatility model is mathematically well-specified using the Breto (2014) leverage framework, both local and global IF2 optimization are conducted, and filter diagnostics including ESS and conditional log-likelihoods are plotted. However, the analysis has several important weaknesses. Two of the three model fits (ARMA and GARCH) contain interpretive errors (ADF misinterpretation and likelihood comparison framing), and the POMP model fit shows clear signs of parameter non-identification that are not adequately diagnosed. The absence of profile likelihoods means no parameter uncertainty is quantified for the primary mechanistic model. The introduction promises forecasting but delivers none. As a result, the conclusions — particularly the ranking of POMP below GARCH and the interpretation of POMP parameter estimates — are not adequately supported.

---

## Key Strengths

| ID | Strength | Why it matters |
|----|----------|---------------|
| 24.11.12 | logmeanexp used correctly to aggregate particle filter likelihoods | Avoids the common error of averaging likelihoods on the natural scale, which gives a biased estimator |
| 24.11.13 | ESS and conditional log-likelihood filter diagnostics plotted for both local and global searches | Provides the reader visibility into particle filter health; a sign of methodological awareness |
| 24.11.14 | Both local and global IF2 searches conducted with MIF2 convergence trace plots | Global search with diverse starting points is the appropriate strategy for nonconvex likelihood surfaces |

---

## Major Points

**M1 (ID: 24.11.7/24.11.8/24.11.4) — POMP model is not identified along key parameters**

Severity: Major

The convergence trace plots (fig_011, fig_014) reveal three signs of non-identification: (1) sigma_nu collapses to approximately 0 in all chains, meaning the leverage correlation process G_n degenerates to a constant and the leverage effect disappears; (2) sigma_eta shows extreme spread across global search chains, ranging from roughly 2 to over 80, with no convergence band; (3) phi fails to converge consistently in the global search, with chains settling at values anywhere from 0.2 to near 1.0. These patterns indicate that the model is not identified — multiple parameter combinations produce similar likelihoods, and the maximum likelihood estimates cannot be trusted.

The appropriate response is not to run more IF2 iterations, but to compute profile likelihoods for the affected parameters, consider whether the model can be identified on this dataset, and potentially constrain or reparameterize.

Suggested action: Compute profile likelihoods for sigma_nu, phi, and sigma_eta. If the profile for sigma_nu is flat near zero, consider whether the leverage model is appropriate for this data or whether a simpler SV model (without leverage) should be the primary model.

**M2 (ID: 24.11.9) — No profile likelihoods or confidence intervals**

Severity: Major

No uncertainty quantification is provided for any estimated parameter in the POMP model. The paper presents point estimates and describes convergence behavior but does not compute profile likelihoods or confidence intervals. For a model with identifiability concerns (M1 above), this omission is especially consequential: without profile likelihoods, the reader cannot assess whether the parameter estimates are credible or merely one of many equivalent solutions.

Suggested action: Compute profile likelihoods for at least sigma_nu, phi, and sigma_eta using the MCAP approach. Report 95% confidence intervals.

**M3 (ID: NEW.1) — POMP measurement model uses Gaussian errors despite evidence that heavy-tailed errors are needed**

Severity: Major

The GARCH analysis section establishes that Gaussian residuals are inadequate for NVIDIA log-returns (the Shapiro-Wilk and Jarque-Bera tests reject normality, and the t-distributed GARCH(1,1) with shape parameter 6.78 is selected as the preferred non-mechanistic model). However, the POMP stochastic volatility model retains a Gaussian measurement equation Y_n = exp(H_n/2) * epsilon_n with epsilon_n ~ N(0,1). This is an inconsistency: the paper demonstrates heavy tails but then uses a model that cannot produce them. A t-distributed measurement model would be more consistent with the paper's own findings.

Suggested action: Consider replacing the Gaussian measurement with a t-distributed measurement error (e.g., epsilon_n ~ t(nu) with nu estimated). This would make the POMP model specification consistent with the GARCH results.

---

## Minor Points

**m1 (ID: 24.11.6) — ADF test result is misinterpreted**

Severity: Minor

The text states "the p-value is less than 0.01, which suggests we keep the null hypothesis that our time series is stationary." The ADF null hypothesis is that a unit root IS present (non-stationarity). A p-value < 0.01 means rejecting the null — this provides evidence against a unit root, supporting stationarity. The conclusion (stationarity supported) is correct, but the reasoning is backwards and reflects a misunderstanding of the test.

Suggested action: Correct the wording to "the p-value < 0.01 leads us to reject the null hypothesis of a unit root, supporting stationarity of the log-return series."

**m2 (ID: 24.11.3) — ARMA(2,2) has better AIC than selected ARMA(0,0) but is not discussed**

Severity: Minor

The AIC table shows ARMA(2,2) = -2173.11, which is 1.87 units lower (better) than ARMA(0,0) = -2171.24. The LRT is conducted only for ARMA(0,0) vs ARMA(0,1) and ARMA(1,0), not for ARMA(0,0) vs ARMA(2,2). The paper does not explain why ARMA(2,2) is dismissed despite its better AIC.

Suggested action: Either conduct an LRT comparing ARMA(0,0) against ARMA(2,2), or acknowledge that the AIC difference is small (~2 units) and argue parsimoniously for ARMA(0,0).

**m3 (ID: 24.11.11) — Numerical inconsistency in reported log-likelihoods**

Severity: Minor

The ARMA section reports ARMA(0,0) log-likelihood as 1087.62, while the conclusion section reports 1092. These differ by ~4 units. The source of this discrepancy is not explained.

Suggested action: Verify and reconcile the reported log-likelihood values across sections.

**m4 (ID: 24.11.15) — Particle filter ESS degeneracy near time ~300–350 not discussed**

Severity: Minor

Figures fig_010 and fig_013 show ESS dropping to near 0 and conditional log-likelihoods becoming highly negative around time step 300–350, which corresponds approximately to the period around May 2023 when NVIDIA had an exceptional one-day return of 0.218. This suggests the model struggles to filter through extreme return events. This is worth acknowledging.

Suggested action: Note that the particle filter degeneracy near the extreme May 2023 return event may indicate model misfit at tail events, consistent with the Gaussian measurement model's inability to handle heavy tails (see M3 above).

**m5 (ID: 24.11.10) — Typographical error in k-period log-return equation**

Severity: Minor

The k-period log-return equation reads r_t(k) = log(X_t / X_{t-1}) = r_t + r_{t-1} + ... + r_{t-k+1}, but the leftmost expression should be log(X_t / X_{t-k}), not log(X_t / X_{t-1}).

Suggested action: Correct the equation.

**m6 (ID: NEW.3) — Forecasting stated as a goal but not attempted**

Severity: Minor

The introduction explicitly states the goal is to "improve predictive accuracy regarding future stock prices," but no forecasts are produced in the analysis. The project would benefit from either demonstrating a simple out-of-sample forecast or removing the forecasting claim from the introduction.

Suggested action: Either produce a short-horizon forecast using the selected model, or revise the introduction to accurately reflect the actual scope of the analysis (in-sample model comparison and fitting).
