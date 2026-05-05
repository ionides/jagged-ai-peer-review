# Peer Review: W22 Project 19
## An Analysis of the Omicron variant of COVID-19 Cases in Wayne County

---

## Summary

This project analyzes daily confirmed COVID-19 Omicron variant cases in Wayne County, Michigan from December 2021 through March 2022 using two modeling approaches: an ARIMA(4,1,4) model and a stochastic SEIR model fitted via iterated filtering (mif2) in the `pomp` package. The authors identify a 7-day reporting cycle via spectral analysis, build an SEIR model with a time-varying transmission rate to account for the transition from pre-Omicron to Omicron dynamics, and conduct local and global searches followed by a profile likelihood for the overdispersion parameter τ. While the project demonstrates competent use of the `pomp` workflow and correctly applies logmeanexp for likelihood aggregation, several serious methodological problems undermine the validity of the conclusions: the epidemiological parameters μ_EI and μ_IR are fixed rather than estimated, the profile likelihood for τ is based on only a few points above the Wilks threshold making the confidence interval unreliable, the H accumulator is not reset between observations (a structural accumvar error), the ARIMA–SEIR log-likelihood comparison is made on different observation models without justification, and the global search reveals that β₁ > β₂ at the MLE — a finding that contradicts the stated model motivation but receives only superficial discussion.

---

## Major Issues

### 1. Accumvar H is never reset — measurement model uses a cumulative rather than incident count

The state variable `H` is declared as an `accumvar`, which in `pomp` means it should be reset to zero after each observation. However, examining `dmeas` and `rmeas`, both use `H` directly as the expected count: `mean = rho*H`. An `accumvar` is supposed to accumulate new-recovery transitions `dN_IR` between observations and then be zeroed after measurement, giving the number of new recoveries (i.e., incident cases) per day. If H is never explicitly reset (the code does not include a line `H = 0` at the end of `seir_step`), then by the end of the simulation H holds the total cumulative count of individuals who ever moved from I to R, not the daily count. In `pomp`, the reset of accumvars is performed automatically at each observation time — but this is only automatic if the variable is correctly declared and the `rprocess` does not reinitialize it. A review of the C snippet confirms that `H += dN_IR` is the only line touching H, and there is no `H = 0` after the measurement step. This means H is cumulative, and `rho*H` grows without bound, making the measurement model nonsensical by the end of the observation window. This is a structural bug that invalidates all likelihood values computed and all subsequent inference. [Wheeler et al. 2024, §Model specification; pomp-accumvar-semantic-audit]

### 2. Epidemiological parameters μ_EI and μ_IR are fixed, not estimated — identifiability not assessed

The authors fix `mu_EI = 0.1` and `mu_IR = 0.08` throughout all searches (line `fixed_params <- params[c("N", "mu_EI", "mu_IR")]`), citing CDC guidance for the incubation and infectious periods. While fixing parameters based on prior information can be defensible, the paper provides no profile likelihood or sensitivity analysis for these values, and no discussion of the effect of this restriction on the remaining parameters. Given that the data span is only 121 days and several parameters are already weakly identified (evidenced by the scatter in the pairs plots), the effect of fixing μ_EI and μ_IR on the estimation of β₁, β₂, ρ, τ, and η is not assessed. In particular, `mu_IR` controls how long individuals remain infectious and is directly confounded with β; fixing it without uncertainty propagation makes all reported confidence intervals on other parameters narrower than they should be. [Wheeler et al. 2024, §Parameter identifiability and uncertainty; Skill Error 1.2]

### 3. Profile likelihood for τ has only two points above the Wilks threshold — confidence interval is unreliable

The authors report a 95% confidence interval for τ of [0.669, 0.706] but acknowledge in the text that "only two points are above the threshold resulting in dubious interval." A profile likelihood requires enough points above the Wilks threshold (max loglik − 1.92 for 95% CI) to clearly identify both endpoints. With only two points above the threshold, the endpoints are determined entirely by the positions of those two points and a single point below the threshold on each side; the CI boundaries are thus dominated by the grid spacing, not by the shape of the profile. This is consistent with Error 1.9 in the weakness reference (profile likelihood too sparse to identify the maximum). The authors correctly note the problem but do not attempt to remedy it (e.g., by adding more grid points around τ ≈ 0.68–0.71). As a result, the CI should not be reported as a reliable inferential product. [531-weakness-reference Error 1.9; Wheeler et al. 2024, §Parameter identifiability]

### 4. Global search reveals β₂ < β₁ at the MLE, directly contradicting the model motivation — not adequately addressed

