# Peer Review: W22 Project 22 — Volatility Analysis on Ethereum

## Summary

This project applies ARCH/GARCH models and three variants of a stochastic volatility POMP model to the daily log-returns of Ethereum (ETH) prices. The authors follow the standard course POMP template for financial volatility and explore model simplification motivated by parameter convergence behavior. While the project demonstrates solid familiarity with the course toolbox and correctly employs `logmeanexp` aggregation, it has significant methodological gaps: no benchmark comparison against even an IID model, no profile likelihood for any parameter, inadequate convergence diagnostics (parameters described as "still fluctuating" without resolution), and a flawed AIC comparison between GARCH and POMP that ignores likelihood-scale differences. The analytical narrative also lacks quantitative detail in several key places.

---

## Major Issues

### 1. No Non-Mechanistic Benchmark Comparison (CC-Yes, Error 1.6)

The authors compare POMP log-likelihoods only against GARCH, which is itself a parametric model requiring the same estimation effort. No comparison to an IID (e.g., negative binomial or Gaussian i.i.d.) model or ARMA-class model is provided. The course explicitly teaches that a benchmark comparison is necessary to assess whether the mechanistic model adds meaningful structure (Wheeler et al. 2024, §Benchmark comparison; Quiz Q11-01). The weakest meaningful benchmark — fitting an i.i.d. Gaussian or negative binomial to the demeaned returns — would take a single line of code. Without it, the claim that POMP models are superior is unsupported.

### 2. AIC Comparison Between GARCH and POMP Is Not Directly Valid (CC-Yes, Error 2.2)

The authors state "AIC favors POMP model" based on comparing GARCH log-likelihoods (from `tseries:::logLik.garch`) to POMP log-likelihoods (from replicated `pfilter` calls). These likelihoods are computed under different observation models and normalization conventions. The `tseries::garch` function is documented to use a non-standard log-likelihood convention (Quiz Q12-02). The paper makes no note of this potential non-comparability. The conclusion section repeats this claim without qualification: "Our POMP models have higher maximized log likelihood than the GARCH models and AIC favors POMP models."

### 3. No Profile Likelihoods for Any Parameter (CC-Yes, Error 1.9)

The project does not compute profile likelihoods for any of the four key parameters (`mu_h`, `phi`, `sigma_eta`, `H_0`). No confidence intervals are reported for the POMP parameters. The pairs plots provide informal scatter evidence but cannot substitute for formal identifiability checks. Without profiles, it is impossible to determine whether parameters are identifiable, and the point estimates reported at the MLE may be unreliable (Wheeler et al. 2024, §Parameter identifiability). This omission also makes it impossible to assess uncertainty in the leverage-related conclusions.

### 4. Inadequate Convergence: Parameters Described as "Still Fluctuating" Without Resolution

In the local search for the simplified POMP model, the authors write: "Seems that all the parameters are still fluctuating after 100 iterations, we will do the global search to see whether they will converge." The global search trace plots (from `plot(if.box)`) are not accompanied by any written evaluation of whether convergence is achieved. The text only states: "Seems this model is the most unstable one" (for the Force Negative model). Convergence is never formally assessed or resolved for any of the three POMP models. This violates course standard (CC-Yes, Error 1.8): multiple searches must show similar terminal likelihoods and the log-likelihood panel must converge upward. The analysis proceeds to conclusions without establishing that the optimizer has found the global maximum.

### 5. Global Search Starting Box Inconsistency in Force Negative Model

For the Force Negative model's global search (line ~1011–1016 in the Rmd), the text states the box is `mu_h = c(-7,-6)` but the code implements `mu_h = c(-6.6, -6.2)`. This undisclosed narrowing of the search box is problematic: it concentrates the global search in a small region identified from the local search, which undermines the purpose of the global search (to explore diverse starting points). This inconsistency between stated and implemented methodology is a reproducibility concern and suggests the search may not be finding the global maximum.

### 6. Misinterpretation of sigma_nu Convergence to Zero

The original POMP model with leverage is simplified because `sigma_nu` converges to zero. The authors treat this convergence as motivation to simplify: "it motivates us to change and simplify the model." However, convergence of a parameter to its boundary (zero) is a diagnostic signal of potential model misspecification or identifiability failure, not straightforward motivation to fix the parameter at its boundary value. The correct response is to assess whether the leverage parameter is identifiable — via a profile likelihood — and to interpret boundary behavior cautiously (Wheeler et al. 2024, §Parameter identifiability; cf. Model 2 MLE at boundary in Wheeler et al.). Instead, the authors treat the boundary MLE as confirmation that leverage is absent from ETH returns, which may be a significant scientific misinterpretation.

---

## Minor Issues

