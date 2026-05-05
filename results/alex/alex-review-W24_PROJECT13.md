# Peer Review: W24 Project 13 — Taiwan COVID-19 SIQRIQR POMP Model

---

## Summary

This project analyzes Taiwan's COVID-19 case data in two phases, fitting SARIMA models to both waves and a custom SIQRIQR POMP model to the second (Omicron) wave. The motivating scientific question — assessing quarantine effectiveness and multi-wave dynamics — is interesting, and the attempt at an original compartmental structure is commendable. However, the project suffers from serious implementation errors in the model code, inconsistent model description, underpowered inference, and incomplete reporting of results.

---

## Weaknesses (prioritized most critical first)

### 1. [Critical] R-language step function contains syntax errors and references undefined variables

The first R-language version of `siqriqr_step` (lines 448–467) contains multiple errors that would prevent execution:

- `rbinom(R_o, 1-exp(-Beta_r*Q_b/N*dt))` — calls `rbinom` with only 2 arguments (requires 3: `n`, `size`, `prob`); also uses `dt` instead of `delta.t`.
- `rbinom(S-dN_SI_o, 1-exp(-Beta_b*Q_b/N*dt))` — same issues.
- `rbinom(I_b, 1-exp(-mu_IQ_b*dt))` — same issues.
- `rbinom(Q_b, 1-exp(-mu_QR_b*dt))` — same issues.
- `S = S - (dN_SE_o + dN_SE_b)` — references `dN_SE_o` and `dN_SE_b`, which are never defined; the model has no `E` (Exposed) compartment and uses `dN_SI_o` and `dN_SI_b` instead.
- The function never returns a named numeric vector, which is required by `pomp`'s `rprocess` interface.

This entire R-language block is broken. The project appears to rely solely on the Csnippet version, but presenting a broken version without acknowledgment is misleading.

### 2. [Critical] Hard-coded absolute file path prevents reproducibility

The POMP section reads the data with:
```r
read_csv(paste0("C:/Users/USER/Desktop/Time Series Analysis/Projects/TW_last_days.csv"))
```
This is a Windows-specific absolute path. No other user can run the code without modifying this line. The data file `TW_last_days.csv` is present in the project directory, so a relative path (or use of `here::here()`) should have been used.

### 3. [Critical] Measurement model is misspecified: H accumulates recoveries, not quarantine entries

The Csnippet updates `H` as:
```c
H += (dN_QR_o + dN_QR_b);
```
This accumulates individuals *leaving* quarantine (i.e., recovering), not new confirmed/reported cases. In a standard POMP epidemiological model, the accumulator variable should track new observed events — typically new detections (quarantine entries: `dN_IQ_o + dN_IQ_b`) rather than recoveries. Using recoveries as the basis for the observation model conflates the confirmation process with the recovery process and undermines the scientific interpretation of `rho` as a detection probability.

### 4. [Critical] Hard-coded intervention (`if (t == 125) e = 100`) is unexplained and unmotivated in the text

The Csnippet includes:
```c
double e = 0;
if (t == 125) e = 100;
...
I_b += dN_SI_b + dN_RI_b - dN_IQ_b + e;
```
An injection of 100 infectious individuals into `I_b` at day 125 is a significant modeling assumption. The text does not discuss this intervention, does not justify why day 125 was chosen, and does not explain why 100 individuals is the appropriate magnitude. This kind of undocumented hack calls into question the validity of any fitted parameters.

### 5. [Major] Parameter transformations are incomplete: `mu_QR_o`, `mu_QR_b`, `mu_QR_r`, `k` are fixed but not transformed

Several rate parameters (`mu_QR_o`, `mu_QR_r`, `mu_QR_b`, `k`) are fixed throughout both local and global searches:
```r
fixed_params <- params[c("mu_QR_o", "mu_QR_r", "mu_QR_b", "k", "N")]
```
There is no justification for fixing these parameters. The recovery rates from quarantine are epidemiologically meaningful and identifiable; fixing them arbitrarily at initial guesses (e.g., `mu_QR_b=0.01`) without discussion is a significant modeling limitation that should be acknowledged.

### 6. [Major] Local search uses `%do%` (sequential) instead of `%dopar%` (parallel)

