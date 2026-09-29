## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Very large Monte Carlo SEs / filtering failures confirm severe model misspecification / particle collapse")
- Human Issue #7: covered (matched by finding: "Very large Monte Carlo SEs / filtering failures confirm severe model misspecification / particle collapse")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (measurement model bug — H accumulates dN_IR instead of dN_EI): A — fundamental structural error in measurement model; human did not raise this specific bug
- Finding 2 (rho and eta fixed without estimation): A — reporting rate and susceptibility fraction fixed without likelihood-based justification; human did not raise this
- Finding 3 (no profile likelihoods): A — no profile likelihood computed for any parameter; human did not raise this
- Finding 4 (global search insufficient computational effort): A — Nmif=50, particle degeneracy, SE >> 1; human did not raise this
- Finding 5 (no non-mechanistic benchmark): A — POMP likelihood never compared to ARMA or other baseline; human did not raise this
- Finding 6 (very large Monte Carlo SEs in reported likelihoods): B — particle collapse and filtering failures confirming severe misspecification (matches Human Issues #6 and #7)
- Finding 7 (H initialized to N*(1-eta) instead of zero): A — initialization inconsistency; human did not raise this
- Finding 8 (ARMA model selection text contradicts code — arima11 printed instead of arima22): A — text-code inconsistency in ARMA selection; human did not raise this
- Finding 9 (rw.sd magnitudes too small for logit-transformed parameters): C — minor; human did not raise this
- Finding 10 (HP filter lambda=100 inappropriate for daily data): C — minor; human did not raise this
- Finding 11 (convergence diagnosis focuses on parameter spread rather than loglik stability): C — minor; human did not raise this
- Finding 12 (global search description appears before the code that runs it): C — minor reproducibility presentation issue; human did not raise this
- Finding 13 (partrans block omits rho and eta from logit transformation): C — minor; human did not raise this
- Finding 14 (data loaded from remote GitHub URL): C — minor reproducibility dependency; human did not raise this
- Finding 15 (no simulation-based diagnostics comparing filtered vs. forward simulations): C — minor; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
