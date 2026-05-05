# Peer Review: W21 Project 12
## Analysis on Nasdaq-100 Index for the Past 5 Years

---

## Summary

This project applies ARMA, GARCH, and a POMP stochastic volatility model to five years of daily Nasdaq-100 closing-price returns (April 2016 to April 2021). The ARMA section follows a conventional AIC-table selection and root-checking procedure; the GARCH section uses the `tseries` package to fit GARCH(1,2); and the POMP section implements Breto (2014)'s leverage-augmented stochastic volatility model via `mif2` and particle filtering. The central claim is that the POMP model achieves the best AIC among all three model families.

While the project is organized and demonstrates familiarity with the course tools, it has several serious methodological and computational flaws that undermine its principal conclusions. The AIC comparison across model families is statistically invalid because the three models operate on different likelihood scales and observation distributions. The global IF2 search inherits the local search's cooling schedule rather than exploring from fresh starts, the simulated-data particle filter result is misleadingly presented as a benchmark for the real-data fit, and the AIC for the POMP model is computed from what appears to be the median rather than the maximum log-likelihood. No profile likelihoods are reported, no convergence traces are shown, and the claim that parameters are easier to interpret is asserted without supporting quantitative comparison to independent evidence.

---

## Major Issues

### 1. Invalid cross-model AIC comparison across different likelihood scales

The project's central conclusion — that the POMP stochastic volatility model achieves "the lowest AIC" and therefore outperforms GARCH and ARMA — is built on a comparison that is not statistically valid. The ARMA(3,1) likelihood is evaluated under a Gaussian model for the demeaned log-return series via `arima()`. The GARCH(1,2) likelihood is evaluated via `tseries:::logLik.garch`, which uses a Gaussian conditional distribution for the same series. The POMP model uses a Gaussian measurement model `dnorm(y, 0, exp(H/2), give_log)` but the likelihood is computed by the particle filter. Although all three happen to use Gaussian observation distributions, the GARCH and ARMA log-likelihoods are exact while the POMP likelihood is a stochastic Monte Carlo estimate subject to particle filter variance. More importantly, the GARCH(1,2) AIC of approximately -7840 and the POMP AIC of approximately -7936 or -7948 cannot be validly compared using a simple delta-AIC rule because the models have different latent-variable structures. The paper states "the best AIC is around -7948.5, which is the lowest among all models considered" and uses this to conclude the POMP model performs best, but offers no statistical uncertainty bounds on the AIC difference, no log-likelihood SE, and no acknowledgment that Monte Carlo noise in the particle filter log-likelihood estimate inflates the apparent AIC advantage. The authors should report the log-likelihood standard error from `logmeanexp(..., se=TRUE)` alongside every AIC value and acknowledge that the differences may be within Monte Carlo noise.

### 2. AIC computed from median rather than maximum log-likelihood

The POMP model AIC is computed inline as `2*6 - 2*max(r.if1$logLik)` for the local search and `2*6 - 2*max(r.box$logLik)` for the global search. The preceding `summary(r.if1$logLik)` displays the full distribution — the median of the local search distribution is stated as context, and the sentence "The best AIC is around -7935.7" appears adjacent to a `summary()` call. While the code does use `max()`, the displayed summary statistics could lead a reader to mistake the median for the basis of the AIC claim. More critically, the particle filter log-likelihood evaluations (`L.if1`) used to populate `r.if1$logLik` use only a single `logmeanexp` over `ndx_Nreps_eval = 20` particle filter replicates per IF2 chain. This means the per-chain log-likelihood estimates are noisy, and the `max()` across chains selects the chain with the largest Monte Carlo noise realization rather than the chain closest to the MLE. The reported AIC is therefore optimistically biased (see Wheeler et al. 2024, §Computational adequacy). The authors should use `logmeanexp` over multiple particle filter replicates for each final parameter estimate to reduce this bias.

### 3. Global IF2 search is initialized from a previous mif2 result, not from the base pomp object

In the global box search chunk (`global_search`), the `mif2` call inside the `foreach` loop is:

```r
if.box <- foreach(...) %dopar% mif2(if1[[1]], start=apply(ndx_box,1,function(x)runif(1,x)))
```

