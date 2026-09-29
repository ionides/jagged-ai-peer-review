# Peer Review: W24 Project 11 — NVIDIA Stock Price Analysis with ARMA, GARCH, and POMP Models

**Reviewer:** Charlie  
**Date:** 2026-09-28  
**Semester:** W24  
**Project:** 11

---

## Summary

This project analyzes NVIDIA Corporation daily stock prices (January 2022 – April 2024) using three modeling frameworks: ARMA, ARMA+GARCH, and a stochastic volatility POMP model for the daily log-returns. The authors correctly identify heavy-tailed residuals from the ARMA(0,0) model as motivation for GARCH and POMP approaches, and they apply the iterated filtering (mif2) framework for POMP inference. Key strengths include the use of logmeanexp-based likelihood evaluation after mif2, a global search from a parameter box, and explicit acknowledgment of partial non-convergence. However, the analysis has serious weaknesses: no profile likelihoods are computed for any POMP parameter, convergence failures for two key parameters are noted but not addressed, a factual error corrupts the conclusion's likelihood comparison, a hard-coded local file path prevents reproduction, and the ADF test null hypothesis is stated backwards throughout.

---

## Major Issues

### 1. No profile likelihood computed for any POMP parameter (CC-Yes, Error 1.9)

The project proceeds directly from iterated filtering to a conclusion without computing profile likelihoods for any parameter. Parameter identifiability is never assessed, and no confidence intervals are reported for any of the six POMP parameters (sigma_nu, mu_h, phi, sigma_eta, G_0, H_0). Profile likelihoods are the course-standard method for constructing valid confidence intervals for noisy particle filter likelihoods, and their absence means it is impossible to know whether the reported point estimates are reliable or whether parameters are identifiable from this dataset. The observation that sigma_nu converges to approximately zero and mu_h fails to converge makes identifiability particularly pressing. This is a course-confirmed error (Q10-02) and should be remedied by computing profile likelihoods for at least the key structural parameters (phi, sigma_eta, mu_h).

### 2. Convergence failure for two parameters acknowledged but not addressed (CC-Yes, Errors 1.5 and 1.8)

The report explicitly states "mu_h, H_0 do not converge" after the local search and then proceeds to the global search without diagnosis or structural revision. The global search summary shows no improvement over the local maximum (both reach logLik = 1111). Per course instruction (Q10-01), when parameters fail to converge while the likelihood has plateaued, this is a signal of model misspecification or unidentifiability — not a simple indication that more iterations are needed. The authors' response ("necessitating further iterations for evaluation") contradicts this teaching. The appropriate next step is to examine whether mu_h and H_0 are identifiable (via profile likelihood) or whether the model needs structural revision.

### 3. Factual error in conclusion: wrong log-likelihood attributed to ARMA(0,0)

The conclusion states "ARMA(0, 0) give us the likelihood of 1092." However, the ARMA(0,0) log-likelihood is reported as 1087.62 earlier in the report (`log-likelihood for ARMA(0, 0): 1087.61849681041`). The value 1092 is the log-likelihood of the ARMA(0,0)+GARCH(1,1) with normal error, a model the authors had already discarded. This inflates the apparent gap between ARMA(0,0) and the POMP model in the conclusion. All three model comparisons in the conclusion are therefore mislabeled, undermining the final model selection argument.

### 4. Hard-coded absolute file path prevents reproducibility

The Rmd file contains `setwd("/Users/huanglingqi/Desktop/Stats 531 Final Project")` at the top of the data-loading chunk. This path exists only on the authors' machine. Any attempt to knit the document on another system will fail at the data loading step. Per the code supplement checklist, hard-coded paths to the author's local filesystem are a reproducibility red flag. The fix is to use a relative path (e.g., `read.csv("NVDA.csv")`) and ensure the data file is included alongside the Rmd.

### 5. ADF test null hypothesis misstated (CC-Yes, Error 2.3)

The text reads: "we see that the test-statistic is about -7.16 and the p-value is less than 0.01, which suggest we keep the null hypothesis that our time series is stationary." The ADF test's null hypothesis is the presence of a unit root (non-stationarity), not stationarity. A p-value < 0.01 means rejecting the null (rejecting the unit root), which supports stationarity. The authors arrive at the correct conclusion but state it using language that reverses the null and alternative hypotheses. This suggests a fundamental misunderstanding of the test being applied.

### 6. Minimum-AIC model not selected or discussed

The AIC table shows that ARMA(2,2) achieves AIC = -2173.11, which is 1.87 units lower than ARMA(0,0)'s AIC of -2171.24, making ARMA(2,2) the model favored by AIC. The authors state they identified "ARMA(0,0), ARMA(0,1), and ARMA(1,0) as potential feasible models" and never discuss ARMA(2,2). The likelihood ratio test was conducted only for ARMA(1,0) and ARMA(0,1) relative to ARMA(0,0), not for ARMA(2,2). Since AIC already penalizes for complexity, selecting a higher-AIC model without justification conflicts with the stated criterion. A full analysis should either select ARMA(2,2) or provide a principled reason for preferring ARMA(0,0).

### 7. Likelihood from tseries::garch() compared to fGarch::garchFit() without checking normalization (CC-Yes, Error 2.9)

