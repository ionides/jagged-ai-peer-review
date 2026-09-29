## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "22.18.N1 — N=40 annual observations too small for 6-parameter SV model; suggests higher-frequency data")
- Human Issue #2: covered (matched by finding: "22.18.M1 — ARMA(0,0) dismissed without scientific discussion; paper selects ARMA(0,1) without justification")
- Human Issue #3: covered (matched by finding: "22.18.N1 — N=40 annual observations too small for 6-parameter SV model; suggests fixing parameters to reduce model complexity")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- 22.18.3: A — POMP does not have the lowest AIC; stated conclusion is factually incorrect (ARMA(0,0) AIC=10.87 beats POMP AIC=16.45)
- 22.18.2: A — Profile likelihood over phi is degenerate and cannot support CI claims
- 22.18.4: A — Global search best estimate sigma_nu=3.59 is implausible and uninvestigated
- 22.18.5: A — No confidence intervals reported for any POMP parameter
- 22.18.N1: B — N=40 annual observations too small for 6-parameter SV model; underlies most technical failures (matches Human Issues #1 and #3)
- 22.18.6: A — Log-likelihood scale convention for GARCH unclear, making cross-model comparison unreliable
- 22.18.7: C — Local IF2 search does not achieve convergence for all parameters
- 22.18.M1: D — ARMA(0,0) finding dismissed without scientific discussion; paper selects ARMA(0,1) without justification (matches Human Issue #2)
- 22.18.N2: C — Section 5.1 header references SSE Composite Index rather than crude oil (copy-paste artifact)
- 22.18.M2: C — Gaussian measurement noise assumption not acknowledged as limitation for financial data
- 22.18.9: C — Np, Nmif, and number of IF2 replicates not reported in the manuscript

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