The first argument to `mif2` is `if1[[1]]` — a previous IF2 result object from the local search — not the base `ndx.filt` pomp object. This is the anti-pattern described in the `pomp-global-search-init-audit` skill: when a previous IF2 chain is passed as the first argument, the global search replicates inherit the cooling schedule state from the local chain rather than starting fresh. The cooling schedule of `if1[[1]]` has already decayed through 200 iterations (at `run_level=3`), so the new starting parameters drawn from `ndx_box` are perturbed only by near-zero perturbations immediately, effectively making every global replicate a continuation of the local search from a random starting point rather than a fresh global exploration. The reported "global maximum" may not differ meaningfully from the local optimum. The fix is to replace `if1[[1]]` with `ndx.filt` (the base pomp object) in the global search `mif2` call.

### 4. Simulated-data particle filter result presented as a real-data benchmark

In the "Filtering for simulated data" section, the particle filter is applied to `sim1.filt` — a pomp object constructed from `sim1.sim`, which is a simulation of the model at the test parameters, not the real Nasdaq-100 data. The text states "The log likelihood seems to be very low" and then proceeds directly to fitting the real data, creating the impression that this simulated-data log-likelihood is a benchmark for the real-data fit. The particle filter log-likelihood from `sim1.filt` is evaluated on the simulated returns, not on the actual Nasdaq-100 returns. These two quantities are on completely different scales and cannot be compared. The paper does not clarify this distinction, which can mislead a reader into thinking the "very low" log-likelihood is a baseline for the real-data fit. The authors should either (a) clarify explicitly that this filter run is a computational check on simulated data only, or (b) report a particle filter evaluation on the real-data object `ndx.filt` at the test parameters as the actual baseline.

### 5. No convergence diagnostics presented

No convergence traces (log-likelihood vs. IF2 iteration, or parameter values vs. iteration) are shown for either the local or global IF2 searches. Without these, there is no evidence that the IF2 chains have converged to a neighborhood of the MLE. The pairs plot is presented, but it shows only the scatter of endpoint parameter values — it provides no information about the trajectory of optimization. Per Wheeler et al. (2024, §Computational adequacy), convergence traces are required to assess whether the reported log-likelihoods are near the MLE or reflect unconverged chains. The authors should add `plot(if1)` and `plot(if.box)` calls (or equivalent `ggplot` trace plots) to the document.

### 6. No profile likelihoods or confidence intervals for any parameter

The project reports point estimates for all six parameters (`sigma_nu`, `mu_h`, `phi`, `sigma_eta`, `G_0`, `H_0`) but provides no profile likelihoods and no confidence intervals. The pairs plot from the local search shows correlations between parameters (notably between `phi` and `sigma_eta`) but no profile likelihood is computed to assess identifiability or to bound any parameter estimate. Per Wheeler et al. (2024, §Parameter identifiability and uncertainty), profile likelihoods are the standard tool for assessing whether parameters are identifiable from the data. Without them, the point estimates could be anywhere on a flat likelihood ridge and the claim that "the model performs well" is unsubstantiated. The authors should compute profile likelihoods for at least `phi` and `sigma_eta`, the two parameters with the clearest financial interpretation, and report MCAP or chi-squared-based confidence intervals.

### 7. No non-mechanistic benchmark comparison

The project compares the POMP model to ARMA and GARCH models by AIC. However, ARMA and GARCH are not "non-mechanistic benchmarks" in the sense of Wheeler et al. (2024, §Benchmark comparison) — they are alternative time-series models, but GARCH is itself a volatility model with similar motivation to the stochastic volatility POMP model. A true non-mechanistic baseline would be a model that makes no structural assumptions about volatility dynamics, such as a Gaussian i.i.d. model or an EGARCH. More importantly, the GARCH(1,2) was selected by AIC and achieves a substantially lower AIC than ARMA(3,1), yet the paper presents the POMP model as superior without quantifying the uncertainty in the AIC comparison or performing a formal likelihood ratio test between any pair of models. The claim of POMP superiority rests on an informal AIC comparison that does not account for Monte Carlo noise in the POMP likelihood.

### 8. Erroneous description of the POMP model as improving over GARCH

