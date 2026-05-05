# Peer Review: W25 Project 01
## "Unveiling the Dynamics of Influenza in the Great Lakes Region"

---

## Summary

This project analyzes CDC ILINet influenza data from HHS Region 5 (Great Lakes) for the years 2015–2024, fitting both a non-mechanistic regression-with-SARMA-errors baseline and a sequence of increasingly complex SEIRS POMP models. The authors show genuine scientific ambition, incorporating seasonal transmission forcing, COVID-19 suppression, vaccine covariates, and a Brownian-motion antigenic drift process into a single mechanistic framework. They honestly report identifiability problems, discuss implausible parameter estimates candidly, and produce some useful profile likelihood diagnostics. Key weaknesses include an invalid direct comparison of ARIMA and POMP log-likelihoods (different observation models and data), manual intra-rprocess resetting of the accumulator variable H that conflicts with the declared `accumvars` mechanism, systematic over-parameterization that leads to biologically implausible estimates, and insufficient documentation of computational effort. Several fixed COVID suppression parameters are hard-coded without proper justification, and the profile likelihood for rho covers a range that excludes the MLE from the global search.

---

## Major Issues

### 1. Invalid direct log-likelihood comparison between SARIMA and POMP models

The paper states: "The maximal log-likelihood is -3622.881, which is similar to that of our regression based SARMA benchmark [−3620.72]. A comforting sign of matching our regression based SARMA benchmark is sufficient for our purpose." This comparison is statistically invalid. The SARIMA model is fitted under a Gaussian observation model on the raw integer count series, while the POMP model is fitted under a negative binomial observation model. These two likelihoods are evaluated on different probability models for the same data, so their numerical values cannot be compared directly to draw conclusions about relative model quality. The POMP model matching the ARIMA log-likelihood is entirely uninformative as a diagnostic because, by sheer coincidence of scale, any negative binomial model evaluated on count data of similar magnitude could produce similar numerical likelihoods. See the SARIMA Baseline Audit skill and Wheeler et al. (2024) §Benchmark comparison. To fix this, the authors should either (a) evaluate both models under a common scoring rule (e.g., out-of-sample predictive likelihood or CRPS on the original observation scale), or (b) construct a non-mechanistic negative-binomial auto-regressive benchmark that can be compared numerically to the POMP model.

### 2. Accumulator variable H is manually reset inside the rprocess Csnippet, conflicting with the declared accumvars mechanism

The complete SEIRS model's Csnippet contains:
```
if (fabs(fmod(t, 1.0)) < 1e-8) {
  H = 0;
}
```
This resets H every integer time step (i.e., every week, since `delta.t = 1/7`). The model also declares `accumvars = "H"`, which instructs pomp to reset H to zero after each observation time by its own internal mechanism. These two reset mechanisms act simultaneously. The internal accumvars reset happens after the likelihood evaluation at each integer time point; the Csnippet reset happens at the start of the Euler step when `fmod(t, 1.0)` is near zero. When `delta.t = 1/7`, the condition `fabs(fmod(t, 1.0)) < 1e-8` is only triggered at exact integers, which coincides with the measurement times. The combined effect is that H is being zeroed by the Csnippet at the beginning of the week rather than at the end (after measurement), potentially causing one full week's accumulation to be lost at each observation. This creates a systematic off-by-one measurement error that biases the reporting rate estimate. The fix is to remove the manual reset from the Csnippet and rely solely on the `accumvars` mechanism, which is the correct pomp approach.

### 3. The "poor man's profile" over alpha and gamma is a global-search scatter, not a true profile likelihood

