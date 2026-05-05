# Final AI Review: Time Series Analysis of Apple Stock Price (w25, Project 11)

## Overall Assessment

This project applies both an ARMA-GARCH family and a discrete-time stochastic volatility POMP model to Apple Inc. daily log-return data (2020–2025) and compares their fit. The POMP workflow is competent: it includes local and global mif2 searches, replicated particle filter evaluations, ESS and conditional log-likelihood diagnostics, and a profile likelihood analysis. The honest discussion of identifiability problems and model weaknesses is commendable. However, three major methodological issues need to be addressed before the project's conclusions can be trusted: (1) the ARMA model selection contradicts the AIC evidence, (2) the profile likelihood over phi is too sparse to support the reported confidence interval, and (3) sigma_eta is near-non-identifiable but this is not diagnosed or reported.

## Key Strengths

**ID 25.11.7 — Multiple GARCH variants compared quantitatively**
The paper fits sGARCH, EGARCH, and GJR-GARCH with multiple error distributions and selects among them using both log-likelihood and AIC. This is rigorous within-family model selection.
*Why it matters:* Demonstrates that GJR-GARCH is not chosen arbitrarily but is supported by quantitative evidence within the GARCH family.

**ID 25.11.8 — Complete POMP workflow**
The paper implements local search, global search, replicated pfilter for MC variability assessment, and a profile likelihood — covering the core components of an IF2-based analysis.
*Why it matters:* Shows command of the computational framework and appropriate concern for optimization convergence.

**ID 25.11.9 — Filter diagnostics reported**
ESS and conditional log-likelihood are plotted for both local and global search (Figures 6.2 and 6.5), revealing periods of poor fit during high-volatility episodes.
*Why it matters:* These diagnostics are essential for assessing particle filter adequacy and are often omitted in weaker submissions.

**ID 25.11.10 — Honest acknowledgment of model limitations**
The paper explicitly identifies potential misspecification and weak identifiability in the POMP model rather than overstating results.
*Why it matters:* Appropriate epistemic calibration strengthens the credibility of positive claims.

## Major Points

**ID 25.11.2 — ARMA model selection contradicts AIC evidence**
Severity: Major

The AIC table (Table 4.1) shows ARMA(3,4) at AIC = -6324.15 and ARMA(1,1) at AIC = -6293.81 — a difference of approximately 30 AIC units. The paper selects ARMA(1,1) citing parsimony, but AIC already penalizes model complexity. An AIC difference of 30 units is far beyond the threshold typically required to override the AIC criterion. Additionally, the R output printed at the top of Section 4.1.1 shows coefficient estimates for ARMA(3,4), creating an internal inconsistency between what R selected and what the paper reports as its chosen model.

*Suggested author action:* Either select ARMA(3,4) as the mean model per AIC and re-run GARCH diagnostics on its residuals, or provide a principled domain-specific argument (e.g., that nearly-white-noise returns make high-order ARMA mean models economically implausible) for why ARMA(1,1) is preferred despite its much higher AIC. Note also that the AIC table contains a potential monotonicity violation: ARMA(4,4) at -6320.64 is worse than ARMA(4,3) at -6321.80, which may indicate a numerical optimization issue in the higher-order fits.

**ID 25.11.3 — Profile likelihood over phi too sparse to support reported CI**
Severity: Major

Figure 6.7 shows very few profile points, particularly in the region phi in [0.84, 0.94], making the shape of the profile likelihood uncertain. The stated 95% CI for phi of (0.959, 0.99) is based on a small number of points near the upper boundary and is not reliable. The cutoff criterion (MLE log-likelihood minus 1.92) is also not stated in the text. The authors themselves note "only a few points fall within this interval," which is an implicit acknowledgment that the result is unreliable, yet the CI is reported as a finding.

*Suggested author action:* Run additional profile evaluations to obtain at least 10–15 points spanning the full range of phi from approximately 0.80 to 0.999. If this is computationally prohibitive, explicitly state that the CI is approximate and should not be interpreted as a precise bound. State the cutoff criterion used.

**ID 25.11.4 — sigma_eta near-non-identifiability not diagnosed**
Severity: Major

Tables 6.1 and 6.2 show sigma_eta ranging from approximately 0.52 to 60+ across the top-10 parameter sets from both local and global search. This more than 100-fold range at similar log-likelihood values (3249–3289) is a clear sign that sigma_eta is nearly non-identifiable. The chosen MLE value of sigma_eta = 0.619 is one point in a near-flat likelihood surface. This is not discussed in the text; the identifiability concern is raised only for phi.

*Suggested author action:* Compute and plot a profile likelihood over sigma_eta. If the profile is flat, state that sigma_eta cannot be estimated from these data with the current model structure and discuss what this means for interpretation.

**ID M1 — mu_h also shows extreme variability across runs**
Severity: Major

In the global search top-10 table (Table 6.2), mu_h ranges from approximately -8.58 to +4.88 across runs achieving similar log-likelihoods. This indicates that mu_h is also poorly identified. The paper discusses only phi identifiability. Combined with sigma_eta non-identifiability, the model appears to have at most one or two well-identified parameters.

*Suggested author action:* Report profile likelihoods for mu_h and sigma_eta, or at minimum acknowledge in the text that mu_h is poorly identified and that the stochastic volatility model may be over-parameterized for this dataset.

## Minor Points

**ID 25.11.1 — Cross-family log-likelihood comparison should note initialization assumptions**
Severity: Minor

The comparison table in Section 6 presents GJR-GARCH (3328.37) and POMP (3288.55) log-likelihoods side by side. Likelihoods from different model classes are in principle comparable for the same observed data. However, the comparison is only valid if both models condition on the same set of observations (no presample burn-in differences in the GARCH implementation). The paper should verify this and add a brief note.

*Suggested author action:* State explicitly that both log-likelihoods are computed over the same N observations and that no presample initialization differences are present.

**ID 25.11.6 — Date anomaly in GARCH residual output**
Severity: Minor

The printed summary of GJR-GARCH standardized residuals shows dates ranging from 1970–1973 rather than 2020–2025. This is likely an R time-index formatting artifact but should be diagnosed and corrected to ensure that time-ordered diagnostics are applied correctly.

*Suggested author action:* Verify the time index in the GARCH fit and correct any date-origin issues in the R code.

**ID 25.11.11 — Profile CI cutoff not stated**
Severity: Minor

The profile likelihood section states the CI is (0.959, 0.99) without specifying the cutoff criterion. For reproducibility, state that the CI uses a cutoff of MLE log-likelihood minus 1.92.

**ID 25.11.13 — No forward simulation from fitted POMP model**
Severity: Minor

The paper does not show simulated trajectories from the fitted POMP model overlaid on the observed log-return series, which is a standard diagnostic for checking whether the model generates realistic volatility dynamics.

*Suggested author action:* Simulate 5–10 trajectories from the fitted POMP model and compare the simulated volatility envelope to the observed data.

**ID M2 — No RNG seeds set**
Severity: Minor

The analysis does not appear to set RNG seeds for mif2 runs or particle filter evaluations. Without seeds, exact reproducibility is not possible.

*Suggested author action:* Set and report RNG seeds for all stochastic computations.

**ID M3 — MC variability context for log-likelihood differences**
Severity: Minor

The logLik_se values across the top runs range from 0.22 to 3.76. When interpreting log-likelihood differences across parameter sets, these SE values should be explicitly discussed to confirm that differences are real and not Monte Carlo noise.

*Suggested author action:* Note in the text that the logLik_se values confirm log-likelihood differences exceed Monte Carlo variability.
