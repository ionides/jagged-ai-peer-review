# Peer Review: W22 Project 17 — US COVID-19 Cases Analysis

## Summary

This project applies SARIMA and SEIR models to US daily COVID-19 case counts from June 5, 2021 to March 29, 2022. The authors use AIC-guided model selection for the SARIMA component and iterated filtering (IF2) with local and global search for the SEIR component. Strengths include the use of a time-varying transmission rate to capture distinct epidemic phases (including Omicron), proper use of `logmeanexp` for likelihood aggregation, and the application of the `pomp` package with the standard run_level framework. However, the project has several serious flaws: the SEIR measurement model links observed cases to recoveries rather than new infections, initial conditions violate population conservation and biological plausibility, no profile likelihoods are computed, and the SARIMA model is non-causal and non-invertible without remediation.

---

## Major Issues

### 1. Measurement model accumulates recoveries instead of new infections

The rprocess code updates `H += dN_IR`, accumulating I→R transitions (recoveries), and the measurement model then sets `Cases = rho * H`. However, the data represent newly confirmed cases, which should correspond to new infections (S→E or E→I transitions), not recoveries. With `mu_IR = 0.1` per day and `mu_EI ≈ 0.1` per day, observed cases are modeled as proportional to events occurring approximately 10–20 days after actual exposure. This introduces a substantial temporal displacement that is never acknowledged or justified. The standard practice for SEIR models is to accumulate `dN_EI` or `dN_SE` in the reporting accumulator. This error could systematically distort all estimated transmission parameters and the implied epidemic dynamics.

**Fix:** Change `H += dN_IR` to `H += dN_SE` (or `H += dN_EI` if onset rather than infection is intended as the reporting event), and verify that the measurement model and process model are semantically consistent.

---

### 2. Initial conditions violate population conservation

The `rinit` function sets `S = N = 334,515,015`, `E = 200,000`, `I = 270,000`, `H = 0`. This means `S + E + I = 334,985,015 > N` at t = 0, violating the closed-population assumption stated in the model. In addition, by June 2021 approximately 100 million Americans had already been infected or vaccinated; setting the entire US population as susceptible is biologically implausible and will cause the model to overestimate the susceptible pool, distorting transmission rate estimates.

**Fix:** Set `S = N - E - I` in `rinit` to enforce compartment conservation, and introduce an initial recovered/immune fraction (either fixed based on external data or estimated as a parameter) to reflect the pre-existing population immunity as of June 2021.

---

### 3. No profile likelihood and no confidence intervals for SEIR parameters

The project estimates 11 free SEIR parameters but reports no profile likelihoods and no confidence intervals for any of them. Without profile likelihoods, it is impossible to assess whether parameters such as `b1`–`b7`, `ei1`, `ei2`, `rho`, or `tau` are identifiable from the data. The reported point estimates may reflect a ridge or a flat region of the likelihood surface rather than a well-defined maximum. This is a fundamental gap in uncertainty quantification. Per Wheeler et al. (2024, §Parameter identifiability), profile likelihoods are essential for distinguishing estimated parameter values that reflect genuine data constraints from those that are essentially unconstrained.

**Fix:** Compute profile likelihoods for at least the key epidemiological parameters (`rho`, `tau`, one or more `b` values), using the MCAP or Wilks threshold to determine confidence intervals.

---

### 4. SARIMA model is non-causal and non-invertible; not remediated

The authors identify that the fitted SARIMA(5,1,5)×(2,1,1)_7 model has roots inside the unit circle (both AR and MA), indicating the model is neither causal nor invertible. This is acknowledged in the report but no action is taken: the model is retained and used for prediction and likelihood comparison. A non-causal model implies future values influence the current value, which contradicts the temporal structure of the data. A non-invertible model means the residuals cannot be expressed as a convergent function of past observations, undermining all residual diagnostics. The conclusion that "SARIMA works well" is not supportable given this finding.

**Fix:** Constrain the ARMA orders or try alternative specifications (e.g., lower p, q) that yield a causal and invertible model. If high-order models are preferred, verify that the roots are genuinely outside the unit circle.

---

### 5. Direct log-likelihood comparison between SARIMA and SEIR is invalid

The conclusion states the SARIMA log-likelihood is −3672.181 and the SEIR log-likelihood is −3684.733, and uses these to rank the models. However, the SARIMA model is fitted to differenced and seasonally differenced data (d=1, D=1, period=7), effectively conditioning on the first 8 observations and computing the likelihood over approximately 290 observations. The SEIR model is fit to all 298 observations. Likelihoods conditioned on different observation sets are not directly comparable. Additionally, the SARIMA uses a Gaussian measurement model while the SEIR uses a normal approximation. The comparison as presented is not valid without adjustment.

**Fix:** Acknowledge this limitation explicitly. If comparison is desired, either compute the SARIMA likelihood on the original (non-differenced) data using a model that incorporates the trend and seasonal structure, or restrict both likelihoods to the same set of observations.

---

### 6. Random walk perturbation sizes for transmission parameters are 10x below standard

The rw.sd for `b1` through `b7` is set to 0.002 on the log scale. The course standard (Ch 15, p31) for parameters estimated on a transformed scale is rw.sd = 0.02. At 0.002, each perturbation moves the log-transformed parameter by only 0.2%, which is extremely small. This severely restricts the ability of IF2 to explore the parameter space during local search, potentially trapping the optimizer near the starting point. The authors observe that parameters have not converged in the local search trace plots, which is consistent with insufficient perturbation magnitude. The global search partially compensates by drawing random starting points from a box, but the subsequent optimization within each global run is still hampered by overly small perturbations.

**Fix:** Increase `rw.sd` for `b1`–`b7` to at least 0.02 to match the course standard, re-run local search, and examine whether convergence improves.

---

## Minor Issues

### 7. Text–code mismatch for starting parameter b5

The mathematical specification of starting parameters (under "Choosing starting points") lists `b5 = 1.5`, but the code chunk initializes `b5 = 0.15`. These differ by a factor of 10. The value 0.15 is consistent with the other `b` values in the code and with the global search box (0.12–0.18), so the code is likely correct. However, the discrepancy undermines confidence in the documentation.

---

### 8. Covariate period for intervention 5 inconsistent with text description

The text states that the b5 period runs from 12/09 to 12/21/2021 (approximately 13 days). The covariate table, however, assigns `rep(5, 40)`, which — starting from the data origin of June 5, 2021 — places the b5 period from 2021-11-12 to 2021-12-21 (40 days). The text description is inconsistent with the actual implementation by approximately 27 days. The code is internally consistent, but the documentation is misleading.

---

### 9. Global search likelihood evaluation uses Np=100 (hardcoded) vs. Np=1000 in local search

In the global search likelihood evaluation chunk, `pfilter` is called with `Np=100` hardcoded, regardless of `run_level`. The local search uses `Np=Np` (= 1000 at `run_level=2`). This inconsistency means the global search log-likelihoods are evaluated at 10x fewer particles than the local search, making the two sets of log-likelihoods less comparable. With `Np=100`, particle filter variance is higher, though this is partially offset by the `replicate(10, ...)` aggregation.

---

### 10. No non-mechanistic benchmark for the SEIR model

The paper compares SARIMA and SEIR to each other, but does not compare either to a simple non-mechanistic baseline such as an IID negative binomial or a POMP model with no mechanistic structure. While benchmark comparison is not required in the course context (531-conventions.md), the SEIR model fits 12.5 log-likelihood units worse than SARIMA. The project would benefit from an IID or autoregressive negative binomial benchmark to assess whether either model captures meaningful temporal structure (see Wheeler et al. 2024, §Benchmark comparison).

---

### 11. Convergence incomplete but not addressed

The authors note in the conclusion that "trajectory plots for some variables still do not show significant convergence." This is identified but no action is taken — no additional global search runs, no increase in Nmif or Np, no discussion of whether the reported likelihood is near the MLE. At run_level=2 with Nmif=100, convergence is not guaranteed, particularly with rw.sd=0.002 for the transmission parameters (see Issue 6). The project should either confirm convergence is adequate or acknowledge that the reported MLE may be suboptimal.

---

### 12. No model diagnostics reported for the SEIR fit

Beyond a visual simulation overlay, no model diagnostics are presented for the SEIR model: no effective sample size (ESS) plot from the particle filter, no conditional log-likelihood trace, and no comparison of summary statistics between simulated and observed data. Per Wheeler et al. (2024, §Model diagnostics), conditional log-likelihood plots are valuable for identifying periods of poor fit and motivating model improvements. This is particularly relevant here given the complex piecewise transmission structure.

---

### 13. `find_best_local` uses unreliable mif2 internal log-likelihood

The function `find_best_local` selects the best local search run by comparing `logLik(mifs_local[[i]])` directly from the mif2 objects. The mif2 internal log-likelihood is not reliable for inference because parameter perturbations are applied in the final iteration (per course notes, Ch 15, p37). The proper approach is to re-evaluate using replicated `pfilter` calls, which is done separately in `local_search.rds`. In practice, the global search only uses `fixed_params` from the selected local best run (all free parameters are overridden by random box draws), so this error has no effect on results. It is nonetheless misleading.

---

### 14. Recovery rate mu_IR fixed without justification in the literature

`mu_IR = 0.1` per day (mean recovery time 10 days) is fixed and not estimated. No citation or sensitivity analysis is provided to justify this choice. For COVID-19 in mid-2021, the mean duration of infectiousness varied substantially across variants and disease severity levels. Fixing this parameter without justification constrains the model in ways that may affect other parameter estimates, particularly `rho`.

---

### 15. QQ-plot non-normality acknowledged but not addressed for SARIMA

The QQ-plot shows heavy tails in the SARIMA residuals, and the authors correctly note the normality assumption does not hold. However, no remediation is attempted (e.g., a transformation of the response, a t-distributed error model, or noting that the model is still useful under mild non-normality). The transition to the SEIR model is partly motivated by this finding, but the SEIR model uses a normal approximation measurement model (`pnorm`/`rnorm`) as well, so the distributional concern is not resolved.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project17/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project17/local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project17/global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project17/mifs_local.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project17/mifs_global.rds`
