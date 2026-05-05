# Peer Review: W22 Project 09
## Time Series Analysis of COVID-19 Cases in Washtenaw County

---

## Summary

This project applies an SEIR compartment model to daily COVID-19 case counts in Washtenaw County, Michigan from July 2021 to April 2022. The authors use `pomp` for likelihood-based inference via iterated filtering (mif2) and particle filters, and compare to negative binomial and SARIMA benchmarks. The use of a time-varying contact rate to capture the Delta-to-Omicron transition is a sensible modeling choice, and the comparison against non-mechanistic benchmarks is commendable. However, the report has several serious deficiencies: the global search uses only a single mif2 pass per starting value rather than two (violating the two-phase convention needed for adequate convergence), mu_IR is fixed without justification, the SARIMA log-likelihood comparison conflates transformed and original scales without an adequate Jacobian correction, convergence diagnostics show a non-increasing likelihood, and no profile likelihoods or identifiability analysis are provided for any parameter. These issues collectively undermine confidence in the reported MLE and downstream conclusions.

---

## Major Issues

### 1. Global Search Uses Only One mif2 Pass Per Starting Value (Convergence Inadequacy)

The global search code (chunk `global`) calls `mif2()` once and then immediately a second `mif2(Nmif=100)` chained on the same object, which is correct in structure, but the first call uses `mf1` (the first element of `mifs_local`) without specifying `Nmif` or `Np`, inheriting them from `mf1`. This means the effective number of iterations for the first pass is whatever `mifs_local[[1]]` has already converged to — the first call effectively re-runs from a new starting point using the local search settings and then runs a second 100-iteration pass. More critically, the local search itself (chunk `local`) already showed that "likelihood does not strictly increase as iterations proceed, which may indicate a problem." The authors note this problem but do not investigate it further, do not revise the model, and proceed to global search anyway. Per the course standard (and Error 1.8 in the weakness reference), declining or non-monotone likelihood during iterated filtering is a signal of model misspecification, not just insufficient computation. The correct response is to diagnose and address the model structure, not to continue with global search. No global search trace plots or convergence diagnostics are shown, making it impossible to assess whether the 500-replicate global search found a consistent maximum.

**Fix:** Show convergence traces for the global search (loglik and parameter panels). If loglik is not consistently increasing, investigate model structure (e.g., add overdispersion noise in transmission, reconsider fixed mu_IR). Multiple global searches finding consistent terminal likelihoods are the minimum standard.

---

### 2. mu_IR Fixed Without Biological Justification

The authors fix `mu_IR = 0.2` (implying a mean infectious period of 5 days) without any citation or sensitivity analysis. The value is described only as "An intuitive value" and is never compared against external estimates for Delta or Omicron COVID-19 variants. Fixing a structurally important parameter without justification can produce biased estimates of the remaining parameters (especially beta). Per Wheeler et al. (2024), implausible or unjustified parameter values may indicate model misspecification rather than biological facts, and profile likelihoods should be used to assess identifiability.

**Fix:** Either cite a source for mu_IR = 0.2 specific to the Delta/Omicron period, estimate it via profile likelihood, or at minimum present a sensitivity analysis showing how the reported MLE and loglik change across a plausible range of mu_IR values.

---

### 3. No Profile Likelihoods for Any Parameter

The report does not compute or show profile likelihoods for any of the estimated parameters (b1, b2, rho, mu_EI, eta, tau). Without profile likelihoods, there is no evidence that the parameters are individually identifiable from the data, and no valid confidence intervals can be reported. The pairwise scatter plot of local search results is a weak substitute — it shows posterior spread of optimizer runs, not the profile likelihood surface. This is a course-confirmed error (Error 1.9 in the weakness reference) and violates the core POMP checklist item #5 (parameter identifiability and uncertainty).

**Fix:** Compute profile likelihoods for at least the scientifically key parameters (b1, b2, rho). Report 95% confidence intervals via the Wilks threshold. A coarse profile with ~10–20 points per parameter at run_level=2 is sufficient.

---

