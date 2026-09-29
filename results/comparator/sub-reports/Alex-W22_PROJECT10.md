## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "SEAPIRD measurement model statistically incorrect — Normal approximation with wrong parameterization")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Inconsistent population size between SIR and SEAPIRD models — SIR uses N=50M, SEAPIRD uses N=500K"; also matched by finding: "SIR global search passes N=500,000 while model stated to use N=50,000,000")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (Inconsistent population size SIR vs SEAPIRD): B — inconsistent N across models, SIR uses 50M while SEAPIRD uses 500K (matches Human Issue #5)
- Finding 2 (No profile likelihood or formal confidence intervals): A — no uncertainty quantification for any estimated parameter
- Finding 3 (SEAPIRD measurement model statistically incorrect — Normal approximation): B — normal approximation with wrong parameterization for SEAPIRD observation model (matches Human Issue #3)
- Finding 4 (SIR global search passes N=500,000 vs stated N=50,000,000): B — hardcoded N=500,000 in global search contradicts stated model specification (matches Human Issue #5)
- Finding 5 (No likelihood benchmark against null/ARMA on common scale): A — likelihood comparison across models is invalid without common observation scale
- Finding 6 (SEAPIRD branching of exposed class statistically invalid): A — rounding of binomial draw fractions violates conservation of individuals
- Finding 7 (mif2 particle count too low — Np=100 for SIR local search): A — Np=100 causes severe particle degeneracy
- Finding 8 (Intervention covariate structure arbitrary): A — 50-day windows not tied to any known policy or epidemiological events
- Finding 9 (SIR rinit sets H=169 instead of 0): C — accumulator variable incorrectly initialized to 169 at t0
- Finding 10 (SEAPIRD rinit sets S=N, population not conserved): C — S=N while I=169 at initialization violates population accounting
- Finding 11 (Weekly periodicity identified but not incorporated into POMP models): C — day-of-week covariate absent from both SIR and SEAPIRD models
- Finding 12 (Smoothed vs raw data inconsistency between models): C — SEAPIRD text claims smoothed data but code uses raw, inconsistent with SIR
- Finding 13 (SEAPIRD global best-fit parameters biologically implausible): C — mu_AR=3.49/day implies <7-hour asymptomatic recovery
- Finding 14 (No convergence diagnostics for SIR — eval=FALSE): C — SIR log likelihood convergence plots suppressed in rendered document
- Finding 15 (Data preprocessing slice operation fragile): C — non-intuitive trimming logic unexplained, November data inclusion unjustified

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
