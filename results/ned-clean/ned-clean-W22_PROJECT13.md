# Ned-Clean Analysis — W22 Project 13

---

## Human Issues

1. Why are initial values treated as known, rather than estimated?
2. The fixed initial value of H does not make sense, but perhaps this does not matter since it gets reset to zero at each observation time.
3. Don't display log likelihood evaluations to 7 decimal places. One is usually enough.
4. The fixed value phi=14 is not explained.
5. For the introduction, it is better to include the background (epidemic situation) in the researched regions, California and Texas.
6. It could be interesting to compare the results for California and Texas, but the report does not make progress on that. Indeed, the report does not put the analysis into the context of the characteristics of the two states analyzed.
7. The visual simulation of local search in California seems to give the wrong value of original daily new cases report in the plot, because the line is the same as the one in Texas. This may be a result of a coding problem where some variable names are re-used for the California and Texas cases.
8. This project builds on previous projects, which is a good thing to do. However, given this helpful start it might have been possible to get further.
9. There is a sign mistake in the Binomial formula which may have been inherited from a past project. It is okay to borrow from cited past projects, but one should borrow critically.
10. The results are shown at low computational intensity, for example, only 5 iterations are used to look for the MLE in the local search. Evidently, the group did not learn to take advantage of greatlakes.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Measurement model contains unexplained fixed scaling factor of 14")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Lack of quantitative comparison between California and Texas models")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Force of infection formula missing negative sign")
- Human Issue #10: covered (matched by finding: "run_level is set to 1, smallest computation settings, only 5 MIF iterations")

