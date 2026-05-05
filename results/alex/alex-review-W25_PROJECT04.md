# Peer Review: W25 Project 04 — COVID-19 in Kerala, India (SEIRS POMP Model)

## Summary

This project applies ARIMA, VAR, and SEIRS POMP models to weekly COVID-19 confirmed case data from Kerala, India (February 2020 – May 2022). The authors motivate a SEIRS model with time-varying transmission rates (β), dispersion parameters (k), and reporting rates (ρ) to capture three distinct epidemic phases. Two global search candidates are presented, and profile likelihoods are computed for several key parameters. The scope is ambitious and the iterative model development is clearly narrated, but the project contains a critical implementation error that fundamentally invalidates the SEIRS dynamics across all model variants.

---

## Weaknesses

### 1. (Critical) R Compartment Update is Missing the dN_RS Outflow — Population is Not Conserved

In every SEIRS C snippet (`seir_step`) across the main model, the appendix models, and all auxiliary R scripts, the recovered compartment is updated as:

```c
R += dN_IR;
```

The correct SEIRS update must be:

```c
R += dN_IR - dN_RS;
```

The transition `dN_RS` is computed correctly (line 785: `double dN_RS = rbinom(R, 1 - exp(-mu_RS*dt));`) and correctly added back to S (line 787: `S -= dN_SE - dN_RS`), but it is never subtracted from R. As a result, individuals flow from R to S (S grows) while R is never depleted — R also grows monotonically. The total population N = S+E+I+R increases by `dN_RS` at every Euler step, violating mass conservation. This bug appears in all four model variants: `seirs_const`, `seirs_varying_k`, `seirs_varying_k_rho` (the main model), and `seirs_global2`. The "SEIRS" dynamics the authors describe and justify throughout the paper — waning immunity, re-infections, multi-wave behavior — are not actually implemented. All results, log-likelihood values, parameter estimates, and simulations from the SEIRS models are produced under a broken model that behaves differently from what is described.

### 2. (Major) H Accumulates Recoveries (dN_IR) Rather Than New Infections — Observation Model Is Mis-specified

The accumulator variable H is defined as `H += dN_IR`, meaning H counts cumulative I→R transitions (recoveries) over each observation interval. The observation model then models confirmed cases as `Y(t) ~ NegBinom(ρ * H, ...)`. Confirmed case counts in an epidemiological surveillance system represent newly detected infections (S→E or E→I transitions), not recoveries. Accumulating recoveries introduces a systematic lag and conflation: during the rising phase of an outbreak, recoveries lag behind new infections; during the declining phase, recoveries exceed new detections. The authors provide no justification for using dN_IR rather than dN_EI (new infectious cases) as the basis for H. This choice is particularly consequential for multi-wave dynamics where the lag structure differs across waves.

### 3. (Major) Typographical Error in Piecewise Parameter Definition Creates an Overlapping and Undefined Interval

The writeup defines the third period for β(t), k(t), and ρ(t) as `t ∈ [63, 119]`, while the second period is `t ∈ [62, 96]`. This implies the intervals overlap (weeks 63–96 belong to both periods 2 and 3), and week 97 through 119 are covered only by the third interval but the notation has the third interval starting at week 63. The actual implementation uses `interval = c(61, 35, 23)`, so the three intervals are weeks 1–61, 62–96, and 97–119 respectively. The stated third-period lower bound should be 97, not 63. This is not a computational error (the code is correct), but the mathematical description in the text is internally inconsistent and misleading.

### 4. (Major) Profile Likelihood Computation for Eta Omits mu_IR from the Random Walk, Freezing a Key Nuisance Parameter

In `Eta_pro.R`, the profile for η is computed using:

```r
rw_sd(b1=0.01, b2=0.02, b3=0.02, k1=0.01, k2=0.02, k3=0.02,
      rho1=.02, rho2=.02, rho3=.02, mu_EI=0.005, mu_RS=0.00)
```

