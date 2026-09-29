# Review: W25 Project 04
## COVID-19 Dynamics in Kerala: ARIMA, VAR, and SEIRS POMP Models

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) with particle filter (pfilter) |
| **R packages used** | pomp, forecast, vars, fGarch, tidyverse |
| **Code publicly available** | Partial — submitted via course repository; HPC scripts included |
| **Data publicly available** | Yes — Kerala Government COVID-19 Dashboard |
| **Benchmark comparison included** | Yes — ARIMA(5,1,5) log-likelihood compared to SEIRS models |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + replicated pfilter used; logmeanexp applied correctly |
| 2 | Benchmark comparison | ~ | ARIMA compared to SEIRS; comparison is directionally correct but ARIMA/SEIRS are on different scales |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported; Monte Carlo SE reported in CSV but not always in text |
| 4 | Model diagnostics | ~ | ESS shown for initial guess only; not shown post-convergence |
| 5 | Parameter identifiability and uncertainty | ~ | Profile likelihoods computed for several parameters; mu_RS never profiled |
| 6 | Computational adequacy | ~ | NP=5000, Nmif=200, 400–800 starts; Model 2 explicitly not converged |
| 7 | Forecast methodology | N/A | No forecasting performed |
| 8 | Model variations and nested comparisons | ~ | Multiple SEIRS variants developed; no formal LRT between variants |
| 9 | Stochasticity | ~ | Binomial transitions, negative binomial measurement; but R compartment bug undermines process model |
| 10 | Reproducibility and extendability | ~ | HPC scripts included; profile scripts reference missing data file |
| 11 | Corroboration with scientific knowledge | ~ | Parameters discussed against literature; near-zero b3 accepted without revision |
| 12 | Measurement model specification | ~ | Negative binomial with time-varying rho and k; code matches text |
| 13 | Initial conditions | ~ | eta estimated; I_0 = 1000 fixed without justification |

---

## Summary

The paper applies ARIMA, VAR(9), and a stochastic SEIRS compartmental model to weekly COVID-19 confirmed case counts in Kerala, India (119 weeks, 2020–2022). The SEIRS model uses piecewise-constant transmission rates, reporting rates, and dispersion parameters across three epidemic phases, implemented in the `pomp` framework with IF2 and particle filtering. The final SEIRS candidates substantially outperform the ARIMA benchmark in log-likelihood.

**Strengths:** The iterative model development is clearly documented; intermediate problematic models are presented in the Appendix with honest discussion of their failure modes; computational parameters (NP=5000, Nmif=200) are at run-level 3; profile likelihoods are computed for multiple parameters with 443 points each; the authors correctly use `logmeanexp` for aggregating replicated particle filter runs.

**Weaknesses:** All SEIRS model implementations contain a critical bug in the `rprocess` step — the R compartment is never decremented by the R→S transition, violating population conservation and creating phantom individuals. This bug directly corrupts parameter estimates across every SEIRS model in the paper. Additionally, SEIRS Model 2's optimization is explicitly reported as unconverged, and the near-zero transmission rate b3 ≈ 0.0024 in Model 1's Omicron wave is accepted without treatment as model misspecification.

---

## Major Issues

### 1. R Compartment Update Missing: Population Conservation Violated in All SEIRS Models

All four SEIRS model implementations in the paper (main model `seirs_varying_k_rho`, plus all three Appendix variants) contain the same critical error. The `rprocess` Csnippet reads:

```c
S -= dN_SE - dN_RS;
E += dN_SE - dN_EI;
I += dN_EI - dN_IR;
R += dN_IR;          // Bug: should be R += dN_IR - dN_RS
H += dN_IR;
```

The S compartment gains `dN_RS` individuals (the R→S flow), but R is never decremented by `dN_RS`. Consequently, `dN_RS` individuals materialize in S from nowhere, and total population N = S+E+I+R increases by `dN_RS` at every time step. With the initialization `R ≈ (1−η)×N` and `mu_RS = 0.005` per week, the phantom inflow to S is approximately `0.000714 × R` per day — at Week 1 with η ≈ 0.71, R ≈ 10 million, yielding roughly 7,000 phantom new susceptibles per week at the outset, growing over time as R accumulates without bound.

This bug causes S to remain artificially inflated throughout the simulation rather than depleting as infections spread, which distorts all transmission rate estimates, the reporting rate estimates, and the epidemiological interpretation of every SEIRS result in the paper. The fix is one line: change `R += dN_IR;` to `R += dN_IR - dN_RS;`. This error appears identically in `blinded.Rmd` (lines 787–792), and in all three appendix model scripts (`results/seirs_const/Global.R`, `results/seirs_varying_k/seirs_varyingk.R`, `results/seirs_global2/seirs_k_rho.R`).

### 2. Near-Zero b3 in SEIRS Model 1 Not Treated as Evidence of Misspecification

