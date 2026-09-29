# Peer Review: W24 Project 02
**Title:** Investigating the alternative prey hypothesis with the POMP framework

---

## Summary

This project applies the POMP framework to model willow ptarmigan population dynamics under the alternative prey hypothesis, using 142 years of Norwegian harvest data (log-CPUE). The authors construct a two-state (log fox, log bird) stochastic differential equation model driven by gamma white noise, compare it to an ARIMA(0,1,5) baseline, and conduct both local and global likelihood searches. While the ecological motivation is interesting and the choice to benchmark against an ARMA model is commendable, the analysis suffers from severe computational failures: the global search achieves a log-likelihood of -176.3, far below both the ARIMA baseline (-99.3) and the local search (-134), yet the authors do not revise the model. Additionally, the measurement model specified in the text (negative binomial) does not match the code (normal distribution), and particle counts as low as Np=5 are used for likelihood re-evaluation. Profile likelihoods, confidence intervals, and simulation-based diagnostics are entirely absent.

---

## Major Issues

### 1. POMP model fits drastically worse than ARIMA benchmark with no corrective action (CC-Yes, Error 1.6 / 1.15)

The global search best log-likelihood is -176.3 (confirmed in `bird_params_middle.csv`), compared to the ARIMA(0,1,5) log-likelihood of -99.3 — a gap of approximately 77 log-likelihood units, or ~154 AIC units. Even the local search yields only -134, a gap of 35 units. The course explicitly teaches (Wheeler et al. 2024; Ch. 17) that when a mechanistic model fits disastrously relative to a benchmark, the model is "probably missing something important," and the correct response is to revise the model structure — not to attribute the gap to computational constraints. The authors write: "The accuracy will be increased if we increase the parameter space," but this is incorrect: the problem is model structure, not insufficient search range. No structural revision is attempted.

**Fix:** Examine residuals from the ARIMA fit and the particle filter conditional log-likelihood trajectory to identify which time periods drive the likelihood gap. Reconsider model structure (e.g., measurement model, state equation form, overdispersion) before concluding.

---

### 2. Measurement model discrepancy between text and code

The text (Methods section) states the measurement model is $Y(t) \sim \text{Negative Binomial}(\text{mean} = \rho\beta_t, \sigma)$. However, the implemented `dmeas` and `rmeas` C snippets use a **normal distribution**:

```c
rmeas: logCPUE = rnorm(logB - logRho, sigma_obs);
dmeas: lik = dnorm(logCPUE, logB - logRho, sigma_obs, give_log);
```

Wheeler et al. (2024) document this exact type of discrepancy as a concrete reproducibility failure. Here it is more serious: the stated model is never fit. All reported likelihoods correspond to the normal measurement model, not the negative binomial described in the text. This calls the interpretation of all results into question.

**Fix:** Either change the code to implement the negative binomial measurement model described in the text (appropriate for count data), or correct the text to describe the normal model actually implemented, with justification.

---

### 3. Np=5 used for particle filter likelihood re-evaluation (CC-Yes, Error 1.4)

After the single mif2 run, the code evaluates likelihood using only 5 particles:

```r
foreach (i=1:10, ...) %dofuture% {
  mif2_out |> pfilter(Np=5)
} -> pf
logLik(pf) -> ll
print(logmeanexp(ll, se=TRUE))
```

With Np=5, the particle filter produces extremely noisy likelihood estimates that are useless for inference. The reported value of -205 (SE=3.14) from this evaluation reflects numerical noise rather than the true model log-likelihood. Course standards specify Np=1,000 at run_level=2 and Np=5,000 at run_level=3 for pfilter evaluation.

**Fix:** Re-evaluate the likelihood with at least Np=1,000 and a sufficient number of replicates (Nreps_eval=10 or more) before reporting any likelihood value.

---

### 4. mif2 internal log-likelihood used directly (CC-Yes, Error 1.4 / course standard)

In the local search code (line 429 of the Rmd), the code executes:

```r
logLik(mifs_local) -> ll
print(logmeanexp(ll, se=TRUE))
```

This uses the log-likelihood values from the final mif2 iteration directly, without a replicated pfilter re-evaluation step. The course standard explicitly states that mif2's internally reported likelihood is NOT reliable for inference, because parameter perturbations are applied in the final iteration. The subsequent `lik_local.rds` block does perform a proper pfilter re-evaluation (Np=100, replicate(10,...)), but the -134 figure in the text is ambiguous about its source, and the SE=8.2 from 10 replicates at Np=100 is large enough to be concerning.

**Fix:** Remove the direct `logLik(mifs_local)` reporting and rely exclusively on the replicated pfilter re-evaluation. Report the SE alongside all likelihood values to make Monte Carlo variability explicit.

---

### 5. Global search produces worse likelihood than local search; poorly designed parameter bounds

The global search yields a best log-likelihood of -176.3, which is substantially worse than the local search result of -134. This is the opposite of what a well-conducted global search should produce. The `runif_design` specifies extremely narrow bounds (e.g., `a` from 7 to 8, `b` from 2 to 3) that are inconsistent with the local search starting values (a=1, b=2) and seemingly hand-tuned rather than principled. Furthermore, the global search code uses `mif2(params=c(guess, fixed_params))`, where `fixed_params <- coef(mif2_out)` comes from the single (unreliable) mif2 run. This creates a poorly initialized global search that is unlikely to find a good optimum.

