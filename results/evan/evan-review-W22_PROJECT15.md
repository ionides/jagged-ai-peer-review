# Final AI Review — w22 Project 15

## Overall Assessment

This project applies SEIR compartmental models to weekly sequenced COVID-19 case counts for the Delta and Omicron variants in the US (Jan. 2021–Mar. 2022). The authors use iterated filtering (IF2) with local and global search strategies and compute profile likelihoods for the transmission rate β to compare the two variants. The scientific question is well-motivated and the modeling approach is appropriate in outline. However, the execution has several important methodological gaps: log-likelihoods are reported from mif2 runs without replicated particle filter evaluation, leaving all likelihood comparisons subject to unquantified Monte Carlo error; the observation model is never specified; there is a clear internal inconsistency in the Delta β profile (the 95% CI does not contain the global MLE); and no non-mechanistic benchmark is provided. The simulation envelopes are extremely wide relative to the data, and biologically implausible recovery-rate estimates (particularly for Delta) are not scrutinized. The paper is a promising first attempt but requires substantial methodological revision to support its central claims.

## Key Strengths

- **Dual-variant comparison design.** Fitting separate SEIR models to Delta and Omicron and comparing parameter estimates is a sensible approach for characterizing variant-specific dynamics.
- **Profile likelihood for β.** Computing profile likelihoods for the key parameter β for both variants is the right tool for quantitative comparison, and the result clearly shows Omicron β exceeds Delta β.
- **Convergence diagnostics provided.** Trace plots (figs 003, 006) and global-search pair plots (figs 004, 007) are shown for both variants, enabling assessment of optimizer behavior.
- **Literature corroboration.** Parameter estimates are qualitatively compared to external references (incubation period, spread rate), grounding the model in external scientific evidence.

## Major Points

**22.15.1 — Likelihoods not properly evaluated via replicated pfilter**
The reported log-likelihoods (−753.17 for Delta, −252.56 for Omicron) appear to come directly from mif2 internal evaluations rather than from replicated independent particle filter runs. A single particle filter evaluation carries substantial Monte Carlo variance (potentially tens of log-likelihood units), making all comparisons — local vs. global, Delta vs. Omicron — unreliable. The comparison "likelihood of model from global search is much higher than the likelihood of model from local search" (Delta: −753 vs. −919) is large enough to survive this, but the within-global comparisons and the variant-to-variant comparison on different scales are not.
Severity: Major
Suggested action: At each candidate parameter vector (local MLE, global MLE, profile grid points), report the log-mean-exp of at least 10 independent pfilter runs. This is the standard procedure described in the course notes.

**22.15.2 — Profile likelihood for Delta β is internally inconsistent**
The profile likelihood for Delta β (fig_009, left) peaks near β ≈ 130 with a 95% CI of approximately [100, 150]. The global MLE from the preceding global search is β = 73.4 — well outside this interval. The authors attribute this to "high correlation between model parameters," but a profile CI is constructed to be invariant to correlations between parameters. The likely explanation is that the profile was initialized from a different starting point than the global MLE, or that the global MLE is a spurious particle-filter artifact. This inconsistency undermines the reliability of the central β comparison.
Severity: Major
Suggested action: Re-run the Delta profile starting from the global MLE parameter vector. Use replicated pfilter at each profile point to reduce MC noise. If the inconsistency persists, investigate whether the global MLE survives replication.

**22.15.3 — Observation model not specified**
The Methods section describes the latent SEIR transitions and parameters but never names the observation distribution. It is unclear whether reports ~ Poisson(ρ·I), Negative Binomial, or something else. The choice of observation model determines the variance structure and directly affects the likelihoods reported throughout the paper.
Severity: Major
Suggested action: State the observation distribution explicitly in the Methods, including how overdispersion (if any) is parameterized.

**22.15.4 — No non-mechanistic benchmark comparison**
No ARMA or other time-series benchmark is presented. Without at least one comparison to a non-mechanistic model, it is not possible to assess whether the SEIR structure is adding explanatory value beyond a simple data description.
Severity: Major
Suggested action: Fit an ARIMA or similar model to the same weekly counts and report the log-likelihood for comparison.

**22.15.5 — Biologically implausible recovery rate for Delta**
The global MLE for Delta yields μ_IR = 5.464 per week, implying a mean infectious period of approximately 1.8 days (0.26 weeks). The standard estimate for the COVID infectious period is 5–10 days. This value is not flagged or discussed in the paper. Combined with the profile inconsistency (M2), this suggests the Delta fit may be at a spurious local optimum.
Severity: Major
Suggested action: Compare estimated μ_IR values to published estimates of the Delta infectious period. If the estimate is implausible, investigate whether the model is misspecified (e.g., the μ_IR and β are confounded) and report the result transparently.

## Minor Points

- **22.15.6 — ESS not monitored.** No effective sample size (ESS) diagnostic is reported for either dataset. ESS monitoring is a standard check for particle filter degeneracy.
  Severity: Minor. Suggested action: Add ESS plots or a table of median ESS values alongside the trace plots.

- **22.15.7 — Number of particles and global search iterations not reported.** The local search uses 100 mif2 iterations (mentioned in text) but the particle count Np and the global search iteration count are not stated. These are necessary for reproducibility and assessment of computational adequacy.
  Severity: Minor. Suggested action: Report Np and Nmif explicitly for both local and global search stages.

- **22.15.8 — Forward simulation envelopes not distinguished from filtering distribution.** Figs 005 and 008 show extremely wide simulation envelopes generated from the MLE parameters. These appear to be unconditional forward simulations, not simulations conditioned on observed data. The paper would benefit from stating this distinction and, ideally, showing filtered (posterior-predictive) trajectories, which should be much tighter.
  Severity: Minor. Suggested action: Clarify that these are forward simulations and add a note on why the envelopes are so wide (stochastic variability in a single-wave model vs. multi-wave observed data).

- **22.15.9 — Reporting rate interpretation.** ρ = 0.1 is justified as "roughly 10% of all cases are sequenced," but ρ in the model represents the fraction of all truly infected individuals who appear in the data. This requires accounting for both the sequencing fraction and the undetected infection rate. A sentence acknowledging this compound interpretation or a brief sensitivity check would strengthen the justification.
  Severity: Minor.

- **22.15.10 — Notation and terminology.** β is labeled "Exposure rate," which is nonstandard; it is typically the transmission rate. This could cause confusion with the E→I transition rate. The SEIR diagram (fig_002) is not accompanied by the differential or difference equations.
  Severity: Minor.

- **22.15.11 — Proofreading.** The title contains "Comparsion" and the body contains several additional typos ("paremetrs," "optimzation," "causiosly," "significcant," "inapppropriate"). The manuscript would benefit from a careful proofread.
  Severity: Minor.
