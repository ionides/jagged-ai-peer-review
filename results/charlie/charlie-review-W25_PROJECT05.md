# Peer Review: W25 Project 05
## "Analysis of Malaria Cases in Florida"

---

## Summary

This project analyzes monthly reported malaria cases in Florida (2006–2016) using two approaches: a SARIMA baseline and a mechanistic SEIR-with-splines POMP model adapted from a dengue model in the literature. The authors identify seasonal structure in the data, fit a SARIMA(0,1,1)(0,1,1)[12] model, and then build a stochastic SEIR model with periodic B-spline forcing and an immigration parameter, estimating parameters via IF2 (iterated filtering). While the combination of SARIMA and POMP approaches is appropriate for this type of data, and the motivation for immigration-based infection pressure is scientifically reasonable, the execution has critical weaknesses: the POMP model substantially underperforms the SARIMA benchmark (-328 vs. -96 log-likelihood), no explanation or resolution is offered; parameter identifiability is not demonstrated; computational effort is marginal; and the measurement model contains internal inconsistencies between the mathematical description and the code.

---

## Major Issues

### 1. POMP model dramatically underperforms the SARIMA benchmark with no resolution

The authors report a SARIMA log-likelihood of approximately -96 and final POMP log-likelihoods around -328, representing a gap of over 230 log-likelihood units. This gap is acknowledged in the Comparison section but dismissed as "scope for improvement." A mechanistic model that performs this far below a simple non-mechanistic baseline provides no evidence that it captures any meaningful biological structure beyond what a time-series model can achieve. Per Wheeler et al. (2024), benchmark comparisons are essential precisely because they reveal whether the mechanistic model adds anything beyond a simple statistical approximation. The authors are comparing AIC-based SARIMA selection with log-likelihood from the POMP model on the log-transformed vs. raw scale, making the comparison potentially invalid on its face (see Issue 2). Regardless of scale comparability, the direction of the result (SARIMA wins by a wide margin) demands a serious discussion and diagnostic follow-up, neither of which is provided.

**Fix:** Either (a) demonstrate that the log-likelihood values are on a comparable scale (same observation model, same data transform), and if so, diagnose why the POMP model fails so badly, or (b) explicitly acknowledge that the comparison is not valid as stated and conduct a proper one.

### 2. Log-likelihood comparison between SARIMA and POMP models is not valid as stated

The SARIMA model is fit on log-transformed data (`log1p(monthly_all$Y)`) while the POMP model is fit on the raw count data with a Poisson measurement model. Log-likelihoods from these two models are defined on different scales and are not directly comparable. The authors nonetheless compare them numerically ("-96 vs. -328") without any acknowledgment of this incompatibility. Wheeler et al. (2024) emphasize that quantitative goodness-of-fit comparisons must be "on the same data and observation model so values are directly comparable."

**Fix:** Either fit the SARIMA model on the same scale as the POMP observation model (raw counts, negative binomial or Poisson), or convert both to the same likelihood scale. Until this is done, no quantitative model comparison is possible.

### 3. Measurement model is Poisson but described as incorporating overdispersion parameter sigma_M

The parameter table (Initial Parameter Settings & Description) lists sigma_M = 0.3 as "Fixed measurement overdispersion," implying a negative binomial or similar overdispersed distribution. However, both the mathematical specification and the C-snippet code implement a Poisson measurement model: `rmeas <- Csnippet("Y = rpois(rho * I + 1e-6);")` and `dmeas <- Csnippet("lik = dpois(Y, rho * I + 1e-6, give_log);")`. The parameter `sigma_M` appears in `paramnames` and `par_trans` (it is log-transformed) but is never used in either `rmeas` or `dmeas`. This is a concrete internal inconsistency between the documented model and the implemented model, and constitutes a reproducibility failure of the type documented by Wheeler et al. (2024). The Poisson measurement model also has no overdispersion, which is inappropriate for count data from disease surveillance that typically exhibits substantial extra-Poisson variation.

