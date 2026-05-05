# Peer Review: W24 Project 08
## King County COVID-19 Weekly Cases Analysis (SEIR / SVEIPR POMP Models)

---

### Summary

This project analyzes weekly COVID-19 confirmed-case counts in King County, Washington (January 2020 - March 2023) using an ARIMA benchmark and two progressively more complex compartmental POMP models: a standard SEIR and a custom SVEIPR (Susceptible-Vaccinated-Exposed-Infected-Potentially-infected-Recovered). The project shows genuine ambition in extending the SEIR baseline with vaccination, asymptomatic infection, and time-varying transmission rates. However, it contains a critical data-contamination bug, several code errors with direct epidemiological consequences, a systematic double-differencing error in the ARIMA section, and inadequate model evaluation. These issues substantially undermine the validity of the reported results.

---

## Weaknesses (prioritized by severity)

### 1. MAJOR: SEIR Section Fitted to Wrong Data (Washtenaw County, Michigan)

In the SEIR section (line 177 of `blinded.Rmd`), the code that is supposed to reload King County data instead reads:

```r
sea_data = full_data |> filter(Admin2 == "Washtenaw", Province_State == "Michigan")
```

This silently overwrites `sea_df` with Washtenaw County, Michigan data. All subsequent SEIR computations -- the initial simulation, the local search (saved to `local_search.rds` and `local_logliks.rds`), and the global search (saved to `seir_global.rds`) -- are therefore performed on Washtenaw County data rather than King County data. The SVEIPR section later uses `rm(list=ls())` and correctly reloads King County data. Consequently, the SEIR and SVEIPR models are estimated on entirely different datasets, making any cross-model comparison invalid. The loglikelihood values reported for SEIR (best: -1194.489) and SVEIPR (best: -1376.675) are incommensurable.

---

### 2. MAJOR: SVEIPR Has Strictly Worse Log-Likelihood Than SEIR, With No Discussion

The SEIR global search achieves a best log-likelihood of -1194.489; the more complex SVEIPR model's global search achieves -1376.675 -- approximately 182 log-likelihood units worse. Even accounting for the data-contamination bug above, the paper presents SVEIPR as a clear improvement over SEIR without acknowledging that its objective function value is dramatically lower. Given SVEIPR has roughly 19 estimated parameters versus SEIR's 6, a penalty-based comparison (AIC, likelihood ratio, etc.) would make the deterioration even starker. This is never mentioned in the conclusion, which instead states the SVEIPR "gives a well simulation outcome."

---

### 3. MAJOR: Double Differencing in ARIMA Section

The variable `sea_df$cases` is constructed as `diff(weekly_cumulative_counts)` -- it is already first-differenced. The AIC table function then calls `arima(data, order=c(p,1,q))`, applying a second difference. Every model in the table (and the selected ARIMA(3,1,3)) therefore applies two differences to data that needed only one. The model described in the text as "ARIMA(3,1,3)" is actually ARIMA(3,2,3) relative to the original weekly cumulative series. The stated motivation -- that one round of differencing produces stationarity -- is correct for `sea_df`, meaning the correct model class to apply was ARMA(p,q) (i.e., `d=0`), not ARIMA(p,1,q).

---

### 4. MAJOR: Bug in SVEIPR Reinfection Transition -- Wrong Compartment

In `sepir_step`, the reinfection flow from R back to S is drawn as:

```c
double dN_RS = rbinom(I, 1 - exp(-mu_RS * dt));
```

The first argument to `rbinom` should be `R` (the recovered compartment), not `I` (the infected compartment). As written, the transition subtracts individuals from I and adds them back to S, rather than moving recovered individuals back to susceptibility. This corrupts the state dynamics throughout the simulation and invalidates the reinfection mechanism that is one of the SVEIPR model's primary innovations.

---

### 5. MAJOR: Euler Step Size Too Coarse in SVEIPR

The SEIR model uses `euler(sir_step, delta.t=1/7)` (daily sub-steps), while the SVEIPR model uses `euler(sepir_step, delta.t=1)` (one step per week). For rate parameters as large as `mu_EPI ~ 1.3/week` or `mu_IR=0.98/week`, a weekly Euler step introduces substantial discretization error. The Euler approximation is only accurate when transition probabilities are small; at `mu_EPI=1.3`, the exact discrete-time probability is `1-exp(-1.3) ≈ 0.73` per step -- far from the infinitesimal limit. The change in step size is not discussed or justified, and the resulting numerical inaccuracy undermines the validity of SVEIPR parameter estimates.

---

### 6. MAJOR: SVEIPR Log-Likelihood Comparison Is Internally Inconsistent

The text states local search best log-likelihood is -1397 and global search best is -1377. Examination of the stored results confirms local best is -1396.783 and global best is -1376.675. While the directional comparison is correct (global slightly improves on local), the text also states "we fail to get a significantly better result in global search" -- yet the improvement is about 20 log-likelihood units. At the same time, the paper never applies a likelihood ratio test or information criterion between SEIR and SVEIPR, and does not compute profile likelihoods as promised (see Issue 10).

---

### 7. MODERATE: Observation Accumulator H Only Counts Symptomatic Transitions

