## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Log-likelihood comparison informal and misleading — tseries::garch uses a conditional likelihood that differs from the full likelihood, addressing the human's concern about whether the software reports the actual likelihood")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Log-likelihood comparison informal and misleading — authors acknowledge the tseries::garch incomparability at line 287 but do not adequately account for it, matching the human's concern about the confusing statement that something is wrong but used anyway")

**Findings classification:**
- Finding 1 (Duplicate stew file name invalidates New Global Search): A — duplicate stew cache key causes second global search to silently reuse first search results
- Finding 2 (Initial global search box excludes claimed superior mode): A — search box constrained to phi in [0.95,0.99] cannot discover phi ~0.5 identified as best
- Finding 3 (Heston SV code does not match stated model equation): A — code implements phi*sqrt(V) instead of phi*V, making the fitted model different from the described model
- Finding 4 (Potential FNG covariate length mismatch): A — fng_subset and merged_df may have different row counts, causing silent recycling or crash
- Finding 5 (No formal statistical inference for FG Index effect): A — no LRT, profile likelihood CI, or test of H0: gamma=0 to support the central claim
- Finding 6 (Log-likelihood comparison informal and potentially misleading): B — different response variables and tseries conditional vs particle-filter full likelihood make comparisons invalid (matches Human Issues #1 and #6)
- Finding 7 (sigma_nu converging to zero not discussed as boundary problem): A — parameter at boundary of support signals possible misspecification but is not diagnosed
- Finding 8 (Fixed df=5 for t-distribution not justified rigorously): C — experimenting with df values 3–25 without showing results or profiling is ad hoc
- Finding 9 (Contradictory claims about local vs global search sign of gamma): C — positive gamma in local search vs negative in global search signals identifiability problem not investigated
- Finding 10 (New Global Search narrative internally inconsistent): C — discussion of differences between searches is unfounded because both return the same cached results
- Finding 11 (Both simple SV global searches overwrite the same output file): C — btc_global_params.csv overwritten by t-distribution results, silently destroying normal-distribution output
- Finding 12 (Justification for differencing FG Index is incomplete): C — visual ACF inspection used instead of ADF/KPSS test; differencing shifts economic interpretation not discussed
- Finding 13 (Title typo — leading "V" missing): C — title reads "olatility analysis on Bitcoin returns"
- Finding 14 (Figure 25 mislabeled as Local Search): C — global search pairs plot labeled as local search, copy-paste error
- Finding 15 (Several typographical and grammatical issues): C — multiple spelling errors, HTML tag errors in references, acknowledged AI polishing did not fix them

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
