# Peer Review: W24 Project 04
## "Comparative Analysis of ARIMA and SEIR Models Using COVID-19 Data"

---

## Summary

This project applies both ARIMA and SEIR models to weekly COVID-19 confirmed-case data from Washington State, with a stated goal of determining whether the SEIR model provides a better fit than ARIMA. The paper presents EDA simulations for three US states and then builds a SEIR POMP model using particle-filter infrastructure. While the project demonstrates familiarity with the basic mechanics of POMP model construction and ARIMA model selection, the analysis is seriously undermined by ad hoc parameter calibration substituted for likelihood-based inference, a misspecified measurement model, the complete absence of quantitative goodness-of-fit reporting, and multiple fundamental software errors. The central comparative claim — that SEIR "more naturally captures epidemic dynamics" — is unsupported because no common metric is ever computed for both models.

---

## Major Issues

### 1. Ad hoc calibration substituted for likelihood-based inference

The entire SEIR fitting procedure uses sum-of-squared-differences minimization (the `cost_function` defined at line 739–748 and reused in the global search), not likelihood maximization. The POMP framework provides `mif2` (iterated filtering) and `pfilter` for proper likelihood-based inference, neither of which is used anywhere in the main analysis. Because the cost function optimizes squared residuals on simulated trajectories rather than the log-likelihood, the resulting parameter estimates are not MLEs, have no formal uncertainty characterization, and cannot be compared to the ARIMA log-likelihood or AIC. This makes the central research question — which model fits better — formally unanswerable with the analysis as presented. (Wheeler et al. 2024, §Likelihood-based inference.)

### 2. No quantitative goodness-of-fit: model comparison is entirely visual

No log-likelihood or AIC value is ever computed or reported for the SEIR model. The ARIMA section uses AIC for model selection among ARIMA variants (a good practice), but then the SEIR section relies exclusively on overlaid trajectory plots. The conclusion that "the SEIR model more naturally captured the specific characteristics of infectious disease spread" (§Conclusion) is therefore unsubstantiated. A visual overlay cannot substitute for a quantitative fit measure, especially when the SEIR simulation produces only a single stochastic trajectory. Wheeler et al. (2024) note that "visual comparisons alone are only a weak and informal measure of goodness-of-fit."

### 3. Misspecified measurement model: `dnbinom` used incorrectly, and `rmeas` uses `rbinom`

The SEIR `dmeas` function uses `dnbinom(cases, I, rho, give_log)` (line 677). In R's `dnbinom`, the second argument is `size` (the dispersion parameter) and the third is `prob` — not the mean. The project apparently intends a negative-binomial with mean `rho * I`, which would require `dnbinom_mu(cases, size_param, rho * I, give_log)`. Using `I` as the size parameter and `rho` as `prob` means the measurement model evaluates a completely different distribution than intended; this invalidates all likelihood evaluations. Compounding this, the `rmeas` function uses `rbinom(I, rho)` (line 681) — a binomial draw, not a negative-binomial — making `dmeas` and `rmeas` inconsistent with each other. The `rmeas` in the global search section (line 846) switches to `nearbyint(I)`, a deterministic rounding with no randomness at all, making this a third, different specification of the same model in the same document. Wheeler et al. (2024, §Reproducibility) identify measurement-model inconsistency between code and text as a concrete reproducibility failure.

### 4. Measurement model conditions on current `I` rather than accumulated incidence `H`

In the `dmeas`/`rmeas`, both the original and final models condition observations on `I` (current infectious count) rather than `H` (accumulated incidence since last observation). For case-count data, reported cases are a fraction of new infections over the interval, not a fraction of the instantaneous infectious pool. The standard POMP approach (exemplified in the course notes and `main.R` which the authors cite) uses an accumulator variable `H` with `accumvars = "H"` in the SEIR object — but the SEIR `pomp()` calls never specify `accumvars`. The SIR model in the EDA section does use `accumvars = "H"`, indicating the authors were aware of this convention, but it is absent from the main SEIR model throughout the paper.

### 5. Global optimization produces a worse fit than local; no explanation or resolution

The paper notes that "global optimization is even less effective than local optimization" (§Global Search). This is a major warning sign that either the cost function surface is poorly behaved, the optimization hyperparameters are misconfigured, or the model itself is misspecified. The authors do not investigate this anomaly; instead, they abandon the global search result and manually re-specify a "Final SEIR Model" with hand-tuned parameters (beta=0.35, sigma=0.3, gamma=1/14, N=5000000, rho=0.5) with no justification. The final model is thus neither likelihood-maximized nor obtained by any reproducible optimization — it is an eyeball calibration, the least defensible approach for a mechanistic model.

### 6. No profile likelihoods and no uncertainty quantification for SEIR parameters

