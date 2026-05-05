# Peer Review: W21 Project 02
# "Study of daily COVID-19 Infected cases in the United States"

---

## Summary

This project attempts to model daily COVID-19 confirmed infection counts in the United States (January 22, 2020 – April 10, 2021) using three POMP-based compartmental models: SEIR, SECSDR, and SEIQR. While the ambition to compare multiple model structures is commendable, the project has pervasive methodological deficiencies that undermine every substantive conclusion. The issues below are ordered from most critical to least critical.

---

## Weaknesses

### 1. [MAJOR] Measurement model for SEIR uses a degenerate normal distribution

In the SEIR `dmeas` snippet, the standard deviation of the normal approximation is set equal to the mean (`sd_cases = sqrt(mean_cases*mean_cases)`, which simplifies to `sd_cases = mean_cases`). This collapses the coefficient of variation to exactly 1 and is not a standard epidemiological measurement model. The conventional choice — negative-binomial with overdispersion parameter `tau`, or at minimum a normal with `sd = sqrt(rho*H*(1-rho)*N)` — is absent. The parameter `tau` is declared and log-transformed in `partrans`, but it appears nowhere in either `dmeas` or `rmeas`, rendering it a phantom parameter that wastes a dimension of the parameter space and misleads any likelihood surface interpretation.

### 2. [MAJOR] SECSDR rprocess contains an illegal double-deduction from Ca

In the SECSDR process model the code draws `dN_CaR ~ Binomial(Ca, ...)` and then draws `dN_CaSy ~ Binomial(Ca - dN_CaR, ...)`. This subtraction is only valid if `Ca - dN_CaR >= 0` at every particle, which is not guaranteed when particles have very small Ca counts. More importantly, the subsequent state update `Ca += dN_ECa - dN_CaSy - dN_CaR` deducts both outflows, which is consistent with the sequential binomial draws — however, the exposure transition is also wrong: `dN_SE` is drawn from S but `dN_ECa` (which is a second binomial draw conditional on `dN_SE`) is what is added to Ca, while S is only decremented by `dN_ECa`, not by `dN_SE`. This means exposed individuals that do not progress to Ca in that step disappear from S without entering E, violating population conservation. There is no E compartment in the state equation update, so individuals lost to `dN_SE - dN_ECa` vanish entirely.

### 3. [MAJOR] SEIQR measurement model links Q (quarantined) to observed infections, not to new diagnoses

Observed daily confirmed cases represent new positive tests, not the number of currently quarantined individuals. Mapping `Infected ~ Normal(Q, ...)` confounds a stock (cumulative quarantine pool) with a flow (daily new cases). This means the measurement equation is dimensionally inconsistent with the data and will systematically overestimate the observed series as Q grows.

### 4. [MAJOR] Cooling fraction and random walk SD for SECSDR and SEIQR mif2 are set to essentially zero

Both SECSDR and SEIQR global searches use `covid_cooling.fraction.50 = 0.00005` and `covid_rw.sd = 0.000000002`. These values are effectively zero: the iterated filter cannot explore the parameter space, and the "optimization" is indistinguishable from evaluating the likelihood at the initial random draw. This invalidates all global-search results and conclusions drawn from them. The author correctly identifies poor fits but does not recognize that the optimizer was never actually searching.

### 5. [MAJOR] SEIQR N is set to 32,000,000 rather than the US population (~328,000,000)

The fixed population parameter for SEIQR is `N = 32000000`, exactly one tenth of the US population, while the SECSDR model and the data context both refer to approximately 328 million people. No justification is provided. This makes SEIQR's dynamics inconsistent with the US context and results in parameters that cannot be compared with the other models.

### 6. [MAJOR] No local search is performed for SECSDR or SEIQR

The project conducts a local search only for SEIR. For SECSDR and SEIQR the workflow jumps directly to a global search (which is itself broken, as noted in weakness 4). Without a local search phase, there is no convergence diagnostic to assess whether mif2 trajectories stabilize, and the iterated filtering chain cannot be verified to have reached a neighborhood of the MLE before evaluation.

