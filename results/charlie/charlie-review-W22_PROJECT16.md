# Peer Review: W22 Project 16
## "Modeling Covid 19 With Multivariate POMP Model"

---

## Summary

This project proposes two POMP compartment models — the *SIR-CDR* model (multivariate, measuring confirmed cases, deaths, and recoveries simultaneously) and the *SIR-D* model (univariate, measuring deaths only) — applied to daily Covid-19 data from Moscow through early 2021. The multivariate SIR-CDR model is novel in spirit, incorporating hospital capacity constraints and simultaneous measurement of three observables. However, neither model is successfully fitted: the SIR-CDR model is set to `eval=FALSE` and never executed, while the SIR-D model converges to biologically implausible parameter values (Mu_SyR ~157 per day) that the authors themselves identify as evidence of misspecification. The report is largely a negative result study presented without a working benchmark, without an IID comparison, without valid profile likelihoods, and with several code-level bugs that call the correctness of the implemented models into question.

---

## Major Issues

### 1. SIR-CDR model is never fitted — the primary claim of the paper is unsubstantiated

The entire SIR-CDR model code block (the model described as the main contribution) is set to `eval=FALSE, include=FALSE` and never executed. No particle filter runs, no likelihood evaluation, and no convergence diagnostics are produced for this model. The authors acknowledge difficulties but provide no results whatsoever for the model they describe as having "modeling advantages." A project cannot claim to propose and evaluate a model that is never run. This is the single most critical deficiency in the report.

### 2. Process model conservation violation in SIR-CDR rprocess (Code bug)

In the SIR-CDR `covid_step` Csnippet, the `Sy` compartment is updated twice in ways that are inconsistent. At line 231, `Sy` is updated as:

```
Sy += dN_SSy + dN_ASy - dN_SyR - dN_SyD;
```

This update already deducts `dN_SyH` transitions implicitly (it does not add them, so Sy is reduced by `dN_SyR + dN_SyD` but hospitalizations are not subtracted). Then the cap-enforcement block at lines 234-242 either truncates Sy or deducts `dN_SyH` again, leading to double-counting: Sy can be decremented by both the `- dN_SyR - dN_SyD` terms above and then additionally by `-(Sy + H - Cap)` in the cap block, which can produce a further inconsistency in the state count. Compartments do not sum to the population correctly through this sequence.

### 3. Process model bug: `dN_SyH` is declared but removed from the equation label in the written math

The mathematical equations (lines 168-169) list `dN_{SyH}` twice — once for hospitalization and once for death — both labeled `dN_{SyH}`. This duplicated label in the equations is a copy-paste error that obscures the model structure. One of these should be `dN_{SyD}`. This means the written model description does not match the implemented code, which is a reproducibility failure per Wheeler et al. (2024).

### 4. Profile likelihood is a slice, not a profile — confidence intervals are invalid (CC-Yes, Error 1.2)

The profile likelihood for Mu_SyR is constructed over the range [0.01, 0.95] (line 609), but the global search found the optimizer converges to Mu_SyR ~157 — a value 165x the upper bound of the profile range. The best loglik achieved in the profile is -1558.8, compared to the global MLE of -1171.7, a gap of approximately 387 log-units. This means the profile never reaches the MLE and is therefore a likelihood slice, not a true profile likelihood. The red Wilks threshold line drawn on this plot is meaningless: the profile is nowhere near the true maximum and no valid confidence interval can be extracted from it. Per the course reference (Error 1.2, CC-Yes), this is a major error that was explicitly taught and tested.

### 5. No comparison to any non-mechanistic benchmark (CC-Yes, Error 1.6)

Neither the SIR-D nor the SIR-CDR model is compared against any non-mechanistic benchmark — no ARIMA, no IID negative binomial, no regression model. The authors report a best log-likelihood of -1171.7 for the SIR-D model with no reference point. Without a benchmark, it is impossible to know whether this model performs better or worse than even a white-noise fit. This was explicitly tested in the course (Q11-01, CC-Yes) and is identified as a major weakness in Wheeler et al. (2024, §Model diagnostics).

### 6. No convergence diagnostics for iterated filtering (CC-Yes, Error 1.8)

The local search trace plots are produced but the authors do not discuss convergence of the log-likelihood panel. The text notes that "some of the simulations have difficulties optimizing the likelihood and quickly drop down to some very small values" but treats this as an observation rather than a convergence failure requiring investigation. The global search results show that out of 20 runs at run_level=2, only 18 returned finite likelihoods and the loglik distribution spans from -16,609 to -1,172 — a range of over 15,000 log-units — with a bimodal distribution (IQR: -14,559 to -1,174, indicating most runs fall into a deep non-converged basin). This is strong evidence that the global search did not converge and that the reported best-value MLE is not reliable.

### 7. Fixed parameters are not justified with sensitivity analysis

