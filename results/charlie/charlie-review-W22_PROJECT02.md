# Peer Review: W22 Project 02
## "Investigation of Ebola in Guinea and Sierra Leone"

---

## Summary

This project applies a SEIRDF (Susceptible-Exposed-Infectious-Recovered-Dead-Funeral) POMP model to WHO Ebola case data from Guinea and Sierra Leone (2014–2016), motivated by the hypothesis that funeral transmission is a primary driver of spread. The authors use iterated filtering (mif2) with local and global searches and compute profile likelihoods for the contact rate parameter Beta. While the paper demonstrates familiarity with the pomp workflow and addresses a scientifically motivated modeling question, it contains several serious methodological and implementation errors that undermine the validity of its conclusions. The most critical issues are: a fundamentally flawed measurement model (binomial with accumulator H is applied incorrectly), incorrect parameter transformations applied to F_size (which is fixed), biologically implausible parameter estimates that are not flagged, the profile likelihood implementation does not vary Beta (making it a likelihood slice, not a profile), no benchmark comparison, and no quantitative goodness-of-fit measures for model comparison. The conclusion that Guinea and Sierra Leone have "the same transmission rate" is not supported by the evidence presented.

---

## Major Issues

### 1. Measurement Model Applied to Accumulator H: Severe Misspecification (CC-Yes, Error 1.3)

The dmeas and rmeas snippets condition observations on the accumulator variable H:

```c
lik = dbinom(reports, H, rho, FALSE) + tol;
reports = rbinom(H, rho);
```

However, H is defined as a running total (`H += dN_IR`) and is reset via `accumvars="H"` only at observation times. This means H accumulates all transitions from I to R+D over the entire inter-observation interval, but it is never reset to zero between observations in the C snippet itself — the pomp accumvars mechanism handles the reset. The measurement model thus treats the *total* number who have left the I compartment since the last observation as the "size" parameter for a binomial, and rho as the reporting probability. However, the transition dN_IR captures those going to *both* R and D, not a clearly defined "cases" count. More critically, reporting rate rho applied to dN_IR (not to dN_EI or new symptomatic incidence) conflates the symptomatic period with reporting, producing a conceptually muddled measurement model whose parameters cannot be interpreted epidemiologically.

Additionally, the tolerance structure `tol = 1e-25` is added to the raw probability (not the log-likelihood), but if `give_log=TRUE` is applied after taking `log(lik + tol)`, this handles the zero case; however when H=0 and reports=0, the likelihood is set to tol instead of 1 (certainty), which may distort the likelihood surface. This implementation differs from best practice (e.g., the course POMP examples where dmeas correctly handles the accumulator).

**Fix:** Redefine H to track new symptomatic cases (dN_EI per interval), with appropriate overdispersion (negative binomial), and ensure the dmeas/rmeas snippets correctly represent the intended observation model.

---

### 2. Profile Likelihood for Beta is a Likelihood Slice, Not a Profile (CC-Yes, Error 1.2)

In the profile likelihood computation for Beta in both countries, the code draws starting parameter values uniformly from the box for *all* parameters including Beta itself:

```r
runif_design(
    lower=c(Beta=3, Beta2=0.5, mu_EI=10, mu_IR=0.7, mu_DF=0.5, rho=0.35, eta=0),
    upper=c(Beta=7, Beta2=1.5, mu_EI=20, mu_IR=1.2, mu_DF=1.2, rho=0.45, eta=0.1),
    nseq=500
) -> guesses
```

Then mif2 is run with rw.sd that includes *all* parameters except Beta itself — but Beta is not fixed to a specific profiled value. The profile rw.sd in the Guinea profile is:

```r
rw.sd=rw.sd(Beta2=0.002, mu_EI=0.002, mu_IR=0.002, mu_DF=0.002, rho=0.002, eta=ivp(0.002))
```

Beta is absent from rw.sd, which means mif2 will not perturb Beta during optimization, but Beta's initial value still varies freely across the 500 guesses spanning [3, 7]. This is not a true profile likelihood. A valid profile requires: for each fixed value of Beta on a fine grid, maximize the log-likelihood over all other parameters. What is computed here is effectively the scatter of likelihood evaluations across random Beta values, grouped post-hoc. The resulting "profile" is really a global search scatter plot filtered by Beta value, not a profile that properly marginalizes nuisance parameters. The confidence interval derived from this (3.003 to 6.974) essentially spans the entire search box and provides no real inferential content.

**Fix:** Implement a proper profile by fixing Beta to a sequence of values, then running mif2 with rw.sd on all other parameters (but Beta excluded from rw.sd and fixed in params), producing the true profile likelihood envelope. See course notes Ch. 16.

---

### 3. F_size is Fixed but Included in log() Parameter Transformation

The model applies a log transformation to F_size:

