# Peer Review: W24 Project 15
## "Analysis of Middle-East Respiratory Syndrome coronavirus in Saudi Arabia"

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) with replicated pfilter likelihood evaluation |
| **R packages used** | pomp, tidyverse, lubridate, tsibble, feasts, forecast, foreach, doParallel, doRNG |
| **Code publicly available** | Yes (Git repository) |
| **Data publicly available** | Yes (Kaggle/WHO dataset; included as weekly_clean.csv) |
| **Benchmark comparison included** | Yes — ARMA(1,4) benchmark with log-likelihood reported |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + replicated pfilter used; but dmeas/rmeas mismatch corrupts the likelihood |
| 2 | Benchmark comparison | ~ | ARMA(1,4) benchmark provided; LRT comparison methodology is flawed |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported; but values are suspect due to measurement model error |
| 4 | Model diagnostics | ~ | ESS and pfilter plots shown; no conditional log-likelihood over time; no filtering-distribution simulations |
| 5 | Parameter identifiability and uncertainty | ~ | Profile likelihood for rho_CH only; profile MLE at boundary; no CI for Beta or mu_IR |
| 6 | Computational adequacy | ~ | Convergence traces shown; global search distribution not reported |
| 7 | Forecast methodology | ✗ | No forecasting attempted |
| 8 | Model variations and nested comparisons | ✗ | No alternative model structures tested |
| 9 | Stochasticity | ✓ | Binomial transitions with NB measurement model |
| 10 | Reproducibility and extendability | ~ | Code present; no sessionInfo or package version pinning; model.png referenced but not in folder |
| 11 | Corroboration with scientific knowledge | ~ | R0 compared to Lin et al. (2018); rho_CH sanity check provided |
| 12 | Measurement model specification | ✗ | dmeas mean is 4x too small relative to rmeas; critical inconsistency |
| 13 | Initial conditions | ~ | Initial conditions estimated as parameters; no sensitivity analysis |

---

## Summary

This project fits a SEIRS camel-to-human spillover model to weekly MERS-CoV case counts in Saudi Arabia from January 2014 to May 2016, following Lin et al. (2018). The latent process models disease dynamics among the camel population (N = 270,000), and human cases are treated as an observation of infectious camel activity. An ARMA(1,4) benchmark is estimated and compared to the SEIRS model using log-likelihoods. A profile likelihood is constructed for the camel-to-human spillover rate rho_CH.

**Strengths:** The project follows the standard STATS 531 POMP workflow competently: iterated filtering with a global search, replicated pfilter likelihood evaluation using logmeanexp, and convergence trace plots. The biological motivation for the camel-reservoir model is well-explained and draws on published literature. An ARMA benchmark is included, and a biological sanity check for rho_CH is provided.

**Weaknesses:** The most critical flaw is an inconsistency between the dmeasure and rmeasure functions: the simulator generates total human cases as 4 × NB(mean = rho*C) but the density function evaluates against NB(mean = rho*C), omitting the factor of 4 from the mean. This means every log-likelihood value computed by pfilter is based on the wrong measurement model, and all downstream inferences are suspect. Additionally, the profile likelihood for rho_CH peaks at the upper boundary of the search range, making the reported confidence interval degenerate. The likelihood ratio test comparing ARMA to SEIRS misapplies Wilks' theorem to non-nested models.

---

## Major Issues

### 1. Critical dmeas/rmeas inconsistency: factor-of-4 error in measurement model likelihood

The model description states that total reported human cases = 4 × primary camel-to-human cases (C_i). The rmeasure correctly implements this:
```c
int total_to_primary = 4;
reports = total_to_primary * rnbinom_mu(k, rho*C);
```
This generates `reports = 4 × NB(mean = rho*C)`, so E[reports] = 4 × rho × C.

However, the dmeasure evaluates:
```c
lik = dnbinom_mu(reports, k, rho*C, give_log);
```
This treats the observed `reports` (total human cases) as if they follow NB(mean = rho*C), i.e., with a mean that is 4 times too small. The likelihood function therefore evaluates the probability of seeing total human cases under a distribution parameterized by primary case counts.

As a result, pfilter computes a log-likelihood for the wrong distribution, and all reported log-likelihood values (-843.17 at initial parameters, -378.33 at the global optimum) are based on this incorrect density. Since rho = 1 is fixed, the effective mean used in dmeas is C rather than 4C. The correct dmeas should use `4*rho*C` as the mean, or equivalently, the raw accumulation should be `C += 4 * dN_IR * rho_CH`.

This is a direct analog of the measurement model discrepancy identified by Wheeler et al. (2024) as a concrete reproducibility failure in their evaluated models. All conclusions about model comparison rest on flawed log-likelihood estimates.

**Actionable fix:** Replace `dnbinom_mu(reports, k, rho*C, give_log)` with `dnbinom_mu(reports, k, 4*rho*C, give_log)` in the dmeas snippet, and correspondingly replace `rnbinom_mu(k, rho*C)` with `rnbinom_mu(k, 4*rho*C)` in the rmeas (dropping the hard-coded `total_to_primary` multiplier). Re-run all optimization and likelihood evaluation after the fix.

---

### 2. Profile likelihood MLE at the boundary of the search range

The profile likelihood for rho_CH is constructed over the range [0.0001, 0.001] with 40 profile points (nprof = 5 starting values per point). The text itself acknowledges: "The rho_CH with the largest log-likelihood is on the edge of the interval (0.001) we choose to construct the plot." The maximum was not found within the searched interval.

As a consequence, the reported 95% confidence interval — "approximately around 0.001" — is degenerate: the upper confidence limit coincides with the upper boundary of the profile grid. The profile does not identify the true MLE and cannot support a valid confidence interval. The statement "the 95% confidence interval is approximately around 0.001, which is quite narrow" is misleading; a flat or boundary-hitting profile does not indicate precision.

Additionally, the global search (which searched rho_CH up to 0.001) found its best estimate at exactly rho_CH = 0.001, consistent with the profile finding. This further confirms the MLE lies at or beyond the boundary.

**Actionable fix:** Extend the profile range to at least [0.0001, 0.005] or larger, and re-run the profile until the likelihood clearly declines on both sides of the maximum. Also expand the global search upper bound for rho_CH accordingly. Only after the profile has a well-defined interior maximum should the CI be reported.

---

### 3. Likelihood ratio test applied to non-nested models

The authors compare ARMA(1,4) (log-likelihood = -422.77, D = 5 parameters) and SEIRS (log-likelihood = -378.33, D = 8 parameters) using a chi-squared likelihood ratio test with df = 3:

```r
cat(paste("p-value:", 1 - pchisq(2 * ll_diff, df=d_diff)))
```

The Wilks approximation — under which 2(ℓ₁ − ℓ₀) follows a chi-squared distribution under H₀ — requires that H₀ is nested within H₁. ARMA(1,4) and the SEIRS POMP model are not nested: neither can be obtained from the other by fixing parameters. Applying the chi-squared LRT to non-nested models produces an invalid p-value and an incorrect basis for rejecting H₀.

Comparing log-likelihoods and AIC values across model classes is legitimate (as taught in the course: likelihoods for different models of the same data are directly comparable). However, a formal chi-squared LRT requires nesting. The correct approach is to compare AIC values or simply note the 44-unit log-likelihood difference as strong practical evidence in favor of SEIRS.

Note: This is related to course-confirmed Error 2.2 in the STATS 531 weakness reference — students were explicitly tested on the distinction between valid likelihood comparison and the specific requirements for the Wilks approximation.

**Actionable fix:** Remove the chi-squared LRT and replace with an AIC comparison (ΔAIC = −2 × 44.44 + 2 × 3 = −82.88 in favor of SEIRS), or simply state the log-likelihood difference and note that it provides strong evidence for the SEIRS model without appealing to the Wilks distribution.

---

### 4. mif2 internal log-likelihood used to claim superiority over ARMA benchmark

In the local search section, the trace plot commentary states: "The log-likelihood converges to above -400, which is better than the ARMA(1,4) model." This uses the mif2 internal log-likelihood (from convergence trace plots) rather than the properly evaluated likelihood from replicated pfilter calls.

The mif2 internal log-likelihood is not reliable for inference: parameter perturbations are applied throughout optimization, and the perturbation-included likelihood is a biased estimate of the true log-likelihood at the converged parameters. The course convention (531-conventions.md) explicitly flags this: "mif2's internally reported likelihood is NOT reliable for inference." The proper comparison comes from the global search result (-378.33), which was correctly evaluated via replicated pfilter with logmeanexp.

