# Human Issues — W22 Project 06

1. The analysis is quite similar to the referenced source (project14 from W21). The data are different, but the model and analysis follow a similar trajectory. It would have been better to discuss explicitly the relationship to that previous work.

2. Signs in the "conservation of mass" flow equations are wrong. For example, we should have $S(t)=S(t_0)- N_{SE}(t)$.

3. The report does not describe the measurement model. From the code, one can see that the `dnbinom` specification is incorrect, since it uses a parameterization corresponding to a binomial distribution.

4. The process model does not include overdispersion (as described in Chapter 17) which might cause problems matching the variability in the data.

5. A benchmark (perhaps log-ARMA) would help to establish the goodness of fit of the model, or identify misspecification issues.

6. Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R expressions.

7. In the code, the authors set $E(0) = 14$ and $I(0) = 7$ but did not explain this setting in the report. This may be done to match by eye, but it should be explained and the decision could have consequences for the conclusions.
