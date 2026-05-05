# Peer Review: W24 Project 05
## "Modeling Flu Cases in Oklahoma"

---

## Summary

This project fits a SEIRS POMP model with a sinusoidally time-varying transmission rate to weekly influenza-like illness (ILI) counts in Oklahoma (2011–2015), alongside a SARIMA baseline. The authors demonstrate competent use of the pomp framework — including iterated filtering (mif2), particle filtering, and iterative global search — and the overall workflow is structured appropriately. However, the central conclusion (that POMP is "unnecessary" because SARIMA has a higher log-likelihood) rests on an invalid direct comparison between two models with different observation distributions. Beyond this key flaw, the analysis suffers from poorly identified parameters, an incorrect seasonal period in the SARIMA grid search, an extremely implausible reporting rate estimate, and the absence of profile likelihoods that the authors explicitly acknowledge they could not compute.

---

## Major Issues

### 1. Invalid log-likelihood comparison between SARIMA and POMP

The paper's primary conclusion — that "the POMP approach is unnecessary for the Oklahoma flu data" — is based on comparing the SARIMA log-likelihood (from `arima()`) to the POMP log-likelihood (from `pfilter()`). These two quantities are not on the same scale and cannot be compared numerically. The SARIMA likelihood is evaluated under a Gaussian distribution on twice-differenced weekly counts, while the POMP likelihood is evaluated under a negative binomial distribution on the original counts. The observed differences in log-likelihood values reflect differences in the measurement model and data transformation, not differences in model adequacy. No valid statistical conclusion about relative model performance can be drawn from this comparison. To compare the two approaches on equal footing, the authors would need to either (a) recast the SARIMA as a state-space model with the same negative binomial observation model and evaluate both likelihoods on the same data, or (b) use a proper information criterion that accounts for the different observation models and number of parameters.

### 2. SARIMA grid search uses incorrect seasonal period

The AIC grid search for the seasonal order (lines 232–246 of the Rmd) specifies `period=12`, implying a 12-observation seasonal cycle. The dataset is weekly, so the annual cycle has period 52. The final model is then fitted with `period=52` (line 254), which is correct. The disconnect means the AIC table that motivated the choice of seasonal orders (SAR=0, SMA=1) was computed under a misspecified seasonal period. The reported minimum-AIC model order may be entirely different from what a correctly specified grid search would recommend. The entire SARIMA model-selection section should be recomputed with `period=52` throughout.

### 3. Reporting rate (rho) estimate is biologically implausible

The best-fit reporting rate is approximately rho = 0.0013 (0.13%), meaning fewer than 1 in 750 true flu cases would be captured in the ILI surveillance data. For Oklahoma ILI surveillance, typical CDC estimates of influenza reporting rates are on the order of 1–10%. At rho = 0.0013 and a peak reported case count of roughly 1,500/week, the model implies approximately 1.15 million true infections per week in a state of 3.8 million — implying that nearly one-third of the entire state would be infected simultaneously at each seasonal peak. This is epidemiologically implausible. Per Wheeler et al. (2024), implausible parameter estimates should be interpreted as evidence of model misspecification rather than accepted as biological findings. The authors do not discuss this estimate's plausibility. A sensitivity analysis fixing rho to a range of values consistent with known flu surveillance capture rates, or imposing an informative prior on rho, is needed.

### 4. Key parameters are poorly identified, but no profile likelihoods are computed

Inspection of the combined global search results (`SEIRS/seirs_lik.csv`) reveals that within 1.92 log-likelihood units of the maximum (the standard 95% confidence region), mu_IR spans 0.27 to 86.6 — a range of over two orders of magnitude. Beta0 spans 0.57 to 9.6 (a 17-fold range), and amp spans 0.36 to 0.97 (nearly the full admissible range). Although some of this spread may reflect search noise rather than true non-identifiability, these patterns are highly suggestive of a poorly identified likelihood surface. The authors acknowledge they were unable to compute proper profile likelihoods due to cluster performance issues. However, the conclusions about the model's convergence and adequacy cannot be trusted without at least addressing the apparent non-identifiability of mu_IR. Per Wheeler et al. (2024, §Parameter identifiability), implausible or unbounded parameter estimates are a diagnostic signal that should prompt investigation of model misspecification, not be dismissed. The authors should, at minimum, flag that mu_IR may be unidentifiable and discuss what this implies for the model's biological interpretation.

### 5. No benchmark comparison for the POMP model

The authors use SARIMA as a "baseline" but compare it to POMP only via the invalid log-likelihood comparison described above. No non-mechanistic statistical baseline is evaluated on the same scale as the POMP model (e.g., fitting a negative binomial regression or autoregressive model and evaluating its log-likelihood via pfilter or an equivalent approach). Wheeler et al. (2024) note that none of 32 reviewed papers performed such a comparison, and demonstrate that it is essential for assessing whether a mechanistic model captures meaningful structure. Without a valid benchmark comparison, the claim that SEIRS modeling is unnecessary (or alternatively, that it adds value) cannot be substantiated.

