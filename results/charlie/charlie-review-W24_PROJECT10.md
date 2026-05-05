# Peer Review: W24 Project 10

**Manuscript title:** POMP Analysis on Covid-19 Cases in Malaysia and Influenza in the U.S.

---

## Summary

This project applies a stochastic SEIRV (Susceptible-Exposed-Infectious-Recovered-Vaccinated) compartmental model using the POMP framework to two datasets: weekly COVID-19 cases from Malaysia (2021-2022) and weekly U.S. influenza A cases (2017-2018 season). The COVID-19 analysis is largely presented as a failure demonstration, while the flu analysis proceeds through local search, global search, and a profile likelihood for the vaccination rate parameter mu_SV. The project's strength lies in attempting likelihood-based inference with iterated filtering (IF2) and providing some profile likelihood computation. However, the project suffers from critical flaws: a major bug in the COVID SEIRV process model, hard-coded local file paths that break reproducibility, the absence of any non-mechanistic benchmark comparison, reliance on visual goodness-of-fit with only limited quantitative reporting, and a profile likelihood computation that is incorrectly implemented (profiling over rho rather than mu_SV). These issues collectively undermine the reliability of the reported conclusions.

---

## Major Issues

### 1. Critical bug in the COVID SEIRV Csnippet: dN_RS drawn from I instead of R

In the COVID process model (`seirv_step` Csnippet, lines 222-224 of blinded.Rmd), the transition from Recovered back to Susceptible is drawn as:

```c
double dN_RS = rbinom(I, 1-exp(-mu_RS*dt));
R -= dN_RS;
S += dN_RS;
```

The binomial draw uses compartment `I` (Infectious) as the pool size instead of `R` (Recovered). This is a direct coding error: individuals are being moved from R to S at a rate governed by a draw from the wrong compartment. As a consequence, R can become negative if `dN_RS > R`, and the dynamics of the recovery loop are fundamentally broken. This error is absent in the flu version of the Csnippet (lines 357-370), which omits the RS loop entirely. The COVID model's failure to converge, which the authors attribute to multiple epidemic peaks and viral mutations, may be partly or entirely caused by this bug. The authors fail to detect or acknowledge this coding error. This error must be corrected and the COVID analysis re-run before any conclusions about model fit can be drawn.

### 2. Profile likelihood is computed over rho, not mu_SV

The profile likelihood section is titled "Profile on mu_SV" and is described as evaluating the influence of vaccination rates. However, the guesses data frame used to seed the profile is constructed by grouping on `rho` (line 558: `group_by(cut=round(rho,2))`), not on `mu_SV`. Furthermore, in the `mif2` call within the profile (lines 575-578), `mu_SV` is absent from `rw.sd`, meaning it is held fixed while all other parameters are allowed to move — but the fixed values come from guesses stratified by rho, not by mu_SV. The resulting profile plot (x-axis labeled mu_SV) does not constitute a valid profile likelihood for mu_SV. The 90% confidence interval reported ("roughly 0.08 to 0.12") is therefore unreliable. A correct profile likelihood for mu_SV requires (a) fixing mu_SV at a grid of values, (b) optimizing over all other free parameters at each grid point, and (c) plotting the maximized log-likelihood against the fixed mu_SV values.

### 3. No non-mechanistic benchmark comparison

Neither the COVID nor the flu analysis includes any comparison of the fitted SEIRV model against a non-mechanistic statistical benchmark (e.g., ARMA, negative-binomial autoregression, or seasonal decomposition). Wheeler et al. (2024) note that none of the 32 papers in their Haiti cholera review performed such a comparison, and that their autoregressive negative binomial benchmark revealed that some mechanistic models failed to beat it. Without a benchmark, it is impossible to assess whether the SEIRV model captures meaningful structure beyond what a simpler statistical model would achieve. The authors should compute the log-likelihood of at least one benchmark model on the flu data and compare it to the SEIRV log-likelihood of -306.8.

### 4. Visual-only goodness-of-fit for simulation; no quantitative assessment of model adequacy

For both the COVID and flu simulations, goodness-of-fit is assessed only by visual inspection of simulated trajectories overlaid on observed data. While a log-likelihood value is reported from the optimization (-306.821 for the flu global search), there is no discussion of what this value implies about model adequacy in absolute terms, no comparison to a saturated model, and no AIC reported. Wheeler et al. (2024) explicitly state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The authors should supplement visual plots with quantitative fit diagnostics and discuss whether the achieved log-likelihood represents adequate fit.

### 5. Hard-coded absolute local file paths break reproducibility

The data loading code in lines 118-119 reads:

```r
data_covid <- read.csv("/Users/ganjingrui/Desktop/cases_malaysia.csv")
```

and line 149:

```r
data <- read_csv("/Users/ganjingrui/Desktop/FluData.csv")
```

