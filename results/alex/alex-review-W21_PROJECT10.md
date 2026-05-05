# Peer Review: W21 Project 10 — Time Series Analysis of COVID-19 in Georgia

---

## Summary

This project analyzes COVID-19 case and vaccination data for the state of Georgia using both ARMA/ARIMA models and SEIR-based POMP models. Three variants of an SEIR model incorporating vaccination are proposed and assessed through simulation only. The project demonstrates some creative modeling ideas but has serious methodological gaps, especially the complete absence of likelihood-based inference for the POMP models.

---

## Weaknesses (Most Critical First)

### 1. [Major] No Likelihood-Based Inference Performed for Any POMP Model

The entire POMP analysis consists only of forward simulations with hand-tuned parameters. No particle filter is run on the actual data in any executed (non-`eval=FALSE`) code block, no likelihood is reported, and no confidence intervals or uncertainty estimates are produced. The authors openly acknowledge in the Appendix that local search attempts produced `-Inf` log-likelihoods, but no working solution is presented. Without any likelihood evaluation, there is no statistical justification for the chosen parameter values, and the POMP section provides no inferential content whatsoever.

### 2. [Major] No Parameter Estimation — All Parameters Are Hand-Tuned

All parameters (Beta, mu_EI, mu_IR, rho, eta, and vaccination terms) are set manually and justified only by back-of-envelope reasoning or literature references. There is no local search (mif2), no global search (multi-start mif2), and no profile likelihood. Consequently, there is no demonstration that the chosen parameters are optimal or even well-identified, and the simulation results cannot be interpreted as statistical fits.

### 3. [Major] Bug in Model 3: N_SV Drawn from I Instead of S

In the mathematical description of Model 3 (Section 4.2.3), the vaccination transition is written as:
```
N_{SV} = binomial(I, 1 - exp(-mu_SV * dt))
```
This is a transcription error in the equations — the vaccinated individuals should be drawn from the susceptible compartment S, not the infectious compartment I. The C code implementation correctly draws from S (`rbinom(S, 1-exp(-mu_SV*dt))`), but the mathematical writeup is inconsistent. This type of error undermines confidence in the correctness of the mathematical model description.

### 4. [Major] Binomial Measurement Model Is Almost Certainly the Source of -Inf Log-Likelihoods (Unresolved)

The measurement model uses `dbinom(reports, H, rho, give_log)`, where `H` is the accumulated number of recoveries (infections resolved). Because `H` is a continuous (non-integer) quantity accumulated via Euler steps with sub-daily delta.t = 1/8, the binomial density `dbinom` will frequently return `-Inf` when `H` is not an integer or when `reports > H`. This is the almost certain cause of the `-Inf` log-likelihoods described in the Appendix. The negative binomial attempt in the Appendix uses `dnbinom(reports, H, rho, give_log)` which also uses `H` as the `size` parameter incorrectly. Neither attempt is corrected or resolved in the main body of the report. A `dnbinom_mu` parameterization (or rounding H to an integer) would be the standard fix.

### 5. [Major] Data Window Choice Is Unexplained and Potentially Cherry-Picked

The POMP models use only a 105-day window (days 299–409 of the daily series, i.e., rows corresponding to approximately November 2020 through mid-February 2021) without justification. The entire pandemic time series for Georgia contains 413 observations. The selection of this window appears designed to capture a "nice" wave but is not motivated by epidemiological reasoning or data quality concerns, and no sensitivity analysis to this choice is provided.

### 6. [Major] Duplicate Introduction Section Content

Section 2.1 ("Data description") is verbatim identical to text already presented in Section 1 ("Introduction"). Two complete paragraphs — describing the NYT and OWID data sources and the Georgia dataset size — appear word-for-word in both sections. This signals poor editorial review and inflates the length of the report without adding content.

### 7. [Major] LRT Degrees of Freedom Are Wrong

