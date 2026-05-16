# Ned-Clean Analysis — W22 Project 17

## Human Issues

1. The conclusion that the sample ACF "indicated dependencies between the data" does not add much to the timeplot. Also, differencing is used as a way to make a stationary model more suitable, which is not quite the same thing as dependence.
2. "4 of the AR polynomial roots are inside the unit circle and one of the MA polynomial roots are inside the unit circle" does not seem to match the figure. Also, the figure shows inverse roots so they should be inside for invertibility and causality.
3. "most of the residual values stay close to the horizontal line y=0 suggesting a good fit of our model" is not a warranted conclusion. The residuals show heteroskedasticity and/or long tails, with some autocorrelation. Residuals are centered on zero by construction.
4. Probably, ARMA modeling on a log scale would fit better.
5. I(0)=270000 is a very large number of initial infected individuals. This is fixed in the code, rather than being estimated, which could cause problems with fitting other parameters.
6. The strong weekly cycle is not in the SEIR model. One could model weekly totals to avoid dealing with day-of-week effects.
7. Likelihoods are not quite comparable before and after differencing. This could explain all or some of the difference between the SARIMA and SEIR log likelihoods. Note that SEIR beats the ARMA likelihood.
8. The source of the data is unclear. The Kaggle link provided refers to something not updated since 2020-07-27. The authors say "the beginning of the pandemic in the US, 2021 June 5st" but that is not when the pandemic began. It is a reasonable date for the arrival of the delta variant, but the project makes no mention of this variant.
9. The model, with time-varying beta, made more sense in the analysis of the cited W21 project. At that time, the dynamics were driven by initial spread and social distancing interventions. More recently, variants and vaccination have been more critical.
10. There is a sign mistake in the Binomial expression which may have been inherited from the cited W21 project. It is okay to borrow from cited past projects, but one should borrow critically.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Log-likelihood comparison between SARIMA and SEIR is invalid — SARIMA on differenced data, SEIR on raw series")
- Human Issue #8: covered (matched by finding: "Data source reproducibility issue — Kaggle version unspecified, date range buried in code")
- Human Issue #9: covered (matched by finding: "References to prior projects without independent validation — different time period, different variants")
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (S(0)=N, no recovered population): A — major, human missed
- Finding 2 (H accumulates recoveries not new infections): A — major, human missed
- Finding 3 (SARIMA vs SEIR log-lik comparison invalid): B — major (matches Human Issue #7)
- Finding 4 (Np=100 in global search likelihood evaluation): A — major, human missed
- Finding 5 (convergence absent, no remediation): A — major, human missed
- Finding 6 (gap in beta period Nov 12 – Dec 8): A — major, human missed
- Finding 7 (mu_IR fixed without epidemiological justification): A — major, human missed
- Finding 8 (SARIMA formula typographical error): C — minor, human missed
- Finding 9 (AIC selects non-causal/non-invertible SARIMA): C — minor, human missed
- Finding 10 (normal approximation for count data): C — minor, human missed
- Finding 11 (b5 starting value text/code mismatch): C — minor, human missed
- Finding 12 (global search box for tau far from starting value): C — minor, human missed
- Finding 13 (no profile likelihood or confidence intervals): C — minor, human missed
- Finding 14 (data source reproducibility — Kaggle version unspecified): D — minor (matches Human Issue #8)
- Finding 15 (references to prior projects without independent validation): D — minor (matches Human Issue #9)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Initial conditions violate population conservation — S=N implies zero prior immunity, E=200,000/I=270,000 listed but S+E+I > N")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Direct log-likelihood comparison between SARIMA and SEIR is invalid — different data transformations, different observation sets")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major 1 (H accumulates recoveries rather than new infections): A — major, human missed
- Major 2 (initial conditions violate population conservation; S=N implausible): B — major (matches Human Issue #5)
- Major 3 (no profile likelihood and no confidence intervals): A — major, human missed
- Major 4 (SARIMA non-causal and non-invertible; not remediated): A — major, human missed
- Major 5 (SARIMA vs SEIR log-lik comparison invalid): B — major (matches Human Issue #7)
- Major 6 (rw.sd for b1-b7 is 10x below standard): A — major, human missed
- Minor 7 (b5 starting value text/code mismatch): C — minor, human missed
- Minor 8 (covariate period for intervention 5 inconsistent with text): C — minor, human missed
- Minor 9 (Np=100 vs Np=1000 inconsistency): C — minor, human missed
- Minor 10 (no non-mechanistic benchmark for SEIR): C — minor, human missed
- Minor 11 (convergence incomplete but not addressed): C — minor, human missed
- Minor 12 (no model diagnostics — ESS, conditional log-lik): C — minor, human missed
- Minor 13 (find_best_local uses unreliable mif2 internal log-lik): C — minor, human missed
- Minor 14 (mu_IR fixed without justification in literature): C — minor, human missed
- Minor 15 (QQ-plot non-normality acknowledged but not addressed): C — minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Initial conditions fixed at biologically implausible values — S=N, R=0, I=270,000 fixed")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No benchmark comparison — SEIR and SARIMA log-likelihoods not computed on compatible basis")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major 1 (global search anchored to local-search solution): A — major, human missed
- Major 2 (self-acknowledged non-convergence undermines SEIR conclusions): A — major, human missed
- Major 3 (H accumulates recoveries rather than new infections): A — major, human missed
- Major 4 (normal approximation with no lower bound enforcement): A — major, human missed
- Major 5 (insufficient computational effort — Np=1000, Nmif=100): A — major, human missed
- Major 6 (no benchmark; SARIMA vs SEIR comparison invalid — incompatible likelihood bases): B — major (matches Human Issue #7)
- Major 7 (no profile likelihoods or parameter identifiability analysis): A — major, human missed
- Major 8 (initial conditions biologically implausible — S=N, R=0): B — major (matches Human Issue #5)
- Minor 9 (SARIMA non-invertible/non-causal acknowledged but not addressed): C — minor, human missed
- Minor 10 (AIC table computed with two separate sequential searches): C — minor, human missed
- Minor 11 (covariate gap Nov 12 – Dec 8): C — minor, human missed
- Minor 12 (global search uses Np=100 inconsistent with local search Np=1000): C — minor, human missed
- Minor 13 (starting parameter table lists N twice — error): C — minor, human missed
- Minor 14 (no model diagnostics — ESS, conditional log-likelihoods): C — minor, human missed
- Minor 15 (no session information, package versions, or compute time): C — minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "ID 22.17.6 — Initial conditions implausible for mid-pandemic start — S=N, R=0 on June 5, 2021")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "ID 22.17.1 — SARIMA vs SEIR likelihood comparison requires qualification — different data transformations")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- ID 22.17.2 (H accumulates recoveries not new infections): A — major, human missed
- ID 22.17.3 (SARIMA model selection contradicts AIC table): A — major, human missed
- ID 22.17.6 (initial conditions implausible for mid-pandemic start): B — major (matches Human Issue #5)
- ID 22.17.4 (no profile likelihood; identifiability not assessed): A — major, human missed
- ID 22.17.7 (incomplete convergence, strong conclusions without qualification): A — major, human missed
- ID 22.17.1 (SARIMA vs SEIR likelihood comparison requires qualification): B — major (matches Human Issue #7)
- Np=100 for global search likelihood evaluation: C — minor, human missed
- Nm/Nreps values not stated in text: C — minor, human missed
- Simulation trajectories substantially overshoot observed data: C — minor, human missed
- Ljung-Box rejection not reconciled with SARIMA adequacy claim: C — minor, human missed
- Figure caption numbering errors: C — minor, human missed
- Normal measurement model can produce negative counts: C — minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 4 | 6 | 4 |
| B (AI major, human also found) | 1 | 2 | 2 | 2 |
| C (AI minor, human missed) | 6 | 9 | 7 | 6 |
| D (AI minor, human also found) | 2 | 0 | 0 | 0 |
| E (Human found, AI missed) | 7 | 8 | 8 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (1+2) / (1+2+7) = 3/10 = 0.30
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+6) / (6+1+6+2) = 12/15 = 0.80

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+8) = 2/10 = 0.20
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+9) / (4+2+9+0) = 13/15 = 0.87

**Doug**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+8) = 2/10 = 0.20
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+2+7+0) = 13/15 = 0.87

**Evan**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+8) = 2/10 = 0.20
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+6) / (4+2+6+0) = 10/12 = 0.83

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- Human Issue #1 (ACF interpretation / differencing not same as dependence): missed by all 4 reviewers
- Human Issue #2 (AR/MA roots description doesn't match figure; inverse roots clarification): missed by all 4 reviewers
- Human Issue #3 (Residuals y=0 claim unwarranted; centered by construction): missed by all 4 reviewers
- Human Issue #4 (ARMA modeling on log scale would fit better): missed by all 4 reviewers
- Human Issue #6 (Strong weekly cycle not in SEIR model): missed by all 4 reviewers
- Human Issue #8 (Data source unclear; Kaggle outdated; delta variant not mentioned): missed by Charlie, Doug, and Evan; covered by Alex — NOT a consensus miss
- Human Issue #9 (Time-varying beta context; variants/vaccination argument): missed by Charlie, Doug, and Evan; covered by Alex — NOT a consensus miss
- Human Issue #10 (Sign mistake in Binomial expression inherited from W21): missed by all 4 reviewers

