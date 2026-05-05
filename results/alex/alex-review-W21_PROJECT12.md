# Peer Review: W21 Project 12 — Analysis on Nasdaq-100 Index for the Past 5 Years

---

## Summary

This project applies ARMA, GARCH, and a POMP stochastic volatility model with leverage (following Breto 2014) to the Nasdaq-100 daily closing prices from April 2016 to April 2021. The report is structured logically and covers the main modelling pipeline. However, there are substantial weaknesses in the POMP implementation, parameter interpretation, convergence diagnostics, and basic data handling that undermine the reliability of the conclusions.

---

## Weaknesses (prioritised from most to least critical)

### 1. [Major] Estimated `mu_h` lies far outside the search box — convergence not achieved

The global search box for `mu_h` is `(-1, 0)`, yet both the local and global MIF2 runs converge to `mu_h ≈ -9.64` (local) and `mu_h ≈ -9.97` (global). A best-fit parameter that sits far outside the search region is the clearest indicator that the optimizer has not converged and that the box was misspecified. The text does not acknowledge this inconsistency at all; instead it claims "the POMP stochastic volatility model performs well." This is the most critical flaw in the analysis.

Similarly, `H_0 = -4.37` is reported as the global best estimate, yet the global box upper bound for `H_0` is `-1` (lower bound `-3.5`), so the best estimate also lies outside the box on the other side.

### 2. [Major] No MIF2 convergence diagnostics (trace plots) are shown

For a POMP analysis centred on iterated filtering, the standard requirement is to display trace plots of log-likelihood and each parameter across MIF2 iterations. These plots allow the reader to judge whether filtering has converged. No such plots appear anywhere in the report. Without them, it is impossible to verify that the 200 iterations of MIF2 were sufficient or that the algorithm did not stall.

### 3. [Major] No likelihood evaluation for the simulated data ("pf1") is reported

Section "Filtering for simulated data" runs a particle filter on the simulated data but the text then simply states "The log likelihood seems to be very low" without actually displaying `L.pf1`. This evaluation step is important for confirming that the model and filtering code are internally consistent (i.e., that particle filtering can recover a reasonable likelihood when the true parameters are known). Omitting the numerical result makes the simulation study uninformative.

### 4. [Major] Global search uses only `if1[[1]]` as the MIF2 template, defeating the purpose of global search

The global search code reads:

```r
if.box <- foreach(i=1:ndx_Nreps_global, ...) %dopar%
  mif2(if1[[1]], start=apply(ndx_box,1,function(x)runif(1,x)))
```

Inheriting settings (particularly `rw.sd` and `cooling.fraction.50`) from a single local-search result (`if1[[1]]`) is appropriate, but the `start` argument should override all parameters with fresh random draws. The code does pass `start=`, so the starting values are randomised; however `if1[[1]]` has already cooled its perturbation schedule, meaning the random-walk perturbation sizes at the beginning of the global run may be smaller than intended. Best practice is to build a fresh `mif2` object from the base filter `ndx.filt` for global search, not from a locally-warmed chain.

### 5. [Major] Inconsistent use of `dmrt` vs. `dmean_z` across model sections

Two distinct demeaned return series are computed:
- `dmrt` (line 48): computed from `data_ts` (a `ts` object constructed with `frequency=365`)
- `dmean_z` (line 69): computed from `close_price` directly with `diff(log(close_price))`

The ARMA and GARCH models use `dmean_z`, while the POMP model uses `dmrt`. Because `data_ts` has `frequency=365` applied to trading-day data (≈252 observations per year), the two series are numerically identical in values but carry different time attributes. The inconsistency is confusing and suggests a lack of coordination; the text does not explain why different objects are used.

### 6. [Major] `frequency=365` applied to trading-day data is incorrect

The `ts` object is constructed with `frequency=365` for data that only includes trading days (approximately 252 per year). This misrepresents the sampling structure and would cause any seasonal decomposition or time-based plotting using that `ts` object to be misleading. The second EDA plot labels the x-axis "Working days" without indices, which hides the problem, but the underlying `ts` specification is wrong.

