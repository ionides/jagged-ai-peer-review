# Final AI Review
## Project: w25 project12 — Comparative Analysis of Volatility Models for Daily Gold Prices

---

## Overall Assessment

This paper undertakes a well-motivated three-way comparison of ARIMA, GARCH, and POMP models for daily gold log-returns, applying mif2 and replicated particle filtering for the POMP components and delivering an honest conclusion that Student-t GARCH outperforms the more complex latent-variable alternatives in-sample. These are genuine strengths. However, the paper has several technical errors that need to be resolved before the results can be trusted: the Heston model produces negative variance and negative volatility-of-volatility estimates that are physically impossible under the stated model; an AIC value stated for the best ARIMA model does not match the table or the log-likelihood; the final comparison table mislabels the GARCH specification; profile likelihoods have identifiability gaps and numerical instability; and no confidence intervals are reported for any model parameter. These issues collectively undermine the inferential claims, particularly for the POMP models.

---

## Key Strengths

**25.12.13 — Correct POMP likelihood evaluation methodology.** The use of mif2 global search followed by replicated pfilter for likelihood estimation is methodologically appropriate. Comparing all models on the same 772-day window (noted explicitly in Section 7) enables valid cross-model log-likelihood comparison.

**25.12.16 — Honest assessment of model hierarchy.** The paper does not oversell the POMP models; it concludes that Student-t GARCH is the most efficient in-sample choice and frames POMP contributions as "narrative colour." This intellectual honesty is scientifically sound and commendable.

**25.12.17 — Quantitative GARCH model selection.** The improvement from Gaussian to Student-t innovations is documented numerically (logLik gain of approximately 15 points), and the convergence behavior of both POMP models is shown via trace plots.

---

## Major Points

**25.12.1 — Physically impossible Heston parameter estimates.**
Concern: The reported estimates sigma = -0.0051 and v0 = -2.38e-5 violate the Heston model's mathematical requirements: sigma is the volatility-of-volatility and must be non-negative; v0 is the initial variance and must be positive. The paper attributes these to "variability inherent in particle filtering" (Section 5.1), but this explanation is incorrect — unconstrained Euler discretization allows the latent state v_t to cross zero and become negative, which is a model specification error.
Why it matters: all Heston log-likelihood values and parameter interpretations may be invalid if the latent state is negative during filtering.
Severity: Major.
Suggested action: Reparameterize using log(v_t) or apply a reflecting/absorbing boundary at zero to enforce positivity. Report whether the likelihood changes after the fix.

**25.12.2 — AIC value for ARIMA(2,0,2) is inconsistent.**
Concern: Section 3.2 states the best ARIMA(2,0,2) has AIC = -5046.32, but Table 1 shows the ARMA(2,2) cell as -5039.59, and the log-likelihood in Table 2 (2525.80) with k=5 parameters gives AIC = -5041.60, not -5046.32. The stated AIC cannot be verified from either the table or the reported log-likelihood.
Why it matters: the ARIMA benchmark is the foundation for all subsequent model comparisons.
Severity: Major.
Suggested action: Verify the AIC convention used by the software and reconcile all three values (table, log-likelihood, stated AIC) before reporting.

**25.12.3 — GARCH specification mislabeled in final comparison.**
Concern: Table 5 lists "GARCH(1,3)" as the GARCH entries, but Section 4 selects GARCH(1,1) after diagnostics, and Table 4 explicitly labels the compared models as GARCH(1,1). It is unclear which model was actually used for the final comparison.
Why it matters: GARCH(1,1) and GARCH(1,3) have different numbers of parameters, affecting AIC comparisons.
Severity: Major.
Suggested action: Decide on one model, update Table 5 and all surrounding narrative to be consistent.

**25.12.4 — kappa profile does not identify a lower confidence bound.**
Concern: The kappa profile (Figure 9) is flat from kappa approximately 0.7 to 1.7 and does not include points below approximately 0.7. The estimated optimum at kappa = 0.737 sits on the left edge of the plotted range. The lower confidence bound cannot be determined, yet the paper claims kappa is "well-identified."
Why it matters: a one-sided profile cannot support a claim of identifiability.
Severity: Major.
Suggested action: Extend the profile to kappa values near zero (e.g., 0.01, 0.1, 0.2, 0.4) to determine whether the likelihood remains flat or eventually drops. Report a two-sided MCAP confidence interval.

