## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SIRV Model 1 — two code errors inconsistent with stated equations")
- Human Issue #3: covered (matched by finding: "SIRV2 selected for final analysis despite SIRV1 having substantially higher log-likelihood")
- Human Issue #4: covered (matched by finding: "SIRV2 selected for final analysis despite SIRV1 having substantially higher log-likelihood")
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- Finding 1 (Major — H accumulator): A — Accumulator H tallies recoveries (dN_IR) rather than new infections (dN_SI) across all three models
- Finding 2 (Major — SIRV1 code errors): B — SIRV Model 1 two code errors inconsistent with stated equations: dN_VI uses V instead of I; dN_SV scales as S²/N rather than S/N (matches Human Issue #2)
- Finding 3 (Major — forecast uses wrong params): A — Final forecast simulation uses hand-tuned initial parameters rather than MLE stored in params_maxlik
- Finding 4 (Major — SIRV2 selected over SIRV1): B — SIRV2 selected for final analysis despite SIRV1 having ~8.75 log-likelihood units higher fit; no formal model selection criterion applied (matches Human Issues #3 and #4)
- Finding 5 (Major — overstated efficacy): A — Overstated vaccine efficacy conclusion given profile likelihood CI spanning nearly the entire (0,1) range for Sigma
- Finding 6 (Major — no benchmark): A — No non-mechanistic benchmark model fit for comparison
- Finding 7 (Major — CI cutoff omitted): A — CI cutoff line commented out of profile likelihood plot, making confidence interval endpoints unreadable
- Finding 8 (Minor — single pfilter): C — Local search log-likelihood re-evaluation uses single pfilter call without replication, producing unquantified Monte Carlo noise
- Finding 9 (Minor — no profiles for other params): C — Profile likelihoods computed only for Sigma; Beta, mu_IR, and rho identifiability never formally assessed
- Finding 10 (Minor — binomial, no overdispersion): C — Binomial measurement model used; COVID-19 case counts exhibit overdispersion warranting negative binomial
- Finding 11 (Minor — no process stochasticity): C — No environmental/process stochasticity beyond demographic noise; no multiplicative noise on transmission rates
- Finding 12 (Minor — no population bound on vaccination): C — Quadratic vaccination model extrapolation has no explicit population cap, creating potential edge cases
- Finding 13 (Minor — run level inconsistency): C — Rmd header sets run_level=1 but analysis loads cached results from run_level=2, making the code non-reproducible as submitted
- Finding 14 (Minor — no model comparison table): C — No table summarizing log-likelihoods or AIC for SIR, SIRV1, and SIRV2; comparison done informally in prose
- Finding 15 (Minor — forecast not from filtering distribution): C — Prediction simulates from t0=0 rather than conditioning on the filtering distribution at the end of the training period

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |
