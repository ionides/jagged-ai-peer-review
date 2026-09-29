# Peer Review: W25 Project 06
## Investigating Hungarian Chickenpox Infections (ARMA / SEIR-POMP / N-BEATS)

---

## Summary

This project analyzes weekly Hungarian chickenpox case counts (2005–2015, n = 522) using three modeling approaches: ARMA time-series, a seasonally forced stochastic SEIR model via the POMP framework, and a deep learning pipeline combining variational mode decomposition (VMD) with the N-BEATS architecture. The project's ambition—comparing mechanistic, statistical, and data-driven methods on a single dataset—is appropriate. However, the POMP analysis contains several serious methodological errors that invalidate the profile likelihood and the convergence claims, the mathematical model description contradicts the code, and the three-way model comparison is not conducted on a common footing. These issues undermine the project's central comparative goal.

**Key strengths:** Inclusion of both local and global mif2 searches; correct use of `logmeanexp` for log-likelihood aggregation; negative binomial measurement model; parameter transformations applied consistently.

**Key weaknesses:** POMP model is substantially worse than the ARMA benchmark but this gap is never acknowledged; profile likelihood is not a true profile and uses the wrong Wilks cutoff; `ivp()` is mis-applied to non-initial-value parameters; the mathematical model in the text omits features present in the equations (births, deaths, importation) but includes them in the equations yet the code implements none; and the three-model comparison uses incompatible metrics.

---

## Major Issues

### 1. POMP model substantially underperforms the ARMA benchmark with no acknowledgment

The ARMA(4,4) model achieves a log-likelihood of −3603.29 (reported in the text). The POMP global search finds a best log-likelihood of −3758.96 (confirmed from `results_1.rds`). The POMP model is therefore worse by approximately 156 log-likelihood units — a decisive margin.

The course convention (531-conventions.md) is explicit: "If the mechanistic model fits disastrously compared to the benchmark, our model is probably missing something important," and the appropriate response is to revise model structure, not to increase computational effort. The paper never compares these numbers, never acknowledges the gap, and instead characterizes the POMP fit as "reasonable" based solely on visual simulation plots. This omission is the single largest substantive failure of the POMP analysis. Quantitative comparison of the POMP and ARMA log-likelihoods should be reported, and the 156-unit deficit should prompt a model-structure revision — not just a summary that "simulations reproduced timing, amplitude, and periodicity."

**Reference:** POMP checklist §2 (Benchmark comparison), §3 (Quantitative goodness-of-fit); Error 1.6 (CC-Yes).

---

### 2. Profile likelihood for ρ is not a true profile, and uses the wrong Wilks cutoff

The "Profile Likelihood for Reporting Rate ρ" section does not compute a profile likelihood. A profile likelihood requires fixing ρ on a grid and optimizing all other parameters at each grid point. Instead, the authors filter the global search results by ρ and apply a log-likelihood cutoff — this is a marginal scatter plot, not a profile, and is correctly called a "Poor Man's Profile" in the text. The problem is that this approximation is then treated as if it produces a valid confidence interval.

Compounding this, the Wilks threshold used is `maxloglik − 4`, whereas the correct 95% CI cutoff for a one-dimensional profile is `maxloglik − 0.5 × qchisq(0.95, 1) ≈ maxloglik − 1.921`. The inflated cutoff of −4 is not the standard criterion and is not justified in the text. Inspection of `results_1.rds` confirms that using the correct Wilks threshold of −1.921 yields only a single global-search point satisfying the criterion (CI degenerates to a point), meaning the global search grid is too sparse to support any CI estimate at all under the correct threshold. The threshold was likely inflated to avoid a degenerate result, but this produces a CI that is not interpretable as a 95% interval.

To fix: either compute a true profile likelihood by re-running mif2 at each fixed ρ grid point with all nuisance parameters optimized, or explicitly state that no profile likelihood was computed and CI bounds are not reported.

**Reference:** Error 1.2 (CC-Yes, Major); POMP checklist §5 (Parameter identifiability).

---

