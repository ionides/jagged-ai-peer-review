# Ned-Clean Analysis — W21 Project 05

---

## Human Issues

1. Evidence of model misspecification: the perturbed model gets log likelihoods around -300, but as perturbations decrease the likelihood drops and filtering failures (large drops in the estimated likelihood) occur — most likely a result of insufficient process and/or measurement noise.
2. All models use binomial measurement, which is problematic due to bounded support and inability to fit overdispersion; no models included additional noise in the rates.
3. The model is not fully described via mathematical equations; the parameter eta is not defined except by the computer code.
4. Initializing to I=1 seems a strong assumption (though it works out okay here).
5. Reference list is limited to course notes plus the data set source; more context could be added.
6. The likelihood at the initial guess is not scientifically as important as the likelihood after parameter estimation — better to report the latter instead.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding 6: "NaN log-likelihoods accepted without diagnosis — same underlying filtering failure concern")
- Human Issue #2: covered (matched by finding 5: "No overdispersion in measurement model despite clear evidence of need")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding 15: "References section is minimal")
- Human Issue #6: missed

**Findings classification:**
- Finding 1 (No global search): A — no global search; analysis terminates prematurely
- Finding 2 (SIR2 code bug — wrong variable printed): A — copy-paste error prints SIR1 likelihood for SIR2
- Finding 3 (Hard-coded contact-rate reduction not estimated): A — 0.7 multiplier fixed, not learned from data
- Finding 4 (H accumulates recoveries not new infections): A — measurement model accumulates wrong flow
- Finding 5 (No overdispersion — binomial only): B — binomial problematic for overdispersion (matches Human Issue #2)
- Finding 6 (NaN log-likelihoods not diagnosed): B — filtering failures/NaN not investigated (matches Human Issue #1)
- Finding 7 (Only one flu season modeled): A — five seasons in EDA, only one fitted
- Finding 8 (Low Np/Nmif — unstable local search): C — 50 iterations and Np=2000 insufficient
- Finding 9 (Informal model comparison, no AIC): C — no formal criterion for model selection
- Finding 10 (Conclusion contradicts likelihood evidence): C — best loglik is SIR2 but text says SEIR is better
- Finding 11 (Raw counts vs percent positive): C — testing intensity confounds raw count observable
- Finding 12 (No sensitivity analysis for fixed parameters): C — N and 0.7 multiplier fixed without checks
- Finding 13 (SEIR mu_EI implausible — <1 day latency): C — biologically implausible values not discussed
- Finding 14 (Figure captions reference incorrect date ranges): C — caption scope mismatches modeling scope
- Finding 15 (References minimal): D — only data source and course notes cited (matches Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding 6: "Declining or unstable log-likelihood traces attributed to NaN rather than model misspecification")
- Human Issue #2: covered (matched by finding 8: "Binomial measurement model — overdispersion not modeled despite author's own acknowledgment")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding 15: "References are minimal")
- Human Issue #6: missed

**Findings classification:**
- Finding 1 (No global search — analysis stops prematurely): A — global search absent; convergence not demonstrated
- Finding 2 (No profile likelihoods — identifiability unassessed): A — no profiles computed for any model
- Finding 3 (Hard-coded contact-rate reduction not estimated): A — 0.7 factor fixed, research question not answered by inference
- Finding 4 (Wrong likelihood printed for third model): A — sir_L_pf printed instead of sir2_L_pf
- Finding 5 (Large log-likelihood SEs — Monte Carlo noise): A — SEs up to 219 log units, estimates are noise
- Finding 6 (NaN/erratic traces signal model misspecification, not numerical inconvenience): B — filtering failure pattern matches human's diagnosis (matches Human Issue #1)
- Finding 7 (No non-mechanistic benchmark): A — no ARMA or baseline comparison
- Finding 8 (Binomial measurement — overdispersion not modeled): B — same concern as human (matches Human Issue #2)
- Finding 9 (Accumulator H tracks recoveries — semantic mismatch): A — wrong compartment flow accumulated
- Finding 10 (No ARIMA or classical time series analysis): C — no preliminary ARIMA or spectral analysis
- Finding 11 (Single flu season — limited data for parameter estimation): C — 52 observations likely insufficient
- Finding 12 (No model diagnostics — no ESS plots): C — no ESS, no conditional log-likelihood traces
- Finding 13 (`sir` variable assigned but unused — dead code): C — dead code reflects incomplete analysis plan
- Finding 14 (Pairs plots not interpreted): C — wide scatter not discussed as diagnostic
- Finding 15 (References minimal): D — only data source and course notes (matches Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding 8: "Large log-likelihood standard errors indicate particle filter degeneracy")
- Human Issue #2: covered (matched by finding 3: "Binomial measurement model causes structural particle filter collapse")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- Finding 1 (Accumulator H tracks recoveries — fundamental measurement model mismatch): A — wrong compartment flow in all three models
- Finding 2 (Third model displays wrong likelihood — SIR1 value shown for SIR2): A — copy-paste error; SIR2 initial likelihood unreported
- Finding 3 (Binomial measurement causes structural particle filter collapse): B — bounded support and overdispersion failure match human's concern (matches Human Issue #2)
- Finding 4 (No global search — convergence conclusions premature): A — local search only from single starting point
- Finding 5 (Hard-coded 0.7 contact-rate reduction not estimated): A — research question not answered by inference
- Finding 6 (No non-mechanistic benchmark): A — no ARIMA or baseline fitted
- Finding 7 (No profile likelihoods or confidence intervals): A — no identifiability assessment for any model
- Finding 8 (Large log-likelihood SEs — particle filter degeneracy): B — SEs up to 197 log units; filtering failure evidence (matches Human Issue #1)
- Finding 9 (Log-likelihood direction inverted in SEIR conclusion): C — "lowest loglikelihood" should be "highest"
- Finding 10 (SEIR pomp inherits incomplete partrans — mu_EI not transformed): C — mu_EI excluded from parameter transformations in initial fluSEIR object
- Finding 11 (Population N fixed without biological justification): C — total Michigan population used without sensitivity check
- Finding 12 (Week-22 breakpoint chosen by inspection, not justified): C — no external event documented or sensitivity tested
- Finding 13 (No model diagnostics beyond visual overlay): C — no ESS, no conditional log-likelihood plots
- Finding 14 (Only 50 IF2 iterations with Np=2000): C — insufficient computational effort not assessed
- Finding 15 (Research question mismatches analysis performed): C — contact-rate change imposed, not estimated

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: contradiction (Evan m2 says NaN indicates particle collapse, not model misspecification; human says filtering failures are most likely from insufficient process/measurement noise — a model misspecification diagnosis)
- Human Issue #2: covered (matched by M6: "Measurement model uses binomial, which imposes insufficient variance")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by m5: "References are vague and incomplete")
- Human Issue #6: missed

**Findings classification:**
- M1 (No non-mechanistic benchmark): A — no ARMA or baseline log-likelihood for comparison
- M2 (No global search — convergence not demonstrated): A — all runs from single starting point
- M3 (Hard-coded 0.7 contact-rate multiplier not estimated): A — research question unanswered by inference
- M4 (Wrong likelihood printed for Model 3): A — sir_L_pf printed instead of sir2_L_pf
- M5 (No profile likelihoods or confidence intervals): A — identifiability of Beta, eta, rho unassessed
- M6 (Binomial measurement — insufficient variance): B — overdispersion concern matches human (matches Human Issue #2)
- m1 (Sign convention confusion in log-likelihood comparison): C — "lowest loglikelihood" inverts correct direction
- m2 (NaN attributed to model misspecification rather than particle degeneracy): F — contradicts Human Issue #1; human says filtering failures stem from insufficient noise (model misspecification); Evan says NaN is particle collapse, not model misspecification
- m3 (No software version information or sessionInfo): C — reproducibility concern
- m4 (Deprecated R idioms in data processing): C — funs() and guides(color=FALSE) deprecated
- m5 (References vague and incomplete): D — dataset URL and lecture notes unverifiable (matches Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 7 | 6 | 5 |
| B (AI major, human also found) | 2 | 2 | 2 | 1 |
| C (AI minor, human missed) | 7 | 5 | 7 | 3 |
| D (AI minor, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 3 | 3 | 4 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 1 |

---

## Per-Reviewer Metrics

**Human Recall** = (B + D) / (B + D + E)
**AI-Unique Rate** = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | F | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 3 | 0 | 3/6 = 0.500 | 5 | 7 | 12/15 = 0.800 |
| Charlie | 2 | 1 | 3 | 0 | 3/6 = 0.500 | 7 | 5 | 12/15 = 0.800 |
| Doug | 2 | 0 | 4 | 0 | 2/6 = 0.333 | 6 | 7 | 13/15 = 0.867 |
| Evan | 1 | 1 | 3 | 1 | 2/5 = 0.400 | 5 | 3 | 8/10 = 0.800 |

Note: Evan's recall denominator is 5 (6 human issues minus 1 contradiction).

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (E for all, or F for all):

- Human Issue #3 (Model not fully described via math equations; eta undefined except by code): missed by all 4 reviewers. (4 out of 4)
- Human Issue #4 (Initializing to I=1 is a strong assumption): missed by all 4 reviewers. (4 out of 4)
- Human Issue #6 (Initial-guess likelihood is less important than post-estimation likelihood; better to report the latter): missed by all 4 reviewers. (4 out of 4)

**Count: 3 out of 6 human issues were consensus misses (50%).**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

No human issue was uniquely covered by exactly one reviewer. Human issues #1, #2, and #5 were each covered by multiple reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer (A or C for all 4) that the human did not mention:

1. No global search performed (Alex finding 1, Charlie finding 1, Doug finding 4, Evan M2) — all 4 raised this as Major.
2. Hard-coded contact-rate reduction factor not estimated (Alex finding 3, Charlie finding 3, Doug finding 5, Evan M3) — all 4 raised this as Major.
3. Wrong likelihood printed for Model 3 / SIR2 prints SIR1 result (Alex finding 2, Charlie finding 4, Doug finding 2, Evan M4) — all 4 raised this as Major.
4. No profile likelihoods or confidence intervals (Alex finding 1 includes this, Charlie finding 2, Doug finding 7, Evan M5) — all 4 raised this as Major.

**Count: 4 universal AI-only flags.**
