# Peer Review: W24 Project 03 — COVID-19 Cases in Japan (SEIR + ARMA)

---

## Summary

This project fits an ARMA/SARIMA model and a time-varying-beta SEIR model to weekly COVID-19 case counts in Japan. The SARIMA portion is generally competent. The SEIR portion contains several significant technical and conceptual problems that undermine the reliability of the results. Issues range from a critical rate-units mismatch and biologically implausible initial conditions, to inconsistent log-likelihood trajectories across searches, a near-empty profile likelihood, and a final simulation that uses manually chosen parameters rather than the estimated MLE.

---

## Weaknesses (Prioritized)

### 1. [Major] Rate units mismatch: transition rates treated as per-week despite being described as per-day

The process model uses `euler(..., delta.t = 1)`, where the time unit is one week (the data are weekly). The transition probabilities are therefore `1 - exp(-mu_EI * 1)` per week. However, the text states that `mu_EI = 1/6.5 day^{-1} ≈ 0.15 day^{-1}` and `mu_IR ≈ 0.1 day^{-1}`, citing CDC sources. With `delta.t = 1 week`, fixing `mu_EI = mu_IR = 0.1` implies a mean exposed duration of **10 weeks = 70 days**, not the claimed 6.5 days, and a mean infectious duration of 10 weeks = 70 days, not 10 days. The rates are fixed and never estimated, so this error propagates into all inference. The correct per-week rate for a 6.5-day latency would be `7/6.5 ≈ 1.077 week^{-1}`.

### 2. [Major] Biologically implausible initial susceptible fraction (eta)

The `rinit` snippet sets `S = nearbyint(eta * N)`, so `eta` is the fraction of Japan's population that is susceptible at the start of the pandemic (January 2020). The best estimates across searches yield `eta ≈ 0.03–0.09`, meaning only 3–9% of the 126 million population is susceptible at the outset, implying 91–97% were already immune or recovered before COVID-19 existed. For a completely novel pathogen, `eta` should be near 1.0. The low `eta` is likely a compensating artifact masking other model misspecifications, but it is never acknowledged or discussed.

### 3. [Major] Global Search 1 produces worse likelihoods than local search — unexplained

The local search achieves a best log-likelihood of −2205.9. Global Search 1 (labeled "Based on Local Search") achieves only −3531.9, which is roughly 1326 log units worse. The subsequent global search using `mifs_global` is even worse at −4457.8. The only search to produce meaningfully better likelihoods is Global Search 2 (−1083.8), which uses a different parameter box. The project never acknowledges or investigates why searches putatively starting from a better region find substantially worse likelihoods. This non-monotone behavior strongly suggests convergence problems.

### 4. [Major] Profile likelihood CI based on only 3 points above the cutoff

The 95% confidence interval for `rho` is derived from a profile with 200 total starting points, but only **3 of the 200 filtered estimates fall above the chi-squared cutoff** (rho ≈ 0.661, 0.781, and 0.926). A CI constructed from three sparse points is unreliable. The profile does not reflect a well-explored likelihood surface and cannot justify a stated CI of [66%, 93%]. The paper acknowledges the profile as "very decentralized" for some parameters but does not address the sparsity of points above the cutoff.

### 5. [Major] Profile likelihood not anchored to the globally-optimized parameter region

The profile for `rho` uses `mifs_local[[1]]` as the base model, which was fit using initial parameters `b1=1, b2=10, b3=20, b4=18`. The best globally-optimized parameters (from Global Search 2) are `b1≈97, b2≈1.2, b3≈42, b4≈7` — a completely different region of parameter space. The profile's maximum log-likelihood (−1079.9) being higher than the global search 2 maximum (−1083.8) suggests the profile happened to land in a better region by chance, rather than by design, and the overall inference is unreliable.

### 6. [Major] Simulation uses manually chosen parameters, not the MLE

In the "Not Based on Local Search" section, the model is simulated with `b1=60, b2=0.06, b3=40, b4=600, rho=0.3, eta=0.05, tau=0.3`. These values are not the maximum likelihood estimates from Global Search 2 (where MLE gives `b1≈97, b2≈1.2, b3≈42, b4≈7, rho≈0.55, tau≈0.60`). In particular, `b2=0.06` is not among the top results and `b4=600` appears only in unstable, off-MLE solutions. The text claims these are from "the best global searching results" but the data in the RDS files do not support this.

### 7. [Major] Highly unstable b4 (contact rate in Olympic period) — not discussed

