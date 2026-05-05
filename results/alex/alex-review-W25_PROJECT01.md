# Peer Review: W25 Project 01
## "Unveiling the Dynamics of Influenza in the Great Lakes Region"

---

### Summary

This project analyzes CDC ILINet influenza data from HHS Region 5 (Great Lakes, 2015–2024) using both a regression model with SARMA errors and a SEIRS-based POMP model. The POMP model is progressively augmented with seasonal transmission, COVID-19 suppression, vaccine effects, and antigenic drift. The project demonstrates considerable effort and genuine engagement with the data and the biology. However, several serious methodological issues undermine the validity of the results and comparisons.

---

### Weaknesses (Prioritized from Most to Least Critical)

---

**1. [Major] Double-specification of H accumulation creates a conflicting reset mechanism**

The advanced SEIRS model specifies `accumvars = "H"` in the `pomp()` call, which instructs the POMP framework to automatically zero out `H` after each observation interval. Simultaneously, the C snippet contains a manual reset:

```c
if (fabs(fmod(t, 1.0)) < 1e-8) {
  H = 0;
} // resets H = 0
```

Because `t` is measured in integer weeks and `delta.t = 1/7`, this condition (`t mod 1 < 1e-8`) fires only when `t` is near an integer value — which corresponds to the start of each week. However, with `delta.t = 1/7`, the Euler steps do not land exactly on integers due to floating-point arithmetic, making the behavior of this reset non-deterministic across platforms and unpredictable in interaction with `accumvars`. This redundancy may cause `H` to be reset at incorrect times relative to what the measurement model assumes, corrupting the relationship between the latent incidence `H` and observed `reports`. This is a silent but potentially severe numerical error.

---

**2. [Major] Data for the basic SEIRS model section is re-loaded from a different file without filtering, breaking reproducibility**

In the basic SEIRS section (Section 4), the code reads:

```r
data = read.csv("ilitotal2015.csv")
```

without applying any year filtering (`filter(YEAR < 2024)`). But in the EDA and SARMA sections, data is filtered to `YEAR < 2024` via `data |> filter(YEAR < 2024) -> data`. The basic SEIRS model therefore uses a different (longer) dataset than is used in all subsequent sections, including the advanced SEIRS model. This makes the likelihood comparison between the basic SEIRS model and the benchmark SARMA model unreliable, since they are not evaluated on the same data.

---

**3. [Major] The `filter(YEAR < 2024)` is applied twice on the same data object in the advanced SEIRS section**

In the chunk beginning the advanced SEIRS section (around line 715), the code applies `data |> filter(YEAR < 2024) -> data` again, even though this filter was already applied in the EDA section (line 257). This is a code hygiene issue that, depending on the rendering environment and chunk execution order, could silently truncate the dataset unexpectedly or behave inconsistently. This should use data already filtered in the prior step, not re-filter it.

---

**4. [Major] Likelihood comparison between SARMA and POMP models is not fully valid**

The paper presents the SARMA model log-likelihood of -3620.72 and the best POMP model log-likelihood of approximately -3622 (from `bvgcseirs_global_search_frho.rds`) as being comparable and nearly equal, and concludes that the mechanistic model matches the benchmark. However:

- These likelihoods are computed on different model types (exact ARMA likelihood vs. particle filter estimate with Monte Carlo error). A direct numerical comparison without accounting for particle filter Monte Carlo variance is not rigorous.
- The standard error of the particle filter log-likelihood estimate is not reported alongside the final comparison, making it unclear how reliable the reported POMP log-likelihood is.
- No likelihood ratio test or formal statistical comparison is conducted.

---

**5. [Major] `gamma` is biologically implausible and the model explicitly acknowledges overfitting via this parameter**

The paper itself computes that at a moderate antigenic distance of `d = 0.5`, the estimated `gamma = 6.95` gives an immunity duration of only ~19 days — far shorter than the biological range of months. The paper attributes this to identifiability entanglement and the model compensating for underpowered seasonality. While the authors are to be commended for diagnosing this issue honestly, the final reported model still uses this biologically implausible parameter value without a satisfactory resolution. An alternative model formulation or constraint on `gamma` is warranted before the model can be considered interpretable.

---

**6. [Major] The profile likelihood for `rho` was computed over a very narrow grid (0.02–0.04 or 0.02–0.08) that may not cover the true MLE**

The poor man's profile shows a maximum at the lower bound of the evaluation range (`rho ~ 0.02`), and the true profile was evaluated over [0.02, 0.04]. These narrow, asymmetric grids do not allow the likelihood to be fully explored toward lower values. The comment in the text that the best estimate is near `rho ~ 0.0386` (upper end of the true profile range) suggests the maximum may have been found near the boundary, which could indicate the optimal `rho` is outside the evaluated range. A wider grid would be needed for a credible confidence interval.

---

**7. [Major] Several key MIF2 hyperparameters are either not reported in the main text or are reported only in supplementary code**

The global search settings (Nmif, Np, rw.sd values, cooling schedule) for the main SEIRS-BVGC model are not described in the main text. The reader cannot assess the adequacy of the search without this information. Nmif = 50 with Np = 2000 may be insufficient for a model with 12+ free parameters and 468 observations. No convergence diagnostics (e.g., ESS trace, likelihood standard error at final parameter values) are presented for the main global search.

