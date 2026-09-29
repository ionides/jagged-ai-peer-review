# Peer Review: W24 Project 13

**Semester:** Winter 2024
**Project:** 13 — COVID-19 in Taiwan: SARIMA and SIQRIQR POMP Model

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) + replicated pfilter |
| **R packages used** | pomp, forecast, ggplot2, doFuture, tidyverse |
| **Code publicly available** | Partial — data loading uses a hard-coded local path |
| **Data publicly available** | Partial — primary data from Google COVID-19 Open Data API; second-wave CSV is a local file |
| **Benchmark comparison included** | No — visual comparison only, no quantitative comparison of ARIMA vs. POMP likelihoods |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2 + replicated pfilter with logmeanexp; correct aggregation method used |
| 2 | Benchmark comparison | ✗ | SARIMA and POMP likelihoods not compared on the same scale |
| 3 | Quantitative goodness-of-fit reporting | ~ | Top-10 loglik tables printed but not discussed relative to any baseline |
| 4 | Model diagnostics | ✗ | No conditional log-likelihoods, no ESS monitoring; simulation plots shown but no quantitative fit assessment |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods, no confidence intervals; non-convergence of eta acknowledged but not addressed |
| 6 | Computational adequacy | ~ | Nmif=50, Np=2000 for both local and global searches; borderline for a 13-parameter model |
| 7 | Forecast methodology | N/A | No forecasts presented |
| 8 | Model variations and nested comparisons | ✗ | Single SIQRIQR model only; no alternative structures tested |
| 9 | Stochasticity | ✓ | Binomial transitions throughout; negative binomial measurement model |
| 10 | Reproducibility and extendability | ✗ | Hard-coded local path; TW_last_days.csv not archived; no sessionInfo() |
| 11 | Corroboration with scientific knowledge | ~ | Parameter estimates printed but not compared to known COVID-19 natural history |
| 12 | Measurement model specification | ✗ | Accumulator H tracks Q→R recoveries rather than I→Q (case detection) transitions; biological mismatch |
| 13 | Initial conditions | ~ | eta estimated; other initial compartments fixed (100 in Q_o at t=0) without justification |

---

## Summary

This project analyzes Taiwan's COVID-19 pandemic using a SARIMA model for the first wave (2021) and a custom SIQRIQR POMP model for the second wave (2022, Omicron). The SIQRIQR model extends the standard SIR framework by adding quarantine compartments and allowing reinfection by a second strain, motivated by Taiwan's notable quarantine policy. The authors conduct both local and global mif2 searches, use logmeanexp for likelihood aggregation, and select a negative binomial measurement model.

**Strengths:**
- Creative compartmental model design that incorporates quarantine dynamics and dual-strain reinfection
- Correct use of logmeanexp for aggregating replicated particle filter likelihoods
- Negative binomial measurement model appropriately handles overdispersion
- Both local and global parameter searches are conducted
- Biological motivation for the model structure is clearly explained

**Weaknesses:**
- The rprocess uses the force of infection from quarantined (Q) rather than infectious (I) compartments — a fundamental model specification error
- The accumulator variable H tracks Q→R recoveries rather than I→Q case-detection transitions, creating a systematic mismatch between model output and the data being fit
- A hard-coded local Windows file path makes the POMP section entirely non-reproducible
- An undocumented event injection (100 individuals inserted at t=125) is not scientifically justified
- No profile likelihoods or confidence intervals are computed for any parameter
- No quantitative comparison between SARIMA and POMP models

---

## Major Issues

### 1. Force of infection uses quarantined rather than infectious compartments

The rprocess Csnippet specifies:

```
double dN_SI_o = rbinom(S, 1-exp(-Beta_o*Q_o/N*dt));
double dN_SI_b = rbinom(S-dN_SI_o, 1-exp(-Beta_b*Q_b/N*dt));
```

The force of infection is `Beta_o * Q_o / N` and `Beta_b * Q_b / N`, meaning quarantined individuals drive new infections. This is biologically backward: quarantined individuals are isolated and removed from community contact. The infectious source should be the `I_o` and `I_b` compartments. As specified, individuals can only be infected by people who have already been detected and removed from circulation, while the truly infectious undetected individuals (I compartments) infect no one. This inverts the intended epidemiological logic and will produce model dynamics that bear no meaningful relationship to the process being described.

**Fix:** Change the force of infection to use `I_o` and `I_b`, respectively: `Beta_o * I_o / N * dt` and `Beta_b * I_b / N * dt`.

---

### 2. Measurement accumulator tracks recoveries rather than new case reports

The accumulator variable is updated as:

```
H += (dN_QR_o + dN_QR_b);
```

This accumulates individuals transitioning from quarantine to recovery (Q→R). However, the observed data (`reports`) represents new confirmed COVID-19 cases, which correspond to the moment of detection and quarantine entry (I→Q transitions). The correct accumulation is `dN_IQ_o + dN_IQ_b`. Using Q→R introduces a systematic temporal displacement between modeled and observed case counts equal to the average quarantine duration. This mismatch distorts all parameter estimates, particularly the transmission rates.