The first global search (SEIRS Model 1) yields b3 ≈ 0.0024 — an essentially zero transmission rate during the Omicron wave, which is the *largest* observed epidemic wave in the data. The paper acknowledges this is "actually very small" and "problematic," but the stated response is: "as the underlying model mechanism involves too many states and transmissions, we fail to track the number of people in each state... and conjecture reasonable explanations." No structural revision is attempted.

Per Wheeler et al. (2024), implausible parameter estimates — especially parameters converging to a boundary value — are strong diagnostic signals of model misspecification, not simply numerical curiosities. A transmission rate of zero during the largest observed wave means the SEIRS Model 1 cannot be correctly describing Omicron dynamics; the model is compensating for the R compartment bug (inflated S) by suppressing β. The appropriate response is model revision, not acceptance.

### 3. SEIRS Model 2 Optimization Is Explicitly Reported as Unconverged

For SEIRS Model 2 (seirs_global2), the paper states: "The log-likelihood reaches -1,240 after 200 iterations and **still exhibits an upward trend**." An upward trend in the log-likelihood trace at the end of 200 iterations means the optimization has not converged. Parameter estimates extracted from an unconverged search are unreliable — the optimizer may move significantly with more iterations. Nevertheless, these parameters are presented as the "best model" and used for further profile likelihood computation. The global search improvement to -1,233 does not resolve this concern because each global search job also uses 200 iterations with the same insufficient convergence.

To resolve this, either (a) increase Nmif until the log-likelihood trajectory genuinely plateaus across replicate runs, or (b) acknowledge explicitly that the presented values are preliminary and quantify the potential gap to the true MLE.

### 4. mu_RS Fixed Without Profile or Sensitivity Analysis

The parameter `mu_RS = 0.005` (corresponding to 200 weeks ≈ 4 years of immunity) is fixed throughout all analyses. The paper notes: "we examined significant divergence results and worse local search and global search results when we try to increase mu_RS, so we give up on that and leave for future exploration."

However, mu_RS is the structural parameter that defines the SEIRS model's advantage over SEIR. Fixing it at an arbitrary value — without estimating it, profiling it, or examining sensitivity to plausible alternatives (e.g., 26 weeks as mentioned in the initial parameter rationale) — means the central modeling choice of the paper is unjustified. The "divergence results" when increasing mu_RS likely reflect model misspecification or parameter identifiability issues that warrant investigation, not avoidance. At minimum, a profile likelihood over mu_RS should be computed to determine whether it is identifiable from the data.

### 5. No ESS Diagnostics After Local or Global Search

Effective sample size (ESS) is shown only for the initial parameter guess (the figure labeled "ESS Check and Simulations, Initial Guess"). For the local search and global search results of the main model (SEIRS Model 1), the paper explicitly states: "we don't include the effective sample size check here." For SEIRS Model 2, no ESS check is shown at any stage.

ESS collapse at specific time points in a fitted model indicates that the particle filter is degenerating — the model cannot plausibly generate observations at those times even with optimized parameters. This is a key diagnostic for identifying periods of model-data mismatch. The initial ESS plot already showed sharp collapse during weeks 10–30 (the first wave). Whether this is resolved after optimization is never demonstrated. Per the POMP checklist (Wheeler et al. 2024, §Model diagnostics), ESS must be monitored for fitted parameters, not just initial guesses.

---

## Computational and Diagnostic Assessment

**Convergence:** For SEIRS Model 1, the local search log-likelihood trace shows convergence to approximately -1,250. For Model 2, the trace explicitly has not stabilized at 200 iterations. The global searches use 400–800 starting points each with NP=5000 and Nmif=200, which is a substantial computational effort; however, the per-job convergence issues undermine the global search results for Model 2.

**Particle filter:** NP=5000 particles is appropriate for this 119-observation series. Profile computations use NP=5000 with Nmif=100 (Rho3_pro.R), which is reasonable. Replicated pfilter runs (10 replicates) with `logmeanexp` are used correctly (Error 1.1 avoided).

**Conditional log-likelihoods:** Not shown at any stage. Per-time-step conditional log-likelihoods would help identify whether the poor first-wave fit visible in simulations corresponds to a genuine likelihood problem.

**Profile likelihoods:** Computed for rho1, rho2, rho3, eta, and mu_IR with 443 grid points each — this exceeds the run-level 3 standard of 30 points significantly and provides dense coverage. The SE filter `loglik.se < 1` is permissive (the Wilks 95% threshold is only 1.92 log units), but typical SE values in the CSV are below 0.01, so this filter is not distorting results in practice. The rho2 profile shows messy structure that is acknowledged but not investigated further.

**Computational scale:** Runs conducted on the Greatlakes HPC cluster; job scripts are included (rjob_runner.sbat). Total CPU-hours are not reported.

---

## Reproducibility Assessment

**Code availability:** All analysis scripts are present in the results subdirectory with clear organization.

**Final parameters:** Global search results are archived as CSV files (e.g., `Global_rho_800.csv`, `Global_rho_jump.csv`), allowing parameter-based reproduction. This is good practice.

