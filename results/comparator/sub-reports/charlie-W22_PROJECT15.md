## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Initial conditions not fully justified — I=1 and E=0 at series start are implausible and may cause early particle filter struggles")
- Human Issue #2: covered (matched by finding: "Initial conditions not fully justified — I=1 and E=0 at series start are implausible and may cause early particle filter struggles")
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #4: missed
- Human Issue #5: covered (matched by findings: "Fixed reporting rate rho=0.1 inappropriate for sequenced GISAID data" and "rho and k both fixed without sensitivity analysis")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Large Monte Carlo standard errors — loglik.se = 5.58 for top Delta result — undermine likelihood comparisons")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Grammar and presentation issues including 'Comparsion' title typo and numerous other errors")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Fixed rho=0.1 inappropriate for GISAID sequenced data): B — matches Human Issue #5
- Finding 2 (Delta Beta profile CI [100,150] does not contain global MLE ~73): A
- Finding 3 (Global search second mif2 call does not re-specify Np, Nmif, rw.sd): A
- Finding 4 (No non-mechanistic benchmark comparison): B — matches Human Issue #3
- Finding 5 (Large MC standard errors — loglik.se = 5.58 — undermine likelihood comparisons): B — matches Human Issue #7
- Finding 6 (No profile likelihoods for mu_EI, mu_IR, or eta): A
- Finding 7 (rho and k both fixed without sensitivity analysis): B — matches Human Issue #5
- Finding 8 (Delta trace plot silently filters out non-converging runs below loglik > -2000): C
- Finding 9 (Initial conditions I=1 and E=0 not estimated or justified): D — matches Human Issues #1 and #2
- Finding 10 (Omicron global search box upper bound Beta=100 misaligned with best results at Beta>300): C
- Finding 11 (Delta Beta profile peak ~130 does not coincide with global MLE ~73): C
- Finding 12 (mu_IR = 5.46 implies ~1.3 day recovery time, biologically implausible for COVID-19): C
- Finding 13 (No conditional log-likelihood, ESS, or filtering distribution diagnostics): C
- Finding 14 (Omicron Beta profile resolution insufficient to precisely locate MLE): C
- Finding 15 (Grammar and presentation issues including title typo "Comparsion"): D — matches Human Issue #9

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
