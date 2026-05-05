# Final AI Review
## Project: final_project_w24 / project04
## Reviewer: Evan (Treatment E, claude-sonnet-4-6)

---

## Overall Assessment

This paper addresses a clearly motivated question — whether a mechanistic SEIR model can better capture COVID-19 transmission dynamics than an ARIMA benchmark — and demonstrates familiarity with both ARIMA model selection and the POMP compartmental modeling framework. The ARIMA analysis is conducted with standard rigor (AIC table, residual diagnostics). However, the SEIR model is not fitted by likelihood-based methods: it uses a least-squares cost function (sum of squared differences) rather than particle-filter likelihood evaluation, which means no valid quantitative comparison between the two models is possible. Several optimization runs appear to fail silently (producing near-zero parameter estimates or flat predictions), and the paper's conclusion that "the SEIR model more naturally captures epidemic characteristics" cannot be verified without quantitative fit metrics. The EDA section presents forward simulations from placeholder parameters rather than exploratory analysis of the observed data. Taken together, these gaps make the central research question effectively unanswerable from the results as presented.

---

## Key Strengths

- **ID: 24.04.S1.** The SEIR compartmental structure is formally specified with binomial transition distributions and exponential holding times (Euler method), consistent with standard POMP practice for stochastic epidemic models.
- **ID: 24.04.S2.** The ARIMA analysis includes a well-organized AIC table across a 4x4 grid of (p, q) values, residual plot, ACF, and QQ plot — the appropriate set of diagnostics for model selection.
- **ID: 24.04.S3.** The paper explicitly frames the research question as a comparison between mechanistic and non-mechanistic approaches, which is the right scientific question to ask for epidemic data.

---

## Major Points

**ID: 24.04.1 — SEIR model fitted without likelihood-based inference**
- **Concern:** The global optimization uses "the sum of the squared differences between observed and simulated cases" (manuscript, GenSA section) as the objective function. No particle-filter likelihood (`pfilter`) is computed at any stage. The local optimization trace plots (fig_008) resemble mif2 convergence traces, but no log-likelihood values are reported, and the procedure cannot be identified as proper IF2 inference.
- **Why it matters:** Least-squares fitting of a stochastic POMP model is not equivalent to maximum likelihood. Without a properly defined measurement model and particle-filter likelihood, the SEIR parameter estimates have no statistical interpretation and cannot be compared to the ARIMA log-likelihood.
- **Severity:** Major
- **Suggested action:** Specify a measurement distribution (e.g., negative-binomial with reporting rate rho). Use `pfilter` from the pomp package to evaluate the particle-filter log-likelihood at the estimated parameter vector. Report this log-likelihood and compare it to the ARIMA log-likelihood on a common footing, noting that the two likelihoods use different measurement distributions and are not directly AIC-comparable without discussion.

**ID: 24.04.2 — No quantitative goodness-of-fit metric for the SEIR model**
- **Concern:** The conclusion that "the SEIR model still fell short of the ARIMA model in terms of fitting precision" is based solely on visual overlay plots. No log-likelihood, AIC, RMSE, or predictive score is reported for the SEIR model.
- **Why it matters:** The paper's primary research question requires a quantitative comparison. Without it, neither the inferiority nor superiority of the SEIR model can be established. The conclusion is scientifically unverifiable.
- **Severity:** Major
- **Suggested action:** Compute at minimum the particle-filter log-likelihood for the SEIR model and compare to the log-likelihood implied by the ARIMA model (noting scale differences). If full pfilter is not feasible, report the least-squares residual sum of squares and a corresponding R-squared for both models as a provisional comparison, explicitly acknowledging its limitations.

**ID: 24.04.3 — Optimization appears to fail; reported results are internally inconsistent**
- **Concern:** In the local search (fig_008), all parameters except N collapse to near-zero values, which the text describes as "converging to a positive number close to 0" — but near-zero beta, sigma, gamma, and rho are epidemiologically impossible for a disease that infected hundreds of thousands. In the global search, the parameters reported (beta = 0.834, rho = 0.660) should produce a visible epidemic curve, yet fig_010 shows the model prediction as essentially flat. This internal inconsistency is unresolved.
- **Why it matters:** If the optimization is numerically failing, all downstream model fits and conclusions are unreliable. The reader cannot assess whether the "Final SEIR Model" (fig_011) is based on valid parameter estimates.
- **Severity:** Major
- **Suggested action:** Verify the forward-simulation code by running it directly with the reported GenSA parameters and checking that the output matches the expected epidemic curve. Check for unit mismatches (e.g., beta scaling, time-step size relative to the data frequency). Report whether the discrepancy between fig_010 and the stated parameters was identified and corrected before producing fig_011. Show the parameter values used for fig_011 explicitly.

