# Peer Review: W21 Project 02
**Title:** Study of daily COVID-19 Infected cases in the United States

---

## Summary

This project fits three mechanistic compartment models — SEIR, SECSDR, and SEIQR — to daily COVID-19 confirmed infection counts in the United States from January 2020 through April 2021 using the `pomp` R package. The stated goal is to capture transmission dynamics and evaluate whether any of the three model structures can reproduce the observed case trajectory. The project's main honest finding — that none of the three models fits the data adequately — is clearly stated. However, the analysis is fundamentally incomplete: the iterated filtering tuning is catastrophically misconfigured for two of the three models (rendering those results meaningless), no quantitative goodness-of-fit comparison is made between models, no non-mechanistic benchmark is included, the data file required to reproduce the analysis is absent from the submission, and several POMP implementation errors undermine the validity of reported likelihoods. The conclusion essentially acknowledges failure without diagnosing why, leaving the reader with no actionable scientific output.

---

## Major Issues

### 1. Catastrophically misconfigured iterated filtering for SECSDR and SEIQR

The `mif2` calls for both the SECSDR model (Section 4.2) and the SEIQR model (Section 5.2) use:

```r
covid_cooling.fraction.50 = 0.00005
covid_rw.sd = 0.000000002
```

A `cooling.fraction.50` of 0.00005 means perturbations shrink to essentially zero after a single iteration (the standard course value is 0.5). A `rw.sd` of 2e-9 on the log scale is negligibly small — the parameter space is never explored. This means iterated filtering for these two models never moves appreciably from the starting values; the reported likelihoods and parameter estimates reflect the random box draws, not any optimization. The conclusion that the models fail to fit the data is therefore not attributable to model misspecification — it may simply reflect that the optimizer was never allowed to run. All downstream inferences for SECSDR and SEIQR are invalidated.

**Fix:** Use `cooling.fraction.50 = 0.5` and `rw.sd` on the order of 0.02 (on the log or logit scale), following the course standard (Ch 15, p31-32).

---

### 2. Missing data file prevents reproducibility

The data is read from `worse_hospitalization_all_locs.csv` (line 34 of `blinded.Rmd`), but this file is not present in the submission directory. Without it, the analysis cannot be reproduced. Per the code-supplement checklist (Wheeler et al. 2024), all auxiliary inputs must be included. This is a complete reproducibility failure.

**Fix:** Include the data file in the submission, or provide a download script.

---

### 3. No non-mechanistic benchmark comparison

None of the three models is compared against any non-mechanistic statistical baseline such as an ARMA, ARIMA, or negative binomial regression model. Without such a benchmark, there is no way to assess whether the mechanistic models capture meaningful structure that a simpler model could not (Wheeler et al. 2024, §Benchmark comparison; STATS 531 Error 1.6). The project concludes all three models fail, but there is no reference point for what "failure" means quantitatively.

**Fix:** Fit at least one non-mechanistic time series model to the same data and report its log-likelihood for comparison.

---

### 4. SEIR measurement model is misspecified: zero variance when H = 0

The SEIR `dmeas` uses a normal distribution with `sd_cases = sqrt(mean_cases * mean_cases) = rho * H`. When `H = 0`, the standard deviation is exactly zero. Evaluating `pnorm(Infected, 0, 0, ...)` with zero standard deviation is numerically degenerate and the `tol = 1e-25` floor is the only thing preventing `-Inf` log-likelihoods at these time points. Since `H` is reset each time step (it is an accumulator), this creates pathological likelihood evaluations throughout the series. The `rmeas` similarly uses `sqrt(rho*H)` rather than the square root of the mean (the standard deviation of a Poisson-type model), so the variance structure is `(rho*H)^2` rather than `rho*H`, which is inconsistent with any standard measurement model.

**Fix:** Use a negative binomial or overdispersed Poisson measurement model with a minimum variance floor not dependent on `H` being nonzero, consistent with course practice (Ch 16).

---

### 5. SECSDR conservation of individuals violated

In `covid_rprocess` for SECSDR (Section 4.1), the exposed flow is computed as:

```c
double dN_SE = rbinom(S, 1-exp((-Beta1*Ca - Beta2*Sy)*dt));
double dN_ECa = rbinom(dN_SE, 1-exp(-dt*mu_ECa));
```

Then `S -= dN_ECa` rather than `S -= dN_SE`. Individuals leave S at rate `dN_SE` but only `dN_ECa <= dN_SE` are subtracted from S. The remaining `dN_SE - dN_ECa` individuals disappear from the population — compartments do not sum to a constant. This violates conservation and silently distorts the dynamics. The SECSDR results are therefore based on an incorrectly implemented model.

**Fix:** Subtract `dN_SE` from S, or redesign the E compartment to correctly route `dN_SE` individuals.

---

### 6. No profile likelihood or confidence intervals for any parameter

No profile likelihoods are computed for any model or any parameter. All three models report point estimates from global or local search without any uncertainty quantification. It is therefore impossible to assess whether any parameter is identifiable from the data (Wheeler et al. 2024, §Parameter identifiability; STATS 531 Error 1.9 is related). Given the poor fit acknowledged in the conclusion, the absence of identifiability assessment means the fitted parameter values carry no interpretable uncertainty.

**Fix:** Compute profile likelihoods for at least the key transmission parameters (Beta, rho) in the best-performing model.

---

### 7. SEIR local search excludes most parameters from optimization

The SEIR local search (Section 3.2) uses:

```r
rw.sd = rw.sd(Beta=0.002, rho=0.002, eta=ivp(0.002))
```

