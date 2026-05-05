# Peer Review: W22 Project 04
## "An Analysis on COVID-19 Omicron Variant in Washtenaw"

---

## Summary

This project models daily COVID-19 case counts in Washtenaw County, Michigan, from December 2021 through April 2022 using a SARIMA model and a custom recurrent SEPIR POMP model. The SEPIR model extends the standard SEIR framework to allow reinfection (R → S) and to separate asymptomatic (P) from symptomatic (I) infected individuals, capturing two features of Omicron biology. While the scientific motivation for the model is sound and the computational effort is substantial (Np = 5000 with replicated pfilter evaluation using logmeanexp), the implementation contains critical bugs in the latent process equations that undermine the validity of all fitted results. Several major methodological gaps — no profile likelihoods, no non-mechanistic benchmark, many key parameters fixed ad hoc — also weaken the conclusions.

---

## Major Issues

### 1. Critical bug: `dN_RS` drawn from I instead of R

**Location:** `sepir_step` Csnippet, line `double dN_RS = rbinom(I, 1-exp(-mu_RS*dt));`

The R → S transition is drawn from compartment I (symptomatic infected) rather than compartment R (recovered). This is a fundamental error: individuals are being removed from I at rate `mu_RS` via this draw, instead of from R. As a result:

- I is depleted by three separate outflows (recovery `dN_IR`, the correctly computed draw, plus this spurious draw `dN_RS`) even though only two outflows are subtracted from I in the update equations.
- R accumulates indefinitely because it is increased by `dN_PR + dN_IR` but never decreased (see Issue 2 below).
- The R → S reinfection mechanism — the core scientific motivation for this model — does not function as intended.

All fitted parameters and simulated trajectories are based on this incorrect process. The bug invalidates the biological interpretation of the SEPIR model.

**Fix:** Change `rbinom(I, ...)` to `rbinom(R, ...)` for `dN_RS`.

---

### 2. Critical bug: R compartment never decreases; population conservation violated

**Location:** `sepir_step` update equations, line `R += dN_PR + dN_IR;`

Although `dN_RS` is computed (albeit from the wrong compartment), R is never decremented by it. The update `R += dN_PR + dN_IR` has no corresponding subtraction of `dN_RS`. Consequently:

- R grows monotonically over time, absorbing all recovered individuals but never returning them to S.
- The total population S + E + P + I + R does not remain constant: individuals are removed from I by the spurious `dN_RS` draw and added to S via `S -= dN_SE - dN_RS` (which correctly adds `dN_RS` to S), but the corresponding decrease from R never occurs.
- The reinfection pathway (R → S) is completely absent from the model dynamics despite being stated as the key motivation.

**Fix:** Add `R -= dN_RS;` after the `dN_RS` computation, and correct the source compartment to R (Issue 1).

---

### 3. Critical bug: accumulator H tracks recoveries, not new infections entering I

**Location:** `sepir_step`, line `H += dN_IR;` and `dmeas`/`rmeas` using `rho*H`

The accumulator H is incremented by `dN_IR` — individuals transitioning from I to R (recoveries) — rather than by the count of individuals newly entering I. The measurement model then predicts `reports ~ Normal(rho*H, ...)`, meaning it models observed cases as a fraction of recoveries in each time step, not newly symptomatic individuals.

This is semantically incorrect: reported confirmed cases correspond to newly diagnosed/symptomatic individuals, which maps to the I → I inflow (`nearbyint((1-alpha)*dN_EPI)`), not to I → R outflow. Because the mean recovery time from COVID-19 is multiple days, lagging the accumulator by the recovery duration introduces a systematic temporal offset in the measurement model.

**Fix:** Replace `H += dN_IR;` with `H += nearbyint((1-alpha)*dN_EPI);` to accumulate new symptomatic infections.

---

### 4. `eta` missing from parameter transformation; perturbed on the natural scale

**Location:** `parameter_trans(log=c(...), logit=c("rho","alpha"))` — `eta` is absent

`eta` (the initial susceptible fraction) is used in `rinit` as `S = nearbyint(eta*N)` and therefore must lie in [0, 1]. However, it is not included in the `logit` transformation list. During mif2, `eta` is perturbed on the natural scale (via `ivp(0.02)`) without constraint. If perturbations push `eta` outside [0, 1], `nearbyint(eta*N)` can produce invalid (negative or super-population) initial conditions. The parameter transformation should include `logit="eta"`.

---

### 5. No profile likelihoods computed for any parameter

**Location:** Summary section; no profile likelihood section present

No profile likelihood curves are computed for any parameter. Without profiles, it is impossible to determine:
- Whether any parameter is identifiable from the data
- What confidence intervals should be reported
- Whether the MLE is well-defined

This is especially critical given that five parameters (`mu_PR`, `mu_IR`, `alpha`, `Beta`, and later `mu_RS`) are fixed at ad hoc values without statistical justification. Profile likelihoods for at least the key biological parameters (e.g., `rho`, `mu_EPI`, `beta`) are the minimum standard for this course. See Wheeler et al. (2024), §Parameter identifiability and uncertainty.

