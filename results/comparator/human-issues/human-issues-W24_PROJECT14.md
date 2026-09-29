# Human Issues — W24 Project 14

1. The background section is missing references.

2. Data whose scale varies considerably over time are often best plotted on a log scale.

3. Some ARIMA code is apparently taken from 531w24 midterm project 6 without credit. The smallest root table is a good idea to copy, but it would be better to give credit.

4. Regression with ARMA errors (looking to understand the time trend, perhaps with an exponential trend function) might be more insightful than differencing and fitting ARIMA.

5. The SEIR model equations do not perfectly match the implemented equations in the code.

6. The parameter values given as the result of the local search are the starting point for that search, as can be seen by looking at the convergence diagnostics. Considerably better likelihood values are obtained by the end of the local search.

7. The modeling and analysis is similar, but in many ways inferior, to a previous STATS 531 final project on tuberculosis (531w16 project 20). That project is cited, but it would have been better to acknowledge more fully what was learned from that paper, and make progress by contrasting that work with the different dataset in question here.

8. There is an inconsistency in log-likelihood values reported within the text and those shown in code outputs (-628.8447 and -629.6903), which raises concerns about the accuracy of the reported results.

9. SEIR has been successful for rapidly transmitted diseases but tuberculosis is different. Only those in poor housing, or with other risk factors, are typically at risk of TB, so treating S as the entire population may be problematic.

10. The report does not discuss the specification and estimation of initial state values. That can be established from the provided code, but should be in the report.

11. The model-based assessment does not get beyond basic iterated filtering to global maximization or profiles. Given the head-start acquired by building on a previous project, one can expect to get further.

12. Adding a diagram for the process model would help readers to easily understand your model.
