# Peer Review: W21 Project 02
**Title:** Study of daily COVID-19 Infected cases in the United States

---

## Summary

This project fits three compartmental POMP models — SEIR, SECSDR, and SEIQR — to daily confirmed COVID-19 infections in the United States from January 2020 to April 2021. The paper demonstrates familiarity with the pomp framework and is candid about model failures: the authors acknowledge that none of the three models produces simulations resembling the observed data. Despite this honesty, the analysis contains numerous critical methodological and implementation errors that undermine every quantitative result. Most severely, the IF2 global searches for the SECSDR and SEIQR models are configured with negligible random-walk perturbation sizes (rw.sd = 2e-9) and an extreme cooling schedule (cooling.fraction.50 = 0.00005), making all reported parameter estimates products of random initialization rather than optimization. Additional problems include a misspecified SEIR dmeasure/rmeas pair (standard deviation equals the mean rather than its square root), an inconsistent population size across models, a complete absence of benchmark comparison, profile likelihoods, or model diagnostics, and no comparison of the three models by log-likelihood on a common basis.

---

## Major Issues

### 1. Negligible rw.sd renders IF2 optimization inoperative for SECSDR and SEIQR

In both the SECSDR global search (Section 4.2) and the SEIQR global search (Section 5.2), a shared scalar constant is defined:

```r
covid_rw.sd = 0.000000002   # = 2e-9
covid_cooling.fraction.50 = 0.00005
```

These values are then applied uniformly to all parameters in `mif2()`. The parameters being optimized span ranges of 0.001–10 (rates) and 0–0.5 (rho), so the minimum meaningful perturbation to traverse any part of the box in 100 Nmif iterations is on the order of 1e-5 to 1e-1. A perturbation SD of 2e-9 is 4–8 orders of magnitude too small to move any parameter. Furthermore, `cooling.fraction.50 = 0.00005` shrinks even this negligible perturbation to approximately 1e-13 by iteration 50, which is below machine epsilon for double-precision arithmetic. The net effect is that each "global search" replicate evaluates the likelihood at its random starting point without any gradient-following optimization. All reported log-likelihoods, parameter estimates, and convergence trace plots for SECSDR and SEIQR are results of random draws from the starting-point box, not from an optimization procedure. The paper's conclusions about these two models' parameter values are therefore invalid.

**Fix:** Replace the shared scalar with individually calibrated rw.sd values approximately 2–5% of the expected parameter range per parameter (e.g., `rw.sd(Beta1=2e-5, Beta2=2e-5, mu_ECa=2e-4, ...)` for ranges of order 0.001 to 0.01). Set `cooling.fraction.50` to a standard value in [0.1, 0.5].

---

### 2. SEIR dmeasure uses variance equal to mean-squared rather than mean (Poisson-like)

In the SEIR dmeasure Csnippet (Section 3.1), the standard deviation of the normal approximation is defined as:

```c
double mean_cases = rho * H;
double sd_cases = sqrt(mean_cases * mean_cases);
```

This computes `sd_cases = |mean_cases|`, meaning the coefficient of variation is 1 regardless of scale. This is not a Poisson approximation (which would use `sqrt(mean_cases)`) nor a negative binomial approximation. The corresponding rmeasure uses:

```c
Infected = rnorm(rho * H, sqrt(rho * H));
```

which applies `sqrt(mean)` as the SD — the two snippets implement different variance functions. The dmeasure evaluates probabilities under variance = mean^2, while the rmeasure generates draws under variance = mean. This inconsistency means the particle filter weights and the simulated trajectories are based on different observation models, invalidating all SEIR likelihood estimates and simulations.

**Fix:** Use a consistent measurement model in both snippets. For a normal approximation, apply `sd_cases = sqrt(mean_cases)` in dmeasure to match rmeasure, or replace both with a negative binomial model (`dnbinom_mu` / `rnbinom`) which is more appropriate for overdispersed count data.

---

### 3. SEIQR model uses wrong population size (N = 32,000,000 instead of 328,000,000)

The SEIQR model initialization (Section 5.1) fixes population size at:

```r
fixed <- c(N = 32000000)
```

