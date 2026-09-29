## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Profile Likelihood for Beta is a Likelihood Slice, Not a Profile — CI spans entire search box, no inferential content")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Profile Likelihood for Beta is a Likelihood Slice, Not a Profile — CI artifact of search box"; also matched by finding: "Conclusion That Guinea and Sierra Leone Have 'Same Transmission Rate' is Unsupported")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "No Non-Mechanistic Benchmark Comparison")

**Findings classification:**
- Finding 1 (Measurement Model H Misspecification): A — severe misspecification of binomial dmeas/rmeas applied to accumulator H
- Finding 2 (Profile Likelihood is a Likelihood Slice): B — profile is a scatter plot over random Beta values, CI spans entire search box (matches Human Issues #1 and #3)
- Finding 3 (F_size in partrans): A — F_size is fixed yet included in log() parameter transformation without justification
- Finding 4 (No Benchmark Comparison): B — no ARMA or non-mechanistic benchmark likelihood reported (matches Human Issue #8)
- Finding 5 (Biologically Implausible Estimates): A — mu_EI ≈ 14.9 day^-1 implies ~96-minute incubation period, not flagged
- Finding 6 (No Overdispersion): A — binomial measurement model used without justification; negative binomial preferred
- Finding 7 (rw.sd Too Small): A — rw.sd = 0.002 is 10x smaller than course standard, limiting optimizer exploration
- Finding 8 (No Quantitative GoF in Text): A — log-likelihood values computed but never reported in paper body
- Finding 9 (Initial Conditions Implausible): A — I₀ fixed at 482 (Guinea) and 935 (Sierra Leone) without justification
- Finding 10 (Sierra Leone Population Misspecified): A — N ≈ 6.19 million used instead of actual 2014 value ~7.1 million
- Finding 11 (Conclusion of Same Transmission Rate Unsupported): B — identical CI bounds are artifact of search box design, not data inference (matches Human Issue #3)
- Finding 12 (Funeral Compartment F Assigned Not Accumulated): A — F set equal to instantaneous new funerals per step rather than accumulated
- Finding 13 (No Model Diagnostics): A — no conditional log-likelihood plots, ESS traces, or residual checks
- Finding 14 (Global Search Results Duplicated): A — bind_rows(results, results) bug inflates apparent search size
- Finding 15 (No R0 Discussion): A — no reproduction number computed despite motivating SEIRDF model by R0 concerns

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 12 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
