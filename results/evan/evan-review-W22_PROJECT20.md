# Final AI Review — w22 Project 20
# Statistical Analysis and Modeling of Flu Reports Time Series (SIRS/SARIMA)

---

## Overall Assessment

This paper makes a well-motivated scientific contribution: it attempts to model the dramatic drop in US influenza cases during 2020–2021 using a SIRS compartmental model with a time-varying transmission rate, testing whether a distinct pandemic-period parameter b is statistically different from the pre-pandemic rate a. The SARIMA section is technically competent, correctly diagnosing and fixing a near-unit MA root and applying an appropriate Box-Cox transformation. The SIRS model is correctly formulated as a POMP with binomial process noise, negative-binomial measurement error, and proper use of logmeanexp for particle filter likelihood aggregation. However, the paper's core hypothesis — that b < a with statistical significance — cannot be evaluated with the current computational results. The profile likelihood optimizations for both a and b produce degenerate confidence intervals (single-point min=max), and the IF2 traces show that key parameters have not converged. The paper would benefit substantially from additional computation and from correcting a mathematical inconsistency between the text and the implemented code.

---

## Key Strengths

- **Correct likelihood aggregation.** The use of `logmeanexp` over replicated `pfilter` evaluations (Section 4.5.1) reflects proper Monte Carlo log-likelihood estimation.
- **Negative-binomial measurement model.** The `dnbinom_mu` specification with estimated dispersion parameter k is appropriate for overdispersed count data.
- **SARIMA unit-root diagnosis.** The identification of the near-unit MA root in the initial SARIMA(2,1,2)×(1,1,0)_52 fit and the model simplification to (2,1,1)×(1,1,0)_52 demonstrates strong ARMA diagnostic practice.
- **Specific, testable hypothesis.** The formulation of the pandemic-drop hypothesis as H_0: a = b is a clear and appropriate scientific target, and the paper's design correctly anticipates what would be needed to test it.

---

## Major Points

**[22.20.1/2] Profile likelihood failure renders the central hypothesis untestable.**
Severity: Major

Both profile likelihoods produce degenerate confidence intervals: parameter a yields CI = [0.253, 0.253] and parameter b yields CI = [1.78, 1.78], meaning only a single evaluation point crosses the 95% cutoff in each profile. Inspecting fig_022 and fig_026 confirms that the profile points are widely scattered below the maximum, indicating that the profile optimization — which must maximize over nuisance parameters at each fixed value of a or b — has not converged. Consequently, no confidence interval for a or b is available, and the null hypothesis a = b cannot be formally tested.

Suggested author action: Increase Npoints_profile (to at least 30), Nreps_profile (to at least 10 per point), Nmif (to at least 100), and Np (to at least 2000–5000). Use a two-stage mif2 call per profile point. The profile trace (fixing a and optimizing over all other parameters) must show a well-defined peak for the resulting CI to be meaningful.

**[22.20.4] IF2 non-convergence.**
Severity: Major

The local search trace plots (fig_014) show that parameters a, b, mu_IR, mu_RS, and d continue to trend upward after 50 IF2 iterations. The paper itself acknowledges this ("do not show evidence of convergence yet") but proceeds to report downstream profile likelihoods and simulations based on these parameter estimates. MLE estimates from a non-converged search are unreliable, and the corresponding profile likelihoods will not locate the true maximum.

Suggested author action: At minimum, increase Nmif to 100 (or use the `mif1 %>% mif2()` double-run pattern already present in the profile code). Convergence is indicated when the loglik trace and parameter traces stabilize. Do not proceed to profile likelihood until the global search traces have plateaued.

**[22.20.5] Mathematical description uses cos, code uses sin.**
Severity: Major

The mathematical definition of the seasonal transmission rate (Section 4) specifies β(t) = β_0(t)(1 + c·cos(2π(t+d)/52)), but the C snippet implements `Beta = Beta0*(1 + c*sin(2*pi*(t+d)/52))`. These differ by a quarter-period shift. While the phase parameter d numerically absorbs this difference, the written model does not describe the implemented model, making the manuscript's results uninterpretable without running the code.

Suggested author action: Correct either the mathematical formula or the code to be consistent. Verify that the sign and reference convention for the phase parameter d is correctly reported and interpreted throughout.

**[22.20.6] b-profile trace plot has a copy-paste error.**
Severity: Major

The code for the b-profile trace plot groups by `round(a, 5)` and plots x=a, y=b — the same as the a-profile trace code — rather than grouping by b. As a result, fig_027 does not show the b-profile trace; it shows an a-b scatter from the b-profile runs. The reported visualization of the b-profile is therefore incorrect.

Suggested author action: Replace `group_by(round(a, 5))` with `group_by(round(b, 5))` and set x=b, y=a in the b-profile trace plot. Regenerate fig_027.

---

## Minor Points

- **[22.20.3] Likelihood comparison across model classes requires care.** The conclusion juxtaposes the SARIMA log-likelihood (~-162, on Box-Cox transformed data over 2010–2020) and the SIRS log-likelihood (~-2000, on raw counts over 2015–2021) without noting that these values are not on the same scale. They operate on different time windows, data transformations, and likelihood conventions and cannot be directly compared. Fit a simple baseline to the same 2015–2021 raw count data and report both on the same scale.

- **[22.20.7] Reporting rate rho fixed without sensitivity analysis.** The value rho = 4e-5 is derived from a rough back-of-envelope calculation and fixed throughout. Since rho directly scales expected observations (rho × H), uncertainty in rho propagates directly to uncertainty in a and b. Either estimate rho as a free parameter (the logit transform is already defined in partrans) or present a sensitivity analysis.

- **[22.20.8] Best-fit mu_IR = 7/week implies ~1-day recovery.** The best local search result reports mu_IR = 7.05. If the unit is week^-1, the expected recovery time 1/mu_IR ≈ 1 day, which is implausibly fast for influenza (typical infectious period 3–7 days). Verify the units and compare to published estimates; if implausible, consider adding a prior constraint or investigating model misspecification.

- **[22.20.M1] dmeasure likelihood guard `lik=0` is numerically incorrect.** The dmeasure code sets `lik = 0` when k < 0, rho < 0, or H < 0. In a log-likelihood context (give_log=1), the correct behavior is to return a very large negative number, not zero. Returning 0 can distort particle weights. Replace with `lik = (give_log ? R_NegInf : 0.0)` when the guard triggers.

- **Np=1000 at run_level=3 is low for final results.** Standard practice uses Np=5000 for final inference. The current setting increases Monte Carlo variability in all reported likelihood values.

- **AIC table headers garbled.** The AIC table in Section 3.1 has incomplete column headers and values that appear rescaled. Report actual AIC values with clear row and column labels.
