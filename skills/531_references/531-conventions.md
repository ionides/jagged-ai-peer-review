<!--
type: reference
name: STATS 531 Course Conventions
version: 0.2.0
source: slides Ch 09, 15, 16, 17; updated 2026-03-25
scope: What NOT to flag when reviewing STATS 531 W25 final projects
-->

# STATS 531 Course Conventions

## Purpose

Prevent false positives in AI review of STATS 531 W25 final projects by documenting course-specific conventions that differ from publication-standard expectations.

Load alongside the main review skill. Do not flag items listed in this reference as errors.

---

## Course Overview

STATS 531 is a graduate-level time series analysis course at the University of Michigan.

Final projects ask students to apply time series methods to a real dataset and write a reproducible Quarto report. They are demonstrations of course competency, not journal submissions.

---

## Methodological scope

**ARIMA-class:** ARMA/ARIMA, spectral analysis, AIC model selection, ACF/PACF diagnostics, Ljung-Box test

**POMP-class:** POMP models, particle filter (`pfilter`), iterated filtering (`mif2`), profile likelihood CIs, simulation-based diagnostics — all via the `pomp` R package

---

## Do NOT flag these as errors

### Formatting
- Reports ~10 pages are normal. Shorter is not automatically inadequate.
- Long supplements with full output, plots, or code are acceptable.

### Code and reproducibility
- Git repo is the submission vehicle. No separate archive required.
- Code expected to run; speed optimization not required.

### ACF residual diagnostics (ARIMA)
- **1/18 rule**: "It is not a major model violation to have one out of 18 lags narrowly outside the dashed lines showing pointwise acceptance regions at the 5% level under a null hypothesis of Gaussian white noise." (Ch 09, p27)
- Some residual autocorrelation is consistent with AIC evidence for larger models — do not treat a single borderline lag as a model failure.
- Mild heteroskedasticity in residuals (amplitude decreasing over time) is worth noting but is not automatically a major flaw.

### POMP: run_level framework
The standard course template uses a `run_level` switch. These are the expected values (Ch 16, p28-30):

| Parameter     | run_level=1 | run_level=2 | run_level=3 |
|---------------|-------------|-------------|-------------|
| Np            | 100         | 1,000       | 5,000       |
| Nmif          | 10          | 100         | 200         |
| Nreps_eval    | 2           | 10          | 20          |
| Nreps_local   | 10          | 20          | 40          |
| Nreps_global  | 10          | 20          | 100         |
| Nsim          | 50          | 100         | 500         |

- run_level=1: minutes (debugging). run_level=2: tens of minutes (preliminary). run_level=3: hours (final, often HPC).
- **"Appropriate values of the algorithmic parameters for each run-level are context dependent."** (Ch 16, p30) — do not penalize students for using values that differ from the table if they explain why.
- Student-level work is typically run_level=2 or 3. Do not flag run_level=2 as insufficient unless results are clearly unstable.

### POMP: likelihood evaluation
- mif2's internally reported likelihood is NOT reliable for inference (parameter perturbations are applied in the final iteration, and fewer particles are used). Students must re-evaluate using replicated `pfilter` calls. This is the course standard. (Ch 15, p37)
- Standard pattern: `replicate(Nreps_eval, logLik(pfilter(m, Np=Np)))` then `logmeanexp(se=TRUE)`. Accept minor variations on this pattern.
- Some Monte Carlo noise in log-likelihoods is expected. Flag only if the standard error is clearly large relative to likelihood differences being compared.

### POMP: iterated filtering diagnostics
- **Weak identifiability** (spread in parameter trace plots even as loglik converges) is expected and is not a problem: "Weak identifiability leads to variability in parameter estimates even when the maximized loglik is well defined. This is not a problem, just a fact we have discovered." (Ch 15, p35)
- What to look for in trace plots: the loglik panel should be **consistently converging** upward across runs. Parameter panels may show spread — that is acceptable.
- rw.sd = 0.02 on log/logit scale is the standard course perturbation size for parameters estimated on a transformed scale. (Ch 15, p31)
- cooling.fraction.50 = 0.5 is the standard (perturbations halved after 50 mif2 iterations). (Ch 15, p31-32)

### POMP: profile likelihood
- Coarse profile plots are acceptable if the profile shape and CI are visible.
- Course standard number of profile points: 5 (run_level=2) or 30 (run_level=3). (Ch 16, p56)
- The target parameter is NOT perturbed in mif2 during profile computation. (Ch 16, p57)
- The profile is the upper envelope of multiple optimization runs — some scatter below the envelope is normal.

