# Peer Review: W24 Project 12
# Time Series Analysis of COVID-19 Cases in Kent County

---

## Summary

This project fits a SEIRS compartmental model to 212 weeks of COVID-19 case data for Kent County, Michigan (Feb 2020 – Mar 2024). The authors use an ARMA(2,1) model as a benchmark, implement piecewise time-varying transmission and reporting rates, and perform local and global searches followed by a profile likelihood over rho3. The project is reasonably structured but contains several methodological and implementation issues that limit confidence in the results.

---

## Weaknesses (Prioritized)

### 1. MAJOR: `global_results` Overwritten with Only Top 6 Rows Before Profile Likelihood

At line 800 of `blinded.Rmd`, the authors execute:
```r
global_results <- global_results %>% arrange(-loglik) %>% head
```
This permanently overwrites `global_results` with only 6 rows. The subsequent profile likelihood box construction (the call to `filter(global_results, loglik > max(loglik) - 20)`) therefore operates on at most 6 data points rather than all 200 global search results. The box ranges computed from 6 rows are narrower and less representative than those from the full set of results, potentially biasing the profile likelihood search region. All downstream profile likelihood inference is affected.

### 2. MAJOR: `sigmaSE` Exceeds Global Search Upper Bound — Parameter at Boundary

The global search bounded `sigmaSE` in the range (0, 0.5), yet the best global result yields `sigmaSE = 0.946` — nearly double the stated upper bound. The local search (which started at `sigmaSE = 0.25`) had already moved to `sigmaSE = 0.866` before the global search, and the global search used `mf1` (a local mif2 result) as the template. This means the global search effectively began from a point already outside its own stated parameter box for `sigmaSE`. The optimization is hitting the upper limit of what the perturbations allow, indicating that the overdispersion parameter is likely not well characterized and the upper search bound was too restrictive. The authors do not acknowledge this inconsistency.

### 3. MAJOR: Profile Likelihood Uses Only 11 Coarse Grid Points and Yields a Degenerate CI

The profile over `rho3` uses `seq(0, 1, by = 0.1)` — only 11 fixed values. Only 3 points exceed the 95% confidence threshold (`rho3 in {0.37, 0.52, 1.0}`), and the upper bound of the resulting CI is 1.0, the natural boundary of the reporting rate. A CI with its upper limit at the parameter boundary is not interpretable as a standard confidence interval. The authors acknowledge that "only 4 points above the threshold" may yield a "dubious interval," but do not take corrective action such as refining the grid or running the profile over a narrower range with more points. The coarse grid and boundary issue substantially undermine the profile likelihood analysis.

### 4. MAJOR: SEIRS Model Fails to Outperform ARMA Benchmark by 32.5 Log Units

The best SEIRS log-likelihood is -1403.97 while the corrected ARMA(2,1) log-likelihood is -1371.47, a gap of 32.5 log units. The SEIRS model has 13 free parameters versus 5 for ARMA(2,1), yet performs substantially worse. This gap indicates either persistent model misspecification, optimization failure, or that the model complexity is not warranted by the data. The authors note this failure but frame it as evidence of "the difficulties in modeling the COVID-19 pandemic" rather than investigating root causes. Possible explanations — such as the `sigmaSE` boundary issue, the near-zero `mu_RS` estimate, or the coarse profile — are not systematically examined.

### 5. MAJOR: Near-Zero `mu_RS` Estimate Renders the SEIRS Extension Biologically Meaningless

The optimal global result yields `mu_RS = 0.00060`, corresponding to an average waning period of approximately 1,659 weeks (~32 years). This means the SEIRS extension — the defining feature distinguishing this model from a simpler SEIR — provides essentially no waning immunity over the study period. The authors acknowledge that "a recovery period of roughly 20 years is not intuitive" and that "moving from SEIR to SEIRS may not provide impactful results," but they do not compute a profile likelihood over `mu_RS` to formally test whether the SEIRS extension is supported by the data. A likelihood ratio test comparing the SEIRS and SEIR models would directly address this concern.

### 6. MAJOR: Biologically Questionable Initial Conditions

The optimal global result estimates `eta = 0.89`, which initializes approximately 72,489 individuals in the Recovered compartment at the start of the time series (February 24, 2020), before COVID-19 had meaningfully spread in the United States. The `rinit` code sets `R = nearbyint((1-eta)*N) - I`, so roughly 11% of the county population is modeled as already recovered from COVID-19 at pandemic onset. This is epidemiologically implausible and is not addressed in the write-up. The high `eta` may be compensating for model misspecification elsewhere rather than representing a real biological quantity.

### 7. MODERATE: `H` Accumulates Recoveries (`dN_IR`), Not New Infections

