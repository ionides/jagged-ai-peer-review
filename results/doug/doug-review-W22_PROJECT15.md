# Peer Review: W22 Project 15
**Title:** Rise and Fall of Delta and Omicron variants: Comparison of Compartmental Models for SARS-CoV-2 variants

---

## Summary

The paper fits parallel SEIR models to weekly sequenced COVID-19 case counts for the Delta and Omicron variants in the United States, using iterated filtering (IF2) via the pomp package. The primary scientific goal is to compare estimated transmission parameters between the two variants. While the project employs a defensible model structure and legitimate likelihood-based inference, the analysis is undermined by a cascade of computational failures: the global search for Delta is severely non-convergent (only 1% of replicates reach near-optimal likelihood), the global search box for Omicron entirely excludes the region containing the MLE, the global IF2 initialization antipattern anchors all searches to the local-search chain, and the Beta profile likelihood for Delta collapses to a single grid point above the CI cutoff. The reported parameter comparisons and confidence intervals are therefore unreliable. No non-mechanistic benchmark comparison is provided, and the reporting rate is fixed without justification from sequencing data, further limiting inferential validity.

---

## Major Issues

### 1. Global IF2 Search Initialized from Previous mif2 Result (Antipattern)

Both the Delta and Omicron global searches contain the antipattern identified in `pomp-global-search-init-audit`: the global search uses `mf1 <- mifs_local[[1]]` and then calls `mif2(mf1, params=c(unlist(guess), fixed_params), ...)`. Because `mf1` is a previous IF2 result object rather than the base pomp object, each global replicate inherits the cooling schedule of the local chain. By the time the global search begins, the cooling is at or near its terminal state, meaning the random-walk perturbations in the new starting locations shrink to near zero almost immediately. The 100-replicate "global" search is effectively 100 restarts from the local-chain neighborhood with minimal exploration capacity. This invalidates the claim that the global maximum has been found.

**Fix:** Replace `mif2(mf1, params=c(unlist(guess), fixed_params), ...)` with `mif2(covid19SEIR, params=c(unlist(guess), fixed_params), ...)` in both the Delta and Omicron global search loops, where `covid19SEIR` is the base pomp object.

---

### 2. Global Search Box Excludes the MLE Region for Both Variants

**Delta:** The global search box specifies `Beta=seq(1,100)`, but the artifact `global_search.rds` shows the MLE is at `Beta=73.4` (within bounds) and `mu_IR=5.46` (outside the stated box of [0.1, 3.0]). The `eta` MLE of 0.0823 also exceeds the box upper bound of 0.08. The `mu_IR` MLE drifted outside the box by a factor of ~1.8 only because IF2 perturbations carried it there accidentally, not systematically.

**Omicron:** The global search uses the same `Beta` box [1, 100], but the Omicron MLE is `Beta=389`, nearly four times the box upper bound. The reported "global maximum" for Omicron was only reached because IF2 drifted outside the initialization box. Only 14% of Omicron global replicates and 1% of Delta global replicates fell within 5 log-likelihood units of the best solution, confirming extremely poor coverage of the parameter space.

**Fix:** Center the global box on the local-search solution and use a generous multiplier (e.g., `[local_MLE * 0.25, local_MLE * 4]` for each parameter). For Omicron, the Beta box must extend to at least 500.

---

### 3. Delta Beta Profile Likelihood Collapses to a Singleton CI

Inspection of `beta_profile.rds` reveals that of the 50 Beta grid points, only **one** point (Beta = 131) has a log-likelihood above the chi-squared CI cutoff (-753.07). This means the reported "95% confidence interval roughly between 100 and 150" is not a valid confidence interval but a single noisy observation. The next-best profile point is 5 log-likelihood units lower, a drop far exceeding Monte Carlo noise given the loglik.se values. The profile is severely non-smooth, indicating either that the optimization at most grid points failed to converge, or that the profile is driven by an ill-identified compensation between Beta and mu_IR (which reaches an implausible value of 69.6 at the profile peak).

The authors acknowledge the discrepancy between the profile peak (Beta ~131) and the global MLE (Beta ~73) and attribute it to parameter correlation, but do not note the singleton nature of the CI. The stated conclusion "we roughly expect the maximum likelihood to be somewhere between 100 and 150" has no valid statistical basis.

**Fix:** Re-run the profile using `profile_design(Beta=seq(lower, upper, length=50), ...)` with starting parameters drawn from a broad box seeded from the global search MLE, multiple restarts per grid point (nprof=15 is appropriate but must use the base pomp object), and log-likelihood evaluated via `logmeanexp` with Np >= 2000.

---

### 4. Global Search Box Excludes Delta MLE for mu_IR; Implausible mu_IR at Profile Peak

The Delta global search box specifies `mu_IR` in [0.1, 3.0] per week. The MLE `mu_IR = 5.46` already lies outside this range. At the Beta profile peak, `mu_IR = 69.6`, corresponding to an infectious period of roughly 0.1 days. This is biologically implausible for Delta COVID-19, where the infectious period is typically 5–10 days (mu_IR ≈ 0.07–0.14 per day, or 0.5–1.0 per week). The optimizer is compensating for a poorly identified beta surface by trading off Beta against an extreme mu_IR, which should be flagged as a sign of model misspecification or parameter non-identifiability, not dismissed as correlation. Per Wheeler et al. (2024), implausible parameter estimates should be interpreted as evidence of model misspecification rather than biological findings.

**Fix:** Impose scientifically informed upper bounds on mu_IR in both the global search box and the profile guess box. Profile mu_IR separately to assess whether it is identifiable.

---

### 5. No Non-Mechanistic Benchmark Comparison

