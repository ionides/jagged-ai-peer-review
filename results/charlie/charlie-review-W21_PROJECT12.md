# Peer Review: W21 Project 12
## Analysis on Nasdaq-100 Index for the Past 5 Years

---

## Summary

This project applies ARMA, GARCH, and POMP stochastic volatility models to daily log-returns of the Nasdaq-100 index from April 2016 to April 2021, motivated by the goal of understanding volatility dynamics and leverage effects. The POMP model follows the Breto (2014) stochastic leverage framework. While the project demonstrates competent use of the pomp package and correctly applies iterated filtering with a global search, it has several significant methodological and reporting deficiencies: the cross-model AIC comparison is invalid due to non-standard GARCH likelihood normalization, convergence diagnostics are entirely absent, no profile likelihoods are computed, and the conclusion contains systematic errors in referring to the index. The filtering-for-simulated-data section is inconclusive and the reported low likelihood is never diagnosed.

---

## Major Issues

### 1. Invalid cross-model AIC comparison due to non-standard GARCH likelihood (CC-Yes, Error 2.9)

The authors compute AIC for GARCH using `tseries:::logLik.garch` and directly compare this to AIC from `arima()` and the POMP particle filter. The `tseries` GARCH implementation is known to report log-likelihoods under a non-standard normalization convention. The course explicitly taught that likelihoods from different packages must be checked for normalization conventions before comparison (Error 2.9). The authors report GARCH AIC = -7839 and POMP AIC = -7948 and treat these as directly comparable without any comment on the potential scale difference. If the tseries normalization differs (as documented in the course), the conclusion that "POMP outperforms GARCH" may be artefactual. The authors must either verify that `tseries:::logLik.garch` uses the same normalization as `arima()` and the pomp particle filter, or acknowledge this as a limitation.

### 2. Missing convergence diagnostics for iterated filtering (CC-Yes, Error 1.8)

The project reports final parameter estimates and log-likelihood values from both local and global mif2 searches but provides no trace plots showing log-likelihood or parameter trajectories across mif2 iterations. Without these diagnostics, there is no evidence that the optimizer found the global maximum. The pairs plot from the local search is not a convergence diagnostic: it shows the final scatter of parameter estimates across replicates but does not show whether individual runs converged. The course standard is to show the log-likelihood panel increasing consistently across iterations (531-conventions.md). This is a course-confirmed error (Error 1.8, CC-Yes) and threatens the validity of all downstream conclusions.

### 3. No profile likelihoods computed (CC-Yes, Error 1.9)

Profile likelihoods are not computed for any of the six model parameters. The only uncertainty information provided is the pairs plot from the local search (subset with logLik > max - 30), which does not constitute a profile likelihood. Without profiles, parameter identifiability cannot be assessed, confidence intervals cannot be reported, and the plausibility of the MLE cannot be verified. Given that the model includes four parameters (sigma_nu, mu_h, phi, sigma_eta) plus two initial condition parameters, some parameters (particularly phi, which is likely poorly identified near 1) may be weakly identified. This is a course-confirmed error (Error 1.9, CC-Yes).

### 4. Global search initialized from a single local search result

The global search code (lines 457-459 of blinded.Rmd) calls `mif2(if1[[1]], start=apply(ndx_box, 1, function(x) runif(1, x)))`. This initializes each global search replicate from `if1[[1]]` -- the first local search result -- rather than from a fresh pomp object. The consequence is that mif2 settings (e.g., cooling schedule) are inherited from a partially converged run rather than reset. The correct practice for a box search is to initialize from a base pomp object or a randomly drawn parameter vector, not from a specific mif2 result. This may bias the global search toward the region of parameter space explored in the local search, defeating the purpose of the global search.

### 5. Filtering for simulated data is inconclusive and undiagnosed

The section "Filtering for simulated data" reports that "The log likelihood seems to be very low" but provides no quantitative result, no diagnosis, and no follow-up. The section notes that simulated data is "much more volatile than the actual demeaned return" -- which itself suggests model misspecification or parameter miscalibration at the chosen initial values -- but this observation is never used to revise the model or initial parameters. According to course instruction (Error 1.5, CC-Yes), a declining or very low likelihood during iterated filtering signals model misspecification; the correct response is structural revision, not simply moving on to fitting the actual data with the same model. The section as written adds no analytical value and leaves a key diagnostic unexplored.

---

## Minor Issues

