# Peer Review: W21 Project 07
**Title:** Information Epidemics: Modeling Search Trends during the GameStop Short Squeeze Using Stochastic Compartmental Models

---

## Summary

This project applies a stochastic SIRS compartmental model to Google Trends search frequency data for the term "gme" during the 2021 GameStop short squeeze, treating information spread as analogous to disease transmission. The paper uses iterated filtering (IF2) for parameter estimation and presents profile likelihood plots for three parameters. While the motivating analogy is creative and the POMP framework is appropriately invoked, the analysis suffers from several critical methodological deficiencies: no non-mechanistic benchmark comparison is included, the profile likelihood computation is pseudo-profile (based on global-search scatter rather than constrained optimization), the measurement model contains a misspecified negative binomial parameterization, the global search is run at a debugging run-level (run_level=1) with severely inadequate computational effort, and the rho parameter is excluded from rw.sd during the global search without justification. The conclusions drawn from the parameter search and profile likelihood plots are unreliable given these issues.

---

## Major Issues

### 1. Pseudo-profile likelihood: no dedicated profile IF2 search was ever executed

The profile likelihood plots in Section 5.2 are not genuine profile likelihoods. The code constructs `guesses2` using `profile_design(eta=seq(0.01,0.1,length=40), ...)`, but the subsequent `stew()` block (results2.rda) iterates over `guesses` — the original global-search grid — not `guesses2`. Furthermore, the rw.sd inside that block (`rw.sd(Beta=0.02, rho=0.02)`) does not fix any parameter at profile-grid values, and the profiled parameter eta is missing from rw.sd entirely. The profile plots for Beta, mu_IR, and mu_RS are then produced by filtering and grouping the combined global search results without any constrained optimization at each parameter value. Applying a chi-squared cutoff (`max(loglik) - 0.5*qchisq(df=1,p=0.95)`) to these scatter plots produces confidence intervals with no valid statistical interpretation. This affects all reported CIs (Beta: [0.55, 8.21], mu_IR: [0.30, 0.99]) and is a major reproducibility and inferential failure. (See the `pomp-pseudo-profile-audit` skill; Wheeler et al. 2024, §Parameter identifiability and uncertainty.)

### 2. No non-mechanistic benchmark comparison

The SIRS model is never compared against any non-mechanistic baseline (ARMA, seasonal ARIMA, negative binomial regression). Without such a comparison, it is impossible to assess whether the mechanistic model captures structure in the data beyond what a simple statistical model achieves. The negative binomial log-likelihood from an auto-regressive benchmark on 88 days of normalized search data would provide an essential reference point. The absence of this comparison is the single most diagnostic shortcoming in the analysis (Wheeler et al. 2024, §Benchmark comparison).

### 3. Severely inadequate computational effort (run_level=1)

The analysis is run at `run_level=1`, which sets `Np=100` particles, `Nmif=10` IF2 iterations, `Nseq=100` starting guesses, and `Nreps_eval=2` likelihood evaluation replicates. These values are appropriate only for debugging, as the comment in the code acknowledges ("helps us debug -- we want to use 3 when actually running"). With only 100 particles and 10 IF2 iterations, the particle filter likelihood estimates have high Monte Carlo variance, and the IF2 chains are far from converged. The reported log-likelihoods and the convergence plots (which are not shown) cannot support any inferential conclusion. The paper should be re-run at run_level=3 (Np=5000, Nmif=200, Nseq=5000) before results are reported (Wheeler et al. 2024, §Computational adequacy).

### 4. Misspecified negative binomial measurement model

The dmeasure Csnippet is `lik = dnbinom(count, H, rho, give_log)`, and the rmeasure Csnippet is `count = rnbinom(H, rho)`. In R's `dnbinom(x, size, prob, ...)`, the parameters are size (dispersion) and prob (success probability), not mean. This means H is used as a dispersion/size parameter and rho as a success probability. With H being the accumulator of new infections (potentially 0 at the start and fluctuating throughout), using H as the size parameter of a negative binomial makes the dispersion data-dependent in an unusual way that is almost certainly unintended. The canonical formulation for POMP epidemic models uses `dnbinom_mu(count, mu=rho*H, size=k, give_log)` where k is a separate overdispersion parameter. As written, the model's likelihood and simulation are using an internally consistent but almost certainly wrong parameterization of the negative binomial. The author acknowledges trouble with the binomial measurement model but the adopted parameterization of dnbinom is not explained or justified. (See Wheeler et al. 2024, §Measurement model specification.)

### 5. rho excluded from rw.sd in global search without justification

In the global search chunk, the `rw.sd` call only perturbs `Beta`, `mu_IR`, `mu_RS`, and `eta`; rho and N are absent from `rw.sd`. Yet rho and N are sampled from the initial `runif_design` box. Once IF2 begins, rho and N are frozen at their starting-point values for each replicate and never updated. This means the global search is effectively a 4-dimensional search over (Beta, mu_IR, mu_RS, eta) with rho and N fixed at random starting points — not a joint 6-dimensional search. The text offers no justification for fixing rho and N during IF2. Given that rho's range is restricted to [0.1, 0.3] and N's range to [1000, 10000], and that the measurement model depends critically on both, this exclusion can materially affect the reported MLE.

