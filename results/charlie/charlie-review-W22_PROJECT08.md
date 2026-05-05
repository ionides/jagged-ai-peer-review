# Peer Review: W22 Project 08
### Analysis of Covid-19 Cases in Turkey

---

## Summary

This project applies time series methods to daily COVID-19 case data from Turkey in 2020, developing a novel SEIREIR compartment model to capture a two-wave epidemic pattern attributed to the emergence of a new viral variant and relaxation of restrictions. The report includes an ARIMA(2,1,0) benchmark analysis and a POMP-based SEIREIR model fit using iterated filtering with global search. While the project demonstrates familiarity with the pomp workflow and attempts a scientifically motivated model structure, it has several critical flaws. The most serious are: (1) the measurement accumulator tracks recoveries rather than new infections, creating a fundamental mismatch between the model and the data; (2) the ARIMA and POMP log-likelihoods are compared directly despite being evaluated on different observations (differenced vs. raw data); and (3) no profile likelihoods are computed for any parameter, leaving parameter uncertainty unquantified. Taken together, these undermine the statistical validity of all reported results.

---

## Major Issues

### 1. Accumulator H tracks recoveries, not infections — fundamental measurement model mismatch

The rprocess Csnippet accumulates `H += (dN_IR_o + dN_IR_b)`, meaning H counts total recoveries from both strains. The dmeasure Csnippet then models `reports ~ NegBinomial(k, rho*H)`. However, `reports` is the observed number of *confirmed positive cases* (new infections), not recoveries. Recoveries lag infections by days to weeks. Measuring reported cases as a function of cumulative recoveries in the same time step is a misspecification of the observation process. The accumulator should count new infections (e.g., `dN_EI_o + dN_EI_b`) or new entries into the infectious compartment, not exits from it. This error silently distorts all parameter estimates and the reported log-likelihood of -2308.

---

### 2. Invalid direct comparison of ARIMA and POMP log-likelihoods

The conclusion states: "The maximum log likelihood of our POMP model is -2336, which is much smaller than that of ARIMA." The ARIMA(2,1,0) log-likelihood of -1692.303 is evaluated on the *differenced* series (d=1), while the POMP model log-likelihood is evaluated on the *raw* (undifferenced) series. These two likelihoods involve different data transformations and cannot be compared directly as evidence of one model outperforming the other. While likelihoods from different model classes on the same observed data are comparable (531-conventions.md), the ARIMA model here implicitly conditions on a different set of observations due to differencing. The authors should note this limitation and, if a benchmark comparison is desired, fit either an ARMA model to the raw data or account for the Jacobian adjustment of the differencing transformation.

---

### 3. No profile likelihoods — parameter uncertainty entirely unquantified

No profile likelihoods are computed for any parameter in the model. With 8 free parameters (Beta_o, Beta_b, Beta_or, Beta_r, mu_EI_o, mu_EI_b, rho, eta), it is not possible to determine whether any of these are identifiable from the data. The global search scatter plots are not a substitute for profile likelihoods: they show where optimization runs cluster, but do not provide confidence intervals or test identifiability. Profile likelihoods are the course-standard method for POMP parameter uncertainty (see SKILL_pomp.md, §5 and 531-conventions.md). Without profiles, the reported MLE cannot be considered validated. This is a course-confirmed error (531-weakness-reference.md, Error 1.2 and 1.9).

---

### 4. Data construction error: active cases vs. new daily cases

The data preprocessing computes `turkey$cases = turkey$Confirmed - turkey$Deaths - turkey$Recovered`. If `Confirmed`, `Deaths`, and `Recovered` are cumulative totals (which is standard in COVID-19 reporting datasets, including the Kaggle source cited), then this formula gives *active cases* on each day, not *new daily cases*. Active cases are a stock variable, not a flow. However, the ARIMA and POMP models treat `turkey$cases` as if it were a flow (new infections per day). The SEIREIR model's measurement model is designed to relate to a daily accumulator (H resets via `accumvars`). Fitting to active cases rather than daily new cases is a fundamental data error that invalidates both the ARIMA and POMP analyses.

---

### 5. Initial conditions for R_b are biologically implausible

The rinit Csnippet sets `R_b = nearbyint((1-eta)*N)`. This initializes a large fraction of the population (approximately `(1-0.1)*84340000 ≈ 75.9 million people`) as recovered from the beta variant at day 0 (the start of 2020), before the beta variant was introduced. Since the beta variant had not yet appeared in the population at the start of the data, `R_b` at t=0 should be zero. This implausible initialization potentially allows the model to achieve superficially good simulation fits by misrepresenting the population structure, and it inflates the effective susceptible pool for the beta variant (since R_o individuals can be re-infected by beta, governed by Beta_r).

---

### 6. Ad hoc injection of 10 individuals at a single fixed time step

The rprocess contains `if (t == 125) e = 10;` which adds exactly 10 individuals to `E_b` at a single time point. This mechanism for "turning on" the beta variant is arbitrary and statistically unjustified. The time point (t=125) is not estimated — it is hard-coded — and the number of seed infections (10) is fixed without justification. Furthermore, the text states the second wave began "after day 150" but the code injects seeds at day 125. If the seeding time or magnitude could affect inference materially, these should be treated as parameters or at minimum their sensitivity explored. This is not the appropriate way to handle variant emergence in a POMP framework.

---

### 7. Missing convergence diagnostics for the global search

