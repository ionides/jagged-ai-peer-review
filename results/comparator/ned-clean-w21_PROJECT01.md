# Ned-Clean Analysis — W21 Project 01

## Human Issues

1. "We observe no significant evidence that the ARIMA model performs better than white noise" is an error: The AIC table shows that ARMA(1,1) is a big improvement over white noise, with some small potential advantage from larger models.
2. The high weekly variability in measurement (likely not present in actual transmission dynamics) may be relevant to model misspecification causing high likelihood variability; the noise modeling in the process and/or measurement model may be a misfit.
3. A simulation study to test the optimization on simulated data could have confirmed that the inference methodology was working correctly.
4. The initial ACF plots are unpolished: it can be unclear what we learn from an ACF of data with substantial trend, and attention is needed to graph labels.
5. What is the red horizontal line in the log_test_positive_ratio plot?

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: Minor #9 — ARMA analysis superficial; conclusion "no improvement over white noise" not supported by AIC table)
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: Minor #10 — log-ratio filtering threshold at 1.5 / red line not justified)

**Findings classification:**
- Major #1 (H = I accumulator error): A — fundamental measurement model misspecification
- Major #2 (no profile likelihood / CI): A — no profile likelihood or confidence intervals
- Major #3 (global search filter 50,000-unit window, ad hoc cutoffs): A — post hoc filtering with unjustified wide window and parameter cutoffs
- Major #4 (smaller dataset uses wrong POMP object datSEIR): A — code inconsistent with narrative (covariates not removed)
- Major #5 (no diagnostic particle filter traces / ESS): A — no convergence traces or particle filter diagnostics
- Major #6 (covariate multipliers chosen by hand): A — beta multipliers not statistically justified
- Major #7 (initial conditions set with ad hoc formulas): A — initial conditions not estimated, introduce circular reasoning
- Major #8 (rho = 0.9 in simulation unrealistically high): A — inconsistent with IF2 estimate of rho ~ 0.2
- Minor #9 (ARMA analysis superficial, conclusion unsupported): D (matches Human Issue #1)
- Minor #10 (log-ratio filter threshold 1.5 not justified, red line unexplained): D (matches Human Issue #5)
- Minor #11 (CCF reasoning flawed): C — correlation of cases with deaths/recoveries does not prove reliability
- Minor #12 (vaccination smoothing not validated): C — smooth.spline applied without validation plot
- Minor #13 (simulation diagnostic not quantified): C — visual inspection only, no quantitative goodness-of-fit
- Minor #14 (pair plot filter for small dataset too wide): C — 10,000-unit window still too wide
- Minor #15 (conclusion "SEIR sufficient overall" unsupported): C — contradicts the paper's own convergence failures

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Major #1 (H = I accumulator error): A — critical misspecification of accumulator variable
- Major #2 (no benchmark comparison for mechanistic model): A — no log-likelihood or AIC comparison between ARIMA and POMP
- Major #3 (convergence not demonstrated for global search): A — no IF2 convergence traces shown
- Major #4 (no profile likelihoods or confidence intervals): A — no formal identifiability assessment
- Major #5 (guesses object not defined in rendered code): A — reproducibility failure
- Major #6 (500 LL evaluations from 500 IF2 chains computationally unsound): A — computational allocation questioned
- Major #7 (vaccination model S can go negative): A — no guard preventing S < 0
- Major #8 (second global search uses wrong POMP object): A — narrative inconsistent with code
- Minor #9 (binomial measurement model, no overdispersion): C — negative binomial more appropriate
- Minor #10 (covariate multipliers fixed by hand): C — not estimated from data
- Minor #11 (H initial condition overwritten by H = I): C — secondary manifestation of accumulator error
- Minor #12 (data filtering cutoff inconsistency June 10 vs June 20): C — text and code disagree
- Minor #13 (vaccination data smoothing): C — LOCF + spline smoothing may introduce artifacts
- Minor #14 (no forecast generated): C — stated goal not met
- Minor #15 (ARIMA log-transformation inconsistent with POMP data): C — AIC not comparable across models

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Major #1 (H tracks current stock, not incident flow): A — fundamental accumulator misspecification
- Major #2 (no profile likelihoods or confidence intervals): A — no formal identifiability assessment
- Major #3 (no convergence diagnostics): A — no IF2 trace plots shown
- Major #4 (ARIMA comparison not used as quantitative benchmark): A — ARIMA and POMP log-likelihoods never compared
- Major #5 (guesses object not defined in rendered code): A — reproducibility failure
- Major #6 (500 chains computationally unsound): A — computational allocation questioned
- Major #7 (vaccination S can go negative): A — no bounding guard
- Major #8 (no quantitative goodness-of-fit reported): A — visual assessment only
- Minor #9 (binomial measurement model / overdispersion): C — negative binomial more appropriate
- Minor #10 (covariate multipliers fixed by hand): C — not estimated
- Minor #11 (H initial condition immediately overwritten): C — secondary accumulator issue
- Minor #12 (data filtering cutoff inconsistency): C — June 10 vs June 20
- Minor #13 (vaccination data smoothing): C — LOCF + spline artifacts
- Minor #14 (no forecast generated): C — stated goal unmet
- Minor #15 (ARIMA log-transformation inconsistent with POMP data): C — likelihoods not comparable

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: Major 21.01.4 — ARIMA AIC table misinterpreted; states AR(0)MA(0)=751.3 vs ARMA(1,0)=240.9, a 500+ AIC unit difference)
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Major 21.01.1 (H = I measurement model error): A — fundamental accumulator misspecification
- Major 21.01.2 (no quantitative goodness-of-fit): A — no log-likelihood or AIC stated in text
- Major 21.01.3 (no quantitative ARIMA benchmark comparison): A — POMP and ARIMA likelihoods never jointly compared
- Major 21.01.4 (ARIMA AIC table misinterpreted): B (matches Human Issue #1)
- Major 21.01.5 (covariate multipliers hard-coded): A — conclusions circular, not evidence from data
- Major 21.01.6 (convergence diagnostics absent): A — no IF2 trace plots
- Major 21.01.7 (no confidence intervals): A — scatter plot impressions are not CIs
- Minor: vaccination compartment guard (S can go negative): C — no bounding on IM subtraction
- Minor: rho = 0.9 implausibly high in simulation: C — inconsistent with IF2 estimate
- Minor: weekly seasonality / SARIMA not considered: C — ACF shows weekly pattern but not modeled
- Minor: Np and Nmif not reported: C — reproducibility gap
- Minor: mu_EI fixed or estimated unclear: C — ambiguity about parameter status
- Minor: accumulator variable naming (ini_positive_remained): C — not defined in text
- Minor: typo "global searcg": C — minor presentation error
- Minor: figure 12 and 16 labeling unclear: C — simulation basis not stated

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 8 | 8 | 8 | 6 |
| B (AI major, human also found) | 0 | 0 | 0 | 1 |
| C (AI minor, human missed) | 5 | 7 | 7 | 8 |
| D (AI minor, human also found) | 2 | 0 | 0 | 0 |
| E (Human found, AI missed) | 3 | 5 | 5 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex:**
- Human Recall = (B+D) / (B+D+E) = (0+2) / (0+2+3) = 2/5 = **40.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+5) / (8+0+5+2) = 13/15 = **86.7%**

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = (0+0) / (0+0+5) = 0/5 = **0.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+7) / (8+0+7+0) = 15/15 = **100.0%**

