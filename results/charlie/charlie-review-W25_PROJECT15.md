# Peer Review: W25 Project 15
## "Volatility Analysis on Bitcoin Returns: a Fear & Greed Index Perspective"

---

## Summary

This project fits a suite of stochastic volatility models to daily Bitcoin log-returns (Jan 2020 – Apr 2025) and asks whether incorporating the Crypto Fear & Greed Index as an exogenous covariate improves model fit. Six model variants are estimated: a GARCH(3,1) baseline, the Breto (2014) leverage-SV model, a modified Breto model augmented with the differenced Fear & Greed Index, both Breto variants with Student's t measurement, and a simplified Heston-style SV model in both normal and t flavors. The project's main claims are that (a) the modified Breto model with t-distribution achieves the best log-likelihood among all candidates, and (b) a negative gamma coefficient indicates that increasing fear drives Bitcoin volatility.

The project demonstrates genuine effort in model building and shows familiarity with the pomp IF2 workflow. However, it contains a critical stew() filename collision that silently invalidates the entire "New Global Search" section, along with a pervasive global-search initialization error that anchors every global search to a previous mif2 chain. Profile likelihoods are absent, model comparison across the six models relies on point log-likelihood values without uncertainty quantification, the Heston process equation is misspecified, and no non-mechanistic benchmark is provided for the POMP models. Several additional methodological and presentation deficiencies are described below.

---

## Major Issues

### 1. stew() filename collision invalidates the "New Global Search" entirely

The Breto model section runs two sequential global searches using `stew()`. Both calls construct their cache filename as `paste0("box_eval_bitcoin_", run_level, ".rda")` (lines 532 and 586 of blinded.Rmd). With `run_level = 3`, both evaluate to the string `"box_eval_bitcoin_3.rda"`. When the document is rendered, the first call writes the file; the second call silently loads from the existing file without executing its body. As a result, `if.box.new` and `L.box.new` are populated with the first search's results, not the narrowed-box search's results.

Every result reported in the "New Global Search" section — the log-likelihood summary, the pairs plot (Figure 12), the convergence diagnostics (Figure 13), and the narrative claiming "the log-likelihood curve now exhibits a single, well-defined peak" confirming the global maximum — is a duplicate of the broad global search output. The central conclusion of that section ("This close agreement gives us strong confidence that we have indeed captured the true global maximum") is not supported by any actual computation. The fix is to assign a distinct filename to the narrowed-box search, e.g., `paste0("box_eval_bitcoin_narrow_", run_level, ".rda")`.

### 2. Global search initialization error across all models: mif2 called on a prior IF2 result

In every global search across all four POMP models, the `mif2()` call inside the `foreach` loop passes a previous IF2 chain as its first argument rather than the base pomp object:

- Breto model global search (line 535): `mif2(if1[[1]], params = apply(bitcoin_box, 1, function(x) runif(1, x)))`
- Breto model new global search (line 589): same pattern with `if1[[1]]`
- Modified Breto normal global search (line 972): `mif2(if2_list[[1]], params = start_params)`
- Modified Breto t-distribution global search (line 1294): `mif2(if2_list[[1]], params = start_params)`

When a previous IF2 result is passed as the first argument, mif2 inherits the internal cooling schedule from that chain. Because the local IF2 search ran for Nmif = 200 iterations with cooling.fraction.50 = 0.5, the inherited chain is at or near its final cooling state — the perturbation standard deviations are already decayed to approximately 0.5^(200/50) × rw.sd = 0.5^4 ≈ 0.06 of their initial values. The random starting parameters drawn from the box are applied for a single step before the perturbations effectively shrink to near zero, meaning every global replicate performs little genuine exploration from its random start. The global searches reported for all four POMP models are effectively anchored near the local-search solution, and the "global maximum" likelihoods may not represent the true global optimum. The fix is to replace `if1[[1]]` / `if2_list[[1]]` / `btc_mif[[1]]` with the base `bitcoin.filt` / `filt_modified` / `btc.pomp` pomp object in each global search loop.

