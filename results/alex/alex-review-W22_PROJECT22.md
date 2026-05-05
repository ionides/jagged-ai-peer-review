# Peer Review: Volatility Analysis on Ethereum (W22, Project 22)

## Summary

This project applies ARCH, GARCH, and POMP models to analyze the daily return volatility of Ethereum (ETH). Three POMP model variants are explored: (1) a leverage-based stochastic volatility model adapted from course notes, (2) a simplified version with the leverage component removed, and (3) a "forced negative" leverage model. The project is readable and follows a coherent progression, but suffers from several methodological, statistical, and presentational weaknesses detailed below.

---

## Weaknesses (Ordered by Severity)

### 1. [Major] AIC Comparison Between GARCH and POMP Is Methodologically Invalid

The paper claims that the POMP model is preferred over GARCH by AIC because the POMP log-likelihood (~2870) is larger than the GARCH(3,4) log-likelihood (~2728). However, these log-likelihoods are computed on fundamentally different scales and with different likelihood definitions. The GARCH log-likelihood from `tseries:::logLik.garch` uses a conditional Gaussian likelihood evaluated on the observed data, while the POMP log-likelihood is a particle-filter-based marginal likelihood estimate. These are not directly comparable quantities, and the difference cannot be converted into a valid AIC comparison. No justification is provided for why these two numbers are on the same scale, and the conclusion that "AIC favors the POMP model" is unsupported.

### 2. [Major] Simplified POMP Model Is Not a Genuine POMP (No Latent State Dynamics)

The simplified model sets sigma_nu = 0 and G_0 = 0, effectively fixing R_n = 0 permanently. The resulting model reduces to a basic stochastic volatility (SV) model in which H_n evolves as an AR(1) with Gaussian noise: `H_n = mu_h*(1-phi) + phi*H_{n-1} + omega_n`. While this is a legitimate model, the paper presents its higher log-likelihood as "surprising" without acknowledging that removing the leverage parameter (which apparently drives sigma_nu toward zero) is motivated empirically but the resulting model eliminates the key distinguishing feature of the original formulation. Furthermore, the simplification is treated as evidence of model improvement without a proper likelihood ratio test to confirm that constraining sigma_nu = 0 does not significantly hurt the fit.

### 3. [Major] No Formal Diagnostic Tests on the Raw Data Prior to Modeling

