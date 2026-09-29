# Peer Review: W24 Project 16
## *Modelling of the Influenza cases and spread in the Netherlands using ARIMA and POMP(SEIR) models*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) + replicated pfilter for likelihood evaluation |
| **R packages used** | pomp, forecast, doFuture, doParallel, doRNG |
| **Code publicly available** | GitHub repository linked in data code; run.r and Blinded.Rmd present |
| **Data publicly available** | WHO FluNet data, loaded via GitHub raw URL |
| **Benchmark comparison included** | No (ARIMA section present but no quantitative cross-model comparison) |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + pfilter used; logmeanexp misapplied across parameter runs |
| 2 | Benchmark comparison | ~ | ARIMA section present but no loglik comparison to POMP |
| 3 | Quantitative goodness-of-fit reporting | ~ | Best loglik reported but from a misapplied logmeanexp call |
| 4 | Model diagnostics | ✗ | No simulations from best-fit parameters; no ESS reporting |
| 5 | Parameter identifiability and uncertainty | ✗ | Profile plots from global search envelope, not true profiles; implausible estimates unreflected on |
| 6 | Computational adequacy | ~ | Global search with 400 starts and Np=10000 is reasonable; trace plots show a different local search |
| 7 | Forecast methodology | N/A | No forecasting performed |
| 8 | Model variations and nested comparisons | ✗ | No alternative model structures compared |
| 9 | Stochasticity | ✓ | Binomial transitions with exponential probabilities; NegBin measurement model |
| 10 | Reproducibility and extendability | ✗ | Hard-coded paths; no archived MLE parameters; code/text inconsistency |
| 11 | Corroboration with scientific knowledge | ✗ | Implausible parameter estimates interpreted as biological findings |
| 12 | Measurement model specification | ✗ | H accumulates recoveries, not incidence; rho ~ 0.003 not discussed |
| 13 | Initial conditions | ~ | Initial conditions parameterized via eta; text/code mismatch in S_u |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

This project fits a dual-branch SEIR POMP model to Netherlands influenza sentinel surveillance data from the 2022-2023 season, with the aim of comparing transmission and recovery dynamics between vaccinated and unvaccinated individuals. The paper introduces an interesting scientific question and uses a global random search on a computing cluster to explore the parameter space. However, the model contains a fundamental structural error (decoupled transmission between the two subpopulations), the accumulator variable H tracks recoveries rather than incidence, and several critical statistical procedures are misapplied or absent. The interpretation of implausible parameter estimates as biological findings rather than evidence of model misspecification is a notable concern.

**Strengths:** Clear scientific motivation; use of cluster computing for global search; correct use of logmeanexp for replicated pfilter calls; includes both vaccinated and unvaccinated compartments; good reporting of computational effort.

**Weaknesses:** Decoupled transmission between subpopulations is a structural model flaw; H accumulates recoveries not incidence; logmeanexp misapplied to summarize the global search; implausible MLE estimates not diagnosed as misspecification; no simulation from best-fit parameters; text/code inconsistency in initialization.

---

## Major Issues

### 1. Decoupled subpopulation transmission — a fundamental structural flaw

The force of infection in the step function uses `Beta_v * I_v / N` for the vaccinated subpopulation and `Beta_u * I_u / N` for the unvaccinated subpopulation. This means vaccinated susceptibles can only be infected by vaccinated infectious individuals, and unvaccinated susceptibles can only be infected by unvaccinated infectious individuals. Cross-group transmission — an unvaccinated infectious person infecting a vaccinated susceptible, or vice versa — is entirely absent from the model.

In any realistic mixed population, disease spreads across vaccination status. The absence of cross-group transmission means the two branches evolve as completely independent epidemics sharing only population size N. Any conclusions about relative transmission rates between vaccinated and unvaccinated groups are drawn from a model where those groups do not interact, which is a scientifically untenable assumption. A corrected force of infection for vaccinated susceptibles would be proportional to (I_v + I_u) or a weighted mixture, and similarly for unvaccinated susceptibles.

