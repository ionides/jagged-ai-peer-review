# Peer Review: POMP Model for Ebola in Guinea and Sierra Leone (W22 Project 02)

## Summary

This project models the 2014-2016 Ebola outbreak in Guinea and Sierra Leone using a SEIRDF (Susceptible-Exposed-Infected-Recovered-Dead-Funeral) POMP model. The authors implement iterated filtering (IF2) for parameter estimation and compute profile likelihoods for the transmission rate Beta in both countries. The core research question is whether the two countries share similar transmission rates. The project has notable methodological and implementation weaknesses that undermine confidence in the conclusions.

---

## Weaknesses (Prioritized, Most Critical First)

### 1. [MAJOR] Measurement Model Fundamentally Misspecified: H is Cumulative, Not Daily

The dmeas and rmeas snippets use the accumulator variable `H` (total infections over time, reset each observation period) directly as the size parameter in a Binomial distribution: `lik = dbinom(reports, H, rho, FALSE)` and `reports = rbinom(H, rho)`. The model uses `accumvars="H"`, which resets H at each observation time so that H represents the flow of new infections in each time period. This is a plausible choice, but the observation model implicitly assumes `reports` is a Binomial draw from `H` infections, with `H >= reports` required always. This interpretation is reasonable, but the dmeas assigns likelihood `tol` (essentially zero, i.e., `1e-25`) whenever `reports == 0` OR `H == 0`, discarding valid zero-count observations. If there are any time points with zero reported cases that are not accompanied by zero modeled infections, those observations are handled incorrectly, which can systematically distort parameter estimates.

### 2. [MAJOR] Wrong Population Size Used for Sierra Leone

The Sierra Leone simulation and searches use `N=6190280`, but the text states the correct population is `N=16190280`. This is a factor-of-almost-3 error in total population size. The stated population (`16190280`) appears in the model introduction but not in the code. The Sierra Leone R script (`SL_SEIRF.R`) and Rmd code both use `N=6190280`, which is approximately 6.2 million, not 16.2 million. All parameter estimates, initial values, and R0-related interpretations for Sierra Leone are based on an incorrect population and are therefore unreliable.

Evidence:
- blinded.Rmd line 466: `params <- c(Beta=20, Beta2=1, mu_EI=12,mu_IR=2,mu_DF=1,F_size=50,rho=0.3,eta=0.025,N=6190280)`
- blinded.Rmd line 489: `params <- c(...,N=6190280)`
- blinded.Rmd line 546: `fixed_params = c(F_size=50, N=6190280)`
- The text says "N=16190280" in the Guinea introduction section but the SL section never states the intended correct population.

### 3. [MAJOR] Profile Likelihood for Beta Not Constructed Correctly -- Beta Is Not Fixed

A proper profile likelihood requires fixing the profiled parameter (Beta) at a grid of values and maximizing over all other parameters. In the code, the profile search (`beta_GU.rds`, `beta_SL.rds`) omits `Beta` from the `rw.sd` argument, which prevents IF2 from perturbing Beta. However, IF2 still re-uses the initial Beta from each guess row (drawn uniformly from [3,7]), but there is no guarantee each run converges to the MLE conditional on that specific Beta value. This is a guess-based sweep rather than a properly constrained profile. In particular, using the same random starting guesses from `runif_design` as in the global search (rather than a grid of fixed Beta values) means the profile is not a true profile likelihood but rather a scatter of global search results, re-analyzed with Beta free only in initialization. The conclusions about identifiability of Beta drawn from this analysis may be unreliable.

### 4. [MAJOR] Funeral Compartment F Modeled as Flow, Not a Stock

In the process model, `F = round(dN_DF)` replaces F entirely each step rather than accumulating. This makes F represent the number of new funerals occurring in each time step dt, not a standing pool of ongoing funerals at which transmission occurs. The force of infection from funerals is `Beta2 * F_size * F / F_size = Beta2 * F`, which is proportional to the number of new funerals in the current step. If funerals represent ongoing risky events rather than a daily instantaneous count, they should carry over across time steps. The current implementation means there is no memory in the funeral compartment, which is epidemiologically inconsistent with the Weitz-Dushoff formulation cited in the paper.

### 5. [MAJOR] Death Rate Hardcoded at Exactly 50% with Deterministic Rounding

The model splits `dN_IR` into recovered and dead using deterministic rounding (`R += round(dN_IR/2); D += round(dN_IR/2)`), fixing the case fatality rate at exactly 50% with no stochasticity. Actual Ebola CFR varied by country and time. Setting this as a fixed constant eliminates the ability to estimate or fit the CFR as a parameter, reducing model flexibility and realism. The rounding also means that odd values of `dN_IR` result in `R` and `D` each increasing by `floor(dN_IR/2)`, so one infection per step is lost from the state space, introducing a systematic conservation-of-population error.

### 6. [MAJOR] R0 Not Computed or Discussed

