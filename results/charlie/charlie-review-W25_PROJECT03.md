# Peer Review: W25 Project 03 — "Flu Cases in Michigan"

---

## Summary

This project applies ARMA, SARMA, and a POMP-based SEIRS model to weekly influenza case counts in Michigan from 2023 through early 2025 (approximately 116 observations). The authors implement seasonal transmission, perform local and global IF2 searches, and attempt profile likelihood analysis for four parameters. The SEIRS model achieves a substantially higher log-likelihood than the ARMA/SARMA baselines. While the project covers a reasonable breadth of methods and shows awareness of POMP infrastructure, it suffers from several serious methodological flaws: the profile likelihoods are computed with a single IF2 restart and single particle-filter evaluation per grid point, making all reported confidence intervals statistically invalid; the log-likelihood comparison between ARIMA (on differenced data, Gaussian) and POMP (on counts, negative binomial) is not a valid direct numerical comparison; the global search is underpowered (10 replicates, Np = 1000, total Nmif = 100); and the `phase` parameter in the rho profile grid is centered narrowly on the MLE, potentially missing the true likelihood surface. The paper also lacks convergence diagnostics for the global search, model diagnostics beyond visual trajectory inspection, and any assessment of the biological plausibility of fitted parameter values.

---

## Major Issues

### 1. Profile likelihoods are computed with a single IF2 restart and a single pfilter evaluation per grid point, making all reported confidence intervals invalid

The profile likelihood loops (Section 6, chunk beginning around line 701) follow this structure for every profiled parameter: a single `mif2()` call is initialized from `MLE_params` with the profiled parameter overwritten, followed by a single `pfilter(..., Np = 5000)` call. The CI cutoff is then `max(profile_X$loglik) - qchisq(0.95, 1) / 2`, where the maximum is taken over the profile results rather than anchored to the global search maximum.

This procedure has three compounding flaws (Wheeler et al. 2024; skill: `pomp-profile-single-restart-audit`):

1. A single restart from the MLE provides no diversity in the constrained optimization. At grid points far from the MLE, the constrained optimizer may fail to reach the constrained maximum, causing the profile to drop too steeply.
2. A single `pfilter` evaluation introduces Monte Carlo noise of approximately 1–5 log-likelihood units for typical epidemic models with Np = 5000. With only 10 grid points and no replicated evaluations, the profile curve is dominated by noise rather than signal.
3. The CI reference should be the global search maximum, not the maximum within the profile. If the two differ by more than Monte Carlo error, the chi-squared threshold is applied at the wrong baseline.

The consequence is immediate: the reported singleton CIs for `phase` (95% CI: [2.7, 2.7]) and `rho` (95% CI: [0.00015, 0.00015]) are almost certainly artifacts of a single noisy pfilter evaluation being above the cutoff while its neighbors are not, not evidence of genuine non-identifiability. The authors' interpretation ("limited identifiability," "poor identifiability") may be qualitatively correct but is not supported by these computations.

Fix: Use `profile_design()` seeded from a high-likelihood box, run multiple IF2 restarts (at least 5–10) per grid value, evaluate log-likelihood via `logmeanexp(replicate(K, logLik(pfilter(...))), se=TRUE)` with K >= 10, and apply the chi-squared cutoff against the global search maximum.

---

### 2. Direct log-likelihood comparison between ARIMA/SARMA and POMP is statistically invalid

Section 5.1 (Table comparing log-likelihoods: ARMA = -497.31, SARMA = -495.40, SEIRS = -375.79) presents these as directly comparable and concludes that the SEIRS model is "significantly better." This comparison is invalid because the three likelihoods are evaluated under fundamentally different observation models and data transformations (skill: `sarima-baseline-audit`):

- The ARMA/SARMA log-likelihoods are evaluated on the first-differenced time series (`diff_flu_ts`) under a Gaussian measurement model.
- The SEIRS (POMP) log-likelihood is evaluated on the original weekly case counts under a negative binomial measurement model (`dnbinom_mu`).

A likelihood on differenced data is not on the same scale as a likelihood on the original data. Likewise, a Gaussian likelihood and a negative binomial likelihood over the same count series are not numerically comparable. The ~120-unit difference in log-likelihoods cannot be used to assert that SEIRS "significantly outperformed" the ARMA/SARMA models.

Fix: To make a valid comparison, either (a) evaluate both models on the original counts under the same observation model (e.g., a negative binomial SARMA benchmark via the `TSGLM` or `tscount` package), or (b) evaluate both models using a proper scoring rule (e.g., continuous ranked probability score) on held-out data. The current table should be removed or clearly qualified as an informal comparison of incompatible likelihoods.

---

### 3. Global search is severely underpowered: 10 replicates, low particle count, and no convergence evidence

Section 4.3 runs only 10 global search replicates (`start_designs` is `replicate(10, ...)`), each with Np = 1000 particles and total Nmif = 100 (50 + `continue(Nmif=50)`). The particle count and replicate count are far below the standard for a model of this complexity. For comparison, Wheeler et al. (2024) used thousands of CPU-hours for profile likelihoods alone. With 10 replicates, the probability that the global maximum was found is low, and the "best global search result" may be a local optimum. Crucially, the global search best log-likelihood (-375.77) is only marginally better than the local search best (-375.83), consistent with the global search failing to meaningfully explore beyond the local search starting point. No convergence traces for the global search are shown; the text only presents a parameter-vs-loglik scatter plot and a pairs plot.

Fix: Increase global search to at least 50–100 replicates from diverse starting points with Np >= 2000 and Nmif >= 100 per stage. Show log-likelihood convergence traces across IF2 iterations for the global search to demonstrate convergence.

---

### 4. Profile likelihood grid for `rho` spans only ±20% around the MLE — range too narrow to detect identifiability issues

The profile grid for `rho` is defined at line 822: `seq(MLE_params["rho"] * 0.8, MLE_params["rho"] * 1.2, length.out = 10)`. This spans only ±20% around the MLE (approximately [0.00012, 0.00018]). A range this narrow is insufficient to detect non-identifiability: if the likelihood surface is flat or slowly declining away from the MLE, the narrow grid will look artificially well-identified simply because it does not extend far enough to reveal the flat region. The reported singleton CI for `rho` cannot be interpreted as evidence of poor identifiability or tight identifiability — the grid does not resolve the likelihood surface adequately (skill: `pomp-profile-range-misalignment`).

Fix: Profile `rho` over at least one order of magnitude on each side of the MLE (e.g., `seq(MLE_rho / 10, MLE_rho * 10, length.out = 25)` on a log scale). Reporting the profile on a log scale for `rho` is also preferable given its small absolute magnitude.

---

### 5. No model diagnostics beyond visual simulation comparison

The paper assesses model fit only by overlaying 20 simulated trajectories against the observed data (Sections 4.1 and 4.3). No quantitative diagnostics are provided: there are no per-observation conditional log-likelihoods, no effective sample size (ESS) monitoring of the particle filter, no filtering-distribution simulations (conditioned on data) compared to forward simulations, and no summary statistics comparing simulated to observed data. Wheeler et al. (2024) explicitly state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit" and demonstrate that models that looked visually reasonable had substantially lower likelihoods than achievable. The absence of any diagnostics makes it impossible to identify where and how the model fails.

Fix: Report (a) the per-time-step conditional log-likelihood trace from `pfilter()`, (b) ESS across time to detect particle collapse, and (c) at least one summary statistic comparison (e.g., peak timing, total seasonal burden) between simulated and observed data.

---

### 6. No benchmark comparison against a non-mechanistic statistical model evaluated on the original count scale

The study includes ARMA and SARMA models, but as noted in Issue 2, these are fitted to differenced data under a Gaussian model and cannot serve as valid benchmarks. There is no comparison of the SEIRS model against a non-mechanistic count-data model such as a negative binomial auto-regression or a SARIMA fitted to the original count series. Wheeler et al. (2024) document that none of the 32 papers in their Haiti cholera review performed such a comparison and that some mechanistic models failed to beat simple benchmarks. Without a valid benchmark, it cannot be established that the SEIRS model captures meaningful structure beyond a well-fitted statistical baseline.

Fix: Fit at least one count-data benchmark (e.g., a negative binomial auto-regression via `tscount::tsglm`, or a Poisson INGARCH model) to the original weekly counts and compare log-likelihoods or AIC on the same data and same observation scale.

---

### 7. Parameters N, S0, E0, I0, R0 are not perturbed in IF2: initial state fractions are frozen during optimization

The `rw_sd` definition (lines 368–378) includes only `Beta0`, `amp`, `phase`, `mu_EI`, `mu_IR`, `mu_RS`, `rho`, and `k`. The initial state proportion parameters `S0`, `E0`, `I0`, and `R0` (which are declared in `partrans` with `barycentric` transformation) and population `N` are not included in the random-walk perturbations. This means the IF2 optimization never updates the initial conditions. The initial proportions `S0 = 0.07, E0 = 0.01, I0 = 0.035, R0 = 0.3` remain fixed at their manually chosen values throughout both local and global searches. Since initial conditions can substantially affect model fit (Wheeler et al. 2024, §Initial conditions), this choice either artificially constrains the optimization or implicitly asserts that these values are known without uncertainty — neither of which is discussed.

Fix: Either include `S0`, `E0`, `I0`, `R0` in `rw_sd` so the optimizer can estimate them, or fix them at scientifically justified values and explicitly assess sensitivity to alternative initializations.

---

## Minor Issues

### 8. Frequency analysis conclusion is inconsistent with the data

Section 2.2 identifies a dominant frequency of approximately 0.0167, corresponding to a period of ~60 weeks (~1.15 years), and states "seasonal patterns occur approximately every 60 weeks." However, influenza has a well-established annual (52-week) cycle, and the data spans only about 116 weeks with two flu season peaks. A 60-week period is inconsistent with both prior scientific knowledge and the two visible peaks (one around week 60 and another around week 110, which are approximately 50 weeks apart). The dominant frequency at 0.0167 may reflect the asymmetry between the two seasons or the overall upward trend, not the true seasonal period. The SARMA model uses a period of 52, creating an internal inconsistency: the frequency analysis concludes 60 weeks but the SARMA assumes 52. This inconsistency is not acknowledged.

---

### 9. SARMA model is fitted to differenced data but the period is fixed at 52 in the non-differenced data's terms

The SARMA model (Section 3.2) fits `SARMA(0,1)×(1,0)₅₂` to `diff_flu_ts` (first-differenced flu series) with `period = 52`. First differencing a series with period 52 transforms it; the seasonal period of the differenced series remains 52 only if the differencing order is appropriate (i.e., `d=0` in the ARIMA notation, not a seasonal difference). The authors apply a non-seasonal first difference (`diff_flu_ts <- diff(flu_ts)`) and then fit a seasonal component with period 52 to the result. This combination — non-seasonal differencing followed by seasonal AR — is an unusual specification that should be motivated and cross-validated. The AIC improvement from ARMA to SARMA is only 1.91 units (from -497.31 to -495.40), which is negligibly small and does not justify the additional seasonal parameter under the standard AIC penalty.

---

### 10. The `amp` parameter is declared as `logit`-transformed but is used in the cosine formula without a [0,1] constraint being necessary

The `amp` parameter controls the amplitude of seasonal forcing in `Beta(t) = Beta0 * (1 + amp * cos(...))`. With `logit` transformation, `amp` is constrained to (0, 1). If `amp` approaches 1, the transmission rate can drop to near zero (`1 + 1 * cos(π) = 0`), which may be appropriate. However, the `logit` transform is declared but `amp` is initialized at 0.47 (a plausible value) and its profile is computed over [0.426, 0.626]. The profile maximum at `amp ≈ 0.548` lies in the interior of the grid, consistent with the model. However, the text should note that the logit transformation prevents `amp` from exceeding 1 and explain the biological interpretation of this constraint.

