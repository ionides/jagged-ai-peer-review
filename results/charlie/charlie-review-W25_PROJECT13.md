# Peer Review: W25 Project 13
## Statistical Modeling of Kepler Light Curves for Exoplanet Detection

---

## Summary

This project applies a POMP framework to Kepler light curve data for exoplanet detection, combining a boxcar transit model with an Ornstein-Uhlenbeck (OU) process to represent correlated stellar noise. The central scientific question is whether this model can accurately capture transit signals and provide interpretable parameter estimates. While the problem domain is interesting and the use of a state-space framework for astrophysical time series has genuine merit, the project suffers from several critical methodological failures: the reported optimization results contain an explicit author-acknowledged placeholder (fabricated log-likelihood values), the inference procedure misuses the particle filter through a non-standard global optimizer rather than iterated filtering, no benchmark model comparison is provided, no profile likelihoods or convergence diagnostics are presented, and hard-coded absolute paths prevent reproduction on any machine other than the author's.

---

## Major Issues

### 1. Fabricated (Placeholder) Log-Likelihood Values Reported as Genuine Results

The most severe issue in this manuscript is that the reported quantitative results are explicitly acknowledged by the author as invented. In the Inference and Optimization section, the text states:

> "Note: I made up these numbers based on typical patterns—swap in your actual log-likelihood values if you have them!"

The two log-likelihood values cited in that section — **-129990.145989** (Iteration 1) and **-151017.163218** (Iteration 36) — are therefore fabricated. The Discussion then cites -151017.163 as the "best log-likelihood" from Iteration 50, repeating a number that has no computational basis.

This failure invalidates all goodness-of-fit claims, all convergence claims, and all comparative statements based on the optimization trace. It also creates an internal contradiction: the text says the log-likelihood "got better over time," but the two cited values go from -129990 to -151017, which is a decrease (more negative = worse fit), directly contradicting the claim of improvement.

No conclusions about model fit or optimization convergence can be credited until the computation is actually run and genuine values are reported. (See the `pomp-placeholder-result-audit` skill for the full diagnostic procedure.)

---

### 2. DEoptim Applied to a Stochastic Particle-Filter Likelihood — the Cost Function is a Random Variable

The project uses `DEoptim` to minimize the negative log-likelihood, where the objective function calls `pfilter(pomp_model, params = params_named, Np = 1000)` with a single stochastic draw per evaluation (chunk `step3`). Because `pfilter` is a Monte Carlo estimator, the objective function is itself a random variable. DEoptim, a deterministic-strategy evolutionary optimizer, is therefore minimizing noise: each time the same parameter vector is evaluated, it receives a different objective value, so the optimizer has no stable surface to descend. The parameter estimates that result from this procedure have no valid statistical interpretation.

The correct approach for POMP inference is iterated filtering via `mif2()`, which uses specially designed perturbation schedules to navigate the stochastic likelihood surface, or PMCMC for Bayesian inference. Replacing DEoptim with `mif2` would immediately provide convergence diagnostics (likelihood traces across IF2 iterations) and yield a proper MLE.

**Reference:** Wheeler et al. (2024) §Computational adequacy; `pomp-inference-misuse` skill.

---

### 3. No Non-Mechanistic Benchmark Comparison

The project never compares the POMP model's fit against any non-mechanistic statistical baseline (e.g., ARIMA, auto-regressive model, or even a simple Gaussian white-noise model). Without such a comparison, it is impossible to determine whether the model's OU + transit structure captures meaningful signal beyond what a simpler model would achieve. The fit could be entirely dominated by the OU component fitting the noise, with the boxcar transit contributing negligibly — this cannot be detected without a benchmark.

**Reference:** Wheeler et al. (2024), §Benchmark comparison; POMP checklist item #2.

---

### 4. No Quantitative Goodness-of-Fit Reporting

Aside from the fabricated log-likelihood values discussed in Issue 1, the paper reports no valid quantitative goodness-of-fit measures. The Discussion states "The quality of the model fit is high, as evidenced by the close alignment of observed and predicted flux values," relying entirely on visual inspection of light curve plots. Visual assessment alone is explicitly insufficient by the standards of this field.

No log-likelihood value computed on real data, no AIC, and no comparable metric appears anywhere in the paper. Even if the DEoptim procedure were corrected, the absence of a quantitative fit summary would remain a gap.

**Reference:** Wheeler et al. (2024): "Visual comparisons alone are only a weak and informal measure of goodness-of-fit"; POMP checklist item #3.

---

### 5. No Convergence Diagnostics

The optimization is described as having converged ("DEoptim converged to a best log-likelihood of -151017.163"), but this value is fabricated (see Issue 1) and no convergence traces are shown. There are no log-likelihood traces across DEoptim iterations, no evidence that multiple independent runs from different starting points reached similar optima, and no comparison of results across different random seeds. Without such evidence, there is no basis for trusting that the reported parameter estimates are near any meaningful optimum.

For comparison, Wheeler et al. (2024) report that their best model required 28,938 CPU-hours across 7,568 parallel jobs to achieve a well-characterized likelihood surface; the authors here use 50 iterations of DEoptim, with no justification of why this is sufficient.

**Reference:** POMP checklist item #6.

---

### 6. No Profile Likelihoods or Parameter Uncertainty Quantification

Profile likelihoods are not computed for any parameter. The paper presents point estimates for all seven parameters (t0_1, P_1, delta_1, d_1, p_1, log_theta_ou, log_sigma_ou) with no confidence intervals of any kind. For the key scientific parameters — transit depth delta_1 and orbital period P_1 — the absence of uncertainty quantification makes it impossible to assess whether the estimated values are identifiable from the data or are merely artifacts of the optimization starting point.

The paper also does not discuss whether the scaling parameter p_1 (estimated at ~0.46) is identifiable separately from delta_1; these two parameters multiply together in the transit model and are potentially collinear.

**Reference:** Wheeler et al. (2024), §Parameter identifiability; POMP checklist item #5.

---

### 7. Hard-Coded Absolute Paths Prevent Reproduction

The data loading code in the setup chunk uses absolute paths to the author's local filesystem:

```r
tce_data <- read.csv("/home/ppratik/ondemand/TCE.csv")
koi_data <- read.csv("/home/ppratik/ondemand/KOI.csv")
false_positive_data <- read.csv("/home/ppratik/ondemand/false_positive.csv")
light_curve_data <- read.csv("/home/ppratik/ondemand/Statistics.csv")
```

These paths resolve only on the author's machine. The repository does include the CSV files (TCE.csv, KOI.csv, false_positive.csv, Statistics.csv), but the code as written will fail immediately on any other machine. This is a textbook reproducibility failure.

**Reference:** Code supplement checklist item: "Relative paths only (no `C:/Users/...`)."

---

### 8. Simulated Flux Used as Model Validation Without Filtering Distribution

The model "validation" in the Results section generates 50 forward simulations from the fitted parameters via `simulate(pomp_model, params = params_est, nsim = 50, ...)` and visually compares them to the observed data. These simulations are drawn unconditionally from the model's prior process distribution — they are not conditioned on the observed data. As a result, the overlap between simulated and observed trajectories is a consequence of the fitted parameters governing the overall variance of the OU process, not evidence that the model correctly accounts for what was observed during the mission. The correct diagnostic is to extract the filtering distribution from `pfilter()`, which conditions the latent OU state on all observed flux values up to each time point.

**Reference:** `pomp-simulate-as-latent-state-inference` skill; simulation checklist item #9 (filtering distribution vs. forward simulation).

---

### 9. Internal Contradictions in Parameter Reporting

The paper contains multiple contradictions in the reported parameter values:

- The Results section states the orbital period P_1 = 11.20 days and calls this "a long-period exoplanet candidate."
- The Discussion repeats P_1 ≈ 11.20929925 days, again described as "long-period."
- The Conclusion changes the period: "orbital period of 11.20929925 days" — consistent — but then states "consistent with a long-period exoplanet," which contradicts the Summary section claim that "the results indicant a long-period planet with an orbital period of approximately 32 days."

The Conclusion section claims "approximately 32 days" while all parameter tables and the Results section report 11.2 days. This contradiction cannot be reconciled by rounding error and further undermines the reliability of the reported results.

---

### 10. DEoptim Time Step Inconsistency: delta.t = 1 but Data Has Non-Integer Spacing

The POMP model uses `rprocess = euler(ou_step, delta.t = 1)` with a hard-coded `delta_t = 1.0` inside the `ou_step` Csnippet. Kepler data is recorded approximately every 30 minutes (long cadence), not at 1-day intervals. The actual time steps in the data will be approximately 0.0208 days (30 minutes / 1440 minutes per day). Using `delta.t = 1` causes the OU process to evolve at a rate that mismatches the observation cadence by roughly a factor of 48. This systematic error inflates the effective variance of the OU process relative to the noise in the data, and it makes the fitted theta_ou and sigma_ou parameters physically uninterpretable in BKJD units.

---

## Minor Issues

- **Writing quality**: The manuscript contains numerous informal phrasings inconsistent with academic prose ("Let me know if your bounds differ," "swap in your actual log-likelihood values if you have them!"), along with pervasive typos ("starlite," "lite curves," "dorm" for `dnorm`, "potentiality," "frum," "bi," "cud"), and second-person address in a third-person report. These suggest the manuscript was not proofread before submission.

- **p_1 misinterpreted as a probability**: The scaling factor p_1 is described as "the probability of the transit being a true exoplanet signal." This interpretation is not supported by the model specification. In the transit model, p_1 simply scales the transit depth (flux_pred -= p_1 * delta_1), so it modulates the effective depth, not a binary true/false probability. The bar plot titled "Estimated Probabilities with Dispositions" and the description "the estimated p_1 is approximately 0.07" (which conflicts with the reported estimate of 0.46) conflate a continuous scaling parameter with a probability.

- **Residuals plot color**: The residuals plot is coded as `col = "yellow"` on a white background, which will be essentially invisible in print or on most displays. The code comment says "line in yellow" as if this is intentional.

- **Python dependency for batman**: The setup chunk imports the `batman` Python package via `reticulate` but `batman` is never actually used in any model computation. The boxcar transit model is implemented entirely in C snippets. This import adds an unnecessary external dependency and increases the risk of environment incompatibility.

- **pomp and spatPomp versions not pinned**: No `renv` lockfile or `sessionInfo()` output is provided. The `pomp` package API has changed substantially across versions. Without version pinning, results may not reproduce on current CRAN releases.

- **No README**: The repository includes no documentation explaining how to run the code, what data files contain, or what order scripts should be executed. The README.rtf file is in a binary-adjacent format and likely insufficient.

- **No seeds set before DEoptim**: The optimization does not set a random seed before calling `DEoptim`, so even if the computation were otherwise valid, results would not be exactly reproducible across runs.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/blinded.Rmd`
