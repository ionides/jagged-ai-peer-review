# Peer Review: W22 Project 21
**Title:** ARMA and POMP Analysis on COVID-19 Variants in the US

---

## Summary

This project applies ARMA and POMP-based compartment models to daily US COVID-19 case counts (January 2020 – April 2022), segmenting the data into three variant-defined periods (pre-Delta, Delta, Omicron) and fitting SEIR and SEIRV models to each segment. The segmented approach is scientifically motivated and the use of particle filters and iterated filtering reflects course methodology. However, the project has several critical technical flaws: the `dmeasure` and `rmeasure` functions specify inconsistent standard deviations (rendering all likelihood evaluations based on a mismatched observation model), the vaccination rate term `alpha/N` in both SEIRV models is wrong by a factor of N, initial conditions do not conserve population in either SEIRV model, and no profile likelihoods are computed for any of the three models. Computational effort for the pre-Delta model is insufficient (only 10 global search replicates with a best-run SE of ~9.7 log-likelihood units), and the declared parameter `tau` appears in `paramnames` but is never used in any Csnippet equation. These issues collectively undermine the reliability of the reported parameter estimates and goodness-of-fit values.

---

## Major Issues

### 1. Inconsistent standard deviation between `dmeasure` and `rmeasure` (all three models)

In all three POMP models, `dmeasure` computes `sd_cases = sqrt(mean_cases * mean_cases)`, which simplifies to `sd_cases = mean_cases = rho * H`. However, `rmeasure` draws `reports = rnorm(rho*H, sqrt(rho*H))`, which uses standard deviation `sqrt(rho*H)`. These are the same distribution only when `rho*H = 1`. In practice the two functions specify different distributions: `dmeasure` evaluates the density of Normal(`rho*H`, `rho*H`) while `rmeasure` samples from Normal(`rho*H`, `sqrt(rho*H)`). This inconsistency means that every likelihood evaluation in this project is scored against the wrong observation density relative to what the simulator produces. All reported log-likelihoods reflect a measurement model that is internally contradictory. The correct approach is to pick one parameterization and apply it consistently, for example using `sd_cases = sqrt(rho*H*(1 + tau*rho*H))` for a negative-binomial-like model, or simply `sqrt(rho*H)` in both snippets for a Poisson-like approximation (Wheeler et al. 2024, §Measurement model specification).

**CC-Yes** (Error 1.3: unit/scale inconsistency in POMP code)

---

### 2. Vaccination rate formula wrong by a factor of N in both SEIRV models

The SEIRV transition for vaccination is coded as:
```
double dN_SV = rbinom(S, 1-exp(-alpha/N*dt));
```
This gives each susceptible individual a per-day vaccination probability of `alpha/N`. With `N = 3 × 10^8` and the best-fit `alpha ≈ 0.109` (Delta segment), the daily per-person vaccination rate is `0.109 / 3×10^8 ≈ 3.6×10^-10`, implying it would take approximately 7.5 million years to vaccinate the susceptible population. For a per-capita vaccination rate, the correct expression is `1-exp(-alpha*dt)`, not `1-exp(-alpha/N*dt)`. The division by N makes `alpha` dimensionless and biologically incoherent. The same error appears in the Omicron SEIRV model. As a consequence, the vaccination compartment V receives essentially no flow during the simulated periods and the parameter `alpha` is effectively unidentifiable in any meaningful biological sense.

---

### 3. Initial conditions do not conserve population in either SEIRV model

**Delta model:** With `eta = 0.1`, `N = 3×10^8`, the initialization sets `S = 3×10^7`, `E = 49087`, `I = 99486`, `V = 900000`, and `R = round(N*(1-eta) - (49087 + 99486 + 900000 + 49743))`. This gives `S+E+I+R+V = 299,950,257`, which is 49,743 less than `N`. The discrepancy arises because `H` (an accumulator variable that is not a population compartment) is subtracted in the R formula but should not be.

