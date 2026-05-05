# Peer Review: W25 Project 12
## "Comparative Analysis of Volatility Models for Daily Gold Prices"

---

## Summary

This paper applies three model families — ARIMA, GARCH (with Normal and Student-t innovations), and two POMP specifications (Heston stochastic volatility and a Markov regime-switching model) — to daily gold log-returns from 2022–2024. The main claimed contribution is a level comparison of all models on the same 772-day window and the addition of latent-state diagnostics (profile likelihoods and mif2 convergence traces) that earlier student projects reportedly lacked. The paper finds that Student-t GARCH(1,1) achieves the highest log-likelihood of the five models and is deemed the most efficient choice. Genuine strengths include: use of likelihood-based inference for POMP models via `mif2` + particle filter evaluation, construction of at least one profile likelihood per POMP model, and acknowledgment of key limitations (leverage effects, intraday data). The evaluation is, however, substantially weakened by a cross-family likelihood comparison that is statistically invalid, biologically implausible parameter estimates that are dismissed without justification, a profiling workflow with only one restart per grid point and no confidence interval computed, a regime-sequence plot based on unconditional simulation rather than the particle-filter distribution, and several labeling and notation errors.

---

## Major Issues

### 1. Invalid direct comparison of ARIMA, GARCH, and POMP log-likelihoods

Table 5 places ARIMA(2,0,2), GARCH(1,3)-Normal, GARCH(1,3)-t, Heston POMP, and Regime-Switch POMP on a single log-likelihood scale and draws the conclusion that Student-t GARCH is the best model. This comparison is not statistically valid. The ARIMA log-likelihood is evaluated under a Gaussian model on the already-differenced log-return series (using `arima()`, which maximizes the conditional log-likelihood of the innovations). The GARCH log-likelihood is computed by `ugarchfit()` using a per-observation score that sums over the same data. The POMP log-likelihood is estimated by a particle filter on the same log-return series under a conditionally Gaussian or normal measurement model. Although all three evaluate something proportional to a log-likelihood on the same data, the ARIMA model's `$loglik` field in R's `arima()` is the *concentrated* Gaussian log-likelihood and the GARCH `LLH` field from `rugarch` reports the sum of log-densities of the standardized residuals — not the marginal likelihood of the observation series. These quantities are not on a common scale, and a one-number comparison does not identify the best model. The authors should either (a) evaluate all models via the same scoring rule applied to the same held-out data (e.g., log-score on a validation window), or (b) restrict comparisons within each model family (ARIMA vs. SARIMA; GARCH-Normal vs. GARCH-t; Heston vs. RS), noting that cross-family LL comparison requires identical observation models and data transformations (Wheeler et al. 2024, §3).

### 2. Negative estimates of sigma and v0 in the Heston model dismissed without justification

The Heston model is defined such that v_t is the instantaneous variance. The parameter sigma governs the volatility of variance and must be strictly positive (sigma > 0) for the model to be well-defined; v0 must also be positive. The reported MLE from the global search is sigma = -0.0051 and v0 = -2.38e-5 (Section 5.1). The authors acknowledge these negative values are "concerning" but wave them away as falling "within acceptable ranges given the variability inherent in the particle filtering process." This is not a valid dismissal: sigma < 0 and v0 < 0 are outside the mathematical domain of the Heston model. A properly specified POMP implementation should either (a) apply log-transformations to sigma and v0 via `parameter_trans(log = c("sigma", "v0"))` and work on the log scale during IF2, or (b) include hard-coded lower bounds in the Csnippet (the existing `if (v < 1e-6) v = 1e-6` guard does not prevent sigma from being negative). The fact that the optimizer crossed the domain boundary indicates that no parameter transformation is declared: there is no `partrans` argument in the `heston_model` `pomp()` call or in the `mif2()` calls. All parameter estimates from the Heston model are therefore unreliable, because the optimizer explored regions outside the model's feasible domain without constraint. This also means the global search effectively ran without the logit/log constraints that would keep sigma and v0 positive.

### 3. Profile likelihood uses a single restart per grid point with a single pfilter evaluation; no confidence interval is reported

For both the Heston (kappa profile, Section 5.1) and RS (log_sigma2 profile, Section 5.2) models, the profile is computed by running exactly one `mif2()` call per grid point, starting from `coef(best_mif)` modified by the fixed parameter value, followed by a single `pfilter()` evaluation with Np = 5000. This workflow has three compounding deficiencies identified in `pomp-profile-single-restart-audit`:
- A single particle filter evaluation introduces Monte Carlo noise of 1–3 log-likelihood units for a 772-observation dataset, which can dominate the profile signal near the peak and produce spurious kinks.
- Starting every profile point from the single global best MLE (with the profiled parameter forced to the grid value) provides no guarantee that the constrained optimum is found at each grid point. Multiple restarts from diverse parameter combinations are required (Wheeler et al. 2024, §5).
- Neither profile is used to compute a confidence interval via the chi-squared threshold. The paper reports qualitative descriptions ("relatively flat," "steep decline") but never applies the `max(loglik) - 0.5*qchisq(0.95, df=1) = max(loglik) - 1.92` cutoff. The entire stated purpose of the profile — to assess identifiability and report a CI for kappa and sigma2 — is therefore unfulfilled.

