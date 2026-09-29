# Peer Review: W25 Project 11
**"Time Series Analysis of Apple Stock Price"**

---

## Summary

This project applies ARMA-GARCH and POMP-based discrete-time stochastic volatility models to Apple Inc. (AAPL) daily log returns from 2020 to 2025. The authors fit a standard GJR-GARCH model and a leverage-effect stochastic volatility model following Bretó (2014), then compare their log-likelihoods. The project demonstrates familiarity with both frameworks and includes convergence diagnostics, profile likelihood analysis, and model selection discussion. However, several serious flaws undermine the analysis: the GARCH diagnostic section is run on the wrong model (eGARCH rather than gjrGARCH), the profile likelihood uses an order of magnitude fewer particles than the main analysis, the profile's upper confidence bound is artificially truncated at the search boundary, and the log-likelihoods being compared derive from different datasets. The local search convergence is also questionable given the authors' own report of a ~100 log-unit spread.

---

## Major Issues

### 1. GARCH diagnostics are run on eGARCH, not the selected gjrGARCH model (CC-Yes)

The selected model for downstream analysis is `gjrGARCH_std`. However, on line 465 of the Rmd, the diagnostic object is assigned as:

```r
model_to_test <- models[["eGARCH_std"]]
```

All statistics reported in the GARCH diagnostics section (skewness, kurtosis, Jarque-Bera test, ARCH-LM test, Ljung-Box tests, Figure 5.1) are therefore properties of the eGARCH-std model, not the gjrGARCH-std model. The conclusion "gjrGARCH successfully captures volatility clustering" is stated without any diagnostic evidence for that model. This invalidates the entire diagnostic section for the chosen GARCH model. The authors must re-run diagnostics on `models[["gjrGARCH_std"]]`.

### 2. Profile likelihood evaluated with Np=100 while main analysis uses Np=1000 (CC-Yes, Error 1.9)

The profile likelihood code (line 898) uses:

```r
mf |> pfilter(Np=100) |> logLik()
```

This is ten times fewer particles than the Np=1000 used throughout the local and global searches. With Np=100, the standard error of the particle filter log-likelihood estimate is approximately 3--5x larger than with Np=1000 for typical financial time series, producing a noisy profile on which the confidence interval cannot be trusted. The resulting CI of (0.959, 0.99) is computed from noisy evaluations and should not be reported as a valid confidence interval. The profile must be re-evaluated with at least Np=1000 particles per point.

### 3. Profile likelihood CI upper bound is truncated at the search boundary (CC-Yes)

The phi profile spans `seq(0.85, 0.99, length=10)`, and the reported 95% CI upper bound is 0.99 -- the exact maximum of that grid. This is not a data-derived upper bound; it is the boundary of the search range. When the CI endpoint coincides with the boundary of the parameter grid, the CI is truncated: the true upper bound may extend beyond 0.99. Similarly, the global search box constrains `phi = c(0.5, 0.99)`, meaning neither the optimization nor the profile has explored phi values above 0.99. Since phi is the log-volatility persistence parameter and the MLE appears to cluster near the boundary, the authors cannot exclude the possibility that the true MLE lies at phi > 0.99. The profile must be extended to phi closer to 1 (e.g., 0.999) to determine whether the CI is genuinely bounded below 1.

### 4. Log-likelihood comparison between GARCH and POMP uses different datasets

The GARCH models are fitted to `na.omit(df$log_return)` (line 292), which is the raw daily log-return series. The POMP model is fitted to `deMeanRtn` (line 119, used in line 586), which is `diff(apple_ts) - mean(diff(apple_ts))` -- the mean-centered log-return series. Because the two likelihoods are evaluated on different data (one mean-centered, one not), the values in Table 7.1 (sGARCH: 3289.09, gjrGARCH: 3328.37, POMP: 3288.55) are not directly comparable. The log-likelihoods are densities evaluated at different observed values, so the comparison is invalid. To make a valid comparison, both models must be applied to the same dataset with consistent preprocessing.

### 5. Local search convergence is not achieved: ~100 log-unit spread across runs (CC-Yes, Error 1.8)

