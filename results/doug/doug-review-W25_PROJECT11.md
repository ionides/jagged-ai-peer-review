# Peer Review: W25 Project 11
## Time Series Analysis of Apple Stock Price

---

## Summary

This project compares two modeling frameworks — ARMA-GARCH variants (sGARCH, EGARCH, GJR-GARCH) and a discrete-time stochastic volatility POMP model — for capturing the conditional volatility of Apple Inc. (AAPL) daily log-returns from January 2020 through 2025. The GARCH section is methodologically sound and reasonably well-executed. The POMP section adapts the Bretó (2014) stochastic volatility model using `mif2`-based inference. Several significant computational errors undermine the validity of the POMP parameter estimates, the global search, and the profile likelihood confidence interval. The direct log-likelihood comparison between GJR-GARCH (using a t-distribution) and the POMP model (using a Gaussian measurement model) is not a like-for-like comparison. No non-mechanistic benchmark evaluated under the same observation model is presented, making it impossible to assess whether the POMP model structure adds value beyond a simpler statistical model.

---

## Major Issues

### 1. Global IF2 search initialized from a previous mif2 result object (anti-pattern)

The global search (chunk beginning at the `box_eval_2` stew block) calls:

```r
if.box <- foreach(i=1:apple_Nreps_global, .packages='pomp', .combine=c) %dopar%
  mif2(if1[[1]], params=apply(apple_box, 1, function(x) runif(1, x)))
```

The first argument is `if1[[1]]`, a previous IF2 chain from the local search, rather than the base `pomp` object `apple.filt`. Passing a previous `mif2` result as the first argument causes each global replicate to inherit the cooling schedule of the local chain — which is at or near its final (near-zero perturbation) state after `Nmif = 50` iterations. The new random starting parameters from `apply(apple_box, ...)` are applied to `params=`, but the cooling-schedule state is not reset. As a consequence the global search effectively performs no meaningful exploration from its new starting point, and the reported "global" maximum is not a true global optimum. The fix is to replace `mif2(if1[[1]], params=...)` with `mif2(apple.filt, params=...)` so each replicate begins with a fresh IF2 chain. (See `pomp-global-search-init-audit` skill; Wheeler et al. 2024, §Computational adequacy.)

### 2. Global search box excludes the region containing the MLE for mu_h

The global search box sets `mu_h = c(-1, 0)`, but the best-fit value of mu_h found by the global search is -8.58 — well outside this range. Inspection of the saved artifact (`box_eval_2.rda`) confirms: `r.box[which.max(r.box$logLik), "mu_h"] = -8.58`. The global search cannot systematically explore values of mu_h near -8.58 because no starting parameter in the box is anywhere near this value; IF2 can only reach it by accidentally drifting far outside the box bounds during optimization. This is not systematic global coverage. The consequence is that the "global maximum" (log-likelihood 3288.96 from `r.box`) reflects accidental drift, not a principled global search. The box should be expanded to bracket the local-search MLE: approximately `mu_h = c(-15, -1)` based on the local and profile search results. (See `pomp-global-search-box-misalignment` skill.)

### 3. Profile likelihood Monte Carlo variance dominates the confidence interval

The profile IF2 search (the `eta_profile` bake block) uses `Np = 100` particles and `replicate(10, mf |> pfilter(Np=100) |> logLik())` for each profile evaluation. This is substantially less computation than the global search (Np = 1000, 10 replicates). The standard error of the profile log-likelihood estimates reaches up to 9.3 units (as recorded in `eta_profile.rds`; the best-point SE is 1.95). The chi-squared CI cutoff is `max(loglik) - 0.5 * qchisq(df=1, p=0.95) = 3305.18 - 1.92 = 3303.26` — a gap of only 1.92 log-likelihood units above which only 3 out of 150 profile points fall. When the Monte Carlo SE (up to 9.3 units) exceeds the chi-squared threshold (1.92 units), the location of the CI boundary is determined by noise, not by the likelihood surface. The reported 95% CI for phi of (0.959, 0.99) cannot be taken at face value. The profile evaluation should use at least `Np = 1000` and `replicate(10, ...)` at minimum, preferably matched to the global search settings. (See `pomp-profile-single-restart-audit` skill.)

