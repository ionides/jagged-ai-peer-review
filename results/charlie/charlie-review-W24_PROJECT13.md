# Peer Review: W24 Project 13
## Taiwan COVID-19 SIQRIQR POMP Analysis

---

## Summary

This project analyzes Taiwan's COVID-19 pandemic data in two phases, using SARIMA models for both phases and an SIQRIQR (Susceptible-Infected-Quarantined-Recovered, with reinfection) POMP model specifically for the second (Omicron) wave. The authors motivate the two-compartment infectious disease structure by citing Taiwan's strict quarantine policy and the biological possibility of reinfection across two strains. The project includes a local and global parameter search using `mif2` with `Np=2000` and `Nmif=50`.

Key strengths include a clearly motivated epidemiological model, use of a negative binomial measurement model, and a working global search across a reasonable parameter range. However, the analysis suffers from critical code defects that render the R-implementation version of the step function non-executable, an undeclared/unused parameter (`Beta_or`) in the Csnippet, hard-coded absolute file paths, absence of any quantitative goodness-of-fit comparison against a non-mechanistic benchmark, no profile likelihoods or confidence intervals for any parameter, and insufficient computational effort (Nmif=50 with no convergence justification). These issues substantially undermine confidence in all reported results.

---

## Major Issues

### 1. Non-functional R prototype step function uses undefined variables

In the R-language version of `siqriqr_step` (lines 448-467), the state update for `S` references `dN_SE_o` and `dN_SE_b` (line 459), which are never defined anywhere in the function. The function computes `dN_SI_o` and `dN_SI_b` but then uses different, non-existent variable names in the update. Similarly, lines 454-457 use `dt` as the time-step variable, but the function signature at line 449 names it `delta.t`. This prototype is broken and non-executable, meaning no one can verify its logic. While the Csnippet version (lines 504-522) does not share these exact bugs, the R prototype is also submitted as part of the code and cannot be relied upon for reasoning about model correctness.

### 2. Parameter `Beta_or` declared but never used in the Csnippet or described in the model

`Beta_or` appears in `paramnames` (lines 552-554), in the initial parameter vector (lines 559-560, 576-578), in `partrans` (line 584), and in `rw.sd` (line 599), yet it does not appear anywhere in the Csnippet body (lines 504-522) and is not mentioned in the model equations or verbal description. This is a declared but dead parameter: it is being estimated but plays no role in the dynamics. Its presence inflates the effective parameter count, distorts the optimization geometry, and makes results uninterpretable. This is a concrete model misspecification.

### 3. Infection force in the Csnippet is driven by Q (quarantined), not I (infectious)

Both `dN_SI_o` (line 505) and `dN_SI_b` (line 509) in the Csnippet use `Q_o/N` and `Q_b/N` as the infection force, i.e., transmission is driven entirely by the quarantined population. This is epidemiologically backwards: quarantined individuals are specifically those who have been isolated and cannot transmit. The infectious populations `I_o` and `I_b` do not appear in the infection force at all. Similarly in the R prototype (line 451). This structural error means the model does not represent the intended dynamics and all estimated transmission parameters (`Beta_o`, `Beta_b`, `Beta_r`) are uninterpretable.

### 4. No benchmark comparison against a non-mechanistic model

The POMP model is never compared to any non-mechanistic statistical baseline. The SARIMA models fit to the second wave are not used as a quantitative benchmark; the paper only notes informally that the SARIMA fit for wave two is poor. There is no log-likelihood or AIC comparison between the POMP model and any ARMA or negative-binomial autoregressive benchmark. As Wheeler et al. (2024) note, none of the reviewed Haiti cholera models performed such a comparison, and their benchmark revealed that some mechanistic models failed to outperform a simple statistical model. Without this comparison, it is impossible to assess whether the SIQRIQR model captures meaningful epidemiological structure.

### 5. No profile likelihoods or confidence intervals reported

No profile likelihoods are computed for any parameter, and no confidence intervals (e.g., via MCAP) are reported anywhere in the paper. The pairs plots from the local and global searches are the only characterization of parameter uncertainty, and these do not provide inferential guarantees. Several parameters, including `eta` (acknowledged not to converge in the local search at line 630), `Beta_or` (dead parameter), and the rates `mu_QR_o`, `mu_QR_r`, `mu_QR_b` (fixed without sensitivity analysis), are not given any uncertainty characterization. As Wheeler et al. (2024) note in their identifiability section, missing profile likelihoods make it impossible to determine whether parameters are identifiable from the data.

### 6. Insufficient computational effort with no convergence justification

The global search uses `Nmif=50` and `Np=2000` for a model with 8 free parameters and a 174-day time series. The convergence traces shown do not provide evidence that 50 iterations are sufficient; the paper acknowledges that the log-likelihood has not converged ("it may need more particles or iterations," line 684). The local search uses `%do%` (sequential, not parallel), so 20 replicates run serially, further limiting effective exploration. No sensitivity analysis of particle count or iteration count is provided. This means the reported maximum log-likelihoods may be far from the true MLE, undermining all downstream conclusions (Wheeler et al. 2024, computational adequacy).

