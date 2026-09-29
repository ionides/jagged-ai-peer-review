---
title: "Review: W24 Project 06"
subtitle: "*Volatility Analysis of NASDAQ*"
---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (`mif2`) with replicated `pfilter` re-evaluation via `logmeanexp`; local + box global search |
| **R packages used** | `pomp`, `rugarch`, `fGarch`, `tseries`, `doParallel`, `doRNG`, `tidyverse` (versions not pinned) |
| **Code publicly available** | Partial — Rmd, Makefile, and `NDAQ.csv` present; no cached `.rda` files in submission, no README, no `sessionInfo()` |
| **Data publicly available** | Yes — `NDAQ.csv` (NASDAQ daily OHLCV, approximately 2019–2024) included |
| **Benchmark comparison included** | Yes — ARMA(4,4), GARCH(4,1)-normal, GARCH(1,1)-t, ARMA(4,4)+GARCH(1,1)-t all fit and compared |

---

## POMP Checklist Scorecard

*✓ = satisfies practice, ~ = partially satisfies, ✗ = does not satisfy, N/A = not applicable*

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ✓ | IF2 + replicated `pfilter`, `logmeanexp(se=TRUE)` used for aggregation |
| 2 | Benchmark comparison | ✓ | Four non-mechanistic models fit and compared quantitatively |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported for all models, but GARCH values are mislabeled (see Major Issue 4) |
| 4 | Model diagnostics | ✗ | No ESS monitoring, no conditional log-likelihood plot, no post-fit forward simulation from final MLE |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods or confidence intervals for any POMP parameter |
| 6 | Computational adequacy | ~ | `run_level=3`, `stew()` caching, and multiple starts used, but global search box is inconsistent with local search findings |
| 7 | Forecast methodology | N/A | No forecasting attempted |
| 8 | Model variations and nested comparisons | ~ | Multiple benchmark variants compared; only one POMP specification tried |
| 9 | Stochasticity | ✓ | Standard stochastic volatility leverage model with process noise on `H_n` and `G_n` |
| 10 | Reproducibility and extendability | ~ | `stew()` caching and `write.table` to `NADQ_params.csv` are good; no README, no package versioning |
| 11 | Corroboration with scientific knowledge | ✗ | `sigma_eta` ranging up to 50 and `sigma_nu` converging near 0 never examined for plausibility |
| 12 | Measurement model specification | ~ | Standard course template; covariate pass-through is correct, but input series is misnamed "demeaned" |
| 13 | Initial conditions | ~ | `G_0`, `H_0` estimated as parameters; `H_0` explicitly fails to converge with no follow-up |

*Checklist based on Wheeler et al. (2024), PLOS Computational Biology 20(4): e1012032.*

---

## Summary

The project fits ARMA, GARCH (normal and t-distributed noise), ARMA+GARCH, and a stochastic-volatility POMP model to five years of NASDAQ daily log returns. The benchmark suite is a genuine strength: four progressively flexible non-mechanistic alternatives are quantitatively compared, going well beyond the course minimum. However, the POMP analysis is materially incomplete. Most critically, the global search box is specified over parameter ranges that entirely exclude the region the paper's own local search already identified as promising — meaning the "global" search does not actually improve on the local search and directly explains the reported non-convergence of `mu_h` and `H_0`. Beyond this, no profile likelihoods, confidence intervals, ESS traces, conditional log-likelihoods, or post-fit simulation diagnostics are presented. The GARCH benchmark section also conflates the `rugarch` log-likelihood output with the raw likelihood and then takes a meaningless second logarithm. The paper's conclusion honestly acknowledges underperformance of the POMP model but cannot diagnose why, because the diagnostics required to answer that question are absent.

**Strengths:**
- Thorough, multi-model benchmark comparison (ARMA, GARCH-normal, GARCH-t, ARMA+GARCH-t) with AIC-based order selection in each case.
- Correct use of `logmeanexp(se=TRUE)` to aggregate particle filter log-likelihoods, avoiding the common log-scale averaging error (Error 1.1 in weakness reference).
- `stew()` caching and `write.table` to a parameter CSV provide a reasonable reproducibility scaffold.
- Honest acknowledgment that the POMP model underperforms and that key parameters did not converge.