### 4. Profile maximum substantially exceeds global search maximum, revealing global search failure

The profile search finds a maximum log-likelihood of 3305.18 (`eta_profile.rds`), which is 16.2 units above the global search maximum of 3288.96 (`box_eval_2.rda`). A correctly executed global search should identify the global optimum; the profile, which explores a restricted grid of phi values, should not be able to substantially surpass the unconstrained global search. The 16-unit discrepancy directly confirms that the global search failed to find the true MLE — a consequence of Issues 1 and 2 above. All parameter estimates reported from the global search (Table 6.2 and Table 6.3) are therefore not the MLE and cannot be interpreted as such. The conclusion that the "final model parameters" come from the global search is not supported. The global search must be re-run with the correct initialization (`apple.filt` as base object) and a corrected box range for mu_h.

### 5. Simulated-data particle filter result presented as a real-data benchmark

The initial pfilter run (`pf1_2.rda`) is evaluated on `sim1.filt`, a pomp object constructed from simulated data (`simulate(sim1.sim, seed=1, params=params_test)`), not on the real-data object `apple.filt`. The saved result gives a log-likelihood of approximately -1564, while IF2 on the real data reaches 3289 — a discrepancy of ~4853 log-likelihood units. These two quantities are on completely different scales because they evaluate different datasets. If the paper presents L.pf1 as an "initial benchmark" for the real-data model fit (the code chunk saves it with `(L.pf1 <- logmeanexp(sapply(pf1, logLik), se=TRUE))`), that comparison is invalid. The initial particle filter should be run on `apple.filt` at `params_test` to provide a real-data starting reference. (See `pomp-simdata-benchmark-error` skill.)

### 6. Log-likelihood comparison between GJR-GARCH and POMP model is not like-for-like

The comparison table reports sGARCH-norm at 3289.09, GJR-GARCH at 3328.37, and the POMP model at 3288.55. GJR-GARCH uses a Student's t-distribution for measurement errors, while the POMP model uses a Gaussian observation model (`lik = dnorm(y, 0, exp(H/2), give_log)`). These likelihoods are evaluated under different distributional families; a model with t-distributed errors will generally yield a higher log-likelihood on heavy-tailed financial returns than a Gaussian model, independent of the underlying process dynamics. The comparison thus conflates model structure (GARCH vs. stochastic volatility) with distributional choice (Gaussian vs. t). The conclusion that "GARCH achieves better fit" is partially an artifact of the distributional mismatch. A valid comparison would either add a t-distributed measurement model to the POMP specification, or compare each POMP variant against its corresponding GARCH variant with the same distributional assumption.

### 7. No non-mechanistic benchmark under the same observation model (Wheeler et al. 2024 practice #2)

The paper compares ARMA-GARCH and POMP but does not present a non-mechanistic benchmark under the same Gaussian observation model as the POMP model. Wheeler et al. (2024) note that mechanistic models should be compared against non-mechanistic baselines to assess whether the mechanistic structure adds value. Here, sGARCH-norm (3289.09) uses a Gaussian likelihood on the returns and achieves virtually the same log-likelihood as the POMP model (3288.55) without any latent stochastic volatility state. This is a natural comparison point, but the paper does not discuss what this near-equality implies about the POMP model's added value over a simple GARCH. The authors should explicitly acknowledge this and assess whether the POMP model provides any improvement over a Gaussian ARMA-GARCH under identical observation assumptions.

---

## Minor Issues

### 8. Profile likelihood plot filtered by round(H_0, 2) rather than phi

The scatter plot in Figure 6.7 (profile likelihood over phi) is produced by:

```r
results |> filter(is.finite(loglik)) |>
  group_by(round(H_0, 2)) |>
  filter(rank(-loglik) < 200) |>
  ungroup() |>
  ggplot(aes(x=phi, y=loglik)) + ...
```

The `group_by(round(H_0, 2))` groups by H_0, not by the profiled parameter phi. Since there are 150 profile rows and `rank(-loglik) < 200` keeps at most 199 rows per H_0 group, no data is actually filtered in this case (all rows are retained). However, if the profile were larger this would introduce a display artifact. Replacing `round(H_0, 2)` with `round(phi, 4)` would make the grouping semantically correct (filtering to top rows per phi grid point, which is the intended display logic). (See `pomp-profile-guess-stratification-error` skill for the related analysis.)

