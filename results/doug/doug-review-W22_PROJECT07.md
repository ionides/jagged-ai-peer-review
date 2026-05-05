# Peer Review: W22 Project 07
## "Volatility Analysis on Ford and Tesla Stock"

---

## Summary

This project applies ARIMA, GARCH, and POMP models to the log-returns of Ford and Tesla stock prices (March 2017 to March 2022, N = 1,258 daily observations). The ARIMA section correctly concludes that log-returns resemble white noise. The GARCH section fits normal and t-distributed GARCH models and compares them by log-likelihood. The POMP section implements the stochastic leverage model of Bretó (2014) using mif2/particle filter inference. While the project demonstrates familiarity with the POMP modeling framework and performs both local and global searches, it contains several serious methodological and implementation errors: the initial benchmark log-likelihood is evaluated on a simulated dataset instead of the real data, producing a nonsensical −1748 benchmark that cannot be compared to later GARCH or IF2 log-likelihoods; the global IF2 search for Tesla is incorrectly initialized from a previous mif2 result object, anchoring it to the local-search solution; Tesla data is truncated to only the last 365 observations while Ford uses the full 1,258 observations, making the two POMP sections incomparable; the paper's claim that "POMP performs much better than GARCH" rests on an incoherent comparison of log-likelihoods across different datasets and model definitions; and no profile likelihoods or confidence intervals are presented for any parameters.

---

## Major Issues

### 1. Initial particle-filter benchmark evaluated on simulated data, not real data

In the Ford POMP section, the initial pfilter run evaluates `sim1.filt` — a pomp object constructed from a single simulated trajectory using `simulate(sim1.sim, seed=531, params=params_test)` — rather than `ford_filter`, the real-data pomp object. The reported value of −1748.8 is therefore the likelihood of the test parameters under a randomly simulated dataset, not under the Ford log-return observations. The text describes this as "our rough benchmark" to compare against the IF2 results. The same structural error appears in the Tesla section, where `sim1.filt` is again passed to pfilter with result −1610.31 presented as a baseline.

Because the simulated and real datasets are different, the two log-likelihood values are on completely different scales and cannot be compared. For a Gaussian observation model on daily log-returns (length N ≈ 1,258 with roughly zero mean and variance ~0.0006), the log-likelihood of reasonable parameters should be on the order of −(N/2)log(2π) − (N/2) ≈ −2,300 to −2,000 at the test parameters. A value of −1,748 is loosely consistent with the right scale but comes from a different (random) dataset and has no evidential value for the Ford data. The narrative presents this value as a meaningful comparison point, which is misleading. The fix is to evaluate `pfilter(ford_filter, Np=ford_Np)` at `params_test` and report that value as the baseline.

### 2. Tesla POMP uses only last 365 observations; Ford POMP uses all 1,258

The Ford POMP section reads the full dataset (`ford$Adj.Close`, 1,259 rows) and constructs `Ford_lreturn` with N = 1,258 observations. The Tesla POMP section reads the Tesla data with `tail(TeslaData, 365)`, keeping only the most recent year's worth of data (approximately March 2021 to March 2022). This means the Tesla POMP model is fitted to a fundamentally different sample than the Ford POMP model: 365 versus 1,258 observations, covering a completely different time period.

All subsequent cross-model comparisons — including the conclusion that "the fitted volatility for Tesla is wider than Ford" and the log-likelihood comparisons between the two POMP models — are invalid because the models are not fitted to the same or comparable data. Tesla's log-likelihood values (707.6 local, 709.6 global) are positive, while Ford's are around 3,150 — the difference of ~2,440 log-likelihood units is almost entirely explained by the dataset size and period difference, not by any genuine difference in model fit. The authors do not acknowledge this discrepancy anywhere in the paper.

### 3. Tesla global IF2 search incorrectly initialized from previous mif2 result

