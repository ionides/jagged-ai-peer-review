# Peer Review: W22 Project 13
**Title:** An Analysis of Omicron Variant COVID Cases in California and Texas
**Reviewer:** Doug
**Date:** 2026-04-13

---

## Summary

This project fits a stochastic SEIR model to daily COVID-19 case counts in California and Texas during the Omicron wave (December 2021 to March 2022), using a piecewise-constant transmission rate beta tied to policy events. The authors employ iterated filtering (mif2) for parameter estimation and compute a profile likelihood for the reporting rate rho. While the project demonstrates familiarity with POMP methodology and tackles a relevant public-health problem, the analysis contains several critical flaws: the global search box is severely misaligned with the true MLE for both states (with IF2-drifted solutions falling 3 to 20 times outside stated parameter bounds), the profile likelihood presented in the Rmd is a pseudo-profile constructed from global-search scatter rather than a genuine constrained optimization, the accumulator variable H accumulates recoveries rather than new infections, and key reproducibility gaps exist because the global search code does not appear in the Rmd. No benchmark comparison against a non-mechanistic model is provided, and the measurement model includes an unexplained fixed scaling factor phi = 14.

---

## Major Issues

### 1. Severe Global Search Box Misalignment Invalidates All MLE Claims

The global search box for California is specified with lower bounds b1 = 3, b2 = 20, b3 = 0, b4 = 700, and for Texas with b1 = 10, b2 = 100. Inspection of the saved result files reveals that all top-ranked solutions have parameter values far below these lower bounds: California MLE has b4 = 221 (box lower = 700, a factor of 3 below); Texas MLE has b1 = 4.4 (box lower = 10) and b2 = 5.4 (box lower = 100, a factor of 18.5 below). These solutions were reached by IF2 drifting far outside the initial search box, not by systematic coverage of the specified space. The 800 global search replicates clustered tightly near a single local optimum for each state (top-10 b2 values for California span [23.4, 25.0], and for Texas span [5.33, 5.45]), indicating no genuine exploration of a broad parameter space. Because the starting box excluded the true MLE region entirely, the claimed global search is in practice a confirmation of the local search result obtained by IF2 drift.

Consequence: All reported parameter estimates, simulation trajectories, and profile-likelihood-derived confidence intervals from the global search are conditional on a constrained, incorrect MLE region. The conclusions about how COVID policies affected transmission cannot be trusted.

Fix: Redesign the global search box to bracket the MLE found by local search (e.g., extend b4 lower bound to at least 100 for California, and b2 lower bound to at least 2 for Texas), re-run the global search, and verify that the best log-likelihood from the global search exceeds or matches the local search best.

### 2. Profile Likelihood Is a Pseudo-Profile, Not a Genuine Constrained Optimization

The profile likelihood section for California reads from `writeup_params.csv` (the global search results), filters rows by log-likelihood range and standard error, groups by rounded rho, selects top rows per group, and applies a chi-squared CI cutoff. No `profile_design()` call, no dedicated foreach loop with rho fixed at a grid of values, and no `mif2()` call that excludes rho from `rw.sd` appear anywhere in the Rmd. This procedure constructs a scatter plot of global-search results, not a profile likelihood in the statistical sense. The chi-squared confidence interval derived from this plot (rho approximately 0.12 to 0.41 for California, and approximately 0.08 to 0.14 for Texas) has no valid statistical interpretation, because the optimization at each rho bin was not constrained to hold rho fixed. The same pseudo-profile pattern is applied to Texas.

Separately, a genuine profile search artifact (writeup_profile_rho.rds, 232 rows at distinct rho values) exists in the project folder but is never loaded or displayed in the Rmd. That genuine profile achieves a best log-likelihood of -1007.3, which is 15 log-likelihood units better than the global search best of -1022.3. This 15-unit discrepancy further confirms that the global search failed to find the true MLE. The genuine profile is unused in the analysis despite representing the better computational result.

Fix: Replace the pseudo-profile code with a genuine profile search: construct a grid of fixed rho values using `profile_design()`, run `mif2()` over all other parameters at each grid point with rho excluded from `rw.sd`, evaluate the log-likelihood at each result, and apply the chi-squared threshold referenced to the global maximum log-likelihood. The already-computed writeup_profile_rho.rds should be incorporated into the analysis.

### 3. Accumulator Variable H Accumulates Recoveries, Not New Infections