Among the top results from Global Search 2, `b4` ranges from 0.97 to over 3042 across the top 10 solutions, all at similar log-likelihoods. This indicates that `b4` is effectively unidentified by the data. The profile likelihood only covers `rho`; no profile is computed for `b4` or any other beta parameter. The dramatic range of `b4` values is never acknowledged, and no confidence intervals or identifiability discussion are provided for the beta parameters.

### 8. [Moderate] SEIR model covers only 46.8% of the available data and misses the largest outbreaks

The SEIR model is deliberately truncated at 31 December 2021 (104 of 222 weeks) to avoid Omicron-era dynamics. While the paper provides a scientific rationale, the consequence is that the model is evaluated on a period without the largest Japanese COVID waves (the BA.2, BA.5, and winter 2022 peaks were several times larger than the 2021 peaks). The ARMA model uses all 222 weeks. The project never discusses this fundamental asymmetry or its implications for comparing the two modeling approaches.

### 9. [Moderate] ARMA and SEIR models are never formally compared

The project states that it uses "two distinct yet complementary modeling approaches" but provides no formal comparison. No AIC/BIC comparison is made between SARIMA and SEIR (which would require evaluating SEIR likelihood on a comparable period), no residual analysis is done for the SEIR model, and no conclusion section synthesizes the two approaches. The SEIR section ends with a profile likelihood for `rho` without returning to the ARMA findings.

### 10. [Moderate] SARIMA notation inconsistency: B^12 in equations but period=4 in code

The SARIMA model equation in the text is written as `phi(B) * Phi(B^12) * (Yn - mu) = psi(B) * Psi(B^12) * epsilon_n`, suggesting a seasonal period of 12 (monthly with a monthly index). However, the code uses `Arima(..., seasonal = list(order=c(1,0,1), period=4))`, consistent with a 4-week (monthly) period for weekly data. The `B^12` in the equations is therefore either a typographical error or refers to a different convention than is implemented.

### 11. [Moderate] Non-convergence in local search: b4, eta, tau still varying at final iteration

The text acknowledges: "for b4, eta, and tau, there are still some variability, indicating potential uncertainty in these estimates or more iterations may be needed for convergence." Despite this observation, no additional local search iterations are run, and the authors proceed directly to global searches. The global search 1 subsequently yields worse likelihoods than the local search, suggesting the lack of local convergence propagated forward.

### 12. [Moderate] tau parameter dramatically larger in best estimates than initial guess — never discussed

The initial value of `tau` (the overdispersion parameter) is set to 0.05. After Global Search 2, the best estimates give `tau ≈ 0.60`, a 12-fold increase. This large overdispersion implies that the normal measurement model variance is dominated by `(tau * H)^2`, i.e., the model relies heavily on overdispersion to fit the data. This is a sign that the process model may be misspecified (e.g., due to the rate units error noted in Issue 1), but the large change in `tau` is never mentioned or interpreted.

### 13. [Minor] Section title "Not Based on Local Search" is misleading

The section describes a global search that is "not based on local search results," but the code uses `mf1 = mifs_local[[1]]` as the base `mif2` object. All mif2 calls inherit the cooling schedule and structural settings from the local search output. The section differs from Global Search 1 only in using a wider parameter box (e.g., `tau` up to 0.2 vs. 0.006, `rho` up to 1.0 vs. 0.3). Calling it "not based on local search" overstates the independence of this search.

### 14. [Minor] Low particle count for likelihood evaluation in global searches

Global Search 2 and the profile likelihood use `Np = 1000` particles with 10 replication evaluations to estimate log-likelihoods. For 104 time points with a nonlinear SEIR model, Np = 1000 can produce noisy likelihood estimates, particularly for high-likelihood regions. The local profile (which gives better likelihoods) uses 200 replications at Np = 10000 — a 20-fold difference in precision. Mixing low-precision and high-precision evaluations makes it difficult to compare likelihoods across searches.

### 15. [Minor] Weekly subsampling description is imprecise

The data processing uses `covid_japan[seq(1, length(covid_japan$date), 7), ]` to select weekly observations. The paper describes this as filtering data "of every week," but the original OWID dataset is daily, so this takes every 7th daily row. The paper later states the result is a "weekly based" series of 222 observations, which is numerically correct, but the subsampling method risks misaligning the selected dates (e.g., the first observation lands on 2020-01-05 but Period 1 is described as starting 01/01/2020, a 4-day mismatch).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/blinded.qmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/local_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/global_search_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/global_search_2.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/global_search_results.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/mifs_global.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/global_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project03/lik_starting_vals.rds`
