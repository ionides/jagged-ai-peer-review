# Peer Review: W22 Project 14
## "Analysis of Stochastic Volatility Models for Ethereum Returns"

---

## Summary

This project analyzes hourly Ethereum cryptocurrency return data using three candidate models: an AR(2)-GARCH(1,1) benchmark, a leveraged stochastic volatility model adapted from Breto (2014) implemented in POMP, and a discretized Heston stochastic volatility model also implemented in POMP. The paper's main conclusion is that the Heston model achieves the best fit by log-likelihood (roughly 34,975 vs. 28,977 for Breto vs. 28,587 for AR-GARCH). While the paper demonstrates familiarity with POMP infrastructure and addresses a genuinely interesting application domain, the analysis contains several critical methodological and code errors that undermine every quantitative conclusion. Most seriously: (1) the Breto global search is initialized from a previous mif2 result object rather than the base pomp object, invalidating the global search claim; (2) the initial particle filter for the Breto model is evaluated on simulated data, not real data, and the resulting log-likelihood is described as anomalously "very low" without recognizing that it cannot be compared to the real-data IF2 results; (3) the Heston rprocess is algebraically incorrect as implemented; and (4) neither model's convergence is convincingly demonstrated. No profile likelihoods, confidence intervals, or model diagnostics are presented.

---

## Major Issues

### 1. Breto Global Search Initialized from a Previous mif2 Result Object (Code Error)

In the Breto global search (Section 3.3), the `mif2()` call passes `data = if1[[1]]` (a previous IF2 chain object) as its first argument rather than `eth.filt` (the base pomp object):

```r
mif2(data = if1[[1]], params=apply(eth_box,1,function(x)runif(1,x)))
```

This is the classic anti-pattern identified in the `pomp-global-search-init-audit` skill. When a previous IF2 chain is passed as the first argument, the global search inherits the cooling schedule from `if1[[1]]`, which has already decayed to near zero after 200 IF2 iterations. The new random starting parameters are drawn from the box (`apply(eth_box, 1, runif)`), but the optimizer immediately stops perturbing them because the perturbations have been cooled away. The claimed "global" coverage of the box is therefore fictitious: every replicate evaluates the likelihood near its random starting point without any gradient-following optimization. The 24-log-unit improvement over the local search reported in the conclusion cannot be attributed to a genuine global search.

**Fix:** Replace `data = if1[[1]]` with `eth.filt` (the base pomp object) in the global mif2 call.

### 2. Breto Initial Particle Filter Evaluated on Simulated Data, Not Real Data

In Section 3.2, the initial particle filter is computed on `sim1.filt` — a pomp object built from simulated data — rather than on `eth.filt` (the real Ethereum data):

```r
pf1 <- foreach(i=1:eth_Nreps_eval, .packages='pomp') %dopar%
  pfilter(sim1.filt, Np=eth_Np)
```

The authors note that "the log-likelihood we got from the simulated data is very low," but then treat this as if it is a benchmark for the real-data model. The simulated and real datasets have entirely different probability densities; the resulting log-likelihood cannot be compared to the IF2 search results on real data. This is the `pomp-simdata-benchmark-error` pattern. The text's observation that the simulated-data likelihood is "very low" is not surprising — it reflects the fact that the simulated data is unlikely under different parameter values — but nothing about it is relevant to the real-data analysis.

**Fix:** Re-run the initial particle filter on `eth.filt` at `params_test` and report that value as the starting benchmark for the real-data Breto model.

### 3. Heston rprocess Is Algebraically Misspecified

The Heston model equation stated in the text is:

$$V_n = (1-\phi)\theta + \phi V_{n-1} + \sqrt{V_{n-1}}\,\omega_n$$

However, the corresponding Csnippet implements:

```c
V = theta*(1 - phi) + phi*sqrt(V) + sqrt(V)*omega;
```

The code applies `sqrt(V)` (i.e., $\sqrt{V_{n-1}}$) to the autoregressive term as well: the mean-reversion term is `phi*sqrt(V)` rather than `phi*V`. This departs from the stated model, which should have `phi*V` in the autoregressive part. The discretized Heston variance process has a well-defined mean structure, and applying `sqrt()` to the level term introduces a square-root nonlinearity in the mean that is not motivated by the continuous-time Heston model or stated in the text. All parameter estimates, likelihood values, and comparisons for the Heston model are therefore based on a model that is not what the authors describe.

**Fix:** Correct the Csnippet to `V = theta*(1 - phi) + phi*V + sqrt(V)*omega;` to match the stated equation.

