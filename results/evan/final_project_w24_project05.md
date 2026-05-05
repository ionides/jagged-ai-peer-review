# Final AI Review: w24, Project 05 — Modeling Flu Cases in Oklahoma

---

## Overall Assessment

This paper addresses a well-motivated question — whether a seasonal SEIRS POMP model can capture weekly influenza dynamics in Oklahoma — and demonstrates commendable scope: exploratory analysis, SARIMA baseline, SEIRS implementation with sinusoidal seasonal forcing, local and global optimization via iterated filtering, and informal parameter profiling. The authors are honest that the POMP model underperforms the SARIMA benchmark and conclude accordingly, which reflects good scientific integrity. However, several methodological issues limit confidence in the results. The SARIMA baseline may have been fitted with the wrong seasonal period (12 weeks instead of 52), which would undermine the comparison. The global search log-likelihoods appear to be taken from mif2 output rather than replicated particle filter evaluations. Most seriously, key transition rate parameters (mu_IR, mu_RS) vary by orders of magnitude across global searches at comparable likelihoods, indicating severe identifiability problems that are not addressed. Profile likelihoods were not computed, so no confidence intervals are available for any parameter. The conclusion that SARIMA is preferred is directionally plausible, but the direct comparison of likelihoods across model classes requires explicit methodological justification that is absent.

---

## Key Strengths

- **ID 24.05.S1 — Appropriate SEIRS model choice.** Waning immunity (R→S transition) is biologically well-motivated for influenza and is a meaningful extension over a basic SIR model. *Why it matters:* Model structure should reflect disease biology; this choice does.

- **ID 24.05.S2 — Negative binomial measurement model.** The final SEIRS specification uses `dnbinom_mu` and `rnbinom_mu`, appropriately accounting for overdispersion in flu case counts. *Why it matters:* Overdispersion is common in disease surveillance data; ignoring it inflates apparent goodness-of-fit.

- **ID 24.05.S3 — Replicated pfilter for log-likelihood evaluation.** The local search correctly runs 10 replicated particle filters to obtain a reliable log-likelihood rather than using mif2's internal (unreliable) likelihood. *Why it matters:* This is the methodologically correct approach and demonstrates understanding of the particle filter's Monte Carlo variability.

- **ID 24.05.S4 — Iterative global search strategy.** Running six global searches with progressively refined parameter ranges and using pair-plots to guide subsequent searches is a reasonable optimization strategy given the high-dimensional parameter space. *Why it matters:* Single global searches with broad priors are unlikely to find the maximum likelihood in complex SEIRS models.

- **ID 24.05.S5 — Honest reporting of negative results.** The authors clearly acknowledge that the SEIRS model does not outperform SARIMA and discuss why. *Why it matters:* Scientific integrity requires reporting results as found, not as hoped.

---

## Major Points

**ID 24.05.1 — Possible wrong seasonal period in SARIMA**
The SARIMA grid search code uses `period=12` (line 321), but the data has weekly frequency with annual (52-week) seasonality. The text describes the selected model as SARIMA((1,1,1)×(0,1,1)[52]), which is inconsistent with the code. If period=12 was actually used, the model captures a 3-month cycle rather than an annual cycle, and the resulting log-likelihood of -838.43 is not a valid benchmark. *Why it matters:* The entire conclusion rests on comparing the POMP log-likelihood (-1003.30) to this SARIMA baseline. *Suggested action:* Verify which period was used in the actual computations. If period=12, refit with period=52 and report the corrected likelihood and AIC.

**ID 24.05.3 — Parameters mu_IR and mu_RS are not identified**
Across global searches 2–5, mu_IR ranges from approximately 35 to 27,000 per week and mu_RS from approximately 175 to 17,000 per week, while achieving log-likelihoods only slightly worse than the best result. This is a clear symptom of a nearly flat likelihood surface in these directions — the model cannot distinguish between these very different biological scenarios. *Why it matters:* Unidentified parameters mean that estimated values cannot be interpreted, and the model may be overfitting a degenerate solution. *Suggested action:* Constrain mu_IR and mu_RS to biologically plausible ranges (e.g., infectious period 1–3 weeks implies mu_IR ≈ 0.33–1.0 per week; immune period several months to a year implies mu_RS ≈ 0.02–0.1 per week) and discuss whether the data can identify these parameters within those ranges.

