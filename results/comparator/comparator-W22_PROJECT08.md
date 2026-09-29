# Comparator Analysis — W22 Project 08

---

## Human Issues

1. Can the authors explain the particular motivation for studying Turkey? Is there some unusual and favorable feature of data collection, for example? Could the authors add some cultural context to help the reader compare the Turkey pandemic experience to USA. What time of year do Turks typically spend more time inside - summer or winter?

2. The report raises the question of why the SEIREIR model fits worse than ARIMA. Perhaps plotting on a log scale might help. One might see that the fixed initial conditions (especially $I_0=100$) are problematic.

3. The authors also tried to learn the periodicity in data using smoothed periodogram. However, the related plot (smoothed periodogram) is missing in the report.

4. The author stated that "The result shows that ARIMA(2,1,0) is better for the data.". However, the rejection of alternative hypotheses (I assume that is what happened) does not really mean one is better than another but more like choosing alternative over null is not statistically supported.

5. The iterated filtering convergence plots show incomplete convergence: the likelihood continues to go up. This suggests more iterations, and/or a larger random walk standard deviation.

6. More discussion of the parameters corresponding to the MLE (or parameter values with likelihood close to the identified maximum) would be nice to see.

7. Captions for graphs would help the reader.

8. The report does not describe the measurement model, apart from presenting code.

9. Typo: "We fix $N=843400$" should be $84.34 \times 10^6$

10. Typo: "$1/1\mathrm{month}$" should read $1/3\mathrm{month}$ for consistency with the text and code.

11. Proof-reading: grammatical mistakes were distracting for some readers.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "R_b initial condition set to (1-eta)*N — biologically wrong before variant appears")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "log-likelihood comparison between ARIMA and POMP is invalid"; also matched by finding: "conclusion misidentifies POMP log-likelihood and draws incorrect ARIMA comparison")
- Human Issue #5: covered (matched by finding: "small random-walk standard deviations likely impair IF2 convergence")
- Human Issue #6: covered (matched by finding: "no confidence intervals or profile likelihood computed for POMP parameters")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "population value inconsistency — text says N=843400, code uses 84340000")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 [Incorrect outcome variable]: A — observed variable is active cases (stock), not incident cases (flow); model–data mismatch
- Finding 2 [Accumulator H tracks recoveries]: A — H accumulates dN_IR transitions; measurement model linked to recoveries, not new cases
- Finding 3 [Hard-coded seed injection at t=125]: A — deterministic seeding of E_b=10 at t=125 is unjustified and outside the likelihood
- Finding 4 [Invalid ARIMA vs POMP LL comparison]: B — directly comparing log-likelihoods from different model families is invalid (matches Human Issue #4)
- Finding 5 [%do% instead of %dopar%]: A — local search runs sequentially despite parallel backend being registered
- Finding 6 [Global search not reproducible]: A — global search chunk has eval=FALSE and required .RData file is absent
- Finding 7 [Population value inconsistency]: B — text states N=843400 while code uses 84340000, off by factor of 100 (matches Human Issue #9)
- Finding 8 [R_b initialization biologically wrong]: D — R_b = (1-eta)*N places large fraction into variant-recovered compartment at time zero (matches Human Issue #2)
- Finding 9 [Parameter transformation incomplete, small rw_sd]: D — random-walk standard deviations too small relative to parameter scale, likely impairing IF2 convergence (matches Human Issue #5)
- Finding 10 [Hard threshold at t=35 not estimated]: C — government restriction effect modeled by hard-coded day-35 cutoff without estimation or sensitivity analysis
- Finding 11 [EDA plots stock not flow]: C — EDA plots active cases and labels them "daily infected cases"; no incidence series constructed
- Finding 12 [AIC table range too narrow]: C — ARIMA AIC search restricted to P,Q ∈ {0,1,2}; auto.arima result suppressed
- Finding 13 [No CI or profile likelihood]: D — no formal uncertainty quantification around the MLE for any parameter (matches Human Issue #6)
- Finding 14 [ESS interpretation incomplete]: C — ESS plot shown but early collapse not diagnosed as evidence of poor fit or bad initial conditions
- Finding 15 [Conclusion misidentifies POMP LL value]: D — reports -2336 as best log-likelihood but csv achieves -2308.6; invalid ARIMA comparison repeated (matches Human Issue #4)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 4 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "R_b initialized with (1-eta)*N at t=0 — biologically implausible initial conditions")
- Human Issue #3: covered (matched by finding: "periodogram not shown; only referenced as unremarkable")
- Human Issue #4: covered (matched by finding: "ARIMA model selection rationale is inconsistent — AIC and LRT give conflicting signals")
- Human Issue #5: covered (matched by finding: "rw.sd ~10x smaller than course standard"; also matched by finding: "missing convergence diagnostics for the global search")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "population size text vs code inconsistency")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Accumulator H tracks recoveries not infections): A — fundamental measurement model mismatch; no human issue addresses this
- Finding 2 (Invalid direct comparison of ARIMA and POMP log-likelihoods): A — different data transformations invalidate cross-model comparison; no human issue addresses this
- Finding 3 (No profile likelihoods): A — parameter uncertainty entirely unquantified; no human issue addresses this
- Finding 4 (Data construction error: active cases vs. new daily cases): A — cumulative subtraction yields active cases not daily flow; no human issue addresses this
- Finding 5 (R_b initialized with (1-eta)*N at t=0): B — biologically implausible initial conditions (matches Human Issue #2)
- Finding 6 (Ad hoc injection of 10 individuals at t=125): A — arbitrary, unjustified seeding mechanism; no human issue addresses this
- Finding 7 (Missing convergence diagnostics for global search): B — convergence not adequately demonstrated (matches Human Issue #5)
- Finding 8 (rw.sd ~10x smaller than course standard): B — inadequate perturbation magnitude impedes optimization; matches human suggestion of larger rw.sd (matches Human Issue #5)
- Finding 9 (Local search uses %do% not %dopar%): C — performance issue only, correctness unaffected; no human issue addresses this
- Finding 10 (No simulation-based diagnostics beyond visual overlay): C — no ESS, no conditional likelihood plots; no human issue addresses this
- Finding 11 (k fixed without justification): C — overdispersion parameter fixed arbitrarily; no human issue addresses this
- Finding 12 (Population size text vs code inconsistency): D — text says 843400, code uses 84340000 (matches Human Issue #9)
- Finding 13 (ARIMA model selection rationale inconsistent): D — AIC selects ARIMA(2,1,1) but LRT used to choose ARIMA(2,1,0) without justification (matches Human Issue #4)
- Finding 14 (No ARMA benchmark on raw series): C — direct POMP benchmark comparison requires undifferenced model; no human issue addresses this
- Finding 15 (Periodogram not shown): D — spectrum() call has include=FALSE, claim of no periodicity unverifiable (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Biologically implausible initial conditions for beta-variant compartment")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Model selection by LRT between ARIMA(2,1,1) and ARIMA(2,1,0) is applied incorrectly")
- Human Issue #5: covered (matched by finding: "Insufficient number of IF2 iterations — Nmif=50 insufficient, convergence traces confirm eta has not stabilized")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Population figure error in text — N=843400 stated but Turkey's population is 84.3 million")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major #1 (Fundamental mismatch between data variable and accumulator — active cases stock vs. new-recoveries flow): A
- Major #2 (Accumulator H tracks recoveries dN_IR, not new detections dN_EI): A
- Major #3 (Global search initialized from previous mif2 object, inheriting exhausted cooling schedule): A
- Major #4 (Global search box excludes region containing best-fit parameters): A
- Major #5 (Reported log-likelihood -2336 inconsistent with stored artifacts showing -2308.63): A
- Major #6 (Invalid log-likelihood comparison between ARIMA and SEIREIR — different distributional families on different data transformations): A
- Major #7 (No profile likelihoods and no parameter confidence intervals): A
- Major #8 (Biologically implausible initial conditions — R_b set to ~75.9 million at time zero for a variant not yet in existence): B — (matches Human Issue #2)
- Minor: Population figure error in text (N=843400 stated, should be 84,340,000): D — (matches Human Issue #9)
- Minor: Local search uses %do% (sequential) instead of %dopar% (parallel): C
- Minor: Global search uses Np=1000, local uses Np=2000, no justification: C
- Minor: Hard-coded beta-variant emergence at t=125 without justification: C
- Minor: No model diagnostics reported (no conditional log-likelihood plots, no ESS monitoring): C
- Minor: Insufficient IF2 iterations — Nmif=50, convergence traces confirm eta has not stabilized: D — (matches Human Issue #5)
- Minor: Model selection by LRT between ARIMA(2,1,1) and ARIMA(2,1,0) applied incorrectly — reasoning that non-rejection means "better" is flawed: D — (matches Human Issue #4)
- Minor: Notation inconsistency — equations use continuous-time differentials but implementation uses discrete-time Euler steps: C
- Minor: Code availability issue — local.RData referenced but absent from project folder: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.08.4 — biologically implausible initial condition R_b = (1-eta)*N at t=0")
- Human Issue #3: covered (matched by finding: "22.08.m5 — periodogram figure appears missing")
- Human Issue #4: covered (matched by finding: "22.08.m6 — ARIMA model selection: AIC and LRT disagree without explanation")
- Human Issue #5: covered (matched by finding: "22.08.5 — optimization has not converged")
- Human Issue #6: covered (matched by finding: "22.08.3 — no profile likelihoods or confidence intervals")
- Human Issue #7: covered (matched by finding: "22.08.m7 — figure captions are absent throughout")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "22.08.m1 — population figure inconsistency, N=843400 vs 84,340,000")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- 22.08.1: A — measurement model mismatch: H tracks recoveries but data is new daily confirmed cases
- 22.08.2: A — ARIMA and POMP log-likelihoods are not directly comparable across different observation representations
- 22.08.3: B — no profile likelihoods or confidence intervals computed (matches Human Issue #6)
- 22.08.4: B — biologically implausible initial condition: R_b = (1-eta)*N at t=0 before beta variant existed (matches Human Issue #2)
- 22.08.5: B — optimization has not converged; also mu_IR_o inconsistency across code blocks (matches Human Issue #5)
- 22.08.m1: D — population figure inconsistency: text states N=843400, code uses 84,340,000 (matches Human Issue #9)
- 22.08.m2: C — beta variant seed of 10 individuals at t=125 is hard-coded without sensitivity analysis
- 22.08.m3: C — ESS collapses near zero during days 5–25, implications not discussed
- 22.08.m4: C — simulation envelope far exceeds observed data range, model not tightly calibrated
- 22.08.m5: D — periodogram figure missing despite being referenced in text (matches Human Issue #3)
- 22.08.m6: D — ARIMA model selection: AIC favors ARIMA(2,1,1) but LRT leads to ARIMA(2,1,0) with no rationale for preference (matches Human Issue #4)
- 22.08.m7: D — figure captions absent throughout (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 4 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 5 | 7 | 2 |
| B (AI major, human also found) | 2 | 3 | 1 | 3 |
| C (AI minor, human missed) | 4 | 4 | 6 | 3 |
| D (AI minor, human also found) | 4 | 3 | 3 | 4 |
| E (Human found, AI missed) | 6 | 6 | 7 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 4 | 6 | 5/11 = 45% | 5 | 4 | 9/15 = 60% |
| Charlie | 3 | 3 | 6 | 5/11 = 45% | 5 | 4 | 9/15 = 60% |
| Doug | 1 | 3 | 7 | 4/11 = 36% | 7 | 6 | 13/17 = 76% |
| Evan | 3 | 4 | 4 | 7/11 = 64% | 2 | 3 | 5/12 = 42% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Can the authors explain the particular motivation for studying Turkey? Is there some unusual and favorable feature of data collection, for example? Could the authors add some cultural context to help the reader compare the Turkey pandemic experience to USA. What time of year do Turks typically spend more time inside - summer or winter? (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The report does not describe the measurement model, apart from presenting code. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: Typo: "$1/1\mathrm{month}$" should read $1/3\mathrm{month}$ for consistency with the text and code. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: Proof-reading: grammatical mistakes were distracting for some readers. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 11 human issues (36%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #7: Captions for graphs would help the reader. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
