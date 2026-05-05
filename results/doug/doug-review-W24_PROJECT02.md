# Peer Review: W24 Project 02
## "Investigating the alternative prey hypothesis with the POMP framework"

---

## Summary

This project applies the POMP framework to model willow ptarmigan (*Lagopus lagopus*) population dynamics in Northeastern Scandinavia from 1872 to 2012, seeking to formalize the alternative prey hypothesis using a Lotka-Volterra-inspired predator-prey-alternative prey system. The study is motivated by prior work (Hjeljord and Loe) that documented long-term ptarmigan decline and rodent cycle dampening. An ARIMA(0,1,5) model is fitted as a benchmark, and a POMP model with fox-bird-rodent dynamics is fitted using iterated filtering (IF2) with both local and global search.

The central contribution — embedding the alternative prey hypothesis in a mechanistic POMP model — is ecologically interesting and methodologically ambitious for an ARMA-dominated ecological literature. However, the analysis is substantially incomplete: the POMP model never out-performs the ARIMA benchmark, no profile likelihoods are computed, the global search is severely underpowered (only 2 valid results), the particle count used for likelihood evaluation in the local search is far too small, and key model equations contain internal inconsistencies. The project reads as a preliminary exploration rather than a finished analysis, and the authors acknowledge this candidly in the conclusion.

---

## Major Issues

### 1. POMP model never out-performs the ARIMA benchmark

The authors report ARIMA(0,1,5) log-likelihood = −99.32, local search POMP best log-likelihood = −134, and global search POMP best log-likelihood = −176.3. The POMP model is substantially worse on every metric. Rather than investigating why — which would be the scientifically productive response — the conclusion simply notes that "the ARMA model is fitting the data better" and moves on. No attempt is made to diagnose whether this gap reflects model misspecification, insufficient computation, a fundamental identifiability problem, or an inappropriate measurement model. The ARIMA result is not even placed on the same likelihood scale as the POMP result (the POMP measurement model uses logCPUE ~ Normal, while the ARIMA model uses a differenced ARIMA on logCPUE; these are not directly comparable without careful adjustment). The failure to reconcile this discrepancy is the most serious gap in the paper.

### 2. Global search is critically underpowered — only 2 valid results in the CSV

The bird_params_middle.csv file contains exactly 2 rows of results from the global search, despite the code specifying `nseq=50` starting points. This means 48 of 50 runs produced non-finite likelihoods and were filtered out via `filter(is.finite(loglik))`. With only 2 valid results, it is not possible to draw any conclusions about the global likelihood surface or parameter identifiability. The reported global MLE of −176.3 is almost certainly not the global maximum — it is simply the best of two surviving evaluations. This should be flagged as a critical computational failure, not as the definitive global search result.

### 3. Particle count for likelihood evaluation is too small (Np = 5 in one key evaluation)

In the single `mif2` evaluation chunk, the code uses `pfilter(Np=5)` (five particles) for the likelihood evaluation after optimization:
```
foreach(i=1:10, ...) %dofuture% { mif2_out |> pfilter(Np=5) }
```
Five particles is far too few for a reliable likelihood estimate in any non-trivial state-space model. The resulting standard error of 3.14 log-likelihood units is enormous — roughly 1.6 AIC units of uncertainty per evaluation — making the reported −205 essentially uninformative. The local search uses Np=1000 for optimization but only Np=100 for the subsequent likelihood table, which is marginally better but still on the low side. Wheeler et al. (2024, §Computational adequacy) emphasize that stochastic likelihood estimates must be stable; these are not.

### 4. No profile likelihoods; parameter identifiability unassessed

No profile likelihoods are computed for any of the 12 parameters. The pairs plot in Figure (local_search_2.png) shows the joint distribution of parameters across the 20 local search runs, but this is not equivalent to a profile likelihood and does not establish identifiability. Several parameters show highly diffuse distributions across the local search runs (the artifact confirms that `sigmaB` reaches 8.59 while other runs converge to very different values), suggesting non-identifiability. Without profile likelihoods, no confidence intervals can be computed and it is impossible to assess whether any parameter is meaningfully constrained by the data. This is a fundamental requirement for inference with POMP models (Wheeler et al. 2024, §Parameter identifiability).

### 5. Model equation inconsistency: bird equation uses the same noise term as fox equation

In Equation (2) (the bird dynamics), the stochastic increment is $W_t^F$ — labeled explicitly as the fox noise term — rather than a separate $W_t^B$. The Csnippet correctly defines separate `dwF` and `dwB`:
```c
logF += (...)*dwF;
logB += (...)*dwB;
```
but the equation in the text shows $W_t^F$ for both, making the written model appear to drive fox and bird dynamics with the same noise realization. This is either a transcription error in the equations or a genuine model discrepancy. Either way, the measurement model specification in the text does not cleanly match the code.

### 6. Measurement model states the wrong distribution for logCPUE

The methods section states "the measurement model $Y(t)$ is our ptarmigan count proxy, *logCPUE*, $y(t) = \text{Negative Binomial}(\text{mean}=\rho\beta_t, \sigma)$". However, the `rmeasure` and `dmeasure` Csnippets implement a Normal distribution:
```c
logCPUE = rnorm(logB - logRho, sigma_obs);   // rmeas
lik = dnorm(logCPUE, logB - logRho, sigma_obs, give_log);  // dmeas
```
The text says Negative Binomial; the code uses Normal. This is exactly the type of model-code discrepancy documented by Wheeler et al. (2024) as a reproducibility failure. Additionally, the parameter $\beta_t$ in the Negative Binomial description appears nowhere in the code, and the notation $\rho\beta_t$ is undefined. The Normal measurement model on logCPUE may be defensible, but it must be stated correctly and justified.

### 7. Global search parameter space appears disconnected from local search results

The local search converges to parameter values with `a` in the range 25–35, `logB_0` around 6–7, and `sigmaB` around 8. The global search uses a prior range of `a` ∈ [7, 8], `logB_0` ∈ [1.6, 1.7], and `sigmaB` ∈ [0.02, 0.04]. This means the global search is exploring a region of parameter space that does not contain the local search MLE. The global search cannot improve on the local search when the search region excludes the local optimum. The authors do not notice or comment on this contradiction, and it largely explains why the global search log-likelihood (−176.3) is worse than the local search result (−135).

### 8. IF2 convergence not demonstrated; only 50 iterations used in local search

The local search uses `Nmif=50` iterations. The trace plots (local_search_1.png) show that several parameters — notably `logB_0`, `sigmaF` — have not converged by iteration 50. Wheeler et al. (2024, §Computational adequacy) require evidence of convergence from multiple independent runs. The authors acknowledge non-convergence for some parameters but do not increase the number of iterations or investigate the impact on reported likelihoods. The standard error of the local search log-likelihood (8.2 log-likelihood units) is large enough that the reported MLE of −134 could be anywhere in a very wide interval.

---

## Minor Issues

- **Bibliography hard-coded to local path**: The YAML contains `bibliography: /Users/ruojunliu/Desktop/references.bib` and figures reference paths like `/Users/ruojunliu/Desktop/STATS 531 - Time Series/pomp_final/...`. These hard-coded absolute paths prevent reproduction on any machine other than the author's. The bibliography file is not included in the project folder, so references cannot be rendered. This is a basic reproducibility failure (Code Supplement Checklist, §Reproducibility).

- **Data path also hard-coded**: `read_excel("/Users/ruojunliu/Desktop/STATS 531 - Time Series/pomp_final/data/bird_data.xlsx")` uses an absolute local path, although the data file is present in the project's `data/` subdirectory. The Rmd does not use the project-relative path.

- **Q_fit_bird_local_mifs.rds contains extra parameters not in the Rmd model**: The artifact `Q_fit_bird_local_mifs.rds` contains 20 parameters including `beta_1`, `delta_1`, `psi`, `theta`, `rho`, `k`, `F_0`, `B_0` that do not appear in the Rmd's `paramnames` vector or any Csnippet. This artifact appears to belong to a different, more complex model that is not described in the manuscript. It is included in the project folder without explanation.

- **ARMA and POMP log-likelihoods are not on the same scale**: The ARIMA(0,1,5) is fitted to the first-differenced series, while the POMP model operates on the undifferenced logCPUE. A valid benchmark comparison would require the ARIMA likelihood to be computed on the same observation scale as the POMP measurement model, accounting for the Jacobian of the differencing transformation. The comparison as stated conflates two different observation processes.

- **`eval=FALSE` on global search chunk means results were not generated from this Rmd**: The global search chunk has `eval=FALSE`, and the CSV results are loaded from an absolute local path. The analysis is not reproducible from the provided Rmd.

- **KPSS test p-value truncation**: The KPSS test for the differenced series produces p-value > 0.05, but the statement "proved by the p-value larger than α=0.05 from KPSS test" misstates KPSS null hypothesis semantics. KPSS tests the null of stationarity; a p-value > 0.05 fails to reject stationarity, it does not prove it.

- **Parameter $\gamma$ in the model**: The parameter $\gamma$ appears in both the fox and bird equations as `[1-γR_t]`, described as "the impact of rodent population on predation efficiency." However, $\gamma$ is constrained to be positive and $R_t \in \{0,1\}$, so the factor $(1-\gamma R_t)$ can be negative if $\gamma > 1$. The model does not constrain $\gamma \le 1$, which could produce biologically impossible negative predation rates. The MLE from the local search has $\gamma \approx 0.5$, which is fine, but no constraint is imposed.

- **No simulation-based model validation**: The paper never simulates from the fitted model and compares trajectories to data. There is no forward simulation, no filtering distribution comparison, and no summary statistics comparison. The only visual of model fit comes from the initial particle filter diagnostic plot with the arbitrary starting parameter values. The fitted model's adequacy is never visually or quantitatively assessed.

- **ACF section cross-reference error**: The text states "Figure \@ref(fig:trend), the partial correlation dies out after 5 lags" but this should reference \@ref(fig:pacf). The PACF figure caption also erroneously reads "ACF of logCPUE" instead of "PACF of logCPUE."

- **Missing `sessionInfo()` and package version documentation**: The README contains only a one-line description. No software versions, R session information, or package versions are documented. The `pomp` version is stated only in passing in the text ("Version 5.6"). The code supplement checklist requires explicit version pinning, particularly for `pomp`, whose API has changed substantially across versions.

- **Rodent covariate treated as known without uncertainty**: The peak rodent year indicator $R_t$ is used as a fixed covariate, but it is derived from multiple sources covering different periods (1871–2013 from six separate references). The quality and consistency of rodent records across a 140-year span is not discussed, and the uncertainty in the rodent cycle data is not propagated into the POMP model.

- **Species name misspelling**: The Latin name is written as *Lapagos lapagos* in the introduction but should be *Lagopus lagopus*.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project02/README.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project02/bird_params_middle.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project02/local_search.rds` (inspected via R)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project02/Q_fit_bird_local_mifs.rds` (inspected via R)