Parameters `mu_EI`, `mu_IR`, and `tau` are declared in `paramnames` but are not perturbed during local search. These parameters are fixed at their initial values throughout the optimization. The result is that the local search effectively holds most model parameters constant, defeating the purpose of the optimization. The global search box does include these parameters, but the local search — which is typically used to find good starting values for global search — cannot refine them.

**Fix:** Include all free parameters in `rw.sd` during local search, or explicitly justify which parameters are being profiled or fixed.

---

### 8. Global search for SEIR uses mif2 without re-specifying rw.sd or Nmif

In the SEIR global search (Section 3.3), `mf1 <- mifs_local[[1]]` inherits the `rw.sd` and `Nmif` settings from the local search (Np=2000, Nmif=200). Then `mf1 %>% mif2(params=c(unlist(guess), fixed_params)) %>% mif2(Nmif=100)` runs a second `mif2` pass with `Nmif=100` but does not reset `rw.sd`. The perturbation magnitude is inherited, not re-specified for the global search box. This means the parameter exploration range during global search is determined by whatever the local search had converged to, not by the geometry of the global search box.

**Fix:** Explicitly specify `rw.sd` in the global search `mif2` calls to ensure appropriate exploration of the global box.

---

### 9. SEIQR population size fixed at 32,000,000 instead of U.S. population

The SEIQR model (Section 5.1) fixes `N = 32,000,000` — approximately the population of Canada — while the SEIR model uses `N = 300,000,000` for the U.S. The data are U.S. national case counts. This two-orders-of-magnitude discrepancy means the SEIQR model parameters (especially Beta and rho) are calibrated to a population size ten times smaller than the data source, leading to parameter estimates that are inconsistent across models and not interpretable as U.S.-population epidemiological quantities.

**Fix:** Set `N = 300,000,000` consistently across all models, or explicitly estimate it.

---

### 10. No convergence diagnostics for SEIR local and global search

Section 3.2 shows trace plots of the local search, but the mif2 trace plot for the SEIR model shows no clear convergence — the log-likelihood panel is not shown to consistently increase across runs, and parameter panels show substantial spread. Despite this, the authors proceed to global search and use the resulting parameters to simulate. For SECSDR and SEIQR, the `plot(mifs_global)` calls are present but the `ylim=10` argument in the SEIQR case (`plot(mifs_global, ylim=10)`) is incorrect syntax and likely causes an error or is silently ignored. There is no discussion of convergence quality in any of the three models.

**Fix:** Confirm that the log-likelihood trace consistently increases, show trace plots for all models clearly, and discuss convergence explicitly (STATS 531 Error 1.8; Wheeler et al. 2024, §Computational adequacy).

---

### 11. SECSDR and SEIQR run_level set to 1 despite `bake`/`stew` caching

The SECSDR section sets `run_level <- 1` (Np=100, Nmif=10, Nglobal=10), which is debugging-level computation. The SEIQR section sets `run_level <- 2` (Np=2000, Nmif=100, Nglobal=50), which is more reasonable. However, for SECSDR the critically misconfigured `rw.sd` and `cooling.fraction.50` (Issue 1 above) dominate over the particle count concern, so both problems compound. The run_level=1 setting for SECSDR means even if the perturbation magnitudes were correct, the computational effort is far below what is needed to assess model fit for data of this length and complexity.

**Fix:** For final results, SECSDR should use at minimum run_level=2 with corrected mif2 tuning parameters.

---

## Minor Issues

### 12. No ARIMA or classical time series analysis of the data

The project jumps directly to mechanistic POMP models without any preliminary time series analysis (ARMA/ARIMA, spectral analysis, or even ACF/PACF plots of the raw data). Standard course practice (Ch 3–9) is to first characterize the data's statistical properties before fitting mechanistic models. Understanding the autocorrelation structure, trend, and seasonality of the observed series would have motivated the model structure choices and identified features the mechanistic models need to reproduce.

---

### 13. Simulation uses hard-coded "best" parameters rather than MLE from optimization

Section 3.4 simulates from `params=c(Beta=1.470177, mu_IR=0.009791881, ...)` hard-coded in the `simulate()` call, rather than extracting them programmatically from the global search results object. This is inconsistent with the values in the table above it and makes the simulation results difficult to trace back to the optimization output. Similarly, Section 4.3 and 5.4 use `para = coef(mifs_global[order(...)[2]])`, selecting the second-best run rather than the best, without explanation.

---

### 14. No discussion of the measurement model's biological meaning

The SECSDR model uses `Di` (daily diagnosed) as the direct observation with `sd = rho*Di + 1e-10` in both dmeas and rmeas. This implies the observation noise scales with the mean (coefficient of variation form), but `rho` is defined in `paramnames` and transformed via log without discussion of its meaning as a noise parameter rather than a reporting rate. The SEIQR model uses `Q` (quarantine compartment) as the observable, which is a reasonable proxy for reported cases but is not discussed epidemiologically. The SEIR model's accumulator `H` tracks cumulative recoveries, which represents confirmed cases only if recovery is synonymous with diagnosis — an assumption that should be stated and justified.

---

### 15. References are incomplete and acknowledgment of prior work is minimal

The references section cites only the course lecture notes and two prior course projects (from W20) as templates. No epidemiological literature on COVID-19 is cited to justify parameter ranges or model structure. No statistical references for POMP methodology (e.g., Ionides et al. 2015, King et al. 2016) are included. The SECSDR and SEIQR structures are taken directly from prior student projects without discussing whether those structures are appropriate for U.S. national-level COVID-19 dynamics.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week9/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week9/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project02/blinded.html`
