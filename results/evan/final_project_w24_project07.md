# Final AI Review: Time Series Analysis of Apple Inc. (AAPL) Stock Price
## STATS 531 W24 — Project 07

---

## Overall Assessment

This project tackles a well-motivated application — modeling AAPL daily log returns using ARIMA, GARCH-family, and POMP stochastic volatility methods. The Bretó (2014) leverage model is correctly formulated and implemented using mif2 with logmeanexp-based likelihood evaluation, and the global search with 100 replications reflects sound computational practice. However, the analysis contains a consequential code error in GARCH model selection that undermines the paper's central conclusion, and the POMP analysis lacks profile likelihoods for identifiability assessment. The conclusion that "GARCH is most effective" is not quantitatively supported by the analysis as presented.

## Key Strengths

- **ID: 24.07.str4 | Correct POMP formulation | Why it matters: Core model validity | Suggested author action: None — retain.**
  The Bretó (2014) leverage stochastic volatility model is correctly transcribed and implemented as a POMP object. The measurement model (`dmeasure`) matches the mathematical description.

- **ID: 24.07.str1 | Correct likelihood aggregation | Why it matters: Fundamental POMP correctness | Suggested author action: None — retain.**
  `logmeanexp` is correctly used to combine replicated particle filter log-likelihoods, yielding an unbiased estimate with Monte Carlo standard error.

- **ID: 24.07.str3 | Global search with convergence diagnostics | Why it matters: Good computational practice | Suggested author action: None — retain.**
  The global search uses 100 replications from randomized starting points with convergence trace plots and pairwise scatter plots, providing a reasonable view of the likelihood surface.

## Major Points

**ID: 24.07.M1 | Concern: GARCH model selection inverted (min instead of max log-likelihood) | Why it matters: Invalidates GARCH model choice and the conclusion built on it | Severity: Major | Suggested author action:**
In the basic GARCH grid search, `min_value <- min(garch_table)` selects the model with the lowest log-likelihood, yielding GARCH(1,4) at log-lik 2616. Log-likelihood should be maximized; GARCH(1,1) at 2646 is the correct selection. Correct the search to `max(garch_table)`, re-run diagnostics for the correct model, and update the conclusion accordingly.

**ID: 24.07.M2 | Concern: Central conclusion ("GARCH most effective") unsupported by explicit quantitative comparison | Why it matters: Main claim requires numerical evidence | Severity: Major | Suggested author action:**
Produce an explicit table comparing log-likelihoods (or AIC on a common scale) for ARMA(1,1), GARCH(1,1)-t (correctly selected), and the POMP leverage model. The raw log-likelihoods are comparable across these model classes for the same dataset. Without this table, the claim that GARCH outperforms POMP cannot be assessed.

**ID: 24.07.M3 | Concern: No profile likelihood; parameter identifiability not quantified | Why it matters: Cannot interpret reported parameter estimates without uncertainty bounds | Severity: Major | Suggested author action:**
The paper acknowledges that σ_ν and φ show weak identification in the convergence diagnostics but provides no profile likelihood or confidence intervals. Compute profile likelihoods for at least σ_ν and φ using mif2-based profiling, and report MCAP-based 95% confidence intervals. If the profile is flat, state this explicitly as evidence of non-identifiability.

**ID: 24.07.M5 | Concern: run_level=3 uses only 1000 particles (same as run_level=2); convergence incomplete | Why it matters: Particle count may be insufficient for reliable MLE | Severity: Major | Suggested author action:**
`AAPL_Np = switch(run_level, 100, 1e3, 1e3)` assigns the same particle count to run_levels 2 and 3. Increase Np to at least 5000 for run_level=3, or explicitly acknowledge this limitation and bound the Monte Carlo error in the reported log-likelihood maximum.

## Minor Points

**ID: 24.07.M4r | Concern: No explicit comparison table of log-likelihoods across model classes | Why it matters: Evidence for main conclusion is implicit | Severity: Minor | Suggested author action:**
Add a summary table showing the total log-likelihood for ARMA(1,1), best GARCH, and POMP. Note that these are all valid log-likelihoods for the same data under different model specifications and can be directly compared.

**ID: 24.07.M6 | Concern: Initial conditions G_0=H_0=0 not justified | Why it matters: Initial log-variance affects early observations | Severity: Minor | Suggested author action:**
Add a brief sensitivity analysis for H_0 or justify the choice. If the global search already estimates H_0, verify those estimates are being used in the final model.

**ID: 24.07.m1 | Concern: Ljung-Box used as model selection criterion | Why it matters: Ljung-Box tests residual autocorrelation; it is a diagnostic, not a selection tool | Severity: Minor | Suggested author action:**
Reframe the Ljung-Box result as a diagnostic check that ARMA(1,1) residuals pass, not as justification for model selection.

**ID: 24.07.new1 | Concern: Live Yahoo Finance download creates reproducibility risk | Why it matters: Stock price adjustments may change results | Severity: Minor | Suggested author action:**
Archive the downloaded data as a static CSV file and document the download date.

**ID: 24.07.new2 | Concern: ESS not monitored during particle filtering | Why it matters: Particle degeneracy is common in stochastic volatility models | Severity: Minor | Suggested author action:**
Report effective sample size during filtering runs. Very low ESS would indicate that more particles are needed or that the measurement model is too restrictive.

**ID: 24.07.m2 | Concern: ACF "Lag 0.07" notation confuses fractional and integer lags | Why it matters: Clarity | Severity: Minor | Suggested author action:**
Clarify that lag=1 (one trading day) appears at position 1/253 on the fractional axis, or simply refer to it as "the first lag."
