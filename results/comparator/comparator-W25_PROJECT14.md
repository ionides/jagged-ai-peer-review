# Comparator Analysis — W25 Project 14

---

## Human Issues

1. Plotting, ACF, spectral analysis and ARMA are all best done on a log scale. Then, the log-ARMA likelihood needs to be computed with care (see the measles case study in Chapter 18).

2. The project acknowledges building on two previous projects on flu in Oklahoma (W24 #5) and aggregated for USA (W22 #43), and makes a clear statement about how it progresses beyond these previous projects. However, there are other 531 projects on flu with profiles, e.g., W24 #16. Review of past 531 work on flu could have been more complete, but readers were satisfied that this project goes beyond previous work in ways other than just using a different dataset.

3. Formally, it is incorrect to say "a strong autocorrelation at lag one that decays gradually across subsequent lags indicates a non-stationary time series". The usual motivation for the sample ACF assumes a stationary model. The rate of decay in that case just depends on the timescale of dependence.

4. There is some confusion in: "The ODEs can be solved by Euler's numerical method. Specifically, the RHS can be expressed as a binomial approximation with exponential transition probability". The ODE model and stochastic models are different things.

5. The main value of ARMA is probably to provide a benchmark to check when the mechanistic model is becoming well specified. The ARMA likelihood is not discussed in this context (and is not presented, though it can be back-calculated from the reported AIC).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (SIRS LL +19821.71 nonsensical, indexing error): A — SIRS log-likelihood value is implausible and caused by a code indexing bug
- Finding 2 (SIRS N = 3.25e8, U.S. population not Nova Scotia): A — SIRS model uses wrong population size
- Finding 3 (SIRS Poisson vs. NegBin measurement model): A — inconsistent distributional assumption invalidates cross-model LL comparison
- Finding 4 (SIRS global search ignores accumulated sirs_lik.csv results): A — best global fit may not be true optimum
- Finding 5 (profile rho best-fit outside its own 95% CI): A — unresolved discrepancy between global search and profile likelihood
- Finding 6 (ARIMA fitted on differenced series but labeled ARIMA(p,0,q)): A — contradictory presentation of the differencing order
- Finding 7 (SIR mu_IR implies ~250-300 day infectious period): A — biologically implausible recovery rate not investigated
- Finding 8 (SIRS step function inconsistent versions in same document): C — two versions used across local and global search
- Finding 9 (SEIRS H accumulates recoveries not new infections): C — measurement model conflates incidence with lagged recovery
- Finding 10 (spectral analysis on undifferenced series, frequency=1): C — raw nonstationary series creates spurious low-frequency peak
- Finding 11 (SIR global search uses only 5 LL replications): C — inconsistent replicate count inflates variance in chain ranking
- Finding 12 (SEIRS lower bounds set to 0 for log/logit-transformed parameters): C — near-zero starts produce numerical instability
- Finding 13 (inconsistent observation variable names cases_obs vs. cases): C — duplicated data preparation with minor variations across models
- Finding 14 (observation count 262 vs. 261 self-contradictory): C — unexplained discrepancy in introduction
- Finding 15 (ChatGPT cited for standard POMP methodology): C — language model cited in place of course notes or literature

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "ARIMA differencing lacks unit root justification")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No non-mechanistic benchmark comparison")

