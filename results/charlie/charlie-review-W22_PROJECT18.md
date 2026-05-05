# Peer Review: W22 Project 18 — Annual Crude Oil Price Analysis

## Summary

This project analyzes annual crude oil prices from 1980 to 2020 using three model classes: GARCH(1,1), ARMA, and a stochastic volatility POMP model adapted from Breto (2014). The authors take log-differences of prices to obtain approximately stationary returns, then fit each model class in sequence. While the project covers the main course requirements and applies the standard SV-POMP template correctly in many places, it contains several serious methodological flaws: the profile likelihood computation is broken (all 100 profile runs have identical phi, defeating the purpose of profiling), the model comparison conclusion is inverted (the paper claims POMP achieves the lowest AIC when it actually achieves the highest among all fitted models), and the GARCH log-likelihood used for cross-model comparison comes from a different package than the GARCH AIC table, raising normalization concerns. These errors materially undermine the main conclusions.

---

## Major Issues

### 1. Profile likelihood is non-functional — phi is never varied

**Evidence:** The profile likelihood code (Section 5.5) calls `mif2(if1[[1]], start=c(unlist(guesses[i,]), params_test), ...)` with `phi` absent from `rw.sd`, which is correct: the target parameter should not be perturbed. However, inspection of the cached results in `blind_new_cache/html/unnamed-chunk-25_...rdb` shows that all 100 profile runs return `phi = 0.9928931` — identical to `coef(if1[[1]])`. The `guesses` dataframe correctly contains phi ranging from 0.8 to 0.99999 (natural scale), but these values are never applied. The most likely cause is that `start=` was a deprecated argument name in the version of `pomp` used; the initial parameters from `if1[[1]]` were used instead. As a result, what is plotted in Section 5.5 is not a profile likelihood for phi at all — it is 100 likelihood evaluations at a single phi value with varying nuisance parameters. No valid confidence interval for phi can be drawn from this plot.

**Severity:** Major. This is a core inferential output of the project. (Wheeler et al. 2024, §Parameter identifiability; Error 1.2 in 531-weakness-reference.md: computing a likelihood slice instead of a profile.)

**Fix:** Use `params=` instead of `start=` in the `mif2` call, or verify which argument name is recognized by the installed version of `pomp`. Re-run the profile and regenerate the CI.

---

### 2. Profile plot mixes results from two incomparable groups, producing a misleading figure

**Evidence:** The `oilprice_params.csv` file (220 rows total) is read in Section 5.5 to produce the profile plot. Rows 1–120 come from local and global search (phi on natural scale, 0.72–1.00; logLik range −3.24 to −2.22). Rows 121–220 come from the profile run (phi values in −0.38 to 0.006; logLik range 0.028 to 0.047). The profile phi values are not on the natural scale (0,1) — their origin is unclear, but they are inconsistent with the `guesses` design (which correctly covers 0.8 to 0.9999). Because the profile logLik values (≈ 0.04) far exceed the global-search logLik values (≈ −2.22), the Wilks threshold sits at −1.87, meaning all 100 profile points fall above the CI threshold and all 120 local/global points fall below it. The plot thus shows "high-likelihood phi < 0" vs "low-likelihood phi near 1," which is the opposite of the model's actual behavior. The authors' conclusion ("when phi is smaller than 0, stack of points lay above the threshold") is technically a correct reading of this corrupted plot, but the plot itself is meaningless.

**Severity:** Major. The profile CI and its interpretation are entirely invalid.

**Fix:** This error is downstream of Issue 1. Fixing the profile computation will resolve the plot.

---

### 3. Claim that POMP achieves the lowest AIC is incorrect — POMP has the highest AIC

**Evidence:** The conclusion states: "the best AIC is around 16.4... which is the lowest among all models considered." Reconstructing the AIC values from reported and recomputed likelihoods:

| Model | Log-likelihood | Parameters | AIC |
|-------|---------------|-----------|-----|
| ARMA(0,0) | −3.435 | 1 | **10.87** |
| ARMA(0,1) | −3.398 | 2 | 12.80 |
| GARCH(1,1) (fGarch) | −3.331 | 3 | 12.66 |
| POMP (global best) | −2.225 | 6 | 16.45 |

POMP has the **highest** AIC, not the lowest. The paper may have confused "lower AIC is better" with "POMP has the best log-likelihood" — the latter is true (POMP logLik is less negative), but the additional 3–5 parameters compared to ARMA and GARCH more than offset this gain. The ARMA(0,0) model (which the authors deliberately set aside) has the best AIC by a wide margin.

**Severity:** Major. This is the primary comparative conclusion of the paper and it is inverted.

