# Final AI Review: w22 Project 14
# Analysis of Stochastic Volatility Models for Ethereum Returns

## Overall Assessment

This project tackles an interesting and challenging problem — modeling hourly Ethereum return volatility using mechanistic stochastic volatility (SV) models from the POMP framework — and makes a commendable contribution by fitting two competing SV model classes (Breto leveraged SV and a discretized Heston SV) against AR and AR-GARCH benchmarks. The Heston model's reported log-likelihood (34975) substantially exceeds that of the Breto model (28977) and the AR-GARCH benchmark (28587), suggesting a genuine improvement in fit. However, several inferential and computational problems prevent the comparison from being accepted at face value: the Breto model has not converged, all POMP models show severe pervasive effective sample size (ESS) collapse that suggests the Gaussian measurement model is misspecified, the Heston local search MIF2 trace declines monotonically (which is a pathological sign), and no profile likelihoods or confidence intervals are reported for any parameter. Addressing these issues would substantially strengthen the conclusions.

## Key Strengths

| ID | Strength | Why it matters |
|----|----------|----------------|
| 22.14.S1 | Two POMP SV model classes compared against each other and against non-mechanistic benchmarks | Provides structured model comparison at multiple levels of complexity |
| 22.14.S2 | Filter diagnostics (ESS, conditional log-likelihoods) shown for all POMP fits | Supports transparency about particle filter performance |
| 22.14.S3 | Forward simulation panel vs actual volatility (fig_017) | Provides a sanity check on the Heston model's simulated behavior |
| 22.14.10 | AR(4) and AR-GARCH models included as principled benchmarks | The AR-GARCH is an appropriate non-mechanistic competitor for volatility modeling |

## Major Points

**22.14.3 — Severe ESS Collapse Throughout Filtering (Gaussian Measurement Model)**
Severity: Major

Figures 011, 015, and 022 all show ESS regularly dropping to values near 1–5 throughout the full time series in every POMP model fitted. This is not confined to the single outlier event on May 19, 2021 — it occurs broadly and repeatedly. A pervasive ESS collapse of this kind indicates that the measurement model is assigning near-zero probability to many observed returns. The most likely cause is the Gaussian noise assumption: Y_n = exp(H_n/2) * epsilon_n (Breto) or equivalent (Heston) will catastrophically downweight any large return, of which there are many in hourly crypto data. The Q-Q plot of AR-GARCH residuals (fig_007) already shows extreme heavy tails — the same underlying observations drive both fits. This level of ESS collapse makes the reported log-likelihoods unreliable as absolute measures and compromises the comparisons.

Suggested author action: Consider a t-distributed measurement model (e.g., Y_n = exp(H_n/2) * t_nu where nu is estimated) or a variance-gamma specification. Report what fraction of time steps have ESS below 10% of Np and whether the collapse pattern is limited to specific time periods or is pervasive.

**22.14.4 — Breto Model Non-Convergence**
Severity: Major

Figure 016 (Breto global search convergence) shows sigma_eta drifting to extreme values (~3×10^5) for at least one chain throughout 200 MIF2 iterations, while mu_h shows no clear convergence and H_0 traces fan out. The paper describes this as "the convergence plot seems better than the local search," which understates the problem. When chains in the global search are still wandering at extreme parameter values after 200 iterations, the reported maximum log-likelihood of 28977 is a lower bound on the true Breto MLE, not the MLE itself. This means the 6000 log-unit gap between Heston (34975) and Breto (28977) could be partially explained by computational failure rather than genuine model differences.

Suggested author action: Run more MIF2 iterations for the Breto model until sigma_eta stabilizes across all chains, or explicitly caveat the comparison. If the gap persists after full convergence, the Heston advantage is confirmed; if it narrows, the conclusion changes.

**22.14.5 — Heston Local Search: Declining MIF2 Log-Likelihood Trace**
Severity: Major

Figure 020 shows the Heston local search loglik trace declining monotonically from ~35500 at iteration 0 to ~34500 by iteration 200. This is the opposite of the expected pattern (log-likelihood should increase or stabilize). A declining trace at the local search stage suggests the MIF2 perturbations are moving parameters away from good starting values. The paper does not comment on this in Section 4.2. The global search (Section 4.3) appears to recover, but it is worth understanding why the local search degraded.

Suggested author action: Report the Np, Nmif, and cooling schedule used. A larger Np or a more gradual cooling schedule may prevent this pathology. The declining local search trace should be explicitly acknowledged and the run settings used to obtain the global search results reported.

**22.14.6 — No Profile Likelihoods or Confidence Intervals**
Severity: Major

Neither the Breto model nor the Heston model includes any profile likelihood analysis or confidence intervals for the parameters. The pair plots (figs 013, 016, 021) show scatter across mif2 runs but these are not profile likelihoods. Without profile likelihoods, it is not possible to assess whether parameters like phi (mean reversion), sigma_omega (volatility of volatility), or theta (long-run variance) are identifiable from the data. The text acknowledges that mu_h shows "uncertainty" based on trace plot spread, but this is not a quantitative statement.

Suggested author action: Compute a profile likelihood for at least one key parameter in the Heston model (phi is a natural choice given its economic interpretation). Report an MCAP confidence interval.

**22.14.M2 — V_0 Non-Convergence in Heston Model**
Severity: Major

Figure 023 (Heston global search convergence) shows V_0 (bottom right panel) still spreading from near 0 to 0.01 after 200 MIF2 iterations. This initial condition is not identified from the data, which means all parameter estimates that co-vary with V_0 inherit additional uncertainty not reflected in the parameter point estimates.

Suggested author action: Either fix V_0 at a reasonable value (e.g., the unconditional mean theta) and run the search without estimating it, or explicitly discuss the identifiability limitation.

## Minor Points

- **22.14.1r — Cross-Model Likelihood Comparison:** The paper compares raw log-likelihoods from garchFit and pomp's pfilter. This comparison is defensible in principle (both evaluate the marginal log-likelihood of the observations), but the paper should explicitly state this and confirm that both use the same number of observations after any subsetting.

- **22.14.M3 — ARMA Model Selection:** The AIC table (Section 2.1) shows ARMA(4,4) with AIC -54737.98, noticeably lower than AR(4) at -54723.34 (a gap of ~14.6 AIC units), yet the paper selects AR(4) "for simplicity." This is a valid choice, but the paper should acknowledge that ARMA(4,4) fits better and that using AR(4) as the benchmark may slightly favor the POMP models.

- **22.14.13 — Reproducibility:** No sessionInfo() output or R package version information is provided. Final MLE parameter vectors for the Heston and Breto models are not archived separately from the Rmd output.

- **Typographical errors:** "Simple Sotchastic Volatility" (Section 4 heading), "Comparsion" (Section 5 heading), "time-seris" (Section 2 intro) should be corrected.

- **Missing figure captions:** None of the 23 figures have descriptive captions. At minimum, figures should be labeled with the model, run type (local/global), and what each panel shows.

- **Citation quality:** The Heston model is cited via Wikipedia (Reference 9). The original source (Heston, 1993, Review of Financial Studies) should be cited instead.
