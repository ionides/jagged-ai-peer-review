# Review: W24 Project 07

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (iterated filtering via `mif2`), particle filter (`pfilter`) |
| **R packages used** | `pomp`, `quantmod`, `doParallel`, `foreach`, `doRNG`, `rugarch`, `tseries`, `forecast` |
| **Code publicly available** | Partial — code is embedded in the Rmd, but expensive computations are cached in `.rda` files |
| **Data publicly available** | Yes — retrieved live from Yahoo Finance via `quantmod` |
| **Benchmark comparison included** | Partial — ARMA and GARCH models are fitted but never formally compared to POMP using log-likelihood on the same scale |

---

## POMP Checklist Scorecard

*checkmark = satisfies practice, ~ = partially satisfies, x = does not satisfy, N/A = not applicable*

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 used correctly but particle count of 1000 is low and convergence is incomplete |
| 2 | Benchmark comparison | x | ARMA and GARCH fitted but log-likelihoods never compared on a common scale to the POMP model |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported for POMP but not stated for ARMA/GARCH; no AIC table |
| 4 | Model diagnostics | ~ | ESS and conditional log-likelihood plots shown; no forward-simulation vs. filtering-distribution distinction |
| 5 | Parameter identifiability and uncertainty | x | No profile likelihoods; sigma_nu and phi convergence problems acknowledged but not resolved |
| 6 | Computational adequacy | x | Only 100 IF2 iterations, 1000 particles, 20 local / 100 global starts; MIF2 convergence traces show non-convergence |
| 7 | Forecast methodology | x | No forecasts generated from POMP model; ARMA forecast ignores volatility clustering |
| 8 | Model variations and nested comparisons | x | No nested model comparisons; GARCH models compared by AIC but not against POMP |
| 9 | Stochasticity | checkmark | Model includes process noise (omega, nu) and measurement noise; appropriate for financial data |
| 10 | Reproducibility and extendability | ~ | Archived `.rda` files provided; global search results file `AAPL_global.csv` referenced but not included |
| 11 | Corroboration with scientific knowledge | ~ | phi near 1 (high persistence) plausible; sigma_eta values in global search appear very large (0-30 range) without discussion |
| 12 | Measurement model specification | ~ | Gaussian measurement model may underfit heavy tails; not compared to t-distribution alternative in POMP |
| 13 | Initial conditions | ~ | G_0 and H_0 estimated but sensitivity analysis absent |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

This project analyzes Apple Inc. (AAPL) daily log returns from April 2020 to April 2024 using three progressively complex model classes: ARIMA, GARCH variants, and a stochastic leverage POMP model based on the Breto (2014) formulation. The POMP model treats leverage as a latent Gaussian random walk and estimates parameters via IF2. While the project demonstrates familiarity with the pomp workflow and motivates the leverage model appropriately, it falls short on several critical dimensions: the three model families are never compared on a common quantitative goodness-of-fit scale, the IF2 optimization shows clear non-convergence for key parameters (notably phi and sigma_eta), profile likelihoods are entirely absent, and there is no evaluation of whether the POMP model outperforms the simpler GARCH benchmarks that are already fitted in the paper.

**Strengths:**
- Correctly implements the Breto (2014) stochastic leverage model in pomp, including the parameter transformation and the covariate-table trick for the filtering vs. simulation objects
- Runs both local and global IF2 searches and reports ESS and conditional log-likelihood diagnostic plots
- Explores three GARCH variants (basic, asymmetric apARCH, t-distribution) with AIC-based model selection within each family

**Weaknesses:**
- No unified quantitative comparison across ARMA, GARCH, and POMP; the paper's stated goal of assessing performance comparatively is not met
- IF2 convergence diagnostics plainly show non-convergence for phi and sigma_eta yet no remediation is attempted
- Profile likelihoods are entirely absent; the identifiability of sigma_nu is explicitly questioned but not formally investigated
- The GARCH model selection chooses the minimum of the log-likelihood table (erroneous direction) when using `tseries::garch`
- Global search parameter box for sigma_eta (0.5–1) is inconsistent with results showing sigma_eta ranging 0–30, suggesting the global search departed far outside the specified box

---

## Major Issues

### 1. No Unified Quantitative Comparison Across Model Families