The model is explicitly motivated by the claim that the Omicron variant has a higher transmission rate than earlier strains, operationalized by setting β₂ > β₁ for the Omicron-dominant period. However, the global search MLE has β₂ < β₁ (specifically: β₂ ≈ 4.0, β₁ ≈ 6.8 from the top results table). The authors acknowledge this ("the global search results in β₂ < β₁, indicating that the Omicron variant isn't contagious as expected") but dismiss it as an unexpected finding without further investigation. This contradicts a core modeling assumption and raises the possibility that (a) the change-point at day 17 is misspecified, (b) the overall model structure is misspecified, or (c) the data do not support the two-β parameterization. The correct response is to test the constraint β₂ > β₁ via a likelihood ratio test against the unconstrained model, or to reconsider the change-point date. Instead, the paper treats this as a curiosity. [Wheeler et al. 2024, §Model variations and nested comparisons]

### 5. ARIMA and SEIR log-likelihoods are compared without accounting for differences in the observation model

The model comparison table reports ARIMA log-likelihood = −618.74 and SEIR log-likelihood = −861.13 and concludes the ARIMA model is better. However, ARIMA models the differenced series (in this code, `arima(data_wayne1$case, order=c(4,1,4))` uses the original series with d=1 internally, so the likelihood is for the differenced observations), while the SEIR model's likelihood is computed on the raw daily counts. These are likelihoods for different observation vectors and cannot be directly compared without adjustment. Furthermore, the ARIMA model uses a Gaussian measurement model while the SEIR uses a truncated normal, adding another incompatibility. The authors acknowledge the performance gap but attribute it solely to the SEIR model's failure to capture the 7-day cycle, without recognizing the fundamental problem with the comparison itself. Per 531-conventions.md, likelihoods from different model classes ARE comparable for the same data — but only when both likelihoods are evaluated on the same observed data vector. Here the ARIMA likelihood is for differences while the SEIR likelihood is for levels, making the comparison invalid. [531-conventions.md §Model comparison; 531-weakness-reference Error 2.2]

### 6. Missing convergence diagnostics for the global search — no evidence the MLE was reached

The global search runs 500 starting points through multiple mif2 stages, but the only convergence evidence presented is the pairs plots (starting points vs. filtered estimates). No likelihood trace plots are shown for the global search, and no comparison of terminal log-likelihoods across runs is presented for the global search. The local search trace plots show high variance (likelihoods range from approximately −1200 to −900 across runs), with one run reaching below −900 while most saturate near −1000. This spread suggests the optimization landscape is complex and convergence to the global maximum is not assured. Without showing that multiple global search runs terminate at similar likelihoods (e.g., a histogram of terminal log-likelihoods or a scatter of loglik vs. parameters restricted to the top runs), there is no evidence the reported MLE of −861 is a reliable global maximum. [531-weakness-reference Error 1.8; Wheeler et al. 2024, §Computational adequacy]

---

## Minor Issues

### 7. rw.sd settings are inconsistent with the parameter transformations used

The code applies `log` transforms to `beta1`, `beta2`, `mu_EI`, `mu_IR`, and `tau`, and `logit` transforms to `rho` and `eta`. The standard course perturbation on a transformed scale is rw.sd ≈ 0.02. However, the code sets `rw.sd(beta1=0.05, beta2=0.05, rho=0.04, tau=0.01, eta=ivp(0.02))`. The τ perturbation of 0.01 on the log scale is substantially smaller than the course standard and may cause underdispersion in the τ search. Additionally, since mu_EI and mu_IR are fixed, their rw.sd entries are irrelevant but were originally included in `params_rw.sd`; the profile search creates a separate `rw.sd_tau_fixed` object with `tau=0.0`, which is correct, but the inconsistency between the two rw.sd specifications is not discussed.

### 8. The spectral analysis misidentifies the dominant period

The authors report that the smoothed periodogram peak frequency is computed as `smooth_spec$freq[which.max(smooth_spec$spec)]` and interpret this as a "90-day cycle." With 121 daily observations, the lowest non-zero frequency in the periodogram is approximately 1/121 cycles per day, corresponding to a period of ~121 days — not 90. A frequency near 1/90 would only correspond to a 90-day period if the dominant spectral peak were at that frequency. The code simply takes the maximum of the smoothed spectrum without checking the actual frequency value. Furthermore, the paper then hardcodes `smooth_spec$freq[13]` to extract the 7-day frequency rather than using `which` to find the peak near 1/7, which is not reproducible if the smoothing span or data length changes. [531-weakness-reference Error 2.8]

