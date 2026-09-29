---
name: pomp-closed-environment-reproducibility-audit
description: Assess the reproducibility status and evidentiary strength of a POMP project that was executed inside an inaccessible environment (corporate VDI, secure enclave, or proprietary data agreement), where no data, rendered HTML, or intermediate artifacts can be independently verified — use when a project's data availability statement reports that raw files cannot be exported and results were captured as screenshots.
---

# POMP Closed-Environment Reproducibility Audit

## Purpose

Some student and practitioner POMP projects are executed on proprietary data within secure environments (e.g., a corporate virtual desktop infrastructure) where data cannot be exported and the analysis environment is closed to external access. The submitted document may consist entirely of screenshots of console output, trace plots, and results tables captured from the secure environment.

This creates a reproducibility failure that is qualitatively different from the failures covered by other skills:
- The `pomp-artifact-audit` skill requires loadable RDS/RDA files — these are unavailable.
- The `code-supplement-checklist-pomp.md` assumes code and data are at least structurally present — here neither is accessible.
- The rendered HTML itself is a screenshot, not a live-rendered document.

A reviewer encountering this pattern must distinguish between (a) claims that can be evaluated from the code and screenshots alone, (b) claims that are unverifiable but plausible, and (c) claims that require external data access. The audit should flag all three categories explicitly.

## When to Activate

Use this skill when:
- A project's data availability statement explicitly states that the data is owned by a third party and cannot be exported or shared.
- The HTML or PDF submitted contains screenshots of R console output, plot windows, or markdown-rendered figures rather than live-rendered output.
- The project folder contains no data files, no intermediate RDS/RDA files, and no rendered HTML — only a source Rmd and a screenshot-based PDF.

Do not use this skill when:
- The data is publicly available and the project is reproducible from the submitted files.
- The project shares a synthetic or anonymized pseudo-dataset that allows partial reproduction.
- The inaccessibility is due to missing files in the supplement (covered by `code-supplement-checklist-pomp.md`) rather than a contractual barrier on the underlying data.

## Procedure

### 1. Identify the reproducibility barrier

Read the data availability statement and any VDI/secure-environment notes. Confirm:
- Is data export prohibited by a third-party agreement?
- Was the analysis run in a closed environment with no outbound data transfer?
- Is the submitted document a static capture (PDF with screenshots) rather than a live-rendered HTML?

Document the specific constraint (e.g., "Apple VDI; no download or export permitted; HTML output captured as console screenshots").

### 2. Catalog what IS evaluable from the submission

Despite inaccessibility, the following can still be reviewed from the code and screenshots:

- **Model specification**: Are the process model, measurement model, and Csnippets consistent with the stated equations? This can be checked by reading the source code.
- **Inference procedure**: Are appropriate methods (mif2, pfilter) used? Are rw.sd values, Np, and Nmif reported in the code?
- **Convergence diagnostics**: Are trace plot screenshots legible enough to assess convergence? Do traces show the expected cooling pattern?
- **Benchmark specification**: Is the ARIMA or regression benchmark correctly specified in the code?
- **Statistical logic**: Are the comparison methods (e.g., log-likelihood comparison) valid as written, independent of the data?

### 3. Catalog what CANNOT be verified

Flag explicitly:
- **Log-likelihood values**: reported values cannot be reproduced; Monte Carlo variability cannot be assessed.
- **Convergence claims**: only a single run of each search is visible; multi-run consistency cannot be checked.
- **Parameter estimates**: cannot be verified against the data; biological plausibility checks (POMP checklist §11) are the only available sanity check.
- **Simulation trajectories**: whether simulations match data cannot be assessed without data access.
- **Goodness-of-fit**: quantitative fit measures cannot be independently validated.

### 4. Evaluate whether a pseudo-dataset is provided

Check whether the author provided a synthetic or anonymized substitute dataset that preserves the key statistical properties of the original (e.g., correct time span, similar variance structure, same covariate relationships). If yes, assess whether the pseudo-data allows meaningful reproduction of the main analysis steps. If no pseudo-data is provided, flag this as a major reproducibility failure per POMP checklist §10.

### 5. Assess the strength of the scientific claims given the limitations

For each major conclusion in the paper, assess:
- Can the claim be evaluated from the code logic alone (e.g., "the model is correctly specified as a linear-Gaussian POMP")?
- Does the claim depend on unverifiable numerical results (e.g., "the noise coefficient b = -0.30 is significant")?
- Is the claim plausible given parameter values visible in screenshots?

Conclusions that depend entirely on unverifiable numerical results should be flagged as "cannot be evaluated" rather than "wrong" — the reviewer cannot confirm or deny them.

### 6. Propose minimum remediation

Recommend one of the following, in order of preference:
1. **Synthetic pseudo-data**: Generate a dataset from the fitted model (using the reported parameter estimates) that mimics the statistical structure of the original. This allows reproduction of all inference steps.
2. **Archived parameter tables**: Publish the final MLE parameter vector and the full local and global search result tables (as CSV) so that at least the reported numerical results can be inspected without re-running the optimization.
3. **Partial public replication**: Identify a publicly available analogous dataset (e.g., a different population's HRV series) and re-run the core analysis to demonstrate that the workflow is reproducible in principle.

## Limitations

- This skill cannot determine whether the reported results are correct — only whether they are verifiable. A project run in a closed environment may have produced entirely valid results that happen to be unverifiable.
- The skill does not evaluate the scientific merit of the data-use agreement or the appropriateness of using proprietary data for a course project. That is a pedagogical rather than methodological judgment.
- If the closed-environment constraint applies to only some of the data (e.g., one covariate is proprietary but the main outcome is public), partial reproducibility is possible and the audit should assess each component separately.
- Does not replace the full POMP reproducibility checklist (SKILL_pomp.md §10); it adds a structured framework for the specific case where the standard checklist is blocked by data access constraints.
