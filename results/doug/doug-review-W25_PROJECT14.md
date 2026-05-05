# Peer Review: W25 Project 14
## "Influenza Case Trends in Nova Scotia: Capturing the Seasonal Behavior"

---

## Summary

This project fits three POMP compartmental models (SIR, SIRS, SEIRS) with seasonal transmission to weekly lab-confirmed influenza case data from Nova Scotia (2014–2019). The SEIRS model is identified as the best-fitting model based on log-likelihood comparison. The project demonstrates genuine effort in constructing biologically motivated models with stochastic dynamics and negative binomial measurement noise, and the SEIRS implementation is largely correct in structure. However, the analysis is undermined by several critical errors: the SIRS model uses a population size corresponding to the United States rather than Nova Scotia (off by a factor of 335), which produces a numerically anomalous positive log-likelihood; the cross-model comparison in the conclusion inverts the log-likelihood interpretation; and the three models use three different measurement model specifications (NegBin, Poisson, NegBin) making direct likelihood comparisons invalid. Additionally, no non-mechanistic benchmark comparison is provided, the global search for SEIRS uses the local-search chain as the first argument to mif2 (anchoring it to the local optimum), and the profile likelihood confidence interval collapses to a single point due to insufficient computational effort.

---

## Major Issues

**1. SIRS model uses U.S. population (N = 3.25e8) instead of Nova Scotia population**

The SIRS model is initialized with `N = 3.25e8` (325 million), which is approximately the population of the United States, not Nova Scotia (~969,000 people in this period). The SEIRS model correctly uses `N = 969400`. This error causes the force of infection `beta * I / N` to be approximately 335 times smaller than intended, the reporting rate `rho * H` to be comparably inflated, and all parameter estimates for the SIRS model to be biologically meaningless. The Poisson measurement model with `lambda = rho * H` near zero produces near-unit densities for zero-count observations (which predominate in influenza data), explaining the anomalous positive log-likelihood of +19821.71 reported for the SIRS model. The fix is to set `N = 969400` (or an appropriate Nova Scotia population estimate for the 2014–2019 period) in the SIRS `params` vector.

**2. Inverted log-likelihood interpretation in conclusion**

The conclusion states: "the SEIRS model performs best, with the lowest value of -590.46, followed by the SIR model at -761.97." This statement inverts the interpretation of log-likelihood: higher log-likelihood (i.e., less negative, closer to zero) indicates better fit, not lower. The SEIRS model achieves the highest (least negative) log-likelihood among the three models, which is correctly identified as the best fit, but the word "lowest" is incorrect. More critically, the SIRS log-likelihood of +19821.71 is reported without any acknowledgment that a positive log-likelihood under a Poisson or negative binomial measurement model on integer count data is numerically impossible and signals a fundamental model error. A positive total log-likelihood over 262 weekly observations implies individual observation likelihoods greater than 1, which cannot occur.

**3. Cross-model log-likelihood comparison is invalid due to different measurement models**

The three models use different measurement models: SIR uses negative binomial (`dnbinom_mu`), SIRS uses Poisson (`dpois`), and SEIRS uses negative binomial (`dnbinom_mu`). A direct numerical comparison of log-likelihoods across these models is not valid, because the Poisson model is a constrained special case of the negative binomial and will always produce an equal or lower log-likelihood on the same data when the negative binomial's overdispersion parameter is estimated freely. Moreover, all three models use different population sizes (SIR: 100,000; SIRS: 325,000,000; SEIRS: 969,400), different starting parameters, and different rho values. Wheeler et al. (2024) note that model comparisons require the same data, the same observation model structure, and comparable parameters. None of these conditions are met here.

**4. No non-mechanistic benchmark comparison**

The ARIMA analysis in the EDA section is used solely for model selection (choosing lag orders). The log-likelihood of the best ARIMA model is never computed and compared to the POMP models. Wheeler et al. (2024) identify benchmark comparison against non-mechanistic models as the single most diagnostic check for whether a mechanistic model captures meaningful structure. Without such a comparison, it is impossible to assess whether the SEIRS model's log-likelihood of approximately -587 represents a genuine improvement over a well-fitted ARIMA or SARIMA baseline. The authors should fit an ARIMA(p,1,q) model with the best AIC orders to the original (non-differenced) data on an appropriate transformed scale, compute its log-likelihood, and compare it to the SEIRS log-likelihood.

