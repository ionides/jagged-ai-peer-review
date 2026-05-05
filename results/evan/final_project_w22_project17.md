# Final AI Review: US COVID-19 Cases Analysis (W22 Project 17)

---

## Overall Assessment

This project fits SARIMA and SEIR models to US daily COVID-19 case counts from June 2021 through March 2022. The authors demonstrate a reasonable understanding of the IF2 workflow — using logmeanexp for replicated likelihood evaluation, conducting a multi-start global search from a parameter box, and presenting filter diagnostics. However, the project has one critical error in model formulation (the measurement model tracks recoveries rather than new cases), a model-selection anomaly in the SARIMA branch that is left unexplained, and no assessment of parameter identifiability. The conclusion that both models "can well model COVID-19 daily cases" is not adequately supported given these gaps.

---

## Key Strengths

**ID 22.17.8 — Correct log-likelihood aggregation.**
The authors correctly use `logmeanexp` to average over 10 replicated particle filter runs at both the local and global search stages. This avoids the common error of averaging log-likelihoods directly.

**ID 22.17.9 — Multi-start global search.**
The global search samples random starting parameters from a user-specified box and applies three successive cooling stages, which is an appropriate strategy for exploring a high-dimensional parameter space.

**ESS and filter diagnostics presented.**
Figure 13 shows the effective sample size near the particle count (N_p ≈ 1000) for most of the time series, with brief drops at transition periods. This positive signal — that the particle filter is not collapsing — is presented, though not interpreted.

---

## Major Points

**ID 22.17.2 — Measurement model accumulates recoveries, not infections.**
Severity: Major.

The `seir_step` Csnippet accumulates `H += dN_IR`, where `dN_IR` is the number of individuals transitioning from the infectious compartment to the recovered compartment. The measurement model then fits observed daily case counts to `rho * H`. In epidemiology, reported COVID-19 cases reflect confirmed new infections — corresponding to the SE transition (`dN_SE`) or the EI transition (`dN_EI`), not the IR transition. Using recoveries introduces a systematic phase shift equal to the full average infectious period, distorting the biological meaning of all fitted contact rates (b1–b7) and the reporting rate (rho). The authors appear to have adopted this code structure from a prior-year project (reference [6]) without verifying the biological meaning of H.

Suggested action: Replace `H += dN_IR` with `H += dN_EI` (or `dN_SE` depending on the intended interpretation of "confirmed case"), and re-run the fitting procedure. The measurement model and parameter estimates will change substantially.

---

**ID 22.17.3 — SARIMA model selection contradicts the reported AIC table.**
Severity: Major.

The AIC table for the seasonal component shows that SARIMA(5,1,5)×(0,1,0)_7 has AIC = 7388.231, while the authors select SARIMA(5,1,5)×(2,1,1)_7 with AIC = 7388.925. The selection criterion stated is "lowest AIC value," yet the selected model does not have the lowest AIC. This is not explained in the text. Either the table contains a numerical error, or the selection was made on other grounds (e.g., the simpler seasonal structure failed a diagnostic test) that are not disclosed.

Suggested action: Re-examine the AIC values for all SARIMA seasonal components. If the SARIMA(5,1,5)×(0,1,0) model is genuinely lower-AIC, explain why it was not selected (e.g., Ljung-Box failure, non-invertibility). If it was selected in error, update the analysis to use the correct model.

---

**ID 22.17.6 — Initial conditions are implausible for a mid-pandemic start.**
Severity: Major.

The model initializes S = N = 334,515,015 (entire US population susceptible) and R = 0 on June 5, 2021, a date well into the pandemic when tens of millions of Americans had already been infected or vaccinated. These fixed starting values are biologically implausible and are not justified in the text. Because the contact rates b1–b7 must compensate for the artificially inflated susceptible pool, the fitted parameter values cannot be interpreted epidemiologically.

Suggested action: Estimate S(0) and R(0) (or equivalently the initial immune fraction) as free parameters within the global search box, or fix them to values consistent with published estimates of prior-immunity by June 2021 (e.g., approximately 100–150 million Americans had some immunity by that date from infection or vaccination).

---

**ID 22.17.4 — No profile likelihood; identifiability not assessed.**
Severity: Major.

None of the 11 free parameters have profile likelihood plots or confidence intervals. The global search results table shows that the top 6 parameter vectors span meaningfully different values (ei2 ranges from 0.589 to 0.670, tau from 0.227 to 0.238) while achieving nearly identical log-likelihoods (-3684.733 to -3684.748), which is a direct signal of weak identifiability. The paper presents the top-1 row as the MLE without acknowledging that many parameter combinations achieve essentially the same fit.

Suggested action: Compute profile likelihood slices for at least the key parameters (rho, ei1, ei2) to determine whether identifiable confidence intervals can be obtained. Report whether the reported MLE is meaningful or whether the model is structurally unidentifiable for some parameters.

---

**ID 22.17.7 — Incomplete convergence, strong conclusions drawn without qualification.**
Severity: Major.

The local search trace plots (fig_011) show most parameters — including ei1, ei2, rho, and tau — have not converged after the full Nmif iterations: chains diverge widely. The global search traces (fig_014) show improvement for the beta parameters, but ei2 remains noticeably spread across chains. The text acknowledges non-convergence ("most of the parameters have not converged") but draws the conclusion that the SEIR model "can well model COVID-19 daily cases" without qualifying that the MLE is not reliably located.

Suggested action: Increase Nmif and/or add additional cooling stages until loglik and parameter traces stabilize. Alternatively, increase Np to reduce Monte Carlo noise. Report uncertainty due to incomplete convergence explicitly in the conclusion.

---

**ID 22.17.1 — SARIMA vs SEIR likelihood comparison requires qualification.**
Severity: Minor-to-Major.

The conclusion directly compares SARIMA log-likelihood (-3672.181) with SEIR log-likelihood (-3684.733) and interprets the SARIMA as performing better. The SARIMA likelihood is computed on the first-differenced series (implicitly, via the `d=1` parameter), whereas the SEIR likelihood is computed on the raw daily case series. These are not the same data transformation, and the likelihoods are not directly commensurable. The paper should at minimum note this caveat.

Suggested action: Add a sentence in the conclusion acknowledging that the SARIMA and SEIR likelihoods are computed under different observation models and cannot be treated as a formal model comparison. A direct comparison would require fitting both models to the same observations under the same likelihood function.

---

## Minor Points

**Np=100 for global search likelihood evaluation.**
The final likelihood evaluations in the global search use `Np=100` particles, which is low. Although the ESS diagnostics suggest the particle filter does not collapse catastrophically, using more particles (e.g., 1000–5000) for the final likelihood table would improve the reliability of the reported MLE.

**Nm/Nreps values not stated.**
The values of `Np`, `Nmif`, `Nreps_local`, and `Nreps_global` are used as variables in the code but never assigned or reported in the visible text. Readers cannot assess the computational scale of the search.

**Simulation trajectories substantially overshoot observed data.**
In fig_012, several simulation trajectories reach 1.5 million daily cases, while the observed maximum is around 800,000. The text describes the fit as "significantly improved" without noting this substantial overshoot.

**Ljung-Box rejection not reconciled with adequacy claim.**
The Ljung-Box test strongly rejects white-noise residuals (p = 0.0003797, df = 3), yet the paper concludes the SARIMA is "adequate." This contradiction deserves at least a sentence of discussion.

**Figure caption numbering errors.**
Caption variables in the code reference "Figure 21" and "Figure 18," but the document is not that long. These appear to be inherited from the source project and not updated.

**Normal measurement model can produce negative counts.**
The measurement model `sd = sqrt((tau*H)^2 + rho*H)` with a Normal distribution can yield negative case counts. The `rmeas` snippet handles this by truncating to zero, but this introduces a systematic bias for small H. This is a minor approximation issue worth a note.