### 4. SARIMA Log-Likelihood Comparison Uses an Incorrect Jacobian Correction

The ARMA benchmark computes a log-likelihood on log-transformed data and then applies a Jacobian correction of `-sum(log_cases)`, which equals `-sum(log(1 + y_n))`. This correction assumes the transformation is `log(y)`, not `log(1 + y)`. For the transformation `z = log(1 + y)`, the correct Jacobian term is `-sum(log(1 + y_n))` (which is what `sum(log_cases)` computes since `log_cases = log(1 + Cases)`), so the formula is actually correct in this specific case. However, the authors report the corrected loglik as `-1308.984` and compare it directly to the SEIR model loglik of `-1547` on the raw count scale. This comparison implies the SARIMA model substantially outperforms the SEIR model. The authors acknowledge this ("The corrected log-likelihood for the original data is -1308.984, which is slightly higher than that of global search") but understate the magnitude — a gap of ~238 log-likelihood units is not "slightly higher"; it is a massive difference that should prompt revision of the SEIR model. The authors attribute the gap to the SEIR model not capturing periodicity, but do not act on this finding.

**Fix:** Quantify the loglik gap explicitly and discuss whether it falls within the range where a mechanistic model might still be useful, or whether it indicates fundamental model misspecification. Per course conventions (Ch 17), a mechanistic model fitting disastrously compared to a benchmark means the model is likely missing something important.

---

### 5. Non-Monotone Likelihood During Local Search Is Noted But Not Addressed

The authors explicitly state: "our likelihood does not strictly increase as iterations proceed, which may indicate a problem." However, no remediation is attempted. Per Error 1.5 in the weakness reference (quiz-tested), a declining or non-monotone likelihood during iterated filtering after some initial increase is a signal of model misspecification, not merely insufficient computation. The authors attribute this to "fluctuation" without further investigation. The correct diagnosis requires examining whether the model structure is adequate.

**Fix:** Investigate whether the measurement model, process noise specification, or parameter constraints are causing the non-monotone loglik. Consider adding environmental stochasticity to the transmission rate (multiplicative gamma noise), which is the standard for COVID-19 SEIR models. Show that increasing Np does not resolve the issue, confirming model misspecification as the cause.

---

### 6. Measurement Model Uses Normal Approximation Instead of Count Distribution

The measurement model (`seir_dmeas`) uses a normal approximation to a count distribution: `pnorm(Cases+0.5, mean=rho*H, sd=sqrt((tau*H)^2 + rho*H), ...)`. While this continuity-corrected normal approximation is defensible for large counts, it can produce negative case values (see `seir_rmeas`, which uses `rnorm` and clips to 0) and may produce poor likelihood evaluations when H is small or zero. The mathematical specification in the text describes only the mean and sd without formally introducing the approximating distribution. A negative binomial measurement model, which is the standard course approach and better handles overdispersion in count data, would be preferable. Per POMP checklist item #12, the measurement model should be carefully specified and the code must match the text — here, the text does not specify the normal approximation, only the moments.

**Fix:** Either formally justify the normal approximation in the text and show it is adequate for the range of H values encountered, or switch to a negative binomial measurement model consistent with the course standard.

---

### 7. H Accumulator Tracks Recoveries, Not New Cases

The accumulator variable H is defined as `H += dN_IR` (transitions from I to R), so H counts cumulative recoveries within each observation interval. However, COVID-19 case counts represent newly confirmed infections (transitions from S to E or E to I), not recoveries. The reporting model `rho*H` thus models reported cases as a fraction of recoveries, which is scientifically incorrect — reported cases should be proportional to new infections (dN_SE or dN_EI), not recoveries. This is a structural flaw that invalidates the biological interpretation of the reporting rate rho. The initial guess section also uses 30 initial infected based on "confirmed cases on July 1st," which is consistent with an infection-reporting model, not a recovery-reporting model.

**Fix:** Change the accumulator to track new infections: `H += dN_SE` (or `dN_EI`) and update the measurement model accordingly. This is a material error that affects the scientific interpretation of rho and the quality of fit.