**5. SEIRS global search uses local-search chain as first argument to mif2**

In `seirs_gs.R` (line 103), the global search is implemented as `mf1 |> mif2(params=c(guess,fixed_params)) |> mif2(Nmif=Nmif)`, where `mf1 = local_mifs_seirs[[1]]`. Using a previous mif2 result object as the first argument to a new mif2 call inherits the cooling schedule of that chain (see `pomp-global-search-init-audit`). Since `mf1` has already completed its Nmif=100 iterations with `cooling.fraction.50=0.5`, the cooling perturbations at the end of `mf1` are near zero. When the global search calls `mf1 |> mif2(params=guess)`, the new starting parameters are applied but the cooling schedule from `mf1` is inherited — meaning the first mif2 call in the global search runs with near-zero perturbations and cannot effectively explore from the new random starting point. The fix is to replace `mf1 |> mif2(params=c(guess,fixed_params))` with `seirs_pomp |> mif2(params=c(guess,fixed_params))`, using the base pomp object rather than the local-search chain. This error is likely responsible for the fact that the profile likelihood (which also uses mf1 but different guesses) found a log-likelihood of -577.4, which is 9.2 units better than the reported global search maximum of -586.6.

**6. Profile likelihood singleton confidence interval**

The profile likelihood analysis over rho produces a result where only a single point lies above the chi-squared cutoff (`max(loglik) - 1.92`), producing a CI of [0.001769433, 0.001769433]. This singleton CI is almost certainly a Monte Carlo noise artifact rather than a genuine representation of the likelihood surface. The `seirs_pf.R` script runs exactly one mif2 call per guess row with no inner loop over multiple restarts per profile grid value. With 121 rows covering 68 unique rho values and a single mif2 chain per row, the profile curve has insufficient precision to determine the true constrained optimum at each rho value. Wheeler et al. (2024, §Parameter identifiability) require profile likelihoods to be computed with sufficient computational effort. The fix requires running multiple mif2 restarts (e.g., 10–20) per profile grid point with diverse starting parameters, and evaluating the log-likelihood via `logmeanexp` over at least 10 pfilter replicates per point.

**7. Profile likelihood maximum exceeds global search maximum by 9.2 log-units**

The profile likelihood maximum (-577.4) is substantially better than the global search maximum (-586.6) by 9.2 log-likelihood units. This means the profile search, which was intended as a constrained optimization, accidentally found a parameter region that the global search had not explored. Under a correctly implemented global search, the global maximum should be at least as high as the profile maximum for any fixed value of a profiled parameter. A gap of 9.2 units indicates the global search failed to find the MLE region and that the reported "global maximum" is not near the true optimum. Wheeler et al. (2024, §Computational adequacy) note that this kind of improvement from increasing search effort indicates the computation was insufficient. The reported log-likelihoods and derived conclusions are therefore unreliable.

**8. SIR global search second mif2 call uses previous chain**

In the SIR global search (blinded.Rmd, lines 418–434), the pattern `mf <- mif2(mf, ...); mf <- mif2(mf)` is used. The second `mif2(mf)` call uses the previous mif2 result as the first argument without specifying new parameters. This inherits the cooling schedule state from the first mif2 call. While the second call uses the same parameters that converged after the first, it does not add genuinely new exploration because the cooling schedule has already decayed. The fix is to evaluate the log-likelihood directly after the first mif2 call and remove the redundant second `mif2(mf)` call, or to restructure the two calls as a single combined search with higher Nmif.

---

## Minor Issues

- **Inconsistent observation count**: The text states "262 observations" in one place and "261 observations" in another (lines 69 and 69 of the document). The actual dataset contains 262 rows in the filtered date range. This inconsistency should be resolved.