while the SEIR model uses `N = 300,000,000` and the SECSDR model hardcodes `S = 328,000,000` in rinit. The US population is approximately 330 million. The SEIQR population is a factor of 10 too small, which inflates the effective per-capita transmission rate by a factor of 10 and makes all SEIQR parameter estimates irreconcilable with the other two models. No acknowledgment or justification is provided for this discrepancy.

**Fix:** Set `N = 328000000` (or use the same value as the other models) in the SEIQR fixed parameter vector. All three models should use consistent values for shared parameters to enable any form of cross-model comparison.

---

### 4. No benchmark comparison against a non-mechanistic model

None of the three mechanistic models is compared against a non-mechanistic statistical baseline such as ARIMA or an auto-regressive negative binomial. Without such a comparison, it is impossible to assess whether any of the three models captures meaningful structure beyond what a simple statistical model would achieve. Wheeler et al. (2024) found that none of the 32 papers in their cholera literature review performed such a comparison, and their auto-regressive negative binomial benchmark revealed that several mechanistic models failed to outperform it. Given that all three models here produce trajectories the author themselves describe as poor, a benchmark comparison would confirm whether this reflects fundamental model inadequacy or merely inadequate optimization.

**Fix:** Fit an ARIMA or auto-regressive negative binomial model to the same data. Report its log-likelihood alongside the POMP models to provide context for the mechanistic models' quantitative fit.

---

### 5. No profile likelihoods; parameter identifiability not assessed

Neither profile likelihoods nor confidence intervals are computed for any parameter of any model. With eight parameters in SECSDR, six in SEIQR, and seven in SEIR, many parameters are likely to be poorly identified from the data — a problem the paper inadvertently acknowledges ("it is hard to find any pattern from the plot"). Without profile likelihoods, the reported parameter estimates at the global MLE have unknown precision and identifiability status. Parameters may be unidentifiable (flat profile) or confounded with one another. Per Wheeler et al. (2024), profile likelihoods are essential to determine whether reported estimates have any statistical meaning.

**Fix:** Compute profile likelihoods for at least the epidemiologically most important parameters (transmission rate Beta, reporting rate rho). Report 95% confidence intervals using the Monte Carlo Adjusted Profile (MCAP) method.

---

### 6. No quantitative goodness-of-fit or model comparison

The paper does not report log-likelihood values for the SEIR model after global optimization (only the SECSDR and SEIQR top-5 log-likelihoods are printed, and these are themselves invalid due to Issue 1). No AIC or other information criterion is reported. No comparison across the three models by a common metric is made. The author's conclusion that "the likelihood analysis seems unreasonable" is stated without specifying what values were obtained or how they compare. Per Wheeler et al. (2024), "visual comparisons alone are only a weak and informal measure of goodness-of-fit."

**Fix:** Report the best log-likelihood for each model after optimization. Compute AIC = -2 * loglik + 2k for each. Compare all three models on this common scale. Note that log-likelihood comparisons are only valid if all models use the same data and the same observation model family.

---

### 7. SECSDR rprocess uses sequential binomial draws on dependent populations without accounting for depletion

In the SECSDR rprocess (Section 4.1), the draws are structured as:

```c
double dN_SE = rbinom(S, 1-exp((-Beta1*Ca-Beta2*Sy)*dt));
double dN_ECa = rbinom(dN_SE, 1-exp(-dt*mu_ECa));
double dN_CaR = rbinom(Ca, 1-exp(-dt*mu_CaR));
double dN_CaSy = rbinom(Ca - dN_CaR, 1-exp(-dt*mu_CaSy));
```

The last line attempts to draw from Ca minus those already removed, but `dN_ECa` (the newly arrived in Ca from E) is not added to Ca before computing dN_CaR and dN_CaSy. In the same step, individuals newly entering Ca via dN_ECa are subjected to competing risks of dying or becoming symptomatic, even though they only just entered the compartment within the same time step. More importantly, Ca is not updated before the competing-risk draws, so the actual Ca population available for the dN_CaR draw should be `Ca + dN_ECa`, not `Ca`. This is a compartment depletion accounting error that distorts the flows out of Ca.

**Fix:** Restructure the process noise to properly account for the state at the start of the Euler step. Either add dN_ECa to Ca before computing the competing-risk draws, or use a multinomial draw to handle the three competing exits from Ca simultaneously.

---

### 8. Global search for SEIQR runs at run_level = 2 but SECSDR at run_level = 1

