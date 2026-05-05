# Peer Review: W25 Project 15
## Bitcoin Volatility Analysis with Fear & Greed Index

---

## Summary

This project presents a volatility analysis of daily Bitcoin returns from January 2020 to April 2025. It compares six models: GARCH(3,1), the Breto stochastic volatility (SV) model, a modified Breto model incorporating the Fear & Greed (FG) Index, each of the latter two also fitted with Student t-distributed innovations, and a Heston-style simple SV model in both normal and t forms. The project's central novelty is integrating a sentiment covariate into the POMP framework. The paper is ambitious and well-structured, but contains several serious methodological, coding, and reporting errors that undermine its conclusions.

---

## Weaknesses (Most Critical First)

### 1. [MAJOR] Duplicate `stew` File Name Invalidates the "New Global Search" for the Basic Breto Model

Lines 532 and 586 both call `stew(file = paste0("box_eval_bitcoin_", run_level, ".rda"), ...)`. Because `stew` caches results to disk and reloads them if the file already exists, the second call (the "New Global Search" with the narrower box) does not run new computations — it silently restores the results from the first global search. The conclusion that "the log-likelihood curve now exhibits a single, well-defined peak" (line 621) for the narrower box is therefore unfounded: those results reflect the original broad search. Any CSV output from the narrowed box is also never produced.

### 2. [MAJOR] Initial Global Search Box for the Basic Breto Model Excludes the Claimed Superior Mode

The first global search box (lines 523-530) sets `phi = c(0.95, 0.99)` and `mu_h = c(-1, 0)`. Yet from the local search (line 518), the authors identify the superior mode as having `phi ~0.5` and `mu_h ~-7`. The initial global search box is therefore entirely disjoint from the region identified as best. Despite this, the narrative (line 568) claims the global search recovers the better mode with `phi ~0.5` and `mu_h ~-7`. This is internally inconsistent: a search constrained to `phi in [0.95, 0.99]` and `mu_h in [-1, 0]` cannot discover parameters at `phi ~0.5` and `mu_h ~-7`. This discrepancy suggests the text was written based on expected behavior rather than the actual code output.

### 3. [MAJOR] Heston SV Code Does Not Match the Stated Model Equation

The model equation (line 1344) states:
`V_n = (1 - phi)*theta + phi*V_{n-1} + xi*sqrt(V_{n-1})*omega_n`

But the C snippet (line 1377, and identically line 1590) implements:
`V = theta * (1 - phi) + phi * sqrt(V) + sqrt(V) * omega`

The term `phi * sqrt(V)` in code corresponds to `phi * sqrt(V_{n-1})`, not `phi * V_{n-1}`. This means the implemented process is not the stated Heston-type CIR process. The fitted model is not the model that is described. This same bug appears in both the normal and t-distribution versions of the simple SV model.

### 4. [MAJOR] Potential FNG Covariate Length Mismatch

In the modified Breto model (lines 727-730), the covariate table is built with:
`dFNG = c(0, diff(fng_subset$FNG_scaled))`
where `fng_subset` is subsetted from the API data independently of the bitcoin merge. Meanwhile `logd` comes from `diff(log(bitcoin$Price))` where `bitcoin = merged_df` (inner join of FNG and bitcoin CSVs). The bitcoin CSV has 1926 data rows; the API with `limit=2000` subsetted to 2020-2025 may yield a slightly different number of rows than the merged dataset, especially if any dates are missing from one source. If `nrow(fng_subset) != nrow(merged_df)`, then `length(c(0, diff(fng_subset$FNG_scaled)))` will not equal `length(logd) + 1`, causing either a silent recycling error or a crash. No explicit length checks or assertions are present in the code.

### 5. [MAJOR] No Formal Statistical Inference for the FG Index Effect

The project's central scientific claim — that fear drives Bitcoin volatility more than greed (based on the sign of gamma) — is supported only by visual inspection of pair plots and the sign of the MLE estimate. There is no likelihood ratio test, profile likelihood confidence interval, or any other formal inferential procedure to establish whether gamma is significantly different from zero. Concluding that the FG Index has a meaningful impact on volatility without a test of `H0: gamma = 0` against `H1: gamma ≠ 0` is statistically unjustified, particularly given the conflicting local-search result (positive gamma) versus global-search result (negative gamma).

### 6. [MAJOR] Log-Likelihood Comparison Across Non-Nested Models Is Informal and Potentially Misleading

