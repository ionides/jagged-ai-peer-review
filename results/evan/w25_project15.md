# Final AI Review: Volatility Analysis on Bitcoin Returns — A Fear & Greed Index Perspective
## STATS 531 Final Project, w25 Project 15

---

## Overall Assessment

This project addresses a genuine scientific question — whether market sentiment as captured by the Fear and Greed Index improves stochastic volatility models for Bitcoin returns — and assembles an impressive breadth of models: GARCH, two Breto variants, and two Heston-style simple stochastic volatility (SSV) models, each fit under both Normal and t-distributed measurement models. The computational infrastructure is solid: replicated particle filtering with `logmeanexp` aggregation, correct run-level settings (Np=2000, Nmif=200, Nreps_global=100), and thoughtful handling of the multimodal likelihood surface through a two-stage global search. However, several significant issues undermine the reliability of the conclusions. A process equation error in both SSV models means those likelihoods correspond to a different model than described. Profile likelihoods are absent for any model, leaving the key scientific parameter (gamma_fng) without a confidence interval and the claim about fear driving volatility without statistical foundation. The comparison between GARCH and POMP models requires clarification about likelihood normalization. These issues need to be addressed before the conclusions can be fully trusted.

---

## Key Strengths

**25.15.S1 — Correct likelihood aggregation**
The paper consistently uses `logmeanexp` to aggregate replicated particle filter log-likelihoods, which is the correct procedure. Standard errors are also reported, indicating awareness of Monte Carlo variability.

**25.15.S2 — Adequate computational effort**
run_level=3 with Np=2000, Nmif=200, and Nreps_global=100 represents solid computational investment. The use of SLURM-aware core detection suggests the code was run on an HPC cluster.

**25.15.S3 — Multimodality diagnosis and two-stage global search**
The paper correctly identifies that mu_h and phi are entangled through the term (1-phi)*mu_h, producing two convergence paths. The subsequent restricted global search (Section 2.2.4) focusing on the superior mode is a methodologically sound approach to isolating the true optimum, and this is a genuine contribution of the analysis.

**25.15.S4 — Correct Jacobian in t-distribution measurement model**
The dmeasure for both t-distributed models correctly applies the log-Jacobian adjustment (`- log(exp(H/2))`), which is a common source of error. This is implemented correctly.

---

## Major Points

**25.15.1 — SSV process equation inconsistency between code and model (Severity: Major)**

*Concern:* The stated mathematical model for the simple stochastic volatility (SSV) is a mean-reverting (CIR-type) process:
V_n = (1-phi)*theta + phi*V_{n-1} + xi*sqrt(V_{n-1})*omega_n
However, both SSV implementations (Sections 2.5.2 and 2.6.1) use:
```c
V = theta * (1 - phi) + phi * sqrt(V) + sqrt(V) * omega;
```
The code uses `phi * sqrt(V)` where the model requires `phi * V`. These are different dynamical systems with different stationary distributions and qualitative behavior. All log-likelihoods reported for both SSV models (~3957 normal, ~4070 t-distribution) describe the misspecified model, not the one stated.

*Why it matters:* Model comparison conclusions involving the SSV models cannot be trusted until the code matches the stated model.

*Suggested author action:* Replace `phi * sqrt(V)` with `phi * V` in the Csnippet for both SSV models, rerun all SSV-related inference, and update all tables and figures that involve these models.

---

**25.15.2 — No profile likelihoods or confidence intervals for any model (Severity: Major)**

*Concern:* The paper's central scientific claim is that the gamma_fng parameter is negative, implying that fear drives volatility more than greed. However, no profile likelihood or confidence interval is reported for gamma_fng or any other parameter across all six models. Without a CI for gamma_fng, its statistical significance cannot be assessed.

*Why it matters:* The claim about fear vs. greed is the paper's novel scientific finding. Without quantified uncertainty, the reader cannot determine whether gamma_fng is significantly different from zero, or whether the local and global search discrepancy (positive gamma at 4075.35 vs. negative gamma at 4075.01, within Monte Carlo error) reflects genuine bimodality with different signs — which would mean the sign of gamma is simply not identifiable from these data.

*Suggested author action:* Compute a profile likelihood for gamma_fng over a grid of values (e.g., -2 to 2 in steps of 0.2), holding other parameters at their MLE via mif2. Report a 95% MCAP CI. If the CI includes zero, soften the fear-drives-volatility claim.

---

**25.15.3 — Gamma_fng sign instability between local and global search (Severity: Major)**

*Concern:* The local search for the modified Breto (normal) model finds gamma_fng = +0.13 (positive, implying greed drives volatility) at logLik = 4075.35 ± 0.34. The global search finds gamma_fng = -0.89 (negative, implying fear drives volatility) at logLik = 4075.01 ± 0.87. These log-likelihoods are indistinguishable within Monte Carlo error. The paper acknowledges the discrepancy but concludes in favor of the global result without adequate justification.

