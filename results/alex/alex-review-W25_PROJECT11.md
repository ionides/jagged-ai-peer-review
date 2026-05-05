# Peer Review: W25 Project 11 — Time Series Analysis of Apple Stock Price

## Summary

This project applies ARMA-GARCH and POMP-based discrete-time stochastic volatility (SV) models to Apple Inc. (AAPL) daily log-returns from January 2020 to early 2025. The writeup is organized, covers the standard pipeline (data exploration, ARMA model selection, GARCH variants, POMP local/global search, profile likelihood), and correctly identifies weaknesses of the POMP fit. However, there are a number of significant methodological, statistical, and presentation errors that substantially weaken the analysis.

---

## Weaknesses (Most Critical First)

### 1. [Major] POMP Parameter Values Are Implausible — sigma_eta and phi Are Out of Range

The `apple_params.csv` file (and the Top-10 tables in the report) show `sigma_eta` values around 3–225 and `phi` values essentially equal to 1.0 (e.g., 0.99999983, 0.99997...). A `phi` of 1 corresponds to a unit-root volatility process, making the model non-stationary. Values of `sigma_eta` exceeding 1 are anomalously large for a log-volatility process calibrated to daily returns. These results strongly suggest the optimizer is hitting a boundary or the parameter space is misspecified, yet the authors proceed to select these as "final" parameters without commentary on whether they are physically meaningful or whether the stationarity condition is satisfied.

Evidence: `apple_params.csv` rows throughout; Table 6.3 (`phi = 0.999...`, `sigma_eta` in the hundreds).

---

### 2. [Major] Inconsistency Between Stated Model and Diagnostic Evaluation

The authors state they selected `gjrGARCH` as the final GARCH model (Section 4.2 and Section 7), but the `garch_residual_diagnostics` function is actually called on `models[["eGARCH_std"]]` (line 465), not the gjrGARCH fit. The diagnostic statistics (skewness, kurtosis, ARCH-LM, Ljung-Box) and all six residual plots therefore correspond to the EGARCH model, not the model the authors claim to be validating.

Evidence: `blinded.Rmd` line 465: `model_to_test <- models[["eGARCH_std"]]`, followed immediately by text interpreting results as belonging to gjrGARCH.

---

### 3. [Major] Log-Return Computation Is Applied to an Already Log-Transformed Series

In the EDA section (line 94), the close prices are overwritten with `1 + log(subset_data$Close)` under the variable `apple_ts`. Then `diffRtn = diff(apple_ts)` is used as the POMP input `deMeanRtn`. This means the POMP model is fitted on first differences of `1 + log(price)`, i.e., `log(p_t/p_{t-1})`, which is numerically valid, but separately at line 123–126, `df$log_return = diff(log(df$Close))` is computed fresh for the ACF plots and ARMA/GARCH fitting. The two series are conceptually the same but derived from different objects; the "+1" offset in `apple_ts` is a coding artifact that could introduce small discrepancies, and neither the ARMA/GARCH models nor the POMP model are confirmed to operate on the identical numerical series.

Evidence: `blinded.Rmd` lines 94–95 vs. lines 117–118 vs. lines 123–126.

---

### 4. [Major] Global Search Is Initialized Only From a Single Local Search Chain

The global search (lines 763–778) uses `mif2(if1[[1]], ...)`, i.e., it starts all global search runs from the first chain of the local search, randomizing only the initial parameter guesses via `apple_box`. This means the IF2 chains inherit the trajectory history and cooling schedule of `if1[[1]]`, potentially biasing the global search toward the local optimum already found. Standard practice is to initialize global search runs fresh from the randomly drawn starting points, not from a completed IF2 object.

Evidence: `blinded.Rmd` line 766: `mif2(if1[[1]], params=apply(apple_box,1,function(x)runif(1,x)))`.

---

### 5. [Major] Profile Likelihood Is Computed at Insufficient Resolution and With Too Few Particles

The profile over `phi` uses only 10 grid points (`seq(0.85, 0.99, length=10)`) with 15 profiles each, and the pfilter calls inside the profile use only `Np=100` particles. With run_level=2, this is well below the recommended minimum for a reliable likelihood surface. The confidence interval (0.959, 0.99) is reported as if it were trustworthy, but the log-likelihood estimates at this particle count carry high Monte Carlo error, undermining the CI validity. The authors themselves note the issue but do not quantify the uncertainty.

Evidence: `blinded.Rmd` lines 874–899.

---

### 6. [Major] STL Decomposition Is Misapplied to Stock Price Data

STL decomposition is used to decompose the raw close price series (line 96–99) with `frequency=260` (trading days/year). STL assumes an additive decomposition with a stable seasonal period, which is not a valid assumption for financial price data. Stock prices are non-stationary and have no true seasonality in the STL sense. The authors acknowledge there is "no clear seasonality," which makes the decomposition uninformative and potentially misleading as an EDA tool for this application.

Evidence: `blinded.Rmd` lines 95–103.

