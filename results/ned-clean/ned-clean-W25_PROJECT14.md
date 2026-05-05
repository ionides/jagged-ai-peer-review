# Ned-Clean Analysis — W25 Project 14

## Human Issues

1. Plotting, ACF, spectral analysis, and ARMA modeling should all be done on a log scale; the log-ARMA likelihood needs to be computed with care.
2. Review of past STATS 531 work on flu could have been more complete (beyond the two projects cited).
3. The claim that "a strong autocorrelation at lag one that decays gradually indicates a non-stationary time series" is formally incorrect.
4. There is confusion between ODE models and stochastic models in the statement about Euler's method and the binomial approximation.
5. The ARMA likelihood is not discussed or presented in the context of providing a benchmark to check the mechanistic model specification.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (SIRS log-likelihood +19821.71 nonsensical, indexing error): A — SIRS LL is impossible positive value due to wrong best_index
- Finding 2 (SIRS uses N=3.25e8, US population): A — wrong population size for Nova Scotia
- Finding 3 (SIRS Poisson measurement model, not NegBin): A — measurement model mismatch
- Finding 4 (SIRS global search ignores accumulated sirs_lik.csv): A — best-fit selection ignores stored results
- Finding 5 (Profile best-fit rho outside 95% CI): A — profile CI inconsistency not investigated
- Finding 6 (ARIMA fitted on differenced series but labeled ARIMA(p,0,q)): A — ARIMA order mislabeling
- Finding 7 (SIR mu_IR implies 250-300 day infectious period): A — biologically implausible recovery rate
- Finding 8 (SIRS step function has inconsistent versions in document): C — two versions with different safety clamps
- Finding 9 (SEIRS H accumulates dN_IR, not new infections): C — accumulator tracks recoveries not incidence
- Finding 10 (Spectral analysis on undifferenced series, frequency=1): C — spurious low-frequency peak risk
- Finding 11 (SIR global search uses only 5 likelihood replications): C — too few replicates per chain
- Finding 12 (SEIRS global search lower bounds set to exactly 0): C — numerical instability risk
- Finding 13 (Inconsistent observation variable names across models): C — cases_obs vs cases naming
- Finding 14 (Observation count self-contradictory, 262 vs 261): C — unexplained discrepancy
- Finding 15 (ChatGPT cited for methodological decisions): C — inappropriate citation for standard topics

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
- Human Issue #3: covered (matched by finding 8: "ACF interpretation of non-stationarity is questionable")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding 2: "no non-mechanistic benchmark comparison")

**Findings classification:**
- Finding 1 (Positive SIRS log-likelihood, numerical error from wrong best_index): A — impossible LL value
- Finding 2 (No non-mechanistic benchmark comparison): B — ARIMA LL never compared to POMP models (matches Human Issue #5)
- Finding 3 (SIRS Poisson measurement model, unjustified, underdispersed): A — inconsistent with SIR/SEIRS NegBin
- Finding 4 (Global search negligible improvement, inadequate computation): A — only 0.9 log-unit gain from 100 global starts
- Finding 5 (Profile likelihood for only one parameter): A — no profiles for Beta0, amp, phase, mu_EI, mu_IR, mu_RS
- Finding 6 (SIRS population N=3.25e8, three orders of magnitude error): A — US population used instead of Nova Scotia
- Finding 7 (SIRS pandemic threshold t<261 not scientifically grounded): A — no pandemic in 2014-2019 data
- Finding 8 (ACF/PACF misidentification and incorrect AIC model selection): B — ACF non-stationarity claim challenged; ARIMA mislabeling identified (matches Human Issue #3)
- Finding 9 (Conflicting observation count 262 vs 261): C — unexplained discrepancy
- Finding 10 (SIR measurement model observes recoveries, not new infections): C — dN_IR vs dN_SI semantics
- Finding 11 (No sessionInfo() or package version documentation): C — reproducibility concern
- Finding 12 (SIRS global search uses sequential lapply, not parallel): C — inconsistent with rest of workflow
- Finding 13 (Profile rho interpretation implausible, ~5% weekly attack rate): C — not cross-validated against surveillance data
- Finding 14 (PACF plot titled "ACF of Influenza Cases"): C — copy-paste error in plot title
- Finding 15 (seirs_pf.R profile: rho fixed correctly but not stated; CI may be incomplete): C — narrow profile CI not flagged as artifact

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding 4: "no non-mechanistic benchmark comparison")

**Findings classification:**
- Finding 1 (SIRS uses N=3.25e8, US population): A — force of infection scaled to wrong population
- Finding 2 (Inverted log-likelihood interpretation in conclusion): A — "lowest" used where "highest" is correct
- Finding 3 (Cross-model LL comparison invalid, different measurement models): A — Poisson vs NegBin plus different N values
- Finding 4 (No non-mechanistic benchmark comparison): B — ARIMA LL never placed alongside POMP LLs (matches Human Issue #5)
- Finding 5 (SEIRS global search uses local-search chain as first mif2 arg): A — inherited cooling schedule prevents exploration
- Finding 6 (Profile likelihood singleton CI): A — degenerate CI from single mif2 per profile point
- Finding 7 (Profile maximum exceeds global search maximum by 9.2 log-units): A — global search failed to find MLE region
- Finding 8 (SIR global search second mif2 call inherits previous chain): A — redundant call with decayed cooling schedule
- Minor: Inconsistent observation count (262 vs 261): C — unexplained discrepancy
- Minor: SIR mu_IR biologically implausible (273-week infectious period): C — acknowledged but not diagnosed as misspecification
- Minor: Accumulator tracks recoveries not new infections: C — dN_IR vs dN_SI for surveillance data
- Minor: No model diagnostics beyond visual simulations: C — no per-observation LL or latent state plots
- Minor: Profile likelihood covers only rho: C — no profiles for Beta0, amp, mu_IR
- Minor: SIRS Poisson measurement model without justification: C — inconsistent with other models
- Minor: SIRS beta switch at t=261 not biologically motivated: C — no pandemic in 2014-2019
- Minor: SEIRS mu_EI estimate at high end of plausible range, not compared to literature: C — instability in trace plots not discussed
- Minor: SIRS best_index mismatch in conclusion code: C — secondary to positive LL error
- Minor: SEIRS global search seeded from CSV with ambiguous state: C — execution order dependency

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
- Human Issue #5: covered (matched by finding 25.14.5: "no non-mechanistic benchmark comparison")

**Findings classification:**
- 25.14.1 (Single pfilter used for final model comparison, no logmeanexp): A — unreliable LL estimates in conclusion table
- 25.14.2 (SIRS Poisson vs NegBin, makes three-way LL comparison invalid): A — measurement model mismatch
- 25.14.3 (SIRS parameters biologically implausible: N=325M, mu_IR unrealistic): A — model misspecification not diagnosed
- 25.14.4 (Profile likelihood for rho collapses to degenerate CI): A — singleton CI not acknowledged as failure
- 25.14.5 (No non-mechanistic benchmark comparison): B — ARIMA LL never compared to POMP models (matches Human Issue #5)
- 25.14.6 (SIR rho≈0.99 implausible, not profiled or constrained): A — near-100% reporting rate is misspecification signal
- 25.14.7 (SIRS pandemic branch never activated, b parameter unidentified): A — t<261 covers all data, b is structurally unidentifiable
- 25.14.m1 (Low pfilter replicates in SIR global search, only 5): C — inconsistent with SEIRS local search (20 replicates)
- 25.14.m2 (ARIMA order ambiguity: ARMA on differenced series labeled ARIMA(p,0,q)): C — equivalent to ARIMA(p,1,q) on original
- 25.14.m3 (ChatGPT citations for methodological decisions): C — should cite course materials or literature
- 25.14.m4 (Conclusion LL value inconsistency: text -590.46, code -591.71): C — values need reconciliation
- 25.14.m5 (Figure captions missing or non-descriptive): C — readability issue
- 25.14.m6 (Spectral period 54 weeks vs model forcing period 52 weeks): C — sensitivity not assessed

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
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 7 | 6 |
| B (AI major, human also found) | 0 | 2 | 1 | 1 |
| C (AI minor, human missed) | 8 | 7 | 10 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 5 | 3 | 4 | 4 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (0+0) / (0+0+5) = 0/5 = **0.00**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+8) / (7+0+8+0) = 15/15 = **1.00**

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+3) = 2/5 = **0.40**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+2+7+0) = 13/15 = **0.87**

**Doug**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+4) = 1/5 = **0.20**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+10) / (7+1+10+0) = 17/18 = **0.94**

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+4) = 1/5 = **0.20**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+6) / (6+1+6+0) = 12/13 = **0.92**

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer:

- **Human Issue #1** (log scale for plotting, ACF, spectral analysis, and ARMA; log-ARMA likelihood care): missed by Alex, Charlie, Doug, Evan
- **Human Issue #2** (review of past STATS 531 flu work was incomplete): missed by Alex, Charlie, Doug, Evan
- **Human Issue #4** (confusion between ODE and stochastic models in Euler/binomial statement): missed by Alex, Charlie, Doug, Evan

**Count: 3 out of 5 human issues (60%) were missed by all reviewers.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Charlie uniquely covered **Human Issue #3** (the ACF lag-1 non-stationarity claim is formally incorrect): missed by Alex, Doug, Evan.
- Human Issue #5 (ARMA likelihood not used as benchmark) was covered by Charlie, Doug, and Evan — not unique to any one reviewer.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

1. **SIRS model uses US population (N = 3.25e8) instead of Nova Scotia population (~969,400)**: flagged as Major by Alex, Charlie, Doug, and Evan. The human review did not raise this.
2. **SIRS measurement model uses Poisson rather than Negative Binomial, making cross-model log-likelihood comparisons invalid**: flagged as Major by Alex, Charlie, Doug (minor), and Evan. Note: Doug classified this as Minor, so this is not strictly all-Major, but all four reviewers flagged it.
3. **Profile likelihood confidence interval is degenerate or collapses to a near-singleton**: flagged as Major by Alex, Charlie, Doug, and Evan. The human review did not raise this.

**Count: 3 universal AI-only flags (raised by all four reviewers, not mentioned by the human).**
