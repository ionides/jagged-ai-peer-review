# Review: W24 Project 10
### *POMP Analysis on Covid-19 Cases in Malaysia and Influenza in the U.S.*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) via the pomp R package |
| **R packages used** | pomp, tidyverse, foreach, doParallel, doFuture, doRNG, ggplot2, DiagrammeR |
| **Code publicly available** | Partial — Rmd in project repository; flu data loaded from a GitHub URL; COVID data loaded from an external URL at runtime and also from a hard-coded local path |
| **Data publicly available** | Partial — flu data via GitHub; COVID data via MoH-Malaysia GitHub; EDA section reads from a local filesystem path that will fail for others |
| **Benchmark comparison included** | No |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2 used with replicated pfilter re-evaluation (correct pattern); COVID analysis truncated before full inference |
| 2 | Benchmark comparison | ✗ | No non-mechanistic benchmark (ARMA, ARNB, or IID) included for either dataset |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihood reported for flu model (−306.8); no baseline for comparison; COVID analysis yields no usable likelihood |
| 4 | Model diagnostics | ✗ | Trace plots shown but no forward simulation from MLE, no ESS monitoring, no conditional log-likelihood plots |
| 5 | Parameter identifiability and uncertainty | ~ | One profile attempted for mu_SV but it is not correctly constructed; no profiles for key epidemiological parameters |
| 6 | Computational adequacy | ~ | Np=5000, Nmif=100 with 20 starts for flu (reasonable); COVID search shows non-convergence; cooling.fraction.50 very aggressive |
| 7 | Forecast methodology | N/A | No forecasting performed |
| 8 | Model variations and nested comparisons | ✗ | No alternative model structures tested; COVID failure not remediated |
| 9 | Stochasticity | ~ | Binomial transitions used (appropriate); no overdispersion in process noise; negative binomial measurement model present |
| 10 | Reproducibility and extendability | ✗ | Hard-coded local paths; no session info; no archived MLE parameters; EDA code non-reproducible |
| 11 | Corroboration with scientific knowledge | ~ | Initial conditions described; fitted parameters not compared to biological priors |
| 12 | Measurement model specification | ~ | Negative binomial measurement model with rho and k; k fixed rather than estimated |
| 13 | Initial conditions | ~ | Initial compartment counts stated and partially justified; not estimated as parameters |

---

## Summary

The paper applies an SEIRV compartmental model to two infectious disease datasets: COVID-19 weekly cases in Malaysia (2021–2022) and U.S. influenza A cases from the 2017–2018 season. Both analyses use the pomp framework with iterated filtering (mif2), followed by a global search and a profile likelihood for the flu data. The paper's stated goal is to compare POMP-based inference across two epidemic contexts and assess the role of vaccination. While the use of likelihood-based inference with replicated pfilter re-evaluation follows course standards, the analysis is severely compromised by two critical bugs in the model code that cause the implemented model to differ substantially from the model described in the text. The COVID-19 analysis is abandoned after a failed local search, and the profile likelihood for the flu vaccination parameter is not correctly constructed. No benchmark comparison is included for either dataset.

**Strengths:**
- Replicated pfilter calls with logmeanexp are used correctly to evaluate log-likelihoods after mif2 optimization.
- A global search from 100 random starting points is run for the flu model.
- The negative binomial measurement model with a reporting rate is reasonable.
- The paper honestly acknowledges that the COVID model fails and attempts a qualitative explanation.

**Weaknesses:**
- The COVID rprocess draws the R→S transition from the infectious compartment I rather than the recovered compartment R — a critical implementation error.
- The flu rprocess omits the R→S loop entirely despite describing it as a core feature of the SEIRV model.
- The "profile likelihood" for mu_SV is not a genuine profile: starting guesses are grouped by rho (not mu_SV), and mu_SV is not held fixed on a grid during optimization.
- No non-mechanistic benchmark is included for either dataset.
- The COVID analysis is abandoned without model revision after convergence failure.

---

## Major Issues

