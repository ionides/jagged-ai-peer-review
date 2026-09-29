# Comparator Analysis — W22 Project 03

---

## Human Issues

1. It is hard to comment constructively on an incomplete piece of work.
2. No need to show raw R output for the ACF and PACF.
3. Page 5: A unit root is not usually described as a "stationary growth process" though one can guess what this means.
4. The requested source code file is not provided, though some of the code appears in the pdf.
5. References are missing.
6. Evidently, the authors ran out of time. It is okay if time limits the scope of the analysis, but that does not need to limit the level of scholarship.
7. More background on Twitch in general and the data in particular would have been useful to many readers.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "title spelling error and writeup extremely terse, project submitted in incomplete state")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "title spelling error and writeup extremely terse, project submitted in incomplete state")
- Human Issue #7: missed

**Findings classification:**
- Finding 1: A — POMP process model never updates latent state S; model uses observed data as covariate
- Finding 2: A — dmeas uses rbinom (random draw) instead of a deterministic conditional density, making particle filter invalid
- Finding 3: A — no IF2 convergence diagnostics (no trace plots, no likelihood profile, no pairs plot)
- Finding 4: A — global search references undefined object `fixed_params`, making the global search unrunnable
- Finding 5: A — AIC comparison between ARIMA and POMP log-likelihoods is invalid because models are fitted on different scales
- Finding 6: A — log(diff(Subscribers)) transformation is undefined for negative differences, which occur in the data
- Finding 7: A — ARIMA(1,1,2) model order inconsistent with pre-differenced series (effectively double-differencing)
- Finding 8: A — no POMP model diagnostics (no ESS over time, no filter mean trajectories, no particle degeneracy check)
- Finding 9: A — compartmental model structure not formally defined, no diagram, no justification, parameter N unexplained
- Finding 10: A — R-squared reported for ARIMA is not a standard or meaningful diagnostic for ARIMA models
- Finding 11: C — residual ACF plot y-axis range is misleading and no formal test (e.g., Ljung-Box) supports the white-noise claim
- Finding 12: C — data reversal from twitch.csv to twitch2.csv is undocumented, raising reproducibility questions
- Finding 13: C — estimated parameter values from the final POMP fit are never reported
- Finding 14: D — title spelling error and writeup extremely terse; project submitted in incomplete state (matches Human Issues #1 and #6)
- Finding 15: C — spectral analysis uses unlabeled variable "x"; smoothed spectral estimate not provided

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Incomplete submission — POMP section appears as screenshot of HTML file with browser chrome visible, analysis cuts off mid-sentence")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Incomplete submission — POMP section appears as screenshot of HTML file with browser chrome visible, analysis cuts off mid-sentence")
- Human Issue #7: covered (matched by finding: "No data source documentation or discussion of what 'Subscribers' measures on Twitch")