The global search runs each starting point through two sequential `mif2` calls but does not show log-likelihood traces for the global search runs. The local search trace plots show the log-likelihood panel, but global search convergence is assessed only from the scatter plot of terminal parameter values. The authors acknowledge "we does not reach the local maximum" but do not investigate further. Standard practice requires showing that multiple independent searches from diverse starting points converge to similar terminal likelihoods. No such evidence is presented for the global search. This is a course-confirmed error (531-weakness-reference.md, Error 1.8).

---

### 8. rw.sd perturbation magnitudes appear excessively small

The local search uses `rw.sd(Beta_o=0.003, Beta_b=0.002, Beta_or=0.002, Beta_r=0.002, mu_EI_o=0.002, mu_EI_b=0.002, rho=0.002, eta=ivp(0.001))`. The standard course perturbation on a log or logit scale is rw.sd=0.02 (531-conventions.md). The values used here are 10x smaller. Although Beta_o, Beta_b, Beta_or, Beta_r are declared with `log=` transformation in `partrans`, the rw.sd of 0.002–0.003 on the log scale corresponds to perturbations of less than 0.3% per step, which is nearly negligible and would severely hamper the ability of IF2 to explore the parameter space. The observed "convergence" in traces may reflect an optimizer that barely moved from its starting values rather than genuine optimization. This is a course-confirmed error (531-weakness-reference.md, Error 1.8, computational adequacy).

---

## Minor Issues

### 9. Local search uses sequential %do% despite parallel backend

The local search bake block uses `foreach(i=1:20, .combine=c) %do% { ... }` (sequential), while the surrounding code registers a parallel backend with `registerDoParallel()`. This is purely a performance issue — correctness is unaffected — but results in 20 sequential mif2 runs when parallelism was clearly intended and available.

---

### 10. No simulation-based diagnostics beyond visual overlay

Model adequacy is assessed only by visual comparison of simulated trajectories to the observed data. No conditional log-likelihood plots, no effective sample size diagnostics (beyond the initial pfilter call), and no quantitative summary statistics comparing simulated and observed data are provided. The initial pfilter plot showing ESS is noted briefly but not interpreted. Per Wheeler et al. (2024) and SKILL_pomp.md §4, these diagnostics are important for identifying where and how the model fails.

---

### 11. Fixed parameters lack principled justification

Five parameters are fixed: N, mu_IR_o, mu_IR_r, mu_IR_b, and k. The recovery rates (mu_IR_o = 0.02, mu_IR_r = 0.02/0.03, mu_IR_b = 0.01) are given rough justification from CDC guidance, but k=10 (the overdispersion parameter for the negative binomial measurement model) is fixed without any justification. Overdispersion is sensitive and fixing k at an arbitrary value may substantially distort inferences about other parameters (rho, Beta values). At minimum, sensitivity to k should be explored.

---

### 12. Population size inconsistency

The text states "We fix N=843400, the population of Turkey in 2020" but the code uses `N=84340000` (84.34 million), which is the correct order of magnitude for Turkey. The text is off by a factor of 100. This appears to be a typographical error in the text, but readers cannot verify which value was actually used without reading the code carefully.

---

### 13. ARIMA model selection rationale is inconsistent

The report states that ARIMA(2,1,1) has the smallest AIC (3385.08) but then selects ARIMA(2,1,0) based on a likelihood ratio test (LRT) claiming it is "better." This is self-contradictory: if AIC selects ARIMA(2,1,1) and the LRT rejects the extra MA parameter, these tests are giving conflicting signals. The report should clarify this apparent contradiction and justify the final model choice. Additionally, the LRT p-value decision is described but not shown numerically.

---

### 14. No benchmark ARMA model on the raw (undifferenced) series

The ARIMA model uses one round of differencing and is not directly comparable to the POMP model. An ARMA model fit to the raw series would serve as a more appropriate benchmark for the POMP likelihood comparison (531-conventions.md §Benchmark comparison). The current setup conflates model selection within the ARIMA class with cross-model comparison.

---

### 15. Periodogram not shown; only referenced as unremarkable

The report states: "We want to check the appearance of periodicity by the smoothed periodogram" but the `spectrum()` call has `include=FALSE` and no plot of the periodogram is rendered. The reader cannot verify the claim of "no evidence of obvious periodicity." Either the plot should be shown or the claim removed.

---

## Summary of Issues by Priority

| # | Issue | Severity | CC? |
|---|-------|----------|-----|
| 1 | Accumulator H tracks recoveries not infections | Major | No |
| 2 | Invalid ARIMA vs POMP log-likelihood comparison | Major | No |
| 3 | No profile likelihoods | Major | CC-Yes (1.2, 1.9) |
| 4 | Data construction: active cases vs. daily new cases | Major | No |
| 5 | R_b initialized with (1-eta)*N at t=0 | Major | No |
| 6 | Ad hoc fixed seeding at t=125 with 10 individuals | Major | No |
| 7 | No global search convergence diagnostics | Major | CC-Yes (1.8) |
| 8 | rw.sd ~10x smaller than course standard | Major | CC-Yes (1.8) |
| 9 | Local search uses %do% not %dopar% | Minor | No |
| 10 | No simulation-based model diagnostics | Minor | No |
| 11 | k fixed without justification | Minor | No |
| 12 | Population size text vs code inconsistency | Minor | No |
| 13 | ARIMA model selection rationale inconsistent | Minor | No |
| 14 | No ARMA benchmark on raw series | Minor | No |
| 15 | Periodogram not shown | Minor | No |

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project08/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project08/covid_params.csv`
