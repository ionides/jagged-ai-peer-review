## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Binomial measurement model causes structural particle filter collapse — bounded support causes -Inf likelihoods, the same symptom the human attributes to insufficient measurement noise")
- Human Issue #2: covered (matched by finding: "Binomial measurement model causes structural particle filter collapse — directly identifies bounded support and absence of overdispersion as the structural problem")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- Finding 1 (Accumulator H tracks recoveries not infections): A — fundamental measurement model mismatch, accumulator bug not identified by human
- Finding 2 (Third model displays wrong likelihood — SIR1 value shown for SIR2): A — copy-paste display error not identified by human
- Finding 3 (Binomial measurement model causes structural particle filter collapse): B — matches Human Issues #1 and #2
- Finding 4 (No global search — convergence conclusions premature): A — missing global search not identified by human
- Finding 5 (Hardcoded 0.7 contact-rate reduction factor not estimated): A — fixed reduction factor not identified by human
- Finding 6 (No non-mechanistic benchmark comparison): A — missing ARIMA baseline not identified by human
- Finding 7 (No profile likelihoods or confidence intervals): A — missing profiles not identified by human
- Finding 8 (Large log-likelihood standard errors indicate particle filter degeneracy): A — large pfilter SEs not identified by human
- Finding 9 (Log-likelihood direction inverted in SEIR conclusion): C — "lowest loglikelihood" phrasing error not identified by human
- Finding 10 (SEIR pomp object inherits incomplete partrans from fluSIR): C — partrans inheritance bug not identified by human
- Finding 11 (Population N fixed without biological justification): C — N justification issue not identified by human
- Finding 12 (Week-22 COVID-19 breakpoint chosen by inspection): C — breakpoint justification not identified by human
- Finding 13 (No model diagnostics beyond visual simulation overlay): C — missing diagnostics not identified by human
- Finding 14 (Only 50 IF2 iterations with Np=2000 — computational effort not assessed): C — computational adequacy issue not identified by human
- Finding 15 (Research question mismatches analysis performed): C — research question mismatch not identified by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
