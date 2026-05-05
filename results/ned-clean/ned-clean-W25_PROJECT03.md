# Ned-Clean Analysis — W25 Project 03

## Human Issues

1. The conclusion about "important implications for public health monitoring and intervention planning" is over-stated and unsupported.
2. The phase profile is misinterpreted: a sharp peak shows very strong identifiability, not "limited identifiability."
3. The rho profile is similarly misinterpreted; the beta0 profile is described as "smooth and fairly symmetric near the peak" when the plotted profile does not have these properties.
4. Data of this kind can be more insightfully plotted on a log scale; the linear analysis (additive decomposition, periodogram, ARMA) are better on a log scale.
5. Incorrect reasoning: "the ACF plot of the log-transformed data still exhibits a slow decay, indicating that the series remains non-stationary." The usual motivation for the sample ACF assumes a stationary model.
6. The interpretation of ARMA residuals is poor — the residuals are far from normal and the time plot shows extreme heteroskedasticity.
7. The ARMA benchmark should be carried out as log-ARMA (as in Chapter 18 measles case study).
8. The report does not explain its own creative contribution beyond applying similar approaches to a new dataset.
9. It is unclear what is learned from the additive decomposition that cannot be seen more clearly from other plots.
10. For comparing ARMA to SARMA it would be better to use AIC than likelihood (degrees of freedom differ), or use a likelihood ratio test.
11. The conclusion "peaks occurring approximately every 60 weeks (around 1.15 years)" is curious given only ~2 years of data and expected annual seasonality at 1.0 yr.
12. Sections are numbered, but there are no figure captions or figure numbers.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: contradiction (Alex says singleton CIs are artifacts of coarse grid/particle noise, NOT evidence of a sharp peak; human says the sharp peak indicates strong identifiability)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Residual Diagnostics Are Cursory — ARMA residuals discussed minimally, normality assumption not appropriate")
- Human Issue #7: covered (matched by finding: "ARMA Differencing Applied to the Wrong Series — code differences raw series, not log-transformed")
- Human Issue #8: covered (matched by finding: "SEIRS Model Borrowed Heavily from a Prior Project Without Sufficient Adaptation")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "Frequency Analysis Interpretation Error — 60-week period not reconciled with expected 52-week annual seasonality")
- Human Issue #12: missed

**Findings classification:**

Note: Alex uses no Major/Minor labels; all findings are treated as Major (from a "Weaknesses" section ordered by severity).

- Finding #1 (Profile methodology flawed — single-path): A — methodologically invalid profile likelihood procedure; human did not raise this
- Finding #2 (Singleton CIs — coarse grid artifact, not sharp peak): F — contradicts Human Issue #2 (human says sharp peak = strong identifiability; Alex says there is no sharp peak, it is noise/coarse grid)
- Finding #3 (Log-likelihood comparison ARMA vs POMP invalid): A — different data transformations make comparison invalid; human did not raise this
- Finding #4 (Data file path inconsistency): A — reproducibility failure from wrong path; human did not raise this
- Finding #5 (Insufficient global search — 10 starting points): A — underpowered global search; human did not raise this
- Finding #6 (Amplitude parameter near constraint boundary): A — amp convergence near logit boundary not discussed; human did not raise this
- Finding #7 (Frequency analysis — 60-week period vs expected 52): B — matches Human Issue #11
- Finding #8 (ARMA differencing on wrong series — raw not log): B — matches Human Issue #7
- Finding #9 (Very small particle count in local search): A — noisy likelihood selection; human did not raise this
- Finding #10 (Profile grid too coarse and narrow): A — 10 grid points with single noisy evaluation; human did not raise this
- Finding #11 (Phase parameter 52.64 outside [0,52] natural range): A — modular equivalence not recognized; human did not raise this
- Finding #12 (Initial state proportions not estimated): A — S0,E0,I0,R0 fixed during optimization; human did not raise this
- Finding #13 (Residual diagnostics cursory): B — matches Human Issue #6
- Finding #14 (SEIRS model borrowed from prior project — limited contribution): B — matches Human Issue #8
- Finding #15 (SARMA fixed ARMA order not fully justified): A — sequential selection procedure not rigorous; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed (Charlie says singletons "may be qualitatively correct" but are not supported computationally; does not affirm the human's specific claim that a sharp peak indicates strong identifiability)
- Human Issue #3: covered (matched by finding: "Profile likelihood grid for rho spans only ±20% — range too narrow to detect identifiability issues")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "SARMA model AIC improvement negligible and joint optimization not performed")
- Human Issue #11: covered (matched by finding: "Frequency analysis conclusion 60-week period inconsistent with annual flu and SARMA's 52-week assumption")
- Human Issue #12: missed

