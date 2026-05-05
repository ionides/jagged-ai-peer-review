# Peer Review: W22 Project 05
## "An Inquiry into the Effects of Vaccination on COVID-19 Cases using Compartment Models"

---

## Summary

This project attempts to model daily U.S. COVID-19 cases from April 2021 to April 2022 using an ARIMA baseline and a custom SVEIQRD (Susceptible–Vaccinated–Exposed–Infected–Quarantined–Recovered–Dead) compartment model implemented in the `pomp` framework, with the stated goal of simulating counterfactual vaccine adoption scenarios. While the ambition of the research question is commendable and the model design reflects genuine epidemiological thought (incorporating vaccination, variants, and quarantine stages), the analysis falls short on virtually every dimension required for valid POMP inference: the measurement model contains a logical error that silently accepts all observations, iterated filtering is run with severely inadequate computation, no convergence is demonstrated, no profile likelihoods are computed, no benchmark comparison is performed, and the stated scientific goal (vaccine scenario simulation) is never actually executed. The conclusion honestly acknowledges model failure but attributes it to epidemiological complexity rather than diagnosing the methodological deficiencies that are the proximate cause.

---

## Major Issues

### 1. Defective `dmeasure` condition renders likelihood evaluation unreliable

The `model_dmeas` Csnippet (Rmd lines 590–606) contains the following guard:

```c
if (cases <= 10*sd || cases >= -10*sd){
```

Because `sd` is always non-negative and `cases` is always non-negative, the condition `cases >= -10*sd` is trivially true for every observation. The `||` (OR) operator means the entire `if` block is entered unconditionally — the `else { lik = tol; }` branch is never reached. Effectively, every observation is assigned a non-trivial likelihood regardless of fit quality. This is a fundamental measurement model error: the filter cannot correctly down-weight particles whose simulated trajectories are inconsistent with the data, so the particle filter cannot function as intended. All reported log-likelihoods are therefore invalid. The correct guard should use `&&` (AND) instead of `||`, restricting the normal density to observations within a plausible range and assigning tolerance otherwise. This bug alone invalidates the entire POMP inference section.

---

### 2. Critically insufficient computation — run_level logic is unreliable

The run_level switch (Rmd lines 731–741) sets `run_level = 3` only when `num_cores >= 8`, but defaults to `run_level = 1` otherwise. At run_level=1, only 50 particles and 5 mif2 iterations are used. Even at run_level=3, the particle count is 500 — low for a 7-compartment model spanning ~360 daily observations. The local search uses a hard-coded `replicate(5, ...)` for likelihood evaluation regardless of run_level (line 785), yielding very noisy likelihood estimates. The text acknowledges the log-likelihood "waves between -7000 and -5000" without recognizing this instability as a computational adequacy problem rather than evidence of model difficulty. Per Wheeler et al. (2024), computational effort must be verified through convergence diagnostics; no such verification is performed.

---

### 3. No convergence demonstrated for iterated filtering

The trace plots show log-likelihood ranging from -7000 to -5000 across runs with no upward trend or clustering near a maximum. The text acknowledges "large variability" but treats this as a data characteristic rather than a convergence failure. The course standard (Error 1.8, CC-Yes) requires showing that multiple independent searches from different starting points reach similar terminal likelihoods. This is not demonstrated. The authors proceed to conclusions from a non-converged optimizer, making all reported parameter estimates unreliable.

---

### 4. No profile likelihoods computed; no confidence intervals reported

The project does not compute profile likelihoods for any parameter. This means there is no basis for assessing whether parameters such as vaccine efficacy (`gamma`), transmission rates (`b1`, `b2`, `b3`), or the vaccination rate (`nu`) are identifiable from the data. Given the model has 14 estimated parameters and only ~360 observations, identifiability concerns are acute. The pairs plots shown are too sparse to substitute for proper profile analysis. Per Wheeler et al. (2024) §Parameter identifiability and uncertainty, and course Error 1.9 (CC-Yes), profile likelihoods are required to make valid inferences about individual parameters.

---

### 5. No benchmark comparison

The mechanistic SVEIQRD model is never compared against any non-mechanistic baseline — not even an IID negative binomial model. The ARIMA analysis is abandoned due to heteroskedasticity, but no log-likelihood comparison between the POMP model and the ARIMA model is presented either. Without a benchmark, it is impossible to assess whether the compartment model captures any meaningful structure beyond what a simple statistical model would achieve. The course standard (Error 1.6, CC-Yes) and Wheeler et al. (2024) §Benchmark comparison both require this. The authors' stated best global log-likelihood of -5677 cannot be interpreted without reference to a baseline.

---

### 6. Stated scientific goal is never executed

The introduction and conclusion frame the project as an investigation of "what if the vaccine rollout was faster or slower," to be answered via simulation from the fitted model. This scenario analysis is never performed. The paper ends with an acknowledgement of model failure. This means the primary research question motivating the SVEIQRD design goes entirely unanswered. The Discussion section proposes future improvements but does not attempt to execute even a crude version of the counterfactual.

