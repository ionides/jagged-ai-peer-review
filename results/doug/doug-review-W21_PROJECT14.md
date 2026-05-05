# Peer Review: W21 Project 14
## SEIR POMP Model for Mumps in Michigan, 1970s

---

## Summary

The paper fits a seasonal SEIR POMP model to 100 weeks of weekly mumps case counts from Michigan (September 1971 to September 1973) using likelihood-based inference via iterated filtering (IF2). The model incorporates a cosine seasonal contact rate and a negative binomial measurement model. While the project correctly applies mif2 and pfilter and makes a genuine attempt at profile likelihood inference for the reporting rate, it suffers from a critical global search initialization error that invalidates the claim of global likelihood maximization, an unusual and potentially misspecified measurement model parameterization, the complete absence of a benchmark comparison, inadequate model diagnostics, and several additional methodological weaknesses that undermine the paper's main conclusion.

---

## Major Issues

### 1. Global Search Initialized from Previous mif2 Result, Not Base POMP Object

The global IF2 search initializes from the first local mif2 result object rather than the base pomp object. In `mumps.R` (and the corresponding chunk in blinded.Rmd), the global search uses:

```r
mif2(mifs_local[[1]], params = c(apply(mumps_box, 1, function(x) runif(1, x[1], x[2])),
                                  mumps_fixed_params))
```

Passing `mifs_local[[1]]` as the first argument rather than `mumpSEIR` (the base pomp object) causes each global replicate to inherit the cooling schedule and internal IF2 state from the converged local chain. The perturbation schedule of `mifs_local[[1]]` has already decayed through 100 IF2 iterations, so the "global" replicates start with near-zero perturbations even when initialized at a new point in parameter space. This effectively prevents the global search from exploring the box from a fresh start. The paper's claim that the global search provides coverage beyond the local search is not supported. Per the `pomp-global-search-init-audit` pattern, the fix is to replace `mifs_local[[1]]` with `mumpSEIR` as the first argument. Wheeler et al. (2024) emphasize the importance of computational adequacy and genuine multi-start optimization.

### 2. Negative Binomial Parameterization Is Epidemiologically Non-Standard and Misleading

The measurement model uses `dnbinom(cases, H, rho, give_log)` (dmeas) and `rnbinom(H, rho)` (rmeas), where H is the accumulator (weekly count of I-to-R transitions). In R's parameterization, `dnbinom(x, size=H, prob=rho)` represents a negative binomial with size parameter H and success probability rho. The mean of this distribution is H*(1-rho)/rho, not rho*H.

This creates two problems. First, the epidemiological interpretation of rho is not the reporting rate in the conventional sense (the fraction of true cases observed). In the standard SEIR measurement model, reported cases ~ NegBin(mean=rho*H, overdispersion=phi), where rho is interpretable as a reporting fraction in (0,1). Here, the expected cases equal H*(1-rho)/rho, which does not reduce to rho*H. The paper's discussion of rho as a "reporting rate" and its 95% CI of [11.14%, 14.52%] is therefore not directly interpretable in epidemiological terms.

Second, when H is near zero (which occurs frequently in the troughs of the seasonal cycle), H acts as the "size" parameter, making the measurement model near-degenerate (only zero cases can be observed when size=0). This creates a hard numerical boundary that distorts the likelihood surface near the trough periods.

The standard fix is to use `dnbinom_mu(cases, mu=rho*H, size=psi, give_log)` where psi is a separately estimated overdispersion parameter. This gives rho a conventional reporting-rate interpretation and decouples overdispersion from the size of H.

### 3. No Benchmark Comparison Against Non-Mechanistic Model

The paper does not compare the SEIR model's log-likelihood against any non-mechanistic baseline (e.g., ARIMA, auto-regressive negative binomial). Without such a comparison it is impossible to assess whether the seasonal SEIR structure captures meaningful epidemiological dynamics beyond what a simple autoregressive model would achieve. Wheeler et al. (2024) highlight this as the single most diagnostic check for mechanistic model utility: none of the 32 papers in their Haiti cholera literature review performed such a comparison. The authors should fit an auto-regressive negative binomial benchmark or SARIMA model on the same data and compare log-likelihoods quantitatively.

### 4. No Model Diagnostics

The paper presents no model diagnostic plots beyond a single forward simulation from the estimated parameters. Specifically absent are:

- Conditional log-likelihood plots to identify periods of poor fit (Wheeler et al. 2024 §Model diagnostics)
- Effective sample size (ESS) traces from the particle filter, which would reveal whether particle degeneracy is occurring at specific time points
- Filtering distribution comparisons (conditioned simulations vs. unconditioned forward simulations)
- Examination of reconstructed latent state trajectories (S, E, I) for biological plausibility

The single-simulation comparison (Figures 7 and 11) shows that the model can produce trajectories that qualitatively resemble the data, but this is a weak and informal measure of goodness-of-fit (Wheeler et al. 2024). The paper concludes that "mumps cases of Michigan in the 1970s can be well modeled by an SEIR pomp model," but this conclusion cannot be validated without formal diagnostic evidence.

### 5. Fixed Initial Conditions Are Unjustified and Potentially Influential

The model fixes E(0) = 20 and I(0) = 10 as hard-coded constants in the rinit Csnippet, while S(0) = eta*N is estimated. These are not epidemiologically justified. At the start of the observation period (September 1971, roughly four years after the MMR vaccine was licensed), the size of the exposed and infectious populations depends on the timing of prior epidemic waves and vaccination coverage — neither of which is addressed. Wheeler et al. (2024, §13) note that initialization strategy affected AIC by ~72 units in one of their models. The authors should either estimate E(0) and I(0) as initial value parameters (using `ivp()` in rw.sd) or perform a sensitivity analysis over plausible initial values and report whether conclusions change.

### 6. Profile Likelihood Seeds from Local-Search Box, Limiting Validity

The profile likelihood box for rho is constructed by filtering the global search results to high-likelihood rows:

```r
box = t(sapply(mifs_global, coef)) %>% ... %>%
  filter(logLik > max(logLik) - 10, logLik_se < 2) %>%
  sapply(range)
```

Because the global search was itself anchored to the local-search solution (Issue 1), this box reflects the locally optimal parameter region rather than the globally optimal one. The profile mif2 therefore explores rho values within a restricted box for the nuisance parameters. Additionally, the profile uses only two sequential mif2 passes (one at the default Nmif from mifs_local[[1]], then a second with Nmif=40), starting from `mifs_local[[1]]` as the base object — again inheriting the local-search cooling schedule. The confidence interval of [11.14%, 14.52%] is conditioned on the local optimum, not the global, and its statistical validity is uncertain.

---

## Minor Issues

### 7. Accumulator Variable Records Recoveries, Not New Infections or Reports

The accumulator H is incremented by `dN_IR` — the weekly count of transitions from I to R (recoveries). In syndromic surveillance, mumps cases are typically reported when patients are diagnosed as infectious, which corresponds to the I-to-R transition only if all recoveries are detected at the moment they recover. More commonly, cases are detected during the infectious period (closer to the EI transition). If reported cases correspond to newly infectious individuals (entering I), the accumulator should be `dN_EI` rather than `dN_IR`. The paper does not justify the choice of `dN_IR` with reference to the Project Tycho data-collection mechanism.

### 8. mu_EI and mu_IR Are Fixed at Values That Deserve Justification

The paper fixes mu_EI = 0.412 per week (corresponding to a mean incubation period of 1/0.412 ≈ 2.4 weeks) and mu_IR = 0.714 per week (mean infectious period of 1/0.714 ≈ 1.4 weeks). The CDC reference cited in the paper states an incubation period of approximately 17 days (≈ 2.4 weeks, consistent with mu_EI) but notes that mumps patients can remain infectious for over a week — suggesting a mean infectious period closer to 1–1.5 weeks, consistent with mu_IR = 0.714. However, neither value is formally derived or cited to a specific quantitative source. The authors should cite the specific values or ranges from which these were derived and acknowledge that fixing them introduces constraints on the fitted parameters.

