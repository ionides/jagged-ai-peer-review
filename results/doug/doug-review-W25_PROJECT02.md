# Peer Review: Examining Explanatory Role of Momentum in Baseball
**Reviewer:** Doug  
**Semester/Project:** W25 Project 02

---

## Summary

This project proposes a POMP model to investigate whether team-level "momentum" contributes to game-to-game variation in the 2024 Detroit Tigers' batting performance. The latent state evolves as a Gaussian AR(1) process, and the observation model is Poisson (or negative binomial) with a covariate for opponent pitching quality. A likelihood ratio test comparing the AR(1)-latent model to a static (no momentum) submodel is used as the primary inferential tool. The paper's main finding — that momentum provides statistically significant explanatory power — rests entirely on the Poisson observation model and is directly contradicted by the negative binomial sensitivity analysis. Beyond this instability, several methodological gaps undermine the validity and interpretability of the reported results: the global MLE for phi is approximately zero with large process noise, suggesting the latent AR(1) process is acting as an overdispersion device rather than capturing genuine autocorrelation; no non-mechanistic benchmark is provided; and the profile likelihood computed in the supplementary code is seeded from a region that is approximately 40 log-likelihood units below the global optimum, rendering it uninformative.

---

## Major Issues

### 1. Absence of a non-mechanistic benchmark

The mechanistic POMP model is never compared against any non-mechanistic statistical baseline (e.g., an ARMA model for runs, or a negative binomial regression on opponent strength alone). Without such a comparison it is impossible to determine whether the AR(1) latent structure captures meaningful serial dependence rather than simply fitting the marginal distribution of runs better than the Poisson assumption permits. Wheeler et al. (2024, §Benchmark comparison) demonstrate that such comparisons are essential: several epidemic models in their review failed to beat a simple auto-regressive negative binomial when the comparison was made quantitatively. An appropriate benchmark here would be a negative binomial GLM or time-series model with the opponent-strength covariate; the authors should compare log-likelihoods on the same observation scale.

### 2. Global MLE reveals the latent AR(1) process captures overdispersion, not momentum

Inspection of the saved artifact (`Output_AR1_pois.RDS`) reveals that the Poisson AR(1) global MLE is phi = -0.012 and sigma = 0.574. A phi value near zero means the latent state has virtually no autocorrelation; the large sigma value means the process is essentially i.i.d. noise. The 40-unit log-likelihood improvement over the static Poisson model is therefore attributable to the latent state absorbing the overdispersion that the Poisson distribution cannot accommodate directly, not to momentum dynamics. This interpretation is confirmed by the negative binomial sensitivity analysis: when the observation model includes a dispersion parameter k that can handle overdispersion directly, the AR(1) model achieves essentially identical log-likelihood to the static model (both approximately -396.46, difference < 0.01). The paper does not report or discuss the global MLE parameter values (phi, sigma, gamma, mu) anywhere in the main text, making it impossible for readers to reach this conclusion independently. The authors acknowledge the model sensitivity issue but do not recognize that the Poisson result likely reflects a measurement-model artifact.

### 3. Primary scientific conclusion is contradicted by the sensitivity analysis and is likely invalid

The paper concludes (Conclusion section) that "momentum does provide explanatory power of a team's offensive performance" based on the Poisson LRT (p < 0.001). However, the negative binomial LRT produces p = 1 (LRT statistic = -0.005, essentially zero). The paper treats the negative binomial result as a sensitivity check and notes the contrast, but does not acknowledge the most natural interpretation: the apparent momentum signal under Poisson disappears entirely when the observation model is correctly specified for count overdispersion. Given that baseball analysts cited in the paper have established that the negative binomial fits runs-per-game better than the Poisson distribution, the primary Poisson-based conclusion is the less credible of the two results. The paper should reverse its framing: the default conclusion should be that momentum is not detectable, with the Poisson result explained as an artifact.

### 4. Mathematical error in the AR(1) transition density (Equation 1)

Equation (1) writes the conditional density as:

$$f_{X_n \mid X_{n-1}}(x_n \mid x_{n-1}) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(\phi x_{n-1})^2}{2\sigma^2}\right)$$

The exponent should be $-(x_n - \phi x_{n-1})^2 / (2\sigma^2)$. As written, the equation expresses $X_n \mid X_{n-1} \sim \mathrm{N}(0, \sigma^2 / \phi^2)$, which is independent of $x_{n-1}$ (i.e., no memory). The Csnippet implementation is correct (`X = phi*X + d_X` where `d_X ~ N(0, sigma)`), so this is a typographical error in the mathematical presentation rather than a code error, but it misrepresents the model to readers.

### 5. Profile likelihood seeded from locally optimal region and is uninformative

In `Full_Code.Rmd`, the profile over phi is constructed by reading the parameter box from a CSV file that at the time of the profile run contained only the initial pfilter result (loglik ≈ -472) and local search results (loglik ≈ -437), not the global search results (loglik ≈ -397.7). The profile box is consequently restricted to sigma ∈ [0.003, 0.010], which is far from the global MLE sigma = 0.574. All 40 phi grid points produce log-likelihoods around -437.5, the profile curve is entirely flat, and the chi-squared CI cutoff (-437.5 - 1.92 = -439.4) encompasses all 40 grid points — giving an uninformative "95% CI" of phi ∈ [-0.25, 0.99], virtually the entire search range. The profile's maximum log-likelihood (-437.5) is approximately 40 units below the global maximum (-397.7), meaning the profile never probed the region of the likelihood surface that actually matters. The authors do not report this profile in the main paper but should correct it for the supplementary analysis and note its limitations.

