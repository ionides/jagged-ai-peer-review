# Human Issues — W25 Project 01

1. $k$ could be an important parameter for fitting the data, and it should be estimated not fixed.

2. Data of this kind can be more insightfully plotted on a log scale (presented in the project later). Also, the linear analysis (additive decomposition, periodogram, ARMA) are better on a log scale. The team is correct to note that comparing likelihoods on log and natural scale requires care (i.e., a Jacobian transformation, see the Measles and Polio case studies in the notes).

3. A log-SARMA benchmark would be a more rigorous test of model specification than SARMA.

4. Influenza cases is either lab-confirmed cases (which depends critically on the amount of testing) or reported influenza-like illness (ILI) which is not all influenza. Later, it seems that what is called "cases" is ILI.

5. It is not clear what is learned from the additive decomposition that cannot be seen more clearly from other plots. To study seasonality of nonlinear and highly variable systems, a simple line plot of superposed seasonal trajectories can be more informative.

6. Listing the raw data is usually inappropriate. Similarly, showing raw R summaries is usually less helpful than identifying and explaining key properties. In other words, showing data and summary statistics follows the same rule as other figures and tables: if you present it, discuss it and explain what you learned from this representation.

7. The ARMA section might be too long. The main thing acquired from this section is a benchmark to compare against mechanistic model fits, so it is better to focus on the mechanistic models.

8. Sec 5.6 is not a poor man's profile as defined in the notes, it is a slice. The plot in 5.6.1 shows terrible likelihoods for large rho, much lower than the benchmark, but this is just due to a mismatch between the state parameters and the proposed reporting rate. This is fixed in Sec 5.7. It would be better to focus more on the profile than the slice.

9. The references are helpful. They do not conform to usual standards for scientific research, but focusing on links rather than full text references makes practical sense in the context of this final project.

10. The report is long and would be easier to read if it were more selective about what is included. Things that are tried and superseded can be noted in the main text and presented only in an appendix.
