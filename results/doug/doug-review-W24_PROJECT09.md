# Peer Review: W24 Project 09
## "Volatility Analysis of NASDAQ 100"

---

## Summary

This project fits three families of models — ARIMA, GARCH, and a POMP-based stochastic volatility model — to 44 years of daily NASDAQ Composite log-returns. The authors adopt Breto's leverage-effect stochastic volatility formulation as the POMP component and compare it against a simplified no-leverage variant. The project's main claim is that the POMP model outperforms GARCH and ARIMA in terms of log-likelihood, and that the leverage effect, while small, is statistically necessary. The application is interesting and the paper demonstrates familiarity with the POMP workflow. However, the analysis is undermined by several serious methodological flaws: (1) the initial particle filter benchmark is evaluated on a simulated dataset rather than the real data, making the reported initial log-likelihood incomparable to all subsequent values; (2) both the local and global IF2 searches are initialized from a previous mif2 result object rather than the base pomp object, invalidating the global search claim; (3) the likelihood comparison between GARCH and POMP models conflates incommensurable likelihood scales; (4) the profile likelihood is computed with a coding error that re-evaluates parameters from the box search rather than the profile search; and (5) the no-leverage simplified model is run at drastically lower computational effort than the full model, making the model comparison unfair.

---

## Major Issues

### 1. Initial particle filter evaluates simulated data, not real data (pomp-simdata-benchmark-error)

In the Breto model section ("Test the model and likelihood estimate"), the authors call `pfilter(sim1.filt, Np=ndx_Np)` where `sim1.filt` is a pomp object constructed from a simulated dataset (`sim1.sim`), not from the real NASDAQ returns. The reported log-likelihood of approximately -17,965 (`est = -1.796512e+04`) is therefore computed against simulated data, not the actual observations. This value is then implicitly treated as the "initial benchmark" for the real-data model and contrasted with the IF2 results (which reach ~43,483 on the real data). This discrepancy of roughly 61,000 log-likelihood units is not explained and makes no sense unless the datasets differ. The benchmark is invalid, and no valid initial real-data pfilter assessment is presented before the IF2 optimization begins.

Fix: Run `pfilter(ndx.filt, params=params_test, Np=ndx_Np)` — using the real-data pomp object `ndx.filt` — and report that log-likelihood as the pre-optimization baseline. The same bug applies to the no-leverage model section where `pfilter(sim1.filt, Np=ndx_Np)` again uses a simulated object, producing the anomalous positive log-likelihood of approximately +18,678.

### 2. Global IF2 search initialized from a previous mif2 result, not the base pomp object (pomp-global-search-init-audit)

In both the full Breto model global search and the no-leverage global search, the `mif2` call passes `if1[[1]]` — a previous IF2 result — as the first argument:

```r
if.box <- foreach(...) %dopar% mif2(if1[[1]],
    params=apply(ndx_box,1,function(x)runif(1,x)))
```

This anti-pattern causes the global search replicates to inherit the cooling schedule from the final state of `if1[[1]]`, which is near the end of its cooling trajectory. The random starting parameters drawn from the box are nominally applied, but the inherited near-zero perturbation magnitude means the search performs very few effective IF2 steps from each new start. The reported "global maximum" of 43,483 may simply be the local-search result dressed as a global result, and the pairplot cannot confirm genuine global coverage under these conditions.

Fix: Replace `mif2(if1[[1]], ...)` with `mif2(ndx.filt, ...)` in both global search loops so that each replicate starts from fresh initial conditions with a full cooling schedule.

### 3. Profile likelihood computation uses the wrong parameter source

In the profile likelihood section, the likelihood evaluation loop reads:

```r
L.prof <- foreach(i=1:100,...) %dopar% {
  logmeanexp(replicate(ndx_Nreps_eval, logLik(
    pfilter(ndx.filt, params=coef(if.box[[i]]), Np=2000))), se=TRUE)
}
```

This evaluates `coef(if.box[[i]])` — parameters from the box search object — rather than `coef(if.prof[[i]])` — parameters from the profile search. The profile likelihood plot is therefore not actually a profile likelihood over `sigma_eta`; it reflects the box-search parameters evaluated at a higher particle count. All conclusions derived from the profile likelihood (the confidence interval for `sigma_eta`, the corroboration of global-search parameter estimates) are based on a mislabeled computation.

Fix: Replace `coef(if.box[[i]])` with `coef(if.prof[[i]])` in the `L.prof` evaluation loop.

### 4. Invalid cross-model log-likelihood comparison between GARCH and POMP

The paper's central claim — that the POMP model (log-likelihood ~43,483) outperforms the GARCH model (log-likelihood ~43,266 from `tseries::garch`, or ~43,364 from `fGARCH`) — rests on a direct numerical comparison of log-likelihoods from different model families. The GARCH log-likelihood is evaluated under a Gaussian conditional distribution on the demeaned returns with the heteroscedasticity modeled through the variance equation. The POMP log-likelihood is also Gaussian (the dmeasure uses `dnorm(y, 0, exp(H/2), give_log)`), applied to the same demeaned return series. While the measurement distributions are nominally the same family, the GARCH and POMP likelihoods are not directly comparable because they differ in parameterization, the number of parameters, and the computational precision of the optimization. The paper acknowledges the parameter count difference in passing ("6 parameters compared to only 3") but does not adjust for it through AIC or BIC. The comparison should be formalized using AIC so that the additional parameters of the POMP model are penalized.

Fix: Compute AIC = -2 * loglik + 2 * k for all models and compare on that basis. Report the exact parameter counts for each model.

### 5. No-leverage model comparison is computationally unfair

