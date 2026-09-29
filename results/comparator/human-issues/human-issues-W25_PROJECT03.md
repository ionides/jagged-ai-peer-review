# Human Issues — W25 Project 03

1. The conclusion "Our findings have important implications for public health monitoring and intervention planning" is over-stated and not supported by evidence or other lines of reasoning.

2. The phase profile is misinterpreted: "The singleton CI suggests limited identifiability — the likelihood is sharply peaked at one value. This indicates the data contains insufficient information about the seasonal timing." The sharp peak shows very strong identifiability, which might be expected from the known seasonal behavior of flu.

3. The rho profile is misinterpreted similarly. The beta0 profile is described as "smooth and fairly symmetric near the peak" when the plotted profile doesn't seem to have these properties.

4. Data of this kind can be more insightfully plotted on a log scale (presented in the project later). Also, the linear analysis (additive decomposition, periodogram, ARMA) are better on a log scale.

5. Incorrect reasoning: "the ACF plot of the log-transformed data still exhibits a slow decay, indicating that the series remains non-stationary." The usual motivation for the sample ACF assumes a stationary model.

6. The interpretation of ARMA residuals is poor, "the residuals are normally distributed but contain some extreme values." These are far from normal, and the time plot of residuals shows extreme heteroskedasticity. The residual diagnostics are trying to remind the team that they should consider a logarithmic transformation.

7. The ARMA benchmark should be carried out as log-ARMA for situations where ARMA fits better on a log scale, as in Chapter 18 (measles case study).

8. The report acknowledges previous 531 flu projects, but it does not explain its own creative contribution beyond applying similar approaches to a new dataset. There is much room for improving on previous approaches, and your own contribution should be clarified. A new dataset could involve unique modeling and inference challenges that require substantial creativity, but the report does not make that argument.

9. It is not clear what is learned from the additive decomposition that cannot be seen more clearly from other plots. To study seasonality of nonlinear and highly variable systems, a simple line plot of superposed seasonal trajectories can be more informative.

10. For comparing ARMA to SARMA it would be better to use AIC than likelihood, since degrees of freedom differ. Or make a likelihood ratio test using Wilks' approximation.

11. The conclusion "peaks occurring approximately every 60 weeks (around 1.15 years)" is curious. The data are only for about 2yr, so seasonality will not be well identified. But, if it has a relationship with the annual cycle, presumably that would be at a period of 1.0 yr.

12. Sections are numbered, but there are no figure captions or figure numbers.
