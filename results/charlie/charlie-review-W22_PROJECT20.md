# Peer Review: W22 Project 20
## Statistical Analysis and Modeling of Flu Reports Time Series (SIRS/SARIMA)

---

## Summary

This project applies a SARIMA model and a SIRS-based POMP model to US weekly influenza case data from 2010 to 2022, with the primary scientific goal of explaining the near-zero flu reports during the 2020-2021 pandemic period via a time-varying transmission parameter. The SARIMA analysis covers pre-pandemic data and achieves reasonable fit; the SIRS model incorporates a step-function switch in mean transmission rate during the pandemic cycle. While the project demonstrates genuine ambition and the POMP setup is structurally sound, several major methodological problems undermine the reliability of the main SIRS results: the measurement model contains a coding error (returning a probability density of 0 instead of log-likelihood of -Inf for invalid states), the seasonal function in the code (sin) contradicts the mathematical writeup (cos), the SARIMA log-likelihood and the POMP log-likelihood differ by roughly three orders of magnitude and no meaningful benchmark comparison is made, the profile likelihoods reduce to degenerate single-point results making confidence interval claims invalid, and convergence of the iterated filtering is not adequately demonstrated.

---

## Major Issues

### 1. Measurement model returns probability 0 instead of log-likelihood -Inf for invalid states (CC-Yes, Error 1.3 analog)

In `sirs_dflu`, when `k < 0`, `rho < 0`, or `H < 0`, the code sets `lik = 0`. However, `dmeasure` is called with `give_log`, so the return value is expected to be a log-likelihood. Returning `0` on the log scale means the measurement density is `exp(0) = 1`, which is a valid positive probability mass — not a penalty. Particles in these invalid states are rewarded instead of discarded. The comment in the code ("quick fix: set lik=0 if some parameters are negative — may need a better solution") acknowledges the problem but does not fix it. The correct fix is to return a large negative number (e.g., `lik = (give_log) ? R_NegInf : 0.0`) when the state is invalid. This bug silently corrupts the particle filter weights for any particle that enters an invalid state and could materially affect all downstream likelihood estimates.

**Evidence:** `blinded.Rmd` lines 454–459 (the `sirs_dflu` Csnippet).

**Fix:** Replace `lik = 0` with the appropriate negative-infinity value on the log scale.

---

### 2. Mathematical model description (cos) contradicts code implementation (sin)

The text defines the seasonal transmission rate as:
$$\beta(t) = \beta_0(t)(1 + c\,\cos(2\pi(t+d)/52))$$
but the C snippet implements:
```
Beta = Beta0*(1 + c*sin(2*pi*(t+d)/52));
```
`sin` and `cos` are related by a phase shift of `pi/2`. Because the phase `d` is estimated, these two functions are not equivalent — the same value of `d` produces different seasonal peaks. The estimated parameter values reported in the conclusion (and all profile likelihood results) correspond to the `sin` version, not the mathematically described `cos` version. All results and interpretations of the phase shift parameter `d` are therefore inconsistent with the stated model.

**Evidence:** Mathematical formula at Section 4 (cos); `sirs_step` Csnippet (`sin`).

**Fix:** Align either the text or the code; re-run all analyses with a consistent specification.

---

### 3. POMP log-likelihood is three orders of magnitude below SARIMA, no meaningful benchmark interpretation

The SARIMA model (fitted on pre-pandemic data, 2010-2020) achieves a log-likelihood of approximately -162.84. The SIRS POMP model (fitted on a different but overlapping window, 2015-2021) achieves a best log-likelihood of approximately -1,922. While the two models cover different time windows, this gap of roughly 1,760 log-likelihood units (on similar amounts of data) strongly suggests fundamental model misspecification in the SIRS model. The conclusion briefly notes this ("log likelihood we obtain from the SIRS model is an order of magnitude different") and speculates about causes, but does not act on this signal by investigating model structure. Per Wheeler et al. (2024) and course conventions (MT2 Q4-02, Error 1.15), when a model fits disastrously compared to a benchmark, the correct response is to revise model structure, not to proceed with profile likelihood computation.

**Evidence:** Conclusion section; HTML output shows SARIMA log-likelihood -162.84, SIRS best loglik -1,922.414.

**Fix:** Diagnose the source of poor fit (e.g., examine conditional log-likelihoods, check whether rho is implausibly small, examine ESS). Revise the model before computing profiles.

---

### 4. Profile likelihoods are degenerate: confidence intervals collapse to single points

