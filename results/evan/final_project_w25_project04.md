# Final AI Review — w25 Project 04
# SEIRS Model for COVID-19 Dynamics in Kerala

---

## Overall Assessment

This project presents a substantive mechanistic analysis of COVID-19 dynamics in Kerala using an iteratively refined SEIRS model fit via POMP/IF2. The work demonstrates genuine engagement with the POMP framework: model development is documented through multiple intermediate variants, profile likelihoods are computed for key parameters, and a second global search is creatively motivated by an anomaly in the mu_IR profile. These are genuine methodological contributions for a student project. However, several issues compromise the current draft's claims: the log-likelihood comparison between ARIMA and SEIRS is presented without noting that the two models operate on different data objects (differenced Gaussian vs. original count series), undermining the central quantitative claim of improvement; global search convergence diagnostics are absent for both SEIRS models; ESS is not checked at the fitted parameter estimates; and a biologically problematic near-zero b3 in Model 1 is acknowledged but its mechanistic implications for the third-wave attribution are not addressed. The paper is a solid foundation that would benefit from targeted additions rather than structural revision.

---

## Key Strengths

**S1 — Iterative model development with appendix documentation.**
The paper develops three SEIRS variants (constant parameters, time-varying k, time-varying k and rho) and documents all intermediate results in the appendix. This allows readers to understand why each modeling choice was made and provides a clear rationale for the final specification.

**S2 — Profile likelihoods computed for key parameters.**
Profile likelihoods for rho_1, rho_2, rho_3, eta, and mu_IR are presented with confidence intervals. The discovery of a second likelihood mode in the mu_IR profile and the subsequent second global search is a particularly strong aspect of the analysis.

**S3 — Biological parameter corroboration.**
Estimated values for mu_EI, mu_IR, rho, and eta are compared against independent clinical literature. This corroboration step is often skipped in student projects and adds credibility to the reported estimates.

**S4 — Appropriate measurement model.**
The negative binomial measurement model with phase-specific dispersion k(t) and reporting rate rho(t) is a well-motivated choice for overdispersed COVID count data with known changes in testing intensity.

---

## Major Points

**ID: C1 — AIC comparison between ARIMA and SEIRS requires qualification.**
The conclusion table compares log-likelihoods and AIC values directly between ARIMA(5,1,5) and the two SEIRS candidates. ARIMA log-likelihoods are computed on the once-differenced series using a Gaussian likelihood; SEIRS log-likelihoods are computed on the original weekly counts using a negative-binomial particle filter. These are different data transformations and different probability models, so the numerical log-likelihood values are not on a common scale. The paper correctly acknowledges that VAR log-likelihoods are not comparable to ARIMA/SEIRS, but applies no analogous caveat to the ARIMA vs. SEIRS comparison. Severity: Major.
Suggested action: Either restrict quantitative comparison to SEIRS model variants only (Model 1 vs. Model 2), or add an explicit statement that the ARIMA–SEIRS log-likelihood comparison is approximate and explain why the direction of the comparison (SEIRS improves on ARIMA) is still meaningful despite the scale difference.

**ID: C2 — Phase boundary overlap makes the model specification ill-defined as written.**
The piecewise definitions show Phase 2 as t ∈ [62, 96] and Phase 3 as t ∈ [63, 119], so weeks 63–96 are simultaneously assigned to both phases. This is a mathematical inconsistency in the written model specification. Even if the code correctly implements non-overlapping boundaries, readers cannot reproduce or verify the model from the manuscript. Severity: Major.
Suggested action: Correct the text to define non-overlapping intervals (e.g., Phase 3: t ∈ [97, 119]) that match the actual boundaries used in the code.

**ID: C3 — Global search convergence diagnostics absent.**
For both SEIRS Model 1 (800 starting points) and Model 2, convergence of the global search is characterized only verbally ("top 10 log-likelihood stay relatively consistent"). No scatter plots of log-likelihood vs. parameter values, no distribution of final log-likelihoods across runs, and no convergence trace figures are provided. Severity: Major.
Suggested action: Add a pairs plot or at minimum a histogram of final log-likelihood values across all global search runs to demonstrate that the global optimum has been adequately explored.

