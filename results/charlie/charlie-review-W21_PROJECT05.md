# Peer Review: W21 Project 05
## Seasonal Influenza in Michigan — POMP Modeling of Contact Rate Change

---

## Summary

This project investigates weekly influenza A case counts in Michigan during the 2019-20 flu season, with the stated goal of modeling the change in contact rate associated with COVID-19-related behavioral changes. Three POMP models are fitted: a standard SIR model, an SEIR model, and an SIR model with a time-varying contact rate that drops by 30% after week 22. While the scientific motivation is coherent and the use of the pomp package is appropriate, the analysis is substantially incomplete. No global search is performed, no profile likelihoods are computed, and the conclusion abandons all three models based on convergence difficulties without proposing or implementing a corrective path. The analysis stops at the local search stage, and critical methodological steps (global optimization, identifiability analysis, goodness-of-fit reporting) are absent. Several implementation issues further undermine the reliability of the reported results.

---

## Major Issues

### 1. No global search performed — analysis stops prematurely (POMP Checklist #6)

The authors explicitly state in Section 4: "global search and profile likelihood calculations are not carried out." This means that parameter estimates are based solely on local searches initialized from manually chosen starting points. Without a global search from diverse starting values, there is no evidence that reported likelihoods are near the MLE. All downstream comparisons and conclusions rest on local optima. This is the most critical gap in the analysis. Per Wheeler et al. (2024), evidence of convergence requires multiple optimization runs from different starting points reaching similar terminal likelihoods. Error 1.8 (missing convergence diagnostics for iterated filtering) is directly applicable here (CC-Yes, Major).

The third model achieves a best log-likelihood of -333 from its local search. That this substantially outperforms the first model (best: -940) is suggestive, but the comparison is unreliable without global searches for each model.

### 2. No profile likelihoods — parameter identifiability unassessed (POMP Checklist #5)

Profile likelihoods are never computed for any model. Without profile likelihoods, it is impossible to determine whether any parameter is identifiable from the 52-week flu season data. The contact rate reduction factor (0.7) in the third model is hard-coded rather than estimated; its uncertainty is never quantified. Error 1.2 and the absence of profile likelihoods apply here (CC-Yes, Major). The conclusion that models are "not appropriate" is undermined by the lack of any identifiability analysis.

### 3. Hard-coded, non-estimated contact rate reduction — a key scientific parameter is not inferred (POMP Checklist #1)

The scientific question is explicitly "Is it possible to model the change of contact rate of influenza in Michigan using POMP models?" Yet in the third (and ostensibly best) model, the post-lockdown contact rate is fixed at 70% of Beta via the expression `0.7*Beta*I/N*dt`. The factor 0.7 is not estimated; it is a manually chosen constant. This means the model does not actually estimate the change in contact rate — it imposes it. The research question is therefore not answered by the analysis. A proper implementation would estimate the reduction factor (e.g., parameterize as `kappa * Beta` where kappa is estimated, or use a step-function covariate with an estimated coefficient).

### 4. Wrong likelihood value printed for the third model's initial evaluation (Section 3.1, chunk SIR2_init_lik)

In the chunk labeled `SIR2_init_lik`, the code reads:

```r
print(sir_L_pf)
```

This prints the likelihood of the **first** model (SIR), not the third (SIR with time-varying rate). The variable `sir2_L_pf` is computed correctly in the chunk but never printed; `sir_L_pf` from the earlier chunk is printed instead. This is a copy-paste error that produces a misleading comparison table in the initial guess evaluation section. The conclusion in Section 4 ("the third model seems to be the best fit") is partly based on visual simulation comparisons, but the reported likelihoods are incorrect for model 3 at this stage.

### 5. Log-likelihood standard errors are extremely large — Monte Carlo noise is unaddressed (Error 1.4, CC-Yes, Major)

Examining the saved CSV files reveals log-likelihood standard errors ranging from 1 to over 219 log units (e.g., SIR model entries show se = 105, 159, 219). For model comparisons to be valid, the standard errors must be small relative to likelihood differences. When the se is 95 log units for an estimate of -940, the estimate is essentially noise. The authors do not comment on this issue. Only results with small standard errors (se < 2–3) should be treated as reliable, yet the analysis treats all rows as comparable outputs.

### 6. Declining or unstable log-likelihood traces attributed to "NaN" rather than model misspecification (Error 1.5, CC-Yes, Major)

