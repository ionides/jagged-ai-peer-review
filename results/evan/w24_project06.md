# Final AI Review — Volatility Analysis of NASDAQ (w24, Project 06)

---

## Overall Assessment

This project presents a well-structured progression of volatility models for NASDAQ log returns — ARMA, GARCH (normal and t-distributed noise), ARMA+GARCH, and a stochastic volatility POMP model with leverage. The overall narrative is clear and the choice of models is appropriate for financial time series. However, the project is undermined by a critical error in the central comparison: the rugarch `likelihood()` function returns a log-likelihood, so applying `log()` to it yields a meaningless number (~8.15), while the values (~3477–3550) are themselves log-likelihoods directly comparable to the ARMA log-likelihood (3324.91) and the POMP log-likelihood (3510). The paper never cleanly resolves what scale its GARCH numbers are on, and the conclusion that "ARMA+GARCH beats POMP" is presented without a valid, clearly labeled comparison table. Additionally, the POMP model's two key parameters (mu_h, H_0) do not converge, and sigma_eta shows extreme spread across global search runs, yet the resulting log-likelihood is treated as a final result. No profile likelihoods or confidence intervals are reported for any POMP parameter. These issues collectively prevent confident conclusions from the mechanistic modeling component.

---

## Key Strengths

**24.06.8 — Correct logmeanexp usage**
The global search code correctly applies `logmeanexp` to aggregate particle filter log-likelihoods across replicates. This is the correct Monte Carlo estimator and avoids the common error of averaging raw likelihoods. *Why it matters:* Correct likelihood aggregation is foundational to all downstream comparisons.

**24.06.9 — Appropriate run-level framework**
The paper uses `run_level=3` for final results (Np=2000, Nmif=200, 100 global replications), which represents a serious computational effort appropriate for this dataset size. *Why it matters:* Insufficient computation is a common failure mode in POMP analyses; this project avoids it.

**24.06.10 / 24.06.11 — Filter and convergence diagnostics produced**
Filter diagnostics (ESS and conditional log-likelihoods, fig_012) and MIF2 convergence trace plots (fig_013) are both present. *Why it matters:* These are the primary tools for assessing whether the POMP fit is trustworthy, and their inclusion shows awareness of good practice.

---

## Major Points

**ID: 24.06.1 — Likelihood-scale confusion invalidates the central model comparison**
*Concern:* The rugarch `likelihood()` function returns a log-likelihood (sum of conditional log-densities). The paper treats the output (~3476–3550) as a raw likelihood and then takes its log (~8.15), reporting the log-of-a-log-likelihood as if it were the log-likelihood. The consequence is that the comparison table in the conclusion is on inconsistent scales. The ARMA log-likelihood (3324.91 from arima()) and the POMP log-likelihood (~3510) are correctly on the log scale, but the GARCH numbers as actually printed in the text are ambiguous. *Why it matters:* The paper's headline conclusion — that ARMA+GARCH beats POMP — depends entirely on this comparison being valid. If the GARCH log-likelihoods are ~3550 (which they are, from the rugarch output), then ARMA+GARCH does beat POMP (3550 > 3510). But this result is not stated clearly; instead the paper reports "a likelihood of 3550.09 and a log likelihood of 8.17," which is internally contradictory and confusing to any reader. *Severity:* Major. *Suggested action:* Create a single summary table of log-likelihoods for all models, explicitly labeled as log-likelihoods. Confirm that rugarch's `likelihood()` returns the log-likelihood (it does), and remove the spurious `log(likelihood(...))` calls. The comparison may actually be valid once the scale confusion is resolved.

