# Ned-Clean Analysis — W22 Project 08

---

## Human Issues

1. No explanation for the motivation to study Turkey specifically; no cultural context for comparing Turkey's pandemic experience to the USA; no discussion of seasonal indoor behavior.
2. The SEIREIR model fits worse than ARIMA — perhaps plotting on log scale would help; fixed initial conditions (especially I_0=100) may be problematic.
3. The smoothed periodogram plot is missing from the report.
4. The statement that "ARIMA(2,1,0) is better for the data" is statistically incorrect — rejection of the alternative hypothesis does not mean one model is better than another.
5. The iterated filtering convergence plots show incomplete convergence (likelihood continues to go up), suggesting more iterations and/or a larger random walk standard deviation.
6. More discussion of parameters corresponding to the MLE (or values with likelihood close to the maximum) is needed.
7. Captions for graphs are missing.
8. The report does not describe the measurement model, apart from presenting code.
9. Typo: "We fix N=843400" should be 84.34 × 10^6.
10. Typo: "1/1 month" should read 1/3 month for consistency with text and code.
11. Grammatical mistakes were distracting.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding #9 — rw.sd too small at 0.002–0.003, impairs convergence)
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding #7 — population value inconsistency, text states N=843400 but code and intro use 84340000)
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Incorrect data variable — active cases not incident cases): A — major, human missed
- Finding 2 (Accumulator H tracks recoveries not new cases): A — major, human missed
- Finding 3 (Hard-coded seed injection at t=125 unjustified): A — major, human missed
- Finding 4 (ARIMA vs POMP log-likelihood comparison invalid): A — major, human missed
- Finding 5 (Local search uses %do% not %dopar%): A — major, human missed
- Finding 6 (Global search results cannot be reproduced from Rmd): A — major, human missed
- Finding 7 (Population value inconsistency): B — major, matches Human Issue #9
- Finding 8 (R_b initialized as (1-eta)*N — biologically nonsensical): C — minor, human missed
- Finding 9 (rw.sd too small, parameter transformation inconsistent): D — minor, matches Human Issue #5
- Finding 10 (Government restriction threshold at t=35 hard-coded): C — minor, human missed
- Finding 11 (EDA plots active-case stock, not daily new cases): C — minor, human missed
- Finding 12 (AIC table search range too narrow, P,Q in {0,1,2}): C — minor, human missed
- Finding 13 (No confidence intervals or profile likelihoods): C — minor, human missed
- Finding 14 (ESS interpretation incomplete): C — minor, human missed
- Finding 15 (Conclusion misidentifies POMP log-likelihood value): C — minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding #15 — periodogram not shown, only referenced as unremarkable)
- Human Issue #4: covered (matched by finding #13 — ARIMA model selection rationale inconsistent; AIC favors 2,1,1 but LRT selects 2,1,0 without adequate justification)
- Human Issue #5: covered (matched by finding #8 — rw.sd perturbation magnitudes excessively small, ~10x below course standard)
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding #12 — population size inconsistency, text states N=843400 but code uses 84340000)
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Accumulator H tracks recoveries not infections): A — major, human missed
- Finding 2 (Invalid direct comparison of ARIMA and POMP log-likelihoods): A — major, human missed
- Finding 3 (No profile likelihoods — parameter uncertainty unquantified): A — major, human missed
- Finding 4 (Data construction error: active cases vs. new daily cases): A — major, human missed
- Finding 5 (R_b initial conditions biologically implausible): A — major, human missed
- Finding 6 (Ad hoc injection of 10 individuals at t=125): A — major, human missed
- Finding 7 (Missing convergence diagnostics for global search): A — major, human missed
- Finding 8 (rw.sd perturbation magnitudes excessively small): B — major, matches Human Issue #5
- Finding 9 (Local search uses sequential %do% despite parallel backend): C — minor, human missed
- Finding 10 (No simulation-based diagnostics beyond visual overlay): C — minor, human missed
- Finding 11 (Fixed parameters lack principled justification — k=10): C — minor, human missed
- Finding 12 (Population size inconsistency): D — minor, matches Human Issue #9
- Finding 13 (ARIMA model selection rationale inconsistent): D — minor, matches Human Issue #4
- Finding 14 (No benchmark ARMA model on raw undifferenced series): C — minor, human missed
- Finding 15 (Periodogram not shown): D — minor, matches Human Issue #3

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by minor — LRT model selection between ARIMA(2,1,1) and ARIMA(2,1,0) applied incorrectly; reasoning is confused)
- Human Issue #5: covered (matched by minor — insufficient IF2 iterations; convergence traces show parameters have not stabilized by iteration 50)
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by minor — population figure error in text, N=843400 vs 84340000 in code)
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major 1 (Data variable mismatch — active cases vs. new recoveries): A — major, human missed
- Major 2 (Accumulator tracks recoveries not detections): A — major, human missed
- Major 3 (Global search initialized from previous mif2 result): A — major, human missed
- Major 4 (Global search box excludes high-likelihood region): A — major, human missed
- Major 5 (Reported log-likelihood inconsistent with stored artifacts): A — major, human missed
- Major 6 (Invalid ARIMA vs SEIREIR log-likelihood comparison): A — major, human missed
- Major 7 (No profile likelihoods or parameter confidence intervals): A — major, human missed
- Major 8 (Biologically implausible R_b initial condition): A — major, human missed
- Minor: Population figure error in text: D — minor, matches Human Issue #9
- Minor: Local search %do% not %dopar%: C — minor, human missed
- Minor: Global search Np=1000, local Np=2000 (inconsistent particle counts): C — minor, human missed
- Minor: Hard-coded variant emergence at t=125 without justification: C — minor, human missed
- Minor: No model diagnostics reported: C — minor, human missed
- Minor: Insufficient IF2 iterations: D — minor, matches Human Issue #5
- Minor: LRT model selection applied incorrectly: D — minor, matches Human Issue #4
- Minor: Notation inconsistency in model equations (continuous vs discrete): C — minor, human missed
- Minor: local.RData referenced but not present: C — minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by minor m5 — periodogram figure appears missing)
- Human Issue #4: covered (matched by minor m6 — ARIMA model selection: AIC and LRT disagree without explanation)
- Human Issue #5: covered (matched by major 22.08.5 — optimization has not converged; authors explicitly state this; mu_IR_o inconsistency noted)
- Human Issue #6: missed
- Human Issue #7: covered (matched by minor m7 — figure captions are absent throughout)
- Human Issue #8: missed
- Human Issue #9: covered (matched by minor m1 — population figure inconsistency; text states N=843400, code uses N=84340000)
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major 22.08.1 (Measurement model mismatch: H tracks recoveries, data is new daily confirmed cases): A — major, human missed
- Major 22.08.2 (ARIMA and POMP log-likelihoods not directly comparable): A — major, human missed
- Major 22.08.3 (No profile likelihoods or confidence intervals): A — major, human missed
- Major 22.08.4 (Biologically implausible initial condition: R_b = (1-eta)*N at t=0): A — major, human missed
- Major 22.08.5 (Optimization not converged; mu_IR_o inconsistency across code blocks): B — major, matches Human Issue #5
- Minor m1 (Population figure inconsistency): D — minor, matches Human Issue #9
- Minor m2 (Beta variant seed hard-coded without sensitivity analysis): C — minor, human missed
- Minor m3 (ESS collapse early in filtering not addressed): C — minor, human missed
- Minor m4 (Simulation envelope far exceeds observed data range): C — minor, human missed
- Minor m5 (Periodogram figure appears missing): D — minor, matches Human Issue #3
- Minor m6 (ARIMA AIC and LRT disagree without explanation): D — minor, matches Human Issue #4
- Minor m7 (Figure captions absent throughout): D — minor, matches Human Issue #7

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 4 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 7 | 8 | 4 |
| B (AI major, human also found) | 1 | 1 | 0 | 1 |
| C (AI minor, human missed) | 7 | 4 | 6 | 3 |
| D (AI minor, human also found) | 1 | 3 | 3 | 4 |
| E (Human found, AI missed) | 9 | 7 | 8 | 6 |

