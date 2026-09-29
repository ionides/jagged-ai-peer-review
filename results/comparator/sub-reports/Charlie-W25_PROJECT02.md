## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Conclusion contradicts the sensitivity analysis — NB model fails to reject null while Poisson model does, yet paper asserts momentum is a material factor")
- Human Issue #2: covered (matched by finding: "No non-mechanistic benchmark")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Mathematical error in the transition density equation — x_n absent from exponent")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major Issue 1 (Mathematical error in transition density equation): B — x_n missing from exponent in Equation (1) (matches Human Issue #5)
- Major Issue 2 (LRT boundary violation): A — sigma=0 lies on boundary of parameter space, chi-squared approximation invalid
- Major Issue 3 (Duplicate vector in MLL computation): A — results_glob concatenated with itself instead of combining local and global search results
- Major Issue 4 (Conclusion contradicts sensitivity analysis): B — NB sensitivity analysis fails to reject null but Discussion asserts momentum is material (matches Human Issue #1)
- Major Issue 5 (Insufficient global search effort): A — only 5 starting points used (explore mode) on acknowledged complex likelihood surface
- Major Issue 6 (Look-ahead bias in covariate Z_n): A — full-season opponent ERA used as time-n covariate, including future games
- Minor: Profile likelihood omitted from main report: C — formal profile for phi computed in code but not shown in report
- Minor: No confidence intervals stated in text: C — only point estimates reported despite identifiability concerns
- Minor: No non-mechanistic benchmark: D — no ARIMA or IID comparison (matches Human Issue #2)
- Minor: phi to -1 finding not investigated: C — convergence to phi near -1 noted but not interpreted or checked for stability
- Minor: X_0=0 initial condition not sensitivity-tested: C — momentum fixed at zero at season start without sensitivity analysis
- Minor: Pairwise scatterplot mislabeling: C — figure labeled as local search results but code references global search output
- Minor: nrow(opp_pitch_games > 0) non-idiomatic: C — comparison operator applied inside nrow() rather than outside
- Minor: Comment error in blinded.Rmd: C — comment says "log(mu) represents expected runs" but mu is already the log-expected runs

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