### 9. Profile Confidence Interval Extraction Uses Raw rho Values Without Enforcing Profile Maximum = Global Maximum

The CI is extracted as:
```r
filter(logLik > max(logLik) - 0.5 * qchisq(df = 1, p = 0.95))
```

The cutoff is computed from `max(results$logLik)`, the profile maximum, rather than the global search maximum. If the profile maximum is lower than the global maximum (possible given Issue 6), the chi-squared cutoff is too permissive, potentially widening the CI. Standard practice is to use the global maximum as the reference point.

### 10. Computational Intensity Set to run_level = 2, Below Production Quality

The paper uses run_level = 2, with Np = 1000 particles, Nmif = 100 iterations, 30 local replicates, 60 global replicates, and 10 evaluation replicates. For a dataset with 100 weekly observations, 1000 particles is marginally adequate for likelihood evaluation (standard error of log-likelihood estimate is typically 0.5–2 units). Reporting 10 evaluation replicates per chain is sufficient. However, the convergence traces (Figure 5) show that several parameters (especially eta) retain high variance across local replicates even at iteration 100, suggesting that convergence has not been fully achieved at this computational level. The paper acknowledges this limitation but does not explore what happens at run_level = 3.

### 11. Global Search Box for rho Extends to 0.9 But Profile Only Covers 0.01–0.50

The global search allows rho up to 0.9 (box: `rho = c(0, 0.9)`), but the profile grid only covers rho from 0.01 to 0.50. If the global MLE for rho (at the global optimum, not the local one) falls outside [0.01, 0.50], the profile maximum would be at the boundary and the CI would be a boundary artifact. The paper does not verify that the profile maximum is in the interior of the grid. The reported MLE for rho (~12%) is well within [0.01, 0.50], so this is not a critical concern, but the paper should confirm the profile maximum is not at a boundary of the search space.

### 12. Conclusion Claims Seasonal Pattern Is Captured Without Quantitative Support

The conclusion states that "the seasonality have already been captured by this model, and usually our model only differs by a constant from the original data." No quantitative measure supports this claim. There is no AIC comparison between the seasonal and non-seasonal model, no likelihood ratio test for the seasonal terms (b2), and no conditional log-likelihood plot showing fit across seasons. The paper should provide quantitative evidence for the importance of the seasonal component — for example, fixing b2 = 0 and comparing log-likelihoods.

### 13. No Assessment of R_0 or Other Epidemiologically Interpretable Quantities

The fitted parameters (b1, b2, Phi, rho, eta) are not translated into epidemiologically meaningful quantities such as the basic reproduction number R_0 = exp(b1) / mu_IR. For an SEIR model with seasonal forcing, R_0 varies with time; reporting the mean R_0 and its seasonal range would allow comparison with independent estimates for mumps (typically R_0 ≈ 4–7 for pre-vaccine era, lower post-vaccine). This check for corroboration with scientific knowledge (Wheeler et al. 2024 §11) is entirely absent.

### 14. Pairwise Plots for Local Search Are Based on Only 10 Points

Table 1 and Figure 6 report results from only the top 10 local search replicates. The pairwise scatter plot in Figure 6 is described as "too sparse to give a clear picture" — this is a self-defeating observation. The plot should include all 30 local replicates, not just the top 10, to reveal any structure in the likelihood surface.

### 15. Paper Uses Single Forward Simulations (nsim = 1) for Fit Assessment

Figures 7 and 11 each show only a single simulation from the estimated parameters, not a distributional envelope. A single stochastic trajectory can look good or bad by chance. The paper would be better served by plotting 50–100 simulations and overlaying the data to assess whether the observed data lies within the ensemble's range — particularly during the peaks of the two epidemic waves. The claim that the model "can describe the seasonal characteristics" (p. 7) is based on a single lucky trajectory.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-mc-noise-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-domain-violation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/hp-filter-lambda-misspecification/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/ode-compartment-observation-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project14/mumps.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project14/mumpSEIR.c`
