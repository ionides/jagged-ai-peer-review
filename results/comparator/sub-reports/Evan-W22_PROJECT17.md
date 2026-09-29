## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Ljung-Box rejection not reconciled with adequacy claim")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "ID 22.17.6 — initial conditions implausible for mid-pandemic start")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "ID 22.17.1 — SARIMA vs SEIR likelihood comparison requires qualification")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- ID 22.17.2: A — measurement model accumulates recoveries (dN_IR) instead of new infections
- ID 22.17.3: A — SARIMA model selection contradicts the reported AIC table
- ID 22.17.6: B — initial conditions implausible (S=N, R=0) for mid-pandemic start date (matches Human Issue #5)
- ID 22.17.4: A — no profile likelihood; identifiability not assessed
- ID 22.17.7: A — incomplete convergence but strong adequacy conclusions drawn
- ID 22.17.1: B — SARIMA vs SEIR likelihood comparison invalid due to different data transformations (matches Human Issue #7)
- Np=100 for global search: C — low particle count for final likelihood evaluations
- Nm/Nreps values not stated: C — computational parameters not reported in text
- Simulation trajectories overshoot: C — trajectories reach 1.5M daily cases vs observed 800K maximum
- Ljung-Box rejection not reconciled: D — Ljung-Box strongly rejects white-noise residuals yet paper claims adequacy (matches Human Issue #3)
- Figure caption numbering errors: C — captions reference non-existent figure numbers inherited from source project
- Normal measurement model negative counts: C — Normal distribution can yield negative case counts

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
