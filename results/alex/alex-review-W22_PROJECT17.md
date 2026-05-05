# Peer Review: W22 Project 17 — US COVID-19 Cases Analysis

## Summary

This project fits a SARIMA model and an SEIR POMP model to daily US COVID-19 case counts (June 2021 – March 2022). The authors compare the two models via log-likelihood and conclude both are adequate. The POMP component is the primary focus of critique below, with secondary attention given to the time-series analysis.

---

## Weaknesses (prioritized, most critical first)

### 1. [Major] Initial state sets S(0) = N with no recovered population

The `seir_rinit` Csnippet hard-codes `S = N` (the full US population of ~334 million), with `R` implicitly zero. By June 2021, tens of millions of Americans had already been infected and/or vaccinated and should not be in the susceptible compartment. This initialization is epidemiologically indefensible for mid-pandemic data, and it inflates the effective susceptible pool, distorting all subsequent parameter estimates (especially beta values).

**Evidence:** `seir_rinit` in the Rmd (lines 365–370):
```
S = N;
E = 200000;
I = 270000;
H = 0;
```
The text acknowledges "our data is not collected from the beginning of the pandemic" (line 426) but does not correct `S`.

---

### 2. [Major] Accumulator variable H is never reset; measurement is on cumulative recoveries, not new cases

The process model accumulates into `H` (via `H += dN_IR`) but `H` is listed in `accumvars`, which resets it to zero at each observation time. However, the measurement model (`dmeas`/`rmeas`) uses `rho * H` as the expected new reported cases — this is appropriate only if `H` is the increment of recoveries within each time step. The issue is that the interpretation conflates "new recoveries" with "new confirmed cases." Newly *reported* cases should track new *infections* (transitions S->E or E->I), not recoveries. Using `dN_IR` (recoveries) as the latent quantity mapped to observed cases introduces a systematic temporal offset and conflates the reporting process with recovery dynamics.

**Evidence:** Lines 357–363 (process model) and lines 372–391 (measurement model). `H += dN_IR` is accumulated from recoveries, but daily confirmed cases represent incident infections, not concurrent recoveries.

---

### 3. [Major] Log-likelihood comparison between SARIMA and SEIR is invalid

The authors directly compare the SARIMA log-likelihood (-3672.181) to the SEIR particle filter log-likelihood (-3684.733) and declare the SARIMA "better." These likelihoods are not comparable: the SARIMA likelihood is evaluated on first-differenced data (so it is a likelihood over increments), while the SEIR likelihood is evaluated on the raw daily cases time series. The number of parameters also differs substantially (SARIMA(5,1,5)x(2,1,1) has 13 ARMA parameters; the SEIR has 11 free parameters). No AIC/BIC adjustment is made. The comparison lacks a principled basis.

**Evidence:** Conclusion section (lines 681–685) directly contrasts `-3672.181` vs `-3684.733` without acknowledging these structural differences.

---

### 4. [Major] SEIR particle filter likelihood evaluation in global search uses only Np=100

In the global search likelihood evaluation chunk (lines 638–644), `evals <- replicate(10, logLik(pfilter(mf, Np=100)))` uses only 100 particles. This is far too few for a model with 13 free parameters and over 290 time points, producing highly variable and unreliable log-likelihood estimates. The run-level 2 setting uses `Np = 1000` for mif2 but drops to 100 for the final evaluation. This inconsistency makes the reported MLE log-likelihood untrustworthy.

**Evidence:** Line 639: `evals <- replicate(10, logLik(pfilter(mf, Np=100)))` versus `Np = switch(run_level, 50, 1e3, 2500)` used in mif2 (line 256).

---

### 5. [Major] Convergence is acknowledged to be absent but no remediation is attempted

The authors explicitly state "Trajectory plots for some variables still do not show significant convergence" (line 673) but do not discuss what this means for the reliability of the MLE or the parameter estimates. No additional mif2 iterations, increased cooling schedule, or expanded run level is attempted. The final parameter estimates are taken from a non-converged optimizer, making all downstream conclusions about the SEIR model parameters unreliable.

**Evidence:** Lines 673–676, and the convergence diagnostic plot produced by `plot(mifs_global)`.

---

### 6. [Major] Gap in the beta time-period specification — period 11/12 to 12/08/2021 is missing

The `beta` piecewise function as written in the model assumptions (lines 323–333) has periods ending at 11/11/2021 and then resuming at 12/09/2021. The 28-day window (November 12 – December 8) is unaccounted for in the stated formulas, though the `seir_covar` covariate table (lines 393–402) appears to assign these days to interventions 5 and 6. This discrepancy between the mathematical specification and the code is confusing and potentially incorrect.

