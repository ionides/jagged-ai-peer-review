# Peer Review: W21 Project 08
## "Statistical Models for Solar Flare X-ray Flux Time Series"

---

## Summary

This project applies a sequence of increasingly complex time series models to solar flare X-ray flux data from the GOES satellite in 2019: a Gaussian binary HMM, a Student-t binary HMM, a Gaussian HMM with AR(1) transitions, and a Heston stochastic-volatility model, all implemented in `pomp`. The authors motivate each model with a clear narrative (heavy tails, correlation in volatility, mean-reversion) and use iterated filtering (mif2) with global search for inference. The project is ambitious in scope and the mechanistic motivation for the Heston model is novel in this domain. However, the work has several serious methodological weaknesses: the "poor man's" profile likelihood used for the HMM models is in fact a likelihood slice rather than a true profile, the Gaussian HMM global search uses only Np=200 particles, the Gaussian HMM AR(1) model is acknowledged to show rising-then-falling likelihood but no structural remedy is attempted, the AIC table mixes ARMA and POMP likelihoods without noting any comparability issues, and the Heston model's search box contains a stray parameter (`sigma_nu`) that is never defined in the model.

---

## Major Issues

### 1. "Poor man's profile" is a likelihood slice, not a profile likelihood (CC-Yes, Error 1.2)

In Sections 5 and 6, the authors construct what they call "Poor man profile CIs" by taking the upper envelope of multi-start optimization runs and applying the Wilks threshold. This is precisely the procedure described in the course as a "poor man's profile." However, the key requirement of a true profile likelihood — re-optimizing over all nuisance parameters at each fixed value of the target parameter — is not met. The scatter plots show points from the global and local search results pooled together without fixing the target parameter and re-optimizing at each value. The resulting CI is unreliable: it can be either too narrow (if the nuisance parameters are not free to compensate) or artificially constrained by the search-box boundaries. The authors acknowledge the limited precision ("CI precision is not high due to limited number of points above the threshold"), but this understates the problem — the procedure is not a valid profile. For the Gaussian HMM, the authors report only four parameters' CIs, giving no uncertainty for sigma0, sigma1, or eta. To fix this, the authors should run a dedicated profile sweep: fix the target parameter on a grid, run mif2 at each grid point starting from the MLE of the nuisance parameters, and report the resulting upper envelope.

### 2. Gaussian HMM global search uses Np=200 particles (insufficient)

In the Gaussian HMM global search (lines 402–420), the likelihood is re-evaluated using `pfilter(Np=200)`. With only 200 particles, the particle filter estimate carries substantial Monte Carlo variance, and the identified maximum may not be the true MLE. This is particularly acute for the global search, where the goal is to compare likelihoods from qualitatively different starting regions. The reported MLE (-106.76) may reflect Monte Carlo noise rather than the true maximized likelihood. By contrast, the initial particle filter evaluation in the same section uses Np=5000. The global search evaluation should use at least Np=2000 or a level consistent with the rest of the analysis.

### 3. Gaussian HMM AR(1): declining likelihood is acknowledged but not addressed structurally (CC-Yes, Error 1.5)

In Section 7 (Gaussian HMM with AR(1)), the authors observe that "the log likelihood goes up then down as the iterations progress" and describe this as "a sign of model misspecification." They acknowledge this is puzzling given the model is a generalization. However, according to course teaching (Q10-01), when iterated filtering shows a rising-then-falling log-likelihood trajectory, the appropriate response is structural revision of the model — not simply reporting the "last iteration estimator." The authors use this problematic estimator anyway and report its likelihood (-78.36) in the comparison table, treating it as a valid comparison point. A model whose inference procedure is explicitly noted to be malfunctioning should not appear in a likelihood comparison table without a strong caveat, and the "last iteration estimator" is not a principled MLE. The authors should either fix the model specification or exclude this model from quantitative comparison.

