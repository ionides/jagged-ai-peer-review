# Peer Review: W22 Project 23
## COVID-19 POMP Modeling (SIR/SEIR/SEIQR) — New York City

---

## Summary

This project fits three nested compartmental POMP models — SIR, SEIR, and SEIQR — to daily COVID-19 positive case counts in New York City during the Omicron wave (December 4, 2021 to February 1, 2022). The authors use iterated filtering (IF2) with local and global searches for each model and compare models by log-likelihood. A strength of the project is its systematic model-building approach and the use of pomp's IF2 infrastructure. However, the project contains multiple critical technical errors: the SEIQR model's force-of-infection term omits the required N-normalization, the three models use fundamentally incomparable measurement models (Binomial vs. Gaussian), and log-likelihoods across models are presented as directly comparable when they are not. Non-convergence of IF2 is explicitly acknowledged yet the non-converged results are interpreted substantively. No non-mechanistic benchmark is provided, no profile likelihoods are computed, and key model diagnostics are absent.

---

## Major Issues

### 1. SEIQR rprocess omits population-size normalization in force of infection

The SEIQR `seiqr_step` Csnippet specifies the S-to-E transition probability as `rbinom(S, 1-exp(-Beta*I*dt))`, without dividing by N. The SIR and SEIR steps correctly use `Beta*I/N*dt`. The omission of N means the effective per-capita transmission rate scales with the raw infectious count rather than the infectious fraction, making the fitted Beta parameter dimensionally inconsistent and biologically uninterpretable. At NYC scales (N ~ 10^6, I ~ 10^3–10^5), this error inflates the force of infection by three to six orders of magnitude relative to the intended model. Every parameter estimated from the SEIQR model — including Beta, all transition rates, and eta — absorbs this misspecification and is unreliable. The stated SEIQR equations in the text do not include this error, so the code is inconsistent with the described model.

Fix: Replace `1-exp(-Beta*I*dt)` with `1-exp(-Beta*I/N*dt)` in the `seiqr_step` Csnippet.

### 2. Log-likelihoods from SIR/SEIR and SEIQR are on incommensurable scales and cannot be compared

The SIR and SEIR models use a Binomial measurement model (`dbinom(pos, H, rho, give_log)`), where `H` is the daily accumulation of recoveries. The SEIQR model uses a Gaussian measurement model (`dnorm(pos, Q, rho*Q+1e-10, give_log)`), where `Q` is the quarantine stock compartment. These two measurement models have different support, different parameterizations, and different probability mass functions. The log-likelihoods (-50,126 for SIR, -85,131 for SEIR, -602 for SEIQR) are computed under incompatible likelihoods and cannot be compared to select the best model. The paper's central conclusion — that SEIQR is superior because it has "the lowest log likelihood value" — is statistically unfounded. A Gaussian model on a compartment with very different magnitude than the binomial H will naturally produce a much higher (less negative) log-likelihood on the same count scale without this indicating a better fit to the data.

Fix: All three models must use the same measurement model family and link the same latent quantity to the data for their log-likelihoods to be comparable. Alternatively, model selection should be restricted to the SIR vs. SEIR comparison (both using the same Binomial measurement model) and the SEIQR model should be evaluated on its own terms with an appropriate information criterion.

### 3. SEIQR measurement model links to Q (stock) without an accumulator, confounding the observation

The SEIQR model's dmeasure uses `dnorm(pos, Q, rho*Q+1e-10)`, linking observed daily positive cases directly to the Q compartment (total quarantined individuals, a stock). The observed `pos` variable is a daily count of new positive tests — a flow — not a snapshot of how many people are currently in quarantine. This stock-vs-flow mismatch mirrors the error described in the `pomp-covid-active-case-stock-flow-mismatch` pattern. Unlike the SIR and SEIR models, there is no accumulator variable declared for the SEIQR model, so no daily flow is computed. The measurement model therefore compares a daily incidence count to a prevalence compartment. The parameter `rho` compensates by absorbing the ratio of Q-stock to daily test-positive flow, yielding a biologically meaningless reporting-rate estimate.

Fix: Introduce an accumulator variable `H` tracking new entries to Q (i.e., `H += t3` where t3 = dN_IQ), declare it in `accumvars`, and link the measurement model to `H` rather than `Q`.

