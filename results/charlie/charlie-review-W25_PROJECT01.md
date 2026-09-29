# Review: W25 Project 01
## *Unveiling the Dynamics of Influenza in the Great Lakes Region*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) via iterated filtering; replicated pfilter for likelihood evaluation |
| **R packages used** | pomp, doFuture, doParallel, forecast, tseries, tidyverse |
| **Code publicly available** | Yes — submitted via course repository; .R files (seirs_global.R, seirs_beta.R) included |
| **Data publicly available** | Yes — CDC ILINet, CDC FluVaxView, CDC vaccine effectiveness data |
| **Benchmark comparison included** | Yes — regression with SARMA(2,1)(0,2)_52 errors |

---

## POMP Checklist Scorecard

*✓ = satisfies practice, ~ = partially satisfies, ✗ = does not satisfy, N/A = not applicable*

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ✓ | IF2 + replicated pfilter used correctly |
| 2 | Benchmark comparison | ✓ | SARMA regression benchmark included and compared quantitatively |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported, but profile CI for rho covers a range inconsistent with the global MLE |
| 4 | Model diagnostics | ✗ | No conditional log-likelihood plots, no ESS monitoring |
| 5 | Parameter identifiability and uncertainty | ✗ | Alpha and gamma profiles are likelihood slices; rho profile does not cover MLE region |
| 6 | Computational adequacy | ~ | Multiple global searches run; convergence partially demonstrated |
| 7 | Forecast methodology | N/A | No forecasting attempted |
| 8 | Model variations and nested comparisons | ✓ | Multiple model versions compared with log-likelihood |
| 9 | Stochasticity | ✓ | Binomial transitions with negative binomial measurement model |
| 10 | Reproducibility and extendability | ~ | Code and data included; no renv/sessionInfo; HPC scripts absent |
| 11 | Corroboration with scientific knowledge | ~ | Parameters checked against literature; biologically implausible gamma and A acknowledged |
| 12 | Measurement model specification | ~ | Negative binomial used; H accumulator has a double-zeroing bug |
| 13 | Initial conditions | ~ | Initial conditions derived from mu_EI and mu_IR; R=0 simplification acknowledged |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

The paper fits a SEIRS POMP model to weekly influenza surveillance data from CDC Region 5 (Great Lakes) spanning 2015 to 2023, incorporating seasonal transmission forcing, antigenic drift modeled as Brownian motion, COVID-19 suppression via logistic ramp functions, and vaccine effects as time-varying covariates. The analysis is compared against a non-mechanistic regression with SARMA(2,1)(0,2)_52 errors, and multiple iterative model refinements are presented with thoughtful biological motivation.

**Strengths:** The project is ambitious, incorporating several biologically motivated mechanisms into a single SEIRS framework. The authors engage seriously with model diagnostics, acknowledging biologically implausible parameter estimates (gamma, A, mu_EI) rather than ignoring them. Benchmark comparison with a competitive SARMA model is included and performed at a comparable likelihood scale. The biological parameter justification section draws on CDC literature. Convergence evidence via trace plots is shown for multiple local and global searches.

**Weaknesses:** The profile likelihood analysis for rho evaluates a grid that excludes the global search MLE by more than an order of magnitude, rendering the reported confidence interval meaningless. The alpha and gamma "profiles" are likelihood slices rather than proper profile likelihoods, a course-confirmed error (CC-Yes, Error 1.2). The H accumulator in the Csnippet contains a double-zeroing bug that discards approximately 1/7 of each week's incidence. The paper's stated data span ("2015 to 2024") does not match the code's filter (`YEAR < 2024`). The estimated COVID suppression amplitude (A ≈ 9%) is biologically implausible given that influenza cases dropped to near zero during 2020–2022.

---

## Major Issues

### 1. Profile likelihood for rho evaluates a range incompatible with the global search MLE

