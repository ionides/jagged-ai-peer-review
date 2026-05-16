# Ned-Clean Analysis — W21 Project 07

---

## Human Issues

1. The interpretation "profile is flat, suggesting convergence issues or nonlinearity of the likelihood surface" is incorrect — a flat profile can result from a linear parameter tradeoff with perfect convergence; the appropriate conclusion is weak or non-identifiability, not the stated causes.
2. It may be unsurprising that simulations do not agree with the particular timing of the information epidemic peaks — the model has no information to enable this; descriptive properties like peak size and width are a better basis for comparison.
3. Rather than estimating N to fit in with the normalization, one could try to include the normalization in the measurement model.
4. The plots called "profiles" are incorrectly calculated — they are computed as a profile over eta but plotted against other parameters, which explains some interpretation issues.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "N is unidentifiable and its interpretation is unclear — N and rho confounded by arbitrary normalization")
- Human Issue #4: covered (matched by finding: "Profile likelihood code uses guesses instead of guesses2 — profiles are not profile likelihoods")

**Findings classification:**

Note: Alex uses three severity labels — [Major], [Moderate], and [Minor]. [Moderate] findings are treated as Minor (not Major) for categorization purposes.

- Finding 1 (Global search at run_level=1): A — AI major, human did not raise this
- Finding 2 (Profile code uses guesses not guesses2): B — AI major, matches Human Issue #4
- Finding 3 (Negative binomial misspecified — H as size parameter): A — AI major, human did not raise this
- Finding 4 (mif2 Nmif argument missing label): A — AI major, human did not raise this
- Finding 5 (Profile CI for Beta extracted from global search): A — AI major, same error type as H4 but H4 already matched; human did not separately raise this specific CI-extraction aspect
- Finding 6 (Data preprocessing replaces "<1" with 0): A — AI major, human did not raise this
- Finding 7 (rw.sd in profile omits key parameters) [Moderate→Minor]: C — AI minor, human did not raise this
- Finding 8 (No likelihood ratio test against simpler benchmark) [Moderate→Minor]: C — AI minor, human did not raise this
- Finding 9 (N unidentifiable and unclear interpretation) [Moderate→Minor]: D — AI minor, matches Human Issue #3
- Finding 10 (Spectral analysis on second half of data) [Moderate→Minor]: C — AI minor, human did not raise this
- Finding 11 (Initial conditions partially fixed without justification) [Moderate→Minor]: C — AI minor, human did not raise this
- Finding 12 (H accumulator initialized to 5) [Moderate→Minor]: C — AI minor, human did not raise this
- Finding 13 (Pairs plot mixes guesses and results) [Minor]: C — AI minor, human did not raise this
- Finding 14 (Conclusion overstates what model demonstrated) [Minor]: C — AI minor, human did not raise this
- Finding 15 (No convergence diagnostics for MIF2) [Minor]: C — AI minor, human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 8: "Data normalization makes count-based measurement model questionable — NB model inappropriate for normalized index, N uninterpretable")
- Human Issue #4: covered (matched by finding 1: "Profile likelihood iterates over wrong design — results2 never uses guesses2")

**Findings classification:**
- Finding 1 (Profile iterates over wrong design — guesses vs. guesses2): B — AI major, matches Human Issue #4
- Finding 2 (Final analysis runs at debug-level run_level=1): A — AI major, human did not raise this
- Finding 3 (Measurement model misspecified — H as size parameter): A — AI major, human did not raise this
- Finding 4 (Key parameters rho and N not perturbed in mif2): A — AI major, human did not raise this
- Finding 5 (No IF2 convergence diagnostics): A — AI major, human did not raise this
- Finding 6 (No benchmark comparison): A — AI major, human did not raise this
- Finding 7 (Arbitrary hard filter on loglik removes valid results): A — AI major, human did not raise this
- Finding 8 (Data normalization makes count-based measurement model questionable): B — AI major, matches Human Issue #3
- Finding 9 (Profile for eta range [0.01,0.1] misaligned with global search upper bound 1.0): C — AI minor, human did not raise this
- Finding 10 (Profile for mu_RS uninformative but no structural response offered): C — AI minor, human did not raise this
- Finding 11 (Simulation diagnostics are forward simulations, not filtering-distribution): C — AI minor, human did not raise this
- Finding 12 (loglik.se threshold of 2 is very permissive): C — AI minor, human did not raise this
- Finding 13 (Profile mif2 cooling.fraction.50=0.3 differs from global search 0.5): C — AI minor, human did not raise this
- Finding 14 (Commented-out code left in Rmd): C — AI minor, human did not raise this
- Finding 15 ("Benchmark" refers to manually chosen parameter set, not model class): C — AI minor, human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 7: "Population N treated as free parameter on normalized data — lacks clear interpretation")
- Human Issue #4: covered (matched by finding 1: "Pseudo-profile likelihood: no dedicated profile IF2 search was executed")