**Findings classification:**

- Major #1 (Profile likelihoods invalid — single IF2 restart, single pfilter): A — invalid profile procedure; human did not raise this
- Major #2 (Log-likelihood comparison ARMA vs POMP invalid): A — different data and distributional families; human did not raise this
- Major #3 (Global search underpowered — 10 replicates, Np=1000): A — insufficient for 13-parameter model; human did not raise this
- Major #4 (rho grid too narrow — ±20%): D — matches Human Issue #3 (rho profile analysis flawed)
- Major #5 (No model diagnostics beyond visual inspection): A — no ESS, no conditional log-likelihoods; human did not raise this
- Major #6 (No valid benchmark against non-mechanistic model): A — no count-data benchmark; human did not raise this
- Major #7 (Initial state parameters not perturbed in IF2): A — S0,E0,I0,R0 frozen; human did not raise this
- Minor #8 (Frequency analysis — 60-week period vs 52-week SARMA inconsistency): D — matches Human Issue #11
- Minor #9 (SARMA AIC improvement negligible; sequential selection procedure): D — matches Human Issue #10
- Minor #10 (amp logit constraint): C — minor technical note; human did not raise this
- Minor #11 (rho implausibly small — 0.00015): C — not compared to independent estimates; human did not raise this
- Minor #12 (Data file path incorrect): C — reproducibility failure; human did not raise this
- Minor #13 (Only 4 of 13 parameters profiled): C — rate parameters not profiled; human did not raise this
- Minor #14 (phase 52.64 outside [0,52] range): C — modular equivalence and profile boundary issue; human did not raise this
- Minor #15 (Pairs plot with 10 points overstates identifiability): C — insufficient sample; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed (Doug attributes singleton CIs to noise/narrow grid, not identifiability strength; does not affirm human's sharp-peak interpretation)
- Human Issue #3: missed (Doug discusses rho grid range but does not address the specific misinterpretation of the rho profile or the beta0 description mismatch)
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "Periodogram frequency interpretation questionable — 60-week period vs annual flu and SARMA inconsistency")
- Human Issue #12: missed

**Findings classification:**

- Major #1 (Accumulator variable tracks recoveries not new infections): A — dN_IR instead of dN_EI; human did not raise this
- Major #2 (Log-likelihood comparison ARMA vs POMP invalid): A — different data transformations; human did not raise this
- Major #3 (Profile likelihood is single-path procedure): A — not true profile likelihood; human did not raise this
- Major #4 (Global search uses only 10 replicates, Nmif=50): A — underpowered; human did not raise this
- Major #5 (Profile range for rho too narrow — ±20%): A — cannot detect identifiability issues; human did not raise this
- Major #6 (No benchmark against non-mechanistic model on same data): A — no count-data benchmark; human did not raise this
- Major #7 (No quantitative model diagnostics beyond visual inspection): A — no ESS, no per-step log-likelihoods; human did not raise this
- Minor #8 (ARMA/SARMA fitted to differenced data without restoring to original scale): C — no formal stationarity tests; human did not raise this
- Minor #9 (Periodogram — 60-week period vs 52 inconsistency): D — matches Human Issue #11
- Minor #10 (amp logit constraint note): C — minor technical note; human did not raise this
- Minor #11 (phase parameter grid wraps around periodicity boundary): C — 52-week periodicity issue in profile; human did not raise this
- Minor #12 (Only 4 of 13 parameters profiled): C — rate parameters not profiled; human did not raise this
- Minor #13 (Parameter estimates not compared to biological knowledge): C — rho and rates not compared to literature; human did not raise this
- Minor #14 (Data file path hard-coded incorrectly): C — reproducibility failure; human did not raise this
- Minor #15 (Single pfilter per profile grid point — excessive Monte Carlo noise): C — single noisy evaluation; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed (Evan says CIs are unreliable artifacts of under-powered computation; does not affirm human's claim that sharp peak = strong identifiability)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Log transformation described but not applied to ARMA fitting data")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed

**Findings classification:**

- Major 25.03.1 (Log-likelihood comparison across incompatible scales): A — different data transformations; human did not raise this
- Major 25.03.2 (Profile likelihood under-powered and CIs unreliable): A — 10 grid points, single mif2/pfilter per point; human did not raise this
- Major 25.03.5 (No particle filter diagnostics): A — no ESS plots or per-step log-likelihoods; human did not raise this
- Major 25.03.14 (No profile likelihood for transition rate parameters): A — mu_EI, mu_IR, mu_RS, k not profiled; human did not raise this
- Minor 25.03.3 (Initial condition parameters fixed during mif2): C — S0,E0,I0,R0 not in rw_sd; human did not raise this
- Minor 25.03.4 (Log transformation described but not applied to ARMA fitting): D — matches Human Issue #7
- Minor 25.03.7 (Single pfilter for selecting best local result): C — noisy selection; human did not raise this
- Minor 25.03.6 (Reporting rate rho implausibly small — not compared to independent estimates): C — 0.015% ascertainment; human did not raise this
- Minor 25.03.15 (Pairs plots with 10 points support limited conclusions): C — 10-point scatter plots are noisy; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 10 | 6 | 7 | 4 |
| B (AI major, human also found) | 4 | 0 | 0 | 0 |
| C (AI minor, human missed) | 0 | 6 | 7 | 4 |
| D (AI minor, human also found) | 0 | 3 | 1 | 1 |
| E (Human found, AI missed) | 7 | 9 | 11 | 11 |
| F (Human-AI contradiction) | 1 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (4+0) / (4+0+7) = 4/11 = 0.364
- AI-Unique Rate = (A+C) / (A+B+C+D) = (10+0) / (10+4+0+0) = 10/14 = 0.714

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (0+3) / (0+3+9) = 3/12 = 0.250
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+6) / (6+0+6+3) = 12/15 = 0.800

**Doug**
- Human Recall = (B+D) / (B+D+E) = (0+1) / (0+1+11) = 1/12 = 0.083
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+7) / (7+0+7+1) = 14/15 = 0.933

**Evan**
- Human Recall = (B+D) / (B+D+E) = (0+1) / (0+1+11) = 1/12 = 0.083
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+4) / (4+0+4+1) = 8/9 = 0.889

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (missed or contradicted by all):

1. Human Issue #1: Overstated public health implications conclusion — missed by Alex, Charlie, Doug, Evan (4/4)
4. Human Issue #4: Data and analysis better on log scale — missed by Alex, Charlie, Doug, Evan (4/4)
5. Human Issue #5: Incorrect ACF reasoning about stationarity — missed by Alex, Charlie, Doug, Evan (4/4)
9. Human Issue #9: Additive decomposition uninformative — missed by Alex, Charlie, Doug, Evan (4/4)
12. Human Issue #12: No figure captions or figure numbers — missed by Alex, Charlie, Doug, Evan (4/4)

Count: 5 out of 12 human issues were missed by all reviewers.

Note: Human Issue #2 (phase profile misinterpreted) was contradicted by Alex and missed by Charlie, Doug, and Evan. It is not a consensus miss since Alex engaged with it, but the human's specific interpretation (sharp peak = strong identifiability) was not affirmed by any reviewer.

### Unique finds per reviewer

Human issues covered by exactly one reviewer (all others missed):

- Alex uniquely covered: Human Issue #6 (ARMA residuals poorly interpreted), Human Issue #8 (no creative contribution)
- Charlie uniquely covered: Human Issue #3 (rho/beta0 profile misinterpreted), Human Issue #10 (use AIC not likelihood for ARMA vs SARMA)
- Doug uniquely covered: none
- Evan uniquely covered: none

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 2 |
| Charlie | 2 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer (Alex, Charlie, Doug, Evan) that the human did not mention:

1. Log-likelihood comparison between ARMA/SARMA and POMP is invalid because the models are fitted to different data transformations and different observation models (Gaussian vs. negative binomial on differenced vs. original series).
2. Profile likelihood is methodologically flawed — single IF2 restart and single pfilter evaluation per grid point, making reported confidence intervals unreliable.

Count: 2 universal AI-only flags.
