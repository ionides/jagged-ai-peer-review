# Final AI Review — w22 Project 04
## An Analysis on COVID-19 Omicron Variant in Washtenaw

---

## Overall Assessment

This project presents an interesting and scientifically motivated extension of the standard SEIR model to study the COVID-19 Omicron wave in Washtenaw County. The authors introduce a recurrent SEPIR structure (adding an asymptomatic "P" compartment and an R→S reinfection pathway), implement time-varying transmission through a covariate-driven Beta, and conduct both local and global iterated-filtering searches. The project demonstrates genuine engagement with the POMP framework and produces a model that visually captures the broad shape of the epidemic curve. However, several methodological gaps substantially limit the strength of the conclusions: a code error in the state-transition step, the absence of profile likelihoods and confidence intervals, a very sparse global search, and no quantitative comparison to the SARIMA baseline. The conclusion that POMP "explains the data better" cannot be assessed without a numerical comparison. Addressing the code bug is the highest priority.

---

## Key Strengths

**ID: 22.04.S1 — Scientifically motivated model structure**
The addition of an asymptomatic "P" compartment (for unreported infectious individuals) and the R→S reinfection loop is well-motivated by documented properties of Omicron. The model diagram is clear and the biological rationale is explained concisely.
Confidence: High

**ID: 22.04.S2 — Time-varying transmission via covariate table**
The use of a six-period intervention covariate to allow Beta to change across epidemic phases is a principled approach to handling a non-stationary epidemic. The covariate construction code is shown and interpretable.
Confidence: High

**ID: 22.04.S3 — Filter diagnostics shown**
Figure 17 shows effective sample size and conditional log-likelihood over the data window from the last filter pass. ESS remains near 5000 for most of the series, indicating the particle filter is operating well. This is a good diagnostic practice.
Confidence: High

**ID: 22.04.S4 — Both local and global search conducted**
The project presents IF2 trace plots for local search and scatter-plot matrices for both local and global searches, demonstrating a multi-stage optimization strategy consistent with course norms.
Confidence: High

---

## Major Points

**ID: 22.04.1 — Code bug: dN_RS drawn from I instead of R**
Concern: In the `sepir_step` Csnippet, the line `double dN_RS = rbinom(I, 1-exp(-mu_RS*dt))` draws individuals from the I (symptomatic infected) compartment rather than from R (recovered). The intended transition is R→S (reinfection). This means the R compartment never depletes into S via the reinfection pathway, the S update `S -= dN_SE - dN_RS` subtracts a draw based on I, and individuals may effectively be removed from I twice per time step.
Why it matters: This is a fundamental implementation error that can invalidate the model dynamics and all downstream parameter estimates. The reinfection pathway — a central motivation for the model — is not correctly implemented.
Severity: Major
Suggested action: Correct to `rbinom(R, 1-exp(-mu_RS*dt))`. Re-run local and global search after the fix and report updated parameter estimates and log-likelihood.

**ID: 22.04.2 — No quantitative SARIMA vs. POMP comparison**
Concern: The paper claims "POMP model can explain the data better" (Summary section) without providing a numerical comparison. The SARIMA AIC of ~1420 and the POMP log-likelihood of -768.17 are presented separately but never placed in a common framework.
Why it matters: The main claim of the analysis — that the mechanistic model provides better fit than the statistical baseline — requires evidence. A log-likelihood comparison or AIC for both models on the same data is needed. Note that ARIMA and POMP likelihoods are on comparable scales for the same data, so a direct comparison is valid.
Severity: Major
Suggested action: Compute the SARIMA log-likelihood (available from the fitted model object) and compare directly to the POMP log-likelihood. Report and discuss.

**ID: 22.04.3 — Profile likelihoods absent; no confidence intervals**
Concern: No profile likelihoods are computed for any parameter. Scatter-plot matrices from the global search show too few points (~5–10) to serve as profiles. No uncertainty is reported for Beta, rho, eta, mu_EPI, or the b_i multipliers.
Why it matters: The authors interpret rho ≈ 1 (near-complete reporting) and eta ≈ 0.9 (90% initially susceptible) as substantive findings. Without confidence intervals, these cannot be distinguished from artifacts of model misspecification or parameter non-identifiability.
Severity: Major
Suggested action: Compute profile likelihoods for at least rho, eta, and mu_EPI using a grid over plausible parameter ranges. Report MCAP confidence intervals.