The project compares log-likelihoods across the Breto models (~4070-4100), modified Breto models, and the simple Heston SV models (~3899 for normal, higher for t). However, the simple SV model uses raw log returns (not demeaned), while the Breto models use demeaned log returns. Using different response variables means the log-likelihoods are not directly comparable. Moreover, the GARCH(3,1) log-likelihood of ~3894 is from `tseries::garch`, which uses a conditional likelihood that differs from the full likelihood computed by the POMP particle filter. The authors acknowledge this at line 287 but do not adequately account for it when comparing models.

### 7. [MAJOR] `sigma_nu` Converging to Zero Is Not Discussed as a Boundary Problem

Line 1017 states that `sigma_nu` converges to zero in the modified Breto model global search. A parameter converging to the boundary of its support is a significant model diagnostic indicating possible model misspecification or a degenerate solution where `G_n` becomes constant (no leverage variation). The authors do not explore whether the model is identifiable when `sigma_nu -> 0`, whether the leverage component is effectively disabled, or whether a simpler model (without the `G_n` random walk) would be preferred. Similarly, the `H_0` non-convergence (also line 1017) is mentioned but not diagnosed.

### 8. [MODERATE] Fixed Degrees of Freedom (df=5) for the t-Distribution Is Not Justified Rigorously

The authors state they "experimented with different values for degrees of freedom ranging from 3-25" (line 1021) but do not show the results of this experiment, nor do they report the log-likelihoods across those values. Fixing df=5 without a proper model selection procedure or profiling over df is ad hoc. Treating df as an estimated parameter (via transformation) would be more principled and would allow a formal test of whether heavy tails are warranted.

### 9. [MODERATE] Contradictory Claims About Local vs. Global Search Sign of Gamma

The local search for the modified Breto model (line 913) finds a positive gamma, while the global search (line 995) finds a negative gamma. The authors dismiss the local search result and rely on the global search, but this discrepancy signals an identifiability problem or multimodal likelihood surface for gamma. The paper does not investigate whether the global search has actually converged, profile the likelihood over gamma, or provide uncertainty quantification. Concluding that "fear drives market volatility more than greed" from a noisy point estimate with contradictory local-search evidence is an overreach.

### 10. [MODERATE] "New Global Search" Narrative Is Internally Inconsistent

Section "New Global Search" (lines 572-621) claims to investigate whether a narrower parameter box improves on the first global search, but due to the stew filename collision (issue 1 above), both searches produce the same cached results. The text nonetheless discusses differences between the two searches ("the log-likelihood curve now exhibits a single, well-defined peak"), indicating the discussion was written based on expected rather than actual computational outputs.

### 11. [MODERATE] Both Simple SV Global Searches Overwrite the Same Output File

Lines 1537 and 1736 both write to `"btc_global_params.csv"` using `write.csv` (which overwrites by default). When the document is rendered sequentially, the file from the normal-distribution SV global search is overwritten by the t-distribution results, silently destroying the normal-distribution output. This also means any downstream use of that CSV would reflect only the t-distribution results.

### 12. [MODERATE] Justification for Differencing the FG Index Is Incomplete

The authors difference the scaled FG Index to achieve stationarity (lines 655-673), citing the slowly decaying ACF. However, an ADF or KPSS unit-root test would be more rigorous than visual inspection of the ACF. Furthermore, differencing transforms the covariate from a level-based sentiment measure to a change-based measure, which changes the economic interpretation: the model now captures the effect of *changes in* fear/greed rather than the level of fear/greed. This interpretive shift is not adequately discussed.

### 13. [MINOR] Title Contains a Typo

The document title (line 2) reads "olatility analysis on Bitcoin returns" — the leading "V" in "Volatility" is missing.

### 14. [MINOR] Figure 25 Is Mislabeled as "Local Search" in the t-Distribution Global Search

Line 1322 labels the global search pairs plot for the t-distribution model as "Figure 25. Local Search Pairwise Relationships," when it is in fact a global search plot. This suggests a copy-paste error and makes it difficult to distinguish the figures.

### 15. [MINOR] Several Typographical and Grammatical Issues Reduce Clarity

- Line 1019: "Stuent's" should be "Student's"
- Line 573: "aerbecause" should be "because"
- Line 829: "Chapte-15" should be "Chapter 15"
- Line 227: "demanded return" should be "demeaned return"; "intial" should be "initial"
- Line 687: "signficantly" should be "significantly"
- Reference [2] (line 1800): Missing the closing `</span>` tag; similar HTML errors in references [3], [9], [10], [11]
- The document acknowledges (line 1813) that UM ChatGPT was used to "polish sentences and correct grammars," yet multiple grammatical errors remain

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project15/bitcoin_2020-01-01_2025-04-06.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project15/Makefile`
