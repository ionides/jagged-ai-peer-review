# Final AI Review
## Project: final_project_w22 / project01
## Topic: CS:GO online player count — stochastic leverage (POMP) model

---

## Overall Assessment

This paper applies a financial volatility modeling pipeline — ARIMA, GARCH, and a POMP stochastic leverage model adapted from Breto (2014) — to daily CS:GO online player count data covering the COVID-19 period (2020–2021). The creative reframing of the log daily change in player counts as a financial "return" is an interesting conceptual move, and the project follows a recognizable course pipeline. However, the paper is undermined by several substantive methodological errors. Most critically, the log-likelihoods reported in the summary table are computed on different transformations of the data, making the central comparison — and the conclusion that "ARIMA performs best" — invalid as stated. The POMP optimization produces openly non-converged parameter estimates, and key inferential outputs (profile likelihoods, confidence intervals) are entirely absent. The paper would need revision addressing these issues before its conclusions can be trusted.

---

## Key Strengths

**22.01.S1 — Correct use of logmeanexp.**
The paper uses `logmeanexp(replicate(..., logLik(pfilter(...))), se=TRUE)` throughout, which is the correct way to aggregate replicated particle filter log-likelihoods while accounting for Monte Carlo variability. This is a frequently missed detail that the paper handles correctly.

**22.01.S2 — Global optimization with randomized starting values.**
One hundred global search replicates are run from a box spanning plausible parameter ranges at run_level = 3. This is an appropriate strategy for navigating a multi-modal likelihood surface and reflects sound computational practice.

**22.01.S3 — Weekly seasonality identified and cross-validated.**
The weekly periodicity is identified both from the ACF (Figure 3, period ≈ 7 lags) and the periodogram (Figure 4, dominant frequency ≈ 0.143 cycles/day). Independently confirming the same cycle with two methods strengthens the EDA.

---

## Major Points

**22.01.1 — Invalid log-likelihood comparison across model classes.**
ID: 22.01.1 | Topic: inference | Severity: Major

The conclusion table compares log-likelihoods across ARIMA(5,1,5) (logLik = 1439.5), GARCH(5,5) (logLik = 1170.1), and POMP (logLik = 1280). These likelihoods are not comparable as presented. ARIMA(5,1,5) uses `d=1`, so it is fitted to the once-differenced demeaned log-returns, while GARCH and POMP are fitted to the undifferenced demeaned log-returns. The two likelihoods are evaluated on series of different lengths and different variables. Additionally, the ARIMA likelihood adjustment in the code (`ARIMA515$loglik - sum(log_df2$demean_players)`) is not explained and its correctness is unclear. The paper's conclusion that "ARIMA performs best" rests entirely on this table and is therefore unsupported.

Suggested action: Either fit all models to the same response variable (the undifferenced demeaned log-returns), or explicitly discuss why the likelihoods are on different scales and refrain from declaring a winner. At minimum, retract the conclusion that ARIMA outperforms GARCH and POMP.

**22.01.2 — Best benchmark model not used; AIC difference misread.**
ID: 22.01.2 | Topic: benchmark | Severity: Major

The AIC table shows SARIMA(5,0,5)×(1,0,1)_7 achieves AIC = −2938.1, compared to ARIMA(5,1,5) at AIC = −2857.1 — a difference of approximately 81 AIC units. The paper nonetheless selects ARIMA(5,1,5) as the benchmark, justifying this by saying "there is not much difference in the AIC values." This misreads the table by 80 points. The correct benchmark by AIC is SARIMA(5,0,5)×(1,0,1)_7. Using the inferior model as a benchmark weakens the comparison against GARCH and POMP.

Suggested action: Correct the model selection. Use SARIMA(5,0,5)×(1,0,1)_7 (or justify a simpler model on grounds of parsimony, not AIC proximity).

**22.01.4 — Differencing of an already-stationary series, without justification.**
ID: 22.01.4 | Topic: arma | Severity: Major

The input series (`log_df2$demean_players`) is the demeaned log-return of player counts — already a first difference of the log-count. Fitting ARIMA with `d=1` applies a second first-difference with no stationarity argument. The ACF in Figure 3 shows rapid decay consistent with a stationary series. No ADF or KPSS test is presented to justify an additional unit root.

