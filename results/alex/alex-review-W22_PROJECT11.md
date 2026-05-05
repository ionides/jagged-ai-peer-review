# Peer Review: Hungarian Chickenpox POMP Model Analysis
**Semester:** W22 | **Project:** 11

---

## Summary

This project fits a modified SEIR model (with explicit vaccination) to aggregated weekly Hungarian chickenpox case counts from 2005 to 2014 using the `pomp` framework. The authors perform a local and global MIF2 search, present convergence diagnostics, and simulate from the estimated parameters. The work shows solid effort and reasonable epidemiological motivation, but has a number of significant methodological and reporting weaknesses outlined below.

---

## Weaknesses (prioritized from most to least critical)

### 1. [Major] R update equation for the recovered compartment is incorrect

The C-snippet sets `R = pop - S - E - I + vac` at every step, rather than applying the standard differential update `R += trans[4] + vac - mu*R`. This formulation assigns all individuals not in S, E, or I directly to R, which is equivalent to enforcing a population-balance constraint in a way that adds all recoveries and vaccinations simultaneously without subtracting natural deaths from R. The recovered compartment therefore does not evolve as a genuine Markov state; instead it is a residual derived from the others. This makes the dynamics of R incorrect and can cause numerical artefacts, especially given that deaths are removed from S, E, and I but R only grows via the accounting identity.

**Evidence:** `R = pop - S - E - I + vac;` (blinded.Rmd, line 246).

---

### 2. [Major] iota (importation rate) is allowed to go negative and the MLE uses a negative value

The `iota` parameter enters the force of infection as `(I + iota)^alpha / pop`. A negative iota would make the effective infectious count `I + iota` negative or near zero, which is epidemiologically meaningless and can cause the likelihood to collapse. The global search lower bound for iota is set to 0, yet the best global-search MLE uses `iota = -0.4295031`. The parameter transform does not constrain iota to be positive (it is left on the natural scale), so negative values can be reached during MIF. This is a model specification error.

**Evidence:** `iota=-0.4295031` in the global simulation call (blinded.Rmd, line 743); `lower=c(..., iota=0, ...)` for the global search design but no positivity constraint in `parameter_trans`.

---

### 3. [Major] Local search MLE produces an implausible R0 of ~83; global search MLE gives R0 = 202 with gamma = 922

The estimates for R0 far exceed the epidemiologically accepted range of 7--12 for chickenpox. The best local MLE is R0 = 82.7 and the best global MLE is R0 = 202. The corresponding gamma values are also extremely high (84 and 922 per year, implying infectious periods of about 4 days and 0.4 days respectively). These values suggest the optimizer has found a likelihood ridge or local maximum where the epidemic dynamics are unrealistic. The discussion section acknowledges the high R0 but does not resolve it; the authors simply note it "requires investigation." No corrective action is taken before drawing conclusions.

**Evidence:** Local MLE table (cpox_params_1.csv, row 1: R0 = 82.67); global simulation params (blinded.Rmd, line 742--743).

---

### 4. [Major] Outliers are removed without statistical justification

Six data points are removed from the time series on the grounds that they are "possible data entry errors," identified solely by visual inspection. No statistical test, residual analysis, or citation of a known data-recording event is provided to support their removal. Removing observations from a POMP model without justification inflates the likelihood and biases parameter estimates; the overdispersion parameter `psi` is specifically designed to accommodate unusual observations within the model.

**Evidence:** "We attribute them to the data entry errors and remove them from the data" (blinded.Rmd, line 43--44); rows removed: `c(122,159,469,486,487,493)`.

---

### 5. [Major] Global search uses a narrower range for R0 (6--14) than the local search result (~83), causing a fundamental inconsistency

The global search explores R0 in the range [6, 14], which is reasonable from the literature. However, the local search converged to R0 ~ 83 with a higher log-likelihood (-3401) than the global search maximum (-3478). This inconsistency is acknowledged but not resolved. One likely explanation is that the local search started from Birmingham measles parameters and wandered into a different region of parameter space; the global search range was not updated based on local results. The result is that the two searches are not coherently related to each other.

**Evidence:** `lower=c(R0=6, ...)`, `upper=c(R0=14, ...)` (blinded.Rmd, line 579--580); local MLE: R0 = 82.67, loglik = -3401; global maximum loglik = -3478 (blinded.Rmd, line 730--731).

---

### 6. [Major] alpha (mixing parameter) is fixed at 1 in the local search but perturbed in MIF, creating a contradiction

In the code, `theta["alpha"] <- 1` is set and alpha is in `estpars` is excluded (the `estpars` set excludes `sigmaSE, mu, alpha, rho, iota`), yet `alpha=cpox_rw.sd` appears in the `rw.sd(...)` call for MIF. This inconsistency means alpha is either estimated (if MIF respects the rw.sd) or fixed (if the parameter vector already has it fixed and the transform excludes it from perturbation). Additionally, alpha is not given a log or logit transform in `parameter_trans`, which means it can be perturbed to negative values. The text says alpha was fixed to 1, but the code does not cleanly implement this.

**Evidence:** `estpars <- setdiff(names(theta),c("sigmaSE","mu","alpha","rho","iota"))` vs. `alpha=cpox_rw.sd` in rw.sd (blinded.Rmd, lines 411, 450); `theta["alpha"] <- 1` (line 413).