**Fix:** Report AIC values for all models side by side. Note that POMP achieves a better log-likelihood than GARCH or ARMA, but this does not translate to better AIC given its larger parameter count. This is scientifically interesting and should be discussed honestly rather than obscured.

---

### 4. GARCH AIC table uses a different package than the reported GARCH log-likelihood

**Evidence:** The AIC table (displayed as a static image `garch.jpg`) is computed using `garch()` from the `tseries` package. The stated GARCH(1,1) log-likelihood of −3.331448 used for model comparison comes from `garchFit()` in `fGarch`. These two packages use different internal conventions for the log-likelihood. Per Error 2.9 (531-weakness-reference.md), `tseries::garch` is known to report non-standard log-likelihood values. The GARCH AIC values in `garch.jpg` are therefore not directly comparable to the POMP AIC (computed from the particle filter log-likelihood) or to the fGarch log-likelihood used for the baseline comparison. The paper presents these as if they are on a common scale without any acknowledgment of the normalization issue.

**Severity:** Major. Cross-model AIC comparisons are invalid if likelihood normalizations differ.

**Fix:** Use a single package for all GARCH computations, verify that its log-likelihood uses the standard normalization, and explicitly state when normalizations may differ.

---

### 5. No simulation-based model diagnostics

**Evidence:** Section 5.2 applies the particle filter to simulated data (from `sim1.sim` with `params_test`) as a sanity check, but this is not a diagnostic of fit to the real oil price data. Nowhere in the paper are simulations from the fitted model compared to the actual observed log-returns. There is no plot of simulated trajectories versus the data, no examination of reconstructed latent states (H or G), no effective sample size (ESS) trace from the particle filter, and no conditional log-likelihood plot. The diagnostic plots shown are only the convergence traces from `mif2` and pairs plots of parameter estimates.

**Severity:** Major. Without simulation-based diagnostics against real data, there is no evidence that the POMP model adequately captures the structure of crude oil price volatility. (Wheeler et al. 2024, §Model diagnostics, §4.)

**Fix:** Add plots comparing simulated returns from the fitted model to the observed log-returns. Plot ESS across time steps. Plot the reconstructed log-variance H over time.

---

### 6. Section 5.4 pairs plot displays local search results, not global search results

**Evidence:** Section 5.4 is titled "MLE from global search" and discusses global optimization. The code that generates the pairs plot reads: `pairs(~logLik+sigma_nu+mu_h+phi+sigma_eta, data=subset(r.if1, logLik>max(logLik)-30))`, where `r.if1` is the local search result from Section 5.3. The global search result is stored in `r.box`. The diagnostic figure in Section 5.4 therefore shows the local search parameter distribution, not the global search distribution, contradicting the section's narrative. The global search finds a better MLE (−2.225 vs −2.909), so the difference is non-trivial.

**Severity:** Major. The claimed diagnostic for the global search is actually from a different optimization run with a meaningfully worse likelihood.

**Fix:** Replace `r.if1` with `r.box` in the pairs plot call in Section 5.4.

---

## Minor Issues

### 7. COVID-era return is included despite the stated exclusion

**Evidence:** The paper states the analysis focuses on "years prior to 2020 since the economy is strongly impacted by COVID-19." However, the code selects `oil[120:160,]`, which includes the year 2020 price. The log-difference at index 40 of `log_diff_data` corresponds to `log(P_{2020}/P_{2019})`, which captures the 2020 COVID oil price crash. The `Year` column labels this observation as 2019, but the return includes the 2020 price. The stated exclusion is not implemented.

**Fix:** Either exclude 2020 from the data (use `oil[120:159,]`) and acknowledge the resulting 39 observations, or acknowledge that the 2019–2020 return is included and discuss its influence.

---

### 8. Text description of the global search box does not match the code

**Evidence:** Section 5.4 lists the global search box as "sigma_nu in (0.005, 0.020)" in the displayed equations. The code (`oilprice_box`) sets `sigma_nu = c(0.005, 0.015)`. The upper bound differs between text and code by a factor of 4/3. This is a reproducibility issue: the stated analysis does not match what was run.

**Fix:** Synchronize the text and the code box bounds. State which was actually used.

---

### 9. The GARCH AIC table is replaced by a static image, breaking reproducibility

**Evidence:** The code block that computes `aic_table` (the GARCH AIC table) produces results that are silently discarded (the `kable(aic_table)` line is commented out). Instead, the rendered document displays `![](garch.jpg)`, a static image that cannot be verified as corresponding to the computed table values. If the image was produced in a different run (with different parameters, data, or library versions), the reader cannot detect the discrepancy.

