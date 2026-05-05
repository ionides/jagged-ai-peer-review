# Peer Review: W25 Project 16
## "Analyzing Whooping Cough with ARMA and POMP"

---

## Summary

This project fits ARMA-family models (ARMA(2,4) and ARCH(1)-X) and POMP compartmental models (SIR and SEIR) to weekly whooping cough case counts in the East North Central US states (2017–early 2025). The authors progress from a simple ARMA residual analysis, through an ARCH model for conditional heteroskedasticity, to a stochastic SIR model for the 2024 outbreak and an SEIR model for the full time series. The POMP analysis uses particle-filter-based IF2 inference with `mif2()`, which is methodologically appropriate. Key strengths include a thoughtful motivation for model extensions, the use of bake/cache files for reproducibility, and honest acknowledgment of model failures.

However, the project has several serious weaknesses. First, the central comparative conclusion — that the ARCH model outperforms the POMP model because its log-likelihood (–1203) exceeds the SEIR log-likelihood (–1442) — is statistically invalid: the two likelihoods are computed under fundamentally different observation models on different data transformations, and no Jacobian argument rescues this comparison. Second, all three global IF2 searches initialize from a previous `mif2` result object rather than the base `pomp` object, which anchors each global search near its corresponding local-search solution rather than exploring fresh starting points across the box. Third, all POMP models accumulate recoveries (`dN_IR`) in the accumulator variable `H`, while the data records new confirmed infections — a semantic mismatch that biases all parameter estimates. Fourth, the SIR global search box upper bound for Beta (250) is below the MLE found at 259, indicating the global optimum was found only through accidental IF2 drift outside the box. These errors collectively undermine the validity of all parameter estimates, model comparisons, and the paper's primary conclusion.

---

## Major Issues

### 1. Invalid log-likelihood comparison between ARCH and POMP models

The paper's central conclusion — "our ARCH model demonstrated superior performance with higher log-likelihood (–1203 vs. –1442)" — is statistically invalid. The ARCH model is fitted to the first-differenced series under a Gaussian observation model, while the SEIR POMP model is fitted to the original weekly count series under a negative binomial observation model. These two likelihoods are defined over different data transformations and entirely different distributional families; numerically comparing them has no statistical justification.

The authors argue (Comparisons section) that "since first differencing is a linear transformation with a constant Jacobian, we can directly compare these fits after accounting for the dropped initial term." This argument is incorrect. While the Jacobian of the differencing transform is 1 (so there is no log-determinant correction for the transformation of the density from increments back to levels), the deeper issue is that the ARCH model conditions on the Gaussian assumption for increments, while the POMP model conditions on a negative binomial assumption for counts. The probability spaces are incompatible: one is defined over the reals, the other over non-negative integers. The Jacobian argument addresses density transformation under a change of variables for the same model, not comparability of likelihoods from two different models applied to two different-scale observations.

Additionally, the ARCH model is fitted to the differenced series (implicitly conditioning on a Gaussian distribution for increments), whereas pertussis case counts are non-negative integers that are zero in most non-outbreak weeks. For such data, the Gaussian assumption on increments produces a qualitatively different likelihood than a count-data model, regardless of the transformation. The fix is to either (a) drop the quantitative comparison entirely and note that the models address different aspects of the data, or (b) evaluate both models under a common observation model and data representation — for example, both under a negative binomial model on original counts, or both using a proper scoring rule (e.g., CRPS) on the original scale.

**Related skill:** `sarima-baseline-audit` (invalid log-likelihood comparison between ARMA-family and POMP models with different observation models).

### 2. Global search initialized from previous mif2 result objects (all three searches)

All three global IF2 searches follow the same pattern: `mf1 <- local_mifs[[1]]` and then inside the `foreach` loop, `mf1 |> mif2(params=c(guess, fixed_params))`. This passes the previous local IF2 result as the first argument to the global search's `mif2()` call, which inherits the cooling schedule — already at or near its final cooled-down state — from the local search. The consequence is that the global search performs very few functional IF2 iterations from each new random starting point before the perturbations shrink to near zero, effectively anchoring each global replicate near the local-search solution rather than exploring the parameter box from fresh starts.

This pattern appears at lines 609–617 (SIR global), 941–950 (SEIR global), and 1187–1195 (SEIR one-data-point-removed global). All three global searches are affected.

