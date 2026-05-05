# Peer Review: Analysis of Stochastic Volatility Models for Ethereum Returns
**Semester:** W22 | **Project:** 14

---

## Summary

This project analyzes hourly Ethereum return data using three models: an AR(2)-GARCH(1,1) benchmark, a Breto (2014) leveraged stochastic volatility model, and a discretized Heston stochastic volatility model. The central claim is that the Heston POMP model achieves the best log-likelihood (~34975) and is therefore the preferred model. The project contains a number of significant technical errors and methodological gaps that undermine this conclusion.

---

## Weaknesses (Prioritized)

### 1. [MAJOR] Critical State Equation Mismatch Between Model and Code

The stated Heston model is:

$$V_n = (1-\phi)\theta + \phi V_{n-1} + \sqrt{V_{n-1}}\,\omega_n$$

But the implemented C snippet (line 439) reads:

```c
V = theta*(1 - phi) + phi*sqrt(V) + sqrt(V)*omega;
```

This substitutes `sqrt(V)` for `V` in the autoregressive term, replacing `phi * V_{n-1}` with `phi * sqrt(V_{n-1})`. The implemented process is therefore:

$$V_n = (1-\phi)\theta + \phi\sqrt{V_{n-1}} + \sqrt{V_{n-1}}\,\omega_n$$

This is a fundamentally different stochastic process from the one claimed in the equations. The mean reversion and persistence properties are altered. All results for the Heston model are based on this misspecified process, and the stated conclusion that this model performs best is built on a flawed implementation.

---

### 2. [MAJOR] Bake/Stew Files Are Absent — Results Cannot Be Verified

The Breto model uses `bake()` (saving to `.rds`) and the Heston model uses `stew()` (saving to `.rda`). Neither set of cached output files exists in the project directory. Only `Blinded.Rmd`, `Blinded.html`, `ETH.csv`, and `Makefile` are present. All reported log-likelihood values (28977 for Breto, 34975 for Heston) come from the pre-rendered HTML and cannot be independently reproduced or verified from the submitted materials. This is a fundamental reproducibility failure.

---

### 3. [MAJOR] Heston Model Uses `stew()` While Breto Uses `bake()` — Mixing Caching Mechanisms Inconsistently

The Breto section uses `bake()` with `.rds` files while the Heston section uses `stew()` with `.rda` files. This inconsistency means the two sections depend on different caching/reproducibility infrastructure. More critically, the `bake()` calls for the Breto model are run twice (lines 291–311 and 313–333) — once to extract `if1` and once to extract `L.if1` — but both calls use the same file name (`Breto_mif1-%d.rds`). The bake mechanism returns the cached object on the second call, so this works only if both calls return the same file. While not fatal, it is confusing and risks a mismatch if the cache is stale.

---

### 4. [MAJOR] Log-Likelihood Comparison Is on Different Scales / Different Datasets

The ARMA-GARCH model is fit on `eth_demeaned = (eth_ret - mean(eth_ret))[1:9000]` — a subset of 9000 observations. The Heston and Breto models appear to use `w = crypto$demeaned`, which is derived from the full dataset (up to ~11130 observations after NA removal). If the models are fit on different numbers of observations, the raw log-likelihood values are not comparable. The conclusion that the Heston model is best rests on this potentially invalid comparison.

---

### 5. [MAJOR] Variable Name Typo Breaks Breto Local Search Code

In the Breto local search chunk (lines 287–289), the random walk standard deviations for initial value parameters are set as:

```r
G_0 = ivp(eth.sd_ivp),
H_0 = ivp(eth.sd_ivp)
```

The variable `eth.sd_ivp` uses a dot (`.`) separator, but the declared variable at line 280 uses an underscore: `eth_rw.sd_ivp`. The object `eth.sd_ivp` does not exist; R will throw an error. The actual `mif2` calls inside the bake blocks (lines 298–305) correctly reference `eth_rw.sd_ivp`, but the standalone `rw.sd` object defined at lines 286–289 uses the wrong name. This means the `eth_rw.sd` object constructed at lines 286–289 would fail, though it is not actually used in the bake block itself. The code is internally inconsistent.

---

### 6. [MAJOR] Global Search Box for Heston Model Contains Physically Unreasonable Ranges

The global search box (lines 583–589) sets:

```r
sigma_omega = c(0, 10)
theta = c(0, 4)
```

