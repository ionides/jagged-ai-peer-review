# Ned-Clean Analysis — W22 Project 21

---

## Human Issues

1. ARMA(4,4) is on the limit of the considered range; if it is the best, should one look further? ARMA(4,4) is already a complicated model.
2. The fitted ARMA(4,4) does not adequately explain weekly periodicity; summing cases over weeks could avoid this issue.
3. Raw R output is hard to read and should be avoided; `avg_7` is undefined in the EDA section; labels and captions for figures are needed.
4. Population models are typically close to log-linear, so ARMA modeling is preferred on the log scale.
5. Setting I_0=1 is wildly implausible; simulations struggle at the start; perhaps start later (e.g., April) with a higher I_0, or account for reporting rate issues and undiagnosed cases.
6. The parameters mu_IR, mu_EI, and tau are fixed in the code; this needs more explanation and justification.
7. The delta wave model has problems with its initial conditions.
8. The ARMA analysis is disconnected from the mechanistic modeling; ARMA is fitted to the complete data while the POMP model is fitted partially, making log-likelihood comparison inappropriate.
9. The iterated filtering searches can get lost — especially evident for the delta variant — due to model misspecification or a random walk intensity that is too large.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ARMA applied to non-stationary series without differencing or transformation")
- Human Issue #5: covered (matched by finding: "pre-Delta initial conditions E=0, I=1 not justified")
- Human Issue #6: covered (matched by finding: "local search for pre-Delta perturbs only Beta, rho, eta — mu_EI and mu_IR fixed")
- Human Issue #7: covered (matched by finding: "vaccination compartment initialization numerically negligible and epidemiologically incorrect")
- Human Issue #8: covered (matched by finding: "no comparison of log-likelihoods across segments or to any null model")
- Human Issue #9: missed

