# Peer Review: W22 Project 06
**Title:** Rubella Transmission POMP Model [1966-1967]
**Reviewer:** Charlie
**Semester:** W22, Project 06

---

## Summary

This project fits a stochastic SEIR POMP model to weekly reported rubella cases in California from 1966 to 1967, using iterated filtering (mif2) for likelihood maximization and profile likelihoods for two key parameters. The paper demonstrates a solid grasp of the POMP modeling workflow, including local and global search, trace plot diagnostics, and profile likelihood construction. However, several issues undermine the validity of the presented results: a critical discrepancy between the mathematical description and the rprocess code (E vs. I in the force of infection), incorrect signs in the state-equation presentation, a measurement model with a non-standard parameterization that is not explained, an eta profile that fails to identify the maximum (acknowledged but not resolved), missing benchmark comparison, and fixed epidemiological rate parameters that are left unjustified. These issues collectively prevent reliable inference from the fitted model.

---

## Major Issues

### 1. Force-of-Infection Discrepancy Between Text and Code (CC-Yes, Error 1.3 analog)

The mathematical model description (Section "SEIR Modeling") states that the transition from S to E follows:

> Delta N_SI ~ Binomial(S, 1 - exp(-beta * E/N * dt))

However, the `seir_step` Csnippet (line ~197) computes:

```
double dN_SE = rbinom(S, 1-exp(-Beta*I/N*dt));
```

The code uses **I** (infected) in the force of infection, not **E** (exposed). This is the standard SEIR convention — the force of infection should depend on I, not E. However, the mathematical presentation in the text uses E, making it inconsistent with the code. This notation error may reflect a misunderstanding of the SEIR structure (in a standard SEIR, exposed individuals do not transmit). The authors must clarify which compartment drives transmission in their model and correct either the equation or the code.

**Actionable fix:** Revise the equation in the text to match the code (use I), or revise the code to use E and provide biological justification for infectious-but-not-yet-symptomatic transmission.

---

### 2. Sign Errors in the State Equation Presentation

The state equations presented in the "SEIR Modeling" section contain two sign errors:

- S(t) = S(0) **+** N_SE(t) — should be **minus** (susceptibles decrease as they move to E)
- R(t) = R(0) **-** N_IR(t) — should be **plus** (recovered individuals accumulate)

The code (`seir_step`) correctly subtracts from S and adds to R, so the model itself is implemented correctly. The mathematical presentation, however, is wrong. This creates confusion about what the model actually does and undermines scientific clarity.

**Actionable fix:** Correct the signs in the S and R equations to match the code.

---

### 3. Measurement Model Parametrization Unexplained and Non-Standard

The `dmeas` Csnippet uses:

```
lik = dnbinom(reports, H, rho, FALSE);
```

In R's `dnbinom(x, size, prob, log)`, this sets **size = H** (the accumulator for recovered individuals) and **prob = rho** (reporting rate). This is an unusual parameterization: the dispersion of the negative binomial distribution varies with H each week, making the measurement model non-standard and hard to interpret. Typically, a POMP measurement model uses a fixed overdispersion parameter (e.g., `dnbinom_mu(reports, mu=rho*H, size=psi, give_log=give_log)`) where the mean scales with H via the reporting rate and dispersion is a fixed parameter.

No justification is provided in the paper for using this parameterization. Its statistical properties (e.g., that the variance is H*(1-rho)/rho^2, which changes with the accumulator) are not discussed. If this parameterization is intentional, it requires explicit justification; if unintentional, the measurement model needs to be revised.

**Actionable fix:** Specify the intended measurement model clearly in the text. If the goal is a negative binomial with mean rho*H and fixed overdispersion psi, revise both dmeas and rmeas accordingly and re-run the analysis.

---

### 4. Global Search Uses Only mifs_local[[1]] as Starting Template

The global search code (line ~452) calls:

```r
mif2(mifs_local[[1]], params = c(apply(rubella_box, 1, function(x) runif(1, x[1], x[2])), rubella_fixed_params))
```

This reuses `mifs_local[[1]]` — the **first** local mif2 object — as the template for all global search runs. This means the random-walk standard deviations and cooling settings come from a single fixed local search result. The standard course approach (and best practice) is to use `mifs_local[[sample(length(mifs_local), 1)]]` or equivalent, drawing the template randomly from the full set of local results, so that starting configurations are diverse. Using a single fixed template means the global search may not actually explore the parameter space as intended; all runs share identical mif2 settings inherited from one local run.

**Actionable fix:** Replace `mifs_local[[1]]` with a randomly sampled element from `mifs_local`, or apply `mif2` directly to the `rubellaSEIR` object with the random starting parameters.

---

### 5. eta Profile Fails to Identify the Maximum; CI Is Invalid

The authors acknowledge in the text (Section "Likelihood Profile for eta"): "the graph states that our eta did not reach the confidence interval cutoff." Despite this acknowledgment, a confidence interval of (0.19%, 0.24%) is still reported in Table 4 and cited in the conclusion. A profile likelihood that does not include any points above the Wilks threshold cannot support a valid confidence interval — the CI computation in this case takes the range of all eta values that happen to be in the data frame after filtering, not a well-defined Wilks interval.

The range of eta in the profile (0.002 to 0.0026) is also extremely narrow (a factor of 1.3 difference). If the profile maximum is outside or at the boundary of this range, the profile is uninformative and the CI is not reliable. This is a fundamental validity issue for one of the two profile analyses in the paper (CC-Yes, Error 1.9 analog).