### 6. Log-likelihood direction misstated in the local search narrative

The Rmd states at line 547: "The local search produced a log-likelihood of [X]. This is several hundred points lower than the likelihood of the initial guess, a promising sign for finding an improved model." Lower log-likelihood means a worse fit (more negative value), not a better one. If the local search produced a genuinely worse fit than the manual starting parameters, this is not a "promising sign" — it would indicate the optimizer moved in the wrong direction. The authors appear to have confused the direction of improvement. This error propagates to the interpretation: if the local search worsened the fit (decreased the log-likelihood), then the characterization of subsequent global search results as "close" to the local search best is also misleading. The text needs to either correct the direction claim or clarify what numerical values are being compared.

---

## Minor Issues

- **SARIMA model text inconsistency.** The SARIMA formula displayed in the text uses `B_{12}` as the seasonal backshift operator (suggesting a period-12 cycle), consistent with the grid search error but inconsistent with the final fitted model at period=52. This should be updated to `B_{52}`.

- **rw.sd for phase is extremely small.** The `rw.sd` for the phase parameter in `mif2` is set to 0.01 (on the natural scale, since phase has no transformation applied). With phase ranging from approximately −25 to 0 weeks, perturbations of 0.01 week per iteration are negligibly small and will result in extremely slow exploration of the phase landscape. A perturbation of 0.1 to 0.5 weeks per iteration would be more appropriate given the scale of the search space.

- **k and initial conditions fixed during global search.** The authors fix S0, E0, I0, R0, and k during the global search, citing fast convergence in the local search. Fixing k (the negative binomial overdispersion parameter) prevents the global search from exploring overdispersion jointly with other parameters, and may bias estimates of rho. At a minimum, k should be jointly optimized or sensitivity to its fixed value should be assessed.

- **Phantom eta parameter in the first SEIRS model.** The initial SEIRS model's `paramnames` vector (line 354) includes `eta`, but `eta` does not appear anywhere in the Csnippet for `rprocess`, `dmeasure`, or `rmeasure`. This phantom parameter is silently unused. While this model is subsequently replaced, the inclusion of eta without explanation may confuse readers and suggests the code was not carefully reviewed before submission.

- **Inconsistency between claimed and actual search count.** The text states the global search used "a total of 750 models" (5 searches × 100 + 1 × 250), but the combined CSV file `SEIRS/seirs_lik.csv` contains 1,354 rows. This discrepancy — most likely due to the appending logic in the global script running multiple times — is unexplained in the text. The total computational effort should be accurately reported.

- **No quantitative goodness-of-fit summary for POMP simulations.** Model validation is conducted primarily through visual inspection of forward simulations. While the particle filter diagnostics (ESS, conditional log-likelihood plot) are shown, no summary statistics of simulated trajectories (e.g., peak timing, peak magnitude, seasonal duration) are compared quantitatively to observed data. Visual agreement is, as Wheeler et al. (2024) note, "only a weak and informal measure of goodness-of-fit."

- **Rationale for restricting data to 2011–2015 requires stronger justification.** The authors restrict the dataset to 2011–2015, citing COVID-era disruption (2020–2023) and computational feasibility. The first rationale is sound, but the computational feasibility argument is weak — a 14-year weekly series (730 observations) is not unusual for POMP analysis. The restriction to four seasons may also reduce the statistical information available to identify model parameters, contributing to the identifiability problems noted above.

- **Decomposition section misstates the seasonal period.** The text at line 98 states that "the seasonal component dominates the time series decomposition" and attributes the dominant frequency of 0.02 cycles/week to "significant daily or weekly seasonality." The correct interpretation is annual seasonality (one cycle per ~50 weeks), not daily or weekly. This is a conceptual error in the EDA section.

- **No discussion of model limitations beyond the parameter estimation issues.** The conclusions mention that flu vaccinations and population dynamics were not included, but do not discuss whether the model's fixed population assumption (N = 3.8 million, constant) is appropriate, or whether the sinusoidal forcing function is a good approximation of true seasonal transmission dynamics for influenza. For example, a cosine basis or school-term forcing (as used in measles models) might better capture the bimodal or skewed seasonal patterns seen in the data.

- **Total computational cost not reported.** The paper mentions that the Great Lakes cluster was used and ran slowly, but does not report the total CPU-hours consumed or the wall-clock time for the global searches. This makes it impossible for readers to assess whether the reported results are likely to be near the global maximum of the likelihood surface, and prevents independent reproduction feasibility assessment.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/great-lakes-seirs-global.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/great-lakes-seirs-local.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/SEIRS/seirs_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project05/SEIRS/seirs_local_results.RDS`