**Fix:** Implement a negative binomial measurement model that actually uses sigma_M (or an equivalent dispersion parameter), or remove sigma_M from the parameter set entirely and update all documentation to reflect that the Poisson model is intentional.

### 4. Cumulative cases C are computed from E->I transitions but the measurement model observes I

The state variable C is defined as cumulative cases and updated as `C += rho * dEI` (proportional to E->I transitions). However, the measurement model observes `Y ~ Poisson(rho * I + 1e-6)` — it observes the current infectious count I, not the new cases from C. This creates an incoherence: C accumulates cases but is never used in the measurement model; instead I (the prevalence, not incidence) is the basis for observations. For a monthly reporting system, one would expect Y to relate to new cases (incidence) or at least to have a consistent definition. Furthermore, `accumvars = "C"` is set in the `pomp()` call, which means C is reset to 0 at each observation time — but since C is not used in dmeas, this has no effect on inference. The state variable C is essentially dead weight in this model.

**Fix:** Align the measurement model with the state variables. If cases are reported incidence, measure Y from accumulated new infections (dEI or the reset accumvar C). If Y measures prevalence, remove C from the model and clarify the epidemiological interpretation.

### 5. No profile likelihoods; parameter identifiability not assessed

The project presents no profile likelihood plots for any parameter. The trace plots show that parameters do not converge across IF2 runs ("our model is weakly identifiable for our parameters because the iterations don't converge in value"), and the authors note this explicitly. This is a correct diagnosis but an unresolved problem: with non-converging parameters, the reported MLEs are not reliable estimates of the true maximum likelihood, and any interpretations of parameter values (e.g., the immigration rate, rho, or spline coefficients) are untrustworthy. Wheeler et al. (2024) require profile likelihoods and MCAP confidence intervals for key parameters. The scatter plots of loglik vs. parameter values from the global search are informative but are not substitutes for proper profile likelihoods.

**Fix:** Compute profile likelihoods for at least the scientifically most important parameters (rho, immigration_rate, and possibly g or sigma_P). If profiles are flat, explicitly report this as evidence of non-identifiability.

### 6. Computational effort is insufficient; no convergence demonstrated

The local search uses Np=1000 particles and Nmif=50 iterations across 10 replicates; the global search uses Np=2000/4000, Nmif=100, across 20 replicates. Given that the trace plots themselves show non-convergence, these settings are clearly insufficient. The fact that the local and immigration models both converge to the same log-likelihood of -332.02 after local search is suspicious — it suggests the optimizer is not exploring the space effectively. Wheeler et al. (2024) emphasize that log-likelihood traces should demonstrate convergence, and that insufficient computation can make a good model look bad. The total computation budget (20 global replicates × Nmif=100 × Np=2000) is modest for a 12-parameter model on 132 monthly observations. No computation time or CPU-hour budget is reported.

**Fix:** Increase the number of particles and IF2 iterations until trace plots show convergence. Run multiple independent global searches and demonstrate that different starting points reach the same final log-likelihood. Report total computation time.

### 7. Global search parameter initialization is flawed: replicate() with base_params creates duplicate initial points

The global search code uses `replicate(20, { c(base_params, c(...)) })` where `base_params <- coef(seir_spline_model)`. Using `c()` to merge the two vectors results in parameters from `base_params` appearing twice in the initialization vector — the randomly drawn values for b_1...b_5, g, rho, etc. are appended after the base parameters, but `c()` does not replace named elements. In R, when you call `c(base_params, c(b_1=runif(1,...), ...))`, you get a vector with duplicated names; the `pomp` framework likely uses the first occurrence of each parameter name, meaning the random variation intended for the global search is silently ignored. This would explain why the global and local searches find identical or near-identical likelihoods. The correct approach is to modify `base_params` directly (e.g., `params <- base_params; params["b_1"] <- runif(1, -2, 2); ...`).

**Fix:** Verify the parameter initialization by printing one of the `global_inits` entries and checking that the intended random values are actually used. Rewrite the initialization to explicitly overwrite named elements in `base_params`.