The full Breto model is run at `run_level=3` with `Np=2000`, `Nmif=500`, `Nreps_global=100`, while the no-leverage model is run at `run_level=2` with `Np=100`, `Nmif=50`, `Nreps_global=20`. The conclusion that the leverage model (max loglik ~43,483) outperforms the no-leverage model (max loglik ~43,280) is based on this unequal computational budget. The difference of approximately 200 log-likelihood units may not survive equal computational treatment. The conclusion that "the leverage effect is required" cannot be supported without running both models at comparable effort.

Fix: Rerun the no-leverage model at `run_level=3` (same `Np`, `Nmif`, and `Nreps_global` as the Breto model). Only after the no-leverage model has been given a fair opportunity to find its optimum can a valid likelihood ratio test be performed.

### 6. Convergence not adequately demonstrated; insufficient computational effort for a 44-year daily series

The dataset contains 13,416 daily observations. For a series of this length, the computational settings at `run_level=3` (`Np=2000`, `Nmif=500`, `Nreps_global=100`) are at the lower boundary of what is adequate for a stochastic volatility model. The convergence traces in the diagnosis plots show that `loglik` increases then gradually decreases, which the authors interpret as overfitting or a local maximum. No evidence is presented that multiple independent global-search replicates converged to the same log-likelihood from distinct starting points; the 100 global replicates are expected to cluster near the local-search solution given the global search initialization error (Issue 2). The paper does not report whether increasing `Np` or `Nmif` further would materially change the maximum log-likelihood, and no likelihood traces showing asymptotic behavior are shown.

Fix: Present log-likelihood traces across IF2 iterations to demonstrate convergence. Report the spread of log-likelihoods across global-search replicates (maximum, median, standard deviation) to assess whether the search found a unique optimum or scattered across local maxima.

### 7. ARIMA AIC table selects the wrong model; AIC value anomaly

The AIC grid search nominally selects ARMA(5,5) as the best model based on the lowest AIC value (-79185.97). However, inspection of the AIC table shows that all other ARMA(p,q) values are in the range -79148 to -79161, while ARMA(5,5) reports -79185.97 — an improvement of about 24 units over the next-best model. This is unusually large and likely indicates numerical instability or a convergence artifact from the `arima()` optimizer for this high-order parameterization, not a genuine model improvement. The authors do not flag this anomaly. In the subsequent GARCH model selection, the authors note that AR(5)/MA(5) coefficients are insignificant, lending further support to the interpretation that ARMA(5,5) is not a well-identified model.

Fix: Examine the ARMA(5,5) parameter estimates for near-canceling roots or near-unit-circle values. Check whether the optimizer converged (verify `arima_ndx$code`). Consider capping the search at lower orders or using `auto.arima()` with a stationarity check to select a more parsimonious model.

---

## Minor Issues

- **Periodogram frequency units**: The peak frequency reported from the smoothed periodogram is 179.4 cycles per time unit, which is physically implausible given a daily series with 365 frequency. The `ts()` call uses `frequency=365`, but the periodogram reports the frequency on the [0, 0.5] scale in cycles per observation. The authors do not convert to interpretable units (cycles per year), making the periodogram result opaque.

- **Misstatement of the text vs. the output table**: The introduction states "the ARIMA model cannot fully capture the time-series behaviors of volatility" and "GARCH suggested a better result based on the likelihood estimate." The text at the GARCH section initially states the log-likelihood is "about 43341" then says it is 43361.47, but the actual output from the HTML shows 43360.37 for ARMA(5,5)+GARCH(1,1) and 43363.89 for ARMA(4,4)+GARCH(1,1). Minor numeric discrepancies accumulate throughout the paper, suggesting the narrative was written at a different computation time than the rendered output.

- **Inconsistent notation in model equations**: The process equation for the Breto model writes $\beta_n = Y_n \sigma_n \sqrt{1-\phi^2}$ where `sigma_n` is undefined in the notation block. The code uses `sigma_eta` for this role but no explicit equation reconciles the two. The mathematical description should be made self-consistent.

- **`sigma_nu` converging to zero is not interpreted as a model misspecification signal**: The profile search and global search consistently show `sigma_nu` near 0.001 (effectively zero on the natural scale). The authors interpret this as confirming that the no-leverage model may suffice, but they do not flag it as a potential sign that the leverage state G is unidentifiable — if sigma_nu = 0, the G process is degenerate and the leverage term contributes nothing. This warrants explicit discussion.

- **Missing confidence interval for leverage vs. no-leverage comparison**: The authors compare the maximum log-likelihoods of the two POMP models (43,483 vs. 43,280) without performing a likelihood ratio test or computing a confidence interval for the improvement. Given the large parameter count difference (6 vs. 4), the improvement of 203 log-likelihood units is highly significant under standard chi-squared asymptotics (chi-squared(2) = 406), but this should be stated explicitly with the appropriate test.

- **`timing.box` assignment error**: The line `timing.box <- .system.time["elapsed"]` references `.system.time`, which is an internal `stew()` artifact that may not be in scope outside the `stew()` block. This suggests the reported timing values are unreliable. The paper does not report actual elapsed wall-clock time for any of the computations.

- **No model diagnostics for the POMP model**: After fitting the POMP model, no filtering diagnostics are presented: no effective sample size (ESS) trace, no conditional log-likelihood plot over time, and no comparison of simulated returns to observed returns from the filtering distribution. The visual comparison in the no-leverage section shows one forward simulation from arbitrary initial conditions, not a filtering-distribution-conditioned simulation.

- **Data mislabeling**: The title and text refer to "NASDAQ 100" but the data loaded is `^IXIC_quote.csv`, which is the NASDAQ Composite index (ticker ^IXIC), not the NASDAQ 100 (ticker ^NDX). These are different indices.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project09/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project09/blinded.md`
