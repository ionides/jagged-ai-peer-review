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
- Finding 1 (Critical State Equation Mismatch Between Model and Code): A — Heston C code uses `phi*sqrt(V)` instead of `phi*V`, fundamentally altering the stochastic process
- Finding 2 (Bake/Stew Files Are Absent): A — cached output files missing; results cannot be independently reproduced
- Finding 3 (Mixing Caching Mechanisms Inconsistently): A — Breto uses `bake()`/`.rds` while Heston uses `stew()`/`.rda`; duplicate bake calls risk cache mismatch
- Finding 4 (Log-Likelihood Comparison on Different Scales/Datasets): A — ARMA-GARCH fit on 9000-obs subset while POMP models use full dataset, making raw log-likelihood comparison invalid
- Finding 5 (Variable Name Typo Breaks Breto Local Search Code): A — `eth.sd_ivp` (dot) referenced but declared variable uses underscore `eth_rw.sd_ivp`
- Finding 6 (Global Search Box Contains Physically Unreasonable Ranges): A — `theta` up to 4 implies 200% SD of returns, orders of magnitude beyond observed data scale
- Finding 7 (No AIC or Likelihood Ratio Test for Formal Model Comparison): A — conclusion that Heston is best rests on raw log-likelihoods with no penalty for parameters or SE of estimate
- Finding 8 (No Simulation-Based Diagnostic for Heston Model): A — Section 4.2 particle filter runs on simulated data rather than real data, conflating diagnostics
- Finding 9 (Misidentification of May 19 2021 Crash Source): C — attributes broad crypto selloff to Russian hackers stealing Bitcoin rather than China's mining restrictions
- Finding 10 (Reference Section Is Empty): C — Section 6 heading has no content; references are embedded only as footnotes
- Finding 11 (Heston Process Constraints Are Weak): C — `if(V < 0){V = 0;}` reflecting boundary not part of Heston model; may bias parameter estimates
- Finding 12 (eth_Nreps_local Set to 20 for Both Local and Global Breto Searches): C — asymmetry in computational effort between POMP models not discussed
- Finding 13 (Cooling Schedule Fixed Without Justification): C — `cooling.fraction.50 = 0.5` used in both POMP models with no sensitivity analysis
- Finding 14 (Heston Model Description Credits Project 16 W18 But Departs Without Explanation): C — source project adaptation not fully transparent given additional departure in state equation
- Finding 15 (Pairs Plot Filtering Inconsistency): C — Breto pairs plot filters to top 50 log units but Heston pairs plot uses all runs unfiltered

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |
