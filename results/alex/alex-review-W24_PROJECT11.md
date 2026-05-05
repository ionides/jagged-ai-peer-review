# Peer Review: W24 Project 11 — NVIDIA Stock Price Analysis with ARMA, GARCH, and POMP Models

---

## Summary

This project analyzes NVIDIA daily stock log-returns from January 2022 to April 2024 using ARMA, GARCH, and a stochastic volatility POMP model. The modeling pipeline follows a reasonable structure, but the work contains a number of statistical, coding, and interpretive errors that undermine the reliability of reported results. The most critical issues concern incorrect statistical terminology, inconsistent likelihood values in the conclusion, a flawed global search box that contradicts reported convergence values, and incomplete reporting of key results.

---

## Weaknesses (Most Critical First)

### 1. ADF Test Conclusion Is Statistically Incorrect (Major)

The text states: "the p-value is less than 0.01, which suggest we keep the null hypothesis that our time series is stationary." This is doubly wrong. First, the null hypothesis of the ADF test is the *presence* of a unit root (non-stationarity), not stationarity. Second, a p-value below 0.01 leads to *rejection* of the null, not retaining it. The correct statement is: a p-value below 0.01 means we reject the null of a unit root, providing evidence that the series is stationary. The conclusion reached is accidentally correct, but the logic stated is inverted and would mislead any reader.

### 2. Likelihood Values Are Inconsistent Between Sections (Major)

The Conclusion states: "ARMA(0,0) give us the likelihood of 1092." However, the model output shown in the ARMA section reports `log-likelihood for ARMA(0,0): 1087.62`. The value 1092 is actually the likelihood reported for the ARMA(0,0)+GARCH(1,1) with normal errors model, which is presented and discarded in the GARCH section. Additionally, the POMP section records a maximum log-likelihood of 1111 (both local and global search), yet the Conclusion rounds this down to 1110. These inconsistencies suggest that the conclusion was not carefully cross-checked against the actual model outputs.

### 3. Global Search Box Contradicts Reported Convergence Values (Major)

The global search box specifies `sigma_eta = c(0.5, 1)` and `mu_h = c(-1, 0)`. However, the text reports that after the global search, `sigma_eta` converges to approximately 5 and `mu_h` settles around -2. Both of these reported convergence values lie far outside the bounds used in the global search box. This is internally contradictory: MIF2 cannot converge to parameter values outside the search box if the box constrains the initial conditions. The reported convergence values may belong to the local search, or the box boundaries were poorly chosen relative to the true parameter region, and neither case is acknowledged or reconciled in the text.

### 4. GARCH Definition Contains a Notational Error (Major)

The GARCH model definition states: "where {sigma_n} is an iid white noise process with mean 0 and variance of 1." This is incorrect. In the standard GARCH formulation, it is `epsilon_n` (the standardized innovation) that is iid with mean 0 and variance 1; `sigma_n` is the conditional standard deviation (a deterministic function of past values), which is neither iid nor white noise. This error conflates the two distinct components of the GARCH model and could confuse a reader trying to understand the model structure.

### 5. Section Header Mislabeled as "ARIMA Model Selection" (Moderate)

The section performing ARMA model selection is titled "ARIMA Model Selection." No integrated (I) differencing is applied within the section — the analysis is conducted directly on `diff_data` (the log-return series), and models of the form ARMA(p,q) are fitted. Using the label ARIMA is misleading since the differencing was a preprocessing step applied outside the model. The section header should be "ARMA Model Selection."

### 6. LRT Test Statistics Are Computed But Not Reported (Moderate)

The code computes `test_stat_1` and `test_stat_2` (the likelihood ratio test statistics comparing ARMA(1,0) and ARMA(0,1) to ARMA(0,0)), but neither the test statistic values, nor the chi-squared critical values, nor the p-values are shown in the output. The reader is simply told "we conclude that retaining the null hypothesis," with no numerical evidence. For a hypothesis test, the actual test statistic and its comparison to the reference distribution must be reported.

### 7. Global Search Uses Only a Single Starting Chain (Moderate)