The global search (bvgcseirs_global_search3.rds) produces a maximum likelihood estimate of rho ≈ 0.004 (reported in the parameter table in Section 5, "Reasonableness of Estimated Parameters"). However, the poor man's profile for rho (Section 5, "Profile Likelihood Evaluation — Poor Man's Profile over rho") evaluates rho on the grid `seq(0.02, 0.08, length.out=25)`, and the true profile (Section 5, "True Profile Likelihood Evaluation") evaluates `seq(0.02, 0.04, length.out=30)`. Neither grid includes values near rho = 0.004. The poor man's profile correctly shows the likelihood is maximized at the lower bound of the grid (rho ≈ 0.02), which signals the true maximum lies below the evaluated range — consistent with the global search MLE at rho = 0.004. Yet the true profile, by re-optimizing other parameters at each fixed rho, finds a maximum near rho ≈ 0.038, contradicting the global search. The two profiles give qualitatively opposite information about where the MLE lies, and the reported 95% CI for rho is computed entirely outside the MLE region. The authors then fix rho = 0.036 for the final global search, but this value has no valid profile likelihood support.

**Fix:** Re-center the profile grid around the global MLE (rho ≈ 0.004), with the grid spanning roughly one order of magnitude on each side (e.g., `seq(0.001, 0.02, length.out=30)`). The CI should be computed from this properly centered profile. The inconsistency between the global search MLE and the profile maximum needs to be resolved before any confidence interval is reported.

---

### 2. Alpha and gamma "poor man's profiles" are likelihood slices, not profile likelihoods (CC-Yes, Error 1.2)

The paper constructs "poor man's profiles" for alpha and gamma by holding all other parameters at their MLE values and varying only the target parameter. The authors explicitly state: "this approach does not re-optimize other parameters at each rho." This is a likelihood slice, not a profile likelihood. A profile likelihood requires maximizing the likelihood over all nuisance parameters at each fixed value of the target parameter. Slices are always narrower than profiles and produce artificially tight apparent confidence regions. The course explicitly tested the distinction between slice and profile (Q10-02, CC-Yes). The conclusions drawn from these plots — that "a moderate antigenic effect (0.25) best explains the data" and that gamma exhibits a "wide optimal range" — are artifacts of the slice approach and cannot support identifiability claims. The same issue applies to the rho poor man's profile, though for rho a true profile is subsequently computed.

**Fix:** Construct true profile likelihoods for alpha and gamma by running mif2 at each fixed value of the target parameter with all other parameters freely estimated. Given computational constraints, 10–15 profile points with 3–5 mif2 replicates each would be sufficient to characterize the profile shape. The existing poor man's profiles can be retained as exploratory tools but should not be used to draw identifiability conclusions.

---

### 3. H accumulator double-zeroing in rprocess discards first sub-step's incidence

The seirs_step Csnippet (Section 4, "Modeling with Seasonal Beta...") contains the following logic at the end of each step:

```c
H += dN_EI;   // accumulate incidence
// ...
if (fabs(fmod(t, 1.0)) < 1e-8) {
  H = 0;      // manual reset at integer t
}
```

Because the model also specifies `accumvars="H"` in the pomp call, H is zeroed by pomp's automatic accumvars mechanism at each observation time before rprocess runs. When rprocess then executes the first sub-step (from t = k to t = k + 1/7 with t = k an integer), H accumulates dN_EI and is then immediately reset to 0 by the manual check. This discards the first sub-step's contribution entirely. The following six sub-steps accumulate normally. As a result, H at each observation time captures approximately 6/7 of the true weekly incidence, causing a systematic ~14% undercount. This forces rho and other parameters to compensate, making parameter estimates unreliable. The manual `H = 0` in seirs_step is redundant with accumvars and should be removed; the automatic accumvars mechanism handles the reset correctly.

**Fix:** Remove the manual `if (fabs(fmod(t, 1.0)) < 1e-8) { H = 0; }` block from seirs_step. The `accumvars="H"` specification already handles the reset at each observation time without discarding the first sub-step's contribution. Rerun the global searches and profile likelihoods after this fix to obtain corrected parameter estimates.