**Findings classification:**
- Issue 1 — Global search code entirely absent from Rmd: A — reproducibility failure not raised by human
- Issue 2 — Profile likelihood is not a genuine profile: A — pseudo-profile approach not raised by human
- Issue 3 — Measurement model contains unexplained fixed scaling factor of 14: B (matches Human Issue #4)
- Issue 4 — H accumulator/accumvars conceptual conflict with phi=14 scaling: A — specific inconsistency between accumvars reset and factor-of-14 not raised by human
- Issue 5 — Force of infection formula missing negative sign in mathematical writeup: B (matches Human Issue #9)
- Issue 6 — run_level=1 gives only 50 particles and 5 MIF iterations: B (matches Human Issue #10)
- Issue 7 — No diagnostic check that MIF has converged: A — convergence diagnostic omission not raised by human
- Issue 8 — Texas rw.sd includes b3 and b4 not in Texas model: A — copy-paste error in rw.sd not raised by human
- Issue 9 — Texas profile CI invalid, built from global search scatter not a dedicated profile: C — Moderate, not raised by human
- Issue 10 — eta inconsistency between stated assumption and parametrization: C — Moderate, not raised by human
- Issue 11 — No ARIMA or other benchmark likelihood computed: C — Moderate, not raised by human
- Issue 12 — b4 implausibly large and unstable: C — Moderate, not raised by human
- Issue 13 — rho described at wrong transition (E-to-I rather than I-to-R): C — Moderate, not raised by human
- Issue 14 — Lack of quantitative comparison between California and Texas models: D (matches Human Issue #6)
- Issue 15 — Covariate table interval lengths not verified against actual data length: C — Minor, not raised by human

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

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Fixed epidemiological parameters without sensitivity analysis")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Factor-of-14 scaling in measurement model is unjustified")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Lack of quantitative comparison between California and Texas models")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Insufficient computation: local search at debugging-level settings")

**Findings classification:**
- Issue 1 — Profile likelihood is a pseudo-profile, not a true profile: A — not raised by human
- Issue 2 — Global search box misaligned with MLE region for b4: A — not raised by human
- Issue 3 — Texas initial likelihood evaluated with California parameters (code-order bug): A — not raised by human
- Issue 4 — Insufficient computation: local search at debugging-level settings: B (matches Human Issue #10)
- Issue 5 — Global search code absent from Rmd: A — not raised by human
- Issue 6 — No benchmark comparison: A — not raised by human
- Issue 7 — Factor-of-14 scaling in measurement model is unjustified: B (matches Human Issue #4)
- Issue 8 — Model description inconsistency: rho described at wrong transition: C — Minor, not raised by human
- Issue 9 — Texas rw.sd specifies parameters not in the Texas model: C — Minor, not raised by human
- Issue 10 — tau perturbation effectively zero on the log scale: C — Minor, not raised by human
- Issue 11 — Fixed epidemiological parameters without sensitivity analysis: D (matches Human Issue #1)
- Issue 12 — No model diagnostics: C — Minor, not raised by human
- Issue 13 — Profile likelihood computed only for rho; other parameters unexamined: C — Minor, not raised by human
- Issue 14 — Lack of quantitative comparison between California and Texas models: D (matches Human Issue #6)
- Issue 15 — Interpretation of policy effects not grounded in identifiability: C — Minor, not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "mu_EI and mu_IR fixed without sensitivity analysis or uncertainty quantification")
- Human Issue #2: covered (matched by finding: "H initial value unjustified")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Fixed Scaling Factor phi=14 Is Unmotivated and Not Estimated")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Direct cross-state log-likelihood comparisons are invalid")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Texas Particle Filter Degeneracy at Initial Parameter Values — SE=12.4 indicates insufficient computation")

**Findings classification:**
- Issue 1 — Severe global search box misalignment invalidates MLE claims: A — not raised by human
- Issue 2 — Profile likelihood is a pseudo-profile: A — not raised by human
- Issue 3 — Accumulator H accumulates recoveries, not new infections: A — not raised by human (Human #2 is about H initial value, distinct concern)
- Issue 4 — No benchmark comparison: A — not raised by human
- Issue 5 — Fixed scaling factor phi=14 unmotivated and not estimated: B (matches Human Issue #4)
- Issue 6 — Texas particle filter degeneracy at initial parameter values (SE=12.4): B (matches Human Issue #10)
- Issue 7 — Global search code missing from Rmd: A — not raised by human
- Issue 8 — mu_EI and mu_IR fixed without sensitivity analysis: B (matches Human Issue #1)
- Minor: Notation error in transition rate (mu_SI should be mu_SE): C — not raised by human
- Minor: rw.sd for tau effectively zero: C — not raised by human
- Minor: Texas rw.sd includes spurious b3 and b4: C — not raised by human
- Minor: H initial value unjustified: D (matches Human Issue #2)
- Minor: Direct cross-state log-likelihood comparisons invalid: D (matches Human Issue #6)
- Minor: No model diagnostics: C — not raised by human
- Minor: Visual-only fit assessment: C — not raised by human
- Minor: Software version not documented: C — not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "C7 — H accumulator initialization")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "C2 — Unjustified phi=14 scaling parameter")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "C1 — Critically insufficient mif2 iterations")

**Findings classification:**
- C1 — Critically insufficient mif2 iterations (~5 iterations, loglik still rising): B (matches Human Issue #10)
- C2 — Unjustified phi=14 scaling parameter: B (matches Human Issue #4)
- C3 — No non-mechanistic benchmark comparison: A — not raised by human
- C4 — Texas profile likelihood too noisy to support reliable CI: A — not raised by human
- C10 — Policy interpretation unsupported by current analysis: A — not raised by human
- C6 — Run-level parameters not documented: C — Minor, not raised by human
- C7 — H accumulator initialization (large initial H influences first-step likelihood): D (matches Human Issue #2)
- C8 — ESS monitoring and conditional log-likelihood plots absent: C — Minor, not raised by human
- C9 — Normal measurement model for count data: C — Minor, not raised by human
- C5 — loglik.se column values unclear: C — Minor, not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 5 | 5 | 3 |
| B (AI major, human also found) | 3 | 2 | 3 | 2 |
| C (AI minor, human missed) | 6 | 6 | 6 | 4 |
| D (AI minor, human also found) | 1 | 2 | 2 | 1 |
| E (Human found, AI missed) | 6 | 6 | 5 | 7 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (3+1) / (3+1+6) = 4/10 = **40%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+6) / (5+3+6+1) = 11/15 = **73.3%**

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+2) / (2+2+6) = 4/10 = **40%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+6) / (5+2+6+2) = 11/15 = **73.3%**

**Doug**
- Human Recall = (B+D) / (B+D+E) = (3+2) / (3+2+5) = 5/10 = **50%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+6) / (5+3+6+2) = 11/16 = **68.8%**

**Evan**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+7) = 3/10 = **30%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+4) / (3+2+4+1) = 7/10 = **70.0%**

---

## Cross-Reviewer Aggregation

### Consensus Misses

Human issues missed by all four reviewers (0 out of 4 covered them):

- **Issue #3:** Don't display log likelihood evaluations to 7 decimal places — 0 out of 4 reviewers covered this.
- **Issue #5:** Include background on the epidemic situation in California and Texas in the introduction — 0 out of 4 reviewers covered this.
- **Issue #7:** Visual simulation of local search in California shows the same line as Texas, suggesting a coding bug with reused variable names — 0 out of 4 reviewers covered this.
- **Issue #8:** The project builds on previous projects but given that helpful start it might have been possible to go further — 0 out of 4 reviewers covered this.

Total: 4 out of 10 human issues were missed by every reviewer.

### Unique Finds Per Reviewer

Human issues covered by exactly one reviewer and missed by all others:

- **Issue #9** (sign mistake in Binomial formula): covered only by Alex (B); missed by Charlie, Doug, and Evan.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-Only Flags

Issues raised by all four reviewers that the human did not mention:

1. **No benchmark comparison** (ARIMA or similar non-mechanistic model): raised by Alex (C, Moderate), Charlie (A, Major), Doug (A, Major), Evan (A, Major). The human did not raise this.
2. **No model diagnostics** (ESS monitoring, conditional log-likelihoods, convergence checks): raised by Alex (A, Major — framed as no convergence diagnostic), Charlie (C, Minor), Doug (C, Minor), Evan (C, Minor). The human did not raise this.

Total universal AI-only flags: 2.
