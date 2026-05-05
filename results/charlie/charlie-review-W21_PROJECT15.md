# Peer Review: W21 Project 15
## An Analysis of COVID-19 Cases in Washtenaw County

---

## Summary

This project fits a Susceptible-Exposed-Infectious-Recovered (SEIR) compartmental model to daily confirmed COVID-19 cases in Washtenaw County, Michigan (March–December 2020). The model employs a piecewise-constant contact rate beta across five periods to account for multiple epidemic waves, and uses likelihood-based inference via iterated filtering (mif2) with a global search over 500 starting points. Key strengths include the inclusion of a benchmark comparison (negative binomial IID and SARMA), proper use of logmeanexp for likelihood aggregation, and a profile likelihood for the reporting rate rho. The main weaknesses are: the SEIR model's loglikelihood is substantially worse than the SARMA benchmark (-1,151.66 vs -1,104.23); key epidemic parameters mu_EI and mu_IR are fixed without identifiability assessment; the rho profile confidence interval rests on only three data points; and the rw.sd for tau is so small that the parameter cannot be meaningfully optimized by mif2.

---

## Major Issues

### 1. SEIR model fails to beat the SARMA benchmark; no structural revision attempted

The SARMA(3,3)x(1,1)_7 benchmark achieves a Jacobian-corrected log-likelihood of -1,104.23, which is 47.4 log-units above the SEIR MLE of -1,151.66. The authors acknowledge this gap and attribute it to the unmodeled weekly periodicity visible in the data and the periodogram. However, no structural revision to the SEIR model is attempted in response. Per Wheeler et al. (2024) and course instruction (MT2 Q4-02), when a mechanistic model fits substantially worse than a non-mechanistic benchmark, the correct response is to revise model structure — not simply accept the result. The identified 7-day seasonal cycle should have motivated at least a sensitivity analysis or model variant incorporating day-of-week effects. As the model currently stands, the conclusion that the SEIR model "can fit the data pretty well" (Conclusion section) is contradicted by the benchmark comparison.

### 2. rho profile confidence interval based on only three points above the threshold

The authors state: "we would want to remain cautious about this result as only three points are above the threshold." A profile likelihood confidence interval requires sufficient coverage of rho values above the chi-squared cutoff to identify both the lower and upper CI bounds with confidence. With only three points above the threshold (Error 1.9, course-confirmed), the shape of the profile is ambiguous near the cutoff, and the reported CI of [40.97%, 48.01%] is not statistically reliable. The profile plotting code (`filter(rank(-loglik) < 3)`) further restricts the visible points to at most 2 per rho bin, compressing the evidence. The profile should be re-run with a denser grid covering the CI region, and the report should present a profile curve with clearly resolved upper and lower CI intersections.

### 3. rw.sd for tau is negligibly small relative to the scale of optimization needed

The perturbation for tau in all mif2 calls is rw.sd = 0.0001 on the log scale (line 319). Since tau uses a log transformation (partrans = log), this corresponds to a multiplicative factor of exp(0.0001) - 1 ≈ 0.01% per IF2 step. The MLE tau is approximately 0.101, while the starting value is 0.001 — a ratio of ~100x, or 4.6 units on the log scale. No single mif2 chain with 100 iterations and rw.sd = 0.0001 can bridge this gap through the random walk perturbation alone. This means tau optimization depends entirely on the choice of starting value sampled by the global search, not on IF2 exploration. Consequently, the mif2 algorithm does not meaningfully optimize tau, making the MLE and all downstream uncertainty assessments for tau unreliable. The standard perturbation size for parameters on a transformed scale is rw.sd = 0.02 (course note Ch 15, p31). The tau perturbation should be revised to at least 0.02 on the log scale.

### 4. MLE for tau lies at the global search box boundary

The global search samples tau uniformly in [0, 0.1] (line 432), but the MLE tau reported in writeup_params.csv is approximately 0.101, which exceeds the box upper bound of 0.1. Since mif2 with rw.sd = 0.0001 cannot move tau far from its starting value (see Issue 3), the MLE is effectively constrained to the boundary of the search region rather than representing a free maximum. This indicates the global search has not explored the likelihood surface for tau adequately. A wider search box (e.g., tau in [0, 1]) and a larger rw.sd are needed to identify the true MLE (POMP checklist #6, computational adequacy; POMP checklist #5, parameter identifiability).

### 5. mu_EI and mu_IR fixed without profile likelihood or identifiability assessment

Both mu_EI and mu_IR are fixed at 0.1 throughout all analyses, including local search, global search, and profile likelihood. While the authors justify the fixed values by citing external literature (incubation period 2-14 days, recovery period ~10 days), no profile likelihood or sensitivity analysis is performed to assess whether the data support these values, or whether fixing them constrains other parameter estimates. Per POMP checklist #5 (parameter identifiability), fixed parameters require explicit justification that they are not identifiable from the data, or a demonstration that results are insensitive to their values. The choice of mu_EI = mu_IR = 0.1 implies identical 10-day incubation and recovery periods, which is biologically arbitrary and not separately justified for Washtenaw County.

### 6. Profile CI construction conflates profile and global search results

The profile confidence interval for rho is computed from the entire writeup_params.csv file (`all = read.csv(PARAMS_FILE) %>% filter(is.finite(loglik))`), which includes local search (id=1), global search (id=2), and profile (id=3) results pooled together. The profile envelope is then constructed by taking the top-ranked loglik per rho bin across all runs. This is not a profile likelihood: the profile likelihood at a given rho value requires optimizing over all other parameters with rho fixed at that value. Using the global search results (where rho was free) as part of the profile curve contaminates the profile with unoptimized nuisance parameters and can produce an artificially high or low profile at certain rho values. The profile likelihood should be constructed only from the dedicated profile optimization runs (id=3), applying `group_by(round(rho, 2))` to those results only.

---

## Minor Issues

### 7. Local search results hidden from the report

The local search results table and pairs plots are set to `eval = FALSE` in the source code (lines 411-419), meaning they do not appear in the rendered report. The local search section describes the trace plots and notes that "some runs are stuck in local maxima," but the reader cannot verify the claims about likelihood progress or parameter trajectories. At minimum, the best few rows from the local search results should be presented to document the starting-point quality for the global search.

### 8. No model diagnostics beyond forward simulation

The project presents no conditional log-likelihood plots, effective sample size (ESS) diagnostics from the particle filter, or filtering-distribution comparisons. Only forward simulations from the MLE are shown. Per POMP checklist #4 (model diagnostics), conditional log-likelihood plots by time point would reveal which periods the model fits poorly (e.g., the winter 2020 surge), and ESS monitoring during pfilter runs would reveal whether particle degeneracy is occurring. These diagnostics were available in the cached pfilter outputs and should have been presented.

### 9. Time-varying beta break dates appear post-hoc rather than pre-specified

The five beta periods are defined by specific calendar dates (e.g., March 24, June 8, June 29, September 12), with break dates that appear to align visually with inflection points in the case time series. Only one break point (the initial period of external importation) has an independent citation. The remaining four are not linked to documented policy events (specific executive orders, school closures, or reopening stages) with citations. Given the documented political and public health timeline of COVID-19 in Michigan, these break dates should be tied to verifiable events, or the sensitivity of results to break point choice should be assessed.

### 10. No model structure comparisons using likelihood

Only one model structure — SEIR with five-period beta — is fitted. No simpler variants (fixed beta, two-period beta, three-period beta) are compared using likelihood ratio tests or AIC. Given that the model has five free beta parameters, a likelihood ratio test comparing five-period vs. four-period vs. three-period beta specifications would be informative about whether all five periods are statistically necessary (POMP checklist #8, model variations).

### 11. Initial conditions include an unexplained 300-person discrepancy in population accounting

The rinit code sets S = eta*N, E = 100, I = 200, H = 0. The initial population is S + E + I = eta*367601 + 300, with R = N - S - E - I = N*(1 - eta) - 300 implicitly recovered at time 0. This means the model assumes N*(1-eta) - 300 individuals have already recovered at the start — a large and biologically implausible number for a county with few recorded cases at the onset. For eta = 0.09768 (MLE), R(0) = 367601*(1-0.09768) - 300 ≈ 331,485. This implies ~90% of the county had already recovered before the epidemic was tracked, which contradicts the data narrative. The initial conditions should be explicitly specified and justified.

### 12. SARMA AIC value inconsistent with reported log-likelihood

The text states the SARMA(3,3)x(1,1)_7 model has AIC of 231.698 on the log(cases+1) scale. The R output `arma33_s11$loglik - sum(log_cases)` gives the Jacobian-corrected loglik of -1,104.23, which would correspond to AIC = 2*(-(-1104.23)) + 2*14 = 2236.46, not 231.698. The AIC value of 231.698 is on the log(cases+1) scale, not the original scale. The comparison of log-likelihoods (-1,104.23 for SARMA vs -1,151.66 for SEIR) is correctly performed on the original scale, but the reported SARMA AIC of 231.698 is on a different scale and should not be cited alongside the other quantities without clarification.

### 13. Measurement model undefined when H = 0

The dmeas Csnippet computes `mean = rho*H` and `sd = sqrt(pow(tau*H, 2) + rho*H)`. When H = 0, mean = 0 and sd = 0, making the normal distribution degenerate. The code handles Cases > 0 by computing `pnorm(Cases+0.5, 0, 0, 1, 0) - pnorm(Cases-0.5, 0, 0, 1, 0)`, which gives 0 in C for non-zero Cases. Only the tolerance (tol = 1e-25) prevents the log-likelihood from being -infinity. While H = 0 may be rare in practice during the epidemic, this edge case should be explicitly handled, for example by adding a small epsilon to the variance.

### 14. Single-core execution reported for a 500-start global search

The code sets NCORES = 1L (line 118), so the foreach %dopar% loops run serially. The 500-start global search with 7 mif2 passes each (700 total iterations per start, NP = 1000 particles, 20 pfilter evaluations) would require an extremely long wall-clock time on a single core. The total computation time is not reported, making it impossible to assess whether the cached results represent adequate computational effort or were terminated early. The report should document the total CPU time and confirm that all 500 starts were completed.

### 15. No discussion of parameter uncertainty beyond rho

The profile likelihood is computed only for rho. No uncertainty assessment is presented for the five beta parameters, eta, or tau, all of which are free parameters in the global search. Given that the model has 8 free parameters (b1-b5, rho, eta, tau), a complete uncertainty characterization requires profile likelihoods for at least the scientifically meaningful parameters. The contact rate parameters (b1-b5) are central to the epidemiological conclusions, yet no confidence intervals are reported for them (POMP checklist #5).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project15/pomp_cache/writeup_params.csv`
