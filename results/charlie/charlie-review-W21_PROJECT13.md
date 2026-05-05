# Peer Review: W21 Project 13
## "An Investigation into COVID-19 in California"

---

## Summary

This project fits an ARIMA(4,1,3) model and a custom SEAPIRD (Susceptible-Exposed-Asymptomatic-Presymptomatic-Infected-Recovered-Deceased) POMP model to daily COVID-19 case counts in California from January 2020 to April 2021. The authors incorporate time-varying transmission via six intervention-period scaling coefficients applied to the baseline transmission rate Beta. The project compares the ARIMA and POMP models using log-likelihood. While the project demonstrates admirable ambition in model complexity and makes use of mif2 with both local and global search, it contains several critical errors in the measurement model that undermine the validity of the fitted likelihoods, and lacks profile likelihoods, no-benchmark comparison, and several methodological safeguards required for credible inference.

---

## Major Issues

### 1. Accumulator variable H tracks recoveries, not cases (CC-Yes, Error 1.3 analog — semantic mismatch)

The accumulator variable `H` is defined in `seapird_step` as:

```
H += dN_IR + dN_AR;
```

This means `H` accumulates the number of individuals moving from I to R and from A to R — that is, **recoveries** — not new infections or confirmed cases. However, both `rmeasure` and `dmeasure` use `H` as the expected number of reported COVID cases:

```
double mean_cases = rho*H;
```

The observed data `cases` represents **new confirmed COVID cases** (infections), not recovered individuals. Fitting `rho*H` (proportion of recoveries) to reported new case counts is a fundamental semantic error. The model is being optimized against a quantity that has no meaningful relationship to what it claims to predict. All reported likelihoods (-3791, -3810) are produced by this misspecified likelihood, and conclusions about model fit are invalid.

**Fix:** The accumulator variable should track new infections (`dN_SE` or `dN_PI`) rather than recoveries, or a separate accumulator for incident cases should be defined and used in the measurement model.

### 2. dmeasure subtracts deaths from cases in a logically inconsistent way

In `dmeas`, the likelihood is evaluated as:

```c
lik = dnorm(cases - deaths, mean_cases, sd_cases, 0);
```

The observation subtracted is `cases - deaths`. The text states "We assume the number of COVID-19 deaths are always reported" and that deaths are counted within the confirmed case tally. However, `mean_cases = rho*H` where `H` is the recovery count (see Issue 1). Subtracting `deaths` from observed `cases` before comparing to `rho*H` (recoveries) has no mechanistic justification. The text in Assumption 2 claims the model targets "recovered cases" but the observed data series is labeled `new_case` (incident infections). This inconsistency means the model never correctly relates latent process states to the observable data stream.

**Fix:** Clearly define whether the target observation is incident cases or recovered cases, build an accumulator that tracks the appropriate quantity, and remove the ad hoc subtraction of deaths unless it is mechanistically motivated and clearly explained.

### 3. Global search parameter box allows rho > 1 (impossible value for a reporting rate)

In the global search box:

```r
rho=c(0,2),
```

The parameter `rho` is declared as a reporting rate (probability) and is logit-transformed. However, the search box specifies natural-scale values from 0 to 2. Values of `rho` drawn from Uniform(0, 2) can exceed 1, which is nonsensical for a probability. While the logit transform is applied during mif2 perturbations, the **initial values** for each global search replicate are drawn from this box using `runif(1, x[1], x[2])` in the natural scale before mif2 starts. Starting at `rho = 1.5` will cause the logit transformation to try to evaluate `logit(1.5)`, which is undefined (and would produce NaN or Inf). Even if the code handles this gracefully, these initial points are invalid and the global search wastes half its effort on infeasible starting points.

**Fix:** Constrain the global search box for `rho` to `c(0, 1)`.

### 4. No profile likelihoods or confidence intervals for any parameters (CC-Yes, Error 1.9)

The project fits 15 estimated parameters (Beta, alpha, 5 rate parameters, 6 intervention coefficients, rho, tau) but reports no profile likelihoods, no confidence intervals, and no uncertainty quantification for any of them. Parameter identifiability is entirely unassessed. With 6 intervention coefficients that share the same Beta baseline, severe collinearity is expected, and the pairs plot (which is shown only for the local search for a subset of parameters) cannot substitute for formal profile likelihoods. Without identifiability assessment, reported MLEs may be unreliable. Wheeler et al. (2024) identify profile likelihoods as essential for assessing whether parameters are estimable from the data.

**Fix:** Compute profile likelihoods for at least the key epidemiological parameters (Beta, rho, alpha, mu_IR) and report 95% confidence intervals.

### 5. No non-mechanistic benchmark comparison (CC-Yes, Error 1.6)

The project compares ARIMA and POMP log-likelihoods but does not compare the POMP model against a simpler non-mechanistic benchmark such as an IID negative binomial model. The ARIMA log-likelihood (-4091) uses a different observation model (Gaussian on differenced counts) and cannot serve as a direct mechanistic benchmark. An IID model fit to the raw case counts would provide the weakest meaningful baseline. Given that the POMP measurement model is misspecified (see Issues 1 and 2), it is unclear whether the improvement in log-likelihood reflects genuine mechanistic insight.

**Fix:** Fit a negative binomial IID or ARIMA model to the undifferenced case counts and compare the POMP log-likelihood on the same scale. Acknowledge the measurement model normalization differences when comparing ARIMA and POMP.

### 6. AIC/likelihood comparison between ARIMA and POMP treated as direct without justification (CC-Yes, Error 2.2)

The conclusion states: "The arima model had a log likelihood of -4091 using 7 parameters. The POMP model had a likelihood of -3792." The authors then conclude POMP performs better. However, ARIMA(-4091) is fitted to first-differenced data with a Gaussian observation model, while the POMP model (-3792) uses the undifferenced raw count series with a normal approximation to a binomial measurement model. These likelihoods are not on the same scale and cannot be directly compared. The ARIMA log-likelihood is evaluated on differenced data (one observation lost to differencing), while the POMP likelihood is evaluated on all 442 observations. Additionally, the two observation models have different normalizations.

**Fix:** Either fit both models to the same untransformed data with the same observation model, or explicitly acknowledge the incomparability and refrain from using the likelihood difference as evidence for POMP superiority.

### 7. Incomplete intervention period specification (placeholder text left in report)

Under Model Assumptions, Assumption 1 states: "We assume lockdown measures across California from **x-x and x-x** scales the force of the invention coefficient..." The intervention time intervals are listed as literal placeholder text "x-x and x-x" — they were never filled in. The actual intervention periods used in the code are defined as day indices (days 1-99, 100-199, 200-249, 250-299, 300-399, 400+) but these are never translated to calendar dates in the paper. Readers cannot assess whether the intervention periods align with the policy events described in the introduction.

**Fix:** Replace placeholder text with actual date ranges and map the numerical day indices back to calendar dates that correspond to the policy events described in the background section.

---

## Minor Issues

### 8. Very limited global search with only 8 replicates

The global search runs only 8 parallel mif2 chains (`foreach(i=1:8,...)`). For a model with 15 estimated parameters and a high-dimensional, potentially multimodal likelihood surface, 8 global search replicates is insufficient to have confidence that the global maximum has been found. The course convention for run_level=3 recommends Nreps_global=100. While the authors appear to have run additional searches on a computing cluster (evidenced by `local_results_greaklakes.csv` and `local_results_greatlakes2.csv`), the total number of global search replicates is not stated clearly.

**Fix:** Report the total number of global search replicates across all runs. Aim for at least 40-100 replicates for a model of this complexity.

### 9. Convergence plots embedded as pre-generated PNG images

The three convergence diagnostic plots (`convergenceplot1.png`, `convergenceplot2.png`, `convergenceplot3.png`) are embedded as static external images rather than generated inline from the saved mif2 objects. This means the displayed convergence plots cannot be verified as coming from the analysis described in the code. If the `.rds` files were regenerated, the plots would not update automatically, creating a reproducibility gap.