**Weaknesses:**
- Global search box (`NADQ_box`) excludes the parameter regions identified as optimal by the paper's own local search.
- No profile likelihoods, confidence intervals, ESS traces, conditional log-likelihoods, or post-fit simulation diagnostics.
- Non-convergence of `mu_h` and `H_0` noted but never investigated or resolved.
- GARCH log-likelihood mislabeled as "likelihood"; a meaningless second logarithm reported as "log likelihood."
- ACF and PACF roles reversed in the preliminary model identification discussion.

---

## Major Issues

### 1. Global search box excludes the region the local search identified as optimal

After completing 20 local `mif2` searches from `params_test`, the text states: "the optimal value of sigma_nu is roughly between (0, 0.005), the optimal value of mu_h is around -10, the optimal value of phi is roughly between (0.8, 0.85) and the optimal value of sigma_eta is roughly between (0, 50)." The box specified immediately afterward for the global search is:

```r
NADQ_box <- rbind(
  sigma_nu = c(0.005, 0.05),
  mu_h     = c(-1, 0),
  phi      = c(0.95, 0.99),
  sigma_eta= c(0.5, 1),
  G_0      = c(-2, 2),
  H_0      = c(-1, 1)
)
```

Every one of these ranges is disjoint from or incompatible with the local-search estimates: `sigma_nu`'s box (0.005, 0.05) excludes the identified optimum (0, 0.005); `mu_h`'s box (-1, 0) is ten units away from the reported optimum near -10; `phi`'s box (0.95, 0.99) is disjoint from the local optimum (0.8, 0.85); `sigma_eta`'s box (0.5, 1) is a narrow sliver that doesn't even reach the reported near-zero lower end. A global search that cannot sample the region the local search has already established as best cannot improve on it or provide meaningful further exploration, and directly explains why the global search's best log-likelihood (stated as 3510) barely exceeds the local search's maximum. This also explains the unresolved non-convergence of `mu_h` and `H_0` in the trace plots: the optimizer is being asked to work in entirely the wrong parameter region. **Fix:** re-specify the box to bracket the local-search estimates (e.g., `sigma_nu` in (0, 0.02), `mu_h` in (-15, -5), `phi` in (0.75, 0.92), `sigma_eta` in (0.1, 5)) and re-run.

### 2. No profile likelihoods or confidence intervals for any POMP parameter

Per Wheeler et al. (2024) §Parameter identifiability (checklist item 5) and the course weakness reference (Error 1.9), profile likelihoods should be computed to establish whether parameters are identifiable and to support confidence intervals. The project reports only point estimates via `summary()` of log-likelihoods and `pairs()` scatter plots; no profile likelihood is computed for any of the six POMP parameters. Without profiles, the claim that certain parameters "converge" (sigma_eta, phi) while others do not (mu_h, H_0) is informal: the distinction could reflect a flat or multimodal surface rather than genuine convergence vs. non-convergence, and the paper has no way to distinguish these scenarios. **Fix:** compute profile likelihoods for at least the most interpretable parameters (phi, mu_h) using the standard course `foreach`-over-mif2 workflow.

### 3. No post-fit model diagnostics presented for the fitted POMP model

The only simulation shown in the POMP section uses `params_test`, an initial guess that the authors explicitly note "doesn't fit well." No simulation or diagnostic plot is produced using the final fitted MLE. There is no ESS trace from `pfilter`, no conditional (per-time-step) log-likelihood plot, and no comparison of the fitted model's simulated trajectories to observed data. Wheeler et al. (2024) state that conditional log-likelihood plots and filtering-distribution comparisons are the primary tools for diagnosing where and why a model fails — the very question the Conclusions section poses ("There is definitely something needs to be done to enhance the performance") but cannot answer. **Fix:** add a `simulate()` call using the best parameter vector from the global search and overlay on observed data; extract and plot per-observation log-likelihoods from `pfilter`; plot ESS across time.

### 4. Confusion between log-likelihood and likelihood in the GARCH benchmarks

For each `rugarch` GARCH fit, the code reports both `likelihood(fit)` and `log(likelihood(fit))`, e.g.:

```r
likelihood(nasdaq_garch41_normal)      # 3476.553  (this IS the log-likelihood)
log(likelihood(nasdaq_garch41_normal)) # 8.153797  (this is log of the log-likelihood, meaningless)
```