### 4. AIC comparison mixes ARMA/GARCH and POMP likelihoods without noting potential non-comparability

The final summary table (Section 9) includes AIC values for ARMA(1,3), GARCH(1,1), ARMA(1,3)+GARCH(1,1), and the POMP models side by side. The GARCH(1,1) likelihood is computed via `tseries:::logLik.garch`, which is known to use non-standard normalization conventions (see Error 2.9 in the weakness reference). The ARMA(1,3)+GARCH(1,1) is fitted via `fGarch::garchFit`, which also has its own normalization. The authors do not remark on whether these values are on the same scale as the POMP particle-filter likelihoods. If the GARCH and ARMA likelihoods are not on the same scale as the POMP likelihoods, the entire AIC table is misleading. The authors should verify that all likelihoods are computed as log p(y_{1:T} | parameters) for the same observed sequence, and state this explicitly. In particular, the GARCH(1,1) is fitted on the demeaned series (y - mean(y)), not on the original series, making its likelihood directly incomparable to models fitted on y.

### 5. Heston global search box contains undefined parameter `sigma_nu`

In the Heston global search (lines 1568–1580), the search box is defined as:
```
heston_box <- rbind(
  sigma_nu=c(0.005,0.05),
  k    =c(0.01, 0.6),
  ...
)
```
The parameter `sigma_nu` does not appear anywhere in the Heston model definition, paramnames, or the rproc1/rproc2 code snippets. It appears to be a leftover from a previous (possibly Breto-type) model variant. When `apply(heston_box, 1, function(x) runif(1, x[1], x[2]))` is called, the resulting named vector will include a `sigma_nu` entry that will either be silently ignored or cause an error depending on the pomp version. This is a code correctness bug that calls the validity of the Heston global search results into question. Additionally, the results folder contains `breto_box_eval-3.rda`, `breto_mif1-3.rda`, and `breto_pf1-3.rda` files — suggesting a Breto model was investigated but omitted from the report, and these artifacts contaminated the Heston search box definition.

### 6. No non-mechanistic benchmark comparison (CC-Yes, Error 1.6)

The paper compares POMP models to ARMA(1,3)+GARCH(1,1), which the authors themselves treat as a baseline. However, neither the ARMA(1,3) nor the GARCH are a proper IID or negative-binomial benchmark. The course emphasizes comparing to a non-mechanistic baseline (e.g., an ARMA or IID model) to test whether mechanistic structure adds predictive power. The comparison between ARMA+GARCH (loglik ~450) and the Heston model (loglik -21.66) is huge and suspicious — it suggests these models are not being evaluated on the same likelihood scale (see Issue 4), rather than demonstrating that the Heston model dramatically outperforms ARMA. A simple ARMA model on the log-scale data, evaluated on the same particle-filter likelihood scale as the POMP models, would allow a meaningful benchmark.

### 7. Gaussian HMM AR(1) model violates the POMP conditional independence requirement

The Gaussian HMM AR(1) model defines the measurement model as `y = Y_state` (identity measurement), where `Y_state` is itself propagated as part of the latent process using `covaryt` (lagged observed data). The `dmeasure` evaluates `dnorm(y, mu0, s0, give_log)` where `mu0 = a0 + b0 * Y_state` and `Y_state = covaryt` (the previous observation). This means the observation density at time n depends on the observation at time n-1, violating the conditional independence requirement of POMP: observations must depend only on the current latent state, not past observations. While this is a standard trick for making non-Markovian models fit the POMP framework (via the covariate channel), the authors do not acknowledge or justify this construction, which may confuse readers about the model's validity.

---

## Minor Issues

### 8. Data aggregation choice (97.5th percentile) is not formally justified