**Fix:** Set global search bounds to cover a broad, biologically plausible region without pre-specifying a narrow range. Initialize global searches from the best local search estimates, not from a single mif2 run. Show convergence traces for global search runs.

---

### 6. No profile likelihoods; no parameter uncertainty quantification (CC-Yes, Error 1.9)

The report presents point estimates (implicitly from local search) but provides no profile likelihoods, no confidence intervals, and no assessment of parameter identifiability. With 12 parameters in the model, identifiability is a genuine concern — the pairs plot (local_search_2.png) shows a scattered, cloud-like pattern with little structure, suggesting poor identifiability. Without profile likelihoods, it is impossible to determine whether any parameter is meaningfully constrained by the data.

**Fix:** Compute profile likelihoods for at least the key scientifically interesting parameters (e.g., gamma, which captures the alternative prey effect). Use MCAP confidence intervals. A sparse profile (5 points at run_level=2, 30 at run_level=3) is acceptable.

---

### 7. No convergence diagnostics for the global search

The local search section references a saved figure (`local_search_1.png`) showing iteration traces, but the global search section presents no trace plots or convergence diagnostics of any kind. There is no evidence that the global search mif2 runs converged, and the fact that global search results (-176.3) are worse than local search results (-134) strongly suggests convergence failure.

**Fix:** Show trace plots for log-likelihood across iterations for global search runs. Multiple searches reaching similar terminal likelihoods from different starting points is the minimum standard for claiming convergence.

---

## Minor Issues

### 8. No simulation-based model diagnostics

The report contains no forward simulations comparing model-generated trajectories to observed data, and no filtering-distribution diagnostics. The only diagnostic shown is the initial particle filter plot (Figure pf1) at the prior parameter guess. Without simulation-based diagnostics for the fitted model, there is no way to assess where or how the model succeeds or fails.

**Fix:** Simulate trajectories from the best-fit parameters and overlay them on the observed data. Examine the conditional log-likelihood trajectory from the fitted model's particle filter run.

---

### 9. Hard-coded absolute file paths undermine reproducibility

Numerous absolute paths to the author's local filesystem are embedded throughout the code (e.g., `/Users/ruojunliu/Desktop/STATS 531 - Time Series/pomp_final/...`, `/Users/ruojunliu/Desktop/bird_params_middle.csv`, `/Users/ruojunliu/Desktop/references.bib`). The project cannot be compiled on any other machine without manually replacing these paths.

**Fix:** Use relative paths throughout (e.g., `data/bird_data.xlsx`, `assets/ptarmigan.jpg`). The project already has an organized folder structure that supports this.

---

### 10. Noise variable labeling inconsistency in Equation (2)

In Equation (2) (the bird/ptarmigan equation), the stochastic term is labeled $W_t^F$ (fox noise), identical to Equation (1). In the code, however, a separate `dwB = rgammawn(sigmaB, dt)` is used for the bird equation. This is a notational error in the text: the bird equation should use $W_t^B$, consistent with the code having two separate noise processes parameterized by `sigmaF` and `sigmaB`.

**Fix:** Correct Equation (2) to use $W_t^B$ throughout.

---

### 11. Large Monte Carlo SE on local search log-likelihood (SE=8.2)

The local search reports a log-likelihood of -134 with SE=8.2. This means the 95% uncertainty interval for the log-likelihood spans approximately ±16 units. With this level of Monte Carlo noise, the comparison to the ARIMA benchmark (-99.3) is unreliable — the true log-likelihood could plausibly be better or worse. Increasing Np (currently 100 in the lik_local.rds evaluation) would reduce this SE.

**Fix:** Increase Np to at least 1,000 for final likelihood evaluation to bring the SE below 1.0.

---

### 12. ACF figure cross-reference error

The text states: "Figure \@ref(fig:trend), the partial correlation dies out after 5 lags." The PACF plot is a separate figure (`fig:pacf`), not the `fig:trend` plot. This is an incorrect cross-reference.

**Fix:** Correct the reference to `\@ref(fig:pacf)`.

---

### 13. Global search `c(guess, fixed_params)` creates ambiguous parameter initialization

In the global search code, `params=c(guess, fixed_params)` is passed to mif2, where `guess` (from `runif_design`) and `fixed_params` (from `coef(mif2_out)`) both contain all 12 parameters. The behavior when duplicate named elements are passed to pomp's `params` argument is not clearly documented, and in practice R's `c()` preserves duplicates. Whether the guesses or fixed_params take precedence is unclear, potentially defeating the purpose of the global search design.

**Fix:** Pass only the parameters that vary across guesses (the design parameters) in `guess`, and separately specify remaining fixed parameters in a way that avoids duplication.

---

### 14. Local search uses only 10 foreach iterations (run_level considerations)

The local search foreach loop runs only 20 iterations (`foreach(i=1:20,...)`), each with Np=1,000 and Nmif=50. Course run_level=2 standards call for Nreps_local=20, but Nmif=100 iterations for adequate convergence. Nmif=50 may be insufficient for parameters to converge, especially for a 12-parameter model.

**Fix:** At minimum run Nmif=100 for the local search, and consider increasing to Nmif=200 for the global search.

---

### 15. Bibliography path is absolute and non-portable

The YAML header specifies `bibliography: /Users/ruojunliu/Desktop/references.bib`, an absolute path. This file is not included in the project repository, so citations cannot be resolved on any other machine.

**Fix:** Include `references.bib` in the project folder and reference it with a relative path in the YAML header.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project02/bird_params_middle.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project02/README.md`
