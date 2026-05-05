# Peer Review: W24 Project 10
## "POMP Analysis on Covid-19 Cases in Malaysia and Influenza in the U.S."

---

### Summary

This project applies an SEIRV compartmental POMP model to two disease datasets: weekly COVID-19 cases in Malaysia (2021-2022) and weekly U.S. Influenza A cases (2017-2018). The COVID-19 analysis is presented as a failure case to motivate the flu analysis, where local search, global search, and a profile likelihood over the vaccination rate parameter are reported. The best log-likelihood achieved for the flu model is -306.821. Several critical issues undermine the technical rigor of the work.

---

### Weaknesses (most critical first)

**1. [Critical] Bug: `dN_RS` drawn from `I` instead of `R` in COVID step function**

In the COVID SEIRV step function (lines 222), the R-to-S waning/reinfection transition is implemented as:
```c
double dN_RS = rbinom(I, 1-exp(-mu_RS*dt));
```
The first argument should be `R` (the number currently in the Recovered compartment), not `I`. Drawing from `I` means the code is actually removing individuals from `R` in proportion to `I`, which is nonsensical: when `R` is large and `I` is small, the reinfection flow is understated, and vice versa. This is a fundamental coding error in the process model that invalidates the COVID SEIRV dynamics. Notably, the flu step function (lines 357-370) drops the `dN_RS` transition entirely — making the flu model an SEIV model without the R-to-S loop, contradicting the stated SEIRV description and the motivation for including waning immunity.

**2. [Critical] Profile likelihood for `mu_SV` is not a valid profile likelihood**

A proper profile likelihood over `mu_SV` requires fixing `mu_SV` to a sequence of values and maximizing over all other free parameters at each fixed value. In the code (lines 555-619), the starting-point guesses are grouped by `rho` (not `mu_SV`), and the `rw.sd` argument in `mif2` does not include `mu_SV` — meaning `mu_SV` is not perturbed during optimization and remains at whatever value it had in the initial guess. This is not a profile over `mu_SV`; it is at best a scatter plot of loglik vs. the `mu_SV` values inherited from the global search. The resulting "90% confidence interval of 0.08 to 0.12" is therefore not statistically valid.

**3. [Major] Flu model silently drops the R-to-S reinfection loop**

The flu `seirv_step` Csnippet (lines 357-370) contains no `dN_RS` transition. The flu model is therefore an SEIV model, not SEIRV. Yet the text and equations throughout Section 3 and Section 6 consistently describe an SEIRV model with a loop from R back to S. `mu_RS` appears in the `paramnames`, `partrans`, and `rw.sd` calls, and is reported in results tables — but it has no effect on the dynamics. This inconsistency between the described model and the implemented model is a major flaw.

**4. [Major] No no-vaccination baseline model for comparison**

The central scientific claim is that vaccination plays a meaningful role and that the SEIRV extension over a plain SEIR is justified. However, no SEIR baseline (without the V compartment) is fitted or compared to the SEIRV model. Without a likelihood-ratio test or AIC comparison against a restricted model that fixes `mu_SV = 0`, there is no statistical evidence that the V compartment improves fit. The profile over `mu_SV` does not fill this gap because the profile itself is incorrectly constructed (see issue 2).

**5. [Major] Flu population size N = 1,000,000 is unjustified and arbitrary**

The flu model uses N = 1,000,000 as a fixed parameter without any justification tying it to an actual surveilled population. The CDC FluView data reports laboratory-confirmed cases nationally; the total U.S. population is approximately 330 million. Using N = 1,000,000 means the model is implicitly treating only a small fraction of the population as relevant, which has substantial consequences for the interpretation of `Beta`, the herd immunity threshold, and the vaccination rate `mu_SV`. No sensitivity analysis is performed.

**6. [Major] Local search `rw.sd` values are used for starting the local search at a hand-tuned simulation point, not data-driven**

