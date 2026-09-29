# Final AI Review — Rubella Transmission POMP Model [1966–1967]

## Overall Assessment

This paper applies a stochastic SEIR model with seasonal forcing to weekly rubella case reports from California, 1966–1967, using the POMP framework. The authors correctly implement iterated filtering (mif2), use logmeanexp to aggregate replicated particle filter likelihoods, adopt a negative binomial measurement model, and compute profile likelihoods for two parameters. These are genuine technical contributions at the level of a course project. However, the analysis has four important methodological gaps that prevent a confident evaluation of model adequacy: no non-mechanistic benchmark is provided, two key epidemiological parameters are fixed without justification, particle filter diagnostics are absent, and the profile likelihood for eta is unidentified yet a confidence interval is reported — a contradiction the paper itself acknowledges. Addressing these issues would substantially strengthen the analysis.

## Key Strengths

**Correct Monte Carlo likelihood aggregation.** The code correctly applies logmeanexp to replicated pfilter log-likelihoods throughout (local search, global search, and profiles), avoiding the common error of averaging on the log scale.

**Negative binomial measurement model.** The use of dnbinom/rnbinom is appropriate for overdispersed count data and is implemented consistently between the density and simulation functions.

**Profile likelihoods attempted.** Computing profile likelihoods for rho and eta, with MCAP confidence intervals, demonstrates appropriate engagement with uncertainty quantification even where the execution has issues.

**run_level framework.** The run_level switch for Np, Nmif, and replicates supports reproducible scaling of computation.

## Major Points

**22.06.1 — No benchmark comparison (benchmark)**
The best global log-likelihood is approximately -556.8. Without a non-mechanistic baseline (ARMA, SARIMA, or negative-binomial regression), it is impossible to determine whether the SEIR mechanistic structure adds explanatory value beyond what a flexible time-series model would provide. Severity: Major. Suggested action: Fit a seasonal ARIMA or SARIMA model to the same data and report its log-likelihood. Note that AIC is not directly comparable across ARIMA and POMP likelihood conventions, but log-likelihoods for the same data are comparable.

**22.06.3 — Unidentified eta profile; CI is statistically invalid (identifiability)**
Figure 12 shows a flat, noisy profile log-likelihood for eta over the entire search range (0.002–0.0026), with no visible peak. The confidence interval reported in Table 4 (lower=0.24%, upper=0.25%) is derived from scattered points that exceed the cutoff by Monte Carlo chance, not from a genuine likelihood ridge. Moreover, the text and Table 4 report different CI values (0.19%–0.24% vs. 0.24%–0.25%), indicating an internal inconsistency. The paper itself states that "our eta did not reach the confidence interval cutoff," which directly contradicts reporting a CI. Severity: Major. Suggested action: Remove the CI for eta. State explicitly that eta is not identified within the current model and data, and discuss what data or model changes would be required for identification.

**22.06.5 — Fixed parameters mu_EI and mu_IR without justification or sensitivity analysis (model-spec)**
The mean latent period (1/mu_EI = 12.5 days) and mean infectious period (1/mu_IR = 2.5 days) are fixed throughout all analyses. No epidemiological citation is provided for these specific values, and no sensitivity analysis is conducted. Conclusions about seasonal forcing and reporting rate depend on these choices. Severity: Major. Suggested action: Cite a source for each value or consider estimating them within the model. At minimum, run the analysis at two or three alternative values to assess sensitivity.

**22.06.6 — No particle filter diagnostics (diagnostics)**
Without effective sample size (ESS) plots or conditional log-likelihood traces from pfilter runs, it is impossible to determine whether the particle filter is functioning well or degenerating at specific time points. Particle filter degeneracy would make all likelihood estimates unreliable. Severity: Major. Suggested action: Plot ESS over time from at least one representative pfilter call. Plot conditional log-likelihoods per time step to identify where the model fits well or poorly.

## Minor Points

**22.06.2 — Incorrect signs in compartment equations (model-spec)**
The written equations show S(t) = S(0) + N_{SE}(t) and R(t) = R(0) - N_{IR}(t). These signs are reversed: S should decrease with infection and R should increase with recovery. The C code (seir_step) is correct. Suggested action: Correct the signs in the mathematical display.

**22.06.4 — rho profile optimization quality (identifiability)**
The profile's own maximum appears slightly below the global maximum used to set the CI cutoff. While the gap is within Monte Carlo variability, it is good practice to verify that the profile optimization achieves a maximum at least as high as the global search. Suggested action: Check whether increasing Nmif or Np in the profile step closes the gap.

**22.06.7 — rho parametrization in dnbinom not explained (measurement)**
In dnbinom(reports, H, rho, FALSE), rho functions as a success probability in a negative binomial, controlling both the mean and variance of reported cases. The interpretation of rho as a "reporting rate" is not straightforward under this parametrization. Suggested action: Clarify in the text how E[reports | H, rho] relates to the actual reporting fraction.

**22.06.8 — Vaccine timeline factual error (interpretation)**
The paper states the model provides a baseline "in the first 2 years of the MMR vaccine program," but the 1966–1967 data precedes the MMR program (which began in 1969) by two years. Suggested action: Correct this statement.

**22.06.9 — Inconsistency between text and Table 4 eta CI values (presentation)**
The text reports the eta CI as (0.19%, 0.24%) while Table 4 shows (0.24%, 0.25%). Suggested action: Reconcile these values and re-check the CI computation.

**M1 — rho double-duty as reporting rate and dispersion (measurement)**
The negative binomial parametrization with H as size and rho as success probability means rho simultaneously determines both the expected count and variance. Suggested action: Add a brief note on how rho enters the measurement model's mean and variance so that readers can assess the biological interpretation.

**M2 — Short data window limits seasonal parameter reliability (model-spec)**
With only two epidemic cycles (~104 weeks), the seasonal forcing parameters (b1, b2, Phi) are estimated from limited data. The paper does not discuss this limitation in the context of parameter reliability. Suggested action: Note this as a limitation alongside the existing computational and geographic scope limitations already in the Limitations section.
