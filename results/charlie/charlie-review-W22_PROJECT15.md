# Peer Review: W22 Project 15
## "Rise and Fall of Delta and Omicron variants: Comparison of Compartmental Models for SARS-CoV-2 variants"

---

## Summary

This project fits SEIR models to weekly sequenced COVID-19 case counts from the GISAID database for the Delta and Omicron variants in the United States, aiming to compare transmission parameters — particularly the exposure rate Beta — between the two variants. The study applies iterated filtering (mif2) with local and global searches and profiles the Beta parameter for each variant. While the mechanistic modeling approach is appropriate and the comparison of Beta across variants is the main scientific contribution, the analysis has several significant methodological weaknesses: the reporting rate is fixed without justification at a value inappropriate for sequenced-case data, convergence evidence is incomplete, the profile likelihood for the Delta variant is internally inconsistent, no non-mechanistic benchmark is compared, and key parameters are left without uncertainty quantification.

---

## Major Issues

### 1. Fixed Reporting Rate Is Inappropriate for the Data Source

The reporting rate `rho` is fixed at 0.1 throughout, justified by the claim that "roughly 10% of all cases are sequenced." However, the data are from GISAID and represent the count of sequenced genomes per week — not confirmed cases. The denominator for a sequencing rate is not the total infected population but rather confirmed positive tests that were selected for sequencing. The sequencing fraction varied substantially over time and between labs, and fixing rho at 0.1 conflates confirmed-case reporting with sequencing fraction. This misspecification is absorbed by Beta and other parameters, undermining the biological interpretability of all estimated parameters. No citation or sensitivity analysis is provided for this choice.

**Fix:** Either estimate rho freely, or carefully justify the 0.1 value with a source that quantifies the sequencing-to-confirmed-case ratio rather than the confirmed-to-total-infected ratio.

---

### 2. Profile Likelihood for Delta Beta Is Inconsistent with the MLE

The authors acknowledge that the Delta Beta profile likelihood yields a 95% CI of approximately [100, 150], yet the MLE from the global search was reported as Beta ~ 73 (the top row of `covid19_params.csv` shows Beta = 73.4). The profile range does not contain the global search MLE, and the authors attribute this to "high correlation between model parameters." This is not a satisfactory resolution. A valid profile likelihood CI must be centered at or near the MLE. When the profile and global search disagree, it indicates either that the profile search box was misspecified, or that the global search did not find the true MLE.

The profile range for Beta was set to [1, 400] with a box derived from the global search filtered at loglik > max - 200 (a very wide tolerance). Using a 200 log-unit window to define the nuisance parameter box inflates the search space and can cause the profile to find different optima than the global search. This is a course-confirmed error (Error 1.2 / Error 1.9): the profile as computed may not represent a genuine profile likelihood.

**Fix:** Reconcile the profile and global search MLEs. Re-run the profile with a narrower box (e.g., loglik > max - 10 or -20) and verify that the profile maximum coincides with the global MLE.

---

### 3. Global Search Uses Only One Round of mif2

In both the Delta and Omicron global searches, each guess is passed through `mif2(...) %>% mif2()` — two sequential mif2 calls where the second call uses the default arguments and does not re-specify `Np`, `Nmif`, `rw.sd`, or `cooling.fraction.50`. The second call inherits the object's stored parameters but uses whatever defaults are active in the environment. This is a fragile pattern and may not provide adequate additional optimization. The standard course practice is to use two explicit mif2 calls with the same settings to ensure adequate exploration, or to chain them with identical arguments.

**Fix:** Make the second mif2 call explicit: `mif2(Np=Np, Nmif=Nmif, rw.sd=..., cooling.fraction.50=0.5)`.

---

### 4. No Non-Mechanistic Benchmark Comparison

The SEIR model is not compared against any non-mechanistic baseline (e.g., ARMA, negative binomial regression, or even an IID negative binomial). Without such a comparison it is impossible to assess whether the mechanistic SEIR structure captures meaningful dynamics beyond what a simple statistical model would achieve. Given the substantial standard errors on the Delta log-likelihood (e.g., loglik.se = 5.58 for the top Delta result), and that the Omicron series is very short (~20 weeks), a benchmark comparison would be especially informative.

Per Wheeler et al. (2024) and course instruction (Error 1.6, CC-Yes), this is a meaningful validation step. The course notes explicitly state: "if the mechanistic model fits disastrously compared to the benchmark, our model is probably missing something important."

**Fix:** Compute the log-likelihood for an ARMA or negative binomial IID model on each variant series and report both alongside the SEIR log-likelihood.

---

### 5. Large Monte Carlo Standard Errors Undermine Likelihood Comparisons

The top Delta global search result reports loglik = -753.17 with loglik.se = 5.58 — an unusually large standard error that spans more than 11 log-likelihood units across two standard deviations. Several other Delta results have similarly large SEs (e.g., loglik.se = 19.25 for the third row). This means the likelihood comparisons in the global search pairs plot and the reported "maximum likelihood estimate" may be unreliable: the true ordering of parameter sets is obscured by Monte Carlo noise.

The global search uses `Np = 2000` (run_level=3 switch value used). With only `Nreps_eval = 10` pfilter replicates and `Np = 2000` particles, for a dataset with 50+ observations, substantial MC noise is expected. The Omicron series is shorter and its SEs are smaller (~0.3-0.6), suggesting the Delta model has more persistent particle degeneracy issues.

**Fix:** For the Delta model, increase Np substantially (e.g., 10,000-20,000) for final likelihood evaluations, or report the SE alongside each comparison explicitly.

