# Peer Review: Volatility Analysis on Ethereum (W22 Project 22)

## Summary

This project investigates the return volatility of Ethereum (ETH) daily price data using ARCH/GARCH models and three variants of a stochastic volatility POMP model: (1) the full leverage model adapted from course notes, (2) a simplified model with the leverage term removed, and (3) a "force negative" variant with a fixed negative leverage coefficient. The project's core contribution is a direct log-likelihood comparison of these models with GARCH benchmarks, concluding that the simplified POMP model is preferred by AIC. While the project demonstrates a reasonable command of the POMP framework and attempts systematic model comparison, it contains several methodological weaknesses that undermine its main conclusions: the global IF2 search is initialized from a previous mif2 result object (invalidating the global optimum claim), multiple parameters fail to converge yet results are reported as final, profile likelihoods are never computed, no ARMA-family benchmark comparison is performed, and the AIC computations conflate the summary log-likelihood with the maximum. The paper also lacks model diagnostics and does not discuss parameter plausibility relative to the financial econometrics literature.

---

## Major Issues

### 1. Global Search Anchored to Local IF2 Result — Invalid Global Optimum

In all three POMP model sections, the global box search is initialized via `mif2(if1[[1]], params=apply(box, 1, function(x)runif(1,x)))`. Passing the previous local-search mif2 result `if1[[1]]` as the first argument to `mif2()` causes the global search to inherit the cooling schedule and internal state of the local chain. Because the cooling schedule in `if1[[1]]` is at or near its final (nearly zero) state after 100 IF2 iterations, the random starting parameters drawn from the box are immediately subjected to near-zero perturbations, meaning the global search is effectively a one-step particle filter evaluation from a random start — not a genuine multi-iteration optimization from a fresh beginning. The reported "global maximum" may therefore be indistinguishable from the local search result. The correct pattern is `mif2(filt, params=apply(box, 1, function(x)runif(1,x)))`, where `filt` is the base pomp object.

This issue affects all three POMP models and is the most critical flaw: the central model-selection claim (simplified POMP is best) rests on log-likelihood estimates from searches that did not genuinely explore the parameter box. (See Wheeler et al. 2024, §Computational adequacy; and `pomp-global-search-init-audit` pattern.)

### 2. Self-Diagnosed Non-Convergence — Results Interpreted as Final Estimates

The authors explicitly acknowledge convergence failures in several places:

- For the full leverage model's local search: "the loglik is still fluctuating around 2865 after 100 iterations" and "$\phi$ is still fluctuating, and $H_0$ doesn't converge."
- For the simplified model's local search: "all the parameters are still fluctuating after 100 iterations."
- For the force-negative model: "$H_0$ does not converge after 100 iterations," and the global search is described as "the most unstable."

Despite these admissions, the paper presents log-likelihood summaries and parameter tables from the best-fit rows, constructs simulation plots from those parameters, and makes model selection conclusions (AIC favors simplified POMP). All of these downstream results are invalidated by the authors' own convergence diagnoses. The non-converged chains cannot reliably characterize the MLE; any conclusions about which model fits best are unsupported. (See Wheeler et al. 2024, §Computational adequacy.)

**Fix:** Substantially increase Np (at minimum to 2,000–5,000), Nmif (at minimum to 200–300), and Nreps_global (at minimum to 50–100 with correctly initialized starts) until convergence traces stabilize. If computational resources are insufficient, restrict all model-selection claims accordingly.

### 3. No Profile Likelihoods — Parameter Identifiability Not Assessed

No profile likelihoods are computed for any parameter in any of the three POMP models. The pairs plots show parameter-log-likelihood scatter, but these are not profiles — they show the joint distribution of parameter values across IF2 chains, not the conditional maximum over other parameters at each value. Without profile likelihoods, it is impossible to determine whether parameters are individually identifiable from the data, what the confidence intervals are, or whether the observed parameter clustering reflects genuine identifiability or algorithmic quirks.

This is especially important given that `sigma_nu` converges to zero in the full model, suggesting a boundary MLE — a situation where profile likelihoods are essential for interpreting whether the leverage component is genuinely unsupported by the data or merely unidentifiable given the computational effort applied. (Wheeler et al. 2024, §Parameter identifiability and uncertainty.)

### 4. No Benchmark Comparison Against Non-Mechanistic Statistical Model

The project compares GARCH models to the POMP models, which is a legitimate within-class comparison. However, neither GARCH nor POMP is compared against a simple ARMA model applied to the squared returns or log-absolute returns. More critically, the log-likelihood comparison between GARCH and POMP is problematic (see issue 5), and without an ARMA-family baseline there is no way to assess whether either model captures meaningful structure. The GARCH(1,1) likelihood can be used as a benchmark, but the cross-class comparison is invalid as stated. (Wheeler et al. 2024, §Benchmark comparison.)

### 5. Invalid AIC Comparison Between GARCH and POMP Models

The paper states: "the maximized log likelihood is 2870, which is larger than the log likelihood of GARCH(3,4)" and uses this to conclude "AIC favors POMP model." This comparison is invalid for two reasons:

(a) **Observation model mismatch**: GARCH(3,4) is fitted with `tseries::garch()` which uses a Gaussian likelihood on the demeaned log-returns. The POMP model uses the same Gaussian measurement model (`dnorm(y, 0, exp(H/2), give_log)`), so the observation models are in the same family — this is one point in favor of the comparison. However, the GARCH likelihood from `tseries:::logLik.garch()` and the POMP pfilter log-likelihood are computed in different software frameworks and may not be directly comparable numerically.

(b) **The POMP log-likelihood reported is from a non-converged search**: The best log-likelihood of 2870 comes from the local IF2 summary table, where parameters are acknowledged as not converged. This value is unreliable as an MLE estimate. Using it to claim POMP beats GARCH is unsupported.

