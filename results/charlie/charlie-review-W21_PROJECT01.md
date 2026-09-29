# Peer Review: W21 Project 01

**Title:** Investigating the effects of vaccinations and government policy on the spread of COVID-19 in the State of Pennsylvania

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2), particle filter (pfilter) |
| **R packages used** | pomp, foreach, doParallel, doRNG, tidyverse |
| **Code publicly available** | Partial — inline Rmd; stew-cached RDA files referenced but not archived |
| **Data publicly available** | Yes — loaded from live URLs (covidtracking.com, github.com/owid) |
| **Benchmark comparison included** | No — ARMA fitted but not quantitatively compared to SEIR |

---

## POMP Checklist Scorecard

*✓ = satisfies practice, ~ = partially satisfies, ✗ = does not satisfy, N/A = not applicable*

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2 + logmeanexp used correctly; convergence entirely absent |
| 2 | Benchmark comparison | ✗ | ARMA fitted but log-likelihood never compared to SEIR |
| 3 | Quantitative goodness-of-fit reporting | ✗ | No absolute log-likelihood value ever stated |
| 4 | Model diagnostics | ✗ | No trace plots, no ESS, no conditional log-likelihoods |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods, no CIs |
| 6 | Computational adequacy | ~ | Np=5000, Nmif=500 run on HPC; convergence not demonstrated |
| 7 | Forecast methodology | ✗ | Promised in introduction; never delivered |
| 8 | Model variations and nested comparisons | ~ | Three models explored; no quantitative model comparison |
| 9 | Stochasticity | ~ | Binomial transitions present; no overdispersion in measurement model |
| 10 | Reproducibility and extendability | ~ | Inline code present; live URLs and no archived parameters |
| 11 | Corroboration with scientific knowledge | ~ | Brief parameter discussion; implausible initial rho |
| 12 | Measurement model specification | ✗ | H = I (stock) used to model positiveIncrease (flow) |
| 13 | Initial conditions | ~ | Estimated from data averages; sensitivity not assessed |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

The project fits a SEIR compartment model to daily new COVID-19 cases in Pennsylvania (June 2020 – March 2021) using iterated filtering via the pomp package. The model is extended progressively to incorporate government-policy covariates (step-changes in Beta) and vaccination (a flow from S directly to R). While the project engages with POMP methodology at appropriate computational scale (Np=5000, Nmif=500, HPC cluster) and asks a scientifically interesting question, the analysis is severely undercut by the absence of any convergence diagnostics, the failure to report a single absolute log-likelihood value, a fundamental mismatch between the measurement model and the data type, and an internal contradiction in the second iterated filtering exercise.

**Strengths:**
- Scientifically motivated model extensions (policy and vaccination covariates) with reasonable biological justification
- Substantial computational effort (8 hours on a 36-core cluster)
- Correct use of logmeanexp for pfilter aggregation

**Weaknesses:**
- No iterated filtering trace plots; convergence is undemonstrated
- Measurement model (H = I, stock) incompatible with data (positiveIncrease, flow)
- Log-likelihood filter of ±50,000 units reveals catastrophic optimization failure
- No absolute goodness-of-fit value reported anywhere
- No profile likelihood; no confidence intervals
- Second iterated filtering contradicts its stated purpose

---

## Major Issues

### 1. Missing convergence diagnostics for iterated filtering (CC-Yes, Error 1.8)

The project runs mif2 with Np=5000 and Nmif=500 for 500 replicates but presents zero trace plots. There is no evidence — not a single panel — showing the log-likelihood rising across IF2 iterations, nor any parameter convergence traces. The pairs plots in the global search output are post-hoc summaries of terminal values, not convergence diagnostics. Without trace plots showing the log-likelihood panel converging upward across replicate runs from diverse starting values, there is no basis for claiming the optimizer found anything near the global maximum. This error was explicitly tested in W25 Q10-01 and Q10-03.

**Fix:** Add trace plots for both the log-likelihood and all free parameters across mif2 iterations, using `plot(m2)` or equivalent. The log-likelihood panel must show consistently upward trajectories across runs.

---

### 2. Measurement model mismatch: H = I (stock) applied to flow data

The accumulator H is defined as `H = I` in the Csnippet, and the paper explicitly states "we introduce an accumulator variable H in our model, which is equal to the current number of infected people. This is in contrast to the number of new infected people." The measurement model then draws `reports ~ Binomial(H, rho)`.