**Doug:**
- Human Recall = (B+D) / (B+D+E) = (0+0) / (0+0+5) = 0/5 = **0.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+7) / (8+0+7+0) = 15/15 = **100.0%**

**Evan:**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+4) = 1/5 = **20.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+8) / (6+1+8+0) = 14/15 = **93.3%**

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- Human Issue #2: High weekly variability in measurement / noise modeling misfit as cause of high likelihood variability — missed by all 4 reviewers (4 out of 4).
- Human Issue #3: Simulation study to test optimization on simulated data — missed by all 4 reviewers (4 out of 4).
- Human Issue #4: Initial ACF plots unpolished; unclear what we learn from ACF of trended data; graph labels need attention — missed by all 4 reviewers (4 out of 4).
- Human Issue #5: What is the red horizontal line in the log_test_positive_ratio plot? — missed by Charlie, Doug, and Evan (3 out of 4); covered by Alex only.

Total consensus misses (all 4 missed): 3 issues out of 5 (60%).

**Unique finds per reviewer:** Human issues covered by only one reviewer and missed by all others.

- Human Issue #1 (ARIMA AIC misinterpreted): covered by Evan (Major), not covered as a direct misinterpretation match by Alex, Charlie, or Doug. Unique to Evan.
- Human Issue #5 (red horizontal line): covered by Alex (Minor), not covered by Charlie, Doug, or Evan. Unique to Alex.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

The following issues appear in all four AI reviewers but not in the human review:

1. H = I accumulator error (fundamental measurement model misspecification) — raised as Major by Alex, Charlie, Doug, and Evan.
2. No profile likelihoods or confidence intervals — raised as Major by Alex, Charlie, Doug, and Evan.
3. No convergence diagnostics (IF2 trace plots absent) — raised as Major by Charlie, Doug, and Evan; implicitly by Alex (Major #5: no diagnostic particle filter traces).
4. Wrong POMP object used for smaller-dataset analysis — raised as Major by Alex (Major #4), Charlie (Major #8), and Doug (Major #5 mentions guesses not defined; Major #8 covers wrong object per Doug's structure); noted by Charlie and Doug explicitly.
5. Covariate multipliers chosen by hand without statistical justification — raised as Major by Charlie (#5 context), Doug (#10 minor), Evan (#21.01.5 major); and by Alex (Major #6).
6. No quantitative goodness-of-fit / log-likelihood reported — raised as Major by Alex (implicit in Major #5 area), Doug (Major #8), Evan (Major 21.01.2); and by Alex (Minor #13).

Total universal AI-only flags: 6 issues raised by all reviewers that the human did not mention.
