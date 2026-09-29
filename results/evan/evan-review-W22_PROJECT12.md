# Final AI Review: Modeling COVID-19 Cases in Michigan (w22 Project 12)

---

## Overall Assessment

This project tackles a well-motivated problem — modeling the Omicron wave of COVID-19 in Michigan — with a sensible dual strategy: ARIMA models for baseline exploration and a SEIR POMP model for the mechanistic analysis. The methodological fundamentals are solid: IF2 is used for optimization, log-likelihoods are aggregated via logmeanexp with standard errors, and a global search over 400 starting points is conducted. The authors honestly acknowledge that forward simulations show excess variance relative to data. However, several important deficiencies limit the reliability of the conclusions. Most critically, the dmeas and rmeas code snippets implement different variance formulas — creating an internal inconsistency between the density used for filtering and the simulator used for forward simulation. The claim that SEIR is "much more explanatory" than ARIMA is never quantified via a direct log-likelihood comparison. No profile likelihoods or confidence intervals are reported, and the MLE reporting rate (rho ≈ 0.995) sits at the boundary of the parameter space — a strong signal of potential misspecification that is not adequately addressed.

---

## Key Strengths

**ID: 22.12.8 | Correct likelihood aggregation**
logmeanexp is used correctly to pool replicated particle-filter log-likelihoods, and Monte Carlo standard errors are reported throughout. This is a methodologically important practice that prevents the common error of averaging log-likelihoods.

**ID: 22.12.9 | Thorough global search**
Four hundred starting points drawn from a biologically informed box provide reasonable coverage of the parameter space. The combination of local and global searches follows good practice.

**ID: 22.12.10 | Particle-filter diagnostics shown**
ESS and conditional log-likelihood panels are presented at the initial parameter values, demonstrating awareness of particle-filter diagnostics.

**ID: 22.12.11 | Honest model assessment**
The authors explicitly note that the final simulations show "variance in the number of cases of our simulations is much higher than the actual data," flagging a clear avenue for model improvement rather than overclaiming.

---

## Major Points

**ID: 22.12.1 | Missing benchmark comparison**
Severity: Major

The conclusion states that SEIR is "much more explanatory than using ARIMA," but no quantitative comparison is made. The ARIMA(5,1,5) model was fit to the same 134-observation Omicron window as the SEIR model, and its log-likelihood is available from the arima() output, yet it is never reported alongside the SEIR log-likelihood of -1155. Without this comparison, the central interpretive claim of the paper is unsubstantiated. Note that AIC differences between ARIMA and POMP models require care due to differences in likelihood conventions; the comparison should be stated at the log-likelihood level and any scale discrepancies noted.

Suggested action: Extract the log-likelihood of ARIMA(5,1,5) on the Omicron data (use logLik() on the fitted arima object) and compare it numerically against the best SEIR log-likelihood. Discuss whether the comparison is valid on a common scale.

**ID: 22.12.2 | Measurement model inconsistency between dmeas and rmeas**
Severity: Major

The density snippet (seir_dmeas) uses the standard deviation formula sqrt(psi^2 * H^2 + rho * H), while the simulator snippet (seir_rmeas) uses sqrt((psi * rho * H)^2 + rho * (1 - rho) * H). Neither formula matches the written measurement model on p. 6, which specifies variance = rho*(1-rho)*H + (psi*rho*H)^2. Because the particle filter and IF2 use dmeas to evaluate likelihoods and rmeas to propagate the state, this inconsistency means the fitted density and the forward simulator correspond to different distributions. This undermines both the likelihood estimates and the visual comparisons between simulated and observed trajectories.

Suggested action: Decide on one canonical variance formula — the written equation on p. 6 is a reasonable choice — and implement it identically in both dmeas and rmeas. Re-run the full inference pipeline with the corrected code.

**ID: 22.12.3 | No profile likelihoods or confidence intervals**
Severity: Major

