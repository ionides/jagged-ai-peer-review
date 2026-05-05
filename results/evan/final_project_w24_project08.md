# Final AI Review — King County COVID-19 Weekly Cases Analysis
## w24 Project 08

---

## Overall Assessment

This project tackles a scientifically ambitious problem — modeling three years of COVID-19 transmission in King County using mechanistic compartmental models — and makes a genuine contribution by extending a standard SEIR framework to the SVEIPR model, which incorporates vaccination, asymptomatic/potentially-infected individuals, reinfection, and time-varying transmission and vaccination rates. The authors use likelihood-based inference (IF2 via mif2) with both local and global search, correctly apply logmeanexp over replicated particle filter evaluations, and are candid about model limitations. These are meaningful achievements. However, the work is undermined by a critical bug in the reinfection mechanism (the recovered-to-susceptible flow draws from the wrong compartment), by a counterproductive reversal in which the more complex SVEIPR model achieves a substantially worse log-likelihood than SEIR (approximately 183 log-likelihood units), and by several inferential gaps including absent profile likelihoods, a large set of hand-fixed parameters, and a nonstandard measurement model without justification. The ARIMA section provides a useful baseline but is never formally connected to the POMP results in likelihood terms. Addressing the code bug and the inferential gaps would substantially strengthen the work.

---

## Key Strengths

**24.08.10 — Correct likelihood computation**
logmeanexp is applied over 10 replicated pfilter evaluations at both the local and global search stages, correctly accounting for Monte Carlo variability in the particle filter likelihood estimate. This is methodologically sound.

**24.08.11 — Scientifically motivated model extension**
The SVEIPR model adds epidemiologically relevant compartments and processes (V, P, time-varying Beta and mu_SV, reinfection) that are well-justified by the COVID-19 literature and by the clear failures of the simpler SEIR model. The motivation is clearly articulated.

**24.08.12 — Honest reporting of model failures**
The authors explicitly acknowledge that the SEIR model fails to capture epidemic peaks and that the SVEIPR model still exhibits timing delays. This candor is commendable and reflects good scientific practice.

**24.08.13 — Use of bake() for reproducibility**
Expensive computations (mif2 runs, pfilter evaluations) are cached with bake(), which facilitates reproducibility and makes the computational workflow transparent.

---

## Major Points

**ID: 24.08.1**
**Concern:** Critical bug in the reinfection (R → S) Csnippet. The code reads `double dN_RS = rbinom(I, 1 - exp(-mu_RS * dt));`, drawing individuals from compartment I rather than R. The compartment update in the vaccine==1 branch decrements S by dN_RS and does not decrement R, so R grows without bound and I is effectively depleted by two separate processes simultaneously. This violates both the intended model structure and conservation of individuals.
**Why it matters:** The reinfection pathway is presented as a key innovation of the SVEIPR model. If this pathway is incorrectly implemented, the model is not doing what the paper claims, and all SVEIPR results are potentially invalid.
**Severity:** Major
**Suggested action:** Change `rbinom(I, ...)` to `rbinom(R, ...)` in the dN_RS line and update the compartment equations so R is decremented: `R += dN_PR + dN_IR - dN_RS`. Re-run the optimization after correcting this error.

---

**ID: 24.08.2**
**Concern:** The SVEIPR model's best log-likelihood (−1377 global, −1397 local) is approximately 183 log-likelihood units worse than the SEIR model (−1194). A more complex model should achieve at least as high a log-likelihood as a nested or simpler alternative if both are optimized to convergence. This reversal is neither explained nor flagged by the authors.
**Why it matters:** Without understanding why the more complex model underperforms, there is no basis for trusting the SVEIPR results. The likely explanations — the dN_RS bug, fixed parameters preventing optimization, or insufficient Np/Nmif for a 20+ parameter model — each require different remedies.
**Severity:** Major
**Suggested action:** After fixing the dN_RS bug, increase Np (to at least 5000 for a model this complex) and Nmif and rerun. Report the log-likelihood gap explicitly and discuss whether it reflects model misspecification, optimization failure, or both.

---

**ID: 24.08.3**
**Concern:** Seven parameters in the SVEIPR global search are fixed at values (`Beta = 1.01, mu_PR = 0.93, mu_IR = 0.98, mu_RS = 0.5, alpha = 0.4, N = 2269675, mu_SV = 0.5`) without scientific justification. In particular, Beta is fixed at 1.01 while the multiplicative scaling factors b1–b8 are estimated, making Beta and each b_i individually unidentifiable.
**Why it matters:** Parameters fixed at ad hoc values make the inference non-likelihood-based for those dimensions. The resulting parameter estimates and log-likelihoods do not reflect the optimal model within this class.
**Severity:** Major
**Suggested action:** Either estimate Beta and the b_i factors jointly (using a constraint such as b_ref = 1 for a reference period) or provide literature-based priors/fixed values with explicit citations. Similarly, justify mu_PR, mu_IR, mu_RS from published COVID-19 natural history data.

---

**ID: 24.08.5**
**Concern:** The paper reports "poor man's profile likelihood confidence intervals" for gamma and eta but does not state the log-likelihood threshold used, the number of points in the range, or whether the reported intervals correspond to a statistically meaningful cutoff.
**Why it matters:** Without a stated threshold (e.g., 1.92 log-likelihood units below the maximum for a 95% CI), the reported intervals have no formal statistical meaning. The wide intervals (e.g., eta from 0.816 to 0.979) suggest weak identifiability that should be acknowledged explicitly.
**Severity:** Major
**Suggested action:** Compute formal profile likelihoods for at least rho, gamma, and Beta. State the threshold used. If parameters are weakly identified, report this as a finding rather than converting it to a spurious CI.

