# Peer Review: W21 Project 06
**Title:** "To The Moon or Not — Analysis on GameStop Stock Price"

---

## Summary

This project applies ARMA, GARCH, and a stochastic volatility POMP model (Breto 2014) to the daily log-returns of GameStop (GME) stock over approximately one year (April 2020 – April 2021). The paper presents AIC-based model selection, particle-filter likelihood estimation, local IF2 search from fixed starting values, and a global IF2 search from randomized box starting values. The POMP model is declared the preferred model based on the highest AIC score among the four candidate models.

Key strengths include a clearly described mechanistic motivation (leverage effect), use of proper plug-and-play methods (mif2 + pfilter), both local and global IF2 searches, and convergence trace diagnostics. However, the analysis suffers from several critical problems: (1) the initial "filtering on simulated data" likelihood is reported without clarification that it is evaluated on a simulated, not real, dataset; (2) the global IF2 search is initialized from a previous mif2 result object rather than the base pomp object, invalidating its claim to global coverage; (3) there is no benchmark comparison against a non-mechanistic model at the same data-model level; (4) profile likelihoods are absent; and (5) the AIC comparison conflates models with different observation distributions on different data transformations.

---

## Major Issues

### 1. Simulated-Data Particle Filter Presented Without Clear Benchmark Qualification

The chunk labeled "Filtering on simulated data" runs `pfilter` on `sim1.filt`, which is a pomp object constructed from a *simulated* dataset (derived from `sim1.sim`), not from the real GME log-return data. The reported log-likelihood `L.pf1` is therefore evaluated on a different dataset than the real data used in the IF2 searches. The narrative does not explicitly clarify that this value is a diagnostic run on simulated data, not an initial benchmark for the real-data model. A reader reading the section flow would not immediately recognize the dataset substitution. This matches the anti-pattern documented in the pomp-simdata-benchmark-error skill: the value `L.pf1` is printed and the section is titled "filtering on simulated data," but the subsequent mif2 section immediately follows with real-data optimization, creating potential confusion about comparability.

**Fix:** Add a clear statement before or after printing `L.pf1` that this likelihood is evaluated on a simulated dataset and cannot be compared to the real-data IF2 log-likelihoods reported later. Optionally, also run `pfilter` on `GME.filt` (the real-data object) at `params_test` to provide a genuine real-data baseline.

---

### 2. Global IF2 Search Initialized from Previous mif2 Result (Anti-Pattern)

The global box search in the chunk "Likelihood maximization using randomized starting values" passes `if1[[1]]` — a previous IF2 result object — as the first argument to `mif2()`:

```r
if.box <- foreach(...) %dopar% mif2(if1[[1]], params=apply(GME_box,1,function(x)runif(1,x)))
```

This is the anti-pattern documented in the pomp-global-search-init-audit skill. When `if1[[1]]` is used as the base object, the global search inherits the cooling schedule that was already run to near-completion during the local IF2 search. As a result, the random-walk perturbations have already shrunk close to zero, meaning the global replicates effectively perform very few functional IF2 iterations from their new starting points. The reported "global maximum" may not differ meaningfully from the local-search optimum dressed up as a global search.

**Fix:** Replace `mif2(if1[[1]], ...)` with `mif2(GME.filt, ...)` in the global search loop, where `GME.filt` is the base pomp object (not a previous mif2 result). This ensures each global replicate starts fresh from a genuine random initial parameter vector.

---

### 3. No Benchmark Comparison Against a Non-Mechanistic Model at the Correct Level

The paper compares ARMA, GARCH, and POMP models by log-likelihood, but these models are evaluated on different data transformations and under different observation distributions (see Issue 4 below). More fundamentally, there is no non-mechanistic benchmark constructed on the *same* data and observation model as the POMP model. The GARCH(1,1) model uses a Gaussian log-return likelihood while the POMP model also uses a Gaussian measurement model, but both are fitted on log-returns. However, GARCH is a legitimate mechanistic-style volatility model, not a non-mechanistic benchmark in the sense of Wheeler et al. (2024): the paper should compare the stochastic volatility POMP model against a simple ARMA-type volatility model (e.g., an autoregressive model on squared returns) evaluated under the same Gaussian assumption, with quantitative log-likelihood reported on the same data. Without such a comparison it is impossible to assess whether the stochastic leverage model captures meaningful structure beyond a simpler statistical model.

Wheeler et al. (2024) note that none of 32 cholera models they reviewed included such a comparison, and that non-mechanistic benchmarks revealed failures in several mechanistic models. The same principle applies here.