**ID 24.05.4 — Profile likelihoods absent; no parameter confidence intervals**
The paper explicitly states that profile likelihoods could not be computed due to computational constraints. The "poor man's profiles" pool heterogeneous global search results and do not constitute proper profiles — they do not trace the maximum likelihood as a function of each parameter with all others optimized. The standard 95% CI cutoff (max loglik − 1.92) is not applied. *Why it matters:* Without CIs, all parameter estimates are point estimates with unknown uncertainty, and no scientific claims about parameter values can be made. *Suggested action:* Compute formal profile likelihoods for at least Beta0, rho, and mu_EI. Report the maximum likelihood parameter vector with MCAP-based 95% confidence intervals.

**ID 24.05.2 — Global search likelihoods likely from mif2, not replicated pfilter**
The result tables for global searches 1–5 report log-likelihoods that appear to come directly from mif2 output (there is no pfilter re-evaluation code in these sections). Only global search 6 is followed by a pfilter run, and that pfilter uses only the single best parameter vector. The best parameter set across global searches is identified by comparing these mif2 log-likelihoods, which the course notes warn are unreliable. *Why it matters:* If mif2 likelihoods are noisy, the "best" parameter set selected may not actually have the highest true likelihood. *Suggested action:* For each global search, evaluate the top 10–20 parameter vectors using replicated pfilter runs and select based on pfilter log-likelihoods.

**ID 24.05.7 — Conclusion treats non-comparable likelihoods as directly comparable**
The conclusion states that the POMP log-likelihood (-1003.30) is "much higher than" the SARIMA log-likelihood (-838.43) and uses this to conclude SARIMA is preferred. However, SARIMA is fitted to a doubly-differenced series with a Gaussian measurement model, while POMP is fitted to the original counts with a negative binomial model. These likelihoods do not correspond to the same statistical model for the same data and cannot be directly subtracted or ranked without further analysis. *Why it matters:* The conclusion may be correct in direction, but the methodological justification is absent. *Suggested action:* Acknowledge explicitly that the two likelihoods are not on a common scale. Alternatively, compare models using a simulation-based forecast criterion (e.g., one-step-ahead prediction performance on held-out data) that applies to both model classes equally.

---

## Minor Points

- **ID 24.05.6 — Short estimated immune period.** The best-fit mu_RS ≈ 0.076/week implies an average immune period of ~13 weeks (~3 months). Published estimates for seasonal flu immunity are typically 6–12+ months. This short estimate may reflect model misspecification. *Suggested action:* Discuss whether the estimated immune period is consistent with published influenza natural history.

- **ID 24.05.8 — Unused parameter eta in initial code.** The first SEIRS model paramnames vector includes `eta` but this parameter is not implemented in the step or init functions. *Suggested action:* Remove eta from paramnames or explain its intended role.

- **ID 24.05.12 — loglik.se not reported.** Monte Carlo standard errors for the replicated pfilter log-likelihoods are computed but never reported in the text. *Suggested action:* Report loglik ± loglik.se after each pfilter evaluation.

- **ID 24.05.13 — Fixed parameter values not documented.** S0, E0, I0, R0, and k were fixed after the local search, but the fixed values and the rationale for fixing them are not stated in the text. *Suggested action:* Add a sentence stating the fixed values and justifying the choice.

- **ID 24.05.NEW1 — Result RDS/CSV files not archived.** Code loads from paths like `SEIRS/seirs_lik_1.csv` and `SEIRS/seirs_local_results.RDS` that are not present in the submission. *Suggested action:* Archive all Great Lakes output files alongside the manuscript.

- **ID 24.05.NEW2 — No per-chain convergence traces for global searches.** Trace plots are shown only for the local search. It is not possible to verify convergence of individual mif2 chains in any global search. *Suggested action:* Show representative trace plots for at least one global search run.
