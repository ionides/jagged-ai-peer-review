# Peer Review: W25 Project 01
## "Unveiling the Dynamics of Influenza in the Great Lakes Region"

---

## Summary

This project models weekly influenza-like illness (ILI) counts in HHS Region 5 (Great Lakes) from 2015 to 2024 using a SEIRS-based POMP framework augmented with seasonal transmission, vaccine effects, COVID-19 suppression, and antigenic drift modeled as Brownian motion. The authors compare their mechanistic model against a regression-with-SARMA-errors baseline. The project's strengths include an ambitious scope (covering three distinct epidemic phases), thorough biological motivation for parameter ranges, and honest acknowledgment of model limitations. However, the mechanistic model is undermined by a critical accumulator bug that corrupts weekly incidence tracking, severe parameter non-identifiability with biologically implausible estimates, absence of proper convergence diagnostics, insufficient profile likelihood analysis (only one parameter profiled, using a non-standard approach), and no effective sample size (ESS) monitoring. These issues are serious enough to cast doubt on the quantitative conclusions and parameter interpretations.

---

## Major Issues

### 1. Double-Reset Bug in the Accumulator Variable H

The Csnippet for the extended SEIRS model (blinded.Rmd, around line 1000) contains a manual reset:

```c
if (fabs(fmod(t, 1.0)) < 1e-8) {
  H = 0;
}
```

This resets H to zero whenever `t` is an integer — that is, at the start of every observation interval. With `delta.t = 1/7`, the Euler sub-steps run through `t, t+1/7, t+2/7, ..., t+6/7`. The condition fires at `t = 1, 2, 3, ...`, zeroing H at sub-step 0 (the very first sub-step of each weekly period) immediately after `H += dN_EI` would have accumulated the first 1/7 of that week's incidence. Then `accumvars = "H"` performs its own reset after measurement. The double-reset means that approximately 1/7 of weekly incidence is systematically dropped on each sub-step where `t` is integer, and the interaction between the Csnippet reset and the `accumvars` mechanism is not clearly defined. This is a concrete reproducibility and validity failure analogous to the measurement model discrepancy documented in Wheeler et al. (2024) as a cautionary example. The authors should remove the manual reset and rely solely on `accumvars`, which is the standard pomp mechanism for accumulator variables.

### 2. Biologically Implausible Parameter Estimates and Identifiability Failure

Multiple parameter estimates are biologically implausible throughout the analysis. The basic SEIRS global search produces `mu_IR = 23.9` (recovery in 7 hours), which the authors themselves call "utterly ridiculous." In the extended model, `gamma = 6.9526` implies that immunity wanes in approximately 19 days under moderate antigenic drift and only 10 days under stronger drift — which the authors acknowledge contradicts empirical knowledge (blinded.Rmd, lines 1347–1370). The estimated `rho = 0.004213444` (0.4% reporting rate) is an order of magnitude below the lower bound of estimates the authors themselves calculate (1%–23%). These are not merely borderline values; they suggest systematic model misspecification rather than genuine biological findings. Wheeler et al. (2024) warn explicitly that "implausible parameter estimates flagged as potential signs of model misspecification" (Wheeler et al., §Identifiability and uncertainty). The authors partially acknowledge this but frame it as a tractable issue that will be left to future work rather than addressing it as evidence of fundamental model failure.

### 3. No Effective Sample Size Monitoring or Particle Filter Diagnostics

No ESS traces are presented for any particle filter run. With a complex 17-parameter model including Brownian motion state components, particle filter degeneracy is a serious risk. Without ESS monitoring, there is no way to determine whether the reported log-likelihoods are reliable estimates of the true likelihood or artifacts of particle collapse. The simulation-based validation checklist (Morris et al. 2019; Wheeler et al. 2024, §Computational adequacy) requires that ESS be monitored during filtering and that persistent ESS collapse be flagged as evidence of model-data mismatch or insufficient particles. The authors use Np = 2000 for mif2 runs and Np = 5000 for likelihood evaluation, but without ESS traces, it is unclear whether these particle counts are sufficient for the extended model with 7 continuous state variables.

### 4. Incomplete Profile Likelihood — Only One Parameter, Non-Standard Construction

