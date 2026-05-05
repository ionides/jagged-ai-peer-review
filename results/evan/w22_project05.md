# Final AI Review: An Inquiry into the Effects of Vaccination on COVID-19 Cases using Compartment Models

**Project:** w22 Project 05
**Model:** SVEIQRD POMP

---

## Overall Assessment

This paper develops a SVEIQRD (Susceptible, Vaccinated, Exposed, Infected, Quarantined, Recovered, Dead) compartmental model using the POMP framework to study the effect of COVID-19 vaccination on US case counts from April 2021 to April 2022. The scientific motivation is sound, and the model formulation is thoughtful, incorporating a time-varying transmission rate to account for the Delta and Omicron variant waves. The authors also explore ARIMA and ARMA-GARCH as non-mechanistic comparisons, finding both inadequate. However, the core analysis does not reach a usable result: the POMP model fails to converge, parameter estimates are unstable across runs with log-likelihood ranges spanning approximately 2000 units, and the paper's central goal — counterfactual simulation of different vaccination scenarios — is never achieved. The paper would benefit substantially from a reduction in model scope to enable at least partial convergence, quantitative model comparison, and some form of the counterfactual analysis originally proposed.

---

## Key Strengths

**22.05.10 — Scientifically motivated time-varying transmission**
The piecewise beta formulation with change-points at the Delta (July 2021) and Omicron (December 2021) variant emergence dates is well-motivated by data patterns and supported by cited scientific sources. This design choice reflects genuine epidemiological thinking about the data generating process.

**22.05.11 — Appropriate use of IF2 within POMP**
The authors correctly use IF2 (iterated filtering) within the R pomp package for likelihood-based parameter estimation, which is the appropriate methodology for this class of model.

**22.05.13 — Data-grounded initial conditions**
Several initial conditions (V(0), Q(0), D(0), R(0)) are derived directly from observed data, reducing the free parameter count and tying the model to reality at the starting date.

**22.05.12 — Transparency about model failure**
The authors honestly report that convergence was not achieved and that the counterfactual analysis could not be completed. This transparency is scientifically appropriate.

---

## Major Points

**22.05.8 — Stated scientific goal not achieved**
ID: 22.05.8 | Severity: Major

The paper's introduction commits to answering "what if the vaccine rollout was faster or slower?" via counterfactual simulation. The conclusion explicitly states this was not accomplished due to convergence failure. No forward simulation from even the best-fit parameter vector is presented, and no sensitivity analysis around the vaccination rate parameter nu is offered. This is the most critical gap: the paper proposes an analysis and does not deliver it.

Suggested action: At minimum, run forward simulations from the best local search parameter vector (loglik -4796.8) under nu, 0.5*nu, and 2*nu. Report these with clear caveats about convergence. Alternatively, restrict the time series to exclude the Omicron wave (ending November 2021) to achieve convergence in a reduced scope and then perform the counterfactual on that period.

**22.05.7 — No benchmark comparison**
ID: 22.05.7 | Severity: Major

The POMP model log-likelihoods (best: -4796.8) are never compared against any non-mechanistic baseline on a common scale. The ARIMA section concludes the model is inadequate without reporting its log-likelihood. Without a quantitative baseline, it is impossible to know whether the POMP model provides any explanatory value beyond a simple time-series model.

Suggested action: Report the ARIMA(1,1,2) log-likelihood evaluated on the same observations as the POMP model. Compare these as lower bounds on model quality, noting that the likelihood scales are comparable for the same observed data.

**22.05.2 / 22.05.3 — Compartment equation errors**
ID: 22.05.2 and 22.05.3 | Severity: Major

Two structural errors appear in the model equations. First, the equation for V(t) does not subtract N_VE(t) (the flow from Vaccinated to Exposed), yet the transition equations include delta_N_VE ~ Binomial(V, ...). This violates conservation of individuals: vaccinated individuals who become exposed are removed from E but not from V. Second, the S(0) equation reads S(0) = N - V(0) - S(0) - E(0) - ... which is self-referential. These are likely typographical errors, but they must be corrected and the code verified to ensure the implemented model matches the intended formulation.

