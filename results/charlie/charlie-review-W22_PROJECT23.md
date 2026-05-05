# Peer Review: W22 Project 23
## COVID-19 POMP Modeling (SIR, SEIR, SEIQR) — New York City

---

## Summary

This project fits three compartmental POMP models (SIR, SEIR, SEIQR) to daily COVID-19 case counts in New York City during the Omicron wave (December 4, 2021 – February 1, 2022) using iterated filtering (`mif2`) for parameter estimation. The authors compare models via log-likelihood and conclude the SEIQR model is best. While the ambition of comparing three nested model structures is commendable, the analysis contains several critical methodological errors that invalidate its core conclusions. The three models use fundamentally incompatible measurement models and likelihood scales, making all cross-model log-likelihood comparisons meaningless. In addition, the SEIQR model contains a force-of-infection specification error (missing population normalization), uses an inappropriate Gaussian measurement model for count data, and its claimed superiority is stated despite acknowledged failure to converge. No profile likelihoods, no benchmark comparison, and no model diagnostics are provided.

---

## Major Issues

### 1. Incomparable likelihoods across models — core conclusion is invalid

The SIR and SEIR models use a Binomial measurement model (`dbinom(pos, H, rho, give_log)`), while the SEIQR model uses a Normal measurement model (`dnorm(pos, Q, rho*Q+1e-10, give_log)`). These likelihoods are on completely different scales: the Binomial is a discrete probability mass function and the Normal is a continuous density. Log-likelihoods from these two different observation model types are not directly comparable. The paper's central conclusion — "From a statistical perspective, we would conclude [SEIQR] as the best fitting model" based on having the highest log-likelihood (-602 vs -50126 vs -85130) — is therefore invalid. The massive difference in log-likelihoods reflects the change in likelihood scale (discrete vs continuous) rather than model quality.

This is a course-confirmed error (CC-Yes, Error 1.14 from weakness reference): likelihoods are comparable only when models share the same observation model and data definition. The remedy is to specify all three models with the same measurement model class (e.g., all Binomial or all Negative Binomial on daily reported cases), then re-run the comparisons.

### 2. SEIQR measurement model observes the quarantine stock, not daily new cases

The SIR and SEIR models correctly use an accumulator variable `H` that tallies new transitions per day, resetting to zero at each observation time. The measurement model then draws from `H`, representing daily incidence. The SEIQR model omits the accumulator entirely: its step function has no `H += ...` line, and the measurement model observes directly from the current quarantine stock `Q` (`dnorm(pos, Q, rho*Q+1e-10, give_log)`). Observing from a stock compartment conflates the cumulative count of people currently in quarantine with daily reported new cases. This is a fundamental misspecification: the observable (daily positive tests) should be tied to daily transitions (new quarantined individuals), not the standing stock. As a result, the SEIQR likelihood measures something categorically different from what the data represent.

### 3. SEIQR force-of-infection missing population normalization

In the SEIQR step function (line 551), the S-to-E transition is:

```
double t1 = rbinom(S, 1-exp(-Beta*I*dt));
```

The SIR and SEIR models correctly normalize: `-Beta*I/N*dt`. The SEIQR model omits the `/N` term. This means `Beta` in the SEIQR model implicitly absorbs the population size and is not interpretable as a standard transmission rate. In a population of ~1.9 million, this makes Beta approximately 1.9 million times larger than comparable models, silently distorting all parameter estimates. The estimated `Beta` values across models cannot be compared.

### 4. SEIR uses daily data with weekly Euler time steps (delta.t = 7)

The SEIR model is constructed with `rprocess=euler(seir_step, delta.t=7)` (line 364), while the SIR model uses `delta.t=1` and the SEIQR model uses `delta.t=1`. The dataset is daily case counts. Using `delta.t=7` means the SEIR Euler steps span one week, which is inconsistent with the daily observation interval. At each observation time (every 1 day), the model will have advanced only a fraction of a weekly step — or the accumulator will integrate over a partial step. This produces incorrect transition probabilities and makes the SEIR likelihood incomparable to the SIR and SEIQR likelihoods even if the measurement models were otherwise identical.

### 5. SEIQR iterated filtering shows no convergence but conclusion proceeds regardless

The authors explicitly state (line 633): "The plot of the log likelihood seems to fluctuate around a mean value, with no apparent convergence." Despite this, the SEIQR MLE is reported and used to declare SEIQR the best model. Lack of convergence in the likelihood trace means the reported parameter estimates and log-likelihood values are not MLEs — they are arbitrary points on the likelihood surface. Drawing scientific conclusions from non-converged optimization is methodologically unsound. The course convention (CC-Yes, Error 1.8) requires consistent upward convergence in the log-likelihood panel of trace plots before results are interpreted.

### 6. SEIQR uses Normal measurement model for count data