However, the observed data is `positiveIncrease`, which counts **new** daily positive tests. Under the model, `reports` is a sample from the current infected pool I — meaning the same infected individual contributes to the count on every day they remain infected. This is not how reported case counts work: a single person who is infected for 7 days appears once in positiveIncrease, but contributes to H for all 7 days. The model therefore generates counts proportional to disease prevalence rather than incidence, producing a systematic mismatch with incidence data.

The standard formulation for daily new infections is `H += dN_EI` inside the Csnippet, with `accumvars="H"` resetting H to zero each day. The authors' use of `accumvars="H"` combined with `H = I` does not accumulate transitions; it simply makes H a one-step copy of I.

**Fix:** Replace `H = I` with `H += dN_EI` so that H accumulates new E→I transitions during each daily interval, matching the incidence interpretation of positiveIncrease.

---

### 3. Log-likelihood filter range of 50,000 units indicates optimization failure

After the global search, results are filtered with `filter(logLik > max(logLik) - 5e4)`. The threshold 5e4 = 50,000 log-likelihood units. For reference, the Wilks 95% confidence threshold for 5 parameters is approximately 5.5 units, and any reasonable global search would retain results within 10–20 units of the maximum to focus on near-optimal estimates. A threshold of 50,000 units is so permissive that it retains essentially all results regardless of quality.

This filter, along with the authors' own observation that "the log-likelihood has large variations even for the same value of the parameters," is strong evidence that the optimizer completely failed to converge. The second analysis uses an equally permissive threshold of 1e4 = 10,000 units. The wide spread in the pairs plots corroborates this interpretation.

**Fix:** Diagnose why optimization failed (trace plots will help) before presenting results. If the model is fundamentally misspecified, revise model structure rather than widening the filter.

---

### 4. No absolute log-likelihood value reported

The project never states the best achieved log-likelihood from either global search. Only relative differences within the pairs plots are shown — and those are filtered through a 50,000-unit window. Without knowing the absolute log-likelihood, it is impossible to assess model adequacy, compare the SEIR model to the ARMA baseline, or determine whether the computational effort was sufficient to approach the MLE.

**Fix:** Report the best log-likelihood value (and its Monte Carlo standard error) from each global search. This single number is the primary output of likelihood-based inference.

---

### 5. No profile likelihood for any parameter

No profile likelihoods are computed. As a result, parameter identifiability is unassessed and no confidence intervals are reported for any estimated parameter. The authors acknowledge that "the simulations do not help us in predicting the values of η or mu_EI," which is precisely the kind of non-identifiability that profile likelihood would characterize. The pairs plots suggest a ridge between Beta and mu_IR, but this is not quantified with a profile.

**Fix:** Compute profile likelihoods for at least Beta and rho, the two scientifically most important parameters. Report MCAP confidence intervals.

---

### 6. Second iterated filtering exercise contradicts its stated purpose

The text states: "we perform a global search for a simple SEIR model without any covariates and without vaccination." However, the code on the next line calls `mif2(datSEIR, ...)` where `datSEIR` is the vaccination-covariate model (`seir_step_mod_ver2`) defined earlier in the Rmd. The object `datSEIR` was last modified to include both the C50 policy covariate and the IM vaccination covariate. The code does not redefine datSEIR to a simpler model before the second search. This means the second analysis does not in fact use a covariate-free SEIR; its results are not interpretable as claimed.

**Fix:** Construct a separate pomp object with only the basic `seir_step` snippet and no covariate table, then perform the second global search on that object.

---

### 7. Underdispersed binomial measurement model for COVID-19 data

The measurement model is `reports ~ Binomial(H, rho)`. The binomial distribution is at most as dispersed as H. COVID-19 daily case counts are highly overdispersed relative to the binomial, due to reporting delays, day-of-week effects, super-spreading events, and surveillance heterogeneity. A negative binomial measurement model with an overdispersion parameter would be substantially more appropriate. The use of a binomial model almost certainly causes the optimizer to find likelihoods that are artificially penalized for natural data variability, contributing to the poor optimization behavior observed.

**Fix:** Replace the binomial measurement model with a negative binomial: `reports ~ NegBin(mu = H * rho, size = psi)` where psi is an estimated overdispersion parameter.

---

## Computational and Diagnostic Assessment

**Convergence:** No convergence evidence is provided. The two global searches each run 500 mif2 replicates from diverse starting values (guesses, not shown in code but referenced), but no trace plots are presented. The extremely wide log-likelihood filter thresholds (50,000 and 10,000 units) are strong indirect evidence of convergence failure.

