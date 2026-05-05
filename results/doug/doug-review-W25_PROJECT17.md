# Peer Review: W25 Project 17
## Time Series Analysis of New York Harbor Conventional Gasoline Regular Spot Price

---

## Summary

This project fits two stochastic volatility (SV) models — a leverage model following Breto (2014) and a basic no-leverage SV model — to monthly log-returns of New York Harbor conventional gasoline spot prices (June 1986 to March 2025), with modifications including a Student-t measurement model and hardcoded regime-shift amplitudes for the 2008 recession and 2020 pandemic periods. Both models are estimated via the pomp framework (IF2 / iterated filtering), and a GARCH benchmark is added for comparison. The central hypothesis is that gasoline prices exhibit weaker leverage effects than freely traded assets.

**Key strengths:** The project uses proper likelihood-based inference (IF2 + particle filter evaluation), a well-structured two-stage local/global search, a quantitative model comparison table with AIC, and an honest self-critique of the hardcoded event-timing design flaw.

**Key weaknesses:** The global searches for all three POMP models use a previous mif2 result as the first argument to mif2, anchoring all global replicates to the local-search solution; the log-likelihood comparison between the SV and GARCH models is invalid because they use different observation models (t-distribution on different scales); the regime-amplitude modification introduces look-ahead bias by hardcoding event windows derived from inspection of the data; the project reports filtered log-likelihoods computed on simulated data as if they were benchmarks on the real data; and no profile likelihoods are computed for any parameter.

---

## Major Issues

### 1. Global search uses previous mif2 result as first argument to mif2 — all three models

For all three POMP models, the global search is structured as:

```r
if.box <- foreach(i=1:Nreps_global,
  .packages='pomp',.combine=c) %dopar% {mif2(if1[[1]],
    params=apply(...box..., ...))}
```

The first argument is `if1[[1]]` — a previous mif2 result object from the local search — rather than the base pomp object (`N_breto_filt`, `T_breto_filt`, `T_basicSV_filt`). This causes the global search to inherit the cooling schedule and internal IF2 state from `if1[[1]]`. Because the local search already ran `Nmif = 200` iterations, the cooling schedule at `if1[[1]]` is near its end state. The new random starting parameters drawn from the box are applied (via `params=`), but the perturbation sizes have already decayed to near zero, so the optimizer performs essentially no exploration from those new starting points. The 100 global replicates are therefore not genuine global searches — they are near-zero-perturbation continuations from the local-search cooling state at diverse but unexplored starting points.

As a consequence, any claim that the global search confirmed or improved upon the local-search MLE should be treated with caution. The pairs plots from the global search (Figures 6, 11, 16) may cluster near the local optimum regardless of the box bounds, not because the global optimum truly lies there, but because no genuine global exploration was performed. The maximum log-likelihoods reported (429.8, 437.1, 434.8) may not represent the true global MLE for any of the three models.

**Fix:** Replace `mif2(if1[[1]], params=...)` with `mif2(base_pomp_object, params=...)` in all three global search loops, using `N_breto_filt`, `T_breto_filt`, and `T_basicSV_filt` respectively.

---

### 2. Log-likelihood comparison between SV and GARCH models is invalid

Section 2.6 compares the modified basic SV model (log-likelihood 434.8) to T-GARCH(3,1) (log-likelihood 435.509) and concludes "the T-GARCH model achieved a higher log-likelihood, suggesting it may be better suited." This numerical comparison is not valid. The GARCH likelihood is evaluated by `garchFit(..., cond.dist="std")` — a Student-t on the demeaned returns via the GARCH variance — while the SV log-likelihood is evaluated by a particle filter using `dt(y/exp(H/2), df, give_log) - (H/2)` on the same demeaned returns, but with a latent volatility process. These are different probability models: the GARCH likelihood integrates out volatility analytically through the GARCH recursion, while the SV likelihood marginalizes numerically over the latent log-volatility. They are both evaluated on the same observed returns, so in principle one could compare them. However, it is unclear whether the denominators (Jacobians) are handled identically in `garchFit` and in the custom dmeasure. In the SV dmeasure, the term `- (H/2)` is the Jacobian for the change of variables from the standardized t to Y. If `garchFit` handles this transformation internally (which it does, via the GARCH standard deviation), and if both return log-likelihoods in the same unit (log-density of the observed returns), the comparison may be numerically valid. But the authors do not verify this equivalence, and the T-GARCH model includes a mean parameter (`include.mean=T` in the second fit), while the SV model assumes zero mean — introducing an unfair degree-of-freedom advantage to the GARCH. The conclusion that T-GARCH "outperforms" the SV model therefore rests on an unverified and potentially unequal comparison. See Wheeler et al. (2024) §3 for discussion of comparable observation models.