### 4. Non-convergence is explicitly acknowledged but results are interpreted substantively

The text states for the SEIQR local search: "The plot of the log likelihood seems to fluctuate around a mean value, with no apparent convergence. Other parameters also fluctuate to a certain extent." Despite this explicit non-convergence diagnosis, the authors proceed to report a best log-likelihood of -602.140, display a pairs plot, present a global search table with parameter estimates, simulate trajectories from the MLE parameters, and conclude that SEIQR "best models" the data. This is an instance of the `pomp-self-diagnosed-nonconvergence-audit` pattern: the authors correctly identify that their optimization failed but draw substantive conclusions from the failed optimization anyway. The reported parameter values from non-converged IF2 chains are random visits to a high-likelihood region, not the MLE, and cannot be used to support scientific conclusions.

Fix: Substantially increase Nmif (from 20 to at least 100–200), Np (from 5000 to 10,000+), and the number of replicates. Present convergence traces that demonstrate stable log-likelihood and parameter values before reporting any estimates.

### 5. SEIR Euler step size is delta.t=7 (weekly) but data and SIR/SEIQR use daily steps

The SEIR model is constructed with `euler(seir_step, delta.t=7)`, using a weekly time step, while the SIR model uses `delta.t=1` and the data itself is indexed in daily units. A weekly Euler step applied to daily-indexed data causes the process model to take one step every 7 observation times, which is inconsistent with the daily observation interval and biologically incorrect. The Euler approximation error also increases substantially for large time steps when transition probabilities are not small. This error distorts the SEIR's mu_EI and mu_IR parameter estimates relative to the SIR model, making any comparison between the two models' parameters meaningless.

Fix: Change `delta.t=7` to `delta.t=1` (or a smaller sub-daily value such as `1/7`) for the SEIR model, consistent with the SIR and SEIQR model specifications.

### 6. SEIR local search likelihood surface pairs plot incorrectly displays SIR data

In the SEIR Local Search section, the pairs plot code reads: `pairs(~loglik+Beta+mu_IR+eta+rho, data=sir_lik_local, pch=16)`. This uses `sir_lik_local` (the SIR local search results) instead of `seir_lik_local`. The displayed pairs plot therefore shows the SIR likelihood surface, not the SEIR surface as labeled. Any discussion of the SEIR likelihood surface geometry is unsupported by the displayed figure.

Fix: Replace `data=sir_lik_local` with `data=seir_lik_local` in this pairs plot call.

### 7. No non-mechanistic benchmark comparison

None of the three mechanistic POMP models is compared against a non-mechanistic statistical baseline (e.g., ARIMA, auto-regressive negative binomial). Without such a comparison, it is impossible to assess whether the mechanistic models capture structure beyond what a simple statistical model would achieve. Wheeler et al. (2024) note that none of the 32 papers in their Haiti cholera literature review performed such a comparison, and that some models failed to beat a simple auto-regressive negative binomial benchmark. This omission is especially critical here because the SIR and SEIR models show poor convergence and the global search underperforms the local search, raising the possibility that the mechanistic assumptions are too restrictive for the Omicron wave dynamics.

Fix: Fit an ARIMA or auto-regressive negative binomial model to the same time series and compare log-likelihoods or AIC values.

### 8. Global search box excludes the MLE region (SIR model)

For the SIR model, the global search reports a best log-likelihood of (from the table) that is demonstrably inferior to the local search result (-50,126). The global search box is `Beta in [1,10], mu_IR in [0,7], rho in [0,0.4], eta in [0.4,0.6]`, but the local search converges to `rho ~ 0.74` (initial value) and `eta ~ 0.95`, both of which lie entirely outside the global search box. The global search therefore cannot systematically cover the high-likelihood region; any solution it found there was the result of accidental IF2 drift outside the box bounds rather than deliberate exploration. This matches the `pomp-global-search-box-misalignment` pattern.

Fix: Extend the global search box to bracket the parameter values identified by the local search. A reasonable starting point is to center the box on the local MLE and add a generous radius (e.g., ±50% for each parameter). Repeat the global search with the corrected box to confirm that the global MLE is stable.

### 9. No profile likelihoods or confidence intervals for any model

