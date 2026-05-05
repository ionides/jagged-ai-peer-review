# Peer Review: W24 Project 12
## "Time Series Analysis of COVID-19 Cases in Kent County"

---

## Summary

This project fits a Susceptible-Exposed-Infected-Recovered-Susceptible (SEIRS) compartmental model to 212 weeks of COVID-19 case counts in Kent County, Michigan (February 2020 to March 2024). The authors introduce time-varying transmission rates and reporting rates across three epidemic phases, a Gamma white-noise overdispersion term on the force of infection, and an importation parameter. A log-ARMA(2,1) benchmark is fitted on the transformed data, and a profile likelihood is computed for one reporting rate parameter. The model is fitted using iterated filtering (IF2) with local and global searches. 

Key strengths include a well-motivated SEIRS model design, a correctly implemented Jacobian correction for the ARMA benchmark log-likelihood, clear presentation of convergence diagnostics, and honest acknowledgment of the model's failure to outperform the ARMA benchmark. 

Critical weaknesses are: (1) the global IF2 search is initialized from a previous `mif2` result object rather than the base `pomp` object, invalidating the claim to global coverage; (2) the profiled parameter `rho3` is not held fixed during profile optimization (it appears in `rw.sd` throughout), so the reported profile likelihood and confidence interval are not valid; (3) many model parameters show no convergence in the global pairs plots, yet the authors do not diagnose this as a sign of model misspecification; and (4) the estimated waning-immunity rate `mu_RS` implies a ~32-year immunity period, which is biologically implausible and unacknowledged as a potential sign of structural misspecification.

---

## Major Issues

### 1. Global search initialized from a previous mif2 result, not the base pomp object

The global search code at line 774 sets `mf1 = local_mifs[[1]]` and then calls `mf1 |> mif2(params = c(guess, fixed_params), ...)` inside the parallel `foreach` loop. Passing a previous `mif2d_pomp` result as the first argument to `mif2()` causes each global replicate to inherit the cooling schedule of the completed local chain, which by this point has decayed to near zero. Although new `params =` are supplied from the random box, the IF2 perturbations are already near their final (negligibly small) values, so the optimizer effectively takes very few functional steps from the new starting point. This is confirmed by artifact inspection: the best global log-likelihood (-1403.97) is only 9.6 units better than the best local result (-1413.57), which is a modest improvement over 200 global replicates with 200 iterations and 5,000 particles each. The reported "global maximum" may be little more than a re-evaluation of the local-search region from slightly varied starts. The correct pattern is `mif2(kentSEIRS, params = c(guess, fixed_params), ...)`, where `kentSEIRS` is the base `pomp` object. The profile search code at line 957 commits the same error (`mf1 |> mif2(...)`), compounding the issue. (Wheeler et al. 2024, §Computational adequacy.)

### 2. Profile likelihood for rho3 is invalid: rho3 is not held fixed during optimization

The profile IF2 search uses `params_rw.sd` unchanged, which includes `rho3 = ifelse(data_weekly$week_num >= 125, 0.02, 0)`. Because `rho3` receives a non-zero random-walk perturbation for the last 87 time points, it is free to drift away from its profile-grid starting value during the IF2 run. Inspection of the saved artifact `lev3_rho3_profile.rds` confirms this: despite the profile design seeding 11 fixed values of `rho3` (seq(0, 1, by = 0.1)), the saved results contain 452 distinct `rho3` values, spanning [0, 1]. What is plotted is not a profile likelihood in the classical sense. The confidence interval [0.37, 1] derived from this curve is statistically invalid. The fix is to add `rho3 = 0` to `rw.sd` within the profile mif2 call, freezing `rho3` at its profile-grid value throughout optimization. (See also the `pomp-profile-guess-stratification-error` skill for closely related issues.)

### 3. Particle filter failures in the global diagnostic plot are under-diagnosed

The effective sample size (ESS) and conditional log-likelihood diagnostic plot (Figure titled "Global Search Diagnostic Plot") shows frequent near-zero ESS and large negative conditional log-likelihood spikes. The authors attribute these to holiday-season reporting artifacts and state they are "remedied later," but no model revision is actually attempted. Persistent ESS collapse is a sign that the model's process or measurement specification is inadequate at those time points — not merely a data quirk. Without addressing these failures, the reported likelihood estimates are unreliable because particle degeneracy at those time points contaminates the overall particle filter estimate. (Wheeler et al. 2024, §Model diagnostics; POMP checklist item 4.)

### 4. Implausible mu_RS estimate treated as a parameter choice rather than a misspecification signal

The optimal global parameter gives `mu_RS = 0.000603 weeks^-1`, corresponding to a 1,659-week (approximately 32-year) immunity period. The authors note this value is "close to 0" and question whether the SEIRS extension over SEIR is justified, but do not treat it as evidence of model misspecification. In Wheeler et al. (2024), an analogous situation — where the MLE for immunity loss was zero — was interpreted as evidence that the model was structurally wrong, not as a valid biological finding. The current analysis should either (a) test a nested SEIR model (fix `mu_RS = 0`) via a likelihood ratio comparison, or (b) interpret the near-zero estimate as evidence that the waning-immunity pathway is unidentifiable from this data and discuss the implications. (Wheeler et al. 2024, §Parameter identifiability; POMP checklist items 5 and 8.)

### 5. Insufficient model diagnostics: no conditional log-likelihood decomposition, no filtering-distribution comparison

The paper does not present per-time-point conditional log-likelihoods (beyond the raw `plot(global_mifs)` output), does not compare filtering-distribution simulations to forward simulations from the MLE, and does not examine reconstructed latent state trajectories (S, E, I, R) for biological plausibility. These diagnostics are essential for identifying where and how the model fails. The recurring ESS collapses visible in the diagnostic figure suggest specific weeks of severe model-data mismatch that deserve targeted investigation. (Wheeler et al. 2024, §Model diagnostics; POMP checklist item 4.)

