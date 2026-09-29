# Human Issues — W25 Project 06

1. Too little time was spent on the mechanistic POMP model compared to ARMA and deep learning. The difficulties experienced with the postulated POMP model need thoughtful diagnostics to figure out how to make both the science and the time series data analysis work together coherently.

2. MAPE is not comparable between data transformations (for the same reason log-likelihood is not), yet the team uses it to assess methods across different data transformations without proper adjustment. Using elaborate modern methods (VMD, N-BEATS) should not come at the expense of complete and careful use of the appropriate methods studied in class.

3. Likelihood is a more efficient inference metric than MAPE; if the team preferred MAPE, they should have calculated MAPE also for the SEIR model to allow a fair comparison.

4. The ADF test is inappropriate and a poor choice here. The peaks are visibly diminishing through time, indicating nonstationarity; the ADF model is especially inappropriate before taking logs and remains a poor choice even after.

5. The claim that "the residual time series plot shows no visible trend or seasonal structure" for ARMA is incorrect. The time plot of residuals shows extreme heteroskedasticity matching seasonal peaks and troughs, which is a diagnostic signal that a logarithmic transformation should be considered.

6. The SEIR model is not compared to the ARMA benchmark. The fitted SEIR model falls short of ARMA by 157 log-likelihood units (3760 vs. 3603), a large discrepancy suggesting the SEIR model is missing something important.

7. Particle depletion, numerical overflow, and degeneracy in measurement likelihoods during inference are typical signs of a poor model fit. The inflexible modeling of seasonality or the lack of overdispersion in the process model may be the issue; diagnostic checks for the POMP model would help track this down.

8. Mean/median summary statistics are not meaningful for a time series with substantial dynamic variation; presenting them and making statements about symmetry is appropriate only when data are well modeled as i.i.d.

9. For comparing ARMA with log-ARMA, a Jacobian calculation should be used to put the log-likelihood and AIC values on the same scale (as in the measles case study, Chapter 18).

10. Examining ACF, PACF, and Box-Ljung statistics for residuals of a large ARMA selected by AIC is almost always uninformative; it would be better to examine normality of residuals, which would reveal long tails and provide another clue that a log transform is appropriate.

11. The Outlook section appears to be produced by GenAI: it lists modern methods without references or details, and the generic assertions are the kind of content GenAI could generate.
