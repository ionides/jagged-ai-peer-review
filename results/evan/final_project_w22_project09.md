# Final AI Review
## Project: final_project_w22 / project09
## Title: Time Series Analysis of COVID-19 Cases in Washtenaw County

---

## Overall Assessment

This project applies a stochastic SEIR compartment model with a two-stage contact rate (separating Delta and Omicron periods) to COVID-19 daily case counts in Washtenaw County, MI. The scope is appropriate for a course project and the modeling motivation — using a biologically-motivated breakpoint at the Omicron emergence — is sensible. The authors include non-mechanistic benchmarks (negative binomial and SARIMA), use logmeanexp over replicated particle filters, and present convergence diagnostics. However, the work is undermined by several serious technical issues: the local search fails to converge and its output seeds the global search; the global search result table shows a single parameter vector repeated six times with a reported best log-likelihood that is inconsistent with the pair plot; b2 and mu_EI are effectively unidentified across the global search; and the reporting rate rho converges to ~0.97, a biologically implausible value that is not examined. These issues collectively prevent confident conclusions about either model fit or parameter interpretation. The manuscript acknowledges some limitations but does not diagnose the most consequential ones.

---

## Key Strengths

**ID 22.09.A — Benchmark Comparison Included**
The project computes log-likelihoods for both a negative binomial model (-1652.25) and a Jacobian-corrected SARIMA(-1308.98), and compares them to the SEIR log-likelihood. Including multiple non-mechanistic benchmarks is good practice and demonstrates the authors understand the purpose of benchmark comparison.
Confidence: High

**ID 22.09.B — Correct Likelihood Estimation Procedure**
Replicated particle filters (10 replicates at Np=5000) are aggregated via logmeanexp, which is the correct procedure for estimating the marginal log-likelihood from particle filter outputs. This shows appropriate understanding of Monte Carlo likelihood evaluation.
Confidence: High

**ID 22.09.C — Two-Stage Contact Rate**
Dividing the time series at the Omicron emergence (December 1, 2021) and estimating separate contact rates b1 and b2 is a well-motivated modeling choice given the known change in transmissibility between variants.
Confidence: High

---

## Major Points

**ID 22.09.1 — Duplicate Rows in Global Search Table and Loglik Discrepancy**
Concern: The global search result table shows the same parameter vector (b1=1.187, b2=1.586, rho=0.969, loglik=-1547.52) repeated six times. Independently, the pair plot (Figure 7) shows the global search cloud spanning loglik from approximately -1870 to -1845, which is nearly 300 log-likelihood units below the reported best of -1547.52. These two observations are mutually inconsistent and are not explained in the manuscript.
Why it matters: It is unclear whether the reported best log-likelihood is reliable, and whether the global search explored the parameter space meaningfully. If the pair plot reflects the actual global search quality, the SEIR model performance relative to benchmarks may be substantially worse than reported.
Severity: Major
Suggested action: Display a representative set of unique parameter vectors from the global search. Explain or resolve the discrepancy between the reported best loglik and the range shown in Figure 7. Check whether the pair plot was generated from the local search rather than the global search, and label accordingly.

**ID 22.09.2 — Local Search Non-Convergence Seeding Global Search**
Concern: The trace plot (Figure 6) shows log-likelihood ranging from approximately -3000 to -15000 across 100 mif2 iterations with no upward trend. The authors note this explicitly but do not diagnose or address it. The first element of this non-converged local search (mf1 <- mifs_local[[1]]) is then used to initialize the global search.
Why it matters: Using a poorly converged starting point as the template for global search can impose a narrow or misspecified parameter neighborhood, reducing the effectiveness of the global search. The non-convergence may also reflect model misspecification or insufficient particle count (Np=2000 for local search).
Severity: Major
Suggested action: Diagnose the non-convergence — test with higher Np, different starting values, or looser random walk SDs. Use purely random starts from the guesses design for global search rather than inheriting from an unconverged local result.

**ID 22.09.3 — Parameter Non-Identifiability: b2 and mu_EI**
Concern: The pair plot (Figure 7) shows b2 ranging from near 0 to approximately 80, and mu_EI ranging from 0 to approximately 40, across the top global search results. Additionally, b2 values extend far beyond the search box upper bound of 10, indicating the optimizer left the initial design space entirely. There is no visible concentration of the cloud near the reported best point estimates.
Why it matters: Without identifiability, the conclusion that "b2 > b1 proves that the Omicron variant is more easily spread" cannot be supported. The point estimate of b2 could be anywhere in a very wide range consistent with near-maximal likelihood.
Severity: Major
Suggested action: Compute profile likelihoods for b1, b2, mu_EI, and rho. Report MCAP confidence intervals. Qualify or remove the causal interpretation of b2 > b1 unless identifiability can be demonstrated. Constrain the parameter space more tightly if scientific knowledge supports it.

