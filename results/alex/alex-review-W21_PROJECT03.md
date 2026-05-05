# Peer Review: W21 Project 03 — Investigation of Vaccination Effect on Covid-19 in California

## Summary

This project fits a series of compartmental models (SIR, SIRV1, SIRV2) to California COVID-19 case data from January–April 2021 to evaluate vaccination effectiveness and forecast pandemic end date. The project has commendable structure and a clear research question, but contains several critical implementation bugs that undermine the validity of all results, as well as methodological and interpretive weaknesses that would prevent reliable scientific conclusions.

---

## Weaknesses (Prioritized by Severity)

### 1. [MAJOR] Accumulator H tracks removals (dN_IR), not new infections — fundamental model misspecification

In all three model step functions (SIR, SIRV1, SIRV2), the accumulator variable H is incremented by `dN_IR` (the stochastic flow from I to R, i.e., recoveries/removals):

```r
H <- H + dN_IR
```

The observed data `New_Report` is constructed as `diff(Confirmed)`, the daily increment in confirmed cases, which represents new infections (S → I transitions). H should accumulate `dN_SI` instead. As a result, the measurement model `New_Report ~ Binomial(H, rho)` links reported cases to removals rather than to new infections. This misspecification affects every model and every parameter estimate in the project.

---

### 2. [MAJOR] Prediction simulation uses initial-guess parameters instead of MLE parameters

In the prediction section, `params_maxlik` is correctly computed from the global search results:

```r
params_maxlik = unlist(results_global[which.max(results_global$loglik),])
```

However, the `simulate()` call immediately below uses the generic `params` variable (the hand-tuned initial guess, `Beta=0.01, Sigma=0.01, mu_IR=0.04, mu_VR=0.9, rho=0.3, eta=0.9`) rather than `params_maxlik`. The pandemic end-date conclusion is therefore based on arbitrary parameter values, not on the fitted model.

---

### 3. [MAJOR] SIRV1 step function: V→I transition hazard uses V instead of I

The SIRV1 ODE specifies the force of infection on vaccinated individuals as `sigma * beta * V(t) * I(t) / N`, giving a per-capita hazard of `sigma * beta * I / N` for each vaccinated person. The code implements:

```r
dN_VI <- rbinom(n=1,size=V,prob = 1-exp(-Sigma*Beta*V/N*delta.t))
```

The hazard uses `V` instead of `I`. This makes the effective infection rate of vaccinated individuals depend on the number of vaccinated people rather than on the number of infectious people, which is biologically incorrect and inconsistent with the stated model. SIRV2 correctly uses `I` in this hazard.

---

### 4. [MAJOR] SIRV1 step function: S→V transition hazard is density-dependent, inconsistent with ODE

The SIRV1 ODE specifies `dS/dt = -beta*S*I/N - u*S/N`, giving a per-capita vaccination hazard of `u/N` (a constant independent of S). The code implements:

```r
dN_SV <- rbinom(n=1,size=S,prob=1-exp(-u*S/N*delta.t))
```

The per-capita hazard is `u*S/N`, which is density-dependent and grows with S. This does not correspond to the stated ODE model. The correct hazard should be `u/N` (or simply `u` if `u` is interpreted as a per-capita rate).

---

### 5. [MAJOR] Run level is set to 1 throughout — results are computed with far too few particles and iterations

The entire analysis uses `run_level = 1`, giving `Np = 100`, `Nmif = 10`, `Neval = 2`, `Nglobal = 10`, and `Nlocal = 10`. These are exploration-grade settings, not production settings. The stored results files reflect this. With only 100 particles and 10 IF2 iterations, the likelihood estimates are highly unreliable, the parameter estimates have poor convergence, and the diagnostic plots (already noted as sparse and uninformative) cannot be trusted. Conclusions about vaccine efficacy and pandemic end dates drawn from these results are not statistically credible.

---

### 6. [MAJOR] Profile likelihood for sigma: Sigma is not held fixed in the first mif2 call

In the profile likelihood code, `mf1` inherits its random walk standard deviations from the SIRV2 local search, where `Sigma = 0.02` is specified in `rw.sd`. The profile for sigma should keep Sigma completely fixed during optimization. The code applies two `mif2` calls in sequence:

```r
mf1 %>%
  mif2(params=c(unlist(guess),fixed_params),cooling.fraction.50=0.3) %>%
  mif2(Nmif=options_Nmif, rw.sd = rw.sd(Beta=0.01,rho=0.02,eta=0.02,mu_IR=0.02,mu_VR=0.02)) -> mf
```

