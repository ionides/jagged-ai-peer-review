# Peer Review: W22 Project 07
**Title:** Volatility Analysis on Ford and Tesla Stock
**Course:** STATS 531, Winter 2022

---

## Summary

This project applies ARIMA, GARCH (normal and t-distributed), and POMP stochastic leverage models to daily log returns of Ford and Tesla stock prices (March 2017–March 2022). The project's stated goal is to compare all three model classes via AIC and to contrast the two stocks. While the GARCH analysis is reasonably conducted and the POMP implementation follows the course template faithfully, the project contains several critical errors that undermine its conclusions: the Tesla POMP model is fitted to only one-quarter of the data used by the Tesla GARCH model, making all cross-model comparisons for Tesla invalid; the main conclusion that "POMP performs much better than GARCH" is directly contradicted by the reported likelihoods; the promised three-way AIC comparison across model classes is never actually delivered; and the computation statistics reported in the text do not match what was actually run (verified against saved `.rda` files). No profile likelihoods are reported for any parameter.

---

## Major Issues

### 1. Tesla POMP uses a different dataset than Tesla GARCH, invalidating all cross-model comparisons for Tesla

The Tesla GARCH models (both normal and t-distributed) are fitted to the full 1,258 log returns covering March 2017–March 2022 (`Tesla_lreturn`, derived from all 1,259 rows of `TSLA_27Mar2017_24Mar2022.csv`). However, the Tesla POMP section reads `TeslaData = tail(TeslaData, 365)` before constructing log returns, restricting the POMP model to only 364 log returns (October 2020–March 2022).

The Tesla GARCH t-dist GARCH(1,1) log-likelihood is 2,484.77 (over 1,258 observations), while the Tesla POMP log-likelihood is 709.6 (over 364 observations). These numbers are not comparable. A log-likelihood computed on 1,258 observations will naturally be approximately 3.5 times larger in magnitude than one computed on 364 observations even for identical models. The conclusion that "POMP models perform much better than GARCH" for Tesla is therefore entirely unfounded from a statistical standpoint.

**Fix:** Refit the Tesla POMP model using all 1,258 log returns, matching the data used by the GARCH models.

---

### 2. Conclusion that POMP outperforms GARCH is contradicted by the reported likelihoods for Ford

