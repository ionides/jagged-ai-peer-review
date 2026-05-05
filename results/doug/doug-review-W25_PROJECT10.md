# Peer Review: W25 Project 10
## Daily Environmental Noise and Heart-Rate Variability

---

## Summary

This project fits a linear-Gaussian POMP model to a proprietary Apple Inc. dataset of daily population-level SDNN (heart-rate variability) in order to quantify the same-day effect of environmental noise (Leq) on HRV, with physical activity (Energy) as a covariate. The model formulation is clear and the use of MIF2 for inference is appropriate for the problem. However, the project has serious computational and statistical inadequacies: the global search is both misconfigured and dramatically underperforms the local search, the ARIMA likelihood comparison is invalid due to the differencing mismatch, profile likelihoods and parameter identifiability analyses are entirely absent, and reproducibility is severely compromised because the underlying data cannot be shared and the HTML was captured as screenshots within a VDI environment. The scientific conclusions about the noise-HRV relationship are therefore not adequately supported by the analysis as currently presented.

---

## Major Issues

### 1. Global Search Dramatically Underperforms the Local Search — Global MLE Is Unreliable

The local search reports a best log-likelihood of approximately -3235, while the global search reports -7936. This is a gap of more than 4700 log-likelihood units — far beyond any plausible Monte Carlo error. Per the `pomp-global-search-box-misalignment` skill, when the global search best log-likelihood is substantially below the local search best, the "global" coverage is invalid and the reported global maximum does not represent the true global MLE.

The global search box for `sigma_proc` uses `lower = 0`, which corresponds to near-zero process noise, while the local search converged to `sigma_proc` pushing toward zero anyway. However, the global box for `a` spans `[-0.5, 0.5]`, and `d` spans `[40, 50]` — both ranges that may not bracket the local MLE. The global search uses only Nmif=150 iterations and Np=2000 particles for 96 guesses, which is a significantly reduced computational effort compared to the local search (Nmif=300, Np=5000). The text acknowledges that the global search "produced an even wider range of sub-optimal values," but does not treat this as the methodological failure it represents. Instead the author proceeds to use the global search paired scatter plot for near-profile diagnostics without acknowledging that the global results are systematically biased. The fix is to (1) re-center the global search box on the local-search MLE with wider margins, (2) increase Np and Nmif to match the local search, and (3) re-examine the pairs plot only after the global search max approaches the local-search max within 2-3 units.

### 2. Invalid Log-Likelihood Comparison Between the ARIMA and POMP Models

The paper reports the ARIMA(5,1,6) log-likelihood as -2591 on the first-differenced series, and the POMP model's best log-likelihood as -3235 on the original SDNN series. From this the conclusion is drawn that the POMP model fits poorly relative to the ARIMA benchmark.

This comparison is invalid. The ARIMA model is evaluated under a Gaussian distribution on the once-differenced SDNN series (d=1), while the POMP model is evaluated under a Gaussian measurement model on the undifferenced series. These are different observation models applied to different data transformations; the log-likelihood values are on incomparable scales and cannot be subtracted or ranked. Per the `sarima-baseline-audit` skill, a direct numerical comparison is only valid when both models are evaluated on the same data transformation under the same distributional family. The paper uses AIC to select ARIMA(5,1,6) on the differenced data, then compares its log-likelihood to the POMP log-likelihood on the level data — this is a comparison of apples to oranges. To fix this, either (a) evaluate both models on the same differenced or level series with the same measurement model, or (b) use a proper scoring rule (e.g., CRPS for one-step-ahead forecasts) that is scale-independent.

The AIC comparison in the conclusion ("AIC penalises models only by the number of parameters, so the POMP's much lower log-likelihood translates into a markedly worse AIC than either benchmark") is thus also invalid, as it presumes the likelihoods are on a common scale.

### 3. No Profile Likelihoods — Parameter Identifiability Completely Unassessed

The project presents no profile likelihood analysis for any of the seven parameters (a, b, c, d, sigma_proc, sigma_obs, X_0). From the convergence trace plots in Figure 4, several parameters show clear convergence problems: `a` (autoregressive memory) drifts steadily upward without plateauing, `c` (activity coefficient) remains diffuse with chain-to-chain dispersion, and `sigma_proc` and `sigma_obs` show a strong trade-off pattern. The text acknowledges these convergence issues but does not address them with profile likelihoods.

