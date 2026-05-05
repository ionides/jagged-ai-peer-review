# Peer Review: W25 Project 08
**Title:** STATS 531 Final Project — Netflix Returns Analysis  
**Reviewer:** Charlie  
**Date:** 2026-04-09

---

## Summary

This project analyzes daily log returns for Netflix (NFLX) and the S&P 500 ETF (SPY) over the period January 2015 to April 2025, fitting a stochastic volatility model (SV) via the POMP framework to study latent volatility dynamics. The work follows a logical progression from exploratory analysis, through GARCH/GJR-GARCH benchmarks, to IF2-based maximum likelihood inference for a leverage stochastic volatility model. A notable strength is that the authors provide archived parameter CSVs and .rda files alongside the Rmd, implement both local and global IF2 searches for both NFLX and SPY, and explicitly report AIC to compare the SV model against GARCH. However, the analysis has several significant weaknesses: (1) a fundamental discrepancy between the measurement model in the text and the code undermines internal validity; (2) the global IF2 search produces a lower maximum likelihood than the local search for NFLX, which the authors do not flag as a warning sign; (3) profile likelihoods are entirely absent despite clear evidence of weak parameter identifiability; (4) no simulation-based model diagnostics are performed; and (5) the global search box for phi is defined in natural parameter space, while IF2 perturbations operate in transformed space, creating a subtle but consequential search mismatch.

---

## Major Issues

### 1. Measurement model discrepancy between text and code

The manuscript states (Section 6.1) that the observation noise is $\epsilon_n \sim N(0, \sigma_\nu)$, implying the measurement density is $Y_n \mid H_n \sim N(0, \sigma_\nu \exp(H_n/2))$. However, the C snippet in `pomp_final.Rmd` (line 196) defines the density as `lik = dnorm(y, 0, exp(H/2), give_log)`, with no $\sigma_\nu$ term. The simulation code `rproc2.sim` (line 168) likewise draws `Y_state = rnorm(0, exp(H/2))` without $\sigma_\nu$. This makes $\sigma_\nu$ a phantom parameter: it is declared in `paramnames`, perturbed by IF2, and reported in results, but has no effect whatsoever on the likelihood. The fitted values of $\sigma_\nu$ therefore carry no inferential meaning, and the model actually estimated differs from the model described. Wheeler et al. (2024) document this exact type of code-text discrepancy as a concrete reproducibility failure in their review of published cholera models.

**Fix required:** Either (a) update the C snippets to include `sigma_nu` in the measurement density, i.e., `lik = dnorm(y, 0, sigma_nu * exp(H/2), give_log)`, and re-run all inference; or (b) remove `sigma_nu` from the parameter vector, acknowledge the model has no separate observation noise scale, and revise the mathematical description accordingly. Option (a) is the scientifically motivated choice given the stated motivation (Section 6.1).

---

### 2. Global search fails to improve on local search for NFLX — not acknowledged as a convergence warning

The maximum log-likelihood from the NFLX global search (4619.78, from `nflx_params_global.csv`) is lower than the maximum from the NFLX local search (4622.77). This is the opposite of the expected result: a global search starting from diverse initial conditions should be at least as good as a local search. The failure of the global search to match the local optimum is a strong indicator that 20 replicates with 1000 particles and 100 IF2 iterations are insufficient to reliably find the maximum, and that the reported log-likelihoods may not be close to the true MLE. The text (Section 6.3) actually acknowledges that "we did not achieve a higher likelihood," but frames this as an observation about the likelihood surface rather than a warning about computational inadequacy. According to Wheeler et al. (2024, §Computational adequacy), reported likelihoods that are not near the MLE undermine all downstream conclusions including AIC comparisons.

**Fix required:** Increase computational effort (at minimum Np = 5000, Nmif = 200, Nreps_global = 100) and demonstrate that local and global searches converge to the same likelihood level. The AIC comparison in Section 8 should not be presented as definitive until convergence is established.

---

### 3. No profile likelihoods despite clear evidence of weak identifiability

The authors explicitly note in Section 6.3 that "sigma_nu and sigma_eta show substantial variability across replicates, highlighting parameter uncertainty," and that "the likelihood surface might be flat or multimodal." The local search pairs plot shows multiple high-likelihood parameter combinations with very different values of sigma_nu and sigma_eta. These are the symptoms that call for profile likelihoods (Wheeler et al. 2024, §Parameter identifiability and uncertainty). No profile likelihoods or Monte Carlo Adjusted Profile (MCAP) confidence intervals are presented for any parameter in either asset. Without them, it is impossible to determine whether reported point estimates are meaningful or whether the flat surface reflects genuine non-identifiability.

