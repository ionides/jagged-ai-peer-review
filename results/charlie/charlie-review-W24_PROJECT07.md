# Peer Review: W24 Project 07
## "Time Series Analysis of Apple Inc. (AAPL) Stock Price"

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) via pomp R package; GARCH via tseries and rugarch |
| **R packages used** | quantmod, pomp, doParallel, foreach, doRNG, tseries, rugarch, forecast |
| **Code publicly available** | Git repository (no external archive/DOI) |
| **Data publicly available** | Fetched live from Yahoo Finance via quantmod |
| **Benchmark comparison included** | No — ARMA/GARCH and POMP likelihoods are never compared quantitatively |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2 used; logmeanexp applied correctly to pfilter replicates |
| 2 | Benchmark comparison | ✗ | POMP model never compared to ARMA or GARCH likelihood |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported but rendered incomparable by data mismatch (see Issue 1) |
| 4 | Model diagnostics | ~ | ESS and conditional log-likelihoods shown; no simulation-based validation |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods; no confidence intervals; sigma_eta ranges 0–150+ |
| 6 | Computational adequacy | ~ | 100 global replicates at Np=1000 Nmif=100; loglik shows reasonable convergence for global search |
| 7 | Forecast methodology | N/A | No forecasting from POMP model attempted |
| 8 | Model variations and nested comparisons | ✗ | No nested model comparisons |
| 9 | Stochasticity | ✓ | Stochastic leverage model with Gaussian noise; normal measurement model |
| 10 | Reproducibility and extendability | ~ | Code present; some plots as .rda archives; no final MLE parameter file |
| 11 | Corroboration with scientific knowledge | ✗ | sigma_nu near zero and sigma_eta near zero at MLE not interpreted scientifically |
| 12 | Measurement model specification | ✓ | Normal observation model is consistent with code and text |
| 13 | Initial conditions | ~ | G_0, H_0 included as estimated parameters; initialization in pfilter is on simulated data (see Issue 1) |

---

## Summary

This project applies ARMA, GARCH, and a stochastic leverage POMP model (following Bretó 2014) to daily log returns of Apple Inc. stock from April 2020 to April 2024. The project demonstrates familiarity with the mechanics of iterated filtering and includes both local and global IF2 searches. However, the analysis contains a critical structural error that invalidates the initial benchmark comparison, and the POMP section lacks profile likelihoods, simulation-based diagnostics, and any quantitative comparison to the ARMA/GARCH models. The conclusion that "GARCH proved to be the most effective" is asserted without supporting evidence.

**Strengths:** The POMP implementation follows the Bretó (2014) leverage model correctly; logmeanexp is used properly for likelihood aggregation; global and local searches are both presented; filter diagnostics (ESS and conditional log-likelihoods) are included.

**Weaknesses:** (1) The initial pfilter benchmark is computed on simulated data rather than the real AAPL data, making the claimed comparison meaningless; (2) GARCH model selection likely picks the worst rather than best model due to a minimum/maximum error; (3) No profile likelihoods or confidence intervals are computed; (4) There is no quantitative comparison of the three model families; (5) Convergence problems in the local search are acknowledged but not resolved.

---

## Major Issues

### 1. Initial pfilter benchmark computed on simulated data, not on real AAPL returns

The pfilter likelihood of −1501.19 reported as the "initial benchmark" (line 484) is computed on `sim1.filt`, which is a pomp object containing data simulated from the model under `params_test`, not the observed AAPL returns in `AAPL_filter`. The code constructs `sim1.sim = simulate(sim1.sim, seed=531, params=params_test)` and then applies `pfilter(sim1.filt, Np=AAPL_Np)`. In contrast, the subsequent mif2 local and global searches both target `AAPL_filter` (lines 505 and 566), which produce log-likelihoods around 2650. The authors treat −1501.19 as a baseline for the real-data optimization ("much higher than the initial benchmark"), but these quantities are on completely different datasets. The true log-likelihood of the test parameters on the real data is not reported anywhere. This error corrupts the stated interpretation of the optimization progress.

**Fix:** Replace `pfilter(sim1.filt, ...)` with `pfilter(AAPL_filter, params=params_test, ...)` to compute an honest baseline on the actual observed data.

---

### 2. Factual discrepancy: description claims "20 replicates with 2000 particles," code uses 10 and 1000

The text at line 484 states "We replicated the filtering process 20 times with 2000 particles in each iteration." However, the code sets `AAPL_Nreps_eval = switch(run_level, 4, 10, 10)` (10 replicates at run_level=3) and `AAPL_Np = switch(run_level, 100, 1e3, 1e3)` (1000 particles at run_level=3). The description is off by a factor of two in both quantities. While 10 replicates at 1000 particles is acceptable, the stated description is factually wrong and undermines confidence in the analysis.

**Fix:** Correct the prose to match the code: 10 replicates with 1000 particles each.

---