---

### 4. Data span misrepresented in text: code filters YEAR < 2024, not through 2024

The Introduction states: "we restrict our analysis to the years 2015 through 2024" (Section 1), and this phrasing is repeated in the Conclusion: "we model influenza dynamics... from 2015 to 2024." However, the data filtering code at line 257 reads `data |> filter(YEAR < 2024) -> data`, and an identical filter is applied again at line 715. The filter `YEAR < 2024` excludes all 2024 data; the actual analysis spans 2015–2023 (approximately 9 years, not 10). The 2024 exclusion is partially justified by the vaccine covariate availability, but the Introduction still claims "our analysis... is concerned with the data from 2015 to 2024." This misrepresentation affects the stated scope of findings.

**Fix:** Change all text references from "2015 to 2024" to "2015 to 2023" (or equivalently "2015 through 2023") to match the code. Alternatively, if 2024 data should be included, change the filter to `YEAR <= 2024` and verify the vaccine covariate is properly padded for 2024.

---

### 5. Estimated COVID-19 suppression amplitude A ≈ 0.088 is biologically implausible given near-zero observed influenza

The EDA (Section 2) documents that "from 2020 to 2022, influenza cases dropped to near zero" — a reduction of over 95% from pre-pandemic levels. However, the final model estimates a maximum COVID suppression amplitude A = 0.0881, meaning the covid_effect term reduces the transmission rate by at most 8.8%. The paper explains this as a "nonlinear compounding effect" whereby a small reduction in beta, when sustained, drives the disease to near-extinction. While this logic is mathematically coherent (if R0 drops below 1), the explanation is not demonstrated quantitatively: no simulation or calculation shows that A = 0.088 actually reproduces the observed two-year near-zero period. The posterior predictive checks (Sections 5.6 and 5.7) show substantial overprediction of peak cases without disaggregating the COVID period specifically. A suppression of only 9% is inconsistent with the observed orders-of-magnitude reduction unless the baseline R0 is very close to 1, which itself raises model specification concerns. The paper identifies this tension but does not resolve it.

**Fix:** Add a simulation that specifically evaluates whether A = 0.088 reproduces the 2020–2022 near-zero period. If it does not, consider whether the COVID suppression onset/offset parameters (r1, r2, t_start, t_end) and amplitude A together need refitting, possibly as estimated rather than mostly fixed parameters.

---

### 6. R0 < 1 at baseline for the interpretable final model

The appendix section "Justification of Biological Plausibility" computes R0 = Beta0/mu_IR = 0.8425/0.8756 ≈ 0.962 for the fixed-rho model (the interpretable final model). R0 < 1 means the infection cannot sustain transmission under constant conditions. The paper notes that the peak R0 including seasonal forcing reaches ≈ 1.074, making persistence possible only during the winter peak. An influenza R0 below 1 at baseline, with persistence dependent entirely on seasonal amplification to breach 1, is inconsistent with the widespread consensus that seasonal influenza has R0 ∈ [1.19, 1.37] (Biggerstaff et al., cited as reference [14] in the paper). This may indicate that the frho model is misspecified or that fixing rho = 0.036 forces other parameters into biologically implausible regions. By contrast, the main estimated model (bvgcseirs_global_search3) implies R0 ≈ Beta0/mu_IR ≈ 1.5758/1.5210 ≈ 1.04, which is at least positive but still below the literature range.

**Fix:** Compute and report R0 for all major model variants, and explicitly compare to literature estimates. If R0 is consistently below the literature range, this is evidence of model misspecification (possibly too high a recovery rate or too low a transmission rate) and should motivate structural revision rather than parameter fixing.

---

### 7. No conditional log-likelihood plots or ESS monitoring (Wheeler et al. 2024, Checklist Item 4)

