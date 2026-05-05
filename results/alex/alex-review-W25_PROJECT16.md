# Peer Review: W25 Project 16 — Analyzing Whooping Cough with ARMA and POMP

---

## Summary

This project analyzes weekly whooping cough (pertussis) case counts in the East North Central states (Michigan, Ohio, Indiana, Illinois, Wisconsin) from 2017 to early 2025, using ARMA/ARCH models and POMP-based SIR/SEIR compartmental models. The dataset contains a prominent 2024 outbreak alongside substantial missing data (all of 2022, much of 2021). The project compares ARCH and SEIR model log-likelihoods to draw conclusions about relative fit. Below are up to 15 weaknesses, ordered from most to least critical.

---

## Weaknesses

### 1. MAJOR — Log-likelihood comparison between ARCH and SEIR is not valid

The authors directly compare log-likelihoods across the ARCH model (–1203) and the SEIR model (–1442), concluding that ARCH is superior. However, these two models are not comparable by log-likelihood: the ARCH model is fit on the **differenced** series (scalar real-valued observations), while the SEIR model is fit on the **raw count** series (non-negative integers modeled via negative binomial). The observation spaces, data transformations, and distributional families are fundamentally different, making the log-likelihood values non-commensurable. Even acknowledging the Jacobian argument mentioned at the end of the comparisons section is insufficient, because the differencing step changes the effective data dimension and the likelihood scaling in ways that are not transparent. No AIC or formal likelihood ratio framework is applied to justify the comparison. The authors partially acknowledge this but still conclude that ARCH is superior.

### 2. MAJOR — Missing data handled by interpolation with no sensitivity analysis

Over two full years of data (all of 2022, most of 2021) are missing. The ARMA section uses `data/interpolated_cases.csv` rather than the raw `data/all_data.csv`. The method of interpolation is never described anywhere in the writeup—there is no explanation of what interpolation technique was used, no discussion of whether it is appropriate, and no sensitivity analysis. Any ARMA model fit or residual diagnostic drawn from this interpolated series inherits unknown assumptions that could substantially affect results, particularly given that the missing period spans more than 25% of the data.

### 3. MAJOR — SEIR model fails to reproduce the 2024 outbreak; root cause not diagnosed

The global SEIR search (log-likelihood –1471) produces simulations that "fail to capture the surge in reported whooping cough cases." The authors acknowledge this but do not provide a detailed diagnosis. In particular, the model uses a step-function beta that switches at a manually chosen date (week 332, April 7, 2024), yet the parameters obtained (base_beta and outbreak_beta on a [0, 25] uniform prior) are not interpreted biologically or compared to literature values for pertussis. The pairs plot from the global search is commented out in the code, preventing readers from assessing identifiability of the six free parameters. The failure of the SEIR model is treated as a finding rather than investigated.

### 4. MAJOR — k (overdispersion parameter) is fixed throughout all POMP models without justification

The negative-binomial dispersion parameter `k` is fixed at 10 (SIR) and 5 (SEIR) and excluded from all local and global searches (it appears only in `fixed_params = coef(coughSEIR, c("N","k"))`). No justification is given for these specific values, no likelihood profile over k is provided, and the sensitivity of results to k is never examined. For count data with extreme overdispersion (such as pertussis outbreaks), k has a large impact on model fit and identifiability of other parameters.

### 5. MAJOR — H accumulator tracks recoveries (N_IR), not infections; measurement model is inconsistent

In the SIR step snippet, `H += dN_IR` — H accumulates transitions from I to R, i.e., recoveries. The measurement model then uses `rho * H` as the mean of reported cases. For whooping cough, reported cases are newly infected individuals, not newly recovered ones. In a standard SIR POMP model for case reporting, H should accumulate `dN_SI` (new infections) or `dN_EI` (new infectious individuals in SEIR). Accumulating recoveries as a proxy for reports is biologically incorrect and leads to a systematic phase shift in the modeled case curve.

### 6. MAJOR — ADF/stationarity test mentioned in the bibliography but never performed or reported

The bibliography contains a reference to "Tests for Stationarity in Time Series—Dickey Fuller Test" (`{ADF}`), yet no ADF test result appears anywhere in the document. The ARMA section proceeds directly to differencing without a formal stationarity test. This is especially important given the pronounced non-stationarity suggested by the 2024 outbreak: differencing alone may not be adequate, and the choice of d=1 should be supported.

