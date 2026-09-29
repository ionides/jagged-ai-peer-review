# Peer Review: W24 Project 04
## "Comparative Analysis of ARIMA and SEIR Models Using COVID-19 Data"

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | Ad hoc: sum-of-squared-differences minimization via Nelder-Mead (`optim`) and simulated annealing (`GenSA`); no particle filter or iterated filtering |
| **R packages used** | `pomp`, `tidyverse`, `ggplot2`, `GenSA`, `doFuture`, `forecast`, `lubridate` |
| **Code publicly available** | Partial — Rmd and week.csv in repository; EDA data downloaded from external URL at runtime |
| **Data publicly available** | Partial — `week.csv` committed; EDA data from `covid19datahub.io` URLs |
| **Benchmark comparison included** | No (qualitative mention only; no quantitative log-likelihood comparison) |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ✗ | SSE minimization used, not likelihood |
| 2 | Benchmark comparison | ✗ | No quantitative comparison between ARIMA and SEIR |
| 3 | Quantitative goodness-of-fit reporting | ✗ | No log-likelihood or AIC reported for SEIR |
| 4 | Model diagnostics | ✗ | No particle filter diagnostics; no ESS, no conditional log-likelihoods |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods, no confidence intervals |
| 6 | Computational adequacy | ✗ | No mif2/pfilter; SSE optimizer with no convergence evidence |
| 7 | Forecast methodology | N/A | No forecasting performed |
| 8 | Model variations and nested comparisons | ✗ | No systematic model comparison |
| 9 | Stochasticity | ~ | Stochastic process model, but deterministic SSE fitting undermines it |
| 10 | Reproducibility and extendability | ~ | week.csv committed; EDA relies on live URL downloads |
| 11 | Corroboration with scientific knowledge | ~ | Population N unjustified; parameter values not compared to epidemiological literature |
| 12 | Measurement model specification | ✗ | Wrong dnbinom parameterization; stock/flow mismatch |
| 13 | Initial conditions | ~ | Initial conditions fixed without sensitivity analysis |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

This project applies ARIMA and SEIR models to weekly COVID-19 case data from Washington State to ask whether the SEIR model provides a better fit than ARIMA for infectious disease dynamics. The ARIMA section performs AIC-based model selection and presents residual diagnostics. The SEIR section constructs a `pomp` object but then fits it using sum-of-squared-differences (SSE) minimization rather than likelihood-based inference, and presents only visual trajectory comparisons. The paper contains multiple critical methodological failures: the SEIR model is not fit by likelihood, the measurement model is mathematically incorrect, the model conflates prevalence (I) with incidence, and the ARIMA model actually fitted in the code differs from the one selected by AIC.

**Strengths:**
- The project addresses a scientifically motivated question and uses a relevant dataset.
- The ARIMA section includes an AIC table, residual plots, ACF, and a QQ-plot, demonstrating awareness of standard diagnostics.
- The SEIR model specification in the text is clearly written with the mathematical transition equations presented.

**Weaknesses:**
- SEIR parameters are fit by SSE minimization, not likelihood — the entire POMP inferential framework is bypassed.
- The measurement model (`seir_dmeas`) uses an incorrect `dnbinom` parameterization, and measures current infectious prevalence (I) against weekly incidence data.
- The ARIMA model fitted in the code (`order = c(3,1,1)`) contradicts the AIC-selected model (`ARIMA(2,1,3)`).
- No log-likelihood values, profile likelihoods, convergence diagnostics, or uncertainty quantification are provided for the SEIR model.

---

## Major Issues

### 1. Ad hoc SSE calibration instead of likelihood-based inference

The SEIR model is fit by minimizing the sum of squared differences between observed and simulated case counts (via `cost_function` in the local and global search sections). The objective function is:

```r
cost_function <- function(params) {
  sim <- simulate(seir_pomp, params = params, nsim = 1, format = "data.frame")
  sum((sim$cases - data$cases)^2)
}
```