**Actionable fix:** Remove or qualify the statement comparing the mif2 trace log-likelihood to the ARMA benchmark. The local search section should state that the trace shows convergence direction, and direct the reader to the global search section for proper likelihood values.

---

### 5. No profile likelihoods or confidence intervals for key parameters (Beta, mu_IR, R0)

The basic reproduction number R0 = Beta / mu_IR = 2.6 is presented as a point estimate with no uncertainty. Neither Beta nor mu_IR has a profile likelihood or confidence interval. Given that R0 is the primary scientific summary of transmission intensity, reporting it without uncertainty is insufficient.

The trace plots show that Beta and mu_IR do appear to converge during local search (noted in the text), but convergence of the optimizer does not imply a narrow likelihood. Profiles are needed to assess identifiability and provide valid CIs.

The course standard (531-conventions.md, §Profile likelihoods) requires profiles for key parameters, particularly those used in scientific interpretation.

**Actionable fix:** Compute profile likelihoods for at least Beta and mu_IR, and propagate uncertainty into the R0 estimate. A profile for Beta/mu_IR jointly or a derived-quantity profile could also be used.

---

### 6. Global search: no distribution of likelihoods across 400 starting points

The global search runs 400 starting points and reports only the single best result (log-likelihood = -378.33). No histogram, scatter plot, or summary of the distribution of likelihoods across runs is presented. Without seeing how the 400 runs distribute, it is impossible to assess whether the global search genuinely explored the parameter space or whether results cluster near the best value (indicating convergence) or scatter widely (indicating insufficient optimization per starting point).

The pairs plot shown uses results from the profile likelihood section (via `read_csv("saudi_mers_params_profile.csv")` in the profile code), not the global search results directly.

**Actionable fix:** Show a scatter plot or histogram of log-likelihoods across the 400 global search runs. A pairs plot of loglik vs. each parameter from the global search (as done in the local search section) would provide evidence of convergence and identifiability.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots from the local search (10 runs × 100 iterations, Np = 2000) are shown. The loglik panel shows upward convergence, which is good. The global search (400 starting points, inherited Np and Nmif from mf1 plus 50 additional iterations) has no associated trace plots or loglik distribution, making convergence assessment for the global phase impossible.

**Particle filter:** ESS is plotted for the initial parameter check (Np = 2000, single run). ESS drops near the outbreak peaks but remains above 500, which the authors interpret as acceptable. This single pfilter run at initial parameters lacks a Monte Carlo SE (no replicate calls), which is a minor issue since it is used only for preliminary checking, not inference.

**Conditional log-likelihoods:** No per-time-step conditional log-likelihood plot is produced. Such a plot would identify whether the model systematically fails to fit specific periods (e.g., the peak around week 80 that the initial simulation did not capture). This is a missed diagnostic opportunity (Wheeler et al. 2024, §Model diagnostics).

**Profile likelihoods:** Profile computed only for rho_CH, and the MLE falls at the search boundary (see Major Issue 2). No profiles for Beta, mu_IR, eta, or eta2.

**Computational scale:** Parallelization via doParallel is used. Total CPU-hours are not reported. The Np = 2000 and Nmif = 100 (local search) / Nmif = 100+50 (global search) are reasonable run_level=2 to run_level=3 settings. The very small rw.sd for eta2 (ivp(0.0001)) and rho_CH (0.0001) may limit exploration, but these are minor parameter-tuning concerns.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file and data is included (weekly_clean.csv). The RDS caching pattern (bake/readRDS) is used to avoid re-running expensive computations.

**Final parameters:** MLE parameter vectors are archived to CSV files (saudi_mers_params.csv, saudi_mers_params_profile.csv), which is good practice consistent with Wheeler et al. (2024).

**Model-code consistency:** As described in Major Issue 1, the measurement model in code does not match the mathematical description. The text says reports = 4 × C_i (where C_i ~ NB with mean Z_i × rho), but dmeas evaluates the likelihood of reports against NB(mean = rho × C), omitting the factor of 4. This is a material discrepancy.

**Package versions:** No sessionInfo() output, renv lockfile, or package version pinning is provided. The pomp API has changed substantially across versions; results may not reproduce on current CRAN releases.

