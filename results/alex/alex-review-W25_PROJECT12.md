# Peer Review: W25 Project 12 — Comparative Analysis of Volatility Models for Daily Gold Prices

---

## Summary

This project compares three modeling frameworks — ARIMA, GARCH (Normal and Student-t), and two POMP models (Heston stochastic volatility and a discrete Regime-Switching model) — applied to daily gold log returns from 2022 to 2024. The structure is reasonable and the breadth of models is commendable. However, the project has several significant methodological, reporting, and interpretive weaknesses that undermine the reliability of the conclusions.

---

## Weaknesses (Prioritized by Severity)

### 1. (Major) Invalid/Physically Meaningless Parameter Estimates Dismissed Without Justification

The Heston model produces negative estimates for `sigma` (volatility-of-volatility, estimated at -0.0051) and `v0` (initial variance, estimated at approximately -2.38e-5). Both of these parameters are constrained to be strictly positive by construction: `v0` is a variance and `sigma` scales the diffusion of a square-root process. A negative `v0` is physically nonsensical. The authors acknowledge these "may seem concerning" but claim they "fall within acceptable ranges given the variability inherent in the particle filtering process." This is not a valid justification. Negative variances indicate model misspecification, numerical instability, or parameter non-identifiability — not acceptable particle filter noise. A positive constraint (e.g., via log-transformation of `v0` and `sigma`) should have been imposed in the parameterization, as is standard practice.

### 2. (Major) Likelihood Comparisons Across Models Are Not Adjusted for Parameter Count (No AIC/BIC Reported for POMP)

Table 5 compares log-likelihoods across ARIMA, GARCH, and POMP models but provides no AIC or BIC to penalize for model complexity. The POMP models have more parameters than the ARIMA or GARCH benchmarks. The authors themselves note (Section 6) that the POMP gains "carry several more parameters," but they never formally quantify this penalty. Without AIC/BIC, the comparison is incomplete. Saying GARCH(1,1)-t achieves the "most efficient" fit is an unsupported informal claim.

### 3. (Major) Inconsistency Between ARMA Order Used in GARCH Code and Stated Model

The ARIMA model selection in Section 3 identifies ARIMA(2,0,2) as best. The GARCH specification in Section 4 describes using "ARMA(2,2)" as the mean component. However, in the code at line 345, the ACF plot label says `"ARMA(1,1)+GARCH(1,1)"`, and at line 388, the same label is reused for the t-distribution version. The prose in Section 4.3 then reverts to describing the model as "ARMA(2,2)+GARCH(1,1)." This inconsistency between prose and code labels creates confusion about which mean specification was actually fitted and compared.

### 4. (Major) Profile Likelihood for Heston Does Not Fix kappa in the rw.sd

In the profile likelihood computation for `kappa` (Section 5.1), the `rw.sd` object passed to `mif2` does not include `kappa`. This means `kappa` is not being perturbed, but the code uses `modifyList(as.list(coef(best_mif)), as.list(fixed_params))` to set the starting value to the fixed `kappa`. However, the profile is supposed to fix `kappa` throughout optimization. Since `mif2` only perturbs parameters included in `rw.sd`, the `kappa` parameter effectively remains fixed at the starting value only because it is not in the `rw.sd`. This is technically correct by accident but is not the standard recommended approach (which is to pass `rw.sd(..., kappa = 0)` explicitly or use `profile_design`). Similarly, for the RS model profile over `log_sigma2`, the `rw.sd` also omits `log_sigma2`, making the profile computation implicit rather than explicit. This should be documented and justified.

### 5. (Major) Only a Single Particle Filter Evaluation per Replicate for Likelihood Scoring

Throughout the global search and profile likelihood evaluation, the log-likelihood for each parameter set is estimated using a single run of `pfilter` with 5,000 particles. Particle filter likelihood estimates are stochastic; a single evaluation can have substantial Monte Carlo variance. Best practice is to replicate the particle filter evaluation multiple times (e.g., 10 replications) and average or take the maximum. Failing to do so means the "best" replicate selected may simply be the one that got a luckier particle filter draw, not the one with the highest true likelihood.

### 6. (Major) Data Extends Beyond the Stated Analysis Period

The paper states "covering the period from January 1, 2022 to December 31, 2024" and applies a filter `filter(Date <= as.Date("2024-12-31"))`. However, the data.csv file contains observations up to April 2025 (the first row is "04/01/2025"). This means the dataset used in the analysis is filtered, but it is not the dataset as originally described — the data source contained future observations that had to be excluded. This is a minor data provenance issue but should be disclosed.

