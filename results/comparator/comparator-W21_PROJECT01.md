# Comparator Analysis — W21 Project 01

---

## Human Issues

1. "We observe no significant evidence that the ARIMA model performs better than white noise" is an error: The AIC table shows that ARMA(1,1) is a big improvement over white noise, with some small potential advantage from larger models.

2. The authors identify model misspecification as a likely cause of the high variability when numerically evaluating and maximizing the likelihood. In the time allowed, it is hard to resolve such issues. The high weekly variability in measurement (likely not present in the actual transmission dynamics) may be relevant. Also, perhaps the noise modeling in the process and/or measurement model is a misfit.

3. The project's interpretation of model misspecification issues is reasonable. However, a simulation study to test the optimization on simulated data could have confirmed that the inference methodology was working correctly. Modeling COVID is not easy: see Projects 13 & 15 for a successful approach.

4. The initial ACF plots are unpolished: it can be unclear what we learn from an ACF of data with substantial trend, and attention is needed to graph labels.

5. What is the red horizontal line in the log_test_positive_ratio plot?

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ARMA analysis superficial; conclusion 'no significant evidence ARIMA performs better than white noise' is not supported by the AIC table")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "log-ratio threshold of 1.5 is ad hoc and unjustified — the red line in the plot")

**Findings classification:**
- Finding 1 (H=I accumulator error): A — fundamental measurement model error; accumulator set to prevalence rather than incident infections
- Finding 2 (no profile likelihoods): A — no profile likelihood traces or confidence intervals reported for any parameter
- Finding 3 (ad hoc 5e4 filter window): A — global search results filtered with a 50,000-unit log-likelihood window, effectively no filtering
- Finding 4 (smaller dataset still uses datSEIR): A — "simple SEIR without covariates" claim is false; code still uses covariate-enriched object
- Finding 5 (no mif2 convergence or ESS diagnostics): A — no particle filter effective sample size or log-likelihood convergence plots shown
- Finding 6 (Beta multipliers chosen by hand): A — covariate multipliers on Beta fixed without statistical justification or sensitivity analysis
- Finding 7 (initial conditions not estimated): A — initial compartment sizes set via circular formulas depending on unknown parameters
- Finding 8 (rho=0.9 in simulation): A — simulation uses rho=0.9 while IF2 results suggest rho~0.2; discrepancy never reconciled
- Finding 9 (ARMA analysis superficial): D — conclusion "no significant evidence ARIMA performs better than white noise" not supported by AIC table (matches Human Issue #1)
- Finding 10 (log-ratio threshold 1.5 unjustified): D — ad hoc red line at 1.5 in the log_test_positive_ratio plot is unexplained (matches Human Issue #5)
- Finding 11 (CCF reasoning flawed): C — correlation of positive cases with deaths/recoveries does not establish positive cases as most reliable
- Finding 12 (vaccination smoothing not validated): C — LOCF imputation followed by smooth.spline with defaults; result not plotted against raw data
- Finding 13 (simulation diagnostic not quantified): C — goodness-of-fit assessed only by visual inspection of simulation envelopes
- Finding 14 (small dataset pair plot window too wide): C — smaller-dataset pair plot filters with a 10,000-unit window, still unreasonably wide
- Finding 15 (conclusion unsupported): C — "SEIR model sufficient overall" conclusion contradicted by poor convergence and model misspecification shown in the analysis

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
- Human Issue #2: covered (matched by findings: "Log-likelihood filter of 50,000 units indicates optimization failure" and "Underdispersed binomial measurement model for COVID-19 data")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Major Issue 1 (Missing convergence diagnostics): A — no trace plots, convergence entirely absent
- Major Issue 2 (Measurement model mismatch H=I stock vs flow data): A — H=I applied to incidence data
- Major Issue 3 (LL filter range of 50,000 units): B — catastrophic optimization failure evidenced by huge filter threshold (matches Human Issue #2)
- Major Issue 4 (No absolute log-likelihood reported): A — best log-likelihood never stated
- Major Issue 5 (No profile likelihood for any parameter): A — no profile likelihoods, no CIs
- Major Issue 6 (Second IF exercise contradicts stated purpose): A — uses wrong model object for second global search
- Major Issue 7 (Underdispersed binomial measurement model): B — binomial insufficient for overdispersed COVID data, noise modeling misfit (matches Human Issue #2)
- Minor: Forecast not delivered: C — promised forecast never produced
- Minor: Covariate multipliers not estimated: C — C50 values manually chosen, not estimated
- Minor: No safeguard against negative compartments: C — S can go negative from vaccination term
- Minor: Initial rho = 0.9 biologically implausible: C — 90% detection rate inconsistent with literature
- Minor: No quantitative comparison between ARMA and SEIR: C — SEIR log-likelihood never compared to ARMA baseline
- Minor: guesses object not shown: C — starting value construction not shown in Rmd
- Minor: No table of fitted parameter estimates: C — pairs plots uninterpretable given 50,000-unit filter
- Minor: Live URL dependency breaks reproducibility: C — covidtracking.com API retired, code cannot re-run

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Measurement model uses binomial when negative binomial is needed for overdispersion — noise modeling in the measurement model is a misfit")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (Accumulator H=I instead of H+=dN_EI): A — fundamental accumulator misspecification affecting all results
- Finding 2 (No profile likelihoods or confidence intervals): A — major omission of identifiability assessment
- Finding 3 (No convergence diagnostics): A — no IF2 trace plots shown
- Finding 4 (ARIMA not used as quantitative benchmark against POMP): A — quotes erroneous ARIMA conclusion but does not flag it as factually wrong; concern is about missing POMP comparison, not the misinterpretation of the AIC table
- Finding 5 (guesses object not defined in rendered code): A — reproducibility failure
- Finding 6 (500 IF2 chains computationally unsound): A — computational allocation concern
- Finding 7 (Vaccination model allows S to go negative): A — missing lower-bound guard on susceptible compartment
- Finding 8 (No quantitative goodness-of-fit reported): A — only visual fit assessment provided
- Finding 9 (Binomial measurement model; negative binomial needed for overdispersion): D — noise modeling in the measurement model is a misfit (matches Human Issue #2)
- Finding 10 (Covariate multipliers fixed by assertion, not estimated): C — no statistical justification for multiplier values
- Finding 11 (H initial condition inconsistent with accumvars mechanism): C — secondary manifestation of accumulator error
- Finding 12 (Data filtering cutoff date inconsistency in text vs. code): C — June 10 stated but June 20 used
- Finding 13 (Vaccination data smoothed before use as covariate): C — fractional reductions to discrete compartment unacknowledged
- Finding 14 (No forecast generated despite stated goal): C — promised prediction entirely absent
- Finding 15 (ARIMA log-transformation incompatible with POMP log-likelihood): C — cross-model AIC comparison would be invalid

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "21.01.4 — ARIMA AIC table misinterpreted; text claims no significant evidence over white noise despite 500+ AIC-unit gap")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- 21.01.1: A — Measurement model sets H = I (stock) instead of incrementing H as a flow of new infections, invalidating the likelihood
- 21.01.2: A — No log-likelihood value, AIC, or other numeric fit metric reported for the POMP model
- 21.01.3: A — No quantitative comparison between ARIMA and POMP likelihoods or predictive accuracy
- 21.01.4: B — ARIMA AIC table misinterpreted; text concludes no improvement over white noise despite 500+ AIC-unit difference (matches Human Issue #1)
- 21.01.5: A — Beta covariate multipliers are hard-coded by assumption rather than estimated, making policy conclusions circular
- 21.01.6: A — No IF2 convergence trace plots shown; number of particles and MIF iterations not stated
- 21.01.7: A — No profile likelihoods, MCAP, or formal confidence intervals reported for any parameter
- Vaccination compartment guard: C — S -= dN_SE + IM does not prevent S from going negative if IM is large
- Reporting rate prior: C — Initial simulation uses rho = 0.9 (implausibly high); IF2 estimate of ~0.2 is inconsistent with this choice
- Weekly seasonality and SARIMA: C — Weekly seasonality identified in ACF but SARIMA(period=7) not considered for the ARIMA benchmark
- Np and Nmif not reported: C — Number of particles and MIF iterations not stated, preventing reproducibility assessment
- mu_EI fixed or estimated: C — Unclear whether mu_EI is fixed at 0.125 or included in IF2 search despite scatter plot appearing to show variation
- Accumulator variable naming: C — ini_positive_remained used in initial conditions but not defined in text
- Typo: C — "global searcg" should be "global search"
- Figure 12 and 16 labeling: C — Simulated trajectories not labeled as drawn from prior, posterior, or MLE parameters

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
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 5 | 8 | 6 |
| B (AI major, human also found) | 0 | 2 | 0 | 1 |
| C (AI minor, human missed) | 5 | 8 | 6 | 8 |
| D (AI minor, human also found) | 2 | 0 | 1 | 0 |
| E (Human found, AI missed) | 3 | 4 | 4 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 2 | 3 | 2/5 = 40% | 8 | 5 | 13/15 = 87% |
| Charlie | 2 | 0 | 4 | 1/5 = 20% | 5 | 8 | 13/15 = 87% |
| Doug | 0 | 1 | 4 | 1/5 = 20% | 8 | 6 | 14/15 = 93% |
| Evan | 1 | 0 | 4 | 1/5 = 20% | 6 | 8 | 14/15 = 93% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: The project's interpretation of model misspecification issues is reasonable. However, a simulation study to test the optimization on simulated data could have confirmed that the inference methodology was working correctly. Modeling COVID is not easy: see Projects 13 & 15 for a successful approach. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The initial ACF plots are unpolished: it can be unclear what we learn from an ACF of data with substantial trend, and attention is needed to graph labels. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 5 human issues (40%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #5: What is the red horizontal line in the log_test_positive_ratio plot? (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
