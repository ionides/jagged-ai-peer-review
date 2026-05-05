# Peer Review: W22 Project 21 — ARMA and POMP Analysis on COVID-19 Variants in the US

---

## Summary

This project fits ARMA and POMP models to US daily COVID-19 case counts from 2020-01-23 to 2022-04-01, segmenting the data into three variant-driven periods (pre-Delta, Delta, Omicron) and applying successively more complex compartmental models (SEIR, SEIRV, SEIRV with vaccine breakthrough). The approach is well-motivated and the code is generally runnable. However, there are serious methodological flaws in the measurement model, the vaccination compartment initialization, the ARMA benchmark, and the search procedures that undermine the reliability of the reported likelihoods and parameter estimates.

---

## Weaknesses (prioritized, most critical first)

### 1. [MAJOR] Measurement model uses SD = mean, making it a unit-coefficient-of-variation normal — not a standard epidemiological distribution

In all three POMP models the `dmeas` Csnippet sets:
```c
double mean_cases = rho*H;
double sd_cases = sqrt(mean_cases*mean_cases);
```
`sqrt(mean^2) = mean`, so the standard deviation is always exactly equal to the mean — a coefficient of variation of 1. This is not a Poisson model, not a negative-binomial model, and not a well-justified normal approximation. A normal with SD = mean assigns significant probability mass to negative counts and degrades rapidly for small values of `rho*H`. The `tau` parameter is declared in `paramnames` and given a log transformation in `partrans`, yet it never appears in either `dmeas` or `rmeas`. The canonical approach for count data is a negative-binomial or Poisson measurement model. This flaw is present identically in all three model variants and renders the reported log-likelihoods incomparable to standard benchmarks.

### 2. [MAJOR] The `tau` parameter is completely unused

`tau` appears in `paramnames`, in `partrans` (log-transformed), and in the starting/search values, but it does not appear anywhere in the Csnippets for `dmeas`, `rmeas`, or `rprocess`. It is an inert ghost parameter that consumes a degree of freedom in the search and biases the likelihood surface geometry. Because it is log-transformed, MIF2 will move it without affecting the likelihood at all, wasting computational effort. This is repeated for all three models.

### 3. [MAJOR] Vaccination compartment initialization is numerically negligible and epidemiologically incorrect

For the Delta SEIRV model, the vaccinated population at initialization is set to:
```r
V = nearbyint(N*0.3*0.01);
```
This is 0.3% of 300 million = approximately 900,000 people, despite the text explicitly stating that 31.15% of the US population was vaccinated on 2021-05-01. The factor `0.3*0.01 = 0.003` is almost certainly a coding error (should be `0.3115`). For the Omicron SEIRV model the vaccinated compartment is similarly initialized as `round(N*(0.5945-0.5935))` — the *difference* between two vaccination percentages (roughly 0.1% of N = 300,000 people) rather than the cumulative vaccinated fraction (~59.45%). This means the V compartment is nearly empty at the start of each segment, making the vaccination dynamics essentially irrelevant to the model fit and producing a SEIRV model that behaves almost identically to an SEIR model.

### 4. [MAJOR] Local search for pre-Delta segment perturbs only Beta, rho, and eta — mu_EI and mu_IR are fixed

In the pre-Delta local search, the random walk SD is:
```r
covid_rw.sd <- rw.sd(Beta=0.002, rho=0.002, eta=ivp(0.002))
```
The parameters `mu_EI` (exposed-to-infectious rate) and `mu_IR` (infectious-to-recovered rate) are never perturbed during MIF2, meaning they are fixed at their starting values throughout the entire local search. These are among the most epidemiologically important parameters (they control the latency period and infectious duration), so fixing them artificially constrains the search and prevents proper exploration of the likelihood surface. This contrasts with the Delta and Omicron local searches, where all relevant parameters are perturbed.

### 5. [MAJOR] Pre-Delta global search uses only 10 starting points (Nmif chain starts), while Delta and Omicron use 20

The global search for the pre-Delta segment uses `foreach(i=1:10, ...)`, while the Delta and Omicron segments use `foreach(i=1:20, ...)`. Given that the pre-Delta segment is by far the longest (464 days vs. 214 and 122 days) and has the highest-dimensional likelihood surface (SEIR vs. SEIRV), using fewer starting points for the most complex problem is inconsistent and likely leads to poor coverage of the parameter space.

### 6. [MAJOR] ARMA model applied to entire, highly non-stationary time series without any differencing or transformation

The ARMA(4,4) model is fitted to the raw, undifferenced daily case counts spanning more than two years and three epidemiological waves with wildly different scales (near-zero early 2020 to ~800,000 during Omicron). The AIC table is computed for `data$cases` — the raw series — with no log transformation, no first-differencing, and no assessment of stationarity. Fitting an ARMA to this series is not a meaningful benchmark: the assumption of a constant mean and constant variance is grossly violated. A standard first step would be log-transformation or differencing. The fact that the ACF of residuals still shows autocorrelation (noted in the text) confirms the model is inadequate, but the root cause is not addressed.

