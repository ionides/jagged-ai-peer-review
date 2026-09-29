# Human Issues — W24 Project 04

1. The introduction promises an investigation of four different regions, but results are only shown for data from one. Simulation results are carried out for three cities. These simulations are discussed as if they were data, which is confusing.

2. The simulations for California, Washington and New York are rather similar. They all have the same population, the same in initial conditions, the same feature that the susceptible fraction jumps straight back to 800,000 after an epidemic. It is unclear, even from the code, what is being plotted and why the curves modeling these three cities are similar but different.

3. Showing simulation results as EDA is unexpected. Better for EDA to focus on data.

4. "QQ plot shows good performance" is unclear, but it should be noted that the QQ plot shows long tails.

5. The fitted values plot shows 1-step predictions, which is not very informative.

6. The code for fitting arima models is derived from the `arima2` package but in fact uses `stats::arima`. It is unclear if that is intentional.

7. Readers attempting to reproduce the numerical results found that the code failed to run.

8. The authors say they use a software package called `GenSA`. This package is not explained. The fitting criterion seems to be least squares, leading to a fit which is essentially constant at zero. This is not very informative. Maximum likelihood, with a plausible measurement model, would be much better - and was the approach taught in class.

9. This SEIR model can only fit one peak, whereas the actual pandemic had multiple waves. The report described this as a "commendable" explanation of the data, which is misleading.

10. Various projects from past years do a better job of explaining COVID-19 dynamics. One of these is cited in the project.

11. The authors plug a single simulation into least squares and optimize that function to an optizer. That does not correspond to maximum likelihood estimation. Methods to evaluate and optimize the likelihood were taught in class, and should be used. Overall, the project does not demonstrate mastery of the ideas or methods for likelihood-based inference discussed in the second half of the course.
