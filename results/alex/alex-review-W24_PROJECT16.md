# Peer Review: W24 Project 16
## Modelling of Influenza Cases and Spread in the Netherlands Using ARIMA and POMP (SEIR) Models

---

### Summary

This project models the 2022-2023 influenza season in the Netherlands using a split SEIR POMP model that separates vaccinated and unvaccinated sub-populations. The stated goal is to quantify the effect of vaccination on transmission rate (Beta) and recovery rate (mu_IR). While the scientific motivation is interesting, the model contains fundamental structural flaws, the statistical inference is poorly characterized, and several key methodological claims are not adequately supported.

---

### Weaknesses (prioritized from most to least critical)

---

**1. [Major] The two sub-populations are completely decoupled — there is no cross-infection between vaccinated and unvaccinated compartments.**

The `seir_step` Csnippet computes the vaccinated exposure rate as `Beta_v * I_v / N` and the unvaccinated exposure rate as `Beta_u * I_u / N`. Vaccinated susceptibles can only be infected by vaccinated infectious individuals, and unvaccinated susceptibles can only be infected by unvaccinated infectious individuals. In any realistic influenza model, a vaccinated person can be infected by an unvaccinated infectious contact and vice versa. This renders the entire model epidemiologically incoherent: the two branches evolve independently, so the "vaccination effect" being measured is not a realistic mixing effect but an artifact of an artificially separated system. The force of infection for each group should include contributions from both `I_v` and `I_u` (scaled by their respective transmission rates).

---

**2. [Major] The susceptible initialization formula is misspecified and contradicts the written description.**

The paper states:
- $S_v = \text{vaccinationRate} \times \eta_v \times N$
- $S_u = \text{vaccinationRate} \times \eta_u \times N$   *(the paper actually writes "vaccinationRate" for both)*

The `seir_rinit` code initializes:
- `S_v = nearbyint(vac_rate * eta_v * N)`
- `S_u = nearbyint((1-vac_rate) * eta_u * N)`

The formula in the text for $S_u$ uses `vaccinationRate` (not `1 - vaccinationRate`), which is an error in the writeup. More critically, both initializations scale `eta` by either `vac_rate` or `(1 - vac_rate)`, so `eta_v` and `eta_u` do not represent susceptible fractions within each vaccination stratum as described — they end up partially confounded with the group size. This makes the biological interpretation of `eta_v` and `eta_u` ambiguous and inconsistent with the stated rationale.

---

**3. [Major] The accumulator variable H counts recoveries (IR transitions), not new infections — the model measures reported recoveries, not reported cases.**

`H += dN_IR_v + dN_IR_u` accumulates individuals transitioning from I to R. Yet the data column `INF_ALL` represents newly detected influenza cases. Detected cases should correspond to new infectious individuals (EI transitions) scaled by a reporting rate, not recoveries. Because influenza has a short infectious period (a few days), the peak timing of recovery transitions will be shifted relative to the peak of new infections. This is a fundamental mismatch between the measurement model and the data-generating process.

---

**4. [Major] The rho parameter is applied a second time inside dmeas/rmeas after already being intended as a reporting fraction, effectively double-discounting H.**

In `seir_dmeas`, the code computes `total_H = rho * H` and uses that as the mean of the negative binomial. However, H is itself already an accumulation of IR transitions for all individuals — the reporting fraction `rho` should be applied once and unambiguously. Combining this with issue 3 (H being recoveries rather than infections) means the measurement model has a doubly incorrect interpretation.

---

**5. [Major] No simulation from the fitted model is presented; there is no visual check that the POMP model can reproduce the observed data.**

Standard practice in POMP modeling is to simulate from the fitted (or near-optimal) parameter estimates and overlay those trajectories on the observed data. This project includes no such plot, making it impossible to judge whether the model captures the shape, peak timing, or scale of the 2022-2023 influenza season. The `run.r` script contains a `simulate()` call, but the resulting plot is never included in the report.

---

**6. [Major] The profile likelihood plots are not genuine profile likelihoods — they are scatter plots of marginal loglik vs. parameter value from a global search, not profiled over nuisance parameters.**

The figures presented for Beta_v, Beta_u, mu_IR_v, mu_IR_u, and the two ratios are produced by filtering the global search results and plotting the top values. A profile likelihood requires, for each fixed value of the parameter of interest, maximizing the likelihood over all other free parameters. The plots shown are ad hoc slices of the global search cloud, which gives a much wider and less informative picture than a true profile. Confidence intervals derived from these plots using the chi-squared cutoff are not statistically valid.

---

**7. [Major] The local MIF2 convergence diagnostic (iterated filtering traces) shows no evidence of convergence before the global search is run.**

