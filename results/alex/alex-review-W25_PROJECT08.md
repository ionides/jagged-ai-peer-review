# Peer Review: W25 Project 08 — Netflix Returns Analysis

## Overview

This project analyzes daily log-returns of Netflix (NFLX) and the S&P 500 ETF (SPY) over 2015–2022. It applies exploratory data analysis, STL decomposition, ARIMA and GARCH-family models, and a stochastic volatility POMP model with time-varying leverage, comparing both assets throughout. The writeup is generally clear and well-organized, but has several significant methodological, statistical, and presentational weaknesses detailed below, prioritized by severity.

---

## Weaknesses

### 1. (Major) Inconsistent Measurement Equation: `epsilon_n` Distribution Mismatch

In Section 6.1, the writeup states the measurement equation is $Y_n = \exp\{H_n/2\}\,\epsilon_n$ where $\epsilon_n \sim N(0, \sigma_\nu)$, implying observation noise is scaled by $\sigma_\nu$. However, the actual C snippet in `pomp_final.Rmd` implements `dmeasure` as `lik = dnorm(y, 0, exp(H/2), give_log)`, i.e., $\epsilon_n \sim N(0,1)$, with no $\sigma_\nu$ scaling in the measurement density. The parameter $\sigma_\nu$ instead governs the random walk of $G_n$. This discrepancy between the written model equations and the actual code is a fundamental documentation error and makes the model description misleading.

### 2. (Major) No Formal Model Comparison or Likelihood-Ratio Test Against GARCH Benchmarks

Section 8.1 claims that "maximum log-likelihood values obtained [for POMP] were higher than those of both GARCH and GJR-GARCH models." However, log-likelihoods from GARCH/GJR-GARCH (reported as per-observation AIC multiplied back to total AIC, then converted) are never placed on the same scale as the POMP log-likelihoods. GARCH models use a different parameterization and the GARCH likelihood is evaluated analytically while POMP uses a Monte Carlo approximation. No proper likelihood-ratio or AIC comparison table is presented. The superiority claim of POMP over GARCH is therefore unsupported.

### 3. (Major) Severe Non-Convergence and Multimodality in NFLX POMP Not Adequately Addressed

The CSV results in `nflx_params_local.csv` and `nflx_params_global.csv` show extreme parameter heterogeneity: `sigma_eta` ranges from near zero to ~1507 (local) and ~679 (global); `mu_h` varies from -10 to +10; `phi` clusters near 1.0 in most replicates but a few replicates with `phi` around 0.75–0.89 achieve the highest likelihoods. The authors acknowledge "unstable convergence" and "existence of traps for local maxima," but do not take corrective action (e.g., profile likelihood, more IF2 iterations, larger particle count, or parameter constraints). Reporting a single maximum row from a clearly non-converged run as the estimated parameters is insufficient.

### 4. (Major) Spurious "Degenerate" Parameter Combinations Not Excluded

Multiple replicates in both local and global searches reach combinations with `phi` near 1.0 and `sigma_eta` of order 10–1500, which corresponds to a near-unit-root, explosively volatile state process. These replicates achieve substantially lower log-likelihoods (~4540–4565 vs ~4622) yet are included in pairs plots without exclusion or comment about whether they represent genuine local maxima or numerical degeneracy. The global search similarly has extreme outliers (e.g., logLik_se of 5.9 or 10.5) indicating particle filter collapse that are not screened out before displaying results.

### 5. (Major) Log-Return Preprocessing Introduces a Spurious Zero Return

In Sections 2.2 and the POMP analysis, log-returns are constructed as `c(0, diff(log(nflx_train$Close)))`, prepending a zero return for the first observation. This artificial zero is passed directly as data to the POMP filter. An initial zero return is not a real trading return; it inflates the sample size by one and may distort the initial filter step, since the covariate for $Y_{n-1}$ at $n=1$ is also zero, directly affecting the $\beta_{n-1}$ leverage term in the state equation.

### 6. (Major) ACF/PACF Interpretation Contradicts Subsequent Analysis

Section 3.1 states "The ACF plots show slow decay for both series, which is characteristic of non-stationary series," but also concludes the series are stationary. Log returns of financial assets typically show near-zero ACF at all lags (they are essentially white noise in mean), and the ADF test correctly rejects the unit root. Describing slow decay in the ACF of stationary log returns as "characteristic of non-stationary series" is an internal contradiction that confuses the reader. The claim of "significant lags" in the PACF is also inconsistent with the overall conclusion of no serial dependence.