No confidence intervals, profile likelihoods, or any measure of parameter uncertainty is reported for the SEIR model. With five free parameters (beta, sigma, gamma, N, rho) fit to a single time series, identifiability is a serious concern — for example, beta/N and rho are known to be confounded in this class of models. The paper reports point estimates from optimization but never asks whether those estimates are identifiable or statistically meaningful. (Wheeler et al. 2024, §Parameter identifiability and uncertainty.)

### 7. EDA uses a SIR model on wrong data and draws unfounded conclusions

The three EDA code chunks (lines 30–330) download COVID-19 data from an external URL, aggregate by calendar week number (not epidemiological week), and build SIR models with fixed population N=1,000,000 and fixed parameters. The resulting simulation plots are described as showing "cyclical fluctuations" that are "not consistent with real-world scenarios," and the commentary interprets these as model problems. However, these models use calendar week grouping which double-counts observations when weeks span two calendar years, and the data source aggregates cumulative confirmed cases with `sum(confirmed)` rather than differencing to get new cases. The EDA section therefore analyzes the wrong quantity (cumulative sums, not incidence), yet draws epidemiological conclusions from these plots.

### 8. Data preprocessing double-differences the series

In the data preparation chunk (lines 610–649), the code first takes `confirmed - lag(confirmed)` to compute daily new cases, then groups by week with `sum(confirmed, na.rm = TRUE)` where `confirmed` is the raw cumulative column — not the differenced column — followed by a second differencing at lines 640–642: `new_confirmed = new_confirmed - lag(new_confirmed)`. This means the final `week.csv` contains second differences of cumulative confirmed cases, not weekly incidence. The description states "1500 data points from Washington State" but the resulting series is 160 weekly observations (line-count of `week.csv`). The modeling is therefore applied to a doubly-differenced series with unclear epidemiological meaning.

---

## Minor Issues

### 9. ARIMA model selection conclusion is inconsistent with the reported code

The text concludes that ARIMA(2,1,3) is chosen based on AIC (§Model selection, line 510), but the residual plots and fitted-values plot are generated from `arima(x = week_ts, order = c(3, 1, 1))` (line 513) — that is, ARIMA(3,1,1), not ARIMA(2,1,3). The text acknowledges comparing these two models but then presents diagnostics for the model that was not selected without stating this clearly. It is unclear which model is the "final" ARIMA model used for comparison with SEIR.

### 10. No random seeds set for SEIR simulations; results are not reproducible

The "Original model" and "Final SEIR Model" simulation chunks use `simulate()` with `nsim=1` and no `set.seed()`. Because a single stochastic trajectory is used to represent model fit, results will differ on each run, making figures non-reproducible. A seed is set only for the GenSA global search (`set.seed(123)` in the `main.R` file, not in the Rmd), and the local Nelder-Mead optimization has no seed.

### 11. Title inconsistency: paper describes SEIR but EDA section builds SIR models

The paper title is "Comparative Analysis of ARIMA and SEIR Models" but the EDA section constructs SIR models (with states S, I, R, H) for three states. The simulations in the EDA are labeled "Simulation of POMP Model with Hospitalization in California/Washington/New York" though there is no hospitalization compartment — H is just accumulated recoveries. This is misleading.

### 12. Population size N=5,000,000 for Washington State is biologically implausible given the data scale

Washington State's population is approximately 7.7 million. The initial model uses N=5,000,000, the local search converges to N≈5,031,249, and the final hand-tuned model uses N=5,000,000. Given that the paper states "1500 data points" and the data appear to show case counts in the range of tens of thousands per week during peak periods, a population of 5 million with `rho=0.5` implies roughly 2.5 million current infections at peak — biologically implausible. No justification is offered for the population size choice, and it is never estimated with uncertainty.

### 13. `main.R` file is unrelated course code from measles SIR example

The `main.R` file in the project folder contains the standard measles Consett 1948 SIR tutorial code from the course notes, not any code for the project's COVID-19 analysis. It is not referenced in the Rmd. This extraneous file increases confusion about what code belongs to the project and what represents the authors' own work.

### 14. Missing particle filter diagnostics and convergence evidence

The paper uses POMP infrastructure but never runs a particle filter evaluation (`pfilter`) to obtain a likelihood estimate, check effective sample size (ESS), or generate conditional log-likelihood plots. There is no evidence of convergence for any optimization — the Nelder-Mead trace plots show parameter trajectories but not the objective function value, so it is impossible to assess whether the 500-iteration budget was sufficient. (Wheeler et al. 2024, §Computational adequacy.)

### 15. Reference to ChatGPT for "code optimization and error correction" is noted but undocumented

Reference [6] cites ChatGPT for code optimization and error correction. Given the measurement-model errors described in Issue 3 above, it is unclear whether ChatGPT introduced or failed to catch these errors. More importantly, the specific changes made via AI assistance are not described, making the provenance of the code opaque and reproducibility harder to assess.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project04/main.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project04/week.csv`
