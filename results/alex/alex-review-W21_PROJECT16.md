# Peer Review: Volatility Analysis on the Shanghai Composite Index
**Semester:** Winter 2021 | **Project:** 16

---

## Summary

This project applies a GARCH(1,1) model and a POMP stochastic-volatility model to weekly closing prices of the Shanghai Composite Index (SSE) covering 2010-2021. The overall structure is reasonable, but the work is largely a direct adaptation of course lecture code with minimal original intellectual contribution. Several critical analytical problems undermine the conclusions, the profile-likelihood section is incomplete and contains a rendering error, and the computational effort is low for a project of this scope.

---

## Weaknesses (Most Critical First)

### 1. [MAJOR] Profile likelihood section contains an incomplete statement and a rendering error

The conclusion sentence in Section 4.4 reads: "The plot above suggests that the maximum log-likelihood over phi is achieved when phi = ." The value of phi is missing entirely — the inline R expression that was supposed to produce a numeric value failed to render. This is a fundamental presentation failure: a key inferential claim is left literally blank. The sentence that follows ("As phi approaches 1, the likelihood becomes unstable") directly contradicts the earlier motivation stated for doing the profile (that phi appeared to be near 1 in local search), and neither claim is quantified.

### 2. [MAJOR] POMP model never actually fits the real data — only a simulated dataset is used for the particle filter check

The `pfilter` call in Section 4.1 runs on `sim1.filt`, which is a pomp object built from a *simulated* dataset (`sim1.sim`), not from the observed Shanghai Composite returns. The local and global MIF2 searches do correctly target `Shanghai.filt`, but the preliminary particle-filter evaluation (the only step that reports a likelihood for a single model state) operates on simulated data. This is not acknowledged or discussed, and the resulting log-likelihood from `L.pf1` is presented without clarification of what data it pertains to.

### 3. [MAJOR] POMP log-likelihood is not comparable to GARCH log-likelihood, but the comparison is made anyway

The conclusion states "the POMP model have even worse log-likelihood score" than GARCH. The GARCH log-likelihood (1269.58) is from `fGarch::garchFit` applied to the demeaned returns. The POMP log-likelihood (best global search result: ~1264) is computed via particle-filter approximation with Monte Carlo error. These two numbers are not on the same footing: the GARCH likelihood is exact under its model assumptions, while the POMP value is a noisy lower-bound estimate with non-trivial standard errors (~0.06-0.13). The paper does not discuss this comparability problem and draws a conclusion that may be unwarranted.

### 4. [MAJOR] Global search box for phi is constrained to [0.9950, 0.9999], precluding discovery of other optima

The global parameter search box sets `phi = c(0.9950, 0.9999)`. This is nearly identical to the local search starting point (`expit(4) ≈ 0.9820`) and prevents the optimizer from exploring substantially lower values of phi. The profile likelihood results (Section 4.4) show that many of the highest log-likelihoods from the global search actually correspond to phi values well below 0.99 (e.g., phi ~ 0.858, 0.827, 0.880 in the params CSV achieve log-likelihoods > 1259). The tight phi constraint in the global search box thus contradicts the profile likelihood findings and likely prevents finding the true MLE.

### 5. [MAJOR] Profile likelihood for phi does not fix phi during optimization — phi is not frozen in rw.sd

In Section 4.4, the profile likelihood search uses `rw.sd` that omits phi entirely (phi has no entry), but phi is still passed through `start=c(unlist(guesses[i,]),params_test)`. However, when phi is not included in `rw.sd`, it is held fixed at the starting value throughout the MIF2 run — which is the correct approach for a profile likelihood. But the starting values for phi come from `guesses`, which was constructed using `profile_design` with `phi` as the profiled variable. The critical issue is that the profile grid over phi uses values from 0.80 to 0.99999, but the global search box used `phi = c(0.9950, 0.9999)`. The profile is therefore inconsistent with the global search constraints — the profile explores a much wider range of phi than the box search did. The paper does not reconcile this inconsistency or explain why phi was constrained so tightly in the global search.

### 6. [MAJOR] Demeaning the returns before fitting is a questionable data transformation that is not justified

The analysis computes `demeaned = wreturn - mean(wreturn)` and fits all models to this demeaned series. While subtracting the sample mean is common, the POMP model already includes a drift parameter (`mu_h`). Demeaning removes the empirical mean return, which may interact with `mu_h` in non-obvious ways. More importantly, fitting a GARCH model to demeaned returns is standard practice but fitting the POMP model (which has its own mean structure) to pre-demeaned returns is not clearly motivated or discussed.

