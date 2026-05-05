# Peer Review: W22 Project 14
## "Analysis of Stochastic Volatility Models for Ethereum Returns"

---

## Summary

This project fits two POMP-based stochastic volatility models — an adaptation of Breto's leveraged SV model and a discretized Heston model — to hourly Ethereum return data, alongside ARMA and AR-GARCH benchmarks. The paper's main claim is that the Heston model substantially outperforms all other models (log-likelihood ~34975 vs ~28977 for Breto and ~28587 for AR-GARCH). While the project shows appropriate awareness of POMP methodology and provides ARMA/GARCH benchmarks, the analysis is compromised by a serious mathematical error in the Heston process equation, missing profile likelihood analysis, an invalid cross-model likelihood comparison, questionable convergence in the Breto model, and several code-level bugs that undermine confidence in the reported results. The Heston model's dramatically superior likelihood (a gap of ~6000 log units over Breto) is unexplained and likely reflects a model misspecification or implementation artifact rather than a genuine improvement.

---

## Major Issues

### 1. Critical mathematical error in the Heston process equation (CC-Yes, Error 1.3)

The discretized Heston volatility equation stated in the text (Section 4) is:

$$V_n = (1-\phi)\theta + \phi V_{n-1} + \sqrt{V_{n-1}}\,\omega_n$$

However, the implemented C code reads:

```c
V = theta*(1 - phi) + phi*sqrt(V) + sqrt(V)*omega;
```

The code computes `phi*sqrt(V)` where the model equation requires `phi*V_{n-1}`. This means the code is fitting a process where the mean-reversion term is `phi * sqrt(V_{n-1})` rather than `phi * V_{n-1}`. The implemented model is therefore neither the stated Heston model nor any standard stochastic volatility model. All parameter estimates, likelihoods, and conclusions drawn from the Heston model are invalid as written. The fix is to change `phi*sqrt(V)` to `phi*V` in the C snippet.

---

### 2. Likelihood comparison between ARMA/GARCH and POMP models treated as invalid, then treated as valid (CC-Yes, Error 2.2)

Section 5 directly compares log-likelihoods across three different model classes:
- AR(4) ARIMA: AIC = -54723.34 (equivalently log-likelihood ≈ 27366)
- AR(2)-GARCH(1,1): AIC = -57162.84 (equivalently log-likelihood ≈ 28588)
- Breto POMP: 28977
- Heston POMP: 34975

The ARIMA AIC of -54723.34 corresponds to a log-likelihood of approximately 27366, but the text uses the AIC value itself in one place ("1586 log units higher than benchmark ARMA model" — but -54723.34/(-2) = 27361, which is not 1586 units below 28953). The authors appear to use AIC values directly as log-likelihoods in some comparisons while using actual log-likelihoods for others. This mixing of AIC and log-likelihood values in Section 3.2 produces arithmetically incorrect numerical comparisons and must be corrected.

More broadly, any direct comparison requires all likelihoods to be on the same scale for the same data, with no data truncation differences. The ARIMA model is fit to `eth_demeaned[1:9000]` (first 9000 observations), while the POMP models use `eth_demeaned` without explicit subsetting (which has 9001+ observations based on the ETH.csv structure). If the datasets differ in length, the comparisons are invalid.

---

### 3. No profile likelihood analysis for any model (CC-Yes, Error 1.9)

Neither the Breto model nor the Heston model includes any profile likelihood computation. There is no assessment of parameter identifiability, no confidence intervals on any parameter estimate, and no determination of which parameters can be inferred from the data. Given that the Breto model trace plots show non-convergence for multiple parameters (mu_h, sigma_eta), and the authors themselves note "the spread in likelihood suggests that maybe the numerics are not working smoothly," profile likelihood analysis is essential to determine whether the parameters are identifiable. Without it, no credible inference about model parameters can be made. Per Wheeler et al. (2024) and course instruction (Error 1.9), profile likelihood is the required method for uncertainty quantification in POMP models.

---

### 4. Breto model convergence failure interpreted incorrectly (CC-Yes, Error 1.5 / Error 1.8)

Section 3.2 states: "The trace plot for the MIF iteration shows the log-likelihood is not always climbing along with each iteration. In addition, the different search seems to get the different value of log-likelihood." The authors attribute this to numerics not "working smoothly," citing the homework solutions. However, by the course standard (Error 1.5), a declining or non-monotonically climbing log-likelihood in iterated filtering is a sign of model misspecification, not merely numerical difficulty. The authors' diagnosis is incorrect. Additionally, the local search for the Breto model uses a single starting point (`params_test`) for all 20 replicates, which is a local search by construction — it does not explore the parameter space. The spread in terminal likelihoods across runs from the same starting point further signals convergence problems that are not properly diagnosed.

---

### 5. Implausible 6000-unit likelihood gap between Heston and Breto is unexplained

The reported log-likelihood for the Heston model (34975) exceeds the Breto model (28977) by approximately 6000 log units on the same data. This is an enormous difference — corresponding to a likelihood ratio of e^6000. For models of similar complexity on the same dataset, such a gap either indicates (a) a bug in one or both implementations, (b) a fundamental misspecification, or (c) different datasets being used. The authors do not remark on this gap or investigate its source. Given the mathematical error in the Heston rproc identified in Issue 1 above, this gap is most likely an artifact of fitting a misspecified model. The authors should not report or rely on the Heston likelihood without resolving this discrepancy.

---

### 6. Typo/variable name error: `eth.sd_ivp` vs `eth_rw.sd_ivp` (reproducibility failure)

At line 287-288 of the Rmd, the `rw.sd` object is constructed using `eth.sd_ivp` (with a period):

