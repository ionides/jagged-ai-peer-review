# Final AI Review: Utah Covid Model (w21, Project 09)

---

## Overall Assessment

This project models COVID-19 new-case incidence in Utah from March 2020 to April 2021. Three approaches are attempted: an ARIMA(5,2,4) fit to the seven-day rolling average, a pomp-based SIR that encountered computational failure, and a deterministic SIR borrowed from an external tutorial. The project deserves credit for engaging real public-health data, using both statistical and mechanistic frameworks, and being candid about computational difficulties. However, several methodological problems undermine the mechanistic analysis: the deterministic SIR is fitted by ad hoc parameter search rather than likelihood-based inference; the pomp model is abandoned without diagnostic evidence; the SIR model is compared to cumulative cases rather than to the incidence series it should predict; and no quantitative comparison between mechanistic and statistical models is made. These issues, taken together, mean the mechanistic section does not produce reliable or reproducible scientific conclusions.

---

## Key Strengths

- The data is well-sourced (official Utah state coronavirus website), fully documented, and covers a meaningful epidemic window including the December 2020 – January 2021 peak.
- The project acknowledges the weekly reporting artifact (fewer cases reported on weekends) and appropriately works with the seven-day rolling average, which is a sound data-handling decision.
- The ARIMA analysis is more complete than the mechanistic section: the AIC table is shown, model order is selected systematically, coefficients are reported, and residual diagnostics are displayed.
- The author is transparent about the pomp failures rather than concealing them, which is methodologically honest.

---

## Major Points

**ID: 21.09.A | Inference methodology | Severity: Major**

Concern: The deterministic SIR parameters (beta = 0.0088, gamma = 0.0458) are described as "the best parameters," but no optimization criterion, objective function, or search algorithm is given. The methodology comes from a tutorial blog post (statsandr.com). This constitutes ad hoc calibration, not statistical inference.

Why it matters: Without a defined objective function, parameter estimates have no statistical meaning, cannot be compared across models, and cannot be reproduced.

Suggested author action: Specify the fitting criterion explicitly (e.g., sum of squared residuals between model-predicted and observed daily incidence, or a Poisson or Gaussian log-likelihood). Report the criterion value. Even for a deterministic ODE model this is straightforward.

---

**ID: 21.09.B | Model specification — observable mismatch | Severity: Major**

Concern: The ARIMA model is fitted to daily new cases (incidence). The deterministic SIR in figs. 008–010 is evaluated against cumulative incidence. The infected compartment I(t) of an SIR model represents currently infected individuals (prevalence), not cumulative cases. Plotting I(t) against cumulative cases conflates a prevalence quantity with a monotonically increasing cumulative count. The "cycle" visible in the SIR curves in fig_008 is an artifact of this mismatch, not a genuine fit to the epidemic wave structure.

Why it matters: This is a fundamental modeling error. The curves cannot be compared scientifically, and the conclusion that the SIR "shows the cycle of the virus better" has no valid basis.

Suggested author action: To compare the SIR to observed data: either (a) plot I(t) against active-case counts (prevalence), or (b) derive a cumulative infection curve from the SIR (S(0) - S(t)) and compare it to cumulative observed cases, or (c) compare the SIR's predicted daily new infections (beta*S(t)*I(t)/N) to daily new-case counts. Option (c) is most appropriate for the data available.

---

**ID: 21.09.C | Pomp model — abandoned without diagnostic evidence | Severity: Major**

Concern: The pomp section states R "struggled calculating the log-likelihood" and that the displayed output was "the best it calculated." Figures 006–007 show the pomp model trajectories peaking around day 20–30 at 5,000–8,000 cases/day, then collapsing to zero — the model completely fails to track the observed data. No particle count, no number of IF2 iterations, no starting parameter values, and no trace plots are provided. The model equations (transition rates, measurement model) are never stated.

Why it matters: Without this information, neither the failure nor the model can be diagnosed or reproduced. The failure could reflect model misspecification (parameters started in an implausible region, wrong model structure), insufficient computation (too few particles or iterations), or a coding error. Abandoning the section without any diagnostic evidence leaves no scientific information from the central course method.

