# Peer Review: W24 Project 04
## "Comparative Analysis of ARIMA and SEIR Models Using COVID-19 Data"

---

## Summary

This project compares ARIMA and SEIR models applied to weekly COVID-19 confirmed case counts from Washington State. The paper describes an EDA using SIR simulations across three U.S. states, an ARIMA model selection section, and a SEIR model section with local and global parameter searches. While the topic is reasonable and the structure follows a sensible outline, the project contains numerous methodological errors in the POMP implementation that undermine the validity of essentially all reported results. Issues range from incorrect measurement models, an optimization approach that bypasses likelihood entirely, and a final "tuned" model with no principled justification. The ARIMA component is more credible but still contains inconsistencies.

---

## Weaknesses (Most Critical First)

### 1. (Major) Measurement model uses wrong parameterization of the negative binomial

In both the original and all subsequent SEIR model versions, `dmeas` is coded as:

```c
lik = dnbinom(cases, I, rho, give_log);
```

The base R `dnbinom(x, size, prob, ...)` parameterization uses `size` and `prob`. Here `I` (number of infectious individuals) is passed as `size` and `rho` (the reporting probability, a small number) as `prob`. This is not the intended negative binomial observation model for infectious disease counts, where one would typically use `dnbinom_mu(cases, k, rho*I, give_log)` with a dispersion parameter `k` — exactly the form used in the course's SIR template. As a consequence, every likelihood evaluation in the SEIR section is based on a mis-specified measurement model. No overdispersion parameter `k` is included in the SEIR parameterization at all.

### 2. (Major) Optimization is done by minimizing sum of squared errors, not maximizing likelihood — standard POMP inference is never performed

The "local search" and "global search" optimization steps minimize `sum((sim$cases - data$cases)^2)` over a single simulation trajectory. This is not likelihood-based inference. It is a naive curve-fitting heuristic that:
- Ignores the stochastic nature of the process model (a single simulation has high variance).
- Does not use the `dmeasure` component at all, rendering the carefully written `seir_dmeas` irrelevant.
- Cannot produce uncertainty estimates or likelihood comparisons.

No particle filter (`pfilter`), iterated filtering (`mif2`), or profile likelihood is ever used. These are the standard POMP inference tools and their absence means the project does not actually demonstrate POMP-based inference.

### 3. (Major) The "Final SEIR Model" parameters are chosen by manual hand-tuning with no justification

After acknowledging that both local and global optimization produced poor fits, the authors simply assign a new set of hand-chosen parameters (`beta=0.35, sigma=0.3, gamma=1/14, N=5000000, rho=0.5`) and re-simulate. No optimization criterion, no likelihood score, and no explanation for why these values are selected is provided. The project then presents this simulation as representative of the model's performance, which is not a scientifically valid procedure.

### 4. (Major) Incorrect `rmeas` (random measurement) in the global search section

In the global search section, the `rmeasure` Csnippet is overwritten to:

```c
cases = nearbyint(I);
```

This replaces the stochastic measurement process with a deterministic assignment, directly setting observed cases equal to the integer-rounded number of infected individuals. This is inconsistent with the stated negative binomial observation model and makes the pomp object structurally incoherent for that section.

### 5. (Major) The EDA SIR simulations have no connection to the main analysis

The EDA section constructs three SIR POMP objects (for California, Washington, and New York) with identical, arbitrarily chosen parameters (`Beta=0.45, mu_IR=0.1, eta=0.80, rho=0.9, k=1, N=1000000`). These are simulation-only exercises with no data fitting. The resulting plots show unrealistic cyclical dynamics, which the authors themselves flag as implausible, yet the section is presented as "EDA." Genuine exploratory data analysis should examine the raw time series (trends, seasonality, distributional properties), not forward-simulate a mis-parameterized SIR model.

### 6. (Major) Data preprocessing in the SEIR section applies cumulative-to-incident differencing twice

