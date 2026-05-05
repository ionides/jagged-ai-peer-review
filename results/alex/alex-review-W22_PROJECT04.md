# Peer Review: W22 Project 04
## "An Analysis on COVID-19 Omicron Variant in Washtenaw"

---

### Overview

This project fits SARIMA and a custom recurrent SEPIR POMP model to daily COVID-19 case counts in Washtenaw County, MI from December 1, 2021 to April 6, 2022, covering the Omicron wave. The model is original and the motivation is reasonable, but there are multiple critical implementation bugs, under-validated modeling choices, and presentation deficiencies that collectively weaken the analysis.

---

## Weaknesses (Prioritized)

### 1. [CRITICAL BUG] `dN_RS` drawn from `I` instead of `R`

In the process simulator (`sepir_step` Csnippet and the compiled `omicron.c`), the recovery-to-susceptible transition is:

```c
double dN_RS = rbinom(I, 1-exp(-mu_RS*dt));
```

This samples from `I` (infected), not from `R` (recovered). The state update then subtracts `dN_RS` from `S` while adding it back via `S -= dN_SE - dN_RS`. This means recovered individuals never actually return to susceptible — the `R` compartment only grows through `dN_PR + dN_IR` but `dN_RS` is never subtracted from `R`. The recurrence mechanism, which is the central biological motivation of the paper, is therefore broken. The model is not actually a recurrent SEPIR; it silently degrades to a SEPIR without reinfection. All fitted parameters and conclusions about reinfection are artifacts of this bug.

### 2. [CRITICAL BUG] `nearbyint` used to split a binomial draw — breaks integer conservation

The split from E into P and I is done as:

```c
P += nearbyint(alpha*dN_EPI) - dN_PR;
I += nearbyint((1-alpha)*dN_EPI) - dN_IR;
```

`nearbyint(alpha * dN_EPI) + nearbyint((1-alpha) * dN_EPI)` does not generally equal `dN_EPI` because of rounding. This means individuals can be created or destroyed at each step, violating conservation of the total population `N`. The correct approach is to draw a binomial subordinate sample: `dN_EP = rbinom(dN_EPI, alpha); dN_EI = dN_EPI - dN_EP`. Over a long simulation, this rounding error compounds.

### 3. [CRITICAL] `H` accumulates `dN_IR` only — asymptomatic infectious `P` are never reported even partially

The measurement equation measures `H`, which accumulates only `dN_IR`. The entire population moving through the P compartment (asymptomatic but, per the model description, also infectious) never contributes to `H`. While the authors intend that P cases are not reported (a design choice), the dmeasure uses a normal approximation to `rho * H` with the implication that `rho` captures under-reporting of symptomatic cases. However, the model forces `rho = 0.95` at the starting point and `rho` converges near 1, meaning essentially all *symptomatic* transitions are reported. Combined with alpha governing the fraction going to P, the identifiability between `alpha` and `rho` is never discussed and their joint uncertainty is not quantified.

### 4. [MAJOR] Time-varying beta implemented as a piecewise covariate with ad hoc breakpoints — no justification or uncertainty

The intervention indicator assigns 6 time periods using hard-coded indices (i <= 24, 25-28, 29-34, 36-41, 42-51, >51), with corresponding beta multipliers b1-b5. The breakpoints do not correspond to any documented epidemiological events or policy changes; they appear chosen visually. No sensitivity analysis is provided for the choice of breakpoints. With 5 free multipliers on a dataset of ~126 days, the model is highly flexible and the likelihood improvement over a simpler model cannot be attributed to biological insight. This parameterization also substantially increases the risk of overfitting.

### 5. [MAJOR] Several key parameters fixed without epidemiological justification

`mu_PR`, `mu_IR`, `alpha`, and `Beta` are fixed throughout local and global search. The paper says "these two parameters can be obtained from statistics" referring to recovery rates, but no source or value is cited for the specific Omicron recovery rate used. `alpha` (the fraction going to P) is fixed at 0.4 with no cited reference. `Beta` (the baseline transmission rate) is fixed at 0.4 with no justification. Fixing parameters without uncertainty quantification means the reported log-likelihood and MLE do not reflect the true uncertainty of the model.

### 6. [MAJOR] `mu_RS` fixed to a value obtained from local search — circular reasoning

After local search, the authors observe that `mu_RS` "explodes to more than 7" and they fix it at 1.529 for global search, citing the impossibility of such rapid reinfection. But given the bug in Issue 1 (dN_RS is drawn from I, not R), this explosion is an artifact. Even setting the bug aside, fixing a parameter at its local MLE from one search round and then running a "global" search is circular: the global search result partially inherits the local search optimum for a key parameter rather than exploring the full parameter space.