---

### 7. Model misspecification: vaccinated compartment dynamics are inconsistent

In the compartment equations (Rmd line 443–451), the differential for E is written as:

```
E(t) = E(0) + N_SE(t) + N_SV(t) - N_EI(t)
```

This adds `N_SV` to the Exposed compartment, implying vaccination immediately causes exposure. This is a typographical or conceptual error in the model description — individuals moving from S to V should go to V, not E. The Csnippet code (line 568–570) correctly implements `E += dN_SE + dN_VE - dN_EI`, so the code and the mathematical exposition are inconsistent. Readers cannot verify the model from the write-up alone.

---

### 8. Local search uses mif2 loglik directly without adequate re-evaluation

The local search code (lines 779–792) uses `mifs_local %>% coef(...)` with `logLik(mifs_local)` directly from mif2 output to find the best-performing local run (`which.max(logLik(mifs_local))`). The course standard (course notes Ch 15, p37) explicitly states that mif2's internally reported likelihood is NOT reliable for inference because parameter perturbations are applied in the final iteration. The subsequent re-evaluation with `replicate(5, pfilter(...))` is done correctly, but the initial selection of which mif2 run to trust for simulation (`max_coefs_local`) is based on unreliable mif2 loglik. This introduces bias in the selected parameters used for simulation (line 822).

---

### 9. Measurement model choice is not epidemiologically justified

The observation model is Gaussian with mean `chi * H` and standard deviation `sqrt((rho * H)^2 + chi * H)`. Daily COVID-19 case counts are discrete, non-negative, and heavily right-skewed. A Gaussian measurement model is unusual for case count data, and the project does not justify this choice. The standard approach for count data is a negative binomial or Poisson measurement model. The Gaussian model can assign positive probability to negative case counts, which the code partially addresses by clipping in `rmeasure` but not in `dmeasure`. Furthermore, the `dmeas` Csnippet uses `dnorm(..., 0)` (no log) but then applies `if(give_log) lik = log(lik)`, which is correct structurally but compounds the logical error in the guard condition described in Issue 1.

---

### 10. Global search box includes fixed parameters, causing silent parameter override

The `covid_box` (Rmd lines 842–863) includes rows for `N`, `initial_V`, `last_week_cases`, `initial_Q`, `initial_R`, and `initial_D` as single-value entries. When `apply(covid_box, 1, function(x) runif(1, x[1], x[2]))` is called (line 869), single-value rows produce `runif(1, x, x)` = exactly `x`, so fixed parameters are preserved. However, the box structure creates an implicit assumption that these scalars are treated as two-element vectors by `rbind`. This is fragile and could silently produce wrong draws if the `rbind` structure is mis-specified. The course-standard approach is to separate fixed and estimated parameters explicitly.

---

## Minor Issues

### 11. rw.sd values are halved relative to course standard without justification

The random walk standard deviations are set to 0.01 (Rmd lines 748–763) for all parameters, whereas the course standard is 0.02 on the log/logit scale (531-conventions.md). This means the parameter perturbations are smaller, requiring more iterations to explore the same region. Given that iteration counts are already at the lower edge (5 at run_level=1), smaller rw.sd compounds the convergence problem. No justification for halving the perturbation size is provided.

### 12. S(0) equation contains a circular reference

The initialization equation in the model description (Rmd line 541) reads: `S(0) = N - V(0) - S(0) - E(0) - I(0) - Q(0) - R(0) - D(0)`, which is self-referential. This should be `S(0) = N - V(0) - E(0) - I(0) - Q(0) - R(0) - D(0)`. The Csnippet implementation in `model_rinit` (line 580) is correct, but the mathematical exposition is wrong.

### 13. No model diagnostics performed

No conditional log-likelihoods, effective sample sizes, or filtering distributions are examined. Per Wheeler et al. (2024) §Model diagnostics, these tools are essential to understand where and how a model fails. The authors observe that simulations overestimate cases but do not decompose this into specific time periods or compartments where the fit breaks down.

### 14. Pairs plot is used as a substitute for profile likelihood without acknowledgement

The pairs plots (Rmd lines 835, 930) display pairwise parameter relationships from the likelihood surface but are described as if they are sufficient to characterize identifiability. The authors note the plots "look sparse" but do not connect this to the need for profile likelihood computation. Sparse pairs plots indicate insufficient sampling of the likelihood surface, not a property of the model.

### 15. Multiple spelling and grammatical errors throughout

The text contains recurring errors: "succeptible" (should be susceptible), "omicron" consistently misspelled as "Omnicron" in variable names and text, "preleminary," "hetersokadasticity," "seperate," "avilability," and "anniversery." The beta notation in the text (line 488–493) is internally inconsistent: the piecewise definition labels values as `b_o`, `b_1`, `b_2` but the code uses `b1`, `b2`, `b3`, and the text later refers to "$b_2$ and $b_3$" as Delta and Omicron parameters even though the piecewise definition has three cases labeled 0, 1, 2. These inconsistencies make the model description difficult to verify.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project05/blinded.Rmd`
