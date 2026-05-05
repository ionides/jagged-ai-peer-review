# Peer Review: W22 Project 04
## "An Analysis on COVID-19 Omicron Variant in Washtenaw"

---

## Summary

This project fits a custom recurrent SEPIR (Susceptible-Exposed-Potential-Infected-Recovered) compartmental model to daily COVID-19 case counts in Washtenaw County, MI from December 2021 through April 2022, using the pomp package with IF2 optimization. A SARIMA baseline is also constructed. While the epidemiological motivation for the recurrent and asymptomatic-branch model is sound and the project demonstrates familiarity with basic POMP workflows (local and global search, convergence trace inspection), several critical methodological errors undermine the validity of all reported inferential conclusions. These include a serious coding error in the rprocess step function (dN_RS draws from the wrong compartment), multiple fixed parameters with no scientific justification, a small-scale search that does not demonstrate convergence, no benchmark comparison quantified against the POMP model, no profile likelihoods, and an invalid direct comparison between the SARIMA and POMP log-likelihoods.

---

## Major Issues

### 1. Critical rprocess bug: dN_RS draws from I instead of R

In the `sepir_step` Csnippet, the transition from R back to S (reinfection / waning immunity) is coded as:

```c
double dN_RS = rbinom(I, 1-exp(-mu_RS*dt));
```

The first argument to `rbinom` (the pool size) should be `R`, not `I`. As written, the code draws the number of individuals moving from R to S as if they were drawn from the I (symptomatic infectious) compartment. This is logically contradictory: the return-to-susceptibility flow cannot come from I. Simultaneously, the subsequent state update compounds the error:

```c
S -= dN_SE - dN_RS;
```

This subtracts dN_RS from S (i.e., adds to susceptibles) but the value was drawn from I. The I compartment is never decremented by dN_RS, so the individuals "removed" from I to create dN_RS are not actually removed from I in the state update — they are neither removed from I nor correctly added to S in a mass-balance sense. This is equivalent to fabricating individuals. All parameter estimates (particularly mu_RS, which controls the rate of this erroneous flow, and rho, which is calibrated against the resulting incorrect dynamics) are invalid.

**Fix:** Replace `rbinom(I, ...)` with `rbinom(R, ...)` and ensure the state update correctly decrements R: `R -= dN_RS + dN_PR + dN_IR; S += dN_RS;`. Re-run all inference after the correction.

---

### 2. No benchmark comparison against a non-mechanistic model

The project fits a SARIMA model and a POMP model but does not compute a quantitative comparison (log-likelihood or AIC) between them on the same scale. The Summary section states that "both models can fit the data well" and "POMP model can explain the data better," but no quantitative evidence for the superiority of the POMP model over the SARIMA baseline is provided. Without a benchmark comparison evaluated on the same observation model and data, it is impossible to assess whether the mechanistic structure captures information beyond a simple statistical time-series model. This is the single most diagnostic check for mechanistic models (Wheeler et al. 2024, §Benchmark comparison).

**Fix:** Evaluate both models on the same log-likelihood scale or use a proper scoring rule (e.g., CRPS on out-of-sample observations). Alternatively, compute the ARIMA log-likelihood under a comparable observation model. At minimum, report the SARIMA AIC from the fitted `arima` object and note explicitly that the two log-likelihoods are not directly comparable due to different observation models.

---

### 3. Direct comparison of SARIMA and POMP log-likelihoods is invalid

The project implies (through the Summary) that the POMP model "fits the data better" than SARIMA. The SARIMA log-likelihood is evaluated under a Gaussian distribution on the differenced data, while the POMP log-likelihood is evaluated under a normal approximation applied to the original count data. These are different observation models on different data transformations; numerical comparison of the two values is statistically invalid. Any conclusion about relative model adequacy based on these numbers is ungrounded (see sarima-baseline-audit skill).

**Fix:** Either: (a) report that the two likelihoods are not comparable and refrain from ranking the models, or (b) evaluate both models under a common observation model on the original (non-differenced) data scale.

---

### 4. No profile likelihoods; parameter identifiability not assessed

No profile likelihoods are computed for any parameter. With 15 parameters (of which only 5 are fixed), and a dataset of approximately 126 observations, identifiability of the full parameter vector is not guaranteed. The pairs plots from the global search show the joint distribution of parameter values across runs, but these are not profile likelihoods and do not provide valid confidence intervals. The authors note that the global search pairs plots suggest "narrow" parameter ranges compatible with the data, but this interpretation is informal and does not substitute for a proper profile likelihood analysis (Wheeler et al. 2024, §Parameter identifiability and uncertainty).

