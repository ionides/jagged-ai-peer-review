# Final AI Review
## Project: final_project_w24 / project15
## Topic: Analysis of MERS-CoV in Saudi Arabia (SEIRS POMP Model)

---

## Overall Assessment

This project makes a genuine scientific contribution by adapting a published camel-reservoir SEIRS model (Lin et al., 2018) to a POMP framework and fitting it to weekly MERS case data from Saudi Arabia. The scientific motivation is clear, the model structure is appropriate for a disease with an animal reservoir, and several important methodological elements are present: an ARMA benchmark with AIC-based selection, a negative-binomial measurement model with overdispersion, conditional log-likelihood and ESS diagnostics, and both local and global parameter searches with trace plots. The profile likelihood for the camel-to-human spillover rate is a welcome addition.

However, the work has several methodological problems that undermine the reliability of the main conclusions. The likelihood ratio test used to claim superiority over the ARMA benchmark is statistically invalid for non-nested models. The profile likelihood for ρ_CH is malformed — its maximum lies outside the evaluated range — rendering the reported confidence interval meaningless. IF2 traces show clear non-convergence for two key parameters, and the global search reveals extreme parameter dispersion suggesting a nearly flat likelihood surface. Replicated particle filter evaluations with Monte Carlo error estimates are absent. These issues together mean that the reported quantitative claims — the best log-likelihood of −378.33, R₀ ≈ 2.6, and the 95% CI for ρ_CH — cannot be taken at face value without additional computation.

---

## Key Strengths

**ID: 24.15.10 | Severity: Strength**
The inclusion of an ARMA(1,4) benchmark with a full AIC table and quantitative log-likelihood comparison is good practice and provides a meaningful non-mechanistic baseline against which the SEIRS model can be assessed.

**ID: 24.15.11 | Severity: Strength**
The negative-binomial measurement model with overdispersion parameter k is appropriate for count data with heavy-tailed outbreaks, and is better specified than a Poisson or Gaussian observation model would be.

**ID: 24.15.12 | Severity: Strength**
Conditional log-likelihood and ESS diagnostic plots are provided for the particle filter, demonstrating engagement with standard POMP diagnostics. The ESS remains above 500 at all time steps, and the low-likelihood periods correspond visibly to outbreak peaks — informative for model assessment.

**ID: 24.15.13 | Severity: Strength**
Both a local IF2 search (10 runs, 100 iterations) and a global random-start search are conducted with trace plots shown, reflecting good practice for avoiding local optima.

**ID: 24.15.14 | Severity: Strength**
The camel-reservoir SEIRS structure is scientifically well-motivated. Modeling the latent dynamics in camels rather than in humans resolves the puzzle of persistent low-level transmission punctuated by outbreaks, which the authors correctly note cannot be explained by a simple human-to-human SIR model.

---

## Major Points

**ID: 24.15.1 | Concern: Invalid likelihood ratio test comparing ARMA and SEIRS**
Why it matters: The paper applies the Wilks approximation to test H₀: ARMA(1,4) vs. H₁: SEIRS, reporting a p-value of 0 and concluding "we can reject H₀ at the 5% significance level." The Wilks theorem requires that the models be nested (H₀ is a special case of H₁) and that parameters lie in the interior of the parameter space — neither condition holds here. The p-value and conclusion are therefore invalid.
Severity: Major
Suggested author action: Remove the LRT framing entirely. The log-likelihoods from the two models are comparable in magnitude (both evaluated on the same observed data), so a direct comparison is meaningful: the SEIRS model achieves log-likelihood −378.33 vs. −422.77 for ARMA(1,4), a difference of 44.4 log-likelihood units, which is practically large and informative even without a formal test. State this comparison directly. Alternatively, compare AIC values if you account for degrees of freedom, but note that AIC penalization conventions differ between model classes.

**ID: 24.15.2 | Concern: Profile likelihood for ρ_CH has maximum outside the evaluated range**
Why it matters: The profile likelihood plot (fig_023) shows log-likelihood increasing monotonically as ρ_CH increases toward 10⁻³, with the maximum at the right boundary of the evaluated range. The reported 95% CI of [0.001, 0.001] is a degenerate point — not an interval — because the confidence threshold is crossed at or beyond the grid boundary. This means the MLE for ρ_CH was not found within the profiled interval.
Severity: Major
Suggested author action: Extend the profile to higher values of ρ_CH (e.g., up to 5×10⁻³) until the likelihood clearly turns down, identifying a proper maximum. Recompute the CI once a genuine interior maximum is found. The current profile provides no actionable information about parameter uncertainty.

**ID: 24.15.4 | Concern: IF2 non-convergence for mu_RS and rho_CH**
Why it matters: The trace plots (fig_017) show mu_RS still monotonically increasing across all 100 iterations with no plateau, and rho_CH still drifting upward. These are signs that the optimizer has not found a stable region of the likelihood surface. If these parameters have not converged, the reported maximum log-likelihood of approximately −400 may not be the true maximum, and the parameter estimates from the local search are unreliable.
Severity: Major
Suggested author action: Increase the number of IF2 iterations (e.g., to 200–300) until trace plots visually plateau. Also consider adjusting the cooling schedule or perturbation sizes. Report whether extending iterations changes the MLE and the associated parameter values.