**Findings classification:**
- Finding 1 [MAJOR] — degenerate measurement model: SD=mean (CV=1); tau unused from likelihood: A
- Finding 2 [MAJOR] — tau parameter completely unused in dmeas/rmeas/rprocess: A
- Finding 3 [MAJOR] — vaccination compartment initialization incorrect for Delta and Omicron: B (matches Human Issue #7)
- Finding 4 [MAJOR] — mu_EI and mu_IR fixed in pre-Delta local search: B (matches Human Issue #6)
- Finding 5 [MAJOR] — pre-Delta global search uses only 10 starting points vs. 20 for others: A
- Finding 6 [MAJOR] — ARMA applied to non-stationary series without transformation: B (matches Human Issue #4)
- Finding 7 [MAJOR] — no profile likelihood or confidence intervals: A
- Finding 8 [MINOR] — SE filter threshold of 8 too permissive for pre-Delta: C
- Finding 9 [MINOR] — Delta local search evaluation uses only Np=2000: C
- Finding 10 [MINOR] — no comparison of log-likelihoods across segments or to null model: D (matches Human Issue #8)
- Finding 11 [MINOR] — pairs plot combines local and global search particles without labeling: C
- Finding 12 [MINOR] — rmeas uses SD=sqrt(rho*H) but dmeas uses SD=rho*H — inconsistency: C
- Finding 13 [MINOR] — initial pfilter uses only Np=100: C
- Finding 14 [MINOR] — no stationarity analysis before ARMA modeling: C
- Finding 15 [MINOR] — pre-Delta initial conditions E=0, I=1 not justified: D (matches Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ARMA model applied to non-stationary, non-homogeneous full dataset")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "local search for pre-Delta uses very small rw.sd values; mu_EI and mu_IR not perturbed")
- Human Issue #7: covered (matched by finding: "initial conditions do not conserve population in SEIRV models")
- Human Issue #8: covered (matched by finding: "no benchmark comparison for ARMA vs. POMP models")
- Human Issue #9: missed

**Findings classification:**
- Major #1 — dmeas/rmeas SD inconsistency: A
- Major #2 — vaccination rate formula wrong by factor of N in SEIRV models: A
- Major #3 — initial conditions do not conserve population in SEIRV models: B (matches Human Issue #7)
- Major #4 — no profile likelihoods computed: A
- Major #5 — pre-Delta global search only 10 replicates and large MC SE: A
- Major #6 — tau declared but never used in any Csnippet: A
- Major #7 — no benchmark comparison for ARMA vs. POMP: B (matches Human Issue #8)
- Major #8 — no convergence diagnostics for global search: A
- Minor #9 — normal model can produce negative support: C
- Minor #10 — pre-Delta rw.sd very small; mu_EI and mu_IR not perturbed: D (matches Human Issue #6)
- Minor #11 — Delta local search Np=2000 with only 5 pfilter evaluations: C
- Minor #12 — global search box for pre-Delta very narrow: C
- Minor #13 — ARMA applied to non-stationary full dataset without transformation: D (matches Human Issue #4)
- Minor #14 — Omicron sigma values not discussed for biological plausibility: C
- Minor #15 — no model diagnostics beyond forward simulation: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ARMA model fitted to full time series without accounting for structural breaks")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "local search rw.sd values very small; mu_EI and mu_IR not perturbed")
- Human Issue #7: covered (matched by finding: "vaccination compartment initialization incorrectly scaled for Delta and Omicron")
- Human Issue #8: covered (matched by finding: "ARMA benchmark not quantitatively comparable to POMP log-likelihoods")
- Human Issue #9: missed

**Findings classification:**
- Major #1 — dmeas/rmeas SD mismatch: A
- Major #2 — vaccination compartment initialization incorrectly scaled: B (matches Human Issue #7)
- Major #3 — smoothed (non-integer) observations passed to measurement model: A
- Major #4 — no profile likelihoods or confidence intervals: A
- Major #5 — no model diagnostics: A
- Major #6 — ARMA benchmark not quantitatively comparable to POMP: B (matches Human Issue #8)
- Major #7 — tau declared but never used: A
- Major #8 — accumulator H tracks recoveries (dN_IR) not new detected cases: A
- Minor: rw.sd values very small; mu_EI and mu_IR not perturbed: D (matches Human Issue #6)
- Minor: pre-Delta global search uses only 10 replicates: C
- Minor: convergence traces not described in text: C
- Minor: pairs plot filter threshold loglik.se < 8 unusually permissive: C
- Minor: vaccination rate alpha/N dimensionally inconsistent: C
- Minor: Omicron R computed as residual — extreme assumption not justified: C
- Minor: no quantitative goodness-of-fit summary: C
- Minor: ARMA fitted to full series without accounting for structural breaks: D (matches Human Issue #4)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ARMA without log-transformation; ACF shows weekly seasonality at lag 7")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ARMA without log-transformation; consider log-transform before fitting")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "pre-Delta rw.sd only perturbs Beta, rho, eta; mu_IR and mu_EI not perturbed")
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "ARMA benchmark not quantitatively compared to POMP models")
- Human Issue #9: covered (matched by finding: "pre-Delta search unconverged; chains spread over 2500 log-lik units; large MC SE")

**Findings classification:**
- 22.21.1 [MAJOR] — measurement model degenerate and internally inconsistent (SD mismatch): A
- 22.21.6 [MAJOR] — tau declared but unused in dmeas/rmeas: A
- 22.21.9 [MAJOR] — Omicron vaccination compartment initialized wrong (V ≈ 300,000 instead of ~177 million): A
- 22.21.2 [MAJOR] — no profile likelihoods or confidence intervals: A
- 22.21.3 [MAJOR] — ARMA benchmark not quantitatively compared to POMP: B (matches Human Issue #8)
- 22.21.4 [MAJOR] — pre-Delta search unconverged; large MC SE (9.7); chains diffuse: B (matches Human Issue #9)
- M1 [MAJOR] — biologically implausible parameter estimates not discussed (mu_IR=0.86, rho=0.9999): A
- 22.21.15 [MINOR] — mu_IR and mu_EI not perturbed in pre-Delta local search: D (matches Human Issue #6)
- 22.21.7 [MINOR] — ARMA without log-transformation; ACF shows weekly seasonality: D (matches Human Issues #2 and #4)
- 22.21.10 [MINOR] — no filtering diagnostics (ESS, conditional log-lik): C
- 22.21.11 [MINOR] — Delta parameter non-identifiability not discussed: C
- 22.21.13 [MINOR] — ARMA on full series vs. POMP on sub-segments; inconsistent comparison: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

Note: Finding 22.21.7 covers both Human Issue #2 (weekly periodicity) and Human Issue #4 (log-scale preference), contributing 2 to the D count from a single finding.

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 4 | 6 | 6 | 5 |
| B (AI major, human also found) | 3 | 2 | 2 | 2 |
| C (AI minor, human missed) | 6 | 5 | 6 | 3 |
| D (AI minor, human also found) | 2 | 2 | 2 | 3 |
| E (Human found, AI missed) | 4 | 5 | 5 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | B+D | B+D+E | Human Recall | A | C | A+B+C+D | AI-Unique Rate |
|----------|---|---|---|-----|-------|-------------|---|---|---------|---------------|
| Alex | 3 | 2 | 4 | 5 | 9 | 55.6% | 4 | 6 | 15 | 66.7% |
| Charlie | 2 | 2 | 5 | 4 | 9 | 44.4% | 6 | 5 | 15 | 73.3% |
| Doug | 2 | 2 | 5 | 4 | 9 | 44.4% | 6 | 6 | 16 | 75.0% |
| Evan | 2 | 3 | 4 | 5 | 9 | 55.6% | 5 | 3 | 13 | 61.5% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer:

- **H1:** ARMA(4,4) is on the limit of the considered range; should one look further? — missed by Alex, Charlie, Doug, Evan (4 out of 4)
- **H3:** Raw R output hard to read; `avg_7` undefined in EDA; labels and captions needed — missed by Alex, Charlie, Doug, Evan (4 out of 4)

**Total consensus misses: 2 out of 9 human issues (22.2%)**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- **H2** (weekly periodicity): covered only by Evan (22.21.7); missed by Alex, Charlie, Doug
- **H5** (I_0=1 implausible): covered only by Alex (Finding 15); missed by Charlie, Doug, Evan
- **H9** (searches get lost; delta variant; too-large RW intensity): covered only by Evan (22.21.4); missed by Alex, Charlie, Doug

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 (H5) |
| Charlie | 0 |
| Doug | 0 |
| Evan | 2 (H2, H9) |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- **Degenerate/inconsistent measurement model (dmeas SD=mean; dmeas/rmeas mismatch):** raised as Major by Alex (#1, #12), Charlie (#1), Doug (#1), Evan (22.21.1) — all four reviewers flagged this as a major issue; human missed it entirely.
- **tau parameter declared but unused in model equations:** raised as Major by Alex (#2), Charlie (#6), Doug (#7), Evan (22.21.6) — all four reviewers; human missed it (human only noted tau was "fixed," not absent from the likelihood).
- **No profile likelihoods or confidence intervals:** raised as Major by Alex (#7), Charlie (#4), Doug (#4), Evan (22.21.2) — all four reviewers; human missed it entirely.

**Total universal AI-only flags: 3**