In Sections 3.2 (first and third models), the authors observe that "the log-likelihood bouncing around" and attribute this to "NaN log likelihood, which means that the model might not be a good fit." While the NaN observation is correct, the interpretation stops short: NaN log-likelihoods and declining or erratic likelihood traces under iterated filtering are signals of model misspecification, not merely numerical inconvenience. The correct response (per Error 1.5, explicitly course-taught) is to revise model structure — for example, switching to a negative binomial measurement model to handle overdispersion. Instead, the authors abandon all three models without proposing any structural fix.

### 7. No benchmark comparison against a non-mechanistic model (POMP Checklist #2; Error 1.6, CC-Yes, Major)

No non-mechanistic benchmark (e.g., ARMA, negative binomial regression) is fitted to the data. The mechanistic models are not compared against any baseline. This means there is no way to assess whether the POMP models capture structure beyond what a simple time series model would achieve. Error 1.6 is directly applicable (CC-Yes, Major).

### 8. Binomial measurement model — overdispersion not modeled despite author's own acknowledgment (POMP Checklist #9 and #12)

Both the SIR and SEIR models use a binomial measurement model: `lik = dbinom(reports, H, rho, give_log)`. The authors themselves note in the conclusion that "over-dispersed model such as negative binomial is suggested by professor." Despite this knowledge, no overdispersed measurement model is implemented. The binomial measurement model has no overdispersion parameter; it will systematically underfit the variance in outbreak counts. This is particularly problematic for a dataset with a sharp peak followed by near-zero counts, which requires a flexible measurement model.

### 9. Accumulator variable H tracks recoveries (dN_IR) rather than new infections — potential semantic mismatch

In both the SIR model (Section 3.1, chunk `SIR_building`) and the time-varying SIR model (chunk `SIR2`), the accumulator is updated as `H += dN_IR` (new recoveries). The measurement model then links observed case counts to H via a reporting probability rho. The data (`TOTAL.A`) represents newly confirmed positive tests — i.e., incident infections, not recoveries. Accumulating recoveries rather than new infections means the measurement model tracks the lagged flow out of I rather than the flow into I, introducing a systematic timing mismatch. The SEIR model has the same error. This will bias the reporting rate and transition rate estimates.

---

## Minor Issues

### 10. No ARIMA or classical time series analysis presented

The report jumps directly to POMP modeling without any preliminary ARIMA analysis or spectral analysis of the seasonal pattern. Even a brief exploration of autocorrelation structure or seasonal decomposition would contextualize the mechanistic modeling and partially substitute for the absent benchmark comparison.

### 11. Single flu season used — 52-week analysis offers limited data for parameter estimation

Only the 2019-20 flu season is analyzed (52 observations). With five parameters in the SIR model and six in the SEIR model, and with the likelihood surface showing erratic behavior, the dataset is likely too short to identify all parameters simultaneously. The authors do not discuss this limitation. Pooling multiple flu seasons (with shared parameters) or fixing some parameters from prior knowledge (e.g., mean infectious period for influenza A is well-established at roughly 5 days) would improve identifiability.

### 12. No model diagnostics presented (POMP Checklist #4)

No effective sample size (ESS) plots, no conditional log-likelihood traces, and no filtering-distribution simulations are shown. The only diagnostic is the trace plot of parameter estimates and log-likelihoods across mif2 iterations. ESS monitoring would reveal whether the particle filter degenerates and whether the likelihood estimates are reliable.

### 13. The `sir` variable assigned at line 531 is unused

At the end of chunk `SIR_lik`, the code assigns `sir <- sir_lik_local[[1]]` but this object is never used subsequently. This is dead code that likely reflects an incomplete analysis plan.

### 14. Pairs plots not interpreted

Pairs plots of parameter estimates against log-likelihoods are produced for all three models but are not interpreted in the text. The pairs plot for model 3 (sir2_lik_local) shows wide scatter with no clear high-likelihood region, which is itself diagnostic of convergence failure — but the authors do not discuss it.

### 15. References are minimal — only course notes and the data source cited

The reference section contains only the data source and course lecture notes. No epidemiological literature on influenza natural history is cited (which would inform the plausibility of estimated beta, mu_IR, and rho), and no methodological references for POMP or iterated filtering are included. The reported parameter values (e.g., Beta = 33.8 per week, mu_IR = 3.1 per week implying a 2.2-day infectious period) are not compared to known influenza A natural history.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project05/sir_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project05/sir2_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project05/seir_lik.csv`
