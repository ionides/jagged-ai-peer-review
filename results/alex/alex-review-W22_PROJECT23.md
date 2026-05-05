# Peer Review: W22 Project 23
## COVID-19 POMP Modeling for New York City (SIR / SEIR / SEIQR)

---

### Summary

This project models the Omicron-variant wave in New York City (December 4, 2021 to February 1, 2022) using three POMP compartmental models: SIR, SEIR, and SEIQR. The authors fit each model with local and global iterated filtering (IF2) and compare the resulting log-likelihoods to select a preferred model. The SEIQR model is declared best. The project shows familiarity with the pomp workflow but contains several serious methodological and implementation errors that undermine the validity of the conclusions.

---

## Major Weaknesses

### 1. Non-comparable log-likelihoods across models due to different measurement distributions

The SEIQR model uses a Normal measurement model (`dnorm(pos, Q, rho*Q + 1e-10, give_log)`) while SIR and SEIR use a Binomial measurement model (`dbinom(pos, H, rho, give_log)`). These two distributions have different supports and normalizing constants, so the resulting log-likelihood values are on incompatible scales. The SEIQR log-likelihoods (~-602) cannot be meaningfully compared to SIR log-likelihoods (~-50,126) or SEIR log-likelihoods (~-85,131) to conclude that SEIQR is the best-fitting model. The central conclusion of the paper rests on this flawed comparison.

**Evidence:** `blinded.Rmd` lines 122-127 (SIR: `dbinom`), lines 351-357 (SEIR: `dbinom`), lines 563-571 (SEIQR: `dnorm`).

---

### 2. SEIQR force-of-infection is missing the population scaling term N

In the SIR and SEIR models the infection rate is correctly specified as `Beta*I/N*dt` (frequency-dependent transmission). In the SEIQR model, the analogous term is `Beta*I*dt` (density-dependent), with no division by N. For a population of N = 1,886,700 this inflates the transmission rate by a factor of nearly two million, making the Beta parameter estimates incomparable across models and potentially causing numerical instability.

**Evidence:** `blinded.Rmd` line 106 (`Beta*I/N`), line 332 (`Beta*I/N`), line 551 (`Beta*I*dt` — missing `/N`).

---

### 3. SEIQR measurement model observes Q (quarantined), not new cases

The SEIQR process model never adds an accumulator variable analogous to H. Instead, observations are drawn directly from the current stock Q: `pos ~ Normal(Q, rho*Q)`. This means the model is comparing the daily count of new reported positives to the level of the quarantine compartment on each day, which is a state stock rather than a flow. This is epidemiologically inappropriate and leads to a fundamentally different likelihood surface from the SIR/SEIR models, further invalidating the cross-model comparison.

**Evidence:** `blinded.Rmd` lines 550-570: no H accumulator is defined or incremented, and `seiqr_dmea` conditions on Q directly.

---

### 4. SEIR model uses delta.t = 7 (weekly steps) while data are daily

The SEIR pomp object is constructed with `euler(seir_step, delta.t=7)`, meaning the Euler integration advances in seven-day steps, yet the observed data are daily (time = 1, 2, ..., 59). With a weekly step size, the accumulator H counts flows over an entire week but is compared to a single day's reported cases. This mismatch between integration step and observation frequency inflates the modeled daily counts and distorts parameter estimates.

**Evidence:** `blinded.Rmd` line 364: `rprocess=euler(seir_step, delta.t=7)`. SIR uses `delta.t=1` (line 134) and SEIQR uses `delta.t=1` (line 592).

---

### 5. SEIR likelihood surface pairs plot incorrectly uses SIR data

The pairs plot for the SEIR local search likelihood surface is generated with `data=sir_lik_local` instead of `data=seir_lik_local`. This means the SEIR section displays the SIR likelihood surface, providing no diagnostic information about SEIR parameter identifiability.

**Evidence:** `blinded.Rmd` line 464: `pairs(~loglik+Beta+mu_IR+eta+rho, data=sir_lik_local, pch=16)`. The correct object would be `seir_lik_local`.

---

### 6. Inconsistent parameter transformations between pomp object and mif2 call for SEIR

