# Peer Review: W25 Project 14 — Influenza Case Trends in Nova Scotia

## Summary

This project models weekly lab-confirmed influenza cases in Nova Scotia (2014–2019) using ARIMA, SIR, SIRS, and SEIRS POMP frameworks. The SEIRS model achieves the best log-likelihood among the three compartmental models and includes profile likelihood analysis over the reporting rate. The project is generally well-structured, but has several methodological, statistical, and presentation weaknesses described below.

---

## Weaknesses (Prioritized)

### 1. [Major] SIRS Log-Likelihood of +19821.71 Is Nonsensical and Unexplained

In the conclusion, the authors report log-likelihood values as: SIR = −761.97, SIRS = **+19821.71**, SEIRS = −590.46. A positive log-likelihood of nearly +20,000 for a discrete-count model is essentially impossible unless the model is being evaluated in probability (not log-probability) space, or there is a coding error in how the SIRS best-index is retrieved. The code at line 1345 sets `mif_sirs <- local_mifs_sirs[[best_index]]`, but `best_index` at that point refers to the SEIRS local search result (line 1346), not the SIRS result. This indexing error means the reported SIRS log-likelihood is meaningless, and the comparative conclusion across models is therefore unreliable. This is the most serious flaw in the project.

### 2. [Major] SIRS Model Uses Population N = 3.25e8 (U.S. Population), Not Nova Scotia

The SIRS initial parameters fix `N = 3.25e8`, which is approximately the population of the United States, not Nova Scotia (~969,400 as correctly used for SEIRS). This mismatch is never acknowledged and fundamentally undermines the SIRS model's epidemiological interpretation: the per-capita transmission rates and the scaling of the observation model (with `rho = 2.8e-5`) are calibrated to a population roughly 335 times larger than the actual study region.

### 3. [Major] SIRS Measurement Model Uses Poisson, Not Negative Binomial

The SIRS model uses a Poisson measurement model (`rpois`, `dpois`), while both the SIR and SEIRS models use a negative binomial. Given that the data are overdispersed (right-skewed histogram, median of 1 vs. max of 87), a Poisson measurement model is likely misspecified, and the difference in distributional assumptions makes formal log-likelihood comparison across the three models invalid.

### 4. [Major] SIRS Global Search Uses Only `global_results_sirs_test_df` for Best Fit, Ignoring Accumulated `sirs_lik.csv` Results

