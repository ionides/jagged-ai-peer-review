# Peer Review: W22 Project 19 — An Analysis of the Omicron Variant of COVID-19 Cases in Wayne County

## Summary

This project applies an ARIMA model and an SEIR POMP model to daily confirmed COVID-19 (Omicron variant) cases in Wayne County, Michigan, covering December 1, 2021 through March 31, 2022. The writing is generally clear and the mechanistic modeling effort is genuine. However, there are a number of significant methodological and reporting issues that undermine confidence in the results.

---

## Weaknesses (prioritized, most critical first)

### 1. [Major] Unfair log-likelihood comparison between ARIMA and SEIR models

The project compares ARIMA(4,1,4) (log-likelihood = -618.74) and SEIR (log-likelihood = -861.13) directly and concludes ARIMA is superior. However, these two likelihoods are computed on different quantities and cannot be compared directly. The ARIMA likelihood is the Gaussian likelihood over the raw or differenced time series with no observation noise model beyond the ARIMA error; the SEIR likelihood is a particle filter estimate of the marginal likelihood under a truncated normal observation model with reporting rate rho. The two models make different observational assumptions over the same data, so a raw log-likelihood comparison is not interpretable as a model selection criterion without careful justification. No AIC or BIC correction accounting for differing numbers of parameters is attempted for the cross-model comparison.

### 2. [Major] Data subsetting inconsistency: title says March 31 but code filters to February 28

The project description consistently states the study period is December 1, 2021 to March 31, 2022 (121 days). However, the ARIMA analysis filters the data as:

```r
data_wayne1 = data_wayne[data_wayne$date >= '2021-12-01' & data_wayne$date <= '2022-02-28',]
```

This cuts the series at February 28, not March 31, producing a 90-day window rather than 121 days. Meanwhile, the SEIR model is fitted to `covid_wayne_winter.csv`, which does contain 121 rows (days 1–121). The ARIMA and SEIR models are therefore fit to different time spans, making the model comparison even less valid. The EDA plots are labeled "12/01/2021 ~ 03/31/2022" but display data only through February 28.

### 3. [Major] Hard-coded, unjustified initial conditions for E and I

The `seir_rinit` snippet hard-codes `E = 6000` and `I = 15000` as fixed constants rather than making them functions of the estimated susceptible fraction `eta` or any fitted parameter:

```c
E = 6000;
I = 15000;
```

No justification is given for these values, they are not estimated, and they are not included in the sensitivity analysis. Hard-coding latent state initial conditions can bias all downstream parameter estimates, particularly `beta1`, `beta2`, and `eta`, and prevent the model from correctly capturing the early epidemic dynamics.

### 4. [Major] mu_EI and mu_IR are fixed without adequate justification, inflating artificial precision

The project fixes both `mu_EI = 0.1` and `mu_IR = 0.08` and states this is "to simplify the search." These values imply a mean incubation period of 10 days and a mean infectious period of 12.5 days, which are inconsistent with the stated epidemiological prior of "usually 14 days to fully recover, yet after 10 days unlikely to infect others." No sensitivity analysis over `mu_EI` and `mu_IR` is conducted. Fixing parameters at arbitrary values without uncertainty quantification artificially narrows the profile likelihoods and confidence intervals for all other parameters.

### 5. [Major] Profile likelihood for tau is unreliable: only two points above threshold and misreported CI

The text explicitly acknowledges "only two points are above the threshold resulting in dubious interval," yet still reports a 95% confidence interval of [0.669, 0.706] (presented in the HTML output as 66.88%–70.62%). An interval based on only two profile points is statistically meaningless. Furthermore, the output table formats tau as a percentage (e.g., "66.88%") due to the code using `sprintf("%.2f%%", 100 * min)`, which multiplies raw tau values by 100 and appends a percent sign — a clear bug that misrepresents the CI bounds. The text states the interval is [0.669, 0.706] but the table shows "66.88%" to "70.62%", which are inconsistent unless tau is actually ~0.007 (not 0.669).

### 6. [Major] Global search finds beta2 < beta1, contradicting the model's epidemiological motivation, and this is not adequately investigated

The stated motivation for having two separate beta values is that the Omicron variant is more contagious than earlier variants (justifying beta2 > beta1 after day 17). However, the global search consistently finds beta2 < beta1. The authors acknowledge this contradicts the biological expectation but offer only a hand-waving explanation about the "long tail." No re-parameterization, constraint on the search space, or biological interpretation of the best-fit parameter regime is given.

