# Human Issues — W25 Project 17

1. The modification of the SV for t-distributed returns (Sec 2.3) is described as a good decision, but the likelihood improves only a little and the estimated degrees of freedom for tau is quite large, which is surprising and warrants discussion.

2. The effective sample size diagnostics show occasional crashes even with the t-distributed tails, which is somewhat surprising.

3. The report identifies seasonality in gasoline prices, which is interesting, but then ignores this exploratory discovery by proceeding with models that do not include seasonality.

4. Various features of commodity prices are different from stocks — there is no economic principle against commodities autoregressing toward a fair market price or having seasonality, whereas the efficient market hypothesis suggests this is not true for stock market assets. GARCH and many of its generalizations cannot handle seasonality; this might be a case for SARMA with GARCH errors.

5. It would be good to comment on the computational requirements of all these experiments, as fitting POMP models usually requires substantial computation; this would also give insight to people wanting to reproduce the results.

6. This project uses monthly data, whereas volatility models are most commonly developed and used for higher-frequency data.

7. The authors should be more careful about language that may imply causation — the claim that government policies can affect the leverage effect requires more evidence given the complexity of the system.

8. The t degree of freedom parameter tau is described as being in the range [0, 60], but the convergence plots suggest that constraint is not enforced; additionally, tau is often sufficiently large that the t distribution should be very close to normal, which is worth discussion.