The authors write (line 695): "the log-likelihood shows good convergence, with a dispersion range of approximately 100 log units." A 100 log-unit spread across replicate searches is not convergence -- it indicates that many runs are far from the optimum and the reported maximum may not be near the MLE. Course convention requires that multiple independent searches reach similar terminal log-likelihoods (within a few units) before conclusions can be drawn. The very wide spread likely reflects Nmif=50 being insufficient (the run_level=2 standard is 100 iterations). The global search and profile likelihood built on top of this unconverged local search inherit this problem. The authors acknowledge the issue but dismiss it without remediation.

### 6. Profile likelihood too sparse: only 10 grid points across a narrow range (CC-Yes, Error 1.9)

The phi profile evaluates only 10 values across [0.85, 0.99]. The authors' own text states "only a few points falling within this interval," meaning the CI is derived from fewer than 5 observations above the Wilks cutoff. A profile with so few points in the confidence region cannot reliably locate the profile maximum or bound the CI endpoints. Furthermore, the range [0.85, 0.99] excludes the lower tail (no points between 0.5 and 0.85) and hits the upper boundary as discussed in issue 3. At run_level=2, at least 15--20 profile points distributed across a well-chosen range are needed to support a credible CI.

---

## Minor Issues

### 7. Figure caption "Figure 4.2" is used twice

Line 143 assigns the caption "Figure 4.2: ACF plots of Log Returns" and line 230 assigns "Figure 4.2: ARMA Diagnostics Plots." The duplicate numbering makes figure references ambiguous throughout the ARMA section.

### 8. Density plot title says "Gold Prices" instead of "Apple Stock Prices"

Line 89 contains `labs(title = "Density Plot of Gold Prices", ...)`. This is evidently a copy-paste artifact from a template or another project. The title should refer to Apple stock prices.

### 9. Pairs plot threshold is 100 log units, reducing diagnostic utility

The local search pairs plot (line 726) uses `logLik>max(logLik)-100` as the filter. Given the 100 log-unit convergence spread, this effectively includes all runs and obscures the parameter patterns near the optimum. A tighter threshold (e.g., 20 log units) would better reveal the structure of the likelihood surface near the MLE.

### 10. Simulation code in evaluation section ignores simulated data

Lines 821--829 simulate 50 datasets from the model (`sims <- simulate(...)`) but the subsequent `sapply` call `function(sim) { logLik(pfilter(apple.filt, params=current_params, Np=apple_Np)) }` never uses its `sim` argument. The code runs 50 independent particle filter evaluations of the original data, not 50 evaluations of 50 simulated datasets. The text claiming "we simulated each set 50 times" (line 852) misrepresents this. While the resulting `logmeanexp` of 50 pfilter runs is a valid likelihood estimate, the description is misleading.

### 11. Profile analysis limited to phi; other parameters not assessed for identifiability

The authors raise identifiability concerns throughout but profile only phi. Parameters such as `mu_h`, `sigma_eta`, and `sigma_nu` are not profiled, leaving their identifiability entirely unassessed. Even a coarse profile for `sigma_eta` (directly related to the leverage effect) would strengthen the analysis.

### 12. Model selection narrative for ARMA is inconsistent

Section 4.1 states ARMA(1,1) was selected "due to its relatively low AIC value and simple structure" and notes ARMA(4,4) also has "very low AICs." However, the printed AIC table is not visually shown in full detail in the rendered text -- the reader cannot verify that ARMA(1,1) is genuinely the parsimony-optimal choice or assess the magnitude of the AIC differences between models. The authors should display the AIC table clearly and confirm that ARMA(1,1) is preferred over all sub-models by a reasonable margin.

### 13. Nmif=50 is below the run_level=2 standard of 100 iterations

The run_level switch sets Nmif to 50 (line 622), which is between the run_level=1 value of 10 and the run_level=2 standard of 100. The authors do not explain why 50 iterations were used rather than 100. Given the convergence problems observed (issue 5), using the full 100 iterations may have substantially improved performance. This choice should be justified.

### 14. No out-of-sample evaluation or forecasting exercise

The project compares in-sample log-likelihoods only. Given the stated goal of understanding "forecasting stock price volatility," no out-of-sample forecast evaluation is performed. At minimum, a brief rolling-window or train/test split analysis would strengthen the claim that either model is useful for prediction.

### 15. ARMA model notation inconsistency

The ARMA model equation on line 163 uses $\psi$ in the description ("Terms with $\psi$ are moving average terms") but the equation uses $\theta_j$ for MA coefficients. The two notations are inconsistent and should be harmonized throughout Section 4.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project11/blinded.Rmd`
