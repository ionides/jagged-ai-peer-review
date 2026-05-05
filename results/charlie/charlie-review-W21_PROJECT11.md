# Peer Review: W21 Project 11
**Title:** Modeling COVID-19 Cases in Michigan: ARMA model v.s. SEIR POMP model

---

## Summary

This project applies an ARMA model and a stochastic SEIR POMP model to Michigan COVID-19 daily case counts during the winter surge (October 2020 – February 2021). The ARMA portion fits an ARMA(2,2) on HP-filtered data. The POMP portion builds a binomial Euler SEIR model with a binomial measurement model, performs local and global likelihood searches, and reports parameter estimates. While the project covers the expected STATS 531 workflow, it suffers from several serious methodological problems: the measurement model is fundamentally misspecified (reporting observations against cumulative rather than incremental infections), the rho and eta parameters are fixed without justification from likelihood inference, the global search uses grossly insufficient computational effort (Nmif=50 re-used from local search without increasing), no profile likelihoods are computed for any parameter, and no non-mechanistic benchmark is reported. The very large log-likelihood standard errors (up to 1005 log units) in the saved results confirm the computation is not reliable.

---

## Major Issues

### 1. Critical measurement model bug: H accumulates recoveries but is never reset (accumvar misuse)

The `seir_step` Csnippet increments `H += dN_IR` — that is, `H` accumulates the total number of individuals who have transitioned from I to R since time `t0`. The `accumvars="H"` argument instructs pomp to reset `H` to zero at each observation time, so `H` represents the incremental flow from I to R between consecutive observation times. However, the measurement model `dbinom(reports, H, rho, give_log)` tries to draw observed cases from a binomial with size `H`. The problem is that new cases arise from the E→I transition (`dN_EI`), not from the I→R transition (`dN_IR`). H should accumulate `dN_EI` (newly infectious individuals who will eventually be detected), not `dN_IR` (recoveries). This is a fundamental structural error: the observed data (new reported positives) is being linked to the wrong flow in the model. The measurement model is measuring recoveries, not infections, and this silently distorts all parameter estimates. All reported likelihoods and parameter estimates are unreliable as a result.

### 2. Reporting rate and susceptibility fraction fixed rather than estimated

The paper fixes `rho = 0.1` and `eta = 0.84` without estimating these quantities from the data. The justification for `rho = 0.1` is a single external preprint (MIT underreporting estimate). In the local search code, only `Beta`, `mu_EI`, `mu_IR`, and `eta` are in `rw.sd`; `rho` is in `fixed_params` and is never varied. Given that reporting rates for COVID-19 varied substantially over the pandemic and across regions, and given that `rho` is strongly collinear with `eta`, fixing both without a sensitivity analysis leaves the identifiability of the remaining parameters entirely unassessed. Wheeler et al. (2024) emphasize that fixed parameters require explicit justification; here the justification is an approximate population-level estimate rather than a likelihood-based argument. CC-Yes (Error 1.2 context: slicing rather than profiling over fixed parameters).

### 3. No profile likelihoods computed for any parameter

No profile likelihood is computed for any model parameter. The project goes directly from local/global search to a conclusion without assessing parameter identifiability or constructing confidence intervals. This is particularly problematic given that the local search trace plots show that `mu_EI` collapses to near zero and `Beta` and `mu_IR` do not converge, which are classic signals of poor identifiability that profile likelihood analysis would reveal and that warrant diagnostic follow-up. See Wheeler et al. (2024) §Parameter identifiability and uncertainty; also CC-Yes Error 1.9 (profile not computed).

### 4. Global search uses far too little computational effort

The global search (300 starting points) calls `mif2` with only `Nmif=50` iterations (the same as the local search), and this is applied twice (`mif2 %>% mif2(Nmif=50)`) for a total of 100 iterations. For a global search across a 4-dimensional space, this is likely insufficient for convergence. The log-likelihood standard errors in `new_global2.csv` confirm this: the best result has SE = 1.08 log units (marginal), but other top results have SEs of 82, 1005, and larger — indicating severe particle degeneracy. Results with SE >> 1 cannot be trusted as valid likelihood evaluations. The standard course convention (run_level=3) suggests 200 Nmif iterations and 5000 particles for a full run. The global search here is closer to a run_level=1 or 2 effort applied at global scale. See Wheeler et al. (2024) §Computational adequacy; CC-Yes Error 1.8.

### 5. No non-mechanistic benchmark comparison reported

The project fits an ARMA(2,2) to HP-filtered data and then fits a SEIR POMP model, but it never compares the POMP model's likelihood to that of the ARMA model or to any other non-mechanistic benchmark (e.g., negative binomial IID, ARMA on raw counts). The conclusion states the POMP model provided "inconclusive results" but does not quantify how much worse it performed relative to a baseline. Without a benchmark, it is impossible to assess whether the SEIR structure captures any meaningful epidemiological signal beyond what a simple statistical model achieves. See Wheeler et al. (2024) §Benchmark comparison; CC-Yes Error 1.6.

### 6. Very large Monte Carlo standard errors in reported likelihoods

