# Peer Review: W21 Project 04
## Extended Analysis on the U.S. 10-year Treasury Bond Yield

---

## Summary

This project applies a stochastic leverage POMP model to monthly U.S. 10-year Treasury bond yield differences (1990-2021, n=374) and compares it to a GARCH(1,1) benchmark. The stochastic volatility model, drawn directly from the STATS 531 course template for financial time series, is fitted via IF2 (mif2) with a global box search. A complementary section uses Loess decomposition and an HP-filtered analysis of the association between yield and CPI. The project has genuine strengths: the use of particle filter likelihood estimation is methodologically sound, computational resources (HPC, 36 cores) were clearly used, and the stochastic leverage model is appropriately motivated. However, the project suffers from a critical dataset substitution error in the initial benchmark run, an invalid log-likelihood comparison between GARCH and POMP, absence of profile likelihoods and model diagnostics, no convergence trace plots, and a GARCH log-likelihood reporting issue. The conclusions are therefore not adequately supported.

---

## Major Issues

### 1. Simulated-Data Particle Filter Reported as Real-Data Benchmark (Critical)

The initial particle filter is run on `sim1.filt`, a pomp object constructed from a simulated dataset (created by calling `simulate(sim1.sim, seed=1, params=params_test)` and then wrapping the result as `sim1.filt`). The reported log-likelihood of -539.67 comes from filtering the simulated data, not the real Treasury yield differences. This value is then mentioned in narrative text as a reference point ("In a second, using 36 cores of CPU on Great Lakes, we obtained a log likelihood estimate of -539.67 with a Monte Carlo standard error of 0.034"), creating the misleading impression that this is a benchmark for model performance on the actual data. Because the simulated data and the real data are different time series, the two log-likelihood values (-539.67 vs. -25.71) are evaluated on completely different datasets and are not comparable whatsoever. The anomalously large gap between these values (-514 units) is precisely the signature of dataset substitution (see pomp-simdata-benchmark-error skill). A meaningful initial benchmark would re-run pfilter on `yield.filt` (the real-data pomp object) at `params_test` and report that value.

### 2. Invalid Direct Comparison of GARCH and POMP Log-Likelihoods

The conclusion states: "The GARCH model for the dataset showed a maximized likelihood of -33.89 with 3 fitted parameters. The POMP model has a maximized log likelihood of -25.71 with 6 fitted parameters. Due to the better performance and possibility of interpretation, we would prefer using POMP model." This comparison is invalid for two distinct reasons. First, the GARCH log-likelihood reported from `tseries:::logLik.garch` uses a non-standard normalization. The tseries package's GARCH implementation is known to report log-likelihoods that are not normalized to the per-observation Gaussian form used by other packages; direct comparison is problematic (course reference: Error 2.9 — trusting software likelihood output without checking conventions). Second, even if normalization were matched, the GARCH model is fitted to `yield_diff` (differenced yields), while the POMP model operates in a state-space where the observation is also `yield_diff`, but the likelihood evaluation conditions on a different measurement model. The comparison would need to be carefully verified to ensure both likelihoods evaluate on the same observation model and data. As stated, the conclusion about POMP being "better" than GARCH is not adequately supported.

### 3. No Convergence Diagnostics for IF2 (Iterated Filtering Trace Plots Absent)

Neither the local search (mif1) nor the global box search (box_eval) shows any convergence trace plot (i.e., `plot(if1)` or `plot(if.box)`). Without trace plots, it is impossible to assess whether IF2 has converged: the likelihood traces should show a consistent upward trend across iterations, and parameter traces should show the expected cooling pattern. The absence of convergence diagnostics is a course-confirmed major error (Error 1.8 in the weakness reference). The local search uses `yield_Nreps_local = 20` replicates and `yield_Nmif = 200` iterations, and the global search uses `yield_Nreps_global = 100` replicates, but none of the traces are shown. Without these, the claim that the global best of -25.71 has been found is unsupported.

### 4. No Profile Likelihoods or Parameter Uncertainty Quantification

The project reports a single point estimate for each parameter (from the global search pairs plots) but provides no profile likelihoods and no confidence intervals for any parameter. Profile likelihoods are the course-expected method for assessing parameter identifiability and constructing valid confidence intervals. The pairs plots shown for the global search (`pairs(~logLik+log(sigma_nu)+mu_h+phi+sigma_eta+H_0, data=subset(r.box,logLik>max(logLik)-10))`) show parameter scatter near the MLE but this is not a substitute for a proper profile. Without profiles, it is unknown whether key parameters of the stochastic leverage model (phi, sigma_eta, sigma_nu) are identifiable from the Treasury yield data, and whether the model is over-parameterized. This is a course-confirmed major issue (Wheeler et al. 2024, checklist item 5; Error 1.9 in the weakness reference).

### 5. Global Search Initialized from Previous mif2 Result (Anti-Pattern)

The global box search initializes each replicate with `mif2(if1[[1]], params=apply(yield_box,1,function(x)runif(1,x)))`. The first argument is `if1[[1]]`, a previous IF2 result object, rather than the base pomp object `yield.filt`. This is the classic anti-pattern identified by the pomp-global-search-init-audit skill: the global search replicates inherit the cooling schedule from `if1[[1]]`, which has already completed 200 mif2 iterations. The perturbations have been cooled to near zero, meaning the "global" replicates effectively begin with near-frozen parameters — they are not exploring the box from fresh starts. The resulting "global maximum" of -25.71 may not represent a true global optimum. The fix is to replace `mif2(if1[[1]], ...)` with `mif2(yield.filt, ...)` in the global search loop.

