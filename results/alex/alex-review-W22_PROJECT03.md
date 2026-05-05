# Peer Review: W22 Project 03 — Subscriber Analysis (Twitch Streamer POMP Model)

## Summary

This project analyzes monthly subscriber counts for a Twitch streamer (Felix "xQc" Lengyel) from March 2017 through March 2022 using both ARIMA and a custom POMP compartmental model. The writeup is extremely brief (7 pages of PDF plus a 5-page browser-rendered HTML snippet for the POMP section) and suffers from fundamental methodological errors in the POMP model construction, inadequate reporting, and an incomplete analysis. Issues are listed below in descending order of severity.

---

## Major Weaknesses

### 1. The POMP Process Model Does Not Actually Update the State Variable S

**Severity: Critical**

The rprocess step (`bvs_step`) only updates `Beta` (via a random walk) and `D` (departures from S via a binomial draw). The subscriber count `S` itself is never updated within the process model. The covariate table supplies a lagged version of `S` from the data rather than from the latent state. This means the latent state evolution is not self-contained: the model is effectively using observed data as a covariate to drive itself, which defeats the purpose of a state-space model. A proper POMP model must propagate S forward as a latent state within the process simulator.

```c
// bvs_step — S is never incremented or decremented
Beta=expit(logit(Beta)+rnorm(0, Beta_sigma));
D=rbinom(S,1-exp(-mu_SB));
```

### 2. The Measurement Model (`dmeas`) Uses `rbinom` — a Random Draw — Instead of a Deterministic Density

**Severity: Critical**

The `bvs_dmeas` Csnippet calls `rbinom(N-S, 1-exp(-Beta*S/N))` to generate `Views` and then evaluates a normal density against it. Because `rbinom` is a random draw, the computed likelihood is stochastic and non-reproducible across particle evaluations, making the particle filter mathematically invalid. The `dmeasure` component must compute a deterministic conditional density p(y | x, theta), not simulate random intermediate quantities.

### 3. No Convergence Diagnostics for the Iterated Filtering (IF2) Run

**Severity: Critical**

The project runs `mif2` with Np=2000 and Nmif=100 for a local search, and then a global search, but presents none of the standard convergence diagnostics: no trace plots of log-likelihood or parameters over IF2 iterations, no likelihood profile, no pairs plot of the global search results. Without these, there is no evidence that the optimizer converged or that the parameter estimates are meaningful.

### 4. The Global Search References an Undefined Object `fixed_params`

**Severity: Critical**

In the global search loop, the code calls:
```r
mif2(Nmif=25, params=c(guess, fixed_params))
```
but `fixed_params` is never defined anywhere in the submitted code. This means the global search code cannot run as written and likely threw errors silently (via `try(..., silent=TRUE)`), so the reported log-likelihood of -866.06 may be from the local search only, or may be entirely invalid.

### 5. AIC Comparison Between ARIMA and POMP Log-Likelihoods Is Invalid

**Severity: Major**

The paper concludes that "the ARMA model performs better than the POMP model" by comparing the POMP log-likelihood (-866.06) against the ARMA AIC table. These quantities are not on the same scale: the ARIMA is fitted on the log-differenced series, while the POMP model is fitted on the raw subscriber counts. A valid comparison would require computing the log-likelihood of the ARIMA model on the same scale and observation space as the POMP model, or using AIC computed from the POMP particle filter likelihood.

### 6. The Transformation Applied Before ARIMA Is Mathematically Inconsistent

**Severity: Major**

The data pre-processing takes a first difference and then applies a logarithm: `log(diff(Subscribers))`. However, the first difference of subscribers can be negative (as visible in the diff plot, which shows values below -10,000). The logarithm of a negative number is undefined. The paper does not acknowledge this problem, and the resulting log-diff series shown in the plot has a minimum near 0, suggesting either the authors used a different transformation (e.g., log of subscribers then diff, or clipping negatives) without disclosing it, or encountered unacknowledged NaN values.

### 7. The ARIMA Model Order Claimed Does Not Match the Transformation

**Severity: Major**

