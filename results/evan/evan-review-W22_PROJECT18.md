# Final AI Review — w22 Project 18

## Overall Assessment

This project applies GARCH(1,1), ARMA, and a stochastic volatility POMP model to annual crude oil log-returns (1980–2019, N ≈ 40 observations). The model selection and theoretical framework are appropriate for the domain. However, the analysis contains several critical technical failures that undermine the main conclusions: the profile likelihood over the key parameter phi is degenerate; the best parameter estimate from the global search (sigma_nu = 3.59) is inconsistent with all local search results and is not investigated; no confidence intervals are reported; and the paper's central claim — that POMP achieves the lowest AIC — is factually incorrect, as ARMA(0,0) has a substantially lower AIC (10.87 vs. 16.45). These failures appear to share a common root cause: the dataset of N ≈ 40 annual observations is too small for reliable estimation of a 6-parameter stochastic volatility model, a limitation that is mentioned briefly in the conclusion but not connected to the specific technical failures.

## Key Strengths

**S1. Both local and global IF2 optimization attempted.**
Sections 5.3 and 5.4 report both a local search (from reasonable starting values) and a global search (from a broad parameter box), with convergence traces for both. This is methodologically sound and reflects an awareness of local optima. Reporting timing and MC standard errors for the log-likelihood is also good practice.

**S2. Filter diagnostics provided.**
Figures 11 and 14 show effective sample size and conditional log-likelihoods from the final IF2 iteration for both searches. These panels are informative and are not always included in student projects.

**S3. Model equations clearly stated.**
The stochastic volatility model is written out in full with proper notation (Section 5.1), which aids review and reproducibility.

## Major Points

**22.18.3 | POMP does not have the lowest AIC — the stated conclusion is factually incorrect.**
The ARMA AIC table (Section 4) shows ARMA(0,0) with AIC = 10.87. The POMP best AIC is 16.45 (Section 5.4). The paper concludes that POMP yields "the lowest AIC among all models considered," which is incorrect. ARMA(0,0) is substantially better by AIC. This needs correction. Note also that ARMA(0,0) — a white noise model — having the best AIC is itself a substantive finding (it is consistent with annual oil log-returns being approximately unpredictable, i.e., weak-form market efficiency), and deserves discussion rather than dismissal.
Severity: Major. Suggested action: Correct the conclusion. Present a unified comparison table. Discuss the scientific meaning of white noise being the best model.

**22.18.2 | Profile likelihood over phi is degenerate and cannot support CI claims.**
Figure 17 shows the vast majority of profile points clustered at logLik ≈ 0.0 for phi < 0.5, while the established best logLik is -2.225. A value of logLik ≈ 0 from a particle filter is a sign of numerical failure (weight degeneracy, insufficient particles, or filter collapse), not a genuine likelihood evaluation. The CI threshold (red line at approximately -1.75) drawn across this plot has no statistical validity. The text's statement that "points lay above the threshold when phi < 0" is therefore uninterpretable.
Severity: Major. Suggested action: Rerun the profile with substantially more particles (Np) and verify that all profile evaluations return plausible logLik values in the range of the overall best (approximately -2 to -3). If computation is the bottleneck, use a coarser grid over phi but with reliable evaluations at each point.

**22.18.4 | Global search best estimate sigma_nu = 3.59 is implausible and uninvestigated.**
The local search pairs plot (Section 5.3) identifies sigma_nu ∈ (0.005, 0.020). The global search reports a best estimate of sigma_nu = 3.59 — approximately 180 times the upper bound of the local range. This discrepancy is not mentioned in the text, and the global search result is accepted as the reported MLE. This is almost certainly a numerical artifact (the optimizer may have found a degenerate solution that does not reflect the true likelihood surface) or evidence that sigma_nu and sigma_eta are not jointly identifiable at N = 40.
Severity: Major. Suggested action: Verify the global best logLik = -2.225 via replicated particle filter evaluations at sigma_nu = 3.59 with high Np. Compare to the value obtained at sigma_nu ≈ 0.011 from the local search. If the global best does not replicate, it should be discarded. Investigate identifiability of sigma_nu vs. sigma_eta.

