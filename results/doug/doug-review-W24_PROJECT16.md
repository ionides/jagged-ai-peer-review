# Peer Review: W24 Project 16
## "Modelling of the Influenza cases and spread in the Netherlands using ARIMA and POMP(SEIR) models"

---

## Summary

This project fits a two-population SEIR model (vaccinated vs. unvaccinated) to one season (October 2022 – May 2023) of WHO sentinel influenza surveillance data from the Netherlands, using a POMP framework with IF2 optimization. The stated goal is to compare transmission rates ($\beta_v$, $\beta_u$) and recovery rates ($\mu_{IR_v}$, $\mu_{IR_u}$) between vaccinated and unvaccinated populations to infer the protective effect of vaccination.

The project demonstrates genuine ambition in extending a standard SEIR to a dual-population structure and in using HPC for the global search. However, it is undermined by several critical technical errors: the accumulator variable tracks recoveries rather than new detections, the two sub-populations are completely isolated (no cross-transmission), the "profile likelihood" plots are misidentified global-search scatter plots rather than true profile likelihoods, key parameters are unidentifiable from the data, the global IF2 search is initialized from a local mif2 result (anti-pattern), and the main scientific conclusions are unsupported by the evidence presented.

---

## Major Issues

### 1. Accumulator variable tracks recoveries, not reported infections

The Csnippet computes `H += dN_IR_v + dN_IR_u` — accumulating recoveries from the infectious compartment. The observation variable `INF_ALL` represents newly detected influenza cases (infections detected during the sentinel week), not recoveries. These are epidemiologically different events. The measurement model `dmeasure` then equates `rho * H` with expected detected cases, so it is effectively fitting observed detections to a scaled recovery count. This mismatch distorts all parameter estimates; in particular, `rho` absorbs the ratio of recoveries to true new detections per week rather than reflecting the actual surveillance reporting fraction. The estimated `rho ~ 0.003` across all top-likelihood runs (inspection of `global_search.rds`) is implausibly low and consistent with this mis-specification. The correct fix is `H += dN_EI_v + dN_EI_u` (newly infectious, analogous to new detections in a symptomatic-infection model) or `H += dN_SE_v + dN_SE_u` (new exposures), depending on the data-generating process for sentinel detection (see Wheeler et al. 2024, §Measurement model specification).

### 2. No cross-population transmission — two independent epidemics

The force of infection for vaccinated susceptibles is `Beta_v * I_v / N`, and for unvaccinated susceptibles it is `Beta_u * I_u / N`. There is no term allowing infectious vaccinated individuals to infect unvaccinated susceptibles, or vice versa. This means the model simulates two completely independent and non-interacting epidemics in the same population. This is epidemiologically implausible: influenza spreads through physical contact, which is not restricted by vaccination status. The standard approach is a mixing matrix. At minimum, the force of infection on vaccinated susceptibles should include a contribution from `I_u`, and vice versa. All claims about vaccination reducing transmission are built on a model architecture that structurally prevents the two groups from influencing each other, which invalidates the comparative interpretation.

### 3. Profile likelihood plots are misidentified global-search scatter plots

The paper presents six "profile likelihood" plots for $\beta_v$, $\beta_u$, $\mu_{IR_v}$, $\mu_{IR_u}$, and their ratios, each with a chi-squared confidence interval cutoff line. Inspection of the code and the `global_search.rds` artifact reveals that `profile_results` is simply the global search output loaded directly via `read_rds("global_search.rds")`. No separate profile IF2 optimization is run with the target parameter fixed at a grid of values. The "profiles" are produced by filtering global-search rows to a log-likelihood range, grouping by rounded parameter values, and selecting top rows per group — this is a scatter plot of the global search, not a profile likelihood. The chi-squared CI cutoff applied to these plots has no statistical justification; the resulting confidence intervals are invalid. True profile likelihoods require running IF2 with the profiled parameter fixed at each grid value (e.g., via `profile_design()`) (Wheeler et al. 2024, §Parameter identifiability and uncertainty).

### 4. Global IF2 search initialized from local search result (anti-pattern)

In `run.r` (line 191), the global search is run as `mf1 |> mif2(params=c(guess, fixed_params))`, where `mf1 <- mifs_local[[1]]` is a completed local mif2 object. Passing a previous mif2 result as the first argument to the global search inherits that chain's cooling schedule, which is already at or near its terminal state. The 400 global search replicates effectively perform very few functional IF2 iterations from their random starting points before perturbations shrink to near zero, anchoring the global search near the local optimum rather than genuinely exploring the parameter space. The fix is to pass the base `pomp` object as the first argument: `mf1 <- fluSEIR` (see pomp-global-search-init-audit skill).

### 5. Severe parameter non-identifiability; conclusions unsupported