**Fix:** Fit an ARMA model for the squared (or absolute) log-returns as a benchmark for volatility modeling, and compare its log-likelihood (evaluated under a Gaussian measurement model on the original log-returns) to the POMP model's log-likelihood.

---

### 4. Invalid Cross-Model Log-Likelihood Comparison (AIC Table in Conclusion)

The conclusion compares ARMA(1,3), GARCH(1,1), GARCH(4,2), and the POMP model by their log-likelihoods and AIC scores. However:

- The ARMA(1,3) log-likelihood of 136.44 is evaluated on the log-return series under a Gaussian model for the mean, not the variance.
- The GARCH log-likelihood of 203.44 is a different computation (the GARCH-specific conditional variance likelihood) computed by `tseries:::logLik.garch()`.
- The POMP log-likelihood of 239.30 is a particle-filter estimate.

These are not comparable on a common scale. The ARMA model fits the mean of log-returns; GARCH fits the conditional variance structure; and the POMP model jointly models the latent log-volatility process. Direct numerical comparison of their log-likelihoods, or the AIC scores derived from them, is not valid because the models condition on different sufficient statistics and are evaluated under different effective observation models. As documented in the sarima-baseline-audit skill, a direct numerical comparison of log-likelihoods from different model families is invalid unless both models are evaluated on the same untransformed data under the same observation model.

**Fix:** Restrict the quantitative model comparison to models that share the same observation model and data transformation. For the GARCH vs. POMP comparison, this requires evaluating the log-likelihood of both under the same Gaussian measurement model for log-returns. The ARMA model comparison should be presented separately as a mean-model diagnostic, not as a volatility-model competitor.

---

### 5. No Profile Likelihoods for Key Parameters

The paper reports no profile likelihoods for any of the four structural parameters (sigma_nu, mu_h, phi, sigma_eta) or the two initial conditions (G_0, H_0). Without profile likelihoods, it is impossible to assess whether these parameters are identifiable from the GME data, and all reported point estimates may be unreliable. The convergence diagnostics show that H_0 and sigma_nu do not appear to converge, which is precisely the situation where profile likelihoods are most needed to determine whether the model is overparameterized or the data are simply uninformative about those parameters.

Wheeler et al. (2024) identify profile likelihood computation as essential for assessing parameter identifiability and providing confidence intervals.

**Fix:** Compute profile likelihoods for at least sigma_nu, phi, and sigma_eta using `profile_design()` to construct a fixed grid for each parameter, optimize the remaining parameters via IF2 at each grid point (with the profiled parameter excluded from `rw.sd`), and apply the chi-squared cutoff to obtain confidence intervals.

---

### 6. Non-Convergence Acknowledged but Not Remediated

The convergence diagnostics section explicitly states that H_0 and sigma_nu "seem not to converge." The conclusion repeats this observation but proposes only vague remedies ("more iterations or better starting values"). Non-convergence of parameters means the reported maximum log-likelihood of 239.8 (local search) and approximately 239.30 (global search) may not be near the MLE. The convergence traces for the global search also show that phi and sigma_eta converge only to a "certain range" rather than a specific value. This pattern is consistent with the global search being anchored near the local search solution (Issue 2), preventing genuine exploration.

**Fix:** Increase the number of particles and IF2 iterations (e.g., Np = 5000, Nmif = 300+), use more global search replicates (100+), fix the global search initialization bug (Issue 2), and re-examine convergence traces. If H_0 remains non-convergent, consider fixing it or placing a tighter prior on it.

---

### 7. Quantitative Model Adequacy Assessment Is Incomplete

The paper does not present conditional log-likelihoods per time point, effective sample size (ESS) traces from the particle filter, or any simulation-based goodness-of-fit statistics beyond a visual comparison of one simulated trajectory against the observed log-returns. Wheeler et al. (2024, §Model diagnostics) emphasize that conditional log-likelihood plots identify specific periods of poor fit, and ESS monitoring reveals particle degeneracy. The simulated trajectory shown in the paper was generated at arbitrary starting parameters before optimization, making it uninformative about the fitted model's adequacy.

**Fix:** After obtaining a well-converged MLE, plot simulations from the fitted model overlaid on observed data; compute and plot conditional log-likelihoods per time step; monitor ESS in the particle filter to ensure no degeneracy.

---

## Minor Issues

### 8. Pairs Plot Subset Criterion Differs Between Local and Global Searches

