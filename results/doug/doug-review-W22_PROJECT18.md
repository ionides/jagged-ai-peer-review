# Peer Review: W22 Project 18 — Crude Oil Price Volatility Analysis

**Reviewer:** Doug  
**Semester:** Winter 2022  
**Project:** 18 — Annual Crude Oil Price Analysis (GARCH / ARMA / POMP)

---

## Summary

This project applies three classes of time series models — GARCH(1,1), ARMA(0,1), and a stochastic-volatility POMP model adapted from the course's financial-volatility case study — to annual crude oil log-returns from 1980 to 2019 (n = 39 observations). The authors report AIC values for each model and conclude that the POMP model provides the best fit. While the project demonstrates a working end-to-end POMP analysis, it suffers from a series of critical methodological and code-level errors that undermine the quantitative conclusions: the global search is initialized from a previous mif2 result rather than the raw pomp object (invalidating the global-search claim), the profile likelihood is seeded before the global search results are written to the CSV (producing a pre-global seed error), the profile φ is not held fixed during the profile IF2 search, convergence is poor and self-acknowledged but not corrected, and no non-mechanistic benchmark comparison is made. The extremely small sample size (n = 39) poses fundamental challenges for all three models that are not addressed.

---

## Major Issues

### 1. Global Search Initialized from Previous mif2 Result, Not the Base pomp Object

In the global box search chunk (`box_eval`), the `mif2()` call passes `if1[[1]]` (a previous mif2 result from the local search) as its first argument:

```r
if.box <- foreach(i=1:oilprice_Nreps_global, .packages='pomp', .combine=c) %dopar%
  mif2(if1[[1]], params=apply(oilprice_box,1,function(x)runif(1,x)))
```

The correct pattern is `mif2(oilprice.filt, params=...)`, using the base pomp object. By passing `if1[[1]]`, each global replicate inherits the cooling schedule state from the concluded local search chain. At the end of `Nmif=200` local search iterations, the cooling schedule is nearly fully decayed, so the new random starting parameters are perturbed by near-zero noise from the very first global iteration. The global search is therefore effectively a re-evaluation of `if1[[1]]`'s final parameter state, not a fresh exploration of the box. The claimed improvement in log-likelihood from local (-2.909) to global (-2.225) search cannot be attributed to genuine global optimization. This is a major methodological error (see skill `pomp-global-search-init-audit`).

**Fix:** Replace `mif2(if1[[1]], ...)` with `mif2(oilprice.filt, ...)` in the global search `foreach` loop. Also supply fresh `Np`, `Nmif`, and `cooling.fraction.50` arguments independently of the local search settings.

---

### 2. Profile Likelihood Seeded from Pre-Global-Search CSV State

The profile likelihood over φ appears in the document *before* the global box search. The profile code reads the accumulated CSV file to construct the starting box:

```r
read.table("oilprice_params.csv", header=TRUE) %>%
  filter(logLik>max(logLik)-20, logLik_se<2) %>%
  sapply(range) -> box
```