```r
G_0 = ivp(eth.sd_ivp),
H_0 = ivp(eth.sd_ivp)
```

But the variable defined at line 280 is `eth_rw.sd_ivp` (with an underscore). This is a name collision bug. The outer `rw.sd` object (lines 282–289) would fail with "object 'eth.sd_ivp' not found." The actual `mif2` calls correctly use `eth_rw.sd_ivp` (lines 303–304, 325–326), so the outer `rw.sd` object is dead code. This is evidence of incomplete refactoring but means the analysis-critical code paths do use the correct variable name.

---

### 7. Global search for Breto model uses single starting mif2 object (Code issue)

The Breto global search (Section 3.3, lines 361–363) calls:

```r
if.box <- foreach(...) %dopar% mif2(data = if1[[1]], params=apply(eth_box,1,function(x)runif(1,x)))
```

It uses `if1[[1]]` as the template, which copies the structure of the first local search result. This is the correct approach, but the box covers `phi = c(0.97, 0.99)` — an extremely narrow range that is not meaningfully a "global" search and does not cover most of the feasible parameter space for phi. The Heston model's box uses `phi = c(0, 1)`, which is more appropriate. The Breto global search may not have explored enough of the parameter space to find the true optimum.

---

## Minor Issues

### 8. AIC comparison between ARMA/GARCH and POMP models directly made without justification (CC-Yes, Error 2.2)

The conclusion section states: "The log-likelihood for the ARIMA-GARCH model is 28587.42... The log-likelihood for the Heston model is roughly 34975.32." The ARIMA-GARCH model log-likelihood of 28587 corresponds to its AIC of -57162.84 divided by -2, but the AIC computed by `garchFit` in the `fGarch` package uses a different normalization than what `pomp` reports. Different packages normalize likelihoods differently (Error 2.9). The authors should verify that the GARCH log-likelihood is on the same scale (same data length, same units) as the POMP likelihoods before drawing conclusions from the comparison.

---

### 9. bake() called twice on the same file to extract different list elements (Code duplication)

For the Breto model (Sections 3.2 and 3.3), the code calls `bake()` twice on the same RDS file — once to extract `[[1]]` (the mif2 objects) and once to extract `[[2]]` (the likelihoods). Since `bake()` caches results, both calls re-run the computation if the cache file does not exist, but the two runs will produce different random-seed results (because parallel seeds may differ). This is a subtle reproducibility issue: the `if1` objects used for coefficient extraction and the `L.if1` used for log-likelihood display may not correspond to each other if the cache is not already populated. The standard practice is to call `bake()` once and destructure the list.

---

### 10. No simulation-based diagnostics / goodness-of-fit assessment

Neither model is subjected to simulation-based diagnostics. There are no plots comparing simulated trajectories to observed data (beyond a single `plot(crypto_sim)` call in Section 4.1 which uses the initial `params_test` values, not the fitted parameters). There is no examination of conditional log-likelihoods over time to identify periods of poor fit, and no filtering-distribution comparison. Given that both models exhibit low effective sample size regularly, these diagnostics are essential for understanding whether model misspecification is driving the poor fit. Per Wheeler et al. (2024), Section on Model diagnostics, such tools are necessary for understanding where and how the model succeeds or fails.

---

### 11. Initial conditions in the Heston model: covariate table set up but not used

The Heston model POMP object is constructed with a `covaryt` covariate (line 479: `covarnames=crypto_covarnames`) and a covariate table is set up. However, the `crypto_rproc1` C snippet does not reference `covaryt` at all — the covariate is unused. This appears to be a copy-paste artifact from the Breto model where `covaryt` plays an essential role (carrying observed returns into the latent process). For the Heston model the covariate column is loaded but serves no purpose, which is harmless but confusing and suggests incomplete adaptation of the template code.

---

### 12. Heston model local search: rw.sd built with `ivp(0.2)` for V_0 but local reps use only 20

The Heston local search (`rw_sd`, line 539-543) sets `V_0 = ivp(0.2)` — a large perturbation for the initial condition. However, `Nreps_local = 20` at run_level=3 is at the lower end. More importantly, the pairs plot in Section 4.2 is for local search results, but the text only shows the global search results (Section 4.3 provides the conclusion about "parameters converging fairly well"). A pairs plot for the global search results should be the primary diagnostic but is not shown (the code comments out the pairs plot at lines 609–610).

---

### 13. Parameter interpretation absent

Neither model includes any interpretation of the fitted parameter values in light of the economic or financial meaning of the model. For the Breto model, the converged values of sigma_nu, phi, sigma_eta are not compared to values reported in prior literature for financial data. For the Heston model, the estimated theta (long-run variance) and kappa (mean reversion rate) are not checked against known properties of crypto volatility. Given that the primary stated motivation is understanding cryptocurrency dynamics, this omission weakens the scientific contribution.

---

### 14. Missing references section

Section 6 is labeled "Reference" but appears to be empty in the Rmd (no bibliography entries are present in the document body). All citations appear as inline footnotes. A properly formatted reference list should be included, particularly for the Breto (2014) paper, the Heston model, and the Wheeler et al. (2024) context.

---

### 15. Confusing language about likelihood scale in Section 3.2

The text states: "The log-likelihood value(28953) we get was 366 log units higher than AR-GARCH (28587) and 1586 log units higher than benchmark ARMA model." However, the AR(4) AIC is -54723.34, which corresponds to a log-likelihood of approximately 27,362 — not a value that is 1,586 below 28,953. The gap would be approximately 1,591 log units if the AR(4) log-likelihood is approximately 27,362. This numerical claim should be stated precisely with the actual log-likelihood values (not AIC) and verified for consistency.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project14/Blinded.Rmd`
