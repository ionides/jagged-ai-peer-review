# Final AI Review — w21 Project 14
# Mumps in Michigan 1970s: Seasonal SEIR POMP Model

---

## Overall Assessment

This paper fits a stochastic SEIR model with a seasonal contact rate to weekly Michigan mumps data (1971–1973) using the pomp framework. The biological motivation is sound, the implementation uses appropriate plug-and-play methods (mif2), and the likelihood is evaluated correctly via replicated particle filters with logmeanexp. However, the paper has several significant methodological gaps that prevent a confident assessment of model adequacy: there is no comparison to any non-mechanistic benchmark, model fit is shown only via unconditioned forward simulation rather than a filtering distribution conditioned on data, the profile likelihood for the reporting rate is effectively supported by very few high-quality evaluations near the peak, global optimization does not converge (particularly for the phase parameter Phi), and model diagnostics (ESS, conditional log-likelihoods) are absent. The conclusion that mumps "can be well modeled" by this SEIR model cannot be substantiated without quantitative comparison to a baseline.

## Key Strengths

- **Correct likelihood evaluation.** The authors correctly use logmeanexp over replicated pfilter runs to evaluate the log-likelihood, demonstrating sound understanding of Monte Carlo variability in particle filter likelihoods.
- **Negative binomial measurement model.** Overdispersion is accounted for via a negative binomial observation model, which is appropriate for count data where the binomial assumption of equidispersion is too restrictive.
- **Local convergence shown for most parameters.** The local mif2 trace plots (Figure 5) show reasonable convergence for b1, b2, Phi, and rho, suggesting the local search is functional.

## Major Points

**ID 21.14.6 — No non-mechanistic benchmark comparison.**
Severity: Major. The paper reports a best log-likelihood of approximately -500 for the SEIR model but provides no ARMA, ARIMA, or seasonal ARIMA baseline. Without a baseline, model adequacy cannot be assessed in absolute terms — a log-likelihood of -500 may be no better than a simple seasonal AR model. This is the single most important missing element.
Suggested action: Fit a seasonal ARIMA (or at minimum an ARMA on the log-transformed series) to the same 100-week data. Report its log-likelihood and AIC alongside the SEIR log-likelihood.

**ID 21.14.1 — Profile likelihood for rho is effectively very sparse near the peak.**
Severity: Major. Although the profile grid specifies 30 rho values, Figure 12 shows that most chains converge to likelihoods far below the maximum (falling outside the y-axis window), leaving only approximately 7 high-quality evaluations near the peak. The CI (11.14%–14.52%) is read off these few points and cannot be trusted. The loess smoother interpolates aggressively between sparse points, creating apparent smoothness that is not grounded in dense optimization.
Suggested action: Run a dedicated profile search with a fresh cooling schedule for each rho grid point, ensuring at least 20 well-converged evaluations near the maximum. Plot individual points before smoothing.

**ID 21.14.2 — Global mif2 convergence is poor, especially for Phi.**
Severity: Major. Figure 8 shows that most global chains spend more than 50 iterations at log-likelihoods between -100,000 and -25,000 before jumping to near -500. The phase parameter Phi remains spread across [0, 8] at iteration 100, indicating non-convergence. A methodological issue contributes to this: the global search uses `mif2(mifs_local[[1]], params=...)`, inheriting the already-cooled perturbation schedule from the local search. This substantially reduces the exploration capacity of the global phase.
Suggested action: Run global mif2 with a fresh cooling schedule (not inherited from local). Consider a second stage of mif2 starting from the top-ranking global candidates. Report the best log-likelihood from global search alongside the number of chains that converge within 2 log-likelihood units of the maximum.

**ID 21.14.7 — No particle filter diagnostics.**
Severity: Major. The paper does not plot ESS over time or conditional log-likelihoods. Without ESS monitoring, it is not possible to verify whether the particle filter is reliable at all 100 time points. Particle degeneracy at specific weeks (e.g., the spike at week approximately 65 in the data) could indicate model misspecification.
Suggested action: Run pfilter on the best-fit parameter vector and plot ESS and conditional log-likelihoods over the 100 weeks. Flag any time windows where ESS drops near 1.

**ID 21.14.5 — Goodness of fit shown by unconditioned forward simulation only.**
Severity: Major. Figures 7 and 11 show single stochastic simulations from the fitted parameters. This is not a goodness-of-fit diagnostic: forward simulation does not condition on data and mixes parameter and process uncertainty in a way that is uninformative about model adequacy. A filtering distribution (conditioned on observed data) should be used instead.
Suggested action: Plot the filtering distribution — median and 95% quantile band from repeated pfilter calls — overlaid on the observed data. This is the appropriate visualization of in-sample fit for a state-space model.

**ID 21.14.8 — Initial conditions fixed without justification.**
Severity: Major. The model initializes with E=20 and I=10 hardcoded, with no biological or data-based justification. For a 100-week time series beginning in September 1971, the starting values of E and I affect the likelihood for the initial time points. No sensitivity analysis is provided.
Suggested action: Either estimate E(0) and I(0) by including them as initial-value parameters with `ivp()` in rw.sd, or demonstrate robustness by showing that the maximum likelihood and key parameters are stable across a range of starting values (e.g., E(0) in {5, 20, 50}, I(0) in {5, 10, 30}).

## Minor Points

- **ID 21.14.3 — rho parameterization and reporting-rate interpretation.** The code implements `dnbinom(cases, H, rho, give_log)` where rho is R's `prob` parameter. Under this parameterization, E[cases|H] = H*(1-rho)/rho, not rho*H. The stated interpretation that rho approximately 12% means "12% of true cases are reported" is not numerically correct under this parameterization. The qualitative direction (low reporting) is unaffected, but the specific numeric CI (11.14%–14.52%) should be reinterpreted, or the measurement model should be reparameterized to directly encode the reporting rate.

- **ID 21.14.4 — b1/eta identifiability uncharacterized.** The global pairs plot shows a negative b1-eta slope suggesting a trade-off on the likelihood surface. No profile likelihood is computed for b1 or eta. Computing profile likelihoods for these parameters would either confirm identifiability or reveal that only their combination is estimable from case counts alone.

- **M1 — Cooling schedule inheritance in global search.** The global search calls `mif2(mifs_local[[1]], params=...)`, inheriting the cooling schedule of the completed local search. This means global chains begin with small perturbations, reducing exploration from distant starting points. This is a technical explanation for the "cliff" convergence pattern observed in Figure 8 and is worth flagging for future reference.

- **M2 — Seasonality assumption not verified in EDA.** The model assumes a 52-week seasonal period but no periodogram or decomposition is shown to confirm annual periodicity in the 100-week data. At minimum, a sentence noting this assumption and its plausibility should be added.

- **Conclusion overclaiming.** The conclusion states that mumps "can be well modeled by an SEIR POMP model," but this is not quantitatively substantiated without a benchmark. The conclusion should be qualified to state that the SEIR model captures seasonal structure qualitatively, pending a formal benchmark comparison.