**Fix:** Compute profile likelihoods for at minimum the key epidemiological parameters (Beta, rho, alpha, mu_EPI, mu_RS). Use profile_design() with the target parameter fixed across a grid and IF2 optimization over the remaining parameters at each grid point.

---

### 5. Multiple key parameters fixed without scientific justification

Five parameters are fixed throughout the analysis: N (population), mu_PR, mu_IR, alpha, and Beta in the global search (and additionally mu_RS from the local search result). The text offers "recovery rates can be obtained from statistics" as justification for fixing mu_PR and mu_IR, but does not cite any source, report the values used, or assess sensitivity to these choices. For Beta (the baseline transmission rate), no justification is given at all. Fixing parameters without justification inflates confidence in the remaining estimates and can bias them substantially if the fixed values are incorrect.

**Fix:** Cite sources for each fixed parameter value, report the values used, and perform at minimum a brief sensitivity analysis (e.g., re-run the global search at a 2x and 0.5x perturbation of each fixed parameter value to assess how strongly the other estimates depend on these assumptions).

---

### 6. Insufficient computational scale; convergence not demonstrated

The local search uses 10 replicates with Np=2000 and Nmif=200. The global search uses 10 replicates with Np=5000 and Nmif=200. Ten replicates is a small number for a 10-dimensional free-parameter space, and there is no evidence that the global search is achieving genuine global coverage. The convergence trace plots show that parameter mu_EPI has a "convergence problem" (the authors' own words), yet this is not treated as a major concern. Wheeler et al. (2024, §Computational adequacy) demonstrate that insufficient replicates can make a good model appear to have a worse likelihood than achievable; the improvement from local to global search (-803 to -768) is small and does not confirm that the global maximum has been found.

**Fix:** Increase the number of global search replicates to at least 20-30, and present the likelihood surface across all replicates (as a histogram of log-likelihoods and as a scatter of converged log-likelihoods vs. starting values) to demonstrate that multiple replicates are reaching the same optimum.

---

### 7. Accumulator variable H tracks the wrong flow for the observation data

The observation data records daily confirmed cases, which represent newly symptomatic individuals entering state I (or equivalently, transitions from E to I). However, the accumulator H is updated as `H += dN_IR` — it accumulates transitions from I to R (recoveries), not new infections. The measurement model then links reported cases to H:

```
double mean = rho * H;
```

This means the model attempts to fit the number of daily reported cases to the number of recovered individuals, not to the number of newly infected. For a disease with a finite infectious period, these quantities are proportional in steady state but differ during growth and decline phases. This is a systematic mismatch between the observation model and the data-generating process (pomp-accumvar-semantic-audit skill).

**Fix:** Change `H += dN_IR` to `H += nearbyint((1-alpha)*dN_EPI)` (new symptomatic cases entering I from E), which correctly accumulates new detectable infections. Re-run all inference after the correction.

---

### 8. Measurement model: normal approximation with potentially non-positive support

The dmeasure Csnippet uses a normal distribution to model count data:

```c
double mean = rho*H;
double sd = sqrt(pow(tau*H,2) + rho*H);
lik = pnorm(reports+0.5, mean, sd, 1, 0) - pnorm(reports-0.5, mean, sd, 1, 0) + tol;
```

This continuity-corrected normal approximation is a reasonable choice for large counts, but can assign non-trivial probability mass to negative values when H is small (early and late in the observation window). More critically, when H=0 (which occurs under many parameter settings), mean=sd=0 and the likelihood for any non-zero observed report is zero (except for the tolerance), causing particle degeneracy. The tolerance `tol=1e-25` is effectively zero in log space and does not protect against this degeneracy. The use of a negative binomial measurement model would be more appropriate for count data (Wheeler et al. 2024, §Stochasticity).

**Fix:** Replace the normal approximation with a negative binomial measurement model: `lik = dnbinom_mu(reports, 1/tau, rho*H, give_log)`, which is natively non-negative and handles overdispersion without the degeneracy problem.

---

### 9. Global search box excludes key parameters without justification; mu_RS fixed at local search value

The global search fixes mu_RS at 1.529 (obtained from the local search) rather than including it in the search box. The stated reason — "if we do not fix this value, mu_RS will explode to more than 7, which is not possible" — reflects an unresolved parameter identifiability problem rather than a scientific constraint. Fixing a parameter at a value found by local search and then conducting a "global" search is circular: the global search cannot explore the parameter space freely. Additionally, the value mu_RS=1.529 implies a half-life of ~0.45 days for immunity, which is biologically implausible (COVID-19 immunity typically lasts months to years). The fact that mu_RS "explodes" during optimization is itself a strong signal of model misspecification that should be diagnosed rather than suppressed by fixing the parameter.

**Fix:** Investigate why mu_RS diverges during optimization. Consider whether the recurrence mechanism is identified by the current data. If the reinfection timescale cannot be reliably estimated from a ~4 month window, consider fixing mu_RS at a biologically plausible value with a literature citation, or removing the recurrence branch and comparing model likelihoods.

---

### 10. Model diagnostics (conditional log-likelihoods, ESS) not examined

The text notes that "the particle fails some time between time 110 and time 120, they recover soon" in the effective sample size plot but does not investigate what causes this failure or whether it indicates model misspecification. Particle filter failure (ESS dropping near zero) for several consecutive time steps can substantially bias the log-likelihood estimate and invalidate parameter estimates for that period. Wheeler et al. (2024, §Model diagnostics) recommend plotting conditional log-likelihoods per observation to identify periods of poor fit; this is not done here.

**Fix:** Plot the conditional log-likelihood per observation time (extracted from the pfilter output). Identify which specific observations are driving the particle filter failure and investigate whether they correspond to anomalous reporting patterns (e.g., holiday reporting spikes) or genuine model-data conflict.

---

## Minor Issues

- **Typo in state variable description**: The description of $I_t$ is duplicated: one bullet says "$I_t$: the number of people at time $t$, who have been infected and are showing symptoms" and the very next bullet also begins "$I_t$: the number of recovered at time $t$." The second should clearly be "$R_t$."

- **Intervention indicator has a gap at time 35**: The intervention indicator loop assigns values for i<=34 and i>35, leaving i=35 with value 6 (the else branch). This is likely unintentional and may affect a single day's transmission rate in the model.

- **rho near 1 interpretation**: The text states that rho near 1 "means most people in state I are reported," but given the accumulator error (issue 7 above — H tracks recoveries, not new infections), this interpretation of rho is incorrect; rho actually compensates for the ratio of recoveries to new infections per time step.

- **SARIMA model: period consistency**: The AIC grid search fits SARIMA models with `seasonal = list(order = c(1,0,0), period=7)`, and the final model uses the same period. The data sampling frequency is daily and weekly seasonality is plausible; the period=7 specification is consistent within the grid search. No issue detected here beyond the general benchmark invalidity noted in Major Issue 3.

- **No out-of-sample validation or forecast**: For a pandemic model with evident policy relevance, no forecast is presented. The Summary notes rising cases in April 2022 as a public concern but does not use the fitted model to project forward. While not a methodological error per se, a short-term forecast conditioned on the filtering distribution would substantially strengthen the scientific contribution (Wheeler et al. 2024, §Forecast methodology).

- **Initial conditions largely fixed**: E=100, I=200, P=50 are hard-coded in `sepir_init`, while only eta (and by implication S and R) is estimated. Sensitivity to these fixed values is not assessed. Wheeler et al. (2024, §Initial conditions) note that initialization strategy can affect AIC by tens of units.

---

## Meta-Skill Reflection

This review identified a specific code error: the `dN_RS = rbinom(I, ...)` bug, which draws the pool of R-to-S transitions from the I compartment rather than the R compartment. This is a variant of the wrong-hazard-variable error (covered by `pomp-rprocess-wrong-hazard-variable`) but differs in that it affects the *size* argument of `rbinom` rather than the *prob/hazard* argument — the compartment being depleted is misidentified, not the force driving the depletion. The existing skill covers the hazard rate variable; it does not explicitly cover the case where the *pool* (size argument) is the wrong compartment. This pattern may recur in models with multiple recovery or waning compartments.

Additionally, the combination of (a) accumulator variable tracking recoveries (dN_IR) rather than new infections, and (b) the rprocess bug making dN_RS draw from I, creates a compound error that is difficult to diagnose from output alone because the simulations still produce vaguely plausible trajectories. The existing `pomp-accumvar-semantic-audit` skill covers part (a). No existing skill explicitly covers the `rbinom(wrong_pool, ...)` pattern as a distinct error type from hazard variable errors.

A new skill `pomp-rbinom-pool-variable-error` could be created to detect cases where the `size` argument of a `rbinom` call in an rprocess Csnippet references the wrong compartment (i.e., a compartment other than the one being depleted by that transition). However, on reflection, this pattern is closely related to the existing `pomp-rprocess-wrong-hazard-variable` skill — both involve referencing the wrong state variable in a transition draw. The existing skill can be naturally extended to cover both the hazard rate and the pool size arguments. No new skill is created; the finding is noted as a potential extension to the existing skill.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rprocess-wrong-hazard-variable/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project04/blinded.Rmd`