The paper does not compare either SEIR model against any non-mechanistic benchmark (e.g., an ARMA model or autoregressive negative binomial). This is the single most diagnostic check for whether the mechanistic structure captures meaningful signal. Wheeler et al. (2024) note that none of the 32 papers they reviewed performed such a comparison, and that some mechanistic models fail to beat a simple autoregressive benchmark. Without this comparison, it is impossible to assess whether the SEIR structure is earning its parametric complexity relative to a simpler alternative.

**Fix:** Fit an ARMA(p,q) or autoregressive negative binomial model to each variant's time series and compare log-likelihoods or AIC. Note: direct log-likelihood comparison requires both models to be evaluated under the same observation model and data transformation.

---

### 6. Reporting Rate Fixed Without Justification

The reporting rate `rho = 0.1` is fixed throughout the analysis, justified by the claim that "roughly 10% of all cases are sequenced." However, GISAID sequencing coverage varied substantially across the Delta and Omicron waves in the United States. The CDC's sequencing effort increased sharply during the Omicron wave, so a fixed rho = 0.1 may misrepresent the observation process for both variants and especially for Omicron. The text notes rho is fixed but provides no citation for the 10% figure and no sensitivity analysis. Per POMP checklist §12, the reporting rate should be estimated or the choice should be justified with a data-grounded citation and sensitivity assessment.

**Fix:** Estimate rho as a free parameter for each variant (using logit transform, as already set up in partrans), or provide a data citation and sensitivity analysis under alternative rho assumptions.

---

### 7. Model Diagnostics Are Absent

The paper presents only simulation envelopes against data. There are no conditional log-likelihood plots, no effective sample size (ESS) monitoring from the particle filter, and no filtering-distribution comparison. For the Delta variant, the simulation envelopes show substantial misfit (the observed data exhibits a multi-month plateau after the summer 2021 peak that the SEIR model cannot reproduce as a sharp-peak process). Per Wheeler et al. (2024) §4, these diagnostic tools are essential for identifying where and why a model fails. Specifically, conditional log-likelihoods would identify the periods of poor fit in the Delta trajectory.

**Fix:** Add plots of per-observation conditional log-likelihoods and ESS across time for each fitted model. Compare filtering-distribution simulations to forward-from-initial simulations to distinguish model misfit from parameter uncertainty.

---

### 8. Parameter Identifiability Not Assessed for mu_EI, mu_IR, and eta

Profile likelihoods are computed only for Beta. No profiles are shown for mu_EI, mu_IR, or eta. The paper acknowledges this limitation in the conclusion ("we could not find time to run profile likelihood for those") but still presents point-estimate comparisons of these parameters between variants and interprets them biologically (e.g., "the value of mu_IR of the Omicron variant is much less than that of the Delta variant"). The local-search convergence traces for eta show poor convergence for Omicron, and the global search box violation for mu_IR in Delta (MLE outside the box) suggests these parameters may be confounded. Per Wheeler et al. (2024) §5, parameter identifiability must be assessed before biological interpretation.

**Fix:** Compute profile likelihoods for mu_EI, mu_IR, and eta for both variants. Defer biological comparisons of non-profiled parameters to supplementary discussion.

---

## Minor Issues

- **Global search size (Omicron vs. Delta mismatch):** The local search for Delta evaluates at `Np=20000` (in `lik_local.rds`) but the global search uses `Np=2000` (run_level=3). For Omicron, the same discrepancy exists. Reported best likelihoods from global search evaluated at Np=2000 may differ from local search evaluations at Np=20000 by a systematic Monte Carlo bias; this makes direct local-vs-global log-likelihood comparison potentially misleading.

- **"k fixed at 10" is a strong assumption not discussed:** The negative binomial overdispersion parameter `k=10` is fixed without justification. For COVID-19 surveillance data, k is often estimated to be much smaller (high overdispersion), and fixing it at 10 may misrepresent the measurement noise and thereby distort all other parameter estimates. At minimum, sensitivity to this choice should be assessed.

- **The text incorrectly describes Delta as "the most deadly variant":** The citation provided ([@delta_death]) claims Delta is deadliest, but by the time of writing (April 2022) this characterization was contested; Omicron caused more total deaths globally due to sheer case volume. The paper is modeling sequenced cases (incidence), not deaths, so this framing is scientifically misleading regardless.

- **Mixing of observed data time indices across variants:** Delta is analyzed on the original week axis; Omicron is re-indexed by subtracting 40 from week numbers (`mutate(week = week-40)`). This reindexing is not explained or justified. While it may be operationally convenient, it means parameters estimated on the two time scales are not directly comparable without re-scaling discussion.

- **`filter(value>-2000)` in local search plot:** The Delta local search convergence trace uses `filter(value>-2000)` to remove poor chains. This filtering removes information about how many chains started poorly and is a form of selective reporting of convergence. All chains should be shown, or the filtering threshold should be justified and reported in the text.

- **Simulation plot uses `guides(color=FALSE)` without distinguishing simulated from observed:** In the simulation figures for both variants, the code adds `color='red'` for simulations and `c='black'` for observed data (note: `c` is not a valid ggplot2 aesthetic; the correct argument is `color`). It is unclear from the rendered plot which band is observed data vs. simulations.

- **No table comparing parameter estimates across variants:** The conclusion compares parameters verbally but provides no side-by-side table of MLEs with any measure of uncertainty. Such a table would make the claimed differences clearer and more verifiable.

- **The comparison of log-likelihoods across variants is not meaningful:** The paper implicitly uses log-likelihood improvement from local to global search as a measure of model quality but does not note that Delta and Omicron likelihoods are on entirely different scales (different data lengths, different data magnitudes) and cannot be directly compared.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/global_searcho.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/lik_local.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/lik_localo.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/lik_localE.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/beta_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/beta_profileo.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/covid19_params.csv`