```r
partrans=parameter_trans(
    log=c("Beta","Beta2","mu_EI","mu_IR","mu_DF","F_size"),
    logit=c("rho","eta")
)
```

Yet F_size is never estimated — it is fixed at 50 in both the global search and profile likelihood:

```r
fixed_params = c(F_size=50, N=10628972)
```

Applying a log transformation to a parameter that is fixed and never estimated is not an error per se (the transform is applied consistently), but it is logically inconsistent: if F_size is to be fixed, it need not appear in partrans, and its inclusion there could cause confusion and potential issues in downstream code.

More substantively, F_size = 50 is never justified biologically or empirically — no citation or sensitivity analysis is provided for this value. The effect of the funeral compartment on transmission depends entirely on F_size, which is fixed without justification.

**Fix:** Remove F_size from partrans or estimate it. Provide a literature-based justification for F_size = 50 or perform a sensitivity analysis.

---

### 4. No Non-Mechanistic Benchmark Comparison (CC-Yes, Error 1.6)

The paper presents no comparison of the SEIRDF model's likelihood against any non-mechanistic benchmark (ARMA, IID negative binomial, regression). The maximum log-likelihood for Guinea is approximately -6515. Without a benchmark, it is impossible to assess whether the SEIRDF model captures meaningful structure in the Ebola data beyond what a simple statistical model would achieve. Given that the model fit appears poor (very wide beta CI, non-convex profile), a benchmark would be informative about whether the model adds value.

**Fix:** Fit an ARMA or auto-regressive negative binomial model to the case counts and report its log-likelihood alongside the POMP model.

---

### 5. Biologically Implausible Parameter Estimates Not Discussed

The best-fit Guinea parameters show mu_EI ≈ 14.9 (day^-1), which would imply an average incubation period of 1/14.9 ≈ 0.067 days — roughly 96 minutes. The known Ebola incubation period is 2–21 days (mean ~8–12 days). Similarly, the initial estimate used in simulation was mu_EI = 15 (days^-1), already biologically implausible. The authors do not flag this discrepancy or discuss it. Per Wheeler et al. (2024), implausible parameter estimates may indicate model misspecification and should be interpreted cautiously, not silently accepted.

**Fix:** Report parameter estimates with units. Compare mu_EI to known Ebola incubation periods. Consider fixing mu_EI to a biologically plausible range or imposing a prior.

---

### 6. Measurement Model Does Not Include Overdispersion

The measurement model uses a binomial distribution for reported cases:
```c
lik = dbinom(reports, H, rho, FALSE) + tol;
```

A binomial measurement model is typically under-dispersed for infectious disease count data. Per Wheeler et al. (2024) and course notes (Ch. 16), a negative binomial measurement model is preferred to capture overdispersion that arises from clustering and reporting heterogeneity. No justification is given for using the binomial, and no diagnostic (e.g., residual plots, simulation-based checks) is presented to assess whether binomial adequately describes the variance structure.

**Fix:** Replace the binomial measurement model with a negative binomial model with an estimated overdispersion parameter.

---

### 7. rw.sd Values Are Too Small for Parameters Estimated in Natural (Not Log) Scale

The iterated filtering perturbation size is set uniformly to 0.002 for all parameters:

```r
ebola_rw.sd <- rw.sd(
    Beta=0.002, Beta2=0.002, mu_EI=0.002, mu_IR=0.002, mu_DF=0.002, rho=0.002, eta=ivp(0.002)
)
```

Per course convention (Ch. 15, p31), rw.sd = 0.02 on the log/logit scale is standard. While the parameters here are estimated on the log/logit scale (due to partrans), rw.sd = 0.002 is 10x smaller than the course standard. This will result in very slow exploration of the parameter space during local search and may explain why the local search traces show poor convergence or high variability. The small perturbation size effectively limits the optimizer's ability to escape local maxima.

**Fix:** Increase rw.sd to approximately 0.02 for parameters on the log/logit transformed scale.

---

### 8. No Quantitative Goodness-of-Fit Summary Reported in Paper Body

While log-likelihood values are computed and stored in CSV files (Guinea best loglik ≈ -6515), they are never explicitly reported in the text of the paper. The conclusions are drawn from visual inspection of simulation overlays and from the CI bounds of the profile. Per Wheeler et al. (2024), "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The paper should report the maximum log-likelihood value for each country's model so readers can assess model quality.

**Fix:** Report the maximum log-likelihood (with SE) for each fitted model in the results section.

---

### 9. Initial Conditions Fixed at Implausible Values Without Justification

The Guinea initialization fixes I = 482 (initial infected) and the Sierra Leone initialization fixes I = 935:

```c
S = nearbyint(eta*N) - 482;
I = 482;
```

