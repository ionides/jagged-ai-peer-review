# Peer Review: W21 Project 07
**"Information Epidemics: Modeling Search Trends during the GameStop Short Squeeze Using Stochastic Compartmental Models"**

---

## Summary

This project applies a stochastic SIRS compartmental model (via the `pomp` R package) to model Google Trends search frequency for "gme" during the 2021 GameStop short squeeze, drawing an analogy between information spread and disease transmission. The core idea is interesting and the SIRS formulation is scientifically motivated. However, the analysis contains several critical implementation errors that invalidate the reported results: the profile likelihood computation iterates over the wrong design (the global search grid rather than the dedicated profile grid), the final analysis runs at debug-level computation (run_level=1, Np=100, Nmif=10), the measurement model is formally misspecified (using the accumulator H as the size parameter), and key parameters are not perturbed during iterated filtering. No convergence diagnostics are shown and no benchmark comparison is provided. The conclusions drawn from profile likelihoods and parameter estimates are therefore unreliable.

---

## Major Issues

### 1. Profile likelihood iterates over wrong design — results2 never uses guesses2 (CC-Yes, Error 1.2)

The profile design is created as `guesses2` using `profile_design(eta=seq(0.01,0.1,length=40), ...)` (lines 305–312), but the `stew` block computing `results2` iterates over `iter(guesses,"row")` — the global search grid — rather than `iter(guesses2,"row")` (lines 315–327). As a result, `results2` is simply a repeat of part of the global search and contains no actual profile likelihood structure. The profile likelihood plots in Section 5.2 are therefore scatterplots of global search results, not true profile likelihoods. Per the course standard (Error 1.2), a profile likelihood requires optimizing over all nuisance parameters at each fixed value of the target parameter; a scatter of global search points does not satisfy this requirement. The confidence intervals reported (e.g., $\beta \in [0.55, 8.21]$) are unsupported by a valid profile.

**Fix:** Replace `iter(guesses,"row")` with `iter(guesses2,"row")` in the `results2` stew block, and verify that `eta` is held fixed and not included in `rw.sd` during the profile mif2 runs.

---

### 2. Final analysis runs at debug-level computation (run_level=1)

The code sets `run_level <- 1` (line 213), giving Np=100, Nmif=10, Nseq=100, and Nreps_global=10. These are the minimum debugging values. With Np=100 particles, the particle filter produces extremely noisy log-likelihood estimates; with Nmif=10 iterations, iterated filtering has almost certainly not converged. The reported best parameter set and all downstream profile plots are therefore based on unreliable likelihood evaluations. The course standard for final results is run_level=3 (Np=5000, Nmif=200), or at minimum run_level=2 (Np=1000, Nmif=100).

**Fix:** Rerun at run_level=2 or 3 and cache the results. The `stew` mechanism is already in place; the run_level switch is the only change needed.

---

### 3. Measurement model is formally misspecified — H used as the size parameter of dnbinom

The dmeasure Csnippet is:
```c
lik = dnbinom(count, H, rho, give_log);
```
In R's `dnbinom`, the signature is `dnbinom(x, size, prob, log)`. Here `H` — the accumulated infection count — is used as the `size` (dispersion) parameter, and `rho` as the success probability. The text describes the measurement model as $Q \sim \mathrm{NegBin}(H, \rho)$ intending H to be the mean (or rate) parameter, not the dispersion. This is not the standard POMP formulation, where the negative binomial is typically parameterized as `rnbinom(n=1, size=psi, mu=rho*H)` with an overdispersion parameter `psi`. Using H as the size produces a distribution whose shape and variance change erratically with the latent state, and the model is inconsistent with the stated mathematical description. This is a concrete model-code mismatch of the type documented as a reproducibility failure in Wheeler et al. (2024).

**Fix:** Reparameterize: introduce an overdispersion parameter `psi` and use `dnbinom(count, size=psi, mu=rho*H, log=1)` and correspondingly `rnbinom(n=1, size=psi, mu=rho*H)` in rmeasure.

---

### 4. Key parameters rho and N are not perturbed in mif2 global search

The global search rw.sd specification is:
```r
rw.sd=rw.sd(Beta=0.02, mu_IR=0.02, mu_RS=0.02, eta=ivp(0.02))
```
Parameters `rho` and `N` are omitted. Since mif2 only updates parameters included in `rw.sd`, `rho` and `N` remain fixed at their starting values from the random design throughout every mif2 run. The text states these parameters are free (not fixed), and they appear in the parameter transformation, but they are never actually optimized. The reported best parameter values for `rho` and `N` are just the starting values from the random design grid.

**Fix:** Add `rho=0.02` and `N=0.02` (or appropriate values on the transformed scale) to the `rw.sd` call in the global search.

---

### 5. No iterated filtering convergence diagnostics shown (CC-Yes, Error 1.8)

No trace plots of log-likelihood or parameters across mif2 iterations are presented anywhere in the report. Without these diagnostics, there is no evidence that the optimizer converged — particularly problematic given the debug-level computation settings and the unconverged parameter surfaces described in the text itself. The course explicitly requires convergence traces to support claims about parameter estimates. The authors acknowledge non-convergence for `mu_RS` and `eta` but attribute it to model misspecification without showing the optimizer traces that would confirm this interpretation.

**Fix:** After the global search, plot `mif2` traces for a representative set of runs (log-likelihood and key parameters vs. iteration number) to assess convergence.

---

### 6. No benchmark comparison (CC-Yes, Error 1.6)

The project presents no comparison of the SIRS model's log-likelihood to any non-mechanistic benchmark (e.g., ARMA, IID negative binomial, or regression on a trend). Without such a comparison it is impossible to assess whether the mechanistic model captures meaningful structure beyond what a simple time series model would achieve. The benchmark log-likelihood reported in Section 4 is for a single manually chosen parameter set, not for a fit to data, and does not constitute a model comparison. This is particularly important given that the profile likelihoods are flat and parameters are poorly identified — a benchmark would help determine whether this reflects fundamental model inadequacy.

**Fix:** Fit at minimum an ARMA model and an IID negative binomial to the same data and report their log-likelihoods alongside the POMP model log-likelihood.

---

### 7. Arbitrary hard filter on loglik removes valid results without justification

In two places, results are filtered by `results[results$loglik < -293,]` (lines 258 and 269). This removes all results with log-likelihood above -293 (i.e., the better-fitting runs), which is the opposite of the intended analysis. The comment suggests this threshold was chosen to remove runs that appeared as "infinite" or pathological, but no explanation is given, and the effect is to discard the best-fitting parameter sets found. The profile likelihood plots in Section 5.2 are therefore conditioned on a truncated subset of results that excludes the global optimum.

**Fix:** Investigate why some runs achieve loglik > -293 and determine whether they are valid. If they represent filter degeneracy or numerical artifacts, exclude them based on loglik.se thresholds rather than an arbitrary upper bound on loglik.

---

### 8. Data normalization makes count-based measurement model questionable

The Google Trends data are normalized so the maximum value is 100, making them an index (not a count of actual individuals). The negative binomial measurement model, which is appropriate for count data, is applied directly to these normalized indices. The interpretation of `rho` as a "reporting rate" and `H` as "number of new infections" breaks down: there is no meaningful relationship between the latent SIRS process (in units of individuals) and the observed index (a dimensionless number bounded at 100). The paper acknowledges in Section 4 that "it is difficult to interpret the reporting rate and population size" but does not address the fundamental incompatibility.

**Fix:** Either rescale the data to approximate counts (acknowledging additional uncertainty), or use a measurement model appropriate for bounded indices (e.g., a beta distribution). Document explicitly how `N` relates to the actual population of potential searchers.

---

## Minor Issues

### 9. Profile likelihood: eta is profiled over range [0.01, 0.1] but global search upper bound is 1.0

The profile design for `eta` is `seq(0.01, 0.1, length=40)`, but the global search uses `upper=c(..., eta=1, ...)`. If the MLE for `eta` lies above 0.1 (which the flat likelihood in the global search suggests is possible), the profile range entirely misses the region of interest and the confidence interval is invalid. Given that parameters did not converge in the global search, the profile range should be informed by where the global search actually concentrated likelihood.

---

### 10. Profile likelihood for mu_RS is acknowledged as uninformative but no structural response is offered

The text states "the profile likelihood plot for mu_RS is so scattered as to be essentially useless" (Section 5.2). This is correct, but the appropriate response — examining whether the resurgence mechanism is supported by the data at all, or testing a nested SIR model without the RS transition — is not taken. The failure of a parameter to be identified is evidence of potential model misspecification that warrants model comparison (SIR vs. SIRS), not just acknowledgment.

---

### 11. Simulation diagnostics are forward simulations, not filtering-distribution simulations

Section 5.1 shows forward simulations from the MLE (or best found) parameters. These do not condition on the observed data and therefore cannot diagnose where the model fails. The appropriate POMP diagnostic is to compare simulations from the filtering distribution (conditioned on observations) to the data.

---

### 12. loglik.se threshold for profile box is 2, which is very permissive

Line 301 filters results by `loglik.se < 2`. A standard error of 2 on the log-likelihood is very large — it corresponds to uncertainty of roughly ±4 log-likelihood units at the 95% level. For a dataset with only 88 observations and log-likelihoods near -300, this standard error is too large to support reliable model comparison. This likely reflects the extremely low Np=100 used.

---

### 13. Profile mif2 uses cooling.fraction.50=0.3, differing from global search (0.5) without explanation

The profile computation (line 320) uses `cooling.fraction.50=0.3`, while the global search uses `cooling.fraction.50=0.5`. The cooling schedule affects how quickly the perturbation magnitude decreases and therefore how well the optimizer converges. This inconsistency is unexplained and makes it harder to interpret differences between the two sets of results.

---

### 14. Commented-out code left in the Rmd

Several lines of commented-out code remain in the Rmd: `# read_csv('price.csv') -> price`, `# price$High[...] <- 0`, `# guesses$N = runif(...)`, and `#write_csv("gme_params.csv")` / `#read_csv("gme_params.csv")`. These suggest abandoned analysis paths. The report should either explain why these were not pursued or remove the dead code.

---

### 15. "Benchmark" in Section 4 refers to a manually chosen parameter set, not a model class

Section 4 states "As a benchmark, we compute the likelihood of the parameter set used in the simulation in the previous section." This is not a benchmark in the standard sense (comparison to a different model class). The term "benchmark" should be reserved for comparisons to non-mechanistic models, and the pfilter evaluation of manually chosen parameters should simply be called a "reference likelihood" or "starting-point evaluation."

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project07/blinded.Rmd`