This flaw undermines all quantitative conclusions drawn from the model, including the core finding that β_v < β_u.

---

### 2. Accumulator H tracks recoveries (IR transitions), not incidence (EI or SE transitions)

In `seir_step`, the accumulator H is incremented by `dN_IR_v + dN_IR_u`, which counts individuals transitioning from infectious (I) to recovered (R) in each time step. The measurement model then assumes:

```
INF_ALL ~ NegBin(k, rho * H)
```

Netherlands sentinel surveillance counts new flu diagnoses (cases entering the healthcare system, approximately at the EI or SE transition), not recoveries. Using IR transitions as the driver of observed incidence introduces a systematic phase lag equal to the infectious period. For vaccinated individuals with estimated mu_IR_v ~ 0.001 (implying infectious periods of hundreds to thousands of days), this lag is enormous. The standard SEIR POMP implementation tracks EI transitions (or SE transitions) in H to represent incidence. This should be corrected to `H += dN_EI_v + dN_EI_u` (or `dN_SE_v + dN_SE_u`).

---

### 3. Logmeanexp misapplied across multiple optimization runs

Section "Result" contains:

```r
logmeanexp(profile_results$loglik, se=TRUE)
```

described as "The negative log likelihood in these runs reach a maximum (likelihood minimum) at:" followed by the output. The `logmeanexp` function computes `log(mean(exp(x)))`, which is the correct aggregation for replicate particle filter runs at a single fixed parameter vector — it converts multiple unbiased estimates on the natural likelihood scale back to the log scale (Error 1.1 in the course weakness reference). It is not appropriate for summarizing log-likelihood values from 349 optimization runs at different parameter vectors. Applied this way, it produces a quantity without a clear statistical interpretation and conflates the best-fit log-likelihood with a weighted average across the parameter space. The correct reporting is simply `max(profile_results$loglik)` = -189.93 (loglik.se = 0.021).

Additionally, the description refers to the "negative log likelihood reaches a maximum (likelihood minimum)" — the maximum of the log-likelihood corresponds to the best fit, not the minimum.

---

### 4. Implausible parameter estimates not diagnosed as model misspecification

The top five global search results (available in global_search.rds) show mu_IR_v values of approximately 0.0015, 0.00017, 0.00018, 0.00030, and 0.667. The first four imply infectious-to-recovery transition rates for vaccinated individuals with mean infectious periods of 667, 5900, 5600, and 3300 days, respectively. These are biologically impossible for influenza.

The paper attributes this to "vaccinated people that actually get sick take longer to recover" and speculates about preexisting conditions. This is a misinterpretation. Per course instruction (Error 1.5 in the weakness reference), when mif2 drives a parameter to a biologically implausible extreme, the correct diagnosis is model misspecification, not a new biological discovery. The near-zero mu_IR_v is consistent with the model compensating for structural issues (the decoupled transmission and the IR-tracking accumulator identified in Issues 1 and 2). The profile plots for mu_IR_v are consistent with an unidentified parameter.

---

### 5. Profile plots constructed from global search envelope are not true profile likelihoods

The "profile" plots for Beta_v, Beta_u, mu_IR_v, mu_IR_u, and the ratios are constructed by:

```r
profile_results %>%
  filter(loglik > max(loglik) - 15) %>%
  group_by(round(Beta_v, 2.0)) %>%
  filter(rank(-loglik) < 3) %>%
  ungroup() %>%
  ggplot(aes(x=Beta_v, y=loglik)) + ...
```

This takes the upper envelope of global search results binned by rounded parameter values. A true profile likelihood requires fixing the target parameter at each grid point and maximizing over all nuisance parameters via a dedicated optimization run at each point (Error 1.2 in the weakness reference). The global search may not have representative coverage at each parameter value, so the upper envelope can underestimate the true profile (CIs will be too wide) or produce a misleading shape. The 95% CI threshold `max(loglik) - 0.5 * qchisq(df=1, p=0.95)` = -191.85 is shown but confidence intervals are not reported numerically. For the ratio β_v/β_u, the profile shape is also unusual — it appears to be relatively flat — suggesting the ratio may not be well-identified.

