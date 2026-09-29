# Final AI Review
## Project: final_project_w25 / project10
## Title: Daily Environmental Noise and Heart-Rate Variability

---

## Overall Assessment

This project tackles a scientifically motivated question — whether daily environmental noise suppresses heart-rate variability at the population level — using a well-structured analysis that progresses from exploratory plots through ARIMA benchmarks to a linear-Gaussian POMP model. The author demonstrates genuine methodological competence: the MIF2 workflow is correctly implemented, logmeanexp is properly used for Monte Carlo likelihood aggregation, trace plots are shown and interpreted with care, and the paper honestly reports that the POMP model underperforms its benchmarks. These are genuine strengths. However, the paper has three interconnected problems that prevent the central quantitative claim (b ≈ -0.30 ms/dB of noise) from being credible in its current form: no uncertainty quantification for the key parameter, a benchmark comparison that conflates likelihoods from different data objects, and an unexplained discrepancy in the global search output that leaves the reported MLE in doubt. Addressing these three issues would substantially strengthen the conclusions.

---

## Key Strengths

**S1 — Correct MC likelihood aggregation.**
The replicated particle filter approach using logmeanexp is implemented correctly throughout the local search likelihood evaluation. This is a methodologically important detail that many students miss.

**S2 — Honest negative result reporting.**
The author explicitly acknowledges that the POMP model achieves a substantially worse log-likelihood than the ARIMA benchmark and discusses plausible reasons rather than dismissing the discrepancy. This scientific integrity is commendable.

**S3 — Thorough local search.**
The local search uses 48 independent MIF2 chains with Np=5000 particles and Nmif=300 iterations, followed by 48 replicate pfilter evaluations per chain. This is a well-designed and computationally serious search.

**S4 — Convergence diagnostics presented and interpreted.**
Trace plots are shown for all parameters and discussed substantively, including the important observation that b converges robustly while a, sigma_proc, and sigma_obs show problematic behavior.

---

## Major Points

**C1 — No profile likelihood or confidence interval for the noise coefficient b.**
ID: 25.10.C1. The paper's central scientific claim is that a one-decibel increase in daily mean noise reduces population-level SDNN by approximately 0.3 ms. This claim rests entirely on the point estimate b ≈ -0.30 from the trace plots. No profile likelihood is computed and no confidence interval is reported. Given that the author explicitly notes the log-likelihood has not fully converged, the precision of this estimate is unknown. Without uncertainty quantification, the quantitative claim cannot be assessed.
Severity: Major.
Suggested action: Compute a profile likelihood for b over a grid (e.g., -0.5 to -0.1 in steps of 0.02), re-optimizing over the remaining parameters at each grid point, and report the 95% MCAP confidence interval.

**C2 — Benchmark comparison is between incommensurable likelihoods.**
ID: 25.10.C2. The ARIMA model is fit to `d_sdnn_ts` (1,874 first-differenced observations) using `arima(d_sdnn_ts, order=c(5,0,6))`, yielding log-likelihood -2591. The POMP model is fit to `sdnn` (1,875 level observations), yielding log-likelihood -3235. These are likelihoods for different response variables (differences vs. levels) and cannot be compared directly to conclude that "the POMP achieves a markedly worse fit." The comparison as presented overstates the evidence against the POMP model.
Severity: Major.
Suggested action: Refit the ARIMA benchmark to the level series — `arima(sdnn_ts, order=c(5,1,6))` — which internally differences the data and returns a likelihood on the same 1,875-observation level series as the POMP model. This produces a directly comparable benchmark.

**C3 — Global search discrepancy is unexplained and undermines the reported MLE.**
ID: 25.10.C3. The global search output displays a best log-likelihood of -7936, while the manuscript text claims -5244. Neither value approaches the local search optimum of -3235. The explanation offered (insufficient iterations, active perturbations at final step) is plausible but insufficient: with 96 chains from diverse starting points, at least some should have found the -3235 neighborhood if it is the true mode. Inspection of the code reveals that the global search fixes X_0=34 while the local search estimates X_0 — this asymmetry likely contributes to the gap but is not discussed. The discrepancy between the displayed and claimed global values is not explained at all.
Severity: Major.
Suggested action: (1) Reconcile the -5244 vs. -7936 discrepancy (likely a caching or seed issue). (2) Add X_0 to the global search's random starting box, consistent with the local search. (3) Present a histogram of all global chain log-likelihoods to show the distribution of terminal values.

**M1 — Ecological fallacy risk from population-level pooling.**
ID: 25.10.M1. The paper's central scientific claim concerns the mechanism by which noise suppresses HRV. The analysis is conducted on a pooled daily median (population-level aggregate), meaning the estimated noise coefficient b reflects the cross-day association between population-average noise and population-average SDNN. This association need not correspond to any individual's noise–HRV response function — it could be driven by confounders that vary at the population level (e.g., seasonal patterns, pandemic-related behavior changes) rather than a physiological noise effect. The pooling rationale is given (individual series are irregular), but the epidemiological limitations of drawing causal inference from a pooled aggregate are not acknowledged.
Severity: Major.
Suggested action: Add a paragraph in the discussion acknowledging that the pooled estimate conflates within-person and between-person variation and that causal interpretation requires individual-level analysis or a mixed-effects model. Qualify the noise coefficient interpretation accordingly.

---

## Minor Points

**C4 — Differencing not justified by formal test.**
The ARIMA analysis applies first-order differencing based on visual inspection of Figure 1 (observed descending trend). No unit-root test (ADF, KPSS) is reported. A slow secular decline in SDNN as the cohort ages could be better modeled with a deterministic trend than with differencing, and the choice affects the ARIMA benchmark structure.
Severity: Minor. Suggested action: Report an ADF or KPSS test result; justify the differencing decision.

**C5 — No ESS monitoring; near-zero sigma_proc suggests potential filter degeneracy.**
With sigma_proc converging to values near zero, the latent process becomes nearly deterministic and particle diversity collapses rapidly. This regime is where particle filter degeneracy is most likely. No ESS plots are shown to confirm the filter is functioning adequately.
Severity: Minor. Suggested action: Add ESS time series from representative pfilter runs; note if ESS falls below Np/10 at any time step.

**C6 — No simulation-based model check at MLE.**
Figure 3 shows forward simulations from the initial-guess parameters, not the MLE. A corresponding figure using the MLE parameter vector would allow visual assessment of whether the fitted model reproduces the observed SDNN dynamics.
Severity: Minor. Suggested action: Re-run `simulate()` with the MLE parameter vector from the local search and overlay against observed data.

**C7 — X_0 treated asymmetrically between local and global searches.**
In the local search, X_0 is estimated via `ivp(0.01)`. In the global search, `fixed_params = c(X_0=34)` fixes it. This asymmetry is not disclosed and likely explains a portion of the global–local likelihood gap.
Severity: Minor. Suggested action: Either estimate X_0 in the global search as well, or justify fixing it and note the asymmetry explicitly.

**C8 — AIC table caption is mislabeled.**
The caption reads "AIC of ARIMA(p,1,q)" but the models are ARMA(p,0,q) fitted to the already-differenced series `d_sdnn_ts`.
Severity: Minor. Suggested action: Correct the caption to "AIC of ARMA(p,q) fitted to first-differenced SDNN series."
