# Peer Review: Volatility Analysis of NASDAQ
**Reviewer:** Charlie  
**Project:** W24 Project 06  
**Manuscript:** Volatility Analysis of NASDAQ (blinded.rmd / blinded.html)

---

## Summary

This project fits ARMA, GARCH, and a stochastic volatility POMP model to NASDAQ daily log returns over approximately five years, using AIC for model selection and likelihood as the primary comparison metric. The paper's stated goal — identifying the best model for financial volatility — is a reasonable applied time series question, and the progression from simple to complex models is logically organized. However, the analysis suffers from several critical flaws: likelihood values across models are reported on incompatible scales and directly compared as if they were comparable, the POMP model fails to beat the ARMA+GARCH benchmark and the authors acknowledge non-convergence without attempting remediation, key POMP diagnostics (profile likelihoods, ESS, convergence traces) are entirely absent, and the model description section contains a notational inconsistency that makes the model specification ambiguous. The conclusions drawn from the POMP analysis are therefore unreliable.

---

## Major Issues

### 1. Likelihood values are compared across incompatible scales

The paper compares log-likelihoods across ARMA, GARCH, and POMP models as if they were on the same scale, but they are not. The `arima()` function in R returns a conventional log-likelihood; the `ugarchfit()` function via `rugarch` reports a scaled per-observation log-likelihood via `infocriteria()`, and the raw value returned by `likelihood()` appears to be the likelihood itself (not the log-likelihood). The paper reports `likelihood(nasdaq_garch41_normal)` = 3476.553 and `log(likelihood(nasdaq_garch41_normal))` = 8.1538, but then states "This model has a likelihood of 3476.553 and a log likelihood of 8.1538." Similarly for GARCH(1,1)-t: likelihood = 3538.768, log-likelihood = 8.1715. Yet the ARMA(4,4) model's log-likelihood is reported directly as 3324.91 from `arima()`. These numbers are presented together and compared in the Conclusions section ("ARMA(4,4) is the best ARIMA model, with a likelihood of 3324.91... GARCH(4,1) has a likelihood of 3476.553... GARCH(1,1) model with t-distributed white noise... has a likelihood of 3538.77"). In fact, comparing 3324.91 (which is a log-likelihood) against 3476.553 (which is a likelihood, not log-likelihood) is meaningless. The values for the GARCH models that should be compared to ARMA are the log-likelihoods (8.15, 8.17, etc.), not the raw likelihood values. This is a fundamental inferential error that invalidates the model ranking in the Conclusions.

**Fix:** The authors must clarify the scale of each reported value, confirm all are log-likelihoods, and re-examine whether model comparisons are valid. Note that models fit to the same data with the same number of observations can be compared via log-likelihood, but the current reporting conflates likelihoods and log-likelihoods.

---

### 2. POMP model does not outperform benchmarks, but no remediation is attempted

The paper reports a POMP global maximum log-likelihood of 3510 (actually 3513 from the summary output), which is lower than the ARMA+GARCH model (stated as 3550.09). The authors acknowledge this in the Conclusions: "POMP model... performs worse than ARMA+GARCH model." However, no substantive remediation is attempted. The authors identify non-convergence of H_0 and mu_h but only list "broader parameters selection" as a limitation. A mechanistic POMP stochastic volatility model should, in principle, achieve a higher likelihood than GARCH-family models on the same data; the failure to do so most likely reflects insufficient computational effort, a poorly specified search box, or unidentifiable parameters — none of which are investigated.

**Fix:** The authors should investigate why the POMP model fails to achieve competitive likelihood. Diagnostic steps should include: (1) examining the pairs plot for identifiability, (2) running additional global search replicates with a better-informed box, (3) checking whether the non-convergence of mu_h and H_0 reflects a fundamental identifiability problem or merely poor initialization.

---

### 3. No profile likelihoods or confidence intervals for POMP parameters

The paper reports no profile likelihoods for any of the four POMP parameters (sigma_nu, mu_h, phi, sigma_eta). The authors note that sigma_nu converges near 0, that mu_h does not converge, and that H_0 does not converge, but make no attempt to assess identifiability. Per Wheeler et al. (2024), profile likelihoods are essential for assessing whether parameters are identifiable from the data, and implausible estimates (e.g., sigma_nu near 0, mu_h estimated around -10 in the local search) should be interpreted cautiously as signs of potential misspecification. Without profile likelihoods, no confidence intervals can be reported and the reliability of any parameter estimates is unknown.

