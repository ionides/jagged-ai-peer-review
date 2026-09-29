# Peer Review: W25 Project 17
## Time Series Analysis of New York Harbor Conventional Gasoline Regular Spot Price

---

## Summary

This project applies Breto (2014) stochastic volatility (SV) models within the POMP framework to monthly New York Harbor conventional gasoline spot price data (June 1986 – March 2025, approximately 460 monthly observations). The central hypothesis is that the leverage effect — the negative correlation between returns and subsequent volatility — is more limited in regulated commodity markets than in freely traded financial assets. Three models are estimated: the original Breto SV model with leverage (normal errors), a modified version adding heavy-tailed Student-t errors and hard-coded regime-shift parameters for 2008 and 2020 market disruptions (with leverage), and a matching no-leverage variant. A T-GARCH model serves as an external benchmark.

Genuine strengths include well-structured POMP code following course conventions (run_level framework, replicated pfilter for log-likelihood evaluation using logmeanexp, appropriate cooling schedules), clear documentation of local and global search procedures, and commendable self-criticism in Section 4. The authors correctly identify their most serious flaw.

The primary weaknesses are: (1) the hard-coded regime shift specification constitutes data snooping that invalidates the AIC comparison, (2) no profile likelihoods or confidence intervals are computed for any parameter, (3) the GARCH benchmark comparison uses an inconsistently specified model, (4) a required data file for Figure 2 is absent from the submission, and (5) the Monte Carlo variability in log-likelihood estimates is not accounted for in the borderline AIC comparison.

---

## Major Issues

### 1. Hard-coded regime shift parameters constitute data snooping (acknowledged by authors)

The authors themselves state in Section 4: "We made a serious mistake in specifying μ_h the way we did in (2.3.1)." The modified SV models include a time-varying mean log-volatility with hard-coded windows t ∈ [262, 275] (2008 recession) and t ∈ [400, 410] (2020 pandemic), identified by visually inspecting the data. This is a textbook case of data snooping: the time windows were selected after observing the data and are not estimated parameters counted in the AIC formula.

The consequence is that the `amplitude` parameter has an implicit additional degree of freedom — the choice of the two intervals — that is not penalized in AIC. The AIC comparison between the modified leverage and no-leverage models (ΔAIC ≈ 1.4) is therefore unreliable. More fundamentally, the improvement in log-likelihood over the base Breto model (from ~429.8 to ~437.1) is at least partly attributable to this post-hoc tuning. The Discussion correctly diagnoses the problem and proposes a probabilistic alternative (Weibull-based inter-event time), but the erroneous results are left in the main analysis rather than being clearly marked as illustrative only.

**Fix:** Either remove the hard-coded windows and replace them with a properly parameterized jump or regime-switching component, or explicitly state that the modified SV results are not suitable for formal model comparison and restrict the AIC table to comparing the base Breto SV models.

---

### 2. No profile likelihoods or confidence intervals for any parameter

Neither the base Breto SV model nor either modified model includes profile likelihood computations. No confidence intervals are reported for any parameter. POMP checklist item #5 (Wheeler et al. 2024) requires profile likelihoods to assess whether parameters are identifiable from the data. The pair plots from the global searches suggest potential identifiability concerns — most notably, higher log-likelihoods correlate with smaller log(σ_ν) in the leverage model (Figure 11), suggesting σ_ν may be approaching zero and thus weakly identified. Without a profile likelihood for σ_ν (and similarly for φ, which shows wide spread in Figure 6), it is impossible to determine whether the leverage parameter σ_ν is identifiable, and the conclusion that "leverage effects are limited" cannot be quantified with any stated confidence.

This is a course-confirmed error (Error 1.9 in the weakness reference): "Profile likelihood too sparse to identify the maximum" — here the profile is absent entirely. The course standard for run_level=3 is 30 profile points, which is computationally feasible for a 460-observation dataset.

**Fix:** Compute profile likelihoods for at least σ_ν, φ, and τ in each model, and report MCAP or Wilks-based confidence intervals. The profile for σ_ν in the leverage model is particularly critical for the paper's central conclusion.

---

### 3. Inconsistent GARCH specification between AIC table and reported log-likelihood

The AIC table (Section 2.6) is computed with `include.mean=F` (no intercept), but the best model GARCH(3,1) is then re-fitted with `include.mean=T` to obtain the log-likelihood (435.509) used in the comparison to the SV model. The code makes this explicit:

