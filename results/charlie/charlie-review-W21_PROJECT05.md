# Peer Review: W21 Project 05
### Influenza A in Michigan — POMP Models for Contact Rate Change

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) with particle filter likelihood evaluation |
| **R packages used** | pomp (>=3.0), foreach, doParallel, doRNG |
| **Code publicly available** | Yes, submitted via course Git repository |
| **Data publicly available** | Yes — CDC FluView Interactive |
| **Benchmark comparison included** | No |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2 + replicated pfilter used, but logmeanexp applied to list not guaranteed correct; loglik.se enormous for Models 1 and 2 |
| 2 | Benchmark comparison | ✗ | No ARIMA or non-mechanistic model fitted |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported for initial guesses and local search, but extreme MC variability undermines comparisons for Models 1 and 2 |
| 4 | Model diagnostics | ~ | Trace plots shown; conditional log-likelihoods and ESS not monitored |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods; no confidence intervals |
| 6 | Computational adequacy | ✗ | Local search only; no global search; Nmif=50 (below run_level=2 standard); no convergence from diverse starting points |
| 7 | Forecast methodology | N/A | No forecasts attempted |
| 8 | Model variations and nested comparisons | ~ | Three models considered but not compared quantitatively via log-likelihood (conclusion abandons this) |
| 9 | Stochasticity | ~ | Stochastic SIR/SEIR with Euler-binomial transitions; measurement model binomial (not overdispersed) |
| 10 | Reproducibility and extendability | ~ | Code provided; CSV files of likelihoods saved; no sessionInfo(); no package version pinning |
| 11 | Corroboration with scientific knowledge | ✗ | Fitted parameters not checked against influenza biological literature |
| 12 | Measurement model specification | ✗ | H accumulates recoveries (dN_IR) rather than new infections (dN_SI); binomial model with no overdispersion |
| 13 | Initial conditions | ~ | Initial susceptible fraction estimated via eta; biological plausibility not discussed |

---

## Summary

This project applies three POMP models (SIR, SEIR, and SIR with hardcoded time-varying contact rate) to weekly CDC influenza A surveillance data from Michigan during the 2019-20 season. The stated research question asks whether POMP models can capture the change in contact rate that coincided with the COVID-19 pandemic's onset. While the data exploration and modeling motivation are clearly presented and the general POMP workflow (simulation, local search, likelihood evaluation) is followed, the project contains a material code bug that appears to have driven a wholly incorrect conclusion, a fundamental measurement model misspecification, and a failure to estimate the key quantity of interest (the contact rate reduction) as a model parameter. Global search, profile likelihoods, and a non-mechanistic benchmark are all absent. The conclusion — that all three models are inappropriate — is not consistent with the saved likelihood results for Model 3.

**Strengths:**
- Data sourcing from CDC FluView is well described; the EDA comparing five flu seasons and highlighting the COVID-19 impact is clear and well-motivated.
- The POMP modeling workflow (Csnippet specification, mif2 local search, replicated pfilter likelihood evaluation with logmeanexp) is correctly structured in principle.
- Saving intermediate likelihood results to CSV files (sir_lik.csv, seir_lik.csv, sir2_lik.csv) is a good reproducibility practice.

**Weaknesses:**
- A code bug causes Model 3's likelihood to be displayed incorrectly, leading to a false conclusion that all models fail.
- H accumulates recoveries (dN_IR) rather than new infections (dN_SI); flu lab reports represent positive test counts (new cases), not recoveries.
- The contact rate reduction in Model 3 is hardcoded (0.7×Beta), not estimated as a parameter.
- No global search, no profile likelihoods, no benchmark comparison.

---

## Major Issues

### 1. Code Bug: Model 3 Likelihood Printed Incorrectly, Driving False Conclusion (CC-Yes, Error 1.4)

In the code chunk `SIR2_init_lik` (Rmd line 458), the displayed result is:

```r
print(sir_L_pf)   # BUG: should be print(sir2_L_pf)
```

This prints the initial likelihood for Model 1 (SIR) rather than Model 3 (SIR with time-sensitive contact rate). The conclusion states: "I found that the second model seems to be a better fit, while the first and third model both have issues with NaN log-likelihood." This diagnosis of Model 3 appears to have been made based on Model 1's result.