**Omicron model:** `V` is initialized as `round(N*(0.5945-0.5935)) = round(N*0.001) = 300,000`, representing only the 0.1% change in vaccination rate over two days rather than the ~59.4% of the population that was actually vaccinated by December 2021. The population sum is short by 87,248. Both errors distort the effective population sizes and initial susceptible fractions used in all downstream inference (Wheeler et al. 2024, §Initial conditions).

---

### 4. No profile likelihoods computed for any model

Profile likelihoods are not computed for any of the three POMP models. Without profile likelihoods, there is no basis for assessing parameter identifiability or constructing confidence intervals. The parameter `eta` in the pre-Delta model, for example, appears constrained near 0.09–0.10 across all runs, but without a profile it is impossible to determine whether this reflects a genuine likelihood ridge or a consequence of the narrow initial search box. Profile likelihoods are standard practice for this course and essential for any formal uncertainty quantification (SKILL_pomp.md §5; Error 1.9 in the weakness reference).

**CC-Yes** (Error 1.9)

---

### 5. Pre-Delta global search: only 10 replicates and large Monte Carlo SE

The global search for the pre-Delta SEIR model uses only 10 `mif2` replicates (file `mifs_global_1.rds`), compared to 20 for the other two models. More critically, the best-run SE for the pre-Delta global search is ~9.72 log-likelihood units, which is very large relative to the inter-run variation in log-likelihoods (the second-best result is at –14,894 vs. –14,149, a difference of ~746 units, so the top run is distinguishable—but the SE of ~9.7 means the best-run's own estimate is uncertain at the level of ~±20 log-units at 2σ). The large SE stems from using only `Np = 50,000` particles for a 464-day time series; more particles or more evaluation replicates are needed to pin down the MLE. The best global search result for this segment should be treated with caution given this Monte Carlo noise (Wheeler et al. 2024, §Computational adequacy; SKILL_pomp.md §6).

**CC-Yes** (Error 1.4)

---

### 6. `tau` declared in `paramnames` but never used in any Csnippet

The parameter `tau` appears in `paramnames` for all three models and is assigned initial values and random walk perturbations (for the pre-Delta local search, `rw.sd` does not include tau, but tau is included in the global search box `tau=c(0.85,1.1)` for Model 1 and `tau=c(0,2)` for Model 2). Despite this, `tau` does not appear anywhere in `seir_step`, `seirv_step`, `seirv2_step`, `dmeas`, or `rmeas`. It was presumably intended as an overdispersion parameter but was never integrated into the model equations. As a result, `tau` occupies a free dimension in the optimization that contributes noise to parameter estimates without any effect on model behavior. The optimizer wastes computational budget searching over a phantom parameter.

---

### 7. No benchmark comparison for ARMA vs. POMP models

The ARMA(4,4) model is fit to the full dataset (log-likelihood ≈ –9,761) but no quantitative comparison is made between the ARMA model and any of the three POMP models. Because the POMP models are fit to sub-segments rather than the full dataset, direct comparison is non-trivial, but the report does not attempt even a segment-specific ARMA benchmark. Without such a comparison there is no objective baseline for evaluating whether the mechanistic models capture structure beyond what a simple statistical model achieves. The course explicitly teaches benchmark comparison as part of model validation (SKILL_pomp.md §2; Error 1.6 in the weakness reference).

**CC-Yes** (Error 1.6)

---

### 8. No convergence diagnostics presented for global search

Trace plots for the global search runs are not shown for any of the three models. Only trace plots from local searches are displayed. Without global search trace plots, there is no visual evidence that the iterated filtering runs converged from diverse starting points to a common high-likelihood region. The pairs plots shown (loglik vs. parameters) indicate that for the Delta model the top two solutions cluster near Beta ≈ 6–7, but divergence among lower-ranking runs is large, suggesting the likelihood surface may not have been adequately explored (Wheeler et al. 2024, §Computational adequacy; Error 1.8).

**CC-Yes** (Error 1.8)

---

## Minor Issues

### 9. `dmeasure` uses a normal approximation that can produce negative support

The measurement model uses `pnorm` to evaluate the probability that a rounded observation equals `reports`. While the continuity-correction approach is reasonable, the underlying Normal distribution has support on all reals, so when `rho*H` is small (as it can be at the start of the pre-Delta or early Delta periods), the model assigns non-negligible probability to negative case counts. A negative-binomial measurement model (as used in Wheeler et al. 2024) would be more appropriate for count data and would naturally handle overdispersion.

---

### 10. Local search for pre-Delta uses very small rw.sd values

The local search for the pre-Delta SEIR model uses `rw.sd(Beta=0.002, rho=0.002, eta=ivp(0.002))`, with `mu_EI` and `mu_IR` not perturbed at all. This means the optimizer can only move in three of the six non-fixed parameter dimensions, effectively locking `mu_EI = 0.08` and `mu_IR = 1.15` at their initial values throughout the local search. The parameter trace plots confirm this: `mu_EI` and `mu_IR` show no variation. This makes the local search very narrow and may explain why the global search produced a substantially better likelihood (–14,149 vs. –16,071 from local). The rw.sd values for `Beta` and `rho` are also very small (0.002 vs. the course standard of 0.02 on a log scale), which would slow convergence considerably.

---

### 11. Delta local search uses Np=2000 with only 5 pfilter evaluations

For the Delta model likelihood evaluation in the local search, the code uses `replicate(5, logLik(pfilter(mf, Np=2000)))`. With only 5 replicates and 2,000 particles on a 214-day series, the Monte Carlo SE on the log-likelihood estimate may be substantial. In contrast, the global evaluation uses `Np=50000` with 10 replicates. The inconsistency in evaluation quality between local and global searches makes the "best local search" results unreliable as a starting point for global search box construction.

---

### 12. Global search box for pre-Delta is very narrow

The pre-Delta global search box (`covid_box1`) constrains `mu_EI` to (0.07, 0.09) and `mu_IR` to (1.0, 1.25), both of which are narrow ranges centered near the fixed initial values used in the local search. This box essentially restricts the global search to a small neighborhood of the initial guess rather than exploring the parameter space broadly. The best global search result may therefore be a local maximum rather than the true global MLE.

---

### 13. ARMA model applied to non-stationary, non-homogeneous full-dataset

The ARMA(4,4) model is fit to the full dataset (all three variant periods combined) without any transformation or differencing, even though the time series clearly exhibits heterogeneous variance and at least two major waves. The residual ACF and QQ-plot both indicate non-IID residuals and heavy tails, yet no remediation is attempted (no log transform, no ARIMA). While the project moves on to POMP modeling, the inadequate ARMA baseline means the "benchmark" model is poorly specified, making it an even weaker reference than it could be (Error 2.5; Error 2.3 in the weakness reference).

---

### 14. Omicron global search finds sigma ≈ 0.27–0.62, but biological plausibility not discussed

The best Omicron global results produce `sigma` (vaccine efficacy reduction factor) values of 0.27–0.62, suggesting that vaccinated individuals have 27–62% of the transmission rate of susceptible individuals. No comparison to independent estimates of Omicron vaccine effectiveness (which were available by April 2022) is provided. Implausible or surprising parameter estimates should be interpreted against external evidence (Wheeler et al. 2024, §Corroboration with scientific knowledge).

---

### 15. No model diagnostics beyond forward simulation

Diagnostic analysis is limited to visual inspection of forward simulations. No conditional log-likelihood plots, effective sample size monitoring, or filtering distribution comparisons are presented for any of the three models. In particular, the filtering distribution (simulations conditioned on observed data) would reveal whether the model's reconstructed latent states are biologically plausible, and per-observation log-likelihood plots would identify specific time windows where the model fails (Wheeler et al. 2024, §Model diagnostics).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/local_results_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/global_search_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/local_results_2.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/global_search_2.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/local_results_3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/global_search3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/mifs_global_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/daily_case_us.csv`