```r
# AIC table computation
fit.garch <- garchFit(form, data=demeaned_data, include.delta=F,
                    cond.dist=c("std"), include.mean=F, ...)

# Final fit for comparison
fit.garch <- garchFit(form, data=demeaned_data, include.delta=F,
                    cond.dist=c("std"), include.mean=T, ...)
```

Adding a mean parameter changes the model and inflates the log-likelihood relative to the model selected by AIC. The reported GARCH(3,1) log-likelihood of 435.509 is therefore from a different (larger) model than the one AIC selected. This is a concrete specification inconsistency that affects the reported comparison between GARCH and SV.

**Fix:** Either compute the AIC table with `include.mean=T` throughout, or use the model without a mean for the final comparison. The comparison must use a single consistent model specification.

---

### 4. Daily data file missing from submission (Figure 2 not reproducible)

The code in Section 2.1 reads `Daily_New_York_Harbor_Conventional_Gasoline_Regular_Spot_Price_FOB.csv` to produce Figure 2 (daily vs. monthly demeaned log returns). This file is absent from the submitted project directory, which contains only `New_York_Harbor_Conventional_Gasoline_Regular_Spot_Price_FOB.csv` (monthly data). Figure 2 cannot be reproduced from the submitted materials.

Per the code-supplement checklist, a reproducibility failure occurs when required data files are missing. The daily returns plot is mentioned in the text as evidence for why monthly data is used for the main analysis, making it a substantive (not decorative) figure.

**Fix:** Include the daily data file in the submission, or remove the daily data dependency from the report.

---

### 5. Monte Carlo variability in log-likelihoods not propagated into the AIC comparison

The key AIC comparison (Section 2.5) reports log-likelihoods of 437.1 (modified SV with leverage) and 434.8 (modified SV without leverage), giving ΔAIC ≈ 1.4 — a difference of only 2.3 log-likelihood units before the parameter penalty. Both estimates are stochastic outputs from the particle filter. The reported Monte Carlo standard error for the modified SV with leverage simulation was 3.38e-6, but this figure was for the simulated data rather than for the fitted model; the actual SEs from replicated pfilter calls on real data (visible in the L.box computation) are not quoted in the text.

When log-likelihood estimates have non-negligible Monte Carlo noise and the difference between models is ~2.3 units, the comparison result may be dominated by simulation variance rather than true likelihood differences. The course standard requires SE reporting alongside log-likelihood estimates (via `logmeanexp(se=TRUE)`). The AIC table in Section 2.5 cites single point estimates with no reference to uncertainty, and the conclusion that the no-leverage model is "statistically favored" overstates what a 1.4 AIC-unit difference with unquantified Monte Carlo error can support.

**Fix:** Report the mean and SE from replicated pfilter calls for each model's final parameter estimate, and note that the ΔAIC is within a range where Monte Carlo noise may affect the conclusion. Consider running additional evaluation replicates at the MLE to pin down the true log-likelihood difference.

---

### 6. Global search initializes all runs from a single local search result (if1[[1]])

All three models' global searches use `mif2(if1[[1]], ...)` as the starting object, drawing parameters from the box but inheriting the cooling schedule history and particle state from the first local search run. The standard course approach starts global searches from the base pomp object so that the cooling trajectory is fresh and consistent across all global runs. Using if1[[1]] means that 100 ostensibly "global" runs actually share identical starting conditions in the parameter perturbation history, limiting the true diversity of the global search.

**Fix:** Replace `mif2(if1[[1]], params=...)` with `mif2(N_breto_filt, params=...)` (or the appropriate model object) so that each global search run starts from a clean mif2 call with randomly drawn parameters and a fresh cooling schedule.

---

## Minor Issues

### 7. tau and amplitude lack parameter transformations in partrans

The `tau` (degrees of freedom) and `amplitude` parameters in both modified models have no log, logit, or other transformation in `T_breto_partrans` / `T_basicSV_partrans`. During iterated filtering, the random walk perturbations are applied on the native (untransformed) scale. For `tau`, this means the optimizer may propose values ≤ 0, which are biologically nonsensical and handled only by a hard clamp (`nearbyint(tau) < 1 ? 1 : ...`). For `amplitude`, negative values would reverse the sign of the volatility shock, an unintended regime. The hard clamp creates a non-smooth boundary that can distort the iterated filtering trajectory. Adding `log="amplitude"` (with amplitude constrained to be positive) and a bounded transformation for `tau` (e.g., logit-scaled between 1 and 60) would be more principled.

---

### 8. No non-mechanistic benchmark for the POMP SV models