The local search for the flu model uses `rw.sd` values of 0.005 for all parameters (lines 436). These extremely small perturbations mean the local search barely moves away from the hand-tuned initial simulation point. The authors acknowledge this was intentional ("we intentionally make values in rw.sd much smaller because we found the results are more sensitive"), but this is not a principled justification — it indicates the optimization landscape may be poorly behaved and the reported convergence may be spurious. No attempt is made to diagnose convergence through paired particle filters or replicated runs.

**7. [Major] Local search uses `Np = 1000` for likelihood evaluation but `Np = 5000` during mif2**

In the local search likelihood evaluation block (lines 463), `pfilter(mf, Np=1000)` is used, while `mif2` itself was run with `Np=5000`. Using fewer particles at the evaluation stage introduces Monte Carlo variability that undermines the reliability of the reported log-likelihood estimates (-316.098 with se 0.053). The global search and profile use `Np=5000` consistently, which is inconsistent.

**8. [Major] The COVID-19 analysis is presented as a "failure" but no serious diagnostics are provided**

The authors conclude the SEIRV model fails on COVID data, but the evidence is limited to visual inspection of non-converging trace plots. There is no quantitative measure of the maximum log-likelihood achieved, no simulation from the best-found parameters to compare against data, and no discussion of what log-likelihood would be expected under a null model. The "failure" conclusion is presented qualitatively without rigorous support.

**9. [Minor] Hard-coded local file paths in the COVID EDA code chunk**

Lines 118-119 use `read.csv("/Users/ganjingrui/Desktop/cases_malaysia.csv")` and line 148 reads from `/Users/ganjingrui/Desktop/FluData.csv`. These are absolute paths to a specific user's local machine. The code is not reproducible for anyone other than the original author. The same CSV files are present in the project directory (`cases_malaysia.csv`, `FluData.csv`) and should be referenced with relative paths.

**10. [Minor] The flu data is loaded from a GitHub URL (personal repo) rather than the local file or a stable official source**

Line 380 loads flu data from `https://github.com/flippy1313/data531/raw/main/fludata_new.csv`, a personal GitHub repository. This URL could become unavailable, and the provenance of this derived dataset is not documented. The `FluData.csv` file already exists in the project directory and should be used instead.

**11. [Minor] Only one parameter (`mu_SV`) is profiled; the profile is insufficiently justified as to choice**

Having identified six free parameters (Beta, mu_EI, mu_IR, mu_RS, mu_SV, rho), only `mu_SV` is profiled, and the selection rationale is motivated purely by scientific interest in vaccination. No uncertainty quantification is provided for the other parameters. A paired profile over `Beta` or `rho` would be more informative about model identifiability, especially given that the global search pair plot suggests `rho` is weakly identified.

**12. [Minor] Confidence interval uses 90% nominal level without justification**

The profile CI is constructed at the 90% level (line 614: `qchisq(df=1, p=0.90)`), while the more standard convention in POMP epidemiological modeling is 95%. No reason is given for the non-standard choice.

**13. [Minor] The mathematical model and diagram both include the R-to-S transition, but this appears only in the COVID (buggy) code, not the flu code**

The compartmental diagram (Figure 1) and differential equations in Section 3 include the R-to-S arrow and Equation (4) governing `dR/dt` with the `mu_RS * R` term. This description is claimed to apply to both datasets, but the flu model implementation omits this transition entirely. The mathematical exposition is therefore inconsistent with at least one of the two implementations.

**14. [Minor] No model diagnostics (e.g., effective sample size, filter failure) are reported for the particle filter**

Throughout the fitting, neither the effective sample size (ESS) from `pfilter` nor any filter failure counts are reported. For the flu model with a relatively small dataset (35 weeks), particle degeneracy could be a concern, especially with the large dispersion parameter k = 10, which should be verified.

**15. [Minor] The `rho` parameter upper bound equals 1.0 in the global search design but the logit transform is used**

The global search design (line 486) sets `upper=c(..., rho=1, ...)`. When `rho = 1`, the logit transform produces `+Inf`, which can cause numerical instability. The upper bound should be set strictly below 1 (e.g., 0.999) when using `logit` transformation.

---

### Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project10/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project10/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project10/cases_malaysia.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project10/FluData.csv`
