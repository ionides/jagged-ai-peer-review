# Final AI Review: Analysis on Covid-19 Cases in Japan
**Project:** w24, Project 03
**Reviewer:** Evan (Treatment E)

---

## Overall Assessment

This project makes a genuine effort to apply mechanistic time-series modeling to COVID-19 in Japan, combining a SARIMA benchmark with an SEIR model that features a scientifically motivated piecewise contact rate. The use of iterated filtering (mif2) with proper logmeanexp aggregation of particle filter likelihoods reflects sound methodological training. However, the project is undermined by several serious problems. Three global searches return best log-likelihoods differing by over 2,500 units, and the actual best-fitting parameter set (from global search 3, loglik ≈ −1083.8) is identified but then set aside in favor of a far inferior result. The profile likelihood for ρ produces a confidence interval that excludes the point estimate from the best global search, rendering the CI logically invalid. The paper's main epidemiological conclusion — that Japan has a high COVID-19 reporting rate — rests entirely on this invalid CI and is therefore unsupported. Additionally, the biological parameters µ_EI and µ_IR appear to be expressed in day⁻¹ but applied in a weekly time-step model, implying a 10-week infectious period that is inconsistent with COVID-19 biology. These issues should be addressed before the analysis can be considered complete.

---

## Key Strengths

| ID | Strength | Why it matters |
|----|----------|----------------|
| 24.03.8 | logmeanexp used correctly to aggregate pfilter log-likelihoods | Ensures unbiased likelihood estimation; contrast with the common error of averaging log-likelihoods |
| 24.03.9 | Piecewise β with event-based breakpoints (state of emergency, vaccination start, Tokyo Olympics) | Principled approach to capturing behavior change; breakpoints are documented and cited |
| 24.03.10 | Trace plots for local search show improving and partially convergent log-likelihood | Demonstrates appropriate convergence monitoring at the local search stage |

---

## Major Points

**24.03.A — Best MLE never identified; global search results are inconsistent and unexplained**

ID: 24.03.7 | Severity: Major

The three global searches return dramatically different best log-likelihoods: global search 1 (−3531.9), global search 2 (−4457.8), and global search 3 (−1083.8). The third search, which explored a wider range of τ (up to 0.2 vs. 0.006 in search 1), finds a result more than 2,400 log-likelihood units better than the previous best. This is a large improvement that should be the focus of all downstream analysis. Instead, the paper does not identify global search 3 as providing the MLE, and the simulation figures (fig_011, fig_016) display results from global search 1 (`best_global_results[1,]`, loglik = −3531.9), not from the actual best-fitting parameter set. The paper notes "we gain a significant improvement in the likelihood value" for search 3 but does not follow through.

*Why it matters:* All downstream analysis — simulations, profile likelihood, and the epidemiological interpretation — should be based on the MLE. Presenting a suboptimal result as the "best simulation" misleads the reader about the model's actual fit.

*Suggested author action:* Designate the global search 3 top result (b1≈96.6, b2≈1.2, b3≈41.5, b4≈7.3, ρ≈0.55, τ≈0.60, loglik=−1083.8) as the MLE. Re-run simulations from this parameter vector. Reconcile why earlier searches failed to find this region (likely because τ upper bound was too low at 0.006).

---

**24.03.B — Profile CI for ρ is logically invalid; epidemiological conclusion unsupported**

ID: 24.03.2 | Severity: Major

The reported 95% confidence interval for ρ is [0.661, 0.926]. However, the best-fitting parameter vectors from global search 3 all have ρ between 0.29 and 0.55 — values that lie below the CI lower bound of 0.661. A confidence interval constructed by the profile likelihood method must contain the MLE; if it does not, the interval is invalid. The likely cause is that the profile was initialized from `mifs_local[[1]]` (the local search MLE, where ρ ≈ 0.17) rather than from the global search 3 MLE, and with only 5 replicates per fixed ρ value (`nprof = 5`), the nuisance parameters may not be properly optimized at lower ρ values.

The paper's conclusion states: "the findings suggest a notably high reporting rate [for Japan], [which] may suggest stringent disease reporting and control measures." This conclusion depends entirely on the profile CI, which is invalid. The substantive epidemiological claim is therefore unsupported.

*Why it matters:* The CI is the primary inferential result for the epidemiologically relevant parameter. An invalid CI invalidates the paper's main interpretive claim.

*Suggested author action:* Re-run the profile using the global search 3 MLE as the starting parameter vector. Increase nprof to at least 20. Verify that the resulting CI contains the point estimate. If ρ is indeed around 0.55, revise the epidemiological interpretation accordingly.

---

**24.03.C — Rate parameters µ_EI and µ_IR appear to have a unit inconsistency**

ID: 24.03.1 | Severity: Major

The manuscript states that µ_EI ≈ 1/6.5 days⁻¹ ≈ 0.154 day⁻¹ and µ_IR ≈ 0.1 day⁻¹, citing CDC guidance. Both parameters are then set to 0.1 in the code. The SEIR model uses weekly data and `euler(seir_step, delta.t = 1)`, where delta.t = 1 corresponds to one week. The binomial transition probability is 1 - exp(-µ · Δt). If µ = 0.1 and Δt = 1 week, the per-week transition probability is 1 - exp(-0.1) ≈ 9.5%, implying a mean sojourn time of 10 weeks — far longer than the 6.5-day incubation period and the approximately 10-day infectious period stated in the text. For a weekly model, µ_EI ≈ 1.08 week⁻¹ (= 7/6.5) and µ_IR ≈ 0.7 week⁻¹ (= 7/10). The fixed values of 0.1 are approximately 10 times too small.