These values are asserted without explanation or citation. The number 482 (Guinea) does not correspond to any obvious epidemiological quantity. The variable eta controls the susceptible fraction but its MLE (~0.00062 from Guinea_params.csv) implies only 0.062% of the population is susceptible at t=0 — an extremely small and biologically questionable value for a country with no prior Ebola immunity. No sensitivity analysis is conducted for these initial conditions. Per Wheeler et al. (2024), initialization strategy can affect AIC by ~72 units.

**Fix:** Estimate I_0 as a free parameter, or provide a data-based justification for fixing it. Discuss sensitivity to initial conditions.

---

### 10. Sierra Leone Population Misspecified in Simulation vs. Model Fitting

The simulation for Sierra Leone uses N = 6,190,280 (line 466 in blinded.Rmd):

```r
params <- c(Beta=20, Beta2=1, mu_EI=12, mu_IR=2, mu_DF=1, F_size=50, rho=0.3, eta=0.025, N=6190280)
```

But the fixed_params in the global search uses the same value N = 6,190,280. However, the actual population of Sierra Leone in 2014 was approximately 7.1 million, not 6.19 million. Guinea's population is correctly specified as 10,628,972. The Sierra Leone population appears to be approximately 1 million short. While this may be a minor data error, it will affect the epidemic dynamics since N appears in the force of infection term (Beta*I/N).

**Fix:** Verify and correct the Sierra Leone population to the 2014 census value (~7.1 million).

---

### 11. Conclusion That Guinea and Sierra Leone Have "Same Transmission Rate" is Unsupported

The paper concludes: "we observe same confidence interval of beta in the two countries, which indicates that the transmission rate is close." However, the authors explicitly acknowledge: "This exact same confidence interval of the two countries may not seem convincing, but this is because we set the same lower and upper bounds and same number of evened space for global search." The identical CI bounds are an artifact of the search box design, not an inference from the data. Furthermore, as noted above, the profile likelihood is not a true profile and the CI essentially spans the entire search range. The conclusion is therefore unsupported.

**Fix:** Revise the conclusion to accurately represent what can and cannot be inferred from the analysis. A proper profile likelihood computed for each country separately with different search bounds would be needed to compare Beta between countries.

---

### 12. Funeral Compartment F is Assigned (Not Accumulated): Epidemic Dynamics May Be Incorrect

In the step function:

```c
F = round(dN_DF);
```

The funeral compartment F is *set* equal to the number of new funerals at each step, rather than accumulated. This means F represents only the instantaneous new funerals at each time step, not the total active funerals. If funerals last more than one time step (dt = 1 day), this underestimates the funeral-related exposure. The model description states "F denotes the number of funerals" but the code tracks only new funerals per step. This is inconsistent with the model diagram and equations in the text, where F(t) = delta_N_DF appears to be intended as a flow, but the exposure term in the force of infection is F * F_size, suggesting F should represent concurrent funerals.

**Fix:** Clarify the biological interpretation of F. If F is meant to represent concurrent active funerals at time t (lasting multiple days), the compartment should accumulate and decay appropriately.

---

### 13. No Model Diagnostics Beyond Visual Simulation Comparison

The paper provides simulated trajectories overlaid on data, but no model diagnostics are shown: no conditional log-likelihood plots, no effective sample size monitoring, no filtering distribution comparisons. Per Wheeler et al. (2024), these diagnostics help identify periods of poor fit and model misspecification. The trace plots show convergence for the loglik only; no residual checks are performed.

**Fix:** Include at least one set of model diagnostics, such as per-observation conditional log-likelihoods or ESS traces from the particle filter.

---

### 14. Global Search Results Duplicated in Guinea_params.csv

The Guinea_params.csv file is produced by:

```r
results %>%
  bind_rows(results) %>%
  ...
  write_csv("Guinea_params.csv")
```

The results dataframe is bound to itself (`bind_rows(results, results)`), duplicating every row. This is a code bug that inflates the apparent size of the global search and could affect downstream analysis if row counts matter.

**Fix:** Remove the `bind_rows(results)` duplication and use `results` directly.

---

### 15. No Discussion of R0 or Epidemiologically Meaningful Parameter Summaries

The paper's research question asks about transmission rates, but no reproduction number R0 is computed or discussed from the fitted parameters. The citation to Weitz and Dushoff (2015) specifically concerns R0 estimation and identifiability in SEIRDF models, but the paper does not follow through with this calculation. Given that the authors motivated the SEIRDF model by noting that simpler models "seriously underestimated" R0, failing to compute R0 from the fitted model is a missed opportunity.

**Fix:** Compute R0 from the fitted parameters (using the next-generation matrix or the relation discussed in Weitz and Dushoff 2015) and compare to literature values for the 2014 Ebola epidemic.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project02/Guinea_params.csv`
