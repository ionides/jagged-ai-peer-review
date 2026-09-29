# Comparator Analysis — W24 Project 16

---

## Human Issues

1. The introduction has no references. It makes exaggerated claims of what the project achieves, in somewhat elaborate language. This does not look like good scholarship. These are deficits most commonly associated with the use of ChatGPT.

2. If you consider `auto.arima` as the best way to identify an ARIMA model, you should say what it does. Alternatively, it may be better to stick with a less sophisticated analysis that you fully understand.

3. ARMA modeling for population dynamics may work better on a log scale.

4. Figures could have numbers and captions to help the reader.

5. Given the weak identifiability, the appropriate conclusions from this study should be fairly inconclusive. However, the methods and models could scale up to a larger data analysis with more statistical power.

6. The conclusions give good attention to the potential implications of the results.

7. Comment on the ARMA benchmark to assess the fit of the mechanistic model. It looks favorable for the POMP model, but log-ARMA might be a more competitive challenge.

8. In the formula for `S_u`, `vac_rate` should read `(1-vac_rate)`. This is correct in the code.

9. The references are not cited in the text, just listed at the end.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding 14: "ARIMA section adds limited value and is not integrated with POMP analysis; discussion is superficial")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding 14: "ARIMA section adds limited value and is not integrated with POMP analysis; discussion is superficial")
- Human Issue #8: covered (matched by finding 2: "S_u initialization formula uses vaccinationRate instead of (1-vaccinationRate) — error in writeup")
- Human Issue #9: missed

