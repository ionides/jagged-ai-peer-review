# Ned-Clean Analysis — W24 Project 01

---

## Human Issues

1. The dataset must somehow determine whether an election is free and fair, since many autocracies claim to have a democratic mandate. A brief explanation would help the reader.
2. Is there an error in Fig. 1? Z(t) seems to be defined as non-negative. It is unusual to require delta Z(t) to be non-negative.
3. The diagram is written with S as a compartment, and in the Csnippet the value of S changes dynamically. For a covariate, the value would be data. New sovereign states entering S could be considered as a covariate process, analogous to birth/immigration in an epidemic model.
4. Delta Z(t) is described as the number of democracies, but is it actually the change in that number? The plot of the graphs for Z(t) and delta Z(t) seem incorrectly labeled.
5. From the measurement model, it is clear that N counts democracies. But, the model does not let states return from democracy to autocracy.
6. The P and R components are not clearly defined. Beta is introduced without definition.
7. In Fig. 4, beta and mu_PR plots would be clearer with the x-axis on a log scale.
8. Fig. 7. The "moderate evidence" has p-values well above the usual evidence requirements. It is still okay to comment on small and statistically insignificant effects, but this needs explanation.
9. Section 2.2. Fig. 2 is explained to show that the parameter estimates are well identified, but some combinations of them seem weakly identified, for example the nonlinear trade-off between mu_RN and rho.
10. In the profile, k is not identifiable as it has values across its whole range that maximize the likelihood.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "S treated as compartment but used as covariate; no mechanism to replenish S with new sovereign states")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "N accumulates monotonically but is never depleted — model can only predict non-decreasing democracy counts")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "negative correlation between Beta and mu_PR/mu_RN is parameter confounding, not substantive evidence")
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (No mif2 code shown; algorithm identity unclear): A — Major; human missed
- Finding 2 (Global search mislabeled as profile likelihood; CI construction invalid): A — Major; human missed
- Finding 3 (Transition rate uses N not R — code-math mismatch): A — Major; human missed
- Finding 4 (delta-Z truncation not accounted for in measurement model; left-censoring): A — Major; human missed
- Finding 5 (S treated as compartment but also as covariate; no replenishment of new sovereign states): B — Major; matches Human Issue #3
- Finding 6 (N accumulates monotonically, never depleted — no return from democracy): B — Major; matches Human Issue #5
- Finding 7 (AIC for IID model uses wrong parameter count — uses 2 instead of 4): A — Major; human missed
- Finding 8 (Poisson log-likelihood hard-coded rather than computed): A — Major; human missed
- Finding 9 (No convergence diagnostics for global search): C — Moderate (not labeled Major); human missed
- Finding 10 (Figure caption numbering incorrect): C — Moderate; human missed
- Finding 11 (Probe results interpretation contradictory and poorly supported): C — Moderate; human missed
- Finding 12 (Negative exponential relationship in pair plot unsupported; parameter confounding): D — Moderate; matches Human Issue #9
- Finding 13 (Rho interpreted as "coding efficiency" — non-standard): C — Minor; human missed
- Finding 14 (Initial condition for S inconsistent with data; P/R/N initial values unjustified): C — Minor; human missed
- Finding 15 (Poisson log-likelihood stated without derivation or reproducible code): C — Minor; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Structural flaw: state S cannot accommodate new sovereign states")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Observation model inconsistency: stock vs. flow mismatch — N accumulates, delta-Z is a flow, nothing leaves N")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Non-identifiability of mu_PR not acknowledged — ranges five orders of magnitude with near-zero correlation with loglik")
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (Critical mismatch between model description and code — N not R in S→P rate): A — Major; human missed
- Finding 2 (Saved RDS file appears to be from a different model; mu_IR renamed to mu_PR): A — Major; human missed
- Finding 3 (Profile likelihood not computed; CIs are invalid): A — Major; human missed
- Finding 4 (Structural flaw: S cannot accommodate new sovereign states): B — Major; matches Human Issue #3
- Finding 5 (Stock vs. flow mismatch: rho*N(t) for delta-Z(t)): B — Major; matches Human Issue #5
- Finding 6 (No convergence diagnostics for IF2): A — Major; human missed
- Finding 7 (Non-identifiability of mu_PR not acknowledged): B — Major; matches Human Issue #9
- Finding 8 (AIC for IID model uses incorrect number of parameters): C — Minor; human missed
- Finding 9 (Duplicate figure caption variable cap_fig7): C — Minor; human missed
- Finding 10 (Mathematical formula contains typographical error — + instead of =): C — Minor; human missed
- Finding 11 (Benchmark comparison conclusion is imprecise): C — Minor; human missed
- Finding 12 (Parameter search design mislabeled as profile_design): C — Minor; human missed
- Finding 13 (No model diagnostics beyond probes): C — Minor; human missed
- Finding 14 (Initial conditions fixed, not estimated; no sensitivity analysis): C — Minor; human missed
- Finding 15 (No RNG seed documentation for mif2 run): C — Minor; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "24.01.3 — Conservation violation: S never replenished with new sovereign states")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "24.01.8 — Measurement model excludes democratic reversals; backsliding years contribute zero likelihood mass")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "24.01.1 — Beta not well identified; profile conclusions overstated")
- Human Issue #10: missed