**Fix:** Verify that both log-likelihoods are in the same units (log-density of the observed demeaned returns). Remove the mean parameter from the GARCH fit (use `include.mean=F` consistently) or add a mean to the SV model. If any Jacobian discrepancy exists, add the corresponding adjustment to the reported log-likelihoods before comparing.

---

### 3. Hardcoded event windows introduce look-ahead bias

The regime-amplitude modification in equations (6) of the text hardcodes the intervals `t ∈ [262, 275]` (2008 recession) and `t ∈ [400, 410]` (2020 pandemic) as the periods of amplified volatility, with multipliers 0.8 and 1.2. These intervals and multipliers were determined by visually inspecting Figure 2, as stated in the paper: "The multipliers (0.8 and 1.2) reflect the empirically observed difference in volatility magnitudes between these events." This procedure looks at the data before fitting the model and incorporates knowledge of specific event timing and relative magnitudes into the model. The hardcoding is not a genuine parameter — it is effectively a form of data-driven model specification that is never cross-validated. The authors acknowledge this as "a serious mistake" in Section 4 and propose a probabilistic alternative (Weibull-based event timing). However, the consequence for the reported results is not adequately quantified: the improved ESS (from < 10 to > 300) and the higher log-likelihood of the modified models relative to the base Breto model are at least partially attributable to the hardcoded regime adjustment rather than to genuine model improvement. Any claim that the modified SV model "better captures" the dynamics therefore cannot be cleanly separated from the benefit of the hardcoded interventions.

**Fix:** At minimum, treat the event boundaries and multipliers as free parameters estimated via IF2, or implement the probabilistic event-timing model sketched in Section 4. If the hardcoded model is retained for the final analysis, report the log-likelihood of the unmodified Breto model and the GARCH model to provide a baseline against which the look-ahead benefit can be assessed.

---

### 4. Initial filtered log-likelihoods are reported for simulated data, not real data

Sections 2.2.2, 2.3.2, and 2.4.2 each state a filtered log-likelihood at initial parameters, e.g., "we computed the filtered log-likelihood as 410.657 (SE = 0.079) for the simulated data." These log-likelihoods are computed on `N_breto_sim1.filt`, `T_breto_sim1.filt`, and `T_basicSV_sim` — all of which are pomp objects constructed from simulated trajectories, not from the actual gasoline return data. The values 410.657, 457.797, and 472.035 are not benchmarks for model fit to the real data; they are filtered likelihoods for a model applied to its own simulated output. Presenting these alongside the IF2 search likelihoods (429.8, 437.1, 434.8 from real data) without clearly distinguishing them misleads the reader into believing there is a meaningful numerical comparison between initial and optimized fits. This matches the `pomp-simdata-benchmark-error` pattern.

**Fix:** Clearly label all three initial log-likelihoods as "on simulated data — not comparable to real-data log-likelihoods." If an initial log-likelihood on real data is desired, run `pfilter(N_breto_filt, params=N_breto_params_test, Np=Np)` and report that value.

---

### 5. No profile likelihoods computed for any parameter

No profile likelihood calculations are reported for any parameter across any of the three POMP models. The key scientific claim — that the leverage effect is absent, evidenced by `sigma_nu` approaching zero — is stated qualitatively from the pairs plot (Figure 11) but is not supported by a formal profile likelihood or confidence interval. Without a profile likelihood for `sigma_nu`, it is unknown whether the data can distinguish `sigma_nu ≈ 0` from `sigma_nu > 0` at any meaningful significance level. The observed convergence of `sigma_nu` to small values could reflect genuine non-identifiability (sigma_nu is unidentifiable from these data) rather than evidence of no leverage effect. This is exactly the kind of misinterpretation that profile likelihoods are designed to prevent (Wheeler et al. 2024 §5: "Implausible parameter estimates flagged as potential signs of model misspecification").

