# Peer Review: W21 Project 11 — Modeling COVID-19 Cases in Michigan: ARMA vs. SEIR POMP Model

---

## Summary

This project models the "winter spike" of Michigan COVID-19 daily case counts (October 1, 2020 – February 1, 2021) using two approaches: an ARMA model on HP-filtered data, and a stochastic SEIR POMP model fitted via iterated filtering (mif2). The project is well-intentioned and covers both classical and POMP-based time series approaches, but contains a number of methodological, model specification, computational, and presentation weaknesses. The most critical issues concern the measurement model, the initialization of the accumulator variable H, and inadequate convergence diagnostics.

---

## Weaknesses (Most Critical First)

### 1. [MAJOR] Accumulator Variable H Initialized Incorrectly — Fundamental Model Error

In `seir_init`, the hidden state H is initialized as:

```c
H = nearbyint((1-eta)*N);
```

H is declared as an `accumvars` variable, meaning it is reset to zero at each observation time and accumulates new transitions during each measurement interval. Initializing H to `(1-eta)*N` (approximately 1.6 million individuals) at time t=0 has no epidemiological meaning. Because H is reset by the `accumvars` mechanism at every observation time, the initial value of H only affects the very first measurement. However, setting it to a quantity equal to the number already recovered — rather than to zero or to something representing current infectious throughput — is conceptually incorrect and would cause the first likelihood evaluation to be evaluated against a vastly inflated H. The correct initialization is `H = 0`.

### 2. [MAJOR] Measurement Model Binomial Is Misapplied — H Rather Than New Cases

The measurement model uses:

```c
lik = dbinom(reports, H, rho, give_log);
```

where H accumulates transitions from I to R over each day. In a standard SEIR POMP model for reported cases, the observable (new reported cases) should be linked to `dN_EI` (new symptomatics) or `dN_IR` — typically to the flow from I to R, which H here tracks. However, if the goal is to model reported cases as a fraction of newly infectious individuals, H should accumulate `dN_EI` (transitions from E to I), not `dN_IR`. Reported cases are generally people who test positive when they become symptomatic (E to I transition), not when they recover. Using H = cumulative I-to-R transitions conflates recovery with reporting and produces a systematically biased measurement model.

### 3. [MAJOR] No Profile Likelihood or Confidence Intervals Reported — Parameter Uncertainty Completely Ignored

The project reports maximum log-likelihood estimates but provides no profile likelihood slices and no confidence intervals for any parameter. With such poor convergence (see below), there is no way to assess whether any parameter estimate is statistically meaningful. For a POMP project, profile likelihood intervals over key parameters such as Beta, mu_EI, mu_IR, and eta are essential for interpreting results.

### 4. [MAJOR] Extremely Poor Log-Likelihood Values — Model Fit Is Catastrophically Bad

The best log-likelihood found from the global search is approximately -10,633 (from `new_global2.csv`), while the initial hand-set parameter point gives a log-likelihood of approximately -54,405 (from `cov_params.csv`). The discrepancy of tens of thousands of log-likelihood units between different runs indicates the surface is not being reliably explored, and the absolute values are extremely negative given only 124 daily observations. A difference in log-likelihood of 44,000 units between the naive starting point and the global search best suggests fundamental problems with either the model, the data, or the computational setup. No comparison is made against a null model to assess whether the SEIR model provides any meaningful fit.

### 5. [MAJOR] Parameter Transformations Incorrectly Applied — logit Transform on Beta Is Invalid

In `parameter_trans`, the authors apply:

```r
partrans=parameter_trans(logit=c("Beta","mu_EI","mu_IR"))
```

A logit transformation constrains parameters to (0, 1). However, Beta (the contact rate) is not bounded above by 1 — in a standard SEIR model, Beta can and often does exceed 1, since it represents contacts per person per unit time. Constraining Beta to (0, 1) artificially prevents the optimizer from exploring Beta > 1, which may partly explain poor convergence of this parameter. A log transformation would be more appropriate for Beta. Notably, even within (0,1), the global search finds Beta values up to 0.999, suggesting the constraint is binding.

### 6. [MAJOR] Global Search Re-runs mif2 Without Adequate Cooling or Particle Count

In the global search, the code does:

```r
mf1 %>%
  mif2(params=c(unlist(guess),fixed_params)) %>%
  mif2(Nmif=50)
```

This re-runs mif2 with Nmif=50 from each guess, but the first `mif2` call uses no explicit Nmif or rw.sd, inheriting those from mf1 (the local search result). Running two mif2 calls sequentially without specifying rw.sd in the second call is non-standard and potentially leads to incorrect perturbation schedules. Additionally, Np=1000 and Nmif=50 are used throughout; for a 124-observation epidemiological time series with four free parameters, this is at the low end and may be insufficient to locate the global maximum reliably.

### 7. [MAJOR] Data Reproducibility Compromised — External URL Dependency

The POMP section reads data from an external GitHub URL:

```r
data <- read.csv("https://raw.githubusercontent.com/jeremyny/G6_Final/main/MI_COVID19_data.csv")
```

This is a different dataset from `covid_data.csv` used in the ARMA section and includes a rolling average column (`Cases_RA`) and vaccination doses (`doses`). If the GitHub repository becomes unavailable, the POMP portion of the analysis cannot be reproduced. The local `covid_data_updated.csv` file exists but is generated mid-script, creating a fragile reproducibility chain. The two datasets (raw cases vs. rolling average) are inconsistently used across sections without adequate explanation.