The saved sir2_lik.csv tells a completely different story: Model 3's local search achieves a best loglik of **-333.4 (SE=1.37)**, which is dramatically better than Model 1's best of -940.4 (SE=95.2) and Model 2's best of -861.0 (SE=31.1). Model 3 also converges stably (tight SE) in contrast to Models 1 and 2. The conclusion that "all three models are not appropriate" and that "global search and profile likelihood calculations are not carried out" appears to rest entirely on this printing error. The correct action would have been to continue with Model 3 through global search and profile likelihood computation.

**Fix:** Replace `print(sir_L_pf)` with `print(sir2_L_pf)` in chunk `SIR2_init_lik`, then revise the conclusion to reflect Model 3's substantially better and stable likelihood.

---

### 2. Measurement Model Observes Recoveries Instead of New Infections

All three models use `H += dN_IR` in the process model and `reports = rbinom(H, rho)` in the measurement model. The accumulator H therefore counts weekly transitions from I to R (recoveries), and the observation model treats reported flu-positive tests as a binomial sample of these recoveries.

CDC FluView clinical laboratory data records positive influenza test counts, which represent new infections detected through testing, not recoveries. In a standard POMP influenza model, the accumulator should be `H += dN_SI` (new susceptible-to-infectious transitions per week). Using recoveries as the observable introduces a systematic lag and conceptual mismatch: patients test positive upon becoming symptomatic (infected), not upon recovery.

This is a fundamental measurement model misspecification, not a minor coding detail. It affects all three models and will distort parameter estimates, particularly for Beta (the contact rate, which directly controls dN_SI) and mu_IR (the recovery rate, which controls dN_IR). With H tracking recoveries, the optimizer has to reconcile the timing of observed peaks with the wrong latent process stage.

**Fix:** Replace `H += dN_IR` with `H += dN_SI` in all three process model Csnippets. This requires moving the H increment before the S decrement to capture the new infections at each Euler step.

---

### 3. Contact Rate Reduction Factor Is Hardcoded, Not Estimated

Model 3 ("SIR model with time sensitive contact rate") addresses the stated research question of modeling the change in contact rate. However, the reduction factor is hardcoded as a constant 0.7 in the Csnippet:

```c
if (t > 22) {
  dN_SI = rbinom(S, 1-exp(-0.7*Beta*I/N*dt));
}
```

The factor 0.7 — implying a 30% reduction in contact rate after week 22 (approximately March 2020) — is a fixed assumption, not a parameter estimated from data. The research question asks whether POMP models can be used to *estimate* the change in contact rate, but Model 3 answers only the question of whether a pre-specified 30% reduction produces plausible simulations.

This reduction factor should be an additional free parameter (e.g., a multiplier `alpha` on the logit or log scale) estimated via iterated filtering. This would allow the data to determine the magnitude of the contact rate change, which is scientifically the central question.

**Fix:** Add a parameter `alpha` (contact rate multiplier after COVID onset), transform on logit scale, and update the Csnippet to use `alpha*Beta` after week 22. Include `alpha` in rw.sd() during mif2 and in the partrans specification.

---

### 4. No Global Search — Convergence Not Established (CC-Yes, Error 1.8)

All three models use only a local search: 20 mif2 runs initialized from the same single initial guess (e.g., `sir_params = c(Beta=31, mu_IR=2.5, rho=0.025, eta=0.0853, N=9.984e6)`). This does not constitute a global search because all runs begin from the same point in parameter space. Without randomly initialized starting values spread across the plausible parameter region, there is no evidence that the optimizer has found the global maximum rather than a local one.

The course standard for demonstrating convergence is to run mif2 from many diverse starting points (global search) and verify that independent runs reach consistent terminal log-likelihoods. The text acknowledges model problems are present but attributes them to model misspecification (NaN log-likelihoods) without checking whether different starting points produce different terminal likelihoods.

**Fix:** Implement a global search using randomly sampled starting values across the plausible parameter ranges (e.g., via `runif` or `sobol` space-filling design) for at least Model 3, which shows a stable likelihood in local search.

---

### 5. Extreme Monte Carlo Standard Errors Invalidate Model Comparisons

The initial likelihood for Model 1 (SIR) is reported as -1278.1 (SE=6.87). After local search, the best reported loglik is -940.4 with SE=95.2. For Model 2 (SEIR), the best is -861.0 with SE=31.1. Standard errors of 95 and 31 loglik units are orders of magnitude larger than what is needed for reliable model comparison (typically SE < 1 is desirable).

A loglik SE of 95 means the 95% confidence interval for the true loglik spans roughly ±190 units from the estimate, making any comparison between models with such variability statistically meaningless. The large SE indicates particle filter degeneracy — the particles collapse at some time points, which is a symptom of model misspecification (consistent with the measurement model error noted in Issue 2). This diagnostic is not discussed in the report.

**Fix:** Investigate the cause of particle degeneracy (likely the measurement model misspecification). Monitor ESS across time steps using `plot(pfilter(...))` to identify when filter collapse occurs. After correcting the measurement model, assess whether SE drops to acceptable levels (<1 loglik unit).

---

### 6. No Non-Mechanistic Benchmark Comparison (CC-Yes, Error 1.6)

No ARMA, ARIMA, or regression model is fitted to the data. The project moves directly from exploratory data analysis to POMP modeling. Without a non-mechanistic baseline, it is impossible to assess whether the POMP models capture meaningful structure that simpler statistical models would miss.

At minimum, fitting an ARMA model and reporting its log-likelihood alongside the POMP models' log-likelihoods would allow a crude assessment of whether the mechanistic structure adds explanatory value. Given that the 2019-20 season includes an unusual sharp drop (the COVID-19 effect), it is plausible that even a simple ARMA model would struggle and that the mechanistic structure genuinely helps — but this comparison is not made.

**Fix:** Fit an ARMA(p,q) model selected by AIC to the weekly reports series and report its log-likelihood for comparison with the POMP models' best likelihoods.

---

### 7. No Profile Likelihoods — Parameter Identifiability Unassessed (CC-Yes, Error 1.9)

No profile likelihoods are computed for any model parameter. The conclusion dismisses this analysis because "global search and profile likelihood calculations are not carried out" due to model failures. However, Model 3 achieves a best loglik of -333.4 (SE=1.37) in local search — a stable, well-defined optimum — which would permit profile likelihood computation for at least Beta, mu_IR, and eta.

Without profile likelihoods, there is no evidence that these parameters are identifiable from 52 weekly observations, no confidence intervals are reported, and the point estimates from local search may be unreliable. This is particularly important for the contact rate Beta and the reporting rate rho, which may be correlated.

**Fix:** Compute profile likelihoods for at least Beta and the contact rate reduction factor alpha (once added as a free parameter) using the course standard of 5–30 profile points, with confidence intervals at the Wilks 95% cutoff.

---

### 8. Conclusion Contradicts Saved Likelihood Evidence

The conclusion states: "I will safely conclude that all three models are not appropriate for fitting the data." However, the file sir2_lik.csv contains 18 rows from the local search of Model 3, with the best loglik of -333.4 (SE=1.37). This is a well-converged, stable optimum — not a model failure. The pairs plot from the local search would show whether this optimum is well-characterized.

The conclusion appears to have been written based on the erroneous display of Model 1's likelihood for Model 3 (Issue 1) and the apparent NaN likelihoods in Models 1 and 2. The appropriate conclusion should distinguish between Model 3 (which appears viable, at least after correcting the measurement model) and Models 1–2 (which show degeneracy).

**Fix:** Revise the conclusion to reflect the actual saved likelihood results. Model 3 should be identified as the candidate for further analysis (global search, profile likelihoods) pending correction of the measurement model and estimation of the contact rate reduction factor.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots are shown for all three models. For Models 1 and 3, the loglik panel does not converge clearly upward; for Model 2, convergence to approximately -1000 is noted (starting from -10000). However, all local searches start from the same single point, so the trace plots show the trajectory of 20 parallel runs from one starting point rather than evidence of global convergence. No multiple diverse starting values are used.

**Particle filter:** Np=2000 particles are used for mif2 and Np=10000–20000 for likelihood evaluation. ESS is not monitored or plotted. The enormous loglik.se for Models 1 and 2 (up to 95 loglik units) is strong evidence of particle filter degeneracy, but this is not investigated.

**Conditional log-likelihoods:** Not reported. Per-time-step log-likelihoods would identify which weeks are most problematic — critical for understanding the measurement model misspecification.

**Profile likelihoods:** Not computed.

**Computational scale:** Nmif=50 for local search, which is below the run_level=2 standard of Nmif=100. The report does not discuss computational cost or run time.

---

## Reproducibility Assessment

**Code availability:** Code is contained in the submitted Rmd file. The code is structured sequentially and generally readable.

**Final parameters:** Likelihood CSV files (sir_lik.csv, seir_lik.csv, sir2_lik.csv) are saved and archived, which is good practice for intermediate results.

**Model-code consistency:** The measurement model (binomial on H) is described in both text and code, and they are consistent with each other. However, as noted in Issue 2, both the text and code use an incorrect measurement model (observing recoveries rather than new infections).

