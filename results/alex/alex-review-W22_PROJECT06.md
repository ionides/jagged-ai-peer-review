# Peer Review: Rubella Transmission POMP Model [1966-1967]
**Semester:** W22 | **Project:** 06

---

## Summary

This project builds a stochastic SEIR POMP model for weekly reported rubella cases in California, 1966-1967, using data from Project Tycho. The authors conduct exploratory data analysis, simulate the model, perform local and global likelihood maximization via iterated filtering (mif2), and construct likelihood profiles for the reporting rate (rho) and susceptible fraction (eta). The work follows a reasonable structure and demonstrates engagement with key POMP concepts, but it contains several notable statistical, methodological, and presentational weaknesses described below.

---

## Weaknesses (Prioritized)

### 1. [Major] Negative Binomial Measurement Model Is Misspecified

The `dmeas` Csnippet uses `dnbinom(reports, H, rho, FALSE)`, where the arguments correspond to `dnbinom(x, size, prob)` in R. In this parameterization, `H` is treated as the `size` (dispersion) parameter and `rho` as the success probability. However, `H` is the accumulator for recovered/removed individuals and will vary widely across time steps and particles, making it a highly unstable dispersion parameter. The standard approach is to use a separate overdispersion parameter (e.g., `psi` or `tau`) so that the mean of the negative binomial is `rho*H` and the dispersion is controlled independently. The `rmeas` Csnippet (`rnbinom(H, rho)`) has the same structural issue. This misspecification can produce wildly incorrect likelihood evaluations and misleading parameter estimates.

### 2. [Major] Conditional Likelihood Assigns Zero to Zero-Count Observations

The `dmeas` function returns only `tol = 1e-25` (not the true likelihood) when `reports == 0` or `H == 0`. A negative binomial can assign meaningful positive probability to zero counts, so truncating these contributions discards valid information and biases the filter. Particularly in epidemiological data where zero-count weeks occur, this leads to systematic underestimation of model fit.

### 3. [Major] Inconsistency Between Stated and Analyzed Time Period

The title, introduction, and key summary statistics consistently refer to the 1966-1967 time period ("weekly rubella reports in California from 1966-1967," "Total number of reported cases from 1966-1967 was 12,460"). However, the data pipeline creates a sequence from 1966-01-02 to 1975-12-21 (501 rows / approximately 10 years) before subsetting to the first 105 rows. 105 weeks corresponds to approximately two years (1966 to early 1968), not just 1966-1967 (104 weeks). The text alternately implies the dataset covers only 2 years while the code creates a 10-year series and then truncates. This inconsistency undermines reproducibility and interpretive clarity.

### 4. [Major] Parameters mu_EI and mu_IR Are Fixed Without Justification

The transition rates mu_EI = 0.08 and mu_IR = 0.4 are fixed throughout all analyses (local search, global search, and profiles). These correspond to mean latent and infectious periods of 12.5 weeks and 2.5 weeks, respectively. The incubation period for rubella is approximately 2-3 weeks (2-3/52 in weekly units, so mu_EI ~ 0.33-0.5), and the infectious period is approximately 1 week (mu_IR ~ 1.0). The chosen values deviate substantially from established rubella biology and no citation or sensitivity analysis justifies fixing them. Given that these parameters directly govern transmission dynamics, this is a critical unaddressed uncertainty.

### 5. [Major] Parameter Transformation Is Incomplete

The `parameter_trans` call applies logit transformations only to `rho` and `eta`. Parameters `b1` and `b2` are unconstrained, but `b2` is the amplitude of the seasonal forcing and should be non-negative; no transformation is applied to enforce this. More importantly, `mu_EI`, `mu_IR`, and `N` are fixed, so they do not need transformations, but the absence of log transforms for any rate parameters is non-standard and can cause mif2 to explore negative rate values in principle (though they are fixed here). At minimum, the omission of a log transform for `b2` should be acknowledged.

### 6. [Major] eta Profile Does Not Reach the Confidence Interval Cutoff

The authors report a 95% CI for eta of (0.24%, 0.25%) from the HTML output table but note in the text that "the graph states that our eta did not reach the confidence interval cutoff." They interpret this as meaning eta "did not converge," but a profile that never falls below the chi-squared cutoff indicates that the profile likelihood is essentially flat over the searched range -- the model is unidentifiable in eta. The correct conclusion is that no reliable confidence interval can be constructed for eta from this search, not that the reported interval bounds are valid. The reported CI bounds (0.24%-0.25%) in the HTML table are extracted from runs that all exceed the cutoff, making them meaningless as a confidence interval. The text in the Rmd also contradicts the HTML table, claiming the bounds are (0.19%, 0.24%).

### 7. [Major] Global Search Starts All Chains from mifs_local[[1]] Only

