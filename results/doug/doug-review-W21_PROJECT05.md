# Peer Review: W21 Project 05
**Seasonal Influenza in Michigan — POMP Modeling of Contact Rate Change**

---

## Summary

This project investigates the 2019-20 Michigan influenza A season with a focus on the sharp drop in cases following the March 2020 COVID-19 outbreak. Three POMP compartmental models are fitted to weekly positive-test counts from CDC clinical laboratory surveillance: a standard SIR with binomial measurement, a standard SEIR with binomial measurement, and an SIR with a hardcoded time-varying contact rate that applies a 30% reduction after week 22. The project uses iterated filtering (mif2) and replicated particle filtering (pfilter) for inference. Key strengths include appropriate use of the pomp framework with parallelization, clear data sourcing, and honest acknowledgment of model limitations. However, the project has substantial methodological weaknesses: it stops before global search and profile likelihoods, citing NaN log-likelihoods that stem from structural model errors rather than fundamental model inadequacy; the accumulator variable tracks the wrong compartment flow; and the conclusion is drawn from a wrong variable display for the third model. None of the three models is appropriate in its current form, but the failure mode is misdiagnosed.

---

## Major Issues

### 1. Accumulator variable H tracks recoveries, not new infections — fundamental measurement model mismatch

In all three models the process Csnippet accumulates `H += dN_IR` (transitions from I to R, i.e., recoveries), while the observation variable `reports` is `TOTAL.A`, the count of newly confirmed positive influenza A tests. Newly reported positive tests correspond to new infections detected at testing (entries into I, i.e., `dN_SI`), not to recoveries. Recovered individuals are no longer infectious and are not being newly tested and reported. Accumulating recoveries in H and linking reports to H via `dbinom(reports, H, rho, give_log)` makes the model claim that positive test reports are a fraction `rho` of people who recover — a biologically incorrect interpretation. The parameter `rho` therefore absorbs the ratio of recoveries to new detections rather than the true reporting rate. All parameter estimates across all three models are affected by this misspecification (Wheeler et al. 2024; see also `pomp-accumvar-semantic-audit`).

**Fix:** Change `H += dN_IR` to `H += dN_SI` in all three process Csnippets so the accumulator tracks new infections that are subsequently observed at rate `rho`.

### 2. Third model displays the wrong likelihood — SIR1 value shown for SIR2

In the chunk `SIR2_init_lik` (line 458), the code computes `sir2_L_pf` for the third model but then calls `print(sir_L_pf)`, printing the likelihood of the first SIR model rather than the third. The `sir2_lik.csv` artifact contains the correct third-model likelihood (best value approximately -333.4 at the local search maximum), while the value actually displayed in the rendered output is the SIR1 initial-guess likelihood (approximately -1278). Any informal comparison of initial-guess likelihoods across models based on the displayed output is therefore invalid for the third model. This is a copy-paste display error consistent with the `pomp-wrong-variable-display-audit` pattern.

**Fix:** Replace `print(sir_L_pf)` with `print(sir2_L_pf)` in the `SIR2_init_lik` chunk.

### 3. Binomial measurement model causes structural particle filter collapse

The measurement model uses `dbinom(reports, H, rho, give_log)`. The binomial distribution requires `reports <= H`; when the simulated epidemic is smaller than observed (H < reports), the density is exactly zero, the log-likelihood is -Inf, and the particle filter collapses. This is a structural cause of the NaN log-likelihoods described in the text for models 1 and 3. Because the local search is run from initial conditions where this boundary is frequently violated, the reported instability is attributable to the measurement model choice rather than to fundamental model misspecification. The SIR2 model achieves far better log-likelihoods in `sir2_lik.csv` (best -333.4) than SIR1 (best -940.4), suggesting that the parameterization matters enormously — and that an appropriate measurement model might resolve the NaN problem.

**Fix:** Replace the binomial measurement model with a negative binomial: `lik = dnbinom_mu(reports, mu=rho*H, size=psi, give_log)` in `dmeas` and correspondingly `reports = rnbinom_mu(psi, rho*H)` in `rmeas`, adding an overdispersion parameter `psi`. This eliminates the hard upper bound on `reports` and allows the particle filter to assign nonzero likelihood even when simulations are smaller than observed counts.

