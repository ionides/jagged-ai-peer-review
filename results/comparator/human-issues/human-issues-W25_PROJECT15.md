# Human Issues — W25 Project 15

1. Why is GARCH selected by log-likelihood not AIC? And, are you sure the software is reporting the actual likelihood not some approximation? Quantities called log-likelihood for GARCH software are sometimes not exactly the log-likelihood. It would be worth saying how you know your numbers are correct.

2. Fig. 7 shows long tails, not "adequate except for slight heavy-tail deviations." Trying a t-distributed GARCH would lead to substantial improvement, as the project later finds for stochastic volatility.

3. Note that the GARCH log-likelihoods do not satisfy nesting. Mathematically, e.g., (p,q)=(3,2) includes (3,1) so should not have a lower maximized likelihood.

4. Interestingly, with the t-distribution, the likelihood does not decrease through iterations, at least for the better mode.

5. Various models are investigated, and it would be nice to have more direct comparison. At least, a table with all the likelihoods. Perhaps also some analysis of conditional log-likelihoods at each time point to see which observations the models differ on.

6. "Even though we cannot directly compare loglikelihood from tseries::garch [12], we can still argue that GARCH(3,1) is the most promising one" could be confusing. Is this calculated conditionally on some initial data? It needs explanation to say something is wrong but we use it anyway.
