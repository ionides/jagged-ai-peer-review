# Peer Review: W25 Project 15
## Bitcoin Volatility Analysis with the Fear & Greed Index

---

## Summary

This project applies six stochastic volatility models to daily Bitcoin log-returns from January 2020 through April 2025: a GARCH(3,1) benchmark, a basic Breto POMP model, a modified Breto model incorporating the Fear & Greed (FG) index, the same modified model with a Student's t measurement distribution, and two Heston-style simple stochastic volatility models (normal and t-distributed). The main scientific question is whether incorporating market sentiment improves volatility modeling and whether fear or greed is the stronger driver of Bitcoin volatility.

Key strengths include a clearly motivated research question, use of iterated filtering (IF2) with multiple restarts at run_level=3, appropriate use of logmeanexp for likelihood aggregation, and a creative attempt to extend the Breto framework with an external covariate. However, the analysis has several critical flaws that undermine the core comparative conclusions: the Breto family and the Heston family are fitted to different versions of the data (making their log-likelihoods incomparable), a filename collision in `stew()` renders the "New Global Search" results unreliable, the Heston-model code does not implement the equation stated in the text, and the GARCH likelihood comparison is acknowledged as invalid but treated as valid in the conclusion. No profile likelihoods or confidence intervals are reported for any model.

---

## Major Issues

### 1. Breto and simple stochastic volatility models are fitted to different data, making cross-family comparisons invalid

The Breto family uses demeaned log-returns (`logd`, line 108-109 and 777): `logd <- log_returns - mean(log_returns)`. The simple stochastic volatility (Heston-style) family uses raw (non-demeaned) log-returns (`btc$log_return`, lines 1363-1366). Because the log-likelihood is a function of the observed data, comparing log-likelihoods across these two families is invalid — they are not evaluated on the same observations. The conclusion claims the basic Breto model "outperforms the benchmarks (GARCH and simple stochastic volatility model)" on the basis of log-likelihood, but this comparison is unsupported. The difference in the mean (a single nuisance parameter) can shift the likelihood by a non-trivial amount.

**Fix:** Re-fit all models on the same data series (either all demeaned or all raw), then restate the comparative results.

---

### 2. `stew()` filename collision makes the "New Global Search" results unreliable

Both the first global search (line 532) and the "New Global Search" (line 586) for the basic Breto model use the identical cache file:

```r
stew(file = paste0("box_eval_bitcoin_", run_level, ".rda"), { ... })
```

Because `stew()` loads from the file if it already exists, the second call silently loads the first global search results rather than executing the new computation. The objects saved in the first call are `if.box` and `L.box`; the second call expects to save `if.box.new` and `L.box.new`. This means either the new objects do not exist in the loaded environment, or stale first-search objects are used. The authors conclude from this block that "the log-likelihood curve now exhibits a single, well-defined peak" and "gives us strong confidence that we have indeed captured the true global maximum" — a conclusion that rests on potentially invalid results.

**Fix:** Use distinct filenames for distinct computations, e.g., `"box_eval_bitcoin_narrow_"`.

---

### 3. Heston model code does not implement the stated process equation

The text defines the volatility process as:

$$V_n = (1-\phi)\theta + \phi V_{n-1} + \xi\sqrt{V_{n-1}}\,\omega_n$$

The R code in both the normal and t-distributed Heston models implements:

```c
V = theta * (1 - phi) + phi * sqrt(V) + sqrt(V) * omega;
```

The persistence term in the text is `phi * V_{n-1}` (linear), but the code uses `phi * sqrt(V)` (square-root). These define different dynamical systems. The code effectively models the square-root of volatility's mean-reversion, not volatility itself. All parameter estimates, interpretations, and comparisons for the simple stochastic volatility models rest on a model that differs from what is described. This matches the code-text discrepancy pattern flagged as a reproducibility failure in Wheeler et al. (2024).

**Fix:** Either correct the mathematical description to match the code, or correct the code to implement the stated model. Clarify whether V is intended as variance or standard deviation.

---

### 4. GARCH vs POMP log-likelihood comparison is explicitly acknowledged as invalid but used in conclusions

Footnote 5 cites the course quiz solution (ionides.github.io/531w25/quiz/quiz2-sol.pdf) and states "we cannot directly compare loglikelihood from tseries::garch." Despite this, the conclusion reads: "the basic Breto model models the volatility well as it outperforms the benchmarks (GARCH and simple stochastic volatility model)." The `tseries::garch` package reports a non-standard log-likelihood value that is not on the same scale as pomp-based particle filter likelihoods. Comparing GARCH loglik=3894.515 against Breto loglik~4100 is therefore without statistical basis. This corresponds to Error 2.9 from the course weakness reference (trusting software likelihood output without checking conventions), which is explicitly course-tested material.

**Fix:** Either compute the GARCH log-likelihood on the same scale using an alternative package (e.g., `rugarch`, which is already loaded), or remove the quantitative GARCH comparison from the conclusions and restrict the claim to qualitative adequacy of GARCH residual diagnostics.

---

### 5. No profile likelihoods or confidence intervals reported for any model

