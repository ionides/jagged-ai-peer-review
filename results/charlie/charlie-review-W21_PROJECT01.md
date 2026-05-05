# Peer Review: W21 Project 01
**Title:** Investigating the effects of vaccinations and government policy on the spread of COVID-19 in the State of Pennsylvania

---

## Summary

This project fits a SEIR compartmental model with covariates (government policy multipliers and vaccination counts) to daily positive COVID-19 case data from Pennsylvania (June 2020 – March 2021) using the `pomp` package and iterated filtering (IF2). The authors progressively build up a model from a simple SEIR to one that incorporates time-varying transmission rates and vaccine-induced immunity. While the project addresses a relevant and timely question and shows familiarity with the `pomp` workflow, the analysis suffers from several serious methodological and reporting deficiencies: the accumulator variable `H` is misspecified (it is set equal to the current stock of infected individuals rather than the cumulative flow), the covariate multipliers for transmission are hard-coded with no statistical justification, convergence of the global search is never demonstrated, profile likelihoods are entirely absent, and no quantitative goodness-of-fit statistics are reported or used to evaluate whether the mechanistic model outperforms the ARIMA baseline cited in the paper. The conclusions are therefore not adequately supported by the presented evidence.

---

## Major Issues

### 1. Critical misspecification of the accumulator variable H

The process model sets `H = I` at every time step (lines 190, 270, 375 of blinded.Rmd), meaning H tracks the instantaneous stock of currently infected individuals rather than the cumulative flow of new infections over a time step. The measurement model then draws `reports = rbinom(H, rho)`, equating daily reported cases to a binomial sample from the total current infected count. This is biologically incorrect: daily reported cases represent new detections, not random samples from all currently-infected individuals simultaneously. The correct formulation should set H to zero at the start of each time step (using `accumvars` to handle the reset) and accumulate only the flow `dN_EI` during the step, so that H counts new transitions into the I compartment per time step. The current implementation fundamentally misaligns the observation model with epidemiological reality and makes all downstream parameter estimates uninterpretable. Specifically, because H conflates stock and flow, the estimated reporting rate `rho` and the transmission rate `Beta` will absorb the stock-vs-flow discrepancy in ways that are impossible to disentangle.

### 2. No benchmark comparison for the mechanistic model

The paper fits an ARIMA model as a "baseline" but explicitly states "We observe no significant evidence that the ARIMA model performs better than white noise. Thus we will use white noise as a benchmark." No log-likelihood or AIC values are ever computed for the ARIMA model, white noise model, or SEIR model under a common metric. Without a quantitative comparison, it is impossible to assess whether the SEIR model captures meaningful dynamical structure beyond a simple statistical model. Wheeler et al. (2024) identify this as the single most diagnostic check for mechanistic model validity; none of the 32 papers they reviewed performed such a comparison. The paper must report the log-likelihood of the SEIR model alongside a non-mechanistic benchmark (e.g., auto-regressive negative binomial) evaluated on the same data under the same observation model.

### 3. Convergence not demonstrated for the global search

The global search results are presented only as a pairs plot of parameter values colored by log-likelihood, and the authors themselves note "the log-likelihood has large variations even for the same value of the parameters." No IF2 convergence traces (log-likelihood vs. iteration number) are provided for any of the mif2 runs. Without these, it is impossible to determine whether the reported likelihoods are near the MLE or whether optimization terminated prematurely. Wheeler et al. (2024) emphasize that a large improvement in log-likelihood was "primarily attributed to increasing computational effort." The text mentions 500 replicates with Np=5000 and Nmif=500, but no evidence is provided that 500 iterations are sufficient, that the likelihood surface has been adequately explored, or that multiple restarts agree on a common maximum. This makes all conclusions about model fit unreliable.

### 4. No profile likelihoods or confidence intervals

Profile likelihoods are never computed for any parameter. The pairs plots suggest substantial non-identifiability (the authors themselves note "the simulations do not help us in predicting the values of eta or mu_EI"), yet no formal identifiability assessment is performed. Without profile likelihoods, it is impossible to know which parameters are identifiable from the data, whether the reported MLEs are biologically plausible, and whether any scientific conclusions can be drawn from the parameter estimates. Wheeler et al. (2024) document cases where MLE estimates of zero for key parameters were evidence of model misspecification rather than biological truth — precisely this kind of diagnostic is needed here.

### 5. Hard-coded covariate multipliers with no statistical justification

The transmission rate multipliers (1.38 from September 13, 1.0 before, and 0.89 from December 1) are set by hand with reference only to narratives about policy changes. These values are not estimated from data. The text states they were chosen "to reflect the shape of the data," which is curve-fitting by eyeball rather than statistical inference. This means the model has additional free parameters (the multiplier values and their change-points) that are informally calibrated rather than estimated via likelihood maximization, making formal model comparison and uncertainty quantification impossible. Wheeler et al. (2024) characterize ad hoc calibration as a major methodological concern. At minimum, the multiplier values should be treated as unknown parameters and jointly estimated with the remaining model parameters, or a sensitivity analysis should demonstrate robustness to the chosen values.