### 6. No Model Diagnostics (No Simulation-Based Fit Assessment)

No model diagnostics of any kind are presented for the fitted POMP model. The project does not compare simulated trajectories from the fitted model against the observed yield differences, does not examine conditional log-likelihoods across time, and does not plot the filtering distribution versus the observed data. Without such diagnostics, there is no basis for the implicit claim that the stochastic leverage model fits the Treasury yield data well. Wheeler et al. (2024) emphasize that visual comparisons and conditional log-likelihood plots are critical for identifying where and how the model succeeds or fails (checklist item 4).

### 7. No Non-Mechanistic Benchmark Comparison for the POMP Model

The POMP model is compared only to GARCH(1,1), not to any ARMA-class benchmark. While a GARCH comparison is relevant for financial volatility, an ARMA model on the differenced yield series provides a more direct and interpretable statistical baseline for the measurement model being used. The project does not compute or discuss ARMA log-likelihoods, making it impossible to assess whether the stochastic leverage model captures meaningful structure beyond a standard ARMA fit. This is a course-confirmed issue (Error 1.6; Wheeler et al. 2024 checklist item 2). Under the course conventions, absence of a benchmark is not automatically a major flaw — but given that the paper's primary claim is that POMP is better than the alternative, the specific GARCH comparison is undermined by the normalization issue (Issue 2 above), making a valid benchmark comparison essential for any conclusions about model quality.

---

## Minor Issues

### 8. Pairs Plot Filter Threshold Too Wide in Local Search

The local search convergence pairs plot uses `subset(r.if1, logLik > max(logLik) - 20)`, a threshold of 20 log-likelihood units. The standard course convention is to use a 10-unit threshold (as correctly applied in the global search). A 20-unit threshold includes parameter configurations far from the MLE region and may obscure the geometry of the likelihood surface near the optimum. The global search pairs plot correctly uses the 10-unit threshold.

### 9. Data Download Fragility and Reproducibility Risk

The data loading code fetches Treasury yield data directly from a live government URL at render time. This means the dataset is not archived in the project repository. If the URL format changes or the website goes down, the document cannot be reproduced. Additionally, the code uses `for (year in 1990:2021)` with individual HTTP requests per year — a fragile pattern. The CPI data is loaded from a local CSV file (`cpi.csv`), creating an inconsistency between how the two data sources are handled. Both should be archived locally or clearly documented for reproduction.

### 10. GARCH Log-Likelihood Reporting Convention Not Verified

The reported GARCH log-likelihood of -33.89 is obtained from `tseries:::logLik.garch()`, which is an internal function (indicated by the triple-colon `:::` access). The tseries package's GARCH log-likelihood may differ from the Gaussian log-likelihood used in the POMP model: it may omit normalization constants or compute the value per observation rather than in total. This convention ambiguity should be acknowledged, and ideally the GARCH log-likelihood should be re-computed with an explicit normalization to match the POMP measurement model.

### 11. Missing Sensitivity Analysis of the Loess Bandwidth

The Loess decomposition uses `span=0.5` for the trend and `span=0.1` for the high-frequency noise, with no justification for these choices and no sensitivity analysis. Different bandwidth choices can substantially change the extracted cycle component. The decomposition is presented as a complementary analysis rather than a primary result, which reduces its impact, but the lack of any discussion of span selection is a presentational weakness.

### 12. HP Filter Lambda Selection Not Justified

The Hodrick-Prescott filter uses `freq=100` (the lambda smoothing parameter) for monthly data. Standard HP filter practice for monthly data uses lambda=14400. The value lambda=100 corresponds to the standard annual-data convention and will substantially under-smooth the monthly series, producing a cycle component that may capture most of the low-frequency movement. This choice is not discussed or justified.

### 13. Coherency Plot Interpretation Incomplete

The squared coherence plot between HP-filtered yield and HP-filtered CPI is shown with no axis labels indicating which frequencies correspond to economically meaningful cycles (e.g., the business cycle at 3-8 years = 0.011-0.028 cycles per month). The conclusion that there is no association is based solely on the visual absence of a "significant peak," but no formal test or significance threshold is overlaid on the coherence plot to support this claim.

### 14. Title Typo

The document title contains a typo: "Extended Analysis on the U.S. 10-year Treasury Bond Yied" — "Yied" should be "Yield."

### 15. Initial Conditions Not Discussed for Identifiability

The model includes two initial value parameters, `G_0` and `H_0`, in the parameter transformation (`yield_partrans` applies log to sigma_eta and sigma_nu, and logit to phi). `G_0` and `H_0` receive IVP-scaled perturbations (`ivp(yield_rw.sd_ivp)` with `yield_rw.sd_ivp = 0.1`) but their sensitivity on model fit is never discussed. The pairs plots show `H_0` varied substantially across the global search replicates, suggesting it may be weakly identified. Without profile likelihoods or a formal identifiability analysis, the role of initial conditions in the fit is unknown.

---

## Files Consulted

### Skill Files
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`

### Project Files
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project04/blinded.html`
