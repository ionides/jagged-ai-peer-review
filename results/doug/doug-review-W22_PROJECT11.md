# Peer Review: Hungarian Chickenpox POMP Model Analysis
**Semester:** W22 | **Project:** 11

---

## Summary

This project fits a modified SEIR-V (susceptible–exposed–infectious–recovered with vaccination) POMP model to weekly national chickenpox case counts from Hungary (2005–2014). The authors incorporate time-varying population and birth-rate covariates, term-time seasonality, and extra-demographic stochasticity following the King measles template. Strengths include a clear disease motivation, a genuine attempt at vaccination modeling, and use of iterated filtering (mif2) with a large particle count (Np=10,000) for the local search. However, the analysis has several critical methodological and computational deficiencies: the R compartment update equation violates population conservation; the global search box excludes the MLE by a factor of 10–60 in several parameters; the global search is seeded from a previous mif2 result (anti-pattern) rather than from the base pomp object; no non-mechanistic benchmark is provided; no profile likelihoods are computed; and several estimated parameters are biologically implausible. The paper's main conclusion — that a modified SEIR-V model successfully captures Hungarian chickenpox seasonality — is not adequately supported given these unresolved issues.

---

## Major Issues

### 1. Population conservation violated in the R compartment update

The rprocess Csnippet sets `R = pop - S - E - I + vac`. After each Euler step, the total compartment count is:

```
S_new + E_new + I_new + R_new = (S_new + E_new + I_new) + (pop - S_new - E_new - I_new + vac) = pop + vac
```

The population therefore grows by `vac` at every time step, so the model has no fixed total population. This is incorrect: vaccinated individuals are already counted in the S compartment (they are subtracted from S before R is assigned), so adding `vac` again to the right-hand side of R double-counts them. The standard remedy is either (a) to set `R = pop - S - E - I` and handle vaccination as an additional flow from S into R without adding it to the population denominator, or (b) to track R as a state via differential equations `R += trans[4] + vac - mu*R` and avoid the residual assignment. This error inflates R at every step, distorting the effective susceptible fraction and all downstream parameter estimates.

### 2. Global search box severely misaligned with the true MLE

The global search specifies `R0 ∈ [6,14]`, `gamma ∈ [60,170]`, `iota ∈ [0,0.4]`, and `vr ∈ [0.1,0.3]`. Inspection of the saved artifact `global_search_1.rds` reveals that the best-likelihood parameter set has R0=202, gamma=922, iota=−0.43, and vr=0.62 — all far outside the declared box. The IF2 chains drifted to these values from within the box, which means the search does not actually explore the stated box but rather uses it as an ineffectual starting distribution. Furthermore, only 1 out of 400 replicates reached within 5 log-likelihood units of the global best, and 2 within 50 units. Presenting this as a "global search" is misleading: the result represents a single accidental escape from the box, not systematic global coverage (Wheeler et al. 2024, §Computational adequacy).

### 3. Global search initialized from a previous mif2 result (anti-pattern)

The code sets `mf1 <- mifs_local[[1]]` and then calls `mf1 %>% mif2(params=c(guess, fixed_params))` for each global replicate. This passes a previous IF2 chain object as the first argument rather than the base pomp object. Because `mf1` has already run 400 IF2 iterations, its internal cooling schedule is at or near its asymptotic state. Each global replicate starts from this near-expired cooling schedule, so the new random starting parameters receive very few functional IF2 iterations before perturbations decay to near zero. The "global search" therefore cannot genuinely explore the parameter space from the declared box (see `pomp-global-search-init-audit` skill). The fix is to pass the base pomp object (`m1`) as the first argument.

### 4. Global search performs worse than local search by 77 log-likelihood units

The best global search log-likelihood is −3478.08 versus the local search best of −3400.71, a gap of 77.4 units. The paper correctly notes this inconsistency but attributes it vaguely to "computational complexity." The real causes are the box misalignment (Issue 2) and the anti-pattern initialization (Issue 3). Because the global search fails to outperform the local search, its "best parameters" (R0=202, gamma=922, vr=0.62) are not reliable MLEs and should not be presented in the Global Model Evaluation table or used to generate simulations. All comparisons between local and global fit are therefore invalid.

### 5. Negative iota in the best-fit global parameter set; potential NaN in force of infection

The global MLE has iota=−0.43. The force-of-infection term is `foi = beta * pow(I + iota, alpha) / pop`. When I is small (near zero) and iota=−0.43, the argument `I + iota` is negative. Because alpha is non-integer (approximately 0.87 in the global MLE), `pow(negative, non-integer)` is `NaN` in standard C, which would produce degenerate particle weights and collapse the effective sample size. That 71 of 400 global search replicates have negative iota indicates the parameter transformation is not constraining iota to be non-negative. The transformation `partrans` does not include `log` for `iota`, so iota is on the natural (unrestricted) scale and can go negative. The model should constrain iota > 0 (e.g., via a log transform in `partrans`) or guard against negative values in the Csnippet.

### 6. No non-mechanistic benchmark comparison

The project provides no comparison of the SEIR-V model against any non-mechanistic statistical baseline such as ARIMA, SARIMA, or auto-regressive negative binomial. Without a benchmark, it is impossible to assess whether the mechanistic model captures meaningful epidemiological structure beyond what a simple statistical model achieves. Wheeler et al. (2024) note that among 32 published cholera models, none performed this benchmark comparison, and that an auto-regressive negative binomial baseline revealed that some models were actually outperformed by the simple benchmark.

