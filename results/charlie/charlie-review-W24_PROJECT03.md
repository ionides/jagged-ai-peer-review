# Peer Review: W24 Project 03
**Title:** Analysis on Covid-19 Cases in Japan
**Reviewer:** Charlie
**Date:** 2026-04-09

---

## Summary

This project analyzes COVID-19 weekly case counts in Japan using two approaches: a SARIMA time-series model and a stochastic SEIR compartmental model fit via iterative filtering (IF2) in `pomp`. The SEIR model incorporates a time-varying contact rate structured around key pandemic events (lifting of the state of emergency, vaccine rollout, the Tokyo Olympics), and inference is restricted to the 2020–2021 period to avoid confounding by the Omicron variant. While the use of a stochastic process model with likelihood-based inference is a genuine strength, the analysis suffers from serious methodological flaws: a critical unit inconsistency in two fixed epidemiological parameters, pervasive convergence failure across global searches, a poorly constructed profile likelihood, and a total absence of model diagnostics. Additionally, the ARMA and SEIR models are fit to different data sets, making any comparison between them impossible.

---

## Major Issues

### 1. Unit inconsistency in fixed epidemiological parameters

The text states that the incubation rate is $\mu_{EI} = 1/6.5\,\text{day}^{-1} \approx 0.154$ and the recovery rate is $\mu_{IR} \approx 0.1\,\text{day}^{-1}$, both justified by CDC references. However, the data have been subsampled to one point per week (`seq(1, nrow, 7)`), so the Euler step `delta.t=1` corresponds to one week (7 days), not one day. The code fixes `mu_EI = mu_IR = 0.1` but never converts these rates to a per-week basis. Consequently, `1/mu_EI = 1/mu_IR = 10` time units, i.e., 10 weeks, which is a biologically implausible incubation period of roughly 70 days — more than ten times the claimed value of 6.5 days. Because these parameters are fixed throughout all searches, every reported log-likelihood and every simulation is biologically misspecified at the process level. The authors should either convert the rates to per-week values ($\mu_{EI}^{(\text{week})} = 1 - e^{-0.154 \times 7} \approx 0.66$ per week in the binomial probability parameterization) or re-run inference with the correct values.

### 2. No benchmark comparison between ARMA and SEIR

The SARIMA and SEIR analyses proceed in parallel but are never directly compared using a common quantitative criterion. Wheeler et al. (2024) identify benchmark comparison as the single most diagnostic check for whether a mechanistic model captures meaningful structure. Here the comparison is impossible by construction: the SARIMA model is fit to 222 weekly observations (January 2020–March 2024), whereas the SEIR model is fit to approximately 104 weekly observations (January 2020–December 2021). The log-likelihoods are therefore not comparable, and the two models address different prediction targets. The authors should either (a) fit both models to the same data span and compare log-likelihoods directly, or (b) acknowledge explicitly that no comparison is being made and explain why.

### 3. Pervasive convergence failure across global searches

The reported best log-likelihoods differ dramatically across the four optimization runs:

| Search | Best log-likelihood |
|---|---|
| Initial `pfilter` | -4219.6 |
| Local search (10 chains, Nmif=50, Np=10000) | -2205.9 |
| Global search 1 (500 starts from local-search box) | -3531.9 |
| `global_search_results` (mifs\_global, 10 starts) | -4457.8 |
| Global search 2 (100 starts, Nmif×7=350) | -1083.8 |
| Global profile (200 starts, profile on $\rho$) | -1079.9 |

Three of the four global searches are substantially *worse* than the local search, indicating that the global searches were exploring the wrong region of parameter space (see also Issue 4 below). None of this is acknowledged in the text, which presents the searches sequentially as if they represent iterative improvement. The authors should present convergence traces for all searches on the same axes, explain the divergence in log-likelihoods, and use only the best-performing parameter vector as the basis for inference and simulation. Wheeler et al. (2024) emphasize that insufficient computation can make even good models look bad; conversely, when global searches consistently underperform local ones, this signals a fundamental problem with the search strategy.

### 4. Global search box excludes the true MLE region

Global search 1 draws starting values from the box `b1∈[50,75], b2∈[100,300], b3∈[0,25], b4∈[0,30], tau∈[0,0.006]`. The best parameters found by global search 2 and the profile are `b1≈97, b2≈1.2, b3≈42, b4≈7, tau≈0.6–1.0`. Every one of these falls outside the global search 1 box: b1 exceeds the upper bound of 75, b2 is 80× below the lower bound of 100, b3 exceeds the upper bound of 25, and tau is 100× above the upper bound of 0.006. Because the box was derived from visual inspection of the local search trace plots (which themselves did not converge to the global maximum), the global search 1 is guaranteed to miss the MLE. Similarly, `mifs_global` (global_search_results) uses a box `tau∈[0,0.01]`, again excluding the true MLE region. A proper global search should use a biologically motivated box rather than one derived from a single inadequate local search.

### 5. Profile likelihood is unreliable and covers only one parameter

The profile likelihood for $\rho$ is based on only Np=1000 particles and NREPS_EVAL=10 replicates, compared to Np=10000 and 200 replicates used in the local search. With such low particle counts, the log-likelihood estimates are noisy, and the resulting profile curve is unreliable. More critically, only 3 of the 200 starting points produce log-likelihoods above the 95% confidence cutoff (-1081.82). Deriving a confidence interval from 3 scattered points is not statistically sound; the profile curve may not have been adequately maximized at those $\rho$ values and the true 95% CI boundary may lie elsewhere. Furthermore, profiles are reported for $\rho$ only; there are no profile likelihoods for the four $\beta$ parameters, $\eta$, or $\tau$, so identifiability of the remaining parameters is completely unassessed. Wheeler et al. (2024) flag the absence of profile likelihoods as a key weakness preventing any assessment of parameter identifiability.

