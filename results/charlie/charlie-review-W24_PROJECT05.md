# Peer Review: W24 Project 05 — Modeling Flu Cases in Oklahoma

## Summary

This project applies time series methods to weekly influenza case counts in Oklahoma (2011–2015) from the CDC FluView dashboard, aiming to assess whether a SEIRS POMP model improves upon a SARIMA baseline. The authors fit a SARIMA((1,1,1)×(0,1,1)[52]) model and a seasonally-forced SEIRS POMP model via iterated filtering (IF2), then compare their log-likelihoods. Genuine strengths include a clear model exposition, multiple rounds of global search with informative pair-plots, effective sample size monitoring, and the inclusion of HPC job scripts. However, the project is undermined by a critical methodological error: the SARIMA log-likelihood and the POMP particle-filter log-likelihood are evaluated under different probability models and cannot be directly compared, yet the main conclusion rests entirely on this comparison. Additional serious problems include a mismatch between the AIC-based SARIMA model selection and the final SARIMA model actually used, the absence of profile likelihoods (explicitly acknowledged), no discussion of parameter identifiability, and no convergence evidence for the local IF2 search.

---

## Major Issues

### 1. SARIMA and POMP log-likelihoods are not directly comparable, invalidating the main conclusion

The conclusion states: "the log-likelihood for the SEIRS model was much higher [i.e., more negative] than the SARIMA approach… This substantial difference in results suggests that the POMP approach is unnecessary." This comparison is statistically invalid. The SARIMA model evaluated with `arima()` uses a Gaussian state-space likelihood for integer count data; the SEIRS POMP model uses a negative binomial observation model evaluated via a particle filter. These two likelihoods are computed under entirely different probability distributions and on different normalizing constants. A difference of hundreds of log-likelihood units between them reflects the model family, not model quality. No conclusion about the relative fit of the two approaches can be drawn from this comparison. The correct approach is to embed a non-mechanistic benchmark (e.g., an auto-regressive negative binomial model) within the POMP framework and compare particle-filter log-likelihoods under the same observation model (Wheeler et al. 2024, §Benchmark comparison).

### 2. SARIMA model selection used period=12, but the reported final model uses period=52

The AIC table grid search (line 238) uses `seasonal=list(order=c(Pi, 1, Qi), period=12)`, fitting models with a monthly seasonal period. The final SARIMA model (line 254) uses `period=52`, a weekly seasonal period consistent with the data frequency. The model selected by the grid search — SARIMA((1,1,1)×(0,1,1)[12]) — is therefore a completely different model from the one reported and used as the baseline — SARIMA((1,1,1)×(0,1,1)[52]). The log-likelihood of the reported model was never validated against alternatives at period=52, meaning the SARIMA baseline is arbitrarily chosen rather than rigorously selected. This error also means the AIC table shown in the report does not support the model actually used.

### 3. No profile likelihoods computed; parameter identifiability is unassessed

The authors explicitly state: "Unfortunately, the great lakes cluster was running very slow while we were finishing up the project. As a result, we were unable to obtain profile likelihoods for the parameters." The SEIRS model has 13 parameters, five of which are fixed after the local search (S0, E0, I0, R0, k) and seven are estimated. Without profile likelihoods, there is no way to assess whether the remaining parameters (Beta0, amp, phase, mu_EI, mu_IR, mu_RS, rho) are identifiable from the data, nor to report confidence intervals. The "poor man's profiles" shown are scatter plots of IF2 endpoints from six heterogeneous search boxes — they cannot substitute for true profile likelihoods because they do not hold the focal parameter fixed while re-optimizing over all others. The claim that parameters converged cannot be verified. See Wheeler et al. (2024), §Parameter identifiability and uncertainty.

### 4. No non-mechanistic benchmark in the POMP framework

The project uses the SARIMA model as a benchmark, but (as noted above) the comparison is invalid. There is no benchmark model evaluated within the same probabilistic framework as the SEIRS POMP model. A negative binomial auto-regressive model (e.g., ARIMA on log-transformed counts, or a POMP model with only measurement noise and no mechanistic process) would provide a meaningful baseline for whether the SEIRS structure captures signal beyond pure statistical dependence. Wheeler et al. (2024) note that none of 32 cholera papers they reviewed performed such a comparison; this project similarly omits it. Without this comparison, the claim that "other POMP-based approaches could… improve upon the SARIMA model" is unsubstantiated.

### 5. Local IF2 search shows non-convergence but this is dismissed without justification

The report states: "The remaining parameters did not converge within this iterated filtering search, but the improvement in likelihood means this is not an issue." Non-convergence of IF2 traces is not rendered harmless by an improvement in likelihood; it indicates that the optimization has not reached a stable region, so the starting point for the global search may be unreliable. With only 20 replicates and 100 IF2 iterations at run_level=3 in the main document, and parameters such as Beta0, amp, phase, mu_EI, mu_IR, and mu_RS showing non-convergence, the local search result cannot serve as a reliable warm start. The claim requires either additional iterations until traces stabilize, or explicit evidence that the global search is insensitive to the starting point. See Wheeler et al. (2024), §Computational adequacy.

