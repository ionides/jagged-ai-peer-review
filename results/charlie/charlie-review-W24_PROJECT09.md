---
title: "Review: W24 Project 09"
subtitle: "*Volatility analysis of NASDAQ 100*"
format: pdf
---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) + particle filter (pfilter) via pomp; ARIMA via arima(); GARCH via tseries and fGarch |
| **R packages used** | pomp, tseries, fGarch, forecast, doParallel, doRNG, doFuture, tidyverse |
| **Code publicly available** | Partial — Rmd and data file submitted; cached .rda stew files not included |
| **Data publicly available** | Yes — NASDAQ IXIC daily closing prices, sourced via Python yfinance |
| **Benchmark comparison included** | Yes — GARCH(1,1) (via both fGarch and tseries) used as benchmark against the POMP stochastic volatility model |

---

## POMP Checklist Scorecard

*checkmark = satisfies practice, ~ = partially satisfies, x = does not satisfy, N/A = not applicable*

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + replicated pfilter used correctly; logmeanexp applied |
| 2 | Benchmark comparison | checkmark | GARCH(1,1) benchmark included and compared by logLik |
| 3 | Quantitative goodness-of-fit reporting | ~ | LogLik reported for all models but text misquotes its own output |
| 4 | Model diagnostics | ~ | Trace plots shown; no simulation-based or conditional logLik diagnostics |
| 5 | Parameter identifiability and uncertainty | x | Profile likelihood code is buggy; CI invalid |
| 6 | Computational adequacy | ~ | Run_level=3 for main model but run_level=2 for comparison model; no timing reported |
| 7 | Forecast methodology | N/A | No forecasting performed |
| 8 | Model variations and nested comparisons | ~ | Leverage vs. no-leverage compared, but at incomparable computational levels |
| 9 | Stochasticity | checkmark | Stochastic volatility process and normal measurement model used |
| 10 | Reproducibility and extendability | ~ | Rmd submitted; stew .rda files missing; no package version pinning |
| 11 | Corroboration with scientific knowledge | ~ | sigma_nu near zero interpreted as weak leverage; plausibility discussed informally |
| 12 | Measurement model specification | checkmark | Normal measurement model y ~ N(0, exp(H/2)) clearly specified in code and text |
| 13 | Initial conditions | ~ | H_0 and G_0 estimated as parameters; sensitivity not assessed |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