### 6. Global search initialization anti-pattern

In `Full_Code.Rmd`, the global search is launched using:

```r
mf1 <- mifs_local[[1]]
mf1 |> mif2(params=c(guess)) |> mif2(Nmif=100) -> mf
```

`mf1` is a previous `mif2` result object, not the base `pomp` object. Passing a prior `mif2` result as the first argument to `mif2()` causes the global replicates to inherit the cooling schedule from `mf1`, which has already cooled to near its final state after 150 iterations. Each global replicate therefore starts with a nearly frozen perturbation schedule, making the "global search" effectively a local search seeded near the local optimum rather than a genuine exploration of the parameter box. The fix is to replace `mf1` with the base `runsPOMP[["AR1_pois"]]` object in the global loop, ensuring each replicate begins with a fresh, uncooled IF2 chain.

### 7. Likelihood ratio test at the boundary of the parameter space

The null hypothesis is $H_0: \phi = 0, \sigma = 0$. Since sigma is constrained to be non-negative, $\sigma = 0$ is on the boundary of the parameter space. Wilks' theorem requires the null hypothesis to be an interior point; when the null is on the boundary, the asymptotic distribution of $2(l_1 - l_0)$ is not chi-squared(2) but a mixture of chi-squared distributions (e.g., approximately $\frac{1}{4}\chi^2_0 + \frac{1}{2}\chi^2_1 + \frac{1}{4}\chi^2_2$ for a two-parameter boundary test). For the Poisson model, the LRT statistic is approximately 79.5, so the p-value is near zero under any reasonable distribution and the qualitative conclusion for that model is unaffected. However, the authors should acknowledge the boundary condition and note that the chi-squared(2) approximation is an approximation rather than an exact result.

---

## Minor Issues

### 8. No parameter estimates or confidence intervals reported in the main text

The main paper reports only log-likelihood values and LRT p-values; it does not report the MLE parameter estimates (phi, sigma, gamma, mu) for any model. Without these values, readers cannot verify claims about the model's behavior or assess whether parameters have scientifically plausible magnitudes. For instance, the global MLE gamma ≈ 0.087 indicates a positive association between opponent runs-allowed and Tigers' runs scored, which is the expected direction, but this is never stated in the paper. Profile likelihoods for gamma, mu, and sigma are absent; only a "poor man's profile" scatter for phi is presented.

### 9. Computational details absent from the main text

The number of particles, number of IF2 iterations, and number of global search replicates are not reported anywhere in the main paper. The paper notes that "the particle filtering algorithm is computationally intensive" and that results were precomputed, but does not state that the global search used Np = 5000 particles, 500 starting points, and approximately 250 IF2 iterations per replicate. These details are necessary for readers to assess the adequacy of the computational effort and to reproduce the analysis.

### 10. Covariate construction uses future data (acknowledged but insufficiently quantified)

The opponent-strength covariate $Z_n$ uses games involving the opposing pitcher from the full 2024 season, including games played after Game $n$. The paper acknowledges this in the Discussion section but does not quantify the extent of the leakage or assess whether it affects the results. A more rigorous approach would construct $Z_n$ using only the opposing pitcher's games from prior seasons or from the portion of the 2024 season preceding Game $n$.

### 11. Minor coding bug in data processing

In `blinded.Rmd` (and `Full_Code.Rmd`), the condition `if (nrow(opp_pitch_games>0))` should be written `if (nrow(opp_pitch_games) > 0)`. The current form applies element-wise comparison to the entire data frame, creating a logical data frame, and then counts its rows — which happens to equal the number of rows of the original data frame. The code is accidentally correct but fragile and misleading.

### 12. Redundant concatenation in MLL calculation

In the Conclusion section, the maximum log-likelihood is computed as:

```r
max(c(Output_AR1_pois[["results_glob"]]$loglik, Output_AR1_pois[["results_glob"]]$loglik))
```

The same vector is concatenated with itself twice, which is harmless but suggests the intent was to combine local and global search results (which would require using `results_loc` for one of the two vectors).

### 13. Parameter transformation inconsistency between displayed and executed code

`blinded.Rmd` defines `partrans <- parameter_trans(log = c("sigma", "mu"))`, but `Full_Code.Rmd` defines the standalone `partrans` as `parameter_trans(log = "sigma")` (mu excluded). The mif2 calls in `Full_Code.Rmd` use `mif_sets$trans_model` (which correctly includes both sigma and mu in the log transform), so the executed analysis is internally consistent. However, the displayed code in `blinded.Rmd` does not correspond to what `Full_Code.Rmd` actually runs for the `pomp()` object instantiation.

### 14. Local search phi convergence not reconciled with global result

The paper notes that the local search has phi converging to approximately -1 and attributes this to "a lack of stability of the random walk." The global search finds phi ≈ -0.012 with sigma ≈ 0.574. The paper acknowledges the discrepancy but does not explain it mechanistically: the local search initialized at sigma = 0.005 finds a very different region of the likelihood surface than the global search. This tension is not resolved in the text.

### 15. Poor man's profile used for pairwise scatter (local search)

The pairwise scatter plot labeled "Pairwise Scatterplot of Log-Likelihood and Parameters" in the Local Search section actually uses `results_glob` (the global search results), not `results_loc` (the local search results), as indicated by the code `results <- Output[["results_glob"]]` preceding the `pairs()` call. The section heading says "Local Search" but the figure is from the global search.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project02/Full_Code.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project02/Output_AR1_pois.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project02/Output_AR1_nbin.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project02/Output_static_pois.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project02/Output_static_nbin.RDS`
