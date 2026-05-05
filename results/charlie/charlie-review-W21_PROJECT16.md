# Peer Review: W21 Project 16
## Volatility analysis on the Shanghai Composite Index

---

## Summary

This project applies a GARCH(1,1) model and a stochastic volatility POMP model (based on the Breto 2014 leverage formulation) to weekly log-returns of the Shanghai Composite Index (570 observations, 2010–2021). The GARCH model is used as a benchmark, and the POMP model is fit via local and global IF2 searches, followed by a profile likelihood over phi. While the project correctly applies the course-standard POMP workflow and uses logmeanexp for log-likelihood aggregation, it contains several serious methodological errors: the global IF2 search is initialized from a previous mif2 result object rather than the base pomp object (defeating the purpose of a global search); phi is not excluded from rw.sd during the profile likelihood computation (causing it to drift and invalidating the profile); the pfilter in the profile section evaluates on the mif2 result rather than the base pomp object; and the profile maximum value is missing from the text. The POMP model's lower log-likelihood than GARCH is noted but attributed solely to computational limitations rather than to structural model issues or the algorithmic errors present in the code.

---

## Major Issues

### 1. Global search initialized from previous mif2 result object, not the base pomp object

In the global search chunk (lines 326-328), the foreach loop calls:

```r
mif2(if1[[1]], params=apply(Shanghai_box,1,function(x)runif(1,x)))
```

The first argument is `if1[[1]]`, which is a mif2 result from the prior local search, not the base `Shanghai.filt` pomp object. This is the anti-pattern identified in the `pomp-global-search-init-audit` skill: passing a previous IF2 result object as the first argument to mif2 causes the global search to inherit the cooling schedule of the local chain. Because `if1[[1]]` has already run for Nmif=50 iterations with cooling.fraction.50=0.5, its perturbation schedule is near or at its terminal cooling state. The new random starting parameters from `apply(Shanghai_box, 1, runif)` are applied to `params=` but the inherited cooling schedule means very few functional IF2 iterations are performed from those new starts before perturbations shrink to near zero. The reported global maximum of 1264 may therefore simply be a re-confirmation of the local-search optimum rather than a genuine global maximum. The fix is to replace `mif2(if1[[1]], ...)` with `mif2(Shanghai.filt, ...)` in the global search loop.

### 2. Profile likelihood: phi is not excluded from rw.sd, allowing it to drift

In the profile chunk (lines 384-390), the rw.sd specification is:

```r
rw.sd=rw.sd(
  sigma_nu  = Shanghai_rw.sd_rp,
  mu_h      = Shanghai_rw.sd_rp,
  sigma_eta = Shanghai_rw.sd_rp,
  G_0       = ivp(Shanghai_rw.sd_ivp),
  H_0       = ivp(Shanghai_rw.sd_ivp)
)
```

Phi is not listed here, but the critical issue is that phi is the profiled parameter and the mif2 call allows it to be part of the optimization (only other parameters are perturbed, which is structurally correct here in that phi is not explicitly perturbed). However, examining the profile design: `guesses` contains phi values drawn from `profile_design()`, and the mif2 start is set via `start=c(unlist(guesses[i,]),params_test)`. This uses `c()` concatenation, which in R may produce a vector where params_test's phi value takes precedence over guesses' phi value (or vice versa, depending on how pomp resolves duplicates). More critically, phi is not fixed (rw.sd for phi = 0 is never set), which means the profile should be invalid. Additionally, the mif2 is called on `if1[[1]]` (not `Shanghai.filt`), compounding the cooling schedule problem from Issue 1. The pfilter evaluation also uses `phi_pro` (the mif2 result object) rather than `Shanghai.filt`, meaning the likelihood is evaluated at whatever parameters the optimizer moved to — not at the profile-grid phi values. This combination invalidates the profile likelihood and any confidence interval derived from it.

### 3. Profile mif2 uses params_test as a fallback, potentially overriding profile-grid values

