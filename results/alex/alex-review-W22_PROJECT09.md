# Peer Review: W22 Project 09 — Time Series Analysis of COVID-19 Cases in Washtenaw County

## Summary

This project applies an SEIR POMP model to daily COVID-19 case counts in Washtenaw County, MI from July 1, 2021 to April 6, 2022 (279 days). The main scientific motivation is to capture the shift from the Delta to Omicron variant by allowing the contact rate beta to take different values in two periods separated at December 1, 2021. Local and global searches are conducted with iterated filtering (mif2), and results are benchmarked against a negative binomial model and a seasonal ARIMA model. The writing is clear and the workflow follows the standard POMP analysis template, but there are several significant technical errors and notable gaps in rigor.

---

## Weaknesses (prioritized, most critical first)

### 1. [Major] Accumulator variable H tracks recoveries, not new infections

In `seir_step`, the accumulator `H` is incremented by `dN_IR` (individuals moving from I to R), not by `dN_EI` (individuals becoming infectious) or `dN_SE` (new exposures). COVID-19 case counts represent newly confirmed infections, not recoveries. The measurement model then links `Cases` to `rho * H`, meaning the model is, in effect, fitting a scaled version of the recovery flow to observed confirmed-case counts. This is a fundamental mis-specification of the measurement process. A standard SEIR-POMP formulation for case-count data would set `H += dN_EI` or `H += dN_SE`. The practical consequence is that the likelihood surface being optimized has no clear epidemiological meaning, and parameter estimates (particularly `rho` and `mu_IR`) are confounded.

Evidence: `seir_step` Csnippet (line 128): `H += dN_IR;`

### 2. [Major] SEIR model likelihood is outperformed by the non-mechanistic SARIMA benchmark

The best log-likelihood reported from the global search is approximately -1547, whereas the SARIMA(3,0,0)x(1,0,1)_7 model (a non-mechanistic benchmark with far fewer parameters) achieves a corrected log-likelihood of -1308. The mechanistic SEIR model is thus about 239 log-likelihood units worse than a simple seasonal ARIMA. The authors acknowledge this briefly but do not investigate why, nor do they attempt to improve the model to close this gap. In a POMP analysis, failing to beat non-mechanistic benchmarks is a strong signal that the mechanistic model is mis-specified or that the optimization has not converged. This point deserves far more discussion.

Evidence: Rmd lines 398, 439.

### 3. [Major] mu_IR is fixed without justification; its value is inconsistent with COVID biology

The recovery rate `mu_IR = 0.2` is fixed for both local and global searches (line 250). This implies a mean infectious period of 1/0.2 = 5 days. While plausible for some COVID variants, no citation is provided for this choice and no sensitivity analysis is performed. More importantly, fixing `mu_IR` removes a parameter that may be essential for fitting the Omicron wave, where infectious periods and disease progression differed markedly from Delta. Because `mu_IR` is also conflated with the accumulator error described in Issue 1, its interpretation is further compromised.

Evidence: `fixed_params <- c(N=372258, mu_IR=0.2)` (line 250).

### 4. [Major] No profile likelihood or confidence intervals for any parameter

The analysis reports point estimates from the global search but provides no uncertainty quantification for any estimated parameter (b1, b2, rho, eta, mu_EI, tau). Profile likelihood confidence intervals are the standard tool for this purpose in POMP analyses and are essential for assessing parameter identifiability. The pairwise scatter plot from local search (line 301) is shown but not discussed in terms of what it reveals about parameter correlation or identifiability. Without uncertainty quantification it is impossible to determine whether, for example, the claimed difference between b1 and b2 is statistically meaningful.

Evidence: No profile likelihood code appears anywhere in the Rmd.

### 5. [Major] Likelihood non-convergence acknowledged but not addressed

The authors note (line 277): "our likelihood does not strictly increase as iterations proceed, which may indicate a problem." However, no remedial action is taken: the number of mif2 iterations (Nmif=100), the number of particles (Np=2000 for local search), and the random walk standard deviations are not adjusted, and no second-round mif2 is applied. Failure to converge in local search undermines the validity of any parameter estimates and the reliability of the global search, which uses `mf1 <- mifs_local[[1]]` as its template.

Evidence: Lines 258-260 (local search settings), line 277 (convergence comment), line 337 (global search inherits from mif1).

### 6. [Major] Measurement model uses a Normal approximation that allows negative case counts

The measurement model uses a Gaussian distribution for the observed case counts: `Cases = rnorm(rho*H, sqrt(pow(tau*H,2)+rho*H))`. Case counts are non-negative integers; a normal approximation can produce negative simulated values, which are then rounded to zero. This is handled in `seir_rmeas` but not in `seir_dmeas`, which uses `pnorm` with a continuity correction. More importantly, using a Gaussian measurement model for count data introduces a likelihood discrepancy relative to what a negative binomial or Poisson measurement model would give, and the authors do not motivate this choice.

Evidence: Lines 140-159 (dmeas and rmeas Csnippets).

### 7. [Moderate] Global search uses only a single mif2 pass per starting point

In the global search (lines 336-337), each starting point undergoes only one additional call to `mif2(Nmif=100)`. The standard practice is to run two or more rounds of mif2 from each starting point to refine estimates and reduce Monte Carlo noise. The global search therefore likely returns preliminary estimates rather than near-optimal ones, which partly explains why the SEIR model falls so far short of the SARIMA benchmark.

Evidence: Lines 336-337: `mif2(params=c(guess, fixed_params)) %>% mif2(Nmif=100) -> mf`

### 8. [Moderate] Covariate split point description is inconsistent with the code and text

The text states that December 1 is the division between the Delta and Omicron periods and that b1 applies to "the first half of time period." The code uses `rep(0, 154)` for b1 and `rep(1, 125)` for b2. July 1 to December 1 is 153 days, so the split appears at day 155 (December 2), not day 154. More importantly, the text's claim that this is the "first half" of the time period is incorrect: 154 of 279 days is just over half, but characterizing a biologically motivated split as "first half" is misleading and suggests the authors may not have carefully verified the date arithmetic. No verification of the split date is shown.

Evidence: Lines 101, 112, 164-165.

### 9. [Moderate] Initial reporting probability rho=0.9 is implausibly high and not justified

The initial guess for `rho` is set to 0.9 (line 198), implying 90% of all infections are reported. For COVID-19 in 2021-2022, especially during the Omicron wave when many asymptomatic cases went untested, the true reporting rate was much lower — studies estimate 10-30% or less. The global search range allows `rho` up to 0.9, which is consistent with the initial guess but not with epidemiological evidence. This choice, combined with fixing mu_IR and the accumulator mis-specification, likely distorts all other parameter estimates.

Evidence: Line 198: `rho=0.9`.

### 10. [Moderate] The ARMA log-likelihood correction is applied but the benchmark comparison is flawed

The SARIMA model is fit on `log(1 + Cases)` and the back-transformation Jacobian correction (`arma30$loglik - sum(log_cases)`) is applied. While the Jacobian computation is technically correct for a log(1+x) transformation, the comparison with the SEIR model log-likelihood is not straightforward: the SEIR model uses integer-valued count observations while the SARIMA model assumes Gaussian errors on the log scale. These models are not comparable on the same likelihood scale in a rigorous sense, and the authors do not acknowledge this limitation.

Evidence: Lines 403, 436, 439.

### 11. [Moderate] Initial exposed population E=30 is hardcoded and not justified relative to the data

The initial compartment values hardcode `E = 30` and `I = 30` (lines 133-134). The text notes that 30 is "an intuitive value based on the confirmed cases on July 1st" but E (exposed but not yet infectious) is a latent quantity with no direct observational anchor. The choice of E = I = 30 is arbitrary and is not varied in the global search (eta only controls the initial S fraction, while E and I remain fixed). This effectively removes an important degree of freedom from the model initialization.

Evidence: `seir_init` Csnippet, lines 133-134.

### 12. [Moderate] The EDA caption text is repeated verbatim

The caption text for Figure 1 appears both as a caption variable (line 47-48) and is then repeated as paragraph prose immediately after the figure (line 68), word for word. This appears to be an editing error where the same text was pasted twice.

Evidence: Lines 44-45 and 68: identical text about the loess smoothing and peak in January 2022.

### 13. [Minor] Two chunk headers contain the typo "cahce=TRUE" instead of "cache=TRUE"

Two code chunks use `cahce=TRUE` (a misspelling of `cache=TRUE`). These chunks will not be cached, meaning they will rerun on every knit despite potentially being computationally expensive. In particular, the global search chunk (which the comment suggests should be cached via `bake`) also uses `cahce=TRUE`.

Evidence: Chunk headers at lines 189 and 328.

### 14. [Minor] Parameter description uses wrong notation mu_SI for the S-to-E rate

The model description (line 101) defines `mu_SI = beta * I(t)` as the rate of S-to-E transition, but the compartment being entered is E (Exposed), not I (Infectious). In an SEIR model, this rate is more conventionally written as `mu_SE` or `lambda` (the force of infection). Using `mu_SI` is confusing because I is a compartment label in the model, creating notational ambiguity.

Evidence: Line 101.

### 15. [Minor] Vaccination and waning immunity are ignored without discussion

The analysis period (July 2021 to April 2022) coincides with widespread COVID-19 vaccination in Washtenaw County, with booster campaigns underway by late 2021. The SEIR model has a closed population where recovered individuals never return to susceptibility, which ignores waning immunity (relevant for Omicron reinfections). No discussion of these important real-world features and their potential impact on model validity appears anywhere in the paper, apart from a single sentence in the conclusion mentioning a "SEQIR model" for quarantine.

Evidence: Lines 443-447 (conclusion).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project09/final_proj_531.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project09/Makefile`