Only the second call omits Sigma from rw.sd; the first call (which inherits mf1's rw.sd) still perturbs Sigma. As a result, the profile values of Sigma reported in the plot may not reflect the intended fixed values.

---

### 7. [MAJOR] SIRV2 deterministic vaccination flow (dN_SV) can produce negative S without bounds check

In the SIRV2 step, the vaccination increment is computed deterministically:

```r
dN_SV <- round(sum(coef(fit)[c(2,3)] * c(delta.t,2*D*delta.t+delta.t^2)))
```

This is a fixed positive quantity independent of the current S. When S becomes small (late in the epidemic), subtracting `dN_SV` from S can drive S below zero, violating the non-negativity constraint required of a valid population compartment model. No clipping or bounding is applied.

---

### 8. [MODERATE] Local search likelihood evaluation uses only a single particle filter replication

For local search across all three models, the loglikelihood is evaluated as:

```r
mifs_local[[i]] %>% pfilter(Np = options_Np) %>% logLik() %>% logmeanexp() -> ll
```

This applies `logmeanexp()` to a single value, which is identical to that single value. The global search correctly uses `replicate(options_Neval, ...)` with `logmeanexp(se=TRUE)` for Monte Carlo averaging. The inconsistency means local search loglik estimates have higher variance and no associated standard error, making the local-vs-global comparison and the parameter estimates from local search unreliable.

---

### 9. [MODERATE] Confidence interval cutoff for sigma is computed but not plotted

The profile likelihood section computes the 95% confidence cutoff using Wilks' theorem:

```r
ci.cutoff <- maxloglik - 0.5*qchisq(df=1,p=0.95)
```

The corresponding horizontal reference line is commented out of the plot (`# + geom_hline(color="red",yintercept = ci.cutoff)`). The confidence interval boundaries for sigma are discussed in text but never formally presented. The claim that sigma is "weakly identifiable" is asserted without supporting visualization.

---

### 10. [MODERATE] Active cases used as I(0) conflates reported active with true infectious

The initial condition `I0 = round(df$Active[1]/1000)` sets I(0) to 2,728 thousand, derived from the reported `Active` column (confirmed cases not yet resolved). In reality, the true infectious population is unknown and may differ substantially from administrative "active case" counts, which depend on reporting completeness, lag times, and resolution criteria. This initial condition is treated as known and fixed throughout all models, without uncertainty propagation.

---

### 11. [MODERATE] Vaccine efficacy conclusion (">80%") is not supported by the analysis

The conclusion states "The vaccine is effective and protective against COVID-19. The vaccine efficacy is over 80% according to our analysis." However, the analysis only estimates sigma (breakthrough infection risk of vaccinated vs. unvaccinated), and notes that sigma is weakly identifiable. No formal confidence interval for sigma is presented, no formal hypothesis test is conducted, and the profile likelihood with all its implementation problems (see issues 5, 6) cannot support a precise efficacy claim. The "80%" figure is not derived or explained anywhere in the writeup.

---

### 12. [MODERATE] SIR model dismissed based on visual inspection of pair plots, not likelihood comparison

The SIR model is rejected because the pair plot "does not give us a clear picture or hint of the ridge in the likelihood surface." No formal likelihood ratio test or AIC/BIC comparison is performed between SIR and SIRV models. Given that the SIR and SIRV models have different numbers of parameters, a proper model comparison requires accounting for degrees of freedom.

---

### 13. [MINOR] Vaccination data modeled by regression fitted to the same data used in the POMP model

The vaccination rate enters SIRV2 as a fixed, externally-estimated quadratic function of time, fitted by OLS (`fit = lm(People_Fully_Vaccinated ~ Day + Day2, data=df)`). This regression uses the same 87 observations that form the POMP analysis dataset. The vaccination schedule is then treated as deterministic and known within the POMP model, ignoring uncertainty in the regression estimates. Furthermore, projecting a quadratic vaccination trend far beyond the observation period (to day 210) is not justified.

---

### 14. [MINOR] Prediction plots show only 5 simulations, claim says 10

The prediction section states "All the simulations were repeated 10 times," but the code uses `nsim=5`. This discrepancy between the stated and actual number of simulations indicates the code or text was not synchronized before submission.

---

### 15. [MINOR] Global search for SIRV1 uses a filter threshold of loglik > max(loglik) - 1000, which is too wide

In the SIRV1 global search pair plot:

```r
pairs(~loglik+Beta+rho+eta+mu_IR+u+Sigma, data = results %>% filter(loglik > max(loglik)-1000))
```

A threshold of 1000 log-likelihood units below the maximum retains virtually all points regardless of fit quality. The SIR and SIRV2 global pair plots use a threshold of 20 units, which is the standard practice. This inconsistency means the SIRV1 pair plot includes low-likelihood noise points and cannot be interpreted as showing the likelihood surface near the MLE.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/Data/covid_data.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/Makefile`
