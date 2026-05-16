# Ned-Clean Analysis — W21 Project 14

---

## Human Issues

1. The global search finds two modes (reporting rate ~10% and ~100%), with the second implying susceptible depletion has no dynamic importance, and a hint of a third mode; the multimodality is not adequately discussed.
2. The log likelihood search sometimes falls off a likelihood cliff (possibly because the binomial/negative binomial measurement or process model lacks sufficient stochasticity), and viewing likelihoods on this scale makes it hard to distinguish candidate modes.
3. The measurement model in the code is negative binomial, rather than the binomial reported in the text; if overdispersion is the issue it could also be needed in the process model.
4. A section on potential future work would be useful given the restrictive time limitations of a course final project.
5. The search and results might look cleaner if phase were reparameterized to take values only in (0, 2pi), since the periodicity of phase adds extra clutter to the numerical results.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding #8 — convergence diagnostics incomplete for global search, mentions diverging directions for rho and likelihood cliff / multimodality)
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding #12 — text says "binomial" but code implements negative binomial)
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding #9 — parameter transformation incomplete; Phi is meaningful only modulo 2pi, periodicity creates unidentified parameterization)

**Findings classification:**
- Finding #1 [Major] NB uses H incorrectly as size parameter: A — AI major, human missed (deeper parameterization flaw, distinct from HI3's text/code discrepancy)
- Finding #2 [Major] H used as both accumulator and distribution parameter; R never tracked: A — AI major, human missed
- Finding #3 [Major] Initial conditions for E and I hard-coded, not estimated: A — AI major, human missed
- Finding #4 [Major] Global search reuses mifs_local[[1]] rather than fresh mif2 calls: A — AI major, human missed
- Finding #5 [Major] Profile likelihood for rho does not properly fix rho: A — AI major, human missed
- Finding #6 [Major] mu_EI and mu_IR fixed without rate unit justification: A — AI major, human missed
- Finding #7 [Moderate] Only a single simulation shown for fit assessment: C — AI minor, human missed
- Finding #8 [Moderate] Convergence diagnostics incomplete for global search: D — AI minor, human also found (matches Human Issue #1)
- Finding #9 [Moderate] Parameter transformation incomplete; Phi meaningful only mod 2pi: D — AI minor, human also found (matches Human Issue #5)
- Finding #10 [Moderate] Profile CI uses raw min/max rather than smooth inversion: C — AI minor, human missed
- Finding #11 [Moderate] No baseline model comparison: C — AI minor, human missed
- Finding #12 [Moderate] Text says "binomial" but code implements negative binomial: D — AI minor, human also found (matches Human Issue #3)
- Finding #13 [Minor] run_level = 2 hard-coded: C — AI minor, human missed
- Finding #14 [Minor] Figure numbering gap: C — AI minor, human missed
- Finding #15 [Minor] Pairwise plots based on only 10 points: C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding #11 — global search box too wide for b1 and b2, explicitly mentions "cliff-like shape of likelihoods seen in Figure 8")
- Human Issue #3: covered (matched by finding #1 — incorrect negative binomial parameterization in measurement model)
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding #1 [Major] Incorrect NB parameterization in measurement model: B — AI major, human also found (matches Human Issue #3)
- Finding #2 [Major] No benchmark comparison: A — AI major, human missed
- Finding #3 [Major] Goodness of fit by single-run visual simulation: A — AI major, human missed
- Finding #4 [Major] Fixed parameters without sensitivity analysis: A — AI major, human missed
- Finding #5 [Major] Profile likelihood only for rho; no CIs for others: A — AI major, human missed
- Finding #6 [Major] Global search initialized from single local search result: A — AI major, human missed
- Finding #7 [Minor] No model diagnostics (ESS, conditional log-likelihood): C — AI minor, human missed
- Finding #8 [Minor] R compartment not tracked; population conservation not verified: C — AI minor, human missed
- Finding #9 [Minor] Conclusion overstates model adequacy: C — AI minor, human missed
- Finding #10 [Minor] Trace plots show slow or incomplete convergence for eta: C — AI minor, human missed
- Finding #11 [Minor] Global search box may be too wide for b1 and b2: D — AI minor, human also found (matches Human Issue #2)
- Finding #12 [Minor] Profile construction has only 15 replicates per rho value: C — AI minor, human missed
- Finding #13 [Minor] Initial conditions for E and I hard-coded, not estimated: C — AI minor, human missed
- Finding #14 [Minor] Only one parameter profile presented: C — AI minor, human missed
- Finding #15 [Minor] No ARIMA/classical time series analysis: C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding #2 — negative binomial parameterization is epidemiologically non-standard)
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding #1 [Major] Global search initialized from previous mif2 result, not base POMP object: A — AI major, human missed
- Finding #2 [Major] Negative binomial parameterization is epidemiologically non-standard and misleading: B — AI major, human also found (matches Human Issue #3)
- Finding #3 [Major] No benchmark comparison against non-mechanistic model: A — AI major, human missed
- Finding #4 [Major] No model diagnostics: A — AI major, human missed
- Finding #5 [Major] Fixed initial conditions are unjustified and potentially influential: A — AI major, human missed
- Finding #6 [Major] Profile likelihood seeds from local-search box, limiting validity: A — AI major, human missed
- Finding #7 [Minor] Accumulator variable records recoveries, not new infections or reports: C — AI minor, human missed
- Finding #8 [Minor] mu_EI and mu_IR fixed at values that deserve justification: C — AI minor, human missed
- Finding #9 [Minor] Profile CI extraction uses raw rho values without enforcing profile max = global max: C — AI minor, human missed
- Finding #10 [Minor] Computational intensity set to run_level = 2: C — AI minor, human missed
- Finding #11 [Minor] Global search box for rho vs profile range mismatch (0.9 vs 0.01–0.50): C — AI minor, human missed
- Finding #12 [Minor] Conclusion claims seasonal pattern captured without quantitative support: C — AI minor, human missed
- Finding #13 [Minor] No assessment of R_0 or other epidemiologically interpretable quantities: C — AI minor, human missed
- Finding #14 [Minor] Pairwise plots for local search based on only 10 points: C — AI minor, human missed
- Finding #15 [Minor] Paper uses single forward simulations (nsim=1) for fit assessment: C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding 21.14.2 [Major] — global mif2 convergence poor, describes chains spending iterations at extreme log-likelihoods before jumping, i.e., the cliff pattern)
- Human Issue #3: covered (matched by finding 21.14.3 [Minor] — rho parameterization and reporting-rate interpretation; identifies dnbinom(cases, H, rho) gives E[cases|H] = H*(1-rho)/rho, not rho*H)
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- 21.14.6 [Major] No non-mechanistic benchmark comparison: A — AI major, human missed
- 21.14.1 [Major] Profile likelihood for rho effectively very sparse near the peak: A — AI major, human missed
- 21.14.2 [Major] Global mif2 convergence poor, especially for Phi; cliff pattern described: B — AI major, human also found (matches Human Issue #2)
- 21.14.7 [Major] No particle filter diagnostics (ESS, conditional log-likelihoods): A — AI major, human missed
- 21.14.5 [Major] Goodness of fit shown by unconditioned forward simulation only: A — AI major, human missed
- 21.14.8 [Major] Initial conditions fixed without justification: A — AI major, human missed
- 21.14.3 [Minor] rho parameterization and reporting-rate interpretation: D — AI minor, human also found (matches Human Issue #3)
- 21.14.4 [Minor] b1/eta identifiability uncharacterized: C — AI minor, human missed
- M1 [Minor] Cooling schedule inheritance in global search: C — AI minor, human missed (mechanistic elaboration of 21.14.2 already matched; separate minor note)
- M2 [Minor] Seasonality assumption not verified in EDA: C — AI minor, human missed
- Conclusion overclaiming [Minor]: C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 5 | 5 | 5 |
| B (AI major, human also found) | 0 | 1 | 1 | 1 |
| C (AI minor, human missed) | 6 | 8 | 9 | 4 |
| D (AI minor, human also found) | 3 | 1 | 0 | 1 |
| E (Human found, AI missed) | 2 | 3 | 4 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Recall = (B+D) / (B+D+E)
AI-Unique Rate = (A+C) / (A+B+C+D)

| Reviewer | B+D | B+D+E | Human Recall | A+C | A+B+C+D | AI-Unique Rate |
|----------|----:|------:|-------------:|----:|---------:|---------------:|
| Alex | 3 | 5 | 60.0% | 12 | 15 | 80.0% |
| Charlie | 2 | 5 | 40.0% | 13 | 15 | 86.7% |
| Doug | 1 | 5 | 20.0% | 14 | 15 | 93.3% |
| Evan | 2 | 5 | 40.0% | 9 | 11 | 81.8% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Global search finds two modes (~10% and ~100% reporting rate), with the second implying susceptible depletion has no dynamic importance, and a hint of a third mode; multimodality not adequately discussed. (Missed by all 4 reviewers)
- Human Issue #4: A section on potential future work would be useful. (Missed by all 4 reviewers)
- Human Issue #5: Phase should be reparameterized to (0, 2pi) to reduce clutter. (Missed by all 4 reviewers)

Count: 3 out of 5 human issues (60%) were missed by every reviewer.

### Unique finds per reviewer

Human issues that only one reviewer covered and all others missed:

- Human Issue #2 (likelihood cliff / hard to distinguish modes): covered by Alex (via finding #8) and by Charlie (via finding #11) and by Evan (via finding 21.14.2) — not uniquely covered by any single reviewer; Doug missed it. This is not a unique find.
- Human Issue #3 (NB vs binomial text/code + overdispersion): covered by Alex (#12), Charlie (#1), Doug (#2), Evan (21.14.3) — covered by all four reviewers; not a unique find.

No human issue was covered by exactly one reviewer. All covered human issues were found by multiple reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

- No benchmark comparison against non-mechanistic model (ARIMA/SARIMA baseline): raised by Alex (#11), Charlie (#2), Doug (#3), Evan (21.14.6) — all four reviewers flagged this as a concern; human did not mention it.
- Single forward simulation used for goodness-of-fit assessment: raised by Alex (#7), Charlie (#3), Doug (#15), Evan (21.14.5) — all four reviewers flagged this; human did not mention it.
- Initial conditions for E and I hard-coded without estimation or justification: raised by Alex (#3), Charlie (#13), Doug (#5), Evan (21.14.8) — all four reviewers flagged this; human did not mention it.
- Global search initialized from local mif2 result rather than fresh/base object: raised by Alex (#4), Charlie (#6), Doug (#1), Evan (21.14.2/M1) — all four reviewers flagged this; human did not mention it.
- No model diagnostics (ESS, conditional log-likelihoods, filtering distribution): raised by Alex (implicitly in #8), Charlie (#7), Doug (#4), Evan (21.14.7) — all four reviewers flagged this; human did not mention it.

Universal AI-only flag count: 5