### 3. `ivp()` applied to all parameters in `rw.sd`, including non-initial-value parameters

In both the local and global search, `rw.sd` is specified as:

```r
rw.sd = rw_sd(
  Beta = ivp(0.05), mu_EI = ivp(0.05), mu_IR = ivp(0.05),
  eta = ivp(0.02), rho = ivp(0.02), amp = ivp(0.05),
  phi = ivp(1), k = ivp(0.1)
)
```

The `ivp()` modifier applies the random walk perturbation only at t = t₀ and sets it to zero at all subsequent time steps. This is the correct specification only for parameters that function as initial conditions (e.g., the initial fraction susceptible, which depends only on the state at t₀). For time-constant process parameters — Beta, mu_EI, mu_IR, rho, amp, phi, k — the perturbation should be a constant standard deviation (e.g., `Beta = 0.05`), applied at every step throughout the filtering to enable gradient-following by the mif2 algorithm.

Using `ivp()` for these parameters means mif2 can only inject diversity at the start of the time series. While different particles will carry different parameter values (from the single perturbation at t₀), no additional exploration occurs as the filter progresses. This substantially reduces the algorithm's ability to locate high-likelihood regions and may explain why the global search log-likelihoods remain far below the ARMA benchmark. The course notes (Ch 16 p31) illustrate constant perturbation for rate parameters explicitly.

Note that `eta` (initial fraction recovered) is a genuine initial-value parameter and `ivp()` is appropriate there.

**Reference:** POMP checklist §6 (Computational adequacy).

---

### 4. Mathematical model description does not match the implemented code

The text presents the following differential equations for the SEIR dynamics:

- dS = μN − β(t)·SI/N − μS
- dE = β(t)·SI/N − σE − μE
- dI = σE − γI − μI + λ
- dR = γI − μR

These equations include (a) a birth inflow μN into S, (b) per-compartment death outflows μS, μE, μI, and (c) an importation term λ in I. None of these three features appear in `seir_step`. The code implements a closed population with no demographic turnover and no importation:

```c
S += dN_RS - dN_SE;
E += dN_SE - dN_EI;
I += dN_EI - dN_IR;
R += dN_IR - dN_RS;
```

Total population N = S + E + I + R is therefore conserved exactly, which is inconsistent with the text's description of μN births and μS, μE, μI deaths. The parameter `mu` appears in `paramnames` but is not used in `seir_step`. The `lambda` importation term described in the text is also absent from the code.

A reader cannot replicate the model described in the text using the provided code. This is a reproducibility failure of the type documented in Wheeler et al. (2024) — discrepancies between the written model specification and the code materially affect what analysis was actually conducted.

**Reference:** POMP checklist §10 (Reproducibility), code-supplement checklist §Traceability; Wheeler et al. (2024) §Model diagnostics.

---

### 5. Three-model comparison uses incompatible metrics and data

The overall conclusion compares ARMA (MAPE 36.82%, in-sample, on national aggregate), POMP (qualitative visual fit), and N-BEATS (MAPE 2.5–3%, out-of-sample validation set, on spatiotemporal county-level features). Three incompatibilities prevent this from being a valid comparison:

- **In-sample vs. out-of-sample:** The ARMA MAPE is computed on the training data; the N-BEATS MAPE is on a held-out validation set. Out-of-sample errors are naturally larger; reporting training-set error for one model and validation-set error for another systematically understates the ARMA error.
- **Data scope:** N-BEATS is trained on 1,220 VMD features derived from 20-county data. The ARMA and POMP models use only the national aggregate. The N-BEATS model has access to substantially more information.
- **Metric non-comparability:** The POMP model is never assigned a MAPE or an out-of-sample metric, making it impossible to place it in the same comparison table as ARMA and N-BEATS.

A valid comparison would require: all three models trained on national aggregate data, evaluated on a held-out test period using the same metric, with POMP models assessed by log-likelihood or MAPE from the filtering distribution.

---

### 6. `emeas` is inconsistent with `dmeas` and `rmeas`

The expected-measurement function is:
```c
emeas: E_infection = rho * H;
```
But the density and random-draw functions use a different state variable:
```c
dmeas: double mu = fmax(rho * NewEI, 1e-6); ...
rmeas: double mu = fmax(rho * NewEI, 1e-6); ...
```

`H` is a cumulative counter of I→R transitions (recovered individuals), accumulating over the entire run. `NewEI` is the count of E→I transitions in the current time step. These represent different quantities: `H` is an ever-increasing counter while `NewEI` is a per-step flow. The appropriate observable in an SEIR model for reported weekly cases is new infections per step (NewEI), not cumulative recoveries (H). The emeas function should be `E_infection = rho * NewEI` for consistency.

This discrepancy means that any functionality relying on `emeas` (e.g., trajectory matching or model-based forecasting using the expected measurement) will produce incorrect values.

**Reference:** POMP checklist §12 (Measurement model specification); code-supplement checklist §Traceability.

---

### 7. No seasonal ARIMA (SARIMA) considered despite prominent 52-week seasonality

The data shows strong annual (52-week) seasonal cycles, visible in both the raw time series plot and the moving-average plot. The ARMA section searches only over ARMA(p, q) with p, q ≤ 4 and no seasonal components. For weekly data with a 52-week period, a SARIMA(p, d, q)(P, D, Q)₅₂ model is more principled. The selected ARMA(4,4) may be capturing some seasonality via high-order AR and MA terms, but this is a less interpretable and potentially less efficient representation than explicit seasonal terms.

The absence of any SARIMA model — or even a discussion of why pure ARMA was chosen over seasonal alternatives — is a methodological gap for a project whose data has textbook seasonal structure.

---

## Minor Issues

### 8. `omega` (immunity waning rate) is never perturbed during global search

The global search guesses include `omega` (drawn from [0.002, 0.01]), but `omega` is absent from `my_rw`. In mif2, parameters absent from `rw.sd` are held fixed at their initialized values. This means each global search run tests a fixed omega value (drawn once at initialization) but never optimizes over it. The paper describes the global search as exploring all key parameters, but omega is effectively a fixed input that varies across runs by sampling, not by gradient-following. This inconsistency is not acknowledged, and the resulting omega estimates are not optimization products.

---

### 9. Profile likelihood CI range is insensitive to the Wilks threshold actually used

As computed from `results_1.rds`: with the correct Wilks cutoff (maxloglik − 1.921), only the single best-fit global search point passes, yielding a degenerate CI. The paper uses maxloglik − 4 to obtain the range [0.869, 0.987]. Neither threshold produces a scientifically valid CI: the correct threshold gives no interval, and the incorrect one gives an interval whose coverage probability is unknown. The paper reports a CI as if it were a valid 95% interval. This should be stated only as an approximation of the plausible range with an explicit caveat that the correct profile was not computed.

---

### 10. Local search: cooling fraction 0.3 departs from course standard without justification

The local mif2 runs use `cooling.fraction.50 = 0.3`, meaning perturbations decay to 30% of their initial size after 50 iterations. The course standard is 0.5 (Ch 15 p31–32). Faster cooling reduces the algorithm's ability to escape local optima; slower cooling may not have converged sufficiently at 100 iterations. The departure is not discussed or motivated. Given that the log-likelihoods from the local search (best: −3870.76) are substantially below the global search best (−3758.96), a sensitivity analysis on cooling fraction would be informative.

---

### 11. Initial SEIR parameter values are biologically implausible for chickenpox

The initial parameter vector sets `mu_EI = 0.08` per week, implying a mean incubation period of 1/0.08 = 12.5 weeks (≈ 87 days). The chickenpox incubation period is 10–21 days (≈ 1.4–3 weeks). Similarly, `mu_IR = 0.05` per week implies a mean infectious period of 20 weeks (≈ 140 days); the actual period is approximately 5–7 days. While these are starting values for optimization, initializing far from the biological plausible range can make convergence more difficult. The global search bounds reach up to mu_EI = 0.6/week (latency ≈ 12 days) and mu_IR = 0.6/week (infectious period ≈ 12 days), but the lower bounds of 0.01/week for both imply latency and infectious periods of 100 weeks, which are unrealistic. No discussion of parameter biological plausibility appears in the text.

