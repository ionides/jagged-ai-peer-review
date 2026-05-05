# Peer Review: W21 Project 04 — Extended Analysis on the U.S. 10-year Treasury Bond Yield

## Summary

This project applies a stochastic leverage POMP model to monthly differences of the U.S. 10-year Treasury bond yield (1990–2021), comparing it against a GARCH(1,1) benchmark. A secondary strand uses Loess decomposition and the Hodrick-Prescott (HP) filter to examine the yield-CPI relationship. The POMP model achieves a reported best log-likelihood of -25.71 versus -33.89 for GARCH, though the comparison is methodologically flawed in ways described below.

---

## Weaknesses (Most Critical First)

### 1. [MAJOR] Log-likelihood comparison between GARCH and POMP is not apples-to-apples

The paper concludes the POMP model outperforms GARCH because -25.71 > -33.89. However, the GARCH(1,1) log-likelihood is computed on the raw `yield_diff` series via `tseries::garch()`, while the POMP log-likelihood is computed on the same differenced series but under a stochastic leverage model with a *different* probabilistic structure. More critically, the POMP model has 6 parameters while GARCH has 3 (or effectively 3 estimated). Without an AIC/BIC adjustment or a formal likelihood ratio test (which is inapplicable across non-nested model classes), the raw log-likelihood numbers cannot be directly compared to declare a winner. The paper makes no attempt to account for the difference in parameter count.

### 2. [MAJOR] No convergence diagnostics are presented for the MIF2 runs

The project performs local (20 replications) and global (100 replications) iterated filtering but shows only one pairs plot of the local search and one pairs plot of the global search. There are no trace plots of log-likelihood or parameter estimates across MIF2 iterations. Without these, it is impossible to assess whether the algorithm has converged or whether the reported best log-likelihood of -25.71 is near the true maximum. For a POMP-based project, convergence diagnostics are essential.

### 3. [MAJOR] The particle filter on simulated data does not demonstrate model identifiability

Section "Filtering on simulated data" states: "We first checked that we could indeed filter and re-estimate parameters successfully for the simulated data." However, no parameter re-estimation on the simulated data is actually shown — only a log-likelihood estimate (-539.67) is reported. Demonstrating that IF2 recovers the true parameters used to generate the simulated data (e.g., showing estimated vs. true values) is the standard practice to validate identifiability. The section heading implies this was done but the evidence is absent.

### 4. [MAJOR] Simulation from the fitted model is absent

There is no simulation from the fitted POMP model to compare against the observed data. Posterior predictive checks or at least a visual overlay of simulated paths on the actual yield-difference series are necessary to assess whether the model captures key data features (e.g., volatility clustering, tail behavior). The paper explicitly declines to simulate from the GARCH model ("we choose not to do"), but the same omission applies to the POMP model.

### 5. [MAJOR] Missing standard errors or confidence intervals for MLE parameter estimates

The best-fit parameters from the global search are never tabulated with uncertainty quantification. While the pairs plots show scatter of parameter estimates across restarts, no profile likelihood intervals or Monte Carlo standard errors for the point estimates are reported. This makes it impossible to judge parameter precision or identifiability.

### 6. [MAJOR] The log-likelihood of -539.67 for the simulated data particle filter is implausibly large in magnitude and unexplained

The particle filter run on simulated data yields a log-likelihood of -539.67, while the actual data global search yields -25.71. This is an enormous discrepancy (more than 500 log-likelihood units) that is never discussed. For data of length n = 374, such a gap strongly suggests either a coding error (e.g., filtering on a different data object), or an issue with the covariate table setup for `sim1.filt`. At minimum, the authors should comment on why the simulated-data log-likelihood is so much worse than the real-data likelihood.

### 7. [MAJOR] The Loess date axis is incorrectly constructed

In Section 5.1, the date variable is defined as:
```r
date = seq(from=1962, length=length(monthdata$Date), by=1/12)
```
The data starts in January 1990, not 1962. This means the x-axis of the Loess plot is shifted roughly 28 years to the left relative to the actual dates. This is an outright error that affects the frequency response plot and the decomposition plot as well, since the same `date` variable is reused.

### 8. [MAJOR] The CPI data manipulation adds a duplicate row without justification

The code adds an extra row to the CPI data:
```r
cpi[nrow(cpi)+1,] = cpi[nrow(cpi),]
cpi[nrow(cpi),1] = "3/1/2021"
```
The original CSV ends at February 2021 (n = 374 rows matching `monthdata`). A row for March 2021 is manufactured by copying February's value. No justification is given for this imputation, and it introduces a spurious data point into the HP-filter and coherence analyses. It is also inconsistent: the yield data includes March 2021 but the CPI data apparently did not originally.

### 9. [MINOR] The GARCH model output is suppressed with `include=FALSE`

The entire GARCH fitting chunk has `include=FALSE`, so the reader sees only a single sentence summarizing the result. The GARCH model coefficients, their standard errors, residual diagnostics, and the full summary are completely hidden. For an analysis where GARCH is the primary benchmark, this is inadequate transparency.

### 10. [MINOR] The model is closely adapted from course notes without sufficient acknowledgment or modification

The stochastic leverage POMP model (state equations for H and G, the `rproc1`/`rproc2` structure, parameter naming conventions, and even the `params_test` values) is taken almost verbatim from the STATS 531 lecture notes on financial volatility. The adaptation to Treasury bond yields is minimal — essentially substituting `yield_diff` for the returns series used in the notes. The analysis would be strengthened by justifying why this model is appropriate for interest rate data (which has fundamentally different dynamics from equity returns) and by attempting at least one custom extension.

### 11. [MINOR] The global search box for `phi` is restricted to (0.95, 0.99) without justification

The search box for `phi` (AR coefficient on H) is `c(0.95, 0.99)`. This near-unit-root constraint is borrowed from the equity volatility application in the course notes but is not motivated for Treasury bond yield differences. If phi values outside this range are plausible, the global search may be missing better solutions.

### 12. [MINOR] The LRT for yield-CPI association is applied to HP-filtered (already transformed) data without acknowledgment of the statistical consequences

An AR(1) model with an external regressor is fit to HP-detrended yield to test the yield-CPI association. The HP filter itself introduces serial correlation into the filtered series, which inflates the effective sample size and distorts the chi-squared distribution of the LRT statistic. No correction is made or mentioned.

### 13. [MINOR] The monthly data construction uses the first trading day of each month, not the average

The code picks `min(day)` within each month, i.e., the first available trading day. This introduces minor timing noise (the first trading day can vary by up to a week across months). The authors mention choosing monthly data for sample size reasons but do not discuss whether averaging within a month or using end-of-month values might be more representative.

### 14. [MINOR] The title contains a typo: "Yied" should be "Yield"

The document title reads "Extended Analysis on the U.S. 10-year Treasury Bond Yied" — missing the letter 'l' in "Yield." This is a minor presentation error but reflects insufficient proofreading.

### 15. [MINOR] The conclusion conflates number of parameters with model quality

The conclusion states: "The POMP model has a maximized log likelihood of -25.71 with 6 fitted parameters." Using more parameters to achieve a higher raw log-likelihood is not inherently better without a penalty for complexity. The conclusion should either invoke AIC/BIC or explicitly acknowledge that the comparison is informal. As written, the argument could be used to justify any over-parameterized model.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project04/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project04/cpi.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project04/Makefile`