**Evidence:** The beta case statement in the model assumption section ends `b4` at 10/03–11/11/2021 and jumps to `b5` at 12/09–12/21. The covariate table assigns 40 time steps to intervention 4, 40 to intervention 5, and 15 to intervention 6 (lines 396–400), which does not line up with the date ranges stated.

---

### 7. [Major] mu_IR is fixed without epidemiological justification

The recovery rate `mu_IR` is fixed at 0.1 (implying a mean infectious period of 10 days) and not estimated. While fixing some parameters is necessary to aid identifiability, the authors provide no reference or sensitivity analysis to justify this value. For COVID-19 variants present during the study period (Delta, Omicron), the infectious period differs, and fixing mu_IR at a single value across all 7 intervention periods is a strong and unjustified assumption.

**Evidence:** Lines 447–448: `fixed_params = params[c("N", "mu_IR")]`. The rationale given (lines 312–318) does not mention mu_IR specifically.

---

### 8. [Minor] SARIMA model formula contains a typographical error

The SARIMA formula (line 131) is written as:
```
phi(B) Phi(B^T) [(1-B)^d (1-B^T)^D Y_n - mu] = psi(B)(epsilon_n) Psi(B^T) epsilon_n
```
The right-hand side has `epsilon_n` appearing twice (once inside `psi(B)(epsilon_n)` and once after `Psi(B^T)`). The standard formulation should be `psi(B) Psi(B^T) epsilon_n`. Additionally, `Phi` in the polynomial definitions (lines 142–143) reuses the symbol `p` for both non-seasonal and seasonal AR orders, which is notational inconsistency.

---

### 9. [Minor] AIC table used for ARIMA order selection selects a high-order model (5,5) with causality/invertibility issues

The authors select ARIMA(5,1,5) based purely on AIC (line 153) and subsequently find that 4 AR roots and 1 MA root lie outside the unit circle (lines 213–225), making the model non-causal and non-invertible. Rather than addressing this by selecting a simpler model or applying root cancellation, the authors accept it as adequate. A non-causal ARIMA model cannot be used for forecasting and has limited interpretive value.

---

### 10. [Minor] The measurement model uses a normal approximation for count data

The `dmeas` and `rmeas` Csnippets (lines 372–391) approximate case counts with a normal distribution (centered at `rho*H` with a combined overdispersion variance). For daily case counts — which are non-negative integers, sometimes in the tens of thousands — a normal approximation with continuity correction is reasonable but the authors never justify this choice or compare it to alternatives (e.g., negative binomial), which is standard for overdispersed count data in POMP models.

---

### 11. [Minor] Starting value for b5 (Omicron period) is inconsistent between text and code

The model assumption section (line 435) states `b5 = 1.5`, but the code at line 445 sets `b5 = 0.15`. The discrepancy is a factor of 10. Given that period 5 corresponds to the onset of the Omicron surge (December 2021), the starting contact rate is epidemiologically significant and this inconsistency undermines reproducibility.

**Evidence:** Line 435 (text): `b5 = 1.5`; Line 445 (code): `b5 = 0.15`.

---

### 12. [Minor] Global search box for tau is far from the starting value

The global search box for `tau` is set to `[0.2, 0.4]` (line 587), while the initial `tau = 0.001` (line 446) is 200 times smaller. The local search will presumably shift tau substantially, but the global search box covers a range that the initial parameter value is entirely outside of. If the true MLE is near the initial value, the global search box will miss it. No discussion of how these bounds were chosen is provided.

---

### 13. [Minor] No profile likelihood or confidence intervals for SEIR parameters

After the global search, only point estimates of the MLE parameters are reported. No profile likelihood or approximate confidence intervals are computed for any of the key epidemiological parameters (e.g., beta values, rho, ei1, ei2). This makes it impossible to assess which parameters are well-identified and which are poorly constrained by the data.

---

### 14. [Minor] Data source reproducibility issue

The dataset is cited as downloaded from Kaggle (line 79) but the specific Kaggle snapshot (version/date) is not specified, making exact replication of the data impossible. The date range stated is "2021 June 5th to 2022 March 29th" but the raw CSV (`us1.csv`) starts from 2020-01-21. The preprocessing filtering step (`filter(date > as.Date("2021-06-04"))`) is buried in code without prominent explanation.

---

### 15. [Minor] References to prior projects without independent validation

The authors cite "Final project w21 project 15" as the source for their SEIR model structure (line 700) and reference it again in the conclusion (line 683: "As project 15 in 2021 said..."). Borrowing a model structure from a prior project without independent justification of its suitability for the current data (different time period, different variants) weakens the methodological contribution. The paper that project 15 itself was based on (reference [8]) should have been consulted directly.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project17/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project17/us1.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project17/Makefile`
