# Peer Review: W25 Project 13
## "Statistical Modeling of Kepler Light Curves for Exoplanet Detection"

---

## Summary

This project applies a POMP model to Kepler light curve data for star kepid 892376, combining a boxcar transit model with an Ornstein-Uhlenbeck (OU) process for correlated noise. Parameter estimation is performed via the DEoptim differential evolution algorithm rather than the course-standard mif2/iterated filtering framework. While the scientific framing is creative and the POMP model structure is articulated clearly, the project is severely undermined by multiple critical deficiencies: the authors explicitly admit that key reported log-likelihood values are fabricated; the optimization appears to have diverged (likelihood worsened across iterations); no convergence diagnostics, profile likelihoods, or benchmark comparisons are provided; and the residual analysis is computed from an ad hoc single simulation rather than the particle filter filtering distribution. Several numerical inconsistencies within the paper further call the reported results into question.

---

## Major Issues

### 1. Authors explicitly admit fabricated quantitative results

The most serious problem in this manuscript appears in the Inference section. After reporting specific log-likelihood values for iterations 1 and 36, the authors write: *"(Note: I made up these numbers based on typical patterns—swap in your actual log-likelihood values if you have them!)"* This note was never removed from the submitted document. The reported log-likelihood trajectory (-129990 at iteration 1, -151017 at iteration 36) is therefore not based on actual computation. Submitted project reports must report results from actual runs of the code. Placeholder or fabricated numerical results are not acceptable evidence for any conclusion drawn in the paper.

### 2. Reported log-likelihood shows optimization divergence, mischaracterized as improvement

The authors claim the log-likelihood "got better over time," but the opposite is true. The log-likelihood moved from -129990 (iteration 1) to -151017 (iteration 36), a decrease of roughly 21,000 log-likelihood units. Because more negative values indicate lower likelihood, the optimization worsened substantially, not improved. Even setting aside the admission that these numbers are fabricated, the paper's written interpretation of its own numbers is backwards. This error corresponds to Error 1.5 in the course weakness reference: observing declining likelihood and not diagnosing it as optimization failure or model misspecification.

### 3. Single particle filter evaluation per parameter set — no logmeanexp aggregation (CC-Yes)

The `neg_log_lik` function calls `pfilter(pomp_model, params = params_named, Np = 1000)` once and returns `-logLik(pf)`. The particle filter produces a stochastic (noisy) estimate of the log-likelihood. Using a single-run log-likelihood as the objective function for DEoptim means the optimizer is chasing Monte Carlo noise rather than the true likelihood surface. The correct approach — replicated pfilter calls aggregated with `logmeanexp` — is absent. This is Error 1.1 (averaging on the wrong scale) and Error 1.4 (ignoring Monte Carlo variability) from the course weakness reference. Without controlling for Monte Carlo noise, the parameter estimates reported by DEoptim are unreliable.

### 4. No convergence diagnostics for the optimization (CC-Yes)

No trace plots or other diagnostics demonstrating that the optimization converged are shown. The course standard (mif2 or any alternative) requires at minimum a plot of log-likelihood across iterations and evidence from multiple searches starting at different initial values that similar terminal likelihoods are achieved. Here, not only are no such diagnostics shown, but the reported iteration-level values are admitted to be fabricated. This is Error 1.8 from the course weakness reference. Without convergence evidence, reported parameter estimates have no statistical foundation.

### 5. DEoptim applied to stochastic particle filter likelihood without justification

The course standard for POMP parameter estimation is mif2 (iterated filtering), which is designed to handle the stochastic nature of particle filter likelihoods. DEoptim treats the objective function as deterministic. Running a global stochastic optimizer against a noisy likelihood evaluator without any variance reduction (replicated pfilter + logmeanexp) or smoothing is methodologically unsound: the optimizer may converge to regions of parameter space where Monte Carlo noise happens to produce a favorable-looking objective value, not the true MLE. The choice of DEoptim over mif2 is not justified in the text beyond a general description of DEoptim's properties.

### 6. No benchmark comparison (CC-Yes)

The project reports only the POMP model log-likelihood (which is in any case fabricated) with no comparison to any non-mechanistic benchmark. An ARMA model or even an IID (negative binomial) model fit to the same data would indicate whether the mechanistic structure adds explanatory power beyond a simpler statistical model. This omission is Error 1.6 from the course weakness reference and POMP checklist item #2 (Wheeler et al. 2024). Without a benchmark, there is no objective basis for the claim that the model "captured transits and noise well."

### 7. No profile likelihoods — parameter identifiability unassessed (CC-Yes)

No profile likelihoods are computed for any of the seven model parameters. For a model with parameters as potentially collinear as transit depth, duration, and period — all affecting the shape of the same periodic dip — identifiability is a genuine concern. The course standard requires profile likelihood plots, computed via mif2 at a grid of target parameter values, to assess whether each parameter is estimable from the data and to produce valid confidence intervals. The absence of any identifiability analysis is Error 1.9 (too few profile points) in the degenerate case of zero profile points. POMP checklist item #5 (Wheeler et al. 2024) flags this as a threat to the validity of all reported point estimates.

