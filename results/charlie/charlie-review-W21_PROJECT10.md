# Peer Review: W21 Project 10
**Title:** Time Series Analysis of COVID-19 in Georgia

---

## Summary

This project analyzes COVID-19 case and vaccination data from Georgia using two complementary approaches: (1) an ARIMA regression model for daily vaccinations and COVID cases, and (2) three variants of a stochastic SEIR compartmental model fitted with the `pomp` package. The mechanistic models incorporate vaccination as either a constant deduction from the susceptible compartment, a linearly increasing deduction, or a vaccination rate parameter. While the project addresses a topical and important question and demonstrates familiarity with both ARIMA and compartment modeling frameworks, the analysis suffers from critical methodological shortcomings: no likelihood-based inference is performed on any of the three POMP models (all parameter values are hand-selected); no iterated filtering, particle filter log-likelihoods, profile likelihoods, or convergence diagnostics are reported for the main analysis; model adequacy is assessed entirely by visual simulation comparison; the mathematical specification of Model 3 contains an error inconsistent with the code; the LRT in the ARIMA section uses incorrect degrees of freedom and is applied to a different time series than the one used for model selection; and rolling-mean-smoothed non-integer data is fed to a binomial measurement model. The conclusions are entirely unsupported by statistical inference.

---

## Major Issues

### 1. No likelihood-based inference performed on any POMP model

None of the three SEIR model variants is subject to any form of likelihood maximization or statistical inference. All parameters — Beta, mu_EI, mu_IR, rho, eta, and the vaccination constants — are hand-selected by the authors and justified by informal reasoning (e.g., "we set V to be 2500 in order to make the product 2500*8 close to the true vaccine mean level"). The appendix acknowledges that attempts at local search using `pfilter` and `mif2` produced -Inf log-likelihoods and were abandoned. The main body presents only forward simulations from manually chosen parameters. Without likelihood maximization, it is impossible to assess parameter uncertainty, compare models formally, or determine whether the model actually fits the data rather than merely producing plausible-looking trajectories. Wheeler et al. (2024) identify likelihood-based inference as the foundation of rigorous mechanistic modeling; ad hoc calibration makes formal model comparison and uncertainty quantification impossible.

### 2. No convergence diagnostics, no mif2 runs in main analysis

The main analysis does not present any iterated filtering (mif2) runs, log-likelihood traces, or evidence that the optimizer was applied to any of the three models. The appendix includes two code chunks (marked `eval=FALSE`) showing failed attempts with `pfilter` that returned -Inf likelihoods. These failed attempts are never resolved and no corrective action is taken in the main analysis. Without convergence diagnostics — likelihood trajectories across iterations, multiple searches from diverse starting values — there is no evidence that reported parameters are near the MLE. The authors themselves acknowledge: "if we can overcome the unsolved obstacles in the future analysis, local & global search may lead to better estimations of the parameters" (Section 5). This is a fundamental incompleteness that renders the POMP analysis methodologically void.

### 3. Smoothed non-integer data fed to a binomial measurement model

The POMP analysis uses a 7-day rolling mean of daily COVID case counts as the observed data (lines using `rollmean(dat[,2], 7)`). This smoothing produces non-integer values. The measurement model in all three SEIR variants is `lik = dbinom(reports, H, rho, give_log)`, which requires integer counts as the first argument. Passing non-integer values to `dbinom` is mathematically invalid and will cause the likelihood to be undefined or silently wrong. The rolling mean is appropriate for visualization but not for use as the observed data in a binomial likelihood model. The particle filter failures (returning -Inf) reported in the appendix are very likely a consequence of this misspecification.

### 4. Mathematical specification of Model 3 is inconsistent with the code

The mathematical equations for Model 3 specify:
$$N_{SV} = \text{binomial}(I, 1-\exp(-\mu_{SV} \cdot dt))$$
indicating that vaccination is a binomial draw from the *infectious* compartment I. This is biologically nonsensical — vaccination acts on the susceptible population, not the infectious population. The code correctly implements `double dN_SV = rbinom(S, 1-exp(-mu_SV*dt))`, drawing from S. The disconnect between the stated mathematical model and the implemented code means the mathematical description in the paper does not accurately represent the model being analyzed. Readers cannot reproduce or evaluate the model from the equations as written.

### 5. Likelihood ratio test uses wrong degrees of freedom and mismatched data

In Section 3, the authors compare ARIMA(1,1,1) and ARIMA(4,1,4) using a likelihood ratio test with `pchisq(delta_ll, 2, lower.tail=F)`, asserting 2 degrees of freedom. However, ARIMA(4,1,4) has 3 additional AR parameters and 3 additional MA parameters compared to ARIMA(1,1,1), for a total of 6 additional parameters. The correct reference distribution is chi-squared with 6 degrees of freedom. Using df=2 produces an anti-conservative test that will reject the null too easily, invalidating the model selection conclusion. Furthermore, the AIC table used to identify candidate models (tab1) is computed on `people_fully_vaccinated`, but the LRT is applied to `daily_vaccinations` — a completely different time series. The conclusion that ARIMA(4,1,4) significantly improves over ARIMA(1,1,1) is based on comparing a model selected from one variable to a test applied to another.