*Why it matters:* If two modes of the likelihood surface — one with positive gamma and one with negative gamma — yield essentially equal log-likelihoods, then the sign of gamma is not identified from these data at this resolution. The paper's main conclusion depends directly on the sign of gamma.

*Suggested author action:* Run a profile likelihood for gamma_fng (see 25.15.2). If both signs yield similar profile likelihood values, acknowledge that gamma_fng is not identifiable from these data and that the fear-vs-greed inference cannot be drawn.

---

**25.15.4 — GARCH benchmark comparison needs clarification (Severity: Major)**

*Concern:* The Conclusion (Section 4) states that the "basic Breto model outperforms the benchmarks (GARCH and simple stochastic volatility model)." However, Section 2.1 cites the course quiz solution [12] to note that `tseries::garch` log-likelihoods cannot be directly compared to those from other packages. The paper cannot simultaneously flag the non-comparability and use GARCH as a beaten benchmark. Additionally, the course quiz solution [12] states that "likelihoods from different model classes ARE directly comparable for the same data" — the issue is specifically about normalization conventions within `tseries::garch`, not a fundamental impossibility.

*Why it matters:* Without a valid GARCH benchmark, it is not established that any POMP model represents an improvement over a non-mechanistic alternative.

*Suggested author action:* Refit a GARCH(1,1) or GARCH(3,1) model using the `rugarch` package, which provides likelihoods on a standard scale. Alternatively, fit an ARMA model to the demeaned log returns and use that as the benchmark. Remove the conclusion that GARCH has been beaten until a valid comparison is available.

---

**25.15.5 — Gamma interpretation conflates changes with levels (Severity: Major)**

*Concern:* The model uses the first-differenced FG index (Delta_FNG) as the covariate. The interpretation in Section 2.3.1 states: "When I_n < 50: Fear dominates, resulting in negative FNG_scaled." This interprets the *level* of the FG index. But the model incorporates the *change* in FNG_scaled, not its level. Gamma describes the effect of a unit increase in Delta_FNG on log-volatility — it governs whether an increase in sentiment (from fear toward greed) raises or lowers volatility, not whether fear or greed is the dominant level.

*Why it matters:* The scientific interpretation of the main result is incorrect as currently stated.

*Suggested author action:* Revise the interpretation of gamma to state: "A negative gamma means that a day-over-day increase in the sentiment index (movement toward greed) is associated with a decrease in log-volatility, while increasing fear (decreasing index) is associated with higher volatility." This is more precise and avoids the level/change conflation.

---

## Minor Points

**25.15.M1 — ACF used without formal test to justify differencing**
The decision to difference the FG index rests on visual inspection of the ACF (Figure 14), showing slow decay. A slowly decaying ACF is consistent with both unit-root non-stationarity and stationary long-memory. An ADF or KPSS test would provide formal justification for the differencing choice.

**25.15.M2 — Degrees of freedom for t-distribution selected informally**
df=5 was selected by trying values 3–25. This informal search over degrees of freedom constitutes implicit model selection without likelihood adjustment. Reporting the log-likelihoods for at least a few df values (e.g., 3, 5, 10) would help justify the choice, or df could be estimated as a free parameter.

**25.15.M3 — Missing consolidated model comparison table**
The six models' best log-likelihoods and MC standard errors are scattered across separate sections. A single summary table with all models, their parameter counts, max log-likelihoods, SEs, and AIC values would allow the reader to evaluate the comparison efficiently and transparently.

**25.15.M4 — Inconsistent reported likelihood for SSV normal model**
Section 2.5.4 text states "high log-likelihood value (~3899.52)" for the simulated-vs-observed comparison, but the code output reports 3957.105 as the best log-likelihood. This appears to be a copy-paste error from an earlier draft.

**25.15.M5 — sigma_nu converges near zero in modified Breto models**
In both modified Breto models, sigma_nu converges to very small values (~1e-5 to ~2e-3). This suggests the G random walk component is nearly degenerate and the leverage mechanism may be weakly identified. A brief note on what near-zero sigma_nu implies for the model's leverage behavior would be informative.

**25.15.M6 — No reproducibility archive**
Code is shown inline, but no standalone script file or data archive is linked or referenced. Providing a GitHub link or supplementary archive would allow independent verification.

**25.15.M7 — Typos and text errors**
"aerbecause" (Section 2.2.4), "divergenece," "demanded return" (should be "demeaned return"), "mispecified." These likely survived the ChatGPT polishing pass [15] and should be corrected.