The global search code uses `mif2(if1[[1]], params=apply(nv_box, 1, function(x) runif(1,x)))`. All global search runs are warm-started from the single best chain `if1[[1]]` from the local search, rather than being independently initialized with random parameters from the box. This defeats the purpose of global search, which is to explore the full parameter space from diverse starting conditions. The proper approach uses randomized starts based solely on the box, without inheriting optimizer state from a specific local chain.

### 8. GARCH(1,1) Discarded for Wrong Reason (Moderate)

The plain GARCH(1,1) model (fitted with the `garch()` function) is discarded because its coefficients are "not statistically significant." However, the reported likelihood of 1596 is not directly comparable to the other models' likelihoods (approximately 1087–1120) because the `garch()` function from the `tseries` package uses a different normalization convention than `garchFit()` from `fGarch`. The discarding justification based on insignificant coefficients is presented without showing the actual p-values or coefficient standard errors, and the 1596 likelihood figure is never reconciled with the later 1120 figure for what is nominally the same model class.

### 9. Root Interpretation for Causality/Invertibility Is Confused (Moderate)

The text states: "both ARMA(0,1) and ARMA(1,0) appear promising, with their roots located inside the unit circle. This suggests that ARMA(0,1) exhibits invertibility, while ARMA(1,0) demonstrates causality." This description reverses standard conventions. For an AR(1) process, causality requires the root of the AR polynomial to lie *outside* the unit circle (equivalently, |phi| < 1). For an MA(1) process, invertibility requires the root of the MA polynomial to lie *outside* the unit circle. The `autoplot()` of ARIMA objects in R plots the *inverse* characteristic roots, so "inside the unit circle" for the displayed inverse roots means the actual roots are outside — but the text does not acknowledge this and states the condition incorrectly.

### 10. k-Period Log-Return Formula Contains a Typographical Error (Minor)

The formula for the k-period log-return is written as:
`r_t(k) = log(X_t / X_{t-1}) = r_t + t_{t-1} + ... + r_{t-k+1}`

The second term `t_{t-1}` is a typo and should be `r_{t-1}`. Moreover, the right-hand side of the first equality (`log(X_t/X_{t-1})`) is just the 1-period return, not the k-period return; the left-hand side should equal `log(X_t/X_{t-k})`.

### 11. Hardcoded Absolute File Path Prevents Reproducibility (Minor)

The data loading chunk uses `setwd("/Users/huanglingqi/Desktop/Stats 531 Final Project")`, an absolute path specific to one author's machine. This makes the code non-reproducible for any other user without manual modification. The data file path should be relative or a note should be added explaining how to set the working directory.

### 12. Conclusion Incorrectly Attributes Lower Likelihood to ARMA(0,0) (Minor)

The Conclusion says "ARMA(0,0) give us the likelihood of 1092." As noted in point 2, the true ARMA(0,0) log-likelihood is 1087.62. Using 1092 — which belongs to ARMA(0,0)+GARCH(1,1) normal — in the comparative table distorts the apparent gain from adding GARCH components and makes the POMP model look less competitive than it is relative to the ARMA baseline.

### 13. Global Search Box for `phi` Is Overly Narrow Without Justification (Minor)

The global search box constrains `phi` to `c(0.95, 0.99)`. While high persistence is typical in financial volatility models, there is no diagnostic or economic justification provided for ruling out lower values of phi. The local search did not produce diagnostics suggesting phi necessarily lies in this narrow range, and restricting the box this severely can cause the global search to miss alternative regions of the likelihood surface.

### 14. No Discussion of POMP Model Simulation or Diagnostic Checks (Minor)

A POMP model fitting is presented, but there are no diagnostic plots comparing simulated data from the fitted model to the observed log-returns (e.g., a simulated vs. observed trajectory overlay), no effective sample size (ESS) trace plots from the particle filter, and no discussion of whether the fitted latent volatility path is economically interpretable. These diagnostics are standard practice for validating POMP model fits.

### 15. "Daily Log Volatility" Statistic Is Mislabeled (Minor)

The text states: "The daily log volatility, averaging about 0.035." The quantity being described is the standard deviation of the daily log-returns (approximately 0.035), not the "log volatility." Log volatility would refer to the logarithm of the volatility (i.e., log(sigma)), which is a different quantity altogether. This terminological imprecision is minor but reflects a pattern of loose language in the statistical exposition.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project11/Stats 531 Final Project.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project11/blinded.html`