---

## Per-Reviewer Metrics

**Human Recall = (B+D) / (B+D+E)**

- Alex: (1+1) / (1+1+9) = 2/11 = 0.182 (18.2%)
- Charlie: (1+3) / (1+3+7) = 4/11 = 0.364 (36.4%)
- Doug: (0+3) / (0+3+8) = 3/11 = 0.273 (27.3%)
- Evan: (1+4) / (1+4+6) = 5/11 = 0.455 (45.5%)

**AI-Unique Rate = (A+C) / (A+B+C+D)**

- Alex: (6+7) / (6+1+7+1) = 13/15 = 0.867 (86.7%)
- Charlie: (7+4) / (7+1+4+3) = 11/15 = 0.733 (73.3%)
- Doug: (8+6) / (8+0+6+3) = 14/17 = 0.824 (82.4%)
- Evan: (4+3) / (4+1+3+4) = 7/12 = 0.583 (58.3%)

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- H1: No explanation for Turkey motivation / cultural context — missed by all 4 reviewers
- H2: SEIREIR fits worse than ARIMA, suggesting log scale and problematic I_0=100 — missed by all 4 reviewers
- H6: More discussion of MLE parameters needed — missed by all 4 reviewers
- H8: Report does not describe measurement model, apart from presenting code — missed by all 4 reviewers
- H10: Typo "1/1 month" should be 1/3 month — missed by all 4 reviewers
- H11: Grammatical mistakes were distracting — missed by all 4 reviewers