### 7. (Major) Regime-Switching Model: Regime Trajectory Based on a Single Simulation, Not Filtered States

The "Inferred Regime Over Time" plot in Section 5.2 is produced using `simulate()`, which draws a forward simulation from the model, not the filtered (posterior) regime probabilities. This is misleading: what is shown is one possible trajectory drawn from the generative model, not the inferred hidden-state sequence from the data. The correct visualization would use particle filter output to display the posterior probability of being in each regime at each time step (e.g., via `filter.mean` or a smoothed state estimate).

### 8. (Major) No Confidence Intervals or Uncertainty Quantification for Profile Likelihoods

Both profile likelihood plots (kappa for Heston, sigma2 for RS) are presented without confidence intervals. In a POMP framework, profile likelihoods are used to construct likelihood-ratio-based confidence intervals: a 95% CI corresponds to the range of parameter values where the profile log-likelihood is within 1.92 units of the maximum. The authors do not construct or report these intervals, missing a key inferential output. The kappa profile is described qualitatively ("flat between 0.7 and 2") but no formal CI is derived.

### 9. (Minor) Inconsistent Figure Numbering

The ACF of squared log returns in Section 4 is labeled "Figure 3" in the caption (line 248), but Figure 3 was already used in Section 2.2 for the log-return time series plot. This duplicate figure number is confusing. This labeling error persists throughout the document.

### 10. (Minor) GARCH AIC Table Description Inconsistency

In Section 4.1, the prose states GARCH(1,3) has the lowest AIC of -5046.13, but immediately declares "GARCH(1,1) is the most standard and practical specification" and proceeds with GARCH(1,1) without a rigorous justification via diagnostics or a formal test. While parsimony is a valid motivation, the diagnostics shown (ACF of squared residuals) show "only a single significant spike at lag 1" for both GARCH(1,1) and GARCH(1,3) — this is presented as evidence for GARCH(1,1), but this same reasoning could justify GARCH(1,3) being unnecessary. The conclusion is defensible but the argument is circular.

### 11. (Minor) The Model Comparison Table (Table 5) Has Hardcoded Log-Likelihood Values

Table 5 in Section 6 uses hardcoded log-likelihood values (`2525.8`, `2528.7`, `2543.4`, `2536.8`, `2539.7`) rather than values computed at runtime. Meanwhile, Section 6 also contains a code chunk that computes `loglik_heston` and `loglik_rs` dynamically but sets `results='hide'`. This means the displayed table values may not match the values actually computed, creating potential reproducibility inconsistency. The hardcoded values should be replaced by in-line R expressions referencing the computed objects.

### 12. (Minor) No Effective Sample Size (ESS) Diagnostics Reported

The authors claim in Section 5.1 that "effective sample sizes stabilizing over iterations" did not indicate particle degeneracy, but no ESS plots or numerical summaries are provided. For a POMP analysis at this level, monitoring ESS (e.g., from `pfilter` output or via `filter.traj`) is standard practice and should be shown to support claims of numerical stability.

### 13. (Minor) Discussion References Prior Course Projects as If They Were Published Studies

Section 7 critiques "Project 7 (Winter 2022)," "Project 6 (Winter 2024)," and "Project 11 (Winter 2024)" as methodological comparisons. While this is interesting context, these are student course projects, not peer-reviewed literature, and the claims about their errors (e.g., "mixed per-day POMP likelihoods") are not reproducibly verified in this paper. This section reads more as a literature dismissal than a rigorous methodological contribution.

### 14. (Minor) The Heston Model Lacks a Leverage Effect Despite Discussion of Asymmetry

Section 4.3 explicitly notes that "GARCH does not treat volatility as a latent process" and mentions "leverage effects" as a limitation, yet the Heston model implemented in Section 5.1 also does not include a leverage term (i.e., no correlation between the return and volatility innovations). The standard continuous-time Heston model includes a correlation parameter `rho` between the Brownian motions driving price and variance. Omitting `rho` means the POMP implementation does not deliver the advertised advantage over GARCH in capturing asymmetry.

### 15. (Minor) Typo in Section Header and Minor Language Issues

Section 2.2 is titled "Stationairty" (misspelling of "Stationarity"). Section 4.1 contains "neccessary" (misspelling of "necessary"). While minor, these suggest the document was not carefully proofread. The acknowledgment that "ChatGPT was used to polish the sentences and correct grammars" (Reference [13]) makes these residual errors more notable.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project12/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project12/data.csv`