Suggested action: Correct the V(t) balance equation to V(t) = V(0) + N_SV(t) - N_VE(t). Fix the self-referential S(0) equation. Verify that model.c implements the correct transitions.

**22.05.6 — No profile likelihoods or parameter confidence intervals**
ID: 22.05.6 | Severity: Major

No profile likelihoods are computed for any parameter. With 15+ free parameters and clear convergence issues, identifiability is the central diagnostic question. The pair plots shown (figure 15) are described as "sparse" by the authors themselves, confirming that inference is not reliable. Without profiles or confidence intervals, no scientific interpretation of any parameter value is justified.

Suggested action: Compute profile likelihoods for at least the scientifically key parameters: nu (vaccination rate), gamma (vaccine protection), and b1/b2/b3 (variant transmission rates). Even coarse profiles at run_level=2 would indicate whether these parameters are identifiable.

**22.05.5 — Monte Carlo noise in log-likelihood not addressed**
ID: 22.05.5 | Severity: Major

Several parameter vectors have loglik.se > 0.2 (up to 0.439 in the local search, 0.277 in the global search). These standard errors are large relative to the log-likelihood differences between parameter vectors, meaning the ranking of parameter vectors is unreliable. The paper does not discuss this or take corrective action (e.g., increasing particle count, using more pfilter replicates, applying logmeanexp correctly).

Suggested action: For any parameter vector reported as "best," use at least 10 replicated pfilter runs and aggregate with logmeanexp. Flag parameter vectors with loglik.se > 0.5 as unreliable.

**22.05.1 — Global search underperforms local search without explanation**
ID: 22.05.1 | Severity: Major

The best log-likelihood from global search (-5677.5) is substantially worse than the best from local search (-4796.8), a difference of ~881 log-likelihood units. This is the reverse of what would be expected if the global search were properly exploring parameter space. The paper does not acknowledge or investigate this anomaly.

Suggested action: Report the parameter ranges used for global search initialization. Verify that global search boxes include the locally optimal region. Check whether global search used sufficient particles and iterations.

---

## Minor Points

**22.05.15 — Computational parameters not reported**
The paper mentions "run level" but never specifies Np (number of particles), Nmif (MIF2 iterations), or number of replicates for any run level. These are necessary for reproducibility and for assessing whether convergence failure is due to insufficient computation.

Suggested action: Add a table or paragraph listing Np, Nmif, and replicates for each run_level used.

**22.05.16 — Non-standard measurement model**
The observation model uses a truncated normal distribution: Cases ~ (round(C_N))+ where C_N ~ N(chi * H_n, (rho * H_n)^2 + chi * H_n). Truncating and rounding a normal to obtain count data is non-standard and may introduce bias. Negative binomial is the standard measurement model for count data in epidemiological POMP models.

Suggested action: Consider replacing with a negative binomial measurement model. If the truncated normal is retained, justify it and check that it handles the zero-inflation plausibly.

**22.05.4 — AIC table non-monotonicity not discussed**
ARIMA(2,4) achieves AIC 9278 while ARIMA(3,4) yields 9311 and ARIMA(4,4) yields 9315. Adding AR terms beyond AR(2) worsens fit by more than 2 AIC units, which may indicate optimization failures for higher-order models.

Suggested action: Verify that higher-order ARIMA estimates converged successfully and note any convergence warnings.

**22.05.9 — Piecewise beta notation inconsistency**
The piecewise definition of beta_t uses ">=" for the first condition (t >= July 1) but ">" for the last condition (t > December 1), leaving the boundary days ambiguous.

Suggested action: Use consistent inequality notation and explicitly define which period covers the boundary dates.

**Notation/typographic errors**
Multiple typos throughout the manuscript ("colloquilly," "afformentioned," "succeptible," "heteroskadasticity," "spesifically"). Figure captions are absent throughout. Proofreading is recommended before any submission.