---

### 6. No simulation from best-fit parameters — key diagnostic absent

The paper does not include a single simulation from the fitted model overlaid on the observed data. This is the primary visual diagnostic for POMP models (Wheeler et al. 2024, §Model diagnostics): after optimization, forward simulations from the MLE parameters should be compared to the observed time series to assess whether the model captures the main features (outbreak timing, peak height, and decline). Without this plot, it is impossible to judge whether the model provides a scientifically plausible description of the data.

---

### 7. Convergence diagnostics shown are from a different local search than used for global optimization

The Rmd displays mif2 trace plots from a local search using Np=2000, Nmif=300, cooling.fraction.50=0.2, and large perturbations (rw.sd=0.15 for Beta parameters). However, the cluster script run.r, which produces the global_search.rds results, uses a separate local search with Np=1000, Nmif=50, cooling.fraction.50=0.6, and rw.sd=0.02 for all parameters. The trace plots in the Rmd are not derived from the initialization used for the global search, so they do not demonstrate convergence of the procedure that generates the main results.

---

### 8. Initialization formula mismatch between text and code

The paper specifies:

$$S_u = (\text{vaccinationRate} \times \eta_u \times N)$$

but the code correctly implements:

```c
S_u = nearbyint((1-vac_rate) * eta_u * N);
```

The code is correct (unvaccinated susceptibles should be a proportion of the unvaccinated population `(1 - vac_rate) * N`), but the mathematical specification in the text incorrectly uses `vaccinationRate` for both. Per the code supplement checklist (Wheeler et al. 2024), discrepancies between mathematical description and code implementation are a reproducibility failure. Readers relying on the text cannot correctly reconstruct the model.

---

## Minor Issues

### 9. No quantitative benchmark comparison between POMP and ARIMA

The paper discusses ARIMA models at length and selects ARIMA(0,1,4) as the best ARIMA specification. The POMP model achieves a best loglik of -189.93 (8 free parameters, AIC ≈ 395.9). The ARIMA AIC values are reported in tables but the ARIMA log-likelihood is not compared numerically to the POMP log-likelihood. A single sentence noting the log-likelihood gap would contextualize the POMP model's performance. Per 531-conventions.md, likelihoods from ARIMA and POMP models are directly comparable when fit to the same data. (Per 531-conventions.md, absence of a benchmark is not automatically a flaw, but the machinery for the comparison is already in place.)

---

### 10. Overdispersion parameter k=10 fixed without justification

The NegBin dispersion parameter k is fixed at 10 throughout. No rationale is provided for this value, and it is not estimated as part of the optimization. The value of k materially affects the width of the measurement distribution and hence the likelihood surface. Sensitivity of conclusions to k should at minimum be noted.

---

### 11. Aggressive cooling (cooling.fraction.50=0.2) in local mif2

The local mif2 in the Rmd uses `cooling.fraction.50=0.2`, which cools perturbations to 20% of their initial value after 50 iterations. The course standard (Ch 15) is 0.5. With Nmif=300, the perturbations drop to 0.2^6 ≈ 0.00006 of their initial value by iteration 300, effectively stopping exploration very early. This may prevent the local optimizer from finding the best nearby optimum and could explain the wide spread seen in parameter trace plots.

---

### 12. Best-fit rho ≈ 0.003 not discussed relative to known surveillance coverage

The best-fit reporting rate rho ≈ 0.003 (0.3%) is not discussed. For Netherlands sentinel surveillance, which covers a subset of general practitioners, a low reporting fraction is expected — but 0.3% would mean only 1 in 300 actual cases appears in the data. This should at minimum be noted as a point of corroboration or implausibility. No comparison to external estimates of Netherlands sentinel surveillance coverage is made (Wheeler et al. 2024, §Corroboration with scientific knowledge).