Profile likelihoods are computed only for `rho` (and a "poor man's profile" for `alpha` and `gamma`). The "poor man's profile" approach, which fixes the profiled parameter while keeping all others at their MLE values without re-optimization, does not constitute a valid profile likelihood. The authors acknowledge this limitation themselves (blinded.Rmd, line 1493: "this approach does not re-optimize other parameters at each rho, and therefore may misrepresent the true likelihood surface"). The true profile over `rho` (blinded.Rmd, lines 1573–1635) uses only 5 mif2 replicates per fixed `rho` value across 30 grid points with Nmif = 100 + 100 — this is likely insufficient to find the constrained MLE reliably. No profile likelihoods are computed for `Beta0`, `Beta1`, `mu_IR`, `mu_RS`, or `alpha` using a proper profile design. Wheeler et al. (2024, §Identifiability) require profile likelihoods for key parameters to assess identifiability, and the failure to compute them means the confidence intervals reported for `rho` cannot be trusted.

### 5. Convergence Not Established — Log-Likelihood Thresholds Are Arbitrary

The global search pair plots are presented with a filter of `loglik > max - 2000` or `max - 500`, which is an extremely wide window that includes near-random starting values and is not informative about convergence. In legitimate POMP analyses (Wheeler et al. 2024, §Computational adequacy), convergence is established by showing that multiple independent random starting points converge to the same likelihood region (typically within 10–20 log-likelihood units of the maximum). The authors use `nseq = 200` starting points with Nmif = 50 + 50 iterations — the number of iterations is modest for a 17-parameter model with Brownian motion components. There is no evidence that the reported maximum log-likelihood is near the true MLE.

### 6. Measurement Model Inconsistency: H Accumulates dN_EI, Not Reported Cases

The authors state that H tracks "incident symptomatic cases, consistent with ILI report definitions" and accumulate H via `H += dN_EI` (transitions from E to I). However, `dN_EI` counts newly infectious individuals, not reported symptomatic cases. ILI surveillance captures individuals who seek medical care with influenza-like symptoms — this is a subset of the infectious population, typically represented by a fraction `rho` of the I compartment (or `dN_IR`, those recovering from acute illness), not by E-to-I transitions. The measurement model `dmeas = dnbinom_mu(reports, k, rho * H)` then multiplies by the reporting rate `rho`. This misalignment between the biological meaning of the accumulator and the observation process creates a structural mismatch analogous to the measurement model discrepancies documented in Wheeler et al. (2024).

### 7. Benchmark Comparison Is Flawed Due to Scale Incompatibility