In the data wrangling chunk (lines 631–648), the code first takes `sum(confirmed)` per week (which is a sum of cumulative counts), then differences the weekly sums. This results in first-differenced cumulative totals, which is equivalent to weekly incidence only if cumulative counts are summed correctly. However, the weekly grouping sums cumulative confirmed cases, not incident cases. A second differencing step then further transforms the data. The result stored in `week.csv` may not correctly represent weekly new cases, and the authors do not verify this against known COVID-19 case counts for Washington State.

### 7. (Major) No likelihood ratio tests, AIC, or any formal comparison between ARIMA and SEIR models

The stated research question is whether SEIR provides a better fit than ARIMA. No quantitative comparison is ever made: no log-likelihoods are reported for the SEIR model, no AIC values are computed, and no formal statistical test is conducted. The conclusion that SEIR "aligns more closely with the actual data peak" is a purely visual, subjective judgment. The comparative goal of the project is never formally addressed.

### 8. (Major) ARIMA model selection inconsistency: AIC selects ARIMA(2,1,3) but ARIMA(3,1,1) is fitted for diagnostics

The text explicitly states that ARIMA(2,1,3) achieves the lowest AIC (3983.290), yet the diagnostic plots (residuals, ACF, QQ-plot) and the final fitted model use `arima(x = week_ts, order = c(3, 1, 1))`. The fitted-versus-actual plot is also produced from the ARIMA(3,1,1) model. The paper never provides any diagnostic or fit visualization for the model it selected (ARIMA(2,1,3)), and does not explain why ARIMA(3,1,1) was ultimately preferred.

### 9. (Minor) Population parameter N is treated as a free optimization variable without constraint relative to known Washington State population

In both the local and global searches, `N` is optimized freely with an upper bound of 10 million. Washington State's population is approximately 7.7 million, yet the global search returns `N = 8,830,174`, exceeding the actual population. The authors do not comment on this implausibility or fix `N` to a known value.

### 10. (Minor) No confidence intervals or uncertainty quantification for any model parameter

Neither the ARIMA section (which could provide standard errors from the Fisher information) nor the SEIR section presents any uncertainty estimates. Profile likelihoods, bootstrap confidence intervals, or particle-filter-based standard errors are entirely absent, making it impossible to assess whether reported parameter estimates are meaningful.

### 11. (Minor) The EDA section claims 1500 data points from Washington State, but week.csv contains weekly aggregates

The introduction states "we primarily used 1500 data points from Washington State." The `week.csv` file contains weekly aggregated data with approximately 160 rows, not 1500 daily observations. This discrepancy is unexplained and suggests either a mischaracterization of the data or confusion between the raw daily data and the weekly aggregates actually used.

### 12. (Minor) The `main.R` file is the unmodified course measles SIR example and is not used by the project

The submitted `main.R` contains the standard course code for fitting a SIR model to the 1948 Consett measles data — it has no connection to COVID-19 or Washington State data. Including this unrelated file without modification or acknowledgment suggests it was not developed as part of the project and adds no analytical value.

### 13. (Minor) Time axis labels are misleading: axes say "Day" but the model and data use weekly time units

Multiple plot labels read `x = "Day"` (e.g., the SEIR simulation plots), but the time variable `week_number` represents sequential weeks, and `delta.t = 0.1` refers to fractional weeks. This mislabeling creates confusion about the temporal scale of the model.

### 14. (Minor) The time-varying beta described in the mathematical model is never implemented in the code

The model description section (lines 590–591) states that the contact rate beta takes value b1 in the first half of the time period and b2 in the second half, implying a time-varying transmission rate. However, none of the implemented Csnippets include a covariate or time-dependent beta. The actual code uses a single constant `beta` throughout. The discrepancy between the stated model and the implemented model is never acknowledged.

### 15. (Minor) Reference to ChatGPT for "code optimization and error correction" without specifying what was generated or corrected

Reference [6] cites `https://chat.openai.com/` for "Code optimization and error correction." This is insufficient documentation. The report should specify which parts of the code were AI-assisted, what errors were corrected, and whether the resulting code was verified to be correct. Given the numerous coding errors present in the submitted code, this raises concerns about whether AI-generated corrections were properly validated.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project04/main.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project04/week.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project04/Makefile`