Neither an ARMA model on log-returns nor an IID Gaussian or t model is used as a reference benchmark for the SV models. The T-GARCH model is itself a mechanistic volatility model that is more complex than a white-noise baseline. Per 531-conventions.md, benchmark comparison is "encouraged but not required," and this is noted as a minor issue rather than a major one. However, the course teaches that an IID (e.g., t-distribution) model provides the weakest meaningful benchmark: a mechanistic SV model that does not clearly outperform an IID fit calls its core motivation into question. Reporting the IID t-distribution log-likelihood would take only a few lines of code and would anchor the interpretation.

---

### 9. Seasonal component detected by STL but not modeled in any POMP specification

Figure 19 shows an STL decomposition of log returns revealing a clear seasonal component. The Discussion acknowledges this as a limitation but does not attempt to incorporate it even in the modified SV model. Because the project's main POMP fits precede this diagnostic, the reader cannot tell whether the detected seasonality is strong enough to materially affect the volatility estimates or the leverage conclusion. At minimum, the seasonal pattern should be described quantitatively (amplitude, dominant frequency) so readers can assess its importance.

---

### 10. Base Breto SV model and modified SV model not formally compared

The paper transitions from the base Breto SV model (Section 2.2, best log-likelihood ~429.8) to the modified SV models (Sections 2.3–2.4, best log-likelihood ~437.1 and ~434.8) without a formal AIC comparison between them. The improvement (~7 log-likelihood units) is described qualitatively as "significant advancement," but with 2 additional parameters (tau and amplitude) added, the AIC difference is approximately 7×2 − 2×2 = 10, which is sizable. Presenting this as part of the model comparison table in Section 2.5 would clarify the contribution of the modifications.

---

### 11. epsilon_n appears in text but not in model equations

Section 2.2.1 states "{ε_n} is an i.i.d. N(0,1) sequence" in the description of the Breto model, but ε_n does not appear in any of equations (1)–(4). The role of ε_n in generating Y_n is left implicit. In Breto (2014), Y_n = exp(H_n/2) · ε_n, which corresponds to equation (4) only if σ_n ≡ ε_n · exp(H_n/2). Explicitly defining this relationship, or simply removing the orphaned mention of ε_n, would improve clarity.

---

### 12. No exploratory data analysis section

The report moves from Introduction directly to model specification and results (Section 2) without a dedicated EDA section. Properties of the log returns relevant to model choice — ACF/PACF of returns and squared returns, fat-tail diagnostics (QQ plot), unconditional variance — are not presented prior to model fitting. While STL decomposition appears at the end as a diagnostic, earlier EDA would motivate the choice of a t-distribution observation model and the heavy emphasis on regime shifts.

---

### 13. Ratio of parameter perturbation sizes not discussed

The rw.sd for `tau` is set to 1.0 (on the untransformed scale), while other parameters use rw.sd = 0.02 on their (log or logit) transformed scale. A step size of 1.0 for a parameter ranging from 5 to 60 is proportionally large relative to the 0.02 used elsewhere. The authors do not justify this choice or report any sensitivity analysis. If the step size is too large, iterated filtering for `tau` will not converge well; if too small, the parameter will not be updated efficiently. This deserves brief justification.

---

### 14. Conclusions overstate statistical evidence for the leverage hypothesis

Section 3 states that the findings "provide evidence that leverage effects in gasoline prices may be less pronounced." However, the ΔAIC between the leverage and no-leverage models is only 1.4 units — below the conventional rule of thumb of 2 AIC units for distinguishing models — and the log-likelihood difference (2.3 units) is smaller than the hard-coded regime specification's influence on the fit. The conclusion is further undermined by the absence of a formal test (likelihood ratio test, profile CI for σ_ν crossing zero) and the data snooping concern noted above. The paper appropriately hedges in the Discussion, but the Conclusion section still presents the hypothesis as supported rather than as tentative.

---

### 15. fGarch log-likelihood normalization not verified

The paper directly compares the fGarch log-likelihood (435.509) to the POMP particle filter log-likelihood (434.8) without verifying that both use the same normalization convention. While for Student-t errors applied to the same data both should in principle evaluate the same density, the fGarch package has historically included sign and scaling conventions that differ across versions and options (Error 2.9 in the weakness reference: "trusting software likelihood output without checking conventions"). A one-line check — confirming the sign convention of `@fit$llh` and comparing against a hand-computed log-density — would validate the comparison.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project17/blinded.Rmd`
