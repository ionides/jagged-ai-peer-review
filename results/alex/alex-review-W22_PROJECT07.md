# Peer Review: Volatility Analysis on Ford and Tesla Stock
**Semester:** W22 | **Project:** 07

---

## Summary

This project compares volatility models (ARIMA, GARCH, and POMP) for Ford and Tesla stock log returns using five years of daily adjusted close prices (March 2017 to March 2022). The POMP model follows the Breto (2014) stochastic leverage framework. While the project covers a reasonable range of models and applies the standard iterated filtering workflow, it contains several serious methodological errors, code bugs, inconsistencies between the Ford and Tesla analyses, and weak or missing model comparisons.

---

## Weaknesses (Most Critical First)

### 1. [MAJOR] Tesla POMP Uses Only 365 Observations While Ford Uses All 1,258

The Ford POMP model is fitted to the full dataset (1,258 log returns), but the Tesla POMP model silently subsets the data to the last 365 observations (`TeslaData = tail(TeslaData, 365)`). This makes any comparison between Ford and Tesla POMP results meaningless because they are fitted to data of vastly different length and time periods. The authors never justify or even acknowledge this inconsistency. The GARCH models, by contrast, use the full dataset for both stocks. This is arguably the most damaging methodological flaw in the paper.

### 2. [MAJOR] POMP vs. GARCH Comparison Is Invalid -- Log-Likelihoods Are Not Comparable

The conclusion states "The POMP models perform much better than the GARCH for both Ford and Tesla," yet no valid comparison is provided. The GARCH log-likelihoods (~3087 for Ford, ~2393 for Tesla with normal GARCH) and POMP log-likelihoods (~3154 for Ford, ~709 for Tesla) cannot be directly compared because:
(a) The GARCH and POMP models are fitted to different data transformations (GARCH uses the raw log returns; the POMP model further mean-centers them, though this is minor), and more critically,
(b) The Tesla POMP uses only 365 observations versus 1,258 for the Tesla GARCH models, making the Tesla log-likelihoods completely incomparable.
The paper promised AIC-based comparison in the introduction but never delivers one.

### 3. [MAJOR] Bug in Tesla GARCH Prediction Plot -- Ford's Volatility Used for Tesla

In Figure 10 (Tesla GARCH prediction plot), lines 432-433 of the Rmd mistakenly use `ford_ahead[,2]` instead of `tesla_ahead[,2]` for the predicted volatility bounds:
```r
lines(tesla_ahead[,1]+ford_ahead[,2], lwd=2, lty=1, col="green")
lines(tesla_ahead[,1]-ford_ahead[,2] , lwd=2, lty=1, col="green")
```
This means Figure 10 displays Ford's predicted volatility envelope around Tesla's predicted returns, making the comparison in the text incorrect.

### 4. [MAJOR] Model Equation for R_n Is Algebraically Trivial (Typographical Error)

The POMP model description (line 459) states:
$$R_n = \frac{\exp\{2G_N\}-1}{\exp\{2G_N\}-1}$$
This fraction always equals 1 (numerator equals denominator), which is clearly a transcription error. The correct formula from Breto (2014) should use `tanh(G_n)` or a similar expression. The code correctly uses `tanh(G)`, so the written equation does not match the implementation. This error is never flagged or corrected in the text.

### 5. [MAJOR] Ford Global Search References a Missing File and Uses Wrong `run_level` Object

The Ford global search code saves to `"ford_global.csv"` but the loading chunk at line 711 instead loads `box_eval-2.rda` and reconstructs `r.box` from `if.box` and `L.box` stored in that file. There is no explicit loading of `ford_global.csv`. The run_level for box_eval is 2 rather than 3, which is inconsistent with the stated run_level=3 used for local search. This creates ambiguity about how many particles and replicates were actually used for the reported global search results.

### 6. [MAJOR] Ford and Tesla POMP Run at Different Computational Scales

Ford POMP uses `ford_Np = 1000`, `ford_Nmif = 100`, `ford_Nreps_local = 20`, `ford_Nreps_global = 100` (at run_level=3). Tesla POMP uses `Tesla_Np = 2000`, `Tesla_Nmif = 200`, `Tesla_Nreps_local = 20`, `Tesla_Nreps_global = 100` (at run_level=3) but the Tesla loops use `%do%` (sequential) instead of `%dopar%` (parallel), while Ford uses `%dopar%`. This means Tesla's iterated filtering, which uses twice as many particles and iterations, is run sequentially, making computation far slower and inconsistent with the Ford analysis. Furthermore, sequential versus parallel execution can affect reproducibility when random seeds are set via `registerDoRNG`.