### 7. [Major] Inadequate particle count and iteration count for reliable inference

At run_level = 2, the code uses NP = 1000 particles, NMIF_L = 100 filtering iterations, and NREPS_EVAL = 20. For a 4-parameter free SEIR model with 121 observations, 1000 particles is borderline, and the standard errors on log-likelihood evaluations (reported as 0.02 for the global maximum) suggest filter variance is low — but the local search traces show strong oscillations indicating the optimizer has not converged reliably. The best local-search likelihood (-884) and global best (-861) differ by 23 units, indicating the local search is insufficient even as a warm start.

### 8. [Moderate] ARIMA model selection via AIC selects ARIMA(4,1,4) despite near-cancellation of AR and MA roots

The inverse characteristic root plot shows AR and MA roots very close to the unit circle and visually nearly coincident, which is a strong signal of near-cancellation (i.e., the model is effectively of lower order). The authors note this concern but choose ARIMA(4,1,4) anyway. The AIC table is not shown in the rendered output so readers cannot verify whether a simpler model would suffice; only the chosen model's AIC is derivable from the printed output.

### 9. [Moderate] Shapiro-Wilk test rejection is not acted upon

The Shapiro-Wilk test rejects normality of ARIMA residuals (p < 0.05), but the authors continue using the Gaussian ARIMA model without modification. No transformation of the data (e.g., square root or log to handle count data) is considered, and no alternative model (e.g., negative-binomial errors, SARIMA to handle the detected weekly cycle) is discussed as a remedy.

### 10. [Moderate] Detected 7-day periodicity is not incorporated into either model

The spectral analysis clearly identifies a 7-day cycle in the case counts, consistent with weekly testing/reporting patterns. The ARIMA model selected (ARIMA(4,1,4)) does not include a seasonal component at lag 7 (i.e., no SARIMA structure). The SEIR model similarly ignores the weekly periodicity. The conclusion merely mentions this as a potential future improvement but does not attempt it. The weekly effect, if unmodeled, is a systematic source of bias in both parameter estimates and likelihood comparison.

### 11. [Moderate] The covariate intervention split (day 17) is fixed and not estimated

The transition from beta1 to beta2 is set to occur after exactly 17 days, corresponding to December 17, 2021 (the date Omicron was first detected in Wayne County). This cut-point is treated as fixed and known, not estimated. No sensitivity analysis around this threshold is presented, despite the fact that the transition date has a large effect on the estimated values of both beta1 and beta2.

### 12. [Moderate] Profile likelihood is performed for tau only; no profiles for other parameters are shown

Only tau receives a profile likelihood analysis. No profiles are shown for beta1, beta2, rho, or eta, which are the epidemiologically more interpretable parameters. Given that the global search shows instability in all of these parameters, profile likelihoods for beta1 and beta2 in particular would be informative and are standard practice in POMP-based epidemiological analyses.

### 13. [Minor] The measurement model equation in the text is self-referential and contains a notation error

The measurement model is stated as:

$$H = \max\{\lfloor H_n \rfloor, 0\}, \quad H_n \sim \mathcal{N}(\rho H_n, (\tau H_n)^2 + \rho H_n)$$

The left-hand side uses $H$ and the distribution uses $H_n$ in the mean, making the equation circular and poorly defined. In the actual code, the mean is `rho*H` where H is the accumulated compartment value, not the observation. The text should clarify that H on the right-hand side refers to the latent accumulated count compartment, not the observed count.

### 14. [Minor] The ARIMA AIC table is presented without the full table being visible in context

The AIC table is rendered via `kable` and shows values for ARIMA(p,1,q) for p,q in 0:4, but the text only states that ARIMA(4,1,4) is chosen because it gives "fairly small AIC value while it does not lose too much model's parsimony." The claim that ARIMA(4,1,4) is parsimonious is inconsistent with having 8 free AR/MA parameters; choosing the model at the corner of the search grid (maximum p and q both equal to 4) strongly suggests the table edge was hit and the search should be expanded.

### 15. [Minor] Acknowledgements section reveals structural similarity to prior projects but does not cite them as methodological sources

The authors note that their topic overlaps with Projects 13 and 15 from W21. While acceptable to acknowledge, neither prior project's methodology (if referenced) nor the course notes are cited in the methods section. The SEIR structure is identical to the course homework template; this should be explicitly credited.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/covid_wayne_winter.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project19/Makefile`
