## Overall Assessment

This project applies a stochastic SIRS compartmental model to Google Trends search-frequency data for "gme" during the 2021 GameStop short squeeze. The scientific motivation is creative and the model choice (SIRS with resurgence) is well-reasoned for a dataset exhibiting multiple peaks. The authors are commendably candid about inconclusive results. However, the submitted analysis has several critical deficiencies: all computations were performed at debug scale (`run_level=1`), a coding error invalidates all profile likelihood calculations, no non-mechanistic benchmark is provided, and no convergence diagnostics are shown. In their current state, the reported likelihoods and confidence intervals cannot be interpreted as meaningful results.

## Key Strengths

- **21.07.S1 — Correct logmeanexp aggregation.** The paper correctly uses `logmeanexp` to aggregate log-likelihoods from replicated pfilter runs (rather than averaging directly), which is a non-trivial detail that many student projects get wrong.
- **21.07.S2 — Motivated model choice.** The SIRS structure is specifically motivated by the re-emergence peaks visible in the data and by analogy to seasonal disease dynamics. This is a stronger justification than simply applying SIR by default.
- **21.07.S3 — Honest assessment of results.** The conclusion candidly attributes the non-convergence of `mu_RS` and `eta` to potential model misspecification rather than claiming false success.

## Major Points

**21.07.1 — Debug-scale computations throughout.**
ID: 21.07.1 | Severity: Major

All results in the paper derive from `run_level=1`: `Np=100` particles, `Nmif=10` IF2 iterations, and `Nseq=100` random starting points. A code comment in the manuscript itself reads "want to use 3 when actually running," confirming these are debug-level settings. With 10 IF2 iterations and 100 particles, the algorithm cannot converge, likelihood estimates have high Monte Carlo variance, and the parameter scatter plots in Section 4 reflect numerical noise rather than the likelihood surface.

Suggested action: Rerun with `run_level=3` (`Np=5000`, `Nmif=200`, `Nseq=5000`). Save `.rda` files from the production run and report the resulting best log-likelihood value in the narrative text.

**21.07.2 — Profile likelihood computation uses the wrong grid.**
ID: 21.07.2 | Severity: Major

Section 5.2 constructs a profile design grid `guesses2` (over `eta`, 40 levels × 15 restarts). However, the `stew(file="results2.rda", ...)` computation block iterates over `guesses` (the global search grid), not `guesses2`. As a result, `results2` is a duplicate of the global search, and the three profile likelihood plots (for `Beta`, `mu_IR`, and `mu_RS`) shown in Section 5.2 are not profiles. The confidence intervals `[0.55, 8.21]` for `Beta` and `[0.30, 0.99]` for `mu_IR` are therefore invalid.

Suggested action: Replace `iter(guesses,"row")` with `iter(guesses2,"row")` in the profile computation block. Compute a separate profile for each parameter of interest. Ensure the profiled parameter is fixed at each grid level while the remaining parameters are freely optimized in the `rw.sd` perturbation.

**21.07.3 — No benchmark comparison against non-mechanistic model.**
ID: 21.07.3 | Severity: Major

No ARMA, ARIMA, or other non-mechanistic model is fit and compared against the SIRS model. The only reference likelihood is for a manually chosen simulation parameter set. Without a benchmark, there is no basis for concluding that the mechanistic model adds value over simpler alternatives. The data have a clear large-peak-then-plateau structure that simpler models may describe well.

Suggested action: Fit at least one ARIMA model to the log-transformed data and compare log-likelihoods numerically. Note that ARIMA and POMP likelihoods are directly comparable for the same observed data.

**21.07.4 — No convergence diagnostics.**
ID: 21.07.4 | Severity: Major

No IF2 trace plots (filter log-likelihood or parameter values over iterations) are presented. The scatterplot matrix in Section 4 shows where parameter values ended up, but not whether the algorithm was still moving when it stopped. Without convergence diagnostics, statements about parameter preferences (e.g., "model converged on estimates of Beta around 1") cannot be verified.

Suggested action: For a representative global search run, plot `traces[,"loglik"]` and the traces of `Beta`, `mu_IR`, `mu_RS` over mif2 iterations. Confirm the filter log-likelihood has plateaued.

## Minor Points

- **21.07.5 — Measurement model parameterization.** The Csnippet `lik = dnbinom(count, H, rho, give_log)` passes `H` (an accumulator for cumulative new infections) as the `size` (dispersion) parameter of the negative binomial. This is non-standard: `H` varies with the filtering trajectory and conflates the reporting process with the overdispersion. A cleaner formulation would use a separate dispersion parameter `phi` and set `mu = rho * H` as the expected count: `lik = dnbinom(count, mu=rho*H, size=1/phi, give_log)`.

- **21.07.6 — rho and N excluded from rw.sd.** The `rw.sd` argument in the mif2 calls perturbs only `Beta`, `mu_IR`, `mu_RS`, and `eta`. Since `rho` and `N` are not perturbed, IF2 never updates them from their initial values, despite the authors listing them as variable parameters. Either include them in `rw.sd` or explicitly fix them and remove them from the variable parameter list.

- **21.07.7 — Spectral analysis subsets to last 43 days without justification.** The smoothed periodogram in Section 2 is computed on `gme$count[45:88]`, omitting the large initial spike. The motivation for this subset is not stated. Including the spike would likely dominate the spectrum; the authors should state explicitly that they are analyzing the post-peak periodicity separately and why.

- **21.07.M1 — ESS not monitored.** Particle filter effective sample size (ESS) is not tracked during filtering. Low ESS indicates filter degeneracy, which can cause unreliable likelihood estimates. Adding `plot(pfilter(...))` or checking `eff.sample.size` for the best parameter set would be a useful diagnostic.

- **21.07.M2 — Best log-likelihood not stated in prose.** The best-fitting parameter set is printed via a code chunk output but is never quoted in the narrative. Readers cannot assess the quality of fit without a reported log-likelihood value.

- **21.07.M3 — Population size N has no clear physical interpretation.** The data are Google Trends indices normalized to a maximum of 100, not counts of individuals. The population parameter N (estimated in the range 1000–10000) therefore has no clear real-world referent, which undermines the interpretability of other parameters (e.g., what does a "reporting rate" of 0.15 mean for a normalized index?). This limitation deserves explicit acknowledgment.