### 4. Regime sequence plot uses forward simulation, not the filtering distribution

The "Inferred Regime Over Time" plot (Section 5.2) is generated by `simulate(rs_model, params = coef(best_mif), nsim = 1, include.data = TRUE)`, which draws a single unconditional forward simulation from the initial conditions — it does not condition on the observed data. The label "Inferred" is therefore incorrect: this is not an inference about the latent regime sequence. To infer the regime sequence, the authors must run `pfilter()` on the fitted RS model and extract the particle-weighted expected value of the regime state at each time point (the filtering distribution). Using `simulate()` for this purpose produces a regime sequence that is statistically independent of the observed gold returns, rendering the plot scientifically meaningless as a diagnostic. Wheeler et al. (2024, §Model diagnostics) identify reconstruction of latent variables from the filtering distribution as a key diagnostic step.

### 5. No benchmark comparison of the mechanistic POMP models against non-mechanistic alternatives

Although the paper includes ARIMA and GARCH models, these do not constitute a proper non-mechanistic benchmark for the POMP models in the sense of Wheeler et al. (2024, §2). A non-mechanistic benchmark for a stochastic volatility model should be an ARMA model fitted to the squared or absolute returns, or an AR-GARCH model (which directly models the conditional variance without treating it as a latent state). The paper's comparison conflates the benchmark role: it presents ARIMA as a baseline for the mean dynamics but does not compare the POMP stochastic volatility models against a correctly specified GARCH model that makes the same observation-model assumptions. Because GARCH actually outperforms both POMP models on the reported numbers (even granting the invalid cross-family LL comparison), the paper's claim that "POMP frameworks add narrative colour but only a modest statistical edge" is based on a confounded comparison (different observation models, different numbers of parameters, and potentially different effective likelihoods).

### 6. Regime-switching model's transition probability p11 near 0.5 implies near-random regime switching, contradicting financial theory

The fitted logit(p11) = 0.09 implies p11 = expit(0.09) ≈ 0.522, meaning the model is in Regime 1 (low-volatility) one period and has only a 52.2% chance of remaining there the next period. This is essentially a coin flip — the low-volatility regime has essentially no persistence. The authors note this in passing but claim it is "consistent with financial theory that volatility spikes tend to persist once triggered" — which actually describes *high*-volatility persistence (p22 = 0.80), not the near-random behavior of the low-volatility regime. A p11 near 0.5 is a sign of model misspecification or label-switching (the two regimes may not be identified from one another in a statistically stable way). The paper provides no diagnostic test for regime identifiability, no confidence interval for p11 or p22, and does not check whether the estimated p11 value differs significantly from 0.5 (i.e., from no regime persistence). This is especially important because the RS model's highest reported log-likelihood (2539.7) barely exceeds the Heston model's (2536.8) despite having two additional parameters, suggesting that the regime structure is not providing a meaningful improvement.

---

## Minor Issues

### 7. Figure numbering is inconsistent

The section on volatility clustering (Section 4, first paragraph) reads "we examine the ACF of squared log returns (Figure 3)" but the figure that follows this reference (line 249) is labeled "Figure 3. ACF of Squared Log Returns" — which duplicates the label used earlier (line 129) for the log-return time series plot. There are at least two distinct figures labeled "Figure 3." The figure presented in the GARCH section showing the ACF of squared log returns is not the same as the log-return series plot. Consistent, sequential figure numbering should be used throughout.

### 8. ARIMA model description contains an inconsistency about the mean specification

Section 3.1 describes the goal as finding the best ARMA(p, q) model, and the AIC grid search selects ARIMA(2,0,2). Section 4.1 then defines the GARCH model with mean specification ARMA(2,2), and Section 4.3 refers to the mean model as "ARMA(1,1)+GARCH(1,1)" in the diagnostic discussion (line 345, 354). The `ugarchspec` calls use `armaOrder = c(2, 0, 2)` for the GARCH-Normal model but the text in Section 4.2 describes a "benchmark ARMA(1,1)+GARCH(1,1)" (line 359). The inconsistency between (2,0,2), (2,2), and (1,1) ARMA specifications creates confusion about which mean specification is actually used in the GARCH models.

### 9. Regime-switching model: the rw_sd for the global search reuses the local-search object without adjustment

