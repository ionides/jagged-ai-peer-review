# Final AI Review: Investigation of Ebola in Guinea and Sierra Leone (w22, project02)

---

## Overall Assessment

This project applies a biologically motivated SEIRDF compartmental model to daily Ebola incidence data from Guinea and Sierra Leone, extending the standard SEIR framework to account for funeral-associated transmission. The epidemiological motivation is sound and grounded in published literature. However, the technical execution has several fundamental problems that prevent the stated scientific conclusions from being drawn. The profile likelihood for the primary parameter of interest (beta) is completely flat over the entire search range, indicating that beta is not identified by the data given the current model. The paper nonetheless interprets the 95% "CI" as evidence that the two countries have similar transmission rates — this is a circular artifact of the shared search bounds, not a statistical finding. Additionally, the profile likelihood methodology is nonstandard (nuisance parameters are not optimized at each fixed beta), final log-likelihood estimates are not obtained from replicated particle filter evaluation, and the measurement model distribution is never specified. Most parameters show no convergence in IF2 traces, and no benchmark comparison is provided. These are interconnected problems that collectively undermine the reliability of all quantitative results in the paper.

---

## Key Strengths

**ID: 22.02.S1**
**Strength:** Scientifically motivated model extension
**Why it matters:** The addition of Death and Funeral compartments is grounded in specific epidemiological literature (Weitz & Dushoff 2015; Park 2020) and directly addresses a known transmission pathway for Ebola. The model is not ad hoc.
**Confidence:** High

**ID: 22.02.S2**
**Strength:** IF2 used for likelihood-based inference
**Why it matters:** The use of mif2 (iterated filtering) is appropriate for stochastic POMP models and reflects correct understanding of the framework. The authors conducted both local and global searches.
**Confidence:** High

**ID: 22.02.S3**
**Strength:** Profile likelihood attempted for key parameter
**Why it matters:** The attempt to compute profile likelihoods for beta, and the honest acknowledgment that beta may be weakly identifiable, shows methodological awareness even if execution is incomplete.
**Confidence:** Moderate

---

## Major Points

**ID: 22.02.1**
**Concern:** Profile likelihood for beta is flat; the reported CI is not a valid confidence interval
**Why it matters:** The profile plots (fig_007, fig_012) show no parabolic shape — log-likelihood values scatter nearly uniformly across beta in [3, 7] with no identifiable maximum. The stated 95% CI [3.003, 6.974] spans essentially the full search range. This means the data contain no information about beta given the model. The conclusion that "both countries have similar transmission rates" is based entirely on this non-informative interval, making the central scientific claim unsupported.
**Severity:** Major
**Suggested author action:** Declare beta non-identified. Investigate whether simplifying the model (fixing some parameters from literature values) or using additional data types enables identification. Do not report the [3, 7] interval as a confidence interval.

**ID: 22.02.2**
**Concern:** Profile likelihood methodology is nonstandard — nuisance parameters not optimized at each fixed beta
**Why it matters:** A valid profile likelihood requires maximizing over all other parameters at each fixed value of the profiled parameter. The paper samples one random starting point from a uniform box and runs a single mif2 per beta value. This produces a noisy likelihood slice, not a profile. The result conflates Monte Carlo noise with genuine likelihood variation and cannot be used to construct confidence intervals via Wilks' theorem.
**Severity:** Major
**Suggested author action:** At each fixed beta, run multiple mif2 searches from diverse starting points. Evaluate the final likelihood for each using replicated pfilter (logmeanexp over replicates). Record the maximum as the profile value.

**ID: 22.02.3**
**Concern:** No replicated particle filter evaluation — all likelihood values come from mif2 internal output
**Why it matters:** The mif2 algorithm's internally reported log-likelihood is biased (due to the cooling schedule) and has high Monte Carlo variance. Final log-likelihood estimates must come from separate replicated pfilter calls. Without this, all reported likelihood values — including convergence thresholds and profile plots — are unreliable. No best log-likelihood is stated anywhere in the paper.
**Severity:** Major
**Suggested author action:** After each mif2 run, evaluate log-likelihood using at least 10 replicated pfilter calls (e.g., Np = 5000) and combine with logmeanexp. Report this as the final log-likelihood for each model/country combination.

