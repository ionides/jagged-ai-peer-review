## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Negative Binomial Parameterization Is Epidemiologically Non-Standard — near-degenerate behavior when H≈0 creates hard numerical boundaries distorting the likelihood surface, matching the 'likelihood cliff' and stochasticity concern")
- Human Issue #3: covered (matched by finding: "Negative Binomial Parameterization Is Epidemiologically Non-Standard — code uses dnbinom with non-standard parameterization, the same measurement-model specification problem the human identifies as text/code discrepancy")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (Global search initialized from mif2 result, not base POMP object): A — major finding about initialization bug in global IF2 search; human does not raise it
- Finding 2 (Negative Binomial Parameterization Is Epidemiologically Non-Standard and Misleading): B — major finding about non-standard NegBin parameterization creating near-degenerate likelihood and non-interpretable rho (matches Human Issues #2 and #3)
- Finding 3 (No Benchmark Comparison Against Non-Mechanistic Model): A — major finding about absent baseline comparison; human does not raise it
- Finding 4 (No Model Diagnostics): A — major finding about absent diagnostic plots and ESS traces; human does not raise it
- Finding 5 (Fixed Initial Conditions Are Unjustified and Potentially Influential): A — major finding about hard-coded E(0) and I(0); human does not raise it
- Finding 6 (Profile Likelihood Seeds from Local-Search Box, Limiting Validity): A — major finding about profile being anchored to local optimum; human does not raise it
- Finding 7 (Accumulator Variable Records Recoveries, Not New Infections): C — minor finding about dN_IR vs dN_EI accumulator semantics; human does not raise it
- Finding 8 (mu_EI and mu_IR Fixed at Values That Deserve Justification): C — minor finding about unjustified fixed rate parameters; human does not raise it
- Finding 9 (Profile CI Extraction Uses Raw rho Without Enforcing Profile Maximum = Global Maximum): C — minor finding about CI cutoff referencing profile max rather than global max; human does not raise it
- Finding 10 (Computational Intensity Set to run_level = 2, Below Production Quality): C — minor finding about unconverged chains at run_level 2; human does not raise it
- Finding 11 (Global Search Box for rho Extends to 0.9 But Profile Only Covers 0.01–0.50): C — minor finding about profile grid misalignment with search box; human does not raise it
- Finding 12 (Conclusion Claims Seasonal Pattern Is Captured Without Quantitative Support): C — minor finding about unquantified seasonality claim; human does not raise it
- Finding 13 (No Assessment of R_0 or Other Epidemiologically Interpretable Quantities): C — minor finding about absent R_0 derivation; human does not raise it
- Finding 14 (Pairwise Plots for Local Search Are Based on Only 10 Points): C — minor finding about sparse pairwise scatter plot; human does not raise it
- Finding 15 (Paper Uses Single Forward Simulations for Fit Assessment): C — minor finding about nsim=1 providing weak fit evidence; human does not raise it

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |
