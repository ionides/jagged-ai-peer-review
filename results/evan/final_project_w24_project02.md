# Final AI Review: Investigating the Alternative Prey Hypothesis with the POMP Framework
# STATS 531 W24, Project 02

---

## Overall Assessment

This project applies the POMP framework to 142 years of willow ptarmigan harvest data from Norway, motivated by the ecologically interesting alternative prey hypothesis — the idea that fox predation on ptarmigan intensifies when rodents are scarce. The scientific motivation is strong, the literature review is solid, and the Lotka–Volterra model structure is sensibly adapted to the problem. The project also completes the full pipeline: exploratory data analysis, an ARIMA baseline, local search with IF2, and a Great Lakes global search with diagnostic plots.

However, the project has several foundational methodological problems that undermine the reliability of all numerical conclusions. First, the primary quantitative claim — that ARIMA outperforms the POMP model in log-likelihood — rests on an invalid comparison: the ARIMA model is fit to the first-differenced log CPUE series while the POMP model is fit to the undifferenced series, so their log-likelihoods are not comparable. Second, the reported log-likelihoods from the POMP model appear to come from mif2 internal estimates or unreplicated pfilter evaluations rather than from replicated independent pfilter runs; the single pfilter output shown has a standard error of ~31 log units, which renders the estimate meaningless for comparison. Third, the global search produced a worse result (-176.3) than the local search (-134), a clear diagnostic of a computational problem that is left unresolved. Finally, no profile likelihoods or confidence intervals are reported, and the scatter plot matrix clearly shows the model parameters are non-identifiable in the current setup. These issues collectively mean the paper's conclusions cannot be trusted as stated. The project is a creditable early attempt that needs significant revision to its inference methodology.

---

## Key Strengths

- **Ecological motivation and literature review (24.02 — strength):** The alternative prey hypothesis is well-motivated through primary sources, and the model structure directly encodes the mechanistic hypothesis via the gamma parameter in the predation term. The data set (142 years of CPUE with peak rodent year covariate) is well-suited to the question.

- **Complete POMP pipeline (24.02 — strength):** The project implements rprocess, rmeasure, dmeasure, and rinit Csnippets correctly in the pomp framework; runs a local search with IF2 and a global search on Great Lakes; and produces ESS and conditional log-likelihood diagnostic plots. This demonstrates fluency with the computational framework.

- **Diagnostic awareness (24.02 — strength):** The authors correctly identify particle degeneracy in the ESS plot and acknowledge that some parameters do not converge, showing appropriate diagnostic self-awareness.

---

## Major Points

**Point 24.02.1 — Invalid ARIMA vs POMP log-likelihood comparison**
*Why it matters:* The primary empirical conclusion of the paper — that ARIMA outperforms the POMP model — is based on comparing log-likelihoods computed on different data transformations. ARIMA(0,1,5) is fit to the first-differenced log CPUE series (log-lik = -99.32); the POMP model is fit to the raw log CPUE series. These numbers cannot be ranked. The conclusion in Section 3.2.2 ("the log-likelihood produced an ARIMA(0,1,5) model is better") is therefore unsupported.
*Severity:* Major
*Suggested action:* To make the comparison valid, either (a) fit a non-differenced ARIMA or ARMA+trend model to the original log CPUE series and compare its log-likelihood to the POMP model's log-likelihood directly, or (b) acknowledge explicitly that the two likelihoods are on different scales, state that direct comparison is not valid, and interpret the relative performance cautiously.

**Point 24.02.2 — mif2 likelihoods reported without replicated pfilter**
*Why it matters:* The log-likelihoods of -205, -134, and -176.3 are presented as estimates of the model's fit quality, but the shown output (`est: -288.64, se: 30.88`) reveals that these likely come from unreplicated single pfilter calls or mif2 internal estimates. A standard error of ~31 log units means the 95% confidence interval on the likelihood estimate spans ~60 log units — completely uninformative. Likelihood comparisons with such noise are meaningless.
*Severity:* Major
*Suggested action:* After each optimization run, evaluate the log-likelihood by running at least 10 independent pfilter replicates at the converged parameter vector, then report the mean +/- SE using logmeanexp to aggregate. Only these replicated estimates are reliable for model comparison.

**Point 24.02.4 — Convergence inadequately demonstrated**
*Why it matters:* The trace plots in Figure 3.2 span only 20 mif2 iterations, and the paper explicitly acknowledges that several parameters (log(B_0), sigma_F) do not converge. Parameters a, b, c, sigma_F, sigma_B remain near zero with occasional large spikes, suggesting boundary artifacts. The global search being worse than the local search is a clear sign that the optimization is not functioning correctly. Without convergence, no parameter estimate is trustworthy.
*Severity:* Major
*Suggested action:* Increase mif2 iterations to at least 50–100 with geometric cooling. Run multiple chains from diverse starting points (ideally drawn from a Latin hypercube over the parameter space). Overlay all chains in a single trace plot. Investigate why the global search underperforms the local search — check whether the parameter box is over-constrained or whether the best run is not being correctly identified.

**Point 24.02.3 — No profile likelihoods or confidence intervals**
*Why it matters:* The scatter plot matrix (Figure 3.3) shows diffuse, structureless clouds across all parameter pairs, indicating the model's parameters are not identifiable from this data with the current level of computation. The paper draws no conclusions about the biological parameter values, but also provides no quantification of uncertainty. Without profile likelihoods, it is impossible to know whether gamma (the key alternative prey parameter) is even estimable.
*Severity:* Major
*Suggested action:* Compute 1D profile likelihoods over a grid for at least gamma and Beta. Even a coarse profile (5–10 points at run_level=2) would reveal whether there is a likelihood maximum and whether the parameter is identifiable. Report approximate confidence intervals using MCAP.

**Point 24.02.5 — Global search worse than local search**
*Why it matters:* A global search is designed to explore a broad parameter space and find the global optimum. If it returns a worse solution than the local search, the global search is broken. The explanation offered (limited parameter space to save time) implies the search box was too narrow, but this would only affect coverage — it should not produce a worse result unless the search was miscoded or the likelihoods were evaluated differently.
*Severity:* Major
*Suggested action:* Diagnose whether the issue is (a) the parameter box boundaries cutting off the region found by the local search, (b) a difference in how likelihoods were evaluated (mif2 internal vs pfilter), or (c) a code error. Report the parameter box used in the global search. After fixing the comparison (24.02.2), re-run and confirm the global search finds a result at least as good as the local search.

---

## Minor Points

**Point 24.02.6 — Measurement model noise structure and logRho scale**
*Why it matters:* Eq. (3.2) uses a single gamma white noise draw (dwB) to scale both the positive birth term (alpha) and the negative predation term, coupling demographic growth and mortality noise into a single random variable. This is biologically unusual. Additionally, logRho is initialized at 3 (implying rho ~ 20), creating a large downward shift in the measurement model mean; the biological interpretation and estimation status of this parameter are not discussed.
*Severity:* Minor
*Suggested action:* Either justify the shared noise structure or use separate noise terms for birth and predation. Add a brief explanation of what rho represents (e.g., harvest efficiency) and whether it is estimated during inference.

**Point 24.02.7 — Inconsistent notation**
Notation alternates between "log.CPUE" and "logCPUE" throughout the manuscript. Standardize to one convention.

**Point 24.02.8 — Figure caption error**
Figure 2.4 is labeled "ACF of logCPUE" but displays the PACF. Fix the caption.

**Point 24.02.11 — ARIMA residuals not validated**
No residual ACF or diagnostic plot is shown for the selected ARIMA(0,1,5) model. At minimum, a residual ACF confirming white noise residuals should be included to validate the baseline model.

**Point 24.02.13 — No parameter estimate table**
The best-found parameter values from the local and/or global search should be tabulated. Readers cannot assess biological plausibility without the actual estimates.

**Point 24.02.15 — AIC table inconsistency**
The text states the selected model is ARMA(0,5) with AIC 204.48, but Table 3.1 shows 204.21 for that cell. Clarify which value is correct and complete the truncated AR4 row.