### 6. AIC Computation Uses Summary Log-Likelihood, Not Maximum

The paper compares models using a statement like "AIC favors POMP model" without showing an explicit AIC formula. The log-likelihood values cited appear to come from `summary(r.if1$logLik)` output, which reports the median and other quantiles — not necessarily the maximum. Because AIC must use the maximum log-likelihood (`max(r.if1$logLik)`) rather than the median or mean of the distribution over replicates, any AIC values reported may be systematically inflated (worse) for the POMP model, potentially reversing the model-selection conclusion. The paper should explicitly show `max(r.if1$logLik)` and `max(r.box$logLik)` as the basis for AIC. (See `pomp-aic-median-loglik-error` pattern.)

### 7. Model Diagnostics Absent

The paper presents only visual comparisons of simulated trajectories to observed data and pairs plots of parameter values. None of the following diagnostics recommended by Wheeler et al. (2024) are reported:

- Conditional log-likelihoods per time point: these would reveal whether specific periods (e.g., the extreme volatility in early 2021 visible in the data) are systematically poorly fit.
- Effective sample size (ESS) monitoring from the particle filter: the paper mentions "the effective sample size reached the maximum most of the time" for the global search but provides no ESS trace plots.
- Filtering distribution comparison: simulations from estimated parameters are compared to data, but these are unconditional forward simulations, not filtering-distribution simulations. No conditioning on observed returns is performed to reconstruct the latent log-volatility path.

(Wheeler et al. 2024, §Model diagnostics.)

### 8. Simplified POMP Model — Forced Simplification Without Statistical Test

The simplified model eliminates the leverage effect by setting `sigma_nu = 0` and `G_0 = 0`, reducing the parameter count from 6 to 4. The authors motivate this by noting that `sigma_nu` converged to near zero in the full model. While this is a reasonable heuristic, the correct statistical procedure is a likelihood ratio test: `2 * (loglik_full - loglik_simplified)` is approximately chi-squared with 2 degrees of freedom under the null that the simplified model is adequate. Without this test, the claim that the simplified model is preferable is only informally supported. Moreover, because the full model's likelihoods are from non-converged chains, even a formal LRT would be unreliable here.

---

## Minor Issues

### 9. Simulations Presented as Evidence of Model Fit — Visual Comparison Only

The paper relies heavily on overlaid plots of simulated vs. observed returns to assess fit. As Wheeler et al. (2024) note, "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The volatility clustering in the simulated series may visually resemble the observed series without the model capturing meaningful structure, because both exhibit GARCH-like volatility clustering by construction. Quantitative goodness-of-fit metrics (log-likelihood, AIC) must supplement or replace these visual comparisons for credible model assessment.

### 10. Force-Negative Model Interpreted Without Scientific Justification

The "force negative" POMP model fixes G at -0.05 to ensure R_n is always negative, forcing large negative returns to always increase volatility. The motivation is scientifically plausible but the model specification is ad hoc: the value -0.05 is not estimated, not validated against data, and not discussed in relation to any financial econometrics literature on the leverage effect. The resulting model is not a formally tested variant but a constrained version of the original model with an arbitrary constraint. This should be acknowledged and the constraint value justified or estimated.

### 11. Computational Parameters at Run Level 2 — Marginal Effort

The project uses `run_level = 2` throughout, yielding `Np = 1000`, `Nmif = 100`, `Nreps_eval = 10`, `Nreps_local = 20`, and `Nreps_global = 20`. For a financial time series with N ~ 1805 observations and a model with complex latent dynamics (the full leverage model), Np = 1000 particles is marginal. The acknowledgment that "the effective sample size reached the maximum most of the time" suggests particle degeneracy may not be severe, but this also suggests the model may not be fully exploiting the particle filter's capacity. Run level 3 (Np = 2000, Nmif = 200, Nreps_global = 100) would be expected for a final analysis.

### 12. Parameter Transformation for mu_h Missing

In both the simplified and force-negative POMP models, `mu_h` is not included in `partrans`. The `mu_h` parameter is unconstrained (it can be any real number), so no transformation is needed. However, the original model also leaves `mu_h` untransformed while `G_0` and `H_0` are likewise untransformed — this is consistent and not an error. But the paper should note that these parameters are estimated on their natural scale.

### 13. EDA Section Does Not Include ACF/PACF of Squared Returns

The exploratory data analysis section plots price, log-price, and demeaned log-returns, but does not show the ACF and PACF of squared returns or absolute returns — the standard diagnostic for volatility clustering that motivates the ARCH/GARCH family. Including these plots would strengthen the motivation for volatility modeling.

### 14. Conclusion Claims Simplified POMP Has "Largest Maximized Log Likelihood" — Unverified

The conclusion states: "The simplified POMP models has the largest maximized log likelihood." This claim is based on comparing the summary output of non-converged local and global searches. Given that all three POMP models' searches show non-convergence, the rank ordering of their log-likelihoods is unreliable. The simplified model's apparent superiority may be an artifact of the different parameter space geometry or the specific (non-converged) chain that happened to find a high-likelihood region.

### 15. References Section Incomplete

Reference [5] links to a prior midterm project by the same author group, effectively self-citing to borrow descriptions without clarifying which specific content was borrowed. References [8]–[13] list previous student projects as methodological references without distinguishing between conceptual inspiration and direct code borrowing. Given that the paper also uses some code patterns from these sources, a clearer statement of what was adapted from prior work (particularly the financial POMP model structure from lecture notes chapter 16) versus what is original contribution would improve scholarly transparency.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-arima-double-invalid-comparison/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-boundary-mle/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project22/blinded.Rmd`
