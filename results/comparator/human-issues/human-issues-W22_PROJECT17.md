# Human Issues — W22 Project 17

1. The conclusion that the sample ACF "indicated dependencies between the data" does not add much to the timeplot. Also, differencing is used as a way to make a stationary model more suitable, which is not quite the same thing as dependence.

2. "4 of the AR polynomial roots are inside the unit circle and one of the MA polynomial roots are inside the unit circle" does not seem to match the figure. Also, the figure shows inverse roots so they should be inside for invertibility and causality.

3. "most of the residual values stay close to the horizontal line y=0" suggesting a good fit of our model" is not a warranted conclusion. The residuals show heteroskedasticity and/or long tails, with some autocorrelation. Residuals are centered on zero by construction.

4. Probably, ARMA modeling on a log scale would fit better.

5. I(0)=270000 is a very large number of initial infected individuals. This is fixed in the code, rather than being estimated, which could cause problems with fitting other parameters.

6. The strong weekly cycle is not in the SEIR model. One could model weekly totals to avoid dealing with day-of-week effects.

7. Likelihoods are not quite comparable before and after differencing. This could explain all or some of the difference between the SARIMA and SEIR log likelihoods. Note that SEIR beats the ARMA likelihood.

8. The source of the data is unclear. The Kaggle link provided refers to something not updated since 2020-07-27. The authors say "the beginning of the pandemic in the US, 2021 June 5st" but that is not when the pandemic began. It is a reasonable date for the arrival of the delta variant, but the project makes no mention of this variant.

9. The model, with time-varying beta, made more sense in the analysis of a prior project which this project closely follows. At that time, the dynamics were driven by initial spread and social distancing interventions. More recently, variants and vaccination have been more critical.

10. There is a sign mistake in the Binomial transition probability expression which may have been inherited from a prior cited project. It is okay to borrow from cited past projects, but one should borrow critically.
