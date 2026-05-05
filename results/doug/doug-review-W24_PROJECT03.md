# Peer Review: W24 Project 03
## "531 Final Project: Analysis on Covid-19 Cases in Japan"

---

## Summary

This project fits a SEIR compartmental model to weekly COVID-19 case counts in Japan (2020–2021) using iterated filtering (IF2) in the `pomp` framework, alongside a SARIMA benchmark. The authors sensibly motivate a time-varying contact rate (four phases keyed to policy events) and correctly implement stochastic binomial transitions and a normal-approximation measurement model. However, the analysis is undermined by a series of critical computational failures: global search regions were poorly specified, resulting in searches that performed worse than the local search; the best log-likelihood value found (–1079.9, in the profile likelihood object) is never identified as the MLE or discussed in the text; tau is severely under-explored in every optimization except the profile; several key parameters show extreme variability at the likelihood maximum, indicating potential non-identifiability; and the profile confidence interval for rho rests on only three grid points, making it unreliable. The paper does not compare the SEIR model against the SARIMA benchmark quantitatively, no model diagnostics (ESS, conditional log-likelihoods) are presented, and mu_EI and mu_IR are fixed rather than estimated, removing important inferential degrees of freedom. Presentation of results is also confused, with multiple searches returning worse likelihoods than earlier ones in a sequence that the text does not explain.

---

## Major Issues

### 1. Global searches perform worse than the local search — the best MLE is never identified

The paper reports four distinct optimization runs with log-likelihoods of: local search (–2205.9), global search 1 (–3531.9), global search 2 / mifs_global (–4457.8), and global search 2 not based on local (–1083.8). Inspection of the saved RDS artifacts confirms that the profile likelihood object (`global_profile.rds`) contains a row with loglik = –1079.9, which is the overall best likelihood across the entire analysis. Yet the text never identifies –1079.9 as the MLE; instead it discusses each search piecemeal, and only the profile CI for rho is presented at the end. The fact that global search 1 (–3531.9) is worse than the local search (–2205.9) is a diagnostic red flag indicating the search box for global search 1 was poorly calibrated — a point the text does not address. The reader is left without a clear, authoritative statement of the final MLE or the parameter vector that achieves it. (Wheeler et al. 2024, §Computational adequacy.)

**Fix:** Report the globally best log-likelihood (–1079.9 from the profile) as the MLE, display the corresponding parameter vector, plot forward simulations from those parameters, and explain why earlier searches underperformed.

### 2. The tau (overdispersion) parameter is severely constrained in all optimization searches except the profile

The initial parameter value for tau was 0.05. Global search 1 imposed an upper bound of 0.006 on tau — an order of magnitude below the starting value — and the mifs_global search used rw.sd of 0.0001 for tau, effectively fixing it. Global search 2 (not based on local) extended the upper bound to 0.2, which allowed tau to reach 0.60 at the best point. The profile then found tau = 1.05 at the optimum. The systematic under-exploration of tau across the searches explains most of the 1,000-unit gap in log-likelihood between the early searches and the profile. The text comments that the log-likelihood "improves" across searches without recognizing that the improvement is driven by relaxing the tau constraint rather than by better optimization.

**Fix:** Specify the intended prior/search range for tau before optimization, justify it biologically (tau governs the standard deviation of reported cases relative to the mean), and use a consistent range across all searches.

### 3. mu_EI and mu_IR are fixed rather than estimated

The paper fixes the incubation-rate parameter mu_EI = 0.1/week and the recovery-rate mu_IR = 0.1/week, citing CDC literature values for days. However, the unit conversion is wrong: if the incubation period is 6.5 days and the model operates on weekly time steps, then mu_EI should be approximately 1/(6.5/7) ≈ 1.08/week, not 0.1/week. More fundamentally, fixing these parameters removes the ability to let data inform epidemiologically important quantities and prevents formal uncertainty quantification. No profile likelihood is reported for either parameter. (Wheeler et al. 2024, §Parameter identifiability.)