**Fix:** Compute profile likelihoods for `sigma_nu` (the leverage parameter) and `phi` (persistence) in the modified leverage model. The profile over `sigma_nu` is the minimum needed to assess the leverage hypothesis.

---

### 6. No non-mechanistic benchmark comparison for the POMP models

The paper does not compare either POMP model against a non-mechanistic benchmark on equal footing. The T-GARCH comparison (Section 2.6) is the closest attempt, but as noted in Issue 2, it is methodologically compromised. There is no ARMA or auto-regressive model comparison, no regime-switching ARMA, and no GARCH(1,1) with the same t-distribution. Wheeler et al. (2024) §2 state: "None of the 32 papers in their Haiti cholera literature review performed such a comparison. Their auto-regressive negative binomial benchmark revealed that some models failed to beat it." The paper should demonstrate that the POMP SV model captures structure that a simpler time series model cannot. Without this, the added complexity of the latent volatility process cannot be justified on empirical grounds.

**Fix:** Fit an AR(p)-t model or GARCH(1,1)-t on the same demeaned returns using a likelihood evaluated in identical units. Report the comparison as an AIC table with the same observation-model convention.

---

### 7. tau and amplitude parameters lack parameter transformation (partrans) declarations

The `T_breto_partrans` and `T_basicSV_partrans` objects declare `log` transforms for `sigma_eta`/`sigma_nu`/`sigma` and a `logit` transform for `phi`, but do not declare any transformation for `tau` or `amplitude`. These parameters have implicit domain constraints: `tau` should be positive (indeed constrained to (0, 60)), and `amplitude` is used as a signed multiplier but is likely intended to be positive. Without a `log` transform on `tau`, IF2 perturbations on the untransformed scale can push `tau` below zero. The Csnippet clamping (`nearbyint(tau) < 1 ? 1 : ...`) prevents a runtime crash but silently distorts the optimization: the effective parameter space for `tau` has a non-smooth boundary at 0 that the unconstrained IF2 walk cannot respect. Similarly, `amplitude` has no declared lower bound, so IF2 can freely explore negative amplitudes, which would reduce rather than increase `mu_h` during the event windows — a biologically unintended direction.

**Fix:** Add `log = c("tau", "amplitude")` (or `logit` if bounded) to the `parameter_trans()` calls for both `T_breto_partrans` and `T_basicSV_partrans`.

---

### 8. Model comparison AIC table uses hardcoded log-likelihoods not computed from the same data or model version

In Section 2.5, the AIC table is constructed with `LogLik = c(437.1, 434.8)` — hardcoded values copied from the narrative text rather than extracted from the live R objects. This means the AIC values displayed in the kable output are not reproducibly linked to the computation. If the analyses were rerun with different seeds or at a different run level, the hardcoded values would not update, producing an inconsistency between the displayed AIC table and the actual results. The parameter counts are computed from `length(T_breto_paramnames)` and `length(T_basicSV_paramnames)` (8 vs. 5), which are live — but the log-likelihoods are frozen.

**Fix:** Extract the maximum log-likelihood from the live result objects (e.g., `max(r.box$logLik)`) rather than hardcoding the values, so the AIC table updates automatically with the computation.

---

### 9. Inadequate model diagnostics — no conditional log-likelihood plot, no filtering distribution plot

The only diagnostics presented are ESS traces (from the mif2 plot calls) and the pairs plots. There is no conditional log-likelihood plot showing where in time the particle filter struggles most, and no comparison of filtering-distribution simulations to the observed returns. The ESS drops to below 10 at t = 405 for the base Breto model, which the authors correctly identify as problematic, but this diagnosis is based on a single ESS plot rather than on a conditional log-likelihood decomposition that would reveal whether specific time points (e.g., t = 275, t = 405) account for the majority of the model's misfit. Wheeler et al. (2024) §4 note that "conditional log-likelihood plots led to discovery that Model 3 could not explain the cholera surge during Hurricane Matthew."