### 7. MAJOR — ARCH model comparison to ARMA(2,4) uses mismatched sample sizes

The ARCH model is fit on `pertussis_diff[-1]` (one additional observation removed to align the lagged exogenous regressor), giving a sample of length n–2, while the ARMA(2,4) log-likelihood is computed on `pertussis_diff` of length n–1. The log-likelihood table directly tabulates these two values and concludes ARCH is better. The different effective sample sizes mean even same-model log-likelihoods are not directly comparable.

### 8. MODERATE — Global search box bounds for SIR are extremely wide and produce unidentifiable mu_IR

The SIR global search uses `upper=c(Beta=250, rho=0.9, mu_IR=60, eta=0.9)`. A mu_IR of up to 60 corresponds to a mean infectious period of less than half a day, which is biologically implausible for pertussis (typical infectious period is 1–3 weeks). The text notes that mu_IR cannot be identified, but no attempt is made to constrain the search to an epidemiologically plausible range, nor is a likelihood profile over mu_IR presented. The best-fit value from the SIR global search (mu_IR=6.92) corresponds to a mean infectious period of less than one day, which is inconsistent with pertussis biology.

### 9. MODERATE — Local MIF2 convergence claimed but trace plot interpretation is weak

The local search trace plots are shown, and the authors say "the log likelihoods are converging fairly well," but no quantitative criterion is applied. The number of MIF iterations (Nmif=50) is modest given six free parameters. No convergence diagnostics such as effective sample size (ESS) from the final particle filter or examination of whether all chains converge to the same region are reported.

### 10. MODERATE — rw.sd for beta uses `ifelse(whoop$week < 332, 0.02, 0)` which applies wrong perturbations

In the SEIR local search, `rw_sd(base_beta = ifelse(whoop$week < 332, 0.02, 0), outbreak_beta = ifelse(whoop$week > 332, 0.02, 0), ...)` perturbs `base_beta` only during the non-outbreak period and `outbreak_beta` only during the outbreak period, indexing by observation position rather than parameter type. The `rw.sd` argument in `mif2` should be a single scalar (or function of iteration) per parameter, not a vector keyed to observation time. This is a misuse of the `rw.sd` API and may produce silent errors or unexpected perturbation schedules.

### 11. MODERATE — Vaccination data from a single state (Michigan) extrapolated to five states without validation

Vaccination rates are sourced only from Michigan county immunization report cards and then assumed to apply uniformly to Ohio, Indiana, Illinois, and Wisconsin. No evidence is provided that Michigan's vaccination coverage is representative of the other four states. Vaccination rates can vary considerably across states, and the extrapolation is especially problematic for states with different demographics or public health policies.

### 12. MODERATE — The SEIR model initializes H=1 rather than H=0; residual accumulation contaminates the first measurement

In `seir_rinit`, `H = 1` is set at initialization rather than zero. Since H is an accumulator that should start empty at time t0 and be cleared each time step via `accumvars`, initializing H=1 means the very first observation is modeled against H=1 rather than H=0. This biases the measurement likelihood for the first observation.

### 13. MINOR — Deaths plot y-axis is mislabeled "Births"

In the EDA section, `plot3` (the deaths plot) is labeled `y = "Births"` in the `labs()` call. This is a copy-paste error that is visible in the rendered HTML output.

### 14. MINOR — Global search results for the full SEIR model are not visualized with a pairs plot

The pairs plot for the full SEIR global search is commented out (`#pairs(...)`), so the reader cannot assess parameter identifiability or correlations among parameters. The SIR pairs plot is shown (from the truncated 2024-only model), but not for the more complex SEIR model with six free parameters. This omission makes it impossible to evaluate the quality of the global exploration.

### 15. MINOR — Scholarship section cross-references cite an incorrect URL for project2024-2

In `references.bib`, the entry `project2024-2` (cited as a predator-prey project) has `url = {https://ionides.github.io/531w20/final_project/}`, pointing to a 2020 project page rather than the 2024 project. The `bdsk-url-1` field correctly references the 2024 project, but the primary `url` is wrong. This is a minor citation error but undermines the scholarship traceability.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/references.bib`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/Makefile`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data.zip` (listing only; contents examined via `unzip -l`)
