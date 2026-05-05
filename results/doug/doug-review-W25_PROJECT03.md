# Peer Review: W25 Project 03 — "Flu Cases in Michigan"

## Summary

This project applies both classical time-series methods (ARMA, SARMA) and a mechanistic POMP framework (SEIRS model with seasonal transmission) to weekly influenza case counts in Michigan from 2023 to early 2025. The seasonal SEIRS model achieves a log-likelihood of approximately −376, substantially better than the ARMA/SARMA baselines (around −495). The project is clearly written and covers most standard components of a POMP analysis course project. However, it contains several methodological flaws that undermine specific conclusions: the accumulator variable tracks the wrong epidemiological flow; the profile likelihoods are computed using a single-path approach from a single starting point rather than through proper constrained optimization across multiple restarts; the direct log-likelihood comparison between ARIMA-family and POMP models is statistically invalid; and the global search relies on only 10 replicates with Nmif=50, which is likely insufficient to confirm global convergence. These issues are detailed below.

---

## Major Issues

### 1. Accumulator variable tracks recoveries rather than new infections (semantic mismatch)

The `rprocess` Csnippet accumulates `dN_IR` (transitions from I to R, i.e., recoveries) into `H`:

```
H += dN_IR;
```

The measurement model then links observed weekly flu cases to `H` via `cases ~ NegBin(rho * H, k)`. However, CDC influenza surveillance data records newly reported/confirmed cases (people who are newly diagnosed and entering the infected/symptomatic state), not recoveries. The correct flow to accumulate is `dN_EI` (transitions from E to I, representing new symptomatic cases), or optionally `dN_SE` if the data represents new infections at the point of exposure.

By accumulating recoveries, the model conflates two different epidemiological events. At the peak of an epidemic, recoveries lag infections by approximately 1/mu_IR weeks, so the temporal alignment is systematically off. The reporting-rate parameter `rho` is therefore estimated to absorb the ratio of recoveries to actual reported infections per time step, and `mu_IR` (the recovery rate) will be distorted by the optimizer to improve fit. All parameter estimates and confidence intervals derived from this model are potentially unreliable (see Wheeler et al. 2024, §Measurement model specification; pomp-accumvar-semantic-audit skill).

**Fix:** Change `H += dN_IR` to `H += dN_EI` in the `seirs_step` Csnippet, re-run all searches and profile likelihoods, and re-evaluate all reported parameter estimates.

---

### 2. Invalid direct log-likelihood comparison between ARMA/SARMA and POMP models

Section 5.1 presents a table comparing log-likelihoods: ARMA(0,1) at −497.31, SARMA(0,1)×(1,0)₅₂ at −495.40, and the SEIRS POMP model at −375.79. The paper concludes from this that "the mechanistic approach better captures the underlying epidemic process."

This comparison is statistically invalid. The ARMA and SARMA models are fitted to the **first-differenced** flu time series under a Gaussian observation model (via `arima(diff_flu_ts, ...)`). The POMP SEIRS model is fitted to the **original** (undifferenced) weekly counts under a negative binomial measurement model. These likelihoods are computed on different data transformations and under different distributional families, and their numerical values are therefore on incomparable scales. A direct comparison of these numbers does not support any claim about relative model quality.

The improvement in log-likelihood from −495 to −376 (approximately 119 units) cannot be attributed to the mechanistic model being better; it is at least partly an artifact of the different data and likelihood scales. The conclusion in Sections 5.1 and 7.1 that "the POMP model significantly outperformed" ARIMA is overstated (see sarima-baseline-audit skill).

**Fix:** Either (a) evaluate the ARMA/SARMA model on the original (undifferenced) raw counts under a comparable observation model, or (b) use a proper scoring rule (e.g., one-step-ahead CRPS on the original case count scale) that applies to both model classes. Alternatively, remove the numerical log-likelihood comparison entirely and note only qualitative differences in interpretability.

---

### 3. Profile likelihood is a single-path procedure, not a true profile likelihood

Section 6 acknowledges that the profile likelihood was computed using "a single-path profile rather than the more advanced method in Chapter 14." In practice, for each grid point the procedure runs a single `mif2()` call starting from the MLE, then evaluates with a single `pfilter()` call (no replicated likelihood evaluation). This is not a valid profile likelihood because:

- A single IF2 run from a single starting point may not find the constrained maximum at each profile grid value, especially if the likelihood surface is multi-modal or the grid point is far from the starting parameter.
- Evaluating log-likelihood with a single `pfilter()` call (rather than `logmeanexp` over multiple replicates) introduces substantial Monte Carlo noise, producing a jagged curve that cannot be reliably used for CI extraction.
- The CI cutoff `max(profile_amp$loglik) - qchisq(0.95, 1)/2` uses the profile maximum rather than the global maximum from the full search, which further biases the confidence interval.