This approach violates the foundational principle of POMP inference. The likelihood is defined (and evaluated) by the `dmeasure` function already specified in the `pomp` object, yet the paper never calls `pfilter` or `mif2`. SSE minimization on a single stochastic simulation is both statistically incorrect (it minimizes the wrong criterion) and extremely noisy (a single simulation trajectory can vary substantially across calls). The course standard is likelihood maximization via `mif2` followed by replicated `pfilter` evaluation. Without likelihood-based inference, formal model comparison, uncertainty quantification, and convergence assessment are all impossible. (Wheeler et al. 2024, §Likelihood-based inference)

**Fix:** Replace the `optim`/`GenSA` SSE optimization with `mif2` iterated filtering, and evaluate the log-likelihood using replicated `pfilter` calls following the course standard.

---

### 2. Incorrect measurement model parameterization

The `seir_dmeas` function in all three SEIR model versions is:

```c
lik = dnbinom(cases, I, rho, give_log);
```

In R's `dnbinom(x, size, prob, ...)`, this sets `size = I` (the current count of infectious individuals) and `prob = rho` (the reporting rate). This is not a standard epidemiological measurement model. The size parameter of the negative binomial should be a fixed overdispersion parameter (conventionally `k`), not the time-varying state variable `I`. The correct form, consistent with the EDA SIR section and the course standard, would be `dnbinom_mu(cases, k, rho*I, give_log)` with a separate shape parameter `k`. As written, the variance of reported cases would scale with `I^2`, which is not epidemiologically motivated and will produce pathological likelihood behavior during filtering.

The `rmeasure` for the SEIR model uses `rbinom(I, rho)`, which is a binomial draw — inconsistent with the negative-binomial `dmeasure`. This means the measurement model used for simulation differs from the one used for likelihood evaluation. (Wheeler et al. 2024, §Measurement model specification)

**Fix:** Introduce an overdispersion parameter `k`, rewrite `seir_dmeas` as `dnbinom_mu(cases, k, rho*I, give_log)`, and rewrite `seir_rmeas` as `rnbinom_mu(k, rho*I)`.

---

### 3. Measurement model conflates prevalence with incidence

The data variable `cases` is derived from `new_confirmed` (weekly new confirmed cases), which is an incidence measure — a flow of new events per week. The measurement model, however, conditions on `I`, the current count of infectious individuals (a prevalence stock). These are fundamentally different quantities and should not be equated.

