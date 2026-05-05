# Peer Review: W22 Project 10 — Modeling South Africa Omicron Variant Cases

---

## Summary

This project fits time series models to daily confirmed COVID-19 (Omicron variant) cases in South Africa from December 2021 through April 2022. The authors employ three modeling frameworks in sequence: ARMA, a basic SIR POMP model, and a more elaborate SEAPIRD POMP model. While the ambition and breadth of the project are commendable, there are numerous methodological, statistical, and presentation weaknesses that substantially limit the reliability and interpretability of the results.

---

## Weaknesses (prioritized from most to least critical)

---

### 1. [MAJOR] Inconsistent population size between SIR and SEAPIRD models with no justification

The SIR model uses `N = 50,000,000` (50 million, intended to represent South Africa's population), but the SEAPIRD model uses `N = 500,000` without any epidemiological justification. This is a critical inconsistency. South Africa has approximately 60 million people. If the SEAPIRD model is using N = 500,000, it is modeling a subpopulation of unknown composition, and the parameters (particularly `rho`, `eta`, and the absolute case counts) become incomparable across the two models. The global search for the SIR model also passes `N=500000` (line 315), inconsistent with the stated `N=50,000,000`. This silently changes the model meaning.

---

### 2. [MAJOR] No profile likelihood or formal confidence intervals for any estimated parameter

Neither the SIR nor the SEAPIRD model includes profile likelihood analysis or any form of uncertainty quantification for individual parameters. The authors report only point estimates from the best run and a single Monte Carlo standard error on the log likelihood. Without profile likelihoods, it is impossible to assess whether parameters are identifiable or whether the reported point estimates are meaningfully constrained by the data. For a POMP project, this is a critical omission.

---

### 3. [MAJOR] SEAPIRD measurement model is statistically incorrect — Normal approximation with wrong parameterization

The SEAPIRD `dmeas` function computes `dnorm(cases - deaths, mean_cases, sd_cases, 0)` but the data variable `cases` already represents confirmed new cases, not a quantity from which deaths need to be subtracted. Additionally, the variance term `tau * rho * H * (1 - rho)` attempts to mimic a binomial variance, but `tau` is a free parameter estimated in the thousands to hundreds of thousands, making the distribution extremely wide in a manner that is not grounded in any clear statistical model. The normal distribution for count data is also a poor choice when counts can be near zero or zero, which happens in this dataset (particularly at the ends of the time series).

---

### 4. [MAJOR] SIR global search passes N=500,000 while model is stated to use N=50,000,000

In the SIR global search code block (line 315), `N=500000` is hardcoded alongside the random draws from `covid_box_sir`, which does not include N. This means the global search uses a fundamentally different population size than the local search and the stated model specification. The reported "best" global log likelihood of -1677 is therefore not directly comparable to the local result of -1997, since they use different N values. No mention of this discrepancy is made in the text.

---

### 5. [MAJOR] No likelihood benchmark against a null or ARMA model on a common scale

The ARMA(3,3) log likelihood is -1492 (from the HTML output). The SIR model achieves -1677 (global) and the SEAPIRD model achieves -1446 (global). The authors state in the conclusion that the SIR model is not competitive with ARMA, but the SEAPIRD model achieves -1446 versus ARMA's -1492. However, these likelihoods are on different scales because the ARMA model uses a Gaussian distribution while the POMP models use different observation models. A direct likelihood comparison is not valid, and the authors do not acknowledge this limitation. No AIC comparison or model selection framework is applied.

---

### 6. [MAJOR] SEAPIRD branching of exposed class is statistically invalid

The SEAPIRD step function computes `dN_EI = rbinom(E, 1-exp(-mu_EI*dt))` and then applies `nearbyint(alpha * dN_EI)` and `nearbyint((1-alpha) * dN_EI)` to split the transitions into asymptomatic and presymptomatic paths. Rounding two fractions of the same binomial draw separately introduces rounding errors and violates conservation of individuals (the rounded P and A increments may not sum to `dN_EI`). The correct approach is a single multinomial draw from E for the three transitions, or a sequential binomial thinning. This is a coding error that can cause individuals to be created or lost.

---

### 7. [MAJOR] mif2 particle count too low — Np=100 for SIR local search

The SIR local search uses `Np=100` particles (line 257), which is far too few for reliable likelihood estimation with an epidemic model on 156 data points. With Np=100, the particle filter will suffer severe degeneracy and the likelihood surface estimated by mif2 will be extremely noisy, undermining the convergence of the IF2 algorithm. The SEAPIRD model uses Np=1000 for local search, which is more reasonable, but the SIR results with Np=100 are not trustworthy.

---

### 8. [MAJOR] Intervention covariate structure is arbitrary and not epidemiologically motivated

The three intervention periods c_1, c_2, c_3 are defined by fixed 50-day windows (days 0-49, 50-99, 100+), not tied to any known South African policy interventions or epidemiological events. The choice of 50-day windows is not discussed or justified. Furthermore, the covariate is coded so that the third period (day >= 100) encompasses the tail of the epidemic, where the epidemic is largely over, which makes the c_3 parameter difficult to identify from the data. No sensitivity analysis on the window boundaries is performed.

---

### 9. [MINOR] SIR rinit sets H=169 instead of 0

In the `sir_rinit` Csnippet (line 203), `H = 169` is set at initialization. Since H is an accumulator variable that should be reset at each observation time, initializing it to 169 is incorrect — it should be initialized to 0 (or to the initial case count if the model uses H at t0 for the measurement). Setting H=169 at t0 will inflate the first predicted report count, introducing a bias into the likelihood evaluation for the first observation.

---

### 10. [MINOR] SEAPIRD rinit sets S=N with no initial removed or exposed individuals

The SEAPIRD `seapird_init` sets S=N, E=0, P=0, A=0, I=169, R=0. This means S + I != N at t0 (specifically, S = N = 500,000 but there are already I=169 infectious individuals), so the population is not conserved at initialization. In the SIR model, the authors use eta to control the initial susceptible fraction, which is a principled approach. The SEAPIRD model drops eta entirely and simply fills S=N, leaving a population accounting error at the start.

---

### 11. [MINOR] Weekly periodicity identified but not incorporated into POMP models

The spectrum analysis correctly identifies a ~7-day periodicity in the data and offers a reasonable explanation (weekly reporting artifacts). However, neither the SIR nor the SEAPIRD model accounts for this weekly cycle. A day-of-week covariate or a weekly reporting factor in the observation model would be straightforward to implement and would substantially improve model fit. The authors identify the problem but do not address it in the POMP framework.

---

### 12. [MINOR] Smoothed data used for SEAPIRD but raw data used for SIR — inconsistent comparison

The SIR model uses raw daily confirmed cases (`confirmed.new`) while the SEAPIRD model uses the 7-day smoothed version (`confirmed.newsm`), as stated on line 388. This makes the two models fundamentally non-comparable in terms of their observation targets and log likelihoods. Smoothed data inflates apparent model fit by removing high-frequency noise that the model does not need to explain. This inconsistency is not acknowledged in the comparison.

Actually, upon re-reading the code: the SEAPIRD `omicron_new` is constructed from `confirmed.new` (line 406-407), not the smoothed version. However, the text at line 388 claims the smoothed version is used. This discrepancy between the code and the text creates confusion about what was actually modeled.

---

### 13. [MINOR] The SEAPIRD global search best-fit parameters are biologically implausible

The reported global best-fit includes `mu_AR = 3.49` (per day), implying an asymptomatic recovery time of approximately 0.29 days — less than 7 hours. Similarly, `c_2 = 10.6` multiplies the baseline transmission rate by more than 10-fold during the second 50-day period, which is not epidemiologically plausible for a phase when Omicron was already well-established. These implausible parameter values suggest the optimizer has not found a biologically meaningful solution and that the parameter space is not sufficiently constrained by the data.

---

### 14. [MINOR] No convergence diagnostics shown for SIR model — the diagnostic chunk is eval=FALSE

The chunk `SIR_diag` (lines 350-360) containing the log likelihood convergence plots for the SIR model has `eval=FALSE` set, so these diagnostic plots are never computed or displayed in the rendered document. The authors state "The log likelihood soon converges" but provide no evidence for this claim in the output. The convergence trace plots from the mif2 runs (parameter traces) are shown, but the actual log likelihood convergence is suppressed.

---

### 15. [MINOR] Data preprocessing slice operation is fragile and its logic is not explained

The data preprocessing code uses `slice((-length(confirmed)+6):-length(confirmed))` to trim the dataset. This expression is non-intuitive and its purpose is not explained. Based on the context (7-day rolling mean requires 6 trailing observations), this appears to remove the last 6 days where the rolling average would be based on fewer than 7 points. However, this approach trims the end of the time series where valid data may exist, and the logic should be made explicit. The dataset length of 156 points, combined with the start date of 2021-11-01, also does not align with the stated focus on data "after December 1st" when Omicron became dominant — if Omicron became dominant in December, the November data is included without justification.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project10/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project10/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project10/Makefile`