### 7. No profile likelihoods computed for any parameter

No profile likelihoods are reported for any of the 11 estimated parameters. The project presents a "poor man's profile" for vr by filtering global-search results, but this is a scatter plot of unconstrained optimization results, not a genuine profile likelihood. As noted in the `pomp-pseudo-profile-audit` skill, applying a chi-squared threshold to such a scatter yields no valid confidence interval. Without proper profile likelihoods, the identifiability of R0, gamma, sigma, rho, and the vaccination rate cannot be assessed, and no confidence intervals can be reported (Wheeler et al. 2024, §Parameter identifiability and uncertainty).

### 8. Implausible parameter estimates not adequately interrogated

The local search MLE gives R0=82.7. The literature consensus for chickenpox is R0≈9–10 (as the authors themselves cite). An R0 approximately 8× the literature value is a potential sign of model misspecification — specifically, the population-conservation error (Issue 1) and the term-time seasonality windows (see Issue 9) may jointly push R0 far beyond plausible values. The paper mentions the high R0 in the Discussion but offers no quantitative investigation, does not examine whether removing vaccination or changing seasonality brings R0 to a plausible range, and does not flag implausible parameter values as a formal limitation. Wheeler et al. (2024) recommend interpreting implausible MLEs as evidence of model misspecification. Recovery time implied by gamma=84 is 1/84 years ≈ 4.3 days, which is within range for chickenpox, but sigma=113 implies an incubation period of 1/113 years ≈ 3.2 days, which is short given the known 10–21 day incubation period for chickenpox.

### 9. Term-time seasonality windows copied from UK measles without verification

The Csnippet uses the same day-of-year windows for school terms (`t>=7&&t<=100`, `t>=115&&t<=199`, `t>=252&&t<=300`, `t>=308&&t<=356`) as the King measles case study for England and Wales. These windows correspond to the English school calendar, not the Hungarian school calendar. Hungarian school terms differ both in timing and structure. Using the wrong seasonal windows misspecifies the transmission forcing function, which will distort estimates of the amplitude parameter and interact with R0. The authors should identify the actual Hungarian school-term dates and update the seasonality windows accordingly.

---

## Minor Issues

### 10. Initial conditions fixed in global search but estimated in local search

The global search fixes `S_0`, `E_0`, `I_0`, and `R_0` to values taken from the local search result (`fixed_params <- c(...)`), while the local search estimates these via `ivp(0.02)`. This inconsistency means the global and local searches do not optimize the same objective, and their log-likelihoods are not directly comparable even setting aside the convergence issue. The treatment of initial conditions should be consistent across searches.

### 11. Outlier removal without formal justification

The authors remove six data points from the time series (`row_idx %in% c(122,159,469,486,487,493)`) as "possible data entry errors," but provide no quantitative criterion (e.g., exceeding 5 SDs from a rolling mean) for identifying them as outliers. The six points are visually highlighted as circles in the plot but no table is given. Removing data points without a pre-specified rule is a form of data dredging. At minimum, the analysis should be shown to be robust to whether these points are included or excluded.

### 12. Measurement model uses normal approximation to negative binomial

The `dmeasure` Csnippet evaluates `pnorm(cases+0.5, m, sqrt(v)+tol, ...)` where `v = m*(1-rho + psi^2*m)`, a normal approximation to the negative binomial. Similarly, `rmeasure` uses `rnorm`. For small expected counts this approximation can produce substantial probability mass below zero and is less accurate than the exact negative binomial. The model should use `dnbinom_mu` / `rnbinom` for robustness, particularly since case counts in low-season weeks may be small.

### 13. rho initialized and reported at implausible values

The paper states rho=0.43 was computed as "total cases / total births over the ten-year period," which is not a valid estimate of the reporting rate. The reporting rate should reflect the fraction of true chickenpox cases that appear in surveillance data, not the ratio of cases to births. This initialization rationale is incorrect. However, since rho is subsequently estimated via IF2 (converging to approximately 0.47 in the local search), the misstatement affects only the starting value, not the final estimate.

### 14. Local search cooling fraction very aggressive

The local search uses `cooling.fraction.50=0.1`, which means that after 50 mif2 iterations the perturbations are already 10% of their initial size. With Nmif=400, the perturbations decay to 0.1^8 ≈ 10^−8 of their original size by the final iteration. This extremely aggressive cooling may prevent adequate exploration and account for the several non-converged chains visible in the trace plots. A more moderate value (0.5) is common practice and allows more thorough mixing before the chains freeze.

### 15. Global evaluation table presents parameters that are biologically incoherent

The table shown for the global search best fit (log-likelihood −3478) has R0=202, gamma=922, and vr=0.62. The text merely notes that the fit "appears to fit well" and "captures seasonality," without acknowledging that gamma=922 implies a recovery time of 0.4 days (nearly instantaneous) and vr=0.62 implies 62% of newborns are vaccinated — contradicting the stated motivation that Hungary has very low vaccination uptake. These values should not be presented as substantive findings without explicit caveats about biological plausibility.

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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-covid-active-case-stock-flow-mismatch/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project11/global_search_1.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project11/lik_local_3_runagain.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project11/local_search_3_runagain.rds`
