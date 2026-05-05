# Peer Review: W22 Project 01
**Title:** Investigation of online player increase in CS caused by COVID-19 Pandemic

---

## Summary

This project investigates whether COVID-19 affected the number of online CS:GO players by treating the log-return series of daily player counts as a financial-returns-style time series and applying GARCH and stochastic volatility (leverage) POMP models. The authors fit an ARIMA(5,1,5) benchmark, a GARCH(1,1) model (labelled GARCH(5,5) in the text but fit with default `garch()` arguments), and a stochastic leverage POMP model adapted from course notes, then compare log-likelihoods. While the project demonstrates familiarity with the `pomp` workflow, it suffers from a fundamentally mismatched research question and modeling strategy, several outright numerical errors in the likelihood comparison table, no profile likelihood or confidence intervals for any parameter, and an incorrect log-likelihood adjustment for the ARIMA model. The conclusion that ARIMA outperforms the POMP model on log-likelihood is presented without correcting for the scale difference, and the entire framing of using a volatility model to answer a question about COVID-19 effects is not adequately justified.

---

## Major Issues

### 1. Research question and modeling strategy are misaligned

The stated goal is to investigate how COVID-19 affected CS:GO player counts. However, the authors pivot immediately to modeling the *log-return* series (day-to-day rate of change) with a stochastic volatility / leverage model. Volatility models characterize variance clustering in returns, not level changes or regime shifts attributable to an external shock. No causal or structural link between the COVID-19 pandemic and the volatility of player-count returns is established or even argued. The analysis therefore does not answer the stated research question. A model that addressed level changes (e.g., a SARIMA or SEIR-inspired POMP model of the raw player counts, with a COVID indicator) would be more appropriate.

**Fix:** Either revise the research question to ask "does COVID-19 change the volatility of engagement?" and justify why volatility is the right target, or use a model that directly addresses player-count levels and their relationship to pandemic events.

---

### 2. Incorrect log-likelihood adjustment for the ARIMA model distorts the summary table

In the code, the ARIMA log-likelihood is computed as:
```r
ARIMA515_loglik = ARIMA515$loglik - sum(log_df2 %>% .$demean_players)
```
The `$loglik` component of an `arima()` object in R is already the full conditional log-likelihood for the differenced series; subtracting `sum(log(y))` is not a standard Jacobian correction for the differencing transformation (and the data here are already the *demean-differenced* log-returns, not the raw counts). The reported value of approximately 1439.5 is therefore numerically incorrect and cannot be meaningfully compared with the GARCH or POMP likelihoods. This error directly corrupts the conclusion table and the final conclusion that "ARIMA performs best." (Error 2.9 in the weakness reference: trusting software output without checking conventions.)

**Fix:** Report `ARIMA515$loglik` directly as the model's log-likelihood and note that it is the conditional Gaussian log-likelihood for the differenced series, comparable on the same observed data as the GARCH and POMP values.

---

### 3. No profile likelihoods or confidence intervals for any parameter

No profile likelihood is computed for any of the six POMP model parameters, and no confidence intervals are reported. The conclusion that the stochastic leverage model provides a good fit rests entirely on the point estimates from global search, with no assessment of identifiability. The pair plots show that parameters such as `sigma_nu`, `G_0`, and `H_0` are poorly identified (they spread widely in the pair plot even after filtering to runs within 10 log-units of the maximum), yet no formal identifiability analysis is performed. (POMP checklist item 5; weakness reference Error 1.9.)

**Fix:** Compute profile likelihoods for at least the key parameters (`phi`, `mu_h`, `sigma_eta`) and report 95% confidence intervals via the Wilks threshold.

---

### 4. Global search convergence is not achieved; conclusion drawn from non-converged results

The authors explicitly acknowledge: "From diagnostics plots above, we see that: mu_h, phi, sigma_eta, G_0 and H_0 do not converge at all." Despite this, they report the maximum log-likelihood of 1280 from the global box search and include it in the summary table as if it were a reliable estimate. When five of six parameters fail to converge, the reported likelihood is not a trustworthy MLE. (Weakness reference Error 1.8; POMP checklist item 6.)

**Fix:** Increase computational effort (more iterations, wider box, or longer cooling) until convergence is demonstrated, or explicitly qualify all conclusions as preliminary due to non-convergence.

---

### 5. GARCH model mislabeled and log-likelihood potentially affected by non-standard normalization

The report states "GARCH(5,5)" in the text and equation, but the code calls `garch(log_df2$demean_players)` with no `order` argument, which fits the default GARCH(1,1). The log-likelihood of 1170.101 is attributed to "GARCH(5,5)" — a model that was not actually fit. Additionally, `tseries::logLik.garch` is known to report a non-standard normalization (it may omit a constant or normalize differently from other packages). The summary table thus compares an incorrectly labelled model's likelihood against the POMP likelihood without verifying that the normalization conventions are consistent. (Weakness reference Error 2.9.)

