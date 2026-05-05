# Peer Review: W21 Project 09 — Utah Covid Model

## Summary

This project attempts to model the spread of COVID-19 in Utah using three approaches: an ARIMA model on seven-day rolling average case counts, a stochastic SIR model built with the `pomp` package (iterated filtering), and a deterministic SIR model fitted by residual sum of squares minimization using the `deSolve` package. The paper's core mechanistic modeling goal — applying POMP methods to estimate parameters and quantify uncertainty — is largely abandoned mid-analysis: the `mif2`/`pfilter` code is entirely commented out, the measurement model contains a fundamental mismatch between `dmeasure` and `rmeasure`, and the final result presented is a deterministic ODE model fitted by least squares. No log-likelihoods are reported, no convergence diagnostics exist, no profile likelihoods are computed, and the ARIMA model fit is used only for comparison in passing without quantitative linkage to the mechanistic model. The paper has significant structural and methodological problems that undermine its main conclusions.

---

## Major Issues

### 1. POMP analysis entirely commented out — no inference performed (CC-Yes, Error 1.8)

The entire iterated filtering and particle filter section of the code is commented out (lines 211–305 in `blinded.Rmd`). This includes all `mif2` calls, all replicated `pfilter` evaluations, all parameter pair plots, and all likelihood estimates. No results from the POMP inference pipeline are actually shown in the paper. The author explicitly acknowledges this: "After a certain number of numerics, R struggled calculating the log-likelihood statistic... this was the best I could do." What is presented instead are two forward simulations from manually chosen parameter guesses (Beta=17, mu_IR=0.5; and Beta=50, mu_IR=0.04). This is ad hoc calibration by eyeballing, not likelihood-based inference. The core methodological deliverable of the POMP section is entirely missing. Per Wheeler et al. (2024) and the course standard, parameters must be estimated by maximizing the likelihood.

### 2. Measurement model mismatch between `dmeasure` and `rmeasure` (CC-Yes, Error 1.3)

The `dmeasure` function (`sir_dcovid`) uses a negative binomial distribution with parameters `mu=s` and `size=theta`, where `s` is passed as a state variable. However, the `rmeasure` function (`sir_rcovid`) draws from a binomial distribution with `size=H` and `prob=rho`, where `H` is the accumulator compartment. The two functions do not define the same observation distribution. Specifically:

- `dmeasure` evaluates `dnbinom(x=count, mu=s, size=theta, ...)` — but `s` is the susceptible compartment, not the expected number of new cases. This is almost certainly a naming collision where the author intended `s` to represent a scale parameter for the negative binomial, not the susceptible count `S`.
- `rmeasure` draws `rbinom(n=1, size=H, prob=rho)`, an entirely different distributional form.

The parameter `theta` is also never included in `paramnames`, meaning it has no defined value in the POMP object. The accumulator variable `H` represents cumulative recoveries (via `dN_IR`) rather than new infections (`dN_SI`), so even the rmeasure is tracking the wrong process if new cases are what is observed. This is a fundamental code error that would silently invalidate any likelihood evaluation.

### 3. Deterministic ODE model fitted by RSS, not likelihood — ad hoc calibration (Wheeler et al. 2024, §Likelihood-based inference)

The final model that is actually presented and discussed is a deterministic ODE SIR model fitted by minimizing residual sum of squares between the I compartment and cumulative case counts. This approach:

- Does not specify or maximize a likelihood function, making formal model comparison and uncertainty quantification impossible.
- Fits cumulative cases (a monotonically increasing curve) to the I compartment of the ODE, which represents active infections at a point in time — not cumulative incidence. These are different quantities, and comparing them is a model specification error.
- Does not account for the observation process (reporting rate, overdispersion).
- Cannot produce confidence intervals for parameters.

Per Wheeler et al. (2024): "Ad hoc calibration (moment matching, eyeball fitting, fitting to summary statistics) is less reliable and makes formal model comparison difficult."

### 4. No log-likelihood or AIC reported for any model — visual-only comparison (CC-Yes, Error 1.6; Wheeler et al. 2024, §Quantitative goodness-of-fit)

No quantitative goodness-of-fit statistic is reported for any model in the paper — not for the ARIMA model, not for the POMP model, and not for the deterministic SIR. The only model comparison is a visual one: the author states the deterministic SIR "seems to show the cycle of the virus better than the pomp model." Wheeler et al. (2024) explicitly state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." Without log-likelihoods or AIC values, no quantitative model comparison is possible. The ARIMA model's AIC table is produced but never used to compare against the mechanistic models.

### 5. Accumulator variable `H` tracks recoveries, not new infections — wrong observable linked to data (POMP specification error)

