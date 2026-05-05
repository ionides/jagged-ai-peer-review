# Final AI Review: Unveiling the Dynamics of Influenza in the Great Lakes Region (w25 Project 01)

---

## Overall Assessment

This paper tackles a genuinely ambitious problem: fitting a mechanistic influenza model to 9 years of weekly ILI data for HHS Region 5, spanning the COVID-19 pandemic disruption. The progressive model development — from basic SEIRS to a model with seasonal forcing, antigenic drift, vaccine covariates, and COVID suppression — is well-motivated and scientifically coherent. The explicit quantitative comparison to a SARMA benchmark is appropriate and correctly executed (both models fitted on raw counts, log-likelihoods directly comparable). The authors engage honestly with model failures, correctly diagnosing the gamma identifiability problem and attempting profile likelihood for rho. These are genuine strengths. However, the paper has critical technical issues that undermine the reported likelihoods: the H accumulator is likely zeroed by the Csnippet before the measurement model evaluates, the profile likelihood for rho is truncated at its lower bound making the reported CI invalid, and the model's key biological parameter gamma remains implausibly large at the final MLE. Addressing these issues is essential before the results can be interpreted reliably.

---

## Key Strengths

**S1 — Correct benchmark comparison setup.**
The authors explicitly avoid log-transforming the data for SARMA fitting so that log-likelihoods are on the same scale as the POMP model. The resulting comparison (SARMA: -3620.72, POMP best: approximately -3600) is valid and shows the mechanistic model is competitive with the non-mechanistic benchmark.

**S2 — Progressive and transparent model development.**
The paper honestly reports the failures of the basic SEIRS (mu_IR = 23.9, log-likelihood much lower than SARMA) before introducing the more complex model. This transparency is commendable and scientifically valuable.

**S3 — Biologically grounded parameter initialization.**
Parameter ranges for mu_EI, mu_IR, rho, and beta are derived from CDC sources and published influenza literature with specific citations and arithmetic justification.

**S4 — Correct distinction between likelihood slice and true profile.**
The paper correctly identifies that the "poor man's profile" is a slice and that a true profile requires re-optimization. A true profile with 30 rho values, 5 MIF runs each, and 20 replicated pfilter evaluations with Np = 5000 is then constructed.

---

## Major Points

**C1 — H accumulator likely zeroed before dmeas evaluation.**
ID: 25.01.1 | Severity: Major

The Csnippet for the complete SEIRS model contains `if (fabs(fmod(t, 1.0)) < 1e-8) { H = 0; }`, which fires at every integer time t during rprocess. Since observations occur at integer times and rprocess runs before dmeas, H is manually zeroed before the measurement model evaluates it. The `accumvars = "H"` declaration in pomp zeros H after each observation — but this is too late, as the manual reset already fires during that same time step's rprocess call. This means `dmeas` evaluates `rho * H` with H = 0, producing a near-zero expected count regardless of model state. The reported log-likelihoods, parameter estimates, and posterior predictive checks may all be computed under a broken measurement model.

Suggested author action: Remove the manual H-reset inside the Csnippet (`if (fabs(fmod(t, 1.0)) < 1e-8) { H = 0; }`) and rely solely on pomp's `accumvars` mechanism. Re-run all local and global searches and check whether log-likelihoods and posterior predictive simulations change substantially.

---

**C2 — Profile likelihood for rho is truncated at its lower boundary.**
ID: 25.01.2 | Severity: Major

The rho profile (Figure 34) shows a monotonically decreasing likelihood curve across the grid range 0.02 to 0.04, with the peak at rho = 0.02 — the left boundary. The reported CI = (0.02, 0.057) therefore has its lower bound defined by the grid edge, not by the chi-squared cutoff. The true maximum may lie below 0.02, consistent with the global search finding rho = 0.004. A valid profile must span the range where the log-likelihood drops at least 5 units below the maximum on both sides; a single-sided profile cannot produce a valid two-sided CI.