The resulting "singleton" confidence intervals for `phase` ([2.7, 2.7]) and `rho` ([0.00015, 0.00015]) — where the CI collapses to the single grid point at the maximum — are artifacts of the high Monte Carlo noise from a single particle filter evaluation and the extremely narrow (±20% of MLE) grid for `rho`. They do not reflect genuine statistical precision.

**Fix:** Use `profile_design()` to construct a grid over the profiled parameter, run multiple IF2 restarts from diverse starting points at each grid value with the profiled parameter excluded from `rw.sd`, evaluate log-likelihood via `logmeanexp` over ≥10 `pfilter` replicates, and use the global (full-search) maximum as the reference for the chi-squared CI cutoff.

---

### 4. Global search uses only 10 replicates with Nmif=50, insufficient to confirm convergence

The global search runs 10 replicate IF2 chains (`replicate(10, {...})`) each with `Np=1000` particles and `Nmif=50` iterations, extended by `continue(Nmif=50)` for a total of 100 iterations. The improvement over local search is only 0.06 log-likelihood units (−375.83 to −375.77), and no convergence diagnostics are shown for the global search (no likelihood traces, no pairs plot colored by starting region). With only 10 diverse starts and a 13-parameter model over a wide box, there is insufficient evidence that the global optimum has been found. The best log-likelihood from the global search being only marginally better than the local search does not by itself confirm convergence — it could mean either that the local search found a near-global optimum or that the global search was too sparse (see Wheeler et al. 2024, §Computational adequacy).

**Fix:** Increase the number of global search replicates to at least 50–100, show convergence traces for all search replicates (log-likelihood across IF2 iterations), and use replicated particle filter evaluations (`logmeanexp` over ≥10 replicates, as done in the global likelihood evaluation) consistently throughout.

---

### 5. Profile likelihood range for `rho` is far too narrow

The profile grid for `rho` is defined as `seq(MLE_params["rho"] * 0.8, MLE_params["rho"] * 1.2, length.out = 10)`, spanning only ±20% around the MLE. For a reporting-rate parameter like `rho`, which can plausibly vary over orders of magnitude and is often poorly identified in epidemic models, restricting the grid to a ±20% window around the MLE guarantees a near-flat profile and a trivially narrow CI. The reported "singleton" CI [0.00015, 0.00015] is entirely an artifact of the grid range choice: the likelihood is approximately flat over this tiny window, so all 10 grid points are above the cutoff. This cannot be interpreted as a meaningful CI or evidence of identifiability (see pomp-profile-range-misalignment skill).

**Fix:** Expand the `rho` profile grid to span at least 2–3 orders of magnitude on a log scale (e.g., `exp(seq(log(1e-5), log(1e-3), length.out=20))`), run the profile, and report the actual CI from that wider grid.

---

### 6. No benchmark comparison against a non-mechanistic model on the same data

Section 5.1 attempts a model comparison but, as noted in Issue 2, does so on different data and likelihoods. There is no valid quantitative comparison of the SEIRS model against a non-mechanistic statistical model on the same original count series. The auto-regressive negative binomial (ARNB) model recommended by Wheeler et al. (2024) as a benchmark is not fitted. Without such a comparison, the claim that "the mechanistic approach better captures the underlying epidemic process" (Section 5.1, 7.1) is unsupported. A mechanistic model achieving −376 log-likelihood could still be beaten by an ARNB on the original case counts, in which case the added biological complexity would not translate to improved predictive performance (see Wheeler et al. 2024, §Benchmark comparison).

**Fix:** Fit an auto-regressive negative binomial model or ARIMA model to the original (undifferenced) case counts under a comparable observation model, compute its log-likelihood, and compare it quantitatively to the SEIRS log-likelihood.

---

### 7. No quantitative model diagnostics beyond visual inspection

The paper presents simulation plots ("SEIRS Simulation with Best Global Parameters") as the primary evidence of fit, but no quantitative goodness-of-fit diagnostics are reported: no conditional log-likelihoods by time period, no effective sample size monitoring from the particle filter, no comparison of simulation summary statistics (mean, variance, skewness across 20 simulations) to observed data. The pairs plot of local search results is used informally to assess identifiability but is not linked to any formal analysis. Wheeler et al. (2024) note that "visual comparisons alone are only a weak and informal measure of goodness-of-fit."

**Fix:** Add conditional log-likelihood plots across time to identify periods of poor fit, report ESS from the particle filter runs at the MLE, and supplement visual comparisons with quantitative simulation diagnostics (e.g., coverage of simulated 95% intervals).

---

## Minor Issues

### 8. ARMA/SARMA are fitted to differenced data without restoring likelihood to the original scale

The paper first log-transforms the series (`log(1 + flu_ts)`) and then abandons the log transformation in favor of differencing (`diff(flu_ts)`, not `diff(log_flu_ts)`). The final ARMA and SARMA models are fitted to `diff_flu_ts` (first difference of the raw counts, not the log-transformed series). This means the model is fitted to week-over-week count increments rather than the original counts, and the Gaussian measurement model on differences is an unusual choice for count data. The paper does not justify this choice or verify that differencing achieves stationarity beyond visually inspecting the ACF. No formal stationarity tests (ADF, KPSS) are reported.