**Fix:** Generate convergence trace plots directly from the `mifs_local` or `mifs_global` objects using `traces()` within the Rmd, as the local search section already does.

### 10. No process noise (environmental stochasticity) in transmission

The SEAPIRD model uses only demographic stochasticity (binomial transitions). No multiplicative gamma noise or other environmental stochasticity is applied to the transmission rate Beta. For COVID-19 data, where superspreading events, weekend reporting effects, and policy shocks create substantial overdispersion beyond demographic noise, this likely leads to underestimated uncertainty in the latent process. Wheeler et al. (2024) note that models without process noise may absorb unmodeled stochasticity into other parameters, distorting estimates.

**Fix:** Consider adding a multiplicative noise term to Beta (e.g., `beta_intervention * exp(Normal(0, sigma^2))` per time step) to capture environmental stochasticity.

### 11. rw.sd = 0.01 uniformly for all parameters regardless of scale

All 15 parameters use `rw.sd = 0.01` in the iterated filtering. However, parameters span very different magnitudes: `tau` ranges from 500 to 4000, `mu_ID` ranges from 1e-8 to 1e-5, and `Beta` from 0 to 2. Since partrans applies log/logit transformations, the rw.sd of 0.01 is applied on the transformed scale, which is more defensible, but the course standard of 0.02 on the log scale is commonly used. The uniformly small perturbation size of 0.01 may slow exploration of the likelihood surface, especially for weakly identified parameters.

**Fix:** Use the course-standard `rw.sd = 0.02` on the log/logit scale for most parameters, or justify the choice of 0.01 with evidence that larger perturbations destabilize the filter.

### 12. Fixed initial conditions with no sensitivity analysis

Initial conditions are fixed at `S = N`, `E = 0`, `A = 0`, `P = 0`, `I = 250`, `R = 0`, `D = 0`. The value `I_0 = 250` is stated as "reasonable" but not justified from data or literature, and no sensitivity analysis is performed. Wheeler et al. (2024) note that initialization strategy can affect AIC by ~72 units for complex models.

**Fix:** Either estimate `I_0` as a free parameter or show that results are robust to plausible alternative initial values (e.g., I_0 = 100, 500).

### 13. The H accumulator semantic mismatch also affects rmeasure

In `rmeas`, the simulated `cases` output is:

```c
cases = rnorm(mean_cases, sd_cases) + D;
```

where `mean_cases = rho*H` with H being recoveries. Adding `D` (deaths) to recovery-based cases makes no mechanistic sense. The `rmeasure` and `dmeasure` are inconsistent: `dmeas` evaluates `dnorm(cases - deaths, rho*H, sd)` while `rmeas` generates `cases = rnorm(rho*H, sd) + D`. These are only consistent if `D` equals `deaths`, but simulated trajectories may have `D` growing unboundedly (it's a stock, not a flow), while `deaths` in the observation data is a daily flow. The mismatch between the stock `D` and the flow observation `deaths` is an additional error.

**Fix:** Use a separate daily-death accumulator variable that resets each time step (like H), and use it consistently in both rmeasure and dmeasure.

### 14. ACF interpretation overstated for stationarity assessment

The authors write "We can see that acfs are outside the band and the value decreases as lag increases. Thus modeling differenced data may be preferable." The ACF showing slow decay is consistent with non-stationarity, but the authors do not apply a formal unit root test (ADF) to distinguish between a unit-root process (appropriate for differencing) and a trend-stationary process (appropriate for detrending). For COVID case data with clear seasonal waves and interventions, a deterministic trend model may be more appropriate than differencing.

### 15. AIC table may contain numerical instability for larger models

The AIC table for ARIMA model selection includes models up to ARIMA(4,1,5). For COVID count data that is clearly non-Gaussian (right-skewed, overdispersed), and with no log-transformation applied, the Gaussian ARIMA assumption is violated. Some AIC values in the table should be checked for whether adding parameters ever increases AIC by more than 2 units (which would indicate optimization failure per MT1 Q3-01). The authors select ARIMA(4,1,3) by AIC but note the QQ-plot shows non-normal residuals without pursuing remediation.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project13/covidSEAPIRD.c`
