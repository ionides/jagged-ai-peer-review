# Ned-Clean Analysis — W25 Project 13

---

## Human Issues

1. The project has major presentation issues with incomplete sections, e.g., text like "tweaked for a typical exoplanet study—let me know if your bounds differ" that looks GenAI generated.
2. The DEoptim description reads like GenAI text ("This method is perfect...," "It's fantastic...").
3. DEoptim is used instead of class methods, with no benchmarks and no serious discussion of convergence diagnostics beyond an assertion — possibly avoiding mastery of class material.
4. "Simulated trajectories follow the general pattern of the observed data" does not match the figure, where simulated trajectories oscillate rapidly unlike the data.
5. The source code has hard-coded fabricated results ("Note: I made up these numbers based on typical patterns—swap in your actual log-likelihood values if you have them!").
6. It would be good to have statistical benchmark models (e.g., a suitable regression model) to assess quality of fit.
7. The residual plot/histogram show clear seasonal patterns with periodicity ~400, and the ACF plot has very large values for all of the first 50 lags, totally inconsistent with the author's interpretations — indicating severe residual autocorrelation and model assumption violations.
8. Many repetitions of symbols in equations make the report harder to read.
9. Only Figure 1 is numbered, but elsewhere there are references to Fig. 2, Fig. 3, etc., which are not numbered.
10. No evidence is provided that the DEoptim algorithm converged ("converged to a best log-likelihood of -151017.163, demonstrating effective optimization over 50 iterations").
11. Technical terms like BKJD need clear explanations for readers without specialized astronomical knowledge.
12. The transit model equation is presented redundantly (multiple times with slight variations), creating unnecessary confusion.
13. Multiple nonsensical uses of "your" make it look like the writing was GenAI-produced.
14. The reference to Rappaport et al. (2012) does not exist — it appears to be a GenAI hallucination.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Log-likelihood values explicitly fabricated")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Log-likelihood decreases across iterations — optimization direction wrong, no evidence of convergence")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Writing quality poor — second-person address, informal language, typos")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 [CRITICAL — fabricated log-likelihood]: B (matches Human Issue #5)
- Finding 2 [CRITICAL — LL decreases, optimization direction wrong]: B (matches Human Issue #10)
- Finding 3 [CRITICAL — delta.t=1 mismatched with data cadence]: A
- Finding 4 [CRITICAL — TCE disposition "Unknown" not "CANDIDATE"]: A
- Finding 5 [CRITICAL — p_1 misinterpreted as probability]: A
- Finding 6 [MAJOR — preliminary plot labels data misleadingly]: A
- Finding 7 [MAJOR — absolute file paths hard-coded]: A
- Finding 8 [MAJOR — batman Python package unused]: A
- Finding 9 [MAJOR — no uncertainty quantification / profile likelihoods]: A
- Finding 10 [MAJOR — transit duration 5.44 days physically implausible]: A
- Finding 11 [MAJOR — "32 days" vs 11.2 days internal inconsistency]: A
- Finding 12 [MODERATE — kepid selection fragile and non-reproducible]: C
- Finding 13 [MODERATE — Np=1000 insufficient for ~71,000 observations]: C
- Finding 14 [MODERATE — residuals computed from single stochastic OU draw]: C
- Finding 15 [MINOR — writing quality, typos, informal language]: D (matches Human Issue #13)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "DEoptim applied to stochastic pfilter — cost function is a random variable, not valid inference")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Fabricated placeholder log-likelihood values reported as genuine results")
- Human Issue #6: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "No convergence diagnostics")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Writing quality — informal phrasings, typos, second-person address")
- Human Issue #14: missed

**Findings classification:**
- Major #1 [Fabricated placeholder log-likelihood]: B (matches Human Issue #5)
- Major #2 [DEoptim on stochastic pfilter — random cost function]: B (matches Human Issue #3)
- Major #3 [No non-mechanistic benchmark]: B (matches Human Issue #6)
- Major #4 [No quantitative goodness-of-fit / no AIC]: A
- Major #5 [No convergence diagnostics]: B (matches Human Issue #10)
- Major #6 [No profile likelihoods / no uncertainty quantification]: A
- Major #7 [Hard-coded absolute paths prevent reproduction]: A
- Major #8 [Simulated flux used as validation without filtering distribution]: A
- Major #9 [Internal contradictions in parameter reporting — 32 days vs 11.2, p_1 inconsistency]: A
- Major #10 [delta.t=1 time step inconsistency with data cadence]: A
- Minor — Writing quality (informal phrasings, typos, second-person): D (matches Human Issue #13)
- Minor — p_1 misinterpreted as probability: C
- Minor — Residuals plot color (yellow on white background, invisible): C
- Minor — batman Python dependency unused: C
- Minor — pomp/spatPomp versions not pinned: C
- Minor — No README: C
- Minor — No random seeds set before DEoptim: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "DEoptim wrapping pfilter is not valid inference for stochastic POMP models")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Fabricated log-likelihood values and internal contradictions in LL direction")
- Human Issue #6: covered (matched by finding: "No benchmark comparison against non-mechanistic model")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Computational adequacy not demonstrated; no convergence diagnostics")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Writing quality and placeholder text — informal language, typos")
- Human Issue #14: missed

**Findings classification:**
- Major #1 [DEoptim wrapping pfilter not valid for stochastic POMP]: B (matches Human Issue #3)
- Major #2 [Fabricated LL + LL decreasing + internal contradictions]: B (matches Human Issue #5)
- Major #3 [No benchmark comparison]: B (matches Human Issue #6)
- Major #4 [Goodness-of-fit assessed only visually; no log-likelihood or AIC]: A
- Major #5 [No parameter identifiability / no confidence intervals]: A
- Major #6 [p_1 conceptual misuse as "probability of true exoplanet signal"]: A
- Major #7 [delta.t=1 inconsistent with data sampling interval]: A
- Major #8 [No convergence diagnostics / computational adequacy not demonstrated]: B (matches Human Issue #10)
- Major #9 [Hard-coded absolute paths and Python dependency]: A
- Minor #10 [OU discretization step hard-coded instead of using dt]: C
- Minor #11 [Internal contradictions — 32 days vs 11.2, p_1 0.46 vs 0.07]: C
- Minor #12 [No model diagnostics beyond residual plots — ESS, filtering distribution]: C
- Minor #13 [Boxcar transit duration 5.44 days implausibly long]: C
- Minor #14 [Writing quality and placeholder text — informal language, typos]: D (matches Human Issue #13)
- Minor #15 [Detrending applied before POMP setup but measurement model uses original error]: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Particle filter role in DEoptim optimization undocumented — unclear whether genuine POMP inference is performed")
- Human Issue #4: covered (matched by finding: "Simulated trajectories show implementation artifacts — sharp vertical jumps inconsistent with smooth OU dynamics")
- Human Issue #5: covered (matched by finding: "Fabricated log-likelihood values and degrading optimization")
- Human Issue #6: covered (matched by finding: "No benchmark comparison against non-mechanistic models")
- Human Issue #7: covered (matched by finding: "ACF of residuals contradicts text description — ACF ~0.95-1.0 at lags 1-5, text claims minimal autocorrelation")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "No uncertainty quantification — no multiple restarts documented to verify convergence")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Writing quality and typos")
- Human Issue #14: missed

**Findings classification:**
- Point 25.13.2 [Fabricated log-likelihood + degrading optimization — MAJOR]: B (matches Human Issue #5)
- Point 25.13.3 [ACF of residuals contradicts text — MAJOR]: B (matches Human Issue #7)
- Point 25.13.4 [Transit depth δ1=0.47 physically implausible — MAJOR]: A
- Point 25.13.1 [Particle filter role in DEoptim undocumented — MAJOR]: B (matches Human Issue #3)
- Point 25.13.7 [Phase-folded light curve shows no transit signal — MAJOR]: A
- Point 25.13.5 [No benchmark comparison — MAJOR]: B (matches Human Issue #6)
- Point 25.13.6 [Time-step mismatch corrupts OU discretization — MAJOR]: A
- Minor — p1 parameter inconsistency (0.076 vs "set to 1.0"): C
- Minor — Writing quality and typos: D (matches Human Issue #13)
- Minor — Simulated trajectories show implementation artifacts (sharp vertical jumps): D (matches Human Issue #4)
- Minor — No uncertainty quantification (no CIs, no multiple restarts for convergence): D (matches Human Issue #10)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 1 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 9 | 6 | 5 | 3 |
| B (AI major, human also found) | 2 | 4 | 4 | 4 |
| C (AI minor, human missed) | 3 | 6 | 5 | 1 |
| D (AI minor, human also found) | 1 | 1 | 1 | 3 |
| E (Human found, AI missed) | 11 | 9 | 9 | 7 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+11) = 3/14 = 0.214
- AI-Unique Rate = (A+C) / (A+B+C+D) = (9+3) / (9+2+3+1) = 12/15 = 0.800

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (4+1) / (4+1+9) = 5/14 = 0.357
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+6) / (6+4+6+1) = 12/17 = 0.706

**Doug**
- Human Recall = (B+D) / (B+D+E) = (4+1) / (4+1+9) = 5/14 = 0.357
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+5) / (5+4+5+1) = 10/15 = 0.667

**Evan**
- Human Recall = (B+D) / (B+D+E) = (4+3) / (4+3+7) = 7/14 = 0.500
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+1) / (3+4+1+3) = 4/11 = 0.364

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: GenAI presentation with incomplete sections ("let me know if your bounds differ") — missed by Alex, Charlie, Doug, Evan
- Human Issue #2: DEoptim description reads like GenAI text ("This method is perfect...," "It's fantastic...") — missed by Alex, Charlie, Doug, Evan
- Human Issue #8: Many repetitions of symbols in equations make the report harder to read — missed by Alex, Charlie, Doug, Evan
- Human Issue #9: Only Figure 1 is numbered; references to Fig. 2, Fig. 3, etc., are unnumbered — missed by Alex, Charlie, Doug, Evan
- Human Issue #11: Technical terms like BKJD need clear explanations — missed by Alex, Charlie, Doug, Evan
- Human Issue #12: Redundant presentation of the transit model equation — missed by Alex, Charlie, Doug, Evan
- Human Issue #14: Rappaport et al. (2012) reference does not exist (GenAI hallucination) — missed by Alex, Charlie, Doug, Evan

**Count: 7 out of 14 human issues were missed by every reviewer.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #4 (simulated trajectories don't match figure): covered only by Evan
- Human Issue #7 (residual ACF very large values, inconsistent with author's interpretation): covered only by Evan

**Alex:** 0 unique finds
**Charlie:** 0 unique finds
**Doug:** 0 unique finds
**Evan:** 2 unique finds (Human Issues #4, #7)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 2 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

- delta.t=1 time-step mismatch between the OU process discretization and the actual Kepler data cadence (~0.02 days): raised by Alex (Finding 3, CRITICAL), Charlie (Major #10), Doug (Major #7), Evan (Point 25.13.6, MAJOR)

**Count: 1 issue raised by every reviewer that the human did not mention.**
