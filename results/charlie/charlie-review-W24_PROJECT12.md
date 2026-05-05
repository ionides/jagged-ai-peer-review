# Peer Review: W24 Project 12
## Time Series Analysis of COVID-19 Cases in Kent County

---

## Summary

This project fits a Susceptible-Exposed-Infected-Recovered-Susceptible (SEIRS) compartmental model to 212 weeks of COVID-19 case counts in Kent County, Michigan (February 2020 to March 2024). The authors incorporate time-varying transmission and reporting rates across three piecewise intervals, gamma white-noise overdispersion in the force of infection, and an importation parameter. They appropriately establish an ARMA(2,1) benchmark on log-transformed data, perform local and global iterated filtering (IF2) searches, and compute a profile likelihood over the third-period reporting rate. Key strengths include using likelihood-based inference throughout, correcting the ARMA likelihood to the raw-count scale for a valid benchmark comparison, and acknowledging the negative result that the SEIRS model does not beat the benchmark. However, several methodological errors undermine the reliability of the presented MLE and profile confidence interval: the global search box for the overdispersion parameter sigmaSE is dramatically too narrow (stated upper bound 0.5, MLE ~0.95), the profile likelihood mif2 call fails to fix the profiled parameter during optimization (allowing it to drift), and rw.sd boundaries are systematically misaligned with the piecewise covariate definitions. Parameter identifiability analysis is limited to one parameter, and model diagnostics remain largely qualitative.

---

## Major Issues

### 1. Global search box for sigmaSE is severely misspecified

The global search specifies an upper bound of 0.5 for `sigmaSE` (code line: `upper=c(..., sigmaSE=0.5, ...)`), yet the optimal result has `sigmaSE = 0.946` and 186 of 200 global search results exceed this stated upper bound. This is not merely a boundary that the optimizer drifted past: the initial random guesses were all drawn from `(0, 0.5)`, meaning the search was seeded in entirely the wrong region for this parameter. When the true MLE is nearly twice the box upper bound, the global search cannot reliably locate the optimum; the reported best log-likelihood of -1404.0 may be substantially below the true MLE. All downstream conclusions - including the benchmark comparison, the profile likelihood, and the confidence interval - are affected. The authors should re-run the global search with a revised box for `sigmaSE` (e.g., upper = 2.0) and report whether the benchmark gap narrows or the CI changes. See Wheeler et al. (2024), Section on Computational Adequacy.

### 2. Profile likelihood does not fix the profiled parameter during optimization

The profile likelihood computation reuses `params_rw.sd` from the local search without setting `rw.sd` for `rho3` to zero. Specifically, `params_rw.sd` assigns `rho3 = ifelse(data_weekly$week_num >= 125, 0.02, 0)`, so during each mif2 run in the profile loop `rho3` is perturbed away from its designed value. The recovered `rho3` values in the profile results confirm this: instead of 50 results at each of the 11 designed values, the output shows severe spreading (e.g., only 37 results near `rho3 = 0.6`, 68 near `rho3 = 0.2-0.3`). The resulting "profile" traces the likelihood over the post-drift value of `rho3` rather than the fixed design values, making the curve invalid as a profile likelihood and the confidence interval unreliable. The fix is to set `rw.sd(rho3 = 0)` in the mif2 call inside the profile loop. See Wheeler et al. (2024), SI Section S8.

### 3. rw.sd boundaries are systematically misaligned with covariate boundaries

The piecewise parameters `b1/b2/b3` and `rho1/rho2/rho3` are defined by the covariates `wave` and `rep_int`, but `params_rw.sd` uses strict vs. non-strict inequalities that are offset by one time step relative to the covariate definitions. For example:

- `b1` is active (via `wave=0`) for `t = 1..54`, but `rw.sd` for `b1` uses `week_num < 54`, perturbating `b1` only at `t = 1..53` and omitting `t = 54`.
- `b2` is active for `t = 55..72` (`wave=1`), but `rw.sd` for `b2` is nonzero at `t = 54..71`, perturbing `b2` at a time point where it does not affect the likelihood and failing to perturb it at `t = 72`.
- The same pattern holds for `rho1/rho2/rho3`.