Suggested author action: Report the number of particles (Np), iterations (Nmif), and starting parameter values used. Show at least one trace plot of log-likelihood vs. iteration. State the measurement model (what distribution was used for observed cases given I(t)?). Even a brief documented failure is more useful than an undocumented one.

---

**ID: 21.09.D | No quantitative comparison between mechanistic and statistical models | Severity: Major**

Concern: The ARIMA has a reported log-likelihood (-2124.52) and AIC (4269.03). No comparable metric is provided for either the deterministic SIR or the pomp model. The claim that the SIR "fits and predicts the data" in the conclusions is therefore unsubstantiated.

Why it matters: A mechanistic model that cannot quantitatively demonstrate any advantage over a statistical benchmark provides no evidence for the underlying biological mechanism.

Suggested author action: Report a goodness-of-fit criterion for the SIR (RSS or a likelihood under a specified noise model) and compare it to the ARIMA. Note that ARIMA AIC and ODE-based RSS are not on the same likelihood scale, but an honest comparison of residuals or R-squared on the same observable is still informative.

---

**ID: 21.09.E | Double-differencing skewed count data without transformation | Severity: Major**

Concern: The ARIMA uses d=2 (two rounds of differencing) on the seven-day average of daily new cases. The raw series is count-like, strictly non-negative, and highly right-skewed. ARIMA assumes approximately Gaussian errors. The residuals in fig_003 show clear heteroscedasticity — small and near-zero in early 2020, large and volatile around the December–January peak — which is the expected signature of a multiplicative error structure not addressed by differencing alone. No unit-root test (ADF or KPSS) is reported to justify d=2.

Why it matters: Differencing a skewed count series without first stabilizing its variance produces residuals that violate ARIMA assumptions, making the model selection and the reported AIC unreliable.

Suggested author action: Apply a log transformation (or square-root transformation) to the seven-day average before fitting ARIMA. Re-examine d=1 vs. d=2 after transformation. Report an ADF or KPSS test result to justify the order of differencing.

---

## Minor Points

- **Ljung-Box contradiction:** The reported p-value of 8.578e-08 strongly rejects white-noise residuals. The text characterizes this as "an okay fit" — this is inconsistent. Acknowledge the residual autocorrelation as a model limitation.

- **ACF mischaracterization:** Fig_002 shows all ACF lags near 1.0, which indicates strong persistence and non-stationarity. The text says "there is no clear lag pattern," which misreads this plot. An ACF that does not decay to zero indicates the series is non-stationary.

- **mu_IR sensitivity:** The recovery rate 1/15 days is fixed using a cross-correlation argument. This method assumes stationarity of both series, which does not hold for epidemic curves. Report the sensitivity of the SIR results to varying this parameter (e.g., 1/10 vs. 1/20 days).

- **Initial conditions unspecified:** For both the pomp and deterministic SIR, the initial number of infected individuals I(0) is not stated. This value substantially affects early epidemic dynamics and must be reported for reproducibility.

- **S(t) vs. observed cumulative cases discrepancy:** In fig_010, the susceptible compartment S(t) declines from 3.25 million to approximately 1 million by April 2021, implying about 2.25 million individuals left S during the modeled period. Observed cumulative cases as of April 2021 were approximately 400,000 — a factor of roughly 5 to 6 difference. Even accounting for substantial under-reporting, this level of discrepancy suggests the SIR is poorly calibrated. This should be discussed explicitly.

- **ARIMA notation:** The displayed ARIMA equation uses both beta and phi for AR coefficients and phi for MA coefficients inconsistently. Standard notation uses phi for AR and theta for MA; the equation as written is internally inconsistent.

- **No population-level dynamics from vaccination:** By late 2020 and early 2021, Utah had begun vaccination. The SIR model does not include a vaccinated compartment and uses the full 3.25M population as susceptible throughout. This is a modeling limitation worth acknowledging.

- **Reproducibility of the deterministic SIR:** The SIR code is reportedly adapted from statsandr.com. The specific function(s) used and their full parameter specifications should be documented in the report so the analysis can be reproduced independently of the external tutorial.

- **Writing quality:** Multiple typographical errors throughout (e.g., "acurate," "suceptable," "dieseas's," "diognostics") reduce the report's professional readability.