### 3. GARCH model selection selects the worst-fitting model

In the basic GARCH grid search, the code populates `garch_table` with values from `tseries:::logLik.garch(fit_garch)` and then selects the model with `min(garch_table)`. If these are log-likelihoods (which are negative for typical financial data), minimizing selects the most negative value — the worst-fitting model, not the best. The tseries package is known to report non-standard likelihood values (Error 2.9, 531-weakness-reference), and directly using `min` without verifying the convention is a reliability risk. As a result, the selected GARCH(1,4) model may be the worst-performing specification in the grid, undermining the entire GARCH section.

**Fix:** Verify the sign convention of `tseries:::logLik.garch`. If it returns standard log-likelihoods, replace `min` with `max`. Alternatively, use AIC (via rugarch or manual computation) for consistent model selection.

---

### 4. No profile likelihoods or confidence intervals for any POMP parameter

Neither local nor global searches are followed by any profile likelihood computation. The global search pairwise plot shows that sigma_eta ranges from near 0 to over 150 and sigma_nu concentrates near zero without any confidence bounds reported. Without profile likelihoods, it is impossible to determine whether any parameter is identifiable from the data. The apparent near-zero MLE for both sigma_nu and sigma_eta (leverage and volatility of volatility) suggests the fitted model may be collapsing toward a deterministic structure, which would be a scientifically important finding — but it is never tested or discussed. This violates POMP checklist item #5 and Error 1.9 from the student weakness reference.

**Fix:** Compute profile likelihoods (using mif2 with the target parameter fixed across a grid, as taught in Chapter 16) for at least sigma_nu, phi, and mu_h. Report 95% confidence intervals using the Wilks threshold.

---

### 5. No quantitative comparison between ARMA, GARCH, and POMP model likelihoods

