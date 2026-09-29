# Human Issues — W22 Project 04

1. Best not to describe weekly periodicity as "seasonality". Outside of the technical use of seasonality in SARMA models, seasonality corresponds to annual cycles.

2. Figure captions would be helpful. For the simulations, the blue line is presumably the data, but this is not described.

3. Diagnostics show a difficulty explaining the resurgence at the end of the data (low effective sample size) but this may not be too critical.

4. The fits around the MLE have a very high reporting rate, close to 1. How do you interpret that?

5. It would be good to compare the likelihood (equivalently, AIC) between the mechanistic model and the ARMA benchmark. In this case, it appears ARMA does somewhat better - maybe showing potential room for improvement in the model.

6. Typo: "$I_t$: the number of recovered at time $t$"

7. Spell checking: e.g., "pubilic", and "casual" for "causal".

8. The plot titled "differenced data" is differenced log data, but the ACF next to it is unlogged data. None of this is apparent unless you study the source code.

9. Referencing observations by date not observation number would be easier to understand.