**ID: 24.04.4 — EDA section presents forward simulations, not data exploration**
- **Concern:** Figures 001–003 are labeled "Simulation of POMP Model with Hospitalization in California" (and analogous for other states). The text analyzes the properties of these simulations (cyclical fluctuations, rapid depletion of susceptibles) and proposes parameter adjustments. No plot of the actual observed COVID-19 case counts for any state is presented in the EDA section. There is no time-series decomposition, no log-scale plot, no discussion of weekly seasonality or outliers.
- **Why it matters:** EDA should reveal data features (non-stationarity, seasonality, heavy tails, reporting artifacts) that motivate model choices. Replacing EDA with untethered forward simulations leaves the reader unable to assess whether model assumptions are appropriate.
- **Severity:** Major
- **Suggested action:** Add plots of the raw observed case counts for Washington State (and optionally California and New York). Include a log-scale plot and note the weekly periodicity visible in the data (fig_007 blue line shows clear weekly oscillation). Discuss how the chosen SEIR structure addresses or ignores these features.

**ID: 24.04.5 — Measurement model undefined; reporting rate rho has no formal meaning**
- **Concern:** The parameter rho is introduced as "the probability of a case being reported," but no measurement distribution (Poisson, negative binomial, normal) is specified. Without a likelihood, rho cannot be estimated in any statistically principled sense; it is effectively just a scaling factor in the forward simulation.
- **Why it matters:** The measurement model is the link between the latent epidemic process and the observed data. Without it, the model is not a proper POMP model — it is a deterministic compartmental model overlaid on data. This also explains why the paper cannot compute a particle-filter likelihood.
- **Severity:** Major
- **Suggested action:** Specify the observation equation: e.g., Cases_t ~ NegBin(mean = rho * I_t, overdispersion = psi). This makes rho estimable from data and enables proper likelihood evaluation.

**ID: 24.04.6 — ARIMA fitted to raw (non-transformed) highly skewed counts**
- **Concern:** The observed Washington State case counts span from near zero to ~900,000 (fig_007), with an extreme right skew. No variance-stabilizing transformation (log or square root) is applied before fitting the ARIMA model. The heavy-tailed QQ plot (fig_004) and the 2022 residual spike are direct consequences of this. Differencing alone does not address variance non-stationarity in count data.
- **Why it matters:** ARIMA assumes approximately Gaussian, constant-variance innovations. Applying it to raw count data with a 1000:1 range violates this assumption and makes AIC-based model selection unreliable.
- **Severity:** Major
- **Suggested action:** Apply a log(x+1) or square-root transformation to the case counts before ARIMA modeling. Rerun AIC selection on the transformed series. Report whether the residual spike and QQ tail behavior are resolved.

---

## Minor Points

- **ID: 24.04.m1 — b1/b2 time-varying beta inconsistency.** The model description introduces a time-varying contact rate with parameters b1 (first half of time period) and b2 (second half), but the optimization reports a single beta, and all equations use a single beta. If b1/b2 was not implemented, remove the description. If it was implemented but collapsed to a single value, report both estimates. (Severity: Minor)

- **ID: 24.04.m2 — Initial conditions not reported.** The initial values of S(0), E(0), I(0), R(0) are never stated in the manuscript. For a 1500-day COVID-19 time series with multiple waves, the initial conditions affect model behavior substantially. (Severity: Minor)

- **ID: 24.04.m3 — Reference [6] cites ChatGPT.** "Code optimization and error correction, https://chat.openai.com/" is listed as a formal reference. AI assistance should be disclosed in a methods acknowledgment rather than treated as a citable source. (Severity: Minor)

- **ID: 24.04.m4 — fig_009 vs fig_011 unexplained difference.** Both figures show the SEIR model after local optimization, but the curves are visibly different. The text describes fig_011 as "tuned and derived" from fig_009 parameters without specifying what changed. The parameter values underlying fig_011 are not reported. (Severity: Minor)

- **ID: 24.04.m5 — Redundant notation.** mu_SI is defined as "beta * I(t)" in the parameter description but does not appear in the transition equations, which use beta directly. Remove mu_SI or use it consistently. (Severity: Minor)

- **ID: 24.04.m6 — Number of particles and mif2 iterations not reported.** If mif2 (or any IF2 variant) was used for local search, the number of particles (Np) and iterations (Nmif) must be reported. Without this, computational adequacy cannot be assessed. (Severity: Minor)