### 9. apple_params.csv contains stale entries from multiple runs with unrealistic parameter values

The file `apple_params.csv` accumulates results across multiple `run_level` values via `write.table(..., append=TRUE)`. The file contains rows with `logLik > 8000` and `sigma_eta > 100` that are clearly from earlier exploratory runs at different parameter scales. These stale entries are not used in the final analysis (the code uses in-memory objects `r.if1`, `r.box`), but they compromise the CSV as a standalone reproducibility artifact. The `write.table(..., append=TRUE)` pattern without clearing the file between runs is a reproducibility red flag; a reader inspecting the CSV would encounter implausible values with no explanation.

### 10. Computational settings: run_level=2 with Nmif=50, Np=1000 is borderline

The paper uses `run_level=2`, giving `Nmif=50`, `Np=1000`, and `Nreps_global=50`. While this is not minimal, the convergence diagnostics (Figure 6.1 and Figure 6.4) show substantial spread across runs — approximately 100 log-likelihood units in local search convergence. The authors acknowledge "poor convergence" in both local and global searches. Run level 3 (`Nmif=100`, `Np=2000`) would be needed to adequately assess convergence, especially for a 6-parameter model on a 1250-point daily series. The profile search using only `Np=100` is particularly inadequate for a model that requires `Np=1000` in the global search to achieve reasonable Monte Carlo accuracy. (Wheeler et al. 2024, §Computational adequacy.)

### 11. Inconsistency between the stated best phi and the parameter table

Section 6 (Global Search) states "the highest log-likelihood was still achieved with a phi value around 0.9, reaching up to 3289." Table 6.3 reports the best parameter set with `phi = 0.910`. However, the profile likelihood CI is (0.959, 0.99), placing the MLE of phi much closer to 1 than the global search suggests. This inconsistency is acknowledged by the authors but not resolved. The text should clearly explain that the global search result for phi is unreliable due to inadequate convergence, and that the profile provides a more reliable estimate for this parameter.

### 12. Missing profile likelihood for additional parameters

Only phi is profiled. The model has six estimated parameters, including sigma_nu (which the authors note shows poor identifiability in pair plots), sigma_eta, and mu_h. Without profile likelihoods for other key parameters, the claim of "weak identifiability" for the overall model cannot be evaluated quantitatively. Wheeler et al. (2024, §Parameter identifiability) recommend computing profile likelihoods for all parameters of scientific interest. At minimum, profiles for sigma_nu and sigma_eta would help evaluate the authors' hypothesis that additional distributional features (fat tails) are needed.

### 13. Notation inconsistency: psi used in text but theta in ARMA equation

The ARMA model specification at Section 4.1 writes the moving-average terms as $\psi$ in prose ("Terms with $\phi$ are autoregressive terms, and terms with $\psi$ are moving average terms") but uses $\theta_j$ in the displayed equation. The correct MA parameter notation in ARMA(p,q) is typically $\theta_j$; the prose reference to $\psi$ is inconsistent with the equation.

### 14. Density plot title mislabeled as "Density Plot of Gold Prices"

Figure 3.1 is titled "Density Plot of Gold Prices" in the ggplot code (`labs(title = "Density Plot of Gold Prices", x = "price", y = "Density")`), while the figure caption reads "Density Plot of Apple Stock Price." The plot title was not updated from a template or copy-paste from a different dataset analysis. This is a minor presentation error.

### 15. Missing sessionInfo() and no package version pinning

The supplement includes no `sessionInfo()` output and no `renv` or equivalent environment specification. The `pomp` package API has changed substantially across versions, and results may not reproduce on future CRAN releases. The code-supplement checklist (POMP-specific item) requires that the `pomp` version be explicitly pinned. At minimum, the rendered HTML should include `sessionInfo()` output, and the project should ideally use `renv::snapshot()` to lock all package versions.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
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
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/box_eval_2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/mif1_2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/pf1_2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/eta_profile.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project11/apple_params.csv`