### 7. run_level = 2 Throughout: Final Results Are Preliminary-Grade

All three POMP models are run at `run_level = 2` (Np = 1000, Nmif = 100, Nreps_global = 20). For a final project, run_level = 3 is the expected standard, particularly when the parameters have not converged at run_level = 2. The authors note instability in convergence but do not increase computational effort as a remedy. While run_level = 2 is not automatically penalized per course conventions, the instability observed here suggests that run_level = 2 is insufficient for these models and that results may not be reliable.

### 8. Nreps_global = 20 in Global Search Is the Minimum

The global search uses only 20 replicates (`Nreps_global = 20` at run_level = 2). Given that multiple runs fail to converge (acknowledged in text) and that the parameter space has 4–6 dimensions, 20 replicates provide weak coverage of the search box. The pairs plots show diffuse clusters with no clear convergence structure. Increasing Nreps_global would strengthen confidence in the reported MLE.

### 9. Initial Simulation Evaluated Only Visually

The model-fit assessment throughout relies entirely on overlaid time series plots of observed vs. simulated returns. The authors state: "We can see the model fits the volatility well." Quantitative goodness-of-fit assessment beyond the log-likelihood table (which itself has the comparability issues noted in Issue 2) is not performed. Conditional log-likelihood plots, effective sample size traces, or simulation-based summary statistics would substantially strengthen the fit assessment (Wheeler et al. 2024, §Model diagnostics).

### 10. Train/Test Split Defined But Never Used

The data is split into train (rows 1–1806) and test (rows 1807–2171) at the start of the analysis (lines 53–54), but the test set is never used for any out-of-sample evaluation, forecasting, or validation. The split is dead code. Either the test set should be used to assess out-of-sample performance, or the split should be removed and the full dataset used for estimation.

### 11. Dmeasure Is Inconsistent with Rproc (Measurement Model Ambiguity)

In both the original and simplified POMP models, `dmeasure` evaluates `dnorm(y, 0, exp(H/2), give_log)`, where `y` is the observed demeaned return. However, `rproc.filt` sets `Y_state = covaryt` and `rproc.sim` sets `Y_state = rnorm(0, exp(H/2))`. The model uses `Y_state` as both a state variable and as the observation. This covariate-injection pattern is standard for this type of stochastic volatility POMP model, but the authors do not explain why this construction is used or verify that it is correctly implemented. The `rmeasure` snippet simply passes `y = Y_state` without any stochastic component, meaning all randomness in the observation equation is actually in `rproc`, not in `rmeasure`. While this is a recognized course pattern, the paper does not acknowledge or explain this architectural choice.

### 12. The Simplified Model Is Not Formally Tested Against the Original

The authors introduce the simplified model (without leverage) and note it has a higher log-likelihood than the original. However, the original and simplified models are nested (the simplified model is the original with `sigma_nu = 0`, `G_0 = 0` fixed). A likelihood ratio test or AIC comparison between these two nested models is never performed. The text only says "the maximized log likelihood becomes larger than the original model" and "AIC favors the simplified POMP model." Since the simplified model has fewer parameters, this favoring should be made explicit with AIC values for both models shown together in a table.

### 13. Pairs Plots Use Different Subsets Across Models (logLik > max - 20 vs. > max - 10)

The local search pairs plots use `logLik > max(logLik) - 20` while the global search pairs plots use `logLik > max(logLik) - 10`. This inconsistency is unexplained and makes visual comparison across models difficult. The 95% Wilks CI threshold is approximately 1.92 log-likelihood units, so the `max - 20` window is very wide and includes many poorly converged runs. Using a consistent threshold (e.g., `max - 10` throughout) would aid interpretation.

### 14. GARCH Likelihood Output from tseries May Not Be Standard

The project uses `tseries:::logLik.garch` (with triple colon, accessing an internal function) to extract log-likelihoods from GARCH models. The `tseries` package is known to report non-standard log-likelihood values (Quiz Q12-02). The authors do not verify that the reported values are on the same scale as the POMP log-likelihoods. The log-likelihood values reported for GARCH models (~2700–2870 range) are in the same order as the POMP values, but this agreement needs to be verified rather than assumed.

### 15. Conclusion Lacks Quantitative Summary Table

The conclusions section claims the simplified POMP model is best, but no summary table of log-likelihoods and AIC values across all models (ARCH(4), GARCH(1,1), GARCH(1,4), GARCH(3,4), original POMP, simplified POMP, Force Negative POMP) is provided in a single location. The GARCH log-likelihoods appear in one table, and the POMP log-likelihoods are scattered across `summary()` outputs throughout the text. A consolidated comparison table would make the main conclusions immediately verifiable.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project22/blinded.Rmd`