Consensus misses: 6 out of 11 human issues (54.5%).

---

**Unique finds per reviewer:** Human issues that only one reviewer covered and all others missed.

- H3 (Periodogram missing): covered by Charlie, Doug missed it, Evan covered it — actually Evan also covered H3 via m5. So H3 is covered by Charlie and Evan.
- H4 (ARIMA model selection language): covered by Charlie, Doug, Evan — not Alex.
- H5 (Convergence incomplete, larger rw.sd): covered by Alex, Charlie, Doug, Evan.
- H7 (Captions missing): covered only by Evan (m7). Alex, Charlie, Doug all missed it.
- H9 (Typo N=843400): covered by Alex, Charlie, Doug, Evan.

Unique finds:
- Alex: none (H5 and H9 are also covered by others)
- Charlie: none (H3, H4, H5, H9 are also covered by at least one other reviewer)
- Doug: none (H4, H5, H9 also covered by others; H3 not covered by Doug)
- Evan: H7 (figure captions absent) — only Evan raised this; all other reviewers missed it. Count: 1.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

---

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

Issues in category A (major) or C (minor) across all four reviewers — i.e., AI-only findings raised by all four:

- Measurement model mismatch: H accumulates recoveries not new infections/detections — raised by Alex (A), Charlie (A), Doug (A), Evan (A). Universal AI-only flag.
- Invalid ARIMA vs POMP log-likelihood comparison (different data representations) — raised by Alex (A), Charlie (A), Doug (A), Evan (A). Universal AI-only flag.
- No profile likelihoods / parameter identifiability unassessed — raised by Alex (C), Charlie (A), Doug (A), Evan (A). Universal AI-only flag.
- Biologically implausible R_b initial condition at t=0 — raised by Alex (C), Charlie (A), Doug (A), Evan (A). Universal AI-only flag.
- Active cases (stock) vs. new daily cases (flow) as the observation variable — raised by Alex (A), Charlie (A), Doug (A), Evan (A). Universal AI-only flag. (Note: overlaps with the accumulator issue but addresses the data construction side.)

Universal AI-only flags: 5 issues raised by all four reviewers that the human did not raise.