The fix is to replace `mf1 |> mif2(params=c(guess, fixed_params))` with `coughSIR |> mif2(params=c(guess, fixed_params), Np=..., Nmif=..., ...)` (using the base `pomp` object as the first argument, not the local mif result), specifying all IF2 hyperparameters explicitly in the global search call. This ensures each replicate starts from a fresh cooling schedule.

**Related skill:** `pomp-global-search-init-audit`.

### 3. Accumulator variable H tracks recoveries, not new infections

In all three POMP models (SIR at line 464, SEIR at line 762, SEIR-comparison at line 1044), the accumulator variable `H` is updated as `H += dN_IR`, meaning it accumulates the flow from I to R (recoveries from infectious). The measurement model then links the observed weekly case counts to this accumulator via `lik = dnbinom_mu(reports, k, rho * H, give_log)`. However, the surveillance data records newly reported whooping cough cases, which correspond to new individuals entering the infectious class (or detected as confirmed cases), i.e., the flow `dN_SI` in the SIR model or `dN_EI` in the SEIR model — not recoveries.

Using recoveries as the proxy for reported cases is a semantic mismatch. In a well-specified SIR model with short mean infectious duration, these two flows will be correlated but not identical. Because `mu_IR` controls how fast individuals leave the infectious compartment, the optimizer will adjust `mu_IR` and `rho` to compensate for the mismatch rather than estimating true biological rates. The SIR MLE for `mu_IR` is 6.92 per week (mean infectious period ≈ 1 day), which is biologically implausible for pertussis (typical infectious period is 1–3 weeks). This implausibility is likely a direct consequence of the accumulator mismatch.

The fix is to change `H += dN_IR` to `H += dN_SI` in the SIR model and to `H += dN_EI` in the SEIR model (or `H += dN_SE` depending on which transition represents detection). This change should be applied to all three model implementations. Parameter estimates must then be recomputed.

**Related skill:** `pomp-accumvar-semantic-audit`.

### 4. SIR global search box excludes the region containing the MLE

The SIR global search specifies an upper bound of `Beta=250` for the transmission rate (line 598–601). However, the MLE found in the global search artifact (`data/global-SIR.rds`) has `Beta = 258.98`, which is outside the declared box. The global search found this solution only through IF2 drift beyond the initial box bounds — accidental exploration rather than systematic coverage.

This is compounded by the fact that 214 of the 600 search replicates (36%) returned `NA` log-likelihoods, suggesting particle degeneracy for a large fraction of starting points. Only 386 replicates produced finite log-likelihoods. Among those, 200 (52%) are within 5 log-likelihood units of the best — a moderate but not conclusive convergence pattern.

