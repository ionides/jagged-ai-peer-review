# Peer Review: Information Epidemics — Modeling Search Trends during the GameStop Short Squeeze Using Stochastic Compartmental Models
**Semester:** W21 | **Project:** 07

---

## Summary

This project applies a stochastic SIRS compartmental model to Google Trends search data for "gme" (GameStop's ticker symbol) over an 88-day window spanning the January 2021 short squeeze. The motivation is appealing and the framing is creative, but the execution suffers from several methodological weaknesses that undermine the reliability of the results. The global search is run at an insufficiently low computational level, the profile likelihood procedure is incorrectly constructed, and several modeling choices are inadequately justified. The authors are commendably transparent about many of these limitations, but transparency does not substitute for correction.

---

## Weaknesses (Most Critical First)

### 1. [Major] Global Search Run at `run_level = 1` — Far Too Small for Reliable Inference

The code sets `run_level <- 1`, which yields `Np = 100` particles, `Nmif = 10` MIF2 iterations, and only `Nseq = 100` starting points. These are clearly labeled "debug" settings in the comment (`# helps us debug -- we want to use 3 when actually running`), yet the saved `results.rda` is the product of these settings. A particle filter with 100 particles on a 6-dimensional parameter space over 88 time points provides extremely noisy likelihood estimates, and 10 MIF2 iterations are nowhere near sufficient for convergence. All downstream inferences — the best-fit parameter set, the profile confidence intervals, and the scatterplot matrix — are therefore unreliable. The fact that `run_level = 3` settings (`Np = 5000`, `Nmif = 200`, `Nseq = 5000`) exist in the code but were not used is a critical failure of reproducibility and scientific rigor.

### 2. [Major] Profile Likelihood Code Uses `guesses` Instead of `guesses2` — Profiles Are Not Profile Likelihoods

The profile likelihood chunk (Section 5.2) builds `guesses2` via `profile_design()` correctly set up to profile over `eta`, but then the `stew` block iterates over `guesses` (the original random global search grid) rather than `guesses2`. This means `results2.rda` is simply a second run of the global search and does not constitute a proper profile likelihood for any parameter. The resulting plots and confidence intervals for `Beta`, `mu_IR`, and `mu_RS` are therefore not profile likelihoods in any valid statistical sense, and Wilks' theorem cannot be applied to derive the stated confidence intervals.

### 3. [Major] Negative Binomial Measurement Model Is Incorrectly Parameterized

The `dnbinom` and `rnbinom` calls use `dnbinom(count, H, rho, give_log)` where `H` is the accumulator for new infections and `rho` is the reporting rate. In R's `dnbinom(x, size, prob)`, the `size` parameter is the dispersion parameter (number of successes in the negative binomial), not a mean. Using `H` as `size` and `rho` as `prob` produces a distribution where the mean is `H*(1-rho)/rho`, not `rho*H` as intended for an epidemiological reporting model. This is a misspecification of the measurement model that causes the likelihood surface to be measuring something other than what is intended. The authors acknowledge that binomial measurement caused problems and switched to negative binomial, but did not verify the parameterization.

### 4. [Major] `mif2()` Call Missing `Nmif` Argument Label — Likely Silent Bug

In the global search chunk, the call is `mif2(..., Np=Np, Nmif, ...)` — the `Nmif` argument is passed positionally without a name. In the `pomp::mif2()` signature, positional arguments after `Np` do not correspond to `Nmif`; this likely passes `Nmif` to an unintended argument or is silently ignored, defaulting `Nmif` to its default value (which may be 1). The same pattern repeats in `results2.rda`. If `Nmif` defaults to 1, the iterated filtering performs only a single filtering iteration, rendering all optimization meaningless.

### 5. [Major] Profile CI for `Beta` Is Extracted from Global Search, Not a Profile

The authors compute a 95% CI for `Beta` of [0.55, 8.21] by filtering the combined `results`/`results2` to rows within 0.5*qchisq(0.95,1) of the maximum, then taking `min`/`max` of `Beta`. This is the projection method applied to a global search scatter, not a profile likelihood. The profile likelihood requires maximizing over all nuisance parameters at each fixed value of `Beta`. Without proper profiling, the interval is almost certainly too wide and statistically invalid. The same issue applies to the CIs for `mu_IR` and `mu_RS`.

### 6. [Major] Data Preprocessing Silently Replaces `"<1"` with `0` — Distorts Measurement at Low Values

The raw data contains entries of `"<1"` for the earliest time points (days 1–14 approximately). The code coerces these to `NA` via `as.numeric()` and then replaces `NA` with `0`. This treats an interval-censored observation ("the true value is in (0,1)") as an exact zero, which biases early dynamics and is inconsistent with the negative binomial measurement model (which assigns zero probability to non-integer count zero if `H > 0`). No acknowledgment or justification of this imputation is provided.

### 7. [Moderate] `rw.sd` in Profile Search Omits Key Parameters — Prevents Proper Optimization

In the `results2.rda` computation, `rw.sd=rw.sd(Beta=0.02, rho=0.02)` only applies random walk perturbations to `Beta` and `rho`. Parameters `mu_IR`, `mu_RS`, `eta`, and `N` have no perturbation and cannot be optimized by MIF2. For a proper global or profile search, all free parameters should be perturbed (or at minimum, the parameters being profiled over should have perturbation set to zero while others remain free). The combination of wrong iteration target (`guesses` vs. `guesses2`) and incomplete `rw.sd` makes the second search doubly invalid.

### 8. [Moderate] No Likelihood Ratio Test Against a Simpler Benchmark

The project computes the benchmark log-likelihood of −297.24 for the hand-tuned parameter set, and the best found is −294. This difference of roughly 3 log-likelihood units is presented without any formal test or comparison against a simpler null model (e.g., a random walk, ARIMA, or constant-rate Poisson model). Without a reference, there is no way to assess whether the SIRS model is adding genuine explanatory power over a trivially simple model. A likelihood ratio test comparing nested models (e.g., SIR vs. SIRS) would be straightforward and informative.

### 9. [Moderate] Population Size `N` Is Unidentifiable and Its Interpretation Is Unclear

The authors fix `N` as a free parameter in [1000, 10000] but acknowledge that because the data are normalized to 100, the absolute population size is not interpretable. The best-fit `N` is approximately 1361, which is implausibly small for an internet-wide phenomenon. Moreover, `N` and `rho` are confounded: any combination of `(N, rho)` that yields the same expected mean will produce similar likelihoods. The authors do not examine this identifiability issue in the pairs plot or profile, and the parameter `N` is excluded from the profile likelihood analysis altogether.

### 10. [Moderate] Spectral Analysis Performed Only on the Second Half of the Data

The smoothed periodogram is computed on `gme$count[45:88]`, explicitly excluding the initial spike. The authors justify this by saying the latter half shows "strong weekly seasonality," but this windowing decision is not formally justified. The spike in early data is the primary phenomenon being modeled; performing spectral analysis only on the post-spike portion and then concluding that seasonality exists introduces selection bias into the exploratory analysis, and the 7.5-day estimated period (not exactly 7) is not discussed critically.

### 11. [Moderate] Initial Conditions Are Partially Fixed Without Justification

The initialization sets `I = 5` and `R = 0` as hard-coded constants while only `S` is set via `eta`. The choice of `I(0) = 5` is arbitrary and has significant impact on the dynamics of a stochastic model. The sensitivity of results to this choice is not explored. In a model with heavy stochasticity and a single large spike at the start, initial conditions matter substantially.

### 12. [Moderate] `H` Accumulator Initialized to 5 and Not Reset Correctly

In the initialization, `H = 5;` sets the accumulator to a non-zero value. Since `H` is listed as an `accumvar` (reset to 0 at each observation time), this initial value only affects the very first measurement interval. However, the chosen initial value of 5 implies that 5 infections are assumed to have occurred before the first observation, which is arbitrary and undocumented.

### 13. [Minor] Pairs Plot Mixes Guesses and Results Without Proper Filtering

The scatterplot matrix in Section 4 binds `guesses` (prior to optimization) with `results` (after MIF2) using `bind_rows(guesses)`, showing guesses as gray and results as red. However, `guesses` have no `loglik` column, so the `mutate(type=if_else(is.na(loglik),...))` logic is correct, but overlaying raw parameter guesses on a likelihood scatter plot obscures the shape of the likelihood surface. The guesses add visual noise rather than insight.

### 14. [Minor] Conclusion Overstates What the Model Has Demonstrated

The conclusion states that "the interpretability offered by compartmental models can be useful in understanding how information might spread like a pathogen" and that "previous research has already showed the utility in modeling information spread using epidemiological methods, and we hope this project has demonstrated some more evidence for such a claim." Given that the parameter search was largely inconclusive, confidence intervals span nearly the entire feasible parameter range, and simulations show only weak qualitative agreement with data, this characterization is too optimistic. The project would benefit from a more calibrated conclusion reflecting the actual strength of the evidence.

### 15. [Minor] No Convergence Diagnostics for MIF2

The project provides no filter convergence plots (e.g., log-likelihood vs. MIF2 iteration, or parameter traces over iterations). For a POMP analysis, these diagnostic plots are essential to judge whether the iterated filtering has converged and whether the cooling schedule is appropriate. Without them, it is impossible to determine whether the optimization was making progress at all, especially given the low `run_level` settings actually used.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project07/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project07/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project07/gme.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project07/Makefile`