**Model-code consistency:** The measurement model in code (`dnbinom_mu(reports, k, mean_reports, give_log)`) is consistent with the mathematical specification NegBinom(ρH, ρH + (ρH)²/k). The process model has the R compartment bug described in Major Issue 1, creating a discrepancy between the stated ODE system and the implemented code.

**Package versions:** No `sessionInfo()` or `renv` lockfile is provided. Package versions are not pinned.

**Auxiliary data:** The primary data file `weekly_df.csv` is included. However, `Rho3_pro.R` (and likely other profile scripts) reads from `"SEIR_Global_rho_800.csv"` but only `"Global_rho_800.csv"` exists in the repository. This filename discrepancy makes the profile scripts non-reproducible from the provided code without manual correction.

**HPC reproducibility:** SLURM job scripts (`rjob_runner.sbat`) are included. Worker counts and memory specifications are present in the R scripts (e.g., `plan(multicore, workers = 36)`).

---

## Minor Issues

- **Piecewise interval boundary typo:** All three piecewise function definitions (β, k, ρ) in the main text specify the third interval as "t ∈ [63, 119]" rather than "t ∈ [97, 119]." The code correctly implements weeks 97–119 via `interval = c(61, 35, 23)`. This is a typographical error in the mathematical writeup that should be corrected to avoid confusion.

- **I₀ = 1000 not justified:** The initial infectious count is hardcoded as `I = 1000` in `seir_init` across all models. For Kerala in early February 2020, there were only 3 confirmed cases. An initialization of 1,000 infectious individuals is substantially larger than the documented situation and is not defended in the text. Initial conditions are discussed elsewhere (η is estimated), but I₀ receives no justification.

- **Figure caption/reference mismatch:** The text refers to "the time series plot (Figure 5)" immediately after the chunk labeled `fig4` (ARIMA fitted vs. actual plot). The figure is labeled as Figure 4 in the chunk but described as Figure 5 in the body text.

- **Hard-coded local file path:** A commented-out line reads `#vaccine <- read.csv("/Users/cathy/Desktop/daily-vaccination-in-kerala.csv", ...)`. While inert, this reveals an absolute local path and is a reproducibility anti-pattern.

- **Vaccine data collected but not modeled:** The vaccination data file is included in the data folder and the first phase boundary explicitly marks vaccine rollout. A SEIRS model without a vaccinated compartment cannot distinguish natural immunity waning from vaccine-induced immunity. This is a meaningful structural limitation that deserves acknowledgment beyond the current brief mention.

- **rho3 ≈ 0.09 in SEIRS Model 2 unexplained:** In Model 2, the third-phase reporting rate rho3 ≈ 0.09 is "too small and beyond our expectation" and the paper states "we fail to explain" this. As with b3 in Model 1, an implausible parameter estimate at a boundary-like value suggests model misspecification, not just a difficult-to-explain result. This should at minimum be flagged as a diagnostic signal.

- **No formal comparison between SEIRS model variants:** The paper develops four SEIRS model variants (const, varying_k, varying_k_rho as Model 1, varying_k_rho as Model 2). These are nested or nearly nested models; a likelihood ratio test or AIC comparison table would clarify whether each structural addition is statistically warranted. The paper describes this iterative development qualitatively but provides no formal comparison.

- **rho2 profile not investigated:** The rho2 profile is described as "much more messy" and attributed to computational difficulties. A messy profile can indicate weak identifiability or multimodality of the likelihood surface for rho2. This should be investigated (e.g., more starts, examining correlation with other parameters) rather than dismissed.

- **Conclusion's AIC comparison parameter count inconsistency:** The code sets `seirs_best_model_num = 12`, while the ARIMA(5,1,5) has 11 free parameters (5 AR + 5 MA + 1 variance). This difference of 1 parameter is small relative to the log-likelihood gap (~90 units), so it does not affect the conclusion, but the count is not explained.

- **No discussion of whether SEIRS outperforms SEIR:** The paper motivates SEIRS over SEIR based on biological reasoning, but never formally tests this claim by fitting a SEIR model and comparing log-likelihoods. The simplest SEIRS variant (constant k and ρ) in the Appendix reaches only -1,800, which is well below the SEIR-equivalent benchmark, but a properly fitted SEIR with the same time-varying β structure is not shown.

---

## Recommendation

**Major Revision.**

The paper has genuine strengths: the iterative model-building documentation is informative, the computational effort is appropriate, the profile likelihood coverage is extensive, and the benchmark comparison is a positive methodological choice. However, the R compartment bug (Major Issue 1) is a fundamental error that invalidates all presented SEIRS parameter estimates and biological interpretations. This must be corrected before results can be trusted. The non-convergence of Model 2 (Major Issue 3) and the acceptance of near-zero b3 without misspecification investigation (Major Issue 2) further limit the credibility of the current conclusions. Following correction of the R compartment bug, re-running all SEIRS models is required, and the results should be assessed afresh against the biological interpretability checks and convergence standards described above.

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

- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/seirs_k_rho.R`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Rho3_pro.R`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Global_rho_800.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project04/results/seirs_global2/seirs_k_rho.R`