The paper does not present conditional log-likelihoods (per-observation log-likelihoods) across time, nor are effective sample sizes monitored during particle filtering. These diagnostics are particularly important given the structural breaks in the data (COVID suppression in 2020–2022, post-pandemic surge in 2022–2023). Conditional log-likelihoods would reveal whether the model fails specifically during the pandemic period or the post-pandemic surge, guiding structural improvements. Wheeler et al. (2024) demonstrate that such plots were essential for discovering Model 3's failure to explain the Hurricane Matthew surge, motivating the addition of hurricane parameters. Without these diagnostics, it is impossible to assess where the model succeeds and fails across the ten-year span.

**Fix:** Add a conditional log-likelihood plot (per-week loglik contributions) using `pfilter()` output. Add ESS monitoring to identify filter degeneracy. Focus attention on the 2020–2022 and 2022–2023 sub-periods.

---

## Computational and Diagnostic Assessment

**Convergence:** Multiple local and global searches are presented with trace plots showing log-likelihood trajectories across IF2 iterations. The loglik panel generally converges upward, and the authors correctly interpret spread in parameter traces as weak identifiability (not failure). However, the absolute convergence is difficult to assess: multiple model versions are explored iteratively rather than starting fresh global searches from diverse initial conditions within a fixed model specification. The "best" model by log-likelihood (loglik > -3600, mentioned in the Conclusion) is different from the interpretable model (loglik ≈ -3622), and the convergence evidence for the final interpretable model is less thorough.

**Particle filter:** Particle counts of Np = 2000 for the profile likelihood computation and Np = 5000 for likelihood evaluation are reasonable for run_level=2/3 work. However, ESS is never monitored, so it is not possible to assess whether particle degeneracy affects inference. The likelihood evaluation uses `replicate(20, logLik(pfilter(...))) |> logmeanexp(se=TRUE)`, which is the correct course-standard pattern.

**Conditional log-likelihoods:** Not reported. This is a meaningful gap given the structural complexity of the 10-year span.

**Profile likelihoods:** A true profile for rho is computed (30 profile points, 5 mif2 runs each), but the grid range [0.02, 0.04] is inconsistent with the global MLE at rho ≈ 0.004 (see Major Issue 1). Profiles for alpha and gamma are likelihood slices, not profiles (see Major Issue 2). No profiles are computed for mu_IR, mu_RS, Beta0, or Beta1, which are the most biologically interpretable parameters.

**Computational scale:** CPU usage and HPC job information are not reported. The paper states runs were performed on a cluster using SLURM (based on the `Sys.getenv("SLURM_CPUS_PER_TASK")` call), but no CPU-hours or cluster specifications are provided.

---

## Reproducibility Assessment

**Code availability:** Source code is included in the submission, including the two R scripts (seirs_global.R, seirs_beta.R) for cluster execution. Cached .rds files are provided for all major computation steps, enabling figures to be reproduced without re-running optimization.

**Final parameters:** Final MLE parameter vectors are stored in .rds files in the gl/ subdirectory. These are loaded throughout the Rmd for reproducibility.

**Model-code consistency:** The measurement model in code (`dnbinom_mu(reports, k, mean, give_log)`) matches the mathematical description. However, the H accumulator double-zeroing identified in Major Issue 3 constitutes a discrepancy between the intended behavior (weekly incidence accumulation) and the actual implementation.

**Package versions:** No `sessionInfo()` output or renv lockfile is provided. The `pomp` API has changed substantially across versions, and results may not reproduce on a different version without pinning. Additionally, the code includes an automatic package installation block that installs missing packages without user consent, which is a coding practice violation.

**Auxiliary data:** Vaccination coverage (Flu_vac_region_5_monthly.csv), vaccine effectiveness (vaccine-effectiveness.csv), and the ILI data (ILINet.csv, ilitotal2015.csv) are all included in the submission. Covariate construction code is embedded in the Rmd.

**HPC reproducibility:** SLURM job submission scripts are not included. Reproduction on a cluster requires manually configuring the parallel environment.

