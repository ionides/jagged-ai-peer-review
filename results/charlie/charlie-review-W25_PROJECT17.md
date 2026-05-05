# Peer Review: W25 Project 17
**Title:** Time Series Analysis of New York Harbor Conventional Gasoline Regular Spot Price  
**Reviewer:** Charlie  
**Date:** 2026-04-09

---

## Summary

This project analyzes monthly spot prices for New York Harbor conventional regular gasoline (June 1986 – March 2025) using three competing volatility models: a direct implementation of Breto's (2014) stochastic volatility model with leverage, a modified version augmenting both models with heavy-tailed (Student-t) errors and hard-coded regime-shift shocks, and a t-GARCH benchmark. Likelihood maximization is performed via IF2 within the `pomp` framework, and models are compared by AIC. The paper's stated hypothesis — that leverage effects are attenuated in regulated gasoline prices — is interesting. However, critical methodological flaws in the global search initialization, the hard-coded structural breaks, absent profile likelihoods, an incompatible GARCH benchmark comparison, and a missing data file collectively undermine the reliability of the reported results. The authors themselves acknowledge the hardcoded-break design as a "serious mistake" in the Discussion, yet this flawed model remains the vehicle for the main conclusion.

---

## Major Issues

### 1. Global search anti-pattern: all three models initialize from a previous IF2 result

In every global search block, `mif2()` is called with a previous IF2 chain as its first argument rather than the base `pomp` object:

- Breto leverage model (line 404): `mif2(if1[[1]], params=apply(N_breto_box,1,function(x)runif(1,x)))`
- Modified SV leverage model (line 694): `mif2(if1[[1]], params=mapply(...))`
- Modified basic SV (line 932): `mif2(if1[[1]], params=mapply(...))`