### 1. Critical bug: R→S transition in COVID rprocess draws from I instead of R

In the COVID SEIRV step function (`blinded.Rmd`, line 222), the transition from recovered to susceptible is coded as:

```c
double dN_RS = rbinom(I, 1-exp(-mu_RS*dt));
R -= dN_RS;
S += dN_RS;
```

The draw uses the infectious compartment `I` as its population size rather than the recovered compartment `R`. This means (a) the number of individuals transitioning R→S is sampled from the wrong pool; (b) the R compartment dynamics are corrupted; and (c) both `dN_IR` and `dN_RS` are drawn independently from `I`, so their sum can exceed `I`, potentially driving `I` negative. The biological interpretation — that recovered individuals may return to susceptibility — is therefore not implemented. The COVID model is not an SEIRV model with reinfection; it is a misspecified process whose dynamics bear no clear relationship to the stated equations (1)–(5). All COVID results and the qualitative conclusions about COVID model failure are unreliable.

**Fix:** Replace `rbinom(I, ...)` with `rbinom(R, 1-exp(-mu_RS*dt))` on that line.

---

### 2. Flu rprocess silently omits the R→S transition

The flu SEIRV step function (`blinded.Rmd`, lines 357–370) does not include any `dN_RS` calculation. The recovered compartment R only increases (`R += dN_IR;`) and never decreases; S never gains from R. The mu_RS parameter is included in `paramnames` and estimated during mif2, but has no effect on any state variable. The "SEIRV model with loop capability" described in the text and in the conclusion is not what is fitted to the flu data: the flu model is effectively SEIV with an absorbing R state.

This means the conclusion "we believe our SEIRV with loop capability can fit the pandemic data well" (Section 7) is based on a model that does not implement the loop. The claim that the vaccine compartment and the reinfection loop together explain flu dynamics is unsupported.

**Fix:** Add `dN_RS` to the flu step function analogously to the intended COVID version (using `rbinom(R, ...)`) and update R and S accordingly. Re-run all downstream analyses.

---

### 3. Profile likelihood for mu_SV is not correctly constructed

The "profile" for the vaccination rate mu_SV (`blinded.Rmd`, lines 555–621) is not a valid profile likelihood. Two problems:

(a) **Starting guesses are grouped by rho, not mu_SV.** The code reads `group_by(cut=round(rho,2))` at line 558, selecting top-5 results per rho value. This does not provide a systematic grid over mu_SV values; it provides a grid over rho values.

(b) **mu_SV is not held fixed on a grid.** A correct profile requires fixing mu_SV at a series of target values and maximizing over all other parameters at each fixed value. In the code, mu_SV is absent from `rw.sd` (line 577), which means it stays at its starting value during mif2. But because starting guesses are selected by rho rather than by mu_SV, the starting values of mu_SV are essentially arbitrary draws from the global search, not a controlled grid. The resulting plot of mu_SV vs. log-likelihood is neither a profile nor a slice; it is a scatter of optimization runs with uncontrolled mu_SV starting values.

This matches Error 1.2 in the weakness reference (likelihood slice vs. profile, CC-Yes, Major). The reported 90% CI for mu_SV (0.08–0.12) cannot be trusted.

**Fix:** Create a grid of mu_SV values (e.g., 20–30 values spanning the plausible range). At each grid point, fix mu_SV and run mif2 with all other parameters free. Extract the profile envelope and apply the Wilks threshold.

---

### 4. No benchmark comparison

Neither the COVID nor the flu analysis includes any comparison of the SEIRV model against a non-mechanistic statistical benchmark. The best log-likelihood for the flu model is reported as −306.8, but this number is uninterpretable in isolation: without a benchmark (e.g., an ARMA model or even an IID negative binomial model fit to the same data), it is impossible to assess whether the mechanistic model captures meaningful structure or whether a simpler statistical model achieves comparable fit.