**Actionable fix:** Expand the eta range substantially (e.g., by an order of magnitude), re-run the profile until a clear interior maximum is found, and only then compute the CI.

---

### 6. Flow Rates Fixed Without Literature Justification

The parameters mu_EI = 0.08 (week^-1, implying a mean latent period of ~12.5 weeks) and mu_IR = 0.4 (week^-1, implying a mean infectious period of 2.5 weeks) are fixed throughout the analysis with no biological justification provided. For rubella, the known latent period is approximately 2-3 weeks and the infectious period is approximately 1 week. The value mu_EI = 0.08 implies a latent period of 12.5 weeks, which is roughly 4-6 times longer than the known biology. Fixing parameters at biologically implausible values introduces structural misspecification. Per Wheeler et al. (2024), implausible parameter values should be flagged as potential signs of model misspecification, not treated as fixed inputs.

**Actionable fix:** Either estimate mu_EI and mu_IR as free parameters (with appropriate rw.sd), or fix them at biologically supported values (mu_EI ~ 0.5/week for a 2-week latent period, mu_IR ~ 1/week for a 1-week infectious period) and cite the supporting literature.

---

### 7. No Benchmark Comparison

The POMP model's fit (log-likelihood approximately -557) is never compared to any non-mechanistic benchmark. No ARMA, regression, or even IID model likelihood is reported. Without this comparison, it is impossible to assess whether the SEIR model captures meaningful structure beyond a simple statistical baseline. This is an explicitly course-taught requirement (CC-Yes, Error 1.6): a benchmark comparison reveals whether the mechanistic model adds value. Wheeler et al. (2024) note that none of the Haiti cholera papers they reviewed performed such a comparison; their benchmark analyses revealed that some mechanistic models failed to beat simple auto-regressive models.

**Actionable fix:** Fit an ARMA or negative binomial regression model to the rubella counts and compare log-likelihoods directly. Even a simple IID negative binomial provides a meaningful floor for model comparison.

---

### 8. No Model Diagnostics

No diagnostic analysis is presented beyond visual simulation overlay (Figures 4, 7, 10). The paper includes no:
- Conditional log-likelihood plot over time (to identify periods of poor fit)
- Effective sample size (ESS) monitoring during particle filtering
- Filtering distribution comparison (simulating forward from the filter vs. from initial conditions)

Wheeler et al. (2024, Section "Model diagnostics") note that conditional log-likelihood plots have been key to discovering model failures (e.g., inability to explain specific outbreak surges) and motivating structural improvements. The absence of these diagnostics leaves it unclear whether the model adequately captures the data-generating process.

**Actionable fix:** Add a conditional log-likelihood plot using the best-fitting parameters and at least check ESS across time.

---

## Minor Issues

### 9. Data Truncation Unexplained

The code loads 501 weeks of California rubella data (1966-1975) but then truncates to the first 105 weeks (`Rubella_CA <- Rubella_CA[1:105,]`) without explanation. The title states the analysis covers 1966-1967 (approximately 104 weeks), so the truncation is presumably deliberate, but no rationale is given. The variable description also confusingly mentions dates in the range 1996-1975 (likely a typo for 1966-1975) when describing the data loading step.

---

### 10. rho Profile CI Implausibly Narrow

The reported 95% confidence interval for rho is (4.83%, 5.52%) — a width of only 0.69 percentage points. Given the Monte Carlo noise in the profile computation (Np=1000, 10 replications) and the large parameter space being optimized at each profile point, such a narrow interval is suspicious. The profile plot uses a LOESS smoother over only 30 rho values with 15 starting points each; the apparent precision may reflect Monte Carlo artifacts rather than genuine identifiability. The authors should assess whether the interval width is robust to changes in the random seed.

---

### 11. run_level = 2 with Potentially Insufficient Global Search

The analysis uses run_level=2 with Np=1000, Nmif=100, and Nreps_global=60. The global search trace plots (Figure 8) show that b1, b2, and eta do not converge from diverse starting points. The authors note this but attribute it to poor identifiability. Given that the measurement model parametrization may be non-standard (Issue 3 above), it is difficult to separate genuine weak identifiability from computational or model misspecification issues. The profile for rho uses only Nmif=40+40 iterations with cooling.fraction.50=0.3, which is more aggressive cooling than the main search.

---

### 12. Initial Conditions E=14 and I=7 Fixed Without Justification

The rinit Csnippet hardcodes E=14 and I=7 as starting compartment counts. No justification is provided for these specific values. While fixing initial conditions is acceptable in the course context (531-conventions.md), the choice of these specific values (which together imply 21 people were in exposed/infected states at the start of the analysis period) should be motivated, for example by back-calculating from early case counts.

---

### 13. Typo in Data Description: "1996-1975"

The code comment and surrounding text describe the time sequence as "starting from 1996 to 1975" — this is clearly a typo for 1966 to 1975. While minor, this creates confusion about the time period under analysis.

---

### 14. Pairs Plot Comment Left in Draft State

Figure 9 has a section header reading "Pairwaise relationships (not sure if we need to inclue this part)" — this is an internal note that was not removed before submission. The header should be cleaned up in the final version.

---

### 15. Conclusion Overstates Model Fit

The conclusion states "we can now say that Rubella in California from the 1966 to 1967 can be well modeled by the SEIR model" based primarily on visual fit. Given the unresolved issues with the eta profile, the non-standard measurement model, and the lack of benchmark comparison, this conclusion is not fully supported by the analysis. A more cautious statement is warranted.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project06/blinded.Rmd`