The `cov_params.csv` file shows that the initial particle filter evaluation (Np=1000, 10 replicates, at the hand-picked starting point) yields a log-likelihood of approximately -54,405 with SE = 41.5 log units. In `new_global2.csv`, several global search results have SEs exceeding 100 or even 1000 log units. A standard error of 41 log units means the true likelihood could plausibly range over 80+ log units, rendering any comparison meaningless. The course standard (Nreps_eval=10, Np=1000) is supposed to produce small SEs; the enormous SEs here indicate either that the model is severely misspecified (particles collapse) or that Np=1000 is insufficient for this model. CC-Yes Error 1.4.

### 7. Inconsistency between described SEIR model and initialization

The mathematical write-up presents the SEIR model with `S(0) = N*eta`, `R(0) = N*(1-eta)`, but the `seir_init` Csnippet also sets `H = nearbyint((1-eta)*N)`. This means `H`, the accumulator for observed cases, is initialized to `N*(1-eta)` — approximately 1.6 million individuals — rather than zero. Since `H` is an `accumvar`, pomp resets it at each observation time, so this initialization only affects the very first observation period. But setting H to a huge non-zero value at t0 means the very first likelihood evaluation uses a binomial with size ~1.6 million, which is internally inconsistent with the stated measurement model logic. The correct initialization for an accumvar is zero. This is a code-text inconsistency of the type documented in Wheeler et al. (2024) §Reproducibility.

### 8. ARMA model selection text contradicts code

The text (line 108) states: "We will consider the ARMA(2, 2) model for meeting the criteria..." and proceeds to use `arima22` for residual analysis. However, the immediately preceding code block prints `arima11` (the ARMA(1,1) object), not the ARMA(2,2) selected for further analysis. The AIC table is also not shown in the text discussion — the reader cannot verify what the winning AIC values were or whether the choice of ARMA(2,2) over, say, ARMA(1,1) is supported by the table. This creates a text-code inconsistency that undermines reproducibility.

---

## Minor Issues

### 9. rw.sd magnitudes appear too small for the logit-transformed parameters

The local search uses `rw.sd(Beta=0.01, mu_EI=0.01, mu_IR=0.001, eta=0.001)`. The course convention for parameters estimated on a logit or log scale is `rw.sd = 0.02`. The values used here — especially `mu_IR=0.001` and `eta=0.001` — are 10–20x smaller than the course standard, which will slow exploration of the likelihood surface dramatically and may be contributing to the poor convergence observed. (531-conventions.md: rw.sd = 0.02 on log/logit scale is standard.)

### 10. HP filter lambda choice is not clearly appropriate for daily epidemic data

The paper uses `hpfilter(..., freq=100)` for daily data, citing a course slide about lambda = 100. The lambda = 100 recommendation is typically for quarterly macroeconomic data; for daily data, much larger lambda values (e.g., 10^6 or higher) are conventional. Using lambda = 100 on daily epidemic case data will over-smooth and may remove epidemic dynamics rather than just trend. The choice is not examined for sensitivity.

### 11. Convergence diagnosis focuses on parameter spread rather than likelihood stability

The local search trace plot analysis (line 381) reports that `beta` "varies between 0.3 and 0.7" and interprets this as model behavior, but does not comment on whether the log-likelihood panel is converging upward across iterations — which is the primary convergence diagnostic. The course convention (531-conventions.md) is that spread in parameter panels is acceptable; what matters is whether the loglik panel converges. The text inverts this priority, treating parameter spread as problematic without checking loglik convergence.

### 12. Global search description appears before the code that runs it

In the Rmd, the text under "SEIR Global Search" (line 387) describes results ("mu_EI stays between 0.0 and 0.15", "eta appeared to be a little lower than our local search") but this narrative appears before the global search code chunk executes and before the pairs plot is shown. This ordering implies the global search results were hand-inspected during code development rather than described from the rendered output, which is a reproducibility presentation issue.

### 13. The partrans block omits rho and eta from the transformation

The `partrans` block applies logit transformation only to `c("Beta", "mu_EI", "mu_IR")`. The parameter `eta` represents a fraction (0 to 1) and should also be logit-transformed to constrain it to (0,1) during optimization. Not transforming `eta` risks mif2 proposing values outside [0,1], which would cause errors or silently invalid compartment sizes. The same applies to `rho` if it were estimated.

### 14. Data loaded from a remote GitHub URL, creating a reproducibility dependency

The POMP section reloads data from a raw GitHub URL (`https://raw.githubusercontent.com/jeremyny/G6_Final/main/MI_COVID19_data.csv`) rather than from the local `covid_data.csv` file used earlier. This creates an external dependency that can break if the repository is deleted or made private, violating the reproducibility standard documented in Wheeler et al. (2024) §Reproducibility and extendability.

### 15. No simulation-based diagnostics comparing filtered vs. forward simulations

The project includes a basic `pfilter` plot (labeled "Particle Filter Check") but does not examine the filtering distribution versus forward simulations, nor does it plot conditional log-likelihoods by time period to identify where the model fits poorly. The conditional log-likelihood plot would be informative here, as the authors note "it was difficult to match the rapid increase and decrease in cases" — precisely the kind of observation that a conditional log-likelihood plot by time would illuminate systematically. See Wheeler et al. (2024) §Model diagnostics.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project11/new_global2.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project11/cov_params.csv`
