# Peer Review: W22 Project 06
## Rubella Transmission POMP Model [1966-1967]

---

## Summary

This project fits a stochastic SEIR POMP model to weekly rubella case counts in California from 1966 to 1967 (105 weeks), using a seasonally-varying contact rate. The authors apply iterated filtering (IF2) with a local search, a global search, and profile likelihoods for the reporting rate (rho) and initial susceptible fraction (eta). While the general methodological framework is appropriate for the problem and the use of a negative binomial measurement model is commendable, the analysis contains several critical technical errors that undermine the reliability of all inference results. The most consequential issues are: (1) the global search is anchored to the local search solution via a known anti-pattern in mif2 initialization, meaning the claimed global search does not constitute genuine global exploration; (2) the global search fails to find the best parameter values, which are subsequently discovered during profile searches, confirming computational inadequacy; (3) the accumulator variable H tracks compartment recoveries (I→R) rather than new infections (E→I), creating a systematic mismatch between the model and the observation process; and (4) the fitted parameter values imply a peak intrinsic R0 of approximately 4,872 — biologically implausible for rubella by three orders of magnitude — with no discussion of this inconsistency. No non-mechanistic benchmark is provided.

---

## Major Issues

### 1. Global search initialization anti-pattern invalidates the global search

The global search (chunk beginning `stew('global.rda', {...})`) calls:

```r
mif2(mifs_local[[1]], params = c(apply(rubella_box, 1, function(x) runif(1, x[1], x[2])), rubella_fixed_params))
```

Passing a previous `mif2` result object (`mifs_local[[1]]`) as the first argument to `mif2()` causes each global replicate to inherit the internal IF2 state and cooling schedule from the completed local chain. Because the cooling schedule from `mifs_local[[1]]` is at or near its final state after 100 iterations, the perturbations applied to the randomly-drawn global starting parameters shrink to near zero almost immediately. In practice, each "global" replicate performs negligible optimization from its new starting point and reverts to the neighborhood of the local-search solution. The resulting "global maximum" is not a genuine global optimum. The correct pattern is `mif2(rubellaSEIR, params=...)` using the base pomp object as the first argument (see `pomp-global-search-init-audit` skill; Wheeler et al. 2024, Section on Computational Adequacy).

Both profile searches commit the same error, using `mifs_local[[1]] %>% mif2(params=...)` as the initialization, which similarly anchors the profile search to the local search region.

### 2. Global search is demonstrably inadequate: profile searches find substantially better solutions

Inspecting the saved artifacts confirms that the global search log-likelihood maximum is -556.76 (from `global.rda`). The rho profile search subsequently achieves -554.08 (2.67 units better) and the eta profile search achieves -551.59 (5.16 units better). A profile search over a fixed value of one parameter should, by construction, find solutions no better than the global MLE — the fact that both profiles exceed the claimed global maximum by substantial margins demonstrates that the global search failed to locate the true MLE. Only 9 of 60 global replicates converged within 5 log-likelihood units of the global maximum, indicating poor coverage of the parameter space (Wheeler et al. 2024, Section on Computational Adequacy).

### 3. Accumulator variable H tracks recoveries (I→R) instead of new infections (E→I)

The Csnippet accumulates `H += dN_IR` — the flow from I to R (recoveries). The Project Tycho surveillance data records reported rubella cases, which correspond to new symptomatic infections at the E→I transition, not recoveries. This creates a systematic lag between what H measures and what the data records: with `mu_IR = 0.4` per week (mean infectious period 2.5 weeks), the accumulator trails the true incidence signal by approximately 2.5 weeks at each observation time. The reporting rate rho consequently absorbs not just underreporting but also this temporal displacement, making all parameter estimates — particularly rho and the transition rates — unreliable. The correct implementation would accumulate `H += dN_EI` (the E→I flow). See `pomp-accumvar-semantic-audit` skill.

### 4. Implausible intrinsic R0: estimated parameters imply R0 ~ 4,872

At the reported best-fit parameters (b1 = 1.096, b2 = 6.479, mu_IR = 0.4), the peak seasonal contact rate is Beta_peak = exp(b1 + b2) = exp(7.575) ≈ 1,949 per week, giving an intrinsic R0_peak = Beta_peak / mu_IR ≈ 4,872. The known R0 for rubella is approximately 6–7 in unvaccinated populations. While the small susceptible fraction (eta ≈ 0.22%) partially compensates, producing an effective R0 ≈ 10.9, the underlying parameter values are biologically extreme. This is a potential signal of model misspecification: a ridge in the likelihood surface may be trading off b1, b2, and eta in a way that the data cannot resolve, producing individually implausible values that cancel out in the effective reproduction number. The authors note that b1 and b2 do not converge (Figure 8 convergence traces), which is consistent with this interpretation. Per Wheeler et al. (2024) Section 11 (Corroboration with scientific knowledge), implausible estimates should be flagged as evidence of potential model misspecification rather than accepted as biological findings. The text offers no such discussion.

### 5. No non-mechanistic benchmark comparison

The SEIR model is not compared against any non-mechanistic benchmark (e.g., SARIMA or auto-regressive negative binomial). Without a quantitative benchmark comparison, it is impossible to assess whether the mechanistic model captures structure beyond what a simple statistical model would achieve. A SARIMA(1,0,1)(1,0,1)[52] fitted to the same series would provide a principled baseline. Wheeler et al. (2024) note that none of the 32 papers in their Haiti cholera literature survey performed such a comparison, and their benchmark revealed that some models failed to outperform it.

### 6. Profile CI for eta is misreported and the profile is poorly converged

