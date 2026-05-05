# Peer Review: W21 Project 16
## Volatility Analysis on the Shanghai Composite Index

---

## Summary

This project applies two models to characterize the return volatility of the Shanghai Composite Index: a GARCH(1,1) benchmark fitted via the `tseries`/`fGarch` packages, and a stochastic volatility (SV-in-mean) POMP model adapted from Breto (2014) and course lecture notes. The authors fit the POMP model using IF2 (`mif2`) via a two-stage local/global search and report a profile likelihood over the persistence parameter phi. While the project correctly identifies the GARCH model as a baseline, correctly uses likelihood-based inference for the POMP model, and attempts a profile likelihood, it has substantial methodological, computational, and reporting weaknesses that prevent any reliable conclusions from the POMP analysis. In particular, the global search is initialized from a prior IF2 result rather than the base pomp object (invalidating the claim to global coverage), the profile likelihood uses only 2 starts per grid point (nprof=2), the profiled parameter phi is not excluded from rw.sd (allowing it to drift), the AIC comparison ignores Monte Carlo noise in the POMP log-likelihood, and the conclusions section contains an incomplete sentence ("phi = " with no numeric value). The POMP model ultimately fails to outperform the GARCH benchmark, but the computational setup is insufficient to judge whether this reflects a genuine model inadequacy or just inadequate optimization.

---

## Major Issues

### 1. Global Search Initialized from Prior IF2 Result (Anti-Pattern)

In the global box search (chunk "unnamed-chunk-6", line ~329), the `mif2` call passes `if1[[1]]` as its first argument rather than the base pomp object `Shanghai.filt`:

```r
if.box <- foreach(i=1:Shanghai_Nreps_global, ...) %dopar% mif2(if1[[1]],
  params=apply(Shanghai_box,1,function(x)runif(1,x)))
```

This is the canonical initialization anti-pattern documented in `pomp-global-search-init-audit`: the global search replicates inherit the internal IF2 state and cooling schedule of the local chain `if1[[1]]`, which is already near its final cooling state after 50 iterations. As a result, the effective number of unconstrained exploration steps is essentially zero — each replicate quickly freezes near wherever the random starting params were dropped, rather than exploring the box from fresh starts. The reported "global maximum" of 1264 may simply be the best lucky initialization near the local-search solution. The fix is to replace `if1[[1]]` with `Shanghai.filt` (the original `pomp` object) in the global `mif2` call.

### 2. Profile Likelihood: Profiled Parameter (phi) Not Fixed in rw.sd

In the profile chunk (unnamed-chunk-9, line ~381), the `rw.sd` passed to the profile `mif2` call contains non-zero perturbations for `sigma_nu`, `mu_h`, `sigma_eta`, `G_0`, and `H_0`, but phi is never listed. The profile_design constructs guesses with phi on a grid, but the `mif2` call does not exclude phi from `rw.sd`. Examining the code:

```r
mif2(
  if1[[1]],
  start=c(unlist(guesses[i,]),params_test),
  Np=1000, Nmif=50,
  rw.sd=rw.sd(
    sigma_nu  = Shanghai_rw.sd_rp,
    mu_h      = Shanghai_rw.sd_rp,
    sigma_eta = Shanghai_rw.sd_rp,
    G_0       = ivp(Shanghai_rw.sd_ivp),
    H_0       = ivp(Shanghai_rw.sd_ivp)
  )
)
```

Because phi does not appear in `rw.sd`, its perturbation defaults to zero - this is actually the correct behavior for excluding phi from the perturbation. However, this profile also inherits the same anti-pattern of passing `if1[[1]]` rather than `Shanghai.filt`, so the profile optimization does not start fresh. Additionally, the profile only uses `nprof=2` starts per phi grid point (from `profile_design(..., nprof=2)`), which is far too few for reliable constrained optimization. With 50 phi grid points and only 2 starts each, many constrained optima will not be found, and the resulting profile curve will be noisy and unreliable.

### 3. Profile Likelihood: Only nprof=2 Starts Per Grid Point