At the time this code runs, `oilprice_params.csv` contains only the local search results (the global search's `write.table(r.box, ...)` call comes later in document order). The profile is therefore seeded exclusively from the locally optimal parameter region. Combined with issue 1, the profile starting box reflects a sub-global optimum, and the resulting profile curve may not reach the true global log-likelihood at any value of φ. The confidence interval derived from this profile is invalid (see skill `pomp-profile-pre-global-seed-error`).

**Fix:** Move the profile likelihood block to appear after the global search block, so the CSV contains global results at box-construction time.

---

### 3. Profiled Parameter φ Not Fixed During Profile IF2 Search (rw.sd Drift Error)

In the profile IF2 call, φ is excluded from the `rw.sd` specification:

```r
rw.sd=rw.sd(sigma_nu = oilprice_rw.sd_rp,
             mu_h     = oilprice_rw.sd_rp,
             sigma_eta= oilprice_rw.sd_rp,
             G_0      = ivp(oilprice_rw.sd_ivp),
             H_0      = ivp(oilprice_rw.sd_ivp))
```

Because φ is absent from `rw.sd`, its perturbation defaults to zero, which is actually the correct behavior in this implementation — φ is held fixed at the profile grid value. However, the starting parameter for the profile run is set via `start=c(unlist(guesses[i,]), params_test)`. Because `params_test` contains `phi=expit(4)` and `guesses[i,]` also contains `phi` from the profile design, the `c()` concatenation creates duplicate names. In R, `c()` appends rather than overrides; `mif2` uses the first occurrence of each parameter name. Whether the grid value or `params_test` value for φ wins depends on which appears first in the concatenated vector. If `params_test` appears first, the profile grid value is silently ignored and all profile runs start from the same φ — invalidating the profile (see skill `pomp-profile-rw-sd-drift-error` and `pomp-global-search-param-override-bug`).

**Fix:** Construct the starting vector without duplicate names: use `c(unlist(guesses[i,]))` alone (dropping `params_test`), or use `modifyList(as.list(params_test), as.list(guesses[i,]))` to ensure the profile grid value overrides the default.

---

### 4. No Non-Mechanistic Benchmark Comparison

The POMP model's AIC (16.45) is compared only against GARCH(1,1) and ARMA(0,1), both of which model the log-returns time series. A critical comparison against a naive benchmark — such as a white noise model or auto-regressive model evaluated on the same data and same likelihood scale — is absent. The analysis selects ARMA(0,0) (white noise) as the best ARMA model by AIC but then proceeds with ARMA(0,1) for ulterior reasons, and the GARCH log-likelihood of -3.331 is cited in section 3.2 but the scale (per-observation vs. total) is unstated. The claim that the POMP model provides the best fit cannot be assessed without a quantitative comparison on a common likelihood scale. Wheeler et al. (2024) identify benchmark comparison as the single most diagnostic check for mechanistic model adequacy.

**Fix:** Report all log-likelihoods on the same scale (total log-likelihood). Compare POMP against ARMA(0,0) white noise and GARCH(1,1) at the same log-likelihood, and verify that the AIC values are computed from total rather than per-observation log-likelihoods.

---

### 5. Extremely Small Sample Size (n = 39) Undermines All Model Inferences

The analysis uses 39 annual observations after data subsetting (1980–2019). This is far too small to reliably identify a stochastic-volatility model with six parameters. The AIC table for ARMA correctly recovers ARMA(0,0) as the best model — consistent with a white-noise process — which the authors acknowledge but then dismiss as an artifact of limited data. For the POMP model, 39 data points provide a very weak basis for profile likelihood inferences about φ near 0.99 (near the boundary of stationarity). The authors briefly acknowledge this limitation but do not analyze its impact on the reliability of the GARCH, ARMA, or POMP results.

**Fix:** Either use monthly or quarterly crude oil price data (which is available at much higher frequency) to obtain a larger sample, or explicitly quantify the uncertainty introduced by the small n and acknowledge that the POMP model is overparameterized for this dataset.

---

### 6. Poor Convergence Self-Acknowledged but Not Addressed

The authors note: "The convergence plots show that some parameters could not converge very well." The diagnostic trace plots confirm that φ and σ_η do not stabilize across iterations. Despite this acknowledgment, no corrective action is taken: neither additional mif2 iterations nor increased particle count is tried. With Np=2000 and Nmif=200 for n=39 observations, the computational budget is not obviously the bottleneck; the non-convergence is more likely a symptom of issues 1 and 3 above (anchored global search, wrong profile seeding). Reporting log-likelihood and AIC values from non-converged searches as final estimates is a major validity concern (Wheeler et al. 2024, item 6: computational adequacy).

**Fix:** After correcting issues 1–3, re-run the optimization and verify convergence in all parameters before reporting final estimates.

---

### 7. GARCH Log-Likelihood Scale Discrepancy

Section 3.2 reports the GARCH(1,1) log-likelihood as -3.331448, described as "will be used as a baseline for further comparison with our POMP model." The POMP model achieves a log-likelihood of approximately -2.225. However, the GARCH model is fit using `garchFit` from the `fGarch` package, whose `logLik()` output may be on a per-observation scale or use a different normalization convention. If the GARCH log-likelihood is per-observation (scaled by n=39), the total log-likelihood would be approximately -130 — far worse than the POMP model. If it is the total, the comparison is more direct. The paper does not clarify the scale, making the comparison uninterpretable.

**Fix:** Explicitly state whether all reported log-likelihoods are total or per-observation, and standardize to the same scale before comparison.

---

### 8. AIC Computation Uses Best Replicate Log-Likelihood: Verify Against Summary Output

The AIC for the POMP model is computed as `2*6 - 2*max(r.box$logLik)` — using the maximum over replicates, which is the correct approach. However, the local search AIC in section 5.3 reports "Best AIC: around 17.81789" alongside the `summary(r.if1$logLik)` output. The code `2*6 - 2*max(r.if1$logLik)` should yield the correct result, but given that convergence is poor (issue 6), the maximum log-likelihood of -2.909 from the local search may be spurious (a noisy particle-filter visit to a high-likelihood region, not a stable MLE). The reliability of the reported AIC values depends on the convergence issues being resolved.

---

### 9. Profile Likelihood Interpretation Reversal

The profile likelihood conclusion states: "When φ is smaller than 0, [a] stack of points lay above the threshold of the 95% confidence interval. However we need to be cautious of the points lay under the threshold line when phi is between 0.5 and 1."

This interpretation is reversed. Points *above* the threshold line are *inside* the 95% confidence region, not outside it. Points below the threshold are *excluded* from the CI. The text also describes φ < 0, which is impossible under the `logit` transformation used in `partrans` (which maps logit-scale values to (0,1) before exponentiation). The profile appears to span the range 0.8–1.0 based on the `profile_design()` call, not below 0. The interpretation is confused and the confidence interval conclusion is unreliable given issues 2 and 3.

**Fix:** Correct the interpretation: the 95% CI for φ consists of the values for which the profile log-likelihood exceeds `max(logLik) - 0.5*qchisq(df=1, p=0.95)`. Re-compute after resolving issues 2 and 3.

---

### 10. No Model Diagnostics: Effective Sample Size and Conditional Log-Likelihoods

No particle filter diagnostics are presented: effective sample size (ESS) across time steps is not monitored, per-time-step conditional log-likelihoods are not plotted, and no forward simulation from the filtering distribution is shown. With n=39 and Np=2000, it is unknown whether particle degeneracy is occurring. Wheeler et al. (2024) identify per-observation conditional log-likelihoods as a key diagnostic for understanding where and how the model fails. For this dataset, the 2008 price crash and 2014–2016 price collapse are plausible periods of poor fit that would be invisible without these diagnostics.

**Fix:** Run `pfilter()` at the MLE and plot `cond.logLik(pf)` across years. Check that ESS does not collapse to near 1 during extreme price movements.

---

## Minor Issues

- **Data subsetting by row number rather than year:** The data subset uses `oil[120:160,]` to extract rows 120–160 from the original 160-row dataset. This relies on the dataset having exactly 160 rows with 1861 as row 1, which should be verified programmatically (e.g., `filter(Year >= 1980 & Year <= 2020)`) to avoid fragility.

- **AIC table for GARCH uses a static image:** The GARCH AIC table (Section 3.1) is inserted as a JPEG image (`garch.jpg`) rather than computed from the code block above it. The code block computes the table but it is commented out (`# kable(aic_table,digits=2)`). This is poor reproducibility practice; readers cannot verify the table values from the code.

- **ARMA model selection reasoning is circular:** The authors note ARMA(0,0) has the lowest AIC, then select ARMA(0,1) because "higher AIC value might imply there are some dependence relationships." This argument uses higher AIC as evidence of dependence, which misuses AIC. The likelihood ratio test between ARMA(0,1) and ARMA(4,5) is appropriate but the selection rationale for ARMA(0,1) as the baseline should be stated more carefully.

- **Filtering simulation on simulated data (Section 5.2) is not informative:** The authors run the particle filter on simulated data from the model (`sim1.filt`) rather than on the actual oil price data. The resulting log-likelihood (-65.07) applies to the simulated dataset, not the observed data. This section does not contribute to understanding model fit to the real data.

- **`start=c(unlist(guesses[i,]), params_test)` in profile uses `nprof=2`:** Only 2 starting points per profile-grid cell (`nprof=2` in `profile_design()`) are used across 50 grid values for a total of 100 profile runs. This is a very low number of restarts per grid point for an identifiability analysis on a volatile log-likelihood surface.

- **No sessionInfo() or package versions reported:** The `pomp` version is not stated, and the `fGarch`, `tseries`, and `forecast` package versions are unspecified. Given that the `pomp` API has changed significantly across versions, the analysis may not reproduce on a different installation.

- **References 8 and 9 cite 2020 lecture notes** for a 2022 project. The 2022 course notes (ionides.github.io/531w22) should be cited rather than the 2020 notes.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/oilprice_params.csv`
