# Ned-Clean Analysis — W24 Project 15

---

## Human Issues

1. It is better to identify an original data source with a complete description, rather than relying on Kaggle's limited descriptions.
2. For highly peaked count data, consider plotting on a log(x+1) scale.
3. Linear models and autocorrelation analysis may also be better applied on a log scale in such cases.
4. The likelihood ratio test is not correct to use to compare an ARMA and POMP model, as they are not nested models.

---

## Alex

**Coverage record:**
- Human Issue #1 (Kaggle data source): missed
- Human Issue #2 (log scale for plotting): missed
- Human Issue #3 (log scale for linear models/ACF): missed
- Human Issue #4 (LRT invalid, non-nested models): covered (matched by Finding 3 — LRT between non-nested models is invalid)

**Findings classification:**
- Finding 1 (dmeasure/rmeasure inconsistency): A — Major, human missed
- Finding 2 (accumulator C tracks recoveries not spillover): A — Major, human missed
- Finding 3 (LRT invalid, non-nested models): B — Major, matches Human Issue #4
- Finding 4 (profile likelihood truncated at boundary): A — Major, human missed
- Finding 5 (global search uses only one MIF2 run, no cooling restart): A — Major, human missed
- Finding 6 (weak identifiability of eta/eta2 dismissed): A — Major, human missed
- Finding 7 (no profile for beta, R0, mu_RS): A — Major, human missed
- Finding 8 (mu_RS not included in rw.sd for profile): C — Minor, human missed
- Finding 9 (ARMA on count data without addressing non-negativity): C — Minor, human missed
- Finding 10 (dN_Nmu draws from total population N): C — Minor, human missed
- Finding 11 (fmin truncation introduces bias): C — Minor, human missed
- Finding 12 (LRT parameter count incorrect): C — Minor, human missed
- Finding 13 (model.png missing): C — Minor, human missed
- Finding 14 (spectral period dismissed without justification): C — Minor, human missed
- Finding 15 (seed/reproducibility concern): C — Minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (Kaggle data source): missed
- Human Issue #2 (log scale for plotting): missed
- Human Issue #3 (log scale for linear models/ACF): missed
- Human Issue #4 (LRT invalid, non-nested models): covered (matched by Major Issue 3 — LRT is statistically invalid, models not nested)

**Findings classification:**
- Major Issue 1 (dmeas/rmeas inconsistency): A — Major, human missed
- Major Issue 2 (profile likelihood truncated at boundary): A — Major, human missed
- Major Issue 3 (LRT invalid, non-nested models): B — Major, matches Human Issue #4
- Major Issue 4 (global search inadequate — single IF2 run per start): A — Major, human missed
- Major Issue 5 (R initialization does not guarantee N constraint): A — Major, human missed
- Major Issue 6 (no model diagnostics beyond ESS): A — Major, human missed
- Major Issue 7 (profile initialized from mifs_local[[1]] not global MLE): A — Major, human missed
- References section empty: C — Minor, human missed
- rho fixed at 1 without justification: C — Minor, human missed
- R0 formula omits mortality: C — Minor, human missed
- ACF/PACF interpretation overconfident for AR(1): C — Minor, human missed
- Seasonality period of 7 months dismissed without exploring structural reasons: C — Minor, human missed
- rw.sd for eta2 too small: C — Minor, human missed
- saudi_mers_params.csv dependency chain undocumented: C — Minor, human missed
- No sessionInfo or package version documentation: C — Minor, human missed
- model.png referenced but not present: C — Minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1 (Kaggle data source): missed
- Human Issue #2 (log scale for plotting): missed
- Human Issue #3 (log scale for linear models/ACF): missed
- Human Issue #4 (LRT invalid, non-nested models): covered (matched by Major Issue 1 — invalid LRT comparing ARMA and SEIRS)