### 6. No quantitative goodness-of-fit statistics reported for any model

No log-likelihood values, AIC values, or any other quantitative fit measure are reported for any of the three SEIR variants. Model comparison across the three variants is performed entirely by visual inspection of 20 simulated trajectories against the observed data. Wheeler et al. (2024) state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The text claims each model "perfectly simulates" the initial case count and peak, but this assessment is made by eyeball comparison with manually tuned parameters. No statistical evidence supports the adequacy of any variant over another.

### 7. No benchmark comparison for the POMP model

No non-mechanistic benchmark (e.g., ARMA, negative binomial regression) is compared against the SEIR model using a common quantitative metric. The ARIMA analysis in Section 3 is for vaccinations and COVID cases separately and is not used to benchmark the SEIR model in Section 4. Wheeler et al. (2024) identify this as the single most diagnostic check for whether a mechanistic model captures meaningful structure beyond what a simpler statistical model would achieve. Without such a comparison, the added complexity of the SEIR formulation cannot be justified.

### 8. H accumulator tracks recoveries but is compared to new case reports

The accumulator variable H is incremented by `dN_IR` (transitions from I to R — recoveries) and used in the measurement model as `dbinom(reports, H, rho)`. However, `reports` is the daily new COVID case count — the number of new positive tests, not the number of recoveries. Biologically, new reported cases correspond more closely to `dN_EI` (new infections, transitions from E to I) or `dN_SE` (new exposures), not to recoveries. Using recoveries as the basis for reported case counts introduces a systematic lag and misalignment between what the model tracks (when people recover) and what the data measures (when people test positive). This misspecification affects all three models.

---

## Minor Issues

### 9. Data duplication in introduction and Section 2.1

Sections 1 (Introduction) and 2.1 (Data Description) contain identical paragraphs describing the data sources (NYT and Our World in Data), the choice of Georgia, and the 413-observation dataset. This verbatim repetition is an editorial issue that should be resolved.

### 10. Vaccine constant V is applied per Euler substep, not per day

In Models 1 and 2, V=2500 susceptibles are moved to R at each Euler substep (delta.t=1/8 day). With 8 substeps per day, this translates to 2500×8=20,000 vaccinations per day. The text states "we set V to be 2500 in order to make the product 2500*8 close to the true vaccine mean level," which shows this is intentional. However, this vaccination rate is hard-coded and not estimated from data, and the text provides no justification for why 20,000/day is appropriate for the January–April 2021 period in Georgia. This is effectively a fixed covariate embedded in the Euler step rather than a model parameter, making it impossible to assess its influence statistically.

### 11. No residual diagnostics for ARIMA models

Neither the ARIMA model for daily vaccinations nor the ARIMA(2,2,4) model for pre-vaccination COVID cases is subject to any residual diagnostic. ACF/PACF plots of residuals and a Ljung-Box test are the standard course-level diagnostics for ARIMA models. Without them, it cannot be assessed whether the model adequately removes the autocorrelation structure from the series.

### 12. Model selection ignores upper-boundary issue in AIC table

The authors note that the AR5/MA5 model has the lowest AIC but discard it because "this is both a highly complex model and at the upper bound of the coefficients we tested." This reasoning is qualitatively sensible, but the correct response is to extend the search (e.g., to AR6/MA6) to verify that the optimum is not at the boundary, rather than simply selecting the next-best model. The selected model (AR4,MA4 identified from one series, then AR1,MA1 compared to AR4,MA4 on a different series) may not be the true optimum.

### 13. ARIMA model is applied to post-vaccination data only after pre-vaccination selection

The ARIMA(2,2,4) model is selected using only pre-vaccination COVID case data (Section 3), then applied to post-vaccination data with `people_fully_vaccinated` as a covariate. This train/test split is reasonable in principle, but no justification is given for assuming the pre-vaccination ARIMA structure persists into the post-vaccination period, when case dynamics may differ substantially. The coefficient on the vaccination covariate is reported as "very small," but no hypothesis test or confidence interval is provided to assess whether vaccination has a statistically detectable association with case trends.

### 14. Inconsistent parameter values between text and equations

The text in Section 4.2.1 states "mu_IR equals 0.9 and R0 equals 3.5" but the simulate call uses `mu_IR=0.09`. With Beta=0.32 and mu_IR=0.09, R0 = Beta/mu_IR ≈ 3.56, which is consistent with the claimed R0=3.5. With mu_IR=0.9, R0 would be approximately 0.36 — biologically implausible. The value 0.9 appears to be a typographical error for 0.09, but this inconsistency between text and code undermines the reader's ability to understand the model parameterization.

### 15. Data loaded from live external URLs without local backup

The POMP models load data from live GitHub URLs (`raw.githubusercontent.com/nytimes/covid-19-data/` and `raw.githubusercontent.com/owid/`). The NYT COVID data repository was archived and may no longer be updated. If these URLs change or become unavailable, the analysis cannot be reproduced. Local data files (`us-states.csv` and `us_state_vaccinations.csv`) appear to be present in the project directory but are not used consistently throughout — the ARMA section reads from live URLs while the EDA section uses the local files. All data reads should use the local copies to ensure reproducibility.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/README.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project10/blinded.Rmd`
