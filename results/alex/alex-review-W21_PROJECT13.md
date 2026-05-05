# Peer Review: W21 Project 13 — An Investigation into COVID-19 in California

## Summary

This project fits both an ARIMA(4,1,3) model and a custom SEAPIRD POMP model to daily COVID-19 case and death data for California from January 22, 2020 through April 7, 2021. The POMP model extends a standard SEIR structure with Asymptomatic (A), Presymptomatic (P), and Deceased (D) compartments and uses six time-varying beta coefficients to capture intervention effects. The project demonstrates competent setup of the pomp machinery and reaches a best global log-likelihood of approximately -3791. However, there are multiple critical methodological flaws in the measurement model, state process, and inference procedure that substantially undermine the reliability of the reported results.

---

## Major Weaknesses

### 1. Accumulator variable H tracks recoveries, not incidence — measurement model is misspecified

The accumulator `H` is updated as `H += dN_IR + dN_AR`, i.e., it counts recoveries, not new cases. Yet in both `rmeasure` and `dmeasure`, `rho * H` is used as the mean of the observed case count. This means the model attempts to explain daily reported cases as a fraction of daily recoveries, which is epidemiologically wrong. New reported cases should be linked to new infections (transitions out of S, i.e., `dN_SE`), or at minimum to transitions into the symptomatic compartment (`dN_PI`). This fundamental mismatch between the latent state process and the observation model invalidates all likelihood values and parameter estimates reported in the paper.

### 2. Deaths are included in `rmeasure` and `dmeasure` inconsistently

In `rmeasure`, simulated cases are set to `rnorm(mean_cases, sd_cases) + D`, adding the current-step death accumulation directly to the case count. In `dmeasure`, the likelihood is evaluated as `dnorm(cases - deaths, mean_cases, sd_cases, 0)`. These two expressions are not consistent with each other: rmeasure generates `cases = X + D` (where X is Normal), but dmeasure evaluates the density of `cases - deaths` as if it were `X`. This would only be self-consistent if `deaths` in the data exactly equals `D` at every time step, which is not guaranteed. More importantly, the text states "We assume all COVID deaths are reported" and then sets `deaths = D` in rmeasure, but `D` in the C code is a cumulative counter that is never reset (there is no `H_D` accumulator reset each step), so `D` grows throughout the simulation and misrepresents the daily death count.

### 3. D is a cumulative stock, not a daily flow — used incorrectly as daily deaths

In the step function, `D += dN_ID` accumulates deaths over the entire simulation. There is no separate daily-death accumulator (analogous to `H` for recoveries). When `rmeasure` sets `deaths = D` and `dmeasure` evaluates `lik = dnorm(cases - deaths, ...)`, it uses the total cumulative death stock, not the daily increment. This would produce nonsensical likelihoods and simulated death observations that grow without bound.

### 4. rho has an improper prior/constraint — logit transform applied but box upper bound is 2

The global search box specifies `rho = c(0, 2)`, but `rho` is constrained with a logit transform (`logit=c("rho", "alpha")`) in `parameter_trans`, which maps the real line to (0, 1). Initializing `rho` uniformly on (0, 2) and then applying logit to constrain it is contradictory: values of `rho` above 1 passed to the logit-constrained optimizer would be invalid as a reporting probability. Moreover, a reporting rate `rho > 1` has no epidemiological meaning. The search box should have been restricted to (0, 1).

### 5. Intervention periods are not aligned to actual dates

The intervention indicator is assigned purely by row index (rows 1–99, 100–199, 200–249, etc.) with no reference to actual calendar dates. Assumption 1 in the text refers to specific date ranges for lockdown measures but leaves them blank ("from x-x and x-x"). The six intervention windows are never described in terms of what events they correspond to, making it impossible to assess whether the model appropriately captures the known policy timeline (e.g., the March 19 statewide stay-at-home order, the December 2020 regional lockdown). The mismatch between the described policy chronology and the arbitrary index-based cutoffs undermines the scientific interpretation of the c_i parameters.

### 6. Likelihood comparison between ARIMA and POMP is not meaningful

The paper compares the ARIMA log-likelihood of -4091 with the POMP log-likelihood of -3791 directly. However, these likelihoods are not comparable: the ARIMA model is evaluated on the differenced series, while the POMP likelihood conditions on the full undifferenced data. Furthermore, the POMP model has 16 free parameters whereas ARIMA(4,1,3) has 7; no penalty for model complexity (such as AIC) is applied. The conclusion that "the POMP model performed better" is not validly supported.