**Fix:** Compute profile likelihoods for at least the key parameters (phi, sigma_eta, mu_h). Report MCAP confidence intervals. Interpret near-zero sigma_nu as a possible sign of model misspecification.

---

### 4. Computational adequacy is insufficient and undocumented

The global search uses only `NADQ_Nreps_global = 100` replicates with `Np = 2000` particles and `Nmif = 200` IF2 iterations. No convergence diagnostics are presented. The pairs plot for the global search covers a 300 log-likelihood unit window (`logLik > max(logLik) - 300`), which is an extremely wide window that includes many poorly converged runs, masking the structure near the MLE. The IF2 convergence traces (from `plot(if.box)`) are mentioned but not interpreted in the text. Per Wheeler et al. (2024), evidence of convergence requires multiple searches from different starting points reaching similar likelihoods — this is not demonstrated. The stochastic variability in the particle filter likelihood estimates (se column from logmeanexp) is not examined.

**Fix:** Show and interpret IF2 convergence traces explicitly. Use a tighter window (e.g., 20 log-likelihood units) for pairs plots. Verify that increasing Np produces stable likelihood estimates. Report computational time and number of cores used.

---

### 5. Model description contains a notational inconsistency (beta_n vs. beta)

In the "Leverage" section, the model equations define H_n using "beta * R_n * exp(-H_{n-1}/2)" where beta appears as a scalar. In the "Main Model" paragraph immediately following, the text states "Where beta_n = Y_n * sigma_eta * sqrt(1 - phi^2)," implying beta is time-varying. In the rprocess code snippet (rproc1), beta is computed as `Y_state * sigma_eta * sqrt(1 - phi*phi)`, confirming beta is time-varying. The text equation for H_n uses beta without the subscript n, creating ambiguity. This is the canonical stochastic volatility model from the course notes but is not properly cited as such, and the notation mismatch between the mathematical equations and the code/paragraph description makes the model specification unclear to the reader.

**Fix:** Either consistently use beta_n in the H_n equation or clarify in the text that beta implicitly depends on n. Cite the original source for this model (Breto et al. 2009 or the course notes) rather than only citing the course slides.

---

### 6. The global search box is inconsistent with local search results

The local search finds that the optimal mu_h is approximately -10 and sigma_nu is near 0. However, the global search box is set to `mu_h = c(-1, 0)` and `sigma_nu = c(0.005, 0.05)`. The local MLE for mu_h (-10) lies far outside the global search box range (-1, 0), meaning the global search cannot explore the region where the local search found the best parameters. This is a critical flaw: the global search is not actually searching a region that includes the best locally found parameters. As a result, the global search maximum (3513) being close to the local search maximum (3509) may simply reflect that both are stuck in a suboptimal region rather than genuine convergence to the MLE.

**Fix:** Expand the global search box to include the parameter ranges suggested by the local search (e.g., mu_h down to at least -15). Re-run the global search with a properly informed box before drawing any conclusions.

---

### 7. ACF/PACF interpretation is used to set ARMA order, bypassing AIC selection

In the data analysis section, the authors interpret the ACF and PACF plots to suggest AR(1) and MA(4) as the appropriate orders. They then conduct an AIC table search across ARMA(p,q) for p,q in {0,...,5}, which correctly selects ARMA(4,4). The initial interpretation of ACF/PACF is therefore redundant and misleading — the spike-counting heuristic identifies different orders (AR=1, MA=4) than the AIC-based selection (AR=4, MA=4). The authors do not reconcile this discrepancy. More importantly, the ACF interpretation is incorrect: spikes in the ACF indicate the MA order, not the AR order; spikes in the PACF indicate the AR order. The paper reverses this ("number of significant spikes in the ACF plot is 1, hence, we can assume that the AR term has value 1").

**Fix:** Correct the ACF/PACF interpretation (ACF guides MA order; PACF guides AR order). Note that for ARMA models the simple spike-counting rule does not apply cleanly. Since AIC table search is performed anyway, the ACF/PACF discussion can be shortened or removed.

---

### 8. No model diagnostics for the POMP model (ESS, conditional log-likelihoods)