Passing `if1[[1]]` (a completed IF2 chain) instead of the base `pomp` object means the global search inherits the internal cooling schedule from the local search, which has already decayed to near-zero perturbations after `Nmif=200` iterations. New random starting parameters are applied to `params=`, but the IF2 optimizer can perform essentially no meaningful exploration from those new starts before the random walk shrinks to zero. The resulting "global maximum" is therefore indistinguishable from the local-search result, and the claim of global coverage is unsubstantiated. The fix is to replace `mif2(if1[[1]], ...)` with `mif2(base_pomp_object, ...)` in all three global search loops. (See POMP checklist item #6: Computational Adequacy; Wheeler et al. 2024.)

### 2. Hard-coded structural breaks constitute look-ahead bias and are acknowledged as a "serious mistake"

The central novelty of the "modified" models is the addition of a state-dependent amplitude shift in $\mu_h(t)$ that activates at hard-coded time indices [262, 275] and [400, 410], corresponding to the 2008 recession and 2020 pandemic. The multipliers 0.8 and 1.2 are chosen based on visual inspection of the observed data. This design introduces look-ahead bias: the model encodes exact knowledge of when the structural breaks occurred and their relative magnitudes, which are directly observable in the training data. The authors explicitly label this "a serious mistake" in Section 4 (Discussion), yet this model is the one used for the main AIC comparison (Section 2.5) and the final conclusion about leverage effects. Conclusions drawn from a model the authors themselves have disavowed cannot be considered reliable. The regime-shift mechanism must be reformulated (e.g., as a hidden Markov state or through a principled Weibull inter-event model as suggested) and the entire analysis rerun before conclusions can be drawn.

### 3. No profile likelihoods or confidence intervals for any parameter

Neither the leverage model nor the no-leverage model presents profile likelihood curves for any of the estimated parameters. Without profile likelihoods, it is impossible to assess whether parameters such as `tau` (degrees of freedom), `amplitude`, `phi`, or `sigma_eta` are identifiable from the data, and no confidence intervals are reported. The main substantive claim — that the leverage parameter $\sigma_\nu$ is effectively zero — is supported only by visual inspection of a pair plot showing that higher log-likelihoods correspond to smaller $\log(\sigma_\nu)$. This is not a formal test of the hypothesis; a profile likelihood for $\sigma_\nu$ is required to determine whether the data provide statistically significant evidence against non-zero leverage. (Wheeler et al. 2024, §Parameter identifiability and uncertainty.)

### 4. `tau` rw.sd = 1 is grossly misscaled

In both modified models, the `rw_sd()` specification sets `tau = 1` (lines 621 and 861). The initial value of `tau` is 5, and the global search box for `tau` spans [5, 30] (model 2) and [5, 60] (model 3). A perturbation SD of 1 on the raw (untransformed) scale of `tau` represents 20% of the lower bound and is far too large for stable convergence — the IF2 chain will diffuse across the entire prior support of `tau` in early iterations. Moreover, `tau` has no entry in `partrans`, so it is optimized on its raw scale where values must remain positive; a random-walk perturbation of SD=1 can easily push `tau` below 1, triggering the clamping logic `(nearbyint(tau) < 1) ? 1 : ...`. The correct approach is to apply a log transformation to `tau` in `partrans` and use a small rw.sd (e.g., 0.1–0.2 on the log scale). (See POMP rw.sd magnitude error pattern; Wheeler et al. 2024, §6.)

### 5. `tau` and `amplitude` lack parameter transformations

The `partrans` specifications for both modified models include log transforms for scale parameters and a logit transform for `phi`, but neither `tau` nor `amplitude` is included (lines 527–529 for T_breto and 792–794 for T_basicSV). The `tau` parameter must be positive and is constrained to [1, 60] via hard-coded clamping in the C snippets — but since IF2 operates on the raw scale, proposals can go negative or to zero, where clamping to 1 creates an artificial boundary that distorts the optimization. Similarly, `amplitude` should be non-negative (a negative amplitude would reverse the intended effect of the regime-shift), yet nothing prevents IF2 from proposing negative values. Both parameters should be included in `partrans` with appropriate transformations (log for `tau`, log for `amplitude`).

### 6. AIC comparison between SV and GARCH models is not valid on a common scale

Section 2.6 directly compares the log-likelihood of the modified SV model (434.8, evaluated via particle filter under the t-distributed observation model) with the T-GARCH(3,1) log-likelihood (435.509, evaluated via QMLE/MLE under the `fGarch` framework). These likelihoods are not comparable: the SV particle-filter likelihood is a Monte Carlo estimate with non-negligible variance (Nreps_eval=20 replicates with Np=2000 particles), while the GARCH likelihood is evaluated analytically under a different statistical framework. The conclusion "the T-GARCH(3,1) model achieved a higher log-likelihood (435.509) than our SV model (434.8)" is drawn from a margin of 0.709 log-likelihood units, which is well within the Monte Carlo error of the SV estimate. No Monte Carlo standard errors are reported for the global-search maximum log-likelihood, so the claimed comparison is statistically meaningless. (Wheeler et al. 2024, §3: Quantitative goodness-of-fit reporting.)

### 7. GARCH grid search uses `include.mean=F` but the final model uses `include.mean=T`

The AIC grid search over all 36 GARCH(p,q) combinations (lines 1026–1033) fits each model with `include.mean=F`, but the final model re-fitted for reporting (lines 1047–1050) uses `include.mean=T`. The optimal order (p=3, q=1) was selected from the `include.mean=F` grid; re-fitting the selected model with `include.mean=T` changes the parameter count and the likelihood surface, invalidating the AIC-based model selection. The same `include.mean` specification must be used throughout.

### 8. Filtered log-likelihoods are reported for simulated data, not for the observed data

Sections 2.2.2, 2.3.2, and 2.4.2 each report an "initial filtered log-likelihood" (410.657, 457.797, and 472.035 respectively), but examination of the code reveals these are computed on simulated trajectories (`N_breto_sim1.filt`, `T_breto_sim1.filt`), not on the actual observed gasoline returns. For example, in Section 2.2.2 the pfilter block (lines 311–320, `eval=FALSE`) applies `pfilter(N_breto_sim1.filt, ...)` — where `N_breto_sim1.filt` is built from the simulated data. Reporting the log-likelihood of a simulated trajectory as an "initial filtered log-likelihood" conflates model simulation with data-based evaluation, and these numbers cannot be interpreted as measures of fit to the observed data.

### 9. Missing data file prevents full reproducibility

The code at line 129 reads `Daily_New_York_Harbor_Conventional_Gasoline_Regular_Spot_Price_FOB.csv`, which is not present in the project folder. Only the monthly CSV is available. Although Figure 2 (the daily returns plot) is produced from this file, the chunk has `eval=TRUE`, so the code will fail to reproduce. The daily data file must be included in the supplement.

---

## Minor Issues

- **Breto model: parameter inconsistency in the text equation.** Equation (4) states $Y_n = \exp\{H_n/2\}\sigma_n$, where the subscript on $\sigma$ suggests it is a state variable, but the code shows `Y_state = rnorm(0, exp(H/2))`. The text description of $\sigma_n$ as an i.i.d. N(0,1) sequence is correct but is placed in the wrong equation numbering; $\beta_n$ involves $Y_n$ which creates a simultaneity that is addressed in the code by using `Y_state` from the *previous* step, but this is not clearly explained in the text.

- **Breto model: initial parameter in text vs. code mismatch.** Section 2.2.2 states $\sigma_\nu = \exp(4.5)$ in the $\theta_0$ equation, but the code sets `sigma_nu = exp(-4.5)` (line 260), which is approximately 0.011. The text incorrectly states $\exp(4.5) \approx 90$. This is a transcription error in the mathematical display.

- **Computational settings not reported in the text.** The run-level settings (Np=2000, Nmif=200, Nreps_global=100, Nreps_eval=20) are buried in code and never mentioned in the narrative. Readers cannot assess computational adequacy without this information. These should be reported explicitly. (Wheeler et al. 2024, §6.)

- **No convergence traces discussed or shown for the Breto model's global search.** The ESS collapse at t=405 is acknowledged for the local search but the global search section repeats this observation without discussion of whether the convergence traces (Figure 7) show genuine parameter movement.

- **"Linear correlations" in global search pair plots.** Section 2.3.4 states "the pair plot indicates linear correlations between the log-likelihood and $(\log(\sigma_\nu), \mu_h, \phi, \sigma_\eta)$." Linear correlations in global-search pair plots indicate the search has not converged to a bounded optimum and the likelihood may increase further outside the explored region — this is a sign of inadequate search coverage, not a positive finding, yet it is not explicitly flagged as a limitation requiring more search.

- **`tau` global box upper bound spans Gaussian region.** The global search box for `tau` in the no-leverage model allows values up to 60 (line 921), and the authors themselves note in Section 4 that t-distributions with $\tau > 30$ are "practically indistinguishable from normal distributions." Including this region in the search box wastes computational budget. The same upper-bound concern applies to the leverage model box (upper = 30).

- **AIC table counts IVP parameters.** The AIC table in Section 2.5 counts `G_0` and `H_0` as free parameters in the leverage model (giving D=8 vs. D=5). Initial value parameters (IVPs) that are not informed by repeated observations contribute to model complexity, but it is worth noting that some authors exclude IVPs from AIC counts; the chosen convention should be stated explicitly.

- **Amplitude global box lower bound is zero for the no-leverage model.** The global search allows `amplitude=0` (line 924), which would deactivate the regime-shift modification entirely. This is not wrong, but the interpretation of models with amplitude near zero is the same as the base model without the modification, and this is not discussed.

- **Typo in Section 2.4.3 narrative.** "The key parametersrs" (line 670, repeated typo) contains a double "rs".

- **Reference [12] (a prior STATS 531 project) is not a peer-reviewed source.** The prior project is cited to motivate the dataset size concern, but course projects do not carry the methodological authority of reviewed work. A published reference on POMP model complexity vs. sample size would be more appropriate.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project17/blinded.Rmd`