---

### 13. Hard-coded absolute file paths in run.r

The cluster script run.r contains:

```r
flu <- read.csv("/home/falarcon/stats531/final/Flu.csv", sep=";")
```

and later:

```r
f_results <- read_rds("/Users/falarcon/Desktop/all/global_search_2.rds")
```

These paths are specific to the author's machines and break reproducibility for any other reader.

---

### 14. AIC tables not checked for optimization consistency

The AIC table for d=1 models includes entries across p=0..4, q=0..4. Several entries in the AIC table likely show irregular patterns (e.g., AIC increasing by more than 2 units when adding one parameter to a nested model). Per Error 2.13 in the course weakness reference, an AIC increase exceeding 2 units when adding one parameter to a nested model indicates numerical optimization failure and should be flagged. The paper does not comment on the internal consistency of the AIC table.

---

### 15. Parallel local mif2 in Rmd not seeded with doRNG

The local mif2 parallel loop in the Rmd:

```r
foreach(i=1:4, .combine=c, .packages=c("pomp")) %dopar% {
  fluSEIR |> mif2(...)
}
```

does not include a preceding `registerDoRNG()` call, making the results not exactly reproducible. In contrast, the global search code block correctly uses `registerDoRNG(12345)`. The Rmd also sets `set.seed(2488820)` at the top, but this does not propagate into parallel workers without `doRNG`.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots from 4 local mif2 runs (Np=2000, Nmif=300) are shown. The loglik panel should be checked for consistent upward convergence. However, as noted in Issue 7, these trace plots come from a separate local search that was not used to initialize the global search on the cluster.

**Particle filter:** Np=10,000 used for likelihood re-evaluation in the global search; replicated 10 times with logmeanexp for each run. Particle count and replicate count are appropriate. ESS is not monitored or reported.

**Conditional log-likelihoods:** Not computed or discussed. Per-time-step log-likelihoods would be informative for identifying time periods of poor fit.

**Profile likelihoods:** See Issue 5. The plots labeled as profiles are upper envelopes of the global search, not dedicated profile computations. No numerical CI bounds are reported.

**Computational scale:** 400 global search starts, each with Np=1,000 local mif2 seed followed by Nmif=1,000 continuation, and 10 replicated pfilter(Np=10,000) evaluations. This is a reasonable effort. Total CPU-hours not reported.

---

## Reproducibility Assessment

**Code availability:** Rmd and run.r are present. The global_search.rds is archived in the repository.

**Final parameters:** The best-fit parameter vector is not archived as a standalone file; it can be recovered from global_search.rds but this requires loading the full 400-row result table.

**Model-code consistency:** Text/code inconsistency in S_u initialization (Issue 8). The accumulator H definition (Issue 2) is consistent between code and run.r but inconsistent with the paper's scientific claim.

**Package versions:** No `sessionInfo()` output or renv lockfile provided. The pomp API version is not pinned.

**Auxiliary data:** Data loaded from a GitHub raw URL; if that URL changes or becomes unavailable, the analysis breaks. No local copy archived.

**HPC reproducibility:** run.r is provided and uses `bake()` for caching, but hard-coded paths (Issue 13) prevent out-of-box reproduction on another system.

---

## Recommendation

**Major Revision.** The paper addresses an interesting scientific question and demonstrates appropriate use of cluster computing and IF2 optimization. However, it contains a structural model flaw (decoupled subpopulation transmission, Issue 1) and an accumulator specification error (H tracks recoveries rather than incidence, Issue 2) that together undermine the core scientific conclusions. The misuse of logmeanexp (Issue 3) and interpretation of implausible estimates as biological findings without considering misspecification (Issue 4) are also major concerns directly covered by course material. Before the conclusions about vaccine effectiveness can be taken seriously, the model structure must be corrected and the analysis re-run.

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
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project16/Blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project16/run.r`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project16/global_search.rds`
