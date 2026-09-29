## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SARIMA non-causal and non-invertible; roots inside unit circle not remediated")
- Human Issue #3: covered (matched by finding: "QQ-plot heavy tails acknowledged but not addressed")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "initial conditions violate population conservation; S+E+I > N; implausible susceptible pool including I=270,000")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "direct log-likelihood comparison between SARIMA and SEIR is invalid due to differencing")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (measurement model accumulates recoveries): A — H += dN_IR accumulates recoveries rather than new infections, causing temporal displacement
- Finding 2 (initial conditions violate population conservation): B — S+E+I > N and implausible susceptible pool (matches Human Issue #5)
- Finding 3 (no profile likelihood): A — no profile likelihoods or confidence intervals computed for any SEIR parameter
- Finding 4 (SARIMA non-causal and non-invertible): B — roots inside unit circle acknowledged but model retained without remediation (matches Human Issue #2)
- Finding 5 (invalid SARIMA–SEIR log-likelihood comparison): B — SARIMA likelihood conditions on fewer observations due to differencing (matches Human Issue #7)
- Finding 6 (rw.sd 10x below standard): A — rw.sd = 0.002 for b1–b7 instead of 0.02, hampering IF2 exploration
- Finding 7 (text–code mismatch for b5): C — b5 listed as 1.5 in text but 0.15 in code
- Finding 8 (covariate period for b5 inconsistent): C — text says 13-day b5 window but code implements 40-day window
- Finding 9 (global search uses Np=100 vs Np=1000): C — hardcoded Np=100 in global search pfilter vs Np=1000 in local search
- Finding 10 (no non-mechanistic benchmark): C — no IID or autoregressive baseline comparison for SEIR
- Finding 11 (convergence incomplete but not addressed): C — convergence failure noted but no corrective action taken
- Finding 12 (no model diagnostics for SEIR fit): C — no ESS plot, no conditional log-likelihood trace reported
- Finding 13 (find_best_local uses unreliable mif2 log-likelihood): C — mif2 internal log-likelihood used for selection despite perturbations in final iteration
- Finding 14 (mu_IR fixed without justification): C — mean recovery time fixed at 10 days with no citation or sensitivity analysis
- Finding 15 (QQ-plot non-normality not addressed): D — heavy tails in SARIMA residuals noted but no remediation attempted (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