Hourly Ethereum returns are on the order of 0.001 to 0.01. A variance (`theta`) of up to 4 corresponds to a standard deviation of returns of 200%, which is orders of magnitude larger than the observed data. Sampling initial parameters from such extreme ranges greatly reduces the efficiency of global search and increases the probability of particle filter degeneracy. The prior box should reflect the scale of the data.

---

### 7. [MAJOR] No AIC or Likelihood Ratio Test Used for Formal Model Comparison

The conclusion that the Heston model is the best is based solely on raw log-likelihood values (34975 vs. 28977 vs. 28587). No penalty for parameters is applied (AIC or BIC), and no standard error of the log-likelihood estimate is reported for the POMP models. Given that the models differ in structure and potentially in observation count, an informal comparison of raw log-likelihoods is insufficient to support the claim that one model is superior.

---

### 8. [MAJOR] No Simulation-Based Diagnostic for Heston Model

The Breto section performs filtering on simulated data as a sanity check (`sim1.filt`) before applying to real data. The Heston section creates `crypto_sim` via `simulate()` and then sets up `sim1.filt`, but the particle filter (`pf1`) in Section 4.2 is run on `sim1.filt` (simulated data), not `crypto.filt` (real data). This means the Section 4.2 local search preamble may be filtering simulated data rather than real data. The text does not make this distinction explicit and may be conflating diagnostics from simulated vs. real data.

---

### 9. [MINOR] Misidentification of the Source of the May 19, 2021 Crash

The text attributes the May 19, 2021 large negative Ethereum return to "Russian hackers stealing 90 million in Bitcoin." Ethereum and Bitcoin are distinct assets. The actual cause of the broad crypto selloff on that date was China's announcement of restrictions on cryptocurrency mining and transactions, amplified by Elon Musk's comments about Bitcoin's environmental impact. Attributing it to a hacker event for a different asset is factually inaccurate and reduces scientific credibility.

---

### 10. [MINOR] Reference Section Is Empty

Section 6 (Reference) is a heading with no content. All references are embedded as footnotes in the text. A project at this level should have a properly formatted reference list. Several key references (the Breto 2014 paper, the original Heston 1993 paper) are cited only in footnotes and not in a bibliography.

---

### 11. [MINOR] Heston Process Is Applied to Variance but Measurement Uses sqrt(V) as SD — Constraints Are Weak

The measurement model `lik = dnorm(y, 0, sqrt(V), give_log)` requires `V >= 0`. The `if(V < 0){V = 0;}` guard is mentioned as the fix, but this introduces a reflecting boundary that is not part of the Heston model and may cause the process to cluster at zero. The text acknowledges this issue but does not discuss whether it creates bias in parameter estimates or log-likelihood evaluations.

---

### 12. [MINOR] `eth_Nreps_local` Is Set to 20 for Both Local and Global Breto Searches at run_level=3

At run_level=3, `eth_Nreps_global` is also 50 (line 267), giving an appropriate distinction. However, `eth_Nreps_local` = 20 and `Nreps_local` = 20 for the Heston model. The Heston global uses `Nreps_global = 100`, which is much larger than the Breto global's 50. The asymmetry in computational effort between the two POMP models is not discussed and could partly explain the difference in performance.

---

### 13. [MINOR] Cooling Schedule Is Fixed Without Justification

Both the Breto and Heston mif2 searches use `cooling.fraction.50 = 0.5` without discussion. This means perturbation magnitudes halve by iteration 50. With `Nmif = 200`, this results in very small perturbations in the later stages. No sensitivity analysis of this schedule is reported.

---

### 14. [MINOR] Heston Model Description Credits Project 16 of W18 Heavily But Departs Without Explanation

The text states the code "was adapted from a previous final project" (Project 16, W18) and that "the key difference is that we do not carry the observed process as a random process." However, the state equation implemented differs from the cited model in the additional way noted in Weakness #1. The relationship to the source project is not fully transparent.

---

### 15. [MINOR] Pairs Plot for Breto Global Search Filters at `logLik > max(logLik) - 50` but Heston Uses All Points

The Breto global pairs plot (line 392) restricts to runs within 50 log units of the maximum, which is appropriate. The Heston global pairs plot (line 612) uses all `r.box` rows without filtering. Low-likelihood runs in the Heston global search would obscure the structure of the high-likelihood region and make the pair plot less informative.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project14/Blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project14/ETH.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project14/Makefile`
