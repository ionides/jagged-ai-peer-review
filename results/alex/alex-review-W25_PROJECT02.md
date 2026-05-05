# Peer Review: W25 Project 02 — Examining Explanatory Role of Momentum in Baseball

## Summary

This project investigates whether team-level offensive momentum contributes to game-to-game variation in runs scored by the 2024 Detroit Tigers, using a POMP model with a Gaussian AR(1) latent state and Poisson (or negative binomial) observation model. The writeup is well-motivated and shows awareness of identifiability concerns, but contains several serious methodological errors and a critical misinterpretation of the central model parameter. The main conclusion — that momentum provides statistically significant explanatory power — rests on a model comparison where the preferred observation model (Poisson) is demonstrably a poor fit relative to the alternative (negative binomial), and where the optimal AR(1) parameters found show essentially no temporal autocorrelation (phi near zero), undermining the claim of "momentum."

---

## Weaknesses

### 1. (Major) Incorrect Sign Interpretation for the Opponent Strength Covariate gamma

The writeup states (Section: Observation Model): "negative values of gamma would indicate that the Tigers score less against stronger pitching (as one may expect)." This is the wrong sign. The covariate Z_n is the average runs allowed by the opposing pitcher against other teams — higher Z_n means weaker pitching. Since lambda_n = exp(X_n + mu + gamma*(Z_n - 4.6)), a stronger pitcher has lower Z_n, meaning Z_n - 4.6 < 0. If gamma < 0, then gamma*(Z_n - 4.6) > 0, which increases lambda_n — predicting the Tigers score *more* against better pitchers. The physically correct sign is gamma > 0, which is exactly what the global search finds (gamma ~ +0.087 at the MLE). The initial guess of gamma = -0.25 and the description of expected negative gamma are both wrong, even though the global search recovers the correct sign. This is a conceptual error in model description that is never corrected in the text.

### 2. (Major) Profile Likelihood Is Computed from a Suboptimal Starting Box and Is Effectively Uninformative

The formal profile likelihood for phi (Full_Code.Rmd, Section "Profile Likelihood") constructs its starting box from the CSV file `run_parms_AR1_pois.csv`, which is written incrementally and at the time of the profile design contains only the results of the *local* search (maximum log-likelihood around -436). The global search, which achieves a maximum log-likelihood of approximately -397.7, is run after the profile. The profile maximum is -437.5 — matching the local search peak, not the global peak (-397.7). This means every starting point for the profile sweep is 40 log-likelihood units below the true maximum, and the resulting profile CI and plot are computed on the wrong likelihood surface. The 95% CI from the profile spans the entire searched range of phi (-0.25 to 0.99), which is not meaningful. The "poor man's profile" shown in blinded.Rmd does use the global search results and is better, but the formal profile, which is the appropriate tool for constructing a CI for phi, is invalid.

### 3. (Major) Optimal AR(1) Parameters Show No Momentum — Conceptual Disconnect in Interpretation

At the maximum likelihood estimates from the global search (phi ~ -0.02, sigma ~ 0.58), the AR(1) process X_n is essentially i.i.d. N(0, sigma^2) — there is no temporal autocorrelation. "Momentum" implies a positive autoregressive structure (phi meaningfully greater than 0). What the model actually finds is that a large, game-to-game IID latent random effect significantly improves fit over no latent state at all. This is a random-effects interpretation, not momentum. The paper's conclusion that "momentum does provide explanatory power" is therefore misleading: what is found is that unexplained game-to-game IID variation exists, not that good/bad performance persists over multiple games.

### 4. (Major) Transition Density Formula Contains a Typo

The written transition density in Section "Latent State Transition Model" reads:

    f_{X_n | X_{n-1}}(x_n | x_{n-1}) = (1/sqrt(2*pi*sigma^2)) * exp( -(phi*x_{n-1})^2 / (2*sigma^2) )

The exponent should be -(x_n - phi*x_{n-1})^2 / (2*sigma^2). As written, the density does not depend on x_n, which would make it an improper density rather than the conditional density of X_n given X_{n-1}. The Csnippet implementation is correct; this is an error in the mathematical writeup only, but it fundamentally misrepresents the model.

### 5. (Major) Primary Conclusion Depends on the Poisson Model, Which Is Strongly Outperformed by Negative Binomial

The main inference (rejecting the null of no momentum) uses the Poisson observation model. The negative binomial static model achieves a maximum log-likelihood of -396.46 versus the Poisson static model's -437.49 — a gain of 41 log-likelihood units for one additional parameter. By any information criterion, the negative binomial is a substantially better fit even without a latent state. Under the negative binomial, the AR1 and static models have virtually identical likelihoods (-396.46 vs -396.46). The paper appropriately discusses this sensitivity, but the primary conclusion is drawn from the Poisson model, which the data themselves indicate is a poor choice. A defensible conclusion would note that the Poisson LRT result is not robust and that the more appropriate negative binomial model yields no evidence for momentum.

### 6. (Major) NBin AR1 Maximum Log-Likelihood Is Slightly Worse Than NBin Static, Suggesting Convergence Failure

In the stored RDS results, the AR1 negative binomial achieves a maximum of -396.461 while the static negative binomial achieves -396.458 — the AR1 model is slightly *worse* than its nested submodel. This is impossible if both were correctly optimized, and it indicates that the AR1 negative binomial global search did not converge to the true MLE. The paper treats these as "nearly identical" without acknowledging this red flag, which raises questions about whether the NBin global search was also inadequately initialized.

### 7. (Moderate) run_level Is Hardcoded to "explore" — Code Cannot Reproduce Stored Results

