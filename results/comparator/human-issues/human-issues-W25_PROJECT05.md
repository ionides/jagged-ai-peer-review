# Human Issues — W25 Project 05

1. In the conclusion, these two likelihoods are improperly compared: "as seen in the difference in likelihoods between the SARIMA model (-96) and the POMP models (-328), there is a significant scope for improvement in the mechanistic models." The SARIMA is fitted to the log of the data, and not adjusted for the transformation.

2. The STL decomposition is informative here, unlike various other epidemic time series. Here, it is not necessary to take logarithms to linearize the dynamics, because this low-prevalence situation (in US, malaria does not spread effectively) is already close to linear, additive dynamics.

3. One could consider detrending rather than concluding "differencing the series will be advisable and possibly needed."

4. Using a periodogram to infer seasonality is overkill. If the periodogram does not show anything surprising (often the case) you don't have to claim that you use it to infer annual seasonality.

5. SARIMA model AIC comparison does not take into account the loss of a datapoint when differencing; AIC is not perfectly comparable.

6. The SARIMA residual diagnostics show a good fit. The report does not explain clearly that this is fitted to the log of the data.

7. It would be nice to have the Jacobian correction so that the SARIMA log-likelihood for log-data can be properly compared to the POMP log-likelihood for the raw data.

8. Two log-likelihoods claimed to both equal -332.02 are neither equal to -332.01 (they are -331.077 and -331.386). A strange typo, but fortunately these likelihoods are indeed close.

9. Rainfall data could be very helpful as a covariate given the known ecology of the mosquito vector. Including that is beyond the expected scope for a good 531 project.
