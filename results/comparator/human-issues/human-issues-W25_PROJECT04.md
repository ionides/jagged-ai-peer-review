# Human Issues — W25 Project 04

1. The introduction is brief and does not outline goals of the project or relevant background information.

2. The interpretation of ARMA residuals is poor, "The residual time series appears centered around zero with no clear patterns." The time plot of residuals shows extreme heteroskedasticity. The residual diagnostics are trying to remind the team that they should consider a logarithmic transformation. Also, the residuals are long-tailed compared to normal.

3. The roots on, and close to, the unit circle suggest poor stability. Thus, the conclusion that "the roots confirm stationarity and invertibility" is weak. There's no point looking at diagnostic plots if you ignore what they are telling you.

4. The ARMA benchmark should be carried out as log-ARMA for situations where ARMA fits better on a log scale, as in Chapter 18 (measles case study).

5. It is hard to interpret the value of a log-likelihood as an argument for or against the model; usually, log-likelihood is useful only to compare models. Thus, there is weak reasoning in the conclusion: "Given the relatively large sample size and the complexity of the data (confirmed, recovered, and deceased cases), this log-likelihood value suggests that the VAR(9) model provides a reasonable fit to the data, capturing the main dynamics without overfitting."

6. The Fig 5 residual plot is showing the log-scale variation that is reminded to use a logarithmic transformation of the data. The explanation of this figure as "no clear patterns, although some variance increases during peaks" makes two incompatible points; first saying there is not a pattern and then identifying one.

7. The report references a previous project that was influential for their analysis. The report could do a better job explaining explicitly what they learned from that project and what their own creative innovations were. This project made plenty of its own contributions, but the reader should not have to go to past projects to assess this.

8. Innovative use of a vector autoregressive (VAR) model. However, it is not clear how this supports substantial conclusions.

9. Erratic use of boldface makes the text harder to read.

10. Incorrect reasoning: "The ACF and PACF plots for confirmed, recovered, and deceased cases show strong autocorrelation and slow decay, indicating non-stationarity and the need for differencing". The usual motivation for the sample ACF assumes a stationary model. Also, differencing is only one way to build a non-stationary model.

11. Fig 1 needs a different scale for deceased. That line is not legible in its current form.

12. ARIMA(5,1,5) is a large model, but also it is not the model with lowest AIC. How about ARIMA(1,1,3) or (1,1,4)?

13. VAR is described as "more transparent" and "easier to interpret". Yet, no useful interpretation of this model is provided.

14. VAR diagnostics show longer than normal tails. A time plot (not shown) would also reveal heteroskedasticity.

15. "The fitted values closely capture the major trends and variations in the data, supporting the use of the VAR model for analyzing the dynamic relationships between these pandemic variables." Authors should check whether using last week to predict this week is detectably worse.

16. Fig 4 has a typo in the time axis (it runs 2024 - 2041).
