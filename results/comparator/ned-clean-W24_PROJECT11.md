# Ned-Clean Analysis — W24 Project 11

---

## Human Issues

1. The introduction (and conclusion) reads like ChatGPT-generated text with sweeping, unsubstantiated statements; ChatGPT use should be properly attributed.
2. ADF test is not appropriate for data with time-varying sample variance.
3. Ljung-Box test is of borderline relevance because the null assumes independence, whereas time-varying variance (GARCH/SV) implies lack of independence even if uncorrelated.
4. The sentence "Having verified both the stationarity and independence of the data, we can now proceed to the next stage: selecting an appropriate ARMA model" does not make sense given that ARMA(0,0) would be the only valid model, yet the group later fits GARCH/SV models.
5. ARMA(0,0)+GARCH seems indistinguishable from plain GARCH — the difference (if any) is the software used; this needs explanation and investigation.
6. The stated GARCH log-likelihood seems far too high and much higher than the stated ARMA(0,0)+GARCH log-likelihood; this inconsistency should be noted and resolved.
7. ARMA(0,0) is an iid Gaussian model; it would be helpful to remind the reader of that.
8. The efficiency-market theory explanation in the conclusions applies equally to SV and GARCH, not just an iid model, making it a logical flaw.
9. Since GARCH is white noise (in the weak sense), ARMA+GARCH is in fact non-Gaussian ARMA — this point is not made.
10. The authors did not provide the data and have absolute file references, failing reproducibility expectations.
11. The huge price jump on 2023/05/25 (305 to 379) is not explained in the EDA section, and its potential influence on model fitting (possible reason for low ESS around time 340) is not discussed.
12. In the GARCH analysis the residuals are found to follow a t-distribution, but the POMP model still uses a normal distribution — this inconsistency is not addressed.
13. There is a clear ESS spike around time 340 (and a smaller one around 510) in the filter diagnostics; it would have been useful to mention this spike and investigate whether something notable happens at those time points.
14. The authors could have benefitted from paying attention to peer review on previous similar projects (e.g., the W22 project 07 comments).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Likelihood Values Are Inconsistent Between Sections")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Hardcoded Absolute File Path Prevents Reproducibility")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "No Discussion of POMP Model Simulation or Diagnostic Checks")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (ADF test conclusion inverted): A — inverted null/rejection logic for ADF; human raised test inapplicability (#2), not this inverted-logic point
- Finding 2 (Likelihood Values Inconsistent Between Sections): B — matches Human Issue #6
- Finding 3 (Global search box contradicts convergence values): A — sigma_eta and mu_h convergence values outside box boundaries
- Finding 4 (GARCH definition notational error — sigma_n vs epsilon_n): A — notation conflates conditional SD with iid innovation
- Finding 5 (Section header "ARIMA" vs "ARMA"): C — misleading section label
- Finding 6 (LRT test statistics computed but not reported): C — no numerical evidence shown for hypothesis test
- Finding 7 (Global search uses single starting chain): C — defeats purpose of global search
- Finding 8 (GARCH(1,1) discarded for wrong reason): C — likelihoods on different scales; human raised indistinguishability of models (#5), not this specific point
- Finding 9 (Root interpretation for causality/invertibility confused): C — standard conventions reversed
- Finding 10 (k-period log-return formula typo): C — t_{t-1} typo and incorrect first equality
- Finding 11 (Hardcoded absolute file path): D — matches Human Issue #10
- Finding 12 (Conclusion attributes 1092 to ARMA(0,0)): C — human issue #6 already matched to Finding 2; this is additional detail on same topic
- Finding 13 (Global search phi box overly narrow): C — no justification for restricting phi to [0.95, 0.99]
- Finding 14 (No POMP model diagnostic checks): D — matches Human Issue #13
- Finding 15 ("Daily log volatility" mislabeled): C — describes SD of returns, not log volatility

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Ljung-Box test misinterpretation leads to incorrect modeling motivation")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "GARCH(1,1) discarded on incorrect grounds")
- Human Issue #6: covered (matched by finding: "Inconsistent log-likelihood figures across sections")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Hard-coded absolute path prevents reproducibility")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "No effective sample size (ESS) diagnostics reported")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (No non-mechanistic benchmark comparison): A — POMP never compared to GARCH on common basis
- Finding 2 (Inconsistent log-likelihood figures): B — matches Human Issue #6
- Finding 3 (Global search initialized from single local replicate): A — all 80 chains inherit local IF2 state
- Finding 4 (Incomplete convergence of key parameters): A — mu_h and H_0 non-convergence acknowledged but unresolved
- Finding 5 (No profile likelihoods): A — identifiability not assessed
- Finding 6 (Hard-coded absolute path): B — matches Human Issue #10
- Finding 7 (ADF test conclusion inverted): A — inverted null/rejection logic; human raised test inapplicability (#2), not this specific point
- Finding 8 (Ljung-Box test misinterpretation): B — matches Human Issue #3
- Finding 9 (GARCH(1,1) discarded on incorrect grounds): B — matches Human Issue #5
- Finding 10 (POMP LL lower than ARMA-GARCH not explained): C — optimization failure vs. genuine model deficiency not discussed
- Finding 11 (timing.box variable bug): C — non-standard object will fail in fresh R session
- Finding 12 (Particle filter on simulated data): C — initial PF log-likelihood not comparable to IF2 results
- Finding 13 (No ESS diagnostics reported): D — matches Human Issue #13
- Finding 14 (Missing sessionInfo()): C — pomp API version not recorded
- Finding 15 (Notation inconsistency in POMP model definition): C — R_n = tanh(G_n) substitution not stated explicitly

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

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "ARMA(0,0) selected without acknowledging volatility clustering — Ljung-Box on squared returns needed")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Invalid cross-model log-likelihood comparison in the Conclusion")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Hard-coded local file path")
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "No model diagnostics for the POMP model")
- Human Issue #14: missed

