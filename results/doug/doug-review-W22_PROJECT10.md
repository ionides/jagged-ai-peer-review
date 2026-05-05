# Peer Review: W22 Project 10
**Title:** Modeling South Africa Omicron Variant Cases
**Reviewer:** Doug
**Date:** 2026-04-13

---

## Summary

This project fits ARMA, SIR (POMP), and SEAPIRD (POMP) models to daily confirmed COVID-19 (Omicron) cases in South Africa from December 2021 through April 2022. The authors conduct exploratory data analysis, fit an ARMA(3,3) baseline, perform spectrum analysis identifying weekly periodicity, then build two mechanistic POMP models. Strengths include a genuine attempt to compare model families by log-likelihood, the inclusion of both local and global IF2 searches, and the use of a biologically motivated complex SEAPIRD model. However, the project is weakened by critical methodological errors in the SEAPIRD measurement model (including a normal distribution on a mixed observations variable, and an rmeasure that conflates case and death counts), inadequate computational effort (only 16 replicates with few particles), no profile likelihoods, an inconsistency in population size between local and global SIR searches, and an invalid direct log-likelihood comparison between ARMA and POMP models evaluated under different observation distributions.

---

## Major Issues

### 1. SEAPIRD rmeasure adds deaths to modeled cases, creating a mismatch between dmeasure and rmeasure

In the SEAPIRD `seapird_rmeas` Csnippet (line ~459), the simulated `cases` variable is computed as:

```c
cases = rnorm(mean_cases, sd_cases) + D;
```

However, in `seapird_dmeas` (line ~481), the density is evaluated as:

```c
lik = dnorm(cases - deaths, mean_cases, sd_cases, 0);
```

These two snippets define different effective observation models. The `rmeasure` adds the cumulative deaths compartment `D` to the simulated cases, while `dmeasure` subtracts the observed `deaths` column from observed `cases` before evaluating the likelihood. Whether `D` (a stock of cumulative deaths) equals observed `deaths` (which from the data construction in the EDA chunk is `death.new`, the daily death count) is not guaranteed, making the two snippets inconsistent. As documented in Wheeler et al. (2024), measurement model discrepancies between code and text are a concrete reproducibility and validity failure. All forward simulations, particle filter likelihood evaluations, and IF2-estimated parameters from the SEAPIRD model are suspect.

**Fix:** Decide on a single, consistent observation variable and distribution. If daily deaths are to be modeled, specify a separate dmeasure/rmeasure pair for deaths that uses the appropriate distributional family. Ensure that both `rmeasure` and `dmeasure` apply identical transformations to the same state variables.

---

### 2. Normal measurement model is poorly motivated and may be inappropriate for count data

The SEAPIRD model uses a normal distribution for reported cases:

```
Y_cases ~ Normal(rho * H, tau * rho * H * (1 - rho))
```

The authors justify this by noting that the case counts are "fairly large" and the mode is around 1925. However, a normal approximation to count data introduces two problems: (a) it can generate negative simulated counts (addressed in rmeasure by clamping to zero, but this creates a discrepancy with the density), and (b) the variance formula `tau * rho * H * (1 - rho)` mixes the over-dispersion parameter `tau` with the binomial variance structure `rho(1-rho)` in an unusual way that is not standard and is not explained. The negative binomial, used in the SIR model, is the standard choice for overdispersed count data and is appropriate even for large counts. The Gaussian approximation is especially problematic near zero (early epidemic stages) where the normal can assign substantial probability mass to negative values.

**Fix:** Replace the normal measurement model with a negative binomial. This is consistent with the SIR component of the paper and with best practice (Wheeler et al. 2024, §Measurement model specification).

---

### 3. No profile likelihoods: parameter identifiability is unassessed

The project fits 13 parameters in the SEAPIRD model (Beta, mu_IR, mu_ID, mu_EI, alpha, mu_AR, mu_PI, c_1, c_2, c_3, rho, tau, and fixed N). No profile likelihoods are computed for any parameter in either the SIR or SEAPIRD models. The SEAPIRD model in particular is highly parameterized: it includes three intervention multipliers (c_1, c_2, c_3) and separate asymptomatic and presymptomatic rates, all fitted to 156 data points. Without profile likelihoods or confidence intervals, there is no way to assess whether these parameters are identifiable from the data. The local and global best parameters for the SEAPIRD model differ substantially for several parameters (e.g., mu_AR: 0.180 vs 3.49; c_2: 1.59 vs 10.6; tau: 262000 vs 624000), suggesting the likelihood surface is flat or multimodal in these directions — precisely the situation where profile likelihoods are essential. This directly violates Wheeler et al. (2024) §Parameter identifiability and uncertainty.

