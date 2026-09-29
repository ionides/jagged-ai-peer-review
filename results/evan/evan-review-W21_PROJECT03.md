# Final AI Review: Investigation of Vaccination Effect on Covid-19 in California
## (w21 Project 03)

---

## Overall Assessment

This project tackles a timely and well-motivated question — whether vaccination measurably slowed COVID-19 transmission in California — through a sequence of three compartment models (SIR, SIRV with estimated vaccination rate, SIRV with externally modeled vaccination trajectory) implemented in pomp with IF2 inference. The progression across model variants and the use of profile likelihood for vaccine-efficacy parameter sigma are genuine strengths. However, several issues substantially undermine the reliability of the conclusions. Most critically, all computations are run at the lowest possible level (Np=100, Nmif=10, Neval=2), making every reported log-likelihood, parameter estimate, and identifiability statement potentially spurious. The forecast that the pandemic would end before July 2021 is drawn from a simulation that passes the hand-picked starting parameter vector rather than the MLE estimates — a coding error that invalidates the primary policy claim. Additionally, the accumulator variable H tracks recoveries rather than new infections across all three models, creating a systematic conceptual mismatch with the observed data. These issues need to be resolved before the main conclusions can be trusted.

---

## Key Strengths

**ID: 21.03.9 — Correct likelihood aggregation**
The analysis consistently applies logmeanexp over replicated pfilter calls rather than averaging log-likelihoods directly. This is methodologically correct and reflects good practice.

**ID: 21.03.10 — Quantitative multi-model comparison**
Three model variants are compared using reported log-likelihoods (-190 for SIR, -182 for SIRV1, -190 for SIRV2), providing a basis for quantitative model assessment. Profile likelihood is computed for the key vaccine-efficacy parameter sigma, and the authors correctly recognize weak identifiability from the profile shape.

**ID: 21.03.S1 — Thoughtful model progression**
The sequence from SIR to SIRV (estimated vaccination rate) to SIRV (externally constrained vaccination trajectory) represents a logical scientific progression. Integrating the quadratic vaccination model as a covariate is a reasonable approach to handling a known external forcing.

---

## Major Points

**ID: 21.03.1 — Critically insufficient computation**
Severity: Major

All models are fitted at run_level=1 (Np=100 particles, Nmif=10 IF2 iterations, Neval=2 pfilter replicates). Convergence trace plots (fig_005, fig_010, fig_015) confirm that parameters wander without stabilizing and likelihood traces remain highly erratic across all three models. With Np=100, particle filter likelihoods carry enormous Monte Carlo variance; the reported standard error of 1.54 for the SIRV2 best fit quantifies this unreliability. No conclusion about which parameters are identifiable, which model fits best, or what the vaccine efficacy is can be drawn from these results. The authors should rerun at run_level=3 (Np=5000, Nmif=200, Neval=20, Nlocal=40) and base all conclusions on those results.

**ID: 21.03.2 — No non-mechanistic benchmark comparison**
Severity: Major

No ARMA, ARIMA, or other non-mechanistic baseline is compared against the POMP models. With only 87 observations and a clear downward trend, even a simple AR model would serve as a reference. Without this baseline, there is no way to assess whether the mechanistic models capture structure that a simpler model cannot — a fundamental requirement for justifying the added complexity and interpretive claims of compartment modeling.

**ID: 21.03.3 — Forecast simulation uses starting-guess parameters, not MLE**
Severity: Major

In the prediction section, the pomp simulate call passes the object `params` (the hand-picked starting guess: Beta=0.01, Sigma=0.01, mu_IR=0.04, mu_VR=0.9) rather than `params_maxlik`, which is correctly extracted from the global search results on the preceding line. Consequently, the forecast figures (fig_019, fig_020) and the conclusion that the pandemic would end before July 2021 reflect guessed parameter values rather than fitted estimates. The fix is straightforward: replace `params=params` with `params=params_maxlik` in the simulate call.

**ID: 21.03.4 — Accumulator H tracks recoveries rather than new infections**
Severity: Major

