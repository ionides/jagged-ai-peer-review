# Peer Review: W22 Project 13 — "An Analysis of Omicron Variant COVID Cases in California and Texas"

---

## Summary

This project fits an SEIR POMP model to daily confirmed COVID-19 case counts for California and Texas during the Omicron wave (December 2021 – March 2022). The authors use a time-varying contact rate governed by a policy-based step function, fix the epidemiological rate parameters, and estimate the remaining parameters via iterated filtering. Both a local and a global search are performed, and a profile likelihood curve for the reporting rate is presented. The project is ambitious in scope but has a number of significant methodological, reporting, and model-specification weaknesses described below.

---

## Weaknesses (prioritized by severity)

### 1. [Major] Global search code is entirely absent from the Rmd

The writeup reads `writeup_params.csv` and `writeup_params_texas.csv` directly without including the code that produced them. No `bake()` call, no `foreach` loop over `guesses`, and no `mif2` call appears for the global search step. This means the analysis is not reproducible from the submitted Rmd alone, and readers cannot verify the number of particles, the number of MIF iterations, the cooling schedule, or the random seed used for the global search. This is the most serious reproducibility failure in the project.

### 2. [Major] Profile likelihood procedure is not a genuine profile likelihood

The section labeled "Profile likelihood for the reporting rate" does not fix rho and re-optimize all other parameters at each fixed value. Instead, it filters the global search results by rho value and plots whatever likelihood values happened to be found in those runs. This is an approximation at best and can systematically underestimate the profile likelihood, yielding confidence intervals that are too narrow or misshapen. A proper profile likelihood requires fixing rho at a grid of values and running MIF from multiple starting points at each grid point to maximize over all remaining parameters.

### 3. [Major] Measurement model contains an unexplained fixed scaling factor of 14

The `dmeas` and `rmeas` Csnippets multiply both the mean and standard deviation of the observation distribution by 14 (`14*rho*H` and `14*sqrt(tau*rho*H*(1-rho))`). The writeup mentions a "fixed scaling parameter phi" and sets phi=14 in a code comment, but never explains where this value comes from, why 14 was chosen, or whether it was estimated or hand-tuned. A factor of 14 in the mean is very large and suggests a fundamental mismatch between the accumulator variable H and the observed case count. This issue deserves explicit justification.

### 4. [Major] The accumulator variable H is not reset between observation times

The SEIR process adds individuals from I to R via `H += dN_IR`, and H is listed as an `accumvars` entry, which should cause it to be reset to zero after each measurement. However, the measurement model scales by `14*rho*H`, suggesting that H is intended to accumulate over 14 days (a two-week window) rather than one day. But if H is declared as an `accumvars`, pomp resets it to zero after each time step of length 1. The factor of 14 and the accumvars declaration appear to be in direct conceptual conflict: either H accumulates over 14 steps (in which case `accumvars` should not include it, or delta.t should be 1/14), or it is reset each step (in which case the factor of 14 inflates the mean without justification). This inconsistency is not addressed anywhere in the writeup.

### 5. [Major] The force of infection formula in the transition probability is missing the negative sign

In the mathematical specification (lines 120-122), the S-to-E transition probability is written as:
`Delta N_SE ~ Binomial(S, 1 - exp(beta * (1/N) * Delta_t))`
The exponent is missing the leading minus sign that should appear before beta. The correct expression is `1 - exp(-beta * I/N * Delta_t)`. The code itself is correct (`1 - exp(-Beta * I / N * dt)`), so this is a typo in the mathematical write-up, but it is a noticeable error that undermines confidence in the exposition.

### 6. [Major] run_level is set to 1 (smallest computation settings) in the submitted Rmd

`run_level = 1` gives `NP = 50` particles, `NMIF_S = 5` filtering iterations, `NREPS_EVAL = 5`, `NREPS_LOCAL = 10`, and `NSTART = 50` starting points. These are far too small for any meaningful inference. The saved CSV files were presumably generated at a higher run level, but since the global search code is absent (see Issue 1), this cannot be confirmed. If a reader knits the Rmd as submitted, the local search will run with only 50 particles and 5 MIF iterations, which is insufficient to approach the likelihood surface reliably.

### 7. [Major] No diagnostic check that MIF has converged

Neither the local nor the global search includes a diagnostic to verify algorithmic convergence. The local search trace plots are described qualitatively ("the likelihood is increasing for all the runs"), but no convergence criterion is stated, and the run length is only 5–10 MIF iterations at run_level 1. For the global search, there is no convergence trace at all because the code to produce it is absent. Good practice requires showing that the log-likelihood stabilizes across MIF iterations and that multiple starting points cluster near the same MLE.