**Fix:** Compute profile likelihoods for at least the key biological parameters (Beta, mu_IR, rho, eta/alpha) using `profile_design()` with multiple restarts per grid point and `logmeanexp` over at least 10 particle filter replicates. Report 95% confidence intervals via the MCAP procedure.

---

### 4. Population size inconsistency between SIR local and global searches

In the SIR global search (chunk `SIR_global_search`, line ~315), the `params` vector sets `N=500000`:

```r
params = c(apply(covid_box_sir, 1, function(x) runif(1, x[1], x[2])), N=500000)
```

However, the SIR model is initialized and the local search is run with `N=50000000` (50 million). The global search thus runs with a population 100 times smaller than the local search. The best global search log-likelihood is reported as -1677, substantially better than the local search value of -1997, but this improvement may simply reflect that `N=500000` better matches the observed case counts (up to ~38,000 daily in a population of 500,000 is a very high attack rate of ~7.6%, while in 50 million it is 0.076%). The global search may therefore not represent a genuine improvement in model fit but rather a different and possibly unrealistic population assumption. South Africa's population is approximately 60 million, making neither value well-justified.

**Fix:** Fix `N` to a biologically plausible value (South Africa population ~60 million) throughout both searches, and include it in the text as a fixed parameter with justification. If N is to be estimated, include it in the search box with a reasonable range.

---

### 5. Invalid direct log-likelihood comparison between ARMA and POMP models

The conclusion states: "SIR model is not that competitive comparing to the basic simple ARMA model, judging from the likelihood perspective." The ARMA(3,3) log-likelihood is reported as approximately -1442 (from `arma_33$loglik`) while the SIR POMP best log-likelihood is -1677 (global) and SEAPIRD achieves -1446. However, the ARMA model evaluates the likelihood under a Gaussian distribution on the observed count series, while the POMP models use negative binomial (SIR) or normal (SEAPIRD) measurement models on the same series. These likelihoods are not directly comparable: they are evaluated under different distributional families and the normalizing constants differ. Statements about one model being "better" than another based on these cross-family log-likelihood values have no valid statistical interpretation. Wheeler et al. (2024) recommend comparing mechanistic and non-mechanistic models using a proper benchmark with the same observation model.

**Fix:** Compare models on the same scale by either: (a) fitting the ARMA model within a POMP framework using the same negative binomial observation model, or (b) comparing all models using a proper scoring rule (e.g., CRPS) on held-out predictions. Alternatively, use AIC values from the same model class only for within-class comparisons.

---

### 6. Insufficient computational effort for reliable inference

The IF2 searches use 16 replicates for both local and global phases. The local SIR search uses only `Np=100` particles, which is extremely low for a model of this complexity. The SEAPIRD global search uses `Np=2500` and `Nmif=250`, which is more reasonable, but the conclusion explicitly states the log-likelihood "does not converge to a point." The authors interpret this as the model reaching a "bottleneck," but non-convergence is a computational failure, not a biological finding. The convergence traces for the SIR local search show wide variation across the 16 chains, consistent with insufficient exploration.

With `Np=100` for the SIR local search, particle degeneracy is likely at many time points, producing highly noisy likelihood estimates that bias the IF2 gradient signal. The reported `loglik.se` of 6.98 for the SIR local search (vs. 0.243 for the global) confirms that the local search likelihood estimates are extremely noisy — a standard error of 6.98 log-likelihood units renders the estimated log-likelihood essentially uninformative. Wheeler et al. (2024) note that "the large improvement in Model 1's log-likelihood was primarily attributed to increasing the computational effort" — this project needs the same attention.

**Fix:** Increase `Np` to at least 1000-2000 for local searches and 5000+ for profile likelihood evaluations. Run 50+ global search replicates. Use `logmeanexp` over at least 10 pfilter replicates for each final likelihood evaluation. Present convergence diagnostics showing that multiple chains reach similar log-likelihoods from different starting points.

---

### 7. No benchmark comparison for mechanistic models

