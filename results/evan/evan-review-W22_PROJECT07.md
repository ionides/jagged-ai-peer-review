# Final AI Review: Volatility Analysis on Ford and Tesla Stock

## Overall Assessment

This paper investigates volatility in Ford and Tesla stock returns using ARIMA, GARCH, and POMP models applied to five years of daily log-returns. The dual-stock comparative structure is a genuine contribution over single-stock analyses, and the t-distributed GARCH section is technically competent, with clear quantitative improvements over normal GARCH and good diagnostic plots. The POMP sections follow the Breto (2014) stochastic leverage model correctly in code. However, the paper contains several substantive errors that affect interpretability: the baseline particle filter is run on a simulated-data object rather than the actual return series, making the reported log-likelihood improvement uninformative; the central comparative claim (POMP outperforms GARCH) is contradicted by the paper's own numbers for Ford; the Tesla prediction figure displays Ford volatility bands due to a variable naming error; and no profile likelihoods or confidence intervals are reported for any POMP parameter. These issues require correction before the paper's conclusions can be trusted.

## Key Strengths

- **Correct likelihood aggregation:** logmeanexp is consistently used across all particle filter replications for both Ford and Tesla, reflecting proper understanding of Monte Carlo likelihood estimation.
- **t-GARCH model selection:** The comparison of normal versus t-distributed GARCH is quantitative and well-supported by both log-likelihood tables and QQ diagnostic plots. The improvement from logLik 3087 to 3189 (Ford) and 2393 to 2485 (Tesla) is credibly attributed to heavy tails in log-returns.
- **Multi-start POMP optimization:** Both local and global searches are conducted with convergence trace plots, demonstrating methodological due diligence.
- **Identifiability acknowledgment:** The paper correctly notes that H_0 and mu_h are weakly identified in both models and appropriately does not treat this as a fatal flaw.

## Major Points

**M1 — Baseline pfilter run on simulated data, not actual returns**

The initial particle filter for Ford reports logLik = −1753.5 (se = 0.22). This is computed on `sim1.filt`, a pomp object constructed from *simulated* data, while the local and global searches optimize on `ford_filter`, which is built from actual Ford returns. The same issue applies to Tesla (baseline −1610.31 on `sim1.filt`, optimization on `Tesla.filt`). The reported "improvement" from negative thousands to positive thousands reflects different underlying data objects, not optimization progress. The baseline comparison is therefore uninformative.
*Severity: Major. Suggested fix: Run the baseline pfilter on ford_filter / Tesla.filt and report those values as the starting-point benchmarks.*

**M2 — Cross-model conclusion contradicted by paper's own numbers**

The conclusion states "The POMP models perform much better than the GARCH for both Ford and Tesla." For Ford, the maximum POMP log-likelihood reported is 3154.3, while the t-GARCH log-likelihood is 3189.5. The t-GARCH exceeds the POMP model for Ford based on the numbers in the paper itself. The comparative claim is at minimum overstated and potentially backwards.
*Severity: Major. Suggested fix: Tabulate all model log-likelihoods using identical data inputs, verify that GARCH and POMP likelihoods are evaluated on the same observations, and revise the conclusion accordingly.*

**M3 — Tesla prediction figure uses Ford volatility bands (code bug)**

In the Tesla GARCH prediction code, lines drawing the green volatility envelope reference `ford_ahead[,2]` rather than `tesla_ahead[,2]`:
```r
lines(tesla_ahead[,1]+ford_ahead[,2], lwd=2, lty=1, col="green")
lines(tesla_ahead[,1]-ford_ahead[,2], lwd=2, lty=1, col="green")
```
Figure 10 therefore shows Tesla's predicted mean return overlaid with Ford's predicted volatility envelope and is uninterpretable for Tesla.
*Severity: Major. Suggested fix: Replace both instances of ford_ahead[,2] with tesla_ahead[,2].*

**M4 — No profile likelihoods or confidence intervals**

Neither the Ford nor Tesla POMP analysis includes profile likelihood computations or confidence intervals for any parameter. The paper qualitatively identifies weak identifiability in H_0 and mu_h from trace plot inspection, but this cannot substitute for quantitative uncertainty bounds. Claims that other parameters (sigma_nu, sigma_eta, G_0) are "well identified" are unverified without profile likelihoods.
*Severity: Major. Suggested fix: Compute profile likelihoods for at least phi and sigma_eta. Use the MCAP procedure or standard profile CI construction.*

**M5 — Measurement model architecture unexplained**

The POMP model sets `rmeasure: y = Y_state` (exact observation, no separate measurement noise) and `dmeasure: lik = dnorm(y, 0, exp(H/2), give_log)`. This means the observation y is perfectly equal to the state Y_state, but the likelihood is evaluated as if y ~ N(0, exp(H_n/2)). This is the correct Breto (2014) architecture — the return is simultaneously observed perfectly and drives the state equation — but this design choice is never explained. Readers cannot assess whether "observation noise" is present or absent, or why the model is structured this way.
*Severity: Major. Suggested fix: Add a paragraph explaining that Y_n is the perfectly observed return that also enters the state transition via the beta term, that there is no separate measurement error, and that the likelihood is evaluated through the filtering distribution of H_n. Cite Breto (2014) explicitly.*

## Minor Points

- **m1 — R_n formula typeset as 1:** The displayed formula R_n = (exp(2G_N)−1)/(exp(2G_N)−1) evaluates identically to 1 for all G_N. The code correctly implements tanh(G), so this is a LaTeX transcription error. Fix: replace with R_n = tanh(G_n).

- **m2 — ARMA AIC table absent from report body:** ARMA results are deferred to the supplementary Rmd. Including the AIC table in the main text — even to confirm ARMA(0,0) is optimal — would contextualize why GARCH and POMP are needed. Negative results are informative.

- **m3 — Global search initializes from local search object:** Both Ford and Tesla global searches run `mif2(if1[[1]], params=apply(box,...))` rather than initializing from the raw filter object with fresh parameters. This may limit global exploration if the local-search object carries internal state.

- **m4 — Inline authoring note not removed:** The phrase "(why we want to use log return instead of return?)" appears in the rendered document at the log-return definition. Replace with a brief explanation or remove.

- **m5 — Ford uses 1000 particles vs Tesla's 2000 at run_level=3:** Ford sets `ford_Np = switch(run_level, 100, 1e3, 1e3)` (capped at 1000), while Tesla uses up to 2000. The uneven computational investment is not discussed and may contribute to the wider spread in Ford log-likelihoods at the 75th percentile.