**ID: 22.02.4**
**Concern:** Measurement model distribution never specified
**Why it matters:** The paper states that rho is the reporting probability but does not give the distributional form of the observation equation. H(t) is defined as a cumulative count — if the observation model applies to H(t) rather than the daily increment Delta H(t), the model would compare cumulative cases to daily incidence, a serious specification error. Without an explicit statement, the model is not fully defined and cannot be evaluated or reproduced.
**Severity:** Major
**Suggested author action:** State the measurement model explicitly — e.g., `Y_t ~ Binomial(H(t) - H(t-1), rho)` — and confirm the code implements this using the daily increment.

**ID: 22.02.5**
**Concern:** Funeral exposure term likely violates conservation of susceptibles
**Why it matters:** The S-to-E transition is written as the sum of two independent Binomial draws: one from S (community transmission) and one with size F*F_size (funeral transmission). The second draw is not bounded by remaining susceptibles, so the sum can exceed S, removing more individuals from S than are present. This is a compartment conservation violation.
**Severity:** Major
**Suggested author action:** Reformulate using a combined hazard: `Delta N_SE ~ Binomial(S, 1 - exp(-(beta*I/N + beta2*F*F_size/N)*dt))`. This draws from S once with the total force of infection.

**ID: 22.02.6**
**Concern:** No benchmark comparison with non-mechanistic models
**Why it matters:** Without comparing the SEIRDF model's log-likelihood to that of a simpler baseline (ARIMA, auto-regressive negative binomial), there is no way to evaluate whether the mechanistic model provides explanatory value beyond a data-adaptive alternative.
**Severity:** Major
**Suggested author action:** Fit an ARIMA model to log-transformed case counts for each country and report the log-likelihood for comparison.

**ID: 22.02.7**
**Concern:** Parameter convergence absent for most parameters
**Why it matters:** IF2 trace plots (fig_004, fig_009) show that mu_EI, mu_IR, mu_DF, and Beta2 retain large variability at 100 iterations with no convergence to a narrow region. The global search scatter (fig_006, fig_011) confirms that most parameters have no identifiable mode. Conclusions treat the model as if parameters have been estimated, but the inference has not converged.
**Severity:** Major
**Suggested author action:** Report non-convergence as a fundamental limitation. Consider fixing biologically constrained parameters from literature, increasing Np and Nmif, or simplifying the model structure.

---

## Minor Points

**ID: 22.02.M1**
**Concern:** mu_EI parameter values are biologically implausible
**Why it matters:** mu_EI values of 10–20 imply an incubation period of 0.05–0.1 days (~1–2 hours), far shorter than the known Ebola incubation of 2–21 days. Either the units are wrong or the parameter is misinterpreted.
**Severity:** Minor
**Suggested author action:** Clarify units and compare estimated parameter values to published Ebola parameter ranges.

**ID: 22.02.M2**
**Concern:** Population N for Sierra Leone is inconsistent between text and trace plot
**Why it matters:** The text states N = 16,190,280 but fig_009 shows N = 6,190,280. This 10-fold discrepancy, if real, would substantially affect model dynamics.
**Severity:** Minor
**Suggested author action:** Check the code and correct the reported value.

**ID: 22.02.M3**
**Concern:** Death rate fixed at 50% without citation or justification
**Why it matters:** The WHO-reported CFR for this epidemic was approximately 40%. The 50% assumption is neither cited nor estimated, and no sensitivity analysis is reported.
**Severity:** Minor
**Suggested author action:** Cite a source for the 50% CFR or estimate it from data.

**ID: 22.02.M4**
**Concern:** The conclusion about equal CIs is circular
**Why it matters:** The paper acknowledges that identical CIs arise because the same search bounds were used for both countries. The CIs cannot serve as evidence of similarity — they are an artifact of the shared design.
**Severity:** Minor
**Suggested author action:** Remove or substantially qualify the conclusion about similar transmission rates.

**ID: 22.02.M5**
**Concern:** Particle count (Np) and iteration count (Nmif) not reported in text
**Why it matters:** Standard POMP reporting requires these quantities for reproducibility and computational adequacy assessment.
**Severity:** Minor
**Suggested author action:** Report Np and Nmif for both local and global searches.

**ID: 22.02.M6**
**Concern:** All figures lack captions
**Why it matters:** Without captions, readers cannot interpret figures without careful cross-referencing of surrounding text.
**Severity:** Minor
**Suggested author action:** Add descriptive captions to all 12 figures.
