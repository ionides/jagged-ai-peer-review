## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by findings: "No Likelihood-Based Inference Performed" and "Visual-Only Goodness-of-Fit Assessment")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major 1 (No Likelihood-Based Inference Performed): B — particle filter produced degenerate likelihoods, POMP analysis could not achieve its primary goal (matches Human Issue #7)
- Major 2 (Binomial Measurement Model Causes Degenerate Likelihood): A — specific technical root cause of degenerate particle filter not raised by humans
- Major 3 (Visual-Only Goodness-of-Fit Assessment): B — all models assessed purely by visual comparison with no quantitative fit statistics (matches Human Issue #7)
- Major 4 (Vaccination Subtraction Can Drive S Below Zero): A — critical structural bug allowing negative susceptible counts not raised by humans
- Major 5 (Model 3 Vaccination Rate Draws From Wrong Compartment): A — equation–code discrepancy using I instead of S as base for vaccination not raised by humans
- Major 6 (No Benchmark Comparison for POMP Model): A — no ARMA or other non-mechanistic benchmark compared against POMP models not raised by humans
- Major 7 (LRT Applied to Mismatched Models with Wrong Degrees of Freedom): A — invalid LRT comparing models on different outcomes with incorrect df not raised by humans
- Major 8 (No Parameter Identifiability Assessment): A — no profile likelihoods or confidence intervals computed not raised by humans
- Major 9 (POMP Applied to Rolling-Mean Data, Misspecified Measurement Model): A — rolling mean creates autocorrelated non-integer observations incompatible with binomial model not raised by humans
- Major 10 (index State Variable / Linear Vaccination Term Unbounded): A — hardcoded slope and unbounded linear vaccination term precludes optimization not raised by humans
- Minor: Data loading from external URLs: C — reproducibility dependent on external URL stability not raised by humans
- Minor: mu_IR not declared in partrans: C — missing log transform for mu_IR in parameter transformation not raised by humans
- Minor: Section 2.1 and Introduction duplicated: C — verbatim repetition of data description not raised by humans
- Minor: N population values inconsistent across models: C — small discrepancies in N across Models 1–3 not raised by humans
- Minor: No random seeds for reproducibility: C — stochastic computations not seeded for reproducibility not raised by humans
- Minor: Susceptible population formula double-counts recoveries: C — EDA formula may double-subtract deaths through cases column not raised by humans
- Minor: No convergence traces or ESS diagnostics: C — particle filter diagnostic plots not included in rendered document not raised by humans
- Minor: References use raw URLs rather than formal citations: C — bibliographic entries are bare URLs not raised by humans

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
