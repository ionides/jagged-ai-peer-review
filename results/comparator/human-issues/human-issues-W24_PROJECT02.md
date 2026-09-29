# Human Issues — W24 Project 02

1. Explain acronyms at first occurrence, e.g., CPUE.

2. The alternative prey hypothesis (mentioned in the project title) could be explained in the introduction. It becomes clearer later on, in the model section.

3. The description of what is denoted by 'peak_rodent_year' was a bit lacking. It was only described; "Peak rodent year is scored as "yes", otherwise 'no'" but it does not describe what is meant by that or how it is decided or when.

4. It could have been explicitly explained why the log of CPUE was used in the model instead of the CPUE itself.

5. ARIMA with differencing parameter I>0 does not have immediately comparable likelihood, so is not appropriate as a benchmark. One could use ARMA with a trend (linear, quadratic, or exponential) instead.

6. If the formal null and alternative hypotheses are defined for the KPSS test, it may be clearer what can legitimately be concluded from it.

7. The log-likelihood search is incomplete, as evidenced by the local search beating the preliminary global search.

8. In Fig 3.1, the effective sample size is usually 1, and never more than 2.2. This indicates serious particle depletion. Evidently, Np=50 particles is insufficient, though model improvements may be needed as well as extra computational effort.

9. Diagnostic plot. The starting point has very low likelihood. A search starting from not such a poor place might be easier.

10. To acknowledge the preliminary nature of the mechanistic model, it is premature to conclude that "ARMA is a better fit to the data".

11. There is a mismatch between the text reported log-likelihood (-205) and the value in the R output (-288).