**Fix:** At minimum, run profile likelihoods for mu_EI and mu_IR to determine whether they are identifiable from the data. If fixing is necessary for practical reasons, provide a sensitivity analysis over plausible ranges. Correct the unit conversion.

### 4. No benchmark comparison between SEIR and SARIMA

The paper fits both a SARIMA and a SEIR model but never compares them quantitatively. The SARIMA log-likelihood is not reported. No AIC comparison is presented. Without this comparison, it is impossible to assess whether the mechanistic SEIR model captures meaningful structure beyond what the purely statistical SARIMA model achieves. (Wheeler et al. 2024, §Benchmark comparison; the paper notes that none of 32 reviewed cholera models performed such a comparison, treating this as a critical gap.)

**Fix:** Report the SARIMA log-likelihood on the same data (the 104-week Japan series) and compare it directly to the SEIR log-likelihood using AIC or a likelihood ratio if the models are nested.

### 5. Profile confidence interval for rho rests on only three grid points

The profile likelihood for rho uses 40 grid values over [0.01, 0.95], but inspection of the saved profile artifact (`global_profile.rds`) shows that only three of the 40 grid values have profile log-likelihoods above the 95% confidence cutoff (–1081.82). The reported CI [0.661, 0.926] is therefore the range of those three values. With such sparse support, the interval boundaries are highly sensitive to random noise in the likelihood evaluation and the CI should not be reported with two-decimal precision. Additionally, at each profile grid point, the profile optimization uses only 10 replicate particle filter evaluations with Np = 1000 particles, substantially lower than the 200 replicates with Np = 10,000 used in the local search, increasing Monte Carlo uncertainty. (Wheeler et al. 2024, §Parameter identifiability.)

**Fix:** Increase the particle count and the number of replicate evaluations in the profile, or use the MCAP procedure to produce profile CIs that are robust to Monte Carlo error. At minimum, acknowledge the extreme sparseness of the CI.

### 6. b4 and b2 are unidentifiable at the likelihood optimum

Examination of the profile artifact shows that at the top three profile points (the only ones above the 95% cutoff), b4 varies from 0.17 to 3,667 — a factor of more than 20,000 — while b2 varies from 0.78 to 4.0 across those same points. This extreme variation in b4 and b2 while log-likelihood remains nearly constant is a strong signal of parameter non-identifiability. The text notes that "ranges of parameters compatible with the data within our current model setting exhibit narrow variability" and that this "instills greater confidence in our MLEs" — a conclusion that is directly contradicted by the artifact. The very high b4 estimates (~3,667 contact rate) are also biologically implausible for a COVID-19 model.

**Fix:** Compute profile likelihoods for b4 and b2 individually. If they are unidentifiable, interpret this as a sign of model misspecification — the four-phase step function may be over-parameterized or the Omicron cutoff may cause the last phase to be unresolvable. (Wheeler et al. 2024, §Model misspecification.)

### 7. No model diagnostics: effective sample size, conditional log-likelihoods, or filtering checks

The paper presents no particle filter diagnostics. ESS is never monitored, so particle degeneracy during filtering cannot be ruled out. No conditional (per-time-step) log-likelihood plot is provided, which would identify specific epidemic periods where the model fits poorly. No comparison of simulations conditioned on the data (filtering distribution) versus forward simulations from initial conditions is shown. Given that the model fails to capture the early 2022 surge (explicitly noted in the text), conditional log-likelihoods would likely reveal whether this is a structural failure or a parameter calibration issue. (Wheeler et al. 2024, §Model diagnostics; simulation-study checklist §10.)

**Fix:** Add ESS diagnostics across the particle filter trajectory. Plot conditional log-likelihoods per time step. Discuss periods of poor fit explicitly.

### 8. SEIR model cannot mechanistically explain multiple epidemic waves without waning immunity

