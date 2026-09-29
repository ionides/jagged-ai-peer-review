# Final AI Review: Volatility Analysis of NASDAQ 100 (w24, Project 09)

## Overall Assessment

This paper applies three modeling frameworks — ARIMA, GARCH, and Breto's stochastic volatility model via POMP — to 53 years of daily NASDAQ 100 log-returns (approximately 13,400 observations). The paper has a clear and coherent narrative: ARIMA residuals show heteroscedasticity, motivating GARCH, which still leaves autocorrelation structure; POMP provides a more flexible stochastic volatility model, and the leverage effect is tested by comparing the full model against a simplified no-leverage variant. The authors show genuine engagement with the POMP framework, including running both local and global search, computing a profile likelihood, and correctly comparing models via likelihood on a common dataset. However, several inferential problems weaken the quantitative conclusions: the AIC table for ARIMA contains an anomalous entry that may have determined model selection; the GARCH-to-POMP likelihood comparison is made without establishing that both likelihoods are evaluated in the same way; the profile likelihood is too sparse and noisy for reliable confidence intervals; and parameter convergence for the full POMP model is incomplete. Addressing these issues would substantially improve the credibility of the paper's main conclusions.

---

## Key Strengths

**ID: 24.09.7 — GARCH benchmark used and compared on likelihood grounds**
The paper uses GARCH as a non-mechanistic benchmark and compares it to POMP via log-likelihood, which is the appropriate quantitative approach for this type of model comparison. This is a methodologically sound choice.

**ID: 24.09.8 — Leverage effect tested via nested model comparison**
Rather than assuming the leverage parameter is important, the authors construct a simplified no-leverage model and fit it with the same procedure. The finding that the no-leverage model achieves lower likelihood is presented as direct evidence for retaining the leverage term. This is an example of good scientific practice.

**ID: 24.09.10 — Residual diagnostics motivate modeling choices**
ACF plots of residuals and squared residuals are used consistently to motivate the sequence of model upgrades (ARMA → GARCH → POMP), giving the modeling progression an evidence-based structure.

---

## Major Points

**ID: 24.09.1 — AIC table anomaly for ARMA(5,5)**
Severity: Major

The AIC table shows ARMA(5,5) with AIC = -79,185.97, while ARMA(5,4) has AIC = -79,148.08. Adding one MA parameter reduces AIC by approximately 38 units — opposite to the expected penalty. This strongly suggests a numerical optimization failure for the ARMA(5,5) fit. Because the paper selects ARMA(5,5) as the best model based on this entry being the minimum in the table, the model selection outcome may be unreliable.

Why it matters: If ARMA(5,5) is a numerical artifact, the chosen benchmark for GARCH and POMP comparison may be incorrectly specified.

Suggested action: Re-fit ARMA(5,5) from multiple random starting points. If the anomaly persists, report it as a numerical failure and select the best model excluding that entry. Flag this result explicitly in the text.

---

**ID: 24.09.3 / 24.09.2 — Monte Carlo variability and mif2 likelihood interpretation**
Severity: Major

The paper reports log-likelihood values for the POMP model as summary statistics (Min/1stQ/Median/Mean/Max) across multiple pfilter runs. However, the comparisons against GARCH appear to reference the Max value across mif2 search iterations rather than a dedicated replicated pfilter evaluation at a fixed final parameter vector. The mif2-internal likelihood is evaluated under a perturbed particle filter and is not a reliable estimate of the model log-likelihood. For valid model comparison, the correct procedure is: (1) identify the best parameter vector from the global search, (2) run at least 10 independent pfilter evaluations at that vector with the final Np, and (3) report logmeanexp of those evaluations.

Why it matters: Using the maximum across mif2 runs can overstate the model's true log-likelihood. The GARCH comparison depends on this number being accurate.

Suggested action: Provide explicit replicated pfilter evaluation at the final parameter vector for both the full model and the simplified model. Use logmeanexp, not Max, as the reported log-likelihood.

---

**ID: 24.09.5 — Profile likelihood too sparse for reliable CI**
Severity: Major

