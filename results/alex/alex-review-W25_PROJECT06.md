# Peer Review: W25 Project 06 — Investigating Hungarian Chickenpox Infections

## Overview

This project applies three modeling approaches to weekly chickenpox case counts in Hungary (2005–2015): an ARMA benchmark, a seasonally forced SEIR model under the POMP framework, and a VMD+N-BEATS deep learning pipeline. The ambition to compare mechanistic, statistical, and machine learning methods is commendable. However, the POMP model contains several implementation errors that undermine the validity of the inference results, and the cross-model comparison suffers from methodological inconsistencies. Issues are ordered from most to least critical.

---

## Weaknesses

### 1. [Critical] Incidence Accumulator Tracks Wrong Compartment — NewEI Is Not Weekly Incidence

The C snippet increments `H` with `dN_IR` (I→R recoveries) and sets `NewEI = dN_EI` at every sub-step:

```c
H += dN_IR;
NewEI = dN_EI;
```

Because the Euler discretization uses `delta.t = 1/7`, there are seven sub-steps per observation week. `NewEI` is overwritten at each sub-step and holds only the E→I transitions from the *last* sub-step when `dmeas`/`rmeas` are evaluated. This systematically underestimates weekly new infectious by a factor of roughly seven. The standard approach is to accumulate E→I transitions in a counter (e.g., `H += dN_EI`) that is reset to zero after each weekly measurement, as done in canonical measles/chickenpox POMP implementations. The observed consequence — implausibly large Beta estimates (83–748) and near-unity rho — is consistent with the model compensating for this undercount.

---

### 2. [Critical] `emeas` Uses Cumulative Recovery Counter, Inconsistent with `dmeas`/`rmeas`

```r
emeas <- Csnippet("E_infection = rho * H;")
```

`H` accumulates I→R recoveries and is never reset, so it grows monotonically throughout the simulation. `dmeas` and `rmeas` correctly use `rho * NewEI` for the per-week measurement distribution, but `emeas` returns an expected value that grows without bound. This makes the expected-value calculation (used for simulation overlays) meaningless and represents an inconsistency in the measurement model specification.

---

### 3. [Critical] Model Is SEIRS but Described Throughout as SEIR

The C snippet includes waning immunity (`dN_RS = rbinom(R, 1 - exp(-omega * dt))`), making this an SEIRS model. Every section header, equation block, and narrative description calls it "SEIR." No discussion of waning immunity appears in the biological motivation. This labeling error propagates through the entire POMP section and obscures the actual model structure from the reader.

---

### 4. [Critical] Population Size N Is Incorrect for a National Model

The model fixes `N = 2267000`, approximately 23% of Hungary's ~10 million population, for data that aggregates all 20 counties and Budapest. No justification for this value is provided. Because transmission scales as `Beta * I / N`, an underestimated N inflates the effective transmission rate. The global search recovers Beta values of 83–748, compared to the starting guess of 15, consistent with this compensatory inflation. All epidemiological rate estimates derived from this model are therefore biased.

---

### 5. [Major] Seasonality Amplitude `amp` Is Unconstrained in the Local `mif2` Call

The `pomp()` object specifies `logit = c("eta", "rho", "amp")` in `partrans`, correctly constraining `amp` to (0, 1) in natural scale. However, the `mif2` call inside the local-search `foreach` loop overrides `partrans` with:

```r
partrans=parameter_trans(log=c("Beta", "mu_EI", "mu_IR", "k"), logit=c("eta", "rho"))
```

`amp` is absent from the `logit` list. As a result, `amp` is treated as an unconstrained real number during optimization, and the recovered natural-scale values range from 2.12 to 2.81 in local search and 1.12 to 1.76 in global search — all greater than 1. With `amp > 1`, the seasonal forcing term `Beta * (1 + amp * cos(...))` goes negative during the cosine trough and is hard-clamped to zero via `if (Beta_t < 0) Beta_t = 0`. This converts seasonal modulation into a periodic complete shutdown of transmission, which is biologically untenable and different from the cosine-forcing model described in the text.

---

### 6. [Major] Written Model Equations Include Terms Not Implemented in Code

The differential equation section documents:
- A birth term `mu * N` and death term `mu * S` in the dS equation,
- A death term in dE (`-mu * E`),
- An importation term `lambda` in dI.

None of these terms appear in the C snippet. The code contains no `mu` parameter (distinct from `mu_EI`/`mu_IR`) and no `lambda`. This discrepancy means the model described mathematically differs from the model actually estimated.

---

### 7. [Major] "Profile Likelihood" for rho Is a Scatter Plot, Not a Profile

