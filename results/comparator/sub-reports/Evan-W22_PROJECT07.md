## Evan

**Coverage record:**
- Human Issue #1: contradiction (AI says the model architecture — no separate measurement noise — is the correct Breto 2014 design; human says the model is missing a normal error)
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "M2 — Cross-model conclusion contradicted by paper's own numbers")
- Human Issue #6: covered (matched by finding: "m2 — ARMA AIC table absent from report body")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "m4 — Inline authoring note not removed")

**Findings classification:**
- M1: A — Baseline pfilter run on simulated data rather than actual returns, making reported log-likelihood improvement uninformative
- M2: B — Cross-model conclusion (POMP outperforms GARCH for both stocks) contradicted by paper's own numbers where Ford t-GARCH exceeds Ford POMP (matches Human Issue #5)
- M3: A — Tesla prediction figure uses Ford volatility bands due to variable naming error in code
- M4: A — No profile likelihoods or confidence intervals reported for any POMP parameter
- M5: F — AI says no separate measurement noise is the correct Breto (2014) architecture; human says the model is missing a normal error (contradicts Human Issue #1)
- m1: C — R_n formula typeset as identically 1 due to LaTeX transcription error; code correctly implements tanh(G_n)
- m2: D — ARMA AIC table absent from report body, only in supplementary Rmd (matches Human Issue #6)
- m3: C — Global search initializes from local search object rather than raw filter, potentially limiting exploration
- m4: D — Inline authoring note "(why we want to use log return instead of return?)" not removed from rendered document (matches Human Issue #9)
- m5: C — Ford uses 1000 particles vs Tesla's 2000 at run_level=3; uneven computational investment undiscussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 1 |