Inspection of `global_search.rds` reveals that within 2 log-likelihood units of the maximum, $\beta_v$ ranges from 0.30 to 23.6, $\mu_{IR_v}$ ranges from 0.00017 to 6.98, and $\eta_v$ ranges from 0.099 to 1.0. The best-fit row has $\beta_v / \beta_u = 23.0 / 8.2 = 2.79 > 1$, meaning $\beta_v > \beta_u$ at the actual maximum likelihood point — the opposite of the paper's main conclusion. The paper's claim that "$\beta_v < \beta_u$ proves that vaccination effectively slows transmission" is not supported by the reported maximum likelihood estimate; it appears to rely on a visual interpretation of where clusters appear in the pairs plots. Parameters are effectively unidentifiable: the data (one 30-week seasonal series) provide insufficient information to distinguish between the 9 freely estimated parameters across two subpopulations (Wheeler et al. 2024, §Parameter identifiability and uncertainty).

### 6. No non-mechanistic benchmark comparison

The ARIMA model is presented only as a qualitative motivation for the SEIR model ("ARIMA is inadequate") rather than as a quantitative benchmark. No log-likelihood or AIC comparison between the ARIMA model and the POMP model is reported, so it is impossible to assess whether the SEIR model captures meaningful structure beyond what a simple statistical model would achieve. Wheeler et al. (2024) note that none of 32 reviewed cholera papers included such a comparison, and that mechanistic models sometimes fail to outperform auto-regressive benchmarks. The ARIMA model's AIC is reported but the POMP model's AIC is not, precluding any comparison (Wheeler et al. 2024, §Benchmark comparison).

### 7. k (dispersion parameter) fixed without justification; not estimated

The negative binomial dispersion parameter `k` is fixed at 10 for all computations (`fixed_params <- c(N=17700000, vac_rate=.679, k=10)`) without any stated justification. The sensitivity of results to this choice is not assessed. Fixing `k` at an arbitrary value affects the shape of the likelihood surface and therefore all parameter estimates. Given that the reporting process for sentinel surveillance data is highly uncertain, `k` should be estimated or at minimum its influence on conclusions should be examined via sensitivity analysis.

### 8. Misleading statement about log-likelihood

The paper states: "The negative log likelihood in these runs reach a maximum (likelihood minimum) at: [−193.66]." The reported value from `logmeanexp(profile_results$loglik, se=TRUE)` is −193.66 — this is the log-likelihood (negative), not the negative log-likelihood. The maximum log-likelihood (best fit) from the global search is −189.93. Calling −193.66 a "minimum" is incorrect; it is the logmeanexp across all runs including poor starting-point runs. This suggests confusion between likelihood and negative likelihood, and between the mean-log-likelihood and the maximum.

---

## Minor Issues

- **No simulation vs. data plot**: The HTML output contains no plot comparing model simulations to the observed influenza time series. Such a plot is essential for visual model checking and is standard in POMP analyses. The `run.r` script generates such a plot (`sims |> ggplot(...)`) but it does not appear in the rendered output.

- **Convergence traces inadequately presented**: The local IF2 convergence traces are shown (4 replicates, Nmif=300), but the global search uses `run.r` parameters (Nmif=1000) that differ from what is coded in the Rmd (Nmif=300, only 4 replicates), creating inconsistency between the displayed traces and the actual optimization used.

- **Hard-coded absolute path in run.r**: Line 215 of `run.r` contains `f_results <- read_rds("/Users/falarcon/Desktop/all/global_search_2.rds")` — an author-specific absolute path that will not run on any other machine.

- **Typos and grammatical errors**: "Forcast" (section header), "computationally intesive", "inmuen systems" (immune), "slighlty". The writing would benefit from proofreading.

- **Single equation for S_u initialization is incorrect in the text**: The paper states $S_u = \text{vaccinationRate} \times \eta_u \times N$, but the code correctly implements $S_u = (1 - \text{vac\_rate}) \times \eta_u \times N$. The text equation has a copy-paste error.

- **No model diagnostics**: No conditional log-likelihood per time point, no effective sample size plot, and no filtering distribution is shown. These are important for identifying where the model fits poorly (Wheeler et al. 2024, §Model diagnostics).

- **Initial condition for I_v and I_u hardcoded to 1**: Starting with exactly one infectious individual per sub-population is a strong assumption for a 30-week seasonal series. Whether results are sensitive to this choice is not discussed.

- **No quantitative goodness-of-fit summary**: Log-likelihood at the MLE is mentioned briefly but no AIC, model comparison table, or discussion of absolute fit quality is provided. Wheeler et al. (2024) note that visual comparisons alone are only a weak measure of goodness-of-fit.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/Blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/run.r`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/global_search.rds`
