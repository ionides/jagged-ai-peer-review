# Comparator Analysis — W25 Project 13

---

## Human Issues

1. There are major issues with how the project is presented. Various things are incomplete in strange ways, e.g., "(tweaked for a typical exoplanet study—let me know if your bounds differ)", that look GenAI generated.

2. The passage describing the DEoptim algorithm reads like GenAI text (e.g., "This method is perfect for handling complex, non-linear, and multi-modal likelihood surfaces ... Why DEoptim? It's fantastic at finding the global maximum...").

3. The use of DEoptim rather than methods studied in class raises questions. There are no benchmarks and no serious discussion of convergence diagnostics beyond an assertion that the search was effective. The project could be avoiding mastery of material covered in class, rather than improving on it.

4. "Simulated trajectories follow the general pattern of the observed data" does not seem to match the figure, where the simulated trajectories oscillate rapidly, unlike the data.

5. The source code has hard-coded results described as "Note: I made up these numbers based on typical patterns—swap in your actual log-likelihood values if you have them!" In various places, the results appear to have been fabricated.

6. It would be good to have statistical benchmark models to help assess the quality of fit from the likelihood of the mechanistic model. A suitable regression model could be appropriate even if ARMA is not.

7. The residual plot and residual histogram are inappropriately interpreted despite very clear seasonal patterns with periodicity approximately 400. The ACF plot shows very large autocorrelation values for all of the first 50 lags, which is totally inconsistent with the author's interpretations and indicates severe residual autocorrelation and violation of residual assumptions.

8. There are many repetitions of symbols in the equations which make the report harder to read.

9. Only Figure 1 is numbered, but elsewhere there are references to Fig. 2, Fig. 3, etc., which are not numbered.

10. The claim that the algorithm "converged to a best log-likelihood of -151017.163 ... demonstrating effective optimization over 50 iterations" is not supported — there is no evidence that the algorithm converged.

11. Technical terms like BKJD (Barycentric Kepler Julian Date) need clear explanations for readers without specialized astronomical knowledge.

12. The redundant presentation of the transit model equation (appearing multiple times with slight variations) creates unnecessary confusion.

13. Multiple nonsensical uses of "your" make it look like the writing was produced to a considerable extent by GenAI.

14. The reference "Rappaport, S., Levine, A., Chiang, E., El Mellah, I., Jenkins, J. M., Kaltenegger, L., … & Villasenor, J. (2012). 'Light-curve Analysis of KIC 12557548b: An Extrasolar Planet with a Comet-like Tail.' The Astrophysical Journal, 752(1), 1." does not exist as cited. This error looks like a GenAI hallucination and is a serious scholarly concern.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Writing quality — informal/GenAI language including second-person address like 'In your implementation'")
- Human Issue #2: covered (matched by finding: "Writing quality — informal/GenAI language including phrases like 'It's fantastic'")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Log-likelihood values are explicitly fabricated")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Log-likelihood decreases rather than improves across iterations")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Writing quality — informal/GenAI language including second-person address like 'In your implementation'")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (Fabricated log-likelihood values): B — log-likelihood values acknowledged as made up (matches Human Issue #5)
- Finding 2 (Log-likelihood decreases across iterations): B — optimization moves in wrong direction, convergence claim unsupported (matches Human Issue #10)
- Finding 3 (delta.t = 1 mismatched with data resolution): A — OU step size of 1 day wrong for ~0.02-day cadence data
- Finding 4 (TCE disposition "Unknown" not "CANDIDATE"): A — scientific conclusion rests on unverified premise
- Finding 5 (p_1 misinterpreted as detection probability): A — p_1 is a depth-scaling factor, not a probability
- Finding 6 (Preliminary plot labels misleading): A — processed data labeled as detrended before detrending occurs
- Finding 7 (Hard-coded absolute file paths): A — non-portable paths prevent reproducibility
- Finding 8 (batman package imported but never used): A — unnecessary dependency that can break compilation
- Finding 9 (No uncertainty quantification): A — no confidence intervals, profile likelihoods, or bootstrap
- Finding 10 (Transit duration physically implausible): A — 5.44-day transit out of 11.2-day period is ~48% of orbit
- Finding 11 (Internal inconsistency: 32 days vs. 11.2 days): A — wrong period value cited in concluding paragraph
- Finding 12 (kepid selection fragile): C — selection by first star with multiple TCEs is non-deterministic
- Finding 13 (Np = 1000 too low for ~71,000 observations): C — particle filter variance too large for reliable likelihood estimates
- Finding 14 (Residuals from single stochastic OU draw): C — proper residual analysis requires filtering-based expected states or averaged simulations
- Finding 15 (Writing quality poor throughout): D — typos, informal phrasing, second-person address, inconsistent figure references (matches Human Issues #1, #2, and #13)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Writing quality: colloquial language, typos, and unrevised placeholder text — including 'your implementation' and 'your specific model' language")
- Human Issue #2: covered (matched by finding: "Writing quality: colloquial language, typos, and unrevised placeholder text — including 'fantastic at' and other GenAI-sounding phrasing about DEoptim")
- Human Issue #3: covered (matched by finding: "No convergence diagnostics for the optimization" and "DEoptim applied to stochastic particle filter likelihood without justification")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Authors explicitly admit fabricated quantitative results")
- Human Issue #6: covered (matched by finding: "No benchmark comparison")
- Human Issue #7: covered (matched by finding: "Residual analysis computed from ad hoc single OU simulation, not particle filter — claims of no significant autocorrelation are not statistically meaningful")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Reported log-likelihood shows optimization divergence, mischaracterized as improvement" and "No convergence diagnostics for the optimization")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Writing quality: colloquial language, typos, and unrevised placeholder text — 'your implementation'/'your specific model' addressing reader as tutorial")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (Fabricated quantitative results): B — authors admit "I made up these numbers"; explicit fabrication (matches Human Issue #5)
- Finding 2 (Log-likelihood divergence mischaracterized as improvement): B — log-likelihood worsened from -129990 to -151017 yet claimed as improvement (matches Human Issue #10)
- Finding 3 (Single particle filter evaluation, no logmeanexp): A — optimizer chases Monte Carlo noise; not raised by human
- Finding 4 (No convergence diagnostics): B — no trace plots, no multi-start evidence (matches Human Issues #3 and #10)
- Finding 5 (DEoptim applied to stochastic likelihood without justification): B — DEoptim treats objective as deterministic; choice over mif2 unjustified (matches Human Issue #3)
- Finding 6 (No benchmark comparison): B — no ARMA or IID model comparison (matches Human Issue #6)
- Finding 7 (No profile likelihoods): A — parameter identifiability unassessed; not raised by human
- Finding 8 (Residual analysis from single OU simulation, not particle filter): B — conclusions about no autocorrelation drawn from a single stochastic realization (matches Human Issue #7)
- Finding 9 (Hard-coded absolute paths prevent reproducibility): A — paths specific to author's machine; not raised by human
- Finding 10 (Internal contradictions in parameter estimates): C — P_1 = 11.20 days vs. "approximately 32 days"; not raised by human
- Finding 11 (OU step hardcodes time step to 1.0): C — bypasses pomp's delta.t variable; not raised by human
- Finding 12 (p_1 misidentified as detection probability): C — scaling factor mischaracterized as false-positive probability; not raised by human
- Finding 13 (Residuals plotted in yellow on white background): C — unreadable plot; not raised by human
- Finding 14 (Writing quality: colloquial language, typos, unrevised placeholder text): D — "fantastic at," "your implementation," "super important," spelling errors (matches Human Issues #1, #2, and #13)
- Finding 15 (No cluster environment or computational cost information): C — makeCluster(36) undocumented; not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 6 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Writing quality and placeholder text — informal language, nonsensical 'your' uses, placeholder text")
- Human Issue #2: covered (matched by finding: "Writing quality and placeholder text — explicit quote of 'It's fantastic at finding the global maximum'")
- Human Issue #3: covered (matched by findings: "DEoptim wrapping pfilter is not valid inference"; "No benchmark comparison"; "Computational adequacy not demonstrated; no convergence diagnostics")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Fabricated log-likelihood values and internal contradictions — explicit 'I made up these numbers' placeholder")
- Human Issue #6: covered (matched by finding: "No benchmark comparison against a non-mechanistic model")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by findings: "Fabricated log-likelihood values — -151017 is worse than -129990 yet described as convergence"; "Computational adequacy not demonstrated; no convergence diagnostics")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Writing quality and placeholder text — nonsensical 'your' uses and informal language")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (DEoptim wrapping pfilter is not valid inference): B — DEoptim minimizes a stochastic pfilter objective, which is methodologically invalid; mif2 is the correct approach (matches Human Issue #3)
- Finding 2 (Fabricated log-likelihood values and internal contradictions): B — results section contains explicit "I made up these numbers" placeholder; -151017 is worse than -129990 yet described as improvement (matches Human Issues #5 and #10)
- Finding 3 (No benchmark comparison): B — no ARMA, GP, or other non-mechanistic baseline provided (matches Human Issues #3 and #6)
- Finding 4 (Goodness-of-fit assessed only visually; no log-likelihood or AIC reported): A — no quantitative fit metric beyond fabricated values; distinct from benchmark concern
- Finding 5 (No parameter identifiability analysis; no confidence intervals): A — no profile likelihoods computed for any parameter
- Finding 6 (Conceptual misuse of p_1 as probability of true exoplanet signal): A — p_1 is a scaling factor, not a posterior probability; bar plot and validation section treat it as classification probability
- Finding 7 (delta.t = 1 inconsistent with Kepler 30-minute cadence): A — OU process calibrated to wrong time scale
- Finding 8 (Computational adequacy not demonstrated; no convergence diagnostics): B — no convergence traces, no multiple independent runs, only fabricated iteration values cited (matches Human Issues #3 and #10)
- Finding 9 (Reproducibility: hard-coded absolute paths and Python dependency): A — machine-specific paths and unspecified Python environment prevent reproduction
- Finding 10 (OU discretization step hard-coded rather than using dt): C — silent inconsistency between declared and actual time step in Csnippet
- Finding 11 (Internal contradictions in reported results): C — period stated as 11 days in Summary vs 32 days in Discussion; p_1 stated as 0.46247 vs ~0.07
- Finding 12 (No model diagnostics beyond residual plots): C — no conditional log-likelihoods over time, no ESS monitoring, no filtering-distribution comparisons
- Finding 13 (Boxcar transit duration implausibly long at 5.44 days): C — physically impossible for an 11-day orbital period; not flagged by authors
- Finding 14 (Writing quality and placeholder text): D — informal language ("It's fantastic," "This is super important," "swap in your actual values"), nonsensical "your" uses, typographical errors (matches Human Issues #1, #2, and #13)
- Finding 15 (Detrending applied before POMP setup; error structure inconsistency): C — LOESS detrending changes residual variance but original photometric errors used in measurement model without justification

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Writing quality and typos — informal register including 'fantastic'")
- Human Issue #3: covered (matched by finding: "Point 25.13.5 — no benchmark comparison against non-mechanistic models")
- Human Issue #4: covered (matched by finding: "Point 25.13.6 — time-step mismatch causes large discrete jumps in simulated trajectories"; also matched by finding: "Simulated trajectories show implementation artifacts — sharp vertical jumps")
- Human Issue #5: covered (matched by finding: "Point 25.13.2 — fabricated log-likelihood values and degrading optimization")
- Human Issue #6: covered (matched by finding: "Point 25.13.5 — no benchmark comparison against non-mechanistic models")
- Human Issue #7: covered (matched by finding: "Point 25.13.3 — ACF of residuals contradicts text description")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Point 25.13.2 — fabricated log-likelihood values and degrading optimization"; also matched by finding: "No uncertainty quantification — no multiple restarts documented to verify convergence")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Writing quality and typos — informal register including 'fantastic'")
- Human Issue #14: missed

**Findings classification:**
- Point 25.13.2: B — fabricated log-likelihood values and degrading optimization (matches Human Issues #5 and #10)
- Point 25.13.3: B — ACF of residuals contradicts text description (matches Human Issue #7)
- Point 25.13.4: A — transit depth δ1 = 0.47 is physically implausible
- Point 25.13.1: A — particle filter role in DEoptim optimization is undocumented
- Point 25.13.7: A — phase-folded light curve shows no transit signal
- Point 25.13.5: B — no benchmark comparison against non-mechanistic models (matches Human Issues #3 and #6)
- Point 25.13.6: B — time-step mismatch likely corrupts the OU discretization (matches Human Issue #4)
- p1 parameter inconsistency: C — p1 described as fixed in specification but estimated at 0.076 in results
- Writing quality and typos: D — misspellings, grammatical errors, and informal register including "fantastic" (matches Human Issues #2 and #13)
- Simulated trajectories show implementation artifacts: D — sharp vertical jumps in simulated flux inconsistent with OU dynamics (matches Human Issue #4)
- No uncertainty quantification: D — no confidence intervals, profile likelihoods, or multiple DEoptim restarts to verify convergence (matches Human Issue #10)
- Reproducibility metadata absent: C — software versions, RNG seeds, and cluster warning messages not addressed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 2 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 9 | 3 | 5 | 3 |
| B (AI major, human also found) | 2 | 6 | 4 | 4 |
| C (AI minor, human missed) | 3 | 5 | 5 | 2 |
| D (AI minor, human also found) | 1 | 1 | 1 | 3 |
| E (Human found, AI missed) | 9 | 6 | 7 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 9 | 5/14 = 36% | 9 | 3 | 12/15 = 80% |
| Charlie | 6 | 1 | 6 | 8/14 = 57% | 3 | 5 | 8/15 = 53% |
| Doug | 4 | 1 | 7 | 7/14 = 50% | 5 | 5 | 10/15 = 67% |
| Evan | 4 | 3 | 6 | 8/14 = 57% | 3 | 2 | 5/12 = 42% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #8: There are many repetitions of symbols in the equations which make the report harder to read. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: Only Figure 1 is numbered, but elsewhere there are references to Fig. 2, Fig. 3, etc., which are not numbered. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: Technical terms like BKJD (Barycentric Kepler Julian Date) need clear explanations for readers without specialized astronomical knowledge. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #12: The redundant presentation of the transit model equation (appearing multiple times with slight variations) creates unnecessary confusion. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #14: The reference "Rappaport, S., Levine, A., Chiang, E., El Mellah, I., Jenkins, J. M., Kaltenegger, L., … & Villasenor, J. (2012). 'Light-curve Analysis of KIC 12557548b: An Extrasolar Planet with a Comet-like Tail.' The Astrophysical Journal, 752(1), 1." does not exist as cited. This error looks like a GenAI hallucination and is a serious scholarly concern. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 14 human issues (36%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #4: "Simulated trajectories follow the general pattern of the observed data" does not seem to match the figure, where the simulated trajectories oscillate rapidly, unlike the data. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
