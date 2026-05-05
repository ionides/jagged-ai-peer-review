# Final AI Review: STATS 531 W25 Project 08
# Netflix Returns Analysis

---

## Overall Assessment

This project presents a structured, multi-method analysis of Netflix (NFLX) log-return dynamics relative to the S&P 500 ETF (SPY), covering EDA, ARIMA forecasting, GARCH/GJR-GARCH volatility modeling, and a Breto (2014) stochastic volatility model implemented as a POMP. The computational execution of the POMP component is largely sound: logmeanexp with replicated particle filters is used correctly for likelihood evaluation, both local and global IF2 searches are implemented with the run_level framework, MC standard errors are reported, and filter diagnostics (ESS and conditional log-likelihoods) are shown and discussed. However, the project has several significant weaknesses. The central empirical claim — that the POMP model outperforms GARCH/GJR-GARCH — is not established on a reliable quantitative basis. No profile likelihoods are computed despite being promised in the methods. A factual inconsistency in the ARIMA section (SPY model order) calls part of the ARIMA analysis into question. The measurement model notation is ambiguous. These issues substantially limit the conclusions that can be drawn and should be addressed.

---

## Key Strengths

**Correct particle filter likelihood evaluation (25.08.8)**
logmeanexp is applied across replicated pfilter runs throughout. This is the most critical computational requirement for POMP inference and is handled correctly.

**Dual search strategy with MC standard errors (25.08.9/10)**
Local and global IF2 searches are both implemented. Reporting MC standard errors on all log-likelihood estimates (e.g., 4622.8 +/- 0.85 for NFLX local search) enables the reader to assess the reliability of individual runs.

**Diagnostic rigor (25.08.11/12)**
Filter diagnostic plots (ESS and cond_logLik over time), convergence trace plots, and parameter pairs plots are all provided and discussed. The acknowledgement of two convergence clusters in the NFLX local search reflects careful inspection of the output.

---

## Major Points

**25.08.1 — Cross-model AIC/likelihood comparison is unreliable**
Severity: Major

The paper concludes in Section 8.1 that the POMP model "provides a better in-sample fit" than GARCH and GJR-GARCH based on log-likelihood comparisons. However, the reported GJR-GARCH AIC for NFLX is -9322.08, which (depending on the number of parameters) implies a log-likelihood of approximately 4661-4666 — higher than the POMP value of 4622.8. The paper does not verify consistent normalization across model classes. This comparison must be revisited before the claim of POMP superiority can stand. Provide all models' log-likelihoods explicitly, confirm the parameter count for GJR-GARCH with skewed-t, and verify that ARIMA and POMP log-likelihoods share the same normalization for the same data. If GJR-GARCH achieves a higher likelihood than POMP, revise the conclusion accordingly.

**25.08.6 — No profile likelihoods computed**
Severity: Major

Section 6.2 states the analysis will "inspect the pairwise likelihood surfaces to evaluate parameter identifiability." The pairs plots shown (fig_016, fig_019, etc.) are scatter plots of IF2 end-points, not profile likelihoods. Without profile likelihoods, no confidence intervals for key parameters (phi, mu_h) can be reported and the degree of identifiability remains qualitative. Compute profile likelihood for at least phi (persistence) using the MCAP procedure. Even a coarse grid with run_level=1 would be informative.

**25.08.4 — ARIMA model order inconsistency for SPY**
Severity: Major

The auto.arima output in Section 5.2 shows ARIMA(5,0,4) for SPY. The diagnostics summary table and all text descriptions refer to "ARIMA(2,0,0)" for SPY. One of these is incorrect. Verify which model was actually fit, update all tables and text accordingly, and re-check the associated AIC and BIC values.

**25.08.7 — Convergence multimodality not resolved**
Severity: Major

The NFLX local search (fig_018) shows two distinct log-likelihood clusters diverging from approximately iteration 20. The paper acknowledges this as evidence of local-maximum traps but does not take any remedial action. Extract the parameters from the top cluster and conduct at least one additional targeted local search initialized from the best parameters found. Without this, it is unclear whether the reported MLE is at a local or global maximum.

**25.08.3 — sigma_nu notation inconsistency in measurement model**
Severity: Major

The observation equation (Section 6.1) uses epsilon_n ~ N(0, sigma_nu) for measurement noise, while the G_n state equation uses nu_n ~ N(0, sigma_nu^2) for leverage variability. Both are labeled sigma_nu, but the code initializes a single `sigma_nu` parameter at exp(-6), which corresponds to leverage variability in the Breto (2014) formulation. The measurement noise appears to have no separate free parameter, or it shares the same label. Use distinct symbols (e.g., sigma_eps for observation noise and sigma_nu for the G_n random walk) consistent with Breto (2014).

---

## Minor Points

**25.08.5 — ACF interpretation contradicts stationarity claim**
Severity: Minor

Section 3.1 states the ACF shows "slow decay for both series, which is characteristic of non-stationary series," then concludes that log-returns are stationary. Log-return ACF for liquid equities is typically near zero at all lags. Revise the ACF description to match what is visible in fig_003 and fig_005; if significant slow decay is genuinely present, investigate the cause before proceeding with ARIMA.

**25.08.2 — mu_h estimates not back-transformed**
Severity: Minor

mu_h values of -7.6 (NFLX) and -9.4 (SPY) are discussed as "low long run volatility" without quantification. Report exp(mu_h/2) as the implied long-run daily volatility and compare against the sample rolling standard deviation. Also report the persistence half-life (-log(2)/log(phi)) so readers can assess economic plausibility.

**25.08.14 — Holdout set defined but not evaluated**
Severity: Minor

A holdout set covering 2023-2025 is constructed in Section 2.1 but is not used to evaluate any model's predictive accuracy. At minimum, report one-step-ahead forecast errors for the ARIMA model against the holdout. This would justify the train-test split design choice.

**25.08.M2 — Log-returns may not be demeaned before POMP fitting**
Severity: Minor

The POMP observation equation assumes Y_n has mean zero. Confirm that log-returns are explicitly demeaned before fitting, or add a mean parameter. If the sample mean is negligible (typical for daily returns), note this explicitly.

**Additional minor issues:**
- Incomplete author note in Section 8.2 ("Add direct discussions of how we expanded on the previous projects") should be completed or removed before submission.
- Incomplete sentence in Section 6.2 where the names of the two search procedures were omitted.
- The beta confidence interval formula in Section 7.4 assumes no ARCH effects; label as approximate given the explicit evidence of GARCH behavior found earlier in the paper.
