## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by findings: "mu_h lies outside search box — convergence not achieved" and "no MIF2 convergence diagnostics (trace plots) are shown")

**Findings classification:**
- Finding 1 (mu_h outside search box): B — MIF2 convergence failure identified through parameter estimates lying outside the search region (matches Human Issue #7)
- Finding 2 (no MIF2 trace plots): B — no convergence diagnostic plots shown for iterated filtering (matches Human Issue #7)
- Finding 3 (no pf1 likelihood reported): A — likelihood evaluation for simulated data never displayed, making simulation study uninformative
- Finding 4 (global search inherits cooled if1[[1]]): A — global search uses a locally-warmed MIF2 chain, defeating the purpose of global search
- Finding 5 (inconsistent dmrt vs dmean_z): A — two distinct demeaned return series used across model sections without explanation
- Finding 6 (frequency=365 on trading-day data): A — ts object constructed with incorrect annual frequency for trading-day data
- Finding 7 (phi=0.95 in text vs phi=0.995 in code): A — discrepancy between stated initial parameters in text and actual code values
- Finding 8 (no parameter interpretation): C — estimated POMP parameters reported but never interpreted in financial terms
- Finding 9 (AIC comparison potentially non-comparable): C — ARMA, GARCH, and POMP likelihoods may not be evaluated on the same conditional density
- Finding 10 (no likelihood profile or CIs): C — only a single point estimate reported; no profile likelihood or confidence intervals for any POMP parameter
- Finding 11 (simulation subsection adds little value): C — filtering on simulated data never shows L.pf1 and performs no re-estimation
- Finding 12 (ARMA model selection inconsistency): C — ARMA(3,1) chosen despite a ~34-unit AIC gap from ARMA(4,5), without showing MA root values numerically
- Finding 13 (Nasdaq-500 misnomer): C — index repeatedly and incorrectly called "Nasdaq-500" in conclusion and references
- Finding 14 (hard-coded unexplained date in data cleaning): C — strftime date 2016-11-04 used in ts construction differs from actual data start with no explanation
- Finding 15 (incomplete Breto citation): C — model attributed to "Breto (2014)" but reference [2] points to course lecture notes, not the original journal paper

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
