# Peer Review: W22 Project 01
**Title:** Investigation of Online Player Increase in CS Caused by COVID-19 Pandemic

---

## Summary

This project investigates whether COVID-19 lockdowns drove an increase in CS:GO online player counts using daily Steam data from January 2020 to January 2022. The authors treat the log-return of daily player counts as a financial "return" series and fit (1) an ARIMA(5,1,5) benchmark, (2) a GARCH(5,5) model, and (3) a stochastic leverage (POMP) model adapted from the Breto (2014) framework. While the framing is creative and the POMP implementation is structurally correct in several respects, the analysis has serious methodological and interpretive deficiencies: the log-likelihood comparison across models is invalid, the global IF2 search is initialized incorrectly, several key parameters fail to converge, no profile likelihoods are computed, and the conclusion inverts the log-likelihood ranking. The study makes no formal inference about the COVID-19 question motivating it, and the scientific connection between the motivating question and the chosen model is never established.

---

## Major Issues

### 1. Invalid cross-model log-likelihood comparison (SARIMA-POMP and GARCH-POMP)

The conclusion table compares log-likelihoods from ARIMA(5,1,5), GARCH(5,5), and the POMP stochastic leverage model directly as if they are on the same scale. They are not. The ARIMA model uses a Gaussian likelihood on the first-differenced demeaned log-return series; the GARCH model uses its own Gaussian likelihood on the demeaned series; the POMP model uses a Gaussian likelihood on Y_state values passed as covariates. These three likelihoods are evaluated on different effective observation models and different data transformations and cannot be ranked numerically without a common observation model on the same data. The conclusion that "ARIMA(5,1,5) performs the best with the highest log likelihood of about 1439.535" is therefore statistically invalid. Per the sarima-baseline-audit skill: a valid comparison requires either a common observation model, or a proper scoring rule (e.g., CRPS) evaluated on the original scale.

Additionally, note that the ARIMA log-likelihood reported in the code is computed as `ARIMA515$loglik - sum(log_df2$demean_players)`, which subtracts the sum of observations from the ARIMA log-likelihood. This non-standard adjustment further invalidates the comparison.

### 2. Global IF2 search initialized from previous mif2 result, not base pomp object

In the global box search chunk, the call is `mif2(if1[[1]], params=apply(GME_box,1,function(x)runif(1,x)), ...)`. Passing `if1[[1]]` (a previous mif2 result) as the first argument rather than the base pomp object `sim1.filt` means each global replicate inherits the cooling schedule from the local search's final state. The cooling perturbations from the inherited chain have already decayed substantially, so the global search effectively performs very few meaningful IF2 steps from each new random start. The reported "global maximum" of 1280 may not represent a genuine global optimum but rather the local-search solution explored with marginally different random starts. Per the pomp-global-search-init-audit skill, the fix is to replace `if1[[1]]` with `sim1.filt` in the global search loop.

### 3. Non-convergence of most parameters in both local and global searches

The authors explicitly acknowledge that "$\mu_h$, $\phi$, $\sigma_\eta$, $G_0$ and $H_0$ do not converge at all" in the global search diagnostics. Out of six parameters, only $\sigma_\nu$ converges. Yet no action is taken: no adjustment to Np, Nmif, or the box boundaries is made, and the reported MLE from a non-converged search is presented as the model's fit. Per Wheeler et al. (2024) §Computational adequacy, convergence diagnostics must be presented and convergence must be achieved before drawing any inference. The reported log-likelihood of 1280 from an unconverged search cannot be taken as a meaningful MLE estimate.

### 4. No profile likelihoods; parameter identifiability unassessed

No profile likelihoods are computed for any parameter. Without these, it is impossible to determine whether any of the six model parameters ($\sigma_\nu$, $\mu_h$, $\phi$, $\sigma_\eta$, $G_0$, $H_0$) are identifiable from the data. The non-convergence documented in Issue 3 is consistent with a flat or poorly-shaped likelihood surface, but this is never examined. Per Wheeler et al. (2024) §Parameter identifiability, profile likelihoods and MCAP confidence intervals must be reported for at least the scientifically key parameters.

### 5. Conclusion inverts model ranking on log-likelihood

The Conclusion states: "We find that the ARIMA(5,1,5) perform the best with the highest log likelihood of about 1439.535." Even granting the invalid cross-model comparison on its own terms, this conclusion is self-contradictory: the table shows ARIMA at ~1439, GARCH at 1170, POMP-fixed at 1277, POMP-randomized at 1280. The ARIMA value is the largest, which the authors correctly identify as "best." However, the body of the results section (after the global search) states the POMP model log-likelihood of 1277 as if it were preferred over GARCH (1170), while simultaneously the conclusion declares ARIMA the winner. This creates an inconsistency: if the ARIMA is best and the comparison is valid, then the entire POMP modeling exercise did not improve on the baseline — a key finding that is buried and not discussed.