The text states: "the graph states that our eta did not reach the confidence interval cutoff." This is incorrect: inspection of the `profile_eta.rda` artifact shows two points (at eta ≈ 0.00239 and 0.00250) with log-likelihoods above the CI cutoff (-553.51). However, the profile curve is highly noisy — the maximum log-likelihood across the 30 profiled eta values varies by approximately 16 units (from -567.2 to -551.6) — and the two points above the cutoff are not contiguous, indicating that the profile has not converged. The text also reports the eta CI as (0.19%, 0.24%), but the actual computed CI from the artifact is (0.24%, 0.25%). These numbers cannot be reconciled: the lower bound 0.19% lies below the profile grid lower bound of 0.20%, which is impossible if the CI is derived from this profile.

### 7. Profile searches use profile-maximum rather than global-maximum as CI reference

Both profile CI computations use `maxloglik = max(results$logLik, na.rm=TRUE)` — the maximum log-likelihood within the profile results — as the chi-squared reference. Because the profile searches found solutions better than the global search (see Issue 2), this is coincidentally closer to the true MLE than the global maximum. However, the profile maximum is itself subject to Monte Carlo noise (logLik_se up to 3.88 units at the eta profile peak), and using a noisy profile-local maximum rather than a robustly estimated global maximum inflates the CI in unpredictable directions. The standard practice is to use the best log-likelihood from the global search as the CI reference, computed with high particle counts and multiple replicates to reduce SE (Wheeler et al. 2024, Section 5).

### 8. Fixed parameters (mu_EI, mu_IR) lack justification and sensitivity analysis

The latent-period rate (mu_EI = 0.08 per week, mean latent period ≈ 12.5 weeks) and recovery rate (mu_IR = 0.4 per week, mean infectious period ≈ 2.5 weeks) are fixed without citing independent scientific sources for rubella's incubation and infectious periods. The known rubella incubation period is 14–21 days (2–3 weeks), corresponding to mu_EI ≈ 0.33–0.5 per week — substantially higher than the 0.08 used. The mean infectious period of 2.5 weeks is at the upper end of the known range but plausible. No sensitivity analysis is performed to assess how these fixed values affect the estimated parameters (b1, b2, rho, eta). Because mu_EI and mu_IR directly govern the shape of the epidemic curve, mis-specified fixed values will distort the contact rate and reporting rate estimates. Per Wheeler et al. (2024) Section 13, initial conditions and fixed parameters should be estimated or subject to sensitivity analysis when they substantially affect model fit.

---

## Minor Issues

- **Text-code discrepancy in force-of-infection formula**: The text states the S→E transition probability as `Binomial(S, 1 - exp(-beta * E/N * dt))`, using E (exposed) in the force of infection. The Csnippet correctly uses `I/N` (infectious compartment) in the force of infection term `rbinom(S, 1-exp(-Beta*I/N*dt))`. In an SEIR model, only infectious individuals (I) drive new transmissions; the exposed class (E) has not yet become infectious. The text equation contains a typo that should be corrected for scientific accuracy.

- **Incorrect eta initial value calculation**: The text states that eta is calculated as "doubling the reported cases (50% response rate) and dividing the [the] population," yielding eta = 0.0023. The actual computation: 12,460 total cases × 2 ÷ 15,717,204 = 0.00159, not 0.0023. The stated rationale does not reproduce the stated value.

- **Data loaded from external URL**: The raw data is loaded via `read.csv("https://raw.githubusercontent.com/...")`, which requires active internet access at render time and is sensitive to repository changes. Reproducibility would be improved by archiving the data file alongside the Rmd.

- **SE of logLik at reported MLE is large (SD = 2.3)**: The text reports the best model with "a maximum likelihood of -556.8 with a standard deviation of 2.3." A standard deviation of 2.3 log-likelihood units for the particle-filter estimate at the MLE indicates that 1,000 particles (Np = 1,000) is insufficient for reliable likelihood evaluation. Wheeler et al. (2024) recommend that this SE be substantially smaller than 1 unit. Increasing Np to 5,000–10,000 for the final likelihood evaluation would substantially improve precision.

- **Global search box for eta is very narrow**: The eta box range (0.002, 0.0026) spans only a 30% range around the initial guess. Given that eta is poorly identified (as the authors acknowledge), the box should be substantially wider to allow genuine exploration of susceptible fraction values. The local search found eta values ranging from 0.00182 to 0.00286 — outside the global box — yet the box was defined more narrowly.

- **Convergence traces not discussed quantitatively**: Figure 8 shows convergence traces but the discussion ("consistently climbing likelihood is promising") is qualitative. No convergence diagnostic such as replicate chain overlap or between-chain variance is reported. The authors note that b1, b2, and eta "tend to be stable ever since the first iteration" with "spread of convergence points" — this description is consistent with the cooling schedule from mifs_local[[1]] being nearly exhausted, preventing genuine parameter exploration (connected to Issue 1).

- **No model diagnostics**: The analysis presents no conditional log-likelihoods, effective sample size diagnostics, or filtering-distribution comparisons. Wheeler et al. (2024) Section 4 emphasizes that these diagnostics are essential for identifying periods of poor fit and distinguishing model inadequacy from parameter misspecification.

- **Plot comment left in code**: The code for Figure 9 (global pairwise) contains the comment "(not sure if we need to inclue this part)" — a draft note that should be removed before submission.

---

## Files Consulted

**Skill files:**
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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-mc-noise-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-boundary-mle/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-covariate-compartment-underflow/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-moment-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rprocess-wrong-hazard-variable/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-population-text-code-discrepancy/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stochastic-dmeas-intermediate/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project06/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project06/global.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project06/local_x.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project06/profile_rho.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project06/profile_eta.rda`