**25.12.5 — sigma_2 profile is numerically unstable.**
Concern: The profile likelihood for sigma_2 (Figure 12) shows two local maxima near sigma_2 = 0.010 and 0.025 with a valley in between, rather than a smooth single-peaked curve. This is inconsistent with a reliable profile and suggests the optimizer is tracking different local modes at different fixed sigma_2 values.
Why it matters: the reported maximum and any CI derived from this profile are unreliable.
Severity: Major.
Suggested action: Use more mif2 replicates per profile point and warm starts from the global optimum; report the MC standard error at each point.

**25.12.6 — Logit inversion error and RS model regime non-persistence.**
Concern: The text states p11 approximately 0.522 from logit_p11 = -0.249882, but the correct inverse logit is exp(-0.249882)/(1+exp(-0.249882)) approximately 0.438. A p11 of 0.44 means the low-volatility regime transitions to high-volatility with probability 0.56 at each step — essentially near-random switching, visible in Figure 11 as extremely rapid regime alternation.
Why it matters: the regime-switching model at this persistence level does not capture stable market states and may not be identifying economically meaningful dynamics.
Severity: Major.
Suggested action: Correct the inverse logit computation; reassess whether the RS model parameters imply economically meaningful regime persistence before interpreting Figure 11.

**25.12.7 — ESS not monitored or reported.**
Concern: Neither figures nor tables show the effective sample size (ESS) of the particle filter over time for either POMP model. The text claims ESS "stabilized" (Section 5.1) but provides no evidence.
Why it matters: if ESS collapses to near zero during filtering, the log-likelihood estimates are unreliable.
Severity: Major.
Suggested action: Include a plot of ESS over the 772 time steps for the best POMP model. If ESS drops below 10% of Np at any point, re-run with higher Np.

**25.12.8 — No confidence intervals for any parameter.**
Concern: No confidence intervals are reported for any parameter in any model. Profile likelihoods are computed but used only qualitatively.
Why it matters: without CIs, the uncertainty in parameter estimates is unquantified and claims about parameter values cannot be assessed for precision.
Severity: Major.
Suggested action: Report 95% CIs using the 1.92 log-likelihood cutoff for POMP profile parameters; report standard-error-based CIs for ARIMA and GARCH.

**25.12.M3 — Predictive accuracy promised but not delivered.**
Concern: The Introduction (Section 1) states that the paper evaluates models on "both fit and predictive accuracy," but Section 6 presents only in-sample log-likelihoods with no out-of-sample evaluation.
Why it matters: readers may rely on the implied out-of-sample claim for practical applications.
Severity: Major.
Suggested action: Either add an out-of-sample evaluation or revise the Introduction to accurately describe the in-sample comparison performed.

---

## Minor Points

**25.12.11 — Logmeanexp and pfilter replication count unspecified.**
Concern: The text states "multiple replicate runs" were used for likelihood evaluation but does not report the number of replicates or confirm that logmeanexp was applied rather than max. If individual run maxima were used, POMP likelihoods may be slightly upward-biased.
Severity: Minor.
Suggested action: State the number of pfilter replicates and confirm logmeanexp aggregation.

**25.12.10 — Heston convergence claimed but reached an invalid region.**
Concern: Figure 10 shows sigma and v0 traces converging to near-zero or negative values; the text interprets this as "strong convergence" without noting that the algorithm converged to a physically inadmissible region of the parameter space.
Severity: Minor.
Suggested action: Note in the figure caption that convergence to sigma approximately 0 and v0 < 0 signals a model constraint violation, not a satisfactory optimum.

**25.12.12 — ARMA order inconsistency in text.**
Concern: ARMA(2,2) is selected in Section 3, but Section 4 refers at two points to "ARMA(1,1)+GARCH(1,1)."
Severity: Minor.
Suggested action: Harmonize all references to the mean equation order throughout Sections 4 and 5.

**Notation and presentation.** The GARCH-t variance equation in Section 4.2 has a LaTeX rendering error making it unreadable. Figure reference numbers in Sections 4 and 5 are inconsistent with the figure sequence. Reference [10] (Wikipedia Volatility Clustering) should be replaced with a peer-reviewed source. The y-axis label in Figure 11 is partially cut off.
