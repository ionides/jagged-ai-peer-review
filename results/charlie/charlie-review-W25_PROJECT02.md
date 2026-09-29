# Peer Review: W25 Project 02
## "Examining Explanatory Role of Momentum in Baseball"

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) with particle filter likelihood evaluation |
| **R packages used** | pomp, tidyverse, ggplot2, foreach, doFuture |
| **Code publicly available** | Partial — Full_Code.Rmd provided in submission folder |
| **Data publicly available** | Yes — mlb-2024-asplayed.xlsx included |
| **Benchmark comparison included** | No |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2 + replicated pfilter used correctly; but global search has only 5 starting points |
| 2 | Benchmark comparison | ✗ | No ARIMA or IID comparison |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihood values reported; no AIC or SE context for model comparison |
| 4 | Model diagnostics | ~ | ESS and trace plots shown; no conditional log-likelihood per game |
| 5 | Parameter identifiability and uncertainty | ✗ | Profile likelihood computed but not shown in main report; no CIs stated in text |
| 6 | Computational adequacy | ✗ | Full_Code.Rmd shows run_level="explore" (5 global starting points) |
| 7 | Forecast methodology | N/A | No forecasts generated |
| 8 | Model variations and nested comparisons | ~ | AR1 vs. static nested comparison is sound; Poisson vs. NegBin explored |
| 9 | Stochasticity | ~ | Process noise present; Poisson observation model lacks overdispersion |
| 10 | Reproducibility and extendability | ~ | Code present; no sessionInfo; parameter transformation inconsistency across files |
| 11 | Corroboration with scientific knowledge | ~ | phi → -1 finding noted but not interpreted |
| 12 | Measurement model specification | ~ | Poisson and NegBin compared; conditional distribution literature acknowledged as sparse |
| 13 | Initial conditions | ~ | X_0=0 fixed without sensitivity analysis |

---

## Summary

The paper applies a POMP framework to model game-level batting performance for the 2024 Detroit Tigers, treating latent momentum as an AR(1) process that modulates a Poisson (or negative binomial) observation model for runs scored. The primary research question — whether momentum significantly contributes to offensive performance variation — is addressed through a likelihood ratio test comparing the AR1 model against a static (no-momentum) nested model.

**Strengths:** The research question is well-motivated and baseball's structure (discrete games, 162-game season, separation of roles) is a sensible setting for a POMP analysis. The covariate for opponent pitching quality is thoughtfully constructed. The paper correctly uses replicated pfilter calls with logmeanexp for likelihood evaluation, and provides iterated filtering trace plots. The sensitivity analysis using a negative binomial measurement model is a meaningful contribution.

**Weaknesses:** A mathematical error in the stated transition density equation (missing $x_n$ in the exponent) undermines confidence in the model presentation. The LRT on which the main conclusion rests is statistically invalid because the null hypothesis ($\sigma = 0$) lies on the boundary of the parameter space, violating the regularity conditions for Wilks' theorem. The conclusion that "momentum is a material factor" is asserted in the Discussion despite the negative binomial sensitivity analysis failing to reject the null — an internal contradiction that is not resolved. The global optimization code in Full_Code.Rmd uses only 5 starting points (explore mode), which is insufficient to identify the MLE on an acknowledged complex likelihood surface. The reported maximum log-likelihoods are also suspect due to a code bug that duplicates the global search results vector instead of combining local and global results.

---

## Major Issues

### 1. Mathematical error in the transition density equation

Equation (1) in the Model section states the conditional density as:

$$f_{X_n \mid X_{n-1}}(x_n \mid x_{n-1}) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(\phi x_{n-1})^2}{2\sigma^2}\right)$$

This is incorrect. For the AR(1) model $X_n = \phi X_{n-1} + \varepsilon_n$ with $\varepsilon_n \sim N(0, \sigma^2)$, the correct density is:

$$f(x_n \mid x_{n-1}) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(x_n - \phi x_{n-1})^2}{2\sigma^2}\right)$$

The term $x_n$ is entirely absent from the exponent in the written equation. The exponent as written does not depend on $x_n$ at all, making the expression a constant with respect to $x_n$ (not a valid density). The Csnippet implementation is correct (`X = phi*X + rnorm(0, sigma)`), so this is a presentation error, but one that calls into question the care taken in presenting mathematical content. **Fix:** Correct Equation (1) to include $(x_n - \phi x_{n-1})^2$ in the numerator of the exponent.

### 2. LRT boundary violation — chi-squared approximation is not valid

The likelihood ratio test constrains $\sigma = 0$ under the null hypothesis. The parameter $\sigma$ is defined to be non-negative ($\sigma \geq 0$ via log-transform), so the null value $\sigma = 0$ lies on the boundary of the parameter space. Wilks' theorem requires the null value to lie in the interior of the parameter space; this condition is violated. The correct asymptotic null distribution in this case is a mixture of chi-squared distributions (specifically, a 50-50 mixture of $\chi^2_1$ and $\chi^2_2$ for the one-sided $\sigma$ constraint), not $\chi^2_2$. Using $\chi^2_2$ makes the test anti-conservative — it will reject the null too often — and the reported p-value of $< 0.001$ cannot be taken at face value. **Fix:** Acknowledge the boundary issue, use a simulation-based null distribution, or at minimum note this as a limitation and report the p-value under the appropriate mixture distribution.

