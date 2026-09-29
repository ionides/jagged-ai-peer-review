## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Sign Errors in the State Equation Presentation")
- Human Issue #3: covered (matched by finding: "Measurement Model Parametrization Unexplained and Non-Standard")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No Benchmark Comparison")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Initial Conditions E=14 and I=7 Fixed Without Justification")

**Findings classification:**
- Finding 1 (Force-of-Infection Discrepancy Between Text and Code): A — text uses E but code uses I in force of infection; no human issue raised this
- Finding 2 (Sign Errors in State Equation Presentation): B — wrong signs in S and R equations (matches Human Issue #2)
- Finding 3 (Measurement Model Parametrization Unexplained and Non-Standard): B — dnbinom parameterization non-standard/incorrect and unexplained (matches Human Issue #3)
- Finding 4 (Global Search Uses Only mifs_local[[1]] as Starting Template): A — single fixed local run template used for all global search; no human issue raised this
- Finding 5 (eta Profile Fails to Identify the Maximum; CI Is Invalid): A — eta profile never reaches Wilks threshold yet CI is still reported; no human issue raised this
- Finding 6 (Flow Rates Fixed Without Literature Justification): A — mu_EI and mu_IR fixed at biologically implausible values with no justification; no human issue raised this
- Finding 7 (No Benchmark Comparison): B — no ARMA or other benchmark fit provided (matches Human Issue #5)
- Finding 8 (No Model Diagnostics): A — no conditional log-likelihood plot or ESS monitoring; no human issue raised this
- Finding 9 (Data Truncation Unexplained): C — 501 weeks truncated to 105 without explanation; no human issue raised this
- Finding 10 (rho Profile CI Implausibly Narrow): C — CI width of 0.69pp is suspiciously narrow given Monte Carlo noise; no human issue raised this
- Finding 11 (run_level = 2 with Potentially Insufficient Global Search): C — global search trace plots show non-convergence; no human issue raised this
- Finding 12 (Initial Conditions E=14 and I=7 Fixed Without Justification): D — hardcoded initial compartment counts not motivated (matches Human Issue #7)
- Finding 13 (Typo in Data Description "1996-1975"): C — typo for 1966-1975; no human issue raised this
- Finding 14 (Pairs Plot Comment Left in Draft State): C — internal draft note not removed before submission; no human issue raised this
- Finding 15 (Conclusion Overstates Model Fit): C — conclusion claims SEIR fits well without resolving open validity issues; no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |
