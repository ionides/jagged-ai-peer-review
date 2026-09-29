## Alex

**Coverage record:**
- Human Issue #1: covered (matched by findings: "Computational settings too low and acknowledged but not improved" and "Profile uses nprof=2 profiles per phi value, too sparse")
- Human Issue #2: missed
- Human Issue #3: covered (matched by findings: "Profile likelihood section contains incomplete statement and rendering error — 'unstable' claim is wrong"; "Global search box for phi constrained to [0.9950, 0.9999], precluding discovery of other optima, while profile finds higher likelihoods"; "Profile inconsistency with global search constraints — profile explores wider phi range than box search")

**Findings classification:**
- Finding 1 (profile rendering error / "unstable" claim): B — profile likelihood section has missing phi value and erroneous "unstable" claim (matches Human Issue #3)
- Finding 2 (POMP fitted to simulated data only): A — particle filter evaluated on simulated dataset, not observed returns; not raised by human
- Finding 3 (POMP vs GARCH log-likelihood not comparable): A — likelihoods on different footing but comparison made anyway; not raised by human
- Finding 4 (global search phi constrained to [0.9950, 0.9999]): B — tight constraint prevents finding true MLE; profile finds higher likelihood than global search (matches Human Issue #3)
- Finding 5 (profile inconsistency with global search constraints): B — profile explores much wider phi range than global search box; paper does not reconcile (matches Human Issue #3)
- Finding 6 (demeaning not justified): A — pre-demeaning interacts with POMP mean structure but is unmotivated; not raised by human
- Finding 7 (computational settings too low, acknowledged but not improved): B — Np=2000, Nmif=50 insufficient for reliable convergence (matches Human Issue #1)
- Finding 8 (ACF used to claim independence incorrectly): C — absence of linear ACF does not imply independence; not raised by human
- Finding 9 (GARCH equation omits alpha0): C — written fitted model drops intercept; not raised by human
- Finding 10 (demeaned return plot no x-axis date labels): C — plotted against integer index instead of calendar time; not raised by human
- Finding 11 (log-price plot double log transformation): C — log("y") applied to already log-transformed values; not raised by human
- Finding 12 (profile uses nprof=2, too sparse): D — only 2 restarts per phi grid point; insufficient computational effort for reliable profile envelope (matches Human Issue #1)
- Finding 13 (no simulation study or posterior predictive check): C — simulator built but never used for model checking; not raised by human
- Finding 14 (conclusion claims positive volatility shift, unsupported): C — GARCH parameters imply mean-reversion, not positive drift; not raised by human
- Finding 15 (references misattribute student projects to Ionides): C — citation error; not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |
