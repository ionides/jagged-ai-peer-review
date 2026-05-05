# Peer Review: W22 Project 05
## "An Inquiry into the Effects of Vaccination on COVID-19 Cases using Compartment Models"

---

## Summary

This project attempts to model daily COVID-19 cases in the United States from April 19, 2021 to April 15, 2022, with the stated goal of investigating how different vaccine adoption rates would affect case counts. The authors first fit ARIMA and ARMA-GARCH models, then construct a custom SVEIQRD POMP compartment model incorporating vaccination, exposure, quarantine, and death compartments. The POMP estimation uses both local and global IF2 searches. The project is ambitious in scope but suffers from critical methodological and coding flaws, and ultimately fails to achieve its stated goal of simulating alternative vaccination scenarios.

---

## Weaknesses (Prioritized)

### 1. [MAJOR] The Primary Research Question Is Never Answered

The stated goal of the project is to simulate counterfactual vaccination scenarios to understand how faster or slower vaccine adoption would have affected COVID-19 cases. This is explicitly promised in the Introduction: "we attempt to answer this question by modelling the COVID-19 pandemic following April 19,2021 using the compartment model framework in epidemiology and simulating different vaccine adoption scenarios from our model." No such simulations are ever produced. The Conclusion acknowledges that the model did not converge sufficiently, but there is no attempt to at least partially address the question, even under admitted uncertainty. The project's core deliverable is entirely absent.

### 2. [MAJOR] Critical Bug in the `dmeasure` Condition — Always-True Guard

In `model_dmeas` (and confirmed identically in `model.c` lines 298-308), the condition guarding the likelihood computation is:

```c
if (cases <= 10*sd || cases >= -10*sd)
```

Because `sd >= 0` always, the condition `cases >= -10*sd` is equivalent to `cases >= (some non-positive number)`, which is true for all non-negative case counts. This means the `else { lik = tol; }` branch (the outlier-rejection clause) is never reached. The intended logic was almost certainly `cases >= 10*sd` (using a positive bound), so the outer `if` should be `cases <= 10*sd && cases >= -10*sd`, i.e., `|cases| <= 10*sd`. As written, the condition is a logical tautology and the density is computed for all observations regardless of how extreme they are, eliminating the intended outlier-protection mechanism.

### 3. [MAJOR] Inconsistency Between `dmeasure` and `rmeasure` Standard Deviation Formulas

The `dmeasure` snippet computes `sd = sqrt(pow(rho*H,2) + chi*H) + tol` (with `tol` added outside the square root), while `rmeasure` computes `sd = sqrt(pow(rho*H,2) + chi*H + tol)` (with `tol` inside the square root). These produce different numerical values of `sd`. The measurement model used for evaluation is therefore not the same as the one used for simulation, creating a fundamental inconsistency between the generative model and the likelihood. This undermines the statistical validity of all IF2 results.

### 4. [MAJOR] Model Equations Have Errors: V Compartment Is Absorbing; VE Flow Missing from E

In the compartment equations (lines 444-451), the `V(t)` equation is:

```
V(t) = V(0) + N_SV(t)
```

There is no subtraction of `N_VE(t)`, meaning vaccinated individuals can never move to the Exposed compartment. However, in the process model code (`model_step`), `dN_VE` is drawn and subtracted from V. The written mathematical equations and the implemented code are contradictory. Additionally, the `E(t)` equation states `E(t) = E(0) + N_SE(t) + N_SV(t) - N_EI(t)`, but should be `E(0) + N_SE(t) + N_VE(t) - N_EI(t)` — the code correctly uses `N_VE` but the written math uses `N_SV`, a copy-paste error that means the displayed model specification is wrong.

### 5. [MAJOR] IF2 Local Search Uses Only 8 Chains Regardless of Run Level

The local search hard-codes `foreach(i=1:8, ...)` regardless of the run level and number of cores. The number of IF2 chains is not scaled with the `run_level` variable even though all other tuning parameters (`Num_Particales`, `Num_Mifs`, etc.) are. With only 8 chains at run level 3 (on a cluster with 8+ cores), the local search is severely underpowered relative to what the run-level framework implies for a global search with 800 starting points. By contrast, the global search correctly iterates over `num_cores` chains. This asymmetry suggests the local search design was not adapted for high-performance computation.

### 6. [MAJOR] Model Does Not Use Actual Vaccination Data Despite Having It Available

The authors have CDC vaccination data at daily resolution and explicitly load it. They then choose to model vaccination as a constant per-capita rate `nu` (estimated as a single parameter) rather than as an observed covariate. The justification given — that they want to simulate different vaccination scenarios — is circular: one can still simulate counterfactuals with a fitted covariate-based flow. Treating `nu` as a fixed estimated constant ignores the time-varying nature of vaccination rates (which peaked and then declined sharply), making the model structurally unable to reproduce the vaccination dynamics actually observed. This is one likely reason the model fails to fit the data.

### 7. [MAJOR] No Profile Likelihood or Confidence Intervals for Any Parameters

The project never computes profile likelihoods, confidence intervals, or any formal uncertainty quantification for the estimated parameters. The only output shown is the top 5 rows from `arrange(global_cache, -loglik)`. With a highly overparameterized model (14 free parameters) and acknowledged convergence issues, the absence of profiles makes it impossible to assess which parameters are well-identified and which are confounded. Standard POMP analysis practice requires at minimum a profile likelihood for the key biological parameters.

### 8. [MAJOR] ARMA-GARCH Section Provides No Fitted Results

The ARMA-GARCH fitting code block is marked `eval=F`, meaning it is never executed and no results are shown. The authors discuss the ARMA-GARCH as a natural extension and claim it produced "computational issues regarding non-invertible Hessian matrix," but no output, no diagnostic, and no fitted model summary is presented. The reader cannot verify the claimed failure or assess whether alternative GARCH specifications were tried systematically. Mentioning a failed approach without showing the failure is insufficient.

### 9. [MINOR] `beta_t` Definition Has Typographical Error in Mathematical Notation

The piecewise definition of `beta_t` (lines 487-493) has the interval conditions written incorrectly:

```
b_o   for  t >= July 1 2021
b_1   for  1 July 2021 < t <= December 1 2021
b_2   for  > t December 1 2021
```

The third condition is syntactically garbled (`> t December 1 2021` is not a valid mathematical expression). Additionally, `b_o` (subscript letter "o") is used in the display while the code uses `b1`, and parameter names shift between the math display (`b_o, b_1, b_2`) and the code (`b1, b2, b3`). The discussion text later refers to `b_2` and `b_3` instead of `b_1` and `b_2`. This cascade of label errors makes the model description confusing to follow.

### 10. [MINOR] `S(0)` Equation Is Self-Referential

The initial condition for `S(0)` is stated as:

```
S(0) = N - V(0) - S(0) - E(0) - I(0) - Q(0) - R(0) - D(0)
```

This equation includes `S(0)` on both sides, which is mathematically incoherent. The code correctly computes `S = N - initial_V - E - I - initial_Q - initial_R - initial_D`, but the written equation is clearly a typo (presumably one `S(0)` on the right should be `V(0)` or simply removed).

### 11. [MINOR] `initial_R` Is Computed Incorrectly — Does Not Reflect True Recovered Population

The initial recovered compartment `initial_R` is set to the number of cases minus deaths in the 6 months before April 19, 2021. This dramatically understates the true recovered population, which should include all individuals who were previously infected and recovered over the full pandemic history (starting in early 2020). Using only 6 months of prior cases while the initial vaccinated count `initial_V` (approximately 85 million) is subtracted from `S` leads to an inconsistently specified initial state — many vaccinated individuals are, in effect, counted as susceptible in the S compartment.

### 12. [MINOR] Pairs Plots Show Only 8 Local Search Points — Effectively Uninformative

The pairs plot for the local search displays results from only 8 replications with 5 pfilter evaluations each. The text acknowledges "the plots of loglik look so sparse that it does not give us a clear picture or hint of the ridge in likelihood surface." With 8 points, such a plot is too sparse to meaningfully characterize the likelihood surface geometry, and including it in the report without noting that this inadequacy stems from the limited number of chains adds little analytical value.

### 13. [MINOR] `loglik.se < 0.5` Filter Criterion Is Too Permissive and Not Justified

The filtering step `local_cache[local_cache$loglik.se < .5, ]` applies a standard error cutoff of 0.5 log-likelihood units. This is a nonstandard threshold that is never motivated. With `Num_Reps = 5` pfilter evaluations at run level 1 (the apparent execution level on the authors' machines), the Monte Carlo uncertainty in log-likelihood estimates can be large, and a threshold of 0.5 may retain very unreliable estimates. No sensitivity analysis to this cutoff is performed.

### 14. [MINOR] The ARIMA Model Section Conflates Differences

The project uses ARIMA(p,1,q) models for the daily case count, which means the model is being fit to the change in daily cases (a second difference of cumulative cases). The text states this is analogous to financial returns, but the analogy is imprecise: returns are first differences of log prices (first difference), while here the authors take the first difference of an already-differenced series. This is noted implicitly in the code (`change_daily_cases`), but the exposition does not clearly distinguish between daily cases and the change in daily cases, creating confusion about what the model is actually modeling.

### 15. [MINOR] Missing Model Diagram Image (`model_diag.png`)

The Rmd references `![](model_diag.png)` but the file in the directory is named `Model_Diag.PNG` (capital letters, different extension). On case-sensitive file systems this reference will fail to render. The HTML output includes the discussion diagram (`discussion_Diag.PNG`) referenced as `![](discussion_Diag.png)` — again a case mismatch. This reproducibility issue means the model diagram may not appear in a fresh rendering.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project05/model.c`
