# Peer Review: W25 Project 16
## "Analyzing Whooping Cough with ARMA and POMP"

---

## Summary

This project applies time-series and mechanistic modeling to weekly pertussis (whooping cough) case counts for East North Central states (Michigan, Ohio, Indiana, Illinois, Wisconsin) from 2017 to early 2025, with particular focus on the 2024 outbreak. The authors fit an ARIMA(2,1,4)/ARCH(1)-X baseline and then develop SIR and SEIR POMP models, ultimately attempting to compare statistical and mechanistic approaches. While the project is ambitious in scope and the motivation is well-grounded in an interesting public-health event, the analysis contains several fundamental methodological errors that undermine its main conclusions: the central log-likelihood comparison between the ARCH and SEIR models is not valid, both POMP models yield biologically implausible parameter estimates that are not discussed, and key model-diagnostic outputs are commented out of the code. The paper does not compute profile likelihoods, does not compare to a proper non-mechanistic benchmark on the count scale, and does not corroborate parameter estimates against known pertussis natural history.

---

## Major Issues

### 1. Invalid log-likelihood comparison between ARCH and SEIR models

The paper's central quantitative claim—that the ARCH model outperforms the SEIR POMP model because its log-likelihood (−1203) exceeds the SEIR's (−1442)—is based on an incorrect statistical argument. The authors write: "Since first differencing is a linear transformation with a constant Jacobian, we can directly compare these fits after accounting for the dropped initial term." This reasoning is wrong. A Jacobian correction converts a density for a transformed variable back to the original variable's scale only when both densities describe the *same* distributional family applied to a 1-to-1 transformation. Here, the ARCH model assigns a Gaussian density to first-differenced counts, whereas the SEIR model assigns a negative binomial density to raw counts. These are fundamentally different probability models for different outcomes; no Jacobian adjustment can make their log-likelihoods commensurable. The comparison is therefore meaningless, and the conclusion that the ARCH model is "superior" is unsupported. To compare the two approaches quantitatively, the authors would need to express both as predictive distributions for the same observable (e.g., the raw weekly count), then evaluate each on held-out data using proper scoring rules or a comparable likelihood.

### 2. Accumulation variable H tracks recoveries rather than new infections

In all three rprocess snippets (SIR, SEIR, and the SEIR with one observation removed), the accumulation variable H is incremented by `dN_IR` (the I→R transition), not by new infections (`dN_SI` in the SIR or `dN_EI` in the SEIR). The measurement model then uses `rho * H` as the expected number of reported cases. Pertussis cases are reported at symptom onset (which coincides with early infectious period, not recovery), so H should track new entries into the infectious compartment, not exits from it. The current formulation introduces a systematic lag equal to the mean infectious period between true case counts and the modeled measurement. Given the estimated mu_IR = 6.92 per week in the SIR model (implying infectious period ≈ 1 day), the lag is negligible for the SIR, but for the SEIR model with mu_IR = 64.2 per week (infectious period ≈ 0.11 days), the model degenerates. This is a textbook `accumvars` semantic error; see the pomp-accumvar-semantic-audit skill for analogous cases.

### 3. Biologically implausible parameter estimates not discussed

The best-fitting SEIR parameter vector from the global search yields mu_IR = 64.2 per week, implying an infectious period of 1/64.2 weeks ≈ 2.6 hours. The true infectious period for pertussis is 1–3 weeks. Furthermore, the estimated initial susceptible fraction eta = 0.787 (78.7% of 48 million = 37.8 million susceptible individuals) is inconsistent with reported vaccination coverage of ≈71–75%. The two transmission rates base_beta = 8.76 and outbreak_beta = 8.72 are nearly identical, indicating the time-varying beta structure failed to identify distinct pre-outbreak and outbreak transmission dynamics. Wheeler et al. (2024) emphasize that implausible parameter estimates should be interpreted as evidence of model misspecification, not biological findings. The authors do not discuss any of these issues, and no comparison to external evidence (e.g., CDC estimates of pertussis infectious period, US pertussis under-reporting rates) is provided. This violates POMP best practice checklist item 11 (corroboration with scientific knowledge).

### 4. Severe parameter non-identifiability not addressed with profile likelihoods

The SIR global search places 196 of 600 starting points within 4 log-likelihood units of the maximum. Among those, mu_IR ranges from 1.9 to 59.8 (essentially spanning its entire prior box of 0–60), Beta ranges from 4.6 to 409, and eta ranges from 0.017 to 0.90. The text acknowledges that "mu_IR is not identifiable" but does not mention the identifiability failures for Beta and eta, and no profile likelihoods are computed to quantify these. Without profile likelihoods, no confidence intervals for any parameter can be given and it is unclear whether any reported point estimate is meaningful. Wheeler et al. (2024, §Parameter identifiability and uncertainty) and POMP checklist item 5 require that profile likelihoods be computed for all key parameters.

### 5. rw.sd argument uses data vector rather than time variable in SEIR local searches

In the SEIR local search (and in the repeated version with one observation removed), the random-walk perturbation intensities are specified as:

```r
rw.sd = rw_sd(
  base_beta = ifelse(whoop$week < 332, 0.02, 0),
  outbreak_beta = ifelse(whoop$week > 332, 0.02, 0), ...
)
```