---

### 9. Periodogram frequency interpretation is questionable

Section 2.2 identifies a dominant frequency of 0.0167 cycles per week, corresponding to a period of ~60 weeks (~1.15 years), and interprets this as the seasonal period of the flu data. However, the data spans only about 2.25 years (116 weeks), so a 60-week period is estimated from fewer than 2 full cycles. With such a short record, the spectral estimate at low frequencies has high variance. The annual flu seasonality (52-week period, frequency ≈ 0.0192) is the biologically expected period, yet the paper does not discuss why the estimated period diverges from 52 weeks. The SARMA model is correctly fitted with period=52, creating an inconsistency between the frequency analysis and the SARMA specification that is not resolved.

---

### 10. `amp` is declared as logit-transformed but can equal 1

The `partrans` declaration sets `logit = c("amp", "rho")`, constraining `amp` to (0, 1). However, the seasonal transmission function `Beta(t) = Beta0 * (1 + amp * cos(...))` requires only `amp >= 0` and `amp <= 1` to ensure non-negative Beta values; the logit transformation is appropriate. But the initial value `amp = 0.47` and the profile grid `seq(0.526, 0.570)` are well within (0,1), so no numerical issues arise in practice. This is a minor note — the constraint is correctly implemented.

---

### 11. Profile likelihood for `phase` grid may wrap around seasonally

The `phase` parameter enters the model as an argument to `cos(2*pi*(t + phase)/52)`, so its likelihood surface is 52-periodic (a shift of 52 weeks is identical to no shift). The profile grid for `phase` is `seq(MLE - 10, MLE + 10, length.out=10)` around the global MLE of ~52.64. This places the grid from ~42.6 to ~62.6, which spans the 52-week periodicity boundary. Depending on the MLE, the global optimum at `phase ≈ 52.64` is statistically equivalent to `phase ≈ 0.64`. The profile likelihood should either be computed on a reduced range (0 to 52) or the periodic structure should be acknowledged in the CI interpretation.

---

### 12. Only 4 of 13 parameters are profiled

The paper profiles only `amp`, `Beta0`, `phase`, and `rho`, omitting `mu_EI`, `mu_IR`, `mu_RS`, `k`, and all initial condition parameters. The paper acknowledges this as a limitation due to computational constraints, which is acceptable for a course project, but the conclusion that "parameters `amp` and `Beta0` are well-identified" (Section 6.2) should not be stated without profiling all scientifically important parameters, particularly `mu_EI` (the exposed-to-infectious rate, which determines the latent period) and `mu_RS` (the waning immunity rate, which is central to the SEIRS vs. SEIR distinction).

---

### 13. Parameter estimates are not compared to independent biological knowledge

The fitted parameters are not compared to published flu natural history values. For example: `mu_EI = 0.9` per week implies a mean latent period of 1/0.9 ≈ 1.1 weeks (≈ 8 days), which is biologically plausible for influenza (typical incubation 2–3 days, but with sub-weekly detection). `mu_IR ≈ 1.8` per week implies a mean infectious period of 0.56 weeks (≈ 4 days), also plausible. `Beta0 ≈ 3.77` per week with `N = 10^7` implies a basic reproduction number of `R_0 = Beta0 / mu_IR ≈ 2.1`, consistent with published flu R₀ estimates. While these values appear broadly consistent with prior knowledge, the paper does not mention this comparison at all, and the very small reporting rate (`rho ≈ 0.00015`) — implying only 0.015% of infected individuals are detected — is surprisingly low and deserves explicit discussion. See Wheeler et al. (2024), §Corroboration with scientific knowledge.

---

### 14. Notation inconsistency: `flu_michigan.csv` path hard-coded as `../Data/`

The data loading code reads `"../Data/flu_michigan.csv"` but the data file `flu_michigan.csv` is located in the project folder itself (same directory as the Rmd). This path would fail if the Rmd were knitted from its own directory. Reproducibility requires that the data path be relative to the Rmd file location, or that a `here::here()` call or the Makefile handle path resolution correctly.

---

### 15. Single particle filter evaluation per profile grid point introduces excessive Monte Carlo noise

Each profile grid point is evaluated with a single `pfilter(..., Np=5000)` call, producing a single noisy log-likelihood estimate. The particle filter log-likelihood estimator has non-negligible variance even at Np=5000 for a 116-observation series with a stochastic process model. The resulting profile curves (especially the 10-point curves shown in the plots) will have visible Monte Carlo jitter. The CI extraction via `which(loglik >= cutoff)` is then sensitive to individual noisy evaluations. The global likelihood evaluation (Section 4.3) correctly uses `logmeanexp` over 10 replicates, but the profile evaluation does not follow this practice.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project03/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project03/flu_michigan.csv`