This means the IF2 random walk does not correctly search the parameter space where each piecewise parameter is most informative. The parameters `b1` and `rho1` are not perturbed at their final active time step, while `b2` and `rho2` are perturbed at a time step where `wave=0`/`rep_int=0` renders them irrelevant. The fix is to align the inequalities so that each parameter is perturbed at exactly the time steps where it enters the likelihood.

### 4. SEIRS model fails to beat the ARMA benchmark by a large margin

The SEIRS model log-likelihood of -1404.0 is 32.5 log-likelihood units below the ARMA(2,1) benchmark of -1371.5. A gap of this magnitude (the equivalent of a likelihood-ratio test statistic of 65 with many degrees of freedom) indicates that the mechanistic model is substantially less capable of fitting the data than a simple statistical benchmark. The authors acknowledge this but frame it as a "close" result and focus the conclusion on modeling novelty. Given that the global search box for `sigmaSE` is misspecified (Issue 1), the true gap may be smaller, but this should be demonstrated. Until a corrected search is run, the claim in the conclusion that the model "adequately fit" the data is not supported quantitatively. See Wheeler et al. (2024), Section on Benchmark Comparison.

### 5. Profile confidence interval is unreliable and incomplete

The 95% confidence interval for `rho3` is reported as (0.37, 1.0). The upper bound at 1.0 is the hard boundary of the logit-constrained parameter, indicating that `rho3` is not identifiable from above - the data are consistent with any `rho3` from 0.37 to 1.0. Furthermore, only 3 points (not 4 as stated in the text) appear above the profile likelihood threshold, and these span `rho3 = 0.37`, `0.52`, and `1.0`, providing extremely sparse coverage of the CI region. A reliable profile would require (a) a finer grid (e.g., steps of 0.02-0.05 rather than 0.10), (b) more profile replicates per grid value, and (c) setting `rw.sd(rho3 = 0)` during optimization (see Issue 2). Profile likelihoods for other key parameters - particularly the transmission rates `b1`, `b2`, `b3`, and the epidemiological rates `mu_EI` and `mu_IR` - are absent entirely, leaving major scientific claims about parameter values unsupported. See Wheeler et al. (2024), Section on Parameter Identifiability and Uncertainty.

### 6. ESS collapse and conditional log-likelihood failures are underdiagnosed

The authors briefly note that the filtering diagnostic plot (Figure showing ESS and conditional log-likelihoods) shows "points of failure" and suggest these coincide with holidays. However, no quantitative analysis is provided: which time points fail, how severe the ESS collapse is, and whether the failures are systematic across all replicates or isolated. ESS collapse is a signal of model-data mismatch that deserves deeper investigation - for instance, by plotting per-observation conditional log-likelihoods against time to identify specific model failures, or by comparing filtering-conditioned simulations to forward simulations to understand whether the model fundamentally cannot explain certain periods. The conclusion mentions potential remedies (new reporting rate parameters for holidays) without implementing them. This leaves open whether the model is misspecified in ways that could be corrected. See Wheeler et al. (2024), Section on Model Diagnostics.

### 7. No profile likelihoods for key biological parameters

The analysis reports a single profile likelihood (over `rho3`), which is itself unreliable due to the rw.sd drift error. No profiles are computed for `mu_EI`, `mu_IR`, `mu_RS`, `b1`, `b2`, or `b3` - parameters that determine the biological interpretation of the model. The estimated `mu_RS = 0.0006 weeks^{-1}` (implying ~32 years of immunity) is identified in the text as biologically implausible, but without a profile likelihood it is impossible to determine whether `mu_RS` is identifiable or whether the data are essentially indifferent to its value. If `mu_RS` is unidentifiable (the profile is flat near zero), this is evidence of model misspecification that should be addressed by considering whether the SEIRS extension is warranted, or whether a SEIR model would be more parsimonious. See Wheeler et al. (2024), Section on Parameter Identifiability.