**ID 22.09.4 — Implausible Reporting Rate (rho ~ 0.97)**
Concern: The best estimate of rho is 0.9695, implying that approximately 97% of all COVID-19 infections in Washtenaw County were officially reported during this period. Published estimates of county-level COVID-19 reporting rates in the US during this period are generally in the range of 5–30%. An extreme value near the upper boundary of the parameter space typically signals model misspecification.
Why it matters: An implausible rho suggests the model is compensating for a structural problem — possibly in the H accumulator, initial condition specification, or measurement model variance. Conclusions drawn from a model with implausible parameter estimates are unreliable.
Severity: Major
Suggested action: Investigate the mechanism driving rho to ~1. Compare to external estimates of reporting rate for Washtenaw County. Inspect whether H is being reset correctly by the accumvars mechanism. Consider placing a biologically informed prior or bound on rho.

**ID 22.09.5 — H Accumulator Semantics Questionable**
Concern: In the process model, H is incremented by dN_IR (the number of individuals moving from I to R) rather than by dN_EI (new infections entering I) or dN_SE. If reported COVID-19 cases represent confirmed infections — which are typically counted when first detected (entering I, not exiting I) — then measuring H at recovery produces a time-shifted and potentially biased measurement of reported incidence.
Why it matters: A mis-timed accumulator will cause the fitted model to systematically lag or lead the data, affecting all parameter estimates including rho, b1, and b2. This may be a contributing cause of the implausible rho estimate.
Severity: Major
Suggested action: Clarify the intended epidemiological interpretation of H. If H is meant to represent newly detected infections, change the increment to dN_EI. Document the choice in the manuscript regardless of what is decided.

---

## Minor Points

**ID 22.09.6 — Large Initial pfilter Monte Carlo SE Not Discussed**
The initial log-likelihood evaluation reports an SE of 1510.358 — an extremely large value indicating that the particle filter likelihood estimate is nearly unreliable at the initial parameter values. This is not acknowledged or discussed.
Severity: Minor
Suggested action: Note that the initial SE reflects poor starting values rather than inadequate particle count, and confirm that the SE at the final parameter estimates is substantially smaller.

**ID 22.09.7 — Gaussian Measurement Model and Negative Count Clamping**
The rmeas function draws from a normal distribution and clamps negative values to 0. The dmeas function evaluates a Gaussian probability mass, which assigns nonzero density to negative counts. At low case counts (early time period), this introduces bias in both simulation and likelihood evaluation.
Severity: Minor
Suggested action: Consider replacing the Gaussian measurement model with a negative binomial model, which is the standard for overdispersed count data in POMP-based infectious disease modeling. At minimum, note this as a limitation.

**ID 22.09.8 — SARIMA Likelihood Scale Note**
The SARIMA log-likelihood is computed on log(Cases+1) and back-transformed using the Jacobian. The correction formula used is standard and technically correct. However, the resulting likelihood corresponds to a Gaussian model on transformed data, while the SEIR likelihood corresponds to a Gaussian model on the original count scale. This subtlety should be noted when presenting the comparison, since the two likelihoods are not on identical scales even after the Jacobian correction.
Severity: Minor
Suggested action: Add a sentence noting that the SARIMA benchmark is an approximation of the count-data likelihood; the comparison is informative but the two values are not strictly on the same scale.

**ID 22.09.9 — ESS Not Monitored**
Effective sample size from the particle filter is not reported or plotted. Low ESS would indicate filter degeneracy, which can cause numerical failures or unreliable likelihood estimates.
Severity: Minor
Suggested action: Plot ESS over time for representative runs. Flag any time periods where ESS is consistently low, as these often correspond to data features the model struggles to explain.

**ID 22.09.10 — mu_IR Fixed Without Citation**
mu_IR is fixed at 0.2 (corresponding to a 5-day infectious period) without citing any COVID-19 clinical literature. The infectious period for Omicron and Delta differ.
Severity: Minor
Suggested action: Cite the clinical literature supporting this choice. Discuss whether a single fixed value is appropriate across both the Delta and Omicron periods.

**ID 22.09.11 — Extreme Simulation Variance in Figure 8**
Figure 8 shows fitted simulations with very large spread — some trajectories near 1000 cases per day long after the Omicron peak — which is substantially wider than the observed data. This is not discussed.
Severity: Minor
Suggested action: Acknowledge the large simulation variance as a sign of model uncertainty or a potential identifiability issue. A well-fitted model should produce simulated trajectories that are broadly consistent with the observed data.
