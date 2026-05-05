# Final AI Review — w21 Project 13
# An Investigation into COVID-19 in California

---

## Overall Assessment

This project presents a serious attempt at mechanistic modeling of California COVID-19 dynamics using a SEAPIRD POMP model with time-varying intervention effects, alongside an ARIMA benchmark. The authors implement the full IF2 pipeline correctly — particle filter with replicated pfilter evaluation and logmeanexp aggregation — and include diagnostics (ESS, conditional log-likelihood traces, convergence plots). The epidemiological motivation for including asymptomatic and presymptomatic compartments is sound, and the intervention covariate structure reflects genuine policy variation over the study period.

However, the paper has several substantial methodological problems that limit the reliability of its conclusions. The most critical is a mismatch between the measurement model and the observed data: the accumulator variable H tallies recovered individuals, but the observation is new confirmed cases — these measure different quantities in the disease process. The parameter space is 15-dimensional but explored with only 8 global starting points, and trace plots reveal that many parameters have not converged; the paper nonetheless claims convergence without qualification. No profile likelihoods or confidence intervals are reported for any parameter. The ARIMA-POMP log-likelihood comparison is presented as a direct quantitative ranking, but the likelihoods are computed on different observation models and series, making this comparison not straightforward to interpret without additional justification. Together these issues undermine the credibility of the parameter estimates and the comparative conclusion.

---

## Key Strengths

**ID 21.13.S1 | Full IF2 pipeline with logmeanexp**
The authors use replicated pfilter calls (5 replicates in local, 10 in global) and aggregate with logmeanexp, which correctly accounts for Monte Carlo variability. This is the appropriate procedure and is applied consistently.

**ID 21.13.S2 | Epidemiologically motivated compartment extensions**
Adding asymptomatic (A) and presymptomatic (P) compartments, with A and P both contributing to the force of infection, reflects the known biology of SARS-CoV-2 transmission. The parameter values for latent and infectious periods are cross-referenced with recent literature.

**ID 21.13.S3 | Intervention covariate structure**
The use of a covariate table with six time-period-specific scaling factors for beta is a principled approach to incorporating non-stationarity in transmission due to California's documented policy changes. Both local and global searches are conducted, and the global search achieves a meaningfully better likelihood (-3792 vs. -3810).

**ID 21.13.S4 | Filter diagnostic plots provided**
ESS and conditional log-likelihood plots (fig_012) and MIF2 convergence traces (fig_013, fig_014) are included, which is appropriate practice.

---

## Major Points

**ID 21.13.1 | Measurement model accumulates recoveries, not cases**
Severity: Major

The accumulator H is updated in the state process as `H += dN_IR + dN_AR` — it tallies transitions from the Infectious and Asymptomatic compartments into Recovery. The measurement model then defines `mean_cases = rho * H`. However, the observed variable `cases` is new confirmed COVID-19 positive cases, not new recoveries. These are distinct quantities in the disease process: new cases correspond to transitions into I (from P) or detections in A, while recoveries occur weeks later. This misalignment means the model is fitting a lag-shifted proxy of incidence to actual incidence. The measurement model also adds the current value of D (cumulative deaths from the state process, not daily deaths) to the simulated cases (`cases = rnorm(...) + D`), which further conflates two distinct observables.

Why it matters: The likelihood is computed under a model whose mean is fundamentally tracking the wrong quantity. Parameter estimates — especially rho (reported ~0.09) and beta — will absorb this mismatch in unpredictable ways, and the numerical value of the reported log-likelihood does not measure fit to the stated quantity of interest.

Suggested author action: Redefine H to accumulate new symptomatic incidence (`H += dN_PI`), or new detectable infections. Separate the deaths observation from the cases observation. Verify that the rmeasure and dmeasure code is internally consistent with what H represents.

---

**ID 21.13.2 | Parameter non-identifiability with no profile likelihoods**
Severity: Major

The MIF2 convergence trace plots (fig_013, fig_014) show substantial spread across chains at 250 iterations for nearly every parameter: Beta, mu_IR, mu_EI, alpha, mu_AR, mu_PI, c_1, c_4, c_5, and c_6 all have chains that have not collapsed to a common value by the end of optimization. The pairs plots (fig_009, fig_011) show diffuse scatter for most parameter pairs with no clear ridge structure, consistent with a weakly identified likelihood surface. Despite this, the paper reports specific point estimates from the best search and interprets the model as having converged.

No profile likelihoods are provided for any parameter, and no confidence intervals are reported. The conclusion in Section 2.2.3 that "the POMP model has converged" is not supported by the trace plots.

Why it matters: Without identifiability checks, reported point estimates are unreliable and may reflect local optima rather than the MLE. Scientific claims about parameter values — such as the implied ~90% asymptomatic fraction (alpha ~0.9) or the best-fit mu_IR ~0.003 implying an infectious period of ~300 days, which is biologically implausible — cannot be trusted without uncertainty quantification.

