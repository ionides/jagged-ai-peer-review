# Final AI Review — w21 Project 12
# Nasdaq-100 Index Volatility Analysis: ARMA, GARCH, and POMP

---

## Overall Assessment

This project applies a well-structured sequence of time-series models — ARMA(3,1), GARCH(1,2), and a POMP stochastic leverage model following Breto (2014) — to five years of Nasdaq-100 daily log-returns. The POMP implementation is technically sound: the covariate structure is correctly used to handle the leverage correlation, parameter transformations are appropriate, and logmeanexp is correctly applied to aggregate replicated particle filter log-likelihoods. A global search over a parameter box is performed, which is good practice. However, standard convergence and identifiability diagnostics are absent, the conclusion overstates the evidence, and several minor presentation issues undermine the manuscript. The overall result demonstrates competence with the POMP framework but needs stronger inference infrastructure to support its conclusions.

---

## Key Strengths

- **ID 21.12.9 — Correct likelihood aggregation.** The logmeanexp function is correctly applied to combine replicated particle filter log-likelihoods, avoiding the common error of averaging log-likelihoods directly. This is a technically important detail.

- **ID 21.12.12 — Faithful POMP implementation.** The code correctly implements the Breto (2014) stochastic leverage model, including the tanh transformation for leverage and the covariate table structure for passing observed returns to the latent process.

- **ID 21.12.13 — Appropriate parameter transformations.** The `partrans` object correctly applies log transforms to sigma_eta and sigma_nu (positivity constraints) and a logit transform to phi (unit interval constraint), ensuring numerically stable IF2 optimization.

- **ID 21.12.15 — Adequate computational effort.** Running at run_level=3 with Np=2000, Nmif=200, 20 local replicates, and 100 global replicates represents a serious computational investment appropriate for a final project.

---

## Major Points

**ID 21.12.7 — Missing IF2 convergence diagnostics.**
Severity: Major. The paper shows a pairs scatter plot from the local search but no IF2 convergence traces (log-likelihood vs. iteration, parameter values vs. iteration). Without trace plots it is impossible to determine whether IF2 has converged: the algorithm may have stalled, the cooling schedule may be too aggressive, or the search may be terminating before reaching the likelihood plateau. The finding that best logLik ≈ 3980 (global) vs. 3974 (local) suggests global search helps, but without traces the nature of improvement is unknown.
Suggested author action: Add convergence trace plots for at least one representative IF2 run from both local and global searches, overlaying multiple replicates on the same plot to verify terminal convergence.

**ID 21.12.8 — No profile likelihoods or confidence intervals.**
Severity: Major. The paper reports point estimates for all six POMP parameters but provides no profile likelihoods and no confidence intervals. The pairs scatter plot is not a substitute: it shows the distribution of estimates across IF2 runs (which reflects optimization variability), not the likelihood surface. The pairs plot shows sigma_eta ranging over an extremely wide range in some runs (values up to ~300 visible), indicating that some parameters are poorly identified or that some runs failed to converge. Statistical conclusions about parameter values — including phi ≈ 0.97 as evidence of volatility persistence — require profile-based inference.
Suggested author action: Compute profile likelihoods for at least phi and sigma_eta. Report 95% confidence intervals using the MCAP or likelihood-ratio method.

---

## Minor Points

- **ID 21.12.6 — No ESS monitoring.** Effective sample size during particle filtering is not reported. In stochastic volatility models, particle degeneracy can be severe, especially during high-volatility episodes (e.g., the March 2020 COVID crash visible in the data). Report ESS for at least one particle filter evaluation run.

- **ID 21.12.5 — Simulated data pfilter result not reported.** The text states "The log likelihood seems to be very low" for the initial parameter values on simulated data, but the numerical value from `L.pf1` is not printed. A simulation check is only informative if the baseline likelihood value is given.

- **ID 21.12.1 (revised) — AIC comparison across model classes lacks qualification.** The paper directly compares AIC from arima(), tseries::garch(), and a particle filter without noting whether these likelihoods are on the same scale. While all three models specify a density over the same observed return sequence, normalization conventions can differ across packages. A brief note acknowledging this and verifying same-scale computation would strengthen the comparison.

- **ID M1 — Normal measurement model for heavy-tailed returns.** The POMP model specifies Y_n ~ N(0, exp(H_n/2)), a Gaussian measurement model. The paper itself notes heavy-tailed residuals in both ARMA and GARCH fits. The POMP model inherits the same limitation. A Student-t measurement model is standard in the financial stochastic volatility literature and would be worth mentioning as a natural extension.

- **ID M2 — Conclusion overstates model adequacy.** The conclusion states the POMP model is "appropriate for the Nasdaq-500 data" and interprets parameters as easier to interpret in financial studies. These claims are too strong given that convergence has not been verified, parameter identifiability has not been assessed, and the measurement model has unaddressed tail issues. The conclusion should be qualified accordingly.

- **ID 21.12.4 — Extreme sigma_eta values in pairs plot.** Some IF2 local-search replicates produce sigma_eta values far from the reported point estimate (pairs plot suggests some runs near ~300). These outlier runs are not commented on and may indicate numerical issues for a subset of replicates. Filtering or reporting the range of terminal likelihoods across replicates would clarify whether these are consequential failures.

- **ID 21.12.10 — Naming error.** The conclusion and final paragraph refer to "Nasdaq-500" three times; the index is the Nasdaq-100. Correct throughout.

- **ID 21.12.11 — ACF figure ambiguity.** Figure 5 is labeled "Nasdaq-100 Index return" but appears in the context of ARMA(3,1) residual diagnostics. Confirm and relabel to specify whether this is the ACF of raw returns or model residuals.