The SEIR pomp object declares `partrans=parameter_trans(log=c("Beta","mu_EI","mu_IR"), logit=c("rho","eta"))`, but the mif2 call inside the local search overrides this with `partrans=parameter_trans(log=c("Beta","mu_EI"), logit=c("rho","eta"))`, omitting `mu_IR` from log-transformation. This inconsistency means mu_IR is searched on the untransformed scale during local search but interpreted on the log-transformed scale when the resulting parameters are used downstream (e.g., in `pfilter` calls that use the object's stored transformation).

**Evidence:** `blinded.Rmd` lines 369-371 vs. lines 427-429.

---

### 7. SEIQR partrans applies log-transform to rho and eta instead of logit

The SEIQR pomp object uses `partrans=parameter_trans(log=c("Beta","mu_I","mu_R1","mu_R2","eta","rho"))`, applying a log transformation to both rho and eta. However, rho and eta are proportions bounded in [0, 1] and should receive a logit transformation as in the SIR and SEIR objects. The log transform allows these parameters to take values greater than 1 during optimization, producing nonsensical probability values.

**Evidence:** `blinded.Rmd` line 596 (pomp object) versus lines 141, 371 (SIR and SEIR use `logit=c("rho","eta")`). The mif2 local-search call at line 646 correctly applies logit to rho and eta, creating yet another internal inconsistency with the stored pomp object.

---

### 8. Global search for SIR uses sequential (%do%) instead of parallel (%dopar%) execution

The global search for SIR is implemented with `%do%` (sequential foreach) rather than `%dopar%` (parallel), while the global searches for SEIR and SEIQR also use `%do%`. Only the local searches and initial pfilter evaluations use `%dopar%`. Given that 100 random starting points are drawn and each requires two mif2 passes plus 10 pfilter evaluations, sequential execution is computationally wasteful and may indicate that the searches were run with a shorter time budget than intended.

**Evidence:** `blinded.Rmd` line 280 (`%do%`), line 499 (`%do%`), line 723 (`%do%`).

---

### 9. No profile likelihood or confidence intervals are computed

The project reports point estimates from global search but provides no profile likelihoods, confidence intervals, or any other measure of parameter uncertainty. Without these, it is impossible to assess whether individual parameters are well-identified or to make valid inferential statements about transmission rates, recovery rates, or reporting rates.

---

### 10. Population figure is inconsistent and likely incorrect

The introduction states "New York City, which has a population size of roughly 18 million," yet the code consistently uses N = 1,886,700 (approximately 1.9 million). The cited source refers to the "metro area" population, not the city's administrative population. New York City's five-borough population is approximately 8.3 million. The stated 18 million figure is wrong, and the 1.9 million used in the code is also substantially below the actual city population. This error has direct implications for the susceptible fraction eta (e.g., SIR/SEIR MLEs find eta near 0.95-0.99, which at N=1.9M implies nearly all 1.9M are susceptible, not 8.3M) and for the force-of-infection term.

**Evidence:** `blinded.Rmd` line 30 ("18 million"), line 150 (`pop = 1886700`), reference [3] links to metro area data.

---

### 11. SIR global search finds a worse MLE than local search

The SIR local search achieves a best log-likelihood of -50,126 while the SIR global search best is -56,544. It is expected that a global search exploring a wider parameter space should find at least as good a solution as a local search. The reversal suggests that the global search ranges (Beta in [1,10], mu_IR in [0,7], eta in [0.4,0.6]) exclude the region where the local search converged (eta near 0.95), so the global search is searching in an uninformative region. The authors note this anomaly but do not explain or resolve it.

**Evidence:** HTML output: local search best = -50,126.19; global search best = -56,543.52. SEIR exhibits the same pattern (-85,891 local vs. -85,131 global — only marginally better).

---

### 12. No model diagnostic checks (simulated vs. observed quantile comparison or residual analysis)

Beyond visual inspection of simulated trajectories, the project performs no quantitative model diagnostics — no simulation-based coverage checks, no examination of particle filter effective sample sizes, and no assessment of filter degeneracy. The absence of diagnostics makes it unclear whether the particle filter is operating reliably, especially given the large log-likelihood values and high particle counts required.

---

### 13. Text states mu_IR = 0.1 as initial value but code uses 0.27

In Section 4 (SIR Model) the text says the initial parameters include `mu_IR=0.1`, but the actual code sets `sir_params=c(Beta=0.48, mu_IR=0.27, ...)`. This discrepancy between stated and implemented initial values is not explained and reduces reproducibility.

**Evidence:** `blinded.Rmd` line 102 ("$\mu_{IR}=0.1$") versus line 153 (`mu_IR=0.27`).

---

### 14. SEIR local search uses only 20 iterations (Nmif=20) whereas SIR uses 50

The SIR local search uses `Nmif=50` iterations while the SEIR and SEIQR local searches use only `Nmif=20`. Given that the SEIR model has one additional parameter, fewer iterations are less likely to achieve convergence. The trace plots confirm that SEIR parameters do not fully stabilize. The asymmetry makes the model comparison less reliable.

**Evidence:** `blinded.Rmd` lines 203 (SIR: `Nmif=50`) vs. line 425 (SEIR: `Nmif=20`), line 643 (SEIQR: `Nmif=20`).

---

### 15. No comparison against a non-mechanistic benchmark

The project does not benchmark any of its POMP models against a simple statistical model (e.g., ARIMA or a negative-binomial regression). Without such a baseline, it is not possible to assess whether the mechanistic models provide genuine explanatory value beyond a data-fitting exercise.

---

## Summary of Issues by Severity

| # | Issue | Severity |
|---|-------|----------|
| 1 | Incomparable likelihoods (different measurement distributions) | Critical |
| 2 | Missing /N in SEIQR force of infection | Critical |
| 3 | SEIQR observes stock Q instead of a flow accumulator | Critical |
| 4 | SEIR delta.t=7 mismatched with daily data | Major |
| 5 | SEIR pairs plot uses SIR data | Major |
| 6 | Inconsistent partrans between SEIR pomp object and mif2 | Major |
| 7 | rho and eta log-transformed instead of logit in SEIQR | Major |
| 8 | Global searches use sequential %do% | Minor |
| 9 | No profile likelihoods or confidence intervals | Major |
| 10 | Population figure incorrect (18M vs. 1.9M vs. 8.3M) | Major |
| 11 | Global SIR worse than local SIR (unexplained) | Minor |
| 12 | No filter diagnostics or residual analysis | Minor |
| 13 | Text mu_IR=0.1 contradicts code mu_IR=0.27 | Minor |
| 14 | Fewer IF2 iterations for SEIR/SEIQR than SIR | Minor |
| 15 | No non-mechanistic benchmark comparison | Minor |

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project23/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project23/blinded.html`