The project fits mechanistic POMP models but never compares them against a non-mechanistic benchmark evaluated on the same scale. While ARMA is fitted, the comparison (Issue 5 above) is invalid due to different observation models. Wheeler et al. (2024) identify the benchmark comparison as the single most diagnostic check: "None of the 32 papers in their Haiti cholera literature review performed such a comparison." The SEAPIRD model achieves a log-likelihood of approximately -1446, barely different from the ARMA log-likelihood of approximately -1442, yet the SEAPIRD model has 13 free parameters vs. 7 for ARMA(3,3). This suggests the mechanistic model is not adding explanatory power beyond the statistical baseline.

**Fix:** Fit a negative binomial auto-regressive model with the same observation model as the SIR POMP component (negative binomial), and compare log-likelihoods directly. This provides a proper baseline for whether the mechanistic structure adds value.

---

### 8. Accumulator variable in SIR tracks recoveries, not new infections; interpretation should be clarified

In `sir_step`, the accumulator `H` increments as `H += dN_IR` — accumulating individuals who move from I to R (recoveries). The measurement model then links `reports ~ NegBin(rho * H, k)`. However, the observed data `confirmed.new` represents newly confirmed infections (daily new cases), not recoveries. Tracking recoveries to explain new case reports is a semantic mismatch: the reporting rate `rho` would absorb the ratio of recoveries to new infections, not a genuine detection probability. In a simple SIR model, the flows dN_SI (new infections) and dN_IR (recoveries) have similar magnitudes in steady state but diverge at epidemic peak and trough — using dN_IR to model new case detections will distort beta, gamma, and rho estimates.

A more appropriate accumulator for observed confirmed cases would be `H += dN_SI` (tracking new infections entering the infectious compartment).

**Fix:** Replace `H += dN_IR` with `H += dN_SI` in `sir_step`. Verify the change does not introduce other inconsistencies with the initial condition (where `H = 169` is set in `sir_rinit`).

---

## Minor Issues

- **Week-7 periodicity not incorporated in POMP models.** The spectrum analysis finds clear weekly periodicity in the data (period ~7 days), and the authors acknowledge this. However, neither the SIR nor SEAPIRD model includes a day-of-week effect in the observation model. This unmodeled periodicity will degrade particle filter performance and increase log-likelihood variance. A simple weekend/weekday reporting multiplier in dmeasure could address this.

- **SEAPIRD initial conditions set S = N without removing the initially infected.** In `seapird_init`, `S = N` is set while `I = 169` is also set, making `S + I > N` at time zero, which violates the population conservation constraint. The correct initialization should be `S = N - I` or `S = nearbyint(N - I)`.

- **H initialized to 169 in SIR rinit.** In `sir_rinit`, `H = 169` is set. Since `H` is declared in `accumvars`, it is reset to zero at each observation time automatically. Initializing H to 169 affects only the very first observation window, but the choice of 169 appears arbitrary and is not discussed. The correct initial value for an accumulator is 0 (or the number of reported cases on the first day, with justification).

- **Global SIR search uses `global_results_sir[1, ]` without sorting by log-likelihood.** The simulation shown after the global search uses `unlist(global_results_sir[1, ])` to get the "best" parameters, but there is no evidence that the results are sorted in descending log-likelihood order. The best parameters should be selected with `arrange(-loglik) %>% slice(1)`.

- **Log-likelihood convergence diagnostic is marked `eval=FALSE`.** The chunk `SIR_diag` containing the log-likelihood convergence trace plots for the SIR model is set to `eval=FALSE` and is not rendered in the output. These diagnostics are essential for assessing convergence and should be included in the rendered document.

- **No discussion of parameter estimates relative to scientific literature.** Beta = 0.932 and eta = 0.575 from the SIR global search, or beta = 2.56 and alpha = 0.0285 from the SEAPIRD global search, are not compared to any independent estimates of Omicron transmission parameters. Wheeler et al. (2024) §Corroboration with scientific knowledge requires checking parameter estimates for biological plausibility. For example, mu_IR = 0.0385/day from SEAPIRD implies a mean infectious duration of ~26 days, much longer than the typical 5-10 day Omicron infectious period.

- **Pairs plots use unfiltered results including non-finite log-likelihoods.** The pairs plots for both models combine local and global search results colored by type, but there is no filter for `is.finite(loglik)` on the global results (only applied to the local SEAPIRD results). Including -Inf log-likelihoods in the pairs plot will distort the axes.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stochastic-dmeas-intermediate/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-covid-active-case-stock-flow-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project10/blinded.Rmd`
