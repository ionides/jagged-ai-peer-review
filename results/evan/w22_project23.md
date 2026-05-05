# Final AI Review: STATS 531 W22 Project 23
# COVID-19 POMP Modeling (SIR / SEIR / SEIQR) for New York City

---

## Overall Assessment

This project fits three compartmental POMP models — SIR, SEIR, and SEIQR — to the Omicron wave of New York City COVID-19 case counts using iterative filtering (mif2). The authors demonstrate familiarity with the overall POMP workflow: they run local and global mif2 searches, aggregate particle filter log-likelihoods with logmeanexp, and show trace plots. However, the project has several critical errors that invalidate its main conclusion. Most importantly, the SEIQR model uses a fundamentally different observation model (Normal distribution on the quarantine stock Q) than the SIR and SEIR models (Binomial distribution on a daily-accumulator H). Because the likelihoods are evaluated under incompatible probability models for the observed data, the reported log-likelihoods cannot be compared, and the conclusion that SEIQR is the best model is not supported. Additional code-level errors — a missing 1/N term in the SEIQR force of infection and a weekly Euler step in the SEIR model — further compromise the analysis. These issues are correctible, but doing so would require substantial revision of the SEIQR model specification and re-running the experiments.

---

## Key Strengths

**22.23.11 — Correct logmeanexp aggregation**
Severity: Minor strength. The paper correctly uses `logmeanexp(se=TRUE)` to aggregate particle filter log-likelihoods across replicate pfilter runs for all three models, which is the appropriate procedure for combining noisy particle filter estimates.

**22.23.12 — Systematic multi-start search across three models**
Severity: Moderate strength. For each model, both a local search (starting from a hand-tuned initial guess) and a global search (drawing 100 random starting points from a uniform design) are conducted. This demonstrates awareness of the importance of avoiding local optima and shows methodological consistency across models.

---

## Major Points

**22.23.1 — Incomparable measurement models invalidate the model comparison**
ID: 22.23.1 | Severity: Major

The SIR and SEIR models observe daily positive cases via `dbinom(pos, H, rho)`, where `H` is a daily accumulator of transitions out of the infectious compartment. The SEIQR model instead uses `dnorm(pos, Q, rho*Q + 1e-10)`, where `Q` is the current stock of quarantined individuals. These are likelihoods under different probability models for the same observed sequence, so their numerical values are not on the same scale. The SEIQR loglik of approximately -601 cannot be compared to the SIR loglik of -50126 or the SEIR loglik of -85130. The conclusion in Section 7 that "the log likelihood value of the SEIQR model is the lowest [best]" is therefore invalid.

Suggested author action: Respecify the SEIQR model with a daily accumulator variable H (tracking transitions into Q or out of I), reset at daily intervals, and use `dbinom(pos, H, rho)` as the observation model — identical in structure to the SIR and SEIR models. Then re-run the mif2 searches and restate the model comparison.

---

**22.23.2 — SEIQR force of infection missing division by N**
ID: 22.23.2 | Severity: Major

The SEIQR step Csnippet uses `rbinom(S, 1-exp(-Beta*I*dt))` (line 752), without dividing by N. The SIR and SEIR models correctly use `Beta*I/N*dt`. Without the N term, Beta has units of inverse persons, and with N ~ 1.9 million susceptibles, even a tiny positive Beta produces an enormous force of infection. The estimated Beta of ~2.9 for SEIQR is therefore meaningless in the same epidemiological sense as the SIR/SEIR Beta parameters, and the SEIQR model is effectively fitting a different functional form.

Suggested author action: Change the SEIQR step to `rbinom(S, 1-exp(-Beta*I/N*dt))` and re-run. This will change the effective parameter scale substantially and likely require re-tuning the initial parameter values.

---

**22.23.3 — SEIR uses weekly Euler step on daily data**
ID: 22.23.3 | Severity: Major

The SEIR model is constructed with `delta.t=7` (line 439), meaning one Euler step per 7 days, while the data is at daily frequency and the SIR model uses `delta.t=1`. This introduces large discretization error in the SEIR transition probabilities and makes the SEIR likelihood incomparable to the SIR likelihood independent of any measurement model issues. No justification for the weekly step is provided.

Suggested author action: Change the SEIR model to `delta.t=1` to match the SIR model and the daily data frequency. Re-run the SEIR local and global searches.

---

**22.23.4 — SIR global search box excludes the local MLE region**
ID: 22.23.4 | Severity: Major

The SIR global search draws eta uniformly from [0.4, 0.6] (line 291), but the local search converged to eta in the range [0.943, 0.959] (Table "SIR Local Search Results"). The global search therefore never explores the region where the local search found its optimum. This explains why the global MLE (-56543) is substantially worse than the local MLE (-50126). The authors note that the global fitting "is not as good as the initial value" but do not identify the cause.