In the RS global search (lines 760–782), the global `mif2()` calls use `rw.sd = rw_sd_vals` which was defined for the local search with `log_sigma1 = 0.005, log_sigma2 = 0.005, logit_p11 = 0.02, logit_p22 = 0.02`. These perturbation sizes are small relative to the scale of the parameters as initialized in the global box (e.g., `log_sigma2` is drawn from `[log(0.005), log(0.1)]`, a range of about 3 units, but the perturbation SD is only 0.005). This mismatch means that the global search particles, once initialized from a random point in the box, can only move very slowly away from their starting values during IF2, which partly defeats the purpose of a broad box initialization. The perturbation sizes for the global search should be calibrated to the box width, not the local-search neighborhood.

### 10. The paper claims ESS trajectories were monitored but no ESS plot is shown

Section 5.1 states "convergence diagnostics and effective sample size trajectories did not indicate particle degeneracy or instability" (line 581). The ESS over mif2 iterations is not shown, and there is no code chunk that computes or plots ESS. ESS monitoring is cited in the Discussion (line 1000) as a distinguishing feature of this project over prior work, but without showing the ESS trajectory or reporting minimum ESS values, this claim cannot be evaluated. If ESS was monitored internally, at minimum the minimum ESS across time and iteration should be reported in the text.

### 11. Heston profile likelihood: pfilter is called on heston_model, not the modified pomp object

In the Heston profile loop (lines 590–614), the `mif2()` call is applied to a modified `pomp()` object (with kappa fixed in params), but the subsequent `pfilter()` call on line 611 passes `heston_model` (the original base object) rather than the modified object. This means the pfilter evaluation uses `heston_model`'s default parameter slots rather than the fitted parameters from `mif_fit`. Since `params = coef(mif_fit)` is supplied explicitly, the params override should propagate correctly — but the inconsistency between the object used for optimization (modified) and the object used for evaluation (original) is a potential source of subtle errors, particularly if the object-level parameter storage differs from what `coef()` returns after optimization. The same issue appears in the RS profile (line 872: `pfilter(rs_p, params = coef(mif_fit), Np = 5000)` uses the modified `rs_p`; this is correct for the RS case but inconsistent with the Heston profile logic).

### 12. No model diagnostics beyond trace plots and profile likelihood

The paper does not examine conditional log-likelihood plots (per-observation contributions to the likelihood), effective sample size trajectories, or comparisons of simulated data against observed data (beyond a single unconditional simulation for the RS regime plot, which is incorrectly labeled as "inferred"). These diagnostics are recommended by Wheeler et al. (2024, §4) and would reveal whether any particular subperiod of the gold return series is driving poor fit in the POMP models — especially relevant given the well-known volatility clustering and occasional extreme moves in 2022–2024.

### 13. The Heston model's sigma and v0 are not constrained to be positive, and the paper does not use parameter transformations

As noted in Issue 2, neither the `heston_model` `pomp()` object nor any `mif2()` call includes a `partrans` argument to enforce positivity of sigma and v0. The regime-switching model likewise does not declare parameter transformations, relying instead on natural parameterizations (log_sigma1, log_sigma2, logit_p11, logit_p22) that are already on an unconstrained scale. The lack of positivity constraints for the Heston model is a specification error; for sigma and v0 to be estimated correctly, they should be estimated on the log scale with back-transformation in the Csnippet.

### 14. Final MLE parameter vectors are not archived; results cannot be reproduced without re-running optimization

The supplement consists of a single Rmd file. No CSV or RDS files containing the final MLE parameter vectors are included. Reproducing the reported results requires re-running `mif2()` with Np = 5000 particles and Nmif = 500 iterations across 20 global replicates for each of two POMP models (plus local searches), which is computationally expensive. Wheeler et al. (2024, §10 and SI §S7) identify archiving final parameter vectors as a minimum reproducibility requirement. The discussion claims the paper improves on prior projects in reproducibility, but this claim is not supported by the absence of archived parameter files.

### 15. The ADF test interpretation states "rejecting the null of stationarity"

Section 2.2 (line 149) states: "If the p-value is less than 0.05, the null can be rejected in favor of stationarity." While this phrasing is directionally correct (a small p-value in `adf.test()` does provide evidence for stationarity), it implicitly frames the null as non-stationarity, which is correct for ADF — but the sentence structure "rejected in favor of stationarity" is slightly imprecise (the null is the unit root, not stationarity directly). More importantly, the paper uses only the ADF test. Best practice (per the stationarity-test-conclusion-audit skill) is to also apply the KPSS test, which has stationarity as its null, so that both a failure-to-reject of KPSS and a rejection of ADF together provide corroborating evidence. Using only ADF leaves the stationarity conclusion one-sided.

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
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project12/blinded.html`
