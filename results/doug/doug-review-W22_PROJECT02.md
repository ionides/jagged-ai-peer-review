# Peer Review: W22 Project 02
**"Investigation of Ebola in Guinea and Sierra Leone"**

---

## Summary

The paper fits a SEIRDF compartmental model to daily confirmed Ebola cases from Guinea and Sierra Leone (2014–2016), motivated by the known role of funeral transmission. The authors use iterated filtering (IF2) for likelihood-based inference and compute profile likelihoods for the transmission parameter Beta. While the paper demonstrates familiarity with the pomp workflow and provides a scientifically motivated model structure, it suffers from several critical methodological and implementation errors that undermine the validity of the parameter estimates, profile likelihoods, and conclusions. The most serious issues are: (1) the global search is anchored to a local-search result object rather than the base pomp object; (2) the measurement model uses a binomial distribution without overdispersion, likely misspecifying the observation process; (3) the accumulator variable H accumulates total transitions out of I rather than new confirmed cases, creating a semantic mismatch; (4) no benchmark comparison to any non-mechanistic model is performed; and (5) the population size for Sierra Leone contains what appears to be a factor-of-10 data entry error.

---

## Major Issues

### 1. Global Search Anchored to Local mif2 Result Object (pomp-global-search-init-audit)

In both the Guinea and Sierra Leone global search sections, the global IF2 replicates are launched using `mf1 <- mifs_local[[1]]` as the first argument to `mif2()`:

```r
mf1 <- mifs_local[[1]]
...
mf1 %>%
    mif2(params=c(guess,fixed_params)) %>%
    mif2(Nmif=200) -> mf
```

This passes a previous `mif2` result object as the base, which causes each global replicate to inherit the cooling schedule of `mifs_local[[1]]` (already near its final cooled state after 100 IF2 iterations). The new random `guess` parameters are applied, but the cooling perturbations shrink to near zero within the first few additional iterations, so the global search does not genuinely explore the parameter box from fresh starts. The correct pattern is `mif2(base_pomp_object, params=c(guess, fixed_params), ...)` where `base_pomp_object` is the original `pomp()` call result. The reported "global maximum" may therefore not differ meaningfully from the local optimum. All parameter estimates and confidence intervals derived from the global search are potentially unreliable. (Wheeler et al. 2024, §Computational adequacy.)

**Fix:** Replace `mf1 %>% mif2(params=...)` with `ebola %>% mif2(params=..., Np=..., Nmif=..., ...)` in the global and profile search loops for both countries.

---

### 2. Measurement Model: Binomial Without Overdispersion

The `dmeas` and `rmeas` Csnippets both use the binomial distribution:

```c
lik = dbinom(reports, H, rho, FALSE) + tol;
reports = rbinom(H, rho);
```

Epidemic case count data is universally overdispersed relative to the binomial (excess variance beyond `H * rho * (1-rho)`). The binomial forces the variance to equal the mean times `(1-rho)`, which is implausible for Ebola surveillance data characterized by clustering, reporting delays, and heterogeneous contact rates. Fitting an underdispersed measurement model to overdispersed data will cause the particle filter to assign very low likelihood to realistic simulation trajectories, pushing the optimizer toward implausible parameters. The standard practice (Wheeler et al. 2024, §Stochasticity) is to use a negative binomial measurement model with an estimated overdispersion parameter `k`. The authors do not justify the binomial choice or test whether overdispersion is present.

**Fix:** Replace `dbinom`/`rbinom` with `dnbinom_mu`/`rnbinom_mu` parameterized as `mu = rho * H` and `size = k`, adding `k` as an estimated parameter.

---

### 3. Accumulator Variable H Accumulates Wrong Flow

The step function accumulates `dN_IR` — transitions from the infectious compartment I to R and D combined — into H:

```c
H += dN_IR;
```