### 7. Only 8 IF2 chains are used in both local and global search — insufficient coverage

The local search runs 8 chains of mif2 with Np=1000 and Nmif=200; the global search uses 8 chains with Np=2500 and Nmif=250. For a 16-parameter model applied to over 400 data points with known multimodality in COVID transmission models, 8 starting points provides extremely limited exploration of the parameter space. The pairs plots included show that parameter estimates have not converged to a tight cluster, suggesting the optimization is not complete.

### 8. alpha is mislabeled and used inconsistently

In the text, alpha is defined as "Presymptomatic case portion," but in the code, `alpha` controls the fraction going to the asymptomatic compartment A: `A += nearbyint(alpha * dN_EI)`, and `P += nearbyint((1 - alpha) * dN_EI)`. So a higher alpha means more people are asymptomatic. The label "Presymptomatic case portion" is the opposite of what the code implements. The text also says "presymptomatic case portion alpha from 14% to 20%" from prior literature, but the estimated alpha values in the results are all above 0.65, a large discrepancy with cited literature that is not discussed.

### 9. nearbyint used for splitting binomial draws introduces rounding bias

The transitions from E to P and A are computed as `nearbyint((1 - alpha) * dN_EI)` and `nearbyint(alpha * dN_EI)`. Rounding `alpha * k` and `(1-alpha) * k` independently does not guarantee their sum equals `dN_EI`. This can cause individuals to be created or destroyed at each step, violating conservation of the population. The correct approach is to draw from a multinomial or to assign `dN_EP = dN_EI - dN_EA` without rounding.

### 10. No profile likelihood or confidence intervals reported for POMP parameters

The analysis jumps from a pairs plot directly to a conclusion about the best parameters and log-likelihood. There are no profile likelihood curves, no bootstrap confidence intervals, and no uncertainty quantification for any estimated parameter. The pairs plots are included but not interpreted in terms of parameter identifiability or correlation structure. This is a substantial gap in the inferential analysis.

---

## Minor Weaknesses

### 11. AIC table selection: ARIMA(4,1,3) chosen by minimum AIC without checking numerical stability

The AIC table is reported but the values are not shown in the text (the code is displayed but output is not discussed). The paper states ARIMA(4,1,3) is chosen for having the "smallest AIC value," but the root plot notes that some inverse AR and MA roots are near the boundary of the unit circle, suggesting near-cancellation and potential numerical instability. The paper acknowledges a "smaller model may be more appropriate" but proceeds with ARIMA(4,1,3) without further investigation.

### 12. Spectrum analysis conclusion is vague and not used

The spectral analysis identifies a dominant cycle of approximately 150 days but the authors conclude the dataset is "not long enough to confirm seasonality" and then make no further use of this result. If seasonality is suspected, it should either be incorporated into the model or the analysis should quantify the evidence for and against a seasonal component more rigorously.

### 13. Convergence described without quantitative evidence

The writeup states "From the diagnostic plots it appears the POMP model has converged" based solely on visual inspection of trace plots (shown as external images). No quantitative convergence diagnostics are provided (e.g., the improvement in log-likelihood across iterations, or whether multiple chains reached the same optimum). Two of the three convergence plots are linked to external image files that may render differently across systems.

### 14. Initial condition I_0 = 250 is not justified and N is not adjusted for initial infecteds

The model initializes S = N = 39,512,223 (the full California population) and I = 250, meaning the total initial population is N + 250. No epidemiological justification is given for exactly 250 initial infected individuals. Additionally, E, A, P, and R all start at zero, which ignores the ramp-up phase of the epidemic from January through March 2020 and may cause the model to misfit the early data.

### 15. Acknowledgment of deaths observation model is inconsistent with the data used

The observation model text describes the distribution of "weekly reported recovered cases" but the data is daily and the observed variable is confirmed cases, not recovered cases. The disconnect between the text description of the measurement model and what is actually implemented in code (and in the data) is never reconciled.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project13/covidSEAPIRD.c`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project13/ca_daily_data.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project13/local_results_greaklakes.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project13/local_results_greatlakes2.csv`