### POMP: benchmark comparison
- Benchmark comparison (POMP vs ARMA/ARIMA) is encouraged but **not required**. Absence alone is not a flaw.
- Losing to ARMA is not automatically a failure: "The aim of mechanistic modeling here is not to beat non-mechanistic models, but it is comforting that we're competitive with them." (Ch 16, p52)
- An IID (negative binomial) model provides the weakest meaningful benchmark. A mechanistic model with likelihood far below even the IID fit suggests something is fundamentally wrong.
- "Sometimes the mechanistic model does not beat simple benchmark models. That does not necessarily mean the mechanistic model is entirely useless... If the mechanistic model fits disastrously compared to the benchmark, our model is probably missing something important." (Ch 17)
- **AIC is not directly comparable across ARIMA and POMP models** (different likelihood scales, data transformations). Flag if students treat AIC as directly comparable without discussion.

### POMP: compartment model implementation
- Euler method is the **standard course approach** for stochastic compartment models. Do not flag its use. (Ch 13) Quote: "Euler's method extends naturally to stochastic models, both continuous-time Markov chains models and SDE models."
- Three stochastic Euler variants are all acceptable: Poisson, Binomial, or Binomial with exponential transition probabilities. The third (`1 - exp(-rate * dt)`) is preferred but all three are valid. (Ch 13, p24)
- Do not flag Euler approximation error as a flaw. Quote: "Close approximation of the numerical solutions to a continuous-time model is less important than it may at first appear." (Ch 13)
- Initial conditions can be treated as fixed or as estimated parameters — both are acceptable. Parameterizing initial compartments as fractions of total population is the course standard. (Ch 16)
- Negative values of R (recovered) in a polio-type model can arise from population model discrepancies and are described as "not a fatal flaw" in course notes. (Ch 16, p18)

### POMP: model specification
- Observable data may have non-Markovian structure even when the latent process is Markovian — this is expected and not an error. (Ch 11)
- Time-homogeneous measurement models are the default; time-varying is acceptable if justified.

### Forecasting
- Point forecasts are acceptable when uncertainty is not the primary question. The course standard is that probabilistic forecasts are preferred but not mandatory.
- Simulation-based forecasts using the fitted model are the standard POMP approach; do not require analytical forecast intervals.

### Model comparison
- `pomp` package is the course standard; do not flag its use.
- **Likelihoods from different model classes (ARMA, POMP, regression, GLM) ARE directly comparable** for the same data — they are all functions of the same observed data. Students are expected to compare across model classes. (MT2 Q4-01)

### Diagnostics
- ARIMA: ACF/PACF + Ljung-Box is standard.
- POMP: simulation-based diagnostics are standard. Formal GOF tests not required.
- Low effective sample size (ESS) in the particle filter does not automatically indicate a model problem — it can also arise when the model fits well but measurement error is small relative to process noise (particles spread by rprocess, few survive dmeasure). Context matters. (MT2 Q2-03)

### Uncertainty
- Profile-based CIs for POMP parameters are expected and appropriate.
- CI from Fisher information / Hessian is only valid for clean, analytical likelihoods — not for noisy particle filter likelihoods.

---

## Genuine review points (do flag these)

These are real issues worth raising despite the course context:

**POMP:**
- Single particle filter run reported without MC variability (no replicated pfilter)
- Profile likelihood with too few points to identify the maximum or CI
- CI from Hessian of noisy particle filter likelihood (invalid — must use profile)
- mif2 loglik used directly for inference without replicated pfilter re-evaluation
- Missing convergence diagnostics for iterated filtering (no trace plots shown)
- Biological parameter interpretation without identifiability check
- Compartment model that violates conservation of individuals (compartments don't sum to population)
- Measurement model where observations depend on past or future observations, not only on current latent state (violates conditional independence requirement)
- When POMP model fits substantially worse than benchmark (large loglik gap), the right response is to revise the model structure — not simply increase Np or Nmif. (MT2 Q4-02)

**ARIMA / classical:**
- AIC comparison between ARIMA and POMP treated as directly valid without noting the scale difference
- Causal language without causal identification
- Forecasts far beyond training data without uncertainty propagation
- AIC table that shows nested model AIC *increasing* by more than ~2 units when adding one parameter — this indicates a numerical optimization failure, not a real model difference (MT1 Q3-01)