**Fix:** Uncomment the `kable(aic_table, digits=2)` line and remove the static image, or at minimum explain why the image rather than the live-rendered table is used.

---

### 10. Nreps_local at run_level=3 is 20, not the course standard of 40

**Evidence:** The code sets `oilprice_Nreps_local <- switch(run_level, 10, 20, 20)`, giving 20 local search starts at run_level=3. The course convention (531-conventions.md, Table: run_level parameters) specifies Nreps_local = 40 at run_level=3. With only 20 starts, coverage of the local parameter landscape is reduced.

**Fix:** Increase `Nreps_local` to 40 for a final run-level=3 analysis, or justify the reduced value.

---

### 11. ARMA model selection bypasses the AIC-optimal model without adequate justification

**Evidence:** The AIC table clearly shows ARMA(0,0) has the lowest AIC (10.87). The authors acknowledge this but choose ARMA(0,1) instead, arguing the white-noise result may be due to limited data. However, this reasoning is circular: if the data support only a white-noise model, that is the correct model for this dataset. Selecting a higher-order model because the optimal one is "uninformative" is a form of model selection bias. The paper could instead treat ARMA(0,0) as the baseline and interpret the white-noise result as a finding (annual returns are not predictably autocorrelated from past annual returns).

**Fix:** Either use ARMA(0,0) as the reference model and discuss what this means, or provide a principled argument (e.g., out-of-sample validation) for preferring ARMA(0,1).

---

### 12. GARCH residuals are heavy-tailed but no alternative error distribution is considered

**Evidence:** The QQ plot for GARCH(1,1) residuals (Section 3.2) shows heavy tails. The authors note this but do not consider a GARCH model with Student-t errors, which is the standard response to heavy-tailed GARCH residuals and is supported by `fGarch`. This limitation is acknowledged only implicitly.

**Fix:** Fit GARCH(1,1) with Student-t errors and compare its AIC to the Gaussian GARCH.

---

### 13. Filtering on simulated data (Section 5.2) is not interpreted

**Evidence:** Section 5.2 runs the particle filter on simulated data (`sim1.filt`) and obtains a log-likelihood of −65.07. This value is reported but never interpreted. The simulated data are generated from the test parameters (`params_test`), which may differ substantially from the MLE. The logLik of −65.07 for simulated data versus −2.22 for real data (with 40 observations each) suggests a very large discrepancy, likely because `params_test` does not match the MLE. This section does not serve a clear diagnostic purpose as presented.

**Fix:** Either remove this section or explain what it demonstrates: e.g., that the particle filter correctly evaluates the likelihood for known data, or as a sanity check that the filter runs without error before applying it to real data.

---

### 14. No ARMA or statistical benchmark comparison for the POMP model

**Evidence:** The paper fits GARCH, ARMA, and POMP but does not formally compare the POMP log-likelihood to a non-mechanistic benchmark in the model diagnostics section. The comparison in the conclusion uses inconsistent normalizations (Issue 4). A rigorous comparison using the same log-likelihood scale (e.g., showing POMP logLik = −2.225 vs ARMA(0,0) logLik = −3.435, noting that POMP uses more parameters) would strengthen the analysis. (Wheeler et al. 2024, §Benchmark comparison; Error 1.6 in 531-weakness-reference.md.)

**Fix:** Add a table comparing all models on log-likelihood and AIC using a consistent normalization, with explicit acknowledgment that ARMA and POMP likelihoods are both evaluated at the observed log-returns and are directly comparable.

---

### 15. Small sample size (40 observations) is not discussed as a limitation for the POMP model

**Evidence:** The POMP model has 6 estimated parameters (sigma_nu, mu_h, phi, sigma_eta, G_0, H_0) fit to 40 annual observations. No discussion of whether the data are sufficient to identify all 6 parameters is provided. The profile likelihood, which would have provided this information, is broken (Issue 1). The convergence diagnostics in Section 5.3 note that "some parameters could not converge very well," which may partly reflect this identifiability challenge.

**Fix:** Discuss the ratio of parameters to observations. Note that the broken profile prevents a proper identifiability assessment and that this is a limitation.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/oilprice_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/pf1-3.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/mif1-3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/profile_phi-3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/crude-oil-prices.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/blind_new_cache/html/unnamed-chunk-20_3176d86e752998e3f42a30d6afa4e368.rdb`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/blind_new_cache/html/unnamed-chunk-23_34fd25e9ec262b9749d549ccda043e79.rdb`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/blind_new_cache/html/unnamed-chunk-25_994a611f7656ee6221c75eb11cb83163.rdb`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/blind_new_cache/html/unnamed-chunk-26_d6eb672ffb99b03269edb2d25a936c78.rdb`
