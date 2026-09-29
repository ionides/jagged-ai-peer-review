# Human Issues — W22 Project 23

1. It can be important to estimate the initial value $I_0$ since it can have considerable effect on the dynamics.

2. Likelihood should not be reported to 4 decimal places. 1 or 2 is sufficient.

3. The measurement model for the SEIQR model is curious. Cases are an instantaneous measurement of Q, so individuals in Q can be counted in many measurement intervals (or none at all, if they move quickly out of Q). Generally, one needs an accumulator variable to make a reasonable measurement model.

4. Conclusion: "The log likelihood value of the SEIQR model is the lowest" is a typo, and should read "highest".

5. It would be useful to have ARMA or iid benchmarks. The SIR and SEIR log likelihoods are very low, perhaps suggesting a problem with the model.

6. One problem may be in the measurement models, which have only binomial variability. There is also no process over-dispersion. In the absence of a benchmark likelihood, it is hard to say whether these are fatal flaws.

7. SEIQR has been used in a previous STATS/DATASCI 531 project, but here the development seems to be independently derived from a separate source.

8. The initializer does not quite satisfy the constraint of summing to $N$.

9. In the implementation of the measurement model, the authors manually override the loglikelihood as -1000 whenever the loglikelihood is numerically evaluated as infinite. This requires care since it could hide other problems.

10. The local search suggests an initial susceptible rate $\eta$ from roughly 0.94 to 0.96, and the authors state that the best initial guess of parameters is with $\eta = 0.95$. However, in the global search, the authors used a range of 0.4 to 0.6 for the parameter $\eta$.

11. Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R code.