The standard SEIR model permanently removes individuals from the susceptible pool upon recovery. With Japan's population of ~126 million and the relatively small first wave (roughly 100,000 cases through May 2020), the susceptible fraction barely changes, which might make multiple waves mathematically possible. However, the three large 2022 waves (peaks in the tens of thousands per week) would deplete a substantial fraction of susceptibles. The paper acknowledges only that "traditional SEIR models typically describe scenarios with only one peak" and attributes multi-wave dynamics entirely to time-varying beta. No analysis is presented showing that susceptible depletion does not prevent the model from reproducing the observed wave structure, and no waning immunity or reinfection mechanism is discussed. The biologically implausible b4 value (~3,667) in the best-fit solution may be a symptom of this structural limitation.

**Fix:** Estimate the implied cumulative infection burden from the fitted model and check whether the susceptible pool remains plausible at each wave. Consider whether an SEIRS (waning immunity) or SEIR with partial susceptibility would better reflect COVID-19 biology.

---

## Minor Issues

- **Unit error in mu_EI and mu_IR initialization.** The text states mu_EI = 1/(6.5 days) = 0.15 day^(-1), then uses 0.1 as the actual value, citing a different value later. If the model time step is one week, then a daily rate of 0.15 should be converted to a weekly rate near 1.05, not 0.1. The parameters as fixed are inconsistent with the cited CDC literature on timescales.

- **Inappropriate auto-installing of packages.** The analysis code begins with `if (!require(...)) install.packages(...)` calls for more than ten packages. This modifies the execution environment without user consent and violates reproducibility standards. Dependencies should be documented (e.g., via `renv`) not auto-installed.

- **Duplicate `library(tidyverse)` call.** The setup chunk loads `tidyverse` twice (lines 38 and 45 of the .qmd), suggesting copy-paste composition.

- **`registerDoParallel()` called twice with conflicting arguments.** The setup chunk calls `registerDoParallel()` once with no argument (using a system default) and then immediately calls `registerDoParallel(8)`. The second call overrides the first; the duplicate call is confusing.

- **`global_search_2.rds` is referenced in the code but not discussed in the text.** The bake call uses the filename `global_search_2.rds` for the "Not Based on Local Search" results, but this name conflicts with the reader's expectation from the "global search 2" label applied to the mifs_global search. The naming is opaque.

- **The rho CI interpretation is questionable.** The text interprets a 95% CI of [66%, 93%] as evidence of "stringent disease reporting and control measures in Japan." A reporting rate this high for COVID-19 (typically estimated at 5–30% in comparable settings) warrants careful discussion. If the estimate is driven by the measurement model misspecification, attributing it to surveillance quality is misleading.

- **SARIMA model uses seasonal period 4 weeks but the data period is ~4.3 weeks.** The estimated spectral peak corresponds to 4.33 weeks; the SARIMA uses period = 4. This rounded value is not justified. At minimum, SARIMA models with period = 4 and period = 5 should be compared.

- **No convergence traces for the global searches.** Iteration traces (log-likelihood versus IF2 iteration) are shown only for the local search. All three global searches report only final log-likelihoods, making it impossible to assess whether convergence was reached.

- **The measurement model description is slightly inconsistent.** The text states "Cases = max{round(C_n), 0}" for rmeasure, but the dmeasure Csnippet uses a truncated normal that includes 0.5 continuity corrections, which is not mentioned in the mathematical description.

- **Missing `pomp` package version.** The analysis uses `pomp` but does not record the installed version (no `sessionInfo()` or `renv.lock`). Given that the `pomp` API has changed across versions, reproduction on a different system is not guaranteed.

- **No RNG seeds set before the second global search ("Not Based on Local Search").** The bake call for `global_search_2.rds` uses `registerDoRNG(1270401374)` inside the bake block (consistent with the first global search), but no explicit seed is set in that code section in the .qmd file; the same seed constant as global search 1 is reused, which could cause confusion if run separately.

- **Data truncation at Dec 26, 2021, not Dec 31, 2021 as stated.** The filter `date < "2021-12-31"` excludes Dec 31 itself. The last data point is Dec 26, 2021. The text describes the analysis as covering data "up to 31/12/2021," which is inaccurate.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/blinded.qmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/local_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/global_search_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/global_search_2.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/global_search_results.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/global_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/mifs_global.rds`
