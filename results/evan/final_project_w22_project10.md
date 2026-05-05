# Final AI Review: Modeling South Africa Omicron Variant Cases
## Project: w22 Project 10

---

> Challenge skipped — Grounding signal was Strong. All major claims are directly supported by specific text or numerical values in the manuscript.

---

## Overall Assessment

This project takes a sensible pedagogical trajectory, escalating from ARMA through SIR to a more elaborate SEAPIRD model while documenting each step with trace plots and scatter plots. The choice of the Omicron wave in South Africa is well-motivated, and the identification of a weekly periodicity in the spectrum analysis is a genuine contribution. However, the project has several significant methodological problems that undermine the main conclusions. Most critically, the SEAPIRD model is fit to a 7-day smoothed version of the data while SIR and ARMA are fit to raw data, making the central likelihood comparison invalid. The Normal measurement model used in SEAPIRD is inappropriate for count data. The ARMA model selection is internally inconsistent (ARMA(4,4) has lower AIC by ~8 units but ARMA(3,3) is selected). No profile likelihoods or confidence intervals are computed, and the large parameter discrepancies between local and global SEAPIRD optima are left unexplored. These issues collectively mean that the main claim — that SEAPIRD outperforms ARMA and SIR — cannot be accepted as stated.

---

## Key Strengths

- **ID: 22.10.S1** — The escalation from SIR to SEAPIRD, with both local and global searches run for each model, demonstrates methodological care. The decision to move to a more complex model after observing poor SIR simulation quality is scientifically appropriate.

- **ID: 22.10.S2** — Convergence trace plots are provided for both POMP models (figs 7 and 13), and pairwise scatter plots are provided for both local and global searches (figs 9, 10, 14, 15). These allow readers to evaluate optimization behavior, even if the conclusions drawn from them are incomplete.

- **ID: 22.10.S4** — The SIR model correctly uses a negative binomial measurement model, which is appropriate for overdispersed count data. This is a good modeling choice.

- **ID: 22.10.S5** — The spectral analysis identifying a ~7-day periodicity is well-executed and the interpretation (reporting delays on weekends) is biologically plausible.

---

## Major Points

**ID: 22.10.3 — SEAPIRD fit on 7-day smoothed data invalidates the central comparison**

Concern: The SEAPIRD section explicitly states "in this part, we used the 7-day average smoothed version of the daily new cases." The SIR model and the ARMA model were fit to raw daily counts. The conclusion ranks all three models by log-likelihood, but log-likelihoods from models fit to different datasets are not comparable. The SEAPIRD likelihood (-1446) is measured against smoothed data whose variance is artificially reduced relative to raw data.

Why it matters: This is the primary quantitative claim of the paper. If the comparison is invalid, the paper cannot conclude that SEAPIRD is the best-performing model.

Severity: Major

Suggested action: Re-fit the SEAPIRD model using the raw daily case counts (the same data used for ARMA and SIR). If the smoothed data is used for computational reasons, restrict all comparisons to models fit on identical data and explicitly note the limitation.

---

**ID: 22.10.4 — Normal measurement model in SEAPIRD is inappropriate for count data**

Concern: The SEAPIRD measurement model is Y_cases ~ Normal(ρH, τρH(1-ρ)), which assigns positive probability to negative case counts. The SIR model correctly used a negative binomial. The justification given ("the mode is around 1925") is not sufficient — even with a mean of 1925, a large τ can produce substantial probability mass on negative values, as observed in the global-search parameter tau = 624,000.

Why it matters: An invalid measurement model can produce artificially high likelihoods and distorted parameter estimates.

Severity: Major

Suggested action: Replace the Normal with a negative binomial measurement model, consistent with the SIR section. If Normal is retained, compute and report the probability mass on negative values at the fitted parameters to demonstrate it is negligible.

---

**ID: 22.10.1 — ARMA model selection is internally inconsistent**

Concern: The AIC table shows ARMA(4,4) = 2991.87 and ARMA(3,3) = 3000.01. The paper selects ARMA(3,3) and states "This suggests a model of ARMA(3,3)," but the AIC criterion directly favors ARMA(4,4) by ~8 units. No justification for overriding the AIC table is given.

Why it matters: AIC-based model selection is a stated methodology of the paper; selecting a model with a higher AIC without explanation contradicts the methodology.

Severity: Major

Suggested action: Either select ARMA(4,4) as the AIC-preferred model, or explicitly justify the choice of ARMA(3,3) (e.g., concern about near-unit-root MA behavior discussed below).

---

**ID: 22.10.2 — MA roots nearly on the unit circle indicate near non-invertibility**

Concern: The fitted ARMA(3,3) reports two MA polynomial roots at 1.000002 (essentially on the unit circle). This indicates the model is on the boundary of invertibility, which can cause numerical instability and suggests the model order or data transformation is misspecified. The raw data are right-skewed (mean 5160, SD 6593, max 37875), and a log or square-root transformation is standard practice for count time series.