### 6. Np = 2000 at run_level = 3 is below the course standard

The code sets `ndx_Np <- switch(run_level, 100, 1e3, 2e3)`, giving Np = 2000 at run_level = 3. The course standard for run_level = 3 is Np = 5000 (531-conventions.md). While the conventions note that appropriate values are context-dependent, the authors do not explain why 2000 particles is sufficient for this model, and the Monte Carlo standard errors on the reported log-likelihoods are not discussed. If the standard error is non-negligible relative to the GARCH-POMP AIC difference of ~109 units, this is not a concern; but if it is comparable to the ARMA-POMP AIC difference of ~678 units, it equally is not a concern -- however, the authors should verify that MC noise is not inflating the apparent advantage of POMP.

### 7. No benchmark comparison on the POMP likelihood scale

The project compares ARMA, GARCH, and POMP using AIC but does not provide a direct benchmark of the POMP model against an IID or simple AR model on the particle-filter likelihood scale. Per Wheeler et al. (2024) and course instruction (Error 1.6, CC-Yes), benchmarking the POMP log-likelihood against a simple model (e.g., an IID Gaussian or the ARMA(3,1) likelihood re-expressed on the same scale) would confirm whether the POMP model is capturing meaningful latent dynamics rather than noise.

### 8. No model diagnostics beyond visual residuals

The project assesses model fit only through residual plots and ACF of residuals. There are no conditional log-likelihoods plotted to identify time periods of poor fit, no ESS monitoring across the particle filter, and no comparison of filtering-distribution simulations to observed data. For a stochastic volatility model applied to financial data, the COVID-19 period (early 2020) is likely to stress the model, and period-specific diagnostics would be informative (Wheeler et al. 2024, Model diagnostics checklist item 4).

### 9. Systematic error: index referred to as "Nasdaq-500" throughout conclusion

The introduction correctly identifies the index as the Nasdaq-100. However, the conclusion (and the reference section) consistently calls it "Nasdaq-500" (e.g., "Nasdaq 500 index data," "Nasdaq-500 Index"). This is factually incorrect and should be corrected throughout.

### 10. Breto (2014) not cited as primary reference

The model is described as following "the implementation of Breto (2014)" but reference [2] points to the course lecture notes, not to the Breto (2014) paper itself. The actual citation -- Breto, C. (2014). On idiosyncratic stochasticity of financial leverage effects. Statistics & Probability Letters, 91:20-26 -- is not included in the reference list. Given that the model equations are taken directly from Breto (2014), this is a missing primary citation.

### 11. The pairs plot threshold (logLik > max - 30) is not justified

The pairs plot uses a threshold of `logLik > max(logLik) - 30`, which is substantially wider than the Wilks 95% confidence set threshold of approximately 1.92 log units. While this is not wrong -- a wider threshold shows more of the parameter space -- the threshold should be noted and the distinction between the displayed region and a formal confidence set should be stated.

### 12. Nreps_local = 20 at run_level = 3 is below the course standard

The code sets `ndx_Nreps_local <- switch(run_level, 10, 20, 20)`, giving 20 local search replicates even at run_level = 3. The course standard for run_level = 3 is 40 replicates (531-conventions.md). As with the Np setting, the authors do not explain this choice.

### 13. No discussion of parameter interpretation against external knowledge

The estimated parameters (phi near 0.98, sigma_eta around 1.2, sigma_nu near 0.01 based on the pairs plot) are not compared to published estimates for similar stochastic volatility models of equity indices. The course checklist item 11 (corroboration with scientific knowledge, Wheeler et al. 2024) calls for checking whether estimated parameters are biologically or financially plausible. In particular, the near-unit-root persistence in H (phi close to 1) should be flagged and discussed.

### 14. Causal/predictive language in conclusion is unsupported

The conclusion states that "the models constructed for volatility of Nasdaq-500 Index are not perfect, and still have a lot of room for improvement." While this is true, the project makes no attempt at forecasting or out-of-sample evaluation. The claim that the POMP model is "appropriate" is supported only by in-sample AIC, with no validation. The conclusion overstates what has been demonstrated.

### 15. Missing sessionInfo or package versions

The project loads pomp, foreach, doParallel, doRNG, tidyverse, kableExtra, and tseries but does not report package versions or a sessionInfo() call. Given that the pomp API has changed across versions, results may not reproduce on current CRAN releases (code-supplement-checklist-pomp.md).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project12/blinded.Rmd`