### 4. Non-Convergence of Both POMP Models Is Explicitly Acknowledged but Results Are Still Interpreted

For the Breto local search, the authors write: "The trace plot for the MIF iteration shows the log-likelihood is not always climbing along with each iteration... The spread in likelihood suggests that maybe the numerics are not working smoothly." For the Heston local search, the authors observe "problems with effective sample size" and "too many particles getting killed off regularly." Despite these explicit convergence failure acknowledgments, the paper continues to report and interpret specific log-likelihood values (e.g., "28953" for Breto local, "34975.32" for Heston) as if they represent meaningful MLEs, and uses them in the final model comparison table.

Per the `pomp-self-diagnosed-nonconvergence-audit` skill, all conclusions that depend on these values — including the claim that the Heston model is "likely the best model" — are invalidated by the authors' own convergence assessment.

**Fix:** Either increase computational resources until genuine convergence is demonstrated (more particles, more iterations, more replicates from diverse random starts), or restrict all claims to model specification and qualitative structure, removing quantitative comparisons.

### 5. No Profile Likelihoods or Confidence Intervals

Neither the Breto nor the Heston model is subjected to profile likelihood analysis. Key parameters such as $\phi$, $\mu_h$, and $\theta$ are estimated without any uncertainty quantification. The pairs plots show that the likelihood surface is poorly identified for several parameters (e.g., $\mu_h$ in the Breto model shows no clear relationship with log-likelihood), yet no profile likelihoods are computed to determine which parameters are identifiable. Without confidence intervals, it is impossible to assess whether any of the estimated parameter values are distinguishable from zero or from the boundaries of the search box. This violates POMP best practice item 5 (Wheeler et al. 2024, parameter identifiability).

**Fix:** Compute profile likelihoods for at least the key parameters of each model, report MCAP confidence intervals, and flag parameters that appear to be unidentifiable.

### 6. AIC Comparison Does Not Account for Monte Carlo Noise in POMP Log-Likelihoods

The final comparison (Section 5) reports AIC-equivalent log-likelihood values for all three models and concludes that the Heston model is best. The GARCH and ARMA log-likelihoods are exact (analytically computed), while the POMP log-likelihoods are Monte Carlo estimates subject to both within-chain noise and selection bias from taking the maximum across multiple replicates. With `Nreps_eval = 20` particle filter evaluations per chain and `Np = 1000` particles, the per-chain log-likelihood SE for a financial return series of ~9000 observations is likely on the order of 2–5 units; taking the max across 20–50 chains introduces an additional upward bias of several units. The claimed 6022-unit advantage of Heston over Breto is large enough that MC noise is not the decisive concern for that comparison, but the 24-unit advantage of the Breto global search over local, and any comparisons against GARCH/ARMA, should be accompanied by SE estimates. Per the `pomp-aic-mc-noise-audit` skill, the paper should report the SE of the best-chain log-likelihood estimate alongside each value.

**Fix:** Report `logmeanexp(replicate(50, logLik(pfilter(...))), se=TRUE)` for the best-parameter vector from each model, and compare AIC differences to twice the SE before drawing model selection conclusions.

### 7. bake() Cache Double-Evaluation Pattern Causes Repeated Computation

Both the Breto and Heston sections use `bake()` in a pattern where the same cache file is called twice in the same document section — once to retrieve `if1` and once to retrieve `L.if1`:

```r
if1 <- bake(file=sprintf("Breto_mif1-%d.rds",run_level), { ... })[[1]]
L.if1 <- bake(file=sprintf("Breto_mif1-%d.rds",run_level), { ... })[[2]]
```

The second `bake()` call uses the same filename as the first. Because the file already exists after the first call, `bake()` loads from the cache and the enclosed computation is never re-executed. The second element (`[[2]]`) is retrieved from the cached list, which is correct only if the list was stored properly in the first call. This code structure is fragile and non-idiomatic: the correct pattern is to cache the entire result list once, then extract both elements from the single cached object. If the file was ever deleted and the code re-ran, only `[[1]]` would be written and the second retrieval would be inconsistent. Per the `pomp-stew-filename-collision` skill, this requires verification that the cache was written in the expected format.

**Fix:** Cache the computation once: `result <- bake(file=..., { list(if1, L.if1) })` then extract `if1 <- result[[1]]; L.if1 <- result[[2]]`.

### 8. Missing Model Diagnostics: No Conditional Log-Likelihoods, Effective Sample Size Tracking, or Simulation Envelopes