The `rugarch::likelihood()` function returns the fitted log-likelihood — consistent with the magnitude (~3477 over ~1257 observations is about 2.77 nats per observation, plausible for Gaussian log-returns). The paper then calls `log(3476.553) = 8.15` the "log likelihood," which is a double logarithm with no statistical meaning. This error is documented in the course weakness reference as Error 2.9 (trusting software output without checking conventions). The final cross-model comparison in the Conclusions section uses the correctly-scaled values (3476.553, 3538.77, 3550.09), so the ranking is not corrupted, but the mislabeling and the reported "log likelihood = 8.15" should be corrected. **Fix:** remove the `log(likelihood(...))` calls; label `likelihood()` output clearly as "log-likelihood."

### 5. ACF and PACF roles reversed in preliminary model identification

The preliminary ARMA order identification section states: "The number of significant spikes in the ACF plot is 1, hence, we can assume that the AR term has value 1. Likewise, the number of significant spikes in the PACF plot is 4. Hence, it can be inferred that the MA term is 4." This has the diagnostic roles reversed: for a pure MA(q) process, the ACF cuts off after lag q; for a pure AR(p) process, the PACF cuts off after lag p. Using ACF to infer AR order and PACF to infer MA order is a fundamental misunderstanding of ARMA identification. The downstream impact is limited because the authors correctly use a full AIC grid search over all (p,q) combinations to select ARMA(4,4), but the stated reasoning is incorrect and should be fixed. **Fix:** correct the description to state that PACF significant spikes inform AR order and ACF significant spikes inform MA order, or remove the heuristic discussion and rely solely on the AIC table.

### 6. `sigma_eta` local-search range of (0, 50) not interpreted as possible model misspecification

The local search reports that `sigma_eta` is "roughly between (0, 50)" — a 100-fold range with no meaningful upper constraint identified. Per Wheeler et al. (2024) §Corroboration with scientific knowledge (checklist item 11) and §Parameter identifiability (checklist item 5), an essentially unbounded parameter range of this kind is a warning sign of either a coding/units problem or a genuinely non-identified parameter in this dataset. The course explicitly taught (Q10-02/MT2) that implausibly wide or flat parameter estimates should trigger investigation rather than acceptance. The paper does not comment on this finding, and the global search box (0.5, 1) silently narrows this range without acknowledgment. **Fix:** compute a profile likelihood for `sigma_eta`; if the profile is flat, interpret this as evidence that the parameter is non-identified and consider fixing it or reparameterizing the model.

### 7. Non-convergence of `mu_h` and `H_0` reported but not investigated

The trace-plot commentary explicitly states: "`H_0` and `mu_h` do not converge." This is the paper's own diagnosis, but the response is to simply note it as a "Limitations" item and suggest "broader parameters selection." The course weakness reference (Error 1.5) teaches that non-convergence of parameters in an iterated filtering run is a signal of model misspecification, not primarily a computational problem. With the search box issue documented in Major Issue 1, the non-convergence is most parsimoniously explained by the optimizer being confined to a parameter region that is far from the true likelihood maximum — but the paper does not consider this explanation. **Fix:** address Major Issue 1 first; if non-convergence persists with a corrected box, compute a profile likelihood for `mu_h` to determine whether it is identifiable, and consider whether the measurement model or process model should be revised.

---

## Computational and Diagnostic Assessment

**Convergence:** Local-search log-likelihoods are summarized via `summary(r.if1$logLik)` and global-search via `summary(r.box$logLik)`. The global maximum (stated as 3510 in the text) barely exceeds the local maximum — consistent with Major Issue 1, where the global search box excludes the local optimum's parameter region. The `plot(if.box)` trace plots are shown and reveal non-convergence in `mu_h` and `H_0`. Multiple search replicates (Nreps_local = 20, Nreps_global = 100) are used, which is appropriate effort, but they cannot compensate for a misspecified search box.

**Particle filter:** `NADQ_Np = 2000` at `run_level=3`. The course reference table suggests Np=5000 at this level, though this is context-dependent. No ESS values are extracted or discussed; filter degeneracy cannot be ruled out.

**Conditional log-likelihoods:** Not computed or plotted anywhere in the report.

**Profile likelihoods:** None computed (see Major Issue 2).

**Computational scale:** `system.time()` is stored in `t.pf1` and `t.if1` but never printed in the rendered output; no wall-clock time or CPU-hours are reported in the text.

---

## Reproducibility Assessment