### 6. Fixed initial condition parameters undermine global search coverage

The authors fix S0, E0, I0, R0, and k at values from the local search for all six global searches, citing computational convenience. However, the local search itself did not converge for these parameters' neighbors, so the fixed values may be suboptimal. More importantly, fixing initial conditions can artificially constrain the likelihood surface and produce false convergence. The interaction between initial state proportions and transmission parameters (Beta0, rho) can be strong: a model with different (S0, I0) can achieve similar observed dynamics with different Beta0 or rho. The claim of convergence in the global search pair-plots is therefore not reliable evidence of having found the global MLE. Wheeler et al. (2024) note that initialization strategy affected AIC by ~72 units in one of their evaluated models.

### 7. SARIMA model formulation has a notation inconsistency that obscures the model

The SARIMA formula uses $B_{12}$ for the seasonal backshift operator (implying monthly seasonality), while the actual model is fitted with period=52. The notation $\Phi(B_{12})$ and $\Psi(B_{12})$ with subscript 12 suggests a 12-period seasonal cycle, contradicting the code and the data's weekly frequency. This is not merely a typo — it directly misleads the reader about which model is being presented and compounds the period-mismatch issue in Major Issue 2.

---

## Minor Issues

- **Unused parameter `eta`**: The initial constant-Beta SEIRS model declares `eta` in `paramnames` (line 354) and sets `eta = 0.05` in the initial parameter vector (line 383), but `eta` appears nowhere in the step function or initial conditions. This ghost parameter has no effect on the model and may indicate a copy-paste error from a reference implementation. It should either be used or removed.

- **Unused packages**: `tseries` and `forecast` are loaded but not used anywhere in the analysis. While harmless, loading unused packages makes the reproducibility environment unnecessarily unclear.

- **Poor man's profiles use heterogeneous search boxes**: The poor man's profiles pool results from six global searches with very different parameter ranges (e.g., mu_EI ranges from [0,100] in search 1 to [0,1] in search 6). Points from early searches with wide boxes reaching the same loglik region as later searches with narrow boxes are still included. The resulting scatter does not uniformly characterize the likelihood surface and should not be interpreted as evidence of parameter identifiability.

- **The report says 750 models were used for poor man's profiles, but seirs_lik.csv contains 1354 rows**: This discrepancy is unexplained and raises questions about which runs are included. The file appears to have been updated across multiple cluster runs, possibly including duplicate or superseded results.

- **Decomposition description contains an error**: The text states "This indicates the data likely has a strong daily or weekly seasonality." The data are already weekly; the seasonality is annual (period~52 weeks), not daily or intra-weekly.

- **Frequency domain interpretation**: The text states "Both periodograms show a clear dominant frequency of 0.02." The dominant frequency is expressed in cycles per observation (week), so omega=0.02 cycles/week corresponds to T=50 weeks, which is annual. The report correctly identifies T=50 weeks but calls this "approximately a year" without noting the unit of the frequency (cycles per week) explicitly. This could confuse readers unfamiliar with the spectrum() output scale.

- **Phase parameter lacks a parameter transformation**: `phase` is not included in `partrans`, leaving it unconstrained on the real line. This is mathematically acceptable, but in the context of the sine seasonality formula $\beta_0 (1 + \text{amp} \cdot \sin(2\pi(t+\text{phase})/52))$, the optimal phase is only identifiable modulo 52 weeks. The search ranges for phase vary across the six global searches (from [-25,0] to [-5,0]), and no justification is given for these ranges or for the implicit assumption that the phase lies within a single cycle. A wrapped or constrained parameterization would be more principled.

- **The initial SEIRS simulation claims the model is "unable to produce simulations which matched the true Oklahoma flu data"**: The first version uses constant Beta with manually-chosen parameters that produce a linearly increasing trend. However, with appropriate parameters an SIR/SEIRS model with constant transmission and a reinfection pathway can produce endemic equilibria, not necessarily a linear trend. The claim that seasonality is necessary for this model is asserted but not demonstrated through any exploration of the constant-Beta model's parameter space.

- **ChatGPT consultation**: The authors state they consulted ChatGPT to identify methods for incorporating seasonality into the transmission rate. The sinusoidal forcing used is a well-established technique in epidemiological modeling; it would be more appropriate to cite the epidemiological literature (e.g., Keeling and Rohani 2008, or the course notes which discuss seasonality) rather than an AI assistant, which cannot be cited or verified.

- **No session info**: The supplement does not include `sessionInfo()` output or explicit package version declarations. The `pomp` API has changed across versions; without version information, reproduction on a different installation is uncertain.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/great-lakes-seirs-global.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/great-lakes-seirs-local.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/great-lakes-seirs-global.sbat`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/great-lakes-seirs-local.sbat`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik_1.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik_6.csv`