The reported confidence intervals for `a` are [0.253, 0.253] and for `b` are [1.78, 1.78] — both intervals contain a single value. This indicates the profile has only one point above the Wilks cutoff, which means the profile is too sparse or too noisy to define a valid confidence interval. The profile for `a` is computed over 20 points (`Npoints_profile = 20` at run_level=3) spanning [0.1, 3], but only a single point falls above the threshold. This is a degenerate result: a valid profile should show a smooth curve with a clear maximum and a connected region above the threshold. The conclusion itself acknowledges "we could test this null-hypothesis and obtain more informative profile likelihood and confidence intervals," effectively admitting the profiles are unreliable.

**Evidence:** HTML output shows `a_ci: min = 0.253, max = 0.253`; `b_ci: min = 1.78, max = 1.78`.

**Fix:** With only 20 profile points across [0.1, 3] and `Nreps_profile = 5`, the profile is too coarse given the noisy log-likelihood surface. Increase `Nreps_profile` substantially, verify that the profile maximum aligns with the global search maximum, and report the profile shape before computing CIs.

---

### 5. Rho (reporting rate) fixed at an implausibly small value with inadequate justification

The reporting rate `rho` is fixed at `4e-5`, implying approximately 1 in 25,000 infected individuals is reported. The justification given ("10% of 120,000 tested divided by 325 million population") conflates the fraction of tested specimens that are positive with the fraction of the infected population that is reported. These are fundamentally different quantities. The correct denominator is the number of truly infected individuals, not the total US population. Given `mu_IR` converges to ~7 per week (mean infectious period ~1 day — biologically implausible for flu), the extremely small `rho` and the short infectious period are likely compensating for each other. Fixing `rho` prevents the model from resolving this confound.

**Evidence:** Section 4, parameter discussion; local search result `mu_IR = 7.05`.

**Fix:** Estimate `rho` rather than fixing it, or provide a more rigorous derivation from independent seroprevalence or reporting-rate studies. Discuss the biological implausibility of `mu_IR ~ 7/week`.

---

### 6. Local search uses sequential (%do%) instead of parallel (%dopar%) execution

The local search loop uses `%do%` (sequential) while the global search uses `%dopar%` (parallel). This is inconsistent and means the local search is substantially slower than intended. More importantly, it indicates the authors may not have fully run the local search under the intended conditions. For a project using run_level=3 (Great Lakes), this may also mean the timing and results diverge from what was expected.

**Evidence:** `blinded.Rmd` local search chunk (line ~559): `foreach(i=1:20,.combine=c) %do% {`.

**Fix:** Replace `%do%` with `%dopar%` in the local search for consistency with the rest of the analysis.

---

### 7. Global search box (parameter range) computed from the full likelihood table including implausible values

The box for profile likelihood starting points is derived from `range()` over the entire `sirs_lik.csv`, which includes rows with log-likelihoods as low as -355,362. The displayed range for `mu_IR` extends to 44.9 (upper bound) and for `mu_RS` to 10.7. These represent clearly non-optimal regions. Starting profile optimization from points uniformly drawn from this vast range will produce many failures and few useful profile points, which explains the degenerate CI results in Issue 4. The standard approach is to restrict the box to points within a reasonable distance (e.g., 50 log-likelihood units) of the maximum.

**Evidence:** HTML output: box range for `mu_IR`: [0.96, 44.9]; `loglik` range: [-355,362, -1,922].

**Fix:** Filter the `sirs_lik.csv` to, e.g., `loglik > max(loglik) - 50` before computing the box for profile starting points.

---

### 8. Missing convergence diagnostics for the global search

The global search produces a pairs plot but no trace plots showing the log-likelihood trajectory across mif2 iterations for the global search runs. Without trace plots, there is no evidence that the global search converged rather than terminating at a poor local maximum. The local search traces show that `mu_IR`, `mu_RS`, `a`, and `b` "increase and do not show evidence of convergence" even after 50 mif2 iterations. This lack of convergence in the local search — acknowledged but unaddressed — calls into question whether the global search produced meaningful results. Per Wheeler et al. (2024, Computational adequacy) and Error 1.8 (CC-Yes), convergence traces are a required diagnostic.

**Evidence:** Local search text: "Parameters mu_RS, mu_IR, a, b, d increase and do not show evidence of convergence yet." No global search trace plots are shown.

**Fix:** Show trace plots for the global search. If parameters are not converging, increase `Nmif` or reduce `rw.sd`. Consider whether the model is identifiable.

---

### 9. SARIMA and POMP likelihoods are applied to different datasets and cannot support the claimed benchmark comparison

