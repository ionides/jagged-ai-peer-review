# Peer Review: W24 Project 05
**Modeling Flu Cases in Oklahoma — SEIRS POMP Model**

---

## Summary

This project applies time series methods to weekly influenza case counts in Oklahoma (2011–2015), fitting a SARIMA baseline and a SEIRS POMP model with seasonally-forced transmission. The work is clearly motivated, uses the `pomp` package appropriately, and demonstrates effort with six iterative global searches on the cluster. The key conclusion — that the SEIRS POMP model underperforms the SARIMA baseline and should not be the preferred approach — rests on a log-likelihood comparison that is undercut by a bug in the SARIMA model selection grid search and by the absence of formal profile likelihoods. Several additional issues with model specification, convergence documentation, and parameter interpretation limit the strength of the conclusions.

---

## Major Issues

### 1. SARIMA Grid Search Used the Wrong Seasonal Period

The AIC table for seasonal model selection is computed with `period=12` (hard-coded inside `get_aic_table_sarma`), but the final selected model is fit with `period=52`. The report explicitly labels the comparison as "SARIMA((1,1,1)×(P,1,Q)_[52])" but the grid search code contains `seasonal=list(order=c(Pi, 1, Qi), period=12)`. A 12-week seasonal period corresponds to quarterly structure, not annual flu seasonality. The winning seasonal order (0,1,1) was selected under the wrong period specification; the optimal seasonal order at period=52 may differ. The AIC values in the table in the report are for a model the authors do not ultimately fit, making the model selection step invalid.

**Fix:** Rerun the grid search with `period=52` throughout and re-select the seasonal order from the correctly-specified table.

---

### 2. Proper Profile Likelihoods Are Absent; Poor Man's Profiles Are Not a Substitute

The authors explicitly acknowledge they could not compute profile likelihoods (Section "Profile Likelihood"). The "poor man's profiles" presented are scatter plots of global search results across parameter values, not proper profiles. A proper profile for parameter θ requires re-optimizing all other parameters at each fixed value of θ. The scatter plots presented here hold other parameters at whatever value was reached by the iterated filtering algorithm from that particular starting point — this is a likelihood slice, not a profile (Error 1.2, CC-Yes, Major). Slices are narrower than profiles and cannot be used to construct valid confidence intervals. Without proper profiles, no uncertainty quantification is available for any of the 13 estimated parameters, and identifiability cannot be assessed.

**Fix:** Compute proper profile likelihoods for at least the key parameters (Beta0, amp, phase, rho) using fixed-parameter mif2 sweeps with re-optimization at each profile point.

---

### 3. H Accumulator Tracks Recoveries, Not New Infections

The accumulator variable H is incremented by `dN_IR` (transitions from I to R), so the observation model links observed cases to the number of newly recovered individuals per week. CDC ILI data captures new clinical presentations, which correspond more closely to newly exposed or newly symptomatic individuals (transitions S→E or E→I). Connecting reported cases to recoveries introduces a systematic temporal lag — the observation peak is shifted relative to the infection peak by the duration of the infectious period. This misalignment between the observation process and the data-generating process could systematically bias parameter estimates, particularly mu_IR (the recovery rate) and rho (the reporting fraction).

**Fix:** Change `H += dN_IR` to `H += dN_EI` (or `dN_SE`) to align the accumulator with the timing of clinical presentation, and recheck parameter estimates.

---

### 4. No Convergence Trace Plots for the Global Search mif2 Runs

The report shows a trace plot for the local search, but the global search — which produces the final parameter estimates used for all conclusions — does not include any convergence diagnostic traces. The pair plots shown for each of the six global searches confirm only the distribution of terminal parameter values; they do not show whether the mif2 algorithm's log-likelihood trajectory converged upward within each run. Without trace plots for the global search, there is no evidence that the global search mif2 runs found the MLE rather than a local maximum. (Error 1.8, CC-Yes, Major)

**Fix:** Add trace plots (`mifs %>% traces() %>% melt() %>% ...`) for at least the final global search (Search 6), showing both the loglik panel and parameter panels across iterations.

---

### 5. Unused Parameter 'eta' in paramnames

The `pomp` object is constructed with `paramnames = c("Beta0", "amp", "phase", "mu_EI", "mu_IR", "mu_RS", "N", "S0", "E0", "I0", "R0", "rho", "k", "eta")` in the initial SEIRS specification, and `eta` also appears in the manually-specified parameter vector (line `params <- c(Beta0 = ..., eta = 0.05, ...)`). However, `eta` is never referenced in any Csnippet — not in `seirs_step`, `seirs_rinit`, `seirs_dmeas`, or `seirs_rmeas`. This is a ghost parameter: it occupies a slot in the parameter vector, participates in optimization bookkeeping, and is recorded in result CSVs, but has no effect on the model. The retained version of the model (with negative-binomial measurement and sinusoidal forcing) still lists `eta` in `paramnames` but never uses it.

**Fix:** Remove `eta` from `paramnames` and from all parameter vectors.

---

## Minor Issues

### 6. logmeanexp SE Not Reported for pf_local