### 7. Hard-coded absolute path prevents reproducibility

Line 394 contains `read_csv(paste0("C:/Users/USER/Desktop/Time Series Analysis/Projects/TW_last_days.csv"))`. This path is specific to the authors' Windows machine and will fail on any other system. Although `TW_last_days.csv` is included in the project folder, the code does not use a relative path to read it, meaning the project cannot be reproduced without manual path editing. Per the code supplement checklist, hard-coded absolute paths to the author's local filesystem are a reproducibility red flag.

### 8. Three rate parameters fixed without justification or sensitivity analysis

`mu_QR_o`, `mu_QR_r`, and `mu_QR_b` (quarantine-to-recovery rates) are placed in `fixed_params` (line 635) and excluded from both the local and global search. The values 0.03, 0.05, and 0.01 (lines 576-578) are asserted without citation or biological justification. No sensitivity analysis examines whether results change under different fixed values. Fixing these parameters without justification may substantially affect estimated transmission rates and reported log-likelihoods. Wheeler et al. (2024) note that initial condition and fixed-parameter choices can shift AIC by tens of units.

---

## Minor Issues

### 9. Accumulator variable `H` tracks recoveries, not case reports

The measurement model (`dmeas`) links `reports` to `rho*H`, where `H` accumulates `dN_QR_o + dN_QR_b` (lines 521, 466) - i.e., transitions from quarantine to recovery. However, the observed variable is daily new confirmed cases, which should correspond to newly entering quarantine (`dN_IQ_o + dN_IQ_b`), not leaving it. A delay introduced by routing observations through the quarantine compartment may affect parameter estimates, particularly the rates `mu_IQ` and `mu_QR`. This inconsistency should be explicitly justified or corrected.

### 10. Ad hoc impulse at t=125 is undocumented and unjustified

Line 513 introduces `if (t == 125) e = 100;` which adds 100 individuals to `I_b` at day 125. This is an undocumented impulse with no explanation in the text, no citation, and no sensitivity analysis. Day 125 of the 174-day second-wave window corresponds to approximately late August or September 2022. There is no discussion of what epidemiological event this is meant to represent. Such an ad hoc intervention can substantially distort the inference if the optimizer simply exploits it.

### 11. Model state inconsistency: `R_b` described twice, `R_o` description missing

In the model description (lines 422-432), `R_b` is listed twice - once as "people who have recovered from the beta variant" and once more at the end of the list with the same label. `R_o` (recovered from Omicron) is never defined in the verbal description despite appearing in the state vector and step function. This is a notation/documentation inconsistency that undermines the clarity of the model specification.

### 12. SARIMA model identified as WARIMA(4,1,1) but auto.arima returns different orders

The text states (line 207) that the first approach (`auto.arima`) suggests WARIMA(4,1,1), while the AIC table approach suggests (3,1,5). But later (line 310) the inverse root plot is described as being for the "(4,1,1) model for the first phase," while line 318 states "our model is a WARIMA(3,1,2)". It is unclear which model is ultimately used for the second wave and why. The AIC comparison table only covers the first wave's data. No AIC table is presented for the second wave.

### 13. Stationarity claims are inconsistent with SARIMA assumptions

The text (lines 106-107) states the differenced data shows "mean stationarity" but that "strict stationarity is unlikely" due to heteroskedastic variance. The authors then proceed to fit SARIMA models that assume homoskedastic, normally distributed errors. The QQ plot deviations are noted but dismissed without testing (e.g., no Ljung-Box or ARCH test). The decision to continue with SARIMA despite acknowledged non-normality and heteroskedasticity is not adequately justified.

### 14. `loglik > max(loglik) - 1000` filter is too permissive

Line 679 filters the global search results to include runs within 1000 log-likelihood units of the maximum. For a 174-observation model, a window of 1000 log-likelihood units is extremely wide and includes virtually all runs regardless of quality. A threshold of 10-20 units is standard (corresponding roughly to a factor of e^10 in likelihood). This permissive filter means the pairs plots in the global search summary may not actually reflect the geometry near the MLE.

### 15. No model diagnostics or forward simulation comparison to data

After the global search, there is no figure comparing forward simulations from the best-fit parameters to the observed data for the POMP model. The only simulation comparison shown is from the initial guesses (lines 557-568), before any fitting. Post-fitting, the analysis jumps directly to pairs plots of parameter estimates. No conditional log-likelihoods, ESS traces, or filtering-distribution plots are provided, making it impossible to assess where the model fits well or poorly (Wheeler et al. 2024, model diagnostics).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project13/TW_last_days.csv`
