# Peer Review: W22 Project 16 — Modeling Covid-19 With Multivariate POMP Model

---

## Summary

This project proposes two POMP-based epidemic models for Moscow Covid-19 data: a multivariate **SIR-CDR** model that simultaneously observes confirmed cases, deaths, and recoveries, and a simpler **SIR-D** model that observes only daily deaths. The SIR-CDR model is presented but never run (all code chunks are set to `eval=FALSE`). The SIR-D model is fitted with local and global IF2 searches and a profile likelihood attempt. Both models fail to capture the data adequately, as acknowledged in the conclusion. The project has significant methodological and reporting weaknesses detailed below, ordered from most to least critical.

---

## Major Weaknesses

### 1. SIR-CDR Model Is Completely Unexecuted

The primary model proposed in the title and abstract — the multivariate SIR-CDR model — has all of its code chunks marked `eval=FALSE, include=FALSE`. This means no particle filtering, no MIF2 search, and no simulation results are ever produced for this model. A model described over several paragraphs with a diagram and detailed equations but never fitted provides no scientific value. The conclusion claims this model is "worth reporting," but with no numerical evidence at all, this claim is unsupported.

### 2. Process Model Bug: Symptomatic Compartment Updated Twice with Conflicting Logic (SIR-CDR)

In the `covid_step` C snippet for the SIR-CDR model, the update to `Sy` occurs twice in a logically inconsistent manner. First, `dN_SyH` is subtracted from `Sy` unconditionally at line `Sy += dN_SSy + dN_ASy - dN_SyR - dN_SyD;`, and then the capacity constraint block either overwrites `H = Cap` and subtracts from `Sy` or subtracts `dN_SyH` again from `Sy`. Additionally, `dN_SyD` is subtracted from `Sy` in the first update but then `dN_SyH` is also listed redundantly in the capacity block. This double-counting of flows is a fundamental bug that would cause negative compartment sizes and incorrect simulation behavior.

### 3. Process Model Bug: Symptomatic Compartment Omits `dN_SyH` Subtraction in the `else` Branch (SIR-CDR)

Examining the capacity constraint block: when `Sy + H <= Cap`, the code does `Sy -= dN_SyH` and `H += dN_SyH`, but `dN_SyH` was already applied to `Sy` in the line `Sy += dN_SSy + dN_ASy - dN_SyR - dN_SyD`. This means symptomatic individuals flowing to hospital are subtracted twice. Because this entire model is never executed (`eval=FALSE`), the bug was never caught.

### 4. Force-of-Infection Splits Beta Incorrectly

In both the SIR-CDR and SIR-D models, the infection process uses two separate binomial draws from `S`: one for new asymptomatics and one for new symptomatics, parametrized as `Beta*Alpha` and `Beta*(1-Alpha)` respectively. However, these are two simultaneous draws from the same source compartment `S`, meaning an individual in `S` can be simultaneously removed by both flows. The correct approach is a single multinomial draw from `S`, or a sequential binomial thinning. As implemented, the total flow out of `S` exceeds what a single correctly-specified Euler-Multinomial step would produce, inflating transmission.

### 5. Measurement Model for SIR-D Is Problematic

The measurement model uses `dnbinom_mu(deaths, k, D, give_log)` where `D` is the accumulator for expected daily deaths. However, `D` is a count of deaths occurring in the latent process — it is itself stochastic and discrete — so using it directly as the `mu` parameter of a negative binomial creates a doubly-stochastic, non-standard measurement structure that is not discussed or justified. If `D` can be 0 (and it will be during early epidemic days), `dnbinom_mu` with `mu=0` will assign probability 1 only if `deaths=0`, making the likelihood extremely sensitive to sparse early data.

### 6. Global Search Is Severely Underpowered

At run level 2, `Nreps_global = 20` starting points are used with only `Np = 1000` particles and `Nmif = 100` IF2 iterations (and an additional `Nmif/2 = 50` refinement step). Twenty global starting points is inadequate to explore a 4-dimensional free-parameter space. Standard practice in the course recommends at least 40-100 restarts for a thorough global search. The sparse global coverage likely contributes to the failure to converge on a good optimum, yet the authors attribute failure entirely to model misspecification.