---

### 7. [Major] ARMA Model Selection Logic Does Not Match Stated Choice

The code selects the ARMA model with the lowest AIC as `best_model` (lines 185–204), but the text (line 215) states "we selected ARMA(1,1) due to its relative low AIC value and simple structure" while noting that AR(4)+MA(4) models also produced very low AIC. It is not demonstrated that the code actually chose ARMA(1,1) — the `best_model` would be whichever order minimized AIC numerically. There is no printout confirming the final selected order, and no AIC table is shown in a way that verifies ARMA(1,1) is optimal. The justification for overriding the automated AIC selection with parsimony is not formally stated.

Evidence: `blinded.Rmd` lines 195–215.

---

### 8. [Moderate] Density Plot Title Hardcodes "Gold Prices" for Apple Data

The density plot of Apple stock close prices (line 88) uses the label `"Density Plot of Gold Prices"` as the title. This is a copy-paste error from a previous project or template that was never corrected, presenting incorrect labeling in Figure 3.1.

Evidence: `blinded.Rmd` line 88: `labs(title = "Density Plot of Gold Prices", ...)`.

---

### 9. [Moderate] Log-Likelihood Comparison Between GARCH and POMP Is Not on Comparable Bases

The final comparison table (Section 7) lists log-likelihoods of 3328.37 (gjrGARCH), 3289.09 (sGARCH_norm), and 3288.55 (POMP). However, the GARCH log-likelihoods are exact (optimizer-maximized), while the POMP log-likelihood is a particle filter estimate with Monte Carlo error. No standard errors are reported in the comparison table, making the difference between sGARCH_norm (3289.09) and POMP (3288.55) — a gap of only 0.54 — appear larger than it actually is once POMP uncertainty is accounted for. The authors draw conclusions from a difference that is smaller than the Monte Carlo noise.

Evidence: Section 7 comparison table and `blinded.Rmd` lines 966–971.

---

### 10. [Moderate] Pairs Plot Threshold Is Too Wide (100 log-likelihood units)

The pairs plot for the local search (line 725) includes all runs within 100 log-likelihood units of the maximum. A threshold of 20 units is conventionally used to focus on high-quality parameter combinations. Using 100 units means the plot includes runs that are essentially very poor fits, making it impossible to identify any clear convergence structure, which the authors acknowledge ("difficult to identify any clear signs of convergence").

Evidence: `blinded.Rmd` line 725: `data=subset(r.if1, logLik>max(logLik)-100)`.

---

### 11. [Moderate] No Formal Stationarity Test for the Log-Return Series

The authors state that log-returns satisfy the stationarity requirement for ARMA modeling based on ACF behavior alone (Section 4). No formal unit root test (e.g., ADF or KPSS) is performed. Given that the data span a period of high structural variation (COVID shock, rate hikes), a formal test would strengthen the stationarity claim.

Evidence: Section 4, lines 145–149.

---

### 12. [Moderate] Profile Likelihood Is Computed Only for phi; Other Parameters Are Ignored

Only a profile likelihood for `phi` is computed. No profiles are shown for `sigma_eta`, `mu_h`, or `sigma_nu`, even though the pair plots suggest poor identifiability for multiple parameters. This provides a very incomplete picture of parameter uncertainty in the POMP model.

Evidence: Section 6.3, lines 862–960.

---

### 13. [Minor] Duplicate Library Imports

Several libraries are imported twice in the same document. Specifically, `library(forecast)` appears at lines 37 and 40, `library(ggplot2)` appears at lines 37 and 43, and `library(kableExtra)` appears at lines 29 and 31. While not technically harmful, this indicates the code was assembled without careful review.

Evidence: `blinded.Rmd` lines 24–47.

---

### 14. [Minor] Acknowledgments Section Contains Potentially Blind-Breaking Self-References

The acknowledgments (lines 981–987) explicitly reference "Project 11" from W24 and state "we noticed that [@apple2024] used basically the same dataset as we do." This cross-referencing of specific prior projects and public acknowledgment of overlapping dataset choices could compromise blinded review integrity.

Evidence: `blinded.Rmd` lines 981–987.

---

### 15. [Minor] Section Heading Typo: "Explorable Data Analysis"

The EDA section is titled "Explorable Data Analysis" (line 75) instead of the standard "Exploratory Data Analysis." This appears to be a typo that was not caught before submission.

Evidence: `blinded.Rmd` line 75.

---

## Summary of Key Findings

The most critical issues are: (1) the POMP model converging to boundary/implausible parameter values with `phi ~= 1` and anomalously large `sigma_eta`; (2) the GARCH diagnostic plots being generated for the wrong model (eGARCH instead of gjrGARCH); and (3) the global search initialization flaw. Together these undermine the reliability of both the GARCH and POMP results. The log-likelihood comparison in Section 7 is also problematic because the margin between sGARCH and POMP is smaller than the Monte Carlo noise in the POMP estimate.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/apple_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/references.bib`
