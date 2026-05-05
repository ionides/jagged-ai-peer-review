# Peer Review: W21 Project 04
## "Extended Analysis on the U.S. 10-year Treasury Bond Yield"

---

## Summary

This project fits a stochastic leverage (SV) POMP model to the monthly first differences of the U.S. 10-year Treasury bond yield, comparing its performance against a baseline GARCH(1,1) model. The POMP model achieves a higher log-likelihood (-25.71 vs. -33.89) using more parameters, and a complementary section explores Loess-based trend decomposition and the association between the yield and CPI via a coherence analysis. While the POMP setup is largely coherent and runs at an appropriate computational level, several critical inferential issues undermine the validity of the central likelihood comparison: the GARCH log-likelihood is produced by `tseries`, which is known to report a non-standard (scaled) likelihood value making direct numerical comparison to the POMP particle filter estimate invalid; the model is never compared to a proper ARMA/ARIMA non-mechanistic benchmark; and no profile likelihoods are computed for any parameter. The complementary sections (Loess decomposition, CPI analysis) are only loosely connected to the primary POMP analysis and add little inferential value.

---

## Major Issues

### 1. GARCH vs. POMP likelihood comparison is invalid due to non-standard GARCH likelihood normalization

The report's central conclusion is that "the POMP model performed better" because POMP achieves log-likelihood -25.71 vs. GARCH's -33.89. However, the GARCH likelihood is computed via `tseries:::logLik.garch(fit.garch)`, and the `tseries` package is known to report a non-standard log-likelihood value — specifically, it may exclude constants or use a different normalization convention compared to a properly computed Gaussian log-likelihood. The POMP `dmeasure` evaluates `dnorm(y, 0, exp(H/2), give_log)`, which includes all normalizing constants. If the two likelihoods are not on the same normalization scale, the comparison is numerically meaningless. The report presents this comparison as the primary motivation for preferring POMP, but does not verify that both likelihoods are computed on the same scale. This error matches the course-documented Warning 2.9 (trusting software likelihood output without checking normalization conventions). The conclusion that POMP is superior cannot be sustained without verifying comparability.

**Fix:** Compute both likelihoods on the same scale (e.g., manually implement or verify GARCH log-likelihood with all constants included), or explicitly acknowledge the potential non-comparability and withdraw the quantitative comparison.

---

### 2. No non-mechanistic ARMA/ARIMA benchmark comparison

The stochastic volatility POMP model's log-likelihood is compared only to a GARCH model (itself subject to the problem in Issue 1). No comparison to a simple ARMA or auto-regressive model for the differenced yield series is provided. An ARMA model fit to the yield differences is a natural benchmark: it would indicate whether the added complexity of a stochastic volatility structure is warranted. Without this, it is impossible to determine whether the mechanistic SV model captures meaningful structure in the data beyond what a simpler statistical model would achieve. This corresponds to POMP checklist item #2 (benchmark comparison) and course Error 1.6.

**Fix:** Fit an ARMA(p,q) model (or auto.arima selection) to the yield differences and report its log-likelihood alongside the POMP model's. Discuss whether the SV model provides a meaningful improvement.

---

### 3. Profile likelihoods absent; parameter identifiability not assessed

No profile likelihoods are computed for any of the six model parameters (sigma_nu, mu_h, phi, sigma_eta, G_0, H_0). The pairs plot from the global search shows the geometry of the likelihood surface qualitatively, but this is not a substitute for profile likelihood-based confidence intervals. In particular, phi (the persistence parameter) and sigma_eta are key to interpreting the stochastic leverage dynamics, but whether these are identifiable from the data is never assessed. This corresponds to POMP checklist item #5 and course Error 1.9.

**Fix:** Compute profile likelihoods for at least the scientifically most important parameters (phi, sigma_eta, sigma_nu) using a grid of fixed values for the target parameter while re-optimizing over all others at each point. Report confidence intervals.

---

### 4. Local search (mif2) starts from a single fixed initial parameter vector

The local iterated filtering run (`mif1`) uses `params=params_test` as the starting point for all 20 replicates. All local searches therefore start from the same location, providing no evidence that the search explored the likelihood surface from diverse starting points. This is partially compensated by the subsequent global search, but the local search results are reported first with a pairs plot, and the pairs plot reflects only the geometry near the single starting point rather than a global exploration. This partially violates POMP checklist item #6 and course Error 1.8.

**Fix:** For the local search, perturb the starting parameters across replicates (e.g., sample from a box around `params_test`), or rely solely on the global search results for parameter estimation and convergence assessment.

---

### 5. Convergence diagnostics (trace plots) are not shown