This is Error 1.6 in the weakness reference (CC-Yes, Major). Wheeler et al. (2024) demonstrated that even visually reasonable mechanistic models can fail to beat a simple auto-regressive negative binomial; discovering this provides information about what the mechanistic model is or is not capturing.

**Fix:** Fit an ARMA or auto-regressive negative binomial model to the flu data and report its log-likelihood. Compare to the SEIRV log-likelihood of −306.8 for an objective assessment of model value.

---

### 5. COVID local search uses parameter values as random walk standard deviations

The COVID local search specifies (`blinded.Rmd`, line 313):

```r
rw.sd=rw_sd(Beta=2, mu_EI=0.25, mu_IR=0.088, rho=0.8, mu_RS=0.22, mu_SV=0.2)
```

These values closely match the initial parameter values used for simulation (`Beta=2, mu_IR=0.088, mu_EI=0.25, mu_RS=0.22, rho=0.8, mu_SV=0.2` from line 274). The standard course perturbation size on the log/logit scale is rw.sd=0.02. On the log scale, rw.sd=2 for Beta means perturbing log(Beta) by ±2 standard deviations, which multiplies or divides Beta by a factor of ~7.4 per iteration. This is approximately 100 times larger than the course standard. Perturbations this large cause mif2 to explore the parameter space at random rather than perform directed optimization, contributing directly to the non-convergence described in Section 5.

**Fix:** Reduce rw.sd values to approximately 0.02 on the transformed scale for all parameters (log/logit). The starting values and perturbation sizes should not be the same numbers.

---

### 6. COVID analysis abandoned without model revision

After observing that the COVID local search fails to converge (Section 5), the paper provides qualitative explanations for the failure (multiple peaks, rapid mutation, non-uniform vaccination rates) but does not attempt any model revision. No global search, no profile likelihoods, and no alternative model structures are explored for the COVID data. The paper proceeds directly to the flu analysis, and the conclusion draws no quantitative inference from the COVID results.

The paper's stated aim includes "shed light on the crucial elements that define the success of public health interventions" for both datasets. Abandoning the COVID analysis after a single local search — one that used incorrect random walk standard deviations (see Issue 5) and a buggy rprocess (see Issue 1) — leaves this aim unmet. The failure may have been due to the coding errors rather than intrinsic model limitations.

**Fix:** After correcting Issues 1 and 5, re-run the COVID local search with appropriate rw.sd values. If non-convergence persists, attempt a global search. If the model genuinely fails to fit COVID multi-wave data, document the log-likelihood gap to a benchmark and consider a time-varying transmission model as described in the paper's own conclusion.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots are shown for both the COVID and flu local searches. For COVID, the authors correctly identify non-convergence. For flu, the trace plots show generally upward-trending log-likelihood, though the cooling.fraction.50=0.1 used for COVID (and 0.2 for flu global search) is considerably more aggressive than the course standard of 0.5. Aggressive cooling means the algorithm may not explore sufficiently before cooling down, limiting its ability to escape local optima. The flu local search shows trace plot convergence, but the rw.sd values of 0.005 (local) and 0.002 (global) on the log scale are smaller than the standard 0.02, which may limit exploration.

**Particle filter:** ESS is not monitored or reported at any point in the analysis. The particle counts used (Np=5000 for flu, Np=5000 for COVID) are reasonable, but without ESS monitoring it is impossible to detect filter degeneracy.

**Conditional log-likelihoods:** Not computed or plotted. Per-time-step log-likelihoods are not shown for either dataset.

**Profile likelihoods:** Only one profile is attempted, for mu_SV, and it is not correctly constructed (see Major Issue 3). No profiles are computed for the key epidemiological parameters Beta, mu_EI, or mu_IR.

**Computational scale:** CPU hours are not reported. The analysis uses 36 parallel workers, with Np=5000 and 100 mif2 iterations across 20 local search runs and 100 global search runs — a moderate computational effort consistent with run_level=3. The bake() pattern is used to cache results, which is appropriate.

---

## Reproducibility Assessment

