# Peer Review: W25 Project 17
## Time Series Analysis of New York Harbor Conventional Gasoline Regular Spot Price

---

### Summary

This project fits stochastic volatility (SV) models and a GARCH benchmark to monthly New York Harbor gasoline spot prices (1986-2025) using the POMP framework. Three models are estimated: (1) Breto's (2014) SV model with leverage, (2) a modified version with heavy-tailed errors and a hard-coded regime-shift amplitude parameter, and (3) the same modification without leverage. AIC comparison favors the no-leverage variant, which the authors interpret as evidence that leverage effects are muted in regulated commodity markets. The project demonstrates solid POMP workflow mechanics but suffers from several important methodological and interpretive weaknesses, listed below in approximate order of severity.

---

### Weaknesses

**1. Hard-coded regime-shift windows constitute data snooping (Major)**

The "amplitude" modification hard-codes specific time windows (t in [262, 275] for the 2008 recession and t in [400, 410] for the 2020 pandemic) directly into the transition equation. The authors themselves acknowledge in Section 4 ("Discussion") that this is a "serious mistake" that introduces researcher bias and prevents the model from generalizing. However, the entire model comparison and hypothesis test in Section 2.5 is conducted using these biased models, and the conclusion that "the leverage effect is more limited in gasoline prices" is drawn from them. The discussion section's acknowledgment does not remedy the fact that the primary findings rest on a fundamentally misspecified, data-snooped model. A model where regime windows are estimated or treated probabilistically should have been used, or the leverage hypothesis should have been tested using the unmodified Breto model only.

**2. Missing daily data file prevents full reproducibility (Major)**

The code in the data preprocessing section (around line 129 of the Rmd) reads `Daily_New_York_Harbor_Conventional_Gasoline_Regular_Spot_Price_FOB.csv` to produce Figure 2 (daily vs. monthly log returns). This file is absent from the project directory; only the monthly CSV is present. The code chunk producing Figure 2 will error or silently fail for anyone attempting to reproduce the analysis, and Figure 2 itself appears to have been rendered from a cached HTML rather than re-executed code.

**3. Inconsistency between AIC selection and final GARCH model fit (Major)**

The AIC table over GARCH(p,q) models (Section 2.6) is built using `garchFit(..., include.mean=F)`, but the final best model is then refitted with `include.mean=T`. Switching from excluding to including a mean term changes the model class and parameter count used for likelihood comparison, so the "best" GARCH selected by the AIC table is not the same model as the one whose likelihood (435.509) is compared against the SV model. The log-likelihoods are therefore not directly comparable in a fair way.

**4. GARCH model labeling error: T-GARCH(3,1) versus T-GARCH(1,3) (Major)**

The HTML output (line 1039) shows `Fitting T-GARCH model with p = 1, q = 3`, but the text in Section 2.6 calls it "T-GARCH(3,1)". In the standard GARCH(p,q) notation, p refers to the ARCH lag order and q to the GARCH lag order. The code selects the row index as p and column index as q from the AIC matrix, so the selected model is GARCH(1,3) (one ARCH lag, three GARCH lags), not GARCH(3,1). The mislabeled model name suggests insufficient attention to output checking.

**5. No parameter transformations for `tau` and `amplitude`; positivity constraints not enforced (Major)**

The `parameter_trans` objects for both modified models apply `log` to positive-constrained scale parameters and `logit` to `phi`, but `tau` (degrees of freedom, must be positive) and `amplitude` (intended to be non-negative) have no transformation applied. During IF2, perturbations in the untransformed scale can push `tau` negative or to zero, which is handled ad hoc by a clamping expression (`nearbyint(tau) < 1 ? 1 : ...`) in the C snippets, but this discontinuous clamping can corrupt the iterated filtering gradients. At minimum, a `log` transformation should have been applied to `tau`.

**6. Leftover development comments in submitted code (Minor)**

The C code snippets for both the Breto leverage model (lines 205-206) and the modified leverage model (lines 493-494) retain comments `// Change this` and `// Change This` on the lines that sample `nu_noise` and update `G`. These comments appear to be copy-paste artifacts from template code indicating work-in-progress placeholders. Submitted code should be clean of such comments.

**7. No exploratory data analysis beyond visual inspection (Minor)**

