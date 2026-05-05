# Peer Review: W24 Project 14 — Tuberculosis in the U.S. (SEIRS POMP Model)

---

## Summary

This project analyzes annual U.S. tuberculosis (TB) case data from 1953–2020 using both ARIMA and POMP (SEIRS compartmental) models. The ARIMA section is reasonably thorough, and the SEIRS model introduces sensible epidemiological structure and a time-varying transmission rate. However, the POMP component has serious methodological deficiencies: no global search is performed, the model specification contains several errors, the parameter estimation workflow is incomplete, and the biological interpretations of several fitted parameters are implausible. Issues are listed below in descending order of severity.

---

## Major Weaknesses

### 1. No Global Parameter Search — Optimization is Effectively Absent

The authors explicitly acknowledge that no global search was run: "Due to time constraint it was not possible to run global search." Only a single local `mif2` run with 50 iterations and 2,000 particles is shown. For a POMP model with 13 free parameters, this is insufficient to claim that the reported parameter values and log-likelihood are meaningful estimates. The entire optimization section reduces to a single, potentially arbitrary starting point. Without at least a local multi-start or global search (e.g., `runif`-initialized particle filters over a box), there is no basis for concluding that the model has been fitted to the data.

### 2. Model Discrepancy: H Compartment Accumulates Recoveries, Not New Infections

In the final C-snippet `seir_step`, the accumulator variable `H` is incremented by `dN_IR` (the recovery flow from I to R):

```c
H += dN_IR;
```

But `H` is then used as the expected number of new TB cases in the measurement model (`dnbinom_mu(Number, k, rho*H, give_log)`). New TB cases are new infections (S→E or E→I transitions), not recoveries. Using `dN_IR` as a proxy for case counts conflates incidence with recovery, which is biologically incorrect. The correct quantity to accumulate for new reported cases would be `dN_EI` (newly infectious individuals) or `dN_SE` (newly exposed).

### 3. Stochastic Model Equations Inconsistent with Implemented Code

The displayed system of stochastic difference equations (the "Adding stochasticity to compartment transitions" section) does not match the C-snippet that is actually used. Specifically:

- The written equations show `dw(t)` appearing only in the S→E transition, but the continuous-time equations above that show it multiplied only in certain terms.
- The C-snippet uses `foi = (Beta - Beta_t*(t-1952)) * I / N` and then `dN_SE = rbinom(S, 1 - exp(-dw * foi * dt))`, which is not identical to any of the two earlier ODE formulations presented.
- The redundant earlier R-code versions of `seir_step` (the non-Csnippet versions) define `H` as accumulating `dN_IR`, and the final C-snippet continues this error, yet the mathematical write-up never clearly states which formulation was ultimately used.

### 4. Population Size Is Fixed at the 2023 Value Throughout the Entire 1953–2020 Period

`N = 333,000,000` (U.S. population circa 2023) is used as a fixed constant for a dataset spanning 1953–2020, during which the U.S. population grew from roughly 160 million to 330 million. The authors themselves flag this as a limitation ("Further Investigation"), but its impact on every estimated parameter (particularly `Beta`, `rho`, and the initial state fractions) is severe and never quantified. Using the 2023 population for 1953 data inflates per-capita rates by roughly a factor of two.

### 5. Implausible Biological Parameter Values — Not Interpreted or Validated

The reported best-fit parameters include:

- `mu_EI = 1.293220e+02` — an exposed-to-infectious rate of ~129 per year, implying an average latency period of about 3 days. TB latency is typically weeks to months (or years in the latent form); a value near 1–12 per year would be realistic.
- `mu_RS = 3.384936e+01` — a loss-of-immunity rate of ~34 per year, implying average immunity duration of about 11 days. This is biologically implausible for TB.
- `mu_IR = 8.155015e-01` — an infectious-to-recovery rate of ~0.82 per year, implying an average infectious period of ~14.7 months. This is within plausible range for treated TB but on the long end.

None of these values are compared to published epidemiological estimates or justified on biological grounds. The parameter estimates appear to be numerical artifacts of the poorly initialized single local search.

### 6. Measurement Model Applied to Raw Case Counts but H Is Not Reset (accumvars)

`H` is listed in `accumvars = 'H'`, meaning it is reset to zero at each observation time. Given that `delta.t = 1/52` (weekly steps) and observations are annual, `H` accumulates `dN_IR` over 52 steps between resets, so the measurement model uses the annual sum of recoveries. This is coherent with annual observations only if `H` is actually counting the right quantity. However, since `H` accumulates `dN_IR` (recoveries) rather than new infections, the fundamental error in point 2 propagates here as well.