**Code availability:** Code is present in the Rmd file. Two data-loading steps in the EDA section use hard-coded local paths (`/Users/ganjingrui/Desktop/cases_malaysia.csv` at line 119, `/Users/ganjingrui/Desktop/FluData.csv` at line 148) that will fail for any other user. The POMP sections load data from GitHub URLs, which is reproducible but fragile to future URL changes.

**Final parameters:** MLE parameter vectors from the global search are written to `final_params_2.csv`, which is a reasonable practice. However, this file is generated at runtime and not archived in the repository, so readers cannot evaluate results without re-running the full optimization.

**Model-code consistency:** The text states both COVID and flu models implement an SEIRV with an R→S reinfection loop (Section 3). The COVID code implements a buggy version of this; the flu code omits it entirely. The implemented models do not match the stated model.

**Package versions:** No `sessionInfo()` output and no renv or packrat lockfile is provided. pomp version is not pinned.

**Auxiliary data:** Data is loaded from external URLs; the cases_malaysia.csv and FluData.csv files are included in the project directory alongside the Rmd but the EDA code does not use the local copies via a relative path.

---

## Minor Issues

- The flu data EDA section (`blinded.Rmd`, line 148) loads FluData.csv from `/Users/ganjingrui/Desktop/FluData.csv`, while the POMP section (line 380) loads from a GitHub URL. The data source inconsistency means EDA figures and POMP figures may use slightly different data representations.

- The global search rw.sd values for all flu parameters (0.002, line 507) are approximately 10 times smaller than the course standard of 0.02 on the log/logit scale. This may cause the global search to over-rely on starting values rather than performing effective local refinement at each starting point.

- The mu_RS parameter is estimated in the flu global search (`paramnames` includes mu_RS; rw.sd=0.002 for mu_RS in the global search) but has no effect on the flu model dynamics because the flu rprocess does not implement the R→S transition (see Major Issue 2). Estimating an inactive parameter consumes degrees of freedom and adds numerical noise without benefit.

- The profile likelihood uses a 90% confidence interval threshold (`qchisq(df=1, p=0.90)`, line 614) without justification for the non-standard level. The course standard and most epidemiological literature use 95%.

- Duplicate reference: References 4 and 6 are identical (`https://www.cdc.gov/coronavirus/2019-ncov/your-health/reinfection.html`).

- The N=1,000,000 fixed population size for the flu model (line 393) is not justified. This does not represent the U.S. population (~330 million) or any clearly defined surveillance catchment area. The implied reporting rate rho is therefore difficult to interpret epidemiologically.

- No simulation-based diagnostic of the flu model is presented using the fitted MLE parameters. The simulation plot in Section 6 uses a manually chosen parameter set (`Beta=10, mu_IR=0.1, ...`), not the MLE. A model diagnostic showing the fitted model's simulated trajectories versus observed flu data would strengthen the goodness-of-fit argument.

- The section title "Why SEIRV Model Failed for Covid-19 data?" (Section 5) proposes three structural explanations for failure, but given that the model code contains a critical bug (Issue 1) and the random walk standard deviations are set incorrectly (Issue 5), the failure is at least partly an implementation artifact rather than a fundamental SEIRV limitation.

- Minor typographical errors: "Methodlogy" (Section 3 heading), "Intepretation" (Section 5 and 6 subheadings), "serach" (Section 6).

---

## Recommendation

**Major Revision.** The paper contains two critical code errors — the COVID rprocess draws the R→S transition from the wrong compartment, and the flu rprocess omits the R→S transition entirely — that mean the models analyzed are not the models described in the text. The "profile likelihood" for the vaccination rate is not validly constructed, and no benchmark comparison is included for either dataset. These issues must be corrected before the analysis can support any of the paper's scientific conclusions. After correction, the COVID analysis should be re-run with appropriate random walk standard deviations, and a non-mechanistic benchmark should be added for the flu model to provide context for the reported log-likelihood.

---

## Files Consulted

### Skill files

- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

### Project files

- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project10/blinded.Rmd`