### 4. No global search — convergence conclusions are premature

Only 20 local mif2 replicates from a single fixed starting point are run for each model. No global box search is conducted. The conclusion that models 1 and 3 "are not appropriate for fitting the data" is based entirely on unstable local searches. NaN log-likelihoods in some replicates indicate particle filter collapse at specific parameter values, not that the model is fundamentally incapable of fitting the data. Wheeler et al. (2024) identify computational adequacy as a core requirement; a global search from diverse starting points is the standard method for establishing whether a parameter region with good likelihood exists.

**Fix:** Run a global search using a parameter box with multiple random starting points (at minimum 20 replicates from a box spanning biologically plausible ranges). Compare the best global log-likelihood to the local search result.

### 5. Hardcoded 0.7 contact-rate reduction factor is not estimated

The third model multiplies `Beta` by `0.7` after week 22. This 0.7 reduction factor is fixed by hand and is not a parameter subject to likelihood maximization. The core scientific hypothesis — that the contact rate changed with the COVID-19 outbreak — is therefore not tested by inference; the 30% reduction is assumed a priori. The research question asks whether POMP models can model the change in contact rate, but the approach taken answers only whether a manually imposed reduction can approximate the data pattern.

**Fix:** Introduce the reduction factor as a free parameter `kappa` constrained to (0,1] via a logit or log transformation, and include it in the mif2 random-walk perturbations. The MLE and profile likelihood for `kappa` would provide evidence-based estimation of the contact-rate change.

### 6. No non-mechanistic benchmark comparison

No ARIMA, ARMA, or negative binomial IID benchmark is fitted. Wheeler et al. (2024) and the course materials identify this as the single most diagnostic check for whether a mechanistic model captures meaningful structure. The conclusion that all three models are inappropriate is stated without reference to any baseline — the models might in fact outperform a simple benchmark for certain parameterizations, which would be meaningful positive evidence. Conversely, if they fail to beat a benchmark, that too is more informative than NaN log-likelihoods during local search.

**Fix:** Fit an ARIMA model to the 52-week series (checking seasonal period appropriately for weekly data) and compare log-likelihoods. This requires only a few lines of code and adds substantial interpretive value.

### 7. No profile likelihoods or confidence intervals

No profile likelihoods are computed for any parameter in any model. Without profiles, there is no assessment of whether parameters are identifiable, and reported point estimates from local search have no attached uncertainty. The confounding between `rho` (reporting rate), `eta` (initial susceptible fraction), and `Beta` is a known identifiability challenge in epidemic POMP models. Wheeler et al. (2024) §5 explicitly requires profile likelihoods for key parameters.

**Fix:** After a global search establishes a stable parameter region, compute profile likelihoods for `Beta` and `rho` using `profile_design()` with the profiled parameter excluded from `rw.sd`.

### 8. Large log-likelihood standard errors indicate particle filter degeneracy

The `sir_lik.csv` artifact shows log-likelihood standard errors of 95.2 and 105.1 for the two best SIR local-search replicates. The `seir_lik.csv` shows SEs ranging from 3.8 to 197.4 for SEIR replicates. Standard errors of this magnitude indicate that the 10 pfilter replicates used to evaluate each local-search endpoint produce wildly inconsistent estimates — the reported log-likelihood values are dominated by Monte Carlo noise, not by the actual likelihood surface. The text does not acknowledge this issue, and the reported parameter estimates cannot be trusted when SEs exceed 1–2 units.

**Fix:** Flag any replicate with loglik.se > 1 as unreliable for parameter comparison. Use more particles (Np ≥ 5000) or more pfilter replicates (at least 10, ideally 50) with `logmeanexp` to obtain stable likelihood evaluations.

---

## Minor Issues

### 9. Log-likelihood direction inverted in SEIR conclusion

The SEIR local-search section states "the current lowest loglikelihood is around -860.9967" and treats this as the best fit. In standard statistical convention, higher log-likelihood (less negative, closer to zero) indicates better fit. The phrase "lowest log-likelihood" inverts the comparison and is misleading, even though the SEIR does have the highest (best) log-likelihood among the three models based on the CSV files. This is a known confusion documented in the `pomp-loglik-direction-error` skill.

**Fix:** Replace "lowest loglikelihood" with "highest log-likelihood" (or "least negative log-likelihood") throughout the document when describing which model fits best.