At line 382, the profile mif2 call uses `start=c(unlist(guesses[i,]),params_test)`. In R, `c()` concatenates named vectors without deduplication. Since `params_test` includes phi, G_0, H_0, sigma_nu, mu_h, and sigma_eta — all of which are also in `guesses[i,]` — the resulting vector has duplicate names. The behavior depends on which occurrence pomp uses (typically the first). If the guesses-derived values appear before params_test in the concatenation, the profile starting points may be correct; if not, they revert to params_test for the duplicated parameters. This ambiguity makes the profile grid initialization unreliable and should be replaced with explicit parameter vector construction that assigns profile-grid values without duplication.

### 4. Profile likelihood CI reference and missing maximum value in text

At lines 416-418, the chi-squared cutoff is computed as:

```r
yintercept=max(results$logLik)-0.5*qchisq(df=1,p=0.95)
```

where `results` is loaded from the full `Shanghai_params.csv` file, which contains results from all searches (local, global, and profile). This is partially correct in using the full results file. However, if the profile IF2 is initialized from `if1[[1]]` (the local mif2 object, as in Issue 1), and evaluated via `pfilter(phi_pro, ...)` rather than `pfilter(Shanghai.filt, ...)`, the log-likelihoods in the profile results may not be comparable to those from the global search. Additionally, line 422 contains an incomplete sentence: "The plot above suggests that the maximum log-likelihood over phi is achieved when phi = ." The phi value at the MLE is missing, indicating the analysis was incomplete at the time of submission. No confidence interval bounds for phi are reported in the text.

### 5. POMP model fails to outperform GARCH benchmark; response is inadequate

The GARCH(1,1) log-likelihood is 1269.58 (from fGarch), while the best POMP log-likelihood from the global search is 1264. The authors acknowledge this gap in the conclusion and attribute it entirely to "limitation of time and computational sources," proposing to "increase the computational force" in future work. Per the course convention (531-conventions.md) and the weakness reference (Error 1.15), when a POMP model fits substantially worse than the benchmark, the appropriate first response is to revise model structure, not simply add more computation. No model diagnostic examination (ESS, conditional log-likelihoods, residual analysis) is performed to determine whether the gap reflects identifiability issues, model misspecification, or genuine computational inadequacy. Furthermore, because the GARCH log-likelihood is from `fGarch` which uses a non-standard likelihood normalization (as noted in Error 2.9 of the weakness reference), direct numerical comparison requires care to ensure both use the same scale and data. This comparison is not discussed.

### 6. pfilter in profile section evaluates on mif2 result, not base pomp object

At line 392, the profile likelihood evaluation is:

```r
evals = replicate(Shanghai_Nreps_eval, logLik(pfilter(phi_pro,Np=1000)))
```

Here `phi_pro` is the mif2 result object, not `Shanghai.filt`. While pfilter applied to a mif2 result object can work (it uses the parameters stored in the object), the parameters in `phi_pro` are the optimized parameters after the constrained mif2 run — which, as noted in Issue 2, may have allowed phi to drift from its profile-grid value. Evaluating the likelihood at drifted parameters does not give the profile likelihood at the specified grid values of phi. The correct pattern is `pfilter(Shanghai.filt, params=coef(phi_pro), Np=1000)`, which evaluates the base pomp model at the parameters found by the profile optimizer.

### 7. No model diagnostics

No effective sample size (ESS) plots, conditional log-likelihood plots, or simulation-based diagnostic comparisons are presented for the POMP model. The particle filter is run in Section 4.1 on `sim1.filt` (a simulated dataset, not the actual Shanghai data), which does not constitute a diagnostic of the fit to observed data. The local and global IF2 trace plots are shown (`plot(if1)` and `plot(if.box)`), but no commentary is provided on whether the log-likelihood trace converges upward consistently across runs. Wheeler et al. (2024) identify conditional log-likelihood plots and ESS monitoring as standard diagnostics; their absence makes it impossible to identify where and why the POMP model underperforms GARCH.

---

## Minor Issues