The data preprocessing section presents only a raw price level plot and a log-returns plot. There is no ACF/PACF analysis of the returns or squared returns (which would motivate the GARCH/SV choice), no stationarity test (e.g., ADF or KPSS), and no formal test for heteroskedasticity (e.g., Engle's ARCH test). The STL decomposition (Figure 19) is placed at the end of Section 2.6 as a GARCH diagnostic rather than as part of exploratory analysis. The presence of clear seasonality (as identified by the STL) should have been detected and discussed before model fitting, not as an afterthought.

**8. AIC comparison between models with different parameter counts but no discussion of penalty adequacy (Minor)**

The AIC comparison in Section 2.5 gives the modified SV without leverage (5 parameters, logLik 434.8, AIC -859.6) a slight advantage over the modified SV with leverage (8 parameters, logLik 437.1, AIC -858.2). The leverage model has three additional parameters (sigma_nu, G_0, H_0) and achieves a 2.3 log-likelihood unit advantage. AIC penalizes each additional parameter by 1, so the 3-parameter penalty of 6 exceeds the 4.6 log-likelihood gain, yielding the AIC preference. The paper does not note that the difference in AIC is only 1.4 units, which is not considered a decisive distinction under conventional guidelines (typically a difference greater than 10 is needed for strong evidence). Presenting a likelihood ratio test or profile likelihood for sigma_nu would have been more rigorous.

**9. Regime-amplitude parameter not identified consistently across models (Minor)**

The global search box for the modified leverage model (T_breto_box) sets sigma_eta in the range [0.001, 0.3], but the local search starting value uses `sigma_eta = exp(-10)` which is approximately 4.5e-5 — well outside this box. The modified model is initialized at a point not covered by the global search box, which means the global search is not guaranteed to cover the neighborhood of the locally optimal solution.

**10. Rw.sd for `tau` is disproportionately large relative to other parameters (Minor)**

For the modified models, `rw.sd` for `tau` is set to 1 (line 621, 860), while all other regular parameters use `rw.sd_rp = 0.02`. The `tau` parameter ranges from 5 to 30 in the search box, so a step size of 1 represents roughly 3-20% of the parameter range per step, far larger than the 2% perturbations applied to other parameters. This asymmetric perturbation scheme can cause tau to dominate early iterations of IF2 and distort convergence behavior for other parameters.

**11. Equation (4) notation is inconsistent with the normal vs. t-distribution models (Minor)**

Equation (4) writes `Y_n = exp{H_n/2} sigma_n` and the text defines `sigma_n ~ N(0,1)` in the base model, but the C snippet for `rproc2.sim` in the Breto model uses `rnorm(0, exp(H/2))`, effectively sampling `Y_state = N(0, exp(H/2))` directly — consistent with the equation. However, equation (4) as written suggests `sigma_n` is the stochastic term and `exp{H_n/2}` is a scale factor, but the body text describing beta later uses `{epsilon_n}` as the i.i.d. N(0,1) sequence without connecting it cleanly to equation (4)'s `sigma_n`. The notation conflates `sigma_n` (used as a noise term in eq. 4) with `sigma_n` in the t-distribution modification (eq. 5), which redefines it as a t-distributed variable.

**12. No simulation-based diagnostics for the final SV models (Minor)**

After model fitting, the authors show pair plots and MIF2 convergence diagnostics but do not simulate from the fitted (best-parameter) SV models to assess in-sample fit. The only simulation shown (Figures 3 and 8) uses the hand-chosen initial test parameters, not the estimated MLE parameters. A comparison of simulated trajectories from the best-fitting model against the observed data is standard practice in POMP-based analysis and would provide qualitative evidence for or against model adequacy.

**13. Filtered log-likelihood for the simulated (not real) data is misleading (Minor)**

Sections 2.2.2, 2.3.2, and 2.4.2 each report a "filtered log-likelihood" evaluated on the simulated data (e.g., 410.657, 457.797, 472.035) using the hand-tuned initial parameters. These numbers reflect how well the filter tracks artificially generated trajectories using the same parameters that generated them, which is not informative about model quality on the actual data. The text does not clearly distinguish these simulation-based filtered log-likelihoods from the estimated log-likelihoods reported later (429.8, 437.1, 434.8), which could mislead readers into interpreting the simulated quantities as pre-optimization performance on real data.

**14. Demeaning formula mismatch between equation and code (Minor)**

The math equation presented around line 120-124 defines the log return as simply `y*_n = log(z_n) - log(z_{n-1})`, without explicitly showing the demeaning step. The code on lines 96-97 then computes `ret.demeaned = returns - mean(returns)`. While the demeaning itself is standard, the equation as written omits this step, and the displayed formula label `y*_n` should reflect the full demeaned return that is actually used as input to the POMP models.

**15. Hypothesis framing tied to regulatory narrative is weakly supported (Minor)**

The paper's central hypothesis — that government regulation limits the leverage effect in gasoline prices — is interesting but the evidence chain is tenuous. The AIC comparison shows a very small margin (1.4 AIC units) in favor of the no-leverage model, and both models contain the hard-coded regime-shift modification that contaminates the comparison. Furthermore, the paper does not compare gasoline to a freely traded commodity (e.g., crude oil futures or an equity index) to empirically demonstrate the contrast, relying entirely on a qualitative appeal to prior literature. The conclusion overstates the strength of the evidence given these limitations.

---

### Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project17/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project17/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project17/New_York_Harbor_Conventional_Gasoline_Regular_Spot_Price_FOB.csv` (directory listing only; not read for content)
