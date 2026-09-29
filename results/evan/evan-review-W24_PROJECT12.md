# Final AI Review: w24 Project 12
# Time Series Analysis of COVID-19 Cases in Kent County

---

## Overall Assessment

This paper presents a SEIRS compartment model for 212 weeks of COVID-19 case data from Kent County, Michigan, using the pomp framework with iterated filtering. The work demonstrates genuine methodological ambition: time-varying transmission and reporting rates across three epidemiological periods, gamma-white-noise overdispersion on the force of infection, an importation parameter, and a truncated-normal measurement model with combined Poisson-scale and overdispersion variance. The benchmark comparison (ARMA(2,1)) is included and reported honestly despite an unfavorable outcome (SEIRS log-likelihood -1404 vs. ARMA -1372). The computational budget is substantial, and MC standard errors are appropriately reported. The main weaknesses are that the profile likelihood is too sparse to support credible confidence intervals, parameter non-convergence is pervasive but insufficiently acknowledged, and the measurement model introduces an undefined variable H. Addressing these issues would substantially strengthen the paper.

## Key Strengths

- **S1 (24.12.8)** Benchmark comparison is included and results are reported honestly, even when unfavorable. The 32.5 log unit gap is acknowledged rather than minimized.
- **S2 (24.12.9, 24.12.10)** Both local and global searches are conducted with a reasonable budget (Np=5000, Nmif=200, 200 global starts), MC standard errors are reported, and filter diagnostics (ESS and conditional log-likelihood, Figure 4.12) are shown.
- **S3 (24.12.M2)** The truncated-normal measurement model with combined Poisson-variance and overdispersion terms (tau parameter) is more sophisticated than the standard negative binomial approach used in many similar analyses.
- **S4 (24.12.14)** Time-varying transmission and reporting rates are motivated by specific epidemiological events (variant emergence, mandate changes), providing scientific grounding for the piecewise structure.

## Major Points

**Major 1 (24.12.1) — Profile likelihood is too sparse to support the reported confidence interval**

The profile likelihood over rho3 (Figure 5.1) shows a scatter cloud with no discernible quadratic shape. Only 4 points lie above the 95% threshold, and the upper bound of the reported CI (0.37–1.0) is the hard boundary of the parameter space, indicating the profile failed to find a maximum. The authors themselves acknowledge "only 4 points above the threshold in red which may result in a dubious interval." A profile with so few points above the threshold cannot support a meaningful CI.

Severity: Major.
Suggested action: Rerun the profile with more points (20+) in the region [0.25, 1.0], use a narrower starting box from the global search results, and ensure each profile evaluation uses replicated pfilter. If the profile remains flat, report this as evidence that rho3 is non-identifiable and remove the CI claim entirely.

**Major 2 (24.12.3) — Non-convergence is pervasive but described as "not a problematic result"**

Figure 4.3 shows that in the local search, b1, b2, b3, rho1, rho2, mu_EI, mu_RS, rho3, tau, and sigma_SE all fail to converge. The global search pairs plots (Figures 4.9–4.11) show extreme dispersion for essentially all parameters. The paper describes this as "not a problematic result" (Section 4.3) and proceeds to interpret specific parameter values (e.g., b3 is largest, rho3 is highest, mu_RS is near zero) without acknowledging that these interpretations are unreliable when convergence has not been established.

Severity: Major.
Suggested action: Acknowledge pervasive non-convergence as a significant limitation. Avoid interpreting individual parameter values at face value. Consider fixing mu_EI and mu_IR to literature values for COVID-19 (incubation approximately 1 week, infectious period approximately 1 week) to reduce dimensionality and improve convergence. If convergence cannot be achieved, frame all parameter estimates as illustrative rather than definitive.

## Minor Points

- **Minor 1 (24.12.4)** The measurement model in Section 4.1 uses variable H in the equation for Y_n without defining H at that point. Readers must infer that H represents new infections in the observation interval. Explicitly define H when it is introduced, and verify that the code implements H consistently with that definition.

- **Minor 2 (24.12.2)** The procedure for obtaining final log-likelihood estimates is not stated explicitly. Whether replicated pfilter runs were used at the mif2 endpoint (the correct approach) is left to inference from the reported MC SEs. A sentence stating the procedure (e.g., "log-likelihoods were evaluated using Nreps=10 replicated pfilter runs at the best parameter vector") would improve reproducibility and transparency.

- **Minor 3 (24.12.5)** Figure 4.12 shows ESS collapse and extreme conditional log-likelihood spikes at the two major peak periods (approximately weeks 40–55 and 95–110). The paper attributes these generically to holiday reporting issues. A more specific attribution — e.g., whether the piecewise transmission or reporting structure fails to capture the rapid rise and fall of those peaks — would strengthen the discussion and motivate the suggested improvements in Section 7.

- **Minor 4 (24.12.16)** The estimated mu_RS near zero (implying approximately 20-year waning immunity) is correctly questioned, but the paper attributes this to a possible model inadequacy rather than non-identifiability. A 4-year dataset cannot estimate a 20-year rate, so mu_RS will be pushed toward zero regardless of its true value. This is an identifiability constraint, not evidence that the SEIRS extension is wrong, and should be framed accordingly.

- **Minor 5 (24.12.M1)** The initial compartment allocations for E(1), I(1), and R(1) are not stated. If eta=0.89 sets S(1) = 0.89 * N, the remaining 11% of the population must be allocated among E, I, and R. If E(0) and R(0) are set to zero, early filtering behavior may be sensitive to this choice. State the initial compartment values explicitly.

- **Minor 6 (24.12.6)** In Section 3.2, the statement "adding a parameter cannot decrease the maximized log-likelihood, so we should not see the AIC increase by more than 2 units" slightly misframes the relationship. AIC can legitimately increase by any amount when adding a parameter if the log-likelihood gain is less than 1. The AIC anomalies in the table are real numerical optimization failures, but the stated reasoning should be corrected.

- **Minor 7 (24.12.7)** The importation parameter iota is described as representing "individuals moving from susceptible to infectious" when it actually acts as a constant additional infectious pressure term inside the force-of-infection expression — as (I + iota) — rather than a literal population flow. Revise the prose description to reflect this distinction.