**ID: 22.04.4 — mif2 log-likelihood not confirmed by replicated pfilter**
Concern: The global search best log-likelihood (-768.17 with SE "less than 1") is reported without explaining how it was computed. If this is the mif2 internal likelihood, it is a biased estimate. The standard approach is to run multiple independent pfilter evaluations at the MLE and report logmeanexp with Monte Carlo SE.
Why it matters: The absolute likelihood value is used to describe model fit, and any profile likelihoods would depend on reliable likelihood evaluation.
Severity: Major
Suggested action: At the reported MLE, run at least 10 independent pfilter evaluations, compute logmeanexp, and report the Monte Carlo SE.

**ID: 22.04.5 — Global search under-sampled (~5–10 points)**
Concern: The global search scatter-plot matrices (figures 15 and 16) contain approximately 5–10 points per panel. One panel (b1 in fig_015) shows one extreme outlier at b1 ≈ 4000 while all others are near 0, which is a sign of optimizer escape rather than exploration.
Why it matters: With so few evaluations, the global optimum may not have been found, and the likelihood surface cannot be characterised.
Severity: Major
Suggested action: Increase the number of random starting points to at least 20–30. Exclude or investigate degenerate solutions (b1 ≈ 4000) and report the distribution of converged log-likelihoods.

**ID: 22.04.6 — Initial conditions E, I, P hard-coded without justification**
Concern: `sepir_init` sets E=100, I=200, P=50 as constants regardless of the parameter vector. Only S and R are adjusted by eta. These values are not justified and are sensitive for an epidemic that begins within the observation window.
Why it matters: Misspecified initial conditions can shift the likelihood substantially and bias parameter estimates, particularly for Beta and b1 which govern early dynamics.
Severity: Major
Suggested action: Either estimate E_0, I_0, P_0 as parameters (with appropriate priors/bounds), fix them at literature-motivated values with justification, or show a sensitivity analysis demonstrating robustness.

---

## Minor Points

**ID: 22.04.M1 — Notation error: R_t mislabeled as I_t**
The model description uses $I_t$ for both the symptomatic infected compartment (fourth bullet) and the recovered compartment (fifth bullet). The fifth bullet should use $R_t$.
Suggested action: Correct notation throughout.

**ID: 22.04.M2 — mu_RS biological plausibility**
mu_RS is fixed at 1.529. If this is a per-day rate, it implies a mean recovery-to-reinfection time of ~0.65 days, which is biologically implausible. The authors note this parameter "explodes" if freely estimated, which signals a possible identifiability or misspecification problem for the reinfection pathway.
Suggested action: Clarify the time unit for all rates. Fix mu_RS at a literature-motivated value (e.g., reflecting observed reinfection rates at months-long intervals) and discuss the discrepancy.

**ID: 22.04.M3 — Gaussian measurement model allows negative counts**
The dmeas/rmeas snippets use a Gaussian approximation. The rmeas clips negatives to zero but the Gaussian support on negative values is conceptually mismatched with count data. A negative binomial or Poisson measurement model would be more appropriate.
Suggested action: Consider replacing with a negative binomial measurement model for a more principled treatment of count overdispersion.

**ID: 22.04.M4 — Simulation plots lack labeled observed data overlay**
Figures 9, 11, and 14 show multiple simulated trajectories but do not include a clearly labeled observed-data line. One faint line appears to represent data but is not identified in the legend or caption.
Suggested action: Add a clearly labeled, distinct-color observed-data line to all simulation comparison plots.

**ID: 22.04.M5 — SARIMA residuals show heteroscedasticity; log-transform not considered**
The residual plot (fig_006) shows much larger residuals during the outbreak peak than during the low-incidence period, consistent with variance heterogeneity in untransformed count data. A log or square-root transformation before SARIMA fitting would reduce this problem.
Suggested action: Consider fitting SARIMA to log-transformed (or square-root-transformed) case counts and compare AIC.

**ID: 22.04.M6 — Seasonal differencing order D not stated**
The SARIMA equation includes $(1-B^7)^D$ but D is never specified in the text. Clarify whether D=0 or D=1 and justify the choice.

**ID: 22.04.M7 — Forward simulation vs. filtering distribution**
Figures 11 and 14 appear to show forward simulations from the fitted parameter vector, not from the filtering distribution (i.e., not conditioned on observed data up to each time point). The difference between these two should be acknowledged, as filtering-distribution-conditioned simulations provide a stronger test of model fit.