Without profile likelihoods, it is impossible to determine whether any parameter is identifiable from the data, whether the noise coefficient `b` is identified separately from the observation noise `sigma_obs`, or whether the reported point estimates near the MLE represent a well-defined ridge or a flat likelihood plateau. Per Wheeler et al. (2024) and POMP checklist item 5, profile likelihoods and Monte Carlo Adjusted Profile (MCAP) confidence intervals are required for any inference. The author states in the conclusion that the noise coefficient b should "be regarded as exploratory," which implicitly acknowledges unidentifiability but does not quantify it. The fix is to run a profile likelihood for at least b and a (the scientifically focal parameters) over a fine grid with IF2 at each grid point, with the profiled parameter excluded from rw.sd.

### 4. Process-Noise vs. Measurement-Noise Trade-off Indicates Potential Model Misspecification

The convergence traces (Figure 4) show a systematic pattern: chains push sigma_proc toward zero while sigma_obs inflates beyond 1 log-ms unit. The text interprets this as the filter preferring to attribute unexplained variability to measurement noise rather than latent state noise. This is a recognized sign of model misspecification in linear-Gaussian POMP models — when the latent process offers no advantage over a pure measurement-noise model, the optimizer collapses process noise. The model may therefore be functionally equivalent to a linear regression with no genuine latent state, raising the question of why the POMP framework is needed at all.

The author acknowledges this but does not test the nested hypothesis: does a model with sigma_proc fixed at zero (i.e., a pure regression) achieve a similar or higher likelihood than the full LG-POMP? Without this comparison, the claim that the latent-state formulation provides useful structure is not supported. A likelihood ratio test between the constrained (sigma_proc=0) and unconstrained models would directly address this.

### 5. Computational Adequacy — Local Search Convergence is Incomplete

The local search uses 48 chains with Nmif=300 and Np=5000. The log-likelihood trace (Figure 4, loglik panel) climbs steeply in early iterations, peaks near log-likelihood ≈ -2700, then drifts downward to a reported maximum of -3235. The text explains this as characteristic of over-diffuse random-walk perturbations combined with Monte Carlo noise in the particle filter. This is not merely a description — it is evidence that the optimization failed to converge.

When the log-likelihood trace decreases after peaking, the rw.sd values are too large relative to the curvature of the likelihood surface at the true MLE. Per Wheeler et al. (2024) §Computational adequacy, convergence should be assessed by multiple searches reaching similar log-likelihoods, and the traces should show decreasing variance with increasing iterations as the cooling schedule takes effect. None of the 48 chains appear to have reached -3235 from a consistently high plateau. The author identifies the problem (over-diffuse rw.sd) and proposes a fix for future work, but does not actually implement it in the current analysis. The result is that the reported MLE of -3235 may not be near the true MLE. At minimum, a second local search with calibrated rw.sd values should be reported.

### 6. No Benchmark Comparison on a Common Scale

While the paper includes ARIMA and linear regression as "benchmarks," both comparisons are methodologically invalid (see Issue 2). The project does not include any valid benchmark comparison. Per Wheeler et al. (2024) §Benchmark comparison, a mechanistic model should be compared quantitatively against a non-mechanistic benchmark evaluated under the same observation model. A natural valid benchmark here would be a linear regression of level SDNN on lagged Leq and Energy evaluated with the same Gaussian log-likelihood as the POMP measurement model (i.e., computing the log-likelihood of the POMP measurement model at the OLS-fitted regression predictions). Without a valid benchmark, it is impossible to assess whether the latent-state formulation provides any predictive advantage over a simple regression.

### 7. Reproducibility Severely Compromised — Data Cannot Be Shared and Analysis Was Run Behind a Firewall

The data availability statement notes that the underlying data are owned by Apple Inc. and are subject to a data-use agreement that "prohibits external distribution of the raw files or derivative data sets." All analyses were run inside Apple's VDI, and "no direct download or export of data is permitted." The HTML was captured as annotated screenshots from within the VDI.

This means:
- The rendered document cannot be reproduced by any external reviewer or reader.
- The R Markdown source cannot be re-run (data inaccessible).
- No synthetic or anonymized pseudo-data was provided for verification.
- The code cannot be fully evaluated because only screenshot-captured outputs are available, not the actual output.

Per Wheeler et al. (2024) §Reproducibility (POMP checklist item 10) and the code supplement checklist, reproducibility requires that "source code, data, and final parameter values" be publicly archived. None of these are available. This is a fundamental reproducibility failure. While the data constraint is imposed by the data owner and not the author, the project should either use a publicly available dataset or provide a complete synthetic pseudo-dataset that allows all analyses to be reproduced.

