---
name: pomp-profile-pre-global-seed-error
description: Detect cases where a POMP profile likelihood box is constructed from a CSV that contains only pre-global-search results (local search or initial pfilter), causing the profile to be seeded from a locally optimal region that is far below the global MLE in log-likelihood and producing a flat, uninformative profile curve — use when reviewing a POMP project that writes search results to a running CSV file and runs the profile search before the global search in document order.
---

# POMP Profile Pre-Global-Search Seed Error Detector

## Purpose

A common POMP workflow accumulates parameter search results in a running CSV file (`write_csv(..., append=TRUE)` or equivalent), and then constructs the profile likelihood box by reading from that CSV and filtering to high-likelihood rows. If the profile search block appears earlier in the document than the global search block, the CSV at the time the profile runs contains only the initial particle filter result and local search results — which may be far from the global optimum. The profile is then seeded from a locally optimal parameter region that bears no relation to the global MLE.

Consequences:
- The profile maximum log-likelihood is near the local optimum (e.g., approximately 40 units below the global MLE).
- Other parameters (e.g., sigma) are restricted to a narrow band near their locally optimal values, not the globally optimal values.
- The profile curve over the target parameter is essentially flat, because the target parameter is unidentified at the local optimum (e.g., phi is unidentified when sigma ≈ 0).
- The chi-squared CI cutoff applied to this flat curve encompasses the entire grid, producing an uninformative CI.

This error is distinct from:
- `pomp-profile-range-misalignment`: that skill handles the case where the profile *grid range* for the target parameter does not include the global MLE value of that parameter. The current error is about the *seed region* for the other parameters being wrong.
- `pomp-pseudo-profile-audit`: that skill handles the case where no profile IF2 search is run at all. Here, the profile IF2 search is correctly structured but seeded from the wrong region.
- `pomp-profile-guess-stratification-error`: that skill handles wrong `group_by` parameter in guess construction. Here, the issue is which *CSV file state* the guesses are drawn from, not which parameter is grouped.

## When to Activate

Use this skill when:
- A POMP project writes search results to a CSV file after each search stage (local, global, profile).
- The profile search code appears in the document *before* the global search code, so the CSV at profile-run time contains only local search results.
- The profile maximum log-likelihood is substantially lower (more negative) than the global search maximum log-likelihood (e.g., by 10 or more units).
- The profile curve is nearly flat across the entire parameter grid.

Do not use this skill when:
- The profile is seeded using `profile_design()` from a fixed parameter grid rather than from a previously-run CSV.
- The profile code appears after the global search and the CSV already contains global search results.
- The profile maximum log-likelihood is close to the global maximum (within Monte Carlo error, typically < 5 units).

## Procedure

### 1. Identify the CSV accumulation pattern

Search the Rmd/R source for blocks that:
- Call `pfilter()` or `mif2()` and then `write_csv()` to a named CSV file.
- Later call `read_csv()` from the same file to construct the profile box.

Note the document order of these blocks: local search block → CSV write → profile block → CSV write → global search block.

### 2. Determine the CSV state at the time the profile is run

Based on document order, identify which search results are in the CSV when the profile box construction code (`read_csv(csv_name) |> filter(loglik > max(loglik) - K)`) runs:
- If only the initial pfilter and local search results are present, the box will be constrained to the locally optimal parameter region.
- If the global search results are also present (because the global search precedes the profile in document order), the box is drawn from a broader, globally-informed set.

### 3. Compare profile maximum to global maximum log-likelihood

Load the saved profile and global search artifacts. Compare:
```r
max(profile_results$loglik, na.rm = TRUE)  # profile max
max(global_results$loglik, na.rm = TRUE)   # global max
```
If the profile maximum is more than ~5 log-likelihood units below the global maximum, flag the discrepancy. A gap of ≥10 units indicates the profile never explored the globally optimal region.

### 4. Examine the profile box for the non-profiled parameters

Check the range of non-profiled parameters (e.g., sigma, mu) in the profile results:
- If sigma spans [0.003, 0.010] in the profile but the global MLE has sigma = 0.574, the profile was restricted to a narrow band near the local optimum.
- Compare against the global MLE values: `result[which.max(global_results$loglik), ]`.

### 5. Assess the CI validity

Compute the CI cutoff as applied in the code (`max(profile_loglik) - 0.5 * qchisq(df=1, p=0.95)`). Determine how many profile grid points fall above this cutoff. If nearly all grid points are above the cutoff, the profile is flat and the CI is uninformative — spanning essentially the entire grid range.

Also verify: the correct CI cutoff should use the *global* maximum log-likelihood, not the profile maximum. If the profile maximum is below the global maximum, using the profile maximum as the reference underestimates the cutoff and inflates the apparent CI.

### 6. Report the finding

For each detected instance, report:
- The code location (chunk name and approximate line) of the CSV read that constructs the profile box.
- The document-order relationship between the profile block and the global search block.
- The discrepancy between the profile maximum (local optimum) and the global maximum.
- The range of non-profiled parameters in the profile versus at the global MLE.
- The consequence: the profile curve is flat, the CI encompasses the entire grid, and the reported confidence interval is invalid.
- The fix: move the profile block to appear after the global search block in the document (so the CSV contains global search results at box-construction time), or seed the profile using `profile_design()` independently of the CSV state.

## Limitations

- This error requires reading both the source code (to determine document order) and the saved artifacts (to compare log-likelihood values). It cannot be detected from the rendered HTML output alone.
- If the local and global search results happen to be in the same region (e.g., the local search found the global optimum), this error has no practical impact. The check in Step 3 will correctly indicate no discrepancy.
- Does not replace the other profile failure mode checks (`pomp-profile-range-misalignment`, `pomp-pseudo-profile-audit`, `pomp-profile-rw-sd-drift-error`, `pomp-profile-indexing-error`, `pomp-profile-guess-stratification-error`); all applicable checks should be run when reviewing a POMP profile likelihood.