However, the observable data records newly confirmed (reported) cases, which corresponds to new entries into the symptomatic/infectious compartment from E, not exits from I. In the SEIRDF model, individuals become reportable when they transition from E to I (i.e., `dN_EI`), not when they recover or die. Accumulating exits from I into H means the measurement model compares reported daily cases against a count of recoveries-plus-deaths, which has different timing and magnitude properties. This is a semantic mismatch (see `pomp-accumvar-semantic-audit`): the reporting rate `rho` will absorb the ratio of exits to entries in I rather than the true detection probability, and all rate parameters may shift to compensate. All estimated parameter values are potentially distorted.

**Fix:** Change `H += dN_IR` to `H += dN_EI` in the Csnippet, so that H tracks newly symptomatic cases entering I (the flow that corresponds to new confirmed infections).

---

### 4. No Benchmark Comparison Against Non-Mechanistic Model

The paper presents no comparison of the SEIRDF model against any non-mechanistic statistical benchmark (e.g., ARMA, negative binomial autoregression). Without such a comparison, it is impossible to assess whether the mechanistic model captures meaningful structure beyond what a simple statistical model would achieve. Wheeler et al. (2024) found that none of the 32 papers in their Haiti cholera review performed such a comparison, and their auto-regressive negative binomial benchmark revealed that several models failed to outperform it. The SEIRDF model has 7–9 parameters and may not achieve likelihood values competitive with a 4–5 parameter ARIMA model.

**Fix:** Fit an ARIMA or negative binomial autoregression model to both series and compare log-likelihoods quantitatively.

---

### 5. Population N for Sierra Leone Contains a Factor-of-10 Error

The text states `N=16190280` for Sierra Leone's population (approximately correct for 2015), but the code uses `N=6190280` in both the simulation and the fixed parameters:

```r
params <- c(..., N=6190280)
fixed_params = c(F_size=50, N=6190280)
```

This is approximately 38% of the correct population. Because the force of infection is `Beta * I / N`, using `N = 6190280` instead of `16190280` inflates the effective per-capita contact rate by a factor of ~2.6. This means the estimated Beta for Sierra Leone is approximately 2.6 times smaller than it would be under the correct population, making the stated comparison of transmission rates between Guinea and Sierra Leone meaningless. The confidence intervals for Beta reported for the two countries cannot be validly compared.

**Fix:** Replace `N=6190280` with `N=16190280` consistently throughout the Sierra Leone sections and re-run all analyses.

---

### 6. Profile Likelihood Is Flat Across Entire Box; Confidence Interval Is Uninformative

For both countries, the authors report that the 95% confidence interval for Beta spans nearly the entire search box (Beta from 3.003 to 6.974 for Guinea; similarly for Sierra Leone). The authors themselves acknowledge this issue:

> "This fact indicated that maybe parameter Beta in SIERDF model above is weakly identifiable..."

However, a profile likelihood spanning almost the entire search box does not merely indicate weak identifiability — it indicates that the profile optimization has likely not found a genuine maximum anywhere in the box. This is consistent with the global search initialization error (Issue 1) and possibly with the population N error (Issue 5) and accumulator mismatch (Issue 3) producing a likelihood surface that is genuinely flat over Beta given the mis-specified model. The text's conclusion that "transmission rates are similar in the two countries" because they share the same confidence interval is not a valid inference from these profiles: the intervals both span the entire search domain because the optimization failed, not because the data truly support identical Beta values.

**Fix:** After correcting Issues 1, 3, and 5, re-run the profile likelihood with a corrected global search initialization and confirm whether a proper peaked profile can be obtained.

---

### 7. F_size Fixed Without Justification

The parameter `F_size` (the average funeral attendance) is fixed at 50 for both countries and is not estimated:

```r
fixed_params = c(F_size=50, N=10628972)
```

No reference is provided for this value, and no sensitivity analysis is performed. Because `F_size` directly multiplies the funeral transmission term `rbinom(F_size * F, 1 - exp(-Beta2 / F_size * dt))`, fixing it without justification conflates `Beta2` and `F_size` in the likelihood. The parameters are not separately identifiable from the data if `F_size` is fixed: only the product `Beta2 / F_size` enters the hazard. The authors should either estimate `F_size` jointly with `Beta2`, fix it to a literature-derived value with citation, or note that only the product is estimable.