The profiles for alpha and gamma (sections "The gamma Issue" and accompanying figures) are constructed by reading saved global-search RDS files (`poor_profile_alpha.rds`, `poor_profile_gamma.rds`) and plotting loglik vs. the parameter of interest. The code does not show a `profile_design()` call, a separate foreach loop with the target parameter held fixed, or a modified `rw.sd` that sets the profiled parameter to zero. These are global-search scatter plots filtered by log-likelihood range. Applying a chi-squared cutoff (as referenced in the rho profile section) to such plots and interpreting the result as a confidence interval is not statistically valid; the profile likelihood theorem requires that all other parameters are re-optimized at each fixed value of the target parameter. See pomp-pseudo-profile-audit skill. The fix is to run genuine profile likelihood searches using `profile_design(alpha, ...)` and `profile_design(gamma, ...)` with those parameters excluded from `rw.sd`.

### 4. Profile likelihood for rho covers a range that excludes the global MLE estimate

The true profile for rho covers `seq(0.02, 0.04, length.out = 30)`. The MLE from the global search (bvgcseirs_global_search3) is reported as `rho = 0.0042`, which lies far outside this profile range. The profile therefore does not include the region of the parameter space where the global optimum was found. The resulting CI based on `max(prof_rho$loglik) - 1.92` is consequently not a 95% CI for the global MLE but rather a CI constrained to the range [0.02, 0.04]. The authors note "a well-defined maximum around rho ≈ 0.0386" but this is an artifact of the profile range, not evidence that the global maximum is in this region. To fix this, the profile range should be extended to include the global MLE (i.e., starting from rho ≈ 0.001 or lower) and the maximum of the profile should be verified to agree with the global search maximum.

### 5. Implausible COVID suppression amplitude A and hard-coded suppression parameters

The COVID suppression curve uses amplitude A estimated at 0.088 (about 9%), but the data show influenza cases dropping to near zero during 2020–2021. A 9% reduction in transmission is orders of magnitude too small to explain this behavior. The authors acknowledge this only partially, attributing it to the "nonlinear compounding effect." More fundamentally, the onset and offset times (t_start = 271, t_end = 333), steepness parameters (r1 = 0.15, r2 = 0.25), and amplitude A are treated as a mix of fixed and estimated quantities with inadequate justification. r1 and r2 are fixed throughout without sensitivity analysis. The suppression end time (t_end = 333) is stated in the text as "week of 05-17-2021" but in the external seirs_beta.R script it is described as "2023-05-08," a two-year discrepancy that is unresolved in the main document. Fixing these parameters without a formal sensitivity analysis means the model's handling of COVID is ad hoc, which undermines the core scientific claim of the paper (capturing pandemic dynamics). See Wheeler et al. (2024) §Parameter identifiability and uncertainty.

### 6. No proper conditional log-likelihood or ESS diagnostics for the final model

The paper does not present per-observation (conditional) log-likelihood plots for the final BVGC-SEIRS model, nor effective sample size (ESS) traces from any pfilter run on the final model. These diagnostics are essential for identifying where the model fits poorly (e.g., whether the 2020–2021 pandemic trough is handled correctly) and for verifying that the particle filter does not suffer from severe particle degeneracy across 450+ weekly observations. Without these plots, the claim that the model "captures the transitions between pre-, during-pandemic, and post-pandemic flu activity" cannot be assessed. See Wheeler et al. (2024) §Model diagnostics (checklist item 4). ESS plots from the initial basic SEIRS model are mentioned in the appendix (seirs_global.R contains ESS check code), but these are for the simpler model at fixed parameters and are not the final model.

### 7. Over-parameterization of the complex model leads to unidentifiable and biologically implausible estimates

The final BVGC-SEIRS model has 16 parameters (many estimated), yet the data are 450 weekly observations of a single observable. The authors report gamma = 6.95, which implies immunity waning in approximately 10–19 days for typical antigenic distances, which they themselves identify as "biologically unrealistic." The authors also report rho = 0.0042 (0.42%) but the profile maximum is at rho ≈ 0.04, a tenfold discrepancy that is never resolved. The gamma-alpha-Beta tradeoff results in strong identifiability entanglement that the authors acknowledge but do not address structurally. This level of over-parameterization, combined with the stochastic Brownian motion drift process (which adds free randomness that can absorb residual variation), suggests the model is memorizing noise rather than capturing biological signal. See Wheeler et al. (2024) §Parameter identifiability and uncertainty (checklist item 5). At minimum, nested likelihood ratio tests should be conducted to verify that each additional component (antigenic drift, vaccine effect) provides statistically significant improvement over the simpler SEIRS baseline.

