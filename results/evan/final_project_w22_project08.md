# Final AI Review — w22 Project 08
# Analysis of Covid-19 Cases in Turkey

---

## Overall Assessment

This project addresses a genuine modeling challenge — the bimodal structure of Turkey's 2020 COVID-19 case data — by extending a standard SEIR framework into a two-variant SEIREIR model. The motivation is scientifically coherent and the effort put into the global search (160 starting points) is commendable for a course project. However, the paper has several technical problems that collectively undermine its quantitative conclusions. Most critically, the POMP accumulator H tracks the flow of recoveries (dN_IR), while the data represents new daily confirmed cases (incidence); this measurement model mismatch means the entire fitted likelihood surface is for the wrong observation model. Compounding this, optimization had not converged at the time of submission by the authors' own admission, and the benchmark comparison between ARIMA and POMP log-likelihoods is methodologically unsound because the two likelihoods are computed over different observation representations. Additionally, the initial condition sets a large fraction of Turkey's population in the R_b compartment at t=0 — before the beta variant existed — which is biologically implausible. These issues need to be addressed before the paper's conclusions can be trusted.

---

## Key Strengths

**ID: 22.08.S1 — Biologically motivated dual-variant model design**
The SEIREIR structure directly addresses the two-peak pattern in the data by separating original-strain and variant-strain dynamics into distinct E-I-R chains. The model incorporates time-varying transmission parameters to reflect Turkey's April 2020 policy restrictions, which is appropriate and well-motivated by the data.

**ID: 22.08.S2 — Negative binomial measurement model**
The measurement model uses `dnbinom_mu(reports, k, rho*H, give_log)`, correctly implementing a count overdispersion model. Using a negative binomial rather than Poisson for epidemic case counts is appropriate practice.

**ID: 22.08.S3 — Substantial global search effort**
The paper runs 160 starting points for the global search with mif2 across an 8-dimensional parameter space. The resulting pairs plot (fig_012) provides a useful visualization of the optimization landscape and shows parameter clustering, which supports some confidence in the search procedure.

**ID: 22.08.S4 — Transparent reporting of non-convergence**
The authors explicitly state that the local maximum has not been reached and describe this as requiring further investigation. This kind of honest reporting is important and allows the reader to correctly interpret the provisional nature of the MLE.

---

## Major Points

**ID: 22.08.1 — Measurement model mismatch: H tracks recoveries, data is new daily confirmed cases**
Severity: Major

The POMP accumulator H is updated as `H += (dN_IR_o + dN_IR_b)`, recording the flow of individuals from the I to R compartment (recoveries) over each time step. The measurement model then uses `rho*H` as the expected value of the observed `reports`. The data is described as "daily confirmed cases," which represents new confirmed infections — an incidence measure. Recoveries are a downstream, lagged flow and are not equal to new confirmed cases. The model is therefore fitting a likelihood defined over the wrong epidemiological quantity.

Why it matters: The entire likelihood surface — the MLE of -2336, the goodness-of-fit assessment, and the ARIMA comparison — is computed under a misspecified observation model. The parameter estimates and model comparison conclusions cannot be trusted until this is corrected.

Suggested author action: Replace `H += (dN_IR_o + dN_IR_b)` with `H += (dN_EI_o + dN_EI_b)` (or the appropriate new-infection accumulator) and confirm that `accumvars="H"` resets H between observations. Verify that rho then represents a case-detection rate for new infections, which is the standard epidemiological interpretation.

---

**ID: 22.08.2 — ARIMA and POMP log-likelihoods are not directly comparable**
Severity: Major

The conclusion treats the log-likelihood comparison (POMP: -2336 vs. ARIMA: -1692.3) as a valid head-to-head test. However, ARIMA(2,1,0) is fit to the first-differenced series under a Gaussian assumption, while the POMP model is fit to the original daily case counts under a negative binomial assumption. These are likelihoods for different observations, so the numerical values are not on the same scale and the direct comparison is not valid without additional justification.

Why it matters: The benchmark comparison is the paper's main inferential conclusion ("POMP cannot beat ARIMA"). An invalid comparison cannot support any statement about relative model quality.

Suggested author action: Fit an ARMA model to the same original observation sequence (daily case counts) and compute the log-likelihood on that scale. Alternatively, explicitly acknowledge in the text that the numerical comparison is approximate because the two models use different data representations, and discuss what qualitative conclusion — if any — can still be drawn.

---

**ID: 22.08.3 — No profile likelihoods or confidence intervals**
Severity: Major