In the Tesla global search code block, the mif2 call uses `if1[[1]]` — the first mif2 result object from the local search — as the first argument: `mif2(if1[[1]], params=apply(Tesla_box, 1, function(x) runif(1,x)))`. The correct pattern is to pass the base pomp object (`Tesla.filt`) as the first argument. By passing `if1[[1]]`, the global search inherits the internal cooling schedule state from the local chain, which is at or near its final (heavily cooled) state after 200 IF2 iterations. This means the random starting parameters drawn from `Tesla_box` are effectively not explored — the perturbations shrink to near zero within a few iterations, and each global replicate converges near the local-search solution rather than exploring the full parameter box.

The Ford global search has the same structural error: `mif2(if1[[1]], params=apply(ford_box, 1, function(x) runif(1,x)))`. The paper refers to these results as confirming "convergence from different starting points," but the search never genuinely starts from those different points. The reported global maxima (Tesla: 709.6, Ford: 3,150.9) may simply be the same local optimum found repeatedly.

### 4. Claim that "POMP performs much better than GARCH" is not supported

The conclusion states: "The POMP models perform much better than the GARCH for both Ford and Tesla." For Ford, the authors compare the POMP log-likelihood of ~3,154 to the t-GARCH(1,1) log-likelihood of 3,189. The POMP model actually achieves a lower log-likelihood than the GARCH model for Ford, directly contradicting the stated conclusion. For Tesla, the POMP log-likelihood of ~709 is positive, while the GARCH log-likelihood of 2,484.77 is much larger — but the Tesla POMP model was fitted to only 364 log-returns versus GARCH's 1,258, making this comparison completely invalid.

No AIC adjustment for number of parameters is provided, and no formal model comparison (likelihood ratio test or AIC) is presented to support the comparative claim. The GARCH models have 5–6 parameters each; the POMP model has 6 parameters plus a more complex computational procedure. A proper AIC comparison using consistent data and the maximum log-likelihood for POMP would be required before any such claim could be made.

### 5. Non-convergence acknowledged but results interpreted as substantively meaningful

The paper acknowledges convergence failures in both Ford and Tesla POMP models. For Ford: "the 75th percentile log-likelihood is many log units away from the maximum log-likelihood estimate" and "$H_0$ and $\mu_h$ are weakly identified." For Tesla: "the projected convergence looks bad on $\mu_h$, $H_0$, and $\phi$." Despite this, the paper proceeds to draw comparative conclusions about volatility differences between Ford and Tesla. The text's rationalization that "weak identifiability is not necessarily a problem" (citing HW8) is partially valid — weak identifiability of some parameters does not invalidate the overall likelihood — but the convergence plots showing that most replicates are tens of log-units below the maximum indicates a genuine convergence failure for multiple parameters, not merely wide CIs for well-identified parameters.

### 6. No benchmark comparison between the mechanistic POMP model and a non-mechanistic baseline

The GARCH models in this project are framed as a preliminary step before POMP, not as a formal baseline for comparison with the POMP model. No quantitative goodness-of-fit comparison on the same dataset with the same observations is presented. Wheeler et al. (2024) identify benchmark comparison as one of the most important methodological practices: "mechanistic models should be compared against non-mechanistic statistical benchmarks... this provides an objective baseline for whether the mechanistic model captures meaningful structure." The paper's final comparative claim depends on a coherent benchmark comparison that is never actually performed.

### 7. No profile likelihoods or confidence intervals for any parameter

The paper reports point estimates of parameters implicitly (through pairs plots and convergence traces) but presents no profile likelihoods and no confidence intervals for any parameter in either the Ford or Tesla POMP model. Wheeler et al. (2024) note that profile likelihoods are essential for assessing whether parameters are identifiable from the data. Given that the authors acknowledge weak identifiability for $\mu_h$ and $H_0$, profile likelihoods are especially warranted here. Without profiles, it is impossible to determine how precisely any parameter is estimated or whether the parameter estimates are meaningfully constrained by the data.