### 7. Profile Likelihood Is Conducted Over a Misspecified Range

The profile is constructed for `Mu_SyR` over the range [0.01, 0.95], but the authors themselves note that the optimized model favors `Mu_SyR` values above 100. Profiling over a range that explicitly excludes the observed optimum has no inferential value. The authors acknowledge this renders the profile "no real meaningful interpretation," yet they still present it without attempting to fix the problem (e.g., by profiling over [1, 200]).

### 8. No Model Comparison or Likelihood Benchmarks

Neither model is compared against any baseline. For the SIR-D model, there is no comparison against a simpler SIR model, no null model log-likelihood, and no discussion of what constitutes an acceptable log-likelihood for this data. The global search yields a best log-likelihood value that is reported in a table but never discussed in terms of whether it is plausible relative to the data size or a saturated model.

### 9. Inconsistency Between Stated and Coded Initial Infection Rate

The text for the local search section states the starting value as `eta = 0.002`, but the code sets `eta = 0.0002` in the `params=c(...)` block. The parameter description also says `eta = 0.0002`. This discrepancy is a presentation error, but it also suggests insufficient proofreading.

---

## Minor Weaknesses

### 10. `Mu_SyR` Renamed from `Mu_R` Between Models Without Explanation

In the SIR-CDR model, the shared recovery rate is called `Mu_R`. In the SIR-D model, the symptomatic recovery rate is called `Mu_SyR`. The relationship between these parameters is never clarified. The text also refers to a `Mu_SyR` parameter in the SIR-CDR description (line 129: "$\mu_{SyR}$: the mean recovery rate for symptomatic cases") but the SIR-CDR parameter list on line 128 says this shares `Mu_R`. The text is self-contradictory.

### 11. Equation 169 in the SIR-CDR Process Model Repeats `dN_SyH`

The process model equations list `dN_{SyH}` twice (lines 168 and 169 in the Rmd), with two different definitions. Line 168 defines it as the flow from Sy to H, and line 169 redefines it as the flow from Sy resulting in death (`Mu_SyD`). This is almost certainly a LaTeX transcription error (the second equation should be `dN_{SyD}`), but it introduces ambiguity in the mathematical presentation.

### 12. Capacity Constraint Is Implemented Incorrectly in the C Code

The capacity block reads:
```c
if (Sy + H > Cap) {
  H = Cap;
  Sy -= (Sy + H - Cap);
}
```
This uses `H` after it has already been set to `Cap` in the same `if` block, so `Sy + H - Cap` evaluates to `Sy + Cap - Cap = Sy`, effectively zeroing out `Sy` regardless of actual overflow. This is a straightforward C scoping bug.

### 13. Population Mismatch Between Data and Parameters

The dataset reports Moscow population as 12,692,466 in the data file, but the model sets `N = 11,920,000` as a fixed parameter throughout, with a note "it's available in our dataset." The value in the dataset is 12,692,466. Using an incorrect population size biases all per-capita rate estimates.

### 14. No Diagnostic Plots for Effective Sample Size or Filter Convergence

No effective sample size (ESS) plots are shown for any particle filter run. The text mentions "constantly single-digit effective sample sizes" for the SIR-CDR model but provides no plot or table to document this for the SIR-D model. ESS diagnostics are a standard requirement for validating that particle filtering is functioning.

### 15. Conclusion Overstates the Value of the Unexecuted Model

The conclusion states that the SIR-CDR model "could lead to modeling advantages" and is "worth reporting." Since the model was never run, there is no empirical basis for this claim. Presenting a model diagram and equations without any output — not even a single simulation trace or pfilter log-likelihood — does not constitute a scientific contribution within the scope of this report.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/data/Moscow.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/run_level_2/cores.rds` (existence confirmed)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/run_level_2/global_search.rds` (existence confirmed)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/run_level_2/local_result.rds` (existence confirmed)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/run_level_2/local_search.rds` (existence confirmed)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/run_level_2/Mu_SyR_prof.rds` (existence confirmed)