The paper reports a single-point MLE but provides no profile likelihoods for any parameter and no confidence intervals. The pairs plots visualize joint optimization outcomes but cannot indicate whether parameters are individually identifiable. The local search trace plots show eta failing to converge, which is a signal of potential non-identifiability. Without profiles, no scientifically meaningful statement about transmission rates (Beta_o, Beta_b, Beta_or) or the relative effect of government restrictions can be made.

Why it matters: Parameter estimation without uncertainty quantification cannot support biological interpretation. Profile likelihoods are the standard tool for this in the POMP framework.

Suggested author action: Compute profile likelihoods for at least Beta_o, Beta_b, Beta_or, rho, and eta. Report 95% confidence intervals using the MCAP procedure. For parameters that appear non-identifiable (e.g., eta), explicitly state this and discuss implications for model interpretability.

---

**ID: 22.08.4 — Biologically implausible initial condition: R_b = (1-eta)*N at t=0**
Severity: Major

The rinit Csnippet sets `R_b = nearbyint((1-eta)*N)`, placing potentially tens of millions of people in the "recovered from beta variant" state at the start of the epidemic (early 2020). The beta variant had not emerged at that time, and no individuals could have been in R_b. This initial condition is biologically impossible and may cause the model to dramatically underestimate susceptibility at the start of the second wave.

Why it matters: Incorrect initial conditions bias all inferred parameters and the fitted trajectories. The model is initialized in an epidemiologically impossible state.

Suggested author action: Set R_b = 0 at t=0. Review all initial compartment assignments. If (1-eta)*N was intended to represent people immune to the original strain (e.g., due to prior immunity from other coronaviruses), this should be stated explicitly and assigned to a different compartment, not R_b.

---

**ID: 22.08.5 — Optimization has not converged; mu_IR_o inconsistency across code blocks**
Severity: Major

The authors explicitly state convergence has not been achieved. Additionally, the initial parameter vector used for the "Simulated graphs" section sets mu_IR_o=0.02, while the fixed_params block used for all optimization sets mu_IR_o=0.05. These represent different assumptions about the recovery rate and the two simulations are not directly comparable.

Why it matters: The reported MLE of -2336 is a lower bound, not a true maximum. The mu_IR_o inconsistency means the pre-optimization and post-optimization simulations differ on a fixed parameter, confounding any comparison between them.

Suggested author action: Resolve the mu_IR_o inconsistency and document the chosen value with rationale. Increase Nmif (currently 50) and run additional restarts. Fix `%do%` to `%dopar%` in the local search block (currently sequential despite a registered parallel backend). Report evidence of convergence by showing stability of the best log-likelihood across independent restarts.

---

## Minor Points

**ID: 22.08.m1 — Population figure inconsistency**
The text states "N=843400[4]," citing a W21 project on Washtenaw County, Michigan. The code uses N=84,340,000, which is Turkey's population. The text value is wrong by a factor of 100 and the citation is erroneous. Correct the text to N=84,340,000 and cite an appropriate Turkish statistical source.

**ID: 22.08.m2 — Beta variant seed is hard-coded without sensitivity analysis**
The Csnippet adds exactly 10 individuals to E_b at t=125 with no justification for the timing or the seed size. The model's second-wave dynamics depend on this seed. Test sensitivity to the seed size (e.g., e=1, 50, 100) and seed timing (±2 weeks) and report the effect on the fitted log-likelihood.

**ID: 22.08.m3 — ESS collapse early in filtering is not addressed**
Figure 008 shows ESS dropping near zero during approximately days 5–25 — the initial epidemic ramp-up, which is the most data-informative period. The text notes this briefly but does not discuss its implications for the reliability of the likelihood estimate or explore whether increasing Np resolves it.

**ID: 22.08.m4 — Simulation envelope far exceeds observed data range**
Both fig_009 and fig_013 show simulation envelopes spanning from near zero to approximately 150,000 cases/day, roughly twice the observed maximum (~80,000). This wide spread suggests the model is not calibrated tightly to the data at the MLE. Discuss this quantitatively and consider whether it reflects measurement model misspecification, overdispersion in k, or parameter uncertainty.

**ID: 22.08.m5 — Periodogram figure appears missing**
The text states the periodogram was plotted to check for periodicity, but the corresponding figure does not appear in the rendered manuscript. Include the periodogram or remove the claim.

**ID: 22.08.m6 — ARIMA model selection: AIC and LRT disagree without explanation**
The AIC table favors ARIMA(2,1,1) (AIC=3385.08) but the LRT rejects the MA(1) term and the paper selects ARIMA(2,1,0) (AIC=3390.61). Both conclusions can be valid, but when they disagree, the rationale for preferring one criterion over the other should be stated explicitly.

**ID: 22.08.m7 — Figure captions are absent throughout**
No figure has a descriptive caption. Add captions that describe what each figure shows and what the key takeaway is.