### 8. Particle count and computational settings are inadequate for the Ford section

The Ford POMP section sets `ford_Np = switch(run_level, 100, 1e3, 1e3)` at run_level=3, using only 1,000 particles. The global search uses 100 replicates with 1,000 particles each and evaluates log-likelihood with 10 pfilter replicates. For 1,258 time steps, 1,000 particles is a modest number; the Monte Carlo standard error reported for the global search is 0.318 log-likelihood units, which is acceptable but could be improved. More critically, the archived `box_eval-2.rda` file appears to be from run_level=2 (1,000 particles, 20 global replicates) rather than run_level=3 as described in the text. The mismatch between the described computational effort and the archived artifacts undermines reproducibility.

---

## Minor Issues

- **Unresolved sentence fragment in introduction**: The sentence "We use the log return rate of price, and calculated as the following: (why we want to use log return instead of return?)" contains an in-progress parenthetical question that was never answered or removed. This indicates the document was not proofread before submission.

- **Figure caption mismatch in Tesla section**: Figures in the Tesla section are labeled "Figure 1" and "Figure 2" in the captions (`fig.cap="Figure 1: Original Data"`, `fig.cap="Figure 2: LogDiffTeslaDmean..."`) despite being the 15th–18th figures in the document. The Ford section already uses Figures 11–14, so the Tesla section's re-use of "Figure 1" and "Figure 2" creates numbering confusion.

- **Wrong-dataset prediction for Tesla GARCH**: In the GARCH prediction code for Tesla (Figure 10), the green confidence band is plotted using `ford_ahead[,2]` instead of `tesla_ahead[,2]`: `lines(tesla_ahead[,1]+ford_ahead[,2], ...)` and `lines(tesla_ahead[,1]-ford_ahead[,2], ...)`. The predicted Tesla volatility band uses Ford's predicted standard errors, which is a copy-paste error that invalidates Figure 10.

- **Tesla model description refers to "Apple"**: The figure caption on the Tesla section states "Figure 1: Adjusted Closing Price of Apple from 2017 to 2022," even though the project is analyzing Tesla stock. This is a clear copy-paste artifact from the cited reference (a W20 project on Apple stock).

- **ARMA model selection not connected to GARCH**: The ARMA analysis concludes that ARMA(0,0) — white noise — best fits the log-returns for both stocks. This finding is not explicitly connected to the GARCH modeling section. The standard justification for GARCH modeling is precisely that ARMA on log-returns leaves heteroskedastic residuals (ARCH effects). The paper should include an ARCH/LM test or squared-return ACF plot to confirm the motivation for GARCH after the ARMA analysis.

- **No model diagnostics specific to the POMP stochastic leverage model**: The POMP section reports convergence traces and pairs plots but does not compare simulated trajectories from the fitted model to the observed log-return series. Forward simulation from the estimated parameters — showing whether the model-implied volatility envelope covers the observed returns — would provide useful informal model validation.

- **`mu_h` not properly log-transformed in partrans**: The `partrans` object includes `log=c("sigma_eta","sigma_nu")` and `logit="phi"` but no transformation for `mu_h`. Because `mu_h` is constrained to be negative (it represents the long-run mean of log-volatility), it should either be negated-log-transformed or bounded via a logit with an appropriate range. Unrestricted `mu_h` can in principle take positive values during IF2 perturbation, which is not meaningful for the model.

- **Reference [2] is cited as Breto (2014) in text but listed as course lecture notes**: The in-text citation "[2] Ch.16 Lecture notes" is the reference actually numbered [2] in the bibliography. The model description credits "Breto (2014)" as the source for the stochastic leverage model, but Bretó (2014) does not appear in the reference list. The actual reference for this model should be cited properly (Bretó C (2014), "On idiosyncratic stochasticity of financial leverage effects," Statistics and Probability Letters).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stochastic-dmeas-intermediate/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project07/blinded.Rmd`
