# Peer Review: W21 Project 01
**Title:** Investigating the Effects of Vaccinations and Government Policy on the Spread of COVID-19 in the State of Pennsylvania

---

## Summary

This project fits a SEIR-based compartmental POMP model to daily COVID-19 positive case counts in Pennsylvania from June 2020 to March 2021, incorporating time-varying infection-rate multipliers (as covariates) and a vaccination covariate that moves susceptibles directly into the recovered compartment. The authors use iterated filtering (IF2 via `mif2`) for parameter estimation and perform both a full-data global search and a smaller-window search on a restricted subset. While the project demonstrates genuine engagement with the POMP framework and makes a creditable attempt to model policy and vaccination effects, the analysis has critical methodological weaknesses: the accumulator variable is semantically misspecified, no profile likelihoods or convergence diagnostics are shown, the ARIMA comparison is not used as a quantitative benchmark for the POMP model, the global search lacks a guesses object in scope in the rendered code, the filtering results are sparse, and no forecast or future prediction is generated despite being stated as a goal. Several additional minor issues further undermine reproducibility and scientific credibility.

---

## Major Issues

### 1. Accumulator Variable Tracks Current Stock Rather Than Incident Flow

In the `seir_step` Csnippet, the accumulator `H` is assigned the current value of the infected compartment — `H = I` — at each Euler step. The pomp `accumvars` mechanism is declared for `H`, which means `H` is reset to zero after each observation time. However, `H = I` overwrites `H` with the stock at the *last sub-step* of the observation period, not the cumulative incidence during the period. As a result, `H` does not accumulate the flow `dN_EI` (new infections entering I) but instead takes a snapshot of I at the end of each day. The measurement model `dbinom(reports, H, rho)` therefore links reported cases to the current infected stock rather than to daily new confirmed infections. This is inconsistent with `positiveIncrease` (daily new positive tests), which is an incidence count, not a prevalence measure. The reporting-rate parameter `rho` will absorb an implicit ratio of prevalence to incidence, distorting all downstream parameter estimates. The correct formulation is to add `dN_EI` (or the analogous flow) to H cumulatively: replace `H = I` with `H += dN_EI` and remove the `accumvars` declaration (pomp's `accumvars` handles the reset automatically when the incremental pattern is used). This is a fundamental model misspecification that affects all presented results.

### 2. No Profile Likelihoods or Confidence Intervals Reported

Profile likelihoods are not computed for any parameter. The project reports a pairs scatter plot of the global search results but presents no profile likelihood curves, no MCAP intervals, and no confidence intervals for any parameter. Without profile likelihoods it is impossible to assess whether parameters such as Beta, rho, mu_IR, or eta are individually identifiable from the data. The authors acknowledge that the likelihood surface shows a ridge between Beta and mu_IR and that eta and mu_EI appear unidentifiable ("simulations do not help us in predicting the values of eta or mu_EI"), yet do not formalize this by computing profile likelihoods. Per Wheeler et al. (2024, §Parameter identifiability), profile likelihoods are necessary to determine whether point estimates are reliable and whether confidence intervals can be formed. This is a major omission.

### 3. No Convergence Diagnostics Presented

No convergence traces (log-likelihood vs. IF2 iteration, parameter values vs. iteration) are shown for either the full-data or the subset global search. The text acknowledges "large variations" in log-likelihood and poor convergence, but the absence of traces makes it impossible for a reader to judge whether any run has approached a stable optimum. Per Wheeler et al. (2024, §Computational adequacy), convergence diagnostics are a required component of any IF2-based analysis. Reporting only the final pairs scatter plot is insufficient; trace plots for the best runs from each search should be included.

### 4. ARIMA Comparison Not Used as a Quantitative Benchmark Against the POMP Model

The authors fit an ARIMA model and produce an AIC table, then conclude that "we observe no significant evidence that the ARIMA model performs better than white noise." This is used only to characterize the marginal ARIMA analysis, not as a quantitative benchmark against the POMP model. The POMP model's log-likelihood is never compared to the ARIMA log-likelihood. Per Wheeler et al. (2024, §Benchmark comparison), mechanistic models must be compared against non-mechanistic benchmarks on a common quantitative scale (log-likelihood or AIC). The direct comparison is absent, making it impossible to assess whether the SEIR model captures meaningful structure beyond what a simple statistical baseline achieves.

### 5. `guesses` Object Not Defined in Rendered Code

The global search code calls `foreach(guess=iter(guesses,"row"), ...)` but the `guesses` object is never constructed in any visible code chunk in the Rmd. The `fixed_params` object likewise appears in the `mif2` call without construction. The `stew` blocks load pre-cached `.rda` files if they exist, hiding the actual run, but without seeing the definition of `guesses` it is impossible to evaluate the box ranges, the number of starting replicates, or whether the global search was initialized from a proper multi-start design. This is a reproducibility failure: the code as written cannot be run from scratch without the missing definitions.

### 6. 500 Log-likelihood Evaluations from Only 500 IF2 Chains Is Computationally Unsound

The log-likelihood evaluation code (`lik_m2 <- foreach(i=1:500, ...) %dopar% logmeanexp(replicate(200, logLik(pfilter(..., Np=20000))), se=TRUE)`) iterates over `i=1:500`, suggesting 500 IF2 chains. For the smaller-data model the particle count drops to Np=5000. Running 500 chains with Nmif=500 each but no box definition visible implies either that all chains start from the same point (which is a local search, not global) or that the guesses object defines a box (which is not shown). Moreover, evaluating the log-likelihood for all 500 final-state chains with 200 replicate pfilters at Np=20000 is extremely expensive, yet no convergence evidence is shown to justify that the 500 chains actually represent different modes. The computational effort may be misallocated: fewer chains with more iterations and shown convergence traces would be more informative.

### 7. Vaccination Model Subtracts Immunized People from S Without Bounding

In `seir_step_mod_ver2`, the step function performs `S -= dN_SE + IM`, where `IM` is a covariate for daily fully-vaccinated individuals. No guard ensures that `S - dN_SE - IM >= 0`. If `IM` exceeds the current susceptible count (possible late in the vaccination campaign), `S` can go negative, corrupting the Euler trajectory and producing nonsensical binomial draws in subsequent steps (`rbinom(S, ...)` with S < 0 is undefined). A minimum clamp (`S = fmax(S - dN_SE - IM, 0.0)`) is required, or `IM` must be capped at `min(IM, S - dN_SE)`.

### 8. No Quantitative Goodness-of-Fit Reported

The project assesses model fit entirely visually: simulation bands are plotted against the data, and the text describes fit quality in qualitative terms ("fits poorly," "better reflects the shape"). No log-likelihood values are reported in the text for any model configuration — not the pre-covariate model, the covariate model, nor the vaccination model. Per Wheeler et al. (2024, §Quantitative goodness-of-fit reporting), visual comparisons are "only a weak and informal measure of goodness-of-fit." At minimum, the best log-likelihood found by the global search and the corresponding parameter values should be stated explicitly.

---

## Minor Issues

### 9. Measurement Model Semantic Issue: Binomial With H = I Rather Than Negative Binomial

The measurement model uses `dbinom(reports, H, rho)`. Given that `H = I` (the current infected stock, which may be large), and `rho` is estimated near 0.2 (from the pairs plot), the binomial parameterization treats the current infected pool as the number of Bernoulli trials. For a prevalence-based formulation this has some logic, but the data are daily counts that exhibit overdispersion (visible in the raw time series with irregular spikes). A negative binomial or overdispersed measurement model would be more appropriate. Per Wheeler et al. (2024, §Stochasticity), overdispersion in the measurement model is often needed for epidemic count data.

### 10. Covariate Multipliers Fixed by Hand Rather Than Estimated

The infection-rate multipliers (1.38 for post-September reopening, 0.89 for post-December restrictions) are chosen by assertion ("we believe...") with no statistical justification. While these are incorporated as fixed covariates rather than estimated parameters, the values are not derived from any optimization or sensitivity analysis. An alternative approach would be to estimate the multipliers (or the effective Beta at each phase) as free parameters via IF2, or at minimum to present a sensitivity analysis showing how conclusions change if the multipliers are varied.

### 11. Initial Condition for H Set to Zero but H Is Immediately Overwritten

In `seir_rinit`, `H = 0` is set as an initial condition. However, because `H = I` in the rprocess step, `H` is overwritten on the first sub-step. Combined with the `accumvars="H"` declaration, the initialization is semantically inconsistent: the accumvars mechanism resets H after measurement, but the first sub-step also overwrites it. This is a secondary manifestation of the accumulator semantic error described in Issue 1.

### 12. Data Filtering Cutoff Inconsistency

The introduction states that data from after "June 10th, 2020" are used, but the actual filter in the code uses `date > '2020-06-20'` (after June 20). A separate object `dat_init_pa` filters `date >= '2020-06-10'` to `date <= '2020-06-20'` for initial condition estimation. This ten-day window is used to set initial compartment sizes but is not included in the fitting data. The text does not clearly distinguish these two date cutoffs, creating potential confusion about what data the model is fitted to.

### 13. Smoothing of Vaccination Data Before Use as Covariate

Missing values in `people_fully_vaccinated` are filled by forward-carrying the last observed value, then a smooth spline is fitted to the result. The smoothed, non-integer daily vaccination increments are then used as the covariate `IM`. Since `IM` directly modifies S (an integer-valued state), the Euler step effectively applies fractional reductions to a discrete compartment. While this is a common approximation, the smoothing introduces artificial regularity into what should be a discontinuous administrative count series, and the forward-fill imputation during early weeks (when vaccination data is missing) introduces uncertainty that is unacknowledged.

### 14. No Forecast or Future Prediction Generated

The introduction states: "we will make a prediction on the future positive cases increase considering the same lock-down control and vaccination increase." No forecast is produced in the paper. The conclusions section also makes no quantitative prediction about future case trajectories. This stated goal is entirely unmet, and the methodology section that discusses the vaccination model as an "academic exercise" does not substitute for the promised prediction.

### 15. ARIMA Log-transformation and Smoothing Are Inconsistent With POMP Data

The ARIMA analysis is performed on `log(positiveIncrease + 1)`, with zero or near-zero values replaced by the average of neighboring values. The ARIMA log-likelihood and AIC apply to this transformed, preprocessed series and are not comparable to the POMP model's log-likelihood, which is evaluated on the raw integer counts via the binomial measurement model. Any cross-model comparison using these AICs would be invalid (per the sarima-baseline-audit framework).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-boundary-mle/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-domain-violation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project01/blinded.Rmd`
