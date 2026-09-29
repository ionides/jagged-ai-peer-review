# Peer Review: W24 Project 14
## Tuberculosis Incidence in the USA — ARIMA and SEIRS POMP Analysis

---

## Summary

This project analyzes annual US tuberculosis (TB) case counts from 1953 to 2020 using both an ARIMA(0,1,5) model and a stochastic SEIRS POMP model with a time-varying (linearly decreasing) transmission rate. The project is motivated by the long-term decline in TB incidence and attempts to explain this trend through a mechanistic model incorporating overdispersion, gamma white-noise stochasticity, and waning immunity. While the biological motivation is reasonable and the choice of SEIRS is appropriate for TB dynamics, the POMP analysis is severely incomplete: there is no global search, the reported log-likelihood comes directly from mif2 output (invalidating it as an inference quantity), no non-mechanistic benchmark comparison is made, and the written mathematical equations contain systematic errors that contradict the code. The ARIMA section is also incomplete, lacking residual diagnostics for the selected model.

---

## Major Issues

### 1. No global search and absent convergence diagnostics (Error 1.8 — CC-Yes, Major)

The project acknowledges explicitly: "Due to time constraint it was not possible to run global search." A single mif2 run is executed from a fixed set of starting parameter values. There are no multiple optimization runs from diverse starting points, and no comparison of terminal log-likelihood values across replicates. The trace plot (`plot(mif_out)`) is produced but never interpreted in text. Without replicated searches, there is no evidence the optimizer found the global maximum. All downstream parameter estimates and likelihood values are potentially unreliable. The course explicitly requires convergence evidence before interpreting POMP results (Ch. 15, p. 35). This is the most critical gap in the analysis.

**Fix:** Run at least 10–20 independent mif2 chains from dispersed starting values, compare terminal log-likelihoods, and show that the best-found values cluster near a common level.

---

### 2. mif2 log-likelihood reported directly without replicated pfilter re-evaluation (Error 1.4 — CC-Yes, Major)

The report states: "best parameters we could find with log likelihood of -628.8447." This value is taken from `logLik(mif_out)`, the mif2 internal likelihood, which is not reliable for inference. mif2 applies parameter perturbations during iteration, including in the final step, so the internally computed likelihood reflects a perturbed parameter vector. The course standard is to re-evaluate the likelihood at the MLE by calling `logLik(pfilter(...))` with many particles, replicated to average out Monte Carlo noise. No replicated pfilter calls appear anywhere in the code. The single mif2 likelihood value cannot be used as the model log-likelihood for model comparison or goodness-of-fit assessment.

**Fix:** After mif2, call `replicate(Nreps_eval, logLik(pfilter(TBseir_C, params = coef(mif_out), Np = Np)))` and aggregate with `logmeanexp(se = TRUE)`.

---

### 3. No non-mechanistic benchmark comparison (Error 1.6 — CC-Yes, Major)

The ARIMA and POMP sections are presented as independent analyses. The ARIMA log-likelihood is never extracted and compared to the POMP model log-likelihood. The conclusion states "the POMP model provides a more comprehensive approach" without quantitative evidence. Without comparing the two models' likelihoods on the same data, there is no basis for preferring the mechanistic model. The course taught explicitly that benchmark comparison is a core model validation step (Ch. 17; 531-weakness-reference.md Error 1.6). An AIC or log-likelihood comparison between ARIMA(0,1,5) and the SEIRS POMP model would determine whether the added complexity is supported by the data.

**Fix:** Report the ARIMA log-likelihood (e.g., `logLik(arima(tb_num, order = c(0,1,5)))`), compare it to the replicated pfilter log-likelihood for the POMP model, and discuss the difference.

---

### 4. Written stochastic Euler equations are systematically incorrect and inconsistent with code

The section "Adding stochasticity to compartment transitions" presents equations such as:
- E(t+δ) = E(t) + Binomial(S(t), 1 − exp(−mu_EI · δ))
- I(t+δ) = I(t) + Binomial(I(t), 1 − exp(−mu_IR · δ))
- R(t+δ) = R(t) + Binomial(R(t), 1 − exp(−mu_RS · δ))

Each equation shows only an outflow from the compartment using the wrong parent pool. For example, the increment to E should equal the S→E flow (Binomial(S, 1−exp(−force_of_infection·δ))) minus the E→I flow (Binomial(E, 1−exp(−mu_EI·δ))). Using mu_EI applied to S(t) as the increment to E conflates the two transitions entirely. These written equations do not match the Csnippet code (which correctly implements the transitions), but the mathematical description of the model is what readers evaluate. Per Wheeler et al. (2024), model-code discrepancies are a documented reproducibility failure.

**Fix:** Replace the stochastic Euler equations with the correct net-flow formulas that show both inflow and outflow for each compartment, matching the Csnippet implementation.

---

### 5. No profile likelihoods; parameter identifiability unassessed

The SEIRS model has 13 estimated parameters including Beta, Beta_t, mu_EI, mu_IR, mu_RS, rho, k, sigmaSE, and four initial condition fractions. No profile likelihoods are computed for any parameter. With annual data and only 68 observations, many of these parameters are likely weakly identifiable or confounded (e.g., Beta and Beta_t are both transmission-related; mu_EI and mu_IR interact). Without profile likelihoods, the reported point estimates carry no uncertainty quantification and identifiability cannot be assessed. The course requires profile likelihoods for POMP models (Ch. 16, p. 56).