The process model accumulates `H += dN_IR`, where `dN_IR` is the number of individuals transitioning from I (infectious) to R (recovered). The observation data, obtained from the New York Times database, records daily new confirmed COVID cases, which correspond to new detections or new infections entering the infectious compartment. Linking new daily confirmed cases to daily recoveries introduces a systematic lag of approximately 1/mu_IR = 7 days and creates a semantic mismatch between the modeled quantity and the observed quantity. The reporting rate rho therefore absorbs not just the detection fraction but also the ratio of recovery events to new infection events, distorting its epidemiological interpretation. The measurement model mean is E[Cases] = 14 * rho * H, where phi = 14 further amplifies the mismatch without biological justification (see Issue 5). A correct formulation would accumulate `H += dN_EI` (new infections leaving the exposed compartment) or `H += dN_SE` (new exposures), which directly correspond to daily new confirmed cases.

Fix: Replace `H += dN_IR` with `H += dN_EI` in the process Csnippet, and verify that the measurement model scaling factor phi is revisited accordingly.

### 4. No Benchmark Comparison Against a Non-Mechanistic Model

The analysis does not compare the SEIR model against any non-mechanistic statistical baseline such as an ARIMA or autoregressive negative binomial model. Without such a comparison, it is impossible to assess whether the mechanistic model captures meaningful structure beyond what a simple statistical model achieves. The conclusion section acknowledges this gap ("We decided to compare pomp models and did not develop a likelihood baseline") but presents this as a minor omission rather than a fundamental gap. Wheeler et al. (2024) demonstrate that some mechanistic models fail to outperform a simple autoregressive negative binomial benchmark, and that per-unit comparisons can expose model failures not visible in aggregate log-likelihoods. For a paper comparing California and Texas, a benchmark comparison would directly quantify the added value of the mechanistic structure.

Fix: Fit an ARIMA or autoregressive negative binomial model to each state's case time series and report the log-likelihood alongside the POMP model log-likelihood, using a common observation model and data scale to make the comparison valid.

### 5. Fixed Scaling Factor phi = 14 Is Unmotivated and Not Estimated

The measurement model sets E[Cases] = 14 * rho * H, hardcoding phi = 14 as a fixed constant. The text acknowledges that phi was "additionally added as a fixed scaling parameter to allow the model to reach the heights of the spike (which proved difficult without it)" but provides no biological or statistical justification for the value 14. This value is not the mean duration in any compartment (1/mu_EI = 3 days, 1/mu_IR = 7 days, sum = 10 days), nor is it a conventional epidemiological scaling. Because H accumulates recoveries rather than infections (Issue 3) and the observation model needs to match reported cases, the phi = 14 likely compensates in an ad hoc way for the accumulator mismatch, but this compensation is not principled. By fixing phi = 14 without estimation or sensitivity analysis, the authors introduce an unacknowledged identification constraint that affects all other parameters. Fixing phi = 14 also means the effective reporting rate is not rho alone but 14 * rho, potentially confounding interpretation.

Fix: Either estimate phi as a free parameter, provide a principled derivation of phi = 14 from the model structure, or acknowledge that phi is a nuisance scaling parameter and assess sensitivity of results to its value.

### 6. Texas Particle Filter Degeneracy at Initial Parameter Values

The Texas local search is initialized at b1 = 20, b2 = 200, rho = 0.4, which lies within the stated global search box. However, the saved Texas local search likelihood evaluation (writeup_lik_local_texas.rds) shows that the best-performing local search replicate achieves a log-likelihood of -1076.5 with a standard error of 12.4. A standard error this large indicates that the particle filter is degenerating at these parameter values, and that the likelihood estimate itself is unreliable (a well-calibrated particle filter run should have SE < 1). The global search later finds a log-likelihood of -1026.7, some 50 units better, at parameter values (b1 = 4.4, b2 = 5.4) far outside the search box. The presentation of the Texas local search convergence traces and simulation in the paper treats these degenerate results as meaningful diagnostics, which they are not.

Fix: Check whether the initial parameter guesses for Texas place the system in a regime where the particle filter collapses (e.g., because beta is so large that the epidemic explodes and depletes the susceptible pool instantly). Lower the starting values for b1 and b2 to be consistent with the region where the global search ultimately found stable likelihood evaluation, and re-run both local and global searches from these corrected starting points.

### 7. Global Search Code Missing from Rmd (Reproducibility Gap)

The Rmd presents `runif_design()` calls that define the global search starting boxes for California and Texas, and then reads results directly from pre-computed CSV files (`writeup_params.csv`, `writeup_params_texas.csv`) without any intervening `bake()` or `foreach/mif2` block. The code that generated these CSVs is absent from the Rmd. Additionally, the run level is set to 1 in the Rmd preamble (NSTART = 50), but the CSVs contain 800 rows each, consistent with run_level = 3 (NSTART = 800). Similarly, the genuine profile artifact (writeup_profile_rho.rds) exists in the project folder but its generating code is not shown. A reader cannot reproduce the global search or profile results from the Rmd alone.