In the local search pairs plot, the code filters `subset(r.if1, logLik > max(logLik) - 20)`, while the global search pairs plot filters `subset(r.box, logLik > max(logLik) - 10)`. Using different cutoffs makes visual comparison of the two scatter plots uninformative. The local-search cutoff of 20 log-likelihood units is quite wide and may include many poorly converged chains.

**Fix:** Use a consistent cutoff (e.g., 10 units below the maximum) for both pairs plots and document why that threshold was chosen.

---

### 9. AIC Calculation for POMP Model Appears to Use Median Log-Likelihood

The conclusion states "The POMP model gives median loglikelihood of 239.30 with AIC score of -466.6. (# of params = 6)." The AIC score of -2(239.30) + 2(6) = -466.6 is computed from the median log-likelihood of 239.30, not from the maximum. AIC should be based on the maximum log-likelihood, not the median. This is a computational error in the AIC calculation for the POMP model.

**Fix:** Compute AIC from the maximum log-likelihood across all search replicates, not the median. Report `max(r.box$logLik)` as the log-likelihood for AIC purposes.

---

### 10. Conclusion Incorrectly Claims "POMP Model is a Good Fit Because Log-Likelihood Converges Quickly"

The conclusion states: "we believe the POMP model is a good fit for the data because the loglikelihood converges really quickly." Convergence of the log-likelihood is a computational diagnostic for the optimization algorithm, not evidence of model adequacy or goodness of fit. A poorly specified model can converge quickly to a local optimum. The paper conflates optimization convergence with statistical goodness of fit.

**Fix:** Separate convergence diagnostics (which assess whether the optimizer found the MLE) from goodness-of-fit assessment (which requires comparing model predictions to data, e.g., via simulation envelopes, conditional log-likelihoods, or benchmark comparison).

---

### 11. Missing rw.sd Justification

The rw.sd values for all regular parameters are uniformly set to 0.02. No justification is provided for this choice. Given that parameters like phi are on a logit-transformed scale and mu_h is on the natural scale, a single rw.sd of 0.02 is unlikely to be appropriate for all parameters simultaneously. The non-convergence of H_0 and sigma_nu may partly reflect poorly calibrated rw.sd values.

**Fix:** Discuss how rw.sd values were selected. Consider running a pilot local search to calibrate rw.sd from the empirical standard deviation of the converged parameter distribution.

---

### 12. Global Search Box for mu_h Is Inconsistently Narrow

The local search uses a starting value of mu_h = -5, but the global search box for mu_h is `c(-1, 0)`. This box does not include the starting value from the local search and may not include the region where the MLE lies. This is a potential box misalignment (as described in the pomp-global-search-box-misalignment skill) and could explain why the global search does not substantially improve on the local search.

**Fix:** Examine what values of mu_h the local search converges to across replicates, and set the global search box bounds to bracket those values with a generous margin. If the local search converges to mu_h near -5, the global box should extend well below -1.

---

### 13. Stationarity of Log-Returns Not Formally Tested

The paper visually inspects the log-return series for stationarity but does not report a formal unit-root test (ADF, KPSS, or Phillips-Perron). Formal stationarity testing is standard practice before fitting ARMA models, and the GME series has the unusual feature of an extreme spike in January 2021 that may affect standard test statistics.

**Fix:** Report at least an ADF or KPSS test on the log-return series. Discuss any implications for the assumed stationarity of the ARMA model.

---

### 14. Model Equation Notation Error

The model equations define beta_n = Y_n * sigma_eta * sqrt(1 - phi^2), but Y_n is also defined as the observed measurement variable. In the POMP implementation, `Y_state` (the state variable) is used in the rproc1 Csnippet for computing beta, while `y` (the observed variable) is used in the measurement model. The text equation should clarify that beta_n uses the *previous* observed return (y_{n-1}), which is passed in as a covariate (`covaryt`) in the filter version.

---

### 15. No Discussion of Model Limitations Regarding the Unprecedented Price Spike

The GameStop price spike in January 2021 is extreme and unprecedented within the data period. The paper does not discuss whether the stochastic volatility model — which assumes smooth random-walk dynamics for the log-volatility process — is appropriate for a series with such a concentrated shock. No sensitivity analysis or model variation (e.g., adding a jump component) is considered. This is a substantive limitation on the scientific interpretation of the results.

**Fix:** Acknowledge in the discussion that the Breto (2014) model does not include jump components. Discuss whether the extremely high log-likelihoods at the spike are consistent with the model's Gaussian measurement assumption or whether outlier periods depress the fit.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project06/blinded.Rmd`