Daily COVID-19 case counts are non-negative integers and are highly overdispersed. Using a Gaussian measurement model (`dnorm`) for count data is inappropriate: the Normal distribution assigns probability mass to negative values (impossible for counts), and its symmetric variance structure does not reflect the skewed, long-tailed nature of case count distributions. At low counts (near zero), the model can generate negative observations. The SIR and SEIR models use Binomial, which at least respects the integer and non-negativity constraints. A Negative Binomial measurement model is standard for overdispersed count data in compartmental POMP models (Wheeler et al. 2024, §Stochasticity).

### 7. No profile likelihoods reported; parameter identifiability unassessed

No profile likelihoods are computed for any model or any parameter. The pairs plots show the likelihood surface from iterated filtering output but do not constitute proper profile likelihood computations. Without profiles, it is unknown whether any parameters are identifiable from the data. The SEIQR model has six free parameters plus fixed population for a 59-day dataset — strong concerns about identifiability are warranted, particularly for `mu_R1`, `mu_R2`, and `eta`. Without profile likelihoods and confidence intervals, none of the reported parameter estimates can be given scientific interpretation (CC-Yes, Error 1.9; Wheeler et al. 2024, §Parameter identifiability and uncertainty).

### 8. Global search uses sequential `%do%` instead of parallel `%dopar%`

The global search loops for all three models (lines 280, 499, 722) use `%do%` rather than `%dopar%`. The local searches correctly use `%dopar%`. For 100 starting points each, the global search computations are run serially. This is both computationally inefficient and suggests that the global search may have been truncated or may not have explored the parameter space adequately relative to what was intended. If the global search produced lower likelihoods than the local search (as observed for the SEIR model), this could be a consequence of insufficient exploration due to the serial loop.

---

## Minor Issues

### 9. SEIR likelihood surface plot displays SIR data (copy-paste error)

Line 464 contains `pairs(~loglik+Beta+mu_IR+eta+rho, data=sir_lik_local, pch=16)`. This is inside the SEIR local search section but uses `sir_lik_local` instead of `seir_lik_local`. The plot in this section therefore shows the SIR likelihood surface, not the SEIR likelihood surface. This is a reproducibility error — the rendered document does not show what it claims to show.

### 10. No non-mechanistic benchmark comparison

No ARMA, regression, or IID benchmark is provided for comparison with the POMP models. While the course does not require this, the absence makes it impossible to assess whether any of the mechanistic models captures meaningful structure beyond what a simple statistical model achieves. Given that all three POMP fits show substantial instability or misspecification, a benchmark comparison would be especially informative here (Wheeler et al. 2024, §Benchmark comparison).

### 11. Initial conditions for E, I, Q are fixed constants, not estimated parameters

In the SEIR and SEIQR models, E=10000, I=7000, Q=200 are hard-coded in the initialization Csnippets but are not included as POMP parameters. These cannot be optimized by `mif2`. Initial conditions can strongly affect fitted results, especially at the beginning of the modeling window. Parameterizing them (e.g., as fractions of N) and including them in the estimation would improve rigor. The course standard is to estimate initial conditions or explicitly justify fixing them.

### 12. SIR accumulator variable H tallies recoveries, not new infections

The SIR step function increments `H += dN_IR` (recoveries), not `H += dN_SI` (new infections). Similarly, the SEIR model uses `H += dN_IR`. In a standard SIR model for case reporting, newly reported cases correspond to new infections (S→I transitions), not to recoveries (I→R transitions). Using recoveries as the accumulator implicitly assumes that all individuals report at recovery, not at infection — a non-standard assumption that is not stated or justified. The choice of which transition drives the accumulator should be explicitly motivated.

### 13. Population size description is inconsistent in introduction

The introduction states the population of New York City is "roughly 18 million" (citing a JHU COVID dashboard URL). All models use N=1,886,700 (~1.9 million). The text later states this is the NYC population, but 18 million is closer to the New York metropolitan statistical area population. The data is correctly filtered to New York City, but the introduction is misleading and the reference cited does not clearly support the 18 million figure.

### 14. No model diagnostics provided

No conditional log-likelihood plots, effective sample size diagnostics, or simulation-based diagnostic comparisons are provided for any of the three models. Without these, it is not possible to identify which time periods the models fit well or poorly, or whether the particle filter is degrading (low ESS). These diagnostics are especially important given the acknowledged convergence issues with the SEIQR model (Wheeler et al. 2024, §Model diagnostics).

### 15. SEIQR local search specifies a conflicting partrans override inside mif2

In the SEIQR local search (lines 644-647), the `mif2` call includes both `paramnames` and a `partrans` argument that overrides the model-level transformation. However, `eta` is listed in `paramnames` but transformed via `logit` in the mif2 call, while the model-level `partrans` uses `log` for `eta`. This inconsistency between the model-level and mif2-level parameter transformations could cause silent errors in how the random walk perturbations are applied to `eta`, potentially corrupting the local search for this parameter.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project23/blinded.Rmd`
