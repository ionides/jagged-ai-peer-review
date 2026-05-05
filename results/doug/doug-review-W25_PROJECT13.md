# Peer Review: W25 Project 13
## "Statistical Modeling of Kepler Light Curves for Exoplanet Detection"

---

## Summary

This project applies a POMP (Partially Observed Markov Process) framework to Kepler light curve data for the star kepid 892376, combining a boxcar transit model with an Ornstein-Uhlenbeck (OU) process to capture correlated stellar noise. The authors use the DEoptim differential evolution algorithm to estimate transit and noise parameters. While the scientific question is interesting and the POMP framework is a reasonable choice for this application, the project has severe methodological flaws: DEoptim is applied to the negative log-likelihood evaluated via a particle filter (pfilter) without the iterated filtering (IF2) framework appropriate for stochastic POMP models, no benchmark comparison is provided, goodness-of-fit is assessed only visually, reported log-likelihood values appear to contain fabricated or contradictory numbers, parameter identifiability is not assessed, and the writing contains numerous internal inconsistencies and apparent placeholder text. These issues collectively undermine the validity of the reported results.

---

## Major Issues

### 1. DEoptim Wrapping pfilter Is Not a Valid Inference Procedure for Stochastic POMP Models

The authors define `neg_log_lik` (chunk `step3`) as a function that calls `pfilter(pomp_model, params=params_named, Np=1000)` and returns the negative log-likelihood from a single particle filter evaluation. DEoptim then minimizes this function. Because `pfilter` with a stochastic process model produces a random (Monte Carlo) estimate of the log-likelihood, the objective function is itself a random variable. DEoptim — a deterministic differential evolution optimizer — is therefore minimizing noise rather than a stable likelihood surface. Each call to `neg_log_lik` with the same parameters produces a different value, so the optimizer has no coherent signal to follow. The standard approach for stochastic POMP models is iterated filtering (`mif2`), which embeds the particle filter inside a properly designed stochastic optimization algorithm that handles Monte Carlo likelihood variability. The parameter estimates reported from this DEoptim run have no valid statistical interpretation as maximum likelihood estimates.

**Fix**: Replace the DEoptim/pfilter combination with `mif2` for parameter estimation, following the standard iterated filtering workflow. If DEoptim is to be retained for comparison, the objective function must be a deterministic function (e.g., a negative log-likelihood evaluated on the deterministic skeleton via `traj_objfun`, or a numerically stable `logmeanexp` over many particle filter replicates).

### 2. Fabricated Log-Likelihood Values and Internal Contradictions

The Results section (line 487-490) states: "Iteration 1: Best log-likelihood = -129990.145989 (a rough start). Iteration 36: Best log-likelihood = -151017.163218 (a big jump!)." Two serious problems arise: (a) the log-likelihood at iteration 36 (-151017) is *more negative* than at iteration 1 (-129990), meaning the fit got worse, not better — yet the text describes this as "a big jump" and "getting better over time"; (b) the same passage explicitly states "I made up these numbers based on typical patterns—swap in your actual log-likelihood values if you have them!" This is placeholder text that was never replaced with actual results. The Discussion section (line 735) then cites a "best log-likelihood of -151017.163" as if it were a real result. The project cannot be evaluated when reported numerical results are acknowledged fabrications.

**Fix**: Re-run the optimization and report actual convergence values. Correct the direction of improvement: log-likelihood increases (becomes less negative) when fit improves.

### 3. No Benchmark Comparison Against a Non-Mechanistic Model

No comparison against any non-mechanistic statistical baseline (e.g., ARMA, Gaussian process regression, or even white-noise model) is provided. Without such a comparison, it is impossible to determine whether the POMP model with an OU process captures meaningful structure beyond what a simple time-series model would achieve. This is the single most diagnostic check for whether a mechanistic model adds value over simpler alternatives (Wheeler et al. 2024, benchmark comparison criterion). The phase-folded light curve and residual plots show some structure, but without a quantitative baseline these visual observations are uninterpretable.

**Fix**: Fit an ARIMA or AR(p) model to the detrended light curve and compare log-likelihoods or prediction errors. This comparison should be quantitative, not only visual.

### 4. Goodness-of-Fit Assessed Only Visually; No Log-Likelihood or AIC Reported

The model fit is evaluated entirely through visual comparisons (light curve overlay, residual time series, residual histogram, ACF of residuals). No log-likelihood value from a properly-evaluated particle filter on the real data is reported, and no AIC or other information criterion is used for model comparison. As Wheeler et al. (2024) note, "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The one numerical likelihood value in the paper is, by the authors' own admission, fabricated.

