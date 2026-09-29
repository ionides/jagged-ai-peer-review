# Human Issues — W25 Project 13

1. There are major issues with how the project is presented. Various things are incomplete in strange ways, e.g., "(tweaked for a typical exoplanet study—let me know if your bounds differ)", that look GenAI generated.

2. The passage describing the DEoptim algorithm reads like GenAI text (e.g., "This method is perfect for handling complex, non-linear, and multi-modal likelihood surfaces ... Why DEoptim? It's fantastic at finding the global maximum...").

3. The use of DEoptim rather than methods studied in class raises questions. There are no benchmarks and no serious discussion of convergence diagnostics beyond an assertion that the search was effective. The project could be avoiding mastery of material covered in class, rather than improving on it.

4. "Simulated trajectories follow the general pattern of the observed data" does not seem to match the figure, where the simulated trajectories oscillate rapidly, unlike the data.

5. The source code has hard-coded results described as "Note: I made up these numbers based on typical patterns—swap in your actual log-likelihood values if you have them!" In various places, the results appear to have been fabricated.

6. It would be good to have statistical benchmark models to help assess the quality of fit from the likelihood of the mechanistic model. A suitable regression model could be appropriate even if ARMA is not.

7. The residual plot and residual histogram are inappropriately interpreted despite very clear seasonal patterns with periodicity approximately 400. The ACF plot shows very large autocorrelation values for all of the first 50 lags, which is totally inconsistent with the author's interpretations and indicates severe residual autocorrelation and violation of residual assumptions.

8. There are many repetitions of symbols in the equations which make the report harder to read.

9. Only Figure 1 is numbered, but elsewhere there are references to Fig. 2, Fig. 3, etc., which are not numbered.

10. The claim that the algorithm "converged to a best log-likelihood of -151017.163 ... demonstrating effective optimization over 50 iterations" is not supported — there is no evidence that the algorithm converged.

11. Technical terms like BKJD (Barycentric Kepler Julian Date) need clear explanations for readers without specialized astronomical knowledge.

12. The redundant presentation of the transit model equation (appearing multiple times with slight variations) creates unnecessary confusion.

13. Multiple nonsensical uses of "your" make it look like the writing was produced to a considerable extent by GenAI.

14. The reference "Rappaport, S., Levine, A., Chiang, E., El Mellah, I., Jenkins, J. M., Kaltenegger, L., … & Villasenor, J. (2012). 'Light-curve Analysis of KIC 12557548b: An Extrasolar Planet with a Comet-like Tail.' The Astrophysical Journal, 752(1), 1." does not exist as cited. This error looks like a GenAI hallucination and is a serious scholarly concern.