The traces plot from `mifs_local` (4 chains, 300 MIF iterations, `cooling.fraction.50 = 0.2`) is presented but not discussed. In particular, the large random walk standard deviations (e.g., `Beta_v = 0.15`, `Beta_u = 0.15`) combined with a very fast cooling schedule may cause the chains to not properly explore the likelihood surface. No quantitative evidence (e.g., replicated likelihood estimates near convergence) is provided to confirm that the local search has converged before seeding the global search.

---

**8. [Major] The reported "best" log-likelihood from the global search is described as a "negative log likelihood maximum (likelihood minimum)," which is a conceptual error.**

The text states: "The negative log likelihood in these runs reach a maximum (likelihood minimum) at:" followed by the output of `logmeanexp(profile_results$loglik, se=TRUE)`. The values stored in `profile_results$loglik` are log-likelihoods (not negative log-likelihoods), because `logmeanexp` is called on the direct output of `pfilter |> logLik()`. Maximizing log-likelihood is the goal, not minimizing it, and describing this as a "likelihood minimum" is incorrect.

---

**9. [Minor] The dispersion parameter k is fixed at 10 with no justification.**

The negative binomial overdispersion parameter `k` is held fixed throughout the analysis. No sensitivity analysis is performed to assess how results change under different values of `k`, and no epidemiological or statistical rationale is offered for choosing 10. Given that `k` can substantially influence the likelihood surface and parameter estimates, this choice should be justified or treated as a free parameter to estimate.

---

**10. [Minor] The data subsetting logic (rows 1-99 vs. rows 100-198) is fragile and not validated.**

The split `fluNL[1:99,] -> fluNL_sentinel` and `fluNL[100:198,] -> fluNL_nonsentinel` assumes that rows 1-99 correspond exactly to sentinel observations and rows 100-198 to non-sentinel observations. This is never verified against the `ORIGIN_SOURCE` column. If the underlying WHO dataset ordering changes, this hard-coded split could silently mix sentinel and non-sentinel data.

---

**11. [Minor] The population size N is set to the total Netherlands population (17.7 million), but the data is from sentinel surveillance — only a fraction of actual cases are captured.**

Sentinel surveillance covers a small, fixed set of providers and the case counts are typically much smaller than true population incidence. Using N = 17,700,000 as the total population without adjustment means the susceptible pool is orders of magnitude larger than the effective observed population, which likely inflates the estimated transmission rates and makes epidemiological interpretation (e.g., R0) unreliable.

---

**12. [Minor] The model diagram label uses "mu_SE" for the S-to-E transition rate, but the code uses "Beta" — the notation is inconsistent between the figure and the model.**

The FluSEIR.png diagram labels the S-to-E arrows as `mu_SE_v` and `mu_SE_u`, whereas the Csnippet code and parameter names throughout the analysis use `Beta_v` and `Beta_u`. This inconsistency makes the diagram misleading.

---

**13. [Minor] The interpretation of mu_IR_v < mu_IR_u (vaccinated take longer to recover) is speculative and epidemiologically questionable without supporting data.**

The paper concludes that vaccinated people who get infected take longer to recover, attributing this to preexisting conditions or weakened immune systems. However, given the structural flaws in the model (decoupled compartments, wrong H accumulation), this result cannot be taken at face value. Furthermore, no literature support is provided for this specific interpretation of mu_IR in the context of flu vaccination.

---

**14. [Minor] The ARIMA section adds limited value and is not integrated with the POMP analysis.**

The paper uses ARIMA as a "reference" but does not quantitatively compare ARIMA and POMP (e.g., via AIC on a common scale, predictive accuracy, or likelihood ratio). The ARIMA section serves mainly as motivation for why the authors chose POMP, but the discussion is superficial and the AIC comparison between ARIMA model orders is not related back to the POMP model selection.

---

**15. [Minor] Reproducibility is partially broken: the global search relies on a pre-saved RDS file from a cluster run, but the cluster script (run.r) saves to a different path than the one read in the Rmd.**

The cluster script saves to `greatlakes_runs/global_search_2.rds`, but `Blinded.Rmd` reads from `global_search.rds` (no subdirectory). The local `run.r` file also contains `read_rds("/Users/falarcon/Desktop/all/global_search_2.rds")` — an absolute personal path that cannot be reproduced by anyone else. The seeding also differs between the two scripts (`registerDoRNG(542451)` in `run.r` vs. `set.seed(2488820)` in `Blinded.Rmd`, with `registerDoRNG` commented out in `Blinded.Rmd`), further undermining reproducibility.

---

### Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/Blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/run.r`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/FluSEIR.png`