Profile likelihoods are not computed for any of the three models. Without them, it is impossible to determine whether key parameters (Beta, mu_IR, rho, eta) are identifiable from the Omicron wave data, which spans only 58 days. Parameters such as eta (initial susceptible fraction) are known to be weakly identified in short outbreak windows, as noted in the text itself ("we found that a larger value of eta fits the data better"). The absence of profile likelihoods means that all reported point estimates could lie on a flat ridge of the likelihood surface, making the biological conclusions unreliable (Wheeler et al. 2024, §Parameter identifiability).

Fix: Compute profile likelihoods for at least the most scientifically important parameters (Beta, eta, and rho) using MCAP or a likelihood-slice approach. Report confidence intervals.

---

## Minor Issues

- **Population size discrepancy in introduction**: The introduction states that New York City has a population of "roughly 18 million," which corresponds to the broader New York metro area; the code and reference [3] correctly use approximately 1.89 million (labeled as the borough population). The text should be corrected to state the proper city population (~8.3 million for New York City proper, or the borough value used in the model).

- **SEIQR global search uses `%do%` instead of `%dopar%`**: Both the SIR and SEIQR global searches use `%do%` (sequential) inside `bake()` while registering a parallel backend. This removes the parallelization benefit and makes the global search needlessly slow. The SEIR global search similarly uses `%do%`. These should be `%dopar%`.

- **SEIR partrans in mif2 call is redundant and potentially inconsistent**: The SEIR local search `mif2()` call includes its own `partrans=parameter_trans(log=c("Beta", "mu_EI"),logit=c("rho","eta"))` and `paramnames=c("Beta","mu_EI", "rho","eta")`, which overrides the `partrans` already declared in the `pomp()` object. The supplied `partrans` omits `mu_IR`, which was declared in the pomp object's `partrans`. This inconsistency may cause `mu_IR` to be perturbed on its natural (non-transformed) scale during IF2, producing poor convergence for that parameter.

- **Fixed initial conditions are not estimated or assessed for sensitivity**: E(0)=10000 and I(0)=7000 for SEIR, and E(0)=10000, I(0)=7000, Q(0)=200 for SEIQR, are all fixed at arbitrary values with no justification, no sensitivity analysis, and no comparison to available surveillance data. Wheeler et al. (2024, §Initial conditions) note that initialization strategy can affect AIC by ~72 units. These should be estimated as free parameters or their sensitivity assessed.

- **No model diagnostics beyond visual inspection**: Effective sample size (ESS) from the particle filter is never reported. Conditional log-likelihoods per observation time are not plotted. Filtering-distribution simulations are not distinguished from forward simulations from estimated initial conditions. These diagnostics are essential for assessing whether particle filter degeneration explains the poor convergence (Wheeler et al. 2024, §Model diagnostics).

- **Conclusion incorrectly describes log-likelihood direction**: The conclusion states "the log likelihood value of the SEIQR model is the lowest" to indicate it is the best model. Log-likelihood is higher (less negative) for better-fitting models; "lowest" is the wrong directional descriptor. This is an instance of the `pomp-loglik-direction-error` pattern. (Note that the underlying ranking is accidentally correct because the SEIQR value of -602 is numerically the largest, but the stated reasoning inverts the convention.)

- **Computational effort is low and not justified**: Local searches use Nmif=20 (SEIR, SEIQR) or Nmif=50 (SIR) with Np=5000. Global searches use only 100 starting points with Nmif=50 or 20. No justification for these choices is provided, and the self-diagnosed non-convergence for SEIQR and the global-search underperformance for SIR suggest the effort was insufficient. Total computational cost is not reported.

- **No assessment of model adequacy for the full pandemic period**: The authors restrict analysis to 58 days of Omicron data because they found the multi-peak full series difficult to model, but this restriction is not discussed as a limitation or compared to approaches that handle multiple waves (e.g., piecewise models, variant-specific transmission parameters). The choice to model only the dominant peak is not evaluated quantitatively.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rprocess-wrong-hazard-variable/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stochastic-dmeas-intermediate/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-covid-active-case-stock-flow-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-multiobs-stock-flow-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-population-text-code-discrepancy/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project23/blinded.Rmd`