The process model accumulates `H += dN_IR`, meaning the observation model is `reports ~ rho * (new recoveries per week)`. In most COVID reporting contexts, positive test counts correspond to symptom onset or test administration (closer to `dN_EI` or `dN_SE`), not to recovery. Using recoveries as the basis for reported cases introduces a systematic lag (approximately `1/mu_IR` weeks) between the true epidemic curve and the model's fitted observations. The authors do not justify this modeling choice.

### 8. MODERATE: `wave == 2` Floating-Point Comparison in C Snippet Is Fragile

The `seirs_step` C snippet determines the transmission rate using the ternary expression:
```c
double Beta = (wave > 0) ? (wave==2) ? b3 : b2 : b1;
```
Since `wave` is a covariate subject to linear interpolation between integer time points (the covariate table defines `wave` only at integer `week_num` values, while Euler stepping uses `delta.t = 1/7`), intermediate values of `wave` can be non-integer (e.g., 1.5 at the midpoint between weeks 71 and 72). The exact equality `wave == 2` will only be true when the interpolated value equals exactly 2.0, meaning the transition from `b2` to `b3` is effectively discontinuous and dependent on floating-point precision. The same issue applies to the `rep_int` covariate in `dmeas` and `rmeas`. Using `wave >= 1.5` or `wave >= 2` as the threshold would be more robust.

### 9. MODERATE: Delta and Omicron Variants Lumped into a Single Transmission Rate `b3`

The third transmission rate `b3` covers July 2021 through March 2024, encompassing both the Delta (R0 ≈ 5–6) and Omicron (R0 ≈ 8–15) variants. These variants have substantially different transmission characteristics and produced distinct peaks in the data. Lumping them together forces a single `b3` to fit both the Delta wave (modest peak, fall 2021) and the massive Omicron peak (January 2022), likely degrading the model fit. The authors mention that `b3` is expected to be the largest transmission rate due to these variants but do not consider adding a fourth segment.

### 10. MODERATE: Global Search Convergence Diagnostics Reveal Widespread Failure

The effective sample size and conditional log-likelihood diagnostic plots (Figure `global-diag`) show systematic particle filter failures at multiple time points across the time series. The authors attribute these to holiday-season reporting anomalies, but provide no quantification of how many time steps fail or how this affects the likelihood estimates. Particle filter collapse leads to unreliable log-likelihood estimates via `logmeanexp`, and the associated Monte Carlo standard errors (some as high as 0.76 in the top results) are notably variable, suggesting the particle filter is not fully stable even at the reported optimum.

### 11. MODERATE: Only One Profile Likelihood Computed

The analysis computes a profile likelihood only for `rho3`. The other 12 free parameters — including the epidemiologically central transmission rates `b1`, `b2`, `b3` and the near-zero `mu_RS` — receive no profile analysis. Given the widespread evidence of weak identifiability in the pairs plots, profile likelihoods for at least the key parameters (`mu_RS`, `b3`, `eta`) are needed to properly characterize parameter uncertainty and assess which parameters are actually constrained by the data.

### 12. MINOR: Incorrect Beta Boundary Interpretation in Global Search

The authors state the global search `b3` range is `(0, 15)`, but the optimal result from the global search yields `b3 = 2.88` — well within bounds — while the profile likelihood box (constructed from only 6 rows, as noted above) shows `b3` ranging up to 4.07. The text description of the global search box and the actual computational box used for profile design are not the same due to the `head(6)` issue.

### 13. MINOR: AIC Table Anomaly Noted but Not Fully Explained

The authors identify "maximization failures" in the ARMA AIC table where AIC increases by more than 2 units when adding a parameter, but do not attempt to diagnose the cause (e.g., by inspecting the optimizer output codes, checking for near-unit-root behavior, or trying alternative optimizers). The warning `possible convergence problem: optim gave code = 1` produced when fitting ARMA(2,1) is suppressed and not mentioned in the write-up.

### 14. MINOR: Periodogram Interpretation Is Misleading

The AR periodogram shows maximum spectral density at frequency 0. The authors conclude there is "an absence of seasonality," but frequency 0 dominating simply reflects a strong trend or long-memory structure in the data — it does not preclude annual or semi-annual cycles. The absence of a clear secondary peak in the periodogram would be the relevant evidence for no seasonality, and the authors do not examine whether any sub-dominant peaks exist at biologically plausible frequencies (e.g., annual cycles at frequency ~0.019 cycles/week).

### 15. MINOR: `W` State Variable Serves No Functional Role

The `W` state variable, defined as a running accumulator of the Gamma white noise process (`W += (dw - dt)/sigmaSE`), is tracked throughout the simulation but is never used in the measurement model or referenced in any diagnostic analysis. While including `W` as an output for filtering diagnostics is sometimes done, it is not used for that purpose here. This adds unnecessary computational overhead and could cause confusion for readers attempting to understand the state space.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_seirs_global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_seirs_local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_rho3_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/mi_covid.xlsx`