### 8. pfilter run on sim1.filt, not Shanghai.filt

Section 4.1 runs the particle filter evaluation on `sim1.filt`, which is the pomp object built around a simulated dataset (generated from `simulate(sim1.sim, seed=1, params=params_test)`), not the observed Shanghai log-return data. The log-likelihood reported is therefore for the simulated data under the test parameters, not for the real data. This section's purpose is unclear and may be misleading. If the intent is to verify that the pfilter runs without error before the main analysis, this should be labeled explicitly and the result not presented as meaningful inference on the Shanghai data.

### 9. Incomplete ACF interpretation and assumption of independence

Section 2.1 concludes from the ACF plot that "the data are all independent." In the context of a GARCH/SV model analysis, the relevant structure is in the squared returns (which capture volatility clustering), not the raw returns. The ACF of squared or absolute returns typically shows significant autocorrelation even when the returns themselves appear uncorrelated — this is the motivation for GARCH modeling. The authors do not check the ACF of squared demeaned returns, missing the primary evidence for conditional heteroskedasticity.

### 10. GARCH AIC table uses tseries::garch with non-standard likelihood normalization

The AIC table in Section 3.1 is computed using `tseries::garch`. As documented in the course weakness reference (Error 2.9), `tseries::garch` reports a non-standard log-likelihood value. The `fGarch::garchFit` log-likelihood reported in Section 3.2 (1269.58) differs from what would be computed by `tseries::garch`. While both objects are used (AIC selection via tseries, then refitting via fGarch), no discussion addresses whether the AIC values in the table are on the same scale as the POMP log-likelihoods used for final comparison. This potentially invalidates the GARCH versus POMP log-likelihood comparison.

### 11. phi box constraint in global search is extremely narrow

The global search box for phi is `c(0.9950, 0.9999)` (lines 317-318), which is a highly restricted range. This range essentially forces the global search to confirm that phi near 1 is optimal, rather than genuinely exploring the full parameter space. If the true MLE for phi were outside this interval, the global search would never find it. The choice of this narrow box should be explicitly motivated with reference to the model's stationarity constraints or prior findings.

### 12. No simulation-based model validation

No plot comparing simulated trajectories from the fitted POMP model to the observed log-returns is provided. While `simulate(sim1.sim, ...)` is used to create a simulated dataset in Section 4.1, this is for debugging purposes and uses `params_test` (not estimated parameters). A standard POMP analysis includes forward simulation from the estimated MLE parameters and visual overlay of simulated trajectories with observed data to assess goodness of fit (Checklist item 9 in SKILL_pomp.md).

### 13. Profile phi range may not include the MLE

The profile is constructed over phi in the range [0.80, 0.99999] (line 372). However, the global search box for phi is [0.9950, 0.9999] (line 317), which means the global search MLE for phi is somewhere in that narrow range. The profile covers a much wider range but was computed using only `nprof=2` guesses per phi value, providing very sparse coverage at each grid point. With 50 phi values and nprof=2, only 100 profile runs are performed total — which with one restart per grid point is inadequate for identifying the constrained maximum at each grid point.

### 14. Missing parameter estimates table

No table of final estimated parameter values (MLE from global search) is presented. The authors report only summary statistics for log-likelihoods. The estimated values of sigma_nu, mu_h, phi, sigma_eta, G_0, and H_0 at the MLE should be stated explicitly along with their profile-based confidence intervals. Without these, the results cannot be replicated or compared to prior literature on SV models.

### 15. Causal language and mischaracterized conclusion about GARCH

Section 3.2 states "The model suggests that the volatility should slightly shift positively as time moving forward." This claim is not supported by the GARCH model — a GARCH(1,1) model is stationary (given alpha + beta < 1) and does not imply an upward trend in volatility. This appears to be a misreading of the fitted parameter values. Additionally, the conclusion refers to performing "a simulation study using the POMP model" when the analysis is actually a likelihood-based parameter estimation exercise, not a simulation study.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project16/blinded.Rmd`