The paper applies ARIMA, GARCH, and a POMP-based stochastic volatility model (Breto's model with leverage effect) to demeaned log-returns of the NASDAQ 100 index spanning 1971 to 2024 (~13,400 daily observations). The authors report that POMP outperforms both ARIMA and GARCH by log-likelihood, and then test whether the leverage component is necessary by building a simplified no-leverage model. The main scientific claim is that the leverage effect is required even though its fitted magnitude is small.

**Strengths:** The paper demonstrates a clean pipeline from data collection through ARIMA, GARCH, and POMP fitting. The use of GARCH as a quantitative benchmark is good practice. The authors apply logmeanexp correctly for aggregating replicated particle filter log-likelihoods, and they use run_level switching to manage computational scale. The scientific question — whether a leverage effect is needed in the volatility dynamics — is well-motivated and clearly posed.

**Weaknesses:** A critical code error in the profile likelihood section causes the profile to evaluate parameters from the wrong optimization (the global search results, not the profile optimization results), completely invalidating the reported confidence interval for sigma_eta. The comparison between the leverage and no-leverage models is unfair because the two models are fitted at incomparable run levels (run_level=3 vs. run_level=2). A declining log-likelihood trajectory in the local search is misdiagnosed as overfitting rather than model misspecification. The text misreports the maximum log-likelihood from the global search as 3483 when the actual output shows 43483, reversing the claimed direction of the comparison with GARCH at that point in the narrative.

---

## Major Issues

### 1. Profile likelihood code evaluates global search parameters instead of profile parameters

The profile likelihood computation (Rmd lines 501–505) contains a critical indexing error. After running 100 profile optimization chains stored in `if.prof`, the log-likelihood evaluation loop reads:

```r
L.prof <- foreach(i=1:100, .packages='pomp', .combine=rbind) %dopar% {
  logmeanexp(replicate(ndx_Nreps_eval, logLik(
    pfilter(ndx.filt, params=coef(if.box[[i]]), Np=2000))), se=TRUE)
}
```

The argument `params=coef(if.box[[i]])` draws parameters from `if.box`, which are the 100 global search results (fitted without fixing sigma_eta), not from `if.prof` (the 100 profile optimization results with sigma_eta constrained). The resulting `r.prof` data frame pairs sigma_eta values from the profile optimizer (`t(sapply(if.prof, coef))`) with log-likelihood values from a separate set of global search evaluations (`L.prof`). The i-th sigma_eta and i-th log-likelihood come from different optimization runs with different sigma_eta values, so the pairing is meaningless.

The consequence is that the profile likelihood plot does not show how the likelihood varies as sigma_eta is held fixed and other parameters are optimized. The plot instead shows a scatter of log-likelihoods from re-evaluated global search parameters plotted against unrelated sigma_eta values. The Wilks-based confidence interval [0.54, 1] for sigma_eta is therefore invalid. The fix is to replace `coef(if.box[[i]])` with `coef(if.prof[[i]])` in the evaluation loop.

### 2. Leverage and no-leverage models compared at incomparable computational levels

The Breto leverage model (Section "Set up different level of modeling") uses run_level=3, giving Np=2000, Nmif=500, Nreps_eval=20, Nreps_local=20, Nreps_global=100. The no-leverage simplified model (Section "Volatility model without leverage") silently resets run_level=2, giving Np=100, Nmif=50, Nreps_eval=10, Nreps_local=20, Nreps_global=20.

The no-leverage model's local search uses 20x fewer particles and 10x fewer IF2 iterations. The global search uses 5x fewer replicates. The conclusion "the 4-parameter model still reported less likelihood values with global search than the original model. This means the model with leverage performed better" is not supported: the no-leverage model may simply be under-optimized. The difference in maximized log-likelihoods between the two models could shrink substantially under matched computational effort. For a meaningful nested comparison, both models must be fitted with the same Np, Nmif, and number of replicate searches.

### 3. Declining log-likelihood during local search misdiagnosed as overfitting (CC-Yes, Error 1.5)

The local search trace is described as showing "a quick increase followed by a gradual decrease," and the paper concludes "This implies that the model might be overfitted and stuck in a local maxima." This misattributes the symptom. The course explicitly taught (Q10-01) that declining likelihood after an initial rise in iterative filtering signals model misspecification — the unperturbed model cannot fit the data — and that the correct response is structural model revision, not simply proceeding to global search with more random starting values. Overfitting and local-maxima entrapment are distinct phenomena from a declining optimization trajectory. The paper does not investigate which structural feature of the model causes the decline.

### 4. Profile design evaluated on only 100 of 600 designed starting points

The `profile_design` call (Rmd lines 476–481) generates a 600-row grid: 40 sigma_eta values (in [0.5, 0.95]) times 15 random starting points per value. However, the subsequent optimization loop runs only `foreach(i=1:100, ...)`. Only i=1 through 100 of the 600 designed starting points are used, leaving 500 starting configurations unevaluated. On average, only the first 2–3 sigma_eta values out of 40 are covered by the profile. Even if the logLik evaluation bug (Issue 1) were corrected, the profile would still be incomplete. The paper acknowledges "the samples we got were pretty few" but attributes this to computation time rather than to the loop bound. The loop bound must be corrected to match nrow(guesses) for a complete profile.

### 5. Profile CI upper bound lies at the boundary of the search range

The reported profile CI for sigma_eta is described as "[0.54, 1]." The profile_design searches sigma_eta only in [0.5, 0.95] (Rmd line 477). An upper CI bound of 1 lies outside the searched range, indicating that the likelihood does not drop below the Wilks threshold within the feasible search region. This means sigma_eta is not identified from above: the data and model are consistent with sigma_eta values well above 0.95. The upper confidence bound is therefore an artifact of the search range, not a genuine statistical limit. The paper presents this as an identified interval without acknowledging the open-ended upper bound.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots are shown for both the local and global search. The local search trace shows a declining log-likelihood trajectory (acknowledged but misdiagnosed; see Major Issue 3). The global search trace is described as showing "better convergence in G_0" but persistent spread in sigma_nu, mu_h, phi, and sigma_eta. The paper does not report how many global search runs reached likelihoods within a few units of the maximum, which is the standard evidence for convergence.

**Particle filter:** Replicated pfilter with logmeanexp is used correctly throughout. The number of particles (Np=2000 at run_level=3) is reported. ESS is not monitored at any point. For a dataset of 13,400 time steps, persistent ESS collapse would indicate model-data mismatch; its absence from the diagnostics is a gap.

**Conditional log-likelihoods:** Per-observation conditional log-likelihoods are not plotted. These would identify specific time periods (e.g., the 2000 dot-com crash, the 2008 financial crisis, 2020 pandemic) where the stochastic volatility model fits poorly and might motivate structural extensions.

**Profile likelihoods:** The profile computation is invalidated by the code bug described in Major Issue 1. No profiles are computed for phi, mu_h, or sigma_nu, leaving identifiability of the other key parameters unassessed. The paper notes phi converges well in traces but does not verify this formally.

**Computational scale:** The global search at run_level=3 is described as having been run on GreatLakes HPC ("more than 5 hours"). Total CPU-hours are not reported. The stew .rda cache files are not included in the submission, so the computation cannot be verified or reproduced without re-running the full HPC job.

---

## Reproducibility Assessment

**Code availability:** The Rmd and data file (^IXIC_quote.csv) are submitted. The stew .rda cache files (pf1_3.rda, mif1_3.rda, box_eval_3.rda, profile_sigma_eta_3.rda, etc.) are not included. Without these caches, the analysis requires re-running multi-hour HPC computations that are not feasible from the submitted files alone.

**Final parameters:** No standalone CSV or RDS file of the MLE parameter vector is archived. Readers cannot evaluate the fitted model without re-running the full optimization.

**Model-code consistency:** The measurement model in code (`lik=dnorm(y,0,exp(H/2),give_log)`) matches the mathematical specification (`Y_n = exp(H_n/2) * epsilon_n`) for the normal measurement model.

**Package versions:** No sessionInfo() output or renv lockfile is provided. The pomp API has changed across versions; results may not reproduce on current CRAN releases.

**Auxiliary data:** The primary dataset file is included. No additional auxiliary inputs are required for this univariate model.

**HPC reproducibility:** The paper mentions HPC (GreatLakes, SLURM) but no job submission scripts (.sbat or .slurm files) are included. Cluster environment specifications (node count, memory, walltime) are not documented.

---

## Minor Issues

- **Text misquotes its own numerical output:** Section "Global search" states "The maximum of the value reached 3483 which is already better than GARCH and ARIMA," but the `summary()` output printed immediately below shows Min=43471, Max=43483. The maximum is 43483, not 3483. The text has dropped the leading "4". At the misprinted value of 3483, the claim would be false (3483 < 43265, the tseries GARCH logLik). The actual maximum (43483 > 43361.47) does support the claim.

- **tseries::garch log-likelihood normalization not verified (CC-Yes, Error 2.9):** The paper explicitly cites a Stack Exchange post about the normalization difference between tseries::garch and fGarch, and notes the tseries values are worse. It then proceeds to compare the POMP logLik (43483) to the fGarch ARMA(4,4)+GARCH(1,1) logLik (43361.47) without verifying that fGarch and POMP use the same likelihood normalization. The tseries two-step approach (GARCH fitted to ARIMA residuals) yields a joint-model approximation, not the full-data likelihood. The paper should verify the normalization conventions or flag the comparison as approximate.

- **No formal AIC comparison for nested leverage/no-leverage models:** The paper compares raw log-likelihoods between the 6-parameter leverage model and the 4-parameter no-leverage model. A likelihood ratio test statistic of 2 * (logLik_full - logLik_reduced) under chi-squared with 2 degrees of freedom would provide a formal test of whether the additional leverage parameters are statistically warranted, which is the scientifically relevant question.

- **No simulation-based goodness-of-fit from the fitted model:** The paper shows a simulation from initial parameter guesses (pre-fitting) as a sanity check, but never shows forward simulations from the MLE or global-best parameter estimates overlaid on observed returns. Such plots, which are the standard POMP model validation tool, would show whether the fitted stochastic volatility model reproduces the observed volatility clustering, heavy tails, and crisis episodes in the returns.

- **Initial pfilter applied to simulated data, not real data:** The initial likelihood test (Rmd lines 336–342) applies pfilter to `sim1.filt`, which contains simulated returns as data, not ndx$demeaned. The output log-likelihood (~-17965) reflects how well the initial parameters describe the simulated data. Comparing this to the S&P 500 initial estimate from the lecture slides is not meaningful, since those values were computed on real S&P 500 data.

- **Spectral analysis applied to returns rather than squared returns:** The periodogram analysis (Rmd lines 86–97) is applied to demeaned returns directly. For volatility analysis, the periodogram of squared returns or absolute returns is more informative, as it reveals heteroskedastic cycles and clustering. The periodogram of returns tests for autocorrelation in the conditional mean, which is expected to be absent in efficient markets and contributes little to the volatility analysis.

- **No profiles for phi, mu_h, or sigma_nu:** Only sigma_eta is profiled. The trace plots show phi converging to ~0.96 and mu_h converging to ~-8.9, but no confidence intervals are reported for these parameters. Profile likelihoods for phi (the key persistence parameter) would be particularly informative for financial interpretation.

- **Model selection criteria switch between ARIMA and GARCH sections:** ARMA(5,5) is selected by AIC (Section "Fitting ARIMA models"). When the ARMA+GARCH model is re-fitted, the order is reduced from (5,5) to (4,4) based on coefficient significance, not AIC. Mixing selection criteria (AIC for ARIMA, significance for GARCH) is not methodologically consistent; AIC or likelihood comparison should be used throughout.

- **Stew cache files absent from repository:** The code uses `stew()` to cache six expensive computation results in .rda files. None of these are submitted. Without them, the code will re-run all HPC computations, which the paper states takes more than 5 hours. The repository is not self-contained for reproduction.

---

## Recommendation

Major Revision. The paper addresses a well-defined question and applies the appropriate POMP framework. However, two structural problems prevent the current conclusions from being trusted. First, the profile likelihood code bug (Major Issue 1) means the only formal uncertainty quantification in the POMP analysis — the CI for sigma_eta — is invalid and must be recomputed with the corrected indexing. Second, the comparison between the leverage and no-leverage models (the paper's primary scientific conclusion) is confounded by a factor-of-20 difference in computational effort (Major Issue 2); this comparison must be rerun at matched run levels before any inference about leverage necessity can be made. The misdiagnosis of declining log-likelihood (Major Issue 3) should be corrected and followed up with structural diagnostics. Once these three issues are addressed, the paper would provide a credible analysis of NASDAQ volatility using a well-established stochastic volatility framework.

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
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project09/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project09/blinded.md`