---

## Minor Issues

- The second code chunk at the top of the Rmd automatically installs missing packages (`install.packages(pkg)`) without user consent, which violates good coding practice (code supplement checklist: "No auto-installing packages without user consent"). This should be replaced with a comment instructing the reader to install required packages manually.

- The imported-cases restarter (`if (I < 10) { double imported = rpois(0.2); I += imported; H += imported; }`) adds imported cases to both I and H. Including imported cases in H means they enter the observation likelihood, inflating the likelihood during the COVID near-zero period. Since imported cases are an artificial modeling device (not true ILI reports), they should not be added to H. Consider adding only to I.

- Multiple fixed parameters (sigma_mut, r1, r2, k, mu_EI, phase) are fixed without profile likelihood or sensitivity analysis. While fixing parameters is sometimes necessary given computational constraints, the paper should at minimum report a sensitivity table showing how the maximum log-likelihood changes as each fixed parameter is varied over a plausible range.

- The paper presents two competing "best" models at the end: the highest-likelihood model (loglik > -3600, biologically implausible parameters) and the interpretable fixed-rho model (loglik ≈ -3622). The Conclusion discusses both but does not clearly state which is the primary result. A single primary model should be designated.

- Trace plots for local searches display well, but the global search pair plots use `loglik > max(loglik, na.rm=TRUE) - 2000` or `-500` as filter thresholds. These windows are extremely wide (2000 log-units covers a range that includes many qualitatively different parameter combinations) and may obscure structure near the MLE. A window of 10–20 log-units is standard for examining near-optimal parameter distributions.

- The spectral periodogram subtitle reads "Cycles per Year" and a vertical line is correctly placed at frequency = 1 (1 cycle per year). The dominant peak at frequency ≈ 1 is interpreted as "a dominant frequency of one cycle per year." However, the data has been set as `ts(..., frequency=52)`, so additional peaks at integer multiples (harmonics at 2, 3, ...) would also be present and deserve brief comment. The paper does not acknowledge higher-harmonic structure that may reflect within-season variation.

- The "Justification of Biological Plausibility" in the appendix uses parameters from the frho model (Beta0=0.8425, mu_IR=0.8756) without clearly labeling which model version these come from. Given that the main paper discusses a different parameter set (Beta0=1.5758, mu_IR=1.521), readers may confuse which model is being justified.

- Notation: the notation `mu_RS` and `mu_{RS}` are used interchangeably between inline math and code. This is a minor presentation inconsistency.

- At line 338, the paper states "we discard [ARMA(3,0)] as there is a mathematical inconsistency between ARMA(3,0) and ARMA(3,1)." The AIC inconsistency (AIC(3,1) > AIC(3,0)) is correctly identified as a potential numerical optimization failure (CC-Yes, Error 2.13 from the student weakness reference), but the diagnosis is framed as a "mathematical inconsistency" rather than an optimization artifact. The language should be revised to note that this may indicate the ARMA(3,1) optimization did not converge, not that ARMA(3,0) is inherently preferred.

---

## Recommendation

**Major Revision.** The project demonstrates genuine ambition and biological thoughtfulness. The benchmark comparison, multiple iterative model refinements, and acknowledgment of biologically implausible estimates are all commendable. However, three issues require correction before the analysis can support its conclusions: (1) the profile likelihood for rho is computed in the wrong region relative to the global MLE, making the reported CI invalid; (2) the alpha and gamma profiles are likelihood slices, not profiles, producing overstated identifiability claims; and (3) the H accumulator double-zeroing is a model implementation error that systematically biases all parameter estimates. After addressing these issues and rerunning the global searches and profiles, the authors should verify that the key comparative finding (POMP likelihood competitive with SARMA) holds. Adding conditional log-likelihood plots to assess fit during the pandemic sub-period would substantially strengthen the model diagnostics.

---

## Files Consulted

### Skill Files

- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

### Project Files

- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project01/blinded.Rmd`