### 7. (Major) STL Decomposition Applied to Non-Stationary Price Series with Artificial Frequency

Section 3.2 applies STL decomposition to closing prices (not returns) with `frequency = 252` (trading days per year), treating this as a meaningful seasonal period. Stock prices have no genuine annual seasonal cycle; the "seasonal" component produced is an artifact of the period choice. The authors acknowledge this but still produce and interpret the decomposition, concluding that "seasonal component appears minimal." Using STL on raw prices obscures any real structure and is not an appropriate diagnostic for either the modeling choices or the stationarity discussion.

### 8. (Minor) GARCH Summary Statistics Are Hidden (`include=FALSE`)

The GARCH(1,1) and GJR-GARCH model fitting chunks (Sections 4.2 and 4.3) use `include=FALSE`, meaning parameter estimates, significance tests, and model fit statistics are never shown in the rendered output. Only the conditional volatility plots are visible. Readers cannot verify parameter estimates, convergence, or whether the leverage parameter $\gamma$ is statistically significant for NFLX or SPY.

### 9. (Minor) Beta Confidence Interval Formula Is Incorrect

Section 7.4 computes the standard error of beta as `sqrt(var(NFLX) / (n * var(SPY)))`. This formula is not the standard OLS standard error for a regression coefficient; the correct OLS SE for beta in a simple regression of $R_{\text{NFLX}}$ on $R_{\text{SPY}}$ is $\hat{\sigma}_\epsilon / (\hat{\sigma}_{\text{SPY}} \sqrt{n})$ where $\hat{\sigma}_\epsilon$ is the residual standard deviation. The formula used ignores the residual variance and will produce overconfident (narrow) intervals. The authors report the interval as further "support" for beta > 1, but this confidence interval is not reliable.

### 10. (Minor) Incomplete Comment Left in Published Writeup

Section 8.2 contains an unresolved placeholder comment: "We extended the analysis beyond classical GARCH by incorporating asymmetric volatility modeling. Add direct discussions of how we expanded on the previous projects." This text is visible in the rendered HTML and indicates the discussion section was not finalized before submission.

### 11. (Minor) Global Search Box for `phi` Restricts Range to (0.9, 0.999), Excluding Best Local-Search Region

The global search sets `phi` bounds at (0.9, 0.999), but the highest-likelihood local search solutions have `phi` around 0.75–0.89 (e.g., rows with logLik ~4622 have phi of 0.752–0.822). The global box thus excludes the empirically best-performing parameter region, making the "global" search misleadingly incomplete. This is a meaningful methodological flaw that likely prevents the global search from finding the true MLE.

### 12. (Minor) No Out-of-Sample Evaluation Despite Defined Holdout Set

A holdout set (2023–2025) is defined at the beginning of the analysis, but it is never used. No out-of-sample RMSE, MAE, or log-score is computed for ARIMA, GARCH, or POMP forecasts against this held-out period. This omission limits the practical conclusions about which model is more useful for prediction.

### 13. (Minor) ARIMA Residual Autocorrelation for SPY Not Addressed

Section 5.3 notes that the Ljung-Box test for the SPY ARIMA model yields a significant p-value (0.03009), indicating remaining autocorrelation in residuals. The authors acknowledge this but take no corrective action, such as increasing the ARIMA order or fitting an ARMA-GARCH model. The paper then proceeds to use ARIMA forecasts without qualification.

### 14. (Minor) Reference 12 Contains a Typo (Wrong URL for NVIDIA Project)

Reference 12 ("Project 11, Winter 2024: NVIDIA Stock Price Analysis") links to `ionides.github.io/531w24/final_project/project07/blinded.html` — the same URL as Reference 11 for Apple Stock Price. The URL for Project 11 should instead point to `project11/blinded.html`. This suggests one or both references are incorrectly cited.

### 15. (Minor) Repeated Code Block for Saving SPY Results

In `blinded.rmd` (lines 772–806), the block that saves `spy_mif` and `spy_params_local.csv` appears twice with identical code. This redundant block suggests incomplete cleanup of the working script before submission and could cause confusion if the file is re-executed.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/blinded.rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/pomp_final.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/nflx_params_local.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/nflx_params_global.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/spy_params_local.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/spy_params_global.csv`
