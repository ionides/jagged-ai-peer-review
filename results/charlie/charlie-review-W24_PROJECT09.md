# Peer Review: W24 Project 09
## Volatility Analysis of NASDAQ 100

---

## Summary

This project applies three time-series modeling frameworks — ARIMA, GARCH, and a POMP-based stochastic volatility model (Breto's leverage model) — to the full historical NASDAQ Composite (IXIC) daily return series from 1971 to approximately 2024. The authors conclude that neither ARIMA nor GARCH fully captures the heteroscedastic residual structure, and that the POMP model achieves a higher log-likelihood than the GARCH benchmarks. A secondary analysis removes the leverage term to test whether it is necessary, finding that the full model outperforms the simplified one.

The project has genuine strengths: it engages seriously with model comparison via likelihood, uses the iterated filtering (IF2) machinery correctly in general, attempts a profile likelihood analysis, and provides a scientifically interesting nested model comparison. However, several critical flaws undermine the main conclusions. A bug in the profile likelihood evaluation code means the profile curve is computed from the wrong parameter vectors, invalidating the confidence interval claim entirely. The global search for the full Breto model uses far too few particles and replicates to be trusted on a dataset of 13,000+ observations. Likelihood comparisons between GARCH and POMP are made on non-equivalent bases. Model diagnostics beyond trace plots are absent, and reproducibility is limited by lack of archived parameter files and missing `sessionInfo()`.

---

## Major Issues

### 1. Profile Likelihood Code Bug Renders the Confidence Interval Invalid

In the profile likelihood evaluation loop (lines 501-504), the likelihood of each profile-optimized parameter vector is evaluated using `coef(if.box[[i]])` rather than `coef(if.prof[[i]])`. The variable `if.box` refers to the global search objects from the preceding section, not the profile objects `if.prof` that were just computed. As a result, `r.prof` contains log-likelihoods associated with global-search parameters, not profile-constrained ones. The profile curve and the stated confidence interval (`sigma_eta` between 0.54 and 1) are therefore based on incorrect parameter evaluations and cannot be trusted.

To fix this, line 503 must be changed to use `coef(if.prof[[i]])`.

This is the most serious error in the paper because the profile likelihood is presented as a key validation of the parameter estimates and the claim about the leverage effect.

### 2. GARCH and POMP Likelihoods Are Not Comparable

The paper's central comparative claim — that "POMP outperformed the previous two methods in terms of likelihood estimates" — rests on comparing log-likelihoods across GARCH (from `tseries::garch` and `fGarch::garchFit`) and the POMP model. These quantities are not comparable without adjustment because:

(a) The GARCH models are fit to ARMA residuals or to the demeaned series under a Gaussian conditional distribution, while the POMP model is a full-data likelihood evaluated on the demeaned series with a different parameterization.

(b) The `tseries::garch` log-likelihood (labeled `L.garch`) is computed on a filtered subset of observations due to initialisation, and the `fGarch` likelihood includes the mean equation, making the observation counts differ.

(c) The POMP likelihood is evaluated at `run_level=3` with only `Np=2000` particles on 13,416 observations, producing a log-likelihood with a standard error described as "quite high" — the authors themselves note this.

Without demonstrating that all models are evaluated on exactly the same observations with the same observation model, the comparison is informal at best and misleading at worst. The authors should either align the observation models explicitly, or limit claims to directional comparisons while acknowledging the caveat.

### 3. Insufficient Computational Effort for the Full POMP Model on a 13,000-Observation Dataset

The full Breto model is fit to 13,416 daily observations. At `run_level=3`, the authors use `Np=2000` particles, `Nmif=500` IF2 iterations, `ndx_Nreps_local=20` local search replicates, and `ndx_Nreps_global=100` global search replicates. For a dataset of this size, 2,000 particles is likely insufficient to produce stable likelihood estimates; the particle filter degenerates rapidly on long series. The authors themselves report "the standard error is quite high" for the best log-likelihood value from the global search. No sensitivity analysis varying `Np` is presented, and no effective sample size (ESS) diagnostics are shown to verify that the particle filter is functioning adequately. Conclusions about parameter estimates and model comparison drawn from a potentially degenerate particle filter are unreliable (Wheeler et al. 2024, Computational adequacy, §6).

### 4. Profile Likelihood Uses `if1[[1]]` as Starting Point and Incorrect Run-Level Settings

Independent of the indexing bug described in Issue 1, the profile optimization loop (`if.prof`) initializes all 100 profile replicates from `if1[[1]]` — the first replicate of the local search — rather than from `guesses[i,]`. The `params` argument is `c(unlist(guesses[i,]), params_test)`, but this is then overridden by `mif2`'s internal initialization from the object passed as its first argument (`if1[[1]]`). The profile design's starting-value diversity is thus not utilized.

Additionally, the profile section hardcodes `Np=2000` and `Nmif=200`, but `ndx_Nreps_eval` is still read from `run_level=3` (set globally earlier), which gives `ndx_Nreps_eval=20`. While the particle count is appropriate here, the replication strategy and starting point issue still undermine the profile.

### 5. No Benchmark Comparison Against a Standard GARCH Baseline on Equivalent Grounds

Wheeler et al. (2024, §Benchmark comparison) emphasize that mechanistic models should be compared against non-mechanistic statistical benchmarks using a quantitative, directly comparable measure. The GARCH model here could serve as such a benchmark, but as noted in Issue 2, the likelihoods are not aligned. More importantly, the paper does not establish whether the GARCH model's Gaussian innovations assumption is the relevant baseline or whether a GARCH model with t-distributed innovations (a standard extension that often fits financial returns much better) was considered. Without a rigorous baseline, the claimed superiority of POMP is not established.

### 6. Simplified Model Comparison Is Methodologically Flawed

The paper constructs a simplified stochastic volatility model without the leverage term and runs it at `run_level=2` with `Np=100` particles and `Nmif=50` iterations, then compares its log-likelihood to the full model run at `run_level=3` with `Np=2000` and `Nmif=500`. This comparison confounds model structure with computational effort. A lower log-likelihood for the simplified model at lower computational intensity could reflect inadequate optimization rather than a genuine likelihood difference. The conclusion that "the model with leverage performed better" is therefore not supported. Both models should be optimized at the same computational settings before comparing log-likelihoods.

### 7. No Model Diagnostics Beyond Trace Plots and Pair Plots

The paper presents IF2 convergence traces and pair plots, but provides no further diagnostics. Missing are:

- Effective sample size (ESS) plots during particle filtering, which would indicate whether the filter is degenerating
- Conditional log-likelihood plots per time step, which would identify specific periods of poor fit
- Simulation-based model checks: forward simulations from the fitted model are not compared systematically to observed data in the full model analysis (only a brief simulation from initial test parameters is shown for the simplified model)
- Filtering-distribution diagnostics

These diagnostics are recommended by Wheeler et al. (2024, §Model diagnostics, §4) and their absence means it is impossible to assess where the POMP model succeeds or fails on the data.

---

## Minor Issues

### 8. Initial Conditions Are Fixed and Not Estimated

The initial conditions `G_0` and `H_0` are included in the parameter search but initialized identically across all global search replicates (drawn from a fixed box). The sensitivity of final results to the choice of initial condition box (`G_0 in [-2,2]`, `H_0 in [-1,1]`) is not assessed. For time series with 13,416 observations, the effect of initialization may be negligible, but this should be stated explicitly rather than assumed.

### 9. Inconsistent run_level for the Simplified Model

The simplified (no-leverage) model analysis silently resets `run_level <- 2` inside a code chunk (line 648), overriding the global `run_level=3` set earlier. This is not explained in the text and creates confusion about which computational settings apply where. It also means that the local search uses `Nmif=50` and `Np=100` for the simplified model — far less than the full model — as noted in Issue 6.

### 10. Log-Likelihood Threshold in Profile Filter Is Hardcoded

The code at line 534 filters the profile results with `r.prof$logLik > 43483` rather than using a relative threshold (e.g., `max(r.prof$logLik) - 10`). This hardcoded value may not correspond to the actual maximum found when code is re-run, producing an empty or arbitrary subset. The standard cutoff of `maxloglik - 0.5*qchisq(df=1,p=0.95)` is already computed correctly as `ci.cutoff` a few lines earlier (line 520) and should be used consistently.

### 11. ARIMA Analysis Selects ARMA(5,5) Incorrectly

The AIC table scan selects ARMA(5,5) as the best model, but the authors then note that AR(4) and MA(4) coefficients were the only significant ones in the GARCH context. The paper switches to ARMA(4,4) without providing a proper model selection rationale — for instance, comparing ARMA(5,5) and ARMA(4,4) on AIC, or using a likelihood ratio test. The selection process is ad hoc.

### 12. Missing sessionInfo() and Package Version Information

The Rmd file loads numerous packages (`pomp`, `fGarch`, `tseries`, `doFuture`, `doRNG`, `plotly`, etc.) but no `sessionInfo()` output is provided in the supplement. Given that `pomp`'s API has changed substantially across versions, the analysis may not reproduce on current CRAN releases (code-supplement checklist, POMP-specific item). The `pomp` version and R version should be pinned, ideally via `renv`.

### 13. Archived `.rda` Files Are Not Provided

The analysis uses `stew()` to cache results in `.rda` files (`pf1_3.rda`, `mif1_3.rda`, `box_eval_3.rda`, `profile_sigma_eta_3.rda`, etc.). These intermediate results are not included in the project folder alongside the Rmd, meaning a reader cannot evaluate the results without re-running the full optimization. Wheeler et al. (2024) recommend archiving final MLE parameter vectors separately so readers can verify results without re-running expensive computations. The project folder contains only the `.csv` and `.Rmd` source file.

### 14. Stochastic Volatility Model Not Described with Adequate Mathematical Precision

The model section states that $\sigma_{w,n}^2 = \sigma_\eta^2(1-\phi^2)(1-\tanh^2(G))$, but the text simply writes "$\omega_n$ is an iid $N(0, \sigma^2_{w,n})$" without spelling out the full heteroscedastic variance formula. A reader unfamiliar with Breto (2014) cannot derive the variance expression from the equations given. The expression for $\beta_n$ is given only in text but the equation for $H_n$ in the code uses `sigma_eta * sqrt(1-phi*phi) * sqrt(1-tanh(G)*tanh(G))`, making it important that the mathematical description match the code exactly.

### 15. Minor Writing and Notation Issues

- The abstract/introduction claims the POMP model "outperformed" ARIMA and GARCH without qualifications, but this claim requires the caveats identified in Issues 2 and 6.
- "Althoguh" (line 99), "samplwas" (line 407), "recoganized" (line 138), "converge well" vs "converged well" are typographic errors.
- The phrase "the profile likelihood validated that the parameters found in the global search" in the conclusion is logically circular given the indexing bug (Issue 1) and does not constitute a valid validation.
- The reference to Strogatz (1994) in the conclusion as a conceptual analogy for economic regime changes is tangential and adds no scientific content.
- Citation [8] (Lecture slides Chapter 14) and citation [9] (Strogatz) are both numbered [8] in the reference list.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project09/blinded.Rmd`