**Auxiliary data:** The data file weekly_clean.csv is present. The file model.png is referenced in the Rmd (`![SEIRS Model Structure](model.png)`) but is not present in the project folder, causing a missing figure in the rendered output.

**HPC reproducibility:** The code checks for SLURM_NTASKS_PER_NODE and uses detectCores() as fallback, suggesting cluster use. No SLURM job scripts or environment specifications are included. A CLUSTER.R file is sourced if present, but this file is not in the repository — its contents and purpose are opaque.

---

## Minor Issues

- **Single pfilter run without Monte Carlo SE at initial parameters:** The line `saudiSEIRS |> pfilter(Np=2000) -> pf; cat("Log-likelihood:", round(logLik(pf), 2))` reports -843.17 from a single run with no standard error. This is used only for a preliminary check (not for inference), but noting the MC noise would be good practice (Error 1.4 in 531-weakness-reference.md).

- **Non-Gaussian ARMA residuals not addressed:** The histogram and QQ plot show heavy tails and non-Gaussian residuals. The authors note this but take no action (no log transformation, no investigation of consequences). For overdispersed count data, a log transform or Poisson/NB ARMA would be more appropriate (Error 2.5 in 531-weakness-reference.md).

- **rw.sd very small for rho_CH and eta2:** In both local and global searches, rw.sd for rho_CH is 0.0001 and for eta2 is ivp(0.0001). The rho_CH range spans 0.0001 to 0.001 (a factor of 10), so a perturbation of 0.0001 on the natural scale is at most one-tenth of the range. This may severely limit IF2's ability to move in the rho_CH direction. Perturbations should typically be specified on a transformed scale (log or logit) to achieve scale-invariant exploration.

- **fmin clamping may break population conservation:** The step function uses `fmin(S, dN_SE + dN_Smu)` and analogous constructions to prevent negative compartments. When activated, this clamping changes the effective transition counts and will not in general preserve S + E + I + R = N = 270,000. The authors mention this as a check, but do not verify that conservation holds in practice. For large compartments (N = 270,000), deviations are likely rare but should be acknowledged.

- **No filtering-distribution simulations:** Simulations are generated forward from estimated initial conditions (forward simulations). No simulations conditioned on the filtering distribution (which incorporates all observed data up to each time point) are shown. These serve different diagnostic purposes and should not be conflated (Wheeler et al. 2024, §Forecast methodology). The visual fit comparison would benefit from filtering-distribution trajectories.

- **No out-of-sample evaluation:** The model is fit to 2014-2016 data and no held-out evaluation or forecast is attempted. Even a brief comparison to 2016-2017 data would strengthen the scientific conclusions.

- **R0 uncertainty:** R0 = Beta/mu_IR = 2.6 is reported as a point estimate with no confidence interval or uncertainty quantification. Given that Beta and mu_IR are estimated parameters with uncertainty, the derived R0 should carry propagated uncertainty.

- **model.png missing from repository:** The Rmd references `![SEIRS Model Structure](model.png)` but the file is absent from the project folder. This produces a broken image in the rendered output.

- **CLUSTER.R referenced but absent:** The line `if (file.exists("CLUSTER.R")) { source("CLUSTER.R") }` references a file not in the repository. Its purpose and contents are unclear.

- **Conclusion overstates profile likelihood result:** "We constructed profile likelihood for the spill-over rate rho_CH with narrow confidence interval" — this is inaccurate given that the profile MLE is at the search boundary and the CI is degenerate (see Major Issue 2).

---

## Recommendation

**Major Revision.** The project demonstrates solid methodological intent and applies the POMP workflow competently, but contains a critical error in the measurement model (Major Issue 1) that invalidates all reported log-likelihood values and model comparisons. The profile likelihood also fails to identify the MLE (Major Issue 2), and the LRT methodology is incorrect for non-nested models (Major Issue 3). These issues must be addressed before any conclusions about model fit or parameter uncertainty can be trusted. After correcting the dmeas/rmeas inconsistency, all optimization and inference should be re-run, and the profile likelihood for rho_CH should be extended to find the true interior maximum.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project15/blinded.html`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project15/weekly_clean.csv` (existence confirmed; content not read)
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project15/Makefile` (existence confirmed; content not read)