The central stated goal is to "assess [model] performances at last" (Introduction), but the Conclusion section compares models only in vague qualitative terms ("GARCH model proved to be the most effective"). Log-likelihoods from ARMA and GARCH models are never reported alongside the POMP log-likelihood of approximately 2655. Without a unified comparison — e.g., a table reporting log-likelihood (and ideally AIC, accounting for parameter counts) for ARMA(1,1), GARCH(1,1)-t, and the POMP leverage model — it is impossible to determine whether the POMP model provides meaningful improvement. Wheeler et al. (2024) emphasize that "visual comparisons alone are only a weak and informal measure of goodness-of-fit" and that mechanistic models must be compared against benchmarks quantitatively. The ARMA and GARCH models are already fitted in this paper; reporting their likelihoods on the same observation scale as the POMP model requires only a few lines of code.

**Fix:** Add a summary table reporting log-likelihood and AIC for ARMA(1,1), the best GARCH(1,1)-t, and the POMP leverage model. Compute the ARMA/GARCH likelihoods using the same observation sequence (mean-centered log returns) as the POMP model.

### 2. IF2 Non-Convergence for Key Parameters — Not Addressed

The MIF2 convergence diagnostics (local_d2.png, global_d2.png) show clear non-convergence: phi traces in the global search do not stabilize, and sigma_eta values fan out across an enormous range (0–30) rather than converging. The text acknowledges that "phi doesn't show convergence in our diagnostics (which is weakly identified)" but takes no corrective action. Simply citing non-convergence without attempting remedies — e.g., increasing Nmif, widening cooling schedule, tightening the random-walk SD on problematic parameters, or fixing phi at interpretable values — does not constitute adequate analysis. Wheeler et al. (2024) note that insufficient computational effort can make a good model appear to perform poorly, and that increasing effort substantially changed inferred log-likelihoods. With only 100 IF2 iterations and 1000 particles, the current settings are likely too conservative for a 1000-observation dataset with six free parameters.

**Fix:** Increase Nmif (e.g., to 200–300) and Np (e.g., to 2000–5000) and re-examine convergence. If phi remains weakly identified, formally assess it via a profile likelihood. Report the total CPU-hours used.

### 3. Absence of Profile Likelihoods — Parameter Identifiability Unresolved

No profile likelihoods are computed for any parameter. The text itself acknowledges uncertainty about whether sigma_nu is identifiable ("this local search did not show us much evidence for the hypothesis that sigma_nu > 0"), but this is precisely the situation requiring a profile likelihood: fix sigma_nu at a grid of values, optimize over all other parameters, and plot the resulting log-likelihood to determine whether sigma_nu = 0 is within the 95% confidence region. Without profiles, there is no formal evidence that any parameter is identified from these data. Wheeler et al. (2024, checklist item 5) treat profile likelihoods as a required practice: "Profile likelihoods should be computed to assess whether parameters are identifiable from the data."

**Fix:** Compute profile likelihoods for at least sigma_nu and phi using `foreach` over a grid with `mif2` re-optimization at each grid point. Report 95% confidence intervals via MCAP.

### 4. Erroneous Model Selection in Basic GARCH Section

The code for basic GARCH parameter selection uses `tseries::garch` and fills `garch_table` with log-likelihood values. It then selects the parameters with the **minimum** log-likelihood (`which(garch_table == min_value)`), but higher log-likelihoods are better fits. This is the opposite of correct model selection. If the intent is to minimize AIC (= -2*logLik + 2k), the sign convention is wrong; if the intent is to maximize log-likelihood, the `min` function should be `max`. The chosen model (p=1, q=4) should be verified. This error may propagate into the GARCH baseline used for comparison.

**Fix:** Replace `min(garch_table)` with `max(garch_table)` and re-run the basic GARCH analysis. Verify whether the conclusion about the best GARCH order changes.

### 5. Global Search Box Inconsistency for sigma_eta

The global search specifies `sigma_eta = c(0.5, 1)` in `AAPL_box` (line 546), but the resulting pairwise scatter plot (global.png) shows sigma_eta values ranging from 0 to approximately 30. This is physically impossible if the search is initialized uniformly within [0.5, 1] and IF2 perturbations are of magnitude 0.02 on the log scale — the optimizer cannot reach sigma_eta = 30 from a starting point in [0.5, 1] in 100 iterations. This suggests either (a) the archived `.rda` files do not correspond to the displayed code, (b) the global search code was edited after the results were generated, or (c) sigma_eta values shown are on the log scale and the axis label is misleading. This discrepancy undermines reproducibility and the credibility of the reported results.