Despite running `mif2` at run_level=3 with Nmif=200, no trace plots (log-likelihood or parameter values across iterations) are presented for any mif2 run, neither for the local nor the global search. The only convergence evidence shown is the pairs plots of terminal parameter estimates, which only capture the final state of optimization without showing whether the algorithm was still improving at termination. This directly violates POMP best practice (checklist item #6) and course Error 1.8.

**Fix:** Display `plot(mif2_object)` output or equivalent trace plots showing the log-likelihood trajectory and parameter trajectories across iterations for representative runs from the global search.

---

### 6. Global search starts from a single local search endpoint rather than random box samples

The global search uses `mif2(if1[[1]], params=apply(yield_box,1,function(x)runif(1,x)))` — meaning it starts from `if1[[1]]` (the first local mif2 object, which itself was initialized from `params_test`) and then perturbs the parameters. This is not equivalent to starting each global search replicate from scratch at a randomly drawn point in the box. Because `mif2` continues from the state of `if1[[1]]`, all global search replicates begin from a warm-started, partially converged state. While the parameters are randomized, the internal filtering state of `if1[[1]]` is inherited, which can bias the search toward the region already explored by the local run. The proper approach is `mif2(yield.filt, params=apply(yield_box,1,function(x)runif(1,x)))` for each replicate.

**Fix:** Initialize each global search replicate from the base pomp object `yield.filt` with randomly drawn parameters from `yield_box`, rather than continuing from a previous mif2 object.

---

## Minor Issues

### 7. AIC comparison between GARCH and POMP not discussed

The conclusion favors POMP based on log-likelihood alone (POMP: -25.71 with 6 parameters; GARCH: -33.89 with 3 parameters). A proper AIC comparison would penalize for the additional 3 parameters in POMP: AIC_POMP = 2*25.71 + 2*6 = 63.42; AIC_GARCH = 2*33.89 + 2*3 = 73.78. The AIC still favors POMP, but this analysis is not presented. More importantly, as noted in Issue 1, the non-comparability of the raw likelihoods means the AIC comparison is also potentially invalid. At minimum, the parameter count difference should be acknowledged.

---

### 8. Loess span choice not justified

The complementary Loess analysis uses `span=0.5` for trend and `span=0.1` for noise extraction without any justification. These choices directly determine what is attributed to "trend," "noise," and "cycles," making the decomposition sensitive to the subjective span selection. A sensitivity analysis over span values, or a data-driven criterion (e.g., cross-validation), would strengthen this analysis.

---

### 9. Date axis of Loess plot is misaligned with the data

The monthly yield data covers 1990-2021, but the Loess plot uses `date = seq(from=1962, length=length(monthdata$Date), by=1/12)`, producing a time axis starting from 1962 rather than 1990. This is an error in the x-axis label/scale that does not affect the fitted values but produces a misleading plot.

---

### 10. Filtering on simulated data section is incomplete

Section 4.1 describes filtering on simulated data using `pf1` and reports a log-likelihood of -539.67, but does not demonstrate parameter recovery (re-estimation of parameters from simulated data). The described purpose of filtering on simulated data is to verify that the filtering and re-estimation pipeline works correctly. Re-running `mif2` on the simulated data and comparing estimated parameters to the known true parameters used to simulate would fulfill this purpose. Without re-estimation, this section only demonstrates that pfilter runs without error.

---

### 11. Loess plot x-axis start year is inconsistent with data range

Related to Issue 9: the code sets `date = seq(from=1962, ...)` but the data begins in 1990. While the monthly `yield` object is correctly defined from `monthdata$Yield` (1990 onward), the Loess plot labels the x-axis as though the series begins in 1962. This date mismatch will confuse readers interpreting the decomposition plots.

---

### 12. Missing sessionInfo() and package version documentation

The Rmd file does not include a `sessionInfo()` call or any documentation of package versions. The `pomp` package API has changed substantially across versions, and results may not reproduce on current CRAN releases. Given that this report uses `pomp` for the main analysis, the package version should be recorded.

---

### 13. CPI LRT conclusion overstated

The report states "we could not find a clear association" between detrended yield and detrended CPI based on the LRT p-value exceeding 0.05. Failure to reject the null does not establish that there is no association; the analysis may simply lack power. The conclusion should be stated more carefully: "we found no statistically significant evidence for an association at the 5% level" rather than claiming absence of association.

---

### 14. CPI labeled "Customer" instead of "Consumer" Price Index

The report consistently uses "Customer Price Index" when the standard term is "Consumer Price Index." This is a minor terminological error that appears in the section title, body text, and references.

---

### 15. Monte Carlo standard error for global search log-likelihood not reported

The best log-likelihood from the global search (-25.71) is reported without a Monte Carlo standard error. Each log-likelihood evaluation uses `logmeanexp(replicate(yield_Nreps_eval, logLik(pfilter(...))))`, and the `se=TRUE` option is passed (as seen in the local search). The global search `L.box` object should include standard errors, but these are not presented for the best result. Without the Monte Carlo SE, it is unclear whether the -25.71 estimate is reliable or noise-dominated.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project04/blinded.Rmd`