In `sir_step`, the accumulator `H` is incremented by `dN_IR` (the number transitioning from I to R, i.e., new recoveries). However, the observable in the data is `Seven.day.Average`, which represents seven-day averaged new *infections* (positive test reports), not new recoveries. The `rmeasure` function draws from `H` via `rbinom(size=H, prob=rho)`, so the simulated observations represent a fraction of new recoveries, not new infections. This is a fundamental model misspecification: the latent process being linked to the data is wrong.

### 6. No convergence diagnostics for iterated filtering — no evidence of optimization (CC-Yes, Error 1.8)

Because the `mif2` code is commented out, there are no trace plots, no convergence trajectories, no replicated searches from different starting points, and no evidence that any optimization was attempted or succeeded. The standard course requirement is to show likelihood traces across IF2 iterations and to run multiple searches from diverse starting values. None of this exists.

### 7. No profile likelihoods — parameter identifiability not assessed (Wheeler et al. 2024, §Parameter identifiability)

No profile likelihoods are computed for any parameter. The recovery rate `mu_IR` is fixed at 1/15 via a cross-correlation analysis rather than estimated and profiled. Other parameters (Beta, rho, eta) are hand-tuned. Without profile likelihoods, there is no basis for confidence intervals and no evidence that any parameter is identifiable from the data.

### 8. SIR model applied to cumulative cases rather than incident cases in the deterministic section

The deterministic ODE fit minimizes the difference between the I compartment (active infections at each time point) and `dat$Cumulative.Cases` (total confirmed cases to date). This is conceptually incorrect: the SIR model's I compartment is a prevalence measure, while cumulative cases is a monotonically increasing incidence sum. These are not the same quantity. A correctly specified deterministic SIR model fit to cumulative data should use the cumulative incidence (S(0) - S(t)) not I(t). This mismatch means the fitted parameters have no valid epidemiological interpretation.

---

## Minor Issues

### 9. `theta` parameter missing from `paramnames` in the POMP object

The `dmeasure` function references `theta` as the size parameter of the negative binomial, but `theta` does not appear in the `paramnames` vector: `paramnames=c("Beta","mu_IR","N","eta","rho")`. In `pomp`, parameters not declared in `paramnames` cannot be passed to C snippets or used consistently. This would cause `theta` to be undefined or to silently take a default value of zero or NA, breaking the negative binomial evaluation.

### 10. ARIMA model with d=2 applied without justification for double differencing

The AIC table uses `order = c(p, 2, q)` for all models, fixing `d=2`. Double differencing is appropriate only if the series has two unit roots. The raw COVID case data is a rolling seven-day average that clearly has a trend, but applying `d=2` without first demonstrating that `d=1` leaves a unit root is an unjustified choice. The author should have presented an AIC comparison across `d=0,1,2` or used formal unit root tests to select the differencing order.

### 11. ARIMA(5,2,4) selected but residual ACF still shows correlated lags

The author notes "there are also a few more lags outside of the ACF boundaries than we would like to see" in the ARIMA residuals but draws no conclusion and takes no remedial action. The `checkresiduals` output shows the Ljung-Box test result, but the author does not discuss whether this suggests the model is inadequate or whether larger (p,q) should be explored.

### 12. Recovery rate fixed via cross-correlation of seven-day averages, not estimated

The `mu_IR` value is fixed at 1/15 days based on a lag correlation analysis between new cases and new recoveries. This ignores that the seven-day smoothed recovery series is a delayed version of the smoothed case series, and the lag of maximum correlation is a rough measure confounded by the smoothing. The parameter should be estimated within the model rather than fixed externally, or at minimum its sensitivity should be assessed.

### 13. Initial conditions in the POMP model are partially misspecified

The `rinit` function sets `R = round(N*(1-eta))`, meaning almost the entire population starts as recovered (e.g., with `eta=0.06`, R starts at approximately 3,055,000). For COVID-19 in March 2020, essentially no one was recovered. This initialization makes the SIR dynamics biologically implausible from the start and is likely a typo where the author intended `S = round(N*eta)` and `R = 0` (or `R = N - S - I`).

### 14. `s` in `dmeasure` is ambiguous and likely wrong

The `sir_dcovid` function signature is `function(count, s, theta, ..., log)`. In `pomp`, lowercase state names are passed to measurement model functions by their declared `statenames`. The declared states are `S`, `I`, `R`, `H` (uppercase). The parameter `s` (lowercase) is not a declared state or parameter name. It is unclear what value `s` would take — it may be zero, NA, or undefined, which would make `dnbinom(x=count, mu=s, size=theta, log=log)` return `-Inf` or an error. This is a critical implementation bug.

### 15. No benchmark comparison between ARIMA and POMP log-likelihoods

While the conventions file notes that benchmark comparison is encouraged but not required, the paper explicitly sets up the ARIMA model in the same section with implied intent to compare models. No quantitative comparison is made, and no ARMA or IID log-likelihood is reported alongside the mechanistic model to evaluate whether the POMP model adds explanatory value. This is a missed opportunity that leaves the model validation incomplete.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project09/blinded.Rmd`