The authors aggregate 1-minute GOES X-ray readings to 12-hour intervals by taking the 97.5th percentile, stating it is "robust against outlier noises." However, this choice is not formally motivated. Using an extreme quantile rather than the mean or median changes the distributional properties of the resulting time series and may introduce systematic bias. The authors do not assess sensitivity to this aggregation choice or compare it to alternatives. A brief sensitivity check (e.g., max vs. 97.5th percentile) would strengthen the data section.

### 9. Student-t HMM uses `euler(delta.t=1/12)` while Gaussian HMM uses `discrete_time`

The Gaussian HMM uses `discrete_time(hmm_step)` while the Student-t HMM uses `euler(thmm2_step, delta.t=1/12)`. The step function in both cases is a discrete Bernoulli transition with no continuous-time meaning, so the use of `euler` with `delta.t=1/12` is incorrect and will cause the step to be called 12 times per observation period. This inconsistency may lead to different effective transition probabilities between the two models, making their likelihoods not directly comparable on the same time scale.

### 10. The "last iteration" estimator for the Gaussian HMM AR(1) is not a valid MLE

The authors use the phrase "last iteration estimator" and acknowledge it is not the MLE (Section 7). Despite this, the result (-78.36) is included in the comparison table (Section 9) without any asterisk or caveat. Readers comparing models by AIC will treat this as a valid MLE-derived AIC, which it is not. The AIC entry for this model should be marked as "not applicable" or excluded.

### 11. Heston Euler discretization formula for the volatility process contains an error

The Heston volatility SDE is $dV_n = \kappa(\bar{\sigma} - V_n)dt + \sigma\sqrt{V_n}dW^V$. The paper implements log volatility Z = log(V), but the discretization formula shown in the text is:
$$V_n = V_{n-1} + \kappa\left(\bar{\sigma}\exp(-V_{n-1}) - 1\right) - \frac{1}{2}\sigma^2 + \sigma(\rho\epsilon_1 + \sqrt{1-\rho^2}\epsilon_2)$$
This does not correspond to a standard Euler discretization of the Heston SDE in log-volatility space; the mean-reversion term mixes levels and exponentials in an unusual way. The code implements this formula directly (`k*(exp(-Z) * s_bar - 1)`), which may not correctly approximate the original SDE. The authors should verify the derivation or cite a source for this discretization.

### 12. Conditional log-likelihood diagnostic is from the last mif2 object, not the MLE

In Sections 6 and 8, the filtering diagnostics (ESS and conditional log-likelihood plots) are computed from `if.box` — the final state of the mif2 objects after iterated filtering — rather than from a pfilter run at the identified MLE. Because mif2 perturbs parameters at each iteration, the conditional log-likelihoods from the last iteration are not representative of the model fit at the MLE. The diagnostic should be generated by running pfilter with the MLE parameter vector.

### 13. Global search box for the Heston model has rho bounded between 0 and 1 only

The Heston model allows correlation $\rho \in (-1, 1)$ between the Brownian motions $W^S$ and $W^V$. However, the global search box restricts `rho = c(0, 1.0)`, excluding negative correlations entirely. The MLE found (`rho = 0.9993`) is at the boundary of this constraint, which is suspicious and may indicate the optimizer is hitting the box boundary rather than finding a genuine interior maximum. The logit transformation applied to rho maps $(-1, 1)$ to the real line, but the box does not use this transformation space — it samples uniformly on the constrained scale. Negative rho values should be explored.

### 14. Paper contains a typo in the conclusion: "likelihoos" and "exhbited"

Section 9 contains "Student-t does better than Gaussian HMM in term of likelihoos" and "the log likelihood exhbited a strange behavior." These are minor typographical errors that should be corrected.

### 15. No sessionInfo() or package versions reported

The report does not include a `sessionInfo()` call or list of package versions. Given that the `pomp` package has undergone API changes, the exact `pomp` version is needed for reproducibility. The `fGarch`, `tseries`, and `forecast` packages are also version-sensitive. A `sessionInfo()` at the end of the document would satisfy minimum reproducibility standards.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project08/blinded.rmd`
