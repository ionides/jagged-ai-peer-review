# Peer Review: "To The Moon or Not - Analysis on GameStop Stock Price"
**Semester:** Winter 2021 | **Project:** 06

---

## Summary

This project applies ARMA, GARCH, and a POMP stochastic volatility (leverage) model to daily GameStop (GME) log-returns over April 2020 – April 2021. The Breto (2014) leverage model is implemented in pomp and fit via iterated particle filtering (MIF2), with local and global searches. The final conclusion ranks the POMP model highest by AIC. While the topic is interesting and the overall pipeline is recognizable from course materials, the project has substantial methodological, statistical, and presentational weaknesses detailed below.

---

## Weaknesses (most critical first)

### 1. [MAJOR] Near-verbatim replication of course slides with minimal adaptation

The POMP section is copied nearly line-for-line from the course lecture slides (Chapter 16). Variable names (`GME_statenames`, `GME_rp_names`, parameter names, Csnippet code, `stew` filenames, random seeds) all mirror the slide examples with only the ticker symbol changed. There is no evidence that the authors critically evaluated whether the model is appropriate for GME's extreme, short-lived spike, or that they adapted the model in any meaningful way. The code comments themselves say "reference from https://ionides.github.io/531w21/16/slides-annotated.pdf" repeatedly with no original contribution.

### 2. [MAJOR] Global search box is poorly motivated and inconsistent with local search results

The global search box for `mu_h` is set to `c(-1, 0)`, but the local MIF2 search consistently converges to values around `-5.1` to `-5.3` (visible in `GME_params.csv`). This means the global search box does not contain the region where the likelihood is actually maximized, severely undermining the purpose of the global search. A proper global search must cover the region of interest, including the locally-found optimum. The final conclusions therefore cannot be trusted to reflect the true global maximum.

### 3. [MAJOR] AIC comparison between ARMA, GARCH, and POMP is statistically invalid

The authors compare AIC scores across ARMA, GARCH, and POMP models as if they are on the same footing. However:
- ARMA is fit to `log_diff` (log-returns) while GARCH and POMP are also fit to demeaned log-returns (`demean_price`), creating an inconsistent baseline.
- GARCH AIC is computed via `tseries::garch`, which uses a different likelihood convention (conditional likelihood, dropping the first observation) from the POMP particle filter likelihood.
- The POMP log-likelihood is a stochastic estimate with non-trivial Monte Carlo error, yet it is compared as a deterministic number to exact GARCH/ARMA likelihoods.
- These three AIC values are not comparable on the same scale and ranking them to declare POMP the winner is methodologically unsound.

### 4. [MAJOR] No global search diagnostic convergence plot interpreted correctly; non-convergence largely ignored

The local MIF2 diagnostic plot (`plot(if1)`) explicitly shows `H_0` and `sigma_nu` failing to converge, and the authors acknowledge this. However, the paper then proceeds to declare the POMP model a success in the conclusion without resolving or adequately investigating the non-convergence. Non-convergence of initial conditions and noise parameters is a serious problem for inference. The offered "easy solution" of more iterations is speculative and is not demonstrated.

### 5. [MAJOR] Particle filter log-likelihood is used as a point estimate without acknowledging Monte Carlo error

The reported POMP log-likelihood of 239.8 (local) and ~239.3–239.7 (global, from `GME_params.csv`) is a stochastic estimate. The standard errors from `logmeanexp(..., se=TRUE)` are reported in the CSV (column 2: ~0.05–0.10) but are never discussed in the text. The AIC of -466.6 is computed from a noisy likelihood estimate without any acknowledgment that the AIC itself has Monte Carlo uncertainty. This uncertainty should be quantified and discussed, particularly when comparing to GARCH AIC differences of similar magnitude.

### 6. [MAJOR] ARMA residual ACF shows significant autocorrelation but this is not investigated

The authors note "there are significant correlations at several different lags" in the ARMA(1,3) residual ACF and suggest adding seasonality, but daily stock log-returns have no obvious seasonal structure. The authors do not investigate whether the significant ACF lags are driven by volatility clustering (which is precisely what GARCH/POMP address). No formal Ljung-Box test is performed. The residual analysis is superficial.

### 7. [MAJOR] GARCH(4,2) is selected without proper justification; AIC comparison is inconsistent

The AIC table for GARCH starts at `p=1`, so GARCH(1,1) cannot be compared to lower-order models using the table. More critically, the authors claim GARCH(4,2) improves log-likelihood from 203.44 to 228.44 (a gain of 25 units with 4 extra parameters), which would strongly favor GARCH(4,2) by AIC (-442.88 vs. -400.89), yet the text dismisses this by saying "they should be approximately the same under the AIC criterion." This is incorrect: the AIC difference of ~42 units is enormous and strongly favors GARCH(4,2). The dismissal without any calculation undermines the model comparison section.

### 8. [MINOR] The simulation comparison plot text does not match the code

The prose on line 343 states: "The plot of simulated returns versus observed returns are shown above." However, the plot comes *after* this sentence in the code (the `plot(...)` chunk is below). This indicates the narrative was written without careful attention to code flow, creating confusion for the reader.

### 9. [MINOR] `GME_rproc.filt` uses `covaryt` but the covariate table setup is fragile

The filter rprocess uses a covariate `covaryt` that includes a leading `0` for time `t0=0`. This is a common pattern from course notes but the authors do not verify that the covariate alignment is correct for their specific data (which has 252 trading days). There is no documentation of this design choice or verification that it produces sensible filtered estimates.

### 10. [MINOR] No likelihood ratio test between nested models

The fixed-leverage model (setting `sigma_nu = 0`) is a special case of the stochastic leverage model. The authors mention this in passing but never formally compare the two with a likelihood ratio test or even report the fixed-leverage log-likelihood. This is a natural and straightforward diagnostic that is omitted.

### 11. [MINOR] Pairs plots are shown but not discussed meaningfully

Two pairs plots are included (local and global search results), but neither is discussed in the text beyond minimal mention. For the global search pairs plot, there is no commentary on whether parameters are identifiable, whether there are ridges in the likelihood surface, or whether the spread of estimates indicates a multimodal likelihood.

### 12. [MINOR] The ARMA(1,3) model choice from the AIC table is not the overall minimum

The authors claim ARMA(1,3) has the best AIC (-260.88) and is chosen because it "is surrounded with a neighborhood of good AIC scores." However, the AIC table is not shown to the reader in the Rmd output (just a `kable` call without inline values in text). The criterion for selecting a model that is "surrounded by good scores" rather than the global minimum is not justified, and the neighborhood criterion is subjective.

### 13. [MINOR] The data covers an anomalous event (short squeeze) without special modeling treatment

The authors identify that GME underwent an extraordinary short squeeze in January 2021, yet they apply a standard stochastic volatility model without any structural break, regime-switching, or heavy-tailed observation noise. No consideration is given to whether the Gaussian observation model `Y_n ~ N(0, exp(H_n/2))` is appropriate for returns that reached +134% in a single day. The heavy tails in all Q-Q plots are symptomatic of this misspecification but are not acted upon.

### 14. [MINOR] Conclusion misstates log-likelihood values and is internally inconsistent

The conclusion section states: "The ARMA(1,3) model gives loglikelihood of 136.44 with AIC score of -262.88." But the AIC table in the code reports -260.88 for ARMA(1,3), and the log-likelihood of 136.44 implies AIC = -2*136.44 + 2*5 = -262.88. The AIC value in the conclusion (-262.88) differs from what is stated in the ARMA section (-260.88). This inconsistency suggests the numbers were not checked carefully.

### 15. [MINOR] Heavy reliance on past student projects as references is not fully disclosed

References [4], [5], and [6] cite previous student projects (midterm project 12, final project 23, final project 12 from prior years), and code comments reference these explicitly. While reusing course infrastructure code is acceptable, the extent of borrowing from prior student projects—including the GARCH AIC function and the simulation/filtering workflow—should be clearly acknowledged. The current references do not distinguish between conceptual sources and copied code templates.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project06/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project06/GME.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project06/GME_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project06/Makefile`
