# Peer Review: W22 Project 15
## "Rise and Fall of Delta and Omicron variants: Comparison of Compartmental Models for SARS-CoV-2 variants"

---

## Summary

This project fits separate SEIR models to weekly sequenced COVID-19 case counts for the Delta and Omicron variants in the United States. The authors perform local and global iterated filtering searches and profile likelihood analysis for the transmission rate Beta, then compare estimated parameters across variants. The ambition of the comparison is reasonable, but the execution has several significant methodological and reporting weaknesses described below.

---

## Weaknesses (most critical first)

### 1. [MAJOR] Reporting rate fixed without justification for Omicron, and inconsistency with the data

The reporting rate `rho` is fixed at 0.1 for both variants on the grounds that "roughly 10% of all cases are sequenced." However, GISAID sequencing coverage varied substantially over time and differed between the Delta and Omicron waves. No citation supports the specific 0.1 value for either wave, and the sequencing fraction for Omicron was known to be falling rapidly by late 2021. Fixing `rho` at the same value for both variants removes a potentially important source of variation and may confound the Beta comparison, which is the central result of the paper. The parameter should either be estimated or justified with wave-specific sequencing statistics.

### 2. [MAJOR] Global search Np is only 2000 particles, severely limiting likelihood accuracy

At `run_level = 3`, `Np = 2000` particles is used throughout the global search, the profile likelihood, and the final evaluation. For the Delta dataset with 64 observations and counts reaching ~78,000 at peak, and for the Omicron dataset with similarly large counts, 2000 particles produces noisy particle filter estimates. This is evidenced by the large standard errors in the `covid19_params.csv` file (e.g., loglik.se up to 85 for some rows). The global search uses the same `Np = Np` (2000) for the evaluation `pfilter` calls, which means the reported maximum log-likelihoods are themselves uncertain. The profile likelihood is also evaluated with only 2500 particles for Omicron (`pfilter(Np=2500)` in the beta_profileomics chunk, which is inconsistent with the stated `Np = 2000` and even lower in the code). The standard practice is to evaluate final likelihoods with 20,000 or more particles.

### 3. [MAJOR] Profile likelihood for Delta does not cover the MLE, and no explanation is given

The authors acknowledge (section "Profile likelihood Comparison for Beta") that the Delta profile's 95% CI "does not cover our maximum likelihood estimate in global search." The MLE from the global search is approximately Beta = 73 (top row of `covid19_params.csv`), while the profile suggests the CI is roughly 100-150. This is a fundamental inconsistency that indicates either (a) the global search did not converge to the true MLE, or (b) the profile likelihood was computed from too small a search box or with insufficient optimization. The authors attribute this vaguely to "high correlation between model parameters" but do not investigate further. This inconsistency should disqualify the Delta Beta estimate from being used in the comparison without further analysis.

### 4. [MAJOR] Omicron data preprocessing introduces a problem: Omicron observations exist before week 40 but are filtered out

The Omicron model is fit only to data with `week > 40` (i.e., weeks 41-65 after re-indexing to weeks 1-25). However, the raw data in `delta_omicron.csv` shows that sporadic Omicron observations exist as early as week 1. Dropping weeks 1-40 and renumbering weeks 41-65 as weeks 1-25 is not explained or justified in the text. Moreover, the renaming means the "year" column is used for plotting Delta but the re-indexed "week" column is used for Omicron models, making the time axes non-comparable across the two variant analyses.

### 5. [MAJOR] The initial condition sets I = 1 (one infected person) for both variants regardless of scale

The `sir_rinit` code always initializes `I = 1`. For a population of N = 300,000,000 with peak weekly sequenced counts of ~90,000 for Omicron, starting from a single infected individual is biologically implausible and may require many irrelevant early-time periods before the epidemic begins. The code also sets `E = 0`, which is inconsistent with a mid-epidemic start. For Omicron in particular, filtering to post-week-40 data means the epidemic is already well underway at the initial time, so the initial condition is especially poorly matched to the data.

### 6. [MAJOR] mu_IR for Delta is implausibly high and not discussed

The top global search result for Delta gives `mu_IR = 5.46` (from `covid19_params.csv`, row 1), corresponding to a mean infectious period of 1/5.46 ≈ 0.18 weeks, or roughly 1.3 days. This is biologically implausible for COVID-19, where the infectious period is typically 5-10 days. The authors do not report or discuss this value in the text, except to note that mu_IR is "larger for Delta than Omicron," which is true but the absolute values are never scrutinized. The Omicron top result has `mu_IR ≈ 0.57`, corresponding to ~1.75 weeks, which is more reasonable but still on the high side. The extreme Delta mu_IR suggests model misspecification or poor identifiability.

### 7. [MAJOR] The global search box for Omicron is identical to Delta (Beta upper = 100) despite Omicron having much larger Beta

The global search for Omicron uses `upper=c(Beta=100, ...)`, the same upper bound as for Delta. However, the Omicron MLE found is Beta ≈ 389 (from `covid19_paramsomics.csv`, row 1), which is far outside the search box. The optimizer apparently extrapolates far beyond the stated bounds via the iterated filtering steps. This means the Omicron global search starting points are systematically biased away from the true optimum, and there is no guarantee that the search explored the relevant parameter space. The fact that the best Omicron result came from a random start at Beta ≤ 100 that then drifted to ~389 during mif2 iterations is a sign that the box is poorly calibrated.