---

## Minor Issues

- **Minor count error in profile description:** The text states "only 4 points above the threshold" in the profile likelihood plot, but the data and code yield exactly 3 points above the 95% CI threshold. This is a minor but verifiable inaccuracy.

- **Transmission rate notation inconsistency:** The force-of-infection formula in the text writes $\mu_{SE}(t) = \frac{\beta(t)}{N(t)}(I + \iota)^\alpha \zeta(t)$, but $\alpha = 1$ is stated separately with a note "we set $\alpha = 1$". This $\alpha$ parameter does not appear in the C code (`seirs_step`) and is not estimated or fixed as a named parameter; it is simply hardcoded as exponent 1. The notation is misleading and the $\alpha$ should either be removed from the mathematical description or explicitly noted as a structural assumption rather than a parameter.

- **ARMA(2,2) MA polynomial notation error:** The equation for ARMA(2,2) uses $\psi_1 \epsilon_{n-2}$ when it should read $\psi_2 \epsilon_{n-2}$: "$ \psi(x) = 1 - 0.3608x + 0.0156x^2$" corresponds to two distinct coefficients ($\psi_1, \psi_2$), but the equation above it writes $\psi_1 \epsilon_{n-1} + \psi_1 \epsilon_{n-2}$ (same subscript for both MA terms).

- **W accumulator serves no purpose:** The state variable `W`, defined as the running sum of $(dw - dt)/\sigma_{SE}$, is tracked in `statenames` and updated every step, but is never referenced in `dmeasure` or `rmeasure` and is not discussed in the text. It adds computational overhead for each particle without contributing to inference or diagnostics. If it is intended as a model-checking diagnostic, its role should be described; otherwise it should be removed.

- **Simulation uses `simulate()` not the filtering distribution:** All model validation plots (initial parameter simulations and global optimum simulations) use forward simulation from initial conditions rather than from the filtering distribution conditioned on observed data. Simulations from the filtering distribution would provide a stronger diagnostic by showing whether the model can explain each period sequentially rather than in aggregate from the start. This limitation is not discussed.

- **Population size not updated for current year:** The fixed population $N = 659{,}000$ is taken from a web source that may reflect a census-year estimate; the actual population changed during 2020-2024. The model does not include birth/death demography, but the population base used for force of infection should be appropriate for the period analyzed. The paper should note the year of the population estimate used.

- **Periodogram interpretation is incomplete:** The authors conclude "absence of seasonality" from a spectral peak at frequency 0 and use this to rule out SARMA models. However, a SARMA model with annual periodicity would exhibit a peak at frequency 1/52 weeks, which is a distinct feature from the long-run trend captured at frequency 0. The periodogram should be examined for peaks near 1/52 before ruling out annual seasonality.

- **No reproducibility documentation:** There is no README file, no `sessionInfo()` output, no `renv` lockfile, and no documentation of the `pomp` package version used. The `pomp` API has changed across major versions and results may not reproduce on a different installation. The code creates `covid_params.csv` as a running accumulation of parameter estimates, but this file is not archived with the submission, meaning the global search pairs plots and benchmark comparison table depend on a file that must be regenerated. See Code Supplement Checklist, Section on Documentation.

- **Local search convergence description is imprecise:** The text says the log-likelihood converges "around -1,500" in the local search diagnostic. Examining the actual IF2 filter mean traces, 14 of 40 replicates end below -1500 with the range spanning -2766 to -1413. A significant fraction of runs did not converge to the vicinity of the optimum, suggesting the local search had incomplete coverage. A quantitative convergence summary (e.g., fraction of runs within X units of best) would be more informative.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_seirs_global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_seirs_local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_rho3_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/lev3_mifs_local.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/mi_covid.xlsx`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project12/Makefile`