### 3. Duplicate vector in maximum log-likelihood computation

In the Conclusion section, the maximum log-likelihoods used for the LRT are computed as:

```r
MLL$pois$AR1 <- max(c(Output_AR1_pois[["results_glob"]]$loglik,
                      Output_AR1_pois[["results_glob"]]$loglik))
```

The same `results_glob` vector is concatenated with itself. This is a no-op — `max(c(x, x)) = max(x)` — and the local search results (`results_loc`) are never included. The local search uses 150 mif2 iterations from the hand-selected starting point, while the global search uses only 100 iterations from random starts. If the local search found a higher log-likelihood (a plausible outcome given the narrow, well-initialized starting point), the LRT statistic and p-value could both be incorrect. The same pattern appears for all four models. **Fix:** Replace the duplicated `results_glob` with `c(results_loc$loglik, results_glob$loglik)` to ensure the global maximum is correctly identified.

### 4. Conclusion contradicts the sensitivity analysis

The Discussion section opens with: "The analysis of our primary model led us to conclude that momentum is a material factor in explaining team-level offensive performance fluctuation in Major League Baseball." However, the paper's own sensitivity analysis (Section: Alternate Models) shows that under the negative binomial observation model, the AR1 and static models achieve "nearly identical maximum log-likelihoods of $\approx -396.46$," and the null hypothesis is not rejected. The paper presents two models that yield opposite conclusions (reject vs. fail to reject) and then asserts the affirmative conclusion without reconciling this contradiction. The evidence is model-dependent and the paper's primary claim is not supported by the body of its own results. **Fix:** Revise the Discussion to accurately reflect that the evidence for momentum is sensitive to the choice of measurement model, and present a more tentative conclusion.

### 5. Insufficient global search computational effort

`Full_Code.Rmd` sets `run_level <- "explore"`, which yields `nseq = 5` global starting points. The paper itself reports "a range of over 40 log-likelihood units" in the global search results and describes "a complicated likelihood surface" with identifiability issues. On a complex 4-parameter surface, 5 random starting points is not sufficient to characterize the global maximum. The acknowledged log-likelihood spread of 40 units suggests some starts are far from the true optimum, meaning the best-found likelihood across 5 starts is not reliable as an MLE estimate. This is course-confirmed (CC-Yes) Error 1.8 (missing convergence evidence via multiple searches reaching consistent likelihoods). **Fix:** Increase the number of global starting points substantially (course standard: nseq=100 at run_level=3), confirm that multiple runs converge to the same terminal log-likelihood, and re-run the LRT with the correctly identified MLE.

### 6. Look-ahead bias in the covariate $Z_n$