### 8. Residual analysis computed from ad hoc single OU simulation, not particle filter

The `compute_flux_pred()` function (used to generate residuals and all downstream diagnostic plots) simulates a single OU trajectory in R at the estimated parameter values and adds it to the transit model. This is a one-off forward simulation from initial conditions, not the particle filter filtering distribution. The filtering distribution conditions on all observed data and is the appropriate basis for residual diagnostics. A single OU realization is stochastic; a different call would produce different residuals and potentially a different ACF. Claims that residuals show "no significant autocorrelation" and "approximate a normal distribution" based on a single realization of a stochastic OU process are not statistically meaningful. This corresponds to POMP checklist item #4 (model diagnostics) and the simulation study checklist's requirement to distinguish filtering-distribution simulations from unconditioned forward projections.

### 9. Hard-coded absolute paths to author's local filesystem prevent reproducibility

The setup chunk reads data from hard-coded paths: `/home/ppratik/ondemand/TCE.csv`, `/home/ppratik/ondemand/KOI.csv`, `/home/ppratik/ondemand/false_positive.csv`, and `/home/ppratik/ondemand/Statistics.csv`. These paths are specific to the author's machine and will fail for any other user. The data files are present in the project repository, but the code does not use relative paths to access them. This is a red flag identified in the code supplement checklist: hard-coded paths to the author's local filesystem prevent reproduction even when the data are technically available.

---

## Minor Issues

### 10. Internal contradictions in reported parameter estimates

The paper contains irreconcilable inconsistencies in its own reported values. In the Results section, the orbital period is stated as P_1 = 11.20 days, but the Conclusion says "an estimated orbital period of approximately 32 days" and the earlier summary refers to a "long-period exoplanet." Similarly, the estimated p_1 is listed as 0.462 in the Results but described as "approximately 0.07" in the Visual Validation section. These are not rounding differences; they are wholesale contradictions. They suggest that different versions of the results were copy-pasted from different runs without reconciliation.

### 11. OU step hardcodes time step to 1.0 regardless of pomp's delta.t

The `ou_step` C snippet sets `double delta_t = 1.0;` with the comment "Renamed from dt to avoid conflict." This bypasses the `dt` variable that pomp's Euler integrator provides to each C snippet. With `euler(ou_step, delta.t = 1)`, the match is coincidental for the nominal case, but if the time series has irregular spacing (which it does — quality filtering removes observations), the actual gaps between consecutive valid observations differ from 1.0. The hardcoded value of 1.0 silently ignores these gaps, producing an incorrect discretization of the OU process for non-unit intervals.

### 12. Scaling factor p_1 misidentified as a detection probability

The paper repeatedly describes p_1 as "the probability of the transit being a true exoplanet signal" (Results) and as "reflecting the probability of the transit being a true exoplanet signal" (Interpretation). In the model specification, p_1 is a scaling factor on the transit depth: `flux_pred -= p_1 * delta_1`. A multiplicative scale applied to transit depth in a deterministic boxcar model has no probabilistic interpretation as a false-positive rate. The false positive probability would need to come from a separate statistical classifier or a hierarchical model, not from the transit depth scale. This misinterpretation affects the discussion of bar plot Figure 3 and the claim about "moderate probability indicating a plausible exoplanet signal."

### 13. Residuals plotted in yellow on white background (readability failure)

The `residuals_plot` chunk specifies `col = "yellow"` for the residuals line plotted against a white background. Yellow on white is not visible in a standard PDF or HTML rendering. The plot is referenced in the discussion ("The residuals plot displays the differences between the observed flux and the predicted flux") but is effectively unreadable. An earlier residuals plot uses `col = "blue"` with the same data; the yellow plot appears to be an unremediated duplicate with a color choice that makes it uninterpretable.

### 14. Writing quality: colloquial language, typos, and unrevised placeholder text

Beyond the admitted fabricated values, the manuscript contains pervasive informal language inconsistent with scientific writing: "super important," "fantastic at," "cud better capture" (cud = could), "bi" (= by), "frum" (= from), "dorm" (= dnorm in the text description), "starlite" (= starlight), "lite curves" (= light curves). The Introduction uses phrases like "tons of light curve data." These are not minor typos; they suggest the document was submitted without proofreading. Additionally, the Model Specification section begins with "your implementation" and "your specific model" — addressing the reader as if this is a tutorial written for someone else, not the authors' own work.

### 15. No information on cluster environment or total computational cost

The paper mentions using 36 cores for parallel computation but provides no information about the cluster environment, walltime, or total CPU-hours expended. For reproducibility, the code supplement checklist (POMP-specific items) requires that cluster job specifications and total computational cost be documented so readers can assess feasibility. The `makeCluster(36)` call also specifies 36 cores while the text says "running DEoptim using 36 cores" — but also says "set up parallel computing with 11 cores" in the commented setup description, another internal inconsistency.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project13/TCE.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project13/KOI.csv`