The conclusion states "the GARCH model proved to be the most effective in forecasting volatility" but no numerical comparison between the log-likelihoods of the three model families is presented. The ARMA log-likelihood can be extracted from the fitted object; the GARCH log-likelihood is in the infocriteria output; the POMP log-likelihood is reported from the global search. Comparing these on the same data and scale would provide the quantitative support needed for the conclusion. Without this, the ranking of models is unsubstantiated (Error 1.6 from weakness reference; POMP checklist item #2). Note that per 531-conventions.md, likelihoods from different model classes (ARIMA, GARCH, POMP) evaluated on the same data are directly comparable.

**Fix:** Collect the best log-likelihood from each model class — ARMA(1,1), best GARCH, and the global POMP search — in a single comparison table. Discuss whether the POMP model adds value beyond the simpler alternatives.

---

### 6. Convergence failure in local search acknowledged but not addressed

The text states "We can hardly say the log likelihood converges from the MIF2 convergence diagnostics plot" for the local search, and the local_d2.png trace plot confirms that sigma_eta is increasing and H_0 is drifting throughout 100 iterations with no sign of stabilization. Despite this acknowledged convergence failure, the project proceeds directly to a global search without any structural revision to the model or increase in computational resources. Error 1.8 from the weakness reference applies: missing convergence evidence for iterated filtering is a major issue. The global search log-likelihood trace (global_d2.png) shows better convergence in the loglik panel but sigma_eta still shows wide spread across runs, reaching values above 200.

**Fix:** Either (a) increase Nmif sufficiently until the loglik trace and key parameter traces stabilize, or (b) revisit model structure if convergence cannot be achieved (e.g., add constraints, reparametrize). At minimum, the convergence failure must be discussed as a limitation rather than passed over.

---

### 7. sigma_nu near zero and sigma_eta implausibly large — scientific interpretation absent

The global search (global.png pairwise plot) reveals that sigma_eta, which controls the volatility of volatility, attains values from near 0 to above 150, and is labeled as "around 0" at the MLE. Simultaneously, sigma_nu (which drives the leverage random walk G_n) concentrates near zero. Together, these suggest that the leverage effect R_n ≈ 0 at the MLE, which would reduce the model to a simpler SV model with no leverage. This is a scientifically important finding — it suggests leverage may not be detectable in the AAPL data over this period — but it is never interpreted. Implausible parameter estimates can indicate model misspecification (POMP checklist item #11), and zero estimates are a diagnostic flag per Wheeler et al. (2024).

**Fix:** Discuss the biological and financial interpretation of sigma_nu ≈ 0 and sigma_eta ≈ 0. Test whether a reduced model without leverage (sigma_nu fixed to 0) achieves a comparable log-likelihood, and compare via likelihood ratio test or AIC.

---

## Minor Issues

- **No simulation-based model validation**: No forward simulations from the fitted POMP model are compared to the observed log returns. The filter diagnostics show ESS occasionally dropping to single digits (global_d1.png around time 400), suggesting periods of model-data mismatch, but this is not investigated through simulated trajectory overlays (POMP checklist item #4).

- **decompose() applied to daily log returns without justification**: The `decompose(data_lr)` call (line 46) applies additive seasonal decomposition with frequency=253 (trading days per year) to log returns. Financial log returns have no physical seasonality at this frequency; the seasonal component found by `decompose` is artifactual. The result is plotted but never discussed or used. This component should either be justified or removed.

- **Run_level=3 set but uses run_level=2 parameter values**: The switch statement at lines 466–470 sets `AAPL_Np = 1000` and `AAPL_Nmif = 100` when run_level=3, which match the course run_level=2 defaults (Np=1000, Nmif=100). The course standard for run_level=3 is Np=5000, Nmif=200. While the conventions file notes that context-dependent values are acceptable, the mislabeling creates confusion about the computational effort invested.

- **ARIMA section title but ARMA model fitted**: The section is labeled "ARIMA Model" throughout, but the model fitted is ARMA (with d=0, no differencing). Since the data are already stationary log returns, an ARMA is appropriate, but the section title is inconsistent with the fitted model.

- **References given as bare URLs rather than bibliographic citations**: References [1], [2], [3], [4], and [6] are raw URLs with no author, title, or publication date. Reference [5] (Bretó 2014) provides partial information but no volume/page numbers. Academic standards require full citations.

- **Acknowledgment of AI tool for LaTeX writing**: Reference [2] cites "CatGPT" (likely a pseudonym for ChatGPT) for writing LaTeX. The appropriateness of this use should be clarified according to course policy, and any AI-generated mathematical content should be verified carefully.

- **Grid search over ARMA(p,q) excludes p=0 or q=0**: The grid search at lines 112–128 considers only p in {1,2,3,4} and q in {1,2,3,4}, excluding pure AR or pure MA models. The best AIC from this restricted grid could be inferior to ARMA(1,0) or ARMA(0,1).

- **AIC comparison within the basic GARCH grid is omitted**: For the basic GARCH table, log-likelihoods are compared without a penalty for model complexity. Models with more parameters will generally have higher (better) log-likelihoods regardless of whether the extra parameters are justified. AIC would be more appropriate.

---

## Computational and Diagnostic Assessment

**Convergence:** The global search log-likelihood trace (global_d2.png) converges rapidly in the first 10–15 iterations and stabilizes near 2650, which is acceptable for a loglik panel. The local search (local_d2.png) shows loglik approaching a plateau but sigma_eta and H_0 are still drifting at iteration 100. More iterations or a structural revision would be needed to declare convergence for the local search.

**Particle filter:** ESS is monitored and plotted. Global filter diagnostics (global_d1.png) show ESS frequently dropping below 100 and occasionally to single digits at certain time points (notably around time 400 and time 800), suggesting model-data tension at specific periods. These drops are not discussed.

**Conditional log-likelihoods:** Plotted but not analyzed. The conditional log-likelihood panel in global_d1.png shows spikes downward at the same time points as the ESS drops, reinforcing that specific market events cause poor model fit. No corrective action is taken.

**Profile likelihoods:** Not computed for any parameter. This is the most significant computational omission.

**Computational scale:** Global search uses 100 replicates at Np=1000, Nmif=100. No CPU time or computational cost is reported for the mif2 runs (only for the initial pfilter: 1.61 seconds). Total computational effort is unquantified.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file with external images loaded from pre-saved PNG files. The `.rda` files (mif1-3_2.rda, pf1-3.rda) cache results. This is standard course practice.

**Final parameters:** No standalone CSV or RDS file of final MLE parameter estimates is provided. Readers cannot evaluate results without re-running mif2 from the archived .rda outputs.

**Model-code consistency:** The mathematical model (equations in Section 4.1) matches the C snippets (`rproc1`, `rproc.filt`) — tanh(G) is used for R_n and the variance formula for omega is correctly implemented.

**Package versions:** No sessionInfo() or renv lockfile is provided. The pomp API has changed across versions, so results may not reproduce on current CRAN releases.

**Auxiliary data:** Data is fetched live from Yahoo Finance at runtime. This is a reproducibility risk: the data could change if Yahoo Finance revises historical prices (split adjustments, etc.), and the exact dataset used is not archived.

---

## Recommendation

**Major Revision.** The project demonstrates reasonable familiarity with the POMP modeling workflow and includes appropriate filter diagnostics. However, three issues require resolution before the analysis can be considered valid: (1) the initial benchmark must be recomputed on the real data rather than simulated data; (2) the GARCH model selection criterion must be corrected; and (3) profile likelihoods must be computed for at least the key POMP parameters to support any inferential claims. The lack of a quantitative cross-model comparison also undermines the stated conclusion. These are addressable with targeted revisions to the code and analysis sections.

---

## Files Consulted

**Skill files — guided-pomp-review:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`

**Skill files — 531_references:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project07/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project07/global.png`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project07/global_d1.png`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project07/global_d2.png`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project07/local.png`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project07/local_d1.png`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project07/local_d2.png`