The opponent strength covariate $Z_n$ is constructed as the average number of runs allowed by the opposing starting pitcher across all their non-Tigers games in the 2024 season. This includes games played after game $n$. The Discussion section acknowledges this limitation but frames it as unlikely to matter because "it is unlikely that the Tigers' Game $n$ performance meaningfully influences their opponent's future games." However, the issue is not causal influence from the Tigers but the use of future information when constructing a predictor for game $n$. Using full-season statistics as a time-$n$ covariate violates temporal causality, can introduce systematic bias in parameter estimation (the opponent's season-end ERA is a better predictor than their current ERA), and means the model cannot be deployed in real time. **Fix:** Restrict $Z_n$ to statistics from games played strictly before game $n$ (using a running mean), or at minimum quantify the magnitude of the look-ahead bias by comparing parameter estimates under the current and causal covariate definitions.

---

## Computational and Diagnostic Assessment

**Convergence:** Iterated filtering trace plots are shown for the local search (20 runs, 150 mif2 iterations) and the log-likelihood panel shows rapid initial increase followed by stabilization — a favorable convergence pattern. However, the global search is conducted with only 5 random starting points (explore mode), providing insufficient evidence of global convergence. The 40-unit log-likelihood range reported in the global results is inconsistent with convergence to a well-defined MLE.

**Particle filter:** ESS is monitored and reported. The minimum ESS in the initial particle filter run is presented and described as "relatively high," which is appropriate commentary. Np=5000 is used for pfilter likelihood evaluation, and 10 replicates are aggregated via logmeanexp — this is correct procedure per course conventions.

**Conditional log-likelihoods:** Per-game conditional log-likelihoods are not plotted. Such a plot would identify specific games where the model fails (e.g., the 15-run outlier game, shutout games), potentially informing model revision.

**Profile likelihoods:** A formal profile likelihood for $\phi$ is computed in `Full_Code.Rmd` (with CI cutoff at the Wilks 95% threshold), but this is not shown in the main report. The report shows only a "poor man's profile" filtered to $\log L > \max - 10$, without reporting the confidence interval for $\phi$. Given that $\phi$ is the key parameter for the research question, the CI should be stated explicitly.

**Computational scale:** Total CPU time is not reported. Run settings suggest moderate computational effort (Np=5000, 20 local runs × 150 iterations, 5 global starts × 100 iterations), but the explore-mode global search is inadequate.

---

## Reproducibility Assessment

**Code availability:** `Full_Code.Rmd` is provided along with precomputed RDS output files. The analysis can largely be reproduced from the provided materials.

**Final parameters:** MLE parameter vectors are archived in the RDS files, allowing the likelihood to be re-evaluated without re-running optimization.

**Model-code consistency:** The Csnippet implementations match the stated model equations (subject to the notation issue in Equation (1) noted above). The measurement model in code is consistent between dmeasure and rmeasure.

**Package versions:** No `sessionInfo()` output or `renv` lockfile is provided. The `pomp` package has undergone API changes across versions; without version documentation, exact reproduction is not guaranteed. The `pomp` and `ggplot2` versions should be documented.

**Parameter transformation inconsistency:** `blinded.Rmd` uses `partrans = parameter_trans(log = c("sigma", "mu"))` (constraining both $\sigma > 0$ and $\mu > 0$), while `Full_Code.Rmd`'s main pomp object definition uses only `parameter_trans(log = "sigma")`. The mif2 optimization in `Full_Code.Rmd` applies `parameter_trans(log = c("sigma", "mu"))` via `rw_trans_models()`, so the actual optimization is consistent with the report's description, but the pomp object itself is created with a different transformation. These inconsistencies should be resolved.

---

## Minor Issues

- **Profile likelihood omitted from main report:** The formal profile likelihood for $\phi$ (with the Wilks 95% CI cutoff shown as a horizontal reference line) is computed in `Full_Code.Rmd` but appears only in the full code, not in the main report. The key parameter's confidence interval should appear in the main analysis, not only in a supplement.

- **No confidence intervals stated in the text:** The Discussion and Conclusion sections report only point estimates (MLL $\approx -397.81$ vs. $-437.50$) without confidence intervals for any parameter. The identifiability concerns flagged by the authors themselves make CIs especially important.

- **No non-mechanistic benchmark:** The nested comparison (AR1 vs. static POMP) establishes that the AR1 extension adds explanatory power within the POMP framework. It does not establish whether the POMP framework itself captures meaningful structure — a comparison against an ARIMA or IID negative binomial baseline would provide this context. Per course conventions, this is not required, but its absence limits the interpretability of the absolute likelihood values.

- **$\phi \to -1$ finding not investigated:** The local search converges to $\phi \approx -1$, implying that good offensive performance in one game predicts poor performance in the next. The paper notes this but provides no sports-domain interpretation and does not investigate whether the result is stable across the global search or specific to the initial starting point.

- **Single initial condition $X_0 = 0$ not evaluated for sensitivity:** The momentum at the start of the season is fixed at zero without assessing sensitivity. For a 162-game series, early-game fit can affect parameter estimates.

- **Pairwise scatterplot in the "Local Search" section uses global results:** The code block labeled as showing parameter correlations for the local search (`results <- Output[["results_glob"]]`) actually references `results_glob`, the global search results. The figure is placed and described in the Local Search context but displays global search output. This mislabeling is confusing.

- **`nrow(opp_pitch_games > 0)` is non-idiomatic:** In the data processing loop (blinded.Rmd line 88 and Full_Code.Rmd line 52), the condition `if (nrow(opp_pitch_games > 0))` applies `> 0` to the entire data frame before calling `nrow()`. While this happens to produce the correct behavior in R (because `nrow()` on the resulting logical object returns the original row count), it triggers implicit warnings on non-numeric columns and is not idiomatic. The intent is clearly `if (nrow(opp_pitch_games) > 0)`.

- **Comment error in blinded.Rmd:** The comment on the `partrans` block reads "log(mu) represents expected runs with no momentum against league-average pitching." This is imprecise: $\mu$ is already the log-expected runs (it appears inside `exp()` in the measurement model), so the comment should say "$\mu$ represents the log-expected runs."

---

## Recommendation

**Major Revision.** The paper addresses an interesting question with a well-suited modeling framework, and the writing is generally clear. However, several methodological issues must be addressed before the analysis can support its conclusions: the LRT boundary violation undermines the statistical test on which the main conclusion rests; the duplicated-vector bug in the MLL computation means the reported MLE and LRT statistic may be incorrect; and the conclusion stated in the Discussion is at odds with the sensitivity analysis. The global optimization effort should be increased and the formal profile likelihood for $\phi$ should appear in the main report. Addressing these issues may well change the paper's primary finding, but would place it on a sound methodological footing.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project02/Full_Code.Rmd`
