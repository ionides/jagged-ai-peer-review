## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by findings: "home_court_avd is on inconsistent scales in dmeas vs. rmeas" and "Away-game case is handled asymmetrically between dmeas and rmeas")
- Human Issue #2: covered (matched by findings: "Model comparison uses in-sample prediction accuracy, not log-likelihood" and "No likelihood-based benchmark comparison")
- Human Issue #3: covered (matched by findings: "No simulation from the filtering distribution" and "Convergence diagnostics are shown but not interpreted")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (home_court_avd inconsistent scales in dmeas vs. rmeas): B — scale inconsistency between dmeas and rmeas is a distinct manifestation of the same underlying dmeas/rmeas inconsistency concern (matches Human Issue #1)
- Finding 2 (away-game handled asymmetrically between dmeas and rmeas): B — directly identifies that dmeas does not subtract home advantage for away games, matching Human Issue #1 precisely
- Finding 3 (Model 3 accuracy evaluation silently uses Model 1): A — coding bug causing Model 3 to be evaluated using Model 1 parameters; not raised by human
- Finding 4 (attendance has no effect on likelihood in Model 3): A — dmeas_att never defined so attendance enters rmeas but not the likelihood; not raised by human
- Finding 5 (latent ELO update uses simulated win, not observed Win): A — structural design flaw in rproc causing particle degeneracy; not raised by human
- Finding 6 (no profile likelihoods computed): A — concerns parameter identifiability and confidence intervals; distinct from Human Issue #2's model-comparison concern
- Finding 7 (model comparison uses in-sample prediction accuracy, not log-likelihood): B — directly matches Human Issue #2's call for likelihood-based (AIC/LRT) rather than predictive-score comparisons (matches Human Issue #2)
- Finding 8 (prediction accuracy computed in-sample): A — out-of-sample evaluation concern not raised by human
- Finding 9 (hard-coded absolute local file paths): A — reproducibility failure; not raised by human
- Finding 10 (no likelihood-based benchmark comparison): B — matches Human Issue #2's underlying concern that likelihoods should be used to assess model improvement rather than prediction accuracy alone (matches Human Issue #2)
- Finding 11 (sigma fixed without justification): C — parameter fixing without sensitivity analysis; not raised by human
- Finding 12 (global search parameter space excludes the MLE): C — search box misconfiguration; not raised by human
- Finding 13 (no simulation from filtering distribution): D — filtering simulations are a model diagnostic tool; matches Human Issue #3's concern about light diagnostic investigation (matches Human Issue #3)
- Finding 14 (p_win stored as redundant state variable): C — design inefficiency; not raised by human
- Finding 15 (convergence diagnostics shown but not interpreted): D — failure to interpret diagnostic output matches Human Issue #3's concern about inadequate diagnostic investigation (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
