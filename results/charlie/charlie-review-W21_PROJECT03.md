# Peer Review: W21 Project 03
**Title:** Investigation of Vaccination Effect on Covid-19 in California

---

## Summary

This project applies SIR and SIRV compartment models using the `pomp` package to California COVID-19 daily case and vaccination data (January 12–April 7, 2021; 87 observations) to assess vaccine effectiveness and forecast pandemic trajectory. Three models are fit via iterated filtering (mif2): a basic SIR, a SIRV model with an estimated vaccination rate parameter, and a SIRV model that incorporates a pre-fitted quadratic vaccination schedule. The project shows genuine effort in mechanistic modeling, including global likelihood searches and a profile likelihood for the vaccine efficacy parameter Sigma. However, the analysis is undermined by a systematic error in the measurement model accumulator (all three models count the wrong epidemiological flow), serious code errors in SIRV Model 1, a forecast that discards the MLE in favor of initial guesses, and unsupported conclusions about vaccine efficacy. The model selected for final prediction (SIRV2) is statistically dominated by SIRV1 by approximately 8.75 log-likelihood units with no acknowledgment of this discrepancy.

---

## Major Issues

### 1. Accumulator H tallies recoveries rather than new infections — all three models

In all three model step functions (`sir_step`, `sirv1_step`, `sirv2_step`), the accumulator variable `H` is incremented by `dN_IR` (the number of individuals leaving the infectious compartment per time step), not by `dN_SI` (the number of new infections). The measurement model then draws `New_Report ~ Binomial(H, rho)`, claiming to model daily confirmed case counts. New COVID-19 reports correspond to newly infected individuals, not to recoveries or removals. With an average infectious period of roughly 20 days (implied by `mu_IR ~ 0.05`), the flows `dN_SI` and `dN_IR` are substantially different in both magnitude and timing. This mismatch means that all three models are fitting the observation model to the wrong latent flow, producing biased parameter estimates and an invalid likelihood. This is an error in the POMP measurement model specification (Checklist item 12: measurement model must correctly link observed data to the latent state).

**Fix:** Replace `H <- H + dN_IR` with `H <- H + dN_SI` in all three step functions. This reflects the standard reporting accumulator used in course examples.

---

### 2. SIRV Model 1 — two code errors inconsistent with stated equations

**(a) `dN_VI` uses the wrong compartment size in the infection probability.**

The stated ODE gives the V-to-I infection rate as `sigma * beta * I(t) / N`. In the Euler discretization, the per-vaccinated-individual probability should be `1 - exp(-Sigma * Beta * I / N * delta.t)`. The code instead uses:

```r
dN_VI <- rbinom(n=1, size=V, prob = 1-exp(-Sigma*Beta*V/N*delta.t))
```

The term `V` appears in the exponent where `I` should appear. This changes the infection hazard from frequency-dependent (proportional to I) to a nonlinear density-dependent term proportional to `V^2/N`. The correct version (using `I`) is implemented in SIRV Model 2, confirming that this is an unintended discrepancy. This error silently distorts all parameter estimates from SIRV1.

**(b) `dN_SV` uses a transition probability that scales with `S^2/N` rather than `S/N`.**

The stated ODE gives the S-to-V rate as `u/N * S(t)`. The per-susceptible individual hazard is `u/N`. The code uses:

```r
dN_SV <- rbinom(n=1, size=S, prob=1-exp(-u*S/N*delta.t))
```

With `size=S`, the expected number vaccinated is `S * (1 - exp(-u*S/N*dt)) ≈ u*S^2/N*dt` for small `dt`, which disagrees with the ODE-implied expectation of `u*S/N*dt`. This gives a vaccination rate that grows with `S^2` rather than linearly with `S`, inflating the vaccination flow early in the epidemic when S is large.

**Fix for (a):** Change the exponent to `-Sigma*Beta*I/N*delta.t`. **Fix for (b):** Change the exponent to `-u/N*delta.t` (removing the extra `S` factor).

---

### 3. Final forecast simulation uses eyeballed initial parameters, not MLE

In the prediction section, the simulation for the pandemic trajectory is called as:

```r
simulate(params=params, nsim=5, ...)
```