### 7. No Likelihood Profile, Confidence Intervals, or Uncertainty Quantification for POMP Parameters

After the single `mif2` run, no particle filter evaluation (`pfilter`) is run to obtain a proper log-likelihood estimate, no replicated `mif2` runs are shown, and no likelihood profiles or confidence intervals are constructed for any parameter. The reported log-likelihood of `-628.8447` appears to come from `logLik(mif_out)`, which returns the filter mean log-likelihood from the last mif2 iteration — a noisy estimator. A dedicated `pfilter` call with more particles would be needed to get a stable likelihood estimate.

### 8. ARIMA Model Selection Conflates Number of Cases with Rate

In the ARIMA section, `model_selection_table` is called on `tb_num` (the raw count of TB cases), but the AIC table caption says "AIC of some ARIMA models (incidence number)" while the smallest-root table caption says "Smallest roots of ARIMA models (incidence rate)." These captions are inconsistent. More importantly, the variable used for ARIMA is the raw case count, not the rate, yet Figure 2 displays the rate. Using raw counts without any population normalization means the ARIMA model partially captures population growth rather than pure disease dynamics.

---

## Minor Weaknesses

### 9. Broken Image Path in the Report

The SEIRS diagram is referenced as:

```
<img src="/Users/shreya/Desktop/Winter/stats_531/PROJECT2/seirs_draw.png" ...>
```

This is an absolute local path on the original author's machine and will fail for any other reader. The image would not render in the HTML output. Figures that are central to the model description should either be embedded as base64 or placed in the project directory and referenced with a relative path.

### 10. The ARIMA Section Runs Simulated CI Code That Is Never Defined

The `model_selection_table` function references `simulation_arima` and `simulation_sarima` functions inside its body, but these functions are never defined anywhere in the Rmd. The call uses `simulation_times = 0` to avoid invoking them, which hides the error, but the code as written would fail if `simulation_times > 0`. This leaves a key part of the model diagnostic workflow non-functional.

### 11. Incorrect Fisher Confidence Interval Formula

In the `model_selection_table` function, the Fisher confidence interval is computed as:

```r
fisher_ci_low <- pc_model$coef - 1.96 * diag(pc_model$var.coef)
fisher_ci_high <- pc_model$coef + 1.96 * diag(pc_model$var.coef)
```

`diag(pc_model$var.coef)` returns the variances, not the standard errors. The standard errors are `sqrt(diag(pc_model$var.coef))`. As written, the confidence intervals are incorrect, and any conclusions drawn from them about whether coefficients are significant are unreliable.

### 12. No Convergence Diagnostics for the mif2 Run Are Interpreted

A `plot(mif_out)` call is made to display convergence traces, but the output is shown without any interpretation. The text does not discuss whether parameters have converged or whether the likelihood is still increasing, making it impossible to judge the quality of the optimization.

### 13. Simulation Plot Lacks Proper Legend and Reference to Actual Data

The simulation plot (the `ggplot` comparing 5 simulated trajectories to actual data) uses `color = .id == "data"` and `guides(color = "none")`, removing the legend. The actual data line is visually indistinguishable in the report text (the authors describe a "cyan line" but the rendering depends on the theme defaults). A proper legend explicitly labeling the data vs. simulated trajectories should be provided.

### 14. Duplicate and Redundant Code Blocks

The `seir_step` and `seir_rinit` functions are defined twice: once as plain R functions and once as C-snippets. The earlier R-function definitions are then silently overwritten. This creates confusion about which version of the model is actually being used and clutters the writeup. The intermediate R-function SEIR model (`TBseir`) is constructed but never actually fitted or used in any analysis after the C-snippet version (`TBseir_C`) is defined.

### 15. Data Has Missing/Anomalous Rows That Are Not Addressed

The raw CSV file contains anomalous year entries such as `"1974 2"` and `"1979 3"` (apparently footnote references embedded in the year field), and missing-value tokens `"––"` and `"—"` scattered across multiple columns. The cleaning code strips some of these, but the handling of `"1974 2"` and `"1979 3"` as year values is not discussed — these rows would parse to `NA` after `as.integer(Year)` and would be silently dropped. The report does not acknowledge the missing 2020 death data (`"––"` in several fields for the last row), nor does it note whether this has any effect on the analysis.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project14/TB_data_usa.csv`