**Fix:** Compute profile likelihoods for at least the key epidemiological parameters (Beta, mu_IR, rho) and report 95% CIs using the Wilks threshold.

---

## Minor Issues

### 6. No residual diagnostics for the selected ARIMA(0,1,5) model

The `build_and_diagnose_model` function is defined with plotting capability (residual plot, QQ plot, ACF), but it is never called on the selected ARIMA(0,1,5) model. The AIC table is shown and the model is selected, but no residual analysis is presented. Residual diagnostics (ACF of residuals, Ljung-Box test, QQ plot) are the standard way to validate ARIMA model adequacy and are expected in a STATS 531 project.

**Fix:** Call `build_and_diagnose_model(tb_num, "ARIMA(0,1,5)", arima_order = c(0,1,5))` and interpret the residual plots.

---

### 7. Hardcoded local file path prevents rendering

The SEIRS model diagram references a hardcoded local path:
```
<img src="/Users/shreya/Desktop/Winter/stats_531/PROJECT2/seirs_draw.png" ... />
```
This image will not render in any environment other than the original author's machine. The diagram does not appear in the rendered HTML, which means readers see no model schematic at the point where the SEIRS compartments are introduced.

**Fix:** Place the image file in the project directory and use a relative path, or embed the diagram using R's `DiagrammeR` or similar package.

---

### 8. Population size is fixed at 2023 value across all years 1953–2020

The parameter N = 333,000,000 is the 2023 US population. This value is used without change for the entire 68-year time series, even though the US population was approximately 160 million in 1953 and grew substantially over the study period. The authors acknowledge this in the "Further Investigation" section but treat it as optional future work rather than a model limitation. Using an incorrect population size biases the per-capita force of infection and the susceptible fraction throughout the series.

**Fix:** At minimum, note this as a limitation in the main text. If computationally feasible, incorporate a time-varying population covariate (year-specific census estimates) as a covariate in the POMP object.

---

### 9. Fisher CI computation error in model_selection_table

In `model_selection_table` (lines 311–312):
```r
fisher_ci_low <- pc_model$coef - 1.96 * diag(pc_model$var.coef)
fisher_ci_high <- pc_model$coef + 1.96 * diag(pc_model$var.coef)
```
`diag(pc_model$var.coef)` returns the diagonal of the variance-covariance matrix — these are variances, not standard errors. The correct expression is `1.96 * sqrt(diag(pc_model$var.coef))`. As written, the CIs use variance values directly, making them dramatically too wide (by a factor equal to the parameter SE) and the resulting `fisher_ci_cover_0_table` flags are incorrect.

**Fix:** Replace `diag(...)` with `sqrt(diag(...))` in both lines.

---

### 10. Stochastic Euler equations omit the RS waning immunity transition

The stochastic Euler equations section lists transitions for S, E, I, R, and H, but the R(t+δ) equation only shows outflow from R (Binomial(R, 1−exp(−mu_RS·δ))). There is no corresponding line for the S compartment receiving recovered individuals. This omission further contributes to the mathematical description not matching the SEIRS model being claimed. The Csnippet correctly handles dN_RS with `S += dN_RS` and `R += dN_IR − fmin(dN_RS, R)`.

---

### 11. Multiple redefinitions of seir_step obscure the actual model

The function `seir_step` is defined three times in the code: (1) an R function without the H accumulator, (2) an R function with H, and (3) a Csnippet with SEIRS dynamics and time-varying Beta. Only the third definition is used in the final POMP object `TBseir_C`. The first two definitions are dead code that creates confusion about which model is actually being estimated.

**Fix:** Remove the two unused R definitions of `seir_step` and present only the Csnippet version that is actually used.

---

### 12. Figure 2 caption is incorrect

Figure 2 is captioned "TB Cases and Deaths over years" but the plot shows the incidence rate and death rate per 100,000 people — not counts. This is the same caption as Figure 1, which shows raw counts. The distinction matters: Figure 1 shows population-unadjusted counts, while Figure 2 normalizes by population.

---

### 13. Intermediate R-based measurement model uses wrong observation variable

The initial R-based measurement functions (before the Csnippet version) use `Rate` as the observed variable:
```r
seir_dmeas <- function (Rate, H, rho, k, log, ...) { dnbinom(x = Rate, ...) }
```
But the final POMP object is built with `obsnames = 'Number'`, and the Csnippet dmeas uses `Number`. The initial R-based functions would have modeled the incidence rate per 100,000 as a raw count, conflating two very different quantities. While only the Csnippet version is used for the actual analysis, the inconsistency in the code suggests incomplete understanding of which variable is being modeled.

---

### 14. ARIMA model selection rationale is not adequately explained

The paper states "based on the AIC and smallest root, the relatively suitable model we choose is ARIMA(0,1,5)." The AIC table is shown but the reasoning is not explained: which cell has the minimum AIC, what the margin over alternative models is, and whether ARIMA(0,1,5) with a smallest MA root of 1.05 (near the unit circle) is actually invertible or nearly non-invertible. An MA root close to 1 is worth investigating as it could indicate near-non-invertibility.

---

### 15. Visual goodness-of-fit presented as primary model validation

The report's conclusion that the POMP model "reasonably captures the overall declining trend" is based solely on visual comparison of 5 simulated trajectories to observed data. The simulations show wide variability around the observed values in the 1960s–1980s. Wheeler et al. (2024) explicitly note that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." Given that the mif2 likelihood is also unreliable (Issue 2), there is effectively no quantitative goodness-of-fit assessment in this project.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project14/TB_data_usa.csv`