### 7. [MAJOR] No likelihood comparison across the three models

The project presents three models but never compares their log-likelihoods on a common scale. Without a table showing best log-likelihood (and standard error) per model — or an AIC comparison — there is no statistical basis for any claim about which model performs best or worst. The conclusion that "all three models fail" relies purely on visual inspection.

### 8. [MAJOR] Data file is missing and reproducibility is broken

The Rmd reads `worse_hospitalization_all_locs.csv`, which is not present in the project directory. None of the other files in the directory substitute for this raw data file. The code cannot be run from scratch, and the provenance of the pre-computed `.rda`/`.rds` files cannot be independently verified. The IHME data source is mentioned in the text but no download link or data version is documented.

### 9. [MINOR] SEIR local search random walk omits mu_EI and mu_IR

The local search `rw.sd` specification is `rw.sd(Beta=0.002, rho=0.002, eta=ivp(0.002))`, leaving `mu_EI` and `mu_IR` fixed at their starting values. These are biologically meaningful rate parameters (mean latent period and mean infectious period), and not allowing them to be optimized produces a severely constrained local search that is unlikely to reach a true MLE.

### 10. [MINOR] SEIR simulation uses hard-coded parameters inconsistent with the global MLE

Section 3.4 simulates using manually specified parameters (`Beta=1.470177`, etc.) taken from the global search result, but these are embedded as literals in the code rather than extracted programmatically from the saved results object. This makes verification fragile and inconsistent with the workflow that retrieved `cov_global_mle` in the previous chunk.

### 11. [MINOR] SEIR measurement model applies a continuity-corrected normal but the rmeas uses a different model

The `dmeas` applies a continuity-corrected normal approximation (`pnorm(Infected, ...) - pnorm(Infected-0.5, ...)`), while `rmeas` draws directly from `rnorm(rho*H, sqrt(rho*H))`. These two are not conjugate representations of the same distribution: `dmeas` uses `sd = mean_cases` (i.e., `rho*H`) while `rmeas` uses `sd = sqrt(rho*H)`. This inconsistency between the generative model and the evaluation model will bias particle weights and produce unreliable likelihood estimates.

### 12. [MINOR] run_level = 1 (toy-level computation) for SECSDR global search

The SECSDR section sets `run_level <- 1`, which corresponds to `covid_Np=100; covid_Nmif=10; covid_Nglobal=10`. With only 10 mif2 iterations and 100 particles, the filter is far too noisy to produce reliable likelihood estimates or meaningful convergence diagnostics. This is a pilot-level run, not a publishable analysis.

### 13. [MINOR] SECSDR rinit uses hard-coded population sizes inconsistent with parameter estimation

The SECSDR initial conditions are hard-coded as `S=328000000; Ca=10; Sy=10; Di=1; R=0` but these are not connected to any parameter (there is no `eta` or equivalent). Consequently there is no mechanism for the optimizer to adjust the initial susceptible fraction, and any parameter transformation that changes effective population size will still use a fixed initial state. For a long epidemic time series spanning over a year this is a significant source of model misspecification.

### 14. [MINOR] Profile likelihood and confidence intervals are absent for all three models

No profile likelihood plots are produced for any parameter in any of the three models. Without profiling, there is no way to assess parameter identifiability, nor to construct confidence intervals for quantities of interest (e.g., R0, mean latent period). The pairs plots shown for SEIR do not substitute for proper likelihood profiles.

### 15. [MINOR] Introduction and background contain no quantitative epidemiological motivation

The introduction cites the global case count as of April 19, 2021 but does not provide any epidemiological motivation for the choice of model structures. Key quantities such as the basic reproduction number R0, the incubation period, or the infectious period for COVID-19 from the literature are never cited or used to set plausible prior ranges for parameters, making the initial parameter guesses appear arbitrary.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project02/blinded.Rmd`