The project never computes R0, the basic reproduction number, which is arguably the most important summary of epidemic transmission dynamics. The Weitz-Dushoff paper that inspired the SEIRDF extension is specifically about R0 estimation, and the authors mention that standard models without D and F "underestimated the basic reproduction number R0." Yet no R0 formula is derived for the SEIRDF model, no estimates are reported, and no comparison with the literature is provided. This is a major gap in substantive scientific output.

### 7. [MAJOR] mu_EI Parameter Value Is Epidemiologically Implausible

The initial guess for `mu_EI` (the rate of leaving the exposed state) is 15, which with daily time steps implies a mean incubation period of `1/15 ≈ 0.067` days, or about 1.6 hours. The literature-established mean incubation period for Ebola is approximately 8-12 days, corresponding to `mu_EI ≈ 0.083 to 0.125`. The fitted values from the global search (e.g., around 14.9 from `Guinea_params.csv`) similarly imply sub-day incubation periods that are biologically impossible. The parameter search range of [10, 20] for `mu_EI` covers only biologically impossible values. This suggests a fundamental unit confusion where the authors may have intended the mean incubation period (in days) rather than the rate.

### 8. [MAJOR] mu_IR Similarly Implausible

Analogously, the global search range for `mu_IR` is [0.7, 1.2], and fitted values are around 0.95. This implies a mean duration of infectious period of `1/0.95 ≈ 1.05` days. The Ebola infectious period is typically 5-10 days. Like `mu_EI`, the parameter values suggest a unit error where durations (in days) are being used where rates are needed.

### 9. [MODERATE] Search Box for Global Search Is Inconsistent with Initial Simulation Parameters

The initial simulation for Guinea uses `Beta=17`, `mu_EI=15`, `mu_IR=1.5`, but the global search box is `Beta in [3,7]`, `mu_EI in [10,20]`, `mu_IR in [0.7,1.2]`. The initial guesses are partially outside the global search box (Beta=17 >> 7). This inconsistency is not explained. If the simulation with Beta=17 appeared visually reasonable, then restricting global search to Beta in [3,7] is not justified by either the simulation or the local search results, and the resulting conclusion that Beta near 5 is optimal may simply reflect the choice of search box.

### 10. [MODERATE] F_size Fixed and Not Estimated

`F_size` (funeral size) is fixed at 50 for both countries and is not estimated. It appears in the log transform in `partrans`, implying the authors considered it estimable, but then it is fixed at 50 in both local and global searches without justification. The sensitivity of results to this assumption is not explored. Funeral sizes are variable across West Africa and could plausibly differ between Guinea and Sierra Leone.

### 11. [MODERATE] Profile Likelihood for Beta Spans the Entire Search Box, Indicating Non-Identifiability That Is Not Adequately Addressed

The reported 95% confidence interval for Beta in Guinea is approximately [3.003, 6.974], which is nearly the entire search box [3, 7]. The authors acknowledge this indicates "weak identifiability" but do not investigate further, do not attempt to profile other parameters, and proceed to compare the two countries on the basis of Beta despite it being essentially unidentifiable. The conclusion that "transmission rates are similar" in the two countries is thus unfounded.

### 12. [MODERATE] bake() Called Twice for Same File With Different Code Blocks

In the Guinea section, `bake(file="lik_local_GU.rds", ...)` is called twice (lines 238-246 and 260-268), with slightly different variable names for the output (`local_logliks` vs. `results`). The second call will return the cached result from the first call but assign it to `results`. This is redundant and potentially confusing but not incorrect if the second call uses the cached file. It does not affect the analysis but signals poor code organization.

### 13. [MODERATE] No Convergence Diagnostics Presented for Global Search

The trace plots (convergence diagnostics) are shown only for the local search. For the global search, only pairs plots of the loglik surface are presented, with no trace plots showing whether the MIF2 runs converged over iterations. Convergence of the global search iterated filtering runs cannot be assessed from the pairs plots alone.

### 14. [MINOR] EDA Is Superficial and Does Not Inform Model Choice

The EDA section presents a single time-series plot for each country and notes that "cases peaked around day 25." No spectral analysis, autocorrelation analysis, or comparison with other published Ebola data analyses is performed. The EDA does not examine the relationship between reported cases and deaths, which would be relevant given the SEIRDF model motivation. The EDA does not motivate specific parameter ranges used in the model.

### 15. [MINOR] Conclusions Attribute Same CI to Both Countries Due to Same Search Box

The authors correctly note: "This exact same confidence interval of the two countries may not seem convincing, but this is because we set the same lower and upper bounds and same number of evened space for global search." This self-refutation of the main conclusion is appropriate disclosure but also means the core research finding -- that Guinea and Sierra Leone have similar transmission rates -- is entirely an artifact of the experimental design rather than a substantive finding. The authors do not propose any remediation.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/Guinea_SEIRF.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/SL_SEIRF.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/EDA.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/Gu.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/SL.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/Guinea_params.csv`
