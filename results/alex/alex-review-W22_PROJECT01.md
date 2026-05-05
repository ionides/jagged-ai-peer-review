# Peer Review: W22 Project 01
## "Investigation of online player increase in CS caused by COVID-19 Pandemic"

---

## Summary

This project investigates daily CS:GO concurrent player counts from January 2020 to January 2022, framing the player-count log-return as a financial "return" series and applying a GARCH model followed by a stochastic leverage (Breto 2014) POMP model. The motivation is creative, but the analysis contains several critical methodological flaws that undermine its conclusions, particularly in the comparison of log-likelihoods across models, in the naming and implementation of the POMP model, and in the absence of uncertainty quantification.

---

## Weaknesses (prioritized from most to least critical)

### 1. [MAJOR] Incomparable log-likelihoods invalidate the model comparison table

The central conclusion of the paper is that POMP outperforms GARCH, which outperforms ARIMA, based on a log-likelihood comparison table. However, the three log-likelihoods are not on the same scale.

- The ARIMA log-likelihood is computed as `ARIMA515$loglik - sum(log(demean_players))`. Subtracting the sum of log-observations is a Jacobian adjustment intended to convert from a log-scale model to the original scale. This is non-standard and makes the ARIMA log-likelihood incomparable to the others.
- The GARCH log-likelihood (1170.101) is the raw output of `tseries:::logLik.garch`, which operates on the demeaned log-returns directly.
- The POMP log-likelihoods (1277, 1280) are obtained from particle filters on the same log-return series, but the ARIMA model has been differenced (`d=1`), so the underlying observation space differs.

The resulting table claims ARIMA achieves log-likelihood ~1439, POMP ~1280, and GARCH ~1170, and concludes ARIMA "performs the best." This ranking is almost certainly an artifact of the incomparable scales rather than a genuine model comparison.

### 2. [MAJOR] Model is named "Fixed Leverage" but implements Stochastic Leverage

The section heading is "POMP Fixed Leverage Model," yet the model equations and code implement a stochastic leverage model where `G_n` follows a Gaussian random walk (making `R_n = tanh(G_n)` time-varying and stochastic). A fixed leverage model would set `R_n` to a constant. This is a fundamental terminological error that persists throughout the paper.

### 3. [MAJOR] Particle filter uses simulated data instead of real observations for the initial evaluation

In the filtering-on-simulated-data section, `sim1.filt2` is constructed from the simulated object `sim1.sim`, and `pfilter(sim1.filt2, ...)` is run on this simulated object. The resulting log-likelihood of 518.4 is from a filter on simulated data, not on the actual CS:GO data. This number is then cited in the text as an estimate from "our initial guess of the parameters" applied to the player data, which is misleading.

### 4. [MAJOR] No profile likelihood or confidence intervals for any POMP parameters

After global maximization, the paper reports a single maximum-likelihood point estimate (a table of `maxlik`) without constructing profile likelihood confidence intervals for any parameter. This is a standard and expected step in POMP analysis and is absent here. The reader cannot assess parameter uncertainty or whether the model is identifiable.

### 5. [MAJOR] Non-convergence in global search acknowledged but not remedied

The diagnostics text explicitly states: "$\mu_h$, $\phi$, $\sigma_\eta$, $G_0$ and $H_0$ do not converge at all." Given that this encompasses nearly all model parameters, the global search result is not trustworthy as a maximum-likelihood estimate. No follow-up analysis is performed (e.g., increasing `Nmif`, narrowing the search box, or running additional rounds of mif2 from the best points).

### 6. [MAJOR] GARCH model label says "(5,5)" but only GARCH(1,1) is actually fitted

The text declares "we utilize GARCH(5,5)" and the section heading and comparison table label it "GARCH(5,5)." However, the code calls `garch(log_df2$demean_players, grad="numerical", trace=FALSE)` with no `order` argument. The default in `tseries::garch` is `order = c(1,1)`, meaning a GARCH(1,1) is estimated. The mismatch between the claimed and actual model is a significant error.

### 7. [MAJOR] Figure number skips from 5 to 7 (no Figure 6)

Figures are labeled 1 through 5, then jump directly to Figure 7 (fitted vs. observed), with no Figure 6. The simulation comparison plot appearing between Figure 5 and Figure 7 is unlabeled. This numbering gap indicates missing documentation of the simulation diagnostic figure.

### 8. [MODERATE] Applying a financial leverage model to gaming data lacks justification

The leverage effect is a well-defined financial phenomenon: negative returns predict future volatility increases. The paper applies this concept to gaming player counts ("rate of increase as returns"), but provides no domain-specific justification for why leverage would exist in this context. No test of the leverage effect's presence (e.g., sign of the leverage parameter, its statistical significance) is reported.

### 9. [MODERATE] ARIMA model selection ignores the SARIMA result and applies `d=1` without justification

The AIC table shown is `table_sD1` (SARIMA with `D=1`), but the text says "we fix d to 1" without testing whether differencing is necessary (e.g., via an ADF or KPSS test). Furthermore, the SARIMA(5,0,5)(1,0,1)[7] achieves AIC of -2938, substantially lower than the ARIMA(5,1,5) value, but the simpler ARIMA is kept purely on grounds of parsimony without a formal likelihood-ratio test or AICc comparison.

### 10. [MODERATE] Missing values in the dataset are loaded but never documented or handled

The `mice` library is loaded, NA counts are computed, and the raw CSV shows many missing rows in `Players` and `Twitch.Viewers`. However, the NA count is never printed or discussed, and no imputation or removal strategy is described. The reader does not know how many observations are missing or how they are handled before analysis.

### 11. [MODERATE] Legend color mismatch in the final simulation plot

In the simulation comparison plot after global optimization (line 591-594 in the Rmd), the plot draws the simulated series in blue (`col="blue"` in the `plot` call) but the legend labels "Simulated" as red. This is a code error that makes the figure uninterpretable.

### 12. [MODERATE] ARIMA applied to already-demeaned log-differences with additional differencing (`d=1`)

The response variable `demean_players` is `diff(log(Players)) - mean(diff(log(Players)))`, which is already stationary by construction (a centered first difference). Applying `arima(..., order=c(5,1,5))` adds a second round of differencing, yielding an ARIMA(5,2,5) in terms of the original log-player series. This double differencing is not motivated and leads to over-differencing.

### 13. [MODERATE] Twitch viewership data collected but never used

The dataset contains a `Twitch.Viewers` column that is scaled and retained in the data frame but never incorporated into any model as a covariate or analyzed as a secondary time series. Given that streaming viewership is plausibly correlated with player count volatility, this represents a missed analytical opportunity that is not even acknowledged.

### 14. [MINOR] Section "Source" discloses heavy structural borrowing that goes beyond standard citation

The Source section acknowledges that the analysis pipeline before GARCH was borrowed from previous midterm projects, and the POMP section was adapted from a W20 final project. While citation is commendable, the extent of structural copying reduces the originality of the contribution. The adjustments described are minimal ("we simplify the analysis").

### 15. [MINOR] Equation label inconsistency: $R_b$ vs $R_n$

In the model description, leverage is defined as $R_b = \frac{\exp(2G_n)-1}{\exp(2G_n)+1}$, but all surrounding equations use $R_n$ as the leverage variable. The subscript $b$ in the definition of $R$ appears to be a typographical error (likely copied from a reference using a different notation) and should read $R_n$.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project01/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project01/GME_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project01/chart.csv`
