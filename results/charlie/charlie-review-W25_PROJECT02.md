# Peer Review: W25 Project 02
## "Examining Explanatory Role of Momentum in Baseball"

---

## Summary

This project applies a POMP framework to investigate whether "momentum" — modeled as a latent AR(1) process — contributes meaningfully to game-to-game variation in the 2024 Detroit Tigers' runs scored. The primary model uses a Poisson observation model with an opponent-strength covariate, and is compared against a static-latent-skill null model via a likelihood ratio test. The project also presents a negative binomial sensitivity analysis. While the paper demonstrates commendable use of IF2/particle filtering infrastructure and raises an interesting question, the main conclusion (that momentum is statistically significant) is fragile: it holds only under the Poisson model and collapses entirely under the negative binomial alternative. The paper acknowledges this fragility but does not address its root causes — most importantly, a model specification error in the transition density, insufficient computational effort, missing profile likelihoods for parameters other than phi, no comparison to a non-mechanistic statistical benchmark, and a likelihood ratio test applied under conditions where Wilks' theorem may not hold.

---

## Major Issues

### 1. Typographical error in transition density equation invalidates the written model

The AR(1) transition is stated as $X_n = \phi X_{n-1} + \varepsilon_n$, yet the transition density displayed in Equation (1) is written as:

$$f_{X_n \mid X_{n-1}}(x_n \mid x_{n-1}) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(\phi x_{n-1})^2}{2\sigma^2}\right)$$

This density is not the correct Gaussian density for an AR(1) model; the numerator in the exponent should be $(x_n - \phi x_{n-1})^2$, not $(\phi x_{n-1})^2$. The Csnippet implementation in the code (`X = phi*X + d_X` with `d_X = rnorm(0, sigma)`) is in fact correct, so this is a typographical error in the manuscript rather than a code bug. Nevertheless, the mathematical expression as written is incorrect and describes a degenerate distribution with no dependence on $x_n$. The authors must correct the equation before publication to avoid misleading readers.

### 2. Missing non-mechanistic benchmark comparison

The POMP model is compared only against another POMP model (the static-skill variant), not against any non-mechanistic statistical baseline. A natural comparison would be an AR(1) or ARMA model directly on runs scored, or an auto-regressive negative binomial model. Without such a comparison, it is impossible to determine whether the mechanistic AR(1) latent-skill model captures structure that a simple time-series model cannot, or whether the apparent significance of momentum merely reflects that an AR(1) model fits any weakly autocorrelated count series better than a white-noise count model. Wheeler et al. (2024) note that none of the 32 papers they reviewed in the Haiti cholera literature performed such a benchmark comparison, and that the absence of a benchmark made it impossible to assess whether models captured meaningful structure. The same gap is present here. The authors should fit at least one non-mechanistic alternative (e.g., SARIMA, auto-regressive negative binomial) and report the comparison quantitatively.

### 3. Insufficient computational effort for global search

The global search uses only `nseq = 500` starting points (in `run_level = "final"`) with `Nmif = 100` re-optimization steps per guess. For a four-parameter model (gamma, phi, sigma, mu), 500 guesses is borderline; however, the log-likelihood spread of over 40 units reported in the paper indicates that the optimization has not converged reliably to the same maximum from different starting values. The mif2 calls in the global search also use only `Nmif = 100` iterations, which is less than the 150 used in the local search. A 40-unit spread in the global search results is a serious warning sign. The authors should increase the number of global restarts and/or IF2 iterations until the spread is reduced to a few log-likelihood units, and they should show replicated global searches reaching essentially the same maximum likelihood. As Wheeler et al. (2024) discuss, large improvements from increasing computational effort are common, and reported likelihoods from an under-converged search may substantially understate the true MLE, undermining the likelihood ratio test.

### 4. Likelihood ratio test conclusion is not robust and Wilks' conditions are not verified

The paper's primary conclusion — that momentum is statistically significant — rests on a likelihood ratio test (LRT) comparing the AR(1) Poisson model to the static Poisson model, yielding p < 0.001. However: (a) the LRT result reverses completely under the negative binomial measurement model, where the AR(1) and static models achieve essentially identical log-likelihoods (~-396.46 each); (b) the null hypothesis constrains phi = 0 and sigma = 0 simultaneously, placing the null on the boundary of the parameter space (sigma >= 0 is enforced via log-transformation). Wilks' theorem requires the null to be in the interior of the parameter space; when nuisance parameters are on the boundary, the chi-squared approximation is invalid and the true null distribution of the LRT statistic is typically a mixture of chi-squared distributions. The authors apply Wilks' approximation uncritically and do not acknowledge the boundary issue. The fragility of the conclusion across measurement models is acknowledged in the paper but not resolved; the boundary issue is not discussed at all.

### 5. Profile likelihoods computed only for phi; identifiability unresolved for other parameters

The paper presents a profile likelihood only for phi and concludes that the data are not very informative about phi given the flat likelihood surface. No profile likelihoods are computed for gamma, sigma, or mu. The global search scatter plots show substantial spread in all parameters, with a 40-unit log-likelihood range, which is consistent with poor identifiability. Without profile likelihoods for all key parameters, it is impossible to know whether gamma (the opponent-strength coefficient) or mu (baseline skill) are identified. Confidence intervals are not reported for any parameter. Wheeler et al. (2024) recommend computing profile likelihoods for all key parameters and using MCAP to obtain confidence intervals; the authors should do so, or at minimum report which parameters are and are not identifiable.

### 6. Inconsistency in parameter transformations between blinded.Rmd and Full_Code.Rmd