### 7. [MAJOR] Computational settings are too low and this is acknowledged but not improved

`Shanghai_Np = 2000` particles, `Shanghai_Nmif = 50` iterations, and `Shanghai_Nreps_local = 20` / `Shanghai_Nreps_global = 50` chains are used throughout. The profile likelihood additionally drops to `Np=1000`. For a model of this complexity with 6 parameters, these settings are on the lower end of what is needed for reliable convergence. The authors acknowledge this in the conclusion ("limitation of time and computational sources") but do not provide convergence diagnostics (e.g., likelihood standard errors or trace plots showing stabilization) that would reassure the reader that the results are meaningful.

### 8. [MINOR] The ACF of returns is used to claim independence, but this conclusion is incorrect for volatility analysis

Section 2.1 states: "The above plot shows that there is no significant autocorrelation for lag# > 0. Therefore, we can safely assume that the data are all independent." The absence of significant ACF in raw returns does not imply independence — it only implies lack of linear autocorrelation. Squared returns or absolute returns typically show significant autocorrelation (ARCH effects), which is precisely the motivation for GARCH and stochastic-volatility models. The paper should check the ACF of squared returns to motivate the heteroskedastic models.

### 9. [MINOR] The GARCH model summary includes the constant term alpha0, but the written equation omits it

The text writes the fitted model as $V_n = 0.143 Y^2_{n-1} + 0.822 V_{n-1}$, dropping the intercept $\alpha_0$. The full GARCH(1,1) equation requires $\alpha_0 > 0$ for the variance process to be well-defined (ensuring positive conditional variance). The omission of $\alpha_0$ from the written fitted model is an error of presentation — the model formula should include the intercept estimated by `fGarch::garchFit`.

### 10. [MINOR] The demeaned return plot has no x-axis date labels, making it uninterpretable as a time series

The code plots `demeaned` against its integer index (`1:length(demeaned)`) without converting back to dates. All other plots use the proper `Date` variable. Plotting against an index rather than calendar time prevents the reader from relating volatility clustering to known economic events (e.g., the 2015 Chinese stock market crash or the 2020 COVID-19 crash), which would strengthen the motivational narrative.

### 11. [MINOR] The log-price plot uses a log scale on the y-axis redundantly

The code sets `plot(Date, log(Price), ..., log="y")`. The y-values are already `log(Price)`, and then the axis is further log-transformed with `log="y"`. This double-transformation means the y-axis shows $\log(\log(\text{Price}))$ instead of $\log(\text{Price})$, which is not what is intended. This is a coding error that produces a misleading plot.

### 12. [MINOR] The profile likelihood uses only nprof=2 profiles per phi value, which is too sparse

In Section 4.4, `profile_design` is called with `nprof=2`, meaning only 2 random restarts per phi grid point across 50 grid points (100 total runs). With only 2 restarts, the maximum over nuisance parameters at each phi value is extremely noisy. Standard practice for POMP profile likelihoods is to use at least 5-10 restarts per grid point to obtain a reliable profile envelope.

### 13. [MINOR] No simulation study or posterior predictive check is presented

The project builds a simulator (`sim1.sim`) but never uses it for model checking. A natural validation step would be to simulate from the fitted POMP model and compare simulated return distributions and ACF patterns to the observed data. This is entirely absent, and instead the simulator is only used to demonstrate the particle filter on a synthetic dataset.

### 14. [MINOR] The conclusion claims the GARCH model "suggests that the volatility should slightly shift positively as time moving forward," which is not supported by the analysis

The conclusion states: "The model suggests that the volatility should slightly shift positively as time moving forward." No such claim is made in or derivable from the GARCH(1,1) analysis presented. GARCH models do not generally imply a positive drift in volatility — in fact, the estimated parameters ($\hat{\alpha}_1 = 0.143$, $\hat{\beta}_1 = 0.822$, $\hat{\alpha}_0$ unreported but positive) imply mean-reversion in variance. This conclusion appears to be an error or fabrication.

### 15. [MINOR] References misattribute prior student projects to Ionides (the course instructor)

References 6, 7, 8, and 9 are formatted as authored by "Ionides, L. E." but describe student final projects from 2016, 2018, and 2020. For example: "Ionides, L. E. (2016). 'Financial Volatility Analysis with SV-in-Mean Model in Pomp'." These were student projects, not publications by the instructor. This is a citation error that reflects either carelessness or a misunderstanding of the course materials.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project16/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project16/Shanghai_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project16/Shanghai Composite Historical Data.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project16/worked/Final Project.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project16/Makefile`
