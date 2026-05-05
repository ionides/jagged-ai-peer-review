# Ned-Clean Analysis — W22 Project 14

---

## Human Issues

1. One could use t-distributed returns within a stochastic volatility model (suggestion for improvement with t-distributed returns).
2. The ARMA models should have been fitted to the return (difference of log price) rather than the raw data; the code reveals they are fitted to the raw data.
3. The AR-GARCH model is undefined — a model specification should be written out.
4. The convergence diagnostics for the Breto model are disappointing, showing decreasing likelihoods and substantial variation, possibly indicating model misspecification.
5. The local search for the stochastic volatility model shows a steady decline in likelihood as random walk variance on parameters is reduced, indicative of model misspecification.
6. In the Heston model, the first plot lacks proper interpretation or caption to describe which row is simulated volatility vs. actual volatility.
7. It would be helpful to compare simulations from all the fitted models.
8. Typo: The Heston model notation for Brownian motions is unclear — W=(W^s, W^nu) should be a bivariate Brownian motion.
9. Typo: Fixing mu=1 looks like a typo; fixing mu=0 is more natural and matches what happened in the code.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Issue 1 (Heston state equation mismatch — sqrt(V) in AR term): A — Critical code/model mismatch; human missed
- Issue 2 (Bake/stew cache files absent — reproducibility failure): A — Major reproducibility concern; human missed
- Issue 3 (Inconsistent caching: bake vs stew, double bake call): A — Code infrastructure inconsistency; human missed
- Issue 4 (LL comparison on different scales/different observation counts): A — Invalid cross-model comparison; human missed
- Issue 5 (Variable name typo eth.sd_ivp vs eth_rw.sd_ivp): A — Code bug; human missed
- Issue 6 (Heston global search box physically unreasonable ranges): A — Search box misspecification; human missed
- Issue 7 (No AIC or likelihood ratio test for formal model comparison): A — Missing formal model comparison; human missed
- Issue 8 (No simulation-based diagnostic for Heston — possibly filtering simulated data): A — Missing/flawed diagnostic; human missed
- Issue 9 (Misidentification of May 19 crash as Russian hackers): C — Factual error in narrative; human missed
- Issue 10 (Reference section empty): C — Missing bibliography; human missed
- Issue 11 (V<0 guard reflecting boundary not discussed): C — Unacknowledged boundary artifact; human missed
- Issue 12 (Nreps_local asymmetry between models not discussed): C — Computational asymmetry; human missed
- Issue 13 (Cooling schedule fixed without justification): C — Missing sensitivity discussion; human missed
- Issue 14 (Heston credited to W18 Project 16 but departure unexplained): C — Incomplete attribution; human missed
- Issue 15 (Pairs plot filtering inconsistency — Breto filtered, Heston unfiltered): C — Diagnostic inconsistency; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Breto convergence failure interpreted incorrectly — declining LL signals misspecification")
- Human Issue #5: covered (matched by finding: same issue 4 — declining/non-monotone LL in Heston local search also addressed)
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No simulation-based diagnostics / goodness-of-fit assessment")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Issue 1 (Critical math error in Heston rprocess — sqrt(V) substitution): A — Major; human missed
- Issue 2 (Likelihood comparison invalid — AIC/LL mixing and different datasets): A — Major; human missed
- Issue 3 (No profile likelihood analysis): A — Major; human missed
- Issue 4 (Breto convergence failure interpreted incorrectly + Heston declining trace): B — Major (matches Human Issues #4 and #5)
- Issue 5 (Unexplained 6000-unit LL gap between Heston and Breto): A — Major; human missed
- Issue 6 (Variable name typo eth.sd_ivp): A — Major; human missed
- Issue 7 (Breto global search phi box extremely narrow — 0.97 to 0.99): A — Major; human missed
- Issue 8 (AIC comparison without normalization justification): C — Minor; human missed
- Issue 9 (bake() called twice on same file): C — Minor; human missed
- Issue 10 (No simulation-based diagnostics/goodness-of-fit): D — Minor (matches Human Issue #7)
- Issue 11 (Unused covariate in Heston POMP object): C — Minor; human missed
- Issue 12 (Heston local rw.sd large ivp perturbation, few reps, pairs plot commented out): C — Minor; human missed
- Issue 13 (Parameter interpretation absent — no economic meaning for estimates): C — Minor; human missed
- Issue 14 (Missing references section): C — Minor; human missed
- Issue 15 (Confusing language about LL scale in Section 3.2): C — Minor; human missed

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

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Non-convergence acknowledged but results still interpreted — Breto and Heston")
- Human Issue #5: covered (matched by finding: same issue 4 — Heston declining local search trace discussed)
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Missing model diagnostics — no simulation envelopes comparing trajectories to observed returns")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Issue 1 (Breto global search initialized from mif2 result — fictitious global search): A — Major; human missed
- Issue 2 (Breto initial particle filter on simulated data, not real data): A — Major; human missed
- Issue 3 (Heston rprocess algebraically misspecified — sqrt(V) in mean reversion term): A — Major; human missed
- Issue 4 (Non-convergence explicitly acknowledged but LL values still reported and compared): B — Major (matches Human Issues #4 and #5)
- Issue 5 (No profile likelihoods or confidence intervals): A — Major; human missed
- Issue 6 (AIC comparison does not account for Monte Carlo noise in POMP LL): A — Major; human missed
- Issue 7 (bake() double-evaluation pattern — reproducibility fragility): A — Major; human missed
- Issue 8 (Missing model diagnostics — no conditional LL, ESS plots, or simulation envelopes): B — Major (matches Human Issue #7)
- Issue 9 (Variable name typo eth.sd_ivp — dead code): C — Minor; human missed
- Issue 10 (Heston global phi box spans 0–1 with logit transform — effectively unconstrained): C — Minor; human missed
- Issue 11 (Breto sigma_eta box implausibly wide — 0.5 to 600): C — Minor; human missed
- Issue 12 (Heston local rw.sd defined but separate variables unused): C — Minor; human missed
- Issue 13 (LL values presented without standard errors): C — Minor; human missed
- Issue 14 (Stationarity assessment informal — no formal unit root test): C — Minor; human missed
- Issue 15 (Missing references and reproducibility information): C — Minor; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Severe ESS Collapse — t-distributed measurement model explicitly recommended")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Breto Model Non-Convergence")
- Human Issue #5: covered (matched by finding: "Heston Local Search: Declining MIF2 Log-Likelihood Trace")
- Human Issue #6: covered (matched by finding: "Missing figure captions — none of the 23 figures have descriptive captions")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major 1 (Severe ESS collapse throughout filtering + t-distribution recommendation): B — Major (matches Human Issue #1)
- Major 2 (Breto model non-convergence — sigma_eta drifting to extreme values): B — Major (matches Human Issue #4)
- Major 3 (Heston local search declining MIF2 log-likelihood trace): B — Major (matches Human Issue #5)
- Major 4 (No profile likelihoods or confidence intervals): A — Major; human missed
- Major 5 (V_0 non-convergence in Heston model): A — Major; human missed
- Minor 6 (Cross-model likelihood comparison needs explicit justification): C — Minor; human missed
- Minor 7 (ARMA model selection — ARMA(4,4) fits better, AR(4) chosen for simplicity): C — Minor; human missed
- Minor 8 (Reproducibility — no sessionInfo or parameter archive): C — Minor; human missed
- Minor 9 (Typographical errors — spelling only, not mathematical mu=1 typo): C — Minor; human missed
- Minor 10 (Missing figure captions for all 23 figures): D — Minor (matches Human Issue #6)
- Minor 11 (Citation quality — Heston cited via Wikipedia): C — Minor; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 8 | 6 | 6 | 2 |
| B (AI major, human also found) | 0 | 2 | 3 | 3 |
| C (AI minor, human missed) | 7 | 7 | 7 | 6 |
| D (AI minor, human also found) | 0 | 1 | 0 | 1 |
| E (Human found, AI missed) | 9 | 6 | 6 | 5 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|--------------:|
| Alex | 0 | 0 | 9 | 0 / 9 = 0% | 8 | 7 | 15 / 15 = 100% |
| Charlie | 2 | 1 | 6 | 3 / 9 = 33% | 6 | 7 | 13 / 16 = 81% |
| Doug | 3 | 0 | 6 | 3 / 9 = 33% | 6 | 7 | 13 / 16 = 81% |
| Evan | 3 | 1 | 5 | 4 / 9 = 44% | 2 | 6 | 8 / 12 = 67% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: ARMA models fitted to raw data rather than log returns — missed by all 4 reviewers
- Human Issue #3: AR-GARCH model undefined, no written-out specification — missed by all 4 reviewers
- Human Issue #8: Brownian motion notation unclear (W should be bivariate BM) — missed by all 4 reviewers
- Human Issue #9: Fixing mu=1 is a typo; mu=0 is more natural and matches the code — missed by all 4 reviewers

Count: 4 out of 9 human issues (44%) were missed by every reviewer.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1 (t-distributed returns): covered only by Evan (via ESS collapse discussion); missed by Alex, Charlie, Doug.
- Human Issue #6 (first Heston plot lacks caption): covered only by Evan (via missing figure captions); missed by Alex, Charlie, Doug.
- Human Issue #7 (compare simulations from all models): covered by Charlie (minor issue 10) and Doug (major issue 8) — covered by two reviewers, not a unique find for either.

Issues uniquely found by each reviewer (covered by that reviewer, missed by all others):

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 2 (Human Issues #1 and #6) |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

- Heston rprocess algebraically misspecified (sqrt(V) substituted for V in mean-reversion term): raised by Alex (Major 1), Charlie (Major 1), Doug (Major 3), Evan (not explicitly — Evan does not raise this as a standalone finding)

Checking more carefully:
- Heston code mismatch: Alex (yes), Charlie (yes), Doug (yes), Evan (no — Evan does not identify this)
- No profile likelihoods: Alex (no — not raised), Charlie (Major 3 — yes), Doug (Major 5 — yes), Evan (Major 4 — yes)

No single AI-only finding is universal across all four reviewers. Three-reviewer consensus on AI-only issues:

- Heston rprocess mismatch (sqrt(V) bug): Alex, Charlie, Doug — 3 of 4 reviewers
- No profile likelihoods: Charlie, Doug, Evan — 3 of 4 reviewers

Count of universal AI-only flags (all 4 reviewers): 0