The paper includes no quantitative model diagnostics beyond convergence traces and pairs plots. There are no plots of conditional log-likelihoods over time (which would identify periods where the model fails to explain the data), no explicit effective sample size plots (the text mentions ESS drops in qualitative terms but does not plot them), and no simulation envelopes comparing simulated trajectories to observed returns. The single outlier event (Russian hacker incident, May 19, 2021) is identified visually but is not formally assessed for its influence on model fit or parameter estimates. This violates POMP best practice item 4 (Wheeler et al. 2024, model diagnostics).

**Fix:** Add plots of conditional log-likelihoods per observation time for both models, add an ESS time series plot, and overlay simulation envelopes on the observed returns series. The anomalous observation should be formally assessed (e.g., by refitting with and without that time point).

---

## Minor Issues

### 9. Heston rprocess Uses Undefined Variable `eth.sd_ivp` in Breto Model Setup

In the Breto local search code (Section 3.2), the `rw.sd` definition outside the `bake()` block references `eth.sd_ivp`:

```r
G_0 = ivp(eth.sd_ivp),
H_0 = ivp(eth.sd_ivp)
```

but the variable is defined as `eth_rw.sd_ivp` (with an underscore before `ivp`) earlier in the chunk. The `rw.sd` object defined before the `bake()` call (lines 282-289) is never actually used — the actual mif2 calls inside `bake()` define their own `rw.sd` inline using the correctly spelled `eth_rw.sd_ivp`. The outer definition is dead code with a typo. While this does not affect the cached computation (which uses the correct inline definition), it indicates that the code was not tested end-to-end without cached results.

### 10. Heston Global Search Box for phi Spans (0,1) but phi Is logit-Transformed

The Heston global search box sets `phi = c(0, 1)` — the full range of logit-transformed parameters. However, `phi` is declared with `logit` in `partrans`, meaning IF2 works on the logit-transformed scale. A box of `(0, 1)` on the natural scale corresponds to `(-Inf, Inf)` on the logit scale, which effectively places no constraint on `phi` during the search. While this is not incorrect in principle (it allows phi to range freely), it is inconsistent with the text's implication that the box constrains the search. It would be more informative to report a narrower box on the logit scale and discuss what values of phi are substantively reasonable.

### 11. Breto Global Search Box for sigma_eta Is Implausibly Wide

The Breto global search box sets `sigma_eta = c(0.5, 600)`. This is an enormous range spanning three orders of magnitude. For the hourly ETH return series, values of `sigma_eta` near 600 would produce catastrophically large volatility draws that would collapse the particle filter. The resulting parameter estimates near the boundary of this box are almost certainly nonsensical, but the authors do not discuss whether the MLE for `sigma_eta` is interior to this box or at a boundary, nor do they check whether the estimated value is consistent with the implied volatility structure of the data.

### 12. The Heston Local Search rw.sd Is Defined But Then a Different Value Is Effectively Used

In the Heston local search (Section 4.2), `rw_sd` is defined using `rwi=0.2` and `rwr=0.02`, but immediately after, variables `crypto_rw.sd_rp = 0.001` and `crypto_rw.sd_ivp = 0.001` are assigned and never used — the actual `mif2()` call uses `rw_sd` (the earlier object). This creates code confusion and raises the question of whether the intended rw.sd values were actually applied.

### 13. Log-Likelihood Numbers Are Presented Without Units or SE

Throughout the conclusion (Section 5), log-likelihood values are stated as bare integers ("28953," "34975.32," "28977") without accompanying standard errors. For POMP models with particle filter estimation, the Monte Carlo SE is integral to interpreting these numbers. A difference of 24 log units between local and global Breto searches may or may not be statistically meaningful depending on the SE.

### 14. Stationarity Assessment Is Informal and Potentially Incorrect

In Section 1, the authors assert "stationarity seems to be holding" based solely on visual inspection of the return series. No formal unit root or stationarity test (ADF, KPSS, PP) is reported. The comment in the code — "seems like we have evidence of stationarity?" — indicates this was not rigorously examined. For a financial returns series at hourly frequency, stationarity is plausible but should be confirmed by at least one formal test to justify subsequent ARMA/GARCH fitting and the use of POMP models without differencing.

### 15. Missing References and Reproducibility Information

No code repository is provided; no final MLE parameter vectors are tabulated in the text. The analysis depends on cached `.rds` and `.rda` files that are not included in the project folder. The ETH.csv data file is present, but without the cache files, the analysis cannot be reproduced. The references section (Section 6) appears empty in the submitted document.

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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-design-variable-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-mc-noise-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-boundary-mle/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project14/Blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project14/ETH.csv`