The profile is constructed with:
```r
guesses <- profile_design(
  phi=exp(seq(log(0.80000),log(0.99999),length.out=50)),
  lower=box[1,c("sigma_nu","mu_h","sigma_eta","G_0","H_0")],
  upper=box[2,c("sigma_nu","mu_h","sigma_eta","G_0","H_0")],
  nprof=2, type="runif"
)
```

With nprof=2, the profile foreach loop runs exactly 100 iterations (50 grid points * 2 starts). At each constrained phi value, only two optimization starts are used, each evaluated with a single `logmeanexp` over `Shanghai_Nreps_eval=10` pfilter runs. Two starts per grid point is inadequate for reliable constrained optimization, especially for a six-parameter model where the likelihood surface may be multimodal or elongated. The profile likelihood curve will be dominated by noise, and any confidence interval derived from it is unreliable.

### 4. Incomplete Sentence in Conclusion Section (Placeholder Result)

Section 4.4 contains the sentence: "The plot above suggests that the maximum log-likelihood over phi is achieved when phi = ." The numeric value of phi at the profile maximum is missing entirely. This is a clear placeholder that was never filled in before submission. This affects the main scientific conclusion of the profile analysis. The authors could read the phi value at the profile maximum from the saved `profile_phi-2.rds` artifact.

### 5. POMP Fails to Beat GARCH Benchmark Without Acknowledging Computational Limitations

The conclusions state: "we see that the POMP model have even worse log-likelihood score" (POMP = 1264 vs GARCH = 1269.58). The authors briefly note this may be due to limited computation, but they do not acknowledge that:

(a) The GARCH log-likelihood is exact while the POMP log-likelihood is a noisy particle-filter estimate subject to Monte Carlo error (the logmeanexp SE from pf1 evaluation is reported but not discussed in this context).

(b) The global search was initialized from a prior IF2 result (Issue 1), so the reported POMP maximum of 1264 may not be near the true MLE.

(c) The local search maximum (1244) is substantially below both the global search maximum (1264) and the GARCH benchmark (1269), suggesting the optimizer has not converged.

Without correcting the global search initialization and running adequate computation, the conclusion that the POMP model underperforms GARCH is not well-supported. The AIC comparison ignores Monte Carlo noise in the POMP log-likelihood (applying the `pomp-aic-mc-noise-audit` skill: the claimed POMP AIC uses max logLik = 1264, GARCH logLik = 1269.58, advantage = 5.58 in favor of GARCH; but this difference could easily be explained by Monte Carlo noise given the logLik_se values in the params CSV, which range from 0.3 to 3.4 across replicates).

### 6. Inadequate Number of Particles and Iterations for Reliable Inference

The run_level=2 settings use Np=2000, Nmif=50, Nreps_local=20, Nreps_global=50. For a financial time series with N=569 observations and a 6-parameter SV model:

- 50 IF2 iterations is near the minimum for observing any convergence. Convergence traces in the `plot(if1)` output should be examined, but the text does not report whether convergence was achieved.
- Np=2000 particles is adequate for a basic check but may introduce substantial likelihood variance for the heavy-tailed behavior suggested by the QQ-plot of GARCH residuals.
- The profile uses Np=1000 (reduced from the global search), increasing variance at the most critical stage.

Wheeler et al. (2024) document that inadequate computational effort is the leading cause of reported POMP model underperformance. Convergence diagnostics are not discussed.

### 7. No Model Diagnostics Beyond Visual Convergence Traces

The project provides no model diagnostics for the POMP model:
- No effective sample size (ESS) plots from pfilter runs, which would identify whether particle degeneracy is a problem.
- No conditional log-likelihood plots showing where the model fits poorly.
- No comparison of simulated trajectories from the fitted model against the observed returns.
- No forward simulation from the fitted parameter vector to validate that the model reproduces the volatility clustering observed in the data.

Wheeler et al. (2024, §Model diagnostics) specifically require these diagnostics as part of rigorous POMP inference.

### 8. Profile Likelihood Plot: Maximum phi Value Missing, Confidence Interval Not Reported

The profile likelihood plot (Section 4.4) shows a horizontal red cutoff line at the 95% chi-squared threshold, but the text does not report:
- The phi value at which the profile maximum is achieved (left blank as noted in Issue 4).
- The 95% confidence interval bounds for phi (lower and upper bounds where the profile crosses the cutoff).
- Whether the profile maximum matches the global search maximum within Monte Carlo error.

Without these, the profile analysis contributes no interpretable scientific content.

---

## Minor Issues

### 9. Stationarity Claim Without Formal Test

Section 2 states "The demeaned log-return looks appropriate to fit a stationary model with white noise" and "we can safely assume that the data are all independent" based on visual ACF inspection alone. No formal stationarity test (ADF, KPSS, or Phillips-Perron) is reported. While visual ACF inspection is common, asserting independence without formal testing is imprecise — the ACF only tests for linear autocorrelation, not independence (the squared returns may exhibit ARCH effects, which is exactly the motivation for the GARCH/SV analysis).

### 10. GARCH AIC Table Starts at p=1, q=1 (No p=0 or q=0 Rows)

The AIC table covers GARCH(p,q) for p=1:5 and q=1:5. It does not include p=0 or q=0 (ARCH-only or GARCH with no ARCH terms), which are natural submodels. The claim that "GARCH(1,1) has the lowest AIC" may not hold against the ARCH(q) or GARCH(p,0) subfamily. A complete comparison should include these simpler cases.

### 11. QQ-Plot Explanation is Superficial

Section 3.2 attributes the heavy tails in the GARCH(1,1) residuals to sample bias: "One possible explanation is that the sample is a little biased to the true distribution." A more accurate explanation is that weekly financial returns are inherently heavy-tailed (leptokurtic), and a Gaussian GARCH model is misspecified for this reason. The authors could consider a GARCH-t model, or note that this motivates the stochastic volatility POMP model which may better capture tail behavior.

### 12. Missing AIC Comparison for POMP

Despite stating that the GARCH log-likelihood "would be the benchmark of our analysis," the paper never computes an AIC for the POMP model explicitly. The comparison in Section 5 is by log-likelihood only (1264 vs 1269.58), without accounting for the difference in parameter counts (GARCH(1,1) has 3 free parameters: alpha0, alpha1, beta1; the POMP model has 6 parameters: sigma_nu, mu_h, phi, sigma_eta, G_0, H_0). A proper AIC comparison would adjust for this difference. Even by log-likelihood alone, the POMP model underperforms, but the AIC comparison would make this explicit.

### 13. Data Description Inconsistency

Section 2.1 states "The index data ... includes a total of 570 observations of weekly average closing price." However, the code computes `N <- dim(Shanghai)[1]` and then `wreturn = diff(log(Price))`, producing 569 returns. The POMP model is fitted to these 569 demeaned returns, not 570 observations. The text should clarify this discrepancy.

### 14. rw.sd Values Are Identical for All Regular Parameters

In the local and global searches, all four regular parameters (sigma_nu, mu_h, phi, sigma_eta) receive the same `rw.sd=0.02`. These parameters are on very different scales:
- sigma_nu after log transformation: exp(-4.5) ≈ 0.011
- sigma_eta after log transformation: exp(-0.07) ≈ 0.93
- phi after logit transformation: expit(4) ≈ 0.982
- mu_h: -0.25

A uniform rw.sd=0.02 on the transformed scale may be too small for some parameters and too large for others. The convergence traces should be inspected to verify that all parameters are moving during IF2 iterations.

### 15. No Benchmark Comparison Against ARMA Baseline

The mechanistic POMP model is compared against GARCH(1,1), which is itself a volatility model. However, a simpler ARMA baseline on the squared or absolute returns is not included. Wheeler et al. (2024) recommend that mechanistic models be compared against simple non-mechanistic statistical benchmarks to verify that the model captures meaningful structure. While GARCH serves as a partial benchmark here, an ARMA on squared returns would provide a cleaner comparison.

---

## Consulted Files

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-mc-noise-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project16/Shanghai_params.csv`