### 3. No profile likelihoods; parameter identifiability unresolved

No profile likelihoods are computed for any model. The text acknowledges a potential identifiability problem between phi and mu_h in the Breto model (the term (1-phi)*mu_h creates a ridge in the likelihood surface), and the convergence traces confirm the multimodal structure, but the identifiability issue is left unresolved. Without profile likelihoods, it is impossible to determine whether the reported MLEs are reliable, whether confidence intervals would span a large portion of parameter space, or whether the phi ≈ 0.5 versus phi ≈ 1 modes reflect genuine bimodality or inadequate computation. For the modified Breto model, the scientific conclusion that gamma_fng < 0 (fear drives volatility) rests entirely on a point estimate with no uncertainty quantification. Wheeler et al. (2024) §Parameter identifiability and uncertainty emphasize that profile likelihoods should be computed for key parameters, and that implausible estimates should be interpreted as potential signs of model misspecification rather than biological (or financial) truths.

### 4. No non-mechanistic benchmark for POMP models

The GARCH model is used as a benchmark in passing, but it is compared to the POMP models only informally and without a consistent comparison basis. The GARCH log-likelihoods are computed via `tseries::garch()` on demeaned returns, while the POMP models use a different data pipeline (some on `bitcoin_ret_demeaned` via covariate injection, others on the raw `log_return`). The project text explicitly notes that the tseries::garch log-likelihoods cannot be directly compared to POMP log-likelihoods (line 287: "we cannot directly compare loglikelihood from tseries::garch"). No ARMA, ARIMA, or auto-regressive negative binomial benchmark is constructed in the pomp framework on the same data to provide a valid apples-to-apples comparison. Wheeler et al. (2024) §Benchmark comparison note that mechanistic models should be compared against non-mechanistic benchmarks with a quantitative (log-likelihood or AIC) comparison on the same observation model.

### 5. Heston process equation is misspecified

The rprocess Csnippet for both the normal and t-distribution Heston models (lines 1374–1378 and 1587–1592) reads:

```
V = theta * (1 - phi) + phi * sqrt(V) + sqrt(V) * omega;
```

The standard Heston/CIR mean-reverting variance process is:

```
V_n = theta*(1-phi) + phi*V_{n-1} + xi*sqrt(V_{n-1})*omega_n
```

The code applies `phi` to `sqrt(V)` rather than to `V` itself, which is not the model stated in the text (equation at line 1344: `V_n = (1-phi)*theta + phi*V_{n-1} + xi*sqrt(V_{n-1})*omega_n`). This is a code-text inconsistency in the process model. The fitted parameters and reported log-likelihoods for the simple Heston model are based on a misspecified process that differs from what is described and claimed. This is the type of code-text discrepancy flagged by Wheeler et al. (2024) as a concrete reproducibility and validity failure.

### 6. Initial particle filter run on simulated data presented as a benchmark for the real-data model

For the Basic Breto model (lines 448–456), the initial pfilter is run on `sim1.filt`, which is a pomp object constructed from a `simulate()` call on the simulated data, not from the actual Bitcoin return series. The log-likelihood reported from this step reflects the fit to the simulated dataset, not to the real data. The surrounding text ("Particle Filtering and Log-likelihood Evaluation") implies this is an evaluation on the real data. Because the simulated and real datasets differ, the log-likelihood values are not on the same scale and cannot serve as a meaningful benchmark or starting point for comparison with the subsequent IF2 results. The same pattern occurs in the modified Breto sections (lines 858–866 and 1180–1187).

### 7. Model comparison table absent; log-likelihood values scattered and incomparable

Six models are estimated, but no consolidated comparison table is presented. The best log-likelihoods across models are reported in different sections with different evaluation procedures (different Np, different numbers of pfilter replicates, different data objects for some runs), making a direct comparison unreliable. The conclusion that the "Modified Breto model with t-Distribution performed best" is asserted in the conclusion but cannot be verified from the reported numbers because the comparison is not made under controlled conditions. A formal AIC comparison on the same data with the same evaluation procedure is needed.