**Reference:** POMP checklist §11 (Corroboration with scientific knowledge).

---

### 12. Log-ARMA vs. linear-ARMA MAPE comparison is also not valid

The text correctly notes that AIC values are not directly comparable across raw-scale and log-scale ARMA models. However, it then uses MAPE to compare them — MAPE on the log scale (4.69%) measures proportional error in log(infections + 1), while MAPE on the raw scale (36.82%) measures proportional error in infections. These quantities have no common interpretation. The statement "the log-ARMA model reduces relative error with a MAPE of only 4.69% versus 36.82%" is not a valid comparison and should be removed or reframed. Comparing models on different observation scales requires back-transforming predictions to a common scale.

---

### 13. `loglik.se < 10` filter is excessively permissive

When combining global and local results, the code applies `filter(is.finite(loglik), loglik.se < 10)`. A standard error of 10 log-likelihood units is very large; this allows points with enormous Monte Carlo noise into the pair plots and profile calculation. With `Nreps_eval = 10` replicated pfilter calls, Monte Carlo SEs of the observed magnitude (most < 1) are reasonable, but the cutoff of 10 admits outliers that could distort the profile scatter. A threshold of 1 or 2 is more defensible.

---

### 14. `rw.sd` is redundantly re-specified inside `mif2` in the local search code

The local search code (in the `seir_local` chunk, lines 587–588) passes `partrans` and `paramnames` directly to `mif2`:
```r
partrans=parameter_trans(log=c("Beta", "mu_EI", "mu_IR", "k"), logit=c("eta", "rho")),
paramnames=c("N", "Beta", ...)
```
These are already stored in the `chickenSEIR` pomp object (defined with `partrans` and `paramnames`), so re-specifying them inside `mif2` is redundant. More critically, the re-specification in the local search omits `omega` and `amp` from `partrans`, while the global pomp object includes `log = c("Beta", "mu_EI", "mu_IR", "k", "omega")` and `logit = c("eta", "rho", "amp")`. The inconsistency between the pomp-object transforms and the mif2-call transforms may silently apply incorrect transformations during the local search.

---

### 15. Duplicate `library(pomp)` and auto-installing packages in setup

The setup chunk calls `library(pomp)` twice (lines 20–21). More importantly, a later chunk (lines 404–410) includes `install.packages(to_install, ...)` without user consent, which violates the code-supplement standard (code should not auto-install packages). This is a minor code quality issue but does affect portability if run in a controlled environment.

---

## Summary of Issue Severity

| # | Issue | Severity |
|---|-------|----------|
| 1 | POMP underperforms ARMA by 156 log-lik units, gap unacknowledged | Major |
| 2 | Profile likelihood is not a true profile; Wilks cutoff is wrong | Major |
| 3 | `ivp()` mis-applied to non-IVP parameters in `rw.sd` | Major |
| 4 | Text model (births, deaths, importation) contradicts code | Major |
| 5 | Three-model comparison uses incompatible metrics and data | Major |
| 6 | `emeas` uses H (cumulative) inconsistent with dmeas/rmeas using NewEI | Major |
| 7 | No SARIMA considered despite 52-week seasonality | Major |
| 8 | `omega` absent from `rw.sd` in global search | Minor |
| 9 | Profile CI is degenerate under correct Wilks threshold | Minor |
| 10 | Cooling fraction 0.3 not justified | Minor |
| 11 | Initial parameter values biologically implausible | Minor |
| 12 | Log-ARMA vs. linear-ARMA MAPE comparison invalid | Minor |
| 13 | `loglik.se < 10` filter is too permissive | Minor |
| 14 | Redundant/inconsistent `partrans` inside local search `mif2` | Minor |
| 15 | Duplicate `library(pomp)`; auto-install without consent | Minor |

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project06/blinded.Rmd`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project06/results_1.rds`
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project06/local_loglikes_1.rds`