**Fix:** Clarify whether sigma_eta in the plot is on the original or log scale. Ensure the code shown in the document matches the `.rda` files used for the figures. If the box was changed, disclose this.

### 6. POMP Model Uses Only Gaussian Measurement Noise Despite Heavy Tails

The dmeasure is `dnorm(y, 0, exp(H/2), give_log)` — a Gaussian measurement model. The GARCH analysis earlier in the paper explicitly documents that the Gaussian GARCH residuals have heavy tails (normal Q-Q plots show many outliers on both sides) and that a t-distribution improves fit. Despite this, the POMP model retains a Gaussian observation distribution with no justification. For financial return data, a t-distributed or skew-t measurement model would be more appropriate and is consistent with the paper's own GARCH findings. Wheeler et al. (2024, checklist item 12) require that the measurement model be carefully specified and justified.

**Fix:** Fit a version of the POMP model with a t-distributed measurement error (using `dt(y/exp(H/2), df=nu, log=TRUE) - log(exp(H/2))`) and compare log-likelihoods to the Gaussian version. The degrees-of-freedom parameter nu can be estimated or fixed at a value suggested by the GARCH-t fit.

### 7. Decomposition of Non-Seasonal Data Is Methodologically Inappropriate

The EDA section applies `decompose(data_lr)` to the log return series. The `decompose` function assumes the series has a deterministic seasonal component. Financial log returns are not expected to have deterministic seasonality: daily returns on a stock exchange occur on trading days only, and the frequency of 253 (trading days per year) does not imply annual seasonality is present. The subsequent ACF analysis correctly concludes no seasonality is observed, but the decomposition plot was still produced and presented without noting this conflict. Using `decompose` on such a series is misleading and produces a seasonal component that is an artifact of the method, not the data.

**Fix:** Remove the `decompose` call from the EDA. If seasonal patterns are of genuine interest, use spectral analysis or STL decomposition with appropriate justification.

---

## Computational and Diagnostic Assessment

**Convergence:** The MIF2 convergence traces (local_d2.png, global_d2.png) show that log-likelihood increases during iterations but that key parameters — particularly phi and sigma_eta in the global search — do not stabilize. Multiple chains in global_d2.png show phi values drifting across the full [0.85, 0.99] range at iteration 100. This is not convergence. The paper acknowledges this but does not remediate it.

**Particle filter:** ESS is monitored (local_d1.png, global_d1.png) and shows frequent collapses to low values, indicating model-data tension. The particle count of 1000 is marginal for a 1000-step time series with repeated ESS collapses; this may be contributing to noisy likelihood estimates. The initial benchmark uses `AAPL_Nreps_eval = 10` replicates with 1000 particles; the reported log-likelihood of -1501.19 (from sim1.filt) is not directly comparable to the later estimate of ~2655 (from AAPL_filter) because they operate on different pomp objects.

**Conditional log-likelihoods:** Conditional log-likelihood plots are provided as part of the filter diagnostics plots. Persistent low-ESS periods coincide with periods of high volatility in the data, suggesting the model has difficulty during volatility spikes.

**Profile likelihoods:** Not computed. See Major Issue 3.

**Computational scale:** The paper does not report total CPU-hours. The Makefile is present in the folder but not referenced in the document. Run levels suggest moderate computation but are insufficient for a dataset of this length.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file. The expensive computations (local and global MIF2 searches) are cached using `stew()` into `.rda` files (`pf1-3.rda`, `mif1-3_2.rda`) which are provided in the project folder. However, `box_eval-3.rda` (the global search results) is **not** included in the project folder, meaning the global search figures cannot be reproduced from the provided files.

**Final parameters:** Final MLE parameter vectors are not archived as a standalone CSV or RDS file. The text mentions `AAPL_params2.csv` and `AAPL_global.csv` but neither file is present in the project folder. Readers cannot evaluate results without re-running the optimization.

