## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding #2 "Global MLE reveals AR(1) captures overdispersion not momentum"; note: finding #3 contradicts human's interpretation that NB analysis shows NB is less necessary)
- Human Issue #2: covered (matched by finding #1 "Absence of non-mechanistic benchmark")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding #4 "Mathematical error in AR(1) transition density")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (Absence of non-mechanistic benchmark): B — no non-mechanistic baseline compared against (matches Human Issue #2)
- Finding 2 (Global MLE reveals overdispersion not momentum): B — phi≈-0.012, large sigma indicate latent AR(1) absorbs overdispersion; NB sensitivity confirms this (matches Human Issue #1)
- Finding 3 (Primary conclusion contradicted by NB sensitivity): F — Doug says Poisson conclusion is an artifact and framing should be reversed; human says NB was found to be less necessary and the investigation is appropriately open-minded (contradicts Human Issue #1)
- Finding 4 (Mathematical error in AR(1) transition density): B — exponent written as -(φx_{n-1})² / 2σ² instead of -(x_n − φx_{n-1})² / 2σ² (matches Human Issue #5)
- Finding 5 (Profile likelihood seeded from wrong region): A — profile box restricted to sigma ∈ [0.003, 0.010], ~40 log-likelihood units below global MLE, rendering profile uninformative
- Finding 6 (Global search initialization anti-pattern): A — global replicates inherit cooled mif2 schedule from prior result object instead of fresh base pomp object
- Finding 7 (LRT at boundary of parameter space): A — sigma=0 is on boundary; Wilks' theorem requires interior null; chi-squared(2) approximation is not exact
- Finding 8 (No parameter estimates in main text): C — MLE values (phi, sigma, gamma, mu) never reported; readers cannot assess scientific plausibility
- Finding 9 (Computational details absent): C — particle count, IF2 iterations, and global replicate count not stated in main text
- Finding 10 (Covariate uses future data): C — opponent-strength covariate Z_n uses full 2024 season including post-game-n data; leakage not quantified
- Finding 11 (Coding bug in data processing): C — misplaced parenthesis in nrow() condition produces accidentally correct but fragile result
- Finding 12 (Redundant concatenation in MLL calculation): C — same vector concatenated with itself instead of combining local and global search results
- Finding 13 (Parameter transformation inconsistency between files): C — blinded.Rmd includes mu in log transform; Full_Code.Rmd standalone partrans excludes mu
- Finding 14 (Local search phi convergence not reconciled): C — local search finds phi≈-1, global finds phi≈-0.012; mechanistic explanation absent
- Finding 15 (Pairwise scatter mislabeled as local search): C — figure in Local Search section uses global search results (results_glob) not local search results

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 1 |