Suggested action: Provide a formal stationarity test (ADF or KPSS) on the demeaned log-returns before applying differencing. If the series is already stationary, use ARMA (d=0) instead.

**22.01.8 — Non-convergence explicitly acknowledged but MLE reported as valid.**
ID: 22.01.8 | Topic: diagnostics | Severity: Major

After the global optimization, the paper states: "mu_h, phi, sigma_eta, G0 and H0 do not converge at all." Despite this, a maximum log-likelihood of 1280 is reported from these runs and used in the final comparison. A non-converged optimization means the reported MLE is an underestimate of the true maximum, and the parameter estimates have no interpretive standing.

Suggested action: Increase Nmif and/or Np, or expand the number of global search replicates, until convergence is achieved. Show trace plots with evidence of stabilization before reporting parameter estimates. Alternatively, acknowledge explicitly that results are preliminary bounds and the true optimum is unknown.

**22.01.3 — sigma_nu at or near zero (parameter boundary).**
ID: 22.01.3 | Topic: identifiability | Severity: Major

The best-fit parameter table (kable output) shows sigma_nu = 0. This is a parameter boundary: sigma_nu controls the volatility of the random walk on G (the leverage state). A value of zero collapses the stochastic leverage model to a deterministic leverage model. This is a substantive model specification finding — the data may not support random leverage — but it is completely unremarked in the paper.

Suggested action: Examine whether sigma_nu is identifiable by computing a profile likelihood across a range of sigma_nu values. Discuss whether the stochastic leverage model is needed, or whether a simpler model (fixed leverage or no leverage) fits comparably.

**22.01.6 — No profile likelihoods or confidence intervals for any parameter.**
ID: 22.01.6 | Topic: identifiability | Severity: Major

All parameter estimates (phi, mu_h, sigma_eta, G_0, H_0, sigma_nu) are reported as point estimates only. No profile likelihoods are computed and no confidence intervals are provided. Given the acknowledged non-convergence and the boundary hit on sigma_nu, parameter uncertainty is substantial and completely uncharacterized.

Suggested action: Compute profile likelihoods for at least phi and sigma_eta. Report 95% confidence intervals using MCAP or likelihood-ratio inversion. This is essential for any mechanistic modeling conclusion.

---

## Minor Points

**22.01.G — GARCH model name, equation, and code are inconsistent.**
The text says "GARCH(5,5)" but the written equation is GARCH(1,1) (one lag of Y^2, one lag of V), and the code calls `garch()` with no order argument (default in the `tseries` package is (1,1)). The paper is describing and fitting a GARCH(1,1) under the name GARCH(5,5).
Suggested action: Correct the model name to GARCH(1,1) to match the equation and code.

**22.01.5 — Filtering step on simulated data is not clearly labeled.**
The particle filter producing L.pf1 = 518.39 is run on `sim1.filt2`, which is constructed from the simulated object `sim1.sim` rather than the real data. This value is presented in the narrative as "we carry out replicated particle filters at our initial guess" without noting it is on synthetic data. The actual inference uses `sim1.filt` (real data), so the impact on results is limited, but the narrative is misleading.
Suggested action: Clarify that L.pf1 is a validation exercise on simulated data, not a likelihood estimate for the real data.

**22.01.M1 — ESS not monitored during particle filtering.**
Effective sample size (ESS) during filtering is never reported. Low ESS can indicate particle degeneracy.
Suggested action: Add `plot(pfilter(...))` or extract ESS from pfilter output to confirm filter health.

**22.01.M2 — Causal language without causal identification.**
The introduction states the paper investigates how COVID-19 "caused" the player increase. The analysis is purely observational; no causal identification strategy (e.g., difference-in-differences, interrupted time series with control) is employed.
Suggested action: Replace "caused by" with "associated with" or "coinciding with" throughout.

**22.01.M3 — Title typo: "Pandamic" should be "Pandemic."**

**22.01.M4 — No sensitivity analysis for the box search bounds on G_0 and H_0.**
The global search bounds for G_0 (−2 to 2) and H_0 (−1 to 1) are not justified. If the true optimum lies outside these bounds, the reported MLE is artificially constrained.
Suggested action: Report the distribution of best-fit G_0 and H_0 values from the global search; if estimates cluster near the boundary, widen the box.