**Findings classification:**
- Finding 1 (Pseudo-profile: guesses2 constructed but guesses iterated in stew block): B — AI major, matches Human Issue #4
- Finding 2 (No non-mechanistic benchmark comparison): A — AI major, human did not raise this
- Finding 3 (Severely inadequate computational effort — run_level=1): A — AI major, human did not raise this
- Finding 4 (Misspecified negative binomial — H as size parameter): A — AI major, human did not raise this
- Finding 5 (rho excluded from rw.sd without justification): A — AI major, human did not raise this
- Finding 6 (Initial conditions H=5 not reset by accumvars): A — AI major, human did not raise this
- Finding 7 (Population N as free parameter on normalized data): B — AI major, matches Human Issue #3
- Finding 8 (Benchmark pfilter uses manual simulation parameters not MLE): C — AI minor, human did not raise this
- Finding 9 (Profile for eta never plotted despite guesses2 constructed): C — AI minor, human did not raise this
- Finding 10 (Global search Nmif argument passed without name): C — AI minor, human did not raise this
- Finding 11 (Goodness-of-fit assessment is purely visual): C — AI minor, human did not raise this
- Finding 12 (H accumulates dN_SI but observations represent search frequency): C — AI minor, human did not raise this
- Finding 13 (No convergence diagnostics): C — AI minor, human did not raise this
- Finding 14 (Model corroboration with external knowledge absent): C — AI minor, human did not raise this
- Finding 15 (Notation inconsistency — beta vs. Beta): C — AI minor, human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 21.07.M3: "Population size N has no clear physical interpretation — normalized data makes N and rho uninterpretable")
- Human Issue #4: covered (matched by finding 21.07.2: "Profile likelihood computation uses the wrong grid — stew block iterates guesses not guesses2")

**Findings classification:**
- 21.07.1 (Debug-scale computations throughout): A — AI major, human did not raise this
- 21.07.2 (Profile likelihood computation uses wrong grid): B — AI major, matches Human Issue #4
- 21.07.3 (No benchmark comparison against non-mechanistic model): A — AI major, human did not raise this
- 21.07.4 (No convergence diagnostics): A — AI major, human did not raise this
- 21.07.5 (Measurement model parameterization — H as size parameter): C — AI minor, human did not raise this
- 21.07.6 (rho and N excluded from rw.sd): C — AI minor, human did not raise this
- 21.07.7 (Spectral analysis subsets to last 43 days without justification): C — AI minor, human did not raise this
- 21.07.M1 (ESS not monitored): C — AI minor, human did not raise this
- 21.07.M2 (Best log-likelihood not stated in prose): C — AI minor, human did not raise this
- 21.07.M3 (Population size N has no clear physical interpretation): D — AI minor, matches Human Issue #3

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 6 | 5 | 3 |
| B (AI major, human also found) | 1 | 2 | 2 | 1 |
| C (AI minor, human missed) | 8 | 7 | 8 | 5 |
| D (AI minor, human also found) | 1 | 0 | 0 | 1 |
| E (Human found, AI missed) | 2 | 2 | 2 | 2 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | B+D | B+D+E | Human Recall | A | C | A+C | A+B+C+D | AI-Unique Rate |
|----------|--:|--:|--:|----:|------:|-------------:|--:|--:|----:|---------:|---------------:|
| Alex | 1 | 1 | 2 | 2 | 4 | 50.0% | 5 | 8 | 13 | 15 | 86.7% |
| Charlie | 2 | 0 | 2 | 2 | 4 | 50.0% | 6 | 7 | 13 | 15 | 86.7% |
| Doug | 2 | 0 | 2 | 2 | 4 | 50.0% | 5 | 8 | 13 | 15 | 86.7% |
| Evan | 1 | 1 | 2 | 2 | 4 | 50.0% | 3 | 5 | 8 | 10 | 80.0% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- **Human Issue #1:** The interpretation "profile is flat, suggesting convergence issues or nonlinearity" is incorrect — appropriate conclusion is weak/non-identifiability. Missed by all 4 reviewers.
- **Human Issue #2:** Simulations not agreeing with timing of peaks is unsurprising; descriptive properties (peak size, width) are a better basis for comparison. Missed by all 4 reviewers.

**Consensus misses: 2 out of 4 human issues (50%)**

### Unique finds per reviewer

Issues covered by exactly one reviewer and missed by all others:

- H3 (include normalization in measurement model / N uninterpretable on normalized data): covered by Alex, Charlie, Doug, and Evan — not a unique find for any single reviewer.
- H4 (profiles incorrectly calculated): covered by Alex, Charlie, Doug, and Evan — not a unique find for any single reviewer.

No human issue was covered by exactly one reviewer and missed by all others.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- **Run_level=1 / debug-scale computation:** Raised as Major by Alex (finding 1), Charlie (finding 2), Doug (finding 3), and Evan (21.07.1). Human did not raise this.
- **No benchmark comparison against non-mechanistic model:** Raised as Major by Charlie (finding 6), Doug (finding 2), and Evan (21.07.3). Alex raises it as Moderate/Minor (finding 8). Three of four treat it as Major.
- **No convergence diagnostics:** Raised as Major by Charlie (finding 5) and Evan (21.07.4). Alex raises it as Minor (finding 15). Doug raises it as Minor (finding 13). Two of four treat it as Major; all four raise it.
- **Negative binomial measurement model misspecified (H as size parameter):** Raised as Major by Alex (finding 3), Charlie (finding 3), and Doug (finding 4). Evan raises it as Minor (21.07.5). Three of four treat it as Major; all four raise it.
- **rho and/or N excluded from rw.sd:** Raised as Major by Charlie (finding 4) and Doug (finding 5). Alex raises it as Moderate/Minor (finding 7). Evan raises it as Minor (21.07.6). All four raise it.

Issues raised as Major by all four reviewers (universal AI-only Major flags):

- **Run_level=1 / debug-scale computation** (universal Major across all four reviewers): 1 issue

**Universal AI-only flags (raised by all four reviewers, human missed): 5 distinct issues total**
- Run_level=1 (all four as Major)
- No benchmark comparison (all four; Major by Charlie, Doug, Evan; Minor/Moderate by Alex)
- No convergence diagnostics (all four; Major by Charlie, Evan; Minor by Alex, Doug)
- NB measurement model misspecified — H as size (all four; Major by Alex, Charlie, Doug; Minor by Evan)
- rho/N excluded from rw.sd (all four; Major by Charlie, Doug; Minor/Moderate by Alex, Evan)
