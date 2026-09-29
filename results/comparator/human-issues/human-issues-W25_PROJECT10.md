# Human Issues — W25 Project 10

1. The mechanistic model falls quite a long way short of the non-mechanistic benchmarks (ARMA and plain regression), indicating problems with the model. More diagnostic plots are needed to explore why the proposed dynamic model structure is not fitting well, for example looking at the likelihood anomalies as in Chapter 18 (the measles case study).

2. The decreasing log-likelihood with iteration is an indication of model misspecification. The proposed solution to use more particles or reduce random walk step size will not help — the problem is exactly that as the random walk step size reduces, the model no longer fits so well.

3. The report does not place the project securely into the context of other 531 projects or a broader literature. The topic is original, but the report should say this, and the team should say what they learned from previous projects, as requested in the assignment description.

4. When AIC suggests a very large ARIMA such as (5,1,6), the data are sometimes indicating a need to think of alternative model specifications — for example, fitting a trend.