The paper presents no particle filter diagnostics for the POMP model. There are no plots of effective sample size (ESS) across time, no conditional log-likelihood plots, no comparison of filtering-distribution simulations to observed data, and no forward simulation comparison. The only "diagnostic" is a single simulation from initial parameter values, labeled as showing poor fit, with no corresponding diagnostic after model fitting. Per Wheeler et al. (2024) and the simulation-study checklist, ESS monitoring is essential for detecting filter degeneracy, and per-time-step log-likelihoods help identify periods of poor fit. Without these, the model's behavior is opaque.

**Fix:** After fitting, run pfilter on the fitted model and plot ESS over time and conditional log-likelihoods. Simulate from the filtering distribution (not just from initial parameters) and compare to observed returns.

---

### 9. GARCH AIC values cannot be compared directly to ARMA AIC due to per-observation scaling

The ARMA AIC table reports values around -6630 (based on the full log-likelihood), while the GARCH AIC table reports values around -5.62 (per-observation, as returned by `infocriteria()` in rugarch). These are on incompatible scales — the GARCH AIC is per observation. With approximately 1257 observations, per-observation AIC of -5.62 corresponds to total AIC of approximately -7072, which is well below the ARMA AIC of -6630. The paper does not acknowledge this scaling difference. While the GARCH models do improve on ARMA (as expected), the comparison is presented confusingly and the AIC values cannot be read directly from the tables as if comparable.

**Fix:** Clarify in the text that the GARCH AIC is reported per observation. Either convert to total AIC for direct comparison or explicitly note the different scales and explain why the comparison is still valid.

---

## Minor Issues

- **Model section title:** "Model Discription" is a typo; should be "Model Description."

- **Global search variable name bug:** In the global search likelihood evaluation loop, `.export = c('NADQ_Nreps_eval', 'NADQ.filt', 'if', 'NADQ_Np')` exports `'if'` which is not a valid variable name (it is a reserved keyword in R). This appears to be a copy-paste error that should be `'if.box'`. It is unclear whether this causes a silent error or is silently ignored in the parallel execution context.

- **Stationarity test conclusion:** The ADF test returns p-value = 0.01 but tseries::adf.test truncates p-values at 0.01. The authors write "The obtained p-value of 0.01 is smaller than the printed p-value" which is technically correct but confusingly phrased. A cleaner statement would note that the p-value is at most 0.01, consistent with strong evidence of stationarity.

- **Missing parameter transformation check:** The partrans definition uses `log=c("sigma_eta","sigma_nu")` and `logit="phi"` but mu_h, G_0, and H_0 have no transformation. This means mu_h, G_0, H_0 are estimated on the untransformed scale. Given the local search finding mu_h near -10 but the global search box constraining mu_h to (-1, 0), this lack of transformation for mu_h is not necessarily wrong but warrants justification.

- **No random seed for reproducibility of ARMA/GARCH sections:** The ARMA and GARCH fitting sections have no set.seed() calls, though these models are deterministic. The POMP section uses set.seed(42). The stew() calls save results to .rda files which help with reproducibility, but the .rda files are not included in the project submission.

- **References are inadequate:** Reference [1] for the GARCH introduction cites Wikipedia for both "NASDAQ" and GARCH modeling, which is inappropriate for the latter. Reference [2] cites only the course slides. The original stochastic volatility model used (Breto et al. 2009, or the course textbook) is not cited. References [2] and [5] are identical.

- **The initial filter likelihood estimate (L.pf1) is reported but not discussed:** The output `-1.824468e+03` is shown for the initial particle filter evaluation but never interpreted. This value of approximately -1824 is far below the final POMP log-likelihood of ~3510, which is suspicious and should be explained — the filtering is apparently being done on the simulated dataset (sim1.filt) rather than the actual data, which may itself indicate a logic error in the setup.

- **Local search pairs plot window is too wide:** Using `logLik > max(logLik) - 300` for the pairs plot includes runs that are 300 units below the best, which is a very large range that obscures the parameter structure near the MLE. A 20-unit window is standard practice and would give more informative plots.

- **The conclusion states the global maximum is 3510 but the summary output shows max = 3513:** This is a minor inconsistency — the text says "the global maximum log likelihood is 3510" but the printed summary shows `Max. 3513`. The authors likely rounded, but should report the value consistently.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project06/blinded.rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project06/blinded.html`
