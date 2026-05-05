# Peer Review: W22 Project 08 — Analysis of Covid-19 Cases in Turkey

## Summary

This project fits a custom SEIREIR (Susceptible–Exposed–Infected–Recovered–Exposed–Infected–Recovered) compartmental model to daily COVID-19 data from Turkey in 2020, motivated by the presence of two apparent infection waves attributed to the original variant and a new beta variant. An ARIMA(2,1,0) model is fitted first as a declared benchmark. The POMP model is estimated via iterated filtering (mif2) using a local search followed by a global search from 160 starting points. While the project demonstrates genuine scientific motivation for the two-wave structure and uses appropriate likelihood-based inference machinery, it is compromised by a fundamental mismatch between the observation data variable and the accumulator variable, an invalid log-likelihood comparison between ARIMA and the SEIREIR model, a global search initialization error that anchors the search to the local optimum, a global search box that is too narrow relative to the converged parameter estimates, and a discrepancy between the log-likelihood value reported in the text and the value in the stored artifacts. No profile likelihoods are computed, so parameter identifiability is entirely unassessed.

---

## Major Issues

### 1. Fundamental mismatch between data variable and accumulator variable

The observation variable is constructed as `turkey$cases = turkey$Confirmed - turkey$Deaths - turkey$Recovered`. Because the Kaggle dataset records cumulative totals for Confirmed, Deaths, and Recovered, this expression computes the number of **active cases on each day** — a stock variable representing how many people are currently infected. The accumulator `H`, by contrast, is incremented as `H += (dN_IR_o + dN_IR_b)`, which counts **new recoveries per time step** — a flow variable. The model therefore evaluates `dnbinom_mu(reports, k, rho*H, give_log)` comparing a daily count of active infections to a scaled count of new recoveries. These two quantities have different units, different dynamics, and different magnitudes. The reporting rate `rho` absorbs whatever scaling is required to make the fit numerically possible, and all parameter estimates derived from this misspecified likelihood are unreliable. The fix requires either (a) recomputing `cases` as the daily increment in confirmed cases (`diff(turkey$Confirmed)`, excluding deaths and recoveries) and accumulating new infections in H, or (b) directly linking the measurement model to the `I_o + I_b` stock compartments rather than using an accumulator at all.

### 2. Accumulator variable tracks recoveries, not detections

Even setting aside the stock-vs-flow problem, the accumulator variable H accumulates recoveries `dN_IR_o + dN_IR_b` rather than new detections (entries into the infected compartment, `dN_EI_o + dN_EI_b`). For a model to be compared against confirmed-case data, the accumulator should reflect the flow of newly confirmed (or newly infectious) individuals, not the flow of individuals leaving the infectious compartment. Accumulating recoveries means that a faster recovery rate paradoxically increases H and inflates the predicted case count, distorting all rate parameters. See Wheeler et al. (2024) §Measurement model specification and the `pomp-accumvar-semantic-audit` principle.

### 3. Global search initialized from a previous mif2 result

The global search uses `mf1 <- mifs_local[[1]]` as the first argument to `mif2()` inside the global search loop. Because `mf1` is a previously run `mif2d_pomp` object, the global search inherits the cooling schedule of the local chain, which has already progressed 50 iterations and is at or near its final cooling state. New random starting parameters drawn from the box are applied via the `params=` argument, but the inherited cooling schedule means that random-walk perturbations are near their minimum size from the first iteration, so the optimizer cannot effectively explore the new starting regions. The reported "global maximum" is consequently not a genuine global maximum; it reflects a local optimum anchored near the local-search solution. The fix is to replace `mf1` with the base `pomp` object `measSEIREIR2` in the global search `mif2()` call. See `pomp-global-search-init-audit`.

### 4. Global search box excludes the region containing the best-fit parameters

The stated global search box bounds are `Beta_o ∈ [1, 100]`, `Beta_b ∈ [50, 140]`, `Beta_or ∈ [0.5, 10]`, and `Beta_r ∈ [30, 70]`. Inspection of the stored `global_search.rds` artifact reveals that the best-fit parameter values in the global search are `Beta_o = 129.3`, `Beta_b = 150.6`, `Beta_or = 2.71`, and `Beta_r = 107.7` — all substantially outside the stated box bounds. Of the 160 global replicates, 9 have `Beta_o > 100`, 20 have `Beta_b > 140`, and 28 have `Beta_r > 70`. These solutions were reached only because IF2 perturbed the parameters outside their initialization box during optimization — an accidental rather than systematic mechanism. The global search therefore provides no reliable coverage of the high-likelihood region for the key transmission parameters. The box should be widened to bracket the MLE region found by the local search. See `pomp-global-search-box-misalignment`.

### 5. Reported log-likelihood is inconsistent with stored artifacts

The conclusion section states "the maximum log likelihood of our POMP model is -2336." The stored `covid_params.csv` artifact, which aggregates all local and global search results, shows a maximum log-likelihood of **-2308.63** (with standard error 0.012). The discrepancy is approximately 27 log-likelihood units — a substantial difference that cannot be explained by Monte Carlo noise. Moreover, the simulation plot displayed after the global search uses parameters `(Beta_o=40.15, Beta_b=36, Beta_or=0.66, Beta_r=57)`, which differ substantially from the maximum-likelihood parameter values in the csv file `(Beta_o=67.04, Beta_b=51.40, Beta_or=0.76, Beta_r=66.58)`. These inconsistencies suggest the text was written at an earlier stage of the analysis and not updated to reflect the final results. See `pomp-artifact-audit` and `pomp-wrong-variable-display-audit`.

### 6. Invalid log-likelihood comparison between ARIMA and SEIREIR models

The conclusion states that "the maximum log likelihood of the SEIREIR model is -2336, which is much smaller than that of ARIMA" and concludes the POMP model "cannot beat the ARIMA." The ARIMA(2,1,0) log-likelihood is -1692.303 (Gaussian on differenced data), while the SEIREIR model is evaluated under a negative binomial measurement model on active cases. These likelihoods measure probability density under different distributional families on different transformations of the data; their numerical values are not directly comparable. No conclusion about relative model adequacy can be drawn from this comparison. The correct approach would be to evaluate both models under a common scoring rule (e.g., out-of-sample CRPS or a shared negative binomial log-likelihood), or to use the ARIMA only as a descriptive benchmark acknowledging the non-comparability of their likelihoods. See Wheeler et al. (2024) §Benchmark comparison and the `sarima-baseline-audit` principle.

### 7. No profile likelihoods and no parameter confidence intervals

The project estimates 8 free parameters but presents no profile likelihoods, no Monte Carlo adjusted profile (MCAP) intervals, and no other form of uncertainty quantification. The pairs plot from the local search shows that eta does not show a clear optimum ("does not converge"), and the text acknowledges this, yet no follow-up analysis is performed. Without profile likelihoods, it is impossible to assess whether parameters such as `Beta_o`, `Beta_b`, `rho`, and `eta` are identifiable from the data. The claim that the model captures the COVID-19 dynamics in Turkey rests on point estimates whose reliability is entirely unverified. See Wheeler et al. (2024) §Parameter identifiability and uncertainty.

### 8. Biologically implausible initial conditions for the beta-variant compartment

The initialization snippet sets `R_b = nearbyint((1-eta)*N)`, placing approximately `(1 - 0.1) × 84,340,000 ≈ 75.9 million people` into the recovered-from-beta compartment at time zero (March 2020). This is biologically impossible: no one had been infected by the beta variant at the start of the time series, and Turkey's total population is only 84.3 million. The intended interpretation appears to be that `R_b` serves as an initial susceptible pool for the second wave, but this is achieved by mislabeling a susceptible subgroup as "recovered" from a variant that did not yet exist. The correct approach would be to track a susceptible-to-beta compartment explicitly and initialize it to a biologically plausible value. See Wheeler et al. (2024) §Initial conditions.

---

## Minor Issues

- **Population figure error in text**: The simulated graphs section states "We fix N=843400, the population of Turkey in 2020." Turkey's 2020 population is approximately 84.3 million. The params vector correctly uses `N=84340000`, but the in-text comment is off by two orders of magnitude (843,400 is approximately the population of a small city, not the country). This should be corrected to 84,340,000.

- **Local search uses `%do%` (sequential) instead of `%dopar%` (parallel)**: The local search chunk uses `foreach(i=1:20, .combine=c) %do%` rather than `%dopar%`. Although `registerDoParallel()` is called earlier, the sequential operator negates the parallelization. For 20 chains this is a minor efficiency concern, but given that parallel computation is set up and `%dopar%` is used elsewhere in the code, this inconsistency should be corrected.

- **Global search uses Np=1000, local uses Np=2000**: The global search evaluates the likelihood with 1000 particles per replicate but the local search uses 2000. Reducing particle count in the global search may increase Monte Carlo noise in likelihood estimates, complicating comparison between the two stages. The text does not justify this choice.

- **Hard-coded variant emergence at t=125 without justification**: The code adds `if (t == 125) e = 10` to `E_b`, seeding the beta variant at day 125. The choice of t=125 and the seed size of 10 are not justified in the text. Day 125 from March 11, 2020, corresponds to approximately mid-July 2020, which the authors attribute to tourism reopening, but the beta variant did not emerge in Turkey until late 2020. The text's invocation of "new variants" to explain the second wave is epidemiologically questionable for the data period covered.

- **No model diagnostics reported**: The project does not present conditional log-likelihood plots, effective sample size (ESS) monitoring across the particle filter, or filtering-distribution simulations conditioned on data. The only diagnostic is a visual overlay of simulations on data. These diagnostics are essential for identifying periods of poor model fit. See Wheeler et al. (2024) §Model diagnostics.

- **Insufficient number of IF2 iterations**: Both local and global searches use Nmif=50 iterations. For a model with 8 free parameters and complex multi-wave dynamics, 50 iterations is typically insufficient for convergence. The convergence traces in the document confirm that several parameters (notably `eta`) have not stabilized by iteration 50.

- **Model selection by LRT between ARIMA(2,1,1) and ARIMA(2,1,0) is applied incorrectly**: The text uses a likelihood ratio test to choose between ARIMA(2,1,1) and ARIMA(2,1,0), and selects ARIMA(2,1,0). The stated reason is that "AIC penalizes less for complexity" — but AIC does penalize for complexity (with a +2k term), and the LRT at 95% confidence is the correct tool for nested model comparison. The reasoning is confused but the conclusion (choosing the simpler model with fewer parameters if the LRT does not favor the complex model) is directionally correct.

- **Notation inconsistency in model equations**: The equations use `dSE_o(t)`, `dEI_o(t)`, etc., with parenthetical `t` suggesting continuous-time differentials, but the implementation uses discrete-time Euler steps with `rbinom` draws. The notation should either be changed to match the discrete-time implementation (e.g., `Delta N_{SE_o}(t)`) or the Euler approximation should be explicitly acknowledged.

- **No discussion of model extendability or code availability**: Code is embedded in the Rmd file, which is positive for reproducibility. However, the `local.RData` file referenced by `load('local.RData')` is not present in the project folder — only `local_search.rds` is present — making the local search results section non-reproducible as written.

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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/covid_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/covid_19_data_tr.csv`