**Package versions:** No `sessionInfo()` output is included and no package versions are pinned. The Rmd does check `packageVersion("pomp") >= "3.0"` and `getRversion() >= "4.0"` which is helpful but insufficient for reproducibility.

**Auxiliary data:** The CDC FluView CSV file is included in the submission directory (FluViewPhase2Data folder). A random seed is set (`set.seed(5312021)`).

---

## Minor Issues

- **Nmif=50 is below course standard:** The local search uses Nmif=50 iterations. The course run_level=2 standard is Nmif=100. With a complex likelihood surface and particle degeneracy, more iterations are warranted.

- **No classical time series analysis:** The project skips ARIMA analysis entirely. Most STATS 531 projects include an ARIMA section as a baseline and scientific context. Even a brief ARMA fit would provide a frame of reference.

- **Biological plausibility of parameters not discussed:** The estimated mu_IR values range from 1.5 to 14 in the local search, implying mean infectious periods ranging from 0.07 to 0.67 weeks (0.5 to 4.7 days). While this range partially overlaps with the known influenza infectious period (1–5 days), the wide spread and extreme values are not discussed. For beta, values of 55–87 per week imply a basic reproduction number R0 = Beta/(mu_IR) in the range of 4–30 depending on the run, which is implausibly high for seasonal influenza (R0 ≈ 1.2–1.4). This warrants comment.

- **eta = 0.0853 implies only 8.5% susceptible:** The initial susceptible fraction is fixed at 8.5% (or estimated near 8.5% in local search) for a population of ~10 million people. This would imply nearly 9 million people have prior immunity at the start of the 2019-20 flu season, which is not discussed or validated against seroprevalence data.

- **Binomial measurement model without overdispersion:** The binomial dmeas is used throughout. Given the variability in weekly testing counts (TOTAL.SPECIMENS varies substantially), a negative binomial or beta-binomial model would be more appropriate. The conclusion mentions the professor's suggestion to try negative binomial but it is not implemented.

- **`logLik()` called on list returned by `.combine=c`:** In `SIR_init_lik`, the pattern `sir_pf %>% logLik() %>% logmeanexp(se=TRUE)` is used. The `.combine=c` in `foreach` for pfilterd.pomp objects returns a list; calling `logLik()` on a list relies on method dispatch to extract log-likelihoods from each element. This is non-standard but likely works correctly via pomp's S4 dispatch. A more explicit pattern (`sapply(sir_pf, logLik)`) would be clearer.

- **Week index used instead of calendar dates:** The time variable is an integer index (1–52) rather than a calendar date, making it difficult to interpret when "week 22" corresponds to on the real calendar without cross-referencing the data setup code. The report identifies week 22 as "10th week of 2020" (approximately March 9–15), which should be stated explicitly.

- **Typos in text:** "contatct" → "contact" (Section 3.1 Model 3 heading); "simualte" → "simulate" (conclusion); "wihch" → "which" (SEIR local search section); "cases" misspelled as "casese" (conclusion).

- **SEIR conclusion mismatch:** The text says "the current lowest loglikelihood is around -860.9967" for the SEIR model (correctly identified from the CSV), but also says the simulation "does not seem to align with the original dataset" when showing the simulation from MLE parameters. If the MLE produces a poor visual fit, this is a sign of model misspecification that warrants investigation (not merely noting), and could be diagnosed using the measurement model issue identified in Issue 2.

- **No description of how `season19` is constructed in SEIR section:** The object `fluSEIR` is rebuilt from `df` inside the SEIR local search chunk (using `df %>% pomp(...)`) rather than referencing the previously built `fluSEIR` object. This redundancy could be simplified, though it does not produce incorrect results.

---

## Recommendation

**Major Revision.**

The project demonstrates familiarity with the POMP framework and presents a well-motivated research question about COVID-19's impact on influenza contact rates. However, three critical issues must be addressed before the analysis can be considered valid: (1) the code bug in `SIR2_init_lik` (printing the wrong model's likelihood) must be fixed and the conclusion revised accordingly; (2) the measurement model must be corrected to accumulate new infections (dN_SI) rather than recoveries (dN_IR); and (3) the contact rate reduction factor must be introduced as an estimated parameter rather than a hardcoded constant. Without these corrections, the central conclusions of the paper are not supported by the analysis.

Additionally, global search and profile likelihood computation should be conducted for Model 3 (which shows a stable, well-behaved loglik in local search), and a non-mechanistic benchmark should be added.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W21/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W21/project05/sir_lik.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W21/project05/seir_lik.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W21/project05/sir2_lik.csv`