The SECSDR global search (Section 4.2) sets `run_level <- 1` (Np=100, Nmif=10, Nglobal=10), while the SEIQR global search (Section 5.2) sets `run_level <- 2` (Np=2000, Nmif=100, Nglobal=50). The SEIR local search uses Np=2000 and Nmif=200 with 20 replicates, while the SEIR global search uses Np=20,000 for final evaluation but only one round of mif2 (via `mf1 %>% mif2(params=...) %>% mif2(Nmif=100)`). This inconsistency means the three models are optimized with radically different computational effort, making cross-model log-likelihood comparisons invalid even after correcting the other issues.

**Fix:** Apply identical optimization settings across all three models. At minimum, use run_level=2 settings for all models, and standardize Np, Nmif, and Nglobal values before comparing log-likelihoods.

---

### 9. No model diagnostics (conditional log-likelihoods, ESS, filtering distribution)

None of the three models includes any model diagnostic beyond visual overlay of simulated trajectories on observed data. No conditional log-likelihood plot is shown to identify periods of poor fit. No effective sample size (ESS) trace is presented to verify that the particle filter is not degenerating. No filtering-distribution comparison is made (pfilter-conditioned simulations vs. forward simulations from initial conditions). Per Wheeler et al. (2024), these diagnostics are essential for understanding where and how the model succeeds or fails, and for guiding iterative model development. In this paper, where all three models produce poor trajectories, diagnostics would help distinguish between model misspecification and optimization failure.

---

### 10. SECSDR rinit does not include E compartment; S = 328,000,000 is hardcoded but not verified

The SECSDR rinit (Section 4.1) initializes `E` is not even declared as a state variable in `covid_statenames`. The statenames vector is `c("S","Ca","Sy","R","Di")` — E is absent. However, the rprocess references `dN_ECa = rbinom(dN_SE, ...)` which draws from dN_SE (the SE transition), implying there is an implicit E compartment. Individuals move from S to Ca without passing through an explicit E compartment in the state vector; dN_SE is computed but immediately used as dN_ECa. This collapses the latency compartment. Whether this is intentional (a modeling choice) or an implementation error is unclear. If intentional, it should be acknowledged in the model description; if an error, the E compartment must be added to statenames and rinit.

---

## Minor Issues

- The introduction contains an ungrammatical URL embedded in running text (`{https://www.who.int/...}`) rather than formatted as a hyperlink or footnote.

- The `tau` parameter appears in `paramnames` and `partrans` for the SEIR model but does not appear in any Csnippet (seir_step, dmeas, or rmeas). It is a declared orphan parameter that consumes a degree of freedom without contributing to the model. Its intended role is never explained.

- The SEIR global search (Section 3.3) calls `mf1 %>% mif2(params=c(unlist(guess), fixed_params))` where `mf1 <- mifs_local[[1]]`. This passes a previous mif2 result as the first argument to the global search, inheriting the cooling schedule from the local chain rather than starting fresh from the base pomp object. The global search is thereby anchored near the local-search solution.

- The SEIQR model uses the quarantined (Q) compartment as the mean of the observation distribution (`lik = dnorm(Infected, Q, rho*Q + 1e-10, give_log)`), treating Q as the daily diagnosed count. However, Q is a stock (cumulative quarantined individuals), not a daily incidence flow. Observing daily new infections through Q without an accumulator or differencing the stock is semantically incorrect.

- Simulated results for SECSDR and SEIQR (Sections 4.3, 5.4) use `para = coef(mifs_global[order(liks_global[,1], decreasing=T)[2]])` — this selects the second-best rather than the best parameter set. No justification for this choice is provided.

- The conclusion (Section 6) discusses future work involving temporal phase decomposition (dividing the 400 days into phases), but no exploratory or preliminary analysis of this decomposition is presented. The discussion is speculative without supporting analysis.

- The reference list (Section 7) cites two other student projects as references [2] and [3] for the SEIQR and SECSDR model structures, respectively, but no formal citation to any peer-reviewed epidemiological or statistical methods paper is included. The mechanistic models should be grounded in published literature.

- The SEIR local search traces plot (Section 3.2) includes `tau` in the trace panels even though tau does not appear in any rw.sd argument and is not being updated by IF2. Plotting a constant parameter as a convergence trace is misleading.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-domain-violation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project02/blinded.Rmd`