---

## Minor Issues

- **Typo in data loading for SARMA model (line 377):** The arima call for `reg_sarma201_002` uses `data$ILITOTA` (missing trailing L) when computing inline. Although the result is loaded from a cached RDS file, this typo means the inline fallback code would fail silently, producing an error only if the RDS file is missing.

- **H accumulator semantics conflict with rprocess design in the basic SEIRS model:** In the basic SEIRS model (Section 4), H accumulates `dN_EI` (E→I transitions, i.e., new cases becoming infectious) while the comment states "H tracks incident symptomatic cases, consistent with ILI report definitions." ILINet records patients presenting with influenza-like illness symptoms, which aligns better with new symptom onsets. The choice of dN_EI over dN_IR is reasonable biologically (symptoms begin when the person enters the infectious compartment) but should be justified more explicitly. In the basic SEIRS model's Euler step (line 459), H is not reset by a Csnippet; the `accumvars` mechanism handles this, which is correct.

- **Data double-filtering for the complex SEIRS model:** The data filtering line `data |> filter(YEAR < 2024) -> data` appears twice: once at line 257 (basic EDA section, which filters to 2015–2023 for the initial analysis) and again at line 715 (beginning of the complex SEIRS section). Although the repeated call is harmless in the first execution, it represents sloppy data management; if the document is re-rendered with a modified YEAR filter in the first block, the second block will not reflect the intended range and the discrepancy will be silent.

- **Vaccine effectiveness interpolation is annual, not seasonal:** The vaccine effectiveness data is assigned as a flat annual value over `floor(n_weeks / nrow(ve_annual))` weeks per season. Vaccine effectiveness typically peaks early in the season and wanes; the constant-within-season assumption is an acknowledged simplification but is not assessed for sensitivity.

- **The poor man's profile rho grid range (0.02–0.08) differs from the true profile range (0.02–0.04):** These two profiles are compared in the narrative but the different ranges make the comparison inconsistent.

- **No sessionInfo() or package versions documented:** The code installs packages at render time and uses `SLURM_CPUS_PER_TASK` for parallelism but no `sessionInfo()` output or package version pinning (e.g., via `renv`) is provided. The pomp API has changed substantially across versions, so the analysis may not reproduce on current CRAN releases.

- **Total computational cost not reported:** The paper mentions running on a cluster and provides `seirs_beta.R` and `seirs_global.R`, but does not report the total CPU-hours used, the number of workers, or the walltime for each search. This makes it impossible to assess whether the computational effort was adequate. See Wheeler et al. (2024) §Computational adequacy.

- **The rho_grid in the true profile covers only [0.02, 0.04] with 30 points and 5 IF2 runs per point:** This amounts to 150 IF2 chain starts (each running 200 total mif2 iterations), which is relatively modest for a 16-parameter model over 450 observations. The resulting profile is described as "considerably noisier," which is consistent with insufficient computation per profile point.

- **Use of ChatGPT for scientific table and plot generation (reference 19):** The paper uses ChatGPT to "prepare" a parameter reasonableness table and a seasonal beta plot. Using a generative AI tool for scientific summarization without independent verification of the generated content is a scholarly integrity concern; the reviewer cannot verify whether the values and interpretations in the AI-generated table are accurate.

- **Section title "Regression Model with SARMA Errors" heading states the model uses SARMA errors but the initial identification uses pure ARMA:** The naming throughout is consistent but the notation `SARMA(2,1)(0,2)_52` for a model without seasonal differencing (D=0) is slightly non-standard; the conventional ARIMA notation would write this as SARIMA(2,0,1)(0,0,2)[52] with a regression component. This may cause confusion for readers unfamiliar with the local convention.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
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
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project01/seirs_global.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project01/seirs_beta.R`