### 7. [MAJOR] POMP Model Description and State Variable Definition Are Inconsistent

The text defines $Y_n = \exp\{H_n/2\}$ as the measurement equation (line 461), but the actual `dmeasure` in code is `lik = dnorm(y, 0, exp(H/2), give_log)`, meaning $Y_n \sim \mathcal{N}(0, \exp(H_n/2))$. This is a critical difference: the first expression makes $Y_n$ deterministic given $H_n$, while the code implements it as a normally distributed random variable. Additionally, the text says "$Y_n$ is the measurement that serves as the perfectly observed latent state," which contradicts the standard POMP framework where $Y_n$ is the observed data (log returns), not a latent state.

### 8. [MINOR] Tesla POMP Section Duplicates Figure Captions From a Different Project

The Tesla POMP section contains two figure captions that are clearly copy-paste errors from a different project (likely an Apple stock project):
- Line 746: `fig.cap="Figure 1: Original Data"` (resets figure numbering mid-document)
- Line 751: `fig.cap="Figure 1: Adjusted Closing Price of Apple from 2017 to 2022 (Daily)"`

These captions refer to Apple stock data when the project is analyzing Tesla, and reset the figure counter back to "Figure 1" in the middle of the document. This indicates the Tesla section was adapted from a prior project without adequate revision.

### 9. [MINOR] Incomplete Sentence Left in Introduction

Line 130 contains an unfinished parenthetical: "(why we want to use log return instead of return?)" -- this appears to be a note-to-self that was never resolved. The question is left unanswered in the text, leaving an unexplained methodological choice.

### 10. [MINOR] GARCH Model Selection Criteria Are Inconsistently Applied

For the normal GARCH, the authors select GARCH(2,1) for Ford (highest log-likelihood) and GARCH(1,1) for Tesla (highest log-likelihood). For the t-distribution GARCH, Ford's optimal model is GARCH(2,3) but GARCH(1,1) is chosen for simplicity; yet for Tesla, all 9 models are deemed similar and GARCH(1,1) is chosen. The authors do not provide the t-GARCH table for Ford (they only mention GARCH(2,3) is optimal), nor do they apply a consistent AIC-based selection criterion across all models. Likelihood-based selection was used for normal GARCH but abandoned for t-GARCH without adequate justification.

### 11. [MINOR] Weak Identifiability of mu_h and H_0 Is Rationalized Rather Than Addressed

The convergence diagnostics for both Ford and Tesla clearly show that `mu_h` and `H_0` do not converge. The text acknowledges this but asserts it is "not a weakness of our model but a statistical fact" citing HW8. While weak identifiability can be a genuine statistical property, the authors make no attempt to investigate why these parameters are weakly identified (e.g., via profile likelihood), whether fixing them would help convergence of other parameters, or whether the model could be reparameterized. Dismissing non-convergence as acceptable without further analysis weakens the scientific contribution.

### 12. [MINOR] Ford Global Search Convergence Discussion References the Wrong Figure

The Ford global search section (lines 670-679) discusses convergence patterns referencing "Figure 12," but Figure 12 is the caption for the Ford local search convergence plot. The global convergence plot is Figure 14. The narrative appears to have been written for the local search figure and then reused for the global search section without updating the figure reference.

### 13. [MINOR] Decomposition Applied to Non-Stationary Log Returns Is Methodologically Questionable

The authors apply classical `decompose()` to the log return series to extract trends (Figure 3). The `decompose()` function uses a centered moving average and assumes an additive or multiplicative decomposition appropriate for seasonal series. Log returns of stocks are generally close to white noise with no strong seasonal or trend components; the "trend" extracted is a moving average smoothing artifact, not a meaningful economic trend. The interpretation given in the text (e.g., "the trend of Tesla also increases but starts decreasing after mid 2020") conflates moving-average smoothing with genuine trend, without justification for this approach.

### 14. [MINOR] References Section Is Labeled "Scholarships" Instead of "References"

The final section heading reads "# Scholarships" (line 1009) where it should read "# References." This is a clear typo or copy-paste error from a template.

### 15. [MINOR] YAML Header Contains Typo That Disables Table of Contents Numbering

Line 9 of the YAML front matter reads `nember_sections: true` instead of `number_sections: true`. This means section numbering in the HTML output is silently disabled. While minor, it indicates insufficient proofreading of the document structure.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/ford_params2.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/Tesla_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/Tesla_params1.csv`