### 8. [Major] Texas params_rw.sd includes b3 and b4 which do not exist in the Texas model

At line 375, the Texas `params_rw.sd` is defined as:
`rw.sd(b1 = 0.01, b2 = 0.01, b3 = 0.01, b4 = 0.01, rho = 0.01, tau = 0.0001, eta = ivp(0.01))`
However, the Texas SEIR model only has parameters b1 and b2. Including b3 and b4 in the random walk standard deviations for a pomp object that does not have those parameters will either cause an error or be silently ignored, but it indicates the Texas code was carelessly adapted from the California code without proper verification.

### 9. [Moderate] The "profile likelihood" for Texas is built from global search results, not a dedicated profile search, yet the CI is interpreted as if it were valid

The text states: "The 95% CI for the Texas reporting rate comes out to be between [min] and [max] which is a much smaller (and lower) interval as compared to California." From the Texas global search CSV, rho values cluster tightly around 0.10, while California rho values cluster around 0.25. Rather than interpreting this as a genuine epidemiological finding, the authors attribute it to the lack of mask mandates in Texas, but the narrow CI is more likely an artifact of the global search not exploring the rho parameter space adequately (since rho reached a boundary of the search space). No investigation of whether the search space was wide enough is performed.

### 10. [Moderate] Initial conditions for S are parametrized via eta but the justification is inconsistent

The initial susceptible population is `S = nearbyint(eta * N)`, implying that only a fraction eta of the total population is susceptible. The starting value eta = 0.01 means only 1% of the population (~395,000 for California) is initially susceptible, which is inconsistent with the stated assumption in the text that "the entire state population, except for those exposed in the last 90 days, are susceptible." If nearly the entire population is susceptible, eta should be close to 1, not 0.01. In the MLE results, eta converges to approximately 0.028, meaning only ~2.8% of 39.5 million people (~1.1 million) are susceptible, which seems too low. The discrepancy between the stated assumption and the parametrization is not reconciled.

### 11. [Moderate] No ARIMA or other benchmark likelihood is computed for comparison

The conclusion acknowledges this omission: "we decided to compare pomp models and did not develop a likelihood baseline nor perform extensive diagnostics. Using an ARIMA model as a baseline would have yielded a stronger analysis." The absence of a benchmark makes it impossible to assess whether the SEIR POMP model achieves a meaningful improvement over a naive time-series model. The authors recognize this weakness but do not address it.

### 12. [Moderate] b4 (the contact rate in the final interval for California) is implausibly large and unstable

The initial value for b4 is 2000, and the global search upper bound for b4 is 3000, while the MLE converges to approximately b4 ≈ 220. This is a large reduction from the starting value, which may indicate that the search was poorly initialized and that the local search required a very large number of iterations to find a sensible region. The fact that b4 starts at 2000 while the MLE is ~220 also raises a question about whether the local search actually converged or merely moved toward a better region of parameter space without reaching it.

### 13. [Moderate] Reporting rate rho is described inconsistently in the model specification

The text states: "The probability of a case being reported is rho, which happens between the stage E and I." However, in the actual model H accumulates transitions from I to R (not from E to I), and the observation model measures rho * H. The description "between stage E and I" is incorrect for this implementation, where detection is linked to the I-to-R transition, not the E-to-I transition. This mislabeling of where in the disease progression detection occurs creates confusion about the model's meaning.

### 14. [Minor] The data subsetting uses strict inequality (">") on both date endpoints

At line 133, the data are filtered as:
`filter(date > as.Date("2021-12-01") & date < as.Date("2022-03-01"))`
This excludes December 1, 2021 and March 1, 2022 themselves. The text claims the analysis covers "12/01/2021 to 03/01/2022 (89 days)" but the strict inequality may cause the actual dataset to be slightly shorter than claimed. The exact number of observations is not confirmed in the writeup.

### 15. [Minor] The covariate table interval lengths do not sum to the same total for both states, and are not explicitly verified

For California, the covariate intervals are `rep(1,14), rep(2,13), rep(3,49), rep(4,13)` which sum to 89. For Texas, they are `rep(1,27), rep(2,62)` which also sum to 89. These counts are hardcoded and assumed to match the actual data length, but no assertion or check is made in the code to confirm that the number of time steps in the data equals 89. If the data filtering produces a different number of rows (e.g., due to missing values or the strict inequality noted above), the covariate table lengths would be misaligned, leading to silent errors in the model.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project13/writeup_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project13/writeup_params_texas.csv`