### 9. Initial conditions E = 6000 and I = 15000 are fixed without justification or sensitivity analysis

The initialization sets `E = 6000` and `I = 15000` as hard-coded constants regardless of N, rather than expressing them as fractions of the population or estimating them. The course standard is to either estimate initial infected fractions as parameters or to justify fixed values. With N ≈ 1.73 million, 15,000 initially infectious individuals represents a prevalence of ~0.87%, which is not motivated by any cited epidemiological source. No sensitivity analysis is performed to assess whether conclusions change under alternative initial conditions.

### 10. The measurement model notation contains an apparent ambiguity — H is used for both the latent variable and the observation formula

In the dmeas/rmeas specification, `H` appears in the formula `mean = rho*H`. The text describes the measurement model as: "H = max(⌊H_n⌋, 0), H_n ~ N(ρH_n, (τH_n)² + ρH_n)". This notation reuses H for both the latent accumulator and the measurement variable (the floor operation on the right-hand side). This ambiguity makes it unclear whether the authors intend the mean to be ρ times the latent H (the accumvar) or ρ times the expected observation. The actual `dmeas` code uses `H` (the accumvar) directly, which is consistent with the former interpretation, but the mathematical notation does not make this clear.

### 11. The ARIMA model selection criterion is applied mechanically — the chosen ARIMA(4,1,4) is large and near-cancelling roots are noted but not resolved

The AIC table selects ARIMA(4,1,4) because it has the lowest AIC among models with p,q ≤ 4. The authors correctly note that the inverse AR and MA roots lie near the unit circle, which suggests near-cancellation. Near-cancelling AR-MA roots indicate model redundancy and often result in poorly identified coefficients. The authors state "we stick to ARIMA(4,1,4) model for the time being" without attempting a simpler model or investigating whether smaller AR or MA orders achieve similar AIC with better-behaved roots. Additionally, the AIC table is not displayed in the review (only the code is shown), making it impossible to verify the selection. [531-conventions.md §ACF residual diagnostics]

### 12. Residual non-normality is noted but not acted upon

The QQ-plot and Shapiro-Wilk test (p << 0.05) both indicate non-normal residuals for ARIMA(4,1,4). The authors acknowledge this but do not attempt a transformation (e.g., log or square root of the case counts) or consider an alternative model (e.g., ARIMA on log-transformed counts). For count data with potential overdispersion, applying Gaussian ARIMA to raw counts and then noting normality failure without remediation is a known weakness. [531-weakness-reference Error 2.5]

### 13. No non-mechanistic benchmark comparison for the SEIR model

The paper compares ARIMA to SEIR but does not provide an IID negative binomial or Poisson baseline log-likelihood, which would be the weakest meaningful benchmark for the POMP model. The SEIR log-likelihood of −861 is substantially below the ARIMA log-likelihood of −619. Knowing where an IID fit sits would help determine whether the SEIR model at least captures more structure than complete independence across days. The benchmark comparison also helps diagnose whether the poor SEIR performance (relative to ARIMA) reflects model misspecification or just the absence of day-of-week effects. [Wheeler et al. 2024, §Benchmark comparison; 531-weakness-reference Error 1.6]

### 14. The profile likelihood starting points are drawn by rounding τ from global search results — this may create a non-uniform grid

The profile is constructed by grouping global search results by `round(tau, 2)` and selecting the best-likelihood row from each group. This means the τ grid is not pre-specified but is determined by wherever the global search happened to place points. In regions of the parameter space not well-explored by the global search, there may be no starting points for the profile, creating gaps. The conventional approach (and the course standard) is to specify an explicit τ grid and use global search results only as warm starts. The authors do not check whether the τ grid covers the full plausible range or whether there are gaps below the Wilks threshold. [531-conventions.md §POMP: profile likelihood; Wheeler et al. 2024, §Parameter identifiability]

### 15. The data subsetting code has an inconsistency — the subset end date differs between text and code

The introduction states the analysis covers "12/01/2021 to 03/31/2022" (121 days), but the subsetting code `data_wayne[data_wayne$date >= '2021-12-01' & data_wayne$date <= '2022-02-28',]` uses an end date of 2022-02-28. February 28, 2022 to December 1, 2021 is only 89 days, not 121. The spectrum analysis then notes "we only have 121 data," suggesting the covariate table `covid_wayne_winter.csv` may use the correct 121-day window while the exploratory analysis uses a different (shorter) subset. This discrepancy means the ARIMA model and the SEIR model may be fitted to different data, making the log-likelihood comparison even less valid than discussed in Issue 5.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project19/blinded.Rmd`