### 6. No benchmark comparison appropriate for the mechanistic model

The project frames ARIMA as a "benchmark" but then does not use it to evaluate whether the POMP model captures meaningful structure beyond the benchmark. Per Wheeler et al. (2024) §Benchmark comparison, the comparison should be quantitative and on a common evaluation scale. Here, the POMP model's log-likelihood is actually lower than ARIMA's, which — if the comparison were valid — would indicate the mechanistic model fails to beat the benchmark. This critical finding is not discussed.

### 7. No connection between motivating question and model

The introduction frames the project as an investigation of how COVID-19 affected CS:GO player counts. However, the stochastic leverage model (Breto 2014) is a financial volatility model with no epidemiological or behavioral components. There is no variable for lockdown policy, vaccination rates, or any COVID-related covariate. The model cannot answer the stated research question. The project never explains what inference the leverage model provides about the COVID-19 effect, nor does it provide any statistical test or parameter comparison before and after the COVID-19 onset.

### 8. Filtering on simulated data rather than original data for the initial particle filter evaluation

The code creates `sim1.filt2` by filtering on data from `sim1.sim` (a simulation from the model at initial guess parameters) rather than on the actual observed data. The log-likelihood estimate of 518.39 reported in the text — "We carry out replicated particle filters at our initial guess of the parameters. We obtain a log likelihood estimate of 518.3896817" — is therefore not the log-likelihood of the model evaluated on observed CS:GO data, but on simulated data. This is a diagnostic step for the simulated data system (checking that the filter can recover parameters) but is presented without this distinction, which is misleading. All subsequent mif2 calls use `sim1.filt` (the filter on real data), so the local and global searches are on the correct object, but this intermediate step creates confusion.

---

## Minor Issues

- **GARCH model misspecification in text vs. code.** The text says "we utilize GARCH(5,5)" but the equation displayed shows a GARCH(1,1) form ($V_n = \alpha_0 + \alpha_1 Y_{n-1}^2 + \beta_1 V_{n-1}$). The `garch()` function call `garch(log_df2$demean_players, grad="numerical", trace=FALSE)` uses default order (1,1), not (5,5). The stated model order is inconsistent with the code and the displayed equation.

- **Seasonal ARIMA period not used in the final model.** The grid search explores seasonal ARIMA models with period=7 (consistent with the weekly cycle identified in the ACF and spectrum). The best seasonal model (SARIMA(5,5)(1,0,1)[7]) achieves AIC -2938, substantially better than ARIMA(5,1,5). Despite this, the authors retain ARIMA(5,1,5) as the benchmark, citing "simplicity" and "not much difference in AIC," when in fact the SARIMA AIC is approximately 97 units lower. The benchmark choice disadvantages the authors' own conclusions.

- **ARIMA log-likelihood adjustment is unexplained and non-standard.** The code computes `ARIMA515_loglik = ARIMA515$loglik - sum(log_df2$demean_players)`. Subtracting the sum of observations is a Jacobian correction for a log-transform, but this is not documented or explained in the text. If applied, it should also be applied consistently to the GARCH and POMP likelihoods for a fair comparison.

- **Initial simulation comparison uses log_df (original series) instead of log_df2 (demeaned returns).** The plot "Observed returns and simulated returns" overlays `Y_state` from the simulation against `log_df$log_diff` (non-demeaned log-returns), while the model was trained on `log_df2$demean_players` (demeaned returns). This is a variable mismatch in the visualization.

- **No effective sample size (ESS) monitoring.** ESS is not reported for any particle filter run. For a run with Np=2000, ESS collapse would indicate model-data mismatch, a critical diagnostic per Wheeler et al. (2024).

- **Pairs plot uses log-transformed sigma_nu in global search but raw in local search.** The local search pairs plot uses `~logLik+sigma_nu+...` while the global search uses `~logLik+log(sigma_nu)+...`. This inconsistency makes the plots non-comparable and may mask identifiability issues in the local search.

- **Research question is not answered.** Despite the title claiming to "investigate" the effect of COVID-19, the paper provides no statistical answer to this question — no event study, no structural break test, no comparison of pre- and post-COVID player dynamics.

- **Figure numbering gap.** Figures are labeled 1-5 in the EDA section, then jump to Figure 7 for the benchmark fitted values. Figure 6 is never defined.

- **Computational cost not reported.** No information is given on run time, CPU-hours, or node configuration for the IF2 searches, making it impossible to assess whether sufficient computation was performed.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project01/blinded.Rmd`