**Fix**: Report the log-likelihood at the estimated parameter values using `logmeanexp(replicate(10, logLik(pfilter(pomp_model, params=params_est, Np=5000))), se=TRUE)`. This provides both a point estimate and a Monte Carlo standard error for the fit quality.

### 5. No Parameter Identifiability Analysis; No Confidence Intervals

No profile likelihoods are computed for any parameter, and no confidence intervals are reported. The seven-parameter model includes both transit parameters (t0_1, P_1, delta_1, d_1, p_1) and OU parameters (log_theta_ou, log_sigma_ou). Without profile likelihoods it is unknown whether these parameters are individually identifiable from a single light curve. In particular, the transit depth (delta_1) and the scaling factor (p_1) are likely confounded — both scale the transit signal amplitude — yet both are estimated freely with no discussion of this identifiability issue. Wheeler et al. (2024) identify profile likelihoods as essential for assessing parameter identifiability.

**Fix**: Compute profile likelihoods for at minimum delta_1, P_1, and p_1. Report confidence intervals via the MCAP procedure or chi-squared cutoffs. Discuss whether p_1 and delta_1 are jointly identifiable.

### 6. Conceptual Misuse of p_1 as a "Probability of True Exoplanet Signal"

The parameter p_1 (initialized to 1.0, bounded between 0.01 and 1) is described in the Results and Discussion as "the probability of the transit being a true exoplanet signal" and is used to classify TCEs as candidates or false positives. This is conceptually incorrect: p_1 is a scaling factor on the transit depth in the boxcar model, not a posterior probability of planetary origin. The bar plot (Figure 3) displays the estimated p_1 value as if it were a classification probability, and the validation section attempts to match the estimated p_1 against KOI dispositions using this probabilistic interpretation. No probabilistic model of false-positive rate is specified anywhere in the measurement model, so p_1 cannot be interpreted as a probability. The Results section also reports p_1 ≈ 0.07 in one place and 0.46247 in another, an additional internal contradiction.

**Fix**: Either fix p_1 = 1 (removing it as a free parameter) and interpret transit detection as a deterministic function of delta_1, or reformulate the measurement model to include an explicit mixture component with a proper probabilistic interpretation of false-positive origin. Remove all statements equating p_1 to "probability of true signal."

### 7. delta.t = 1 for OU Process Is Inconsistent With the Data Sampling Interval

The `rprocess` is defined with `euler(ou_step, delta.t = 1)`, and the ou_step Csnippet hard-codes `double delta_t = 1.0`. The Kepler PDCSAP flux data used in this project (loaded from `Statistics.csv`) has a cadence of approximately 30 minutes (long-cadence Kepler data), corresponding to roughly 0.02 days between observations rather than 1 day. Using delta.t = 1 means the OU process takes single unit steps between observations that are actually separated by ~0.02 days. The OU parameters theta_ou and sigma_ou are thus calibrated to the wrong time scale, and the resulting noise model does not correspond to the stated continuous-time OU formulation. Furthermore, using delta.t equal to the observation interval (delta.t = 1 in day units, while observations may be sub-daily or daily) raises the question of whether there is any sub-observation-interval process noise at all.

**Fix**: Check the actual time spacing in `light_curve_data$time` (it should be approximately 0.0204 days for Kepler long-cadence). Set `delta.t` to a small fraction of this (e.g., `delta.t = 0.001`). Remove the hard-coded `double delta_t = 1.0` in `ou_step` and use the pomp-provided `dt` variable directly.

### 8. Computational Adequacy Is Not Demonstrated; No Convergence Diagnostics

The DEoptim run uses 50 iterations with a population size of 100. No convergence traces of the log-likelihood across iterations are shown (only fabricated values are cited). There is no evidence that increasing the number of iterations or particles would not change the results, and no multiple independent runs from different starting points are compared to verify that the same optimum is found. The particle filter uses Np = 1000, which may be insufficient for a 763-observation time series — the Monte Carlo variance of the log-likelihood estimate with 1000 particles should be reported. Wheeler et al. (2024) identify computational adequacy as one of the most critical checks for POMP analyses.

**Fix**: Show log-likelihood convergence traces across DEoptim iterations (or switch to mif2 and show the standard IF2 convergence diagnostics). Run multiple independent searches and compare terminal log-likelihoods. Evaluate the Monte Carlo SE of pfilter with increasing Np to verify 1000 particles is adequate.

### 9. Reproducibility: Hard-Coded Absolute Paths and Python Dependency

The Rmd file contains hard-coded absolute paths (`/home/ppratik/ondemand/TCE.csv`, etc.) that are user- and machine-specific. The analysis also depends on the Python `batman` package accessed via `reticulate`, but no Python environment specification (e.g., conda environment YAML or `renv` lockfile) is provided. These barriers mean the analysis cannot be reproduced by anyone other than the original author on the original machine without non-trivial setup. Wheeler et al. (2024) identify complete reproducibility — including archived code and data — as a fundamental requirement.

**Fix**: Use relative paths or `here::here()`. Archive all required data files alongside the Rmd. Provide a `renv.lock` or `environment.yml` specifying the Python environment. Note that `batman` (the Python package) is imported but apparently not used in any code chunk — if it is unused, remove the dependency; if it is used, document the usage.

---

## Minor Issues

### 10. OU Discretization Step Hard-Coded Rather Than Using `dt`

The `ou_step` Csnippet sets `double delta_t = 1.0` manually instead of using the pomp-provided integration step variable (`dt`). This means changing `delta.t` in the `euler()` call would have no effect on the actual integration step used inside the Csnippet, producing a silent inconsistency between the declared and actual time step. The comment "Renamed from dt to avoid conflict" suggests the author was aware of the conflict but chose the wrong resolution — the correct fix is to use `dt` directly (which is the conventional name in pomp Csnippets) or to verify that `dt` is not reserved.

### 11. Internal Contradictions in Reported Results

The Summary section states the estimated orbital period is "approximately 11 days" (P_1 = 11.20929925), but the Discussion summary (line 729) states "an orbital period of approximately 32 days." These are inconsistent. Similarly, the estimated p_1 is stated as 0.46247 in the parameter table but reported as approximately 0.07 in the visual validation section. These contradictions suggest the text was assembled from multiple drafts without cross-checking.

### 12. No Model Diagnostics Beyond Residual Plots

Beyond residual histograms and an ACF plot, no POMP-specific diagnostics are reported. In particular: (a) conditional log-likelihoods over time are not plotted (which would identify time periods of poor fit, e.g., around transit events); (b) effective sample size from the particle filter is not monitored; (c) simulations from the filtering distribution (conditioned on observed data) are not shown — only unconditional forward simulations via `simulate()` are presented. Wheeler et al. (2024) recommend filtering-distribution comparisons as a primary diagnostic for identifying model misspecification.

### 13. Boxcar Transit Duration Is Implausibly Long

The estimated transit duration d_1 ≈ 5.44 days is extremely long for an exoplanet transit. For a star similar to the Sun, most planetary transits last between 1 and 8 hours, with durations exceeding 0.5 days being rare and only expected for extremely long-period planets in grazing orbits. A 5.44-day transit duration for an 11-day orbital period would imply the planet spends nearly half its orbital period transiting the star, which is physically impossible for any bound planetary orbit. No discussion of whether this estimate is physically plausible is provided. This may reflect a model misfit or an optimization failure (consistent with the fabricated log-likelihood values), but the authors do not flag it.

### 14. Writing Quality and Placeholder Text

The manuscript contains multiple instances of informal language inconsistent with academic reporting (e.g., "It's fantastic at finding the global maximum," "This is super important," "swap in your actual log-likelihood values if you have them!"). Several typographical errors appear throughout (e.g., "lite curves," "starlite," "fir subsequent," "frum," "bi large random variations," "dorm" for `dnorm`). The presence of acknowledged placeholder text (the fabricated log-likelihood values) makes it unclear which other parts of the narrative are similarly placeholder rather than actual results.

### 15. Detrending Applied After Quality Filtering but Before POMP Model Setup Is Inconsistent

The preprocessing applies LOESS detrending with span = 0.5 to the quality-filtered flux (lines 162-173), producing `flux_detrended`. The POMP model then treats this detrended flux as the observation. However, the measurement model in `dmeasure_ou` uses the covariate `obs_err` derived from the *original* `PDCSAP_FLUX_ERR` normalized by the *original* flux median — not from the detrended flux. After LOESS detrending, the residual variance structure changes, so using the original photometric error as the observation noise standard deviation in the normal likelihood is not well-justified. No discussion of how detrending affects the error structure is provided.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/blinded.Rmd`