The authors correctly note (blinded.Rmd, lines 308–323) that the SARMA model is fitted to raw (untransformed) data to allow likelihood comparison with the POMP model. However, the SARMA model fitted to non-log-transformed count data has heavy-tailed, non-normal residuals (confirmed by the authors' own Q-Q plot), and the log-likelihood of an ARIMA model fitted to raw counts is not on the same footing as the log-likelihood of a POMP model with a negative-binomial measurement model. Specifically, the ARIMA model implicitly assumes Gaussian errors, producing a likelihood on a different probability scale. The comparison of `logLik = -3620.72` (SARMA) vs. `logLik = -3622.88` (SEIRS) is not meaningful because the two models define probability density over the data using different base measures. A valid benchmark would use a non-mechanistic time-series model with the same negative-binomial observation model (e.g., auto-regressive negative binomial, as recommended by Wheeler et al. 2024, §Benchmark comparison).

### 8. COVID Suppression End Date: Internal Inconsistency

The text of blinded.Rmd (line 694) states that `t_end = 333` corresponds to "the week of 05-17-2021, when most states in HHS region 5 lifted mask mandates." However, `seirs_beta.R` (line 49) documents the same constant as "Week of 2023-05-08, Public Health Emergency for COVID-19... expires at the end of 2023-05-11" — a full two years later. Furthermore, the comment in seirs_beta.R (line 54) uses a third end time: "returned to baseline by week 436." These three inconsistent justifications for the same parameter value (333) indicate confusion about the temporal anchor of the analysis and undermine the credibility of the hardcoded suppression endpoint. The suppression model is presented as a key feature, but neither the chosen endpoint nor the logistic ramp parameters (r1 = 0.15, r2 = 0.25) are estimated from the data — they are fixed based on inconsistently-documented reasoning.

---

## Minor Issues

### 9. Duplicate Parameter in `rw_sd_profile` (Code Bug)

In the profile likelihood code (blinded.Rmd, lines 1600–1611), `gamma` appears twice in `rw_sd(...)`:

```r
rw_sd_profile <- rw_sd(
  rho = 0,
  mu_RS = 0.005,
  gamma = 0.01,       # first occurrence
  Beta0 = 0.01, Beta1 = 0.01,
  mu_EI = 0.01, mu_IR = 0.01,
  eta = 0.00005,
  alpha = 0.01, gamma = 0.01,   # second occurrence
  ...
)
```

In R, duplicate named arguments in a function call typically cause an error or silently use the last value. This may invalidate the profile results or cause an unreported error. The authors should verify this code ran without error and remove the duplicate.

### 10. Data Inconsistency: `data$ILITOTA` vs. `data$ILITOTAL`

At blinded.Rmd line 377, the SARMA model is fitted as `arima(data$ILITOTA, ...)` — missing the final `L` from `ILITOTAL`. This is a potential silent error that would cause the model to fit on an unexpected column or return an error. The `.rds` file is cached so this typo may not have been caught at runtime, but it introduces reproducibility doubt about whether the fitted model in the cached file actually uses the intended data column.

### 11. No Seed or Computational Budget Reported for Global Searches (Main Results)

The global searches in the Rmd are loaded from cached `.rds` files with no documentation of how many particles, iterations, or starting points were used in producing those files. The `seirs_beta.R` file provides some of this information for the final search, but the intermediate global searches (e.g., `bvgcseirs_global_search1.rds`, `bvgcseirs_global_search2.rds`, `bvgcseirs_global_search3.rds`) lack corresponding documentation in the Rmd. Wheeler et al. (2024, §Computational adequacy) require that computational effort be reported.

### 12. Profile Likelihood Range for `rho` Does Not Bracket the MLE

The profile likelihood for `rho` is computed over the range `[0.02, 0.04]` (blinded.Rmd, line 1588), but the authors report their MLE at `rho ≈ 0.004213444` — roughly 5 times outside the lower bound of the profiled range. The profile therefore does not bracket the true maximum, and the resulting 95% CI cannot be valid. The authors acknowledge the discrepancy (observing the poor man's profile maximizes at its lower bound, line 1493), but the true profile is computed on the wrong range. The computed CI of rho is therefore unreliable.

### 13. `eta` Non-Identifiability Not Adequately Addressed

The authors note that `eta` (initial infected fraction) is non-identifiable across both the basic SEIRS and extended models. For identifiable parameters, non-identifiability of `eta` inflates log-likelihood uncertainty and may compromise estimates of correlated parameters. The authors treat this as a known limitation but do not fix `eta` to a principled value, offer a sensitivity analysis, or discuss how uncertainty in `eta` propagates to conclusions about `Beta0`, `rho`, or `mu_RS`.

### 14. Posterior Predictive Check Conflates Forward Simulation with Model Validation

The "posterior predictive check" (blinded.Rmd, lines 1517–1565 and 1685–1726) simulates trajectories from the estimated MLE parameters using `simulate()`. This produces forward simulations from estimated initial conditions, not from the filtering distribution conditioned on observed data. As noted in Wheeler et al. (2024, §Forecast methodology), forward simulation and filtering-distribution simulation serve different diagnostic purposes and should not be conflated. The relevant diagnostic for model fit is a comparison of simulations conditioned on all observed data (via `pfilter()`), not forward simulations from a fixed parameter vector, which will show much greater uncertainty.

### 15. ChatGPT Used to Generate Parameter Interpretation Table and Code

The authors explicitly state that ChatGPT was used to "create the following table" (blinded.Rmd, line 1263) of parameter interpretations, and to "help preparing the above plot" (line 1335). Using a language model to interpret biological plausibility of parameter estimates is methodologically unreliable — a language model cannot perform quantitative validation and may hallucinate or mischaracterize biological ranges. These judgments should rely on primary literature and the authors' own quantitative calculations, not on an AI-generated table. The authors do cite primary literature elsewhere and perform some calculations independently, but the direct outsourcing of biological interpretation to ChatGPT undermines the credibility of the parameter assessment.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project01/seirs_beta.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project01/ilitotal2015.csv`