The simple GARCH(1,1) fit using `garch()` from the `tseries` package yields a reported "likelihood of about 1596," while the equivalent ARMA(0,0)+GARCH(1,1) normal-error model from `garchFit()` in the `fGarch` package yields 1092 — a gap of ~500 log-units for nominally similar models. The `tseries::garch()` function uses a non-standard likelihood convention that is not directly comparable to the standard conditional log-likelihood reported by `fGarch` or `arima()`. The authors dismiss the tseries model because of insignificant coefficients, not because of this normalization discrepancy, suggesting they are unaware of the incompatibility. The likelihood figure of 1596 should not appear in the report without an explicit normalization caveat.

---

## Minor Issues

### 8. No simulation-based diagnostics for POMP model fit

After completing mif2 optimization and reporting a maximum log-likelihood of 1111, the project provides no simulation-based model diagnostics. The fitted stochastic volatility model is never simulated forward to check whether it reproduces the observed volatility clustering, heavy tails, or overall return distribution. Per the POMP checklist (Item 4), simulation from the filtering distribution and comparison to observed data is standard practice for assessing where and how a POMP model succeeds or fails. Without such diagnostics, there is no evidence the fitted model is a reasonable description of NVIDIA return dynamics.

### 9. sigma_nu converges to approximately 0 — leverage effect absent but uninterpreted

The local search reports "sigma_nu stabilizes at 0." Since sigma_nu controls the variance of the Gaussian random walk for the leverage process G, a value near zero effectively eliminates the leverage dynamics from the model, making G constant. This is potentially an important substantive finding — that a leverage effect is not present in NVIDIA returns over this period — but the authors do not discuss or interpret it. An estimate at or near a boundary of the parameter space is also a potential signal of model misspecification (analogous to Wheeler et al. 2024, §Parameter identifiability) and warrants examination via a profile likelihood for sigma_nu.

### 10. Global search box excludes the region where local search found its MLE

The local search finds sigma_eta converging to approximately 5, but the global search box sets `sigma_eta = c(0.5, 1)`. The MLE from the local search lies far outside the global search box for this parameter. As a result, the global search likely cannot explore the parameter region known to have high likelihood, and the "global" search is not truly global for sigma_eta. That the global maximum equals the local maximum (both logLik = 1111) is consistent with the global search failing to find the same solution independently, rather than confirming convergence from diverse starting points.

### 11. Likelihood comparisons across R packages not verified for consistent normalization

The conclusion compares log-likelihoods from `arima()` (ARMA, 1087.62), `garchFit()` (GARCH, 1120), and `pfilter()` (POMP, ~1111) and treats these as directly comparable. While likelihoods for different models of the same data are in principle comparable, different R packages may include or omit additive constants (e.g., constant terms in the Gaussian log-likelihood). The report does not verify that all three packages use the same normalization convention. A brief check of whether the ARMA and GARCH likelihoods are consistent (e.g., comparing `arima()` vs. `garchFit()` on the same ARMA(0,0) specification) would confirm comparability.

### 12. Section title reads "ARIMA Model Selection" when no differencing is applied

The section heading is "ARIMA Model Selection" but the analysis fits only ARMA models to the log-return series, which is already stationary. No differencing is ever applied (the I component of ARIMA). This mislabeling persists throughout the section. The correct heading is "ARMA Model Selection."

### 13. Likelihood ratio test statistics not shown

The report states "After conducting the two nested hypothesis tests, we conclude that retaining the null hypothesis" but the computed test statistics (`test_stat_1` and `test_stat_2`) are never printed, and no chi-squared p-values are reported. The reader cannot verify whether the rejection threshold was applied correctly or whether the factor-of-2 conversion from log-likelihood difference to the LRT statistic (LRT = 2 × Δloglik) was used. Including `2 * test_stat_1` compared against `qchisq(0.95, df=1)` would make the reasoning transparent.

### 14. GARCH(1,1) dismissed on p-value grounds rather than substantive model evaluation

The authors discard the simple GARCH(1,1) from `tseries` because "the p-value for three coefficient are greater than 0.1." Selecting or discarding models based on individual coefficient p-values conflicts with the AIC/likelihood framework used elsewhere in the report. A model with higher likelihood is a better fit by the stated criterion regardless of individual coefficient significance. The stated reason for discarding the model is also internally inconsistent: if insignificant coefficients were grounds for rejection, the ARMA(0,0) model's intercept (which has no formal significance test) would require the same scrutiny.

### 15. Shapiro-Wilk test applied to raw GARCH residuals rather than standardized residuals

When validating the ARMA(0,0)+GARCH(1,1) normal model, the authors apply Shapiro-Wilk and Jarque-Bera tests to the GARCH residuals (epsilon_n) and conclude they are non-normal. The correct diagnostic for a GARCH model is to examine the standardized residuals z_t = epsilon_t / sigma_t, which should be approximately iid N(0,1) if the model is correctly specified. Raw residuals epsilon_t are heteroskedastic by construction in a GARCH model and will appear non-normal even when the model fits well. Using raw residuals for this test leads to a misleading rejection.

---

## Files Consulted

### Skill Files

- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

### Project Files

- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project11/Stats 531 Final Project.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project11/blinded.html`
