# Final AI Review — w24 Project 13

## Overall Assessment

This paper makes a genuinely interesting scientific contribution by proposing a novel SIQRIQR compartmental model motivated by Taiwan's documented quarantine policies and the two-strain COVID-19 epidemic structure. The integration of SARIMA and POMP frameworks and the creative model design are commendable. However, the POMP implementation contains a fundamental error: new infections are driven by the quarantined compartments (Q_o, Q_b) rather than the infectious compartments (I_o, I_b). Since quarantined individuals are by definition removed from the transmission chain, this misspecification renders all estimated parameter values epidemiologically uninterpretable. Additional major issues — a hard-coded and undisclosed perturbation, absent benchmark comparison, missing profile likelihoods, and non-convergent mif2 traces — mean the results as presented cannot support the paper's conclusions. Substantial revision is required.

## Key Strengths

**ID 24.13.A — Correct likelihood aggregation.**
logmeanexp is applied correctly to replicated pfilter evaluations (5 replicates in local search, 10 in global search). This is a methodologically sound practice that the paper implements correctly.

**ID 24.13.D — Global search design.**
The global search draws 50 random starting points via runif_design and achieves a meaningfully higher best log-likelihood (-2697 vs -2865 from local search), demonstrating awareness of the multi-modal likelihood surface that complex POMP models produce.

**ID 24.13.E — Identification of weekly seasonality.**
ACF analysis of the differenced data (fig_006) clearly identifies a period-7 seasonal structure that is scientifically plausible (weekly testing cycles) and correctly motivates the SARIMA component of the analysis.

## Major Points

**ID 24.13.1 — Transmission force driven by quarantined, not infectious, individuals.**
Severity: Major.
In the Csnippet (and R prototype), both forces of infection are computed as `Beta_o*Q_o/N` and `Beta_b*Q_b/N`. Standard epidemiological models use the infectious (I) compartment because quarantined individuals cannot contact susceptibles. Using Q instead of I means the model transmits disease faster when more people are in quarantine — precisely the opposite of the intended quarantine effect. All estimated Beta values, R0 estimates, and policy conclusions rest on this misspecified mechanism.
Suggested author action: replace Q_o/N with I_o/N and Q_b/N with I_b/N in both forces of infection, then re-run all fitting.

**ID 24.13.2 — Undisclosed hard-coded perturbation at t=125.**
Severity: Major.
The Csnippet contains `if (t == 125) e = 100;` followed by `I_b += ... + e;`, injecting 100 individuals into the infectious beta compartment at day 125. This structural assumption is never mentioned in the model description, figures, or discussion. It is evidently driving the second rise in cases seen in the simulations, yet readers cannot evaluate or critique an assumption they are not told about.
Suggested author action: disclose this assumption explicitly, justify the timing (t=125) and magnitude (e=100) by reference to epidemiological events in Taiwan, and test sensitivity to this value.

**ID 24.13.3 — No benchmark comparison.**
Severity: Major.
The paper's central claim is that POMP improves upon SARIMA for the second wave, but this is never demonstrated quantitatively. The best POMP log-likelihood is approximately -2697 while the SARIMA log-likelihood for the same period (from auto.arima output) is -2552. A proper comparison requires noting that the ARIMA likelihood conditions on differenced data while the POMP likelihood conditions on raw counts; these are on different scales. The paper should explicitly compute both likelihoods on a common basis or clearly explain why direct comparison is not possible, rather than omitting any comparison.
Suggested author action: compare AIC values from both model classes while explicitly noting the scale difference, or compare simulated vs observed data visually with equal prominence for both models.

**ID 24.13.4 — No profile likelihoods or parameter uncertainty.**
Severity: Major.
The pairs plots (fig_016, fig_017) show that several parameters — notably Beta_b, Beta_r, Beta_or — range over one to two orders of magnitude across the top search results. This indicates poor identifiability, yet no profile likelihoods or confidence intervals are reported for any parameter. The conclusion that the SIQRIQR model captures "quarantine effectiveness" or "Omicron transmissibility" cannot be drawn when the associated parameters are unidentified.
Suggested author action: compute profile likelihood slices for at least Beta_o and rho, and report 95% MCAP confidence intervals.

**ID 24.13.5 — Non-convergent mif2 traces.**
Severity: Major.
Figure fig_015 shows that Beta_b and Beta_r continue to increase monotonically through all 50 mif2 iterations across all 20 runs without plateauing. The loglik traces remain highly variable. The text acknowledges this as "a bit ambiguous" for Beta_r but takes no corrective action. Non-convergence means the reported parameter estimates and log-likelihoods are not at or near the maximum likelihood, so any inference drawn from them is unreliable.
Suggested author action: increase Nmif to at least 200, and/or reduce the random walk standard deviation for Beta_r and Beta_b. Show updated traces demonstrating plateau.

## Minor Points

**ID 24.13.6 — Fixed parameters without justification.**
Several parameters (mu_QR_o=0.03, mu_QR_r=0.05, mu_QR_b=0.01, k=10) are fixed throughout all searches without epidemiological justification. Taiwan's quarantine policy during this period mandated specific isolation durations that could anchor these rates; this information should be cited.
Suggested author action: add a short table of fixed parameter values with epidemiological sources or explicitly acknowledge sensitivity to these choices.

**ID 24.13.7 — Code inconsistency between R prototype and Csnippet.**
The R prototype step function references undefined variables dN_SE_o and dN_SE_b (line 535) and uses undefined `dt`. This prototype was evidently not tested. While the Csnippet is the active implementation, presenting untested code undermines reproducibility.
Suggested author action: correct the R prototype to match the Csnippet or remove it from the manuscript.

**ID 24.13.8 — Severe Monte Carlo variability for some parameter sets.**
The local search results show loglik.se values as high as 89.3. This indicates that Np=2000 is insufficient at those parameter settings. Results with loglik.se > 10 should be treated as unreliable.
Suggested author action: flag such rows explicitly, or increase Np to 5000 for final likelihood evaluation.

**ID 24.13.M1 — No ESS diagnostics.**
ESS monitoring during pfilter runs is standard practice for diagnosing particle filter degeneracy. Its absence makes it impossible to assess filter reliability.
Suggested author action: extract and plot conditional log-likelihoods and ESS over time for the best parameter set.

**ID 24.13.M2 — rho search range constraint not justified.**
The global search constrains rho to [0.4, 0.6] without discussion. This narrow range may prevent finding the true MLE.
Suggested author action: justify this range with reference to surveillance estimates or expand to [0.1, 0.9].

**ID 24.13.M3 — Biologically inconsistent initial conditions.**
The model starts with I_o=0 and Q_o=100 — quarantined individuals without a corresponding infectious source. This is biologically inconsistent.
Suggested author action: initialize Q_o=0 and use I_o>0 to seed the epidemic.

**ID 24.13.9 — AIC table minimum vs auto.arima choice not reconciled.**
The manual AIC table minimum (ARIMA(3,1,5), AIC=3584.99) differs from the auto.arima recommendation (ARIMA(4,1,1), AIC=3602.26) and the discrepancy is not discussed.
Suggested author action: either select the AIC-optimal model or explain why auto.arima is preferred despite a higher AIC.
