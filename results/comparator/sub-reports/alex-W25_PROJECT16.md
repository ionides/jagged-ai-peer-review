## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by findings: "SEIR model failure treated as finding rather than investigated" and "Local MIF2 convergence claimed but ESS and other convergence diagnostics not reported")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (Log-likelihood comparison ARCH vs SEIR invalid): A — different observation spaces make likelihood values non-commensurable; human did not raise this
- Finding 2 (Missing data interpolation undescribed, no sensitivity analysis): A — over two years of missing data handled opaquely; human did not raise this
- Finding 3 (SEIR model failure not diagnosed, pairs plot commented out): B — failure treated as finding rather than investigated, no root-cause analysis (matches Human Issue #4)
- Finding 4 (k overdispersion parameter fixed without justification): A — observation-model k fixed at arbitrary values, no profile; human did not raise this
- Finding 5 (H accumulator tracks recoveries N_IR instead of infections): A — biological measurement model error causing phase shift; human did not raise this
- Finding 6 (ADF test cited in bibliography but never performed): A — stationarity test absent despite citation; human did not raise this
- Finding 7 (ARCH vs ARMA comparison uses mismatched sample sizes): A — different effective n in log-likelihood table; human did not raise this
- Finding 8 (SIR global search bounds implausibly wide, mu_IR unidentifiable): C — biologically implausible upper bound, no profile; human did not raise this
- Finding 9 (MIF2 convergence claimed but ESS and diagnostics absent): D — no quantitative convergence criterion, no ESS from final filter (matches Human Issue #4)
- Finding 10 (rw.sd ifelse misuse applies wrong perturbations to beta): C — MIF2 API misuse in perturbation schedule; human did not raise this
- Finding 11 (Vaccination data from Michigan extrapolated to four other states): C — no validation of representativeness; human did not raise this
- Finding 12 (SEIR initializes accumulator H=1 instead of H=0): C — biases measurement likelihood for first observation; human did not raise this
- Finding 13 (Deaths plot y-axis mislabeled "Births"): C — copy-paste labeling error; human did not raise this
- Finding 14 (Pairs plot for full SEIR global search commented out): C — parameter identifiability cannot be assessed; human did not raise this
- Finding 15 (Citation URL for project2024-2 points to 2020 page): C — minor citation error; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
