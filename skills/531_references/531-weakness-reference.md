<!--
type: reference
name: STATS 531 Student Weakness Reference
version: 0.2.0
source: W25 quizzes Q1–Q13 (49 questions) + MT1 + MT2
scope: Error detection and severity calibration for STATS 531 final project reviews
-->

# STATS 531 Student Weakness Reference

## Purpose

Document errors that STATS 531 W25 students were explicitly tested on and commonly made wrong in quizzes.

When one of these errors appears in a final project, it should be flagged with higher confidence than general methodological concerns, because the student had direct instruction and assessment on the topic.

This reference answers two questions:
1. **Was this error explicitly taught?** — If students were tested on it in a quiz, the error is course-confirmed (CC-Yes).
2. **Is this a known student misconception?** — Wrong answer choices in quizzes directly document the errors students default to.

This reference does **not** replace `531-conventions.md`. Use both together:
- `531-conventions.md`: suppresses false positives (what NOT to flag)
- `531-weakness-reference.md`: amplifies true positives (what to look for more carefully)

---

## How to use

When reviewing a project:

1. Check whether any of the **documented errors** below appear in the project.
2. If an error matches a quiz-tested misconception, flag it as **CC-Yes** in the scorer.
3. Severity is either **Major** or **Minor** — apply as listed below.
4. Issues outside this reference: apply standard severity, flag as CC-No.

---

## Severity definitions

- **Major** — Materially affects validity of the main analysis or conclusions. Authors must address this.
- **Minor** — Does not invalidate the analysis but reflects a misunderstanding or missed best practice. Worth noting.

---

## Part 1: POMP and Likelihood Inference Errors

Tested in W25 Q8–Q11, Q13; MT2.

---

### Error 1.1 — Averaging log-likelihoods instead of using logmeanexp

**Quiz source:** Q9-02 (explicitly tested; all wrong answers make this error)

**What it looks like:**
- Reporting `mean(c(-2446, -2444, -2443, -2442, -2440))` as the log-likelihood estimate
- Averaging multiple particle filter runs on the log scale

**Why it is wrong:** The particle filter produces unbiased estimates on the natural scale, not the log scale. Correct aggregation is `logmeanexp`. Averaging on the log scale systematically underestimates the true likelihood, invalidating model comparisons.

**Severity: Major**

---

### Error 1.2 — Computing a likelihood slice instead of a profile

**Quiz source:** Q10-02 (explicit distinction tested)

**What it looks like:**
- Varying one parameter while holding all others fixed at their MLE values
- Calling the result a "profile likelihood" without optimizing over nuisance parameters at each target value

**Why it is wrong:** A profile likelihood requires maximizing over all other parameters at each target value. A slice does not. Slices are narrower than profiles and produce artificially tight confidence intervals.

**Severity: Major**

---

### Error 1.3 — Inconsistent units between latent process and measurement model

**Quiz source:** Q8-03 (unit consistency in POMP code explicitly tested)

**What it looks like:**
- Using weekly data but specifying rate parameters per day without converting
- Mixing `dt = 1/52` (years) and rate parameters defined per week

**Why it is wrong:** All time units must be consistent in POMP code. Rate parameters must match the time unit of the latent process. Inconsistent units produce silently wrong parameter estimates.

**Severity: Major**

---

### Error 1.4 — Ignoring Monte Carlo variability in reported log-likelihood

**Quiz source:** Q9-02 (implicit; correct answer requires knowing particle filter estimates are noisy)

**What it looks like:**
- Reporting a single particle filter log-likelihood run as if exact
- Not reporting standard error or replicated estimates
- Treating two log-likelihood values as different without accounting for Monte Carlo noise

**Why it is wrong:** Each particle filter run is a random estimate with variance. Comparisons between models may be dominated by Monte Carlo noise if replication is absent.

**Severity: Major**

---

### Error 1.5 — Declining likelihood during iterated filtering, attributed to wrong cause

**Quiz source:** Q10-01 (explicitly tested; model misspecification is the correct diagnosis)