The fix is to extend the box upper bound for Beta beyond the local-search MLE, e.g., to at least `Beta=300` or `Beta=500`, and to diagnose and address the 36% particle degeneracy (likely caused by the very large `Beta` values combined with small `Np=1000` in the local search, which also uses the anti-pattern from issue #2).

**Related skill:** `pomp-global-search-box-misalignment`.

### 5. SEIR model fails to distinguish outbreak from endemic transmission (base_beta ≈ outbreak_beta at MLE)

The SEIR model introduces a time-varying transmission rate that switches from `base_beta` to `outbreak_beta` at week 332 (April 2024). However, the global search MLE has `base_beta = 8.76` and `outbreak_beta = 8.72` — a difference of less than 0.04, which is negligible. The parameter `outbreak_beta` is therefore unidentifiable as a separate driver of the 2024 surge: the optimizer finds essentially the same value for both periods. This defeats the scientific purpose of the time-varying beta parameterization.

Moreover, only 5 out of 500 SEIR global search replicates (1%) fell within 5 log-likelihood units of the best, indicating extremely poor convergence. The loglik range spans from –35040 to –1471, indicating that the vast majority of starting points led to particle degeneracy or numerical failure. The SEIR model's log-likelihood of –1471 may not be near the global optimum for this parameterization.

The authors acknowledge that the SEIR model simulations "fail to capture the surge in reported whooping cough cases" but do not discuss the parameter-identifiability consequence: if `base_beta ≈ outbreak_beta`, the model cannot attribute the 2024 surge to any distinct change in transmission dynamics.

Profile likelihoods are entirely absent for both models. Without profiles, it is impossible to assess whether any key parameters are identified from the data. Given the near-identical beta values at the SEIR MLE and the implausible mu_IR estimate at the SIR MLE, there is strong circumstantial evidence of identifiability problems.

**Related skills:** POMP checklist items #5 (parameter identifiability) and #6 (computational adequacy).

### 6. No benchmark comparison for the mechanistic models

The paper does not compare either POMP model against a non-mechanistic statistical benchmark such as an auto-regressive negative binomial or Poisson model fitted to the same original count data. The ARCH model is used as a baseline, but as documented in issue #1, this comparison is invalid due to different observation models. There is no valid quantitative benchmark to establish whether the POMP model captures any meaningful structure beyond what a simple count-data time-series model would achieve.

Per Wheeler et al. (2024): none of the 32 papers in their Haiti cholera literature review performed such a comparison, and their auto-regressive negative binomial benchmark revealed that some models failed to beat it. Without a comparable benchmark here, it is impossible to assess whether the mechanistic SIR/SEIR structure is contributing scientifically useful information.

**Related skill:** POMP checklist item #2 (benchmark comparison).

---

## Minor Issues

- **Label error in EDA plot**: The `plot3` object labels its y-axis as "Births" (line 201) but the plot title says "Weekly Deaths" and the data is `Deaths`. This is a copy-paste error from `plot2`.

- **ARCH-X specification**: The ARCH model uses the lagged pertussis case count as an external regressor in the variance equation (`x_exog`). However, `ugarchfit` is called with `data = pertussis_diff` (line 308) but the spec was built with the lagged-level series as an external regressor of length `length(pertussis_diff)`. The mismatch between the length of the differenced series and the lagged series (which was manually trimmed) should be verified for off-by-one alignment.

- **rw.sd for global SIR search not explicitly set**: The global SIR search (lines 611–623) calls `mf1 |> mif2(params=c(guess, fixed_params)) |> mif2(Nmif=100)`. No `rw.sd`, `Np`, `Nmif`, or `cooling.fraction.50` arguments are passed to the first `mif2` call in the chain. These are inherited from the `mf1` local mif object. The computational parameters used for the global search are therefore never explicitly stated in the code and cannot be verified independently.

- **SEIR initial conditions: E=15, I=25 hardcoded**: In both SEIR implementations, the initial exposed and infectious counts are hardcoded to 15 and 25 (lines 765–770, 1047–1053). These are not estimated. For a model spanning 2017–2025, the initial conditions substantially affect the early-period likelihood. No sensitivity analysis of these fixed values is reported (POMP checklist §13).

- **Missing data imputation not documented for POMP**: The paper notes that 2022 data is missing and that an `interpolated_cases.csv` file exists in the data folder. The ARMA analysis uses this interpolated file, but the POMP models use `all_data.csv` directly and the SEIR `dmeas` Csnippet handles `ISNA(Cases)` by contributing zero log-likelihood. The interpolation method and its impact on the ARMA analysis are not described.

- **No convergence traces shown for SEIR global search**: Convergence traces for the SEIR local search are displayed, but the corresponding pairs plot for the global search is commented out (`#pairs(...)`). For a model with such poor convergence (only 5/500 replicates within 5 LL units of the best), the pairs plot is a critical diagnostic that should be reported rather than suppressed.

- **No model diagnostics**: Neither model reports conditional log-likelihoods per time point, effective sample size (ESS) traces from the particle filter, or filtering-distribution simulations conditioned on data (POMP checklist §4). These diagnostics would reveal which periods are poorly fitted and provide mechanistic insight into the model's failures.

- **SEIR parameter implausibility not discussed**: The SEIR MLE has `mu_IR = 64` per week (mean infectious period ≈ 2.7 hours) and `eta = 0.787` (78.7% of the 48 million person population initially susceptible). Both values are biologically implausible for pertussis, which has a known infectious period of 1–3 weeks and a population with substantial immunity from prior infection or vaccination. The paper does not discuss whether these estimates represent model misspecification (POMP checklist §11).

- **No profile likelihoods reported**: Neither the SIR nor the SEIR model reports profile likelihoods for any parameter. Given the evidence of non-identifiability (base_beta ≈ outbreak_beta at the SEIR MLE; implausible mu_IR at both MLEs), profile likelihoods are essential for characterizing which parameters are identified. Without them, the reported point estimates have unknown uncertainty (POMP checklist §5).

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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data.zip` (inspected via R: `data/global-SIR.rds`, `data/global-SEIR.rds`, `data/global-SEIR_1datapointrmv.rds`, `data/mifs_local_SIR.rds`, `data/mifs_localSEIR.rds`, `data/whoop_truncated_params_SIR.csv`)