---

## Minor Issues

### 8. AIC Grid Search Uses Differenced Data Without Justification for Differencing

The paper differences the SDNN series because Figure 1 shows a "descending trend," and then applies the AIC grid search to the differenced series to select ARIMA(5,1,6). However, the visual trend in Figure 1 is modest and no stationarity test (ADF, KPSS) is reported to justify the differencing decision. The conclusion that "it looks like there is no trend" after differencing is purely visual. If the series is difference-stationary rather than trend-stationary, an ARIMA with d=1 is appropriate; if trend-stationary, an ARMA with a deterministic trend term is more efficient. The choice should be supported by a formal stationarity test.

### 9. ARIMA Model Order Selection: AIC is Applied to the Differenced Series but the ARIMA(5,0,6) is Also Referred to Without Explanation

The AIC table selects ARIMA(5,1,6) (with d=1 implicit from differencing the input), but later the log-likelihood reported uses `arima(d_sdnn_ts, order=c(5,0,6))` — i.e., fitting an ARMA(5,6) to the already-differenced series. The stated model name is ARMA(5,6) but the effective model is ARIMA(5,1,6) on the original series (equivalent). The paper does not clearly distinguish between these representations, which may confuse readers about whether d=1 is applied once or twice.

### 10. Simulation from Initial Guess Shows No Trend — But the Data Exhibits a Clear Downward Trend

Figure 3 shows simulation trajectories from the initial guess centered around the observed SDNN level but with no systematic downward trend visible in the simulations while the data (Figure 1) shows a consistent decline from approximately 37 ms to approximately 28 ms over the study period. This suggests the initial guess for the drift parameter `d` (set to 41) does not approximate the observed trend well, or that the model structure lacks a mechanism to reproduce systematic long-run drift. The author does not address this discrepancy, which deserves at least a brief comment.

### 11. Pairs Plot (Figure 5) Is Based on Global Search Results That Are Invalid

Figure 5 presents a pairs plot of parameter estimates from the global search as a near-profile diagnostic. Given that the global search converged to log-likelihoods around -7936 while the true MLE is near -3235, the parameter estimates in this plot do not represent the likelihood surface near the MLE. The visual inference about identifiability drawn from Figure 5 (e.g., which parameters are well-constrained) is therefore unreliable. The pairs plot should be re-made from a properly converged global search.

### 12. The Conclusion's AIC Comparison Numerically Mixes Values from Incompatible Models

The conclusion states: "Because AIC penalises models only by the number of parameters, so the POMP's much lower log-likelihood translates into a markedly worse AIC than either benchmark." This statement rests on subtracting log-likelihoods computed on different data transformations (differenced vs. level) under different distributional assumptions. The AIC values are therefore not comparable. This statement should be removed or heavily qualified.

### 13. The Linear Regression Benchmark Log-Likelihood Is Computed Incorrectly for Comparison Purposes

The linear regression reports a log-likelihood of -3825. However, `lm()` in R reports the Gaussian log-likelihood under the MLE residual variance. This is on the original SDNN scale with a Gaussian distribution — the same data and the same distributional family as the POMP measurement model. This comparison is actually valid (unlike the ARIMA comparison), but it is not highlighted as such, and the degree-of-freedom adjustment between the two models is not discussed. A proper AIC comparison of the linear regression and the POMP measurement model would be informative.

### 14. Physical Activity Covariate (Energy) Is Dropped Without Analysis

The paper states that "Energy" (active energy expenditure) is included in the model specification and in the covariate table, but the conclusion and the local-search trace plots focus exclusively on the noise coefficient `b` and largely ignore the activity coefficient `c`. The trace plots show `c` to be diffuse and poorly identified. No interpretation of the estimated activity effect is provided in the body of the report. If the author believes `c` is not identifiable or scientifically interesting, this should be acknowledged explicitly; if it is scientifically important (as suggested by its inclusion), it deserves analysis.

### 15. No Out-of-Sample or Forecast Evaluation

The project does not hold out any portion of the data for out-of-sample evaluation. Given that one stated motivation is to understand the predictive relationship between environmental noise and HRV, a brief evaluation of one-step-ahead forecast accuracy (even on a held-out month) would substantially strengthen the scientific case for the latent-state model. Per POMP checklist item 7, forecasts should be generated from the filtering distribution and prediction uncertainty should be propagated.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project10/blinded.pdf` (rendered as page images via PyMuPDF)
