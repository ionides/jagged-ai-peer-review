## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "tau and amplitude parameters lack partrans declarations — tau constraint [0,60] not enforced in IF2 optimization")

**Findings classification:**
- Major #1 (global search wrong anchor — mif2(if1[[1]]) instead of base pomp object): A — global search inherits decayed cooling schedule, no genuine exploration
- Major #2 (SV vs GARCH log-likelihood comparison invalid): A — different observation models, unequal degrees of freedom, Jacobian equivalence unverified
- Major #3 (hardcoded event windows — look-ahead bias): A — event intervals and multipliers derived from visual data inspection, not estimated
- Major #4 (initial log-likelihoods computed on simulated data, not real data): A — values 410.657, 457.797, 472.035 are on model-simulated output, not actual gasoline returns
- Major #5 (no profile likelihoods for any parameter): A — leverage hypothesis rests on qualitative reading of pairs plot, no formal CI for sigma_nu
- Major #6 (no non-mechanistic benchmark comparison): A — GARCH comparison is methodologically compromised; no ARMA or AR(p)-t baseline
- Major #7 (tau and amplitude lack parameter transformation declarations): B — IF2 can push tau below zero; clamping silently distorts optimization; [0,60] constraint not properly enforced (matches Human Issue #8)
- Major #8 (AIC table uses hardcoded log-likelihoods): A — values not extracted from live R objects, table will not update on rerun
- Major #9 (inadequate diagnostics — no conditional log-likelihood plot): A — only ESS traces and pairs plots; no per-observation likelihood decomposition
- Major #10 (daily data loaded only for visualization, missing file dependency): A — daily CSV absent from submission, no daily analysis performed
- Minor (simulated log-likelihood notation mismatch — sigma_nu sign): C — code sets exp(-4.5) but text states exp(4.5)
- Minor (tau rw.sd = 1 is disproportionately large): C — 20% of starting value vs. 0.02 for other parameters, compounded by integer clamping
- Minor (write.table appending in eval=FALSE chunks — vestigial code): C — CSV accumulation never executed or read back
- Minor (GARCH AIC tie-breaking ambiguity in which.min logic): C — undefined behavior if two models tie
- Minor (STL decomposition applied to log-returns not squared returns): C — does not directly show volatility seasonality; stated conclusion unsupported
- Minor (parameter estimates not reported in any table): C — best-fit parameters inferrable only from pairs plots
- Minor (missing daily CSV file): C — document will fail to render without Daily_New_York_Harbor file

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