In the global search, `mif2(mifs_local[[1]], ...)` restarts every global chain from the first local MIF2 result with new random starting parameters. This is correct in principle, but uses the filter and perturbation settings inherited from the first local chain (Np and cooling settings from the local run). More critically, every one of the 60 global runs inherits the MIF2 configuration from the same single local run, meaning that if that run is atypical (e.g., it converged to a suboptimal region), all global chains inherit that bias in their algorithmic settings. A more robust approach is to call `mif2` from scratch with the global parameter guesses and explicitly set Np and Nmif.

### 8. [Moderate] rho Profile Range Inconsistent with Global Search Results

The global search box for rho is set to (0, 0.2), and the profile for rho is sampled over the same range (0, 0.2). However, the best global parameter estimates converge to rho ~ 0.06, and the reported 95% CI from the profile is very narrow (4.83%-5.52%). The profile should have been verified visually to confirm the CI cutoff line intersects the profile curve on both sides, i.e., that there are points both above and below the cutoff at each boundary. This is stated but no explicit confirmation or enlarged profile plot over a narrower range is shown to validate the CI.

### 9. [Moderate] Decomposition Analysis Confuses Trend with Vaccine Efficacy

The text states that the decomposition "appears to illustrate that the rate of rubella transmission did not notably decrease in the first 2 years of the MMR vaccine program." However, 105 weeks of data starting in January 1966 ends in early 1968 -- the MMR vaccine was introduced in 1969, so the data analyzed predates the vaccine by at least one year. The comparison of trends against vaccine efficacy is therefore not grounded in the data presented and is misleading.

### 10. [Moderate] R0 Calculation Uses Wrong Formula and Wrong Compartment

The text uses the approximation R0 ≈ L/A (lifespan over mean age of infection) to obtain R0 ≈ 9.95. However, for an SEIR model, R0 = beta / mu_IR, where beta is the transmission rate. The L/A heuristic is a rough epidemiological approximation, not derived from the model structure. The authors then do not use this R0 estimate to constrain or verify beta. Moreover, the transition in the binomial in the Csnippet reads `dN_SE = rbinom(S, 1-exp(-Beta*I/N*dt))`, meaning S flows to E based on contact with I, which is correct for a standard SEIR. But the written equation labels it `Delta N_{SI}` (not `Delta N_{SE}`), implying confusion in notation between SEIR and SIR.

### 11. [Moderate] Comment Left in Published Document

Section title "Pairwise relationships (not sure if we need to include this part)" appears verbatim in the rendered HTML (line 521 of the Rmd). This suggests incomplete revision before submission. Similarly, commented-out code blocks (the Hodrick-Prescott filter code) were not removed from the Rmd and appear as visible commented sections in the code-folding display.

### 12. [Moderate] Initial Values for E and I Are Hardcoded Without Justification

In `seir_init`, `E = 14` and `I = 7` are fixed integer constants, not estimated or derived from any epidemiological reasoning. For a population of ~15.7 million, these values are essentially zero and there is no discussion of sensitivity to these initial conditions. Initial infected individuals are often treated as parameters subject to estimation or at least sensitivity analysis in POMP analyses.

### 13. [Minor] Contradictions in Reported eta CI Bounds Between Rmd and HTML

The Rmd text (line 736) states the 95% CI for eta is "(0.19%, 0.24%)," but the rendered HTML table shows the bounds as (0.24%, 0.25%). These cannot both be correct; the discrepancy suggests the text description was written based on a different run or an earlier draft, but the table reflects the actual computation. This inconsistency should have been caught before submission.

### 14. [Minor] Data Imputation Uses Sequential Forward Filling With Potential Edge Cases

Missing values are imputed as the mean of the previous and next observation. The loop processes rows sequentially from i=1, so if consecutive missing values occur, the second missing observation's "previous" value is already an imputed value, not an observed one. This creates a cascading imputation bias. The paper notes n=4 missing values but does not verify they are non-consecutive.

### 15. [Minor] Comment in Text Uses Incorrect Direction of Bivariate Association

The text says "we find...a potential preference for lower values of eta" from the pairwise plot, and that the b1-b2 relationship is linear. However, in a model where beta = exp(b1 + b2*cos(...)), b1 and b2 are not truly independent -- they jointly determine the range of transmission rates -- so a linear ridge in b1-b2 space is expected and indicates a structural identifiability issue, not just a correlation. This identifiability issue is not acknowledged or discussed beyond noting that parameters "diverged."

---

## Summary of Critical Issues

The most severe problems are: (1) the negative binomial measurement model is structurally misspecified (H as dispersion rather than mean); (2) zero-count observations are excluded from the likelihood, biasing inference; (3) the incubation and infectious period parameters are fixed at biologically implausible values without justification; (4) the eta profile does not establish a valid confidence interval but the paper reports one anyway; and (5) there is a systematic inconsistency between the stated 1966-1967 analysis period and the code's data construction logic.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project06/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project06/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project06/Makefile`