**Fix:** Change to `H += (dN_IQ_o + dN_IQ_b)`.

---

### 3. Hard-coded local file path makes POMP analysis non-reproducible

The POMP section loads data with:

```r
read_csv(paste0("C:/Users/USER/Desktop/Time Series Analysis/Projects/TW_last_days.csv"))
```

This path cannot be resolved by any reader. The `TW_last_days.csv` file is included in the project submission directory but the path is not relative. This means the entire POMP analysis — the model definition, all local and global searches, and all results — cannot be reproduced by any reader. This is a reproducibility failure documented in the code-supplement checklist.

**Fix:** Use a relative path (`read_csv("TW_last_days.csv")`) consistent with the file's location in the project directory.

---

### 4. Undocumented ad-hoc event injection at t=125

The Csnippet contains:

```c
double e = 0;
if (t == 125) e = 100;
...
I_b += dN_SI_b + dN_RI_b - dN_IQ_b + e;
```

One hundred individuals are inserted into the I_b compartment at time step 125, with no justification in the text, no citation to an external event, no estimation of the magnitude, and no sensitivity analysis. This is a hard-coded intervention that directly manipulates the latent state rather than modeling an intervention as a parameter or covariate. The text describes the model as capturing "quarantine policy relaxation" but provides no connection between t=125 and any policy event. This approach is not a principled modeling technique and its influence on parameter estimates cannot be assessed.

**Fix:** Either remove this term, model the external event as an estimated parameter with a clear biological interpretation, or connect it to a covariate (e.g., a documented policy change date) and estimate its magnitude.

---

### 5. No profile likelihoods or confidence intervals

No uncertainty quantification is provided for any of the estimated parameters. The local search explicitly flags that eta "Does not seem to converge which is concerning," yet no follow-up analysis is performed. Profile likelihoods are not computed for any parameter, and no confidence intervals of any kind are reported. Without these, it is impossible to assess whether any parameter is identifiable from the data, and the printed point estimates from the global search cannot be interpreted. This also means there is no diagnostic for the convergence issue with eta. See Wheeler et al. (2024), Section on parameter identifiability.

**Fix:** Compute profile likelihoods for key parameters (at minimum Beta_o, Beta_b, rho, eta) using mif2 with the target parameter fixed at a grid of values.

---

### 6. Wrong seasonal frequency specification in ts() objects

The code uses:

```r
ts_data1 <- ts(tw_df_first$new_confirmed, frequency = 52)
ts_data2 <- ts(tw_df_second$new_confirmed, frequency = 52)
```

The data is daily, and the ACF analysis correctly identifies a 7-day (weekly) seasonal pattern. For daily data with weekly seasonality, the correct specification is `frequency = 7`. Using `frequency = 52` defines the seasonal period as 52 days, causing `auto.arima` to search for a 52-day seasonal cycle rather than the 7-day cycle documented in the EDA. The selected seasonal model orders from auto.arima are therefore based on an incorrect periodicity assumption, undermining the SARIMA analysis throughout.

**Fix:** Change both `ts()` calls to `frequency = 7`.

---

### 7. No quantitative benchmark comparison between SARIMA and POMP

The paper's stated goal is to "compare and contrast the performances of an ARIMA and POMP model," but this comparison is only visual. The SARIMA model is fit to the first wave; the POMP model is fit to the second wave. No common holdout period or common data segment is used to compare the two approaches on the same likelihood scale. The POMP log-likelihoods are printed in R output tables but never referenced in the discussion. Without a quantitative comparison — even an informal one noting the log-likelihood of a SARIMA model applied to the second-wave data — the stated comparative goal is not achieved.

**Fix:** Report the log-likelihood of the SARIMA model on the second-wave data and compare it to the POMP log-likelihood, acknowledging any differences in observation model when interpreting the comparison.

---

### 8. Broken R-language rprocess prototype

The R-language prototype `siqriqr_step` (used before the Csnippet implementation) contains multiple errors that prevent execution:

- Uses `dt` (undefined in this scope) instead of `delta.t` (the argument name declared in the function signature)
- Refers to `dN_SE_o` and `dN_SE_b` (undefined) instead of `dN_SI_o` and `dN_SI_b`
- `rbinom` calls are missing the `n=1` and `size=` argument names (e.g., `rbinom(R_o, 1-exp(...))` should be `rbinom(n=1, size=R_o, prob=1-exp(...))`)
- The function has no return statement and modifies only local variables

While the Csnippet implementation that follows is used for actual computations, including non-functional R code in the report creates confusion about the model specification and undermines the presentation.

**Fix:** Either correct the R prototype to be syntactically valid and consistent with the Csnippet, or remove it and present only the Csnippet with a clear mathematical description of the transitions.

---