### 7. [MAJOR] No profile likelihood or confidence intervals computed for any parameter

After completing both local and global searches the project does not construct profile likelihood curves for any parameter in any of the three models. There is therefore no uncertainty quantification for the estimated parameters (Beta, mu_EI, mu_IR, rho, eta) and no way to assess whether the estimates are well-identified. The pairs plots are provided but they reflect the full scatter of search particles, not proper likelihood profiles. This is a fundamental gap in the POMP analysis.

### 8. [MINOR] Local search SE filter threshold of 8 is far too permissive for the pre-Delta model

The pre-Delta local search results are filtered with `filter(loglik.se < 8)`. A standard-error threshold of 8 log-likelihood units is very large: it means that individual replicate log-likelihoods can vary by roughly ±16 units, indicating severe particle depletion or filter degeneracy. The best reported local search value (-16,474) has loglik.se = 5.07, which is still large. By comparison, the Delta and Omicron local searches use thresholds of 10 and 0.5 respectively — the Omicron threshold is appropriately tight. The inconsistency across segments makes cross-segment comparisons unreliable.

### 9. [MINOR] The Delta local search evaluation uses only Np=2000 particles, yielding highly variable log-likelihood estimates

For the Delta model, the log-likelihood evaluation after local search uses only 5 replicates with Np=2000:
```r
evals <- replicate(5, logLik(pfilter(mf, Np=2000)))
```
For a 214-day time series with a 6-compartment model, 2000 particles is inadequate. The pre-Delta local search uses Np=20000, which is more appropriate. The inconsistency inflates the Monte Carlo variance of the Delta estimates and makes the comparison between local and global search values less meaningful.

### 10. [MINOR] No comparison of log-likelihoods across segments or to any null model

The three POMP models are fit to separate time segments and the log-likelihoods are reported in isolation (-14,148 for pre-Delta, -2,707 for Delta, -1,640 for Omicron) without any discussion of what constitutes a good fit. There is no comparison to a simple null (e.g., the per-segment ARMA or a constant-rate model), and because the segments have different lengths and observation scales, the magnitudes are not directly comparable. A per-observation likelihood or AIC comparison to the ARMA benchmark would help establish whether the POMP models add value.

### 11. [MINOR] The pairs plot for the global search combines local and global search particles without labeling the source

For each segment, the pairs plots mix `global_results` and `local_results` in a single `bind_rows` call without color-coding or faceting by search type. Since the local and global searches use different starting points and the local search is far from the MLE, merging them obscures whether the global search has converged to a distinct, better region or simply revisited local search territory.

### 12. [MINOR] The `rmeas` Csnippet draws from a normal with SD = sqrt(rho*H) but `dmeas` uses SD = rho*H (the mean)

There is an inconsistency between the simulation measurement model (`rmeas`) and the evaluation measurement model (`dmeas`). In `rmeas`: `reports = rnorm(rho*H, sqrt(rho*H))` — standard deviation is `sqrt(rho*H)` (Poisson-like variance). In `dmeas`: `sd_cases = sqrt(mean_cases*mean_cases) = rho*H` — standard deviation is `rho*H` (CV = 1). This mismatch means that simulated trajectories are drawn from a different distribution than the one used to evaluate the likelihood. Simulations will therefore appear tighter than what the measurement model actually represents, making visual fit assessments misleading.

### 13. [MINOR] The initial pfilter evaluation uses only Np=100, which is too small to give a reliable likelihood estimate

The initial particle filter evaluation for each segment uses `Np=100`:
```r
covid1 %>% pfilter(params=params, Np=100)
```
This is used to report the initial log-likelihood before any search. With 100 particles and hundreds of observations, the logmeanexp estimate will have very high variance and the reported value is not informative. A minimum of 1,000–2,000 particles is needed for a reasonable initial estimate.

### 14. [MINOR] No stationarity analysis or spectral analysis precedes the ARMA modeling

The ARMA section jumps directly to an AIC table without any examination of the ACF/PACF of the raw series, any unit root tests, or any discussion of whether the series is stationary. The time series spans multiple epidemiological waves with a strongly time-varying mean; this should be acknowledged and motivate either differencing, transformation, or a fully nonstationary model before fitting ARMA.

### 15. [MINOR] The pre-Delta segment start date (2020-01-23) is also the global start of the dataset; initial conditions assume E=0, I=1, which is plausible but not justified

The pre-Delta SEIR model initializes with `E=0` and `I=1`, which effectively assumes a single infectious case imported on day 0. While this is a common convention for epidemic initiation, the text does not justify this choice or discuss sensitivity to the initial condition. Given that by 2020-01-23 the US already had confirmed imported cases and community spread was underway in some areas, the assumption of a single infectious individual on the first day of the data could bias the trajectory of the model fit for the early phase of the outbreak.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/daily_case_us.csv`
