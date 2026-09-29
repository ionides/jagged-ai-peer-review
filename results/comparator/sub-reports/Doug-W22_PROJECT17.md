## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SARIMA model not invertible or causal, roots outside unit circle")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "initial conditions fixed at biologically implausible values, including I=270,000 and S=N")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no benchmark comparison — SARIMA and SEIR log-likelihoods not on compatible basis")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (global search anchored to local-search solution): A — genuine global search not performed; human did not raise this
- Finding 2 (self-acknowledged non-convergence undermines SEIR conclusions): A — non-convergence acknowledged but conclusions drawn anyway; human did not raise this
- Finding 3 (accumulator variable accumulates recoveries not new infections): A — H += dN_IR is a model misspecification; human did not raise this
- Finding 4 (measurement model normal approximation with no lower bound enforcement): A — inappropriate for overdispersed count data; human did not raise this
- Finding 5 (insufficient computational effort, Np=1000, Nmif=100): A — run_level=2 inadequate for 13-parameter model; human did not raise this
- Finding 6 (SARIMA and SEIR log-likelihoods not on compatible basis, comparison invalid): B — matches Human Issue #7
- Finding 7 (no profile likelihoods or parameter identifiability analysis): A — 11 free parameters with no profiles; human did not raise this
- Finding 8 (initial conditions fixed at biologically implausible values): B — matches Human Issue #5
- Finding 9 (SARIMA model not invertible or causal, roots outside unit circle): D — matches Human Issue #2
- Finding 10 (AIC table via two sequential searches, not joint): C — sequential ARIMA then SARIMA selection; human did not raise this
- Finding 11 (covariate coding gap November 12 to December 8, 2021): C — unassigned period in piecewise table; human did not raise this
- Finding 12 (global search evaluation uses Np=100 inconsistent with local search Np=1000): C — inconsistent particle count across evaluations; human did not raise this
- Finding 13 (N listed twice with conflicting values in parameter table): C — proofreading error in starting points section; human did not raise this
- Finding 14 (no model diagnostics, ESS not monitored, no conditional log-likelihood plots): C — particle filter diagnostics absent; human did not raise this
- Finding 15 (no reproducibility info, no sessionInfo or package versions): C — code supplement deficiency; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