**Findings classification:**
- Major Issue 1 (LRT invalid, non-nested models): B — Major, matches Human Issue #4
- Major Issue 2 (accumulator tracks recoveries not new infections): A — Major, human missed
- Major Issue 3 (profile rho_CH unreliable; maximum at boundary): A — Major, human missed
- Major Issue 4 (global search initialized from previous mif2 result): A — Major, human missed
- Major Issue 5 (no convergence evidence for global search): A — Major, human missed
- Major Issue 6 (dmeasure/rmeasure inconsistent scaling): A — Major, human missed
- Major Issue 7 (LRT degrees of freedom incorrect): A — Major, human missed
- R_0 formula incorrect: C — Minor, human missed
- Model diagram missing: C — Minor, human missed
- Fixed rho=1 not adequately justified: C — Minor, human missed
- Profile CI computed from wrong source: C — Minor, human missed
- Spectral analysis period calculation error: C — Minor, human missed
- mu in rw.sd absent (note only): C — Minor, human missed
- Insufficient Np and Nmif: C — Minor, human missed
- No model diagnostics beyond ESS: C — Minor, human missed
- Pairs plot uses local search results for profile section: C — Minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (Kaggle data source): missed
- Human Issue #2 (log scale for plotting): missed
- Human Issue #3 (log scale for linear models/ACF): covered (matched by finding 24.15.7 — Gaussian ARMA applied to skewed count data; same underlying concern that linear/Gaussian models are inappropriate for count data without transformation)
- Human Issue #4 (LRT invalid, non-nested models): covered (matched by finding 24.15.1 — invalid LRT comparing ARMA and SEIRS)

**Findings classification:**
- 24.15.1 (LRT invalid, non-nested models): B — Major, matches Human Issue #4
- 24.15.2 (profile likelihood maximum outside evaluated range): A — Major, human missed
- 24.15.4 (IF2 non-convergence for mu_RS and rho_CH): A — Major, human missed
- 24.15.5 (global search reveals extreme parameter dispersion): A — Major, human missed
- 24.15.3 (no replicated pfilter evaluations): A — Major, human missed
- 24.15.17 (conclusion overstates statistical evidence from invalid LRT): A — Major, human missed
- 24.15.6 (R0 = 2.6 without CI or identifiability check): C — Minor, human missed
- 24.15.7 (Gaussian ARMA on skewed count data): D — Minor, matches Human Issue #3
- 24.15.8 (best-fit parameter vector not shown): C — Minor, human missed
- 24.15.18 (4x multiplier not estimated within model): C — Minor, human missed
- 24.15.9 (same eta2 for initial E and I without sensitivity): C — Minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 6 | 6 | 5 |
| B (AI major, human also found) | 1 | 1 | 1 | 1 |
| C (AI minor, human missed) | 7 | 9 | 9 | 4 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 3 | 3 | 3 | 2 |

---

## Per-Reviewer Metrics

Human Recall = (B+D) / (B+D+E)
AI-Unique Rate = (A+C) / (A+B+C+D)

| Reviewer | B | D | E | A | C | Human Recall | AI-Unique Rate |
|----------|--:|--:|--:|--:|--:|-------------:|---------------:|
| Alex | 1 | 0 | 3 | 6 | 7 | 1/4 = 25.0% | 13/14 = 92.9% |
| Charlie | 1 | 0 | 3 | 6 | 9 | 1/4 = 25.0% | 15/16 = 93.8% |
| Doug | 1 | 0 | 3 | 6 | 9 | 1/4 = 25.0% | 15/16 = 93.8% |
| Evan | 1 | 1 | 2 | 5 | 4 | 2/4 = 50.0% | 9/11 = 81.8% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Identify original data source rather than relying on Kaggle — missed by all 4 reviewers
- Human Issue #2: Plot highly peaked count data on log(x+1) scale — missed by all 4 reviewers

Count: 2 out of 4 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3 (log scale for linear models/ACF): covered only by Evan (missed by Alex, Charlie, Doug)
- Human Issue #4 (LRT invalid): covered by all four reviewers — not a unique find for any.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- dmeasure/rmeasure inconsistency: raised as Major by Alex (Finding 1), Charlie (Major Issue 1), Doug (Major Issue 6) — Evan does not explicitly raise this as a separate finding (the 4x multiplier is mentioned as a Minor point 24.15.18, not the dmeas/rmeas code inconsistency directly). So this is not truly universal across all four.
- Profile likelihood truncated / maximum at boundary: raised as Major by Alex (Finding 4), Charlie (Major Issue 2), Doug (Major Issue 3), Evan (24.15.2) — raised by all four as Major. Human missed.
- Global search convergence / inadequate optimization: raised as Major by Alex (Finding 5), Charlie (Major Issue 4), Doug (Major Issues 4 and 5), Evan (24.15.4 and 24.15.5) — raised by all four as Major. Human missed.

Universal AI-only Major flags (raised by all four reviewers, human missed): 2

1. Profile likelihood is truncated — its maximum lies at the boundary of the evaluated range, making the reported CI invalid.
2. Global search / IF2 convergence inadequacy — insufficient computation, non-convergence of key parameters, or global search not properly initialized.
