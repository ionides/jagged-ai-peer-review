# Peer Review: W21 Project 15
**An Analysis of COVID-19 Cases in Washtenaw County**

---

## Summary

This project fits a time-varying-beta SEIR model to daily COVID-19 case counts in Washtenaw County, Michigan (March–December 2020) using iterated filtering (mif2) in the `pomp` package. The model uses a five-segment step function for the contact rate to accommodate multiple epidemic waves, and the observation process is specified as a discretized truncated normal. The authors perform a local and global parameter search, compute a profile likelihood for the reporting rate, and provide a benchmark comparison against a negative binomial IID model and a SARMA model. Genuine strengths include: the inclusion of a non-mechanistic benchmark comparison, use of replicated pfilter calls with logmeanexp for likelihood evaluation, and a multi-stage global search with diverse starting points. However, the analysis has several critical deficiencies: the measurement noise parameter tau is effectively not estimated due to an anomalously small perturbation size; the profile likelihood for the reporting rate is acknowledged to have only three points above the Wilks threshold; two key epidemiological parameters are fixed without any sensitivity or identifiability check; and the SEIR model is substantially outperformed by the SARMA benchmark (~47 log-likelihood units) without any model revision. Several analysis results are suppressed from the rendered HTML via `eval=FALSE`, compromising reproducibility.

---

## Major Issues

### 1. Measurement noise parameter tau effectively not estimated

The perturbation size for tau is set to `rw.sd(..., tau = 0.0001, ...)`. Since tau is log-transformed (via `parameter_trans(log = c(..., "tau", ...))`), this specifies a perturbation of 0.0001 on the log scale per iteration. The course standard for log-transformed parameters is rw.sd = 0.02 — the chosen value is 200 times smaller. Over 700 total mif2 iterations in the global search, the maximum accumulated drift in log(tau) is approximately sqrt(700) × 0.0001 ≈ 0.003 log units, or a relative change of about 0.3% in tau. This means the iterated filtering algorithm cannot meaningfully optimize over tau.

The consequence is visible in the cached parameter file (`pomp_cache/writeup_params.csv`): the top-ranked MLE has tau = 0.1012, essentially at the upper boundary of the search box (`upper = c(..., tau = 0.1)`). The global search happened to sample starting points near the upper boundary of the tau box, and the tiny rw.sd prevented tau from moving, so the reported "MLE" for tau reflects the starting point distribution rather than genuine optimization. The true MLE for tau may lie above 0.1. This undermines all downstream inferences. The rw.sd for tau should be set to the standard 0.02 on the log scale, and the search box for tau should be expanded to confirm the optimum is interior.

### 2. Profile likelihood for rho too sparse to support valid confidence intervals

The 95% confidence interval for rho [40.97%, 48.01%] is read from a profile that has only three points above the Wilks threshold (chi-square cut-off for 95% CI). The authors themselves acknowledge: "we would want to remain cautious about this result as only three points are above the threshold." The course standard requires approximately 5 points at run_level=2 or 30 points at run_level=3 (531-conventions.md). A profile with three points above the threshold cannot reliably identify the profile maximum or the CI endpoints. This is Error 1.9 from the student weakness reference (course-confirmed, Major). The profile must be recomputed with a finer grid of rho values, or more starting points per rho slice, to produce a valid CI.

### 3. Key epidemiological parameters mu_EI and mu_IR fixed without profiling or sensitivity analysis

The incubation rate (mu_EI) and recovery rate (mu_IR) are fixed at 0.1 day^-1 based on a qualitative literature range and are excluded from all optimization stages ("we will set both mu_EI and mu_IR to 0.1 and fix them during the local and global search"). No profile likelihood or sensitivity analysis is reported for these parameters. Fixing parameters that are poorly determined by the data or that interact with other parameters (e.g., mu_EI and the contact rate b_j) can introduce substantial bias in the remaining estimates and obscure model misspecification. Wheeler et al. (2024) document that implausible fixed parameters can be interpreted as evidence of model misspecification rather than biological truths. At minimum, a sensitivity analysis or profile likelihood for mu_EI and mu_IR should be reported.

### 4. SEIR model substantially outperformed by SARMA benchmark with no model revision

The SARMA(3,3)×(1,1)_7 benchmark achieves an adjusted log-likelihood of -1,104.23 on the original data scale, versus the SEIR MLE of -1,151.66 — a gap of approximately 47 log-likelihood units. This is a large gap by any standard. The 531-conventions.md course note states: "If the mechanistic model fits disastrously compared to the benchmark, our model is probably missing something important." The authors correctly identify the 7-day periodic component (driven by administrative reporting rhythms) as a likely explanation, but no model revision is attempted. The appropriate response is to investigate the model's structural failure — for example, by examining conditional log-likelihoods per time step — and attempt to address the source of misfit (e.g., by incorporating a weekly effect in the measurement model or contact rate). Reporting the loss without revision limits the scientific contribution of the analysis.

### 5. Global search convergence diagnostics absent

No trace plots are shown for the global search, which runs seven sequential mif2 stages per starting point. The only convergence evidence presented for the global search is a pairs plot of final parameter estimates. Without likelihood traces across mif2 iterations, there is no direct evidence that the 700-iteration global search has converged. The local search shows trace plots for 20 runs, but these cover only 50 mif2 iterations from a single starting point region and do not substitute for global search convergence diagnostics. This is Error 1.8 from the student weakness reference (course-confirmed, Major). Trace plots for the global search — showing loglik and parameters across the sequential mif2 stages for a representative sample of starting points — should be provided.

### 6. No model diagnostics beyond unconditional forward simulation

The diagnostic assessment consists entirely of visual comparison of forward simulations (conditioned on the estimated parameters but not on observed data) with the observed time series. No conditional log-likelihoods per time step are computed or plotted; no effective sample size (ESS) monitoring is reported; no filtering distribution plots are presented. Per Wheeler et al. (2024), conditional log-likelihood plots are essential for identifying where and why a model fails, and are the primary tool that motivated model improvements in their study. Given the large likelihood gap with the SARMA benchmark, such diagnostics are especially important here for diagnosing which time periods the model fails to explain.

### 7. Profile likelihood computed only for rho; b1–b5 and eta not profiled

Profile likelihoods are computed only for the reporting rate rho. The five time-varying contact rate parameters (b1–b5) and the initial susceptible fraction (eta) have no profile likelihood or confidence interval. With five beta parameters and the acknowledged difficulty of the likelihood surface (the local search shows some runs "stuck in local maxima"), identifiability of each contact rate segment is unclear. The pairs plots of the global search results suggest concentrated parameter regions, but these are insufficient substitutes for proper profiles. At a minimum, profile likelihoods for eta and the most important contact rate segments should be reported.

### 8. ARMA model selection code not rendered; benchmark AIC unverifiable

The code chunks that generate the AIC table justifying the choice of SARMA(3,3)×(1,1)_7 (four `eval=FALSE` chunks labeled `generate_aic_table` and the four calls) are not executed in the rendered HTML. The AIC of 231.698 appears in the text but the computation producing it is suppressed. Readers cannot verify which model was selected or whether the search over (P, Q, SP, SQ) was exhaustive. The AIC table code should be executed (or its results tabulated) in the rendered document.

---

## Minor Issues

### 9. Local search results table and pairs plot not rendered

The local search results table ("Local search results (in decreasing order of likelihood)") and the associated pairs plot are both in `eval=FALSE` chunks and do not appear in the rendered HTML. Readers can see the trace plots but not the numerical results or parameter scatter from the local search.

### 10. Initial compartment values E(0) and I(0) fixed without sensitivity

E(0) = 100 and I(0) = 200 are fixed based on a qualitative argument about travelers and are not estimated or profiled. No sensitivity analysis examines how the results change under different initial conditions. Given that initial conditions can substantially affect model fit (Wheeler et al. 2024 document an AIC impact of ~72 units for one model from initialization strategy), at least a brief sensitivity check is warranted.

### 11. Initial pfilter evaluation uses fewer particles than the rest of the analysis

The initial log-likelihood evaluation for the starting parameter guess uses `Np=500` (line in the `writeup_lik_starting_values.rds` bake block), while the rest of the analysis uses `NP = 1000` (the run_level=2 value). The reported initial log-likelihood of -1,351.26 ± 25.50 is therefore based on a noisier particle filter estimate. The large SE of 25.50 further suggests 500 particles is inadequate even for this preliminary check.

### 12. Optimal tau at the boundary of the search domain

The search box specifies `upper = c(..., tau = 0.1)`, yet the best parameter set in the cache has tau = 0.1012, essentially at the upper boundary. When an MLE lies on the boundary of the search space, the optimization may not have found the true maximum. The authors do not flag this or attempt an expanded search. This compounds the issue with the small rw.sd (Issue 1 above).

### 13. R compartment not tracked; population conservation unverifiable

The recovered compartment R is not included in `statenames`, so S + E + I + H does not equal N. While H is properly declared as an accumulation variable (reset each time step), there is no way to verify that the model conserves the population, since R = N - S - E - I is implicit but never checked. Tracking R explicitly would allow population conservation to be verified as a sanity check.

### 14. 7-day weekly periodicity not incorporated into the SEIR model

The periodogram identifies a dominant 7-day frequency (omega_2 = 0.14375 cycles/day, corresponding to a 7-day reporting cycle). This is the primary reason the SEIR model is outperformed by the SARMA model. The authors acknowledge this in the conclusion but make no attempt to address it — even a simple day-of-week effect in the measurement model's reporting rate could substantially reduce the benchmark gap. The limitation is real but should be accompanied by a brief attempt at correction.

### 15. Gaussian measurement model choice not discussed

The measurement model uses a discretized truncated normal with variance (tau*H)^2 + rho*H. The more standard choice for overdispersed count data in POMP COVID models is the negative binomial, which is directly parameterized for overdispersion and avoids the need for a tolerance constant `tol = 1e-25` to prevent log-likelihood collapse when H is small. No justification is provided for the Gaussian choice over the negative binomial. Given the measurement model can substantially affect inference (Wheeler et al. 2024), a brief justification or comparison would strengthen the analysis.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W21/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W21/project15/pomp_cache/writeup_params.csv`