### 9. Unused parameters in paramnames inflate complexity without contributing to dynamics

The `paramnames` argument lists `Beta_or` and `mu_QR_r`, but neither appears in the Csnippet rprocess. They are included in the initial parameter vector and in the rw.sd specification for mif2, meaning they are perturbed during iterated filtering without affecting model dynamics. This wastes computational budget on non-contributing parameters and adds noise to the optimization without benefit. The parameter `mu_QR_r` is described in the compartment list but never appears in the transition equations.

**Fix:** Remove `Beta_or` and `mu_QR_r` from paramnames and from the mif2 random walk specification, or incorporate them into the rprocess if they were intended to play a role.

---

### 10. No convergence diagnostics for global search; eta instability unresolved

The local search acknowledges that eta "does not seem to converge." The global search is described as providing "better convergence," but no trace plots are shown for the global runs. For the local search, trace plots are computed but the text discussion focuses on qualitative convergence without quantifying whether runs agree in their terminal log-likelihood values. The global search uses `Nmif=50` with `Np=2000` — a relatively low computational budget for a model with 8 free parameters. No evidence is presented that further iterations would not change the estimates substantially.

**Fix:** Show likelihood traces for the global search; report the spread in terminal log-likelihoods across global runs; increase Nmif to at least 100 and verify stability.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots are computed for the local search and shown in the report. However, convergence of the log-likelihood panel across runs is not explicitly assessed. Several parameters (notably eta and Beta_r) show visible spread without clear plateau. No trace plots are shown for the global search.

**Particle filter:** No ESS monitoring is performed or reported. The particle count is Np=2000, which is reasonable for a daily time series but not verified via sensitivity analysis. No evidence of filter degeneracy assessment.

**Conditional log-likelihoods:** Not computed. Per-observation log-likelihood plots would help diagnose whether the event injection at t=125 improves model fit at specific time points.

**Profile likelihoods:** Not computed. See Major Issue 5.

**Computational scale:** The local search is run sequentially (`%do%` rather than `%dopar%`). The global search uses parallel execution with Nseq=50 starting values. Total computation time is not reported.

---

## Reproducibility Assessment

**Code availability:** The Rmd file and TW_last_days.csv are included in the submission. However, the POMP section depends on a hard-coded Windows path. The data loading section for the ARIMA analysis fetches from a live API URL, which may not remain stable.

**Final parameters:** Top-10 parameter vectors from local and global searches are printed as R output. These are readable but not archived as standalone CSV or RDS files for direct re-use.

**Model-code consistency:** The measurement model specification (negative binomial via dnbinom_mu) is consistent between the text and code. However, the accumulator variable H measures Q→R rather than I→Q transitions, which is inconsistent with the stated interpretation that H measures new confirmed cases.

**Package versions:** No `sessionInfo()` output is provided. Package versions for pomp, forecast, and ggplot2 are not reported.

**Auxiliary data:** TW_last_days.csv is present in the submission directory, resolving the data dependency if the path is corrected.

**HPC reproducibility:** No cluster-based analysis; not applicable.

---

## Minor Issues

- The AIC table for the first wave searches non-seasonal ARIMA orders (`arima(data, order=c(p,1,q))`) without seasonal terms, but the paper's motivation is SARIMA. The table is not directly comparable to the `auto.arima` result, which includes seasonal structure.

- No residual ACF plot is shown for either SARIMA model. Only QQ plots and visual fits are presented. Ljung-Box test or residual ACF would be expected diagnostics.

- The compartment description contains two entries for $R_b$ (lines 419 and 430 of the Rmd) and omits $R_o$. The text also states "O denotes beta" for $I_b$, which is a copy-paste error (should read "b denotes beta").

- Causal language is used throughout ("assess the effectiveness of government policies") without a causal identification strategy. The POMP model describes association and dynamics, not causal effects of policy interventions.

- Typos: "fous" (→ "focus"), "dtrains" (→ "strains"), "acll" (→ "call"), "Futhermore" (→ "Furthermore").

- No `sessionInfo()` output or package version documentation is included anywhere in the report.

- The initial condition places 100 individuals in Q_o at t=0 without justification. Given the force-of-infection error (Issue 1), this means Q_o is the sole driver of transmission, so the initial value of Q_o functions as the seed for the entire epidemic. Sensitivity to this choice is not explored.

---

## Recommendation

**Major Revision — with core model re-specification required.**

The two fundamental model errors (force of infection driven by quarantined rather than infectious individuals; accumulator variable measuring recoveries rather than case detections) mean that the SIQRIQR analysis as presented does not model the intended epidemiological process. All parameter estimates and conclusions from the POMP section are derived from a misspecified model and should not be interpreted. These issues, together with the non-reproducible local file path and the undocumented state injection, represent the minimum revisions required before the analysis can be evaluated. Profile likelihoods and a quantitative SARIMA–POMP comparison are also necessary for the paper's stated goals to be achieved.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project13/TW_last_days.csv`
