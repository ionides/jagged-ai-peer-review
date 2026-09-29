## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "loglik.se filter threshold of 10 too permissive; several runs show substantial particle-filter instability")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (NewEI accumulates wrong compartment): A — code bug causes systematic undercount of weekly incidence; not raised by human
- Finding 2 (emeas uses monotonically growing H): A — inconsistency between emeas and dmeas/rmeas; not raised by human
- Finding 3 (SEIRS mislabeled as SEIR throughout): A — waning immunity term present in code but not acknowledged; not raised by human
- Finding 4 (population N = 2267000 incorrect for national model): A — underestimated N inflates transmission estimates; not raised by human
- Finding 5 (amp unconstrained in local mif2 call): A — constraint omitted from partrans, amp > 1 in results; not raised by human
- Finding 6 (written equations include terms absent from code): A — birth, death, importation terms documented but not implemented; not raised by human
- Finding 7 (profile likelihood is a marginal scatter plot): A — wrong method and wrong chi-square threshold used; not raised by human
- Finding 8 (cross-model comparison information asymmetry): A — NBEATS uses county-level features, ARMA/POMP use national aggregate; not raised by human
- Finding 9 (VMD fit on full dataset including validation period): A — data leakage inflates NBEATS MAPE; not raised by human
- Finding 10 (ARMA ignores 52-week seasonality): C — no SARIMA considered; not raised by human
- Finding 11 (ARMA MAPE evaluated in-sample only): C — in-sample vs. validation MAPE comparison inconsistency; not raised by human
- Finding 12 (loglik.se < 10 filter too permissive): D — retained runs with high SE indicate particle-filter instability (matches Human Issue #7)
- Finding 13 (start_params undefined in local search code): C — implicit parameter source, reproducibility concern; not raised by human
- Finding 14 (duplicate library(pomp) call): C — cosmetic error, not raised by human
- Finding 15 (Beta range 83–748 implausibly wide, unexplained): C — likely artifact of confounded N and unconstrained amp; not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 10 |
| F (Human-AI contradiction) | 0 |