The variable `params` is the initial hand-tuned guess `c(Beta=0.01, Sigma=0.01, mu_IR=0.04, mu_VR=0.9, rho=0.3, eta=0.9, N=N)` set earlier in the SIRV2 section. The MLE parameters are stored in `params_maxlik` (computed on the preceding line), but `params_maxlik` is never used in the `simulate()` call. The conclusion that "the COVID-19 pandemic will end before the end of July 2021" and the claim that "vaccine efficacy is over 80%" are therefore derived from arbitrary starting values, not from the optimized model. This renders the primary research question unanswerable from this analysis (POMP Checklist item 7: forecasts must use fitted parameter values).

**Fix:** Replace `params=params` with `params=params_maxlik[names(params)]` or the appropriate subset excluding `loglik` and `loglik.se`.

---

### 4. SIRV2 selected for final analysis despite SIRV1 having substantially higher log-likelihood

The global search results stored in the `.rda` files show:

- SIR global maximum log-likelihood: -190.55
- SIRV1 global maximum log-likelihood: -181.96 (8.59 log-likelihood units better than SIR; 17.2 on the 2*loglik scale)
- SIRV2 global maximum log-likelihood: -190.71 (worse than even the basic SIR)

The paper states "the log-likelihood from SIRV model [SIRV1] is higher than that from SIR model" but then proceeds to use SIRV2 for prediction without presenting the SIRV1 vs SIRV2 log-likelihood comparison. SIRV2 is statistically dominated by SIRV1 by ~8.75 log-likelihood units (a difference far exceeding any reasonable AIC penalty for the additional parameter in SIRV1). No formal model selection criterion (AIC, likelihood ratio test) is applied anywhere. The choice to use SIRV2 is unjustified statistically. (POMP Checklist items 3 and 8: quantitative model comparison is required.)

**Fix:** Report AIC or log-likelihoods for all three models in a table and use the best-fitting model (SIRV1) as the basis for inference and prediction. Alternatively, justify why SIRV2 is preferred despite its inferior fit.

---

### 5. Overstated vaccine efficacy conclusion given extremely wide profile likelihood CI

The profile likelihood for Sigma covers values from approximately 0.0004 to 0.85 above the Wilks 95% threshold (computed from the stored results: cutoff = -192.59). The profile likelihood reveals that essentially all tested values of Sigma on (0, 0.85) are statistically indistinguishable from the maximum. The paper itself notes "parameter sigma in SIRV model above is weakly identifiable," yet the Conclusion section states "The vaccine is effective and protective against COVID-19. The vaccine efficacy is over 80% according to our analysis." A 95% CI that spans nearly the entire (0,1) range (0.04% to 85% vaccine *failure* probability) provides no evidential basis for claiming greater than 80% efficacy. This is an overconfident conclusion not supported by the computed profile. (POMP Checklist item 5: implausible or unidentifiable parameters must not be interpreted as point estimates.)

**Fix:** The conclusion should report the CI for Sigma and state that vaccine efficacy is not identifiable from this data alone, consistent with the discussion in the Future Works section.

---

### 6. No non-mechanistic benchmark comparison

No ARMA, auto-regressive negative binomial, or other non-mechanistic model is fit to the data. The SIRV2 maximum log-likelihood (-190.71) is actually worse than the basic SIR (-190.55), which itself may not beat a simple time series benchmark. Without a benchmark, there is no evidence that any of the three compartment models captures structure in the data beyond what a simple statistical model would achieve. (POMP Checklist item 2; Error 1.6 from the weakness reference: CC-Yes, Major.)

**Fix:** Fit an ARIMA model or a negative binomial regression to the daily case counts and report its log-likelihood for comparison.

---

### 7. CI cutoff line omitted from profile likelihood plot

The code that would display the Wilks 95% confidence cutoff line on the profile likelihood plot is commented out:

```r
# + geom_hline(color="red", yintercept = ci.cutoff)
```

Without the reference line, the reader cannot visually identify confidence interval endpoints, and the claim that sigma is weakly identifiable cannot be assessed from the figure. The text computes the cutoff correctly (-192.62) but does not display it.

**Fix:** Uncomment the `geom_hline` call so the CI cutoff is visible on the profile plot.

---

## Minor Issues