**Findings classification:**
- Finding 1 (rbinom inside dmeas — dmeasure not deterministic): A — POMP measurement model structurally misspecified; rbinom drawn inside density evaluation
- Finding 2 (single log-likelihood, no Monte Carlo uncertainty): A — single scalar log-likelihood reported without replication or standard error
- Finding 3 (AIC comparison between ARIMA and POMP treated as directly valid): A — cross-scale AIC comparison invalid; models evaluated on different observation scales
- Finding 4 (no iterated filtering convergence diagnostics): A — no trace plots or convergence evidence for mif2 runs
- Finding 5 (undefined variable `fixed_params` in global search): A — global search code references undefined variable, making results unreliable
- Finding 6 (likelihood clamped at -100 in dmeasure): A — ad hoc floor prevents proper particle downweighting, biases likelihood
- Finding 7 (Subscribers state not tracked as latent variable — used as covariate instead): A — model bypasses POMP latent-state inference by using lagged observed data as covariate
- Finding 8 (N fixed at 41,500,000 with no justification): A — denominator N is nine orders of magnitude larger than initial subscriber count, making Beta unidentifiable
- Finding 9 (no profile likelihoods or confidence intervals): A — no uncertainty quantification for any POMP parameter
- Finding 10 (incomplete submission — POMP section as HTML screenshot, cuts off mid-sentence): B — incomplete submission identifies same underlying concern as Human Issues #1 and #6 (matches Human Issues #1 and #6)
- Finding 11 (log-differencing conflates two transformations without diagnostic justification): C — log(diff(x)) undefined for negative differences; more principled approach not used
- Finding 12 (R-squared reported for ARIMA model): C — R2 not a standard or well-defined fit measure for a differenced ARIMA model
- Finding 13 (ACF plot lag-0 spike incorrect): C — residual ACF shows unusual lag-0 bar, possibly misconfigured
- Finding 14 (title and course name typos): C — "Subsciber Analysis" and "SATST531" are typographic errors
- Finding 15 (no data source documentation or Twitch background): D — no URL, access date, or explanation of what "Subscribers" measures on Twitch (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major 1 (invalid ARIMA–POMP log-likelihood comparison): A — likelihoods on different scales cannot be compared
- Major 2 (dmeasure clips lik to [−100, 0]): A — clamping distorts particle weights and makes log-likelihood meaningless
- Major 3 (dmeasure uses rbinom, making density stochastic): A — random intermediate in dmeasure violates proper density semantics
- Major 4 (rmeasure and dmeasure measure different quantities): A — dmeasure evaluates Subs+D−S while rmeasure produces Subs
- Major 5 (rprocess never updates Subscribers state S): A — S is never incremented, making BVS a trivial persistence model
- Major 6 (Subscribers is both covariate and latent state — circular): A — pinning latent state to observed data defeats POMP modeling
- Major 7 (no convergence diagnostics for POMP analysis): A — no trace plots, ESS, or replicate comparisons shown
- Major 8 (global IF2 initializes from mifs_local[[1]] instead of base object): A — global search inherits local chain cooling schedule
- Major 9 (no profile likelihoods or parameter identifiability assessment): A — no uncertainty quantification for any parameter
- Major 10 (no proper benchmark comparison for POMP model): A — ARIMA fit on transformed scale cannot serve as benchmark
- Minor: Typo in title ("Subsciber"): C — also misspelling in CSV column "AvgVeiwers"
- Minor: N fixed at 41,500,000 without justification: C — population normalizer unjustified and never estimated
- Minor: fixed_params referenced but never defined: C — would cause runtime error, suggests template copy incomplete
- Minor: rw.sd values match starting-parameter values: C — perturbation SD of 0.37 for mu_VS is very large
- Minor: Model description inconsistent with code (Viewers never reset in rprocess): C — text describes a different model than implemented
- Minor: R2 = 0.983 misleading for ARIMA model: C — R-squared is not a standard ARIMA metric
- Minor: Stationarity assessed only visually without formal test: C — no ADF/KPSS/Phillips-Perron test conducted
- Minor: AIC grid on pre-differenced series but model called ARIMA(1,1,2): C — d=1 label is redundant and confusing
- Minor: PDF embeds local HTML file screenshots (file:///C:/Users/Ahmed/...): C — reproducibility and presentation concern

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Presentation — missing reference list")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- 22.03.2: A — ARIMA vs POMP comparison is ungrounded; ARIMA log-likelihood never reported for comparison
- 22.03.3/22.03.4: A — dmeas contains stochastic draw and illegal likelihood clipping, making particle filter weights invalid
- 22.03.5: A — no convergence diagnostics (trace plots) shown for mif2 runs
- 22.03.6: A — no POMP parameter estimates reported
- 22.03.1: C — transformation pipeline ambiguity (log-differenced EDA vs ARIMA d=1)
- 22.03.7: C — AR root of 1.01363 near unit circle not discussed
- 22.03.8: C — R² reported but not a meaningful metric for ARIMA estimated by MLE
- 22.03.9: C — periodogram spike at Nyquist frequency left unexplained
- 22.03.10: C — total Twitch user base (N=41.5M) used as population size without justification
- 22.03.11: C — residual ACF prematurely described as white noise without Ljung-Box test
- Presentation-missing-reference: D — single citation "[1]" has no bibliography entry (matches Human Issue #5)
- Presentation-supplement-formatting: C — POMP supplement appears to be a browser-printed HTML file with local file path in header
- Unacknowledged-strength-forward-simulation: C — forward simulation trajectories qualitatively consistent with observed data not acknowledged as supporting evidence

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 10 | 9 | 10 | 4 |
| B (AI major, human also found) | 0 | 1 | 0 | 0 |
| C (AI minor, human missed) | 4 | 4 | 9 | 8 |
| D (AI minor, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 5 | 4 | 7 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 1 | 5 | 2/7 = 29% | 10 | 4 | 14/15 = 93% |
| Charlie | 1 | 1 | 4 | 3/7 = 43% | 9 | 4 | 13/15 = 87% |
| Doug | 0 | 0 | 7 | 0/7 = 0% | 10 | 9 | 19/19 = 100% |
| Evan | 0 | 1 | 6 | 1/7 = 14% | 4 | 8 | 12/13 = 92% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: No need to show raw R output for the ACF and PACF. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: Page 5: A unit root is not usually described as a "stationary growth process" though one can guess what this means. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The requested source code file is not provided, though some of the code appears in the pdf. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 7 human issues (43%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #5: References are missing. (Covered only by Evan)
- Human Issue #7: More background on Twitch in general and the data in particular would have been useful to many readers. (Covered only by Charlie)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 1 |