At line 1010, the best global parameter is selected solely from `global_results_sirs_test_df` (the current run's 50 chains), while the code appends all prior results to `sirs_lik.csv`. The comparison in the pair plot uses `all_results` from the CSV, but the simulation and reported best fit ignore accumulated runs. This inconsistency means the "best global fit" shown for SIRS may not be the true optimum across all stored results.

### 5. [Major] Profile Likelihood Best-Fit rho Lies Outside Its Own 95% CI — Inconsistency Not Resolved

The authors acknowledge that the best-fit rho from the global search (0.001132) falls outside the 95% CI from the profile (approximately 0.001769), and that the profile peak is higher than the global search maximum. This is an important signal of incomplete convergence or an inadequate global search. While the authors note this, they do not investigate or attempt to resolve the discrepancy, which should be a core part of interpreting the profile likelihood result.

### 6. [Major] ARIMA Model Selected and Fitted on Differenced Series, but Framed as ARIMA(p,0,q)

The AIC table is computed on `diff_series` (first-differenced data), but the models are specified as `arima(data, order = c(p, 0, q))` with `d=0`. This means the report is fitting ARIMA(p,0,q) to the differenced series, which is equivalent to ARIMA(p,1,q) on the original series — but the final model is labeled "ARIMA(5,0,5)" or "ARIMA(2,0,2)." The text claims "d=1 due to first-order differencing," yet the code does not enforce d=1 in the `arima()` call. This is a contradictory presentation that creates ambiguity about the actual fitted model.

### 7. [Major] SIR Recovery Rate mu_IR ~0.003–0.004 Implies Infectious Period of ~250–300 Days

The best SIR fits yield mu_IR ≈ 0.00366 (local) and ≈ 0.00329 (global), implying a mean infectious period of approximately 1/(0.00366) ≈ 273 days. For influenza, the typical infectious period is 3–7 days. This extreme implausibility is mentioned only briefly as "very low recovery rate" without investigating the cause, which is likely a structural identifiability problem in the SIR model given the long time series. No attempt is made to constrain or fix mu_IR to a biologically realistic value in the SIR model, in contrast to the more careful treatment in SEIRS.

### 8. [Moderate] SIRS Step Function Has Inconsistent Versions Within the Same Document

The SIRS step function is defined twice in the Rmd (lines 577–597 and lines 857–887). The second version adds numerical safety clamps (`fmin`/`fmax`) and uses `M_PI` instead of the literal `3.141592653589793`. The POMP object is rebuilt at line 889 using the second version, but the local search at lines 700–743 uses the first version (via the earlier `sirs_pomp` object). Results from local search and global search may therefore correspond to subtly different model implementations.

### 9. [Moderate] SEIRS H Compartment Accumulates dN_IR, Not New Infections — Mismatch with Model Description

In the SEIRS step snippet, `H += dN_IR` accumulates recoveries from I (the I-to-R flow), so the measurement model `rho * H` is a fraction of recoveries, not incidence. In an influenza context, reported cases typically track new infections or new symptomatic cases, not recoveries. While this is the same convention used in the SIR model, it is not explained or justified, and it conflates the observation with a lagged state change.

### 10. [Moderate] Spectral Analysis Is Applied to Undifferenced Series with `frequency = 1`, Undermining Period Interpretation

The spectral analysis (lines 126–145) sets `frequency = 1` on the undifferenced case series. The dominant period found is ~54 weeks, which is taken as confirmation of a yearly cycle. However, this analysis uses the raw series, which was shown to be nonstationary (ACF decaying slowly), and a trend component can create spurious low-frequency peaks. The spectral analysis should be applied to the differenced or detrended series for a valid interpretation.

### 11. [Moderate] SIR Global Search Uses Only 5 Likelihood Replications per Chain (`replicate(5, ...)`)

The SIR global search evaluates log-likelihood with only 5 particle filter replications per starting point (line 436), compared to 20 in the local search evaluation (line 363). With only 5 replicates, the log-mean-exp estimate has higher variance, which can affect ranking of starting points. The local and global SIR searches also use different Np values (2000 vs. 2000 for evaluation) but inconsistent replicate counts.

### 12. [Moderate] SEIRS Global Search Lower Bounds for amp, mu_EI, mu_IR, mu_RS, rho Are Set to Exactly 0

The `runif_design` lower bounds for `amp`, `mu_EI`, `mu_IR`, `mu_RS`, and `rho` are all 0. Because `log` and `logit` transformations are applied to these parameters, starting values at or near 0 will produce -Inf or extreme values in transformed space, likely causing numerical instability in early mif2 iterations. A small positive lower bound (e.g., 1e-3) would be safer.

### 13. [Moderate] Inconsistent Observation Variable Names Across Models (cases_obs vs. cases)

The SIR model uses `cases_obs` as the observation variable (defined in the data and measurement model), while the SIRS and SEIRS models use `cases`. The data is re-read and re-processed separately for each model section with different variable names. This inconsistency is not flagged, and the data preparation code is duplicated three times with minor variations that could introduce subtle bugs.

### 14. [Minor] Reported Observation Count Is Self-Contradictory

The introduction states "The dataset contains 262 observations" and then two sentences later says "We have 261 observations in our dataset." No explanation is given for the discrepancy; the filter from 2014-09-06 to 2019-09-07 applied in the code produces one of these counts, but the inconsistency is unexplained and undermines confidence in data handling.

### 15. [Minor] ChatGPT Cited as a Reference for Standard POMP Methodology Choices

Two references (`rwsd` and `profile`) cite ChatGPT as the source for decisions about setting `rw.sd` values for mu_EI and mu_IR, and for interpreting why a profile-likelihood peak can exceed a global search maximum. Both of these are standard topics covered in the course notes and literature. Citing a language model for methodological rationale is inappropriate in a scientific report, especially when authoritative sources are available.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_ls.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_pf.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_gs.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/influenza_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/sirs_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/final_citations.bib`
