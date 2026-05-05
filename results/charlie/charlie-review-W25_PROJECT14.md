# Peer Review: W25 Project 14
## "Nova Scotia's Influenza Cases: Capturing the Seasonal Behavior"

---

## Summary

This project fits SIR, SIRS, and SEIRS compartmental models to weekly lab-confirmed influenza cases in Nova Scotia (2014–2019) using the POMP framework. The work includes exploratory data analysis with ACF/PACF/spectral analysis, an ARIMA baseline, particle-filter-based local and global searches for each model, and a profile likelihood over the reporting rate for the SEIRS model. While the project is broad in scope and demonstrates familiarity with pomp workflows, it has several critical weaknesses: the SIRS model's Poisson measurement model is underdispersed relative to the data, the final model comparison contains a gross numerical error (positive log-likelihood for SIRS), convergence of the global search is inadequate (only a marginal improvement from local search), the profile likelihood is conducted only for a single parameter, and no non-mechanistic benchmark comparison is performed. The ARIMA model is discussed but never formally compared to the POMP models on a common scale.

---

## Major Issues

### 1. Positive log-likelihood reported for SIRS model — clear numerical error

In the Conclusion, the authors print the final model comparison as `SIR = -761.97, SIRS = 19821.71, SEIRS = -590.46` and state "the SEIRS model performs best, with the lowest value of -590.46." The SIRS value of +19821.71 is plainly impossible for a log-likelihood on this data — it is orders of magnitude larger than any plausible value and positive. This arises because the variable `best_index` is re-defined at line 1346 *after* it is used at line 1345 to extract `mif_sirs`. Specifically, the code reads:

```r
mif_sir  <- local_fits[[best_index]]          # uses SIR best_index from line 376
mif_sirs <- local_mifs_sirs[[best_index]]     # also uses SIR best_index — wrong!
best_index <- which.max(unlist(local_ll_seir[, "loglik"]))
mif_seirs <- local_mifs_seir[[best_index]]
```

`mif_sirs` is indexed by the SIR model's `best_index`, not the SIRS model's best index. The SIRS object indexed by whatever integer happened to be stored as the SIR best index may correspond to an unconverged or pathological run, producing a nonsensical positive value. The conclusion and discussion based on this comparison are therefore unreliable. The authors should compute and report each model's best log-likelihood using the correct best-fit objects.

### 2. No non-mechanistic benchmark comparison

None of the mechanistic models (SIR, SIRS, SEIRS) is compared against a non-mechanistic statistical benchmark such as an ARIMA or auto-regressive negative binomial model. While ARIMA models are fitted in the EDA section, their AIC values (on the differenced series) are never converted to a log-likelihood on the original scale and never placed alongside the POMP model log-likelihoods. Without such a comparison, it is impossible to assess whether the mechanistic structure captures meaningful dynamics beyond what a simple statistical time series model achieves. Wheeler et al. (2024) identify this as the single most diagnostic check for mechanistic model evaluation, noting that none of the 32 papers in their Haiti cholera review performed it.

### 3. SIRS measurement model uses Poisson — unjustified, underdispersed

The SIRS model uses `dpois` / `rpois` as its measurement model (`sirs_dmeas`, line 610), while the SIR and SEIRS models both use negative binomial. Influenza count data exhibit heavy right-skew (range 0–87, median ~1), which is typical of overdispersed count data that a Poisson model cannot accommodate. The Poisson measurement model is never justified in the text. This misspecification will distort parameter estimates and penalize the SIRS model's log-likelihood relative to the other models, making model comparisons unfair. The authors should use a negative binomial measurement model (with estimated dispersion parameter) for all three models, or justify the Poisson choice with evidence that the data do not exhibit extra-Poisson variation. Wheeler et al. (2024) explicitly recommend overdispersed measurement models for epidemic count data.

### 4. Global search shows negligible improvement over local search — inadequate computation

For the best SEIRS model, the global search maximum log-likelihood is -586.6 and the local search maximum is -587.5, a difference of only 0.9 log-units across 100 global starting points. Such a marginal improvement suggests either that (a) the optimization has not escaped local optima and genuinely better regions of parameter space have not been explored, or (b) the parameter box is too narrow to constitute a true global search. The global search uses only Nmif = 100 iterations and 2000 particles, and the parameter box is adopted directly from a prior year's project without justification specific to this dataset. The authors should report log-likelihood traces from the global mif2 runs to demonstrate convergence, use a wider parameter box with more starting points, and run a second-stage mif2 from the best global candidates (Wheeler et al. 2024, computational adequacy).

### 5. Profile likelihood conducted for only one parameter, using a non-standard CI cutoff

Profile likelihoods are presented only for the reporting rate rho in the SEIRS model. No profiles are shown for the key epidemiological parameters: Beta0, amp, phase, mu_EI, mu_IR, or mu_RS. For a model with seasonal forcing, the amplitude and phase parameters are of direct scientific interest and may be poorly identified. In addition, the 95% confidence interval uses a cutoff of `max(loglik) - 0.5 * qchisq(df=1, p=0.95)` (i.e., a drop of 1.92 log-units), which is the standard likelihood-ratio-based threshold. However, the authors do not apply the Monte Carlo Adjusted Profile (MCAP) correction to account for Monte Carlo noise in the particle filter likelihood estimates. With loglik standard errors around 0.4–2.2 (as shown in the influenza_params.csv), the uncorrected CI may be substantially too narrow. The authors should either apply MCAP or acknowledge this limitation explicitly.

### 6. SIRS model population size is inconsistent and unjustified