**Fix:** Confirm the GARCH order actually fit, report the correct model name, and verify that the log-likelihood normalization is consistent with the other models being compared.

---

### 6. No benchmark comparison for the POMP model against a non-mechanistic alternative

The ARIMA model is presented as a "benchmark model," but it models the *differenced* log-return series, while the POMP model is applied to the *demeaned* log-return series. These are different observation series, so the likelihoods are not directly comparable (the Jacobian from differencing changes the scale). Furthermore, no IID negative-binomial or simple Gaussian benchmark is computed for the same series as the POMP model to establish a floor for comparison. (POMP checklist item 2; weakness reference Error 1.6.)

**Fix:** Apply all models (ARIMA, GARCH, POMP) to exactly the same observed series and confirm that the likelihood normalizations are consistent before comparing.

---

### 7. Unnecessary differencing of an already-stationary series

The authors compute log-returns (first difference of log players), then apply ARIMA with d=1 (one additional difference). The spectral analysis and ACF of the log-return series show no sign of non-stationarity — the ACF decays quickly and the periodogram shows a clear 7-day cycle but no unit-root behavior. Differencing a stationary series introduces a non-invertible MA unit root and yields a model that is harder to interpret and potentially non-causal. (Weakness reference Error 2.1.)

**Fix:** Fit ARMA (with d=0) directly to the log-return series, incorporating the weekly seasonal component via SARMA. Use d=1 only if a unit-root test on the log-return series supports it.

---

## Minor Issues

### 8. SARIMA comparison abandoned without full justification

The authors state "the most competitive SARIMA model gives lower AIC than ARIMA(5,1,5)" and then select ARIMA(5,1,5) as the baseline because "the ARIMA model is relatively simple." A SARIMA model with lower AIC should be preferred, not discarded for simplicity without a principled argument. The AIC table for SARIMA(3,0,5)(1,0,0)[7] is shown but not the final selected SARIMA, making the comparison non-reproducible. The stated rationale contradicts the principle of AIC-based model selection.

---

### 9. No simulation-based goodness-of-fit diagnostic for the POMP model

The only model diagnostic for the POMP leverage model is a single forward simulation (from initial guess parameters) overlaid on the observed returns. No simulation from the MLE parameters with replicated trajectories is shown. No effective sample size (ESS) profile or conditional log-likelihood plot is presented. (POMP checklist item 3 and 4.)

---

### 10. H_0 non-convergence not adequately addressed

The trace plot from the local search (Figure shown via `plot(if1)`) is described as showing that `H_0` does not converge. The authors use this as motivation for the global search, but the global search trace plot (`plot(if.box)`) also shows non-convergence for multiple parameters. This is noted briefly but dismissed without further action. If `H_0` is a poorly identified initial condition, fixing it or profiling over it would be appropriate.

---

### 11. Summary table values are inconsistent with the code output

The conclusion section table lists POMP with fixed values as log-likelihood 1277 and POMP with randomized values as 1280. The local search (`summary(r.if1$logLik)`) reports a best of approximately 1277, and the global search (`summary(r.box$logLik)`) reports a maximum. However, the CSV file shows values ranging up to approximately 1276.8, making the stated "1280" appear rounded or taken from a different run. The exact source and reproducibility of the 1280 value should be clarified.

---

### 12. Causal language used without causal identification

The introduction and conclusion use language like "COVID-19 affects the players" and "quarantine policy... may explain the peak." The analysis is purely descriptive and correlational; no causal identification strategy is employed. (Weakness reference Error 2.10.)

---

### 13. Data subsetting inconsistency

The code applies the rescaling (`Players/1000`) to both `df` and `player_df`, but the spectral analysis and ARIMA modeling are done on `log_df2$demean_players`, which is derived from `player_df` before the rescaling line for `df` is applied. The log-differencing removes the constant factor (log(1000) cancels), so the numerical results are correct, but the code structure is confusing and could lead to errors in future modifications.

---

### 14. Figure 5 label refers to "noice" (noise misspelled) and "circle" (should be "cycle")

The decomposition figure caption reads: "The plots are raw data, trend, noice and circle." These are typos in the caption. Additionally, the STL decomposition variable is named `` `Rate cycles` `` in the code but "circle" in the caption, suggesting a copy-paste error.

---

### 15. Local search uses `sim1.filt` for likelihood re-evaluation but global search also uses `sim1.filt`; the simulation object `sim1.filt2` is constructed but never used in the main inference

The filtering object `sim1.filt2` (which wraps the simulated data) is built in the "Filtering on simulated data" section and used for the initial particle filter check. However, all subsequent `mif2` and `pfilter` calls use `sim1.filt` (filtered on the real data), not `sim1.filt2`. This means the initial particle filter check (loglik 518.4) is evaluated on simulated data, not the actual data — a potentially misleading diagnostic. The distinction between the two objects is never clearly explained in the text.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week9/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week9/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project01/GME_params.csv`