Additionally, the local search CSV reveals that several replicates converge to phi near 1.0 with sigma_eta > 10, which is a degenerate solution (infinite persistence and extreme process noise). These should be flagged as potential model misspecification rather than alternative local maxima.

**Fix required:** Compute profile likelihoods for at minimum phi, mu_h, and sigma_eta. Report MCAP confidence intervals. Flag degenerate solutions as evidence of potential model misspecification rather than simply "multiple likelihood regions."

---

### 4. AIC comparison between SV and GARCH is not methodologically valid

Section 8.1 claims the POMP model achieves a higher log-likelihood and better AIC than GARCH/GJR-GARCH. However, the GARCH AIC is computed from the `rugarch` package using a per-observation scaling (`infocriteria(nflx_garch)["Akaike", 1] * n_obs`), while the POMP log-likelihood is the log of the predictive likelihood approximated by the particle filter with 1000 particles. These two quantities are not directly comparable: (a) they use different observation models (GARCH conditions on the full history through the volatility recurrence, SV uses a latent state); (b) Monte Carlo error in the particle filter log-likelihood is not accounted for in the AIC calculation; (c) the first observation in the POMP model uses an initial Y_state drawn from `rnorm(0, exp(H_0/2))` that is not a true prediction, potentially inflating the SV log-likelihood. The authors do not acknowledge any of these comparability issues.

**Fix required:** Either restrict the comparison to a carefully aligned one-step-ahead prediction log-likelihood for both models on the same data, or acknowledge that the raw log-likelihood values are not directly comparable and soften the conclusion in Section 8.1.

---

### 5. No simulation-based model validation

The project fits a stochastic volatility model but never uses the fitted model to simulate from the filtering distribution and compare to data. There are no forward simulation plots, no ESS plots shown in the text (they are mentioned as stable but not displayed), no conditional log-likelihood plots identifying periods of poor fit, and no comparison of simulated summary statistics to observed ones. The only model-fit evidence presented is the pairs plots of parameter values across replicates and the raw convergence traces. Per Wheeler et al. (2024, §Model diagnostics), visual comparisons of simulated trajectories to data are a minimum requirement; conditional log-likelihoods are what identify problematic periods. Given that the model is known to have weak identifiability (Issue 3), simulation-based diagnostics are especially important for assessing whether the high log-likelihood represents meaningful model fit or overfitting.

**Fix required:** Simulate trajectories from the model at the MLE and compare to observed log returns. Plot per-observation conditional log-likelihoods to identify dates of poor fit (which likely include the major NFLX crash events already identified in Section 7.2). Plot ESS over time.

---

### 6. Global search box for phi is in natural space, but IF2 perturbations act in transformed space

The global search box for phi is defined as `c(0.9, 0.999)` in natural space (pomp_final.Rmd, line 409), and initial values are drawn uniformly from this interval. However, the `partrans` object (line 200-203) applies a logit transformation to phi. When IF2 starts from, say, phi = 0.99 (natural), the logit-transformed value is `log(0.99/0.01) ≈ 4.6`, and the random walk standard deviation of 0.02 on the logit scale represents a tiny perturbation — this is fine. But the uniform draw in natural space between 0.9 and 0.999 maps to a logit range of approximately 2.2 to 6.9, which is very non-uniform in transformed space and concentrates starting points near the upper boundary. This biases the global search toward high-persistence solutions and may explain why global search replicates cannot find the moderate-persistence solutions (phi around 0.75-0.85) that the local search identifies as the highest-likelihood region.

**Fix required:** Draw starting values for phi uniformly on the logit scale (e.g., between logit(0.9) and logit(0.999), or equivalently between 2.2 and 6.9), which corresponds to uniform coverage in the space where IF2 operates. Alternatively, document this design choice and assess whether it materially affected results.

---

### 7. Incomplete benchmark comparison for POMP versus GARCH

The GARCH(1,1) and GJR-GARCH models are used as benchmarks, which is appropriate. However, the comparison is used only to argue for the SV-POMP model's superiority based on AIC (Section 8.1). No attempt is made to compare models using held-out predictive performance on the test set (2023 onward). The holdout set is defined in Section 2.1 but is never used for ARIMA, GARCH, or POMP evaluation. The paper therefore does not address its own stated research question of whether the POMP model "can better capture the dynamics," because "better" is assessed only in-sample. Wheeler et al. (2024, §Benchmark comparison) emphasize that the comparison must be quantitative; a complete benchmark would include out-of-sample log-likelihood on the holdout period.

