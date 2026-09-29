# Human Issues — W24 Project 11

1. The introduction reads like ChatGPT. The conclusion also reads like it has been edited by ChatGPT. A tell-tale sign is sweeping statements made in elaborate language which are not well supported or linked to specific results from the project. According to the rules of the course, ChatGPT is allowed but should be properly attributed as a source.

2. ADF test is not designed for situations with time-varying sample variance, since neither the model used as a null hypothesis, nor the alternative model used to motivate the test statistic, have that feature.

3. Ljung-Box is also of borderline relevance. The null assumes independence, whereas time-varying variance suggests a model should have a lack of independence even if it is uncorrelated — GARCH and stochastic volatility both have that property.

4. The following sentence does not make sense: "Having verified both the stationarity and independence of the data, we can now proceed to the next stage: selecting an appropriate ARMA model." If we really want a stationary, independent model, the only possible ARMA model is ARMA(0,0). Later, the group claim that models which are not independent (e.g., GARCH and stochastic volatility) fit the data better, highlighting the flaw in the reasoning.

5. ARMA(0,0)+GARCH seems to be indistinguishable from GARCH, since there is no ARMA component. So, is the difference only the software used to fit the model? That could use some explanation and investigation.

6. The stated GARCH log-likelihood seems far too high, and is much higher than the stated ARMA(0,0)+GARCH log-likelihood. Such inconsistencies should be noted, and ideally resolved.

7. ARMA(0,0) here is an independent, identically distributed (iid) Gaussian model. It would be helpful to remind the reader of that.

8. The conclusions contain some thoughtful reasoning, but also have logical flaws. The explanation, "This aligns with the efficient market theory, emphasizing the importance of market unpredictability to prevent arbitrage opportunities," is true of stochastic volatility and GARCH as well as an iid model.

9. Since GARCH is white noise (following the definition provided by the group, with white noise interpreted in the weak sense) the ARMA + GARCH model is in fact ARMA, just non-Gaussian ARMA.

10. The authors did not provide the data with their report, so they do not meet the reproducibility expectations for the final project. Also, they have some absolute rather than relative file references.

11. In the "Exploratory Data Analysis" section, authors don't explain the huge jump on 2023/05/25 and its potential influence on their model fitting. As can be seen in their data plot, the close price on 2023/05/24 is 305 and the next day close price increases to 379, which is a considerable surge. This may be the reason for low ESS in their POMP model at time 340 (roughly). In section "POMP Model - Local Search", there is a great decrease in ESS, probably suggesting a bad fit on 2023/05/25.

12. In their GARCH analysis, they find the residuals following a t-distribution are more reasonable, but in their POMP model, they still build the model using normal distribution.

13. In the filter diagnostics that plotted effective sample size and conditional likelihood for the last iteration of their filtering process, there is a clear spike around time 340, as well as a smaller spike around 510. It would have been useful to mention this spike, even if it turns out to be irrelevant in their modeling. Is there something of note that happens around those time points in the data? Or is this something worth adjusting the model to account for?

14. The authors could have benefitted by paying attention to peer review on previous similar projects for this course, e.g., https://ionides.github.io/531w22/final_project/project07/comments.html.