---

## Minor Issues

### 8. Initial Conditions: E and I Fixed Without Justification

The initial conditions fix E = 30 and I = 30 as "intuitive values" but these are not estimated as parameters and no sensitivity analysis is provided. The initial infected count of 30 is described as based on "confirmed cases on July 1st" but July 1, 2021 had far fewer than 30 confirmed cases in Washtenaw County (the Delta wave had not yet peaked). Per POMP checklist item #13, initial conditions can substantially affect model fit and should be estimated or justified. In Wheeler et al. (2024), initial conditions affected AIC by ~72 units for one model.

**Fix:** Estimate E_0 and I_0 as parameters (standard approach: parameterize as fractions of N), or cite a data source justifying the fixed values.

---

### 9. Benchmark Comparison Gap Is Undercharacterized

The authors say the SARIMA corrected loglik of -1308.984 is "slightly higher" than the SEIR global search loglik of -1547. A difference of ~238 log-likelihood units is enormous (AIC difference ~476 units). The authors attribute this to the SEIR model not capturing weekly periodicity, but this is a major finding that should prompt model revision (e.g., adding day-of-week reporting effects), not just a note in the conclusion. Per course convention (Ch 17), "If the mechanistic model fits disastrously compared to the benchmark, our model is probably missing something important."

---

### 10. Global Search Box for b1 and b2 Includes Zero

The global search lower bounds for b1 and b2 are both set to 0. A contact rate of 0 means no transmission, which is epidemiologically degenerate. Including zero in the search box can cause numerical problems in the particle filter (degenerate trajectories). The search range for b2 (0 to 10) is also very wide without justification from the literature on COVID-19 contact rates.

**Fix:** Set lower bounds for b1 and b2 to a small positive value (e.g., 0.1). Justify the upper bounds with reference to known COVID-19 reproduction numbers and generation times.

---

### 11. No Model Diagnostics Beyond Visual Simulation Comparison

The report shows simulations from the fitted model but does not compute conditional log-likelihoods per time point, effective sample size (ESS) traces, or filtering-distribution-conditioned simulations. These diagnostics would identify specific periods where the model fits poorly (e.g., the Omicron peak in January 2022) and guide model improvement. Per POMP checklist item #4, such diagnostics are essential for understanding model adequacy.

---

### 12. Covariate Intervention Split Is Hard-Coded Without Robustness Check

The `seir_covar` defines intervention = 0 for the first 154 days and intervention = 1 for the remaining 125 days, corresponding to the Delta/Omicron split at December 1, 2021. The split is motivated by CDC data but is not treated as a parameter — it is hard-coded. The sensitivity of results to the exact split date is not explored. A one- or two-week shift in the split date could materially affect b1 and b2 estimates.

---

### 13. Local Search Uses Only 20 Replicates Starting from the Same Point

The local search runs 20 mif2 replicates all starting from the same parameter vector `(b1=2.3, b2=5.2, ...)`. This is useful for diagnosing identifiability (spread in parameters with similar loglik) but does not explore the likelihood surface more broadly. The local search is typically used to refine a good starting point; here it is the sole basis for concluding that b2 > b1 before global search results are examined.

---

### 14. Missing sessionInfo() and Package Version Documentation

The code supplement does not include `sessionInfo()` output or package version documentation. Given that the `pomp` API has changed substantially across versions, results may not be reproducible on current CRAN releases. Per the code supplement checklist, software versions should be documented.

---

### 15. The Caption for Figure 1 Is Repeated in the Text Verbatim

The paragraph following Figure 1 (line 68 in the Rmd) repeats the figure caption text verbatim: "Figure 1 shows a time series plot smoothed by the Loess method, where the blue smoothed line displays an increasing trend before January 2022 and a decreasing trend after that. Figure 2 shows the average COVID-19 cases by month, where a peak in January 2022 is very obvious." This text already appears in the caption for Figure 1 (lines 47-48) and Figure 2 (lines 57-58), making it redundant in the body.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project09/final_proj_531.Rmd`