Suggested author action: Expand the global search box to include eta in [0.85, 1.0] (or at minimum [0.7, 1.0]) to cover the region of the local optimum. A two-stage search — broad initial exploration followed by a refined search in the promising region — is a useful strategy.

---

**22.23.7 — No non-mechanistic benchmark**
ID: 22.23.7 | Severity: Major

No ARMA, SARIMA, or other non-mechanistic baseline model is fitted to the data. Without a benchmark, there is no way to assess whether the mechanistic models explain any systematic structure in the data beyond what a simple statistical model would capture.

Suggested author action: Fit an ARMA(p,q) model (or a negative-binomial regression with time trend) to the same 60-day Omicron window and report its log-likelihood alongside the POMP models. Losing to ARMA is not a failure; it provides context for interpreting the POMP log-likelihoods.

---

**22.23.8 — No profile likelihoods or confidence intervals**
ID: 22.23.8 | Severity: Major

No profile likelihoods are computed for any model, and no confidence intervals are reported for any parameter. The pairs plots show substantial scatter (e.g., SEIQR Beta ranges from 0.4 to 8.6 across the top-6 global search results), suggesting poor parameter identifiability, but this is not formally assessed.

Suggested author action: Compute profile likelihoods for at least Beta (transmission rate) and rho (reporting rate) in the best-fitting model. Use the MCAP procedure or the profile likelihood CI to assess parameter uncertainty.

---

**22.23.5 — SEIQR declared best model despite non-converged mif2**
ID: 22.23.5 | Severity: Major

The SEIQR trace plots (fig_015) show no visible convergence in the loglik panel or in most parameter panels across 20 mif2 iterations. The authors themselves write: "The plot of the log likelihood seems to fluctuate around a mean value, with no apparent convergence." Despite this acknowledgment, Section 7 concludes that SEIQR is the best model. Non-convergence of mif2 means the reported log-likelihood is a lower bound on the true MLE, not an estimate of it.

Suggested author action: Increase Nmif and run additional mif2 iterations until convergence is visible in the trace plots. If convergence cannot be achieved, this is a signal of model misspecification (which, given Issues 22.23.1 and 22.23.2, is likely the case) and should be explicitly discussed rather than used as the basis for a model-selection conclusion.

---

## Minor Points

**22.23.6 — SEIR pairs plot uses SIR likelihood data (code bug)**
ID: 22.23.6 | Severity: Minor

The code at line 539 reads `pairs(~loglik+Beta+mu_IR+eta+rho, data=sir_lik_local, pch=16)` inside the SEIR local search results section. This plots the SIR likelihood surface as though it were the SEIR surface. Figure 11 therefore shows SIR, not SEIR, pairs.

Suggested author action: Replace `sir_lik_local` with `seir_lik_local` on that line and regenerate fig_011.

---

**22.23.9 — mu_IR = 0.006 in SIR MLE is biologically implausible**
ID: 22.23.9 | Severity: Minor

The best SIR local-search result (Table "SIR Local Search Results") shows mu_IR = 0.006, implying a mean infectious period of 1/0.006 ≈ 167 days. For Omicron, the typical infectious period is 5–10 days (mu_IR ~ 0.1–0.2). This extreme value is not flagged or discussed. It is likely a symptom of the model attempting to compensate for the low-peaked simulation outputs visible in fig_007 by keeping individuals infectious for very long periods.

Suggested author action: Flag this as a potential identifiability or misspecification issue. Compare the estimated mu_IR to literature values for Omicron. Consider whether the model can simultaneously fit the rapid rise-and-fall of the Omicron wave with biologically realistic parameter values.

---

**22.23.13 — "Lowest log-likelihood = best model" is non-standard language**
ID: 22.23.13 | Severity: Minor

Section 7 concludes "the log likelihood value of the SEIQR model is the lowest." In standard statistical usage, a higher (less negative) log-likelihood indicates a better fit. The authors appear to use "lowest" to mean "smallest absolute value," which is non-standard and misleading.

Suggested author action: Replace "lowest log-likelihood" with "highest log-likelihood" throughout, and clarify that a log-likelihood of -601 is higher (better) than -50126 within the same model class (noting that the between-class comparison is invalid for the reasons stated above).

---

**No model diagnostics (conditional log-likelihoods, ESS)**
Severity: Minor

No per-time-point conditional log-likelihoods are plotted for any model, and effective sample size (ESS) is never reported. These diagnostics are essential for identifying which portions of the time series the model fits poorly and for detecting particle degeneracy.

Suggested author action: Extract and plot the per-observation filter log-likelihoods and ESS from a pfilter run at the final MLE for the best model.