---

### 7. [Major] No comparison to a baseline model (e.g., SARIMA, simpler SIR, or null log-likelihood)

The project does not report any reference log-likelihood to contextualize the SEIR fit. Without a baseline, it is impossible to judge whether the POMP model provides meaningful improvement over, say, a seasonal regression or a simpler SIR model. A likelihood ratio test or AIC comparison against a simpler alternative is standard for POMP epidemiological analyses and is absent here.

---

### 8. [Major] Only a single simulation replicate is shown for model evaluation

Both the local and global model evaluations present only `nsim=1` simulation against the data. A single stochastic realization can look arbitrarily good or bad. The standard practice is to show multiple simulations (e.g., nsim = 100 with quantile bands) to communicate the uncertainty in the model's predictions and to assess whether the data falls within the model's predictive distribution.

**Evidence:** `nsim=1` in both simulate calls (blinded.Rmd, lines 559 and 741--745).

---

### 9. [Major] The vaccination implementation conflates vaccination with recovery and underestimates its effect

Vaccinated individuals flow directly from S to R via `vac = nearbyint(vr * br * 0.92 * dt)`. This means only newborns are vaccinated each week (since `br` is the birth rate), whereas in Hungary vaccination of older susceptible children also occurs. Furthermore, the 0.92 efficiency factor is applied multiplicatively to the flow, but the immunity provided by varicella vaccine is >90% only for severe disease; mild breakthrough cases still occur. These modeling choices are not justified epidemiologically, and the distinction between an explicit vaccine compartment and the recovery compartment is never discussed.

---

### 10. [Moderate] Duplicate rows in cpox_params_1.csv inflate the apparent number of search results

The saved parameter CSV file contains many exact duplicate rows (e.g., the top-ranked parameter set appears at least 3 times with identical values). This suggests the same run was combined into the CSV multiple times. While this does not change the MLE itself, it gives a misleading impression of the number of independent search evaluations and inflates confidence in the global search coverage.

**Evidence:** cpox_params_1.csv rows 1--3 are identical; rows 4--6 are identical; rows 7--9 are identical; etc.

---

### 11. [Moderate] Cooling fraction of 0.1 is very aggressive for MIF2

The cooling fraction of 0.5 after 50 iterations (`cooling.fraction.50 = 0.1`) means the random walk standard deviation is reduced to 10% of its initial value after only 50 iterations. With Nmif = 200 (run_level = 2), this leaves very little exploration after the first quarter of iterations. The standard recommendation for MIF2 is a cooling fraction around 0.5 or higher. The aggressive cooling likely explains why the filter fails to find the region of parameter space consistent with the literature R0.

**Evidence:** `cpox_cooling.fraction.50 <- 0.1` (blinded.Rmd, line 397).

---

### 12. [Moderate] Initial parameters are taken wholesale from Birmingham measles without epidemiological justification for most

The authors borrow `sigma`, `gamma`, `amplitude`, `alpha`, `iota`, `psi`, and `sigmaSE` directly from a Birmingham measles dataset. Measles and chickenpox have different latent periods, infectious periods, and transmission dynamics. While R0, rho, and vr are adjusted using external information, the other parameters are not justified for chickenpox. For example, the initial sigma (rate of leaving latent stage) = 45.6 per year from the measles calibration implies a 8-day latent period, which is within the chickenpox range (10--21 days), but `gamma` = 32.9 per year implies a 11-day infectious period (chickenpox is typically 5--7 days). No sensitivity analysis is performed to assess how sensitive results are to these assumed initial values.

---

### 13. [Moderate] The rho justification is circular and questionable

The reporting rate rho is set to 0.43 by dividing total reported cases by total births over the study period. This interpretation is incorrect: rho is the fraction of true infections that are reported, not the fraction of births that become cases. In a population where most unvaccinated individuals get chickenpox in childhood, rho should be estimated relative to total infections, not births. The calculation conflates incidence with birth cohort size and likely underestimates rho.

**Evidence:** "Calculated by total number of cases divided total number of births in this ten year period" (blinded.Rmd, lines 333--334).

---

### 14. [Moderate] The global search MLE used for simulation has iota < 0 and gamma > 900, but these implausible values go unremarked in the discussion

The global-search simulation uses `gamma = 922.5` (infectious period of ~0.4 days, far shorter than the true chickenpox infectious period of 5--7 days) and `iota = -0.43` (negative importation). These values are presented in the global model evaluation table without comment. The authors describe the global model fit as acceptable ("captures seasonality") without noting that the underlying parameter values are epidemiologically impossible.

---

### 15. [Minor] The seasonality windows are copied from measles without adaptation to chickenpox

The term-time seasonality function uses the same school-term windows as the King measles case study (days 7--100, 115--199, 252--300, 308--356). These windows correspond to English school terms. Hungarian school terms differ (typically September to June with different holiday schedules). No justification is given for using English school-term seasonality to model Hungarian chickenpox, and no sensitivity analysis is performed.

**Evidence:** `if ((t>=7&&t<=100) || (t>=115&&t<=199) || (t>=252&&t<=300) || (t>=308&&t<=356))` (blinded.Rmd, lines 204--207).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project11/finalProject.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project11/cpox_params_1.csv`
