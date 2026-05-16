# Ned-Clean Analysis — W21 Project 02

---

## Human Issues

1. None of the models can capture the multiple COVID waves; the data shows multiple waves from interventions and new strains, and no model can represent these dynamics — quantitative understanding may require additional modeling detail.
2. Please explain what the "infected" variable measures (e.g., number of positive tests) and whether this raises issues for understanding the data.
3. The project claims it is impossible to use SEIR, SEIQR, and SECSDR to simulate the data, but appropriate modifications could allow these models to fit. The key question is what modification(s) are needed. The project could have hypothesized how extra compartments would fix the problem before implementing them.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding 3: "SEIQR measurement model links Q stock to daily case flow — dimensionally inconsistent")
- Human Issue #3: missed

**Findings classification:**
- Finding 1 [MAJOR]: A — Degenerate normal in SEIR dmeas; sd set equal to mean rather than sqrt(mean)
- Finding 2 [MAJOR]: A — SECSDR rprocess double-deduction / population conservation violation
- Finding 3 [MAJOR]: B — SEIQR links Q (quarantine stock) to daily case observations, raising issues about what observed "Infected" measures (matches Human Issue #2)
- Finding 4 [MAJOR]: A — Cooling fraction and rw.sd essentially zero for SECSDR and SEIQR; optimizer never explored parameter space
- Finding 5 [MAJOR]: A — SEIQR N=32,000,000 instead of US population (~328M)
- Finding 6 [MAJOR]: A — No local search for SECSDR or SEIQR
- Finding 7 [MAJOR]: A — No likelihood comparison across three models
- Finding 8 [MAJOR]: A — Missing data file; reproducibility broken
- Finding 9 [MINOR]: C — SEIR local search rw.sd omits mu_EI and mu_IR
- Finding 10 [MINOR]: C — SEIR simulation uses hard-coded parameters inconsistent with global MLE
- Finding 11 [MINOR]: C — SEIR dmeas/rmeas sd inconsistency (dmeas uses sd=mean; rmeas uses sd=sqrt(mean))
- Finding 12 [MINOR]: C — run_level=1 (toy-level computation) for SECSDR global search
- Finding 13 [MINOR]: C — SECSDR rinit hard-codes population sizes not connected to parameter estimation
- Finding 14 [MINOR]: C — Profile likelihood and confidence intervals absent for all three models
- Finding 15 [MINOR]: C — Introduction lacks quantitative epidemiological motivation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by Minor 14: "No discussion of measurement model's biological meaning — what H, Di, Q represent epidemiologically")
- Human Issue #3: missed

**Findings classification:**
- Major 1: A — Catastrophically misconfigured IF2 for SECSDR and SEIQR (rw.sd=2e-9, cooling.fraction.50=0.00005)
- Major 2: A — Missing data file prevents reproducibility
- Major 3: A — No non-mechanistic benchmark comparison
- Major 4: A — SEIR measurement model misspecified; zero variance when H=0; rmeas uses different variance form than dmeas
- Major 5: A — SECSDR conservation of individuals violated; S decremented by dN_ECa instead of dN_SE
- Major 6: A — No profile likelihood or confidence intervals for any parameter
- Major 7: A — SEIR local search excludes most parameters (mu_EI, mu_IR, tau not in rw.sd)
- Major 8: A — SEIR global search inherits rw.sd from local search without re-specifying
- Major 9: A — SEIQR N=32M instead of US population
- Major 10: A — No convergence diagnostics discussed despite non-convergent traces
- Major 11: A — SECSDR run_level=1 vs SEIQR run_level=2; inconsistent computational effort
- Minor 12: C — No ARIMA or classical time series analysis before mechanistic modeling
- Minor 13: C — Simulation uses hard-coded "best" parameters; second-best set used for SECSDR/SEIQR
- Minor 14: D — No discussion of measurement model's biological meaning; what H/Di/Q represent epidemiologically; 100% reporting assumption unstated (matches Human Issue #2)
- Minor 15: C — References incomplete; only course notes and student projects cited

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 11 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by minor bullet: "SEIQR uses Q stock as mean of observation distribution — treating stock as daily incidence flow")
- Human Issue #3: missed

**Findings classification:**
- Major 1: A — Negligible rw.sd renders IF2 inoperative for SECSDR and SEIQR
- Major 2: A — SEIR dmeasure uses variance = mean-squared; inconsistency between dmeas and rmeas
- Major 3: A — SEIQR N=32M wrong population size
- Major 4: A — No benchmark comparison against non-mechanistic model
- Major 5: A — No profile likelihoods; parameter identifiability not assessed
- Major 6: A — No quantitative goodness-of-fit or model comparison
- Major 7: A — SECSDR rprocess sequential binomial draws without compartment depletion accounting
- Major 8: A — Inconsistent run_level across models; cross-model log-likelihood comparison invalid
- Major 9: A — No model diagnostics (conditional log-likelihoods, ESS, filtering distribution)
- Major 10: A — SECSDR rinit does not include E compartment; statenames omit E
- Minor (URL): C — Ungrammatical URL embedded in running text
- Minor (tau): C — Tau declared in paramnames and partrans but appears nowhere in any Csnippet
- Minor (global search anchor): C — SEIR global search inherits cooling schedule from local search via mf1
- Minor (Q stock): D — SEIQR uses Q (stock) as daily observation mean without differencing; treating stock as flow (matches Human Issue #2)
- Minor (second-best): C — Second-best parameter set selected for SECSDR/SEIQR simulation without justification
- Minor (future work): C — Conclusion discusses temporal phase decomposition without supporting analysis
- Minor (references): C — Reference list cites only student projects; no peer-reviewed literature
- Minor (tau trace): C — SEIR local search traces show tau even though tau not in rw.sd; constant parameter displayed as convergence trace

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by 21.02.5 Major: "SEIQR and SECSDR measurement models use rho as noise only; 100% reporting assumed; implausible for COVID testing context")
- Human Issue #3: missed