Consensus misses (all 4 reviewers failed): Human Issues #1, #2, #3, #4, #6, #10 — 6 out of 10 (60%).

**Unique finds per reviewer:** Human issues covered by only one reviewer and missed by all others.

- Human Issue #8: covered only by Alex (Charlie, Doug, Evan all missed)
- Human Issue #9: covered only by Alex (Charlie, Doug, Evan all missed)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 2 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

All four reviewers raised these AI-only findings (none of which appear in the human issues list):

- H accumulates recoveries rather than new infections (dN_IR instead of dN_EI/dN_SE): raised as major by Alex, Charlie, Doug, and Evan — 1 universal AI-only flag
- No profile likelihood / parameter identifiability not assessed: raised by Alex (minor), Charlie (major), Doug (major), Evan (major) — 1 universal AI-only flag
- Initial conditions biologically implausible (S=N, no prior immunity): raised as major by Alex, Charlie, Doug, Evan — note this partially overlaps with Human Issue #5 (I(0) fixed/large), but all reviewers framed this broader than the human did, and the additional concern about S=N and prior immunity is AI-only — partial overlap; however, Human Issue #5 is already counted as covered

Universal AI-only flags count: 2 issues raised by all four reviewers that the human did not raise at all.

1. Accumulator H tracks recoveries (dN_IR) rather than new infections — all 4 reviewers flagged this as a major flaw not mentioned by the human.
2. No profile likelihood computed for any SEIR parameter — all 4 reviewers flagged this; the human did not mention it.