In the main report (blinded.Rmd), the parameter transformation is defined as:

```r
partrans <- parameter_trans(log = c("sigma", "mu"))
```

In Full_Code.Rmd, the same transformation for the AR1_pois model is defined differently in two places: the `rw_trans_models` function specifies `parameter_trans(log = c("sigma", "mu"))`, but the outer `partrans` object defined near the top of the code (used during global search) specifies only `parameter_trans(log = "sigma")` (line 182-184 of Full_Code.Rmd), omitting mu. This inconsistency means that the mu parameter is not constrained to be positive (i.e., is not log-transformed) in all parts of the optimization, which could lead to negative values of mu being explored and inconsistent optimization behavior. The authors should ensure that the parameter transformation is applied consistently throughout all optimization stages.

### 7. Data leakage in opponent-strength covariate construction

The covariate $Z_n$ is constructed using season-long statistics from the 2024 season, which means that $Z_n$ for Game 1 is computed using data from Games 2 through 162. The paper acknowledges this issue briefly in the Discussion/Limitations section but treats it as a minor concern. In a model whose primary purpose is causal inference about momentum, this data leakage is non-trivial: the covariate for any given game is informed by future information, which could induce spurious correlations or distort the estimated role of the latent state. This is particularly problematic if the goal were forecasting, but even for explanatory purposes it introduces a confound. The authors should either construct $Z_n$ using only information available before Game $n$ (e.g., rolling averages), or provide a more thorough argument for why the full-season average is a legitimate approximation.

---

## Minor Issues

### 8. Scatterplot in Model Fitting section uses global search results mislabeled as local

In blinded.Rmd, the scatterplot plotted in the chunk `scattplot_loc` (labeled under "Local Search") actually plots `Output[["results_glob"]]` — the global search results — not the local search results. The code reads:

```r
results <- Output[["results_glob"]]
```

This appears before the global search section header, so the figure is placed in the narrative as if it follows the local search. The caption should clearly label this as global search output, or the code should be corrected to use local search results for the local search section.

### 9. Bug in opponent-strength fallback condition

In both blinded.Rmd and Full_Code.Rmd, the fallback logic for computing opponent strength has a parenthesis error:

```r
if (nrow(opp_pitch_games>0)) {
```

The `> 0` comparison is inside `nrow()`, which means it always evaluates to `nrow(TRUE)` = 1, which is always truthy. The intended logic is `nrow(opp_pitch_games) > 0`. As a result, the fallback branch (using all opponent games rather than pitcher-specific games) is never executed, and for starting pitchers with no non-Tigers games in the dataset, `mean()` would be called on an empty data frame, potentially producing `NaN`. The authors should verify that no `NaN` values appear in `det_games$opp_strength` and correct the condition.

### 10. Model equation presentation uses a non-standard density form

Equation (2) presents the Poisson probability mass function as a density $f_{R_n | X_n, Z_n}(\cdot)$, written using the notation $\Prb{R_n = r_n \mid \ldots}$. More substantively, the model parameters are presented without a discussion of their prior ranges or biological/domain plausibility. For instance, no argument is made for why $\phi$ should be constrained to the explored range of $[-0.25, 1.5]$ in the global search, or why sigma values above 0.6 are excluded. Expanding the search bounds slightly and verifying robustness to those bounds would strengthen the analysis.

### 11. Initialization is fixed at $X_0 = 0$ with no sensitivity analysis

The latent state is initialized at $X_0 = 0$ ("neutral momentum") without any justification that this is appropriate for the start of the baseball season, or analysis of sensitivity to this choice. While the AR(1) process will converge toward its stationary distribution over time, the first several games' likelihoods will be affected by this initialization. The authors should either estimate the initial condition or demonstrate that the likelihood and parameter estimates are insensitive to reasonable alternative values of $X_0$.

### 12. "Poor man's profile likelihood" is presented without explanation of its limitations

The poor man's profile for phi (plotting loglik vs. phi from the global search without re-maximizing over nuisance parameters for each phi value) is presented in the main text. The authors correctly call it a "poor man's profile" but do not explain to the reader why it differs from a proper profile likelihood. Given that the paper later presents a proper profile likelihood (in Full_Code.Rmd), the poor man's version in the main text is superfluous and potentially misleading — it can show a flat surface even when a proper profile would reveal a peak — and should be removed or supplemented by the proper profile in the narrative.

### 13. No RNG seed reported for global search initial conditions in blinded.Rmd

The main report does not display the set.seed calls used before the global search. While the code in Full_Code.Rmd does set seeds, readers of blinded.Rmd cannot verify reproducibility. The seeds used in the computation should be reported, along with the number of particles and iterations, so that another researcher could attempt to reproduce the key log-likelihood values.

### 14. Wilks' theorem applied without checking whether the chi-squared approximation is reasonable

Beyond the boundary issue (Major Issue 4), the LRT with df = 2 may have poor finite-sample calibration on a time series of length 162. No parametric bootstrap or simulation-based calibration of the null distribution is performed. Given that the conclusion of the paper rests entirely on the LRT p-value, the authors should at minimum acknowledge the small-sample concern and consider a simulation-based assessment of the null distribution of the test statistic.

### 15. Missing sessionInfo() and package versions

The supplement does not include `sessionInfo()` output or a pinned package environment. The `pomp` package API has changed across versions and results may not be reproducible on current CRAN releases without version pinning. The authors should include `sessionInfo()` at the end of Full_Code.Rmd, or use `renv` to lock package versions, consistent with best practices for POMP code supplements (see code-supplement-checklist-pomp.md).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project02/Full_Code.Rmd`