- **SIR mu_IR biologically implausible**: The SIR local search best parameter has `mu_IR ≈ 0.00366` per week, implying a mean infectious period of approximately 273 weeks (1,913 days). The typical influenza infectious period is 3–7 days. The text acknowledges "very low recovery rate" but does not identify this as a sign of model misspecification (Wheeler et al. 2024, §Corroboration with scientific knowledge). The authors should compare estimated parameters to independent epidemiological literature and flag implausible values as evidence of structural model inadequacy.

- **Accumulator variable accumulates recoveries, not new infections**: All three models (SIR, SIRS, SEIRS) set `H += dN_IR`, linking observed case counts to the flow from I to R (recoveries). The SIR model text explicitly states that "reported cases are modeled as a noisy observation of the newly recovered individuals." However, lab-confirmed influenza cases in surveillance databases typically record newly identified (tested/confirmed) infections, not recoveries. Recovering patients rarely seek new medical attention. If the data records newly confirmed infections, the accumulator should track `dN_SI` (or `dN_SE` for SEIRS). While the authors' choice may be defensible as a proxy (each infection produces exactly one recovery), this assumption should be stated and justified explicitly.

- **No model diagnostics beyond visual simulations**: The paper does not present conditional log-likelihood plots (per-observation log-likelihoods over time), filtering distribution comparisons, or reconstructed latent state trajectories conditioned on the data. Wheeler et al. (2024, §Model diagnostics) identify these as essential tools for understanding where and how a model succeeds or fails. Adding a plot of per-observation log-likelihood contributions would identify which influenza seasons are poorly explained by the model.

- **Profile likelihood covers only rho**: The profile likelihood analysis is limited to the reporting rate rho. No profiles are presented for the transmission rate Beta0, seasonal amplitude amp, or the recovery rate mu_IR, which are arguably more policy-relevant for understanding influenza dynamics. The rho profile should be supplemented with profiles for at least the key biological parameters.

- **SIRS model uses Poisson measurement model without justification**: The SIRS model uses `dpois` / `rpois` for the measurement model, while the SIR and SEIRS models use negative binomial. Influenza case counts are well-known to exhibit overdispersion beyond Poisson. No justification is given for this design choice, and it makes the SIRS model less realistic regardless of the N error.

- **SIRS beta switch at t=261 is not biologically motivated**: The SIRS model uses a threshold `if (t < 261) beta = a; else beta = b;` to distinguish "pre-pandemic" and "pandemic" seasons, but the data spans 2014–2019 (no pandemic year). The labels `a` and `b` (for "pre-pandemic" and "pandemic") do not correspond to any identifiable pandemic event in this time period, making this structural choice uninterpretable. No justification is provided for why t=261 is a meaningful threshold.

- **SEIRS mu_EI estimate yields implausibly short latent period**: The SEIRS local search best parameters show `mu_EI ≈ 1.21` per week, implying a mean latent period of approximately 0.83 weeks (5.8 days). For influenza, the incubation period is typically 1–4 days, so this estimate is at the high end but within the plausible range. However, no comparison to independent literature values is made, and the instability of the mu rates noted in the trace plots deserves more discussion.

- **SIRS best_index mismatch in conclusion**: The conclusion code (blinded.Rmd, lines 1342–1357) assigns `mif_sirs <- local_mifs_sirs[[best_index]]` where `best_index` was computed for the SIR model (ranging over 5 replicates), not the SIRS model (which has 10 replicates). This means the SIRS model used in the final comparison may not be the best-fit SIRS chain. Given the positive log-likelihood error makes this comparison invalid anyway, this is a secondary concern, but the code structure should index SIRS chains with a separate `best_index_sirs`.

- **SEIRS global search seeded from influenza_params.csv but CSV state is ambiguous**: The seirs_gs.R and seirs_pf.R scripts both read and write to `influenza_params.csv`, with the document relying on a specific execution order (ls.R first, then gs.R, then pf.R). If these scripts are not run in that order, or if the CSV is not reset before re-running, results from a previous run contaminate subsequent runs. The use of `bake()` in seirs_ls.R protects the local search but not the CSV. The paper should explicitly state the execution order and include a reproducibility note.

---

## Files Consulted

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
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_gs.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_ls.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_pf.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_results.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_pf.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/influenza_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/sirs_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/Lab-confirmed_Influenza_Cases.csv`