**What it looks like:**
- Observing likelihood decline after several iterated filtering iterations
- Attributing it to too few particles or iterations rather than model misspecification

**Why it is wrong:** If the unperturbed model shows declining likelihood, this signals model misspecification, not numerical insufficiency. More particles or iterations will not fix this; structural revision is needed.

**Severity: Major**

---

### Error 1.6 — Not comparing to a non-mechanistic benchmark

**Quiz source:** Q11-01 (explicitly tested; benchmark comparison is a validation tool, not competition)

**What it looks like:**
- Reporting only the POMP model likelihood without comparing to ARMA, regression, or GLM
- Concluding the POMP model is good without reference to a simpler model

**Why it is wrong:** A benchmark reveals whether the mechanistic model adds value. The course explicitly taught this as part of model validation. Absence means the model's added complexity is unjustified.

**Severity: Major**

---

### Error 1.7 — CI from Hessian of noisy particle filter likelihood

**Quiz source:** Q9-02 / Q10-02 (indirect; consequence of misunderstanding particle filter noise)

**What it looks like:**
- Computing standard errors from the Hessian of the particle filter log-likelihood
- Treating particle filter output as smooth enough for second-derivative methods

**Why it is wrong:** Particle filter log-likelihood is stochastic and non-differentiable. Hessian-based CIs are invalid; profile likelihood is the appropriate method.

**Severity: Major**

---

### Error 1.8 — Missing convergence diagnostics for iterated filtering

**Quiz source:** Q10-01 / Q10-03 (iterated filtering diagnostics explicitly tested)

**What it looks like:**
- Reporting final parameter estimates without showing the likelihood trajectory across iterations
- No trace plot or diagnostic showing convergence of the optimizer
- No replicated searches from different starting points

**Why it is wrong:** Without convergence diagnostics, there is no evidence the optimizer found the global maximum. Multiple searches with similar terminal likelihoods are the minimum standard.

**Severity: Major**

---

### Error 1.9 — Profile likelihood too sparse to identify the maximum

**Quiz source:** Q10-02 (profile likelihood construction explicitly tested)

**What it looks like:**
- Profile likelihood plot with fewer than ~10 points
- Shape of the profile is unclear; maximum is ambiguous
- Confidence interval endpoints determined from an obviously coarse grid

**Why it is wrong:** A profile likelihood must have enough points to clearly show the maximum and identify where the likelihood drops by the Wilks threshold. A sparse profile does not support valid confidence intervals.

**Severity: Major**

---

### Error 1.10 — Overly narrow convergence criterion

**Quiz source:** Q10-03 (explicitly tested; spread within Wilks threshold is expected)

**What it looks like:**
- Concluding convergence failed because parameter estimates spread across multiple runs
- Not checking whether all runs find similar terminal likelihood values

**Why it is wrong:** The course taught that multiple searches finding likelihoods within a few log units of each other indicates convergence. Spread in weakly identified parameters within the Wilks 95% confidence set is statistically expected, not failure.

**Severity: Minor**

---

### Error 1.11 — Treating demographic stochasticity as sufficient for overdispersion

**Quiz source:** Q11-03 (explicitly tested; additional noise in rates needed beyond basic stochasticity)

**What it looks like:**
- Using a simple compartment model with binomial transitions and claiming adequate variance
- Not adding overdispersion parameters when residual plots or ESS suggest poor fit

**Why it is wrong:** Basic POMP compartment models have demographic stochasticity only. Real disease data often requires explicit overdispersion in rates or the measurement model.

**Severity: Minor**

---

### Error 1.12 — Parametric bootstrap claimed to validate the model

**Quiz source:** Q13-03 (explicitly tested; bootstrap tests inference, not model)

**What it looks like:**
- Simulating from the fitted model, re-fitting, and claiming this validates the model is correct
- Conflating self-consistency of the inference pipeline with accuracy of the model