**Code availability:** Rmd, Makefile, and `NDAQ.csv` are present; no separate archive is expected for a course project. The `stew()` caching mechanism means expensive computations are only re-run when `.rda` files are absent, which is good practice.

**Final parameters:** `write.table` appends parameter rows to `NADQ_params.csv` during both local and global searches. However, this file is not included in the submission materials, and no single isolated "best fit" parameter vector is extracted and reported as the definitive MLE.

**Model-code consistency:** The C snippets for `dmeasure`, `rmeasure`, and `rprocess` match the mathematical description in the text. However, `demeaned_returns <- as.numeric(ts_data)` does not subtract the mean (mean ≈ 0.00058, sd ≈ 0.018; numerically small but a real code-text mismatch given the model explicitly assumes demeaned `Y_n`).

**Package versions:** No `sessionInfo()`, no `renv`, no package pinning. `pomp` and `rugarch` APIs have changed across versions; exact reproduction on a different environment is not guaranteed.

**Auxiliary data:** Only `NDAQ.csv` is needed and is included. No auxiliary inputs are required.

**HPC reproducibility:** Code detects `SLURM_NTASKS_PER_NODE`, indicating cluster use, but no job-submission script, environment specification, or timing output is included.

---

## Minor Issues

- The pairs plot threshold `logLik > max(logLik) - 300` is far too permissive: the Wilks 95% confidence region for 4 parameters spans only ~4.74 log units below the MLE. Including points 300 log units below adds no diagnostic information about parameter uncertainty and may obscure the shape of the likelihood near the maximum. The standard course practice uses a threshold of about 10 units.
- `demeaned_returns <- as.numeric(ts_data)` performs no demeaning (the mean is not subtracted). The variable name promises a transformation that does not occur. Numerically minor, but creates a code-text mismatch.
- The text states "the global maximum log likelihood is 3510," which does not exactly match either printed `summary()` output (whose maxima are 3509 and 3513 respectively, as the rendered HTML shows).
- `Nreps_local = 20` at `run_level=3` is the same as at `run_level=2`; the course reference table suggests 40 at `run_level=3`. This is minor given that the box misspecification (Major Issue 1) is the binding constraint, but worth noting.
- No AIC is reported for the POMP model, only raw log-likelihood. For a fair parsimony comparison with the benchmark models (which were selected by AIC), AIC for the POMP model (6 parameters) should also be reported.
- Only one POMP model structure is tried (the course's standard leverage specification). In contrast, four structural variants are tried on the benchmark side. At minimum, a no-leverage variant (setting `beta = 0`) would test whether the leverage component adds value.
- No README, no `sessionInfo()`, and no package version documentation; exact reproduction on a different `pomp`/`rugarch` version is uncertain.
- The Limitations section states "There is definitely something needs to be done to enhance the performance" and "Broader parameters selection needs to be considered" without proposing any concrete corrective steps. The box misspecification identified in Major Issue 1 is a specific, actionable diagnosis that should appear here.
- Section heading reads "Model Discription" — should be "Description."
- All five references are bare URLs or book-title strings without full bibliographic information (author, year, volume, pages, DOI). Reference [1] is a Wikipedia URL.

---

## Recommendation

**Major Revision.** The benchmark comparison work is solid and represents genuine methodological effort, but the POMP analysis has a demonstrable internal inconsistency — the global search box excludes the parameter region the paper's own local search identifies as optimal — that directly explains the reported non-convergence and the POMP model's underperformance relative to ARMA+GARCH-t. Before the POMP analysis can be considered complete, the authors must: (1) correct the global search box to bracket the local-search estimates and re-run; (2) compute at least one profile likelihood to support any identifiability claim; (3) add post-fit diagnostics (simulation from the final MLE, ESS trace, conditional log-likelihood plot) instead of relying solely on a pre-fit simulation from a known-poor parameter vector; and (4) correct the "likelihood" / "log likelihood" labeling in the GARCH section. Of the five "quick-priority" checklist items (benchmark comparison, quantitative GOF, computational adequacy, parameter identifiability, forecast methodology), benchmark comparison is well-satisfied, quantitative GOF is partially satisfied with the labeling error, and computational adequacy, parameter identifiability, and model diagnostics are not satisfied in the POMP section.

---

## Files Consulted

- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project06/blinded.rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project06/blinded.html`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project06/NDAQ.csv`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project06/Makefile`