### 6. Profile likelihood CI uses the profile maximum rather than the global maximum

The confidence interval cutoff is computed as `max(profile_results_rho3$loglik) - 0.5 * qchisq(df=1, p=0.95)`, using the maximum log-likelihood within the profile results (-1404.86) rather than the global MLE (-1403.97). This raises the cutoff by approximately 0.89 units, making the confidence interval appear narrower than it should be. The correct reference is the overall maximized log-likelihood from all searches combined. The practical effect here is small, but when the profile maximum substantially undershoots the global maximum (as it does here by ~0.9 units), the CI is anticonservative. (POMP checklist item 5.)

### 7. Weak parameter identifiability acknowledged but not acted upon

The pairs plots from both the local and global searches show broad ridges for most parameters (b1, b2, rho1, rho2, mu_EI, mu_RS, tau, iota), indicating that many parameters are weakly identified individually even though the likelihood has been maximized. The authors note this observation correctly but take no remedial action — they do not fix poorly identified parameters to literature-based values, compute additional profile likelihoods for other key parameters, or simplify the model. With 13 free parameters and data exhibiting 3 epidemic waves, the degree of non-identifiability is a substantive finding that deserves systematic treatment. (Wheeler et al. 2024, §Parameter identifiability; POMP checklist item 5.)

---

## Minor Issues

### 8. ARMA(2,2) equation contains a duplicate subscript

In the ARMA(2,2) equation (Section 3), the second MA term is written as `psi_1 * epsilon_{n-2}` instead of `psi_2 * epsilon_{n-2}`. This is a typo (the MA polynomial for ARMA(2,2) has coefficients `psi_1` and `psi_2`), though it does not affect the numerical results since the code correctly calls `arima(log_y, order = c(2, 0, 2))`.

### 9. Duplicate N column in profile results artifact

The saved file `lev3_rho3_profile.rds` contains two columns named `N...14` and `N...15`, both taking value 659,000. This arises because the profile guesses include `N = 659000` from `mutate(N = 659000)` and `fixed_params` also contains `N`. The duplication is harmless here (both are 659,000) but indicates that `fixed_params` is being appended redundantly in `c(guess, fixed_params)` when `N` is already set in `guesses`.

### 10. The force of infection in the Csnippet drops the alpha exponent

The text states the force of infection is `mu_SE(t) = beta(t)/N(t) * (I + iota)^alpha * zeta(t)` with `alpha = 1` cited from course notes. The Csnippet implements `foi = (Beta*(I+iota))/N`, which is the `alpha = 1` special case and is numerically equivalent. However, since `alpha` appears in the mathematical specification but not in `paramnames` or the Csnippet, a reader may be confused about whether `alpha` was estimated or fixed. A comment in the code or a clarifying sentence in the text would resolve this.

### 11. SEIRS model fails to beat ARMA benchmark but this failure is not fully discussed

The paper states that the SEIRS model log-likelihood (-1404.0) is 32.5 units below the ARMA(2,1) benchmark (-1371.5) and attributes this to "the difficulties in appropriately modeling the COVID-19 pandemic." This is insufficient. A 32.5-unit gap represents a highly significant difference (chi-squared p-value effectively zero). The authors should discuss whether the gap is expected given the different measurement models (discretized Normal vs. log-Normal), whether improving the measurement model or addressing ESS failures might close it, and whether the mechanistic model adds interpretive value despite the worse likelihood. (Wheeler et al. 2024, §Benchmark comparison; POMP checklist item 2.)

### 12. No model comparison between SEIR and SEIRS

The waning-immunity parameter `mu_RS` is near zero, and the authors note it raises questions about the SEIRS vs. SEIR choice. A formal likelihood ratio test comparing a restricted SEIR model (mu_RS fixed at 0) versus the full SEIRS model would take one line of additional analysis and would directly address this question. Without it, the paper does not provide statistical justification for the added complexity of the SEIRS structure. (POMP checklist item 8.)

### 13. Reporting rate intervals are inconsistent between transmission and reporting rate piecewise definitions

The transmission rate piecewise function uses intervals [1,54], (54,72], (72,212], while the reporting rate piecewise function uses [1,54], (54,125], (125,212]. The mismatch is not biologically motivated in the text — the paper explains why the transmission epochs coincide with variant emergence but does not explain why the reporting rate changes at week 125 (July 2022) rather than week 72 (July 2021). A sentence justifying the differing breakpoints would improve clarity.

### 14. Initial conditions fixed rather than estimated, with no sensitivity analysis

Only `N` is formally fixed; all other compartment sizes at t=0 are determined by the single estimated parameter `eta`. Setting `S(1) = eta * N`, `E(1) = 0`, `I(1) = 1`, `R(1) = (1-eta)*N - 1` effectively fixes the exposed and infected populations at t=0 to biological minimum values, which may not match the epidemic state in February 2020. The authors acknowledge this limitation in the Conclusion but do not assess sensitivity of the results to these assumptions. Estimating E(0) and I(0) separately, or at minimum assessing how the likelihood changes under alternative initializations, would strengthen the analysis. (POMP checklist item 13.)

### 15. No sessionInfo() or package version documentation

The Rmd document does not include a `sessionInfo()` call or any documentation of R and package versions. Given that the `pomp` API has changed across versions, results may not be reproducible on current CRAN releases without explicit version pinning. A `sessionInfo()` block or an `renv` lockfile would address this. (Code supplement checklist, reproducibility section.)

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
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_mifs_global.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_mifs_local.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_rho3_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_seirs_global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_seirs_local_search.rds`