**Why it is wrong:** The parametric bootstrap can only detect errors in the inference procedure, not in the model formulation itself, because it uses the same simulator for generating and fitting data.

**Severity: Minor**

---

---

### Error 1.13 — Misinterpreting low ESS as always indicating a model problem

**Quiz source:** MT2 Q2-03

**What it looks like:**
- Concluding "the model is misspecified" solely because effective sample size (ESS) drops at certain time points
- Not considering that small measurement error (tight dmeasure) can also cause low ESS with a well-fitting model

**Why it is wrong:** Low ESS has two distinct causes: (A) model misspecification — particles can't reach the observed data; or (C) model fits well but measurement variance is small, so most particles are rejected by dmeasure even though the latent process is correct. Diagnosis requires looking at the overall log-likelihood and residuals, not just ESS.

**Severity: Minor**

---

### Error 1.14 — Claiming likelihoods from different model classes are not comparable

**Quiz source:** MT2 Q4-01

**What it looks like:**
- Refusing to compare POMP model log-likelihood to ARMA or regression log-likelihood
- Stating that "likelihoods from different model classes cannot be compared"
- Treating AIC comparison as invalid because the models are from different families

**Why it is wrong:** Likelihoods for different models of the same data ARE directly comparable — they are all densities evaluated at the same observed data. AIC comparisons are valid across non-nested models. The Neyman-Pearson lemma underlies this. Restricting comparison to nested models is a common misconception.

**Severity: Minor**

---

### Error 1.15 — Increasing Np/Nmif as the first response when POMP fits poorly vs benchmark

**Quiz source:** MT2 Q4-02

**What it looks like:**
- POMP model likelihood is substantially below an ARMA or IID benchmark
- Student response is to re-run with more particles or iterations
- No consideration of model structure changes

**Why it is wrong:** When the model fits disastrously compared to a benchmark, the problem is the model, not the computation. The right first step is to revise model structure — add overdispersion, reconsider compartments, examine residuals. More computation only helps if the model is fundamentally sound.

**Severity: Minor**

---

## Part 2: ARMA and Classical Time Series Errors

Tested in W25 Q1–Q7, Q12; MT1.

---

### Error 2.1 — Treating differencing and detrending as equivalent

**Quiz source:** Q1-01 (explicitly tested; they are not equivalent)

**What it looks like:**
- Differencing a trend-stationary series when detrending (trend + ARMA noise) is appropriate
- Claiming ARIMA and trend + ARMA are interchangeable

**Why it is wrong:** Differencing a trend-stationary series introduces an MA unit root and can produce a non-causal model. The choice depends on whether the trend is stochastic or deterministic.

**Severity: Major**

---

### Error 2.2 — AIC comparison between ARIMA and POMP without noting non-comparability

**Quiz source:** Q4-05 / Q11-01 (model comparison criteria explicitly tested)

**What it looks like:**
- Directly comparing AIC values from an ARIMA model and a POMP model as if they measure the same thing
- No note that likelihoods are computed differently (exact vs. particle filter, different observation models)

**Why it is wrong:** AIC is only comparable across models that use the same data and the same likelihood definition. ARIMA and POMP models often have different observation models and likelihood normalizations; direct AIC comparison is invalid without explicit justification.

**Severity: Major**

---

### Error 2.3 — ADF test misinterpretation

**Quiz source:** Q1-03 (explicitly tested; ADF does not address nonlinear trends)

**What it looks like:**
- Using ADF p-value alone to conclude the series is stationary
- Ignoring nonlinear trend, structural breaks, or pandemic-era disruptions visible in the data

**Why it is wrong:** ADF tests unit root vs. stationarity but does not distinguish nonlinear trends, seasonal patterns, or structural breaks. Visual evidence can be more informative.

**Severity: Minor**

---

### Error 2.4 — Misinterpreting ACF as complete characterization of stationarity

**Quiz source:** Q4-01 (explicitly tested)

**What it looks like:**
- Concluding the series is stationary because ACF decays quickly
- Not checking for time-varying variance or structural breaks