`mu_IR` is absent from the rw.sd specification, which means it receives no random walk perturbation and is held fixed at whatever value the starting guess carries. A profile likelihood requires maximizing over all nuisance parameters at each fixed value of the profiled parameter. Freezing `mu_IR` — which the authors themselves identify as a poorly identified parameter with multiple potential optima — produces a profile for η that does not represent the true marginal likelihood. The resulting CIs for η are therefore unreliable.

### 5. (Major) AIC Comparison Between ARIMA and SEIRS Models Is Methodologically Invalid

In the Conclusion section, the ARIMA(5,1,5) AIC is compared directly to AIC values computed for the SEIRS models. These AIC values are not comparable because: (a) the log-likelihoods are on different scales — the ARIMA log-likelihood is a Gaussian approximation to the likelihood of the observed data, while the SEIRS log-likelihood is a particle filter estimate of the exact model likelihood under a negative binomial observation model; (b) the SEIRS log-likelihood is a Monte Carlo estimate with stochastic error, not a fixed quantity. While the text acknowledges the VAR model's incomparability due to multivariate data, it treats the ARIMA vs. SEIRS comparison as valid despite the model class distinction. A proper comparison would either use a common observation model or focus only on residual diagnostics and forecast quality.

### 6. (Major) Time Series Objects Specified with Incorrect Frequency

All time series objects in the EDA and ARIMA sections are created with `frequency=7`:

```r
confirmed.ts <- ts(data = weekly_df$Confirmed, start = c(2020, 1), frequency = 7)
```

For weekly data, `frequency=7` implies that a "season" consists of 7 weekly observations (roughly 7 weeks), which is not the appropriate frequency setting. Weekly data aggregated over years should use `frequency=52` if annual seasonality is to be modeled, or `frequency=1` if no seasonality is assumed. While this does not affect the ARIMA estimation itself (since the data argument is treated as a numeric sequence), it produces incorrect time axis labeling and affects the interpretation of the ACF/PACF lag scale. The EDA conclusions about seasonality drawn from these plots rely on this misspecification.

### 7. (Moderate) VAR Lag Selection Discards Information Criteria Recommendations Without Adequate Justification

The authors report that most information criteria suggest a lag around 20, but manually select `p=9` to "balance complexity and overfitting risk." No formal justification (e.g., Akaike weights, cross-validation, or residual tests at multiple lags) is provided for why 9 is a better choice than, say, 10 or the IC-optimal 20. With only 119 weekly observations and 3 variables, a VAR(9) model already estimates 9 × 3 × 3 + 3 = 84 parameters, consuming most of the sample. The choice of p=9 appears arbitrary without a more systematic justification.

### 8. (Moderate) VAR Log-Likelihood Computed via an Approximation That Does Not Match True ML

The log-likelihood is manually computed as:

```r
log_likelihood_manual <- -(n_obs*k/2)*log(2*pi) - (n_obs/2)*log(det(Sigma_u)) - (n_obs*k/2)
```

The last term `-(n_obs*k/2)` corresponds to `-(1/2) * tr(Sigma_u^{-1} * Sigma_u * n_obs)`, which evaluates to `-(n_obs*k/2)` only when using a plug-in (not ML) estimate — and even then this is the concentrated log-likelihood at the plug-in Sigma. The `vars` package provides a `logLik` method that returns the correct value; the stated reason that "a constant term prevented direct extraction" is not a valid technical explanation for using a manual formula. The manual computation may not equal the true ML log-likelihood.

### 9. (Moderate) mu_RS Fixed at 0.005 (200-Week Immunity) Without Epidemiological Basis, and Justification Is Circular

The authors acknowledge that `mu_RS = 0.005` implies a 200-week (approximately 4-year) immunity period, which they state is "generally too large." The sole justification given is that increasing `mu_RS` causes numerical instability and worse search results. This is a form of circular reasoning: the parameter is fixed at a value not because it is epidemiologically justified but because the model fails when it is varied. The instability itself may be a symptom of the R compartment bug (Issue 1), since a properly implemented SEIRS would have a well-defined steady state that is more numerically stable under variation in `mu_RS`. The fix-and-ignore approach prevents the model from capturing realistic waning immunity timescales (estimated 6–12 months for COVID-19).