### 6. No quantitative goodness-of-fit statistics reported

Neither a log-likelihood value nor an AIC is reported for any model variant. Model comparison between the simple SEIR, the policy-covariate SEIR, and the vaccination SEIR is performed entirely by visual inspection of simulated trajectories against observed data. Wheeler et al. (2024) state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The reported pairs plots display logLik values but no best logLik value is extracted and stated in the text. The reader cannot assess whether the model achieves a plausible fit to the data.

### 7. Measurement model is not overdispersed

The measurement model uses a binomial distribution: `lik = dbinom(reports, H, rho, give_log)`. Count data for infectious disease case reports is virtually always overdispersed relative to binomial (or Poisson) assumptions, especially for daily new case counts during a pandemic. A negative binomial measurement model is strongly recommended in the literature (Wheeler et al. 2024; see §Stochasticity). The binomial measurement model will likely produce over-confident parameter estimates and underestimate uncertainty. The authors do not justify this choice or test it against an overdispersed alternative.

### 8. Second global search uses the wrong POMP object

The "Iterative filtering on a smaller dataset" section states it performs global search for a "simple SEIR model without any covariates and without vaccination." However, the code still passes the object `datSEIR`, which at that point in the script has been updated to include the vaccination covariate (`covar50_IM`) and uses `seir_step_mod_ver2`. The code does not subset the data to September–December 2020 or remove the covariates. The narrative description is therefore inconsistent with the code that was actually executed. Results from this section cannot be interpreted as described in the text.

---

## Minor Issues

### 9. Accumulator variable declared but also serving as a state variable

The `pomp` call declares `accumvars = "H"`, which instructs `pomp` to reset H to zero after each observation. However, the rprocess sets `H = I` (a stock) at the end of each step. The combined effect is that H will be zero at each observation time (because `accumvars` resets it after the measurement is taken) and will equal I only transiently during a step. This interacts with the measurement model in a non-obvious way. The authors should clarify what value of H is actually passed to the measurement model and verify it aligns with their biological intention.

### 10. ARMA benchmark analysis is incomplete

The paper states an AIC table is computed but only reports that "we observe no significant evidence that the ARIMA model performs better than white noise." The AIC table is produced but no model is fit and its log-likelihood extracted. A proper benchmark comparison would fit an ARMA(p,q) or seasonal ARIMA model and compare its log-likelihood (on an appropriate scale) to the SEIR model's log-likelihood. Stating that white noise is the benchmark because ARIMA offers no improvement is a misuse of baseline comparisons — it means the data may have been over-differenced or log-transformed in a way that removes the signal.

### 11. Initial condition formulation is internally inconsistent

The `rinit` function computes `S = nearbyint(eta*N) - ini_recovered` and `R = nearbyint((1-eta)*(N-ini_recovered) + ini_recovered)`. These formulas are not clearly derived from epidemiological principles and the relationship between `eta` (intended as the susceptible fraction) and the initial recovered population is not transparent. In the params vector, `eta=0.9` and `rho=0.9` are both set to 0.9 but serve completely different roles (susceptible fraction and reporting rate, respectively). The coincidence of these values and the unclear rinit formula raise the possibility of a parameter confusion error.

### 12. Data availability: external URLs may break

All data are loaded from live URLs (`covidtracking.com` and `github.com/owid`). The Covid Tracking Project stopped updating in March 2021, and URL structures may have changed. No local data files are included. This prevents independent reproduction and makes the analysis fragile over time. The code-supplement checklist requires that all data needed to reproduce results be included alongside the code.

### 13. Random seeds not properly managed for the global search

The script sets `registerDoRNG(4082879)` early in the document but the `stew()` calls do not explicitly record per-job seeds. The stochastic results of the parallel IF2 runs may not be exactly reproducible across different cluster configurations, R versions, or `doRNG` versions. The particle count and IF2 iteration counts are reported, but per-job seeds for the particle filter evaluations are not documented.

### 14. No sensitivity analysis for key fixed parameters

The parameters `mu_EI = 0.125` (incubation rate) and the initial conditions are fixed based on literature values or heuristic estimates, and no sensitivity analysis is performed to assess how estimates of `Beta`, `rho`, and `eta` depend on these fixed values. For a model with known identifiability challenges (acknowledged by the authors), this is a significant omission.

### 15. No forecasting or out-of-sample evaluation

The paper states in the introduction that it will "make a prediction on the future positive cases increase," but no forecast is produced. The conclusions section does not address forecasting at all. If forecasting was a stated goal, the paper should include either: (a) a held-out evaluation of forecasts against subsequent data, or (b) forward simulations from the filtering distribution with propagated parameter uncertainty, as described in Wheeler et al. (2024).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project01/Makefile`