In Full_Code.Rmd (line 96), `run_level <- "explore"` sets nseq = 5, Nmif = 10 (profile), and nprof = 10. The stored RDS files, however, reflect a "final" run with nseq = 500. Anyone attempting to reproduce the results by running Full_Code.Rmd as submitted will obtain results from only 5 global starting points rather than 500, producing qualitatively different diagnostics and potentially different conclusions. The code should either default to "final" or include clear instructions for switching the run level.

### 8. (Moderate) Pairwise Scatterplot in "Local Search" Section Uses Global Search Results

In blinded.Rmd (lines 297-304), the scatterplot titled "Pairwise Scatterplot of Log-Likelihood and Parameters" is placed in the "Local Search" section but is constructed from `Output[["results_glob"]]`. The accompanying text correctly says "we also plot the pairwise scatterplot of parameters," but the visual organization implies these are local search results. This is a presentation inconsistency that may mislead a reader about which search produced the identifiability concerns displayed.

### 9. (Moderate) Wilks Approximation May Not Apply Due to Boundary Parameter

The likelihood ratio test for H0: (phi, sigma) = (0, 0) is evaluated against chi-squared with df = 2. However, the null hypothesis places sigma at the boundary of its feasible parameter space (sigma >= 0). In boundary testing problems of this type, the asymptotic null distribution of the LRT statistic is typically a mixture of chi-squared distributions (e.g., a mixture of chi-squared(1) and chi-squared(2)), not a pure chi-squared(2). Using chi-squared(2) is conservative in this case (yields a larger p-value than the boundary-corrected test), but given the already extremely small p-value (~5e-18), this does not change the Poisson-based conclusion. Nonetheless, the approximation should be acknowledged.

### 10. (Moderate) No Exploratory Autocorrelation Analysis Before Model Construction

The EDA section (Section "Exploratory Data Analysis") shows only a time series plot and a five-number summary. The project's central research question concerns temporal autocorrelation in runs scored, yet no autocorrelation function (ACF) plot or formal test (e.g., Ljung-Box) is presented prior to model construction. Even if the POMP approach subsumes such analysis, documenting the degree of raw autocorrelation in the data would strengthen the motivation and provide a baseline comparison for what the latent AR(1) structure is capturing.

### 11. (Moderate) Code Comment Incorrectly States "log(mu) represents expected runs"

In blinded.Rmd (line 193) and Full_Code.Rmd (rw_trans_models), the comment reads: "log(mu) represents expected runs with no momentum against league-average pitching." Since mu is constrained via `parameter_trans(log = c("sigma", "mu"))`, the internal parameter is log(mu) and exp(mu) gives expected runs. The comment conflates mu (the log-rate, which is the model parameter) with log(mu) (the transformed parameter used internally in optimization). Since the model formulation defines lambda = exp(X + mu + ...), mu itself is the log of expected runs, not log(mu). The comment introduces confusion about the parameterization.

### 12. (Minor) Inconsistent parameter_trans Between blinded.Rmd POMP Object and Full_Code.Rmd Initial Object

In blinded.Rmd (line 195-196), `partrans <- parameter_trans(log = c("sigma", "mu"))` constrains both sigma and mu to be positive. In Full_Code.Rmd (line 182-183), the initial `partrans <- parameter_trans(log = "sigma")` constrains only sigma. The actual mif2 fitting uses the correct transform from `rw_trans_models()`, so the fitted results are unaffected, but the inconsistency in the initial POMP object construction is confusing and could cause problems if the initial POMP object's partrans is used (e.g., for direct pfilter calls on the initial object before mif2).

### 13. (Minor) No Model Adequacy Assessment via Simulation or Residual Analysis

Beyond the initial simulation plot (which uses starting parameter values, not MLE estimates) and the ESS plot, there is no formal model adequacy assessment. A standard check would simulate from the fitted model at estimated parameters and compare summary statistics of simulated runs (mean, variance, distribution shape, ACF) with the observed data. This is especially important given the authors' own concerns about model misspecification and the large range in maximum log-likelihood values across global search starting points (approximately 40 log-likelihood units for both Poisson and negative binomial AR1 models).

### 14. (Minor) Opponent Strength Uses Season-Wide Data Including Future Games

The paper acknowledges in the Discussion section that Z_n is constructed using the full season's data for the opposing pitcher, which includes games occurring after game n against the Tigers. While the authors note this may have minimal practical impact, using post-game data in the covariate construction technically violates the causal structure of the model. The paper suggests restricting to pre-game-n data as a future direction, but this is a genuine methodological concern for the current analysis, not merely a future direction.

### 15. (Minor) nrow(opp_pitch_games > 0) Is Incorrect Code, Even If Functionally Benign

In blinded.Rmd (line 88) and Full_Code.Rmd (line 52), the condition `if (nrow(opp_pitch_games > 0))` applies `> 0` to the entire data frame before calling `nrow`. The intended test is `nrow(opp_pitch_games) > 0`. In practice, for a data frame with character columns, applying `> 0` to the full data frame either throws a warning or returns a logical matrix whose row count equals the original row count, so the condition evaluates correctly for both empty and non-empty results in this specific context. However, this is incorrect code that happens to produce the right behavior here and could silently fail in other contexts. It should be written as `nrow(opp_pitch_games) > 0`.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project02/Full_Code.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project02/Output_AR1_pois.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project02/Output_static_pois.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project02/Output_AR1_nbin.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project02/Output_static_nbin.RDS`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project02/mlb-2024-asplayed.xlsx`