The profile likelihood section filters global search results by log-likelihood and plots `rho` vs. `loglik`. This is a marginal scatter plot of global search output, not a profile likelihood. A proper profile fixes `rho` at a grid of values, re-runs `mif2` optimizing all other parameters at each fixed value, and reports the optimized log-likelihood. Additionally, the confidence interval threshold used is `maxloglik - 4`, whereas the correct 95% threshold from the chi-square(1) distribution is `maxloglik - 1.92`. The looser cutoff (about 2x too wide) is acknowledged in a code comment but not corrected. With only 3 global search points within even the relaxed cutoff, the reported rho CI is statistically meaningless.

---

### 8. [Major] Cross-Model Comparison Is Not Methodologically Equivalent

The deep learning model uses VMD features derived from all 20 county-level time series (1220 features total), while ARMA and POMP operate on aggregated national data only. The MAPE of 2.5% for NBEATS versus 36.8% for ARMA is presented as evidence of deep learning superiority, but the models are not competing on equal information. A fair comparison would require either applying ARMA and POMP to county-level data or restricting the deep learning model to national-aggregated inputs.

---

### 9. [Major] VMD Decomposition Uses the Full Dataset Including the Validation Period

In `model.ipynb`, `VmdTransformer` is fitted on the complete 522-week series before any train/validation split:

```python
transformer = VmdTransformer(K=K)
df_vmd = transformer.fit_transform(df)  # full dataset
```

The resulting VMD modes — which are used as exogenous features for NBEATS — encode information from the last 100 weeks designated as the validation set. This constitutes feature-level data leakage. The reported 2.5% MAPE on the validation set is therefore optimistic and does not reflect genuine out-of-sample performance.

---

### 10. [Minor] ARMA Model Ignores 52-Week Seasonality

The AIC table covers only non-seasonal ARMA(0:4, 0:4). Given that the data exhibits a prominent annual cycle (clearly visible in the time series plot), a seasonal ARIMA (SARIMA) with period 52, or at minimum a model that accounts for the seasonal component, should be considered. The near-unit-circle AR root (modulus = 1.0008) in the fitted ARMA(4,4) is also consistent with unmodeled seasonality driving the AR polynomial toward a near-unit root.

---

### 11. [Minor] ARMA Forecast Accuracy Is Evaluated In-Sample Only

All RMSE, MAE, and MAPE statistics for the ARMA model use fitted values from the full 522-week series. No train/test split is performed. The 36.8% MAPE therefore reflects in-sample fit, not forecasting ability, making the comparison with the deep learning model's validation-set MAPE inconsistent even beyond the information-asymmetry issue noted above.

---

### 12. [Minor] Log-Likelihood Standard Error Filter Is Too Permissive

Both the local and global search results are filtered with `loglik.se < 10`. Several local search runs have `loglik.se` values of 0.63, 1.31, and 0.98 — indicating substantial particle-filter instability. The conventional threshold in POMP practice is `loglik.se < 1` (or more conservatively `< 0.5`). Retaining high-se estimates inflates apparent parameter uncertainty and can misrepresent the log-likelihood surface.

---

### 13. [Minor] `start_params` Undefined in Local Search Code

The `foreach` loop in the local search chunk calls `mif2(..., params = start_params)`, but `start_params` is never defined in the visible code. It appears to default to the parameters embedded in `chickenSEIR`, but this is implicit and non-reproducible without the reader tracing through the pomp object initialization.

---

### 14. [Minor] Duplicate `library(pomp)` Call

The setup chunk at the top of the Rmd contains `library(pomp)` on two consecutive lines. While harmless, this suggests the document was not carefully proofread.

---

### 15. [Minor] Beta Range in Global Search Is Implausibly Wide and Unexplained

The global search recovers Beta estimates spanning 83–748, far from the initial guess of 15 and the biologically interpretable range for varicella. This range is reported in the results data frame but never discussed in the text. Given the confounded N and unconstrained amp issues noted above, these estimates are likely artifacts rather than meaningful epidemiological quantities. The paper would benefit from explicitly acknowledging this and interpreting the estimates cautiously.

---

## Summary

The project's strongest contribution is the comparative design spanning three model classes. The deep learning section is well-implemented modulo the VMD leakage issue, and the ARMA section follows standard practice. The POMP section, however, contains overlapping implementation errors — particularly the NewEI accumulation error and the unconstrained `amp` parameter — that collectively invalidate the quantitative inference results. Fixing these would require re-running all searches but would substantially improve the mechanistic modeling contribution.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project06/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project06/data/chickenpox.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project06/data/chickenpox_raw.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project06/results_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project06/local_loglikes_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project06/mifs_local_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project06/model.ipynb`