The introduction states that SARIMA "use[s] for getting the likelihood estimation benchmark for the POMP model." However, the SARIMA model is fit to pre-pandemic data (2010-2020, 500 weeks, BoxCox-transformed), while the SIRS model is fit to 2015-2021 pandemic data (different window, no transformation). Likelihood values from models fit to different datasets are not directly comparable. The conclusion makes an implicit comparison ("log likelihood value around -162" for SARIMA vs. "around -2,000" for SIRS) without acknowledging that this comparison is invalid. A meaningful benchmark would require fitting both models to the same dataset on the same observation scale (Error 2.2, CC-Yes; also 531-conventions.md: "AIC is not directly comparable across ARIMA and POMP models").

**Evidence:** SARIMA fit on `ts_bc[1:400]` (BoxCox-transformed, 400 points); SIRS fit on `df_pand` (raw counts, 313 points, different window).

**Fix:** Either fit a benchmark model (e.g., negative binomial IID, ARMA) to the same pandemic-period data as the SIRS model, on the same observation scale, or remove the comparison from the conclusion.

---

## Minor Issues

### 10. AIC table values appear to be normalized (not standard log-likelihood scale)

The AIC table for SARIMA shows values in the range [0.90, 1.53]. These are almost certainly normalized by the number of observations (as reported by the `sarima` package from the `astsa` library, which reports AIC per observation). Using per-observation AIC for model selection is fine, but the absolute values cannot be compared to the POMP model log-likelihoods, and the text does not clarify this normalization. This contributes to the confusion in the conclusion where SARIMA "-162" and SIRS "-2000" are compared.

**Evidence:** AIC table: AR0/MA0 = 1.53, AR2/MA2 = 0.90; SARIMA fit output: `log likelihood = -162.84, aic = 337.69`.

---

### 11. Reporting rate rho is fixed and partrans includes logit(rho) but rho is in fixed_params

The `partrans` specification includes `logit=c("rho","c")`, but `rho` is in `fixed_params` and not perturbed during mif2. This means the transformation is defined but never used for `rho`. While this does not break the code, it is inconsistent and may cause confusion about which parameters are actually being estimated.

**Evidence:** `blinded.Rmd`: `partrans(logit=c("rho","c"))` and `fixed_params <- c(N=3.25e8, rho=4.e-5)`.

---

### 12. BoxCox transformation introduces an arbitrary offset (+1050) with no justification

The transformation applied is `((cases + 1050)^0.2 - 1) / 0.2`, where the `+1050` offset is not justified. The Box-Cox lambda of 0.21 is computed from the original series but the transformation applies an arbitrary constant offset before exponentiating. There is no explanation for why 1050 was chosen, and using an arbitrary offset changes the transformation's properties and makes the log-likelihood non-comparable to standard Box-Cox formulations.

**Evidence:** `blinded.Rmd` line ~116: `ts_bc <- ((ts(df$cases[1:500], start = c(2010,40), frequency = 52)+1050)^.2-1)/.2`.

---

### 13. SARIMA prediction description is inaccurate

Section 3.3 states "we use the data in the interval 2010-2018 to predict the total flu cases in the interval 2018-2020," but the code fits the model to `BoxCox_ts[1:400]` (approximately 2010 week 40 through 2018 week 13) and then forecasts 100 steps ahead (to approximately 2020). The claim that the model was trained only through 2018 is approximately correct, but the actual training window ends mid-2018, not at year-end 2018. This is a minor inaccuracy in the description.

**Evidence:** `blinded.Rmd`: `BoxCox_ts <- ts(ts_bc[1:400], ...)` with training data ending around week 400 from 2010 week 40 (~2018 week 13).

---

### 14. No model diagnostics beyond visual simulation comparison for the SIRS model

The POMP analysis does not include conditional log-likelihood plots (per-observation log-likelihoods from the particle filter), ESS analysis across the full fitted dataset, or filtering-distribution comparisons. The only diagnostic is a visual overlay of 20 forward simulations against the data. Per Wheeler et al. (2024, Model diagnostics), conditional log-likelihoods would help identify specific time windows where the model fails. Given the enormous gap between SIRS and SARIMA likelihoods, these diagnostics are particularly needed.

**Evidence:** Section 4.5.1 shows a simulation overlay; no conditional log-likelihood or ESS diagnostic plots are shown for the fitted model.

---

### 15. Seasonal model inconsistently applied: pandemic cutoff is week 260, but data starts at week 1 from 2015

The `sirs_step` code uses a hard threshold of `pandemic__week = 260` to switch from transmission rate `a` to `b`. The data index is reset so that week 1 corresponds to week 40 of 2015. Week 260 from that origin is week 40 of 2020 (260 weeks = 5 years), which is consistent with the stated intent. However, this threshold is hardcoded as a constant rather than being defined as a parameter or derived from the data structure, making the model fragile to data window changes and not documented in the mathematical writeup.

**Evidence:** `sirs_step`: `double pandemic__week = 260;`; data setup in Section 4.1.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project20/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project20/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project20/README.txt`