Fix: Include the complete global search and profile computation code in the Rmd, inside `bake()` wrappers with the correct run-level parameters. If the computation was run on a cluster, document this explicitly and include job submission scripts or equivalent.

### 8. mu_EI and mu_IR Fixed Without Sensitivity Analysis or Uncertainty Quantification

The incubation rate mu_EI = 1/3 per day and the recovery rate mu_IR = 1/7 per day are both fixed as constants, excluded from `fixed_params` in one code block but declared as `fixed_params` in another (the Rmd uses `fixed_params = params[c("N", "mu_EI", "mu_IR")]` but then passes all parameters including mu_EI and mu_IR to mif2 via the full params vector). These parameters are also excluded from `rw.sd`, effectively fixing them. The biological values cited (3-day incubation, 7-day infectious period) apply to the Omicron variant broadly, but there is substantial uncertainty in these estimates and they interact with the transmission parameters. No sensitivity analysis assesses how conclusions change if mu_EI or mu_IR take different values. Wheeler et al. (2024) flag implausible fixed parameters as a potential indicator of model misspecification.

Fix: Either estimate mu_EI and mu_IR with appropriate perturbation sizes and profile likelihoods, or conduct a formal sensitivity analysis over a range of biologically plausible values (e.g., mu_EI in [1/5, 1/2], mu_IR in [1/10, 1/5]) and report whether conclusions about the beta step-function parameters are robust.

---

## Minor Issues

- **Notation error in transition rate**: The text labels the S-to-E transition rate as mu_SI ("mu_SI = beta * I(t) denotes the rate at which individuals in S transition to E"). In standard SEIR notation this should be mu_SE. Code is correct; text is mislabeled.

- **rw.sd for tau is effectively zero**: Both the California and Texas local search use `tau = 0.0001` in `rw.sd`. On the log scale (which partrans applies to tau), this perturbation is so small that tau will not move meaningfully during optimization. tau is effectively fixed at its starting value (2000 for California, 1000 for Texas) without being declared as a fixed parameter. The authors acknowledge uncertainty about tau ("it is unclear where to move for tau") but the near-zero rw.sd prevents IF2 from exploring it.

- **Texas rw.sd includes spurious parameters b3 and b4**: The Texas `params_rw.sd` definition (line ~375) is copied verbatim from the California setup and includes b3 = 0.01 and b4 = 0.01 perturbations. The Texas model has only two beta parameters (b1, b2) and no b3 or b4 in its paramnames. These spurious entries are silently ignored by mif2 but indicate a copy-paste error that was not caught.

- **H initial value unjustified**: The initial value of H is set to 613,559 for California and 696,761 for Texas. These values are described as "recovered individuals in the past 90 days that are unlikely to be infected" but no calculation or reference is provided to verify these figures. Since H is an accumulator variable that is reset at each observation time, its initial value affects only the first measurement model evaluation; this is a minor concern but should be documented.

- **Direct cross-state log-likelihood comparisons are invalid**: The conclusion notes that rho differs between California (approx 0.25) and Texas (approx 0.10) and calls this "an interesting result, as there is no reason for the estimates of the reporting rate to be significantly different between two similarly sized states." However, this comparison implicitly treats the two model fits as comparable despite the models having different numbers of beta parameters (four for California, two for Texas), different measurement model structures, and different computational trajectories. The CI comparison is therefore not statistically appropriate.

- **No model diagnostics**: The analysis does not present effective sample size (ESS) monitoring, conditional log-likelihoods per observation period, or residual diagnostics. These tools are necessary to identify periods where the model fails to fit the data (e.g., the rapid rise and fall of the Omicron wave within 89 days). Wheeler et al. (2024) describe how per-observation conditional log-likelihoods can expose specific intervals of poor fit.

- **Visual-only fit assessment at initial parameters**: The simulation plots shown before local search ("The simulations based can capture general trend of the data but are slightly lagged behind the initial outbreak") constitute only informal model checking. No quantitative measure of fit at the initial parameters or after local search is reported beyond the log-likelihood point estimate.

- **Software version not documented**: No `sessionInfo()` output or package versions are provided. The pomp API has changed across versions, and the code may not reproduce on current CRAN releases without version information.

---

## Files Consulted

### Skill files
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-boundary-mle/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-multi-series-length-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`

### Project files
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_params_texas.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_lik_local.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_lik_local_texas.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_lik_starting_values.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_lik_starting_values_texas.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_profile_rho.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/Cali_formatted.Rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/Texas_formatted.Rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/Makefile`