The local search code uses:
```r
foreach(i=1:20,.combine=c) %do% { ... mif2(...) }
```
This runs sequentially. The global search correctly uses `%dopar%`. The inconsistency means the local search is unnecessarily slow and suggests the code was not carefully reviewed. It is also inconsistent with standard POMP workflow pedagogy.

### 7. [Major] Global search filter threshold of `loglik > max(loglik) - 1000` is far too permissive

The pairs plot filter:
```r
filter(is.finite(loglik), loglik > max(loglik, na.rm=TRUE) - 1000)
```
A window of 1000 log-likelihood units is enormous (roughly equivalent to allowing models that are exp(1000) times less likely). This suggests the global search results have very high variance, but the authors do not comment on this, nor do they report the actual best log-likelihood value or the range of log-likelihoods obtained.

### 8. [Major] No likelihood profile or uncertainty quantification for any parameter

Neither confidence intervals nor likelihood profiles are reported for any parameter. After conducting both local and global searches, the project simply prints the top-10 parameter sets but draws no statistical conclusions about parameter uncertainty. This is a fundamental gap in the POMP inference workflow.

### 9. [Major] Model description has internal inconsistencies (Beta vs. Omicron labeling confusion)

The compartment description (lines 419–430) labels the compartments as pertaining to Omicron (`I_o`, `Q_o`) and Beta (`I_b`, `Q_b`). However, the introduction states that the data covers the Omicron wave and the prior wave was Delta, not Beta. Furthermore, `R_b` is listed twice in the compartment descriptions (once for "people who have recovered from the beta variant" on lines 424 and 431), and `R_o` is never properly described. The text describes `Beta_b` as the infection velocity of "beta" while the scientific motivation is for an Omicron/prior-strain framework — terminology is inconsistent throughout.

### 10. [Major] SARIMA model for the first wave is not the same as what is described

The text states (line 310): "This is the (4,1,1) model for the first phase." However, the inverse roots plot is stated to be for the model selected by `auto.arima` (the WARIMA(4,1,1) model), while the AIC table approach suggested ARIMA(3,1,5). The authors say they use the `auto.arima` suggestion "because it does not only consider AIC but also different criteria," but `auto.arima` also uses AIC by default unless otherwise specified. The justification for preferring `auto.arima` over the AIC table result is circular and unsupported.

### 11. [Moderate] `ts()` frequency argument is misspecified for daily data

The time series objects are created with:
```r
ts_data1 <- ts(tw_df_first$new_confirmed, frequency = 52)
```
`frequency = 52` corresponds to weekly observations (52 weeks per year). The data is daily, so the correct frequency for weekly seasonality in daily data would be 7. Using `frequency = 52` on daily data misrepresents the seasonal structure and may distort `auto.arima`'s seasonal component selection.

### 12. [Moderate] No simulation diagnostic plots after fitting; only initial-guess simulations are shown

The simulation plot showing model trajectories against data (after `simulate()` with the initial guess parameters) is presented as a diagnostic, but there are no equivalent plots after local or global search optimization. Without post-fit simulations, it is impossible to visually assess whether the optimized model actually captures the data's key features.

### 13. [Moderate] The `Beta_or` parameter appears in `paramnames` and `rw.sd` but is not used in the Csnippet

The Csnippet `siqriqr_step` does not reference `Beta_or` anywhere in the transition equations, yet it is included in `paramnames` and given a random walk perturbation. This is a ghost parameter that wastes estimation effort and inflates the parameter space without contributing to the model dynamics.

### 14. [Minor] SARIMA model is referred to as "WARIMA" inconsistently with no formal definition

The authors introduce the term "WARIMA" (Weekly ARIMA) informally (line 167: "we can call it a WARIMA model") but use this term interchangeably with SARIMA throughout. The distinction is never formalized or cited. The fitted models `sarima_model1` and `sarima_model2` from `auto.arima` are standard SARIMA fits with `frequency=52`, not explicitly weekly-seasonal ARIMA models as described.

### 15. [Minor] Data loading in POMP section re-downloads from Google API rather than using the saved CSV

The EDA section loads data directly from the Google API URL, which is fragile (the URL may become unavailable). The POMP section then reads from the local CSV file. These two data sources should be consistent, and the provenance of `TW_last_days.csv` (how it was derived from the raw API data) is never explained — the 174 rows of the CSV do not obviously correspond to a clearly defined date range relative to the full dataset.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project13/TW_last_days.csv`