**Model-code consistency:** The Rmd local search chunk (lines 501-521) references `write.table(local_results, file="AAPL_params2.csv", ...)` but the object `local_results` is never defined in the code — only `r.if1` is created. This is a bug that would cause the code to fail if run. Similarly, the global search chunk does not write `r.box` to disk correctly in the provided form.

**Package versions:** No `sessionInfo()` output is provided and no `renv` lockfile is present. The `pomp` version used is unknown, which is a reproducibility risk given API changes across versions.

**Auxiliary data:** Data is fetched live from Yahoo Finance at runtime using `getSymbols`. While this makes the data source transparent, results will differ if Yahoo Finance revises historical prices (which happens occasionally for corporate actions). The actual data used is not archived.

**HPC reproducibility:** The code references `SLURM_NTASKS_PER_NODE`, indicating cluster usage, but no SLURM job scripts are provided. It is unclear whether computations were run locally or on a cluster.

---

## Minor Issues

- The Introduction states "We will mainly use ARIMA, GARCH and POMP to model the stock prices" but the paper models log returns throughout, not prices. This discrepancy is never reconciled.

- Reference [2] cites "CatGPT" (presumably ChatGPT/Claude) for LaTeX generation. This is an unusual citation; AI-assisted writing should be disclosed in the methods, not cited as a reference with a URL.

- The ARIMA model selection grid searches only p, q in {1,2,3,4} — excluding ARMA(0,0) (i.e., white noise), which is a natural baseline for financial returns. Including p=0 or q=0 would allow the AIC to confirm whether any AR/MA structure is warranted.

- The text refers to "2000 particles" in the Local Search section ("20 local filtering objects, each with 2000 particles") but the code specifies `AAPL_Np = switch(run_level, 100, 1e3, 1e3)`, which gives 1000 particles at run_level=3. This is a direct contradiction.

- The initial benchmark log-likelihood of -1501.19 is computed on `sim1.filt` (which uses simulated data from the test parameters), not on the actual AAPL data. The comparison to the local/global search likelihoods of ~2650 is therefore meaningless — these are different datasets.

- The `run_level` variable is set to 3 in the filter section but the local and global search chunks use `eval=FALSE`, making it ambiguous which settings were actually used to produce the saved `.rda` files.

- `AAPL_Nreps_global = switch(run_level, 10, 20, 100)` gives 100 repetitions at run_level=3, but the global search text states "100 repeated iterations." It should be clarified that this is 100 independent starting points, not iterations.

- The text in the Conclusion states "some of the parameters do not display convergence, we can learn from [6] that this reflects the uncertainty about the parameter given the data." Reference [6] is a homework solution; the claim about parameter non-convergence reflecting uncertainty is an over-simplification that obscures a genuine computational problem.

- The pairwise plot for global search (global.png) includes `G_0` and `H_0` but these are absent from the local search pairwise plot (local.png). This inconsistency makes cross-search comparisons harder.

- Figure axis labels in global.png are very small and the scatter points overlap substantially, making it difficult to read the parameter ranges. Using `ggpairs` or increasing figure dimensions would improve readability.

---

## Recommendation

**Major Revision.**

The paper applies a reasonable model framework (Breto 2014 stochastic leverage) to an interesting financial dataset and demonstrates basic familiarity with the pomp workflow. However, it fails to deliver on its stated goal of comparing model performance: no unified quantitative comparison across ARMA, GARCH, and POMP is ever presented. The IF2 optimization shows clear non-convergence for key parameters (phi, sigma_eta) with no remediation. Profile likelihoods — the standard tool for assessing parameter identifiability — are entirely absent despite the paper explicitly noting identifiability concerns. A bug in the GARCH model selection (minimizing rather than maximizing log-likelihood) casts doubt on the GARCH baseline. Archived result files referenced in the code are missing from the supplement.

Before acceptance, the authors must: (1) produce a unified log-likelihood/AIC comparison table across all model families; (2) increase computational effort and demonstrate convergence, or provide formal evidence via profile likelihoods that problematic parameters are weakly identified; (3) fix the GARCH model selection direction error; (4) archive all intermediate result files (`AAPL_global.csv`, `box_eval-3.rda`) and a `sessionInfo()` output; and (5) resolve the contradiction between stated particle counts and code.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/local.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/local_d1.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/local_d2.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/global.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/global_d1.png`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project07/global_d2.png`
