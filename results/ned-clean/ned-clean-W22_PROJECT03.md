# Ned-Clean Analysis — W22 Project 03

---

## Human Issues

1. Hard to comment constructively on an incomplete piece of work (project is severely incomplete; submission appears incomplete).
2. No need to show raw R output for the ACF and PACF.
3. Page 5: A unit root is not usually described as a "stationary growth process."
4. The requested source code file is not provided, though some of the code appears in the pdf.
5. References are missing.
6. Time limits the scope of the analysis, but that does not need to limit the level of scholarship.
7. More background on Twitch in general and the data in particular would have been useful to many readers.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "title contains spelling error and writeup is extremely terse / submitted in incomplete state")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major #1 (POMP process model does not update S): A — process model never increments/decrements state variable S
- Major #2 (dmeas uses rbinom, stochastic density): A — measurement model uses a random draw instead of a deterministic density
- Major #3 (no IF2 convergence diagnostics): A — no trace plots, no evidence of optimizer convergence
- Major #4 (global search references undefined fixed_params): A — undefined variable causes global search to fail silently
- Major #5 (AIC comparison between ARIMA and POMP invalid): A — likelihoods computed on different scales and observation spaces
- Major #6 (log-differencing mathematically inconsistent): A — log of negative numbers is undefined; not disclosed
- Major #7 (ARIMA order does not match transformation): A — d=1 applied to already-differenced series produces double differencing
- Major #8 (no POMP diagnostics — ESS, filter convergence): A — no effective sample size, no filter mean trajectories
- Major #9 (compartmental model not justified or formally defined): A — no mathematical formulation, no diagram, no scientific justification
- Major #10 (R-squared for ARIMA is meaningless): A — R² is not a standard or meaningful ARIMA diagnostic
- Minor #11 (residual ACF described as white noise without formal test): C — no Ljung-Box test; several lags near 95% confidence bound
- Minor #12 (data in reverse chronological order in twitch.csv): C — reversal and data cleaning step not documented
- Minor #13 (no estimated parameter values from final POMP fit): C — only log-likelihood reported; no fitted parameter values
- Minor #14 (title spelling error and writeup is extremely terse / incomplete state): D — matches Human Issue #1
- Minor #15 (spectral analysis conducted on wrong series): C — periodogram labeled "Series: x"; variable not tied to actual data

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "incomplete submission — POMP section appears as screenshot of HTML file")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no data source documentation or discussion of what 'Subscribers' measures on Twitch")

**Findings classification:**
- Major #1 (POMP measurement model uses rbinom inside dmeas): A — stochastic draw violates POMP determinism requirement
- Major #2 (single log-likelihood with no Monte Carlo uncertainty): A — no pfilter replication, no SE; course standard requires logmeanexp
- Major #3 (AIC comparison between ARIMA and POMP treated as valid): A — likelihoods on different scales cannot be compared directly
- Major #4 (no iterated filtering convergence diagnostics): A — no trace plots, no evidence of convergence or global optimum
- Major #5 (global search uses undefined variable fixed_params): A — undefined variable likely causes global search to fail
- Major #6 (likelihood clamped to 0 or -100 in dmeasure): A — ad hoc floor prevents particle filter from downweighting implausible particles
- Major #7 (process model does not track Subscribers as latent variable): A — S is supplied as covariate from observed data; no latent dynamics
- Major #8 (N fixed at 41.5M with no scientific justification): A — denominator is nine orders of magnitude larger than initial subscriber count
- Major #9 (no profile likelihoods or CIs): A — no parameter identifiability assessment; five free parameters
- Major #10 (incomplete submission — POMP section as browser screenshot): B — matches Human Issue #1
- Minor #11 (log-differencing undefined for negative values): C — log(diff(Subscribers)) undefined when differences are negative; not disclosed
- Minor #12 (R² = 0.983 for ARIMA model is misleading): C — R² is not a standard ARIMA goodness-of-fit measure
- Minor #13 (residual ACF lag-0 spike display issue): C — unusual y-axis range; possible misconfigured lag argument
- Minor #14 (title typo and course name typo): C — "Subsciber" and "SATST531" typos; not proofread
- Minor #15 (no data source documentation / what "Subscribers" means on Twitch): D — matches Human Issue #7

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "PDF renders a local file path in the POMP section — sections screenshotted from separate rendered file")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major #1 (invalid log-likelihood comparison between ARIMA and POMP): A — different observation scales; cannot compare numerically
- Major #2 (dmeasure clips log-likelihood to 0 or -100): A — clamping at -100 distorts particle weights and biases likelihood estimate
- Major #3 (dmeasure uses rbinom internally, stochastic): A — non-deterministic density makes particle filter weights theoretically invalid
- Major #4 (rmeasure and dmeasure semantically inconsistent): A — dmeas evaluates density for Subs+D-S while rmeas produces Subs directly
- Major #5 (rprocess does not update Subscribers state variable): A — S never incremented; growth driven entirely by covariate
- Major #6 (Subscribers supplied as covariate and declared as state — circular specification): A — latent state pinned to observed data; no latent dynamics
- Major #7 (no convergence diagnostics for POMP): A — no trace plots, no ESS diagnostics, no comparison across replicates
- Major #8 (global IF2 search initializes from mifs_local[[1]] rather than base pomp object): A — inherits local cooling schedule; not a genuine global search
- Major #9 (no profile likelihoods, CIs, or identifiability assessment): A — five free parameters, 60 observations; identifiability in doubt
- Major #10 (no benchmark comparison for POMP model): A — ARIMA fit on different scale cannot serve as benchmark
- Minor: Typo in title — C — "Subsciber Analysis" and CSV column "AvgVeiwers" spelling errors
- Minor: N fixed at 41.5M without justification — C — normalizing quantity for force-of-infection term unexplained
- Minor: fixed_params referenced but never defined — C — global search code would throw runtime error
- Minor: rw.sd values match starting parameter values — C — perturbation SD of 0.37 for mu_VS is very large; pomp-rw-sd-magnitude-error pattern
- Minor: Model description incomplete (Viewers variable not in state vector) — C — rprocess never creates/resets Viewers; text describes different model than code
- Minor: R² = 0.983 for ARIMA is misleading — C — R² not a standard ARIMA metric
- Minor: Stationarity assessed only visually — C — no formal ADF/KPSS/Phillips-Perron test
- Minor: AIC table grid search on log-differenced data but model called ARIMA(1,1,2) — C — d=1 label redundant; confusing notation
- Minor: PDF renders local file path in POMP section — D — matches Human Issue #1 (submission in incomplete/non-integrated state)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "supplement formatting — POMP section appears as browser-printed HTML exposing local file path")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "missing reference list — single citation '[1]' has no corresponding bibliography entry")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major 22.03.2 (ARIMA-POMP comparison ungrounded): A — POMP LL is -866.06 but ARIMA LL never reported on comparable scale
- Major 22.03.3/4 (dmeas fundamentally broken — rbinom stochastic draw + lik clamping): A — two combined errors: non-deterministic density and inverted weighting via clamping
- Major 22.03.5 (no convergence diagnostics for mif2): A — no trace plots; cannot assess whether MLE found
- Major 22.03.6 (no parameter estimates from POMP fit reported): A — fitted values of Beta_sigma, mu_VS, mu_SB, Beta_0 not reported
- Minor 22.03.1 (transformation pipeline undocumented — log-diff vs ARIMA d=1): C — which series is passed to arima() not explicitly stated
- Minor 22.03.7 (AR root near unit circle): C — AR root of 1.01363 noted but not discussed
- Minor 22.03.8 (R² not appropriate for ARIMA): C — R² not a standard metric for ARIMA estimated by MLE
- Minor 22.03.10 (N fixed at 41.5M without justification): C — entire platform user base used as denominator for single channel model
- Minor 22.03.11 (residual ACF described as white noise prematurely): C — multiple lags near 95% band; Ljung-Box test absent
- Minor 22.03.9 (periodogram spike at f≈0.5 not explained): C — prominent spike at Nyquist frequency uncommented
- Minor: missing reference list: D — matches Human Issue #5
- Minor: supplement formatting (POMP section as browser-printed HTML): D — matches Human Issue #1

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 10 | 9 | 10 | 4 |
| B (AI major, human also found) | 0 | 1 | 0 | 0 |
| C (AI minor, human missed) | 4 | 4 | 8 | 6 |
| D (AI minor, human also found) | 1 | 1 | 1 | 2 |
| E (Human found, AI missed) | 6 | 5 | 6 | 5 |

---

## Per-Reviewer Metrics

**Alex:**
- Human Recall = (B+D) / (B+D+E) = (0+1) / (0+1+6) = 1/7 ≈ 14.3%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (10+4) / (10+0+4+1) = 14/15 ≈ 93.3%

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+5) = 2/7 ≈ 28.6%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (9+4) / (9+1+4+1) = 13/15 ≈ 86.7%

**Doug:**
- Human Recall = (B+D) / (B+D+E) = (0+1) / (0+1+6) = 1/7 ≈ 14.3%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (10+8) / (10+0+8+1) = 18/19 ≈ 94.7%

**Evan:**
- Human Recall = (B+D) / (B+D+E) = (0+2) / (0+2+5) = 2/7 ≈ 28.6%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+6) / (4+0+6+2) = 10/12 ≈ 83.3%

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (E for all four):

- Human Issue #2: No need to show raw R output for the ACF and PACF.
- Human Issue #3: A unit root is not usually described as a "stationary growth process."
- Human Issue #4: The requested source code file is not provided.
- Human Issue #6: Time limits the scope but does not need to limit the level of scholarship.

Count: 4 out of 7 human issues (57.1%) were missed by every reviewer.

### Unique finds per reviewer

Human issues covered by exactly one reviewer (all others missed):

- Human Issue #5 (references missing): covered only by Evan. All others missed.
- Human Issue #7 (more background on Twitch/data): covered only by Charlie. All others missed.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

1. The dmeasure function uses rbinom (a stochastic random draw) instead of a deterministic density, making particle weights non-reproducible and theoretically invalid. (Alex Major #2; Charlie Major #1; Doug Major #3; Evan Major 22.03.3/4)
2. No IF2 convergence diagnostics are shown — no trace plots of log-likelihood or parameters over mif2 iterations. (Alex Major #3; Charlie Major #4; Doug Major #7; Evan Major 22.03.5)
3. The ARIMA-POMP log-likelihood comparison is invalid because the two models are fitted on different data scales and observation spaces. (Alex Major #5; Charlie Major #3; Doug Major #1; Evan Major 22.03.2)
4. The likelihood in dmeasure is clamped at -100, preventing the particle filter from correctly downweighting implausible particles and corrupting the likelihood surface. (Alex Major #6; Charlie Major #6; Doug Major #2; Evan Major 22.03.3/4)

Count: 4 universal AI-only flags (all classified Major by all four reviewers).