The likelihood ratio test comparing ARIMA(1,1,1) to ARIMA(4,1,4) uses `pchisq(delta_ll, 2, lower.tail=F)`, implying 2 degrees of freedom. However, ARIMA(4,1,4) has 8 parameters (ar1, ar2, ar3, ar4, ma1, ma2, ma3, ma4) and ARIMA(1,1,1) has 2 parameters (ar1, ma1), so the difference is 6 degrees of freedom, not 2. This error makes the p-value reported invalid (it is anti-conservative) and the stated conclusion unreliable.

### 8. [Major] ARMA Model for COVID Cases Uses Wrong Data Split

The ARIMA model for COVID cases is fit on `pre_vac_data` (cases before the first fully vaccinated observation), and then the regression with vaccination as covariate is applied to `post_vac_data` only. However, ARIMA coefficients estimated on the pre-vaccination regime are directly applied to the post-vaccination data without re-estimation or any justification for why coefficients from one epidemiological regime should govern the other. This approach is methodologically problematic.

### 9. [Minor] Susceptible Population Calculation Conflates Cumulative Cases with Active Immunity

The EDA susceptible population formula subtracts `cases` (cumulative confirmed cases) as a proxy for individuals who have recovered and are immune. This is a rough approximation that ignores: (a) deaths from COVID-19 already counted in `cases`, causing double-subtraction with the `deaths` term; (b) potential waning immunity; (c) reinfection. The `deaths` term is explicitly subtracted separately, which creates a double-count for COVID deaths (they are included in both `cases` and `deaths`).

### 10. [Minor] Vaccination Rate in Models 1 and 2 Is Hard-Coded, Not a Fitted Parameter

In Models 1 and 2, vaccination is a fixed constant (2500 or 2200 + index*4 per Euler step) embedded directly in the Csnippet with no corresponding parameter. This means it cannot be estimated, included in a likelihood search, or assigned uncertainty. Making it a named parameter would be trivial and necessary for any real inference.

### 11. [Minor] Model 2 Uses `index` as a State Variable Incorrectly

The `index` counter in Model 2 is declared as a state variable in `statenames`, but it is a deterministic time counter, not a stochastic state. This is conceptually wrong and can interfere with particle filtering (each particle would track its own `index`, which would all be identical, wasting memory). A covariate table or use of `t` directly in the Csnippet would be more appropriate.

### 12. [Minor] The Quadratic Vaccination Fit Is Presented as an Inferential Finding Without Residual Diagnostics

The quadratic model for cumulative vaccinations is fit and its coefficients are reported, but no residual diagnostics (residual plots, normality check, ACF of residuals) are shown. For a time series context, ignoring autocorrelation in residuals is a notable omission that could invalidate standard errors on the quadratic coefficients.

### 13. [Minor] AIC Table Search Reaches Upper Boundary Without Expanding

For the vaccination ARIMA analysis, the authors note that the most complex model (AR5, MA5) has the lowest AIC but is at the upper bound of the search. Standard practice is to expand the grid when the optimum occurs at the boundary. The authors dismiss this without a principled argument, and the selection of ARIMA(4,1,4) over AR5/MA5 is not formally justified.

### 14. [Minor] No Diagnostics for the ARIMA Models

For all fitted ARIMA models (both vaccination and cases), there are no residual diagnostics presented — no ACF/PACF of residuals, no Ljung-Box test, and no residual normality checks. This is standard practice for ARIMA analysis and its absence makes the model adequacy claims unverifiable.

### 15. [Minor] Live URL Data Downloads Create Reproducibility Risk

The code reads data directly from live GitHub URLs (`https://raw.githubusercontent.com/nytimes/...` and `https://raw.githubusercontent.com/owid/...`). Both repositories continue to be updated, so the data fetched today may differ from the data used in the report. While the project also includes local CSV files, the main ARMA and POMP code blocks pull from the live URLs rather than the local files. This threatens reproducibility.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project10/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project10/us-states.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project10/us_state_vaccinations.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project10/Makefile`