*Why it matters:* This unit error means the latent SEIR compartments evolve on a timescale roughly 10 times slower than the actual COVID-19 biology. The apparently good fit (loglik = −1083.8) may be achieved by compensating other parameters, but the compartment dynamics would be biologically meaningless.

*Suggested author action:* Convert all rates to week⁻¹ units for consistency with the weekly data. Verify by checking that the mean sojourn time in E (= 1/µ_EI in the units used) matches the intended incubation period. Consider allowing µ_EI and µ_IR to be estimated rather than fixed.

---

**24.03.D — No convergence diagnostics for global searches**

ID: 24.03.12 | Severity: Major

Trace plots (loglik and parameters vs. mif2 iteration) are provided for the local search (fig_009), but no analogous convergence diagnostics are shown for any of the three global searches. The dramatic differences between global search results (spanning over 2,400 log-likelihood units) suggest that searches explored very different regions of parameter space and may not have converged. Without trace plots for the global searches, it is impossible to assess whether any of them reached a stable optimum.

*Why it matters:* Convergence diagnostics are essential for trusting that the reported log-likelihoods represent genuine optima rather than early-stopping values.

*Suggested author action:* Show mif2 trace plots for global search 3 (the best-performing search), or at minimum plot the distribution of final log-likelihoods across all starting points to demonstrate that the search found a stable region.

---

**M1 — Initial conditions are biologically implausible**

ID: M1 | Severity: Major

The model initializes with E(0) = 100 exposed and I(0) = 200 infectious individuals at the start of the time series (week of Jan 5, 2020). Japan's first confirmed COVID-19 case was reported on January 16, 2020, and the first week in the dataset has 0 new cases. Starting with 200 infectious individuals is inconsistent with the data and the known epidemiological context. This likely contributes to why simulations "still be not able to capture the other major outbreaks" and miss the onset period. The initial susceptible fraction η is estimated (and converges to approximately 0.1), but E(0) and I(0) are fixed at large values without justification.

*Why it matters:* Biologically implausible initial conditions can distort parameter estimates for the entire epidemic trajectory, not just the initial period.

*Suggested author action:* Set E(0) and I(0) to small values (e.g., 0 and 1) consistent with the early epidemic. Alternatively, estimate E(0) and I(0) as part of the optimization or justify the choice with a sensitivity analysis.

---

**24.03.4 — No quantitative benchmark comparison between ARIMA and SEIR**

ID: 24.03.4 | Severity: Major

The paper fits both a SARIMA model and an SEIR model but provides no quantitative comparison between them on any common metric. The SARIMA AIC (5572.36 for the selected model) is reported but no log-likelihood for ARIMA on the same time window as the SEIR analysis is provided. Without this comparison, it is unclear whether the mechanistic SEIR model provides a better statistical description of the data than the time-series benchmark.

*Why it matters:* The purpose of fitting a mechanistic model alongside a benchmark is to demonstrate added scientific value. Without a comparison, the mechanistic model's contribution is undemonstrated.

*Suggested author action:* Refit the SARIMA to the Jan 2020 – Dec 2021 window (the same window as the SEIR). Report its log-likelihood (via `logLik(sarima_fit)` divided by 2 to match the convention, or directly). Compare with the SEIR best loglik. Note the different scales if needed.

---

## Minor Points

| ID | Concern | Severity | Suggested author action |
|----|---------|----------|------------------------|
| 24.03.3 | Simulation figures (fig_011, fig_016) show results from global search 1 (loglik = −3531.9) rather than the actual best parameters from global search 3 (loglik = −1083.8) | Minor | Replace simulation figures with results from the global search 3 MLE |
| 24.03.5 | SARIMA equation uses B^12 for the seasonal polynomial but the model uses period = 4; should be B^4 | Minor | Correct the seasonal lag in the mathematical equation to match the code |
| 24.03.13 | Key references (ARMA, SIR/SEIR, ACF/PACF, Spectrum Analysis, Seasonality) are Wikipedia articles | Minor | Replace with textbook citations (e.g., Shumway & Stoffer for time series, Keeling & Rohani for epidemic models) |
| 24.03.14 | µ_EI and µ_IR are fixed throughout all analyses and their sensitivity is never assessed | Minor | Show at least a brief sensitivity analysis or note this as an explicit limitation |
| 24.03.6 | The rmeas and dmeas measurement model is a truncated normal, which is the standard pomp tutorial approach. The paper does not justify why this is preferred over a negative binomial. | Minor | Either justify the truncated normal choice or consider a negative binomial, which is more standard for overdispersed count data |
| 24.03.N1 | The paper uses Ljung-Box test output for SARIMA residual diagnostics, reporting p = 0.024. The model selection was already done via AIC; this result simply confirms residual correlation without exploring alternative models that might resolve it | Minor | Acknowledge the residual autocorrelation as a limitation; note which higher-order SARIMA models were considered |
