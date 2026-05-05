# Peer Review: Final Project W21, Project 01
# "Investigating the effects of vaccinations and government policy on the spread of COVID-19 in the State of Pennsylvania"

---

## Summary

This project applies a SEIR-based POMP model to COVID-19 data from Pennsylvania (June 2020 - March 2021), incorporating government policy changes as fixed covariate multipliers on the transmission rate and vaccination counts as a direct S-to-R flow. The team uses iterated filtering (IF2) for parameter estimation. While the topic is well-motivated and the modeling effort is ambitious, there are substantial methodological, computational, and presentation problems that undermine the validity and interpretability of the results.

---

## Major Weaknesses

**1. Accumulator variable H is set to current I, not cumulative new infections — fundamental measurement model error**

The process model sets `H = I` (the total number currently infected) rather than accumulating new infections over the reporting interval. The intended meaning, as stated in the text, is that reports are a binomial sample from H. But drawing a binomial sample from the current prevalence (total I) conflates prevalence with incidence, making the measurement model structurally incorrect. A correct accumulator should track new entries to I during each day (`H += dN_EI; reset to 0 at observation times`) and draw reports from that count. As written, the model reports a fraction of all current infections at every time step, which is not how positive PCR tests work and will bias all estimated parameters.

**2. No profile likelihood or confidence intervals are reported for any parameter**

The project presents only pair plots of the likelihood surface from global search results. There are no profile likelihood traces, no confidence intervals, and no standard errors reported for any estimated parameter. For a POMP analysis, confidence intervals derived from profile likelihood or Monte Carlo methods are essential for assessing parameter uncertainty. Without them, the practical scientific conclusions (e.g., the inferred value of rho ~ 0.2) cannot be assessed for statistical significance.

**3. The global search filter results are post hoc filtered with ad hoc cutoffs that discard most runs**

After the global search, the authors filter with `filter(logLik > max(logLik) - 5e4)` — a window of 50,000 log-likelihood units — and additionally filter `mu_IR < 0.2` and `mu_EI > 0.2`. These cutoffs are not justified, and a 50,000-unit window for a time series of ~260 days is astronomically wide (good practice is a window of 10-20 log-likelihood units). This means that effectively no filtering of poor runs is occurring, and the pair plot includes highly sub-optimal parameter combinations. The filtering for `mu_IR` and `mu_EI` also imposes biological constraints after the fact without prior justification.

**4. The "smaller dataset" filtering analysis uses `datSEIR` (which includes the full covariate model) rather than a simplified pomp object**

The code for the smaller dataset analysis (Section "Iterative filtering on a smaller dataset") passes the same `datSEIR` object — which includes the policy covariate `C` and vaccination covariate `IM` — to mif2 without rebuilding the pomp object for the restricted time window or removing covariates. This means the "simple SEIR without covariates" claim in the text is false; the code still uses the covariate-enriched model on the full dataset. The intent and the code are inconsistent.

**5. No diagnostic particle filter traces (effective sample size, log-likelihood convergence) are shown**

Good practice in POMP analysis requires showing: (a) mif2 convergence plots of log-likelihood and parameters across iterations, and (b) particle filter effective sample size (ESS) traces to verify filter health. Neither is presented. Without these diagnostics, it is impossible to tell whether IF2 converged, whether the particle filter is degenerating, or whether the likelihood estimates are trustworthy.

**6. The covariate multipliers on Beta are chosen by hand without statistical justification**

The authors set Beta multipliers of 1.38 (from September 13, 2020) and 0.89 (from December 1, 2020) without any statistical derivation. These multipliers are stated as approximate values ("~1.4 times" and "~0.9 times") with no sensitivity analysis. These hard-coded values drive the shape of the simulated epidemic and dominate the inferences on Beta, but they are never estimated or validated. Treating them as fixed known quantities without uncertainty is a major modeling limitation that should at minimum be acknowledged, and ideally addressed by including them as estimated parameters or by running sensitivity analyses.

**7. Initial conditions are set with a mix of data-derived values and arbitrary choices, not estimated**

The initial compartment sizes use ad hoc formulas (e.g., `I = ini_positive_remained / rho`, `E = ini_positive_remained * mu_IR / mu_EI`) that depend on the true parameter values which are unknown. Setting initial conditions as explicit functions of estimated parameters introduces circular reasoning and will create identifiability problems. The correct approach is either to estimate initial conditions as free parameters (using `ivp()` in the rw.sd specification) or to use fixed biologically-motivated values with sensitivity analysis.

**8. Reporting rate rho = 0.9 in the simulation is unrealistically high and inconsistent with the IF2 results**

The simulation section uses `rho = 0.9`, implying 90% of all infections are reported. This is an extremely optimistic assumption given the well-documented under-reporting of COVID-19, especially in 2020. Furthermore, the IF2 results suggest `rho ~ 0.2` as a higher-likelihood region. The discrepancy between the simulation parameters and the fitted parameters is never reconciled or discussed.

---

## Minor Weaknesses

**9. The ARMA analysis is superficial and its role in the study is unclear**

The ARMA/AIC table is fitted to log-transformed and normalized case counts, but the conclusion ("no significant evidence that ARIMA performs better than white noise") is not supported by the table itself — the table is shown but not interpreted, and using ARMA as a benchmark is not meaningful without comparing log-likelihoods on a common scale to the POMP model.

**10. The log-ratio filtering for data quality uses ad hoc threshold (1.5) without justification**

The data quality check computes `log(totalTestResultsIncrease / positiveIncrease)` and draws a red line at 1.5 as a threshold, but the choice of 1.5 is not explained. No formal test or reference is provided. The decision to begin analysis at June 20 (rather than a date selected based on this criterion) is not connected to the plot.

**11. The CCF analysis is used to justify using positiveIncrease as the target variable, but the reasoning is flawed**

Finding that positive cases are highly correlated with death and recovery data is expected by construction (recoveries and deaths are a subset of confirmed cases). This correlation does not establish positive cases as "the most reliable source of information." A better justification would reference the consistency and completeness of the testing record relative to other variables.

**12. The smoothing of vaccination data using `smooth.spline` with default parameters is not validated**

Missing vaccination values are first forward-filled (carry-last-observation-forward), then smoothed with `smooth.spline` using default degrees of freedom. The combination of LOCF imputation followed by spline smoothing can introduce artifacts, and the result is not plotted against the raw data for validation. The daily increments derived from the smoothed totals are used directly as a fixed covariate in the POMP model without uncertainty.

**13. The simulation diagnostic comparing simulation to data is not quantified**

The project uses visual inspection of simulation envelopes against observed data as the main goodness-of-fit check. No quantitative simulation diagnostics (e.g., proportion of observed data within the simulation quantile range, or a formal simulation test) are provided.

**14. The pair plot filtering window for the small dataset analysis is also 1e4, which is very wide**

The smaller-dataset pair plot filters with `filter(logLik > max(logLik) - 1e4)` — a window of 10,000 log-likelihood units — which for a shorter time series is still unreasonably wide, allowing near-degenerate parameter combinations into the plot.

**15. The conclusion that the SEIR model is "sufficient overall" is not supported by the results**

The conclusion states "the SEIR compartment model seems sufficient overall to model Covid-19 data," yet the analysis itself demonstrates poor convergence, large likelihood variance, and clear model misspecification. The conclusion should instead acknowledge these failures as evidence of model inadequacy and suggest specific next steps (e.g., time-varying Beta, stochastic beta, additional compartments for asymptomatic transmission).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project01/Makefile`