### 6. No model diagnostics

The paper provides no particle filter diagnostics: there are no effective sample size (ESS) traces, no per-observation conditional log-likelihood plots, and no filtering-distribution simulations compared against forward simulations. Without ESS monitoring, it is impossible to know whether the particle filter degenerates (ESS collapsing to near 1) during likelihood evaluation, which would invalidate all log-likelihood estimates. Conditional log-likelihood plots would reveal which time periods drive the poor fit. Wheeler et al. (2024) demonstrate that these diagnostics led to key model improvements (e.g., discovery of the hurricane parameter for the cholera model). The absence of any diagnostics here means the authors cannot localize model failures or assess whether the SEIR structure is fundamentally incompatible with the data.

### 7. Data handling: subsampling instead of aggregating

The "weekly" data are created by `covid_japan_week <- covid_japan[seq(1, nrow(covid_japan), 7), ]`, which takes every 7th row from daily data. This is subsampling (selecting a single day's count per week), not weekly aggregation. As a result, each observation represents cases on one specific day rather than the total cases over a 7-day period. This induces high variability from day-of-week reporting patterns and discards 6/7 of the available data. The SEIR model assumes that `H` accumulates all transitions over a week, which is inconsistent with the observation being a single-day count. The correct approach is to sum daily cases within each 7-day window.

### 8. Fixed initial conditions E=100, I=200 with no sensitivity analysis

The initial conditions for the Exposed and Infectious compartments are fixed at E(0)=100 and I(0)=200 (Section "Model Initialization"). These values are arbitrary and could substantially influence model fit during the first weeks of the time series. Wheeler et al. (2024) note that initialization strategy affected AIC by ~72 units in a comparable model. Because only the susceptible fraction $\eta$ is estimated via `ivp(0.02)`, the model initialization is partially ad hoc. The authors should either estimate E(0) and I(0) as free parameters, justify the chosen values from external data, or perform a sensitivity analysis showing that the reported log-likelihoods are robust to the initialization.

---

## Minor Issues

### 9. SARIMA equation uses $B^{12}$ but code implements period=4

The mathematical specification of the SARIMA model (Section "Model Specification") writes the seasonal components as $\Phi(B^{12})$ and $\Psi(B^{12})$, which corresponds to a period of 12 (appropriate for monthly data). However, the code uses `seasonal=list(order=c(1,0,1), period=4)`, which correctly implements the period of ~4 weeks identified by spectral analysis. The equation is a notation error carried over from a template for monthly data. The text and equation should be updated to use $B^4$ consistently with the code.

### 10. Convergence not achieved in local search for b4, eta, tau

The text acknowledges (Section "Local Search") that "for b4, eta and tau, there are still some variability, indicating potential uncertainty in these estimates or more iterations may be needed for convergence." Despite this acknowledgment, no additional local search iterations are run before proceeding to global search. The trace plots of the local search show the log-likelihood still improving at iteration 50, and the best local log-likelihood (-2205.9) is substantially below what is achieved later (-1079.9). A more thorough local search (higher Nmif or a second stage) should be completed before using the local search output to inform global search bounds.

### 11. Global search 2 misleadingly labeled as "not based on local search"

The code at line 671 reads `mf1 = mifs_local[[1]] # take the output of previous IF process (local search)`, so the global search 2 uses the local search mif2 object as its starting structure (inheriting the `rw.sd` schedule from the local search). This contradicts the section heading "Not Based on Local Search." The only element not inherited from the local search is the starting parameter values, which are drawn from a new box. The inherited `rw.sd` from the local search (with very small perturbation for tau=0.0001) nonetheless shaped the optimization trajectory. The authors should clarify what "not based on local search" means or relabel the section.

### 12. Conceptual error: log-likelihood normalization

After presenting global search 1 results (Section "Based on Local Search"), the text states: "the reasons might be that the new cases number is too high. And log scale may be needed to normalized the log-likelihood." This conflates two unrelated concepts: a log transformation of the response variable and the scale of the log-likelihood itself. Log-likelihood values are not "normalized" — they are compared across models on the same data. The poor simulation from global search 1 is attributable to the box misalignment (Issue 4), not to the scale of the observations.

### 13. Auto-installing packages violates reproducibility norms

The setup chunk calls `if (!require("pkg")) install.packages("pkg")` for all 11 packages. This silently modifies the user's R library without consent and may install versions inconsistent with those used by the authors. The code supplement checklist requires that software versions be documented and that packages not be auto-installed. At minimum, a `sessionInfo()` call or an `renv` lockfile should be provided so that the package versions used are known.

### 14. Sparse quantitative reporting of SEIR fit quality

The paper presents simulation overlays comparing the model to data, but these are the only goodness-of-fit assessments for the SEIR model. No AIC is computed, no residual analysis is shown, and the log-likelihood values are scattered across sections without a clear summary table. Wheeler et al. (2024) note that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." A table summarizing the best log-likelihood for each search, along with the corresponding parameter values, would substantially improve transparency.

### 15. Rho confidence interval interpreted without considering model misspecification

The wide 95% CI for $\rho$ (0.66–0.93) is interpreted as evidence of "stringent disease reporting and control measures." However, an overly wide or implausible CI can equally indicate model misspecification. With only 3 points above the chi-square cutoff (-1081.82) and large uncertainty in tau (ranging from 0.05 in local search to 1.05 in the profile), the profile is unreliable and the CI should not be interpreted substantively without first resolving the convergence and computational issues noted above.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/blinded.qmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/Makefile`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/lik_starting_vals.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/local_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/global_search_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/global_search_2.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/global_search_results.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/global_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project03/mifs_global.rds`