**22.18.5 | No confidence intervals reported for any POMP parameter.**
The paper presents point estimates but no uncertainty quantification. The profile likelihood is malformed (see above), so it cannot currently yield valid CIs. This leaves all parameter estimates without credible uncertainty bounds.
Severity: Major. Suggested action: Once the profile is recomputed correctly, report MCAP or likelihood-ratio CIs for at least phi and sigma_nu. If the profile is flat, acknowledge that the parameters are weakly identified and discuss implications.

**22.18.N1 | N = 40 annual observations is too small for a 6-parameter SV model — this underlies most technical failures.**
The stochastic volatility model has 6 parameters (sigma_nu, mu_h, phi, sigma_eta, G_0, H_0). Fitting this model to 40 annual observations is extremely challenging. The non-convergence of IF2, the degenerate profile, and the implausible global MLE all have a common root: the data are too sparse to identify all parameters jointly. This limitation is mentioned briefly in the conclusion but is not connected to the specific failures documented above.
Severity: Major. Suggested action: Discuss this limitation explicitly in the analysis sections. Consider fixing some parameters (e.g., G_0 = 0) to reduce the parameter space, or use higher-frequency (monthly or weekly) data if available to increase N.

**22.18.6 | Log-likelihood scale convention for GARCH is unclear, making cross-model comparison unreliable.**
The GARCH(1,1) log-likelihood is reported as -3.33 (Section 3.2). For N = 40 observations, this is an unusually small absolute value for a total log-likelihood; a per-observation normalized value would be more typical at this magnitude. If GARCH reports a normalized logLik and POMP reports a total, they are not directly comparable. The paper does not clarify the convention.
Severity: Major. Suggested action: State explicitly whether log-likelihoods are summed or averaged across observations for each model. For GARCH, print the raw log-likelihood alongside the AIC to enable verification.

## Minor Points

**22.18.7 | Local IF2 search does not achieve convergence for all parameters.**
Figure 12 shows diverging log-likelihood traces and non-converged mu_h chains at iteration 200. The text acknowledges this but does not increase Nmif or Np. The reported local MLE may not be at the true maximum.
Severity: Minor. Suggested action: Increase Nmif (e.g., to 300–400) and/or Np for the local search, or add cooling schedule diagnostics.

**22.18.M1 | ARMA(0,0) finding is dismissed without scientific discussion.**
The best-AIC ARMA model being white noise is a substantive result — it suggests that annual crude oil log-returns are approximately unpredictable, consistent with weak-form market efficiency at annual frequency. Instead of dismissing this and selecting ARMA(0,1) "for analysis purposes," the paper should discuss this finding.
Severity: Minor. Suggested action: Include a brief discussion of the white noise finding and its economic interpretation.

**22.18.N2 | Section 5.1 header references SSE Composite Index rather than crude oil.**
The text in Section 5.1 states "We utilized the POMP model proposed in the lecture to analyze the volatility of SSE Composite Index." This appears to be a copy-paste artifact from the referenced 2021 project. The data being analyzed is crude oil, not SSE.
Severity: Minor. Suggested action: Correct to refer to crude oil prices.

**22.18.M2 | Gaussian measurement noise assumption is not acknowledged as a limitation for financial data.**
The SV model uses Gaussian epsilon_n. Financial log-returns are typically heavy-tailed; a Student-t measurement distribution would be more realistic. For a course project using the standard model, this is acceptable, but it should be noted.
Severity: Minor. Suggested action: Add one sentence in Section 5.1 acknowledging the Gaussian assumption and noting that Student-t extensions exist.

**22.18.9 | Np, Nmif, and number of IF2 replicates are not reported in the manuscript.**
The computational parameters that govern reliability of particle filter estimates are not stated. A reader cannot assess whether the results are computationally adequate.
Severity: Minor. Suggested action: State Np, Nmif, and the number of starting points used in both local and global searches.
