# Peer Review: W25 Project 15
## Volatility Analysis on Bitcoin Returns: A Fear & Greed Index Perspective

---

## Summary

This project analyzes daily Bitcoin return volatility using six models: a GARCH(3,1) benchmark, two variants of the Breto stochastic volatility POMP model (one plain, one augmented with a Fear and Greed Index covariate), and two simple Heston-style stochastic volatility POMP models (one with Gaussian, one with Student's t measurement noise). The authors also extend both the FG-augmented Breto model and the simple stochastic volatility model to use t-distributed measurement errors. The paper's key claimed finding is that fear drives Bitcoin volatility more strongly than greed (negative gamma_fng at the global MLE).

While the project tackles a genuinely interesting research question and applies a reasonable battery of models, it is undermined by several critical methodological errors: the global IF2 searches for all POMP models are initialized from a previous mif2 result object rather than the base pomp object (anchoring every global search to a local optimum), the initial particle filter benchmarks are computed on simulated data rather than real data (making the reported initial log-likelihood values meaningless as benchmarks for the real-data models), a mis-specified process equation in the Heston model, and the absence of any profile likelihood analysis or formal parameter identifiability assessment. Cross-model log-likelihood comparisons are presented without acknowledging that the measurement models differ across the six model families, making the comparisons numerically invalid.

---

## Major Issues

### 1. Global search IF2 initialized from previous mif2 result, not base pomp object

In all four POMP global searches (basic Breto, modified Breto with FG, modified Breto with t-distribution, simple stochastic volatility normal, simple stochastic volatility t), the `mif2()` call inside the global foreach loop passes a previous mif2 result as its first argument rather than the base pomp object:

- Basic Breto global search (line ~535): `mif2(if1[[1]], params = apply(bitcoin_box, 1, function(x) runif(1, x)))`
- Modified Breto global search (line ~972): `mif2(if2_list[[1]], params = start_params)`
- Simple stochastic volatility global search (line ~1509): `mif2(btc_mif[[1]], params = start_params, ...)`

Passing a previous IF2 chain as the first argument to `mif2()` causes the new chain to inherit the internal cooling schedule from the completed local search. Because the local chain is at or near its final, heavily-cooled state (with perturbations shrunk to near zero), the global search replicates have very few effective IF2 iterations from the new random starting points. The reported "global maximum" is therefore indistinguishable from an extended local search and does not constitute evidence of having explored the full parameter box. All conclusions about global optima and multimodality are undermined by this error. The fix is to replace `if1[[1]]` (or `if2_list[[1]]`, `btc_mif[[1]]`) with the base pomp object (`bitcoin.filt`, `filt_modified`, `btc.pomp`) in each global search foreach loop. See `pomp-global-search-init-audit/SKILL.md` for the precise diagnostic.

### 2. Initial particle filter benchmark computed on simulated data, not real data

For all three model families that use a two-object construction pattern (the basic Breto model, the modified Breto model, and the modified Breto with t-distribution), the initial particle filter is run on an object derived from a simulate() call:

- Basic Breto (line ~452): `pfilter(sim1.filt, Np = bitcoin_Np)` — `sim1.filt` is constructed from `sim1.sim`, which is a simulated dataset, not real Bitcoin data.
- Modified Breto (line ~858): `pfilter(sim_modified.filt_modified, Np=Np)` — `sim_modified.filt_modified` is built from `sim_modified.sim`, likewise simulated.
- Modified Breto t-distribution (line ~1180): same pattern.

The log-likelihood from filtering simulated data is evaluated under a completely different dataset than the subsequent IF2 searches on real data. The two values are not on the same scale and cannot be compared. The text presents these values as "a good place to start with" in the context of real-data inference, which is misleading. The correct approach is to run the initial particle filter on the real-data pomp object (`bitcoin.filt` or `filt_modified`) at the test parameters. See `pomp-simdata-benchmark-error/SKILL.md`.

### 3. Heston process equation in code does not match text specification

The stated model equation is:
`V_n = (1 - phi)*theta + phi*V_{n-1} + xi*sqrt(V_{n-1})*omega_n`

The implemented Csnippet (line ~1377) is:
```
V = theta * (1 - phi) + phi * sqrt(V) + sqrt(V) * omega;
```

The mean-reversion term has `phi * sqrt(V)` instead of `phi * V`. This produces a materially different dynamics: the Heston model's mean-reversion term is proportional to the level of variance, not its square root. The implemented equation is neither the Heston model nor a standard stochastic volatility specification. The same error appears in the t-distribution variant (line ~1590). All parameter estimates, log-likelihoods, and comparisons involving the simple stochastic volatility models are invalidated by this specification error.

### 4. No profile likelihoods computed; parameter identifiability not formally assessed

The paper identifies a potential identifiability issue between mu_h and phi (their joint appearance in `(1-phi)*mu_h`) but does not compute profile likelihoods for any parameter in any model. Without profile likelihoods, the reported MLE values cannot be trusted as well-identified point estimates, and no confidence intervals can be reported. The sign and magnitude of gamma_fng — the paper's central scientific claim — likewise rests on a single global search result with no uncertainty quantification. Per Wheeler et al. (2024), profile likelihoods are essential for assessing parameter identifiability and the convergence behavior of sigma_nu to zero and H_0 non-convergence noted in the text are strong signals of identifiability problems that require formal investigation.

### 5. No benchmark comparison against non-mechanistic models

The GARCH(3,1) log-likelihood is acknowledged as not directly comparable to the POMP log-likelihoods (citing Reference [5]) yet the Conclusions section still asserts "the basic Breto model models the volatility well as it outperforms the benchmarks (GARCH and simple stochastic volatility model)" without any quantitative basis for this comparison. Furthermore, no ARIMA or auto-regressive benchmark is compared against any POMP model using a common observation model. Per Wheeler et al. (2024) and the POMP checklist, such comparisons are the single most diagnostic check for whether a mechanistic model captures meaningful structure beyond a statistical baseline. The comparisons among the six models are also invalid because the models use different measurement distributions (Gaussian vs. t), different data objects (some use `bitcoin_ret_demeaned`, others use the raw `log_return` column from the merged data frame), making the log-likelihoods incommensurable.

### 6. Duplicate stew() file name invalidates new global search for basic Breto

The second ("new") global search for the basic Breto model (line ~586) uses:
```r
stew(file = paste0("box_eval_bitcoin_", run_level, ".rda"), {...})
```
This is the same filename as the first global search (line ~532). Since `stew()` does not rerun a computation if the target file already exists, the second search is never executed; instead, the first search's results are loaded. The claimed improvement from restricting the box to `phi in [0.45, 0.5]` and `mu_h in [-7.75, -7.4]` is therefore not actually demonstrated — those results are simply the original broad global search results reloaded under a different variable name (`if.box.new`). The conclusion that "this close agreement gives us strong confidence that we have indeed captured the true global maximum" is not supported.

### 7. Cross-model log-likelihood comparisons are invalid due to different datasets

The basic Breto model uses `bitcoin_ret_demeaned` as its data, constructed from `merged_df` with the FG index merge. The simple stochastic volatility models use `btc$log_return`, also from `merged_df`. However, the basic Breto model also excludes one observation (using `bitcoin_ret_demeaned`) while the SSV model uses `btc$log_return` directly from the merged data frame. The data lengths and transformations may differ. More critically, the GARCH model uses `bitcoin_ret` (pre-demeaning), and is fitted to a potentially different series length. No table confirms that all models are fitted to identical series. Direct log-likelihood comparisons across models fitted to different data are invalid.

---

## Minor Issues

### 8. Degrees of freedom for t-distribution fixed without formal justification

The paper states the Student's t-distribution with 5 degrees of freedom was chosen by "experimenting with different values for degrees of freedom ranging from 3-25" and visual inspection. The degrees of freedom should be treated as a parameter to be estimated via likelihood maximization, or at minimum the comparison should report log-likelihoods for each tested df value so readers can evaluate the selection. The current description amounts to informal model selection without quantitative justification.

### 9. Data reproducibility: Fear & Greed Index fetched live from API

The FG Index is fetched at render time via `GET("https://api.alternative.me/fng/?limit=2000")`. Because the API returns the most recent 2000 days, the dataset will shift backward in time as the document ages, producing different results on different render dates. This violates reproducibility standards. The fetched data should be archived in the project folder and loaded from the saved file, similar to how `bitcoin_2020-01-01_2025-04-06.csv` is handled.

### 10. Stationarity of FG Index assessed only by ACF inspection, not formal test

The paper concludes that the Fear and Greed Index is non-stationary based solely on a slowly-decaying ACF plot. No formal unit-root test (ADF, KPSS, or Phillips-Perron) is reported. The claim should be supported by a formal test, as ACF inspection is subjective. Similarly, the claim that the differenced series is stationary should be confirmed with a formal test, not only visually.

### 11. sigma_nu converges to zero without identifiability discussion

The convergence plots for the modified Breto model show sigma_nu converging to zero across nearly all IF2 chains. The text notes this observation but does not discuss its implications: sigma_nu = 0 means the random walk driving the leverage process G_n is degenerate (no noise), which implies G_n is constant and the leverage R_n is fixed. This is a potential model misspecification or identifiability failure that should be investigated via profile likelihood, not dismissed as evidence of convergence.

### 12. Title typo: "olatility" should be "Volatility"

The YAML title field reads `"olatility analysis on Bitcoin returns: a Fear & Greed Index perspective"`, missing the initial 'V'. This is a presentation error that should be corrected before submission.

### 13. H_0 non-convergence dismissed without investigation

The convergence plots for the modified Breto model show H_0 not converging. The text notes this but concludes "we also observe that H_0 does not converge, however G_0 converges close to zero." Non-convergence of H_0 means the reported MLE for the initial log-volatility is unreliable, which can affect all parameter estimates that co-move with H_0. This should be investigated, potentially by fixing H_0 at a sensible value or by computing a profile over H_0.

### 14. No final MLE parameter table for reproducibility

The final MLE parameter vectors are reported only inline via `print(best_params)` calls embedded in chunks. There is no consolidated table of MLE values for all six models, and no archived CSV of final parameter estimates independent of the optimization code. Per Wheeler et al. (2024) and the code supplement checklist, final parameter estimates should be archived as a standalone file so readers can evaluate results without re-running expensive optimization.

### 15. Model comparison narrative inconsistent with POMP log-likelihood direction

Section "Simple Stochastic Volatility Model" (around line 1551) states: "The high log-likelihood value (~3899.52) and visual agreement between simulated and observed data support the adequacy of the fitted model." Later (around line 1652), the Heston t-distribution log-likelihood at particle filter initialization is reported as "~3985.43 compared to the normal model (~3040.33), indicating a significantly better fit." However, these are particle filter evaluations at initial (unimodal test) parameters, not at the MLE — the text incorrectly implies these represent the fitted model's performance. The comparisons should be based on the global-search MLE log-likelihoods, reported consistently across all models with matching datasets.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
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
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project15/blinded.Rmd`
