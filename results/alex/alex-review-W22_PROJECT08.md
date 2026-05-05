# Peer Review: Analysis of Covid-19 Cases in Turkey
**Semester:** W22 | **Project:** 08

---

## Summary

This project fits a custom SEIREIR (Susceptible-Exposed-Infected-Recovered-Exposed-Infected-Recovered) POMP model to daily COVID-19 case counts from Turkey in 2020, aiming to capture two epidemic waves driven by an original strain and a new variant. An ARIMA(2,1,0) benchmark is also presented. The model construction is creative and the code is functional, but several methodological, statistical, and reporting issues reduce confidence in the results.

---

## Weaknesses (prioritized from most to least critical)

### 1. [MAJOR] Incorrect definition of the outcome variable ("cases")

The observed variable is computed as `turkey$cases = turkey$Confirmed - turkey$Deaths - turkey$Recovered`, which produces the number of *currently active* cases (a stock), not new daily *incident* cases (a flow). The measurement model (`dmeas`) links `reports` to the accumulator `H`, which accumulates *recoveries* (`dN_IR_o + dN_IR_b`). Fitting active-case counts to a recovery-based accumulator is a fundamental model–data mismatch. Daily incident (new) confirmed cases should be used as the observation, or `H` should accumulate new infections/confirmations.

### 2. [MAJOR] Accumulator H tracks recoveries, not new cases

In `seireir_step`, `H += (dN_IR_o + dN_IR_b)` counts transitions into the recovered compartments. The measurement equation `lik = dnbinom_mu(reports, k, rho*H, give_log)` then models observed reports as a noisy fraction of *recoveries*. In a standard SEIR/SIR formulation, the accumulator should track new infections or new confirmed cases (e.g., `dN_EI_o + dN_EI_b`), not recoveries. This is a structural error that invalidates the probabilistic measurement model.

### 3. [MAJOR] Hard-coded seed injection at t=125 is unjustified and lacks uncertainty

The second wave is initiated by unconditionally adding `e = 10` to `E_b` when `t == 125`. This deterministic external seeding (a) is not estimated or uncertain, (b) is not justified scientifically (why 10 exposed individuals, why exactly day 125?), and (c) is not incorporated into the likelihood, making the particle filter's representation of uncertainty incomplete. A proper treatment would either estimate the seeding time and size as parameters or model the variant emergence as a stochastic event.

### 4. [MAJOR] Log-likelihood comparison between ARIMA and POMP is invalid

The paper concludes "it still can't beat the ARIMA" by directly comparing ARIMA log-likelihood (-1692) with the POMP particle filter log-likelihood (-2336). These are log-likelihoods from fundamentally different likelihood functions and observation models (ARIMA uses a Gaussian on differenced data; POMP uses a negative binomial on active-case counts). A direct numerical comparison is not meaningful and cannot support a conclusion about model fit.

### 5. [MAJOR] Local search uses `%do%` instead of `%dopar%`

The local search code block (line 387) uses `foreach(...) %do% {...}` (sequential execution), while the preamble registers a parallel backend with `registerDoParallel()`. This means the 20 IF2 runs are executed sequentially, which is both computationally inefficient and inconsistent with the stated intention of using parallel computation. (The global search code, which is wrapped in an `eval=FALSE` block, uses `%dopar%`.)

### 6. [MAJOR] Global search results cannot be reproduced from the Rmd

The global search code chunk has `eval=FALSE` (line 473), meaning it is never executed when knitting. The results are loaded from a pre-saved `global.RData` file, but that file is not included in the project directory (only `global_search.rds` is present). The local search likewise saves to `local.RData` (not present) and loads from it in a subsequent chunk. The submitted code is therefore not reproducible, and the reader cannot verify the global search results.

### 7. [MAJOR] Population value inconsistency

The introduction and code both state `N = 84340000` (84.3 million, Turkey's actual population). However, the text in the "Simulated graphs" section states "We fix N=843400, the population of Turkey in 2020" — off by a factor of 100. This is either a typographical error or indicates that an incorrect value was used at some point, raising doubt about which value produced the stored results.

### 8. [MINOR] `eta` initializes `R_b` as `(1-eta)*N`, conflating initial immunity with variant recovery

The initial condition sets `R_b = nearbyint((1-eta)*N)`, which places a large fraction of the population into the "recovered from beta variant" compartment at time zero — before the beta variant has even appeared. This is biologically nonsensical; at the start of the epidemic no one has recovered from the beta variant. This compartment should be initialized to 0. The use of `eta` here appears to be a misapplication of the initial susceptible fraction concept.

### 9. [MINOR] Parameter transformation is incomplete / inconsistent across searches

In `measSEIREIR2`, log transforms are applied to `Beta_o`, `Beta_b`, `Beta_r`, `Beta_or`, and logit transforms to `rho`, `mu_EI_o`, `mu_EI_b`, `eta`. However, `mu_IR_o`, `mu_IR_r`, `mu_IR_b` are fixed, and the random-walk standard deviations for the betas in the local search are very small (`0.002`–`0.003` on the log scale), while `Beta_o` and `Beta_b` span large ranges. This mismatch between the perturbation magnitude and the parameter scale likely impairs convergence.

### 10. [MINOR] Government restriction effect is modeled by a hard threshold at t=35 without estimation

The switch from `Beta_o`/`mu_IR_o` to `Beta_or`/`mu_IR_r` at `t > 35` is hard-coded. The cutoff day (t=35, roughly mid-April 2020) is not estimated, not discussed in detail, and not explored for sensitivity. Since this threshold has a large influence on the first-wave dynamics, at a minimum the choice should be justified and sensitivity analysis performed.

### 11. [MINOR] EDA does not compute daily new cases; the plotted series is a stock, not a flow

The "Explanatory data analysis" section plots `turkey$cases` (active cases stock) and describes it as "Daily infected cases," but it is not a daily count of new infections. No new-cases (incidence) series is ever constructed or analyzed. The interpretation of peaks and trends in the EDA would differ substantially if daily new confirmed cases were used.

### 12. [MINOR] AIC table search range is too narrow (P, Q in {0,1,2})

The ARIMA AIC table only considers AR and MA orders up to 2. The auto.arima call (line 81, `eval=FALSE`) is suppressed from output. Restricting to such a small grid without reporting the auto.arima result means a potentially better model may have been missed, and the benchmark is not as strong as it could be.

### 13. [MINOR] No confidence intervals or profile likelihood are computed for POMP parameters

After the global search, no profile likelihood or confidence intervals are constructed for any parameter. The pairs plot gives a qualitative sense of parameter uncertainty, but no formal inference is made. Standard practice in POMP analyses is to compute profile likelihoods for key parameters such as `Beta_o`, `rho`, and `eta`.

### 14. [MINOR] ESS interpretation is incomplete

The particle filter ESS plot is shown but the discussion only notes that ESS is "small around day = 10." Small ESS at early time points is often a sign of poor model fit or a bad initial condition, but this is not diagnosed further. ESS collapsing near the first peak (the most informative part of the data) would be a more serious concern and deserves explicit comment.

### 15. [MINOR] Conclusion misidentifies the POMP log-likelihood value and draws incorrect comparison

The conclusion states "the maximum log likelihood of the SEIREIR model is -2336," but the best entry in `covid_params.csv` achieves approximately -2308.6. The value -2336 appears to correspond to the initial particle filter evaluation (before optimization), not the post-optimization MLE. Additionally, the direct comparison with the ARIMA log-likelihood of -1692 (from a different model class and observation equation) is incorrectly presented as evidence of ARIMA superiority.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/covid_19_data_tr.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/covid_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project08/Makefile`