The SVEIPR model introduces compartment P (potentially infected / asymptomatic). The accumulator `H` is updated only with `H += dN_IR` (symptomatic-to-recovered transitions), not with `dN_PR` (asymptomatic-to-recovered). The measurement model links observed cases to `rho * H`. If P represents asymptomatic or pre-symptomatic infections that eventually recover, their path through the epidemic is entirely invisible to the likelihood. This creates a structural confound: `alpha` (the fraction routed through P) is effectively unidentifiable from `rho`, since increasing `alpha` reduces H and the effect can be compensated by increasing `rho`. The consequence is that the "potentially infected" compartment adds model parameters without contributing any information.

---

### 8. MODERATE: Vaccine Uptake Multiplier c4 Takes Epidemiologically Implausible Values

In global search results, the best-fit c4 values (multiplier on `mu_SV` during weeks 76-97) reach 207, 286, and 316. With `mu_SV=0.5`, the effective vaccination rate becomes `mu_SV_intervention * (I+P)/N ≈ 143/week * (I+P)/N`. This is not a recognizable per-capita weekly transition rate; it suggests the optimizer is exploiting numerical artifacts rather than identifying a meaningful vaccination process. The parameter `c4` (and similarly `c5`) are effectively unbounded from above in the fitting, which indicates a lack of biological constraint on the vaccination compartment dynamics.

---

### 9. MODERATE: SEIR ARMA Model Poorly Identified -- Extreme Parameter Values in Global Search

The SEIR global search (operating on Washtenaw data) returns beta values spanning from 0.16 to 114,712 across particles, with many returning NaN log-likelihoods (67 out of 100). The top-2 best results include Beta=1159 and Beta=3087 with near-zero mu_IR and mu_EI. These are biologically absurd (effective reproduction numbers in the thousands), yet they achieve log-likelihoods similar to epidemiologically reasonable parameter sets. This suggests the SEIR likelihood surface for this dataset is extremely flat and the model is not well-identified. No profile likelihood or Monte Carlo standard errors are computed to quantify identifiability, and the issue is not discussed.

---

### 10. MODERATE: Claimed "Poor Man's Profile Likelihood" CIs Are Not Actually Computed

The text states: "If we construct poor man's profile likelihood confidence interval, we can find that gamma ∈ (0.806, 0.988), eta ∈ (0.816, 0.979)." These are reported as confidence intervals but are actually just the range of global search results filtered to log-likelihood within some unspecified threshold. No filtering threshold is shown, no confidence level is stated, and no code is present to construct these intervals. The method is described informally but never implemented correctly; it should use results within 1.92 log-likelihood units of the maximum to approximate 95% intervals.

---

### 11. MODERATE: SVEIPR Local Search Does Not Estimate Several Key Parameters

In the local search, `rw.sd` is specified for `b1..b8`, `c1..c5`, `mu_EPI`, `rho`, `tau`, `eta`, `gamma`, but several parameters with direct epidemiological meaning -- `Beta`, `mu_SV`, `mu_PR`, `mu_IR`, `mu_RS`, `alpha` -- are held fixed. Of these, `mu_RS` (reinfection rate, fixed at 0.5) and `alpha` (asymptomatic fraction, fixed at 0.4) are key features of the SVEIPR model's claimed innovations. Not estimating them means the model's two novel structural features are never compared to data.

---

### 12. MODERATE: ARIMA(3,1,3) Selected Despite Non-Normal Residuals Without Diagnostic Follow-Up

The QQ plot shows heavy tails and the authors note "the distribution of residuals has heavier tails than the normal distribution." This violates the Gaussian white noise assumption of ARIMA models. A natural response would be to explore transformations (e.g., square root or log of case counts, common in epidemiology), robust alternatives, or at minimum to quantify whether the departure from normality affects inference. Instead the authors move on without investigation, using "this is consistent with earlier results" as a terminal observation.

---

### 13. MINOR: SEIR Model Reported Log-Likelihood Value Inconsistent With Stored Data

The text states the best local search SEIR log-likelihood was "-1195.194." The stored `local_logliks.rds` shows the best value is -1195.915. While a small numerical difference (possibly arising from a different cached run), this suggests at least one figure in the paper was not regenerated from the saved objects.

---

### 14. MINOR: SVEIPR Initial Conditions Are Fixed at Implausibly Large Values

The SVEIPR `rinit` sets E=1000, I=500, P=500 at t0=1 (week 1 of January 2020). King County had at most a handful of confirmed cases at that time -- the first death was in late February 2020. Starting with 2000 active cases out of a 2.27 million population is inconsistent with the stated historical context and with the initial conditions justified for the SEIR model (E=20, I=5).

---

### 15. MINOR: Bibliography Contains Duplicate Entries and an Irrelevant Citation

The `.bib` file duplicates several entries verbatim (e.g., `2024/hw01`, `2002/statistical_inference`, `2024/lec05`, `2024/lec06`) appearing twice each. Additionally, the citation for ARIMA (CAO2020135491) is for brucellosis in Hebei province, China -- used to justify applying ARIMA to COVID-19. A more directly relevant citation would strengthen the methodological motivation. The CEYLAN2020138817 reference is a better fit and is also cited; the brucellosis reference adds noise without supporting the argument.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/final_project.bib`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/SVEIPR_results_run_level_3/lik_local_run_level_3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/SVEIPR_results_run_level_3/lik_global_run_level_3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/local_logliks.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/seir_global.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/local_search.rds`