### 8. [MODERATE] Two Different Data Streams Used for ARMA and POMP — No Justification

The ARMA section uses raw daily case counts from `covid_data.csv`, while the POMP section uses a 7-day rolling average (`Cases_RA`) from the GitHub-sourced dataset. Switching between raw and smoothed data across the two modeling approaches makes any comparison between ARMA and POMP model fits meaningless, since they are not modeling the same observational data. This inconsistency is never acknowledged or justified in the text.

### 9. [MODERATE] HP Filter Lambda Choice Is Incorrect for Daily Data

The HP filter is applied with `freq = 100`. The authors cite course slides as justification for lambda=100, but in the cited slides, lambda=100 is recommended for annual macroeconomic data (business cycle frequency). For daily epidemiological data, a much larger lambda would be appropriate to extract a smooth trend. Using lambda=100 on daily data will over-smooth the cycle component, potentially removing meaningful epidemiological signal. The authors treat the HP filter cycle as if it were a stationary residual suitable for ARMA modeling without verifying this choice.

### 10. [MODERATE] rho Fixed at 0.1 Without Sensitivity Analysis

The reporting rate rho is fixed at 0.1 throughout, based on a single external literature estimate. There is no sensitivity analysis of model results to the choice of rho, no attempt to estimate rho jointly with other parameters, and no acknowledgment of the uncertainty this choice introduces. Given that rho directly scales the measurement model, its choice substantially affects all other parameter estimates.

### 11. [MODERATE] Initial Conditions for E and I Are Hard-Coded Without Uncertainty

E(0) = 90,000 and I(0) = 66,000 are hard-coded in `seir_init` as fixed constants, not as functions of model parameters. This means these quantities are never optimized or profiled despite being highly uncertain. For comparison, the total Michigan population is 10 million, so E(0) + I(0) = 156,000 represents about 1.56% initially infected/exposed — a quantity that could vary considerably and affect the entire trajectory.

### 12. [MODERATE] Convergence Diagnostics Are Incomplete and Partially Misread

The text notes that "mu_EI gave a suspicious result as it had a steep drop and converged around 0" and is self-aware about non-convergence. However, the global search section text confusingly describes what appears to be the local search results ("mu_EI stays between 0.0 and 0.15") before the global search code is run, suggesting the narrative was written out of order. No geometric cooling fraction is reported or discussed, no assessment of whether the likelihood stopped improving is provided, and no replicate runs from the same starting values are shown to evaluate Monte Carlo variability.

### 13. [MODERATE] ARMA Model Selection Is Poorly Justified — Code Shows ARMA(1,1) But Text Selects ARMA(2,2)

The code block explicitly fits and prints `arima11` (the ARMA(1,1) model) but then the text says "We will consider the ARMA(2,2) model." The residual analysis is then performed on `arima22`. There is no clear numerical justification given for why ARMA(2,2) is preferred over ARMA(1,1) or other nearby models in the AIC table, and the AIC table itself is never discussed numerically in the text.

### 14. [MINOR] Weekly Seasonality in Residuals Is Noted but Not Addressed

The ARMA residual analysis notes "a larger spike on every seventh lag" in the ACF, suggesting weekly reporting periodicity. However, no attempt is made to address this — no SARMA model is considered, no day-of-week covariate is introduced in the POMP model, and no pre-processing step removes the weekly cycle. This is a meaningful feature of COVID-19 case data (testing labs report fewer cases on weekends) that is left unaddressed.

### 15. [MINOR] No Simulation-Based Model Check After Fitting

After fitting the SEIR model, there is no posterior predictive simulation comparing fitted model trajectories against the observed data. The initial simulation at hand-chosen parameter values is shown, but no simulation from estimated parameters is presented. Without such a visual check, it is impossible to assess whether the fitted model plausibly reproduces the observed winter spike trajectory.

---

## Summary Table

| # | Severity | Issue |
|---|----------|-------|
| 1 | Major | H accumulator initialized to (1-eta)*N instead of 0 |
| 2 | Major | Measurement model links reports to I-to-R flow rather than E-to-I flow |
| 3 | Major | No profile likelihood or confidence intervals for any parameter |
| 4 | Major | Catastrophically poor log-likelihood values with no null model comparison |
| 5 | Major | logit transform on Beta incorrectly constrains it to (0,1) |
| 6 | Major | Global search mif2 setup is non-standard and underspecified |
| 7 | Major | External URL dependency breaks reproducibility |
| 8 | Moderate | Different data streams (raw vs. smoothed) used for ARMA and POMP |
| 9 | Moderate | HP filter lambda=100 inappropriate for daily data |
| 10 | Moderate | rho fixed at 0.1 with no sensitivity analysis |
| 11 | Moderate | Initial conditions E(0), I(0) hard-coded and never estimated |
| 12 | Moderate | Convergence diagnostics incomplete and narrative is out of order |
| 13 | Moderate | ARMA model selection poorly justified; ARMA(1,1) printed but ARMA(2,2) chosen |
| 14 | Minor | Weekly seasonality in residuals identified but not addressed |
| 15 | Minor | No simulation from estimated parameters to check model fit |

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project11/covSEIR.c`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project11/covid_data.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project11/covid_data_updated.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project11/cov_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project11/new_global2.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project11/Makefile`