**Findings classification:**
- 21.02.1 [Major]: A — SEIR dmeas/rmeas inconsistency; dmeas uses variance=mean^2, rmeas uses variance=mean
- 21.02.2 [Major]: A — Phantom parameter tau declared but never used in any Csnippet
- 21.02.3 [Major]: A — E compartment absent from SECSDR statenames and rinit; latency period collapsed
- 21.02.4 [Major]: A — SEIQR N=32M inconsistent with US scale; exhausts susceptibles unrealistically
- 21.02.5 [Major]: B — SEIQR/SECSDR measurement models assume 100% reporting (rho as noise only), implausible for COVID testing; raises issues about what Infected represents (matches Human Issue #2)
- 21.02.6 [Major]: A — No non-mechanistic benchmark
- 21.02.7 [Major]: A — Numerically absurd log-likelihood values (~-1e14) in SEIQR diagnostics; numerical overflow
- 21.02.8 [Major]: A — No profile likelihoods or confidence intervals
- 21.02.m1 [Minor]: C — Np and Nmif not reported anywhere in manuscript
- 21.02.m2 [Minor]: C — SECSDR rinit hardcodes S=328M with no E initialization
- 21.02.m3 [Minor]: C — No EDA or preliminary time-series analysis; ACF, log-transform absent
- 21.02.m4 [Minor]: C — Data description incomplete; what "Infected" represents not stated (Human Issue #2 already covered by 21.02.5)
- 21.02.m5 [Minor]: C — Reference list minimal; only course notes and student projects cited

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 11 | 10 | 7 |
| B (AI major, human also found) | 1 | 0 | 0 | 1 |
| C (AI minor, human missed) | 7 | 3 | 7 | 5 |
| D (AI minor, human also found) | 0 | 1 | 1 | 0 |
| E (Human found, AI missed) | 2 | 2 | 2 | 2 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 2 | 1/3 = 33% | 6 | 7 | 13/14 = 93% |
| Charlie | 0 | 1 | 2 | 1/3 = 33% | 11 | 3 | 14/15 = 93% |
| Doug | 0 | 1 | 2 | 1/3 = 33% | 10 | 7 | 17/18 = 94% |
| Evan | 1 | 0 | 2 | 1/3 = 33% | 7 | 5 | 12/13 = 92% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: None of the models can capture the multiple COVID waves; dynamics require additional modeling detail. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: Appropriate model modifications exist; the project could have hypothesized what changes are needed before implementing additional compartments. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 3 human issues (67%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2 was covered by all four reviewers (Alex, Charlie, Doug, Evan each addressed it in some form), so no reviewer has a unique find on it.

No human issue was covered by exactly one reviewer.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- Misconfigured mif2 (rw.sd/cooling near zero) for SECSDR and SEIQR: raised by Alex (Finding 4, Major), Charlie (Major 1), Doug (Major 1), Evan (not explicitly as a single finding — Evan raises the issue indirectly via the numerically absurd likelihoods finding 21.02.7, but does not explicitly call out the rw.sd misconfiguration). Raised by 3 of 4 reviewers as Major.
- SEIQR N=32M wrong population size: raised by Alex (Finding 5, Major), Charlie (Major 9), Doug (Major 3), Evan (21.02.4, Major). Raised by all 4 reviewers as Major. → Universal AI-only Major flag.
- No profile likelihoods / confidence intervals: raised by Alex (Finding 14, Minor), Charlie (Major 6), Doug (Major 5), Evan (21.02.8, Major). Raised by all 4 reviewers (Major by 3, Minor by 1). → Universal AI-only flag (near-universal as Major).
- SECSDR/SEIQR compartment / conservation error: raised by Alex (Finding 2, Major), Charlie (Major 5), Doug (Major 7 and Major 10), Evan (21.02.3, Major). Raised by all 4 reviewers as Major. → Universal AI-only Major flag.
- No non-mechanistic benchmark: raised by Charlie (Major 3), Doug (Major 4), Evan (21.02.6, Major). Raised by 3 of 4 as Major (Alex does not raise this). Not universal.
- Missing data file: raised by Alex (Finding 8, Major), Charlie (Major 2). Raised by 2 of 4. Not universal.
- SEIR dmeas/rmeas mismatch: raised by Alex (Finding 1+11), Charlie (Major 4), Doug (Major 2), Evan (21.02.1, Major). Raised by all 4 reviewers. → Universal AI-only Major flag.

**Universal AI-only Major flags (raised as Major by all 4 reviewers, not in human issues):**
1. SEIQR population size N=32M instead of US population (~328M)
2. SECSDR/SEIQR compartment errors (conservation violation or missing E compartment)
3. SEIR dmeas/rmeas inconsistency (variance model mismatch between scoring and sampling)

Count: 3 universal AI-only Major flags.