### 8. Local search log-likelihood re-evaluation uses a single pfilter call without replication

In the local search re-evaluation step for all three models:

```r
mifs_local[[i]] %>% pfilter(Np = options_Np) %>% logLik() %>% logmeanexp() -> ll
```

`logmeanexp` is applied to a single scalar, which returns that scalar unchanged. There is no replication (contrast with the global search, which uses `replicate(options_Neval, ...)`). Single-run particle filter log-likelihoods carry Monte Carlo noise that is not quantified. While this does not bias the optimization, it produces noisy local search likelihood estimates without reported standard errors. (Error 1.4: CC-Yes, Major in the weakness reference, though here it affects diagnostics rather than final inference.)

**Fix:** Wrap the pfilter call in `replicate(options_Neval, ...)` and apply `logmeanexp(se=TRUE)` consistently, as done in the global search.

---

### 9. No profile likelihoods for parameters other than Sigma

Profile likelihoods are computed only for Sigma. Key parameters such as Beta, mu_IR, and rho are estimated but their identifiability is never assessed. The pairs plots from global searches show scattered points with no clear ridge for most parameters, suggesting weak identifiability for multiple parameters, but no CIs are reported. (POMP Checklist item 5.)

---

### 10. Binomial measurement model — no overdispersion

All three models use `dmeasure <- dbinom(x=New_Report, size=H, prob=rho, log=log)`. COVID-19 daily case counts exhibit substantial overdispersion relative to the binomial. A negative binomial measurement model would be more appropriate. The course standard is to consider overdispersion explicitly. (POMP Checklist item 9; Error 1.11 in the weakness reference.)

---

### 11. No environmental/process stochasticity beyond demographic noise

All three models use purely binomial transitions (demographic stochasticity) with no multiplicative noise on transmission rates. COVID-19 dynamics exhibit strong environmental stochasticity (super-spreading events, policy changes, reporting bursts). The course material (Ch 13, Ch 16) demonstrates adding gamma white noise to the transmission rate. The absence of process overdispersion likely contributes to poor model fit.

---

### 12. Vaccination quadratic extrapolation has no population bound

The quadratic vaccination model predicts ever-increasing daily vaccinations. During the forecast period (days 88–210), the predicted cumulative vaccinations would exceed the susceptible pool for some simulations, potentially driving `S` negative. No constraint prevents `dN_SV` from exceeding `S`. While `rbinom(size=S, ...)` technically cannot produce more than S vaccinations in a single step, the rounding and day-counter logic (`D` state variable) can create edge cases that should be verified.

---

### 13. Run level inconsistency between submitted Rmd and cached results

The Rmd header sets `run_level = 1` (Np=100, Nmif=10), but the analysis loads cached `.rda` files suffixed with `-2` (corresponding to run_level=2 with Np=1000, Nmif=100). Readers running the Rmd will reproduce run_level=1 results (very different from those displayed) unless they re-generate the `-2` cache. The submitted run level should match the cached results used for the write-up, or the code should be restructured so that the narrative and executed output are consistent.

---

### 14. No formal model comparison table

There is no table summarizing log-likelihoods (or AIC values) for SIR, SIRV1, and SIRV2. The comparison is done informally in prose ("the log-likelihood from SIRV model is higher") without quantitative detail. A simple table with model name, number of parameters, log-likelihood, and AIC would make the comparison transparent and allow evaluation of whether added parameters in SIRV models are statistically supported.

---

### 15. Forecast does not condition on filtering distribution

The prediction code re-creates the SIRV2 pomp object with an extended time horizon and calls `simulate()` from `t0=0`. This generates trajectories from initial conditions and has no memory of the actual data observed during January–April 2021. The course standard for POMP forecasting is to run the particle filter up to the end of the training data and simulate forward from the filtering distribution, which conditions on all observed cases. The current approach will produce forecasts inconsistent with the end-of-training-period system state. (POMP Checklist item 7.)

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/results/sir_lik_global_eval-2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/results/sir_lik_local_eval-2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/results/sirv1_lik_global_eval-2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/results/sirv1_lik_local_eval-2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/results/sirv2_lik_global_eval-2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/results/sirv2_lik_local_eval-2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project03/results/sirv2_profile_sigma-2.rda`