The expression `ifelse(whoop$week < 332, 0.02, 0)` is evaluated in the calling environment at construction time and produces a 381-element numeric vector, not a time-indexed expression. In pomp, `rw_sd()` stores the expression as a `safecall` object evaluated at each mif2 iteration with the current observation time available as `time`. The correct usage would reference the `time` variable, e.g., `ifelse(time < 332, 0.02, 0)`. Passing a pre-evaluated vector may result in only the first element being used for every time step, or trigger recycling behavior—either way, the intended time-varying perturbation schedule is not implemented correctly, and the local search results should be considered suspect.

### 6. No non-mechanistic benchmark comparison on the count scale

Wheeler et al. (2024, §Benchmark comparison) identify absence of a non-mechanistic benchmark as the single most common deficiency in published mechanistic epidemic models. The authors frame the ARCH model as serving this benchmark role, but as explained in Major Issue 1, the ARCH is fit to differenced data under a Gaussian likelihood and cannot be compared to the SEIR on the raw count scale. A proper benchmark would be an auto-regressive negative binomial or Poisson model fit to the raw weekly counts, evaluated using the same log-likelihood. Without this, it is impossible to assess whether the mechanistic model captures any structure beyond a simple statistical model.

### 7. Key diagnostics commented out; effective sample size never reported

Three particle-filter diagnostic calls are present in the code but commented out:
- `#plot(pf)` (at lines 501, 812, 1092) — would show per-observation log-likelihood contributions and effective sample size (ESS)
- `#min(pf@eff.sample.size)` (line 502) — would report minimum ESS across time

ESS monitoring is essential for detecting particle filter degeneracy, which can produce silently misleading log-likelihood estimates. Wheeler et al. (2024, §Computational adequacy) and POMP checklist item 6 require ESS to be reported. Additionally, the global SEIR pairs plots are also commented out (lines 962–965), so readers cannot visually assess parameter identifiability for the main SEIR model. These omissions prevent assessment of computational adequacy.

---

## Minor Issues

### 8. Missing data interpolation not documented

The ARMA and ARCH analyses use `data/interpolated_cases.csv`, which contains no missing values, while the POMP analyses use `data/all_data.csv`, which has 79 NAs (44 in 2021 alone, and all 6 available 2022 records are NA). No code for constructing the interpolated dataset is present in the supplement. Inspection of the interpolated file reveals values of 1.0–1.7 for the 2022 period—a linear interpolation between values just before and after the reporting gap—which may understate true incidence and distort the ARCH model. The paper should either include the interpolation code, explain the method explicitly, and justify why linear interpolation is appropriate when data are missing due to reporting failures.

### 9. ARMA log-likelihood inconsistency between sections

The text reports the ARMA(2,4) log-likelihood as −1368 in the ARMA section (line 358) but as −1366 in the comparison section (line 1238). The computed value from the code is −1367.999 ≈ −1368. The comparison section value of −1366 is incorrect and should be corrected.

### 10. ARMA(2,4) convergence failure not addressed

The paper notes that ARMA(2,4) "experienced convergence problems" but proceeds to use it for the ARCH comparison without discussion. A model with a convergence warning may have unreliable parameter estimates and an unreliable log-likelihood, undermining the ARMA-vs-ARCH comparison. The authors should either select a model that converges cleanly or explain why the convergence warning is inconsequential.

### 11. No formal stationarity test before differencing

The paper applies first-differencing to justify ARMA modeling, stating this "removes trends." No unit-root test (ADF or KPSS) is applied to the original series to justify the order of integration. Differencing a stationary series can introduce unnecessary moving-average terms and inflate model complexity.

### 12. ARCH(1) order not justified

Only ARCH(1) is fitted. No comparison to GARCH(1,1) or higher-order ARCH specifications is provided, despite the fact that GARCH(1,1) generally outperforms ARCH(q) on financial and epidemiological count data. The residual tests reject both the Ljung-Box and ARCH-LM hypotheses for the fitted ARCH(1), suggesting inadequacy, yet no higher-order model is attempted.

### 13. Omega parameter omitted from the ARCH variance equation

The reported variance equation `sigma_t^2 = 0.533 * eps_{t-1}^2 + 2.139 * x_t` does not include the constant `omega` term that was specified in the ugarchspec model. The parameter table from the ugarch output should include `omega`; its omission from the displayed equation suggests the authors did not report a parameter from the fitted model. This should be checked and corrected.

### 14. SIR local search does not perturb mu_IR

In the SIR local search (line 544), the rw.sd specification pertubs only Beta, rho, and eta, while mu_IR is held fixed at 0.5. Yet the text says the global search "allows mu_IR to vary." The practical consequence is that the local search provides starting points biased toward mu_IR = 0.5, and the reported best local loglik of −212 vs. the global best of −204 reflects this restriction. This inconsistency should be acknowledged.

### 15. Population assumed constant with no demographic processes

The model fixes N = 48,000,000 with no births, deaths, or waning immunity, over an 8-year period that includes the COVID-19 pandemic disrupting vaccination schedules. The paper mentions this as a limitation but does not assess how strongly the fixed-population assumption biases estimates—particularly given that the full dataset spans 2017–2025 and the authors cite declining vaccination coverage as the likely driver of the 2024 surge. A brief sensitivity analysis varying eta (initial susceptible fraction) over a biologically constrained range would substantially strengthen the SEIR analysis.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/global-SIR.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/global-SEIR.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/global-SEIR_1datapointrmv.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/mifs_local_SIR.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/mifs_localSEIR.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/mifs_localSEIR_1datapointrmv.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/whoop_truncated_params_SIR.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/all_data.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/interpolated_cases.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project16/data/vaccination_rates.csv`