**Fix required:** Evaluate GARCH, GJR-GARCH, and SV-POMP models on the 2023–2025 holdout set using one-step-ahead log-predictive scores or RMSE on log returns, enabling a genuine forecast comparison.

---

## Minor Issues

- **Section 3.1 — ACF/PACF interpretation error:** The text states "The ACF plots show slow decay for both series, which is characteristic of non-stationary series." But the series being tested is already the log return (first difference), not the price. Slow decay in the ACF of log returns would indicate autocorrelation in returns, not non-stationarity. In practice, the ACF of returns for both series should show near-zero autocorrelation at all lags if the series are truly i.i.d. — the text contradicts its own conclusion that the series are stationary.

- **Section 3.2 — STL decomposition:** The authors apply STL decomposition to the closing price series with frequency = 252. The resulting "seasonal" component for annual periodicity in a stock price series is not a meaningful economic quantity. The decomposition is not referenced anywhere in the subsequent modeling and appears to be included for completeness without substantive interpretation.

- **Section 6.1 — Notation inconsistency:** The measurement equation states $\epsilon_n \sim N(0, \sigma_\nu)$ (i.e., standard deviation $\sigma_\nu$), but the earlier description says $\epsilon_n$ is "a noisy measurement of $\exp\{H_n\}$ the conditional variance." The roles of $\sigma_\nu$ and the measurement equation are inconsistently described across the two paragraphs of Section 6.1.

- **Section 6.2 — Duplicate code block for spy_local_mif save:** In the blinded.rmd file, the code block at lines 784-794 is an exact copy of lines 772-782 (both save `spy_mif` and `spy_ll_mif` to `spy_local_mif2.rda`). The second block was presumably intended to save `spy_mif_global` and `spy_ll_global` to `spy_global_mif2.rda` but was not corrected before submission.

- **Section 6.3 — Misleading statement about ESS:** The text states "Overall, most of the particles contribute effectively to the posterior at each time step." This is not demonstrated — no ESS plots are shown in the HTML output, and the convergence plots shown are the IF2 parameter traces, not the filtering ESS.

- **Section 8.2 — Incomplete sentence left in manuscript:** The text states "Add direct discussions of how we expanded on the previous projects." This is an unfinished placeholder that was not removed before submission.

- **Reference 5 and 6 — Duplicate and incorrect URLs:** Reference 5 is labeled "Netflix Declining Subscriber Growth — GeekWire" but the URL points to a Bloomberg article. Reference 6 is labeled "Netflix Pricing Increase — Bloomberg" and uses the same Bloomberg URL as Reference 5. These are the same source cited twice under different names.

- **Reference 12 — Incorrect URL:** Reference 12 (Project 11, Winter 2024: NVIDIA Stock Price Analysis) links to `ionides.github.io/531w24/final_project/project07/blinded.html` (Project 7), not Project 11.

- **Section 7.4 — Beta standard error formula:** The standard error for beta is computed as `sqrt(var(NFLX) / (n * var(SPY)))`. The standard OLS formula for the standard error of the slope coefficient is `sigma_eps / (sqrt(n) * sd(SPY))` where `sigma_eps` is the residual standard deviation — the formula used omits the residual variance and is incorrect. The resulting confidence interval is therefore unreliable.

- **No `sessionInfo()` or package versions documented:** The code uses quantmod, rugarch, pomp, and doParallel, which have version-sensitive APIs. No `sessionInfo()` output is included, making exact reproduction difficult. Per the code-supplement checklist, pomp and spatPomp package versions should be explicitly pinned.

- **Data provenance is live/dynamic:** Data is fetched live from Yahoo Finance using `getSymbols()` with a fixed end date of `2025-04-01`. Because Yahoo Finance data is subject to retrospective adjustments (splits, dividend adjustments), results may not be exactly reproducible at a later date even if the code is run with the same parameters. Archived data files (nflx_ohlcv.csv, spy_ohlcv.csv) should be included in the submission.

- **No total computational cost reported:** The project does not report total CPU time or wall time for the IF2 runs. Per Wheeler et al. (2024) and the code-supplement checklist, reporting computational cost allows reviewers to assess whether the effort was adequate and readers to assess feasibility of reproduction.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/blinded.rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/pomp_final.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/nflx_params_local.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/nflx_params_global.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/spy_params_local.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project08/spy_params_global.csv`