**ID: C4 — ESS not shown for final fitted parameter estimates.**
ESS is appropriately checked for the initial guess (Figures 12–13) and noted to improve after optimization, but no ESS plot is shown for the locally or globally optimized parameter estimates. ESS collapse at the fitted parameters indicates that the particle filter is struggling and the reported log-likelihood values may be unreliable. Severity: Major.
Suggested action: Include ESS-over-time plots for the best global search parameter vectors from both SEIRS models.

**ID: C5 — Final log-likelihood values should be explicitly confirmed as replicated pfilter estimates.**
The final log-likelihoods for the global search candidates (-1239.449 and -1233.212) are described as having "small Monte Carlo standard error" but it is not stated explicitly whether these come from replicated pfilter evaluations or from the mif2 internal log-likelihood (which is systematically biased). Severity: Major.
Suggested action: State explicitly that final log-likelihood estimates are obtained by running pfilter with Np = 5000 over N replicates (specify N) and averaging via logmeanexp. Report the Monte Carlo standard error on these estimates.

**ID: C6 — mu_RS fixed without sensitivity analysis.**
mu_RS = 0.005 (corresponding to ~200-week immunity duration) is acknowledged as biologically implausible but is fixed for numerical stability. Since mu_RS controls susceptible replenishment and governs the model's ability to generate multiple epidemic waves, this parameter is central to the SEIRS dynamics. Its value is not explored via profile likelihood or sensitivity analysis. Severity: Major.
Suggested action: Compute a one-dimensional profile of log-likelihood as a function of mu_RS, or explicitly characterize it as an unidentifiable parameter with a flat profile.

**ID: C7 — Near-zero b3 in Model 1 contradicts mechanistic attribution of the third wave.**
The best global search parameter for Model 1 yields b3 ≈ 0.0024, which is effectively zero transmission in Phase 3. If b3 ≈ 0, the third wave in Model 1 cannot be attributed to increased Omicron transmissibility — the primary scientific explanation for the Omicron surge. The model can visually reproduce three waves, but the mechanism is inconsistent with known biology. This is partially resolved by Model 2 (b3 ≈ 9.14). Severity: Major.
Suggested action: Make explicit that Model 1's b3 estimate is mechanistically implausible and that Model 2 is preferred not just for log-likelihood but because it recovers a biologically interpretable b3. Consider computing a profile likelihood for b3 in Model 1 to confirm it is poorly constrained.

---

## Minor Points

**ID: C8 — Profile likelihoods missing for b3, rho_3 (Model 2), and mu_EI.**
The paper identifies convergence problems and possible identifiability issues for these parameters in the text but does not present profile likelihoods for them. For a paper that otherwise invests significantly in profile computation, these gaps are notable. Severity: Minor.
Suggested action: Add profile plots for at least b3 (to confirm or refute its identifiability) and rho_3 in Model 2 (to explain why rho_3 ≈ 0.09 rather than the expected ~0.85).

**ID: C9 — NegBinom parameterization should be clarified.**
The measurement model Y(t) ~ NegBinom(rho*H, rho*H + (rho*H)^2/k(t)) uses a mean/variance parameterization. Clarifying which R package convention is used would aid reproducibility. Severity: Minor.
Suggested action: State the NegBinom parameterization convention used (mean = rho*H, variance = rho*H + (rho*H)^2/k) and cite the relevant pomp measurement model code.

**ID: C10 — Initial compartment allocations E0, I0, R0 not stated.**
The text specifies S0 = eta*N but does not describe how E0, I0, and R0 are initialized. Since N = S + E + I + R is conserved, the remaining compartments must sum to (1-eta)*N; the specific allocation affects the early epidemic trajectory. Severity: Minor.
Suggested action: State the initial conditions for all compartments explicitly.

**ID: MS3 — Global search range for b3 in Model 1 appears inconsistent with the best result.**
The global search range for b3 is stated as [10, 50], but the best result yields b3 ≈ 0.0024, far below the stated floor of 10. This suggests the range may apply to a transformed parameter scale or the local search generated this value. Severity: Minor.
Suggested action: Verify and correct the reported global search ranges to match the ranges actually used in the code.