Why it matters: Near-unit-root MA behavior invalidates standard asymptotic theory for the coefficient standard errors and raises questions about whether the ARMA model is a reliable baseline.

Severity: Major

Suggested action: Apply a log or Box-Cox transformation to the data before fitting the ARMA model; re-run the AIC table and model diagnostics. Note whether the near-unit-root issue persists after transformation.

---

**ID: 22.10.6 — SEAPIRD parameters severely non-identifiable; between-search discrepancies not addressed**

Concern: The SEAPIRD local and global optima differ dramatically for several parameters: tau: 262,000 (local) vs 624,000 (global), a 2.4-fold difference; mu_ID: ~3.25×10^-4 vs ~8.64×10^-6, a 37-fold difference; mu_AR: 0.180 vs 3.49, a 19-fold difference. These large discrepancies suggest that the surface of the SEAPIRD likelihood is flat or multimodal in these parameter directions, making the reported best-parameter estimates unreliable.

Why it matters: If parameters are not identifiable, the model cannot be used to draw scientific conclusions about the Omicron transmission process. The paper interprets parameter values but does not address identifiability.

Severity: Major

Suggested action: Compute profile likelihoods for at least beta and rho. Flag mu_ID, mu_AR, and tau as potentially non-identifiable. Consider fixing non-identifiable parameters at biologically motivated values and re-estimating the remaining parameters.

---

**ID: 22.10.8 — No profile likelihoods or confidence intervals for any parameter**

Concern: Neither the SIR nor the SEAPIRD analysis reports profile likelihoods or confidence intervals. Pairwise scatter plots and trace plots are presented as a substitute, but these diagnostics reveal the shape of the search, not calibrated uncertainty. The parameter values reported in the conclusion are point estimates with no associated uncertainty.

Why it matters: Without confidence intervals, it is impossible to assess whether differences in parameter values across models or searches are meaningful.

Severity: Major

Suggested action: Compute profile likelihoods for the key parameters (beta, rho, eta for SIR; beta, rho for SEAPIRD) using MCAP or the standard pomp profile approach.

---

**ID: 22.10.5 — SIR local search MC standard error of 6.98 log-likelihood units is too large**

Concern: The SIR local search reports log-likelihood = -1997 with standard error = 6.98. A standard error of this magnitude means the true log-likelihood at these parameters is highly uncertain (a 95% range of roughly ±14 log-likelihood units). This result cannot support reliable comparison with ARMA (-1492) or with the global SIR result (-1677). The number of particles (Np) is not stated in the text.

Why it matters: Computational imprecision of this magnitude means the local search result is essentially uninformative; it cannot be cited as evidence of poor SIR performance in this parameter region.

Severity: Major

Suggested action: Report Np for all pfilter evaluations. Increase Np until the MC standard error falls below ~1 log-likelihood unit. Re-run the local search with adequate particle counts before interpreting the result.

---

## Minor Points

**ID: 22.10.9 — SEAPIRD population size N = 500,000 vs SIR N = 50,000,000**

Concern: The SIR model uses N = 5×10^7 (consistent with South Africa's population) while the SEAPIRD uses N = 500,000, a 100-fold reduction. This choice is not explained. If N = 500,000 represents an effective or regional population, this should be stated and the implications for parameter interpretation should be discussed.

Severity: Minor

Suggested action: Add a sentence justifying the choice of N = 500,000 for SEAPIRD and discussing how this affects the interpretation of beta and other rate parameters.

---

**ID: 22.10.10 — Np and Nmif not reported in text**

Concern: The number of particles and mif2 iterations are not explicitly stated in the manuscript. These are required for reproducibility and for assessing computational adequacy.

Severity: Minor

Suggested action: Add a table or paragraph stating Np, Nmif, and the number of independent starting points for each model and each search.

---

**ID: 22.10.11 — 7-day periodicity identified but not incorporated into POMP models**

Concern: The spectrum analysis clearly identifies a weekly periodicity in the data, plausibly attributed to weekend reporting delays. Neither the SIR nor the SEAPIRD model includes any mechanism for this periodicity (e.g., a periodic reporting rate).

Severity: Minor

Suggested action: Acknowledge this limitation explicitly and note it as a direction for future work. The 7-day smoothing applied in SEAPIRD partially addresses this but introduces the dataset comparison problem discussed above.

---

**ID: 22.10.12 — ARMA residual diagnostics suggest distributional mismatch not analyzed**

Concern: Figure 3 shows heavy tails in the QQ plot of ARMA residuals and residual autocorrelation, consistent with fitting untransformed right-skewed count data. The text notes "performance is not that well" but does not diagnose the cause.

Severity: Minor

Suggested action: Note that the heavy residual tails are likely caused by fitting a Gaussian ARMA to right-skewed count data without transformation, and that this is a known limitation of the ARMA baseline.