**Why it is wrong:** ACF tests the white noise hypothesis for a specific transformation. It does not rule out time-varying variance or non-stationarity in higher moments.

**Severity: Minor**

---

### Error 2.5 — Not transforming highly skewed count data

**Quiz source:** Q4-02 (explicitly tested; log transformation recommended for right-skewed counts)

**What it looks like:**
- Applying Gaussian ARMA to overdispersed count data without transformation
- QQ-plot shows severe right tail but no remediation attempted

**Why it is wrong:** Gaussian ARMA assumes approximately normal residuals. Long-tailed counts often benefit from log transformation. The course explicitly taught this for disease count data.

**Severity: Minor**

---

### Error 2.6 — Using Ljung-Box test for ARMA model selection

**Quiz source:** Q4-05 (explicitly tested; LBT adds little over AIC for model selection)

**What it looks like:**
- Selecting among ARMA models using Ljung-Box p-values rather than AIC
- Preferring LBT because it produces a p-value

**Why it is wrong:** AIC and LBT measure different things. The course explicitly taught that AIC or likelihood comparison is preferred for model selection; LBT is weak for this purpose.

**Severity: Minor**

---

### Error 2.7 — Running redundant formal tests when visual evidence is conclusive

**Quiz source:** Q4-04 (explicitly tested; formal tests add nothing to obvious patterns)

**What it looks like:**
- Reporting Shapiro-Wilk p = 10^-21 alongside a clearly non-normal QQ-plot as if the test adds credibility
- Reporting multiple diagnostic tests without interpreting what to do differently

**Why it is wrong:** Formal tests are redundant when visual evidence is unambiguous. The better response is to investigate consequences and explore alternatives.

**Severity: Minor**

---

### Error 2.8 — Confusing spectral frequency and period units

**Quiz source:** Q5-01 (explicitly tested; period = 1/frequency, units matter)

**What it looks like:**
- Misidentifying the period corresponding to a spectral peak
- Confusing cycles per observation with cycles per year without unit conversion

**Why it is wrong:** Incorrect unit conversion leads to wrong scientific interpretation of seasonal cycles.

**Severity: Minor**

---

### Error 2.9 — Trusting software likelihood output without checking conventions

**Quiz source:** Q12-02 (explicitly tested; tseries::garch reports non-standard values)

**What it looks like:**
- Comparing likelihoods from different packages without checking normalization conventions
- Reporting positive log-likelihoods for continuous data without noting this is unusual

**Why it is wrong:** Different packages normalize likelihoods differently. Direct comparison is invalid without verification.

**Severity: Minor**

---

### Error 2.10 — Causal language without causal identification

**Quiz source:** Q2 / Q7 (interpretation of time series models explicitly covered)

**What it looks like:**
- Concluding that a variable "causes" an outcome based on a fitted time series model
- Using language like "X drives Y" when the model is correlational

**Why it is wrong:** ARIMA and POMP models describe association and dynamics, not causation. Causal claims require a causal identification strategy beyond model fit.

**Severity: Minor**

---

### Error 2.11 — ADF rejection treated as automatically requiring differencing

**Quiz source:** W26 Class 08

**What it looks like:**
- ADF test rejects the unit root null hypothesis
- Student immediately differences the series, claiming "the data is non-stationary, so I differenced"
- No consideration of whether the series is trend-stationary (deterministic trend + ARMA)

**Why it is wrong:** ADF rejection means the unit root null is rejected — it does not prescribe differencing. If the series has a deterministic trend, detrending (trend + ARMA) is the correct approach. Differencing a trend-stationary series introduces an MA unit root and can produce a non-causal, non-invertible model. The two approaches (differencing vs. detrending) are not equivalent.

**Severity: Minor**

---

### Error 2.12 — Checking stationarity before addressing distributional problems

**Quiz source:** W26 Class 09

**What it looks like:**
- Residual quantile plot shows clear long-tailed or non-normal distribution
- Student proceeds to run ADF or ACF tests on the residuals without first addressing the distributional issue
- Stationarity testing treated as the primary diagnostic tool regardless of residual shape

