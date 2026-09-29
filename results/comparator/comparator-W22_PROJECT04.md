# Comparator Analysis — W22 Project 04

---

## Human Issues

1. Best not to describe weekly periodicity as "seasonality". Outside of the technical use of seasonality in SARMA models, seasonality corresponds to annual cycles.

2. Figure captions would be helpful. For the simulations, the blue line is presumably the data, but this is not described.

3. Diagnostics show a difficulty explaining the resurgence at the end of the data (low effective sample size) but this may not be too critical.

4. The fits around the MLE have a very high reporting rate, close to 1. How do you interpret that?

5. It would be good to compare the likelihood (equivalently, AIC) between the mechanistic model and the ARMA benchmark. In this case, it appears ARMA does somewhat better - maybe showing potential room for improvement in the model.

6. Typo: "$I_t$: the number of recovered at time $t$"

7. Spell checking: e.g., "pubilic", and "casual" for "causal".

8. The plot titled "differenced data" is differenced log data, but the ACF next to it is unlogged data. None of this is apparent unless you study the source code.

9. Referencing observations by date not observation number would be easier to understand.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "rho converges near 1; identifiability between alpha and rho never discussed")
- Human Issue #5: covered (matched by finding: "likelihood benchmark comparison is missing")
- Human Issue #6: covered (matched by finding: "I_t listed twice in state description; second entry should be R_t")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (dN_RS drawn from I not R): A — critical bug: recovery-to-susceptible transition samples from wrong compartment, breaking reinfection mechanism
- Finding 2 (nearbyint breaks integer conservation): A — critical bug: non-conservative compartment split allows individuals to be created or destroyed
- Finding 3 (H accumulates dN_IR only; rho near 1): B — rho converges near 1 and identifiability with alpha is unaddressed (matches Human Issue #4)
- Finding 4 (time-varying beta with ad hoc breakpoints): A — major: 6 hard-coded breakpoints lack epidemiological justification or sensitivity analysis
- Finding 5 (key parameters fixed without justification): A — major: mu_PR, mu_IR, alpha, Beta fixed with no cited sources
- Finding 6 (mu_RS circular reasoning): A — major: parameter fixed at local MLE then used in global search
- Finding 7 (no profile likelihood or confidence intervals): A — major: no uncertainty quantification for any estimated parameter
- Finding 8 (likelihood benchmark comparison missing): B — POMP log-likelihood never compared to SARIMA or null model (matches Human Issue #5)
- Finding 9 (initial conditions hard-coded): C — moderate: E, I, P fixed constants not estimated from data
- Finding 10 (I_t copy-paste error): D — I_t listed twice in state table; second entry should be R_t (matches Human Issue #6)
- Finding 11 (spectral analysis on non-stationary series): C — moderate: spectrum applied to original trending series rather than differenced data
- Finding 12 (particle filter SE very large at start): C — moderate: SE=78.32 at initial parameters indicates filter failure at that point
- Finding 13 (global search uses only 10 starting points): C — moderate: weak coverage of 9-dimensional parameter space
- Finding 14 (SARIMA model selection incomplete): C — minor: seasonal component held fixed; no exploration of alternative seasonal orders
- Finding 15 (introduction data description mismatch): C — minor: plot description does not match the actual analysis window

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by findings: "No non-mechanistic benchmark comparison" and "AIC comparison between SARIMA and POMP not addressed")
- Human Issue #6: covered (matched by finding: "Typographical error: $I_t$ defined twice")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (dN_RS drawn from I instead of R): A — critical bug in R→S transition compartment
- Finding 2 (R compartment never decreases): A — critical bug; population conservation violated
- Finding 3 (accumulator H tracks recoveries not new infections): A — critical bug in measurement model
- Finding 4 (eta missing from parameter transformation): A — eta perturbed on natural scale without constraint
- Finding 5 (no profile likelihoods): A — no profile likelihoods computed for any parameter
- Finding 6 (many parameters fixed without justification): A — mu_PR, mu_IR, alpha, Beta, mu_RS fixed ad hoc
- Finding 7 (no non-mechanistic benchmark comparison): B — POMP vs SARIMA comparison absent (matches Human Issue #5)
- Finding 8 (insufficient global search replicates): A — only 10 replicates instead of standard 100
- Finding 9 (typographical error: $I_t$ defined twice): B — second definition should be $R_t$ (matches Human Issue #6)
- Finding 10 (AIC comparison between SARIMA and POMP not addressed): D — paper asserts both fit well without formal comparison (matches Human Issue #5)
- Finding 11 (spectral frequency/period calculation not shown): C — 0.13 cycles/day claim undocumented, units unclear
- Finding 12 (convergence of mu_EPI acknowledged but not addressed): C — convergence problem noted and ignored
- Finding 13 (initial conditions for E, I, P fixed without justification): C — arbitrary round numbers used, no sensitivity analysis
- Finding 14 (residual diagnostics for SARIMA not interpreted fully): C — non-normality dismissed, no Ljung-Box test
- Finding 15 (intervention period indicator gap at time step 35): C — one-day anomaly in intervention schedule undiscussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Model diagnostics (ESS) not examined")
- Human Issue #4: covered (matched by finding: "rho near 1 interpretation")
- Human Issue #5: covered (matched by findings: "No benchmark comparison" and "Direct comparison of SARIMA/POMP log-likelihoods invalid")
- Human Issue #6: covered (matched by finding: "Typo in state variable description")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major 1 (rprocess bug: dN_RS draws from I instead of R): A — critical coding error invalidating all inference
- Major 2 (No benchmark comparison): B — no quantitative comparison of SARIMA and POMP on same scale (matches Human Issue #5)
- Major 3 (Direct comparison of SARIMA/POMP log-likelihoods invalid): B — different observation models on different data transformations make numerical comparison invalid (matches Human Issue #5)
- Major 4 (No profile likelihoods): A — parameter identifiability not assessed for any parameter
- Major 5 (Multiple key parameters fixed without justification): A — five parameters fixed with no cited sources or sensitivity analysis
- Major 6 (Insufficient computational scale; convergence not demonstrated): A — only 10 replicates; mu_EPI convergence problem acknowledged but not addressed
- Major 7 (Accumulator H tracks wrong flow): A — H accumulates dN_IR (recoveries) instead of new infections
- Major 8 (Measurement model: normal approximation issues): A — non-positive support and particle degeneracy when H=0
- Major 9 (Global search excludes mu_RS; fixed at local search value): A — circular search and biologically implausible immunity half-life
- Major 10 (Model diagnostics: ESS not examined): B — particle filter failure not investigated; no conditional log-likelihoods per observation (matches Human Issue #3)
- Minor (Typo in state variable description): D — second bullet labeled $I_t$ should be $R_t$ (matches Human Issue #6)
- Minor (Intervention indicator gap at time 35): C — loop leaves i=35 with unintended value
- Minor (rho near 1 interpretation): D — rho near 1 misinterpreted due to accumulator error (matches Human Issue #4)
- Minor (No out-of-sample validation or forecast): C — no forecast presented despite policy relevance
- Minor (Initial conditions largely fixed): C — E=100, I=200, P=50 hard-coded with no sensitivity analysis

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.04.M4 — Simulation plots lack labeled observed data overlay")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "22.04.3 — Profile likelihoods absent; no confidence intervals — calls out rho≈1 as needing scrutiny")
- Human Issue #5: covered (matched by finding: "22.04.2 — No quantitative SARIMA vs. POMP comparison")
- Human Issue #6: covered (matched by finding: "22.04.M1 — Notation error: R_t mislabeled as I_t")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- 22.04.1: A — Code bug: dN_RS drawn from I instead of R
- 22.04.2: B — No quantitative SARIMA vs. POMP comparison (matches Human Issue #5)
- 22.04.3: B — Profile likelihoods absent; no confidence intervals; calls out rho≈1 as needing justification (matches Human Issue #4)
- 22.04.4: A — mif2 log-likelihood not confirmed by replicated pfilter
- 22.04.5: A — Global search under-sampled (~5–10 points)
- 22.04.6: A — Initial conditions E, I, P hard-coded without justification
- 22.04.M1: D — Notation error: R_t mislabeled as I_t (matches Human Issue #6)
- 22.04.M2: C — mu_RS biological plausibility
- 22.04.M3: C — Gaussian measurement model allows negative counts
- 22.04.M4: D — Simulation plots lack labeled observed data overlay (matches Human Issue #2)
- 22.04.M5: C — SARIMA residuals show heteroscedasticity; log-transform not considered
- 22.04.M6: C — Seasonal differencing order D not stated
- 22.04.M7: C — Forward simulation vs. filtering distribution distinction not acknowledged

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 7 | 7 | 4 |
| B (AI major, human also found) | 2 | 2 | 3 | 2 |
| C (AI minor, human missed) | 6 | 5 | 3 | 5 |
| D (AI minor, human also found) | 1 | 1 | 2 | 2 |
| E (Human found, AI missed) | 6 | 7 | 5 | 5 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 6 | 3/9 = 33% | 6 | 6 | 12/15 = 80% |
| Charlie | 2 | 1 | 7 | 2/9 = 22% | 7 | 5 | 12/15 = 80% |
| Doug | 3 | 2 | 5 | 4/9 = 44% | 7 | 3 | 10/15 = 67% |
| Evan | 2 | 2 | 5 | 4/9 = 44% | 4 | 5 | 9/13 = 69% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Best not to describe weekly periodicity as "seasonality". Outside of the technical use of seasonality in SARMA models, seasonality corresponds to annual cycles. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: Spell checking: e.g., "pubilic", and "casual" for "causal". (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The plot titled "differenced data" is differenced log data, but the ACF next to it is unlogged data. None of this is apparent unless you study the source code. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: Referencing observations by date not observation number would be easier to understand. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 9 human issues (44%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: Figure captions would be helpful. For the simulations, the blue line is presumably the data, but this is not described. (Covered only by Evan)
- Human Issue #3: Diagnostics show a difficulty explaining the resurgence at the end of the data (low effective sample size) but this may not be too critical. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 1 |