---

**ID: 24.08.6**
**Concern:** The SVEIPR measurement model uses a Gaussian approximation with variance formula `sqrt((tau*H)^2 + rho*H)`, evaluated via a continuity-corrected normal CDF. The SEIR model used a negative binomial measurement model (dnbinom_mu), which is standard for infectious disease count data. No justification is given for switching to the Gaussian approximation in SVEIPR.
**Why it matters:** The Gaussian approximation is questionable for weekly case counts with many near-zero values and a distribution that is highly skewed during outbreak peaks. The formula for sd mixes a multiplicative term (tau*H) and a Poisson-variance-like term (sqrt(rho*H)) without derivation. This makes the measurement model ad hoc and potentially invalid.
**Severity:** Major
**Suggested action:** Revert to a negative binomial measurement model (dnbinom_mu) for the SVEIPR model, or provide a formal derivation and justification for the Gaussian approximation with this particular variance formula.

---

**ID: 24.08.7**
**Concern:** The data processing pipeline conflates two distinct operations. Converting from cumulative confirmed cases to weekly incidence (first difference) is a data cleaning step. Whether to additionally difference the incidence series for stationarity is a separate modeling decision. The paper justifies the ARIMA d=1 parameter by saying the data is cumulative, but if sea_df$cases already contains incidence (weekly differences), then d=1 in ARIMA applies a second difference. The ACF of the raw data (Figure 2) is described as showing "the weekly differentiation has removed most of the autocorrelation," but Figure 1 shows a highly non-stationary incidence series, so a further difference for ARIMA modeling may be unnecessary and distorts the model.
**Why it matters:** Applying an unnecessary second difference removes meaningful signal and changes what process is being modeled, affecting model selection and residual interpretation.
**Severity:** Major
**Suggested action:** Clarify explicitly what transformation is applied to get sea_df$cases (cumulative → incidence? incidence already?). Fit ARIMA on the incidence series (d=0 or d=1 based on diagnostic tests). Show ACF of the series actually modeled.

---

**ID: 24.08.8**
**Concern:** The SEIR local search best parameter set has mu_IR = 5.33 per week, corresponding to an average infectious period of 1/5.33 weeks ≈ 1.3 days. This is biologically implausible for COVID-19 (where the infectious period is typically 5–10 days ≈ 0.7–1.4 weeks). This implausible estimate is not flagged or discussed in the paper.
**Why it matters:** Biologically implausible parameter estimates indicate model misspecification or poor convergence and should trigger further investigation rather than being reported as the "optimal" result. This is a course-confirmed type of error (interpreting parameter estimates without an identifiability check).
**Severity:** Major
**Suggested action:** Flag mu_IR = 5.33/week as implausible. Check whether this estimate corresponds to a genuine likelihood maximum or a convergence artifact. Compare to published COVID-19 natural history estimates. Consider adding a prior constraint or fixing mu_IR to a biologically plausible value with justification.

---

## Minor Points

**ID: 24.08.9**
**Concern:** The SEIR local search convergence is described as "successful" but Figure 9 shows that many chains (approximately half) collapse to very low log-likelihoods after ~iteration 20, with only a subset converging near the reported maximum of -1196. Calling this "successful" overstates the robustness of the optimization.
**Severity:** Minor
**Suggested action:** Discuss the convergence failure of several chains. This is expected behavior for mif2 and is not a failure of the approach per se, but should be reported accurately.

**ID: 24.08.4 (minor reframing)**
**Concern:** The ARIMA log-likelihood (−1455.81) and the SEIR log-likelihood (−1194) are computed on different transformations of the data (differenced vs. level series) and are not directly comparable. The paper presents both numbers without noting this distinction.
**Severity:** Minor
**Suggested action:** Add a sentence noting that the ARIMA and POMP likelihoods are not directly comparable because they are computed on different data transformations, and that a valid benchmark comparison would require fitting both models to the same data.

**ID: 24.08.13 (minor)**
**Concern:** The `run_level` variable controls Np, Nmif, and nseq throughout the code, but it is never defined or documented in the rendered output. Readers cannot determine what computational settings were used for the reported results.
**Severity:** Minor
**Suggested action:** State the run_level used and document the corresponding Np, Nmif, and nseq values near the beginning of the analysis.

**ID: misc-1**
**Concern:** Figures 19, 20, and 21 (likelihood surface pairs for SVEIPR local search) lack axis labels and captions explaining what parameter combinations are shown. The text mentions pairs (b3, b5) and (rho, tau) but readers cannot identify which figure corresponds to which pair.
**Severity:** Minor
**Suggested action:** Add descriptive captions to all pair plot figures.

**ID: misc-2**
**Concern:** The SVEIPR model initializes E=1000, I=500, P=500 at week 1 (January 22, 2020). King County had just confirmed its first case at that time; initial values of this magnitude are inconsistent with the historical epidemiological context and should be estimated or justified.
**Severity:** Minor
**Suggested action:** Either estimate initial conditions using the ivp() mechanism in rw.sd or justify the chosen values with epidemiological reasoning.
