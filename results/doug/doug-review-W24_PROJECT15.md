# Peer Review: W24 Project 15
## Analysis of Middle-East Respiratory Syndrome Coronavirus in Saudi Arabia

---

## Summary

This project fits a SEIRS compartmental POMP model to weekly MERS-CoV case data from Saudi Arabia (January 2014 to May 2016), treating camel-to-human spillover as the observation mechanism and the camel SEIRS dynamics as the hidden Markov process. The approach is biologically motivated and follows a published model (Lin et al. 2018). The ARMA(1,4) benchmark comparison is appropriate in intent, and the global IF2 search and profile likelihood for the spillover rate rho_CH represent genuine effort toward likelihood-based inference. However, the project contains several critical methodological errors that undermine the validity of the main conclusions: an invalid likelihood ratio test comparing the POMP and ARMA models, an incorrect accumulator variable definition that causes the measurement model to track recoveries rather than new infections, a profile likelihood rw.sd specification that allows the profiled parameter to drift, and insufficient convergence evidence. Several additional structural and inferential problems are detailed below.

---

## Major Issues

### 1. Invalid likelihood ratio test comparing ARMA and SEIRS models

The project applies a formal Wilks likelihood ratio test to compare the ARMA(1,4) log-likelihood (-422.77) to the SEIRS log-likelihood (-378.33), computing a chi-squared p-value and concluding that the SEIRS model is "significantly better" (Conclusion section and Global Search section). This comparison is invalid for two distinct reasons.

First, the two models are evaluated on different observation models: the ARMA likelihood is Gaussian on the raw count data, while the SEIRS likelihood is evaluated under a negative binomial measurement model. Log-likelihood values from these two families are not on the same scale and cannot be compared numerically. The Wilks approximation for a likelihood ratio test applies only when both models are nested within the same parametric family evaluated on the same data under the same observation model.

Second, the ARMA(1,4) and SEIRS models are not nested. The Wilks result (chi-squared with degrees of freedom equal to the difference in parameter counts) applies only to nested models; comparing non-nested models via this statistic has no theoretical justification (see sarima-baseline-audit skill).

The project should either evaluate both models under a common observation model (e.g., both as count regression models), use a proper scoring rule on the predictive distribution, or simply report both likelihoods as descriptive summaries without a formal significance test.

### 2. Accumulator variable tracks recoveries, not new infections

In the rprocess Csnippet (`seirs_step`), the accumulator variable C is defined as:

```
C += dN_IR * rho_CH;
```

This accumulates the flow from I to R (camel recoveries) scaled by rho_CH. However, the stated biological interpretation is that C represents primary human infections caused by contact with infectious camels — an event that should be proportional to the rate at which camels are infectious, not to the rate at which they recover. The mathematically correct accumulation for a spillover model in which human infections arise at rate rho_CH * mu_IR * I (as stated in the measurement model equation) would be:

```
C += dN_EI * rho_CH;  // new infections entering I
```

or equivalently:

```
C += (number entering infectious state) * rho_CH;
```

Accumulating recoveries rather than new infectious events creates a systematic mismatch between the measurement model and the data-generating process. Because recoveries lag entries to I, the timing of C is shifted, and rho_CH absorbs a distorted ratio. All parameter estimates (particularly rho_CH, mu_IR, and Beta) may be biased as a result. This is the most consequential code-level error in the project (see pomp-accumvar-semantic-audit skill).

### 3. Profile likelihood allows rho_CH to drift during IF2

In the profile likelihood computation (chunk beginning at line 762), the mif2 call uses:

```r
rw.sd=rw_sd(Beta=0.02, eta=ivp(0.01), eta2=ivp(0.0001), mu_EI=0.01, mu_IR=0.01, mu_RS=0.001, k=0.01)
```

Notably, rho_CH is absent from this rw.sd specification, which means its perturbation defaults to zero inside the mif2 call. This is actually the correct pattern for a profile likelihood. However, the profile grid is constructed from `profile_design(rho_CH = seq(0.0001, 0.001, ...))` with only `nprof=5` starting points per grid value, and the IF2 runs only 100 iterations with cooling.fraction.50=0.3. With 5 starting points per profile slice over 40 grid values, the optimization at each fixed rho_CH value has very limited coverage of the remaining parameter space. The result is a profile curve that may not represent the true profile maximum at each rho_CH slice, producing an unreliable confidence interval. The authors acknowledge the profiled MLE sits at the edge of the searched interval (0.001) but do not extend the grid or increase nprof. The reported 95% CI of approximately 0.001 (essentially a point) is therefore not reliable.

Additionally, the CI computation (line 826-828) uses `max(results$loglik)` where `results` contains only the profile search outputs. If the global search found a higher likelihood than the profile search, the cutoff is too low, making the CI artificially wide. The correct reference maximum should come from the full accumulated parameter table (`saudi_mers_params_with_profile.csv`).

### 4. Global search initialized from a previous mif2 result object rather than the base pomp object

In the global search chunk (line 635), the code sets `mf1 <- mifs_local[[1]]` and then calls `mif1 |> mif2(params=c(unlist(guess), fixed_params))`. This initializes each global search replicate by passing a completed local-search mif2 chain as the first argument to mif2, with new random starting parameters supplied via `params=`. This is the anti-pattern identified in the pomp-global-search-init-audit skill: the global replicate inherits the cooling schedule state from the local search (`mifs_local[[1]]`), which has already completed 100 IF2 iterations at a cooling fraction of 0.5. The perturbed parameters therefore shrink rapidly from the new random starts, effectively anchoring the search near the local-search solution rather than genuinely exploring the box. The reported global maximum of -378.33 may not represent a true global optimum.