### 6. Initial conditions H=5 not reset by accumvars mechanism

The `rinit` Csnippet sets `H = 5` at initialization. Since H is declared in `accumvars`, it is automatically reset to zero after each observation time by pomp's accumvars mechanism. However, the non-zero initialization of H at t=0 means the measurement model is evaluated against H=5 (not the accumulated dN_SI from the first interval), which artificially inflates the likelihood for the first observation. The correct initialization is `H = 0`. This is a minor structural inconsistency, but it could affect the log-likelihood estimate at the first observation time point.

### 7. Population N treated as a free parameter on normalized data

The search frequency data are normalized by Google Trends to have a maximum of 100. Treating N as a parameter estimated from normalized data (range [1000, 10000]) lacks clear interpretation, because the scale of the observations is arbitrary. The reporting rate rho then must simultaneously absorb the arbitrary normalization scale and the true reporting fraction, making both parameters uninterpretable. The authors acknowledge this difficulty but do not resolve it, noting "it is difficult to interpret the reporting rate rho and population size N." A more principled approach would be to fix N at a chosen population size and interpret rho relative to normalized units, or to explicitly model the normalization as part of the measurement model.

---

## Minor Issues

### 8. Benchmark pfilter uses manual simulation parameters, not MLE

The benchmark log-likelihood (Section 4) is evaluated at `params <- c(Beta=1.3, mu_IR=0.5, mu_RS=0.03, rho=0.4, eta=0.5, N=3000)` — the hand-chosen simulation parameters, not the MLE. This is an appropriate pre-search diagnostic, but the text presents it alongside the global search as if it is a reference point for comparison. The log-likelihood at the MLE should be the relevant benchmark. The paper would benefit from explicitly distinguishing the pre-search baseline from the post-search MLE evaluation.

### 9. Profile for eta is never plotted despite guesses2 being constructed for it

The `profile_design()` call constructs a grid over `eta=seq(0.01,0.1,length=40)`, suggesting a profile over eta was intended. However, no profile plot for eta appears in Section 5.2. The three plots shown are for Beta, mu_IR, and mu_RS. The text does not explain why the eta profile was dropped. If the eta profile was computed (even using the incorrect pseudo-profile procedure), it should be shown for completeness; if it was not, the paper should not construct guesses over it.

### 10. Global search Nmif argument passed incorrectly

In the global search chunk, the call is `mif2(params=c(unlist(guess)), Np=Np, Nmif, ...)`. The argument `Nmif` is passed positionally without naming it, which in R means it is passed as the second positional argument. In `mif2()`, the second positional argument is `Np` (not `Nmif`). The named argument `Nmif=Nmif` should be used. If the code actually ran as written, Nmif would be interpreted as an additional element of the `Np` argument or produce an error, depending on the pomp version. The double `mif2(Nmif)` call at the end is also positionally ambiguous.

### 11. Quantitative goodness-of-fit assessment is purely visual

Beyond reporting the MLE log-likelihood value, the goodness-of-fit assessment in Section 5.1 is entirely visual — simulated trajectories are plotted against observed data with no quantitative summary. There is no AIC comparison, no log-likelihood ratio test against the benchmark, and no conditional log-likelihood plot to identify periods of poor fit. The authors themselves acknowledge the simulations are "quite inconclusive." A more rigorous assessment would include at minimum the AIC and a comparison to the pre-search benchmark. (Wheeler et al. 2024, §Quantitative goodness-of-fit reporting.)

### 12. H accumulates dN_SI (new infections) but observations represent search frequency

The choice to accumulate `dN_SI` (new susceptible-to-infected transitions) as the proxy for search activity is reasonable but not discussed. The observed quantity (normalized Google Trends search frequency) is a population-level aggregate whose relationship to "new infections" in the model is unclear. At minimum, the paper should acknowledge that H represents new daily "infections" in the information-spread sense, and explain why this is the appropriate quantity to link to search frequency rather than, say, the current I compartment.

### 13. No convergence diagnostics are shown

There are no convergence trace plots, no pairs plots showing the distribution of starting guesses versus converged results across all parameters, and no discussion of whether the IF2 chains converged. Given that the analysis was run at the debugging run level (run_level=1 with Nmif=10), it is highly unlikely that any chain has converged, making the absence of convergence diagnostics especially problematic. (Wheeler et al. 2024, §Computational adequacy.)

### 14. Model corroboration with external knowledge is absent

The parameter estimates are not compared to any independent epidemiological or social-media literature values. For example, the estimated recovery rate mu_IR ≈ 0.5/day implies the average "infection duration" (period of active interest in the event) is about 2 days; no discussion of whether this is plausible for a social media trend is provided. The transmission rate Beta ≈ 1 is also not compared to any prior estimates for information cascades. (Wheeler et al. 2024, §Corroboration with scientific knowledge.)

### 15. Notation inconsistency: beta vs. Beta

The mathematical section uses lowercase β consistently (e.g., the force of infection is β I/N), but the code and results use `Beta` (capitalized). The Conclusion section alternates between "β" and "beta" without definition. This is a minor presentation issue but should be made consistent throughout.

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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project07/blinded.Rmd`