For Ford, the GARCH t-distributed GARCH(1,1) log-likelihood is 3,189.48, while the POMP maximum log-likelihood from the local search is 3,154.3 and from the global search is 3,150.9. Thus the GARCH model achieves a higher log-likelihood than the POMP model by approximately 35–39 log units. Even after penalizing for the difference in parameter count (GARCH(1,1) has 4 parameters vs. POMP's 6), the GARCH model is clearly preferred by AIC by more than 70 units. The conclusion on the final page states "The POMP models perform much better than the GARCH for both Ford and Tesla" — this claim is directly contradicted by the numbers in the paper itself.

**Fix:** Reread the log-likelihood tables and correct the comparative conclusion. Investigate whether the POMP model specification or computation can be improved before concluding POMP is worse.

---

### 3. Promised AIC comparison across ARIMA, GARCH, and POMP is never delivered

The Introduction explicitly states: "We will compare the performance of the 3 kinds of models for volatility using AIC." However, no such three-way AIC comparison table appears anywhere in the paper. The ARIMA section concludes that ARMA(0,0) (white noise) is selected and is "not particularly useful," at which point the ARIMA analysis is abandoned. No ARIMA model is ultimately fitted or retained for comparison. The GARCH and POMP sections compare models within each class but no synthesis table compares GARCH to POMP by AIC or log-likelihood on a common dataset for Ford (or a corrected Tesla dataset).

**Fix:** Either produce the promised AIC comparison table across all three model classes, or revise the introduction to accurately describe what comparisons are made.

---

### 4. Ford global search actual computation does not match reported methodology

The text states: "For the global search, we fit 100 repeated iterations with 2000 particles each." However, the saved file `box_eval-2.rda` (which the code actually loads via `load("box_eval-2.rda")`) contains an `if.box` object with only 20 elements and particles Np = 1,000 (run_level = 2, not run_level = 3). The file naming convention (`box_eval-2.rda`) and the verified object contents confirm that the run_level = 2 global search was loaded, which produces 20 global replicates at 1,000 particles, not the 100 replicates at 2,000 particles described in the text.

Similarly, the Ford initial pfilter text claims "20 times with 2000 particles" but the saved file `pf1-3.rda` contains 10 pfilter replicates with 1,000 particles.

This discrepancy means the reproducibility criterion is violated: the reported computational effort is inconsistent with what was actually run. (CC-Yes: Error 1.8 — Missing/misreported convergence diagnostics.)

**Fix:** Ensure the loaded `.rda` files correspond to the computational settings described in the text, or correct the descriptions to match the actual computations.

---

### 5. No profile likelihoods reported for any parameter

Neither the Ford nor Tesla POMP analysis includes any profile likelihood computation. Without profile likelihoods, confidence intervals cannot be reported and parameter identifiability cannot be formally assessed. The paper acknowledges that parameters such as `mu_h`, `phi`, and `H_0` show poor convergence across multiple runs but dismisses this as "weak identifiability" without providing profile likelihood evidence to distinguish identifiability from numerical non-convergence.

Per Wheeler et al. (2024), profile likelihoods should be computed for key parameters to assess identifiability and report confidence intervals. This is also a core course expectation per Chapter 16 of the course notes. (CC-Yes: Error 1.9 — Profile likelihood absent.)

**Fix:** Compute profile likelihoods for at least the key parameters (e.g., `phi`, `sigma_eta`, `mu_h`) for both Ford and Tesla POMP models.

---

### 6. Typographical error in the leverage function formula renders it mathematically incorrect

The formula for the leverage ratio `R_n` (line 459 of the Rmd) is typeset as:

$$R_n = \frac{\exp\{2G_N\}-1}{\exp\{2G_N\}-1}$$

Both the numerator and denominator are identical, so the formula evaluates to 1 for all `G_n`, which is not the intended leverage function. The correct formula from Breto (2014) is:

$$R_n = \frac{\exp\{2G_n\}-1}{\exp\{2G_n\}+1} = \tanh(G_n)$$

The code correctly implements `tanh(G)`, so this is a typesetting error only, but it misrepresents the model to the reader.

**Fix:** Correct the denominator to `exp{2G_n}+1`.

---

### 7. Normal GARCH and t-GARCH log-likelihood values compared without noting different normalization conventions

The normal GARCH table uses `tseries:::logLik.garch()` while the t-GARCH table uses `-fit.garch@fit$llh` from `fGarch`. These two functions may report log-likelihoods under different normalization conventions, and the `tseries::garch` function drops the first `max(p,q)` observations, creating a slight difference in effective sample size between the two tables. The paper directly compares values across the two tables (e.g., GARCH(2,1) normal = 3087.87 vs. GARCH(1,1) t-dist = 3189.48) without noting these potential incompatibilities. (CC-Yes: Error 2.9 — trusting software likelihood output without checking conventions.)

**Fix:** Verify that both likelihood values use the same normalization and effective sample size, or note the limitations of the cross-table comparison.

---

## Minor Issues

### 8. Tesla prediction plot (Figure 10) uses Ford forecast uncertainty, not Tesla's

In the code for Figure 10 (Tesla GARCH forecast), lines 432–433 plot:

```
lines(tesla_ahead[,1] + ford_ahead[,2], ...)
lines(tesla_ahead[,1] - ford_ahead[,2], ...)
```

The code uses `ford_ahead[,2]` (Ford's predicted standard deviation) instead of `tesla_ahead[,2]` (Tesla's predicted standard deviation) to construct the prediction bands for the Tesla plot. Since Tesla has higher volatility than Ford, this understates Tesla's forecast uncertainty.

**Fix:** Replace `ford_ahead[,2]` with `tesla_ahead[,2]` in Figure 10.

---

### 9. Figure captions in the Tesla POMP section misidentify the stock as "Apple"

The chunk at line 751 uses `fig.cap="Figure 1: Adjusted Closing Price of Apple from 2017 to 2022 (Daily)"`. The data and analysis are for Tesla, not Apple. Additionally, the Tesla POMP section restarts figure numbering at "Figure 1" and "Figure 2," duplicating figure numbers already used in the Ford section and the EDA.

**Fix:** Correct the figure captions to reference Tesla and use sequential figure numbering throughout.

---

### 10. Tesla local and global POMP searches use sequential execution rather than parallel

The Ford POMP section uses `%dopar%` for both local and global mif2 searches. The Tesla POMP section uses `%do%` (sequential) for both. With 20 local replicates at Np = 2,000 and Nmif = 200, and 100 global replicates, sequential execution substantially increases runtime and may have limited the practical thoroughness of the Tesla search compared to Ford.

**Fix:** Replace `%do%` with `%dopar%` in the Tesla local and global search loops, consistent with the Ford implementation.

---

### 11. No benchmark comparison for POMP models

Neither the Ford nor Tesla POMP analysis is compared against a non-mechanistic benchmark model (e.g., ARMA on squared returns, IID negative binomial). The ARIMA analysis was abandoned after finding ARMA(0,0) best on log returns; this model was not retained as a baseline for the POMP log-likelihood comparison. Without a benchmark, it is impossible to assess whether the POMP stochastic leverage model captures volatility structure beyond what a simple model achieves. (CC-Yes: Error 1.6 — no benchmark comparison.)

Note: Absence of a benchmark is a minor issue in this course context but is worth flagging as a gap in the evaluation.

---

### 12. Citation numbering is internally inconsistent

The POMP model structure is described as following "Breto (2014)[2]," but citation [2] in the Out-Class References section is Ghahramani and Thavaneswaran (2008) on GARCH model identification. The Breto (2014) reference is never listed. In-class citation [2] is Chapter 16 lecture notes, creating further ambiguity. Readers cannot locate the source for the POMP model specification.

**Fix:** Add a proper reference for Breto (2014) and reconcile the citation numbering so [2] refers to a single, consistent source throughout the paper.

---

### 13. Decomposition of log returns treated as revealing meaningful trends

The paper applies classical additive decomposition (`decompose()`) to the log return series and interprets the extracted trend component as meaningful (Figure 3). Log returns of financial assets are approximately white noise by the efficient market hypothesis; any trend extracted by `decompose()` from such a series is dominated by the centered moving average smoothing window, not a genuine economic trend. Describing the extracted trend as evidence that "the trend of Tesla also increases but starts decreasing after mid 2020" overstates what can be inferred from this decomposition.

**Fix:** Either remove the decomposition plot and its interpretation, or note explicitly that the moving-average trend from `decompose()` applied to near-white-noise log returns does not reflect a genuine price trend.

---

### 14. Global search box for `phi` is overly narrow given the observed bimodal behavior

Both Ford and Tesla global searches restrict `phi` to the range (0.95, 0.99). However, the local search trace plots and pair plots show that `phi` exhibits bimodal behavior — some filters converge to values near 1 while others show a distinct second mode. A search box that covers only the upper portion of the parameter space near 1 may miss the second mode entirely, preventing the global search from exploring whether the lower mode corresponds to a higher likelihood. The global search box for `phi` should be widened to at least (0.5, 0.999) to allow genuine global exploration.

---

### 15. Incomplete sentence and informal language in the text

Line 130 contains an incomplete, parenthetical question in the middle of the narrative: "(why we want to use log return instead of return?)" — this appears to be an unresolved author note left in the final submission. The text should either answer this question or remove the parenthetical.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/box_eval-2.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/box1_eval-3.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/m1if1-3.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/mif1-3_3.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/p1f1-3.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/pf1-3.rda`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/ford_params2.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/Tesla_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/Tesla_params1.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/TSLA_27Mar2017_24Mar2022.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project07/F_27Mar2017_24Mar2022.csv`