The standard course approach for this situation is to add an accumulator variable `H` (tracking new recoveries or new infections between observation times) using `accumvars`, and condition the measurement model on `H` rather than `I`. The EDA SIR section uses this pattern correctly (`accumvars = "H"`), but the SEIR section omits it entirely. This mismatch means the likelihood function is computing the probability of observing incidence counts under a prevalence distribution, producing systematically wrong parameter estimates regardless of the optimization method. (POMP Checklist #12; Wheeler et al. 2024)

**Fix:** Add an accumulator variable (e.g., `C` for cumulative incidence) to the SEIR step function, set `accumvars = "C"` in the `pomp()` call, and use `C` in `seir_dmeas`.

---

### 4. ARIMA model fitted in code contradicts model selected by AIC

The AIC table analysis (Section "Model selection") concludes that "ARIMA(2, 1, 3) achieve the smallest AIC value 3983.290." However, the subsequent code fits:

```r
arima_model <- arima(x = week_ts, order = c(3, 1, 1))
```

This is `ARIMA(3,1,1)`, not the AIC-selected `ARIMA(2,1,3)`. All subsequent diagnostics (residual plot, ACF, QQ-plot, and fitted value figure) are computed for `ARIMA(3,1,1)`. The stated conclusion that the selected model fits well is therefore unsupported — the diagnostics apply to a different model than the one chosen. This is a direct inconsistency between analysis and reporting.

**Fix:** Fit `arima(week_ts, order = c(2,1,3))` and recompute all diagnostics for the model actually selected by AIC.

---

### 5. No quantitative goodness-of-fit reported for the SEIR model

No log-likelihood values, AIC, or any other quantitative fit measure is reported for the SEIR model at any stage (initial, locally optimized, globally optimized, or final manual model). The comparison between ARIMA and SEIR is conducted entirely by visual inspection of simulated trajectories against observed data. Wheeler et al. (2024) explicitly state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." Without numerical fit statistics, the paper's central question — whether the SEIR model provides a better fit than ARIMA — cannot be answered. (POMP Checklist #3; Error 1.4)

**Fix:** Compute and report log-likelihood values for the SEIR model using replicated `pfilter` calls (with `logmeanexp`), and compare them numerically to the ARIMA log-likelihood.

---

### 6. No convergence diagnostics for iterated fitting

Neither the local search (`optim` with Nelder-Mead) nor the global search (`GenSA`) provides evidence of convergence to the global optimum of the SSE objective (let alone the likelihood). The trace plots shown track parameter values across iterations of the SSE optimizer, not likelihood values. There are no replicated searches from diverse starting points, no evidence that different starting values yield consistent terminal SSE values, and no particle filter convergence traces. The course standard requires multiple searches from different starting points reaching similar likelihoods. Without this, there is no basis for trusting the parameter estimates. (Error 1.8; POMP Checklist #6)

**Fix:** Use `mif2` with replicated searches from diverse starting values, show log-likelihood traces across iterations, and demonstrate that multiple runs converge to similar likelihoods.

---

### 7. No parameter identifiability or uncertainty quantification

No profile likelihoods are computed for any SEIR model parameter. No confidence intervals are reported. The paper presents point estimates from SSE minimization without any assessment of whether the parameters are identifiable from the data. Given that the SEIR model has five free parameters (beta, sigma, gamma, N, rho) fitted to weekly case data from a single state, identifiability is a genuine concern that the authors do not address. (POMP Checklist #5)

**Fix:** Compute profile likelihoods for at least the key epidemiological parameters (beta, gamma, sigma) and report confidence intervals using the MCAP method or the standard Wilks threshold.

---

### 8. No quantitative comparison between ARIMA and SEIR (no benchmark)

The paper's stated research question is whether the SEIR model provides a better fit than ARIMA. However, the comparison is qualitative throughout. The conclusion ("the SEIR model still fell short of the ARIMA model in terms of fitting precision") is based on visual comparison of trajectory plots, not log-likelihood or AIC values. Since both models are evaluated on the same observed data, their log-likelihoods are directly comparable. Without numerical fit statistics, the research question is unanswerable. (POMP Checklist #2; Error 1.6)

**Fix:** Report log-likelihoods for both models on the same dataset and compare numerically. The ARIMA log-likelihood is available from `arima_model$loglik`.

---

## Computational and Diagnostic Assessment

**Convergence:** No iterated filtering (mif2) is used. The Nelder-Mead and GenSA optimizers minimize SSE, not log-likelihood. The parameter trace plots shown are from SSE optimization and do not indicate likelihood convergence. No replicated searches from different starting values are performed. There is no basis for claiming the optimizer found a global or near-global solution.

**Particle filter:** `pfilter` is never called. No ESS values are reported. No conditional log-likelihoods are shown. The particle filter — the computational core of POMP inference — is entirely absent from the analysis.

**Conditional log-likelihoods:** Not computed or shown.

**Profile likelihoods:** Not computed. No confidence intervals are reported for any parameter.

**Computational scale:** Not reported. The GenSA search uses `max.call = 500` iterations, which is extremely low for a 5-parameter global search.

---

## Reproducibility Assessment

**Code availability:** The Rmd file and `week.csv` are in the repository. The `main.R` file contains only course example code (Measles/Consett data from the course notes) unrelated to the project analysis, suggesting it was not used in the final project.

**Final parameters:** The locally optimized parameters (`beta = 1.1305`, etc.) and the manually chosen final parameters (`beta = 0.35`, etc.) are hard-coded in the Rmd. They are not archived as separate files. The global optimization result is printed inline but not committed as a file.

**Model-code consistency:** The measurement model in the text describes a reporting rate rho, but the code uses `dnbinom(cases, I, rho, give_log)` which is not a standard reporting-rate formulation. The rmeasure for the SEIR model (binomial draw `rbinom(I, rho)`) is inconsistent with the dmeasure (negative binomial).

**Package versions:** No `sessionInfo()` output is provided. No package versions are pinned via `renv` or similar.

**Auxiliary data:** The EDA section downloads data live from external URLs (`https://storage.covid19datahub.io/location/...`). These URLs are not guaranteed to remain stable, creating reproducibility risk. The `week.csv` file used in the SEIR section is committed, which partially mitigates this.

**HPC reproducibility:** Not applicable; the analysis runs locally.

---

## Minor Issues

- **Title mismatch:** The paper title says "SEIR Models" but the EDA section (the first three simulation plots) implements a SIR model with an H (hospitalization) accumulator, not a SEIR model. The title should reflect which model is actually used in each section.

- **Final SEIR model uses hand-tuned parameters:** The "Final SEIR Model" section uses manually chosen parameters (`beta = 0.35`, `sigma = 0.3`, `gamma = 1/14`, `N = 5000000`, `rho = 0.5`). These are not derived from any optimization procedure. The text says "Based on the locally optimized parameter data, we again tuned..." but the locally optimized parameters differ substantially. The basis for these final values is not explained.

- **Population parameter N lacks scientific justification:** Washington State's population in 2020 was approximately 7.7 million. The model uses N = 5,000,000 as the initial value without justification. The local search recovers N = 5,031,249 and the global search recovers N = 8,830,174. The discrepancy between these estimates and actual population is not discussed.

- **ChatGPT cited as reference:** Reference [6] ("Code optimization and error correction, https://chat.openai.com/") is not a standard academic reference. Use of AI tools may be disclosed in an acknowledgments section with a description of what was used and how, but listing it as a numbered literature reference is inappropriate.

- **rmeasure inconsistency between local and global search sections:** In the local search section, `seir_rmeas` is `rbinom(I, rho)` (binomial). In the global search section, a new `rmeasure` is defined as `cases = nearbyint(I)` (deterministic rounding of I). These are two different stochastic simulation models used at different points in the analysis without explanation.

- **Residual spike around 2022 not investigated:** The text notes "the residuals suddenly increase around 2022" in the ARIMA section but offers no analysis. For COVID-19 data, this spike likely corresponds to the Omicron wave. Whether this represents a limitation of the ARIMA model or a structural change in the data generation process is a substantive question that deserves investigation (e.g., testing for a structural break, examining whether an ARIMA model with intervention variables or a segmented model improves fit).

- **EDA SIR plots labeled as "SEIR":** The three EDA simulation plots are labeled "Simulation of POMP Model with Hospitalization" (in California, Washington, New York). The models here are SIR+H, but the EDA section introduces these as if they are part of the SEIR analysis. The connection between the EDA and the subsequent SEIR model is not explained — the EDA uses different data (cumulative confirmed cases summed over weeks vs. weekly new confirmed cases) and a different model structure.

---

## Recommendation

**Reject / Major Revision.** The paper contains multiple fundamental methodological errors that prevent the stated research question from being answered. The SEIR model is not fit by likelihood-based inference (the core POMP methodology taught in the course); the measurement model is mathematically incorrect; the model conflates prevalence with incidence; and the ARIMA model discussed in the text is not the one fitted in the code. None of the course-standard POMP inference tools (mif2, pfilter, profile likelihood) are applied. For the paper to support any conclusion about SEIR vs. ARIMA model fit, these issues must be resolved before any scientific conclusions can be drawn.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project04/main.R`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project04/week.csv`