Suggested author action: Compute profile likelihoods for at least the key parameters (Beta, rho, alpha). Report MCAP confidence intervals. Explicitly acknowledge that some parameters are not well-identified. Discuss the implausibility of the best-fit mu_IR value and consider whether it signals model misspecification.

---

**ID 21.13.3 | Insufficient global search for a 15-dimensional parameter space**
Severity: Major

The global IF2 search uses only 8 random starting points for a parameter space of 15 dimensions. The loglik trace (fig_013) shows wide spread at the end of 250 iterations, indicating many chains have not found the same optimum. The best local search loglik (-3810) is within 20 units of the best global (-3792), and only some global chains reached this level. It is not clear that the global optimum has been reliably identified.

Why it matters: If the global search has not found the true MLE, all downstream comparisons and parameter estimates are based on a suboptimal solution. The claim that the POMP model achieves a specific likelihood is uncertain.

Suggested author action: Run substantially more global starts (20-40 minimum for this dimensionality). Report the distribution of final log-likelihoods across all starts. Consider whether the convergence criterion is sufficient.

---

**ID 21.13.4 | ARIMA-POMP likelihood comparison requires qualification**
Severity: Major

Section 2.3 compares the ARIMA(4,1,3) log-likelihood (-4091) to the POMP log-likelihood (-3792) and concludes the POMP model "performed better." However, the ARIMA model was fit to first-differenced case counts under a Gaussian innovations model, while the POMP model was fit to raw (undifferenced) case counts under a different measurement model. These likelihoods are not directly comparable as written, because the observation models differ and because the ARIMA likelihood is for a transformed series.

Why it matters: The paper's central comparative claim rests on this number, but the numbers are not measuring the same thing. The directional conclusion (POMP fits better with richer structure) may well be correct, but it needs proper support.

Suggested author action: Acknowledge explicitly that the two log-likelihoods are not directly numerically comparable due to different observation models and data transformations. Alternatively, construct a Gaussian ARMA model on the raw (undifferenced) case counts and compare its likelihood to the POMP likelihood on the same series under the same observation model. Treat the current comparison as qualitative.

---

**ID 21.13.5 | Mathematical description inconsistent with code for I-compartment transitions**
Severity: Major

The mathematical description in Section 2.2 writes `dN_IR = Binomial(I, 1-exp(-mu_IR dt))` and `dN_ID = Binomial(I, 1-exp(-mu_ID dt))` as if both are drawn independently from the full I compartment, which would allow the sum to exceed I (violating conservation). The code correctly implements `dN_ID = rbinom(I - dN_IR, ...)`, drawing deaths only from the residual after recoveries. This inconsistency between the mathematical description and the implementation could confuse readers or indicate that the intended model is not the implemented one.

Why it matters: Reproducibility requires that the mathematical description and the code agree. If someone re-implements from the equations, they will produce a different (incorrect) model.

Suggested author action: Update the mathematical description to reflect the sequential draw: explicitly state that dN_ID is drawn from I minus dN_IR, or use a multinomial formulation.

---

## Minor Points

**ID 21.13.M1 | Notation inconsistency for E-to-A/P rate**
The parameter is called mu_EAP in the text's parameter table, mu_{EI} in a parenthetical remark, and mu_EI in the code. Use a single consistent name throughout.

**ID 21.13.M2 | Placeholder text in intervention assumptions**
Section 2.2.1 contains "We assume lockdown measures across California from x-x and x-x" with unfilled placeholder values. The code uses day-count thresholds (100, 200, 250, 300, 400) that are never mapped to calendar dates in the text. Readers cannot verify the correspondence between intervention periods and actual California policies.

**ID 21.13.M3 | ESS dips at times ~75 and ~330 not discussed**
The filter diagnostic plot (fig_012) shows substantial ESS drops at approximately day 75 and day 330. These correspond to early-epidemic onset and the December 2020 surge. These dips suggest the model has difficulty explaining rapid case rises and may indicate model-data tension at these times. Acknowledging this would strengthen the diagnostic discussion.

**ID 21.13.M4 | Measurement model produces potential negative case counts**
The Normal measurement model with the given parameterization can produce negative values for cases. The code partially addresses this by flooring to zero, but a count-appropriate model (Negative Binomial or Poisson with overdispersion) would be more appropriate and would not require ad hoc correction.

**ID 21.13.M5 | ARIMA residuals show non-normality and possible seasonality**
The QQ-plot (fig_004) shows heavy tails, and the ACF of residuals shows exceedance at lags 6 and 22. The paper notes these issues but takes no remedial action (e.g., log transformation, heavier-tailed innovations, or seasonal ARIMA). A brief discussion of why these were not pursued would improve the ARIMA section.

**ID 21.13.M6 | Missing session info and software versions**
No sessionInfo() output or pomp version is reported. For reproducibility, at minimum the R and pomp versions should be stated.

**ID 21.13.M7 | Typos and incomplete references**
"Comparision" (section heading 2.3), "paris plot" (text before fig_007). References [6]–[11] are missing author, journal, volume, and page information.