### 10. (Moderate) Profile Likelihood CIs Computed Using Inconsistent Filtering Thresholds

For each profile, the threshold for the confidence interval is computed using:

```r
max(profile_results$loglik) - 0.5 * qchisq(df=1, p=0.95)
```

where `max(profile_results$loglik)` is from the full (unfiltered) results, but the plot uses only points filtered by `loglik.se < 1`. The CI is then computed by filtering the full (unfiltered) data against this threshold. This means the CI boundary can include points with high Monte Carlo standard error (SE > 1), potentially including unreliable estimates. A consistent approach would apply the same `loglik.se < 1` filter to both the threshold computation and the CI extraction.

### 11. (Moderate) Initial State I = 1000 Fixed Regardless of Epidemic Phase and Scale — Not Justified

The rinit snippet sets `I = 1000` as a hardcoded constant for all models. With Kerala's population of 34.5 million, setting I_0 = 1000 (a ~0.003% infection prevalence) is an ad hoc choice with no epidemiological justification, no sensitivity analysis, and no attempt to estimate this initial condition as a free parameter. The initial number of infectious individuals can substantially affect filter degeneracy during the early outbreak period (weeks 1–30), which the authors themselves observe as an ESS collapse near zero in the initial guess diagnostic.

### 12. (Moderate) ARIMA(5,1,5) Selected Without Checking for Near-Cancellation of AR and MA Roots

The authors note that some MA inverse roots lie near the unit circle (stability check section), which indicates near-unit-root behavior. For an ARIMA(5,1,5) model, AR and MA roots that nearly cancel each other produce parameter redundancy and inflated standard errors. The writeup does not check whether the AR and MA polynomials share nearly common roots — a standard diagnostic for over-parameterized ARIMA models. The model could be substantially reduced in complexity if near-cancellation is present.

### 13. (Minor) Figure References Are Internally Inconsistent

The code chunk labeled `fig4` (the ARIMA fitted vs. actual plot) is described in the subsequent text as "Figure 5," and the chunk labeled `fig5` (model diagnostics) is referenced in text as "Figure 5" as well. There is a systematic offset between the chunk label numbering and the text references for at least Figures 4–6, creating confusion when cross-referencing.

### 14. (Minor) Global Search for SEIRS_Candidate2 (seirs_global2) Does Not Specify a Latin Hypercube or Random Design — Starting Points Are Drawn From a Previous Profile

The second global search (`Global_Rho.R` in `seirs_global2`) does not use a fresh `runif_design`; instead, it uses the locally optimal starting point from a previous profile and reruns the local search. This means Global Search 2 is effectively a local search initialized from a particular point in parameter space rather than a systematic coverage of the global space. The claim that this constitutes a "Global Search 2" is therefore overstated, and the improvement in log-likelihood may simply reflect a better local neighborhood rather than genuinely different global exploration.

### 15. (Minor) The Negative Binomial Observation Formula in the Text Uses an Unusual Parameterization Without Clarification

The text writes `Y(t) ~ NegBinom(ρ*H, ρ*H + (ρH)²/k(t))`, using a (mean, variance) parameterization. The code uses `dnbinom_mu(reports, k, mean_reports, give_log)` which in R corresponds to `size=k, mu=mean_reports`. While the formula is mathematically consistent with R's implementation, this non-standard parameterization style (mean, variance) is unusual in epidemiological POMP modeling (where NegBinom is typically specified by mean and overdispersion), and no clarification is provided that the second argument in the formula is the variance, not a probability or size parameter.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/data/weekly_df.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/results/seirs_varying_k_rho/seirs_k_rho.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/results/seirs_varying_k_rho/Global_Rho.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/results/seirs_varying_k_rho/Eta_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/results/seirs_varying_k_rho/muir_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/results/seirs_varying_k_rho/Rho3_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/results/seirs_global2/seirs_k_rho.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project04/Makefile`