### 8. Birth rate parameter r is biologically implausible and inconsistent

The parameter r = 0.135 is listed as "Birth rate" with units implied as per-month (since the model uses monthly time steps). A birth rate of 0.135 per month corresponds to approximately 162% per year — far exceeding any plausible human birth rate (which is approximately 0.01–0.015 per year for Florida). This is likely a transcription error from the dengue source model where r may have had different units or interpretation. During the global search, r is randomized in `runif(1, 0, 0.001)`, suggesting the authors recognized the problem but did not address it in the base model or documentation.

**Fix:** Clarify the units of r and verify that the value used is consistent with Florida's demographic data. Given that malaria is imported and not endemic, consider whether a full birth-death demographic structure is even necessary for a 10-year window.

---

## Minor Issues

### 9. Measurement model uses I (prevalence) rather than new infections for a reporting context

Monthly reported cases in a surveillance system represent newly diagnosed cases (incidence), not the stock of currently infectious individuals. Observing Y ~ Poisson(rho * I) implies that all currently infectious individuals are observed each month, which conflates stock and flow. A more appropriate measurement model would link Y to new cases per reporting period (e.g., rho * dEI accumulated over the month, via the accumvar C). This is a minor issue if the authors acknowledge it, but it is related to Major Issue 4 and affects interpretation of rho.

### 10. SARIMA model selection table is restricted to a very narrow grid

The AIC model selection grid searches only p_max=1, q_max=1, P=1, Q=1. This means the selected model SARIMA(0,1,1)(0,1,1)[12] is the best among only a 2x2x2x2=16 models. Standard practice is to search a broader grid (e.g., p,q up to 3-5, P,Q up to 2) to ensure the globally best SARIMA model is found. The claim that this is the "best fitting model" is only valid within the restricted search space.

### 11. Periodogram frequency axis labeling is misleading

The code labels the x-axis as "Frequency (cycles per year)" but `spec.pgram` for monthly data with default settings returns frequency in cycles per observation (here, cycles per month). The identified dominant frequency 0.0888 cycles/month corresponds to a 11.26-month period (approximately annual), but the text states it "translates to a cycle period of 12 months." The conversion and labeling should be made explicit to avoid confusion.

### 12. Invertibility check does not verify that the model is on the boundary

The authors report the model is invertible, but for the airline model (SARIMA(0,1,1)(0,1,1)[12]), it is common for the MA coefficients to be near or at -1, indicating the model is on the boundary of invertibility (unit root in the MA polynomial). The code checks `Mod(roots) > 1` but does not check whether roots are near 1 (e.g., within a tolerance). Being near the boundary has implications for forecast uncertainty and parameter stability that should be acknowledged.

### 13. No ESS monitoring during particle filtering

Neither the local nor global search reports effective sample size (ESS) from the particle filter. For a model that shows poor fit (log-likelihood of -328 vs. a baseline of -96), ESS collapse is a likely symptom that would explain the poor optimization performance. The simulation study checklist (Wheeler et al. 2024, §Model diagnostics) requires ESS monitoring to detect particle degeneracy.

### 14. Simulation comparison is purely visual with no quantitative summary statistics

The simulated trajectories plots compare 100 simulated paths to observed data visually, but no summary statistics are computed (e.g., coverage of observed data by simulation envelope, peak timing comparison, seasonal amplitude). Wheeler et al. (2024) note that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." Given that the model appears to systematically over-predict case counts based on the simulation plot description, quantitative summaries would clarify the extent of the discrepancy.

### 15. Session information and package versions not reported

No `sessionInfo()` output or package version information is provided. The `pomp` package has undergone substantial API changes across versions, and the code relies on `doFuture` with `plan(multisession)` which is version-sensitive. Without version information, the code may not reproduce on other installations. The code-supplement checklist requires explicit pinning of `pomp` version and, ideally, an `renv` lockfile.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project05/blinded.Rmd`
