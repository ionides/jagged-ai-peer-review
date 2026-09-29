# Human Issues — W25 Project 08

1. The ADF test is not designed to look for non-stationary variance which is the main issue here. The assertion "we reject the null hypothesis of a unit root and conclude that the series are stationary" is a classic example of false reasoning — not all processes without a unit root are stationary. This logical flaw has consequences for time series analysis.

2. There is a weakly supported assertion that the ARIMA(2,0,2) model captures NFLX's complex dynamics and accounts for its volatile behavior. The ARIMA model cannot explain the volatility dynamics.

3. Various ARMA models are fitted, but not compared against the null (white noise). The larger ARMA models probably have roots close to canceling. Log-returns are close to uncorrelated, so for a linear Gaussian model they are inferred (incorrectly) to be approximately independent.

4. The asymmetric t-distribution for GARCH looks like a suitable model, judged by likelihood, but more could be said about contrasting these different models.

5. The claim that "NFLX consistently exhibits higher volatility than SPY, reflecting its sensitivity to company-specific factors compared to the broader market" is questionable — it seems like the aggregate should (almost) necessarily have lower variability, so it is unclear whether this finding is meaningful.

6. Section 7 is unrelated to course material and doesn't contribute to the model development issues in earlier sections.

7. The model fit of the mechanistic and non-mechanistic models could be compared, e.g., by AIC. One can also compare conditional log-likelihoods of individual observations to see in which parts of the dataset the mechanistic hypothesis is (and is not) helpful.

8. Figure numbers and captions would help the reader.

9. All the time spent on ARMA doesn't make much sense given the GARCH and POMP models. Better to spend additional time on those, looking at additional diagnostics for the models of most interest.

10. The identified points with low effective sample size may indicate a longer-tailed distribution is needed to fit the returns.