**Fix:** For the best-fitting model (modified basic SV), compute per-observation filtered log-likelihoods by running pfilter with `filter_mean=TRUE` and examining the log-likelihood contributions by time. This would directly quantify how much of the total log-likelihood deficit is attributable to the 2008 and 2020 events.

---

### 10. Daily data loaded in Section 2.1 but only used for a visualization — no analysis justification

Section 2.1 loads a daily gasoline price series (`Daily_New_York_Harbor_Conventional_Gasoline_Regular_Spot_Price_FOB.csv`) and plots it alongside the monthly series in Figure 2, but no daily analysis is performed. The text states "our analysis focuses on monthly prices." The daily data file is referenced in the Rmd but not provided in the project folder (only the monthly CSV is present). This creates a missing-file dependency: if someone attempts to render the document, the daily data chunk will fail. The file inclusion also suggests the authors considered but did not pursue a daily-frequency analysis, which given the substantial aggregate volatility of monthly returns (ESS collapse at the pandemic) would have been a natural robustness check.

**Fix:** Either include the daily data file in the submission or wrap the daily data chunk in `tryCatch()` and remove the claim that daily analysis could reduce outlier effects (since it was not performed).

---

## Minor Issues

- **Simulated log-likelihood notation mismatch.** The text in 2.2.2 states $\theta_0 = (\sigma_\nu, ...) = (\exp(4.5), ...)$ but the code sets `sigma_nu = exp(-4.5)`. The exponent sign is negative in the code but positive in the text equation for all three models. This is either a typo in the narrative or in the code; the values are of different magnitudes and the correct initialization should be stated unambiguously.

- **`tau` receives rw.sd = 1 in the modified models.** In the local search for both `T_breto` and `T_basicSV`, `tau = 1` is set in `rw_sd(...)`. The starting value of `tau` is 5. A perturbation SD of 1 on a parameter with value 5 (20% of its value, untransformed) is large relative to the typical rw.sd values of 0.02 used for other parameters. The Csnippet clamps `tau` to integers (via `nearbyint`), further complicating the gradient for the particle filter. This likely contributes to noisy convergence of `tau`.

- **`write.table` appending in local and global CSV export chunks is never read back.** The `write.table(..., append=TRUE)` calls for saving parameters to CSV files (e.g., `N_breto_params_3.csv`) appear in `eval=FALSE` chunks, meaning they are never executed during rendering. Simultaneously, there is no corresponding `read.csv` of these files for subsequent analysis. The CSV accumulation pattern is thus vestigial code that serves no purpose in the submitted document.

- **GARCH AIC table selection has numerical tie-breaking ambiguity.** The code uses `which(aic_table == min(aic_table), arr.ind=T)` to select the best GARCH order. If two models tie in AIC (which can happen with three decimal places of precision), this will select both, and the subsequent `p = index[1]` will take the first row — but the behavior is undefined if the tie resolution is row-order dependent. A more robust approach would use `which.min` on the vectorized table.

- **No seasonal decomposition of the volatility time series.** The STL decomposition in Section 2.6 is applied to the log-return series (demeaned returns), which is approximately mean-zero and by construction has no trend. The result is a seasonal component with very small amplitude. A more informative decomposition would apply STL to the squared returns (as a proxy for volatility), which would reveal whether volatility itself is seasonal — the object of concern given gasoline's well-known summer/winter price seasonality. The current figure does not directly support the conclusion that the models "fail to account for seasonal patterns."

- **Parameter estimates not reported in any table.** The final estimated parameter values for any of the three models are not summarized in a table or in the text. The best-fit parameters from the global search can be inferred from the pairs plots, but no explicit MLE table is provided. Wheeler et al. (2024) §10 recommend archiving final parameter estimates as standalone files.

- **Missing file `Daily_New_York_Harbor_Conventional_Gasoline_Regular_Spot_Price_FOB.csv`.** The project folder contains only `New_York_Harbor_Conventional_Gasoline_Regular_Spot_Price_FOB.csv`. The daily data file referenced at line 127 of the Rmd is absent. The document will fail to render completely without this file (though the chunk error may be suppressed by `warning=FALSE`).

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
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project17/blinded.Rmd`