### 8. [MAJOR] Profile likelihood for Beta is not plotted together in a way that supports the stated confidence intervals

The profile likelihood plot uses `facet_wrap(~variant, scales="free")` with free y-axes and free x-axes, making it impossible to directly compare the absolute log-likelihoods or the CI thresholds across variants. The authors state confidence intervals of "roughly 100 to 150" for Delta and "320 to 440" for Omicron, but these intervals are read off separately from the faceted plots. The appropriate presentation would overlay the two profiles on the same scale (after centering by their respective maxima) so the reader can verify the stated intervals. The code also applies different filtering (`filter(loglik>maxloglik-40)` for Delta but no such filter for Omicron before grouping), introducing asymmetry in what data enter each panel.

### 9. [MINOR] rho is fixed but also included in `partrans` with logit transformation

The parameter `rho` is fixed at 0.1 throughout (`fixed_params <- c(N=300000000, k=10, rho=0.1)`), yet it appears in `parameter_trans(logit=c("eta","rho"))`. Applying a logit transformation to a parameter that is never estimated introduces unnecessary code complexity. More importantly, in the local search `rw.sd(Beta=sds, mu_IR=sds, mu_EI=sds, eta=ivp(sds))`, rho is not listed—which is correct, since it is fixed—but this inconsistency between the declared transformation and the actual optimization is confusing and error-prone.

### 10. [MINOR] The accumulator variable H accumulates dN_IR (recoveries) rather than incidence

The process model accumulates `H += dN_IR`, counting recoveries as the quantity linked to the observation. For sequenced case data, one would expect to link to new infections (dN_EI or dN_SE), not recoveries. Using dN_IR introduces a time lag between infection and reporting of approximately 1/mu_EI + 1/mu_IR weeks. With the estimated parameters (especially the large mu_IR for Delta), this lag is very short, which may partly explain why the model still fits, but the structural choice is not biologically motivated or discussed.

### 11. [MINOR] Convergence assessment is qualitative and superficial

The convergence diagnostics for both variants (local search trace plots) are described in vague terms ("the likelihood seems to increase in general," "some of the runs seems to get stuck"). There is no quantitative convergence check, no comparison of the maximum log-likelihood across chains, and no mention of whether the traces had stabilized by iteration 100. For the Delta local search, the text notes potential non-convergence of Beta, mu_IR, and eta but simply defers to the global search without verifying that the global search resolves it.

### 12. [MINOR] The simulation plots use `guides(color=FALSE)`, which is deprecated and produces a warning in recent ggplot2 versions

The code uses `guides(color=FALSE)` (a deprecated argument) and `c='black'` (an unrecognized argument that silently fails, so the observed data line does not render in black as intended). This likely causes the observed data to be plotted with a default aesthetic rather than the intended black line, making it hard to distinguish observed from simulated in the output. The correct form is `guides(color="none")` and `color='black'`.

### 13. [MINOR] The model does not account for vaccination or waning immunity

The SEIR model assumes a fully susceptible population (minus an initial R compartment set by eta) and permanent immunity upon recovery. This is a strong assumption for the Delta wave, which occurred after widespread vaccination in the US. The authors acknowledge this limitation in the conclusion but do not attempt to quantify how it might bias the parameter estimates. A simple extension (e.g., SVEIR or adjusting the effective susceptible fraction) could have at least bounded the bias.

### 14. [MINOR] The total population N = 300,000,000 is questionable for GISAID sequencing data

The model uses the entire US population (N = 300,000,000) as the susceptible pool. The observations, however, are counts of sequenced viral genomes, not total COVID-19 cases. Sequencing is a highly filtered subsample with substantial laboratory and geographic heterogeneity. Using total US population as N implies that essentially every American is one step from being sequenced, which is not a sensible epidemiological interpretation. The reporting rate rho = 0.1 is meant to bridge this gap, but with N = 300 million and rho = 0.1, the model effectively assumes 30 million cases are missed per week at the Omicron peak—far more than the actual case burden. The model scale is not internally consistent.

### 15. [MINOR] The number of global search starting points (Nglobal = 100) is adequate but only one round of mif2 is used per starting point

In the global search, each starting point is optimized with `mif2() %>% mif2()`—only two mif2 calls with `Np = 2000` particles and a default (not specified) `Nmif`. The second `mif2()` call does not specify Nmif, defaulting to the object's stored value from the first call. However, the first call also uses only `Np = Np` (2000) without specifying Nmif, so it inherits the Nmif from the local search mif2 object (`mf1`). With Nmif = 100 iterations but only 2000 particles, convergence from a random start in a poorly-specified box (see weakness 7) is not guaranteed within this budget, particularly for Omicron where the MLE is at Beta ≈ 389, far from the search starting points.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/delta_omicron.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/covid19_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/covid19_paramsomics.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/final.bib`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project15/Makefile`