### 7. [MAJOR] No profile likelihood or confidence intervals for any parameter

The paper reports a best log-likelihood of -768.17 from global search but provides no confidence intervals for any estimated parameter. Pairs plots are used as a proxy for the likelihood surface, but they show only the sampled log-likelihoods for the 10 chains and cannot substitute for profile likelihood. Given the large number of fixed and free parameters, and the covariate structure, understanding parameter uncertainty is essential and entirely absent.

### 8. [MAJOR] Likelihood benchmark comparison is missing

The best POMP log-likelihood (-768.17) is never compared to that of the SARIMA model on the same data, nor to a simple null model. The paper claims "POMP model can explain the data better" but provides no quantitative basis for this claim. A likelihood-ratio or AIC comparison between the SARIMA and POMP models would substantiate or refute this assertion.

### 9. [MODERATE] Initial conditions are hard-coded and not estimated

The initial E, I, P values (E=100, I=200, P=50) are fixed constants, not linked to any parameter or data. `eta` governs only S and R. This means the model cannot account for uncertainty in the initial epidemic state at December 1, 2021, which is the start of the Omicron wave. For a rapidly growing epidemic at the start of the observation window, the initial conditions can strongly influence the trajectory.

### 10. [MODERATE] Text description of states contains a copy-paste error

In the state description list, `I_t` is listed twice:
- "I_t: the number of people at time t, who have been infected and are showing symptoms."
- "I_t: the number of recovered at time t."

The second entry should be `R_t`. This indicates the model description was not carefully proofread and raises concern about whether model components were fully thought through.

### 11. [MODERATE] Spectral analysis performed on original non-stationary series

The spectral density plot (`spectrum(dat$reports, c(5, 5), ...)`) is applied to the original case counts, which are clearly non-stationary (strong trend through the Omicron peak). Spectrum estimation on a non-stationary series is unreliable; the apparent 7-day period is a plausible artifact of the data collection/reporting cycle, but this should be verified on the differenced or detrended series. The authors note the ACF of differenced data shows 7- and 14-day spikes but do not perform spectral analysis on the differenced data.

### 12. [MODERATE] Particle filter standard error is very large at the starting point (SE = 78.32)

The reported log-likelihood for the initial parameter guess is -3611.64 with SE = 78.32. A standard error this large (relative to the log-likelihood scale) means the particle filter with Np=5000 is essentially failing to track the data at this parameter point. This should be flagged as evidence that the initial parameters are extremely poor, not merely "far from satisfactory." The authors do not discuss the implications for the reliability of the subsequent IF2 optimization.

### 13. [MODERATE] Global search uses only 10 starting points

The global search launches only 10 parallel `mif2` runs from randomly drawn starting points. For a 9-dimensional free parameter space (b1-b5, mu_EPI, rho, eta, tau) with fixed parameters artificially constraining the search, 10 random starts provides very weak coverage of the parameter space. Standard practice is 50-200 starts to improve confidence that the global optimum has been found.

### 14. [MINOR] SARIMA model selection table uses a fixed seasonal AR(1) for all models

The AIC table varies `p` and `q` in SARIMA(p,1,q) but holds the seasonal component fixed at SAR(1) with period 7. There is no exploration of seasonal MA terms or higher-order seasonal AR. The choice of D=0 (no seasonal differencing) is not discussed. The selection procedure is therefore incomplete.

### 15. [MINOR] Introduction data description mismatch

The introduction describes the data plot as showing the full COVID-19 series from "2020-03-01 to 2022-04-06" and references "time 25" and "time 35" for peaks. However, the data are filtered to start at 2021-12-01 for analysis, and the plot uses `Time = 1:n()` starting at 1. The description of the plot does not match either the full historical series (the filter removes early data) or the actual analysis window. The description appears to have been written for a different version of the analysis.

---

## Summary

The project addresses a relevant and interesting epidemiological question and the SEPIR-with-reinfection concept is a reasonable extension of standard SEIR modeling. However, two implementation bugs — the `dN_RS` compartment error and the non-conservative compartment split — undermine the model's correctness at a fundamental level. Beyond these bugs, the heavy use of fixed parameters, ad hoc time-varying beta breakpoints, absence of confidence intervals, and lack of a likelihood benchmark make the quantitative conclusions unreliable. A thorough revision addressing the bugs and adding profile likelihood analysis would substantially strengthen the work.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project04/omicron.c`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project04/Washtenaw.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project04/references.bib`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project04/Makefile`