**Findings classification:**
- Finding 1: A — two sub-populations are completely decoupled with no cross-infection between vaccinated and unvaccinated compartments
- Finding 2: B — susceptible initialization formula for S_u uses vaccinationRate instead of (1-vaccinationRate) in the writeup, contradicting the code (matches Human Issue #8)
- Finding 3: A — accumulator variable H counts IR recoveries rather than new infections, mismatching the measurement model to the data
- Finding 4: A — rho applied a second time inside dmeas/rmeas, effectively double-discounting H
- Finding 5: A — no simulation from the fitted model is presented; no visual check that the model reproduces observed data
- Finding 6: A — profile likelihood plots are scatter plots of marginal loglik from global search, not genuine profile likelihoods; confidence intervals derived from them are invalid
- Finding 7: A — local MIF2 convergence diagnostic shows no evidence of convergence before the global search
- Finding 8: A — log-likelihood is described as "negative log likelihood maximum (likelihood minimum)" — a conceptual error
- Finding 9: C — dispersion parameter k is fixed at 10 with no justification or sensitivity analysis
- Finding 10: C — data subsetting logic (rows 1-99 vs. 100-198) is fragile and never validated against the ORIGIN_SOURCE column
- Finding 11: C — population size N set to total Netherlands population (17.7M) is inappropriate for sentinel surveillance data
- Finding 12: C — model diagram labels S-to-E transition as mu_SE but the code and parameter names use Beta — notation inconsistency
- Finding 13: C — interpretation that vaccinated individuals take longer to recover (mu_IR_v < mu_IR_u) is speculative and lacks literature support
- Finding 14: D — ARIMA section is superficial and not quantitatively integrated with the POMP analysis (matches Human Issues #2 and #7)
- Finding 15: C — reproducibility partially broken due to mismatched file paths between cluster script and Rmd, and differing seeds

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
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
- Human Issue #5: covered (matched by findings: "implausible parameter estimates not diagnosed as model misspecification" and "profile plots constructed from global search envelope are not true profile likelihoods")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no quantitative benchmark comparison between POMP and ARIMA")
- Human Issue #8: covered (matched by finding: "initialization formula mismatch between text and code — S_u uses vac_rate in text but (1-vac_rate) in code")
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Decoupled subpopulation transmission): A — structural flaw where vaccinated and unvaccinated branches do not interact
- Finding 2 (H accumulates recoveries not incidence): A — accumulator tracks IR transitions instead of EI/SE transitions
- Finding 3 (Logmeanexp misapplied across optimization runs): A — logmeanexp used to summarize global search rather than replicate pfilter runs
- Finding 4 (Implausible estimates not diagnosed as misspecification): B — mu_IR_v near zero interpreted as biology rather than model failure (matches Human Issue #5)
- Finding 5 (Profile plots not true profiles): B — upper envelope of global search used instead of dedicated profile optimization; ratio may not be well-identified (matches Human Issue #5)
- Finding 6 (No simulation from best-fit parameters): A — key visual diagnostic absent; no forward simulation overlaid on data
- Finding 7 (Convergence diagnostics from different local search): A — trace plots in Rmd come from a different procedure than the global search
- Finding 8 (S_u initialization formula mismatch): B — text uses vac_rate where code correctly uses (1-vac_rate) (matches Human Issue #8)
- Finding 9 (No quantitative benchmark comparison): D — ARIMA and POMP log-likelihoods not compared numerically (matches Human Issue #7)
- Finding 10 (k=10 fixed without justification): C — overdispersion parameter not estimated or sensitivity-tested
- Finding 11 (Aggressive cooling in local mif2): C — cooling.fraction.50=0.2 departs from course standard of 0.5
- Finding 12 (rho ≈ 0.003 not discussed): C — 0.3% reporting rate not evaluated against external surveillance coverage estimates
- Finding 13 (Hard-coded file paths): C — absolute paths specific to author's machines break reproducibility
- Finding 14 (AIC table consistency not checked): C — AIC increases when adding parameters not flagged as possible optimization failures
- Finding 15 (Parallel mif2 not seeded with doRNG): C — doRNG not called before parallel loop, making results not exactly reproducible

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Severe parameter non-identifiability; conclusions unsupported")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #8: covered (matched by finding: "Single equation for S_u initialization is incorrect in the text")
- Human Issue #9: missed

**Findings classification:**
- Major 1 (Accumulator variable tracks recoveries, not infections): A — accumulator H sums dN_IR rather than new detections, distorting all parameter estimates
- Major 2 (No cross-population transmission): A — force of infection for each subpopulation uses only its own infectious compartment, producing two independent epidemics
- Major 3 (Profile likelihoods are misidentified scatter plots): A — "profile likelihood" plots are global-search scatter plots; no separate profile IF2 optimization was run; chi-squared CI cutoff is invalid
- Major 4 (Global IF2 initialized from local search result): A — global search passes a completed local mif2 object as its base, inheriting a near-terminal cooling schedule
- Major 5 (Severe parameter non-identifiability; conclusions unsupported): B — parameters range widely within 2 log-likelihood units; best-fit point has beta_v > beta_u, opposite of paper's main conclusion (matches Human Issue #5)
- Major 6 (No non-mechanistic benchmark comparison): B — no log-likelihood or AIC comparison between ARIMA and POMP model is reported (matches Human Issue #7)
- Major 7 (k dispersion parameter fixed without justification): A — k=10 is fixed arbitrarily with no sensitivity analysis
- Major 8 (Misleading statement about log-likelihood): A — paper calls logmeanexp value a "likelihood minimum" and conflates it with the maximum log-likelihood
- Minor (No simulation vs. data plot): C — model simulation overlay on observed time series absent from rendered output
- Minor (Convergence traces inadequately presented): C — displayed traces use Nmif=300/4 replicates but actual global search used Nmif=1000
- Minor (Hard-coded absolute path in run.r): C — author-specific absolute path prevents reproduction on other machines
- Minor (Typos and grammatical errors): C — multiple spelling errors throughout the document
- Minor (S_u equation incorrect in text): D — text states S_u = vac_rate * eta_u * N but code correctly implements (1 - vac_rate) * eta_u * N (matches Human Issue #8)
- Minor (No model diagnostics): C — no conditional log-likelihood per time point, no ESS plot, no filtering distribution shown
- Minor (Initial condition hardcoded to 1): C — starting with exactly one infectious individual per subpopulation is a strong untested assumption
- Minor (No quantitative goodness-of-fit summary): C — no AIC or model comparison table provided

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by findings: "24.16.2/24.16.3 — profile likelihood plots are scatter plots, not proper profiles; key parameters unidentified" and "24.16.7 — causal language used without causal identification")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "24.16.6 — no quantitative benchmark comparison of ARIMA vs. POMP log-likelihoods")
- Human Issue #8: covered (matched by finding: "24.16.1 — initial condition formula for S_u uses vaccinationRate where it should use (1 - vaccinationRate)")
- Human Issue #9: missed

**Findings classification:**
- 24.16.2/24.16.3: B — profile likelihood plots are scatter plots, not proper profiles; Beta_v and Beta_u near-unidentified (matches Human Issue #5)
- 24.16.4: A — measurement model (observation equation) never stated in the paper
- 24.16.1: B — S_u initial condition formula uses vaccinationRate instead of (1 - vaccinationRate) (matches Human Issue #8)
- 24.16.5: A — mif2 convergence trace plots absent; no evidence of algorithm convergence
- 24.16.6: B — no quantitative comparison of ARIMA vs. POMP log-likelihoods despite both being reported (matches Human Issue #7)
- 24.16.7: B — causal language ("proves") used without causal identification; conclusions overclaim (matches Human Issue #5)
- 24.16.13: C — negative spike in conditional log-likelihood around week 35 not discussed
- misc: C — notation inconsistency (mu_SE_v in diagram vs. Beta_v in code/text), rendering artifacts, and multiple typographical errors
- misc-2: C — pairs plot (fig_013) rendered at very low resolution, nearly illegible

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 7 | 5 | 6 | 2 |
| B (AI major, human also found) | 1 | 3 | 2 | 4 |
| C (AI minor, human missed) | 6 | 6 | 7 | 3 |
| D (AI minor, human also found) | 1 | 1 | 1 | 0 |
| E (Human found, AI missed) | 6 | 6 | 6 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 6 | 3/9 = 33% | 7 | 6 | 13/15 = 87% |
| Charlie | 3 | 1 | 6 | 3/9 = 33% | 5 | 6 | 11/15 = 73% |
| Doug | 2 | 1 | 6 | 3/9 = 33% | 6 | 7 | 13/16 = 81% |
| Evan | 4 | 0 | 6 | 3/9 = 33% | 2 | 3 | 5/9 = 56% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The introduction has no references. It makes exaggerated claims of what the project achieves, in somewhat elaborate language. This does not look like good scholarship. These are deficits most commonly associated with the use of ChatGPT. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: ARMA modeling for population dynamics may work better on a log scale. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Figures could have numbers and captions to help the reader. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The conclusions give good attention to the potential implications of the results. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: The references are not cited in the text, just listed at the end. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 9 human issues (56%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: If you consider `auto.arima` as the best way to identify an ARIMA model, you should say what it does. Alternatively, it may be better to stick with a less sophisticated analysis that you fully understand. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