The paper reports MLE point estimates but provides no profile likelihoods or uncertainty quantification for any parameter. The pairs plot (Figure 18) shows that psi and rho are poorly concentrated: rho piles up near 1.0 (at the upper boundary of its logit-transform range) and psi spans roughly 0.5–0.9 without clear concentration. An MLE at a parameter boundary is a red flag for model misspecification or non-identifiability and requires investigation via profiling rather than accepting the boundary value as the answer.

Suggested action: Compute profile likelihoods for rho and eta at minimum. If the profile for rho is flat near 1, this indicates the model cannot distinguish rho = 0.8 from rho = 1.0, and the reporting-rate interpretation should be tempered. MCAP-based confidence intervals are the appropriate method for this type of model.

**ID: 22.12.7 | Fixed mu_EI and mu_IR without sensitivity analysis**
Severity: Major

The infectious period (mu_IR = 0.14/day) and incubation rate (mu_EI = 0.33/day) are fixed throughout all searches. These values imply specific epidemiological assumptions about the Omicron variant that, while literature-informed, are uncertain. All downstream parameter interpretations — including the basic reproduction number R0 = beta0/mu_IR — depend on these fixed values. No sensitivity analysis assesses how the MLE of beta0, eta, or rho would shift under different mu_EI or mu_IR values.

Suggested action: Conduct a sensitivity analysis by re-running the global search under two alternative sets of (mu_EI, mu_IR) values bracketing the literature range, or compute profile likelihoods treating these as free parameters. Report whether conclusions about beta0 and eta are robust.

---

## Minor Points

**ID: 22.12.5 | Potential under-convergence in global search**
Severity: Minor

The local search trace plots (Figure 16) show that several IF2 chains have not converged by iteration 50 — log-likelihood values at the end of the run still span from about -1200 to -1500. The global search uses the same Nmif=50 budget (inherited via chained mif2). Increasing Nmif to 100–200 for the global runs, or demonstrating that the best log-likelihoods are stable across repeated runs, would strengthen the convergence claim.

**ID: 22.12.6 | ADF test applied to differenced series**
Severity: Minor

The ADF test is applied to the already-differenced case series and the result cited as justification for using d=1. The logic is somewhat circular: the test confirms stationarity after differencing but does not test the raw series or choose between differencing and other detrending strategies. A brief note clarifying this and showing the ACF or ADF result on the raw series would improve the argumentation.

**ID — ESS collapse at end of time series**
Severity: Minor

Figure 15 (particle filter check at initial parameters) shows ESS collapsing near zero at approximately t = 120–134, accompanied by very negative conditional log-likelihoods at the same time points. This pattern at the tail of the Omicron wave — where observed cases return to near zero — suggests the model has difficulty tracking the descent phase. This is worth noting as evidence of possible model misspecification in the recovery dynamics.

**ID — Hard-coded regime change at t = 33**
Severity: Minor

The beta regime switch in seir_step is hard-coded as `if(t > 33)`. The motivation ("around the inflection point") is qualitative, and the sensitivity of results to this threshold is unexplored. Making t_switch a parameter, or at minimum justifying day 33 from the data (e.g., showing it corresponds to the peak of the Omicron wave), would improve transparency.

**ID — Initial compartment values E=30000, I=15000 not justified**
Severity: Minor

E and I initial values are hard-coded in seir_rinit without reference to data or prior estimates. For a 4-month window, the initial conditions influence the early rise of the modeled epidemic. A brief sensitivity check or derivation from cumulative case counts at the start of the window would strengthen the analysis.

**ID — rho at boundary signals potential misspecification**
Severity: Minor

The MLE rho = 0.995 is epidemiologically implausible for COVID-19 (a reporting rate of 99.5% is not consistent with known under-reporting), suggesting the model may be absorbing unexplained variation into rho. The authors note that psi and rho lack convergence, but do not discuss the epidemiological implication. This interpretation should be highlighted.