In all three model step functions, the accumulator variable H is incremented by `dN_IR` (the I-to-R transition, i.e., recoveries). The observation model then links daily new reports to H via a Binomial distribution. The data, however, represent daily new confirmed cases, which correspond to new infections entering the system (the S-to-I transition, dN_SI). Linking observations to recoveries introduces a systematic lag and a conceptual mismatch: the model is claiming that what we observe each day is proportional to recoveries, not new infections. If this is an intentional simplification assuming all infections are eventually reported upon recovery, this assumption must be stated and its implications discussed. Otherwise, `H <- H + dN_SI` is the correct formulation.

**ID: 21.03.5 — SIRV1 outperforms SIRV2 in likelihood without explanation**
Severity: Major

The global search reports a best log-likelihood of -182 for SIRV1 and -190 for SIRV2. Since SIRV2 is a more complex model with an additional parameter (mu_VR) and uses external vaccination information, it should fit at least as well as SIRV1. The inferior fit suggests either that the SIRV2 global search is less thorough due to run_level=1 noise, or that the deterministic vaccination covariate constrains the model in a way that reduces fit. This reversal is not acknowledged or discussed. An analysis claiming that SIRV2 is the preferred model must resolve why it achieves a lower maximum likelihood than the simpler SIRV1.

---

## Minor Points

**ID: 21.03.6 — Profile likelihood for sigma: CI cutoff suppressed, too sparse**
Severity: Minor

The code constructs the CI cutoff threshold correctly (`ci.cutoff <- maxloglik - 0.5*qchisq(df=1,p=0.95)`) but then comments out the line that draws it on the profile plot. The profile contains only about 20 points at run_level=1. The result (fig_018) shows a shallow maximum around sigma=0.1 but the authors correctly note weak identifiability. To make this result credible, the CI line should be displayed, more profile points used (>=30 recommended), and the computation should be repeated at higher Np. Suggested action: uncomment the geom_hline line and re-run at run_level=3.

**ID: 21.03.7 — SIRV1 vaccination transition probability may have S-dependence inconsistency**
Severity: Minor

In `sirv1_step`, the S-to-V transition uses `prob=1-exp(-u*S/N*delta.t)`, where the hazard rate u*S/N makes the per-capita vaccination rate depend on S. The mathematical specification states dS/dt = -u*S/N, which gives a per-capita rate of u/N (constant). The code introduces an additional factor of S/N in the rate, effectively making vaccination self-accelerating in S. The intended model should likely use `prob=1-exp(-u/N*delta.t)` or simply `prob=1-exp(-u*delta.t)` depending on how u is defined. Authors should verify consistency between the equations and the code.

**ID: 21.03.M1 — Measurement model uses Binomial; overdispersion not considered**
Severity: Minor

All three models use a Binomial measurement distribution. Daily COVID case reports exhibit substantial day-of-week effects and reporting variability (visible in fig_001), suggesting overdispersion relative to the Binomial. A Negative Binomial measurement model would be more appropriate and is the standard for count data of this type. At minimum, the Binomial assumption should be acknowledged as a simplification.

**ID: 21.03.M2 — EDA is limited; no ACF or log-scale examination**
Severity: Minor

The exploratory analysis shows new cases (fig_001) and the vaccination trajectory (fig_002) but does not examine autocorrelation structure, does not plot on a log scale, and does not check for periodicity (e.g., day-of-week effects). A brief ACF plot of new cases would motivate the time-series modeling approach and help diagnose any residual structure.

**ID: 21.03.M3 — Computational settings hidden from rendered output**
Severity: Minor

The chunk setting `run_level` and all `options_*` parameters uses `include=FALSE`, so the reader cannot verify what settings were used. Given that run_level is the most consequential parameter for the reliability of all results, it should be displayed in the report.

**ID: 21.03.M4 — Minor writing errors**
Severity: Minor

Line 564: "agasinst" should be "against." Line 557: "EXISTING!" appears to be an unintentional editing artifact and should be removed or replaced with "EXCITING!"
