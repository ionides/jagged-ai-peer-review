# Final AI Review: An Analysis of COVID-19 Cases in Washtenaw County
## project15, w21

---

## Overall Assessment

This project demonstrates competent application of the pomp likelihood-based framework to COVID-19 case data in Washtenaw County. The authors correctly use iterated filtering (IF2) with logmeanexp aggregation of replicated particle filter evaluations, conduct a broad global search from 500 random starting points, and honestly acknowledge that their SEIR model is outperformed by a seasonal ARMA benchmark. The step-function transmission rate beta is a reasonable modeling choice for accommodating multiple epidemic waves, and the comparison against both a negative binomial i.i.d. baseline and a SARMA(3,3)x(1,1)_7 model is a genuine contribution. The main areas for improvement are the sparsity of the profile likelihood for rho, the absence of convergence diagnostics for the global search, and the lack of profiles for the five beta parameters that are central to the scientific conclusions.

## Key Strengths

- **21.15.m9 — Correct MC likelihood aggregation.** logmeanexp is consistently used to aggregate replicated pfilter log-likelihoods. This is the correct procedure and is implemented throughout local search, global search, and profile likelihood evaluation.
- **21.15.m11 — Broad global search.** Five hundred random starting points from a uniform box covering a wide parameter space is thorough, and the scatter matrix (fig_007, fig_008) shows convincing convergence of the IF2 estimates to a consistent region.
- **21.15.m12 — Honest benchmarking.** The authors correctly report that the SEIR model log-likelihood (-1,151.66) is worse than the SARMA benchmark (-1,104.23, on comparable scales) and attribute the gap to an unmodeled 7-day weekly cycle. This is an intellectually honest and informative conclusion.

## Major Points

**21.15.M2 — Profile likelihood for rho is too sparse to support the reported CI.**
The profile likelihood plot (fig_009) shows approximately 25 scattered points with only 3 above the 95% chi-squared threshold (MLE - 1.92). The reported CI [40.97%, 48.01%] rests on these 3 points and the profile surface is noisy near the maximum. The authors themselves note caution is warranted. With so few points above the cutoff, the CI boundaries are effectively determined by single observations and may shift substantially with additional computation.
*Severity: Major.*
*Suggested action:* Re-run the profile with finer resolution in rho in [0.35, 0.55], targeting at least 5–10 points above the threshold. Report the resulting CI only when the profile surface is smooth enough to identify clear boundary crossings.

**21.15.M3 — No convergence diagnostics for the global search.**
The global search code runs seven sequential mif2 passes per starting point, but no trace plots of loglik or parameters vs. IF2 iteration are shown for the global search runs. The scatter matrix (fig_007, fig_008) shows where the optimization ended up, but not whether those runs converged. Some local-search traces (fig_005) show b3 reaching implausible values (~100) and b4 reaching ~20 in some chains, suggesting the likelihood surface is challenging to navigate. Without global search traces, it is not possible to verify that the reported MLE (-1,151.66) is a genuine optimum rather than a locally-trapped value.
*Severity: Major.*
*Suggested action:* Include trace plots for loglik and key parameters (e.g., b1, b5, rho) from the global search, analogous to fig_005 for the local search. Even a summary showing the top 20 runs' loglik vs. iteration would substantially improve confidence in convergence.

## Minor Points

- **21.15.M4 — ARMA benchmark comparison: explain the Jacobian correction.** The code computes `arma33_s11$loglik - sum(log_cases)`, which correctly converts the ARMA log-likelihood from the log-transformed scale to the original count scale, making it comparable to the SEIR log-likelihood. However, the paper does not explain this step. Readers may not realize the correction is applied, or may question whether the sign is correct. *Suggested action:* Add one sentence explaining that the ARMA log-likelihood is adjusted for the log(y+1) transformation via a change-of-variables Jacobian correction.

- **21.15.M1 — Sensitivity of fixed mu_EI and mu_IR.** These rates are fixed at 0.1 throughout the global search, based on CDC guidance. While this is defensible given the external evidence, the remaining estimated parameters (especially rho and eta) are sensitive to these choices, and no sensitivity runs are reported. *Suggested action:* Add a brief sensitivity check: re-run the global search with mu_EI = 0.07 and mu_EI = 0.2 and compare the resulting MLE and rho estimate.

- **21.15.M5 — Fixed initial conditions E_0=100, I_0=200 without sensitivity.** These values are fixed based on a narrative argument about external travelers. The early-period dynamics depend on these choices, and no sensitivity analysis is provided. *Suggested action:* Report how the log-likelihood and rho estimate change when E_0 and I_0 are varied by a factor of 2 (e.g., E_0 in {50, 100, 200}).

- **21.15.m7 — Run-level parameters not reported.** Np, Nmif_S, Nmif_L, NREPS_LOCAL, NREPS_EVAL, and NSTART are used in the code but never stated in the text. The reader cannot assess computational adequacy. *Suggested action:* Report these values in a computational summary paragraph or table.

- **21.15.m8 — ESS not reported.** Effective sample size from the particle filter is not monitored. With Np=500 and early epidemic dynamics that may produce degenerate filtering distributions, ESS could be low during certain intervals. *Suggested action:* Add ESS monitoring or report minimum ESS encountered during the best-fit pfilter run.

- **21.15.m14 — Truncated normal measurement model lacks justification.** Negative binomial is the standard choice for overdispersed count data in epidemic POMP models. The truncated normal is used without comparing to negative binomial or citing a specific reason for the preference. *Suggested action:* Either fit a negative binomial measurement model as an alternative, or provide explicit justification for the normal approximation.

- **21.15.new1 — No profiles for beta parameters.** Five contact-rate parameters (b1–b5) drive the multi-wave structure and are the primary scientific result. No profile likelihoods are shown for any of them, making it impossible to assess their individual identifiability or construct CIs. *Suggested action:* Add profile likelihoods for at least two scientifically important periods (e.g., b2 for the spring lockdown phase, b5 for the fall wave).

- **21.15.new2 — Forward simulation vs. filtering distribution.** Figures 4 and 6 show forward simulations from the MLE parameters, not filtering-distribution-conditioned simulations. These are unconditional forward projections and show what the model can produce in principle, not how well it fits the observed trajectory conditional on the data. *Suggested action:* Note in the figure captions that these are forward simulations, and consider adding a filtering-based diagnostic (e.g., conditional log-likelihoods plotted over time) to complement the visual fit.

- **21.15.m6 — Pathological divergence in local search traces.** Fig_005 shows b3 traces reaching ~100 in some chains. This is not discussed. *Suggested action:* Briefly acknowledge this in the text and note that the global search was designed to overcome such local optima.