### 10. SEIR pomp object inherits incomplete partrans from fluSIR

The SEIR model is first built in the `SEIR_building` chunk using `fluSIR %>% pomp(rprocess=..., rinit=..., paramnames=..., statenames=...)`, inheriting the `partrans` from `fluSIR` (which declares transformations for `Beta`, `mu_IR`, `rho`, `eta`). This inherited `partrans` does not include `mu_EI`, which the SEIR model adds. The `fluSEIR` object used in the initial pfilter therefore has no declared transformation for `mu_EI`, leaving it on the natural scale during optimization. The SEIR is correctly rebuilt in the `SEIR_par` chunk with a new `partrans` that includes `mu_EI`, but any pfilter results reported from the first `fluSEIR` object (the initial-guess likelihood in chunk `SEIR_init_lik`) use the incomplete transformation.

**Fix:** Build `fluSEIR` directly from `df %>% pomp(...)` rather than by modifying `fluSIR`, or confirm that the initial `fluSEIR` partrans does include `mu_EI`. Alternatively, rebuild `fluSEIR` only once in the `SEIR_par` section and use that object for all downstream computations.

### 11. Population N fixed without biological justification or sensitivity assessment

Michigan's total population (9.984 million) is used as N throughout all models, initializing about 8.5% of this (approximately 848,000 people) as susceptible (`eta ≈ 0.0853`). The effective susceptible pool for seasonal influenza is much smaller due to prior immunity, age structure, and vaccination. No justification is provided for these values, no sensitivity analysis is performed, and the estimated `eta` values do not change substantially across local search replicates in any model. The biological plausibility of using total population as N is never discussed.

**Fix:** Discuss the biological rationale for the chosen N. Consider using the estimated susceptible population from prior immunity and vaccination data, or estimate N as a free parameter with appropriate bounds.

### 12. Week-22 COVID-19 breakpoint is chosen by inspection, not justified externally

The third model applies the contact-rate reduction from week 22 onward. Week 22 of the 2019-20 dataset corresponds to approximately the 10th week of 2020 (early-to-mid March 2020). Michigan's first COVID-19 case was detected in early March 2020, and Governor Whitmer's stay-home order was issued on March 24, 2020 (closer to week 24-25 of the dataset). The text does not document which specific event motivates week 22, and no sensitivity analysis tests alternative breakpoints.

**Fix:** State the specific external event corresponding to week 22, or introduce the breakpoint as a model parameter to be estimated or profiled over a plausible range.

### 13. No model diagnostics beyond visual simulation overlay

The only diagnostic for each model is a visual overlay of 20 simulations against the data. No conditional log-likelihood plots, no effective sample size (ESS) monitoring, no per-observation likelihood decomposition, and no summary-statistic comparison are provided. Wheeler et al. (2024) §4 explicitly identifies visual comparison as insufficient and recommends conditional log-likelihood plots to identify specific periods of poor fit.

**Fix:** Plot per-observation conditional log-likelihoods from the best local-search pfilter run for each model. This would reveal which weeks drive particle degeneracy (likely the peak weeks where H < reports under the binomial model).

### 14. Only 50 IF2 iterations with Np=2000 — computational effort not assessed

Each local search uses Np=2000 and Nmif=50. At 52 observations per season, 2000 particles is borderline, and 50 iterations may be insufficient for the cooling schedule to reach convergence. The trace plots are described as "bouncing around," consistent with numerical noise at these settings. No evidence is presented that increasing computational effort was explored.

**Fix:** Report a second local search with Np=5000 and Nmif=100 to assess whether the instability is numerical rather than structural. Report the final log-likelihood values at the end of the cooling schedule.

### 15. Research question mismatches the analysis performed

The stated research question asks whether POMP models can model the change in contact rate of influenza in Michigan. The third model imposes a change by hand rather than estimating it, so the research question is not answered by inference. The conclusion should either acknowledge this gap or be reframed as a model-building exercise that establishes the framework for a future estimation study.

**Fix:** Either estimate the contact-rate reduction factor as a parameter (addressing the research question) or reframe the conclusion to accurately describe what was and was not inferred from the data.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project05/sir_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project05/seir_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project05/sir2_lik.csv`
