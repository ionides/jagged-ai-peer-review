# Comparator Analysis — W21 Project 09

---

## Human Issues

1. Basic SIR/SEIR models with fixed parameters simply cannot explain the multiple peaks observed in the pandemic. Rather than looking for different ways to fit an inadequate model, one could work on improving the model. Varying transmission rates (e.g., to model varying social distancing mandates) would be one way to start on that. Modeling multiple COVID waves is not easy: see Projects 13 and 15 for successful approaches.

2. $\beta$ and $\gamma$ parameters are mentioned at some point, but not defined.

3. The plot of "recovered" exactly matches "new cases". Something strange may be going on. The project does not explain how "recovered" is defined.

4. For the ODE analysis, the fitted cumulative incidence is not increasing. Clearly, there is some error.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Measurement Model Is Internally Inconsistent — H accumulates recoveries but is used to model new cases, conflating the two quantities")
- Human Issue #4: missed

**Findings classification:**
- Finding 1 (POMP Model Abandoned): A — entire particle-filter section commented out; no pfilter or mif2 results shown
- Finding 2 (No Likelihood-Based Inference): A — no log-likelihood values, no standard errors, no model comparison possible
- Finding 3 (ODE SIR Replaces Rather Than Supplements POMP): A — deterministic deSolve/RSS approach bypasses stochastic POMP framework
- Finding 4 (Measurement Model Internally Inconsistent): B — H accumulates recoveries but measurement produces new-case labels; conflates recoveries and new cases (matches Human Issue #3)
- Finding 5 (`s` Parameter in dmeasure Undefined): A — lowercase `s` not in statenames or paramnames; would cause runtime error
- Finding 6 (Fitting Cumulative Cases Instead of Incidence): A — ODE fitted against cumulative counts rather than daily incidence; RSS autocorrelation problem
- Finding 7 (No Parameter Uncertainty Quantification): A — no confidence intervals, profile likelihoods, or standard errors in any section
- Finding 8 (Particle Count and MIF Settings Inadequate): C — Np=20 too few for reliable likelihood; rw.sd values not calibrated
- Finding 9 (ACF Interpretation Incorrect): C — strong autocorrelation misread as "no clear lag pattern"
- Finding 10 (ARIMA Model Selection Not Justified): C — d=2 not tested; MA roots computed for only 2 of 4 MA terms
- Finding 11 (SIR Model Does Not Include Death Compartment): C — stated model includes deaths but neither SIR implementation does
- Finding 12 (Recovery Rate Derivation Informal): C — mu_IR fixed by visual lag2.plot inspection rather than estimated
- Finding 13 (Initial Conditions Biologically Implausible): C — eta implies 5–7% of Utah already recovered at near-zero cumulative case date
- Finding 14 (No Global Search for Parameters): C — only local searches (commented out); no parameter box or global optimization
- Finding 15 (Presentation and Writing Quality Issues): C — typos, legend mismatch, ARIMA equation missing differencing operator, hidden summary chunk

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Accumulator variable H tracks recoveries, not new infections — wrong observable linked to data")
- Human Issue #4: covered (matched by findings: "Deterministic ODE model fitted by RSS — fits cumulative cases to I compartment, different quantities" and "SIR model applied to cumulative cases rather than incident cases in the deterministic section")

**Findings classification:**
- Finding 1 (POMP analysis entirely commented out): A — no inference performed; core POMP deliverable missing
- Finding 2 (Measurement model mismatch between dmeasure and rmeasure): A — dmeasure uses negative binomial on susceptible compartment s; rmeasure uses binomial on H; fundamentally different distributions
- Finding 3 (Deterministic ODE fitted by RSS, not likelihood): B — fits cumulative cases to I compartment, conceptually incorrect; addresses same root cause as Human Issue #4
- Finding 4 (No log-likelihood or AIC reported for any model): A — visual-only comparison; no quantitative goodness-of-fit
- Finding 5 (Accumulator H tracks recoveries, not new infections): B — H incremented by dN_IR instead of dN_SI; wrong observable linked to data (matches Human Issue #3)
- Finding 6 (No convergence diagnostics for iterated filtering): A — no trace plots, no replicated searches; mif2 code commented out
- Finding 7 (No profile likelihoods — parameter identifiability not assessed): A — parameters hand-tuned; no confidence intervals possible
- Finding 8 (SIR model applied to cumulative cases rather than incident cases): B — I(t) is prevalence, cumulative cases is monotonically increasing incidence sum; misspecification explains non-increasing fitted curve (matches Human Issue #4)
- Finding 9 (theta missing from paramnames): C — theta undefined in POMP object; would silently break negative binomial evaluation
- Finding 10 (ARIMA with d=2 without justification): C — double differencing unjustified without formal unit root test or AIC comparison across d values
- Finding 11 (ARIMA(5,2,4) residual ACF shows correlated lags): C — Ljung-Box result not discussed; no remedial action taken
- Finding 12 (Recovery rate fixed via cross-correlation, not estimated): C — mu_IR fixed externally; confounded by seven-day smoothing
- Finding 13 (Initial conditions partially misspecified — R starts near N): C — with eta=0.06, nearly entire population starts recovered, biologically implausible for March 2020
- Finding 14 (s in dmeasure ambiguous and likely wrong): C — lowercase s not a declared state; likely zero or NA, breaking dnbinom evaluation
- Finding 15 (No benchmark comparison between ARIMA and POMP log-likelihoods): C — implied comparison never made quantitatively

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by findings: "ODE SIR fitted by RSS — biologically incorrect to match I to cumulative cases" and "model fitted to cumulative cases while POMP object observes daily new cases — I rises and falls while cumulative continues to rise")

**Findings classification:**
- Finding 1 (POMP inference absent — mif2/pfilter all commented out): A — no converged likelihood, parameters not estimated by IF2
- Finding 2 (dmeasure/rmeasure distributional mismatch): A — dnbinom in dmeasure vs rbinom in rmeasure; undeclared s and theta
- Finding 3 (ODE SIR by RSS on cumulative cases — not POMP): B — fitting I(t) to cumulative data is biologically incorrect; I rises and falls while cumulative is monotone (matches Human Issue #4)
- Finding 4 (no benchmark comparison between ARIMA and mechanistic model): A — visual claim unsupported by quantitative log-likelihood comparison
- Finding 5 (no quantitative goodness-of-fit for mechanistic model): A — no RSS value, R-squared, AIC, or log-likelihood reported
- Finding 6 (POMP observes daily new cases but ODE fitted to cumulative cases): B — the red I curve rises and falls while blue cumulative points continue to rise, demonstrating the mismatch (matches Human Issue #4)
- Finding 7 (parameter identifiability and uncertainty not assessed): A — no profile likelihoods, CIs, or SEs for beta, gamma, or rho
- Finding 8 (recovery rate estimated by lagged cross-correlation — ad hoc calibration): A — noisy cross-correlation used as point estimate without uncertainty propagation
- Finding 9 (no model diagnostics presented): A — no conditional log-likelihood plots, no ESS monitoring, no residual analysis
- Finding 10 (forecast methodology absent): A — conclusion based on visual curve inspection, not formal forecast
- Finding 11 (ARIMA d=2 fixed without justification): C — over-differencing possible; no stationarity tests reported
- Finding 12 (parameter s undeclared in dmeasure — defaults to zero in C): C — proximate cause of particle filter crash
- Finding 13 (biologically implausible initialization — 95% of population initialized as recovered): C — contradicts March 2020 COVID-19 context
- Finding 14 (ACF interpretation vague and incorrect): C — sustained autocorrelation misread as no pattern
- Finding 15 (prose typographical and grammatical errors): C — multiple misspellings throughout

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "21.09.B — observable mismatch, I(t) plotted against cumulative cases, identifying a fundamental error in the SIR fit to cumulative incidence")

**Findings classification:**
- 21.09.A: A — no optimization criterion for SIR parameters; ad hoc calibration rather than statistical inference
- 21.09.B: B — I(t) conflated with cumulative cases; SIR cycle is artifact of mismatch, not a genuine fit (matches Human Issue #4)
- 21.09.C: A — pomp model abandoned without diagnostic evidence (no particle count, no IF2 iterations, no trace plots, no model equations)
- 21.09.D: A — no quantitative comparison between mechanistic and statistical models
- 21.09.E: A — double-differencing skewed count data without variance-stabilizing transformation; no unit-root test reported
- Ljung-Box contradiction: C — p-value strongly rejects white noise but text calls it "an okay fit"
- ACF mischaracterization: C — ACF near 1.0 indicates non-stationarity; text says "no clear lag pattern"
- mu_IR sensitivity: C — recovery rate 1/15 days fixed by cross-correlation; sensitivity to alternative values not explored
- Initial conditions unspecified: C — I(0) not stated for pomp or deterministic SIR
- S(t) vs. observed discrepancy: C — S(t) implies ~2.25M infections vs. ~400K observed, suggesting poor calibration
- ARIMA notation: C — beta and phi used inconsistently for AR and MA coefficients
- No vaccinated compartment: C — vaccination begun by late 2020 but no vaccinated compartment included in SIR
- Reproducibility of deterministic SIR: C — code adapted from external tutorial without full parameter documentation
- Writing quality: C — multiple typographical errors throughout

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
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 5 | 8 | 4 |
| B (AI major, human also found) | 1 | 3 | 2 | 1 |
| C (AI minor, human missed) | 8 | 7 | 5 | 9 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 3 | 2 | 3 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 3 | 1/4 = 25% | 6 | 8 | 14/15 = 93% |
| Charlie | 3 | 0 | 2 | 2/4 = 50% | 5 | 7 | 12/15 = 80% |
| Doug | 2 | 0 | 3 | 1/4 = 25% | 8 | 5 | 13/15 = 87% |
| Evan | 1 | 0 | 3 | 1/4 = 25% | 4 | 9 | 13/14 = 93% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Basic SIR/SEIR models with fixed parameters simply cannot explain the multiple peaks observed in the pandemic. Rather than looking for different ways to fit an inadequate model, one could work on improving the model. Varying transmission rates (e.g., to model varying social distancing mandates) would be one way to start on that. Modeling multiple COVID waves is not easy: see Projects 13 and 15 for successful approaches. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: $\beta$ and $\gamma$ parameters are mentioned at some point, but not defined. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 4 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
