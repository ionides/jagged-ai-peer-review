# Human Issues — W25 Project 14

1. Plotting, ACF, spectral analysis and ARMA are all best done on a log scale. Then, the log-ARMA likelihood needs to be computed with care (see the measles case study in Chapter 18).

2. The project acknowledges building on two previous projects on flu in Oklahoma (W24 #5) and aggregated for USA (W22 #43), and makes a clear statement about how it progresses beyond these previous projects. However, there are other 531 projects on flu with profiles, e.g., W24 #16. Review of past 531 work on flu could have been more complete, but readers were satisfied that this project goes beyond previous work in ways other than just using a different dataset.

3. Formally, it is incorrect to say "a strong autocorrelation at lag one that decays gradually across subsequent lags indicates a non-stationary time series". The usual motivation for the sample ACF assumes a stationary model. The rate of decay in that case just depends on the timescale of dependence.

4. There is some confusion in: "The ODEs can be solved by Euler's numerical method. Specifically, the RHS can be expressed as a binomial approximation with exponential transition probability". The ODE model and stochastic models are different things.

5. The main value of ARMA is probably to provide a benchmark to check when the mechanistic model is becoming well specified. The ARMA likelihood is not discussed in this context (and is not presented, though it can be back-calculated from the reported AIC).