---

**8. [Major] The `rw_sd_profile` code in the profile likelihood chunk contains a duplicate `gamma` entry**

In the true profile likelihood code (around line 1600–1611), the `rw_sd()` call lists `gamma = 0.01` twice:

```r
rw_sd_profile <- rw_sd(
  rho = 0,
  mu_RS = 0.005,
  gamma = 0.01,
  ...
  alpha = 0.01, gamma = 0.01,
  ...
)
```

In R, duplicate named arguments in a function call cause the second value to overwrite the first silently, with a warning. This is a code error that may have caused `phase` (which appears between the two `gamma` entries) to be effectively excluded from perturbation, potentially restricting the profile optimization.

---

**9. [Moderate] The COVID suppression end date is inconsistent between files**

In the Rmd around line 692–694, `covid_end = 333` is stated to correspond to "week of 05-17-2021" when most states lifted mask mandates. However, in `seirs_beta.R`, line 48, the comment reads: "Week of 2023-05-08, Public Health Emergency for COVID-19, declared under Section 319 of the Public Health Service Act, expires at the end of 2023-05-11." Week 333 from the start of 2015 data corresponds to mid-2021, not 2023. The inconsistency in the comment in `seirs_beta.R` is confusing and could mislead a reader trying to reproduce or verify the COVID suppression parameterization.

---

**10. [Moderate] The `R = 0` initialization in the advanced SEIRS model is biologically inconsistent for a 2015 start date**

The model is initialized in January 2015, which is mid-flu season. Setting `R = 0` (no recovered individuals) while using `eta * N` as initial infected/exposed means the entire remaining population is susceptible. This is biologically implausible for a population with multi-year flu history. The authors acknowledge this but claim immunity is "implicitly modeled through Beta and mu_RS." This is an incomplete justification: setting R = 0 at the start of a well-established annual endemic disease substantially inflates the initial susceptible pool and likely biases the early dynamics of the simulation.

---

**11. [Moderate] The spectral analysis (periodogram) labels are misleading**

The periodogram is produced with `spec.pgram()` using `xlab = "Frequency"` and `sub = "Cycles per Year"`, but the R `spec.pgram` function with weekly data returns frequency in cycles per week, not per year. The abline at `v = 1` is labeled as "1 cycle per year," but if the x-axis is cycles per week, the annual peak occurs at `1/52 ≈ 0.019`, not at 1. The authors' conclusion that "we observe a dominant frequency of one cycle per year" correctly identifies the seasonal pattern, but the plot's axis and the `abline(v = 1)` placement appear incorrect unless `spec.pgram` was returning frequency in cycles per observation (i.e., per week, so the annual frequency is ~1/52). This requires clarification or correction.

---

**12. [Moderate] The Brownian motion antigenic drift model is not validated against the data**

The antigenic drift is modeled as a Brownian motion with standard deviation `sigma_mut = 0.14` per week (sqrt). This parameter is fixed using a calculation based on literature drift rates. However, no check is performed to verify that this parameterization actually produces realistic antigenic distances over the 9-year window (e.g., by simulating from the model and comparing to known antigenic characterization data). The high value of `gamma` discovered during optimization may itself indicate that the BM model for antigenic drift is misspecified.

---

**13. [Moderate] The `H` accumulator is decremented by imported cases but should not be**

In the `rprocess` snippet (around line 990–996), imported infectious cases are added to both `I` and `H`:

```c
if (I < 10) {
    double imported = rpois(0.2); 
    I += imported;
    H += imported;
}
H += dN_EI;
```

However, `H` is meant to accumulate newly symptomatic cases (transitions from E to I via `dN_EI`). Imported cases added directly to `I` bypass the E compartment, so adding them to `H` as if they are newly symptomatic is inconsistent with the model definition. This could inflate apparent incidence during the pandemic suppression period when true transmission is near zero and the restarter fires frequently.

---

**14. [Minor] The AIC selection for the SARMA model involves a non-standard argument about mathematical inconsistency**

The text argues against `ARMA(3,0)` by saying there is "a mathematical inconsistency between ARMA(3,0) and ARMA(3,1)." This language is non-standard. If the authors mean that the likelihood surface is not smooth between these two models in the AIC table (e.g., a non-monotone pattern suggesting numerical issues), this should be stated more precisely. As written, the justification is unclear and may confuse the reader.

---

**15. [Minor] The "poor man's profile" is described as a profile likelihood but lacks re-optimization**

The text correctly notes that the poor man's profile "does not re-optimize other parameters at each rho." This is a significant limitation — what is computed is technically not a profile likelihood but a conditional likelihood slice. The presentation initially refers to it as a "profile likelihood" before clarifying the limitation. The text would benefit from calling it a "conditional likelihood" from the outset to avoid conceptual confusion with the proper profile likelihood that follows.

---

### Summary of Positive Aspects

- Strong biological motivation and thorough parameter initialization with literature support.
- Honest and detailed self-critique of model deficiencies (gamma issue, rho estimation).
- Use of both poor man's profile and true profile likelihood for rho, with posterior predictive checks.
- Thoughtful discussion of the COVID suppression effect using logistic ramp functions.
- Clear differentiation from prior work in related projects.

---

### Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project01/seirs_beta.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project01/seirs_global.R`