The log-likelihood after the local search is reported as `round(logmeanexp(logLik(pf_local)), 3)` — a bare point estimate with no standard error. The course-standard pattern is `logmeanexp(..., se=TRUE)` to obtain and report the Monte Carlo standard error alongside the estimate (Error 1.4, CC-Yes, Major for inference comparisons; Minor here since pf_local is only used for preliminary comparison). All subsequent particle filter evaluations do report SE, which is correct.

---

### 7. Biological Plausibility of Estimated Parameters Not Checked

The final parameter estimates (mu_EI ≈ 0.57/week → latent period ~12 days; mu_IR ≈ 1.23/week → infectious period ~5.7 days; mu_RS ≈ 0.076/week → immunity duration ~13 weeks; rho ≈ 0.001) are never compared against known flu biology. An immunity duration of 13 weeks is shorter than typical cross-season immunity and may indicate model misspecification. A reporting fraction of 0.1% is extremely low and could indicate that the modeled infectious population is severely overestimated. Checking these values against independent estimates would either support the findings or reveal a structural problem with the model. (Wheeler et al. 2024, §Corroboration with scientific knowledge)

---

### 8. SARIMA Residual Diagnostics Are Incomplete

The SARIMA section shows an ACF plot and a residual time series, but does not include a Ljung-Box test. The residual plot still shows annual spikes at reduced magnitude compared to the ARMA residuals, suggesting incomplete seasonal adjustment. The report attributes this to the SARIMA's improved handling of seasonal trends but does not quantify residual autocorrelation beyond visual inspection.

---

### 9. Data Restriction to 2011–2015 Is Partly Computationally Motivated

The report states the data was restricted partly because "The Great Lakes cluster was running slow when working on this project." Decisions about the scope of an epidemiological analysis should be driven by scientific criteria (data quality, structural stability, homogeneity of surveillance). Using computational limitations to justify a shortened time series is not a methodological defense. The COVID-era exclusion is scientifically defensible, but the further restriction to 2011–2015 rather than 2010–2019 is not fully motivated.

---

### 10. Model Structure Sourced from ChatGPT Without Literature Citation

The seasonal transmission forcing specification (`Beta = Beta0*(1 + amp*sin(2*pi*(t+phase)/52))`) was suggested by ChatGPT (disclosed in the report). This particular form is standard in the seasonal SEIR literature and is not itself incorrect, but the decision to adopt it from an AI tool rather than a peer-reviewed source means no citation is available to validate that it is the best or most common choice for influenza. The report should cite a published model that uses this forcing structure.

---

### 11. Local Search Dismisses Non-Convergence of Parameters Too Quickly

The report states: "The remaining parameters did not converge within this iterated filtering search, but the improvement in likelihood means this is not an issue." Non-convergence of parameters in the local search may indicate weak identifiability or a poorly specified parameter space, not merely an under-explored likelihood surface. While the course notes acknowledge that parameter spread is expected under weak identifiability, dismissing all non-convergence in a local search without any follow-up analysis is premature. The global search does partially remedy this.

---

### 12. Phase Parameter Is Not Constrained for Periodicity

The phase parameter in `Beta0*(1 + amp*sin(2*pi*(t+phase)/52))` has period 52; values of phase and phase+52 yield identical models. Without a constraint or periodic transformation, the parameter space contains infinite identical modes. The logit/log/barycentric transforms applied to other parameters address their natural constraints, but phase is left unconstrained. This does not affect the correctness of any individual fit, but it means profile plots over phase will show artificial multimodality.

---

### 13. rw.sd = 0.01 Is Half the Course Standard

All parameters use `rw.sd = 0.01` in mif2. The course standard perturbation size on a log or logit scale is 0.02. While the conventions file notes these values are context-dependent, the authors provide no justification for halving the perturbation. A smaller step size can cause the optimizer to explore the parameter space more slowly, which could be a partial explanation for why some parameters did not converge in the local search.

---

### 14. No Sensitivity Analysis of Particle Count

The analysis uses Np=2000 throughout. The loglik.se values from the final global search are approximately 0.004–0.005, which is acceptably small. However, no explicit sensitivity check (e.g., comparing likelihoods at Np=1000 and Np=2000) is presented. For a project concluding that the POMP model is inferior to SARIMA by a margin that is described as "substantial," verifying that the particle count is adequate for that specific conclusion would strengthen the argument.

---

### 15. Conclusion Overstates Certainty Given Absent Profile Likelihoods

The final conclusion states the SEIRS POMP model is "not the best time series approach for modeling Oklahoma influenza data" based on the log-likelihood comparison. Given that (a) no profile likelihoods were computed so parameter values may be suboptimal, (b) the H accumulator may introduce a systematic offset in observations, and (c) the SARIMA baseline was selected via a misspecified grid search, this conclusion rests on shaky foundations. A more measured conclusion acknowledging these limitations would be appropriate.

---

## Files Consulted

### Skill Files
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

### Project Files
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project05/great-lakes-seirs-global.R`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project05/great-lakes-seirs-local.R`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik_6.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik.csv`