**Why it is wrong:** Diagnostic analysis has an ordering. Gross distributional violations (long tails, outliers) undermine the validity of stationarity tests. The correct sequence is: (1) inspect residual distribution, (2) transform if necessary, (3) then assess autocorrelation and stationarity. Running ADF on obviously non-normal residuals produces unreliable inference.

**Severity: Minor**

---

### Error 2.13 — AIC table inconsistency treated as valid result

**Quiz source:** MT1 Q3-01

**What it looks like:**
- AIC table shows adding one parameter *increases* AIC by more than 2 units
- Student accepts this as a valid result rather than flagging a numerical failure
- No comment on the implausibility of the AIC difference

**Why it is wrong:** For nested models differing by one parameter, AIC = −2loglik + 2k. Adding one parameter changes AIC by 2 − 2×(loglik_new − loglik_old). Since the unconstrained model always has at least as high a likelihood, adding a parameter can *increase* AIC by at most 2 and *decrease* it by any amount. An increase greater than 2 indicates numerical optimization failure.

**Severity: Minor**

---

### Error 2.14 — Time-varying sample variance taken as proof of non-stationarity

**Quiz source:** MT1 Q1-02

**What it looks like:**
- Observing that rolling variance changes across time windows and concluding "the series is non-stationary"
- Not distinguishing between non-stationarity and conditional heteroskedasticity (e.g., GARCH)

**Why it is wrong:** A stationary model with stochastic conditional variance (like GARCH) can produce time-varying sample variance. Time-varying sample variance is consistent with stationarity. Non-stationarity requires additional evidence (e.g., unit root tests, structural breaks, diverging mean).

**Severity: Minor**

---

### Error 2.15 — Not using multiple optimization starting points for borderline AIC comparisons

**Quiz source:** MT1 Q3-03

**What it looks like:**
- Two ARMA models have AIC values within 1–2 units of each other
- Student accepts the result from a single optimization run
- No attempt to verify with multiple random starting points

**Why it is wrong:** Numerical optimization of ARMA likelihoods can get stuck in local maxima, especially for larger models. When results are borderline, multiple starts (e.g., using `arima2::arima`) are needed to confirm the comparison is reliable.

**Severity: Minor**

---

### Error 2.16 — Confusing AIC difference with the likelihood ratio test statistic

**Quiz source:** MT1 Q3-04

**What it looks like:**
- Computing the likelihood ratio test statistic as AIC₀ − AIC₁ instead of 2×(ℓ₁ − ℓ₀)
- Treating ΔAIC and the LRT statistic as interchangeable

**Why it is wrong:** ΔAIC = AIC₀ − AIC₁ = (−2ℓ₀ + 2k₀) − (−2ℓ₁ + 2k₁) = −2(ℓ₁ − ℓ₀) + 2(k₁ − k₀). For nested models with k₁ − k₀ = 1: ΔAIC = 2(ℓ₁ − ℓ₀) − 2. So the LRT statistic = 2(ℓ₁ − ℓ₀) = ΔAIC + 2. They differ by the penalty term.

**Severity: Minor**

---

## Summary

This reference encodes student errors from W25 quizzes Q1–Q13, W26 quizzes Class 01–20, MT1, and MT2.

**31 errors total:**
- 15 POMP/likelihood errors (Errors 1.1–1.15): 8 Major, 7 Minor
- 16 ARMA/classical errors (Errors 2.1–2.16): 2 Major, 14 Minor

Sources by section:
- Errors 1.1–1.12: W25 quizzes Q8–Q11, Q13
- Errors 1.13–1.15: MT2
- Errors 2.1–2.10: W25 quizzes Q1–Q7, Q12
- Errors 2.11–2.12: W26 quizzes Class 08, 09
- Errors 2.13–2.16: MT1

Use alongside `531-conventions.md` (what not to flag) for complete calibration.