These are absolute paths to the author's local machine. The code will fail to run on any other machine. Although the flu data is later re-loaded from a GitHub URL (line 380) and the COVID data from a different GitHub URL (line 183), the EDA section uses the hard-coded paths and produces the ACF and time series plots shown early in the document. This inconsistency means the EDA figures cannot be reproduced from the published code without access to the author's local files. All file paths should use relative paths or public URLs.

### 6. Flu SEIRV model omits the R->S loop that motivates the model

The authors justify the SEIRV model extension with the RS loop (lines 53-57) by citing evidence that recovered individuals can be reinfected by COVID-19 and influenza. However, the flu Csnippet (lines 357-370) does not include the `dN_RS` transition — the R->S pathway is simply absent. The parameter `mu_RS` is still included in `paramnames` and estimated in both local and global searches, but it has no effect on the flu model dynamics because it is not referenced in the Csnippet. This is both a modeling inconsistency (the stated motivation for the model applies to flu yet the flu model ignores it) and a potential identifiability problem, as `mu_RS` is being estimated while playing no role in the likelihood.

### 7. Insufficient evidence of global search convergence

The global search uses 100 starting points with `Nmif=100` followed by `mif2(Nmif=50)`. The authors do not show convergence traces (log-likelihood as a function of iteration) for the global search, only the pairs plot of parameter estimates versus log-likelihood. The pairs plot itself shows that the `Beta~loglik`, `mu_EI~loglik`, and `mu_IR~loglik` relationships "did not clearly show a trend of convergence" (line 542), yet the authors proceed to treat the global search maximum as the MLE. Wheeler et al. (2024) note that insufficient computational effort is a primary reason for poor optimization results. The number of particles used for final likelihood evaluation (Np=5000 with 10 replicates) produces a standard error of 0.031, which is acceptable, but the optimization traces themselves should be shown and convergence formally assessed before accepting the reported maximum as the MLE.

### 8. Cooling fraction and rw.sd magnitudes suggest poor optimization geometry

The local search uses `rw.sd` values equal to the parameter values themselves (e.g., `Beta=2` for a parameter of order 2, `mu_EI=0.25` for a parameter of order 0.25). These perturbation standard deviations on the transformed scale are extremely large. The global search then reduces `rw.sd` to 0.002, which is extremely small. Neither setting is justified, and the dramatic change between local and global search settings is unexplained. The authors acknowledge in the conclusion (line 623) that "we intentionally make values in rw.sd much smaller because we found the results are more sensitive to the change of parameters," but do not discuss the implications for whether the local search is actually exploring the parameter space meaningfully. Poor `rw.sd` calibration can prevent IF2 from converging to the MLE regardless of computational effort.

---

## Minor Issues

- **Duplicate reference numbers:** References 4 and 6 are identical URLs (lines 629, 633: both point to `https://www.cdc.gov/coronavirus/2019-ncov/your-health/reinfection.html`). One should be removed.

- **Typographic errors:** Section 3 heading reads "Methodlogy" (line 35). Line 288 contains a stray period mid-sentence ("our model might not have. a good performance").

- **N population size for flu model is unjustified:** The flu SEIRV model uses `N=1000000` (1 million) as the total population, but the US population susceptible to influenza is orders of magnitude larger. The authors do not justify this choice or discuss whether it interacts with the reporting rate parameter `rho` and the absolute case counts from the CDC surveillance data. The effective population size and its relationship to the surveillance data scale should be explicitly discussed.

- **`mu_RS` estimated but inactive in flu model:** As noted in Major Issue 6, `mu_RS` appears in `paramnames` and is estimated in optimization but has no effect on flu model dynamics. The reported global search estimate for `mu_RS` is meaningless. The table in line 545 should not report `mu_RS` as an estimated parameter for the flu model.

- **No `sessionInfo()` or package version information:** The analysis uses `pomp`, `foreach`, `doFuture`, `doParallel`, `doRNG`, and other packages without specifying version numbers. The `pomp` API has changed substantially across versions. Per the code supplement checklist, package versions should be pinned (e.g., via `renv`) for reproducibility.

- **Profile confidence interval uses 90% level without justification:** The authors compute a 90% CI for mu_SV (line 614: `qchisq(df=1, p=0.90)`) without justifying this non-standard choice. The conventional level is 95%. No explanation is given for using 90%.

- **COVID model analysis is abandoned without attempting model improvement:** The authors conclude that the SEIRV model failed on COVID data and shift focus to flu data, but they do not attempt any model modifications (e.g., time-varying Beta, variant indicators, or a simpler SEIR without vaccination) to better understand the failure. Given the bug identified in Major Issue 1, it is unclear whether the failure is methodological or computational.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project10/blinded.Rmd`