**Findings classification:**
- Finding 1 (Global IF2 search anchored to local search result): A — cooling schedule depleted; starting values from box have no effect
- Finding 2 (Initial particle filter on simulated data): A — log-likelihood not comparable to IF2 results on real data
- Finding 3 (Invalid cross-model LL comparison): B — matches Human Issue #6
- Finding 4 (No profile likelihoods): A — identifiability not assessed despite non-convergence evidence
- Finding 5 (ADF test conclusion inverted): A — inverted null/rejection logic; human raised test inapplicability (#2), not this specific point
- Finding 6 (No benchmark comparison for POMP): A — GARCH constitutes natural non-mechanistic benchmark
- Finding 7 (No model diagnostics for POMP): B — matches Human Issue #13
- Minor: k-period log-return formula error: C — log(X_t/X_{t-1}) is 1-period return, not k-period
- Minor: Hard-coded local file path: D — matches Human Issue #10
- Minor: NVIDIA data file not included: C — same underlying reproducibility issue as Human #10, already matched
- Minor: Inconsistent LL values between sections: C — Human #6 already matched to Finding 3
- Minor: GARCH(1,1) discarded for wrong reasons: C — beta_1 implausibly small; different specific claim from Human #5 (indistinguishability)
- Minor: Shapiro-Wilk test on residuals: C — test statistic and p-value not reported
- Minor: ARMA(0,0) without acknowledging volatility clustering / Ljung-Box on squared returns: D — matches Human Issue #3
- Minor: Missing root plot for ARMA(0,0): C — ARMA(0,0) has no AR or MA polynomial; plot unnecessary
- Minor: Convergence comment overstated (sigma_nu at zero): C — boundary estimate indicating absent leverage; scientifically important
- Minor: Missing sessionInfo(): C — pomp API version not recorded

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 10 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Numerical inconsistency in reported log-likelihoods")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: covered (matched by finding: "POMP measurement model uses Gaussian errors despite evidence that heavy-tailed errors are needed")
- Human Issue #13: covered (matched by finding: "Particle filter ESS degeneracy near time ~300–350 not discussed")
- Human Issue #14: missed

**Findings classification:**
- M1 (POMP model not identified along key parameters): A — sigma_nu collapses to 0, sigma_eta extreme spread, phi fails to converge
- M2 (No profile likelihoods or confidence intervals): A — no uncertainty quantification for POMP parameters
- M3 (POMP Gaussian measurement despite heavy-tail evidence): B — matches Human Issue #12
- m1 (ADF test result misinterpreted): C — inverted null/rejection logic; human raised test inapplicability (#2), not this point
- m2 (ARMA(2,2) better AIC not discussed): C — AIC difference ~2 units; LRT not conducted
- m3 (Numerical inconsistency in log-likelihoods): D — matches Human Issue #6
- m4 (ESS degeneracy near time 300–350 not discussed): D — matches Human Issue #13
- m5 (k-period log-return formula typo): C — log(X_t/X_{t-1}) should be log(X_t/X_{t-k})
- m6 (Forecasting stated as goal but not attempted): C — introduction promises forecasting but none delivered

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 3 | 5 | 5 | 2 |
| B (AI major, human also found) | 1 | 4 | 2 | 1 |
| C (AI minor, human missed) | 9 | 5 | 8 | 4 |
| D (AI minor, human also found) | 2 | 1 | 2 | 2 |
| E (Human found, AI missed) | 11 | 9 | 10 | 11 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (1+2) / (1+2+11) = 3/14 = 0.214
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+9) / (3+1+9+2) = 12/15 = 0.800

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (4+1) / (4+1+9) = 5/14 = 0.357
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+5) / (5+4+5+1) = 10/15 = 0.667

**Doug**
- Human Recall = (B+D) / (B+D+E) = (2+2) / (2+2+10) = 4/14 = 0.286
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+8) / (5+2+8+2) = 13/17 = 0.765

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+2) / (1+2+11) = 3/14 = 0.214
- AI-Unique Rate = (A+C) / (A+B+C+D) = (2+4) / (2+1+4+2) = 6/9 = 0.667

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (E for all four):

- Human Issue #1: ChatGPT-generated text, attribution required
- Human Issue #2: ADF test inappropriate for time-varying sample variance
- Human Issue #4: Flawed reasoning sentence about stationarity and independence leading to ARMA selection
- Human Issue #7: ARMA(0,0) is iid Gaussian; reader should be reminded of this
- Human Issue #8: EMH explanation in conclusion is a logical flaw — applies equally to GARCH/SV, not just iid model
- Human Issue #9: ARMA+GARCH is non-Gaussian ARMA; this equivalence is not noted
- Human Issue #11: The 2023/05/25 price jump is unexplained in EDA and its influence on model fitting not discussed
- Human Issue #14: Authors could benefit from reviewing peer reviews of prior similar projects

Count: 8 out of 14 human issues were missed by every reviewer (8/14 = 57%).

### Unique finds per reviewer

Issues covered by exactly one reviewer and missed by all others:

**Alex:** Human Issue #5 (ARMA(0,0)+GARCH indistinguishable from plain GARCH — software difference) was not covered by Alex. Checking: Charlie covered #5 (Charlie 9=B), Doug missed #5, Evan missed #5. So #5 is not a unique find for Alex. Alex's coverage: #6 (shared with Charlie, Doug), #10 (shared with Charlie, Doug), #13 (shared with Charlie, Doug, Evan). Alex has no unique finds.

**Charlie:** Human Issue #3 (Ljung-Box borderline relevance) — covered by Charlie and Doug, not by Alex or Evan. Not unique to Charlie. Human Issue #5 (GARCH discarded wrong reason) — covered only by Charlie. Alex missed #5, Doug missed #5, Evan missed #5. Charlie #5 is a unique find.

**Doug:** Human Issue #3 — covered by Charlie and Doug. Not unique to Doug.

**Evan:** Human Issue #12 (POMP Gaussian vs t-distribution) — covered only by Evan. Alex missed #12, Charlie missed #12, Doug missed #12. Unique to Evan.

Summary of unique finds:

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 (Human Issue #5: ARMA(0,0)+GARCH indistinguishable from GARCH) |
| Doug | 0 |
| Evan | 1 (Human Issue #12: POMP uses Gaussian despite t-distribution finding) |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

- No profile likelihoods: raised by Alex (Finding 14 partially), Charlie (Finding 5), Doug (Finding 4), Evan (M2). All four reviewers flag the absence of profile likelihoods. The human does not mention this.
- Global search initialized incorrectly (from local search replicate): raised by Alex (Finding 7), Charlie (Finding 3), Doug (Finding 1), Evan (not explicitly — Evan does not mention this). Not universal — Evan omits it.

Universal (all four): No profile likelihoods — 1 issue.

Nearly universal (three of four): Global search initialized from single local replicate (Alex, Charlie, Doug but not Evan) — not counted as universal.