The fix is to pass the base pomp object (`saudiSEIRS2`) as the first argument to mif2 in the global search loop, ensuring each replicate starts fresh with an uncooled schedule.

### 5. No convergence evidence for the global search

The project shows convergence traces for the local search (mifs_local) but not for the global search (results). The global search performs only two mif2 calls per replicate (one with default settings inherited from mf1, then one with Nmif=50), which is a very small number of iterations given that the local search itself required 100 iterations to approximately converge. No likelihood traces from the global search are shown. Without convergence traces for the global search, it is impossible to assess whether the reported log-likelihood of -378.33 is a stable maximum or an artifact of insufficient optimization. Per Wheeler et al. (2024), evidence of convergence from multiple starts reaching similar likelihoods is a required practice (POMP checklist item 6: Computational Adequacy).

### 6. dmeasure and rmeasure use inconsistent scaling for human cases

The dmeasure Csnippet is:
```
lik = dnbinom_mu(reports, k, rho*C, give_log);
```

The rmeasure Csnippet is:
```
int total_to_primary = 4;
reports = total_to_primary * rnbinom_mu(k, rho*C);
```

The dmeasure evaluates the probability of `reports` under a NegBin with mean rho*C, while rmeasure generates `4 * rnbinom_mu(k, rho*C)`. The two Csnippets are therefore inconsistent: dmeasure treats reports directly as a NegBin(k, rho*C) draw, while rmeasure generates total human cases as four times a NegBin draw. The particle filter uses dmeasure to weight particles; if the actual data `reports` includes the 4x multiplier but dmeasure does not, the likelihood is evaluated on the wrong scale. This inconsistency between dmeasure and rmeasure means that simulations and likelihood evaluations are from different models, invalidating both the reported log-likelihood and any simulated trajectories used to validate the model fit (see pomp-inference-misuse skill, Step 4).

### 7. Likelihood ratio test degrees of freedom are incorrect even ignoring the non-comparability issue

Even setting aside the fundamental non-comparability of ARMA and POMP likelihoods, the LRT in the Global Search section assigns D1=8 to the SEIRS model. The model has the following estimated parameters: Beta, rho_CH, eta, eta2, mu_EI, mu_IR, mu_RS, k — that is 8 parameters. Fixed parameters (N, rho, mu) are excluded, which is correct. However, the ARMA(1,4) model with a mean term has parameters phi_1, theta_1, theta_2, theta_3, theta_4, mu, sigma^2 — that is 7 parameters, not 5 as claimed in the text. The AIC reported by R's arima() for ARMA(1,4) uses the correct parameter count, but the text miscounts D0, inflating the degrees of freedom for the test from the correct 8-7=1 to 8-5=3.

---

## Minor Issues

- **R_0 formula**: The project computes R_0 = Beta / mu_IR. The standard definition in a SEIRS model with demography and an exposed class is R_0 = Beta * mu_EI / ((mu_EI + mu) * (mu_IR + mu)), not simply Beta / mu_IR. The simplified formula ignores the probability of surviving the latent period and natural mortality. The reported R_0 = 2.6 is therefore not directly comparable to the Lin et al. (2018) estimate.

- **Model diagram file missing**: The model description references `model.png` (a diagram of the SEIRS structure) but this file is not present in the project subfolder. The image does not render in the project output.

- **Fixed rho = 1 not adequately justified**: The project fixes the reporting rate rho = 1, stating that "almost all camel-infected human cases are recorded." No citation or epidemiological justification for near-complete surveillance is provided. Given that MERS is a novel pathogen with imperfect surveillance infrastructure, this assumption warrants justification or sensitivity analysis.

- **Profile CI computation reads from results not saudi_mers_params_with_profile.csv**: As noted in Major Issue 3, the confidence interval cutoff uses only the profile search maximum, not the global maximum from the full parameter accumulation file. If the global search found higher likelihoods (it did: -378.33 vs. the profile maximum), the cutoff is shifted upward and the CI is underestimated.

- **Spectral analysis period calculation error**: The code computes `round(12/(num_weeks_per_year * freq.pg_sm), 2)` and describes the result as a period in "months." The factor of 12 in the numerator assumes the fundamental unit is years, but freq.pg_sm is in cycles/week and num_weeks_per_year = 52.143, so the formula yields months only if 52.143 * freq / 12 gives cycles/month, which is dimensionally inconsistent. The correct calculation for period in weeks is simply 1/freq.pg_sm; converting to months requires dividing by (52.143/12). The displayed value may still be approximately correct but the derivation is written incorrectly.

- **mu in rw.sd is absent**: The local search rw.sd does not include mu (camel birth/death rate), which is fixed. This is appropriate and consistent with the model, but the report does not explicitly acknowledge that mu is held at 1/(52*14) throughout all searches. A brief note in the text would aid reproducibility.

- **Insufficient Np and Nmif for final likelihood evaluation**: The project uses Np=2000 particles throughout with Nmif=100 for the local search and only two mif2 passes for the global search. For a 5-dimensional state process (S, E, I, R, C) with 125 weekly observations, 2000 particles may be marginal but appears workable given the ESS reported. However, the sensitivity of the reported log-likelihoods to Np is not assessed.

- **No model diagnostics beyond ESS**: The project shows only the ESS plot from pfilter at the initial parameters. No conditional log-likelihood plot, no filtering-distribution simulations versus forward simulations, and no residual diagnostics are presented for the fitted model. Per POMP checklist item 4, such diagnostics are required to identify specific periods of poor fit.

- **Pairs plot uses local search results for profile section**: The pairs plot in the profile likelihood section (line 802) uses `results` which at that point in the code refers to the profile search results (if loading from CSV). This is correctly labeled, but a comparison of the global search and profile search scatter in the same pairs plot would be more informative.

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
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project15/weekly_clean.csv`