---

## Minor Issues

### 8. gamma_fng scientific conclusion drawn from a single point estimate without uncertainty

The project concludes that "fear drives market volatility more than greed" based solely on the sign of the MLE for gamma_fng from the global search. However: (a) the local search found a positive gamma_fng (indicating greed dominates) while the global search found negative, without resolution of this contradiction; (b) no confidence interval or profile likelihood is reported for gamma_fng; (c) the global search itself is compromised by the initialization error described in Issue 2. The stated conclusion is not supported by the available evidence.

### 9. H_0 non-convergence acknowledged but not addressed

The text notes that H_0 does not converge in the modified Breto global search (line 1017), but no action is taken. Non-convergence of an initial condition parameter suggests either that H_0 is not identifiable from the data, that the global search box for H_0 is poorly specified, or that the model is misspecified for the initial period. Wheeler et al. (2024) §Initial conditions note that initial values can substantially affect model fit and should be estimated carefully or have sensitivity assessed.

### 10. FG Index stationarity justification is informal and potentially incorrect

The ACF of the raw FG index decays slowly (Figure 14) and the authors conclude it is non-stationary, motivating differencing. However, a slowly decaying ACF does not definitively establish non-stationarity for a bounded series (0-100). No formal unit root test (ADF, KPSS) is reported. The choice to difference the index is consequential for the model interpretation: differencing means the model captures the effect of changes in sentiment, not the level of sentiment, which may not be the economically relevant quantity. This modeling choice is made without adequate justification.

### 11. rw.sd values are uniform across parameters; no rationale provided

All four random-walk standard deviations in the IF2 search are set to either 0.02 (regular parameters) or 0.1 (initial value parameters) without any justification. Given that sigma_nu converges to values near zero (on the order of 1e-4 to 1e-3), a uniform rw.sd of 0.02 on the natural scale is large relative to the MLE and may impede convergence. The authors do not discuss whether the rw.sd magnitudes were tuned or what the rationale was for their choice.

### 12. t-distribution degrees of freedom chosen by "experimenting" without formal selection

The report states that 5 degrees of freedom were selected because "the model captured the data best when the residuals were assumed to come from a t-distribution with 5 degrees of freedom" after experimenting with values from 3 to 25 (line 1021). No likelihood-based criterion, AIC comparison, or profile likelihood over degrees of freedom is presented. Selecting degrees of freedom by informal experimentation and then reporting the best result without correction introduces selection bias.

### 13. stew() not used for the modified Breto and Heston searches; reproducibility reduced

The Breto model uses `stew()` for caching, but the modified Breto, t-distribution Breto, and both Heston model sections do not use `stew()` for their IF2 and particle filter computations. Without caching, the document cannot be reproduced without re-running all expensive computations from scratch. The code supplement does not document total computational cost (CPU-hours), making it impossible for readers to assess feasibility of reproduction.

### 14. Title typo and code quality issues

The document title reads "olatility analysis on Bitcoin returns" (missing leading "V"). Multiple library loading calls are repeated redundantly within each model section (e.g., `library(doParallel)`, `library(doRNG)` appear in nearly every chunk). The `plan(multisession)` call from `doFuture` is invoked in the modified Breto sections but the `doFuture` backend is not actually used (the code uses `%dopar%` which requires `doParallel`). These code quality issues suggest the code was assembled from templates without systematic review.

### 15. References incomplete and improperly formatted

Several HTML footnote tags in the References section are not properly closed (lines 1800–1818: missing `</span>` and `>` closing angle brackets on multiple references). Reference [2] is a raw PDF semanticscholar URL with no author, title, or journal information. Multiple footnote IDs are duplicated (footnotes 4 and 12–14 all share `id="footnote-4"`). The Breto (2014) model is not formally cited despite being central to the methodology; the citations to w22 projects 14 and 22 are used as primary methodological references in place of the original peer-reviewed source.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project15/blinded.Rmd`