Across all six models, no profile likelihood is computed and no confidence intervals are reported for any parameter. The pairwise scatter plots of global search results provide some visual sense of parameter clustering but do not constitute profile likelihoods: they show the distribution of starting-point-dependent terminal estimates, not the maximized likelihood as a function of each parameter with all others profiled out. This is a course-confirmed major error (Error 1.9 from the weakness reference; POMP checklist item #5). Without profiles, identifiability of key parameters such as phi, mu_h, and gamma_fng cannot be assessed.

**Fix:** Compute profile likelihoods for at least the scientifically most important parameters (phi, gamma_fng) using the standard IF2-based profile approach from Chapter 16 of the course notes.

---

### 6. sigma_nu converges to boundary (zero) in modified Breto models — not investigated as model misspecification

The text notes for the modified Breto model: "sigma_nu converges to zero." This implies the G random walk has zero variance, which collapses the leverage effect (R_n becomes constant). A parameter estimate at the boundary of its feasible region is a diagnostic signal of model misspecification, as discussed in Wheeler et al. (2024) in the context of zero transmission rates. The authors observe this but do not investigate whether the leverage component (G, R_n) is identifiable or whether a simpler model without leverage achieves the same likelihood. The conclusion does not mention this potential degeneracy.

**Fix:** Fit a nested model without the leverage component (sigma_nu fixed at zero) and compare log-likelihoods via a likelihood ratio test to assess whether leverage is supported by the data.

---

### 7. Fear & Greed Index loaded from a live time-dependent API — analysis is not reproducible

The FG index is fetched via:

```r
response <- GET("https://api.alternative.me/fng/?limit=2000")
```

The `limit=2000` parameter returns the most recent 2000 observations as of the request time. As time passes, the window shifts: a reader reproducing this analysis in a later period will receive a different dataset (different starting date). The Bitcoin price data is read from a local CSV (`bitcoin_2020-01-01_2025-04-06.csv`), but the FG index is not archived locally. This creates a non-reproducible analysis even though the Bitcoin data is static.

**Fix:** Archive the FG index data as a local CSV file alongside the Bitcoin data, or pin the API query to fixed start/end dates that guarantee the same response.

---

## Minor Issues

### 8. Student's t degrees of freedom selected by trial-and-error without formal model selection

The text states: "We experimented with different values for degrees of freedom ranging from 3–25, and found that the model captured the data best when the residuals were assumed to come from a t-distribution with 5 degrees of freedom." No likelihood values for alternative df settings are reported, and df is treated as fixed rather than estimated. Formally, df should either be estimated as a free parameter via mif2 (with an appropriate transformation to keep it positive and above 2) or compared across values using log-likelihoods from replicated pfilter runs. The current approach is an informal search over a discrete grid with no quantitative support for the chosen value.

---

### 9. "New Global Search" is local parameter refinement, not a global search

The third optimization for the basic Breto model restricts phi to [0.45, 0.50] and mu_h to [-7.75, -7.40] — a narrow band centered on the previously found local optimum. Calling this a "New Global Search" is misleading: it is a local refinement around one mode. A genuine global search would draw starting values from the full biologically plausible range, not a 0.05-unit interval. The conclusion drawn from this ("gives us strong confidence that we have indeed captured the true global maximum") is not supported by the methodology.

---

### 10. H_0 non-convergence acknowledged but not remediated

The text notes "we also observe that H_0 does not converge" for the modified Breto model global search. Non-convergence of an initial condition parameter can indicate that either the model is insensitive to H_0 (weak identifiability) or that the optimization is numerically unstable for this parameter. Neither interpretation is explored. The standard remediation (fixing H_0 at a plausible value and checking sensitivity, or reparameterizing) is not attempted.

---

### 11. Interpretation of gamma sign is fragile across local and global optima

The local search for the modified Breto model (normal residuals) yields a positive gamma_fng, but the global search yields a negative gamma_fng. The paper concludes from the global search that "fear drives market volatility more than greed," but this conclusion is sensitive to which optimum is found. The instability of the gamma sign between local and global searches suggests that the FG index effect is weakly identified. Without a profile likelihood for gamma_fng, the sign conclusion has no inferential support.

---

### 12. Title typo

The document title reads "olatility analysis on Bitcoin returns: a Fear & Greed Index perspective." The initial "V" is missing.

---

### 13. run_level=3 uses Np=2000, below the course standard of Np=5000

The course conventions (Ch. 16, p.28-30) specify Np=5,000 for run_level=3. The project sets Np=2,000 at run_level=3 for all models. While the conventions note that "appropriate values of the algorithmic parameters for each run-level are context dependent," with approximately 1,826 daily observations the particle count may be marginal. The standard error of log-likelihood estimates is not systematically reported across all models, so it is unclear whether the Monte Carlo noise is negligible relative to the likelihood differences claimed.

---

### 14. No consolidated model comparison table

Six models are evaluated across the paper but their log-likelihoods are presented in separate sections without a single summary table. The reader must collect numbers manually: GARCH loglik~3894 (non-standard), basic Breto~4100, modified Breto (normal)~4075–4100, modified Breto (t)~4090+, simple SV (normal)~3899, simple SV (t)~unknown from global search. The absence of a table makes it impossible to assess model comparisons systematically, especially given the additional confound that Breto and Heston models are fitted to different data.

---

### 15. Covariate alignment for dFNG uses an ad hoc zero-padding without justification

The covariate table for the modified Breto model pads the differenced FNG series at t=0 with zero:

```r
covar_df <- data.frame(
  time = 0:length(logd),
  covaryt = c(0, logd),
  dFNG    = c(0, diff(fng_subset$FNG_scaled))
)
```

This forces the first data point to use dFNG=0, effectively treating the initial sentiment change as neutral. No justification is given for this choice, and sensitivity to this initialization is not explored. Alternative choices (e.g., using the first observed dFNG value, or dropping the first observation) could alter results near the start of the sample.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project15/Makefile`