**ID: 24.15.5 | Concern: Global search reveals extreme parameter dispersion**
Why it matters: The global search scatter matrix (fig_022) shows Beta ranging from near 0 to above 10,000 and mu_EI, mu_IR ranging from near 0 to 30, with high-likelihood points widely scattered throughout these ranges. This pattern is consistent with a very flat likelihood surface, meaning many structurally different parameter combinations yield comparable likelihoods. The paper does not discuss or acknowledge this dispersion.
Severity: Major
Suggested author action: Discuss the dispersion explicitly as evidence of parameter non-identifiability. Consider fixing more parameters to literature values (as Lin et al. do) and computing profiles for the remaining free parameters. At minimum, report the range of log-likelihoods across the global search to convey how much uncertainty exists about the MLE location.

**ID: 24.15.3 | Concern: No replicated pfilter evaluations; log-likelihoods presented as exact**
Why it matters: Particle filter log-likelihood estimates have Monte Carlo variance. The reported values (−378.33, −843.17) appear to be from single pfilter evaluations. Without replication (e.g., 10–20 independent pfilter runs using logmeanexp), the reported estimates could differ from the true log-likelihood by a substantial amount, making the comparison with the ARMA log-likelihood (which is exact) unreliable.
Severity: Major
Suggested author action: Evaluate the final parameter set using at least 10 replicated pfilter runs and report the logmeanexp ± standard error. This also quantifies whether the log-likelihood improvement over ARMA is robust to Monte Carlo noise.

**ID: 24.15.17 | Concern: Conclusion section overstates statistical evidence**
Why it matters: The Conclusion states the SEIRS model is "significantly better" than ARMA based on the LRT. As noted above, the LRT is invalid, so this conclusion cannot be supported in a frequentist sense.
Severity: Major
Suggested author action: Revise the conclusion to state that the SEIRS model achieves a substantially higher log-likelihood than the ARMA benchmark (difference of 44.4 units), consistent with meaningfully better fit, but that formal significance testing between non-nested models requires methods beyond Wilks (e.g., AIC comparison or simulation-based calibration).

---

## Minor Points

**ID: 24.15.6 | Concern: R₀ = 2.6 reported without confidence interval or identifiability check**
Why it matters: R₀ = β/μ_IR, but both β and μ_IR show wide dispersion in the global search and non-trivial spread in the local search traces. A point estimate of R₀ without a CI is difficult to interpret, especially given the poor identifiability of the constituent parameters.
Severity: Minor
Suggested author action: Compute a profile likelihood for R₀ or at minimum propagate the uncertainty in β and μ_IR into a range for R₀. Compare to Lin et al.'s reported R₀ range in more quantitative terms.

**ID: 24.15.7 | Concern: Gaussian ARMA applied to skewed count data without flagging as limitation**
Why it matters: The residual histogram and Q-Q plot both show heavy-tailed, non-Gaussian residuals. The ARMA model is used only as a benchmark, so this does not invalidate the main analysis, but it means the ARMA log-likelihood is computed under a misspecified model. The comparison with SEIRS should note this asymmetry.
Severity: Minor
Suggested author action: Add a brief note that the ARMA benchmark assumes Gaussian errors, which is violated, and that a negative-binomial ARMA would provide a fairer comparison. This does not need to be implemented but should be acknowledged.

**ID: 24.15.8 | Concern: Best-fit parameter vector from global search not shown**
Why it matters: The text introduces the global search best parameters but the actual values are absent from the manuscript. This prevents readers from assessing biological plausibility or reproducing the results.
Severity: Minor
Suggested author action: Add a table with the best-fit parameter vector from the global search, analogous to the starting-value table already provided.

**ID: 24.15.18 | Concern: The "4× multiplier" for total human cases is an external fixed assumption**
Why it matters: The model computes total human cases as 4 × primary camel-to-human infections, citing a single estimate that each cross-species primary infection results in four human infections (secondary transmission). This scaling factor is not estimated within the model and is not subjected to sensitivity analysis.
Severity: Minor
Suggested author action: Acknowledge this assumption explicitly and note that uncertainty in this multiplier propagates into all inferences about absolute case counts. A brief sensitivity check (e.g., what if the multiplier is 2 or 6?) would strengthen the paper.

**ID: 24.15.9 | Concern: Same parameter η₂ used for initial E and I without sensitivity**
Why it matters: Setting initial E₀ = I₀ = η₂ × N is an untested constraint. If the true initial state has substantially more exposed than infectious camels (or vice versa), this could bias the estimated dynamics during the first outbreak.
Severity: Minor
Suggested author action: Either cite stronger justification for equal initial E and I (e.g., steady-state endemic equilibrium calculation), or conduct a brief sensitivity analysis showing that results are robust to modest departures from this equality.
