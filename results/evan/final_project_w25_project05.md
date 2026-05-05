# Final AI Review: Analysis of Malaria Cases in Florida

## Overall Assessment

This project analyzes monthly malaria counts in Florida (2006–2016) using a SARIMA model and an adapted SEIR-with-splines POMP model with an immigration term. The adaptation of a dengue POMP model to malaria is scientifically motivated and the immigration term is well-reasoned given that Florida malaria is predominantly imported. Computational effort is reasonable — a global search with 20 starting points using logmeanexp-aggregated pfilter replicates follows course conventions. However, the project has three major methodological problems that undermine its conclusions: the comparative evaluation between SARIMA and POMP is statistically invalid, no profile likelihoods or confidence intervals are provided for any parameter, and convergence diagnostics indicate the search has not yet converged. These issues prevent drawing reliable conclusions about model adequacy or parameter estimates.

## Key Strengths

**S-1 (25.05.9) — Correct likelihood evaluation.** The authors correctly use `logmeanexp` over 10 replicated `pfilter` runs (Np = 2000–4000) to obtain stable log-likelihood estimates. This avoids the common error of reporting a single particle filter evaluation or averaging log-likelihoods directly.

**S-2 — Reasonable global search effort.** Twenty starting points with Np = 2000, Nmif = 100, and 10 pfilter replicates at Np = 4000 for evaluation represents a genuine effort to explore the likelihood surface.

**S-3 — Scientifically motivated model adaptation.** The decision to add an immigration parameter is grounded in the epidemiology: malaria has been locally eradicated in Florida and reported cases are almost entirely imported. This mechanistic insight is a genuine contribution relative to a direct application of the dengue model.

## Major Points

**ID: 25.05.1 | Concern: Invalid SARIMA vs. POMP likelihood comparison | Severity: Major**

The Comparison section states: "as seen in the difference in likelihoods between the SARIMA model (−96) and the POMP models (−328), there is a significant scope for improvement in the mechanistic models." This comparison is not valid. The SARIMA model is fit to `log1p(monthly_cases)`, a continuously transformed variable, while the POMP model is fit to raw integer counts Y. The two log-likelihoods involve different observation distributions and response scales; they cannot be directly compared. The paper's conclusion that the POMP model is inferior to SARIMA by a margin of ~232 log-likelihood units does not follow.

*Suggested author action:* Either remove the direct comparison entirely or fit a count-data baseline (e.g., auto-regressive negative binomial on raw counts) at the same scale as the POMP model. Alternatively, acknowledge explicitly that the two likelihoods are not on the same scale and that no conclusion about relative fit can be drawn from this comparison.

**ID: 25.05.4 | Concern: No profile likelihoods; scatter plots are not profiles | Severity: Major**

The scatter plots in fig_010 (loglik vs. parameter value) display the endpoint parameter values from 20 global optimization runs at their final log-likelihood. These are not profile likelihoods. A profile requires fixing a target parameter at a grid of values, re-optimizing all other parameters at each grid point, and plotting the resulting maximized likelihood. Without profiles, no confidence intervals can be computed, and identifiability of individual parameters cannot be assessed. With 14+ free parameters and 132 data points, identifiability is a pressing concern.

*Suggested author action:* Compute profile likelihoods for at least the most epidemiologically important parameter (immigration_rate, ρ, or σ_P). Report 95% confidence intervals using the profile likelihood cutoff (χ²(1)/2 ≈ 1.92 log-likelihood units) or the MCAP method.

**ID: 25.05.5 | Concern: Unconverged parameter traces | Severity: Major**

The trace plots (fig_009) show that multiple parameters — including gamma, mu_EI, rho, sigma_P, immigration_rate, and epsilon — remain widely dispersed across the 20 chains at iteration 100 with no plateau. The log-likelihood trace is still increasing at the final iteration. This means the reported best parameter estimates and best log-likelihoods are preliminary. The conclusion that the immigration model achieves loglik ≈ −329.8 should be treated as a lower bound on the achievable likelihood, not a stable estimate.

*Suggested author action:* Increase Nmif to at least 200–300 and verify that the log-likelihood trace has flattened. Report results only when convergence is established. If computation is prohibitive, clearly label all results as preliminary.

## Minor Points

**ID: 25.05.2 | Concern: sigma_M declared but has no effect in code | Severity: Minor**

The parameter sigma_M = 0.3 appears in paramnames and in the parameter transformation vector but is absent from the dmeasure C-snippet (`dpois(Y, rho * I + 1e-6, give_log)`). The measurement model is equidispersed Poisson, not a negative binomial with overdispersion sigma_M as the model description implies. This is misleading.

*Suggested author action:* Either implement negative binomial measurement noise using sigma_M (as done in the source dengue paper), or remove sigma_M from the parameter vector and acknowledge that the measurement model is Poisson.

**ID: 25.05.6 | Concern: sma1 = −1.000 at the invertibility boundary | Severity: Minor**

The fitted SARIMA yields sma1 = −1.000 (SE = 0.197). A coefficient of exactly −1 places the seasonal MA polynomial on the boundary of the invertibility region. This can indicate overdifferencing (applying D = 1 when seasonal differencing is not needed) or that the model order is not appropriate. The code checks and reports "invertible," which is technically true at the boundary, but this result warrants discussion.

*Suggested author action:* Discuss the boundary estimate. Consider whether D = 1 is appropriate, and compare AIC for models with D = 0.

**ID: 25.05.7 | Concern: Population growth rate r is biologically implausible | Severity: Minor**

The initial parameter sets r = 0.135 month^{-1}, which implies 13.5% monthly population growth — corresponding to roughly 4-fold annual growth. This is clearly implausible for a U.S. state population. The parameter likely originates from the source dengue paper using a different time unit or interpretation. Although the global search reduces this to r ≈ 0.033, even 3.3% monthly growth is unrealistic.

*Suggested author action:* Clarify the intended time units for r and correct the initial value to a realistic figure (e.g., ~0.1% per month for U.S. demographic growth).

**ID: 25.05.10 | Concern: SARIMA equation notation error | Severity: Minor**

The SARIMA model equation writes `(1 + θ_1)(1 + Θ_1 B^{12})ε_t`, omitting the backshift operator B from the non-seasonal MA polynomial. The correct expression is `(1 + θ_1 B)(1 + Θ_1 B^{12})ε_t`.

*Suggested author action:* Correct the equation to include the B operator in the non-seasonal MA polynomial.

**ID: M-1 | Concern: ESS not monitored during particle filtering | Severity: Minor**

The effective sample size (ESS) of the particle filter is not reported or monitored. Very low ESS indicates filter degeneracy, which can cause unreliable likelihood estimates. Given the relatively small particle count (Np = 1000 in local search), monitoring ESS provides useful diagnostic information.

*Suggested author action:* Report minimum or average ESS from representative pfilter runs to confirm the filter is not degenerating.