**Particle filter:** Np=5000 is used in mif2 and Np=20,000 is used for final likelihood re-evaluation with 200 replicates per chain. These are reasonable particle counts. However, ESS is never monitored during filtering. The Monte Carlo SE of the likelihood estimates is computed (`se=TRUE` in logmeanexp) but never reported or discussed.

**Conditional log-likelihoods:** Not computed. Plotting per-time-step log-likelihoods would identify which periods of the epidemic are poorly fit by the model — a standard diagnostic that is especially valuable here given the model's acknowledged misspecification.

**Profile likelihoods:** Not computed for any parameter. No confidence intervals are reported.

**Computational scale:** The full-data global search ran 8+ hours on a 36-core Linux cluster. This is a genuine computational investment, but without convergence diagnostics the effort cannot be evaluated.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file and is substantially complete. However, the actual stew-cached `.rda` files (box_eval_covar.rda, box_eval_simple.rda) are not in the project folder, so the expensive computation cannot be re-evaluated or verified without re-running it.

**Final parameters:** No final MLE parameter vector is archived or reported in a table. Readers cannot evaluate the fitted model without re-running the 8-hour optimization.

**Model-code consistency:** The text states the second analysis uses a "simple SEIR model without any covariates and without vaccination," but the code uses the vaccination-covariate datSEIR object. This is a direct inconsistency between text and code.

**Package versions:** No sessionInfo() or renv lockfile is provided. The pomp API has changed across versions; results may not reproduce on current CRAN releases.

**Auxiliary data:** All data is loaded from live URLs at runtime. The covidtracking.com API has since been discontinued, meaning the code cannot be re-run as written. The vaccination data URL may also be unstable.

**HPC reproducibility:** The global search is described as running on a cluster but no job submission scripts or environment specifications are included.

---

## Minor Issues

- **Forecast not delivered:** The introduction states "we will make a prediction on the future positive cases Increase considering the same lock-down control and vaccination increase." No forecast is produced in the paper.

- **Covariate multipliers not estimated:** The C50 values 1.38 and 0.89 are manually chosen by reasoning ("~1.4 times the actual rate") rather than estimated statistically. No sensitivity analysis is performed for these values. They function as hidden fixed parameters that directly affect the likelihood surface.

- **No safeguard against negative compartments:** In `seir_step_mod_ver2`, the update `S -= dN_SE + IM` can produce negative S if IM (daily new vaccinations) exceeds the remaining S population, particularly late in the vaccination campaign. No nearbyint clipping or bounds-checking is present for S.

- **Initial reporting rate rho = 0.9 is biologically implausible:** The initial guess rho = 0.9 implies 90% of infections are detected. Epidemiological consensus during the study period estimated true detection at 5–20% of infections. The pairs plot post-optimization shows rho ~ 0.2, consistent with the literature. While the initial guess does not affect the MLE in principle, it may affect convergence speed.

- **No quantitative comparison between ARMA and SEIR:** The ARMA section concludes "we observe no significant evidence that the ARIMA model performs better than white noise" and nominates white noise as a benchmark, but the SEIR log-likelihood is never compared to either. Cross-model log-likelihood comparison is valid (MT2 Q4-01) and is expected in a complete analysis.

- **guesses object not shown:** The code references `iter(guesses, "row")` in both global searches but the construction of `guesses` and `fixed_params` is not shown in the Rmd. Readers cannot determine how starting values were distributed.

- **No table of fitted parameter estimates:** No summary table presents the final parameter values. The pairs plots are the only output, but with a 50,000-unit filter these are uninterpretable as parameter estimates.

- **Live URL dependency breaks reproducibility:** All data is fetched from remote URLs. The covidtracking.com API was retired in March 2021, meaning the code cannot run on new machines. Local data files should be included.

---

## Recommendation

**Major Revision.** The project engages with a scientifically important question and deploys substantial computational resources, but three intersecting problems make the current results uninterpretable: (1) no trace plots, so convergence is undemonstrated; (2) a fundamental mismatch between H (stock) and the incidence data; and (3) no absolute log-likelihood reported. Additionally, the second analysis is internally inconsistent (uses wrong model object). These issues must be resolved before the results have statistical validity. The authors should also add a negative binomial measurement model and profile likelihoods for at least the two key parameters.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W21/project01/blinded.Rmd`
