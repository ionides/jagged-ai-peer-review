# Ned-Clean Analysis — W21 Project 09

---

## Human Issues

1. Basic SIR/SEIR models with fixed parameters cannot explain the multiple peaks observed in the pandemic. Rather than fitting an inadequate model in different ways, the model should be improved (e.g., varying transmission rates to model social distancing mandates).
2. Beta and gamma parameters are mentioned but not defined.
3. The plot of "recovered" exactly matches "new cases" — something strange may be going on, and the project does not explain how "recovered" is defined.
4. For the ODE analysis, the fitted cumulative incidence is not increasing — there is some error.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Measurement Model Is Internally Inconsistent — H accumulates recoveries but is used as proxy for new cases, conflating the two quantities")
- Human Issue #4: covered (matched by finding: "Fitting Cumulative Cases Instead of Incidence — fitting cumulative data with RSS is methodologically wrong")

**Findings classification:**
- Finding 1 (POMP Model Essentially Abandoned): A — POMP mif2 and particle filter section entirely commented out; no likelihood-based results shown
- Finding 2 (No Likelihood-Based Inference): A — no log-likelihood values, standard errors, or principled basis for parameter selection
- Finding 3 (ODE SIR Replaces Rather Than Supplements POMP): A — deterministic RSS-based ODE bypasses the stochastic POMP framework
- Finding 4 (Measurement Model Internally Inconsistent): B — H accumulates recoveries but rmeasure uses it for new cases; conflates flows (matches Human Issue #3)
- Finding 5 (`s` Parameter in `dmeasure` Undefined): A — `s` not declared in statenames or paramnames; would cause runtime error
- Finding 6 (Fitting Cumulative Cases Instead of Incidence): B — ODE fitted to cumulative cases rather than incident new cases, methodologically flawed (matches Human Issue #4)
- Finding 7 (No Parameter Uncertainty Quantification): A — no confidence intervals, profile likelihoods, or standard errors for any model
- Finding 8 (Particle Count and MIF Settings Inadequate): C — Np=20 too few particles; rw.sd values on inconsistent scales
- Finding 9 (ACF Interpretation Incorrect): C — text claims "no clear lag pattern" but ACF shows strong persistent autocorrelation
- Finding 10 (ARIMA Model Selection Not Justified): C — d=2 not justified; MA roots computed for only 2 of 4 MA terms
- Finding 11 (SIR Model Does Not Include Death Compartment): C — death compartment promised in introduction but absent from implementation
- Finding 12 (Recovery Rate Derivation Informal): C — mu_IR fixed by lag2.plot inspection without formal cross-correlation or uncertainty
- Finding 13 (Initial Conditions Biologically Implausible): C — eta=0.05 implies 5–7% of Utah already recovered at pandemic start
- Finding 14 (No Global Search for Parameters): C — only local searches (commented out); no parameter box or global optimization
- Finding 15 (Presentation and Writing Quality Issues): C — multiple typos, incorrect legend mapping, missing differencing operator in ARIMA equation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Severe dmeasure/rmeasure distributional mismatch — H accumulates recoveries (dN_IR) not new infections (dN_SI), so rmeasure tracks wrong process")
- Human Issue #4: covered (matched by finding: "Deterministic ODE SIR fitted by RSS on cumulative cases — I(t) is prevalence, cumulative cases is monotonically increasing incidence sum; these are different quantities")

**Findings classification:**
- Finding 1 (POMP inference entirely absent): A — all mif2/pfilter code commented out; no log-likelihood or convergence diagnostics
- Finding 2 (Severe dmeasure/rmeasure mismatch): B — dmeasure uses negative binomial with undefined `s` and `theta`; rmeasure uses binomial with H (recoveries); H tracks wrong process (matches Human Issue #3)
- Finding 3 (Deterministic ODE by RSS on cumulative cases): B — ODE I(t) fitted to cumulative incidence, wrong quantity; no likelihood-based uncertainty (matches Human Issue #4)
- Finding 4 (No benchmark comparison): A — no quantitative comparison of ARIMA vs. SIR log-likelihoods
- Finding 5 (No quantitative goodness-of-fit): A — no RSS, R-squared, AIC, or log-likelihood reported for mechanistic model
- Finding 6 (Cumulative vs. incidence mismatch): A — POMP object uses daily new cases; ODE uses cumulative cases; different observable (Human Issue #4 already matched to Finding 3)
- Finding 7 (Parameter identifiability not assessed): A — no profile likelihoods or confidence intervals for any parameter
- Finding 8 (Recovery rate ad hoc calibration): A — mu_IR fixed by cross-correlation without uncertainty propagation; should be estimated via likelihood
- Finding 9 (No model diagnostics): A — no conditional log-likelihood plots, no ESS monitoring, no residual analysis for SIR
- Finding 10 (Forecast methodology absent): A — no probabilistic forecasts generated from filtering distribution
- Finding 11 (ARIMA d=2 without justification): C — d=2 fixed throughout grid search without stationarity tests
- Finding 12 (`s` undeclared in dmeasure): C — `s` not in statenames or paramnames; defaults to zero in C, breaking negative binomial
- Finding 13 (Initial conditions biologically implausible): C — R = round(N*(1-eta)) initializes ~95% of Utah as recovered in March 2020
- Finding 14 (ACF interpretation incorrect): C — text concludes "no clear lag pattern" but ACF shows strong persistent autocorrelation
- Finding 15 (Typographical errors): C — multiple misspellings throughout

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Model specification — observable mismatch: I(t) is prevalence but fitted to cumulative cases; cumulative curve monotonically increases while I(t) rises and falls")

**Findings classification:**
- Major Issue 1 (Inference methodology — no optimization criterion): A — deterministic SIR parameters described as "best" but no objective function, criterion, or algorithm specified
- Major Issue 2 (Observable mismatch — I(t) vs. cumulative cases): B — I(t) plotted against cumulative cases; prevalence conflated with monotonically increasing cumulative count (matches Human Issue #4)
- Major Issue 3 (POMP abandoned without diagnostic evidence): A — no particle count, IF2 iterations, trace plots, or measurement model stated
- Major Issue 4 (No quantitative comparison): A — no log-likelihood or AIC comparison between ARIMA and SIR models
- Major Issue 5 (Double-differencing without transformation): A — d=2 on skewed count data without log/sqrt transform or unit-root test
- Minor (Ljung-Box contradiction): C — p-value 8.578e-08 rejects white noise but text characterizes fit as "okay"
- Minor (ACF mischaracterization): C — all ACF lags near 1.0 indicates non-stationarity but text says "no clear lag pattern"
- Minor (mu_IR sensitivity not assessed): C — recovery rate 1/15 fixed using cross-correlation; sensitivity to 1/10 vs. 1/20 not examined
- Minor (Initial conditions unspecified): C — I(0) not stated for either model
- Minor (S(t) vs. cumulative discrepancy): C — S declines by ~2.25M but only ~400K cumulative cases observed; discrepancy not discussed
- Minor (ARIMA notation inconsistency): C — beta and phi used inconsistently for AR coefficients; standard notation not followed
- Minor (No vaccination compartment): C — vaccination began in late 2020/early 2021 but no vaccinated compartment modeled
- Minor (Reproducibility of deterministic SIR): C — SIR adapted from statsandr.com but specific functions not documented
- Minor (Writing quality): C — multiple typographical errors throughout

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "21.09.B — Model specification observable mismatch: I(t) is prevalence, plotting against cumulative cases is biologically incorrect; the 'cycle' in SIR curves is an artifact of this mismatch")

**Findings classification:**
- 21.09.A (Inference methodology — no optimization criterion): A — deterministic SIR parameters called "best" but no objective function specified; tutorial-based ad hoc calibration
- 21.09.B (Observable mismatch — I(t) vs. cumulative cases): B — I(t) is prevalence, cumulative cases is monotonically increasing; the visible "cycle" is an artifact of the mismatch (matches Human Issue #4)
- 21.09.C (POMP abandoned without diagnostic evidence): A — no Np, Nmif, trace plots, or measurement model documented; failure not diagnosable
- 21.09.D (No quantitative comparison): A — ARIMA has AIC 4269.03 but no comparable metric for SIR; conclusion of SIR superiority unsubstantiated
- 21.09.E (Double-differencing without transformation): A — d=2 on right-skewed count-like data without variance stabilization or unit-root test
- Minor (Ljung-Box contradiction): C — p-value 8.578e-08 rejects white noise; text says "okay fit"
- Minor (ACF mischaracterization): C — ACF near 1.0 at many lags indicates non-stationarity; text says "no clear lag pattern"
- Minor (mu_IR sensitivity): C — recovery rate 1/15 fixed; sensitivity to alternative values not reported
- Minor (Initial conditions unspecified): C — I(0) not stated for pomp or deterministic SIR
- Minor (S(t) vs. cumulative discrepancy): C — S declines by ~2.25M but only ~400K cumulative cases; factor-of-5 discrepancy not discussed
- Minor (ARIMA notation): C — beta and phi used inconsistently for AR vs. MA coefficients
- Minor (No vaccination compartment): C — vaccination not modeled despite beginning late 2020
- Minor (Reproducibility of deterministic SIR): C — external tutorial source not fully documented
- Minor (Writing quality): C — multiple typographical errors throughout

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 8 | 4 | 4 |
| B (AI major, human also found) | 2 | 2 | 1 | 1 |
| C (AI minor, human missed) | 8 | 5 | 9 | 9 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 2 | 2 | 3 | 3 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+2) = 2/4 = **0.50**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+8) / (5+2+8+0) = 13/15 = **0.87**

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+2) = 2/4 = **0.50**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+5) / (8+2+5+0) = 13/15 = **0.87**

**Doug**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+3) = 1/4 = **0.25**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+9) / (4+1+9+0) = 13/14 = **0.93**

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+3) = 1/4 = **0.25**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+9) / (4+1+9+0) = 13/14 = **0.93**

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- **Human Issue #1** (Fixed-parameter SIR inadequacy for multiple peaks; model improvement needed): missed by Alex, Charlie, Doug, Evan
- **Human Issue #2** (Beta and gamma parameters not defined): missed by Alex, Charlie, Doug, Evan

**Count: 2 out of 4 human issues (50%) were missed by every reviewer.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3 (Recovered plot matches new cases): covered only by Alex and Charlie — NOT unique to a single reviewer.
- Human Issue #4 (Fitted cumulative incidence not increasing): covered by Alex, Charlie, Doug, and Evan — not unique.

No human issue was covered by exactly one reviewer and missed by all others.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- **POMP model abandoned / no likelihood-based inference**: raised as Major by Alex (Findings 1–2), Charlie (Finding 1), Doug (Major Issue 3), Evan (21.09.C) — all four reviewers flagged this.
- **Deterministic ODE replaces POMP / RSS instead of likelihood**: raised as Major by Alex (Finding 3), Charlie (Finding 3), Doug (Major Issue 1), Evan (21.09.A) — all four reviewers flagged this.
- **No quantitative comparison between mechanistic and statistical models**: raised as Major by Charlie (Finding 4), Doug (Major Issue 4), Evan (21.09.D); Alex addresses this through Finding 2 (no likelihood) — flagged by all four.
- **Double-differencing (d=2) without transformation or unit-root test**: raised as Major by Doug (Major Issue 5) and Evan (21.09.E); raised as Minor by Alex (Finding 10) and Charlie (Finding 11) — flagged by all four, though as Minor by Alex and Charlie.

Strictly universal-major (all four classify as Major):
- POMP abandoned / no inference: 1 issue
- Deterministic ODE by RSS / ad hoc calibration: 1 issue
- No quantitative model comparison: 1 issue

**Count: 3 issues raised as Major by all four reviewers that the human did not mention.**