The paper states "ARIMA(1,1,2) is the best with the smallest AIC," but the AIC table is computed on the log-differenced series — a series that has already been manually differenced once. Fitting an ARIMA with d=1 on an already-differenced series applies two differences to the original data. The correct model designation would be ARIMA(1,0,2) on the differenced series, equivalent to ARIMA(1,1,2) on the log-subscribers. This confusion is never resolved.

### 8. No POMP Model Diagnostics — No Effective Sample Size, Filter Convergence, or Simulation Checks

**Severity: Major**

Beyond the single simulation plot and the final log-likelihood number, the POMP analysis presents no diagnostics: no effective sample size (ESS) over time from the particle filter, no filter mean trajectories compared to the data, and no examination of whether the particle filter is degenerating. The simulation plot alone (which shows plausible-looking trajectories) is insufficient to validate the model.

### 9. The Compartmental Model Structure Is Not Justified or Formally Defined

**Severity: Major**

The BVS (Beginning-Viewers-Subscribers) compartmental model is described only in prose. There is no mathematical formulation, no diagram of compartment flows, no statement of what the state space is, and no justification for why this particular compartmental structure is appropriate for Twitch subscriber dynamics. The parameter N (total number of users = 41,500,000) is fixed with no explanation of where this number comes from or what population it represents.

### 10. The R-squared Value Reported for ARIMA Is Meaningless

**Severity: Major**

The coefficient table for the ARIMA(1,1,2) model reports R2 = 0.983. R-squared is not a standard or meaningful diagnostic for ARIMA models; it typically reflects the model's ability to fit the cumulative level (which trivially improves with differencing and integration). The paper presents this as evidence of good fit without acknowledging that residual diagnostics (ACF, QQ plot) are the appropriate tools for ARIMA validation.

---

## Minor Weaknesses

### 11. The Residual ACF Plot Shows Significant Autocorrelation at Lag 0 = 1.0 but the Y-axis Range Is Misleading

**Severity: Minor**

The residual ACF plot in Section 2.3 shows the ACF scale going from -0.2 to 1.0, with lag 0 at 1.0 (correct). However, several lags (approximately lags 2-4) appear to reach close to the 95% confidence bound. The paper claims "ACF plot shows a white noise process" without any formal test (e.g., Ljung-Box), which overstates the quality of the residual fit.

### 12. The Data Is in Reverse Chronological Order in `twitch.csv` but Appears Correctly Ordered in `twitch2.csv`

**Severity: Minor**

The raw `twitch.csv` file lists data from March 2022 down to March 2017 (most recent first), while the analysis-ready `twitch2.csv` is chronologically ordered. The paper does not mention this reversal or the data cleaning step that produced `twitch2.csv`, leaving reproducibility questions about how the transformation from one to the other was done.

### 13. The Paper Does Not Report Estimated Parameter Values from the Final POMP Fit

**Severity: Minor**

After running the global search, the paper reports only the log-likelihood (-866.06) and does not report the estimated values of Beta_sigma, mu_VS, mu_SB, Beta_0, or N from the best-fitting run. Without these, it is impossible to interpret the scientific content of the POMP model.

### 14. The Title Contains a Spelling Error and the Writeup Is Extremely Terse

**Severity: Minor**

The title reads "Subsciber Analysis" (missing a 'r'). The conclusion section for the ARMA model (Section 2.4) is a single sentence and the POMP conclusion is two sentences. The overall writeup is far too brief for a final project: the POMP section is embedded in a browser-rendered HTML file rather than a proper PDF section, suggesting the project was submitted in an incomplete state.

### 15. The Spectral Analysis Is Conducted on the Wrong Series

**Severity: Minor**

The periodogram in Section 2.2 is labeled "Series: x" and uses an unspecified variable `x`. Based on context it appears to be the log-diff series, but the variable name in the plot title and axis label is not tied to the actual data variable name used in the code, making the analysis non-reproducible and hard to verify. Additionally, dismissing seasonality solely on the basis of a raw (unsmoothed) periodogram is insufficient; a smoothed spectral estimate would be more reliable.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project03/blinded.pdf`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project03/twitch.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project03/twitch2.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project03/Makefile`
