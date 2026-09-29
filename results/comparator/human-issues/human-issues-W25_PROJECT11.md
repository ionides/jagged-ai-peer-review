# Human Issues — W25 Project 11

1. Are the GARCH quantities called "likelihood" actually likelihoods or just something similar? See Quiz 2, Q12-02.

2. "despite having the lowest log-likelihood, sGARCH-norm achieves the lowest AIC due to its simpler structure": this doesn't look right, because 30 units of log likelihood would require an additional 30 parameters if it is not to have a higher AIC.

3. The t distribution can be used for stochastic volatility models just as readily as for GARCH models. It is good for non-mechanistic and mechanistic models to challenge each other for new ideas. But, the insights from them can and should be included in the mechanistic models.

4. The conclusion, "ARMA modeling is crucial for capturing autocorrelation structures in financial time series" is not clearly supported. Essentially no autocorrelation is found, and then the analysis moves on to GARCH models which assume the autocorrelation is zero.

5. Most of this project could have been done as a midterm project. There are many past midterm and final projects doing similar things, so the analysis is quite routine. The stochastic volatility part is not well developed: an existing model is used, and weaknesses are not fixed.

6. Although the author acknowledges the poor convergence in the local search, they have decided to use 1000 particles with 50 iterations. Maybe it's worth trying more particles and more iterations (something like 5000 particles and 100 iterations). This way, they may be able to see if it's the problem with particle filtering or if there is model misspecification.

7. Fig 3.1 has a caption "density of gold prices". Also, a histogram of marginal values of a time series is usually not a good idea. When the time series has a trend, it is an especially poor choice.

8. The sample ACF of index prices is uninformative. This plot estimates autocorrelation for a stationary time series, but the time plot (and common knowledge of investments) suggests that it is close to a random walk, which is non-stationary.

9. The reason given for choosing ARMA(1,1) is parsimony, but (1,0) and (0,1) have better AIC and more parsimony.

10. Quite a long time is spent on ARMA considering that it gets discarded in favor of better models.

11. The team decided to use the close price rather than the adjusted close price. On August 28, 2020, a stock split occurred, which would cause the raw close price not accurately to reflect market fluctuations. The report's observation that "a major shift occurred in 2020, marked by a rapid surge in prices and increased volatility" is likely due to the use of the raw closing price as affected by the stock split.