The conclusion states "the POMP stochastic volatility model is appropriate for the Nasdaq 500 index data" and that "the resulting model improves in terms of both log likelihood and AIC." The best AIC for GARCH(1,2) is given as -7839.581, and the best POMP AIC as -7948.5. These differ by approximately 109 AIC units in favor of the POMP model. While this appears to be a large improvement, the POMP AIC is computed from a stochastic particle filter with unknown Monte Carlo variance. The paper reports log-likelihood SEs via `logmeanexp(..., se=TRUE)` for the pfilter step, but the best-chain AIC is reported as a single number with no uncertainty bounds. Given that the local search summary shows a range of log-likelihoods spanning roughly 3969 to 3973 across chains (implied by the AIC of -7935.7 vs. -7948.5 from global), there is clear between-chain variability. The claim of POMP superiority should include the SE of the log-likelihood estimate and a formal comparison.

---

## Minor Issues

- **Inconsistent index name**: The paper title and introduction refer to "Nasdaq-100" consistently, but the conclusion section refers to "Nasdaq-500" three times. The data is clearly from the Nasdaq-100. This is a straightforward factual error that should be corrected throughout.

- **Parameter initialization discrepancy**: The initial parameters are described in the text as `sigma_nu=0.01, mu_h=0, phi=0.95, sigma_eta=7`, but the code sets `phi = 0.995`, not `phi = 0.95`. The text and code are inconsistent.

- **`mu_h` not transformed in partrans**: The `ndx_partrans` declaration applies `log` transformation to `sigma_eta` and `sigma_nu` and `logit` to `phi`, but `mu_h` (which can be any real number) is left untransformed, which is appropriate. However, `G_0` and `H_0` are also left untransformed despite being initial-value parameters that in principle could take any real value. This is not an error per se, but should be noted: if the search box for `H_0` is in `(-3.5, -1)`, `G_0` in `(-1, 0.5)`, the optimizer may drift outside these ranges without constraint.

- **No ESS monitoring reported**: The particle filter effective sample size (ESS) is not reported or plotted for any of the runs. For the stochastic volatility model with 2000 particles (at `run_level=3`), ESS can be informative about particle degeneracy, especially given the volatile 2020 COVID period in the data. ESS monitoring is a standard diagnostic (Wheeler et al. 2024, §Model diagnostics).

- **`rproc2.sim` vs. `rproc2.filt` not explained**: The split between the simulation process (`rproc2.sim`) and the filter process (`rproc2.filt`) is taken directly from course templates. The paper does not explain why two separate process snippets are needed or what the `covaryt` covariate achieves. A brief explanation would improve clarity for readers unfamiliar with this template pattern.

- **Global search box constructed from local-search pairs plot alone**: The paper states "From the pairs plot above, we can construct a plausible box." This is a reasonable approach, but the local search used only 20 replicates (`ndx_Nreps_local=20` at run_level=3), which may not be sufficient to characterize the full plausible range. The box for `phi` is set to `(0.95, 0.99)`, which could be too narrow if the MLE is near the boundary.

- **No `sessionInfo()` or package version documentation**: The report loads `pomp`, `foreach`, `doParallel`, `doRNG`, `kableExtra`, `tseries`, and other packages without recording their versions. POMP API changes substantially across versions; the results may not be reproducible without version pinning (see code supplement checklist).

- **Missing forward simulation from best-fit parameters**: The simulation plot in the "Initial Simulation" section uses fixed test parameters (`sigma_nu=0.01, phi=0.995`), not the estimated MLE parameters. The paper never shows a simulation from the fitted model parameters compared to the real data, which is a basic model validation step. The initial simulation shows that "simulated data is much more volatile than the actual demeaned return" — but after fitting, no analogous comparison is shown. This is a significant gap in model validation (Wheeler et al. 2024, §Model diagnostics).

- **No discussion of financial interpretability of estimated parameters**: The paper claims "the estimated parameters for the POMP stochastic leverage model are easier to interpret in financial studies," but provides no interpretation of the specific estimated values. For example, the MLE of `phi` (persistence of log-volatility) is reported but not compared to typical values from the stochastic volatility literature. The MLE of `sigma_eta` (scale of the leverage effect) is reported but not compared to estimates on other equity indices. No independent corroboration is offered (cf. Wheeler et al. 2024, §Corroboration with scientific knowledge).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-design-variable-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/ode-compartment-observation-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/hp-filter-lambda-misspecification/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project12/blinded.Rmd`