---

### 6. Many biologically important parameters fixed without statistical justification

**Location:** Code blocks defining `fixed_params` and `fixed_params2`

The parameters `mu_PR`, `mu_IR`, `alpha`, and `Beta` are fixed throughout both local and global search. In the global search, `mu_RS` is additionally fixed at a value obtained from local search (1.529 per day, implying reinfection within less than 1 day, which is biologically implausible for COVID-19 immunity loss). No literature values are cited for these rates, no sensitivity analysis is performed, and no justification is given for why these specific values are held constant. Fixing parameters that are not identifiable is legitimate, but that determination requires profile likelihoods (Issue 5). The ad hoc choice of which parameters to fix undermines the scientific interpretation of fitted estimates.

---

### 7. No non-mechanistic benchmark comparison

**Location:** Summary section

The paper concludes that "POMP model can explain the data better" than SARIMA but provides no quantitative comparison. The SARIMA AIC and the POMP log-likelihood are reported in separate sections without conversion to a common scale, and the claim that POMP is superior is unsupported. A log-likelihood comparison between the best POMP fit (−768) and a comparable ARMA/IID model fit would quantify whether the mechanistic structure adds explanatory power. See Wheeler et al. (2024), §Benchmark comparison; Error 1.6 (CC-Yes).

---

### 8. Insufficient number of global search replicates

**Location:** Global search code: `foreach(i=1:10, .combine=c)`

Only 10 global search replicates are run. For a model with 9 free parameters (b1–b5, mu_EPI, rho, eta, tau) optimized over a broad box, 10 replicates is unlikely to adequately explore the parameter space and provide evidence of convergence to the global maximum. The course standard for run_level=3 is Nreps_global = 100. The pairs plots show some clustering, but with only 10 points it is difficult to assess whether the highest-likelihood region has been reliably identified.

---

### 9. Typographical error in model description: $I_t$ defined twice

**Location:** POMP model section, bullet point list of state variables

The list defines $I_t$ twice: once as "the number of people at time $t$, who have been infected and are showing symptoms" and again as "the number of recovered at time $t$." The second definition should read $R_t$. This is a presentational error that creates confusion about the model structure.

---

## Minor Issues

### 10. AIC comparison between SARIMA and POMP not addressed

**Location:** Summary section — "both of two models can fit the data well"

The SARIMA model has AIC ≈ (not explicitly stated but implied by model selection table) and the POMP model achieves log-likelihood −768. The paper does not attempt to compare these on a common scale. While AIC and POMP log-likelihoods are technically comparable for the same data (see 531-conventions.md), the paper makes no such attempt and simply asserts that both fit "well." A formal comparison or at minimum a discussion of why direct comparison was not made would strengthen the conclusion. (Error 2.2, CC-Yes)

### 11. Spectral frequency/period calculation not shown

**Location:** Seasonality section — "an approximately seven days (1/0.13) period"

The authors read 0.13 cycles per day from the spectral density plot and invert it to claim a 7-day period (1/0.13 ≈ 7.7, not exactly 7). The spectral plot x-axis units are not clearly labeled, and the identification of 0.13 as the dominant frequency is not documented. The calculation should be shown explicitly with units.

### 12. Convergence of `mu_EPI` acknowledged but not addressed

**Location:** Model Fit Analysis section — "Parameter mu_EPI might have some convergence problem"

The authors note that `mu_EPI` shows poor convergence in trace plots but proceed without any remediation. A parameter with convergence problems either requires a wider search box, a different parameterization, or should be fixed. Simply noting the problem and ignoring it is insufficient.

### 13. Initial conditions for E, I, P fixed without justification

**Location:** `sepir_init` Csnippet — E = 100, I = 200, P = 50

E, I, and P are fixed at arbitrary round numbers (100, 200, 50) rather than estimated as parameters or initialized from data. For a pandemic in rapid growth phase at the model start date (December 1, 2021), the initial infected counts substantially affect the early trajectory. No sensitivity analysis to these values is presented. This issue is less critical than the code bugs but warrants acknowledgment.

### 14. Residual diagnostics for SARIMA model are not interpreted fully

**Location:** SARIMA section — "the Q-Q plot indicates that the residuals do not follow normal distribution. Nevertheless, we have to admit that the data around the peaks are hard to fit and our SARIMA model generally performs well."

The non-normality of residuals and the large residuals near peaks are acknowledged but dismissed without further investigation. No Ljung-Box test is reported. The ACF of residuals is not checked. Given the obvious non-normality, a log-transform of case counts before SARIMA fitting would be worth exploring (Error 2.5, CC-Yes).

### 15. The intervention period indicator leaves a gap at time step 35

**Location:** `intervention_indicator` loop — the condition uses `i>35` for period 4, skipping i=35

The loop assigns `intervention_indicator[i] = 4` only for `i>35 & i<=41`, meaning time step 35 itself is unassigned (retains its initialized value of 0, which falls into the `else` branch using base `Beta`). Whether this is intentional is unclear, but it produces a one-day anomaly in the intervention schedule that is not discussed.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project04/omicron.c`