The paper constructs a profile likelihood for sigma_eta and reports a 95% CI of approximately 0.54 to 1. The manuscript itself acknowledges that "the samples we got were pretty few." The particle filter standard error within a single profile point is approximately 0.82 log-likelihood units (from the global search summary statistics), which is non-negligible relative to the chi-squared threshold of 1.92 used for a 95% CI. With few noisy profile points, the CI boundary is determined by random variation rather than the true profile shape.

Why it matters: The confidence interval is the primary uncertainty quantification result for the POMP model. An unreliable CI weakens the paper's inferential conclusions about sigma_eta.

Suggested action: Compute a formal MCAP confidence interval with at least 10–15 profile points, display the chi-squared cutoff as a horizontal line on the profile plot, and report the CI numerically. If computational constraints prevent this, describe the profile as directional evidence only and make no formal CI claim.

---

**ID: 24.09.6 — Convergence not achieved for phi and mu_h**
Severity: Major

The paper explicitly acknowledges that phi and mu_h do not converge well in either local or global search for the full POMP model. Trace plots show these parameters spanning wide ranges. Despite this, the paper draws conclusions about specific parameter values (e.g., "phi was at 0.96," "the leverage effect converged to a really low value") and uses the best-achieved likelihood to claim that POMP outperforms GARCH.

Why it matters: If the global optimizer has not found a consistent maximum, the reported "best" log-likelihood may be well below the true maximum, making the model comparison unreliable. Parameter interpretations derived from non-converged runs are also unreliable.

Suggested action: Demonstrate that independent restarts of the global search produce consistent top log-likelihoods (within particle filter noise). If this is not feasible, qualify all parameter-level conclusions and the model comparison as preliminary.

---

**ID: 24.09.4 — Likelihood comparability between GARCH and POMP not fully justified**
Severity: Major

The paper's main conclusion — that POMP outperforms GARCH — rests on comparing log-likelihood values across model classes (GARCH from tseries and fGARCH, and POMP from pfilter). Both appear to be evaluated on the same ndx$demeaned series, which is necessary for comparability. However, the unexplained ~100 log-likelihood-unit discrepancy between fGARCH (43,363) and tseries GARCH (43,265) for nominally the same model specification raises serious questions about whether the GARCH and POMP likelihoods are computed under the same conventions (e.g., same treatment of initial conditions, same conditioning set). The paper proceeds to compare POMP against tseries GARCH without addressing this discrepancy.

Why it matters: If the GARCH likelihood uses a different convention from the POMP likelihood (e.g., conditioning on initial observations vs marginalizing over them), the comparison may be invalid.

Suggested action: Explicitly verify and state that both GARCH and POMP log-likelihoods are marginal likelihoods for the same sequence of observations. Investigate and explain the fGARCH vs tseries discrepancy. Consider presenting the comparison using only one GARCH implementation.

---

## Minor Points

**Notation inconsistency:** The full model uses sigma_{w,n} (apparently time-varying) while the simplified model uses sigma_w (constant). It is unclear whether this difference is intentional or a notational imprecision.

**Ljung-Box test for model selection:** Ljung-Box p-values are used to motivate model transitions. This is a less preferred approach compared to AIC-based selection.

**ESS not monitored:** Effective sample size from the particle filter is never mentioned. Reporting ESS (or at least noting it was not tracked) is standard practice for particle filter analyses.

**No summary comparison table:** A table showing log-likelihood and number of parameters for all four models (ARIMA, GARCH, full POMP, simplified POMP) would substantially improve readability and the clarity of the main comparison.

**Run level parameters:** Np and Nmif values for each run level are stated inline in different sections rather than in a consolidated specification. A table of run levels would clarify the computational setup.

**sigma_w^2 structural constraint:** The simplified model constrains sigma_w^2 = sigma_eta^2 * (1 - phi^2), which equates the process noise to the stationary variance of the AR(1) log-volatility. This is a specific modelling choice that deserves brief justification.

**Strogatz citation:** Reference [9] (Strogatz nonlinear dynamics) appears in the conclusion but is not connected to any specific methodological point. It should either be connected to a claim or removed.

**Proofreading:** Several typos are present throughout ("samplwas," "samll," "Althoguh," "recoganized," "paremeters"). The manuscript would benefit from careful proofreading.