---

### 8. rw.sd Values Are Very Small Relative to Parameter Scales on the Untransformed Scale

The rw.sd settings of 0.002 for all parameters may be adequate on the log/logit scale (since `partrans` transforms Beta to log-Beta and rho to logit-rho). However, the authors provide no justification that these values were calibrated for the expected parameter uncertainty. For Beta starting at 17 (Guinea), the log scale value is ~2.8, and a perturbation of 0.002 corresponds to a 0.2% change per iteration. Whether this allows adequate exploration depends on the likelihood surface curvature, which is not assessed. No convergence diagnostics are presented in the text to verify that the traces have stabilized.

---

## Minor Issues

### 9. dmeas/rmeas Boundary Handling Inconsistency

The `dmeas` Csnippet sets `lik = tol` when either `reports == 0` or `H == 0`, but `rmeas` draws from `rbinom(H, rho)` which naturally returns 0 when `H = 0`. There is an asymmetry: `dmeas` uses `tol = 1e-25` (effectively a negligible positive likelihood) rather than the exact binomial probability `dbinom(0, 0, rho) = 1`. While this has minimal practical effect when `reports > 0`, the handling when `reports = 0` and `H > 0` falls through to `tol` rather than `dbinom(0, H, rho)`, which would be the correct zero-count probability. This could artificially penalize zero-report days.

### 10. rm(list=ls()) Inside Document

The Sierra Leone section begins with `rm(list=ls())`, which clears the R workspace mid-document. This is a reproducibility anti-pattern: it makes the document sensitive to execution order and prevents verification that the Guinea and Sierra Leone models share identical structural code. Code supplement checklist standards recommend against global workspace modifications.

### 11. No Quantitative Goodness-of-Fit Values Reported

The text discusses convergence and profile likelihoods but never reports the maximum log-likelihood values achieved for either country. Without these values, it is impossible to assess the absolute model fit, compare the two countries quantitatively, or evaluate the adequacy of the particle filter. Wheeler et al. (2024) emphasize that visual comparisons of simulated to observed trajectories are "only a weak and informal measure of goodness-of-fit."

### 12. No Model Diagnostics Beyond Simulation Plots and Pairs Plots

The paper presents forward simulations from hand-chosen initial parameters (§Simulation and Guess the parameter) but does not present: (a) conditional log-likelihoods per time step to identify periods of poor fit, (b) effective sample size traces from the particle filter, or (c) filtering-distribution simulations conditioned on observed data. The pairs plots show high scatter and no clear convergence, which the authors interpret as motivation to proceed to the global search, but no further diagnostics are provided after the global search to verify adequate fit.

### 13. Conclusions Overstate Comparison Between Countries

The conclusion states: "we observe very similar transmission rates in Guinea and Sierra Leone." This conclusion is based on the two confidence intervals for Beta spanning the same range [3, 7] — but both intervals span nearly the entire search box, which the authors themselves acknowledge is due to weak identifiability. Two parameters are not "similar" simply because their flat confidence intervals overlap; the data do not provide evidence to distinguish any value of Beta in [3, 7] from any other, let alone to conclude that the two countries have the same rate. This inference is not statistically valid.

### 14. Missing pomp and Package Version Information

The code does not record the version of pomp or any other packages used. The pomp API has changed substantially across versions, and results may not reproduce on current CRAN releases. A `sessionInfo()` output or renv lockfile should be included. (Code supplement checklist, §Documentation.)

### 15. Initial Conditions Are Fixed Without Sensitivity Analysis

The initial number of infected individuals is hardcoded (`I = 482` for Guinea, `I = 935` for Sierra Leone) and `R = nearbyint((1-eta)*N)` implies nearly all recovered individuals at t=0, which is inconsistent with the outbreak beginning. No sensitivity analysis is performed on initial conditions. Wheeler et al. (2024) note that initialization strategy can affect AIC by ~72 units. The choice of `eta` as a fitted parameter partially addresses this, but the hard-coded initial `I` values and the `R = (1-eta)*N` initialization deserve justification.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project02/blinded.Rmd`