---

### 6. No Profile Likelihood for mu_EI, mu_IR, or eta

The conclusion section directly states: "our findings for parameters other than Beta should be interpreted cautiously since we could not find time to run profile likelihood for those." The scientific conclusions compare mu_EI, mu_IR, and eta between variants ("the Omicron variant... will take more time for a people infected by Omicron variant to recover"), yet no uncertainty quantification exists for these parameters. Drawing biological comparisons from point estimates of parameters that show poor convergence in trace plots is not statistically supportable.

Per the POMP checklist (#5) and Error 1.9 (CC-Yes), parameter identifiability must be assessed with profile likelihoods before interpreting estimates.

**Fix:** Either compute profiles for the remaining parameters or restrict the conclusion to Beta, for which a profile is provided.

---

### 7. Reporting Rate and k Fixed Without Sensitivity Analysis

Both `rho = 0.1` and `k = 10` are fixed without any sensitivity analysis. The overdispersion parameter `k` in particular directly controls the variance of the negative binomial measurement model, and its value of 10 is relatively large (implying relatively low overdispersion). The choice is not justified, and given that neither parameter is estimated or profiled, the analysis cannot reveal whether the model fit is sensitive to these assumptions. Fixing k at 10 when it should be estimated is especially consequential because k affects all likelihood comparisons.

**Fix:** Estimate k from the data (include it in the mif2 search with appropriate rw.sd), or at minimum present results for two or three fixed values.

---

## Minor Issues

### 8. Delta Trace Plot Filters Out Runs Below loglik > -2000

The local search trace plots filter results using `filter(value > -2000)` for Delta and `filter(value > -1000)` for Omicron. This masking means runs that never converged (stuck in bad regions) are silently excluded from the convergence diagnostic. A trace plot that hides non-converging runs overstates the evidence for convergence. The number of excluded runs is not reported.

---

### 9. Initial Conditions Are Not Fully Justified

The initialization sets `E = 0`, `I = 1`, `R = nearbyint((1-eta)*N)`. Setting I=1 (fixed, not estimated) and E=0 at the start of the data series means the model assumes exactly one infectious individual at week 0. For a series that begins in January 2021 (Delta) or week 40 (Omicron), when the variant was already circulating, this initialization is implausible and may cause the particle filter to struggle during early time points. No sensitivity analysis or justification is provided.

---

### 10. Omicron Global Search Box Is Misaligned with Best Parameters

The Omicron global search uses `upper=c(Beta=100, ...)` as an upper bound, but the top Omicron results have Beta values of 389, 218, 263, 614 — all far above 100. The global search box upper bound for Beta was 100 for Omicron (line 389), yet the saved results show the best parameters at Beta >> 100. This means the global search could not have found those high-Beta parameter values directly from the `runif_design` — they must have been reached through `mif2` updating from lower initial values. The box for the global search was therefore too narrow, and the authors were lucky that mif2 moved the parameters to the right region. This is a form of parameter box misalignment (related to the pomp-global-search-box-misalignment skill).

---

### 11. Profile Beta Range for Delta Does Not Overlap MLE

The Delta Beta profile spans [1, 400], yet the best global search MLE for Delta was Beta ~ 73. The profile finds its peak near Beta ~ 130. These should coincide, and they do not. This is related to Major Issue #2 but also independently indicates that the profile search box (derived from loglik > max - 200) may have included a different mode than the one the global search identified. The discrepancy is not diagnosed in the text beyond the phrase "high correlation between parameters."

---

### 12. mu_IR Estimates Are Biologically Implausible for Delta

The top Delta global search result shows mu_IR = 5.46, implying a mean recovery time of 1/5.46 ≈ 0.18 weeks, or about 1.3 days. This is biologically implausible for COVID-19, where the infectious period is typically 5-10 days. The authors do not flag this as a potential sign of model misspecification (as recommended in Wheeler et al. 2024, POMP checklist #11). Instead, they report only the incubation rate (mu_EI) as consistent with the literature.

---

### 13. No Simulation-Based Diagnostics Beyond Visual Overlay

The simulation plots show 100 forward simulations from MLE parameters overlaid on the data. No conditional log-likelihood plot, no effective sample size plot, and no filtering distribution comparison are presented. The simulation plots show that the Delta model produces simulations with sharper peaks than the data (the data shows prolonged fluctuations), which is a sign of model misspecification. This is acknowledged in the text but not investigated diagnostically.

---

### 14. Omicron Beta Profile Range Does Not Include the Global Search MLE (Different Issue)

For Omicron, the profile spans [100, 500], and the global search MLE was reported as Beta ~ 389. The profile finds its CI in [320, 440]. While this is approximately consistent, the profile maximum is visually around 350-360 (from the description), and the global MLE of 389 is near but not squarely at the profile peak. With only 50 profile points and 15 profile replicates, the profile resolution may be insufficient to precisely locate the MLE (Error 1.9, Minor per course conventions given 50 points at run_level=3).

---

### 15. Grammar and Presentation Issues

The report contains numerous grammatical errors and awkward phrasing throughout: "Comparsion" in the title (misspelling), "paremetrs" (line in global search section), "inapppropriate" (triple p), "statisticly significcant" (conclusion), and "causiosly." These should be corrected before any submission. The EDA section uses `year` as the x-axis variable but labels it "year" when it represents a decimal year — using "week" as the time index would be more informative for a weekly series.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/covid19_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/covid19_paramsomics.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/delta_omicron.csv`