Several parameters are fixed without estimation: Alpha = 0.3, D_rate = 0.01, eta = 0.0002, N = 11,920,000. The Alpha = 0.3 asymptomatic rate is sourced from a study (reference [6]) but no sensitivity analysis is conducted. More critically, eta = 0.0002 is set to a rounded estimate from "the number of confirmed cases in day 1" with no uncertainty propagation. For a model that is already exhibiting misspecification signals, fixing these parameters may mask the true source of model failure. Per Wheeler et al. (2024, §Initial conditions), the choice of initialization strategy can substantially affect AIC.

### 8. SIR-D process model has a logical error in the clamping code

In the SIR-D `covid_step` Csnippet (lines 394-403), the clamping block for the case where `dN_SyD + dN_SyR > Sy` reads:

```c
Sy = 0;
R += nearbyint(Sy*(dN_SyR/(dN_SyD+dN_SyR)));
D += nearbyint(Sy*(dN_SyD/(dN_SyD+dN_SyR)));
```

After `Sy = 0`, the subsequent `nearbyint(Sy * ...)` expressions always evaluate to 0 regardless of the ratio. This means when the clamping condition is triggered, zero individuals are added to R or D, rather than the intended proportional allocation of the remaining Sy individuals. The correct implementation would have saved the old value of Sy before zeroing it out and used that saved value in the allocation. This is a silent C code bug that produces incorrect dynamics without any error message.

---

## Minor Issues

### 9. SIR-CDR dmeas sums log-likelihoods additively rather than multiplying densities

The SIR-CDR `covid_dmeas` Csnippet (line 208) computes:

```c
lik = dpois(deaths, D, 1) + dpois(confirmed, C, 1) + dpois(recovered, Rr, 1);
lik = (give_log) ? lik : exp(lik);
```

Summing log-likelihoods when `give_log=1` and then exponentiating when `give_log=0` is correct for the joint likelihood of three independent observations. However, the resulting `lik` when `give_log=0` would be `exp(sum of three log-densities) = product of three densities`, which is correct. But when the model is run in non-log mode (e.g., for particle filter resampling weights), this correctly returns the product density. This implementation is valid, though unconventional; it is only an issue if `dpois(..., 1)` returns values that can be extremely negative, causing numerical underflow when exponentiated.

### 10. D_rate is interpreted as a fixed "death rate" but is biologically conflated with a competing hazard

In the SIR-D model, `dN_SyD` is computed as `rbinom(Sy, 1-exp(-D_rate*Mu_SyR*dt))`, meaning the death rate is defined as a fraction of the symptomatic recovery rate (D_rate * Mu_SyR). When Mu_SyR is very large (as found in the optimization, ~157/day), the death rate per day approaches 1.57/day, which is greater than 1 and nonsensical. This parametrization ties death dynamics to recovery dynamics in an unconstrained way that breaks when Mu_SyR is large. This design choice is a contributing cause of the apparent misspecification.

### 11. Profile likelihood threshold uses incorrect reference loglik

The Wilks threshold on the profile plot (line 656) uses `max(global_results$loglik) - 0.5*qchisq(df=1, p=0.95)` as the reference. The reference loglik should be the unconstrained MLE, which the profile itself should achieve at its peak — not the global search maximum. In this case the profile never reaches the global MLE (the best profile point is 387 log-units below the global MLE), so the displayed threshold is entirely below the profile curve and has no interpretive value. The code draws the threshold at approximately -1174, but no profile point is anywhere near this value.

### 12. Run_level = 2 with only Nreps_profile = 4 and Npoints_profile = 10

At run_level=2, the profile uses only 10 points over Mu_SyR in [0.01, 0.95] with 4 replicate optimization starts per point. With the range restricted far from the MLE region, and so few replicates, this profile could not be reliable even if the range were correct. For a parameter that ultimately takes values around 157, profiling over [0.01, 0.95] with 10 points provides no information about the true profile shape.

### 13. No simulation-based diagnostics for SIR-D model relative to observed data

The forward simulation from the best parameters shows the model "failed to capture the general non-linear shape of the data" but no quantitative assessment of this failure is made. There is no conditional log-likelihood plot, no filtering ESS analysis, and no comparison between the simulated trajectories and the observed data beyond a visual plot of 5 simulated trajectories. Per Wheeler et al. (2024, §Model diagnostics), conditional log-likelihoods and filtering distributions are the appropriate diagnostic tools.

### 14. Misspelled "miss-specified" throughout

The word "misspecified" is consistently spelled "miss-specified" throughout the paper (e.g., lines 546, 553, 567, 663). This is a minor but persistent typographical error across multiple sections.

### 15. No sessionInfo() or package version documentation

There is no `sessionInfo()` output, no `renv` lockfile, and no documentation of the `pomp` package version used. As noted in the code supplement checklist, the `pomp` API has changed across versions and results may not reproduce on current CRAN releases. This is particularly relevant for a project that uses `stew`/`bake` caching, as the cached `.rds` files may not be readable across different R versions (as confirmed: the `local_search.rds` file returned "unknown input format" when read with a different R version).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project16/run_level_2/global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project16/run_level_2/Mu_SyR_prof.rds`