Suggested author action: Extend the rho grid from at least 0.001 to 0.10 and re-run the profile. If the maximum is near rho = 0.004 (consistent with the global search), the CI will shift substantially. The profile grid should always be checked to ensure the maximum is an interior point before extracting a CI.

---

**C4 — gamma is biologically implausible and the model is identifiability-entangled.**
ID: C4 | Severity: Major

The final MLE yields gamma = 6.95 (preferred model, Section 5.5), implying immunity duration of approximately 19 days under moderate antigenic drift d = 0.5. The profile over gamma (Figure 30) shows essentially flat log-likelihood for gamma > 5, meaning the data cannot identify gamma above a threshold. The model exploits the product mu_RS * gamma to fit seasonal patterns, creating identifiability entanglement — the data cannot separately identify the base waning rate and the drift amplification. The authors correctly diagnose this but leave gamma at its MLE without imposing biologically motivated constraints.

Suggested author action: Impose an upper bound on gamma such that the effective immunity duration mu_RS(t)^{-1} does not fall below a biologically plausible minimum (e.g., 4 weeks) for expected antigenic distances. Profile gamma within this constrained range. If the data cannot identify gamma even within constraints, fix it at a biologically reasonable value and report this as a limitation.

---

## Minor Points

**C3 — "Poor man's profile" CI from a likelihood slice is invalid.**
ID: 25.01.3 | Severity: Minor

Figure 31 shows a dashed line at loglik_max - 1.92 and implies a CI from the slice. A likelihood slice does not re-optimize over nuisance parameters and therefore does not produce a valid confidence interval. The authors correctly distinguish slice from profile in prose but draw the chi-squared cutoff on the slice figure, which could mislead readers.

Suggested author action: Remove the dashed CI line from Figure 31 and label it explicitly as a "likelihood slice, not a profile."

---

**C5 — k (overdispersion) fixed at 10 without profiling.**
ID: C5 | Severity: Minor

k controls the width of the negative binomial measurement distribution and is confounded with rho. k is included in paramnames with a log transform, so it is estimable, but no random-walk standard deviation is assigned to it in any mif2 call. The reported CI for rho is conditional on k = 10; the true joint uncertainty in (rho, k) is larger than reported.

Suggested author action: Include k in at least one global search with a small random-walk standard deviation. Report whether estimates of rho and other parameters change materially when k is freed.

---

**C6 — Log-likelihood standard errors vary substantially across searches; evaluation protocol not documented.**
ID: C6 | Severity: Minor

The best log-likelihood from global search 1 has loglik.se = 0.322, while the profile likelihood uses 20 pfilter replicates with Np = 5000. The global search log-likelihoods used for the SARMA comparison should be computed with consistent and adequate replication. The paper does not state how many pfilter replicates were used for each reported final log-likelihood in the global searches.

Suggested author action: Add a methods paragraph specifying the number of pfilter replicates and Np used for each final log-likelihood evaluation. Standardize to at least 10 replicates with Np >= 2000 for the comparison against the SARMA benchmark.

---

**X2 — "Posterior predictive check" terminology is incorrect.**
ID: X2 | Severity: Minor

Sections 5.6.2 and 5.7.2 describe "posterior predictive checks" but the simulations are unconditional forward simulations from the MLE, not conditioned on observations through a filtering distribution. These are properly called "unconditional forward simulations at MLE" or "prior predictive simulations." Posterior predictive checks would require simulating from the filtering (smoothing) distribution conditioned on all observations.

Suggested author action: Relabel as "forward simulations at MLE" or "unconditional predictive simulations."

---

**X3 — Number of mif2 starting points for main model global searches not reported.**
ID: X3 | Severity: Minor

The number of starting points (nseq) for the complete SEIRS global searches is not stated in the main text (only "nseq = 200" appears for the basic SEIRS in Section 4.5). Reproducibility requires knowing how many starting points were used.

Suggested author action: Report nseq for each global search in a summary table or methods paragraph.