### 7. [Major] `mu_h` is not correctly referenced in the initial simulation description

The text states the initial parameters are `sigma_nu=0.01, mu_h=0, phi=0.95, sigma_eta=7`, but the code sets `phi=0.995` (not 0.95) in `params_test`. This discrepancy between description and code is not explained.

### 8. [Minor] No parameter interpretation is provided for the POMP model results

The conclusion claims "the estimated parameters for the POMP stochastic leverage model are easier to interpret in financial studies," but no interpretation is actually offered. The estimated values (`sigma_nu ≈ 8.7e-4`, `mu_h ≈ -9.97`, `phi ≈ 0.971`, `sigma_eta ≈ 1.38`) are reported but never discussed in terms of their financial meaning — e.g., what `mu_h ≈ -10` implies about the unconditional volatility level, or whether `phi ≈ 0.97` indicates high volatility persistence. Given that `mu_h` is so far from the plausible range established during search, interpreting it would also reveal the convergence problem.

### 9. [Minor] AIC comparison across ARMA, GARCH, and POMP is potentially non-comparable

The ARMA AIC is computed on `dmean_z` using `arima()`, the GARCH AIC is computed manually from the `tseries::garch()` log-likelihood, and the POMP log-likelihood comes from `pfilter` on `dmrt`. The paper does not verify that all three are evaluating the same conditional likelihood (i.e., the same data, same observation model). In particular, the ARMA AIC is computed with a Gaussian observation model, while GARCH uses a numerical approximation. Direct AIC comparison is only valid if the likelihoods are calculated over the same observations with the same observation density.

### 10. [Minor] No likelihood profile or confidence intervals for POMP parameters

After the global search, only the single best point estimate is reported, with a log-likelihood standard error from particle-filter replication but no profile likelihood or confidence interval for any parameter. This makes it impossible to judge parameter uncertainty or whether parameters are well-identified.

### 11. [Minor] The "Filtering for simulated data" subsection adds little value as presented

The simulation check is described as a way to verify that the filter can recover parameters from simulated data, but the result (`L.pf1`) is never shown, and no re-estimation from simulated data is performed. The section ends with "The log likelihood seems to be very low" followed immediately by moving on to fitting the real data. A proper simulation study would re-estimate parameters from the simulated data and compare them to the generating values.

### 12. [Minor] ARMA model selection rationale partially inconsistent

The text states ARMA(4,3) and ARMA(4,5) are ruled out due to near-unit MA roots, and ARMA(3,1) is chosen. However, the ARMA AIC table lists the lowest value at (4,5) = -7270.120, while ARMA(3,1) has AIC = -7235.88 (visible in the HTML output). The ~34-unit AIC gap is large, and rejecting (4,3) on invertibility grounds is reasonable, but the text does not show the MA roots for (4,3) numerically, only asserting them. A more careful analysis would confirm whether ARMA(3,1) is genuinely close to non-invertible or well within the unit circle.

### 13. [Minor] Incorrect index name throughout — "Nasdaq-500" used in multiple places

The index being analysed is the Nasdaq-100 (NDX), as correctly stated in the title and introduction. However, multiple places in the conclusion and one reference entry repeatedly call it "Nasdaq-500" (which does not exist as a standard index). This is careless and raises questions about whether the authors understand the data they used.

### 14. [Minor] The data-cleaning code uses a hard-coded but unexplained date

The code sets `doy <- strftime("2016-11-04", format = "%j")` to determine the start of the `ts` object, but the data starts on April 11, 2016. The hard-coded date `2016-11-04` is unexplained and different from the actual start date in the CSV. This inconsistency in data handling is not discussed.

### 15. [Minor] Reference [2] is cited as "Breto (2014)" in the model description but the reference list points to course lecture notes

The model is attributed to "Breto (2014)" in the text, and reference [2] is listed as course lecture notes (Ionides, STATS 531). The original Breto (2014) journal paper is not cited. This is an incomplete citation that does not give proper credit to the original source and prevents readers from checking the model specification.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project12/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project12/HistoricalData_1618091005375.csv`