The SIRS model uses N = 3.25e8 (325 million, roughly the US population) in the initial simulation and local search, while Nova Scotia's population is approximately 969,400. This is a three-orders-of-magnitude error. The SEIRS model correctly uses N = 969,400. The SIR model uses N = 100,000 (also not Nova Scotia's population and not justified). Using an incorrect population size changes the scale of the force of infection and will produce biologically implausible parameter estimates for Beta, rho, and initial state proportions. The authors note the SIRS model parameter mu_IR = 6.44 (implying a mean infectious period of about 2.2 hours), which is epidemiologically absurd for influenza; this is almost certainly an artifact of the incorrect population size. The authors should use a consistent, correct population size across all models (969,400 or the population for the period of study).

### 7. SIRS model "pandemic year" threshold is not scientifically grounded

The SIRS step function uses a hard threshold `if (t < 261)` to switch between pre-pandemic (`a`) and pandemic (`b`) transmission rates. The dataset spans 2014–2019 (weeks 0–261), none of which contains a recognized influenza pandemic. The 2009 H1N1 pandemic predates the study period. The text defines `a` and `b` as "average transmission rates for pre-pandemic years and pandemic seasons" but provides no justification for applying this distinction to a 2014–2019 dataset. In practice, setting t < 261 vs. t >= 261 means the last observation (or near-last observation) switches to the "pandemic" regime, which makes no epidemiological sense and conflates a model feature with the dataset boundary. This structural misspecification likely contributes to the SIRS model's poor fit and the anomalous final log-likelihood.

### 8. ACF/PACF misidentification and incorrect AIC model selection

The AIC table is computed on the **first-differenced** series with `order = c(p, 0, q)` (i.e., ARMA models on the differenced data), but the reported AICs correspond to ARIMA(p,1,q) on the original scale. The code at line 175 calls `aic_table(data = diff_series, P = 5, Q = 5, seasonal = FALSE)`, fitting ARMA(p,q) to `diff_series`. The minimum AIC of 1821.56 is then labeled as belonging to ARIMA(5,0,5), which is incorrect — fitting an ARMA(5,5) to the differenced series is equivalent to ARIMA(5,1,5) on the original series. Moreover, the authors conclude that ARIMA(2,0,2) may be better due to parsimony, yet neither model is formally compared to the POMP models via log-likelihood on the original (undifferenced) series. The ACF interpretation ("non-stationary") is also questionable: the ACF of a seasonal epidemic series decaying to zero does not indicate non-stationarity per se, and no formal stationarity test (ADF, KPSS) is conducted.

---

## Minor Issues

### 9. Conflicting observation count in text

The Introduction states both "The dataset contains 262 observations" and "We have 261 observations in our dataset" in consecutive sentences (lines 67–69). The correct number should be stated consistently and verified from the data.

### 10. SIR measurement model observes recoveries, not new infections

The SIR step function accumulates `cases = dN_IR` (recoveries), and the text at line 247 correctly states "newly recovered individuals." However, influenza surveillance data typically count new diagnoses/reports, which correspond to new infections (dN_SI) or new symptomatic cases emerging from exposure, not recoveries. This interpretation is inconsistent with standard epidemiological modeling practice and is not discussed. The authors should clarify whether reported cases represent incident infections or recovered individuals, and justify the choice.

### 11. No sessionInfo() or package version documentation

No `sessionInfo()` output, `renv.lock`, or package version list is provided. The `pomp` API has changed substantially across versions; results may not reproduce on current CRAN releases. This is flagged in the code-supplement checklist as a POMP-specific red flag.

### 12. Global search for SIRS uses sequential (not parallel) lapply

The SIRS global search at lines 932–968 uses `lapply` (sequential) rather than the `foreach %dopar%` used elsewhere. With 50 chains, this is substantially slower than necessary and inconsistent with the rest of the workflow. The SIR and SEIRS global searches both use parallel execution.

### 13. Profile likelihood for rho reports an implausible interpretation

The text states "only about 0.1769% of true infections are actually reported in our data — roughly 1-2 reported cases for every 1,000 infections." A reporting rate of 0.1769% implies that the true weekly infection burden in Nova Scotia is roughly 50,000 individuals during peak weeks (87 observed / 0.001769). Nova Scotia's entire population is under 1 million, which would imply 5% of the population infected per week at peak — an implausible figure not discussed or cross-validated against independent surveillance estimates. The authors should compare the implied incidence to external data (e.g., ILI rates, serology) to assess biological plausibility, as recommended by Wheeler et al. (2024, §Corroboration with scientific knowledge).

### 14. PACF plot in EDA section has incorrect title

The PACF of the differenced series is titled "ACF of Influenza Cases" instead of "PACF of Influenza Cases" (line 105 of the Rmd): `pacf(diff_series, main = "ACF of Influenza Cases")`. This is a copy-paste error.

### 15. seirs_pf.R profile script does not include rho in rw.sd

The profile likelihood script (`seirs_pf.R`, line 106–110) fixes `rho` by omitting it from `rw.sd`, which is the correct approach for a profile over `rho`. However, this is not stated anywhere in the main text or in comments. Additionally, the profile search stratifies guesses by rounded rho values (`group_by(cut=round(rho,5))`), but it is not confirmed that the resulting profile covers a sufficiently wide range of rho values; the reported CI is extremely narrow (a single point at 0.001769) and may reflect an incomplete profile rather than a genuinely tight constraint.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_ls.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_gs.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/seirs_pf.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/influenza_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/README`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project14/Makefile`