**Findings classification:**
- 24.01.2 (Code-math mismatch in S→P transition: N used instead of R): A — Major; human missed
- 24.01.3 (Conservation-of-population violation: S never replenished): B — Major; matches Human Issue #3
- 24.01.8 (Measurement model excludes democratic reversals): B — Major; matches Human Issue #5
- 24.01.1 (Beta not well identified; profile conclusions overstated): B — Major; matches Human Issue #9
- 24.01.9 (No IF2 convergence trace plots): A — Major; human missed
- 24.01.4 (logmeanexp/pfilter documentation unclear): C — Minor; human missed
- 24.01.5 (AIC comparability across same observations not confirmed): C — Minor; human missed
- M1 (ESS not reported): C — Minor; human missed
- M2 (Figure numbering errors — two figures each labeled "Figure 2" and "Figure 7"): C — Minor; human missed
- M3 (Typographical error in transition equation — + instead of =): C — Minor; human missed
- Probes choice (exponential growth rate probe may not be most sensitive for sparse count data): C — Minor; human missed
- rho interpretation (coding efficiency interpretation needs more justification): C — Minor; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "24.01.3 — Conservation violation: S never replenished with new sovereign states")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "24.01.8 — Measurement model excludes democratic reversals; backsliding years contribute zero likelihood mass")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "24.01.1 — Beta not well identified; profile conclusions overstated")
- Human Issue #10: missed

**Findings classification:**
- 24.01.2 (Code-math mismatch in S→P transition: N used instead of R): A — Major; human missed
- 24.01.3 (Conservation-of-population violation: S never replenished): B — Major; matches Human Issue #3
- 24.01.8 (Measurement model excludes democratic reversals): B — Major; matches Human Issue #5
- 24.01.1 (Beta not well identified; profile conclusions overstated): B — Major; matches Human Issue #9
- 24.01.9 (No IF2 convergence trace plots): A — Major; human missed
- 24.01.4 (logmeanexp/pfilter documentation unclear): C — Minor; human missed
- 24.01.5 (AIC comparability across same observations not confirmed): C — Minor; human missed
- M1 (ESS not reported): C — Minor; human missed
- M2 (Figure numbering errors): C — Minor; human missed
- M3 (Typographical error in transition equation — + instead of =): C — Minor; human missed
- Probes choice (exponential growth rate probe may not be most sensitive for sparse count data): C — Minor; human missed
- rho interpretation (coding efficiency interpretation needs more justification): C — Minor; human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 4 | 2 | 2 |
| B (AI major, human also found) | 2 | 3 | 3 | 3 |
| C (AI minor, human missed) | 6 | 8 | 7 | 7 |
| D (AI minor, human also found) | 1 | 0 | 0 | 0 |
| E (Human found, AI missed) | 7 | 7 | 7 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|--------------:|
| Alex | 2 | 1 | 7 | 3/10 = 30% | 6 | 6 | 12/15 = 80% |
| Charlie | 3 | 0 | 7 | 3/10 = 30% | 4 | 8 | 12/15 = 80% |
| Doug | 3 | 0 | 7 | 3/10 = 30% | 2 | 7 | 9/12 = 75% |
| Evan | 3 | 0 | 7 | 3/10 = 30% | 2 | 7 | 9/12 = 75% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer (all four of Alex, Charlie, Doug, Evan):

- Human Issue #1: The dataset must explain how it determines whether an election is free and fair, since autocracies claim democratic mandates.
- Human Issue #2: Possible error in Fig. 1 — Z(t) defined as non-negative makes delta Z(t) non-negative unusual.
- Human Issue #4: Delta Z(t) labeled as number of democracies vs. change in that number; graphs for Z(t) and delta Z(t) appear incorrectly labeled.
- Human Issue #6: P and R components not clearly defined; beta introduced without definition.
- Human Issue #7: In Fig. 4, beta and mu_PR plots would be clearer with x-axis on log scale.
- Human Issue #8: "Moderate evidence" probe p-values well above usual significance thresholds; needs explanation.
- Human Issue #10: In the profile, k is not identifiable.

**Count: 7 out of 10 human issues were missed by every reviewer.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- No human issue was covered uniquely by only one reviewer. The three covered issues (#3, #5, #9) were covered by all four reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- Code-math mismatch in S→P transition (N used instead of R): raised as Major by Alex (Finding 3), Charlie (Finding 1), Doug (24.01.2), Evan (24.01.2).
- No convergence diagnostics for IF2: raised as Major by Alex (Finding 9 — Moderate), Charlie (Finding 6), Doug (24.01.9), Evan (24.01.9).

Note: Alex labeled convergence diagnostics as "MODERATE" rather than Major; the other three labeled it Major. For universality across all four, "code-math mismatch" is the only finding labeled Major by all four reviewers.

**AI-only findings raised by all four reviewers (Major or not):**
- Code-math mismatch in S→P transition: 4/4 reviewers, all labeled Major
- No convergence diagnostics: 4/4 reviewers (Major by Charlie, Doug, Evan; Moderate by Alex)
- Rho interpretation as "coding efficiency" needs more justification: 4/4 reviewers (Minor/Moderate by all)
- Figure numbering errors: 4/4 reviewers (Minor by all)
- Typographical error in transition equation (+ instead of =): raised by Charlie, Doug, Evan (3/4; Alex did not raise this specific typo)

**Count of universal Major AI-only flags: 1 (code-math mismatch). Count of universal AI-only flags at any severity: 3 (code-math mismatch, convergence diagnostics, rho interpretation).**