The EDA section shows only time series plots of price, log-price, and demeaned log-returns. There are no formal stationarity tests (e.g., ADF, KPSS) on the return series, no ACF/PACF plots to characterize serial correlation in squared returns (which would motivate ARCH/GARCH), and no tests for ARCH effects (e.g., Engle's ARCH-LM test). These are standard diagnostics for financial volatility modeling and their omission weakens the justification for the entire modeling approach.

### 4. [Major] Particle Filter Likelihood Estimates Are Not Sufficiently Replicated for Reliable Inference

For all three POMP models, the log-likelihood evaluation uses Nreps_eval = 10 replications and Np = 1000 particles at run_level = 2. For a time series of ~1806 observations with heavy-tailed returns, 1000 particles is on the low end and may produce biased or high-variance likelihood estimates. The standard errors on the log-likelihood estimates are not systematically reported across models in a comparative table, making it impossible to assess whether the observed differences in log-likelihoods across models (which are often only 1-2 units) are statistically meaningful given the Monte Carlo error.

### 5. [Major] Global Search Uses Only a Single IF2 Chain as Seed (Warm-Start Bias)

In all three POMP models, the global search is implemented as:
```
mif2(if1[[1]], params=apply(box,1,function(x)runif(1,x)))
```
This starts all global search chains from the converged state of the first local search chain (`if1[[1]]`), not from fresh random starting points with freshly initialized particle clouds. This is a warm-start approach that can bias the global search toward the local neighborhood already explored, undermining the purpose of the global search. The standard approach is to pass the pomp object (not an mif2 object from a previous run) to each global search chain.

### 6. [Major] Test Set Is Defined but Never Used

At the very beginning of the data processing, the code partitions the data into a training set (rows 1-1806) and a test set (rows 1807-2171). However, the test set variable `test` is never referenced again in the analysis. If the intent was out-of-sample evaluation, it was not carried out. If it was not intended, this unused partition creates a misleading impression of a train/test validation framework that does not exist.

### 7. [Major] "Force Negative" POMP Model Is Poorly Motivated and Scientifically Questionable

The "Force Negative" POMP model fixes G = -0.05 in the Csnippet, making R_n = tanh(-0.05) ≈ -0.05 — a constant slightly negative value — for all time. This is not a meaningful test of the leverage effect. The authors claim this forces R_n to be negative, which is correct, but tanh(-0.05) is very close to zero, making the leverage effect negligible in practice. The model therefore neither removes leverage (like the simplified model) nor meaningfully tests negative leverage. The scientific interpretation provided ("large negative Y_n will always lead to increase in H_n...making the model unstable") is not clearly connected to the near-zero value of tanh(-0.05), and the description in the text claims `sigma_nu = 0` and `G_0 = -0.05` but the Csnippet hardcodes `-0.05` instead of using a parameter, preventing legitimate estimation.

### 8. [Moderate] No Likelihood Ratio Test or Formal Model Selection Between POMP Variants

The paper compares three POMP models but never performs a likelihood ratio test to determine whether the simpler models are statistically preferred. The original full model has 6 parameters, the simplified model has 4 parameters, and the forced-negative model has 4 parameters. A likelihood ratio test (or equivalently, a proper AIC comparison on the same scale) between the full POMP model and the simplified model would be appropriate, since the simplified model is a restricted version (sigma_nu = 0, G_0 = 0) of the original. The differences in log-likelihoods are small (< 2 units) and well within Monte Carlo noise given the standard errors, yet the paper concludes the simplified model is "best."

### 9. [Moderate] Inconsistency in Global Search Box Notation vs. Actual Box

For the Force Negative model's global search, the text states the box is:
`mu_h = c(-7,-6), phi = c(0.7,0.9), sigma_eta = c(0.9,1.1), H_0 = c(-1,1)`
but the actual code uses `mu_h = c(-6.6,-6.2)`, which is a much narrower range. This narrower box reflects information from the local search but contradicts the stated box. The discrepancy is not explained in the text.

### 10. [Moderate] No Profile Likelihood or Confidence Intervals for Key Parameters

The project reports only point estimates (the best MLE from the global search) for all parameters. No profile likelihood confidence intervals are computed for any parameter. This is a significant gap for the key parameters phi (persistence) and sigma_eta (volatility of log-volatility), whose values determine the economic interpretation of the model. Without uncertainty quantification, claims about parameter values are difficult to evaluate.

### 11. [Moderate] GARCH Residual Diagnostics Are Incomplete and Conclusions Are Superficial

The GARCH residual analysis consists only of residual time series plots and Q-Q plots. The conclusion "no obvious patterns in the residuals" and "roughly homoscedastic" is not supported by ACF/PACF plots of the residuals or their squares, which are the standard checks for remaining ARCH effects after GARCH fitting. A Ljung-Box test on squared standardized residuals would be needed to formally assess whether the GARCH models adequately capture the volatility clustering.

### 12. [Moderate] Local Search Convergence Plots Show Non-Convergence but Analysis Proceeds Without Remediation

The text acknowledges that in the original POMP local search, "other parameters don't seem to converge" and "loglik is still fluctuating around 2865 after 100 iterations." Similarly, for the simplified model, "all the parameters are still fluctuating after 100 iterations." Despite this, the global search uses the same Nmif = 100 and does not address the non-convergence. Standard practice would be to increase Nmif or Np at run_level 3, but run_level 3 parameters (Np = 2000, Nmif = 200) are defined but never used.

### 13. [Minor] AIC Table Computes Negative AIC Values (Sign Convention Inconsistency)

The `garch_aic` function computes `2 * length(fit$coef) - 2 * logLik`, which should yield positive AIC values in ordinary use. However, the displayed table shows negative values (e.g., -5262.51 for GARCH(0,1)). This suggests that `tseries:::logLik.garch` returns a negative value (negative log-likelihood), so the AIC is being computed as `2k - 2*(negative logLik) = 2k + 2*|logLik|`, which would be incorrect. This is never addressed, and the sign interpretation is confusing. The GARCH log-likelihood table that follows shows positive values (2712.45), revealing the inconsistency with the AIC table.

### 14. [Minor] Data Provenance and Time Range Description Contains Minor Errors

The text states "the data consist of the daily price of ETH from 2016-03-10 to 2021-02-17," but ETH was released in 2015, making the start date plausible but the end date notable since the training data ends before the sharp price increase starting in 2021 that was mentioned in the introduction. The test set covers the period of this increase but is never analyzed. Additionally, the number of training observations (1806) and returns (1805) are not explicitly stated, making data handling harder to verify.

### 15. [Minor] Lack of Simulation-Based Model Validation (Prediction Intervals)

The simulation plots compare observed returns against a single simulated trajectory from the fitted model. This does not constitute model validation since a single simulation can match the scale of volatility by chance. A proper simulation check would involve generating multiple trajectories and comparing percentile envelopes or using a formal simulation-based test to assess whether the observed data is consistent with the model's predictive distribution.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project22/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project22/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project22/Makefile`