---

### 11. The reporting rate `rho` has an implausibly small MLE value (approximately 0.00015) that is not discussed

The best global search result reports `rho ≈ 0.00015`, meaning the model infers that approximately 1 in 6,700 infectious individuals per week is reported as a flu case in Michigan. Michigan has a population of approximately 10 million. With `I0 ≈ 0.035 × 10^7 = 350,000` initially infectious, this would imply weekly reports on the order of `0.00015 × 350,000 ≈ 52` cases at baseline, which is consistent with the early data (e.g., 42 cases in week 2). While internally consistent, the authors do not compare this estimate to known CDC reporting rates or literature estimates of influenza detection fractions. Per Wheeler et al. (2024), implausible parameter estimates should be flagged as potential signs of misspecification or confounding. The extreme sparsity of reported cases relative to estimated true infections deserves explicit discussion.

---

### 12. The data file path in the code references a parent directory that may not exist in the project folder

Line 38 reads: `data <- read.csv("../Data/flu_michigan.csv")`. However, the project folder contains `flu_michigan.csv` directly (not in a `../Data/` subdirectory). This path will fail unless the working directory is set to a subdirectory of the project folder, which is inconsistent with standard Rmd rendering behavior. The `flu_michigan.csv` file is present in the project root, but the code as written will not read it unless the user sets a non-standard working directory. This reproducibility failure should be corrected to use the local path `"flu_michigan.csv"`.

---

### 13. Only 4 of 13 parameters are profiled; no profile likelihoods for the rate parameters mu_EI, mu_IR, mu_RS, and k

Section 6.1 explicitly acknowledges that profiles for `mu_EI`, `mu_IR`, `mu_RS`, and `k` were not computed due to computational constraints. These are arguably the most biologically interesting parameters: the latent period (`1/mu_EI`), infectious period (`1/mu_IR`), and immunity duration (`1/mu_RS`) are key epidemiological quantities with literature comparators. Without profile likelihoods for these parameters, it is impossible to assess whether they are identifiable or whether the estimates are consistent with known influenza biology.

---

### 14. The `phase` parameter in the global search is not bounded appropriately and the best value of 52.64 weeks is outside the natural [0, 52] cycle range

The global search box for `phase` is `runif(1, 0, 52)` (Section 4.3, line 527), but the best global result reports `phase = 52.64`. Since `phase` appears in `cos(2π(t + phase)/52)`, values at 0 and 52 are equivalent (both give `cos(2πt/52)`). A best estimate of 52.64 is essentially equivalent to ~0.64, suggesting the optimizer drifted slightly outside the natural [0, 52] period boundary. This should be noted and the `phase` parameter should be constrained or its periodic equivalence discussed. Additionally, the profile for `phase` is computed over a range centered on `MLE_params["phase"]` — if this is 52.64, the grid `seq(52.64 - 10, 52.64 + 10)` = [42.64, 62.64] spans across the 52-week periodicity boundary, making the profile geometrically non-monotone and the CI interpretation unclear.

---

### 15. Pairs plot interpretation overstates confidence in identifiability from only 10 global replicates

Section 4.3 states that the pairs plot of global search results "provides insight into the parameter identifiability and sensitivity" and identifies clear patterns for `amp` and `phase`. With only 10 global replicates, a pairs plot shows 10 points; any apparent patterns or correlations between parameters are not statistically meaningful with such a small sample. The text interprets these patterns as if they reflect the shape of the likelihood surface, but with n = 10 observations in a 13-dimensional parameter space, the pairs plot is essentially noise. This overinterpretation should be corrected or the pairs plot removed.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project03/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project03/flu_michigan.csv`