**ID: 24.06.2 — Non-convergence of mu_h and H_0 invalidates POMP likelihood as a final estimate**
*Concern:* Both the local search (fig_013 trace plots) and the text explicitly confirm that mu_h and H_0 do not converge after 200 MIF2 iterations. The mu_h traces range from approximately −10 to +5 at the final iteration, and H_0 similarly shows wide dispersion. *Why it matters:* When parameters do not converge, the MLE has not been found. The reported log-likelihood of 3510 is therefore a lower bound on the achievable log-likelihood, not the optimum. Comparing this lower bound to the GARCH log-likelihood treats an underestimate as if it were the true maximum. *Severity:* Major. *Suggested action:* Either run additional iterations or expand the search, or explicitly acknowledge that the POMP log-likelihood is a lower bound and caveat the comparison accordingly. Reparameterization (e.g., fixing mu_h to a literature value) may help.

**ID: 24.06.3 — sigma_eta is severely non-identifiable in the global search**
*Concern:* The global search pairs plot (fig_011) shows sigma_eta ranging from near 0 to above 100 across 100 replications with no concentration near any particular value, even among high-likelihood runs. *Why it matters:* A parameter whose value cannot be identified from the data provides no scientific information; conclusions about the leverage effect or volatility dynamics that rely on sigma_eta are unreliable. *Severity:* Major. *Suggested action:* Compute a profile likelihood over sigma_eta to determine whether the data contain information about this parameter. If the profile is flat, acknowledge non-identifiability and consider fixing sigma_eta to a value from the literature.

**ID: 24.06.5 — No profile likelihoods or confidence intervals**
*Concern:* No profile likelihoods are computed for any POMP parameter; no confidence intervals are reported. The paper states point estimates (phi ≈ 0.8, sigma_nu near 0) without any uncertainty quantification. *Why it matters:* Point estimates without uncertainty bounds are uninterpretable, particularly given the identifiability problems already noted. *Severity:* Major. *Suggested action:* Compute profile likelihoods and MCAP confidence intervals for at least phi and sigma_nu, the two parameters that appear best-identified.

---

## Minor Points

**ID: 24.06.4 — ACF/PACF order interpretation is reversed**
*Concern:* The paper states that the number of significant ACF spikes determines the AR order and the number of significant PACF spikes determines the MA order — this reverses the standard Box-Jenkins rule. *Why it matters:* The conceptual error suggests a misunderstanding of the role of these diagnostics, though the AIC table ultimately selects the model so the final choice is unaffected. *Severity:* Minor. *Suggested action:* Correct the text: PACF cutoff informs AR order; ACF cutoff informs MA order. Emphasize that the AIC table is the primary selection tool.

**ID: 24.06.5b — GARCH and ARMA AIC tables are on different scales**
*Concern:* The ARMA AIC table shows total AICs (~−6600), while the GARCH AIC table shows per-observation AICs (~−5.5). These are presented side by side without noting the difference. *Why it matters:* A reader comparing the two tables directly would reach wrong conclusions. *Severity:* Minor. *Suggested action:* Add a note explaining that the GARCH AIC values are per-observation (from rugarch) while the ARMA AIC values are total (from arima()); or standardize to the same scale.

**ID: 24.06.13 — No forward simulation from fitted POMP model**
*Concern:* The paper shows a simulation from the initial (unfitted) parameters but does not show a simulation from the estimated MLE parameters for comparison with observed data. *Why it matters:* Forward simulation from the fitted model is an important diagnostic for whether the model captures key features of the data (volatility clustering, tail behavior). *Severity:* Minor. *Suggested action:* Simulate trajectories from the fitted model and overlay on the observed log returns; assess whether volatility clustering is reproduced.

**ID: 24.06.10b — Data description is incomplete**
*Concern:* The exact date range, number of observations, and data source (Yahoo Finance via quantmod) are not stated explicitly in the text. *Severity:* Minor. *Suggested action:* Add one sentence to the Data section specifying the exact date range and the number of trading-day observations.

**ID: 24.06.6 — Code export typo in global search**
*Concern:* The foreach export argument includes `'if'`, which is an R reserved keyword and not a valid variable name to export. This may be a transcription artifact from blinding but could affect reproducibility. *Severity:* Minor. *Suggested action:* Check the original code; if this is an error, correct `'if'` to `'if.box'` or remove it from the export list.