**Findings classification:**
- Major Issue 1 (No non-mechanistic benchmark comparison): B — ARIMA and POMP analyses never compared numerically; ARIMA log-likelihood absent (matches Human Issue #5)
- Major Issue 2 (SIRS model uses US population size N=3.25e8): A — biologically invalid transmission parameters for Nova Scotia study
- Major Issue 3 (Single unreplicated pfilter; impossible positive log-likelihood): A — Monte Carlo noise invalidates model ranking; +19,821 SIRS loglik physically impossible
- Major Issue 4 (Wrong index used to extract best SIRS model): A — SIR best_index reused for SIRS, so SIRS fit in conclusion is arbitrary
- Major Issue 5 (No convergence trace plots for SIR model): A — no evidence SIR optimizer converged
- Major Issue 6 (Profile likelihood CI is degenerate): A — single-point interval with min=max=0.001769433; MLE outside reported CI
- Major Issue 7 (Inconsistent measurement models across POMP models): A — NegBin for SIR/SEIRS vs Poisson for SIRS makes log-likelihood comparison invalid
- Minor: Log-likelihood comparison direction misstated: C — text says "lowest value" is best but higher log-likelihood is better
- Minor: Inconsistent observation count: C — two consecutive sentences report 262 vs 261 observations
- Minor: Unit error in data summary: C — "1 case per day" should be "1 case per week"
- Minor: ARIMA differencing lacks unit root justification: D — ACF decay used to conclude d=1 without ADF test or formal stationarity reasoning (matches Human Issue #3)
- Minor: H accumulator tracks recoveries rather than symptom onset: C — dN_IR used as observation proxy instead of dN_EI, introducing systematic lag
- Minor: SIRS global search uses only 3 pfilter replicates: C — fewer replicates than SIR/SEIRS produces higher Monte Carlo variance
- Minor: No package versions or sessionInfo provided: C — pomp API changes make results non-reproducible without version pins
- Minor: Duplicate and inconsistent data loading across sections: C — CSV loaded and filtered independently in three code chunks with differing column names

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No non-mechanistic benchmark comparison — ARIMA log-likelihood never computed or compared to POMP models")

**Findings classification:**
- Major 1 (SIRS N=3.25e8): A — SIRS model uses U.S. population instead of Nova Scotia population
- Major 2 (inverted log-likelihood): A — conclusion incorrectly identifies "lowest" log-likelihood as best fit
- Major 3 (cross-model comparison invalid): A — three models use different measurement models and population sizes, making log-likelihood comparison invalid
- Major 4 (no non-mechanistic benchmark): B — ARIMA log-likelihood never computed or compared to POMP models (matches Human Issue #5)
- Major 5 (SEIRS global search inherits local-search chain): A — global search seeds from mif2 result object, inheriting decayed cooling schedule
- Major 6 (profile likelihood singleton CI): A — only one profile grid point exceeds chi-squared cutoff, producing a degenerate confidence interval
- Major 7 (profile max exceeds global search max): A — profile maximum 9.2 units better than global search maximum, indicating failed global optimization
- Major 8 (SIR global search second mif2 call): A — second mif2(mf) call inherits cooling schedule from first, adding no genuine exploration
- Minor (inconsistent observation count): C — text says both 262 and 261 observations
- Minor (SIR mu_IR biologically implausible): C — implied infectious period of ~273 weeks versus typical 3-7 days
- Minor (accumulator variable tracks recoveries): C — H accumulates dN_IR (recoveries) rather than dN_SI (new infections)
- Minor (no model diagnostics beyond visual simulations): C — no per-observation log-likelihood plots or filtering distribution comparisons
- Minor (profile covers only rho): C — no profiles for Beta0, seasonal amplitude, or mu_IR
- Minor (SIRS Poisson without justification): C — SIRS uses Poisson while SIR and SEIRS use negative binomial, no justification given
- Minor (SIRS beta switch at t=261): C — pre-pandemic/pandemic threshold at t=261 not biologically motivated for 2014-2019 data
- Minor (SEIRS mu_EI implausible latent period): C — implied latent period at high end of plausible range with no literature comparison
- Minor (SIRS best_index mismatch): C — SIRS comparison uses best_index computed for SIR model, not SIRS chains
- Minor (CSV state ambiguous): C — influenza_params.csv read and written by multiple scripts with order-dependent reproducibility

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "25.14.5 — No non-mechanistic benchmark comparison; ARIMA log-likelihood never compared to POMP models")

**Findings classification:**
- 25.14.1: A — Single pfilter call used for final model comparison rather than replicated logmeanexp
- 25.14.2: A — SIRS uses Poisson measurement noise while SIR and SEIRS use Negative Binomial, invalidating likelihood comparison
- 25.14.3: A — SIRS parameter estimates biologically implausible (N ≈ 325 million, 1-day infectious period); misspecification not diagnosed
- 25.14.4: A — Profile likelihood for rho collapses to degenerate CI (min = max = 0.00177); numerical failure not acknowledged
- 25.14.5: B — No non-mechanistic benchmark comparison; ARIMA log-likelihood never compared to POMP models (matches Human Issue #5)
- 25.14.6: A — SIR reporting rate rho ≈ 0.99 epidemiologically implausible; not diagnosed via profile likelihood
- 25.14.7: A — SIRS pandemic branch never activated so parameter b is structurally unidentified; not acknowledged
- 25.14.m1: C — SIR global search uses only 5 pfilter replicates per chain, below standard practice
- 25.14.m2: C — ARIMA model order ambiguity: fitting to differenced series makes selected "ARIMA(2,0,2)" actually ARIMA(2,1,2)
- 25.14.m3: C — ChatGPT cited for methodological decisions (rw.sd settings, profile likelihood interpretation)
- 25.14.m4: C — Conclusion states SEIRS best log-likelihood as -590.46 but code output shows -591.71
- 25.14.m5: C — Most figures lack descriptive captions
- 25.14.m6: C — Spectral analysis identifies dominant period of 54 weeks but model uses 52-week seasonal forcing with no sensitivity assessment

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 7 | 6 | 7 | 6 |
| B (AI major, human also found) | 0 | 1 | 1 | 1 |
| C (AI minor, human missed) | 8 | 7 | 10 | 6 |
| D (AI minor, human also found) | 0 | 1 | 0 | 0 |
| E (Human found, AI missed) | 5 | 3 | 4 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 0 | 5 | 0/5 = 0% | 7 | 8 | 15/15 = 100% |
| Charlie | 1 | 1 | 3 | 2/5 = 40% | 6 | 7 | 13/15 = 87% |
| Doug | 1 | 0 | 4 | 1/5 = 20% | 7 | 10 | 17/18 = 94% |
| Evan | 1 | 0 | 4 | 1/5 = 20% | 6 | 6 | 12/13 = 92% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Plotting, ACF, spectral analysis and ARMA are all best done on a log scale. Then, the log-ARMA likelihood needs to be computed with care (see the measles case study in Chapter 18). (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: The project acknowledges building on two previous projects on flu in Oklahoma (W24 #5) and aggregated for USA (W22 #43), and makes a clear statement about how it progresses beyond these previous projects. However, there are other 531 projects on flu with profiles, e.g., W24 #16. Review of past 531 work on flu could have been more complete, but readers were satisfied that this project goes beyond previous work in ways other than just using a different dataset. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: There is some confusion in: "The ODEs can be solved by Euler's numerical method. Specifically, the RHS can be expressed as a binomial approximation with exponential transition probability". The ODE model and stochastic models are different things. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 5 human issues (60%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: Formally, it is incorrect to say "a strong autocorrelation at lag one that decays gradually across subsequent lags indicates a non-stationary time series". The usual motivation for the sample ACF assumes a stationary model. The rate of decay in that case just depends on the timescale of dependence. (Covered only by Charlie)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |
