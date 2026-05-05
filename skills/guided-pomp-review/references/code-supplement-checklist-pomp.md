# Code and Data Supplement Checklist (POMP-Focused)
*Adapted from Biometrical Journal standards for computational reproducibility, with additions for POMP manuscript review*

Apply this checklist to evaluate code and data supplements in statistical papers. Items marked **[POMP]** are additions or modifications specific to POMP manuscripts; all other items apply generally.

---

## Reproducibility

### Completeness
- [ ] Supplement contains ALL code and data to reproduce ALL figures, tables, and results
- [ ] Master scripts or Makefiles automate full reproduction workflow
- [ ] Different simulation settings executed via parameters, not manual code edits
- [ ] No "copy-paste" programming with near-identical script variants
- [ ] **[POMP]** Final MLE parameter vectors are archived as standalone files (e.g., CSV or RDS), separate from the optimization code — readers should be able to evaluate results without re-running the full optimization (Wheeler et al. 2024, SI §S7)
- [ ] **[POMP]** All auxiliary inputs are included: covariate matrices, spatial adjacency matrices, population data, and any other inputs beyond the primary case count time series

### Traceability
- [ ] Comments state which figure/table each code section produces
- [ ] Output filenames match manuscript numbering (Table1.csv, Figure2.png)
- [ ] Results saved with descriptive filenames in organized folders
- [ ] **[POMP]** Model-code consistency: the observation (measurement) model in code matches the mathematical specification in the text — discrepancies here are a reproducibility failure documented in Wheeler et al. (2024) and can materially affect results

### Randomization
- [ ] RNG seeds set for exact reproducibility
- [ ] Monte Carlo errors verified to be negligible (results stable across reruns)
- [ ] **[POMP]** Particle filter seeds recorded per run: the number of particles, IF2 iteration counts, and per-job random seeds are documented so that stochastic likelihood estimates are exactly reproducible

### Data Restrictions
- [ ] If data cannot be shared: synthetic/anonymized pseudo-data provided
- [ ] Original data available to editors for audit if needed

### Computational Cost
- [ ] For long-running code: intermediate results provided
- [ ] Parameters documented to reduce runtime for spot-checks
- [ ] Spot-checks possible without full rerun
- [ ] **[POMP]** For HPC/cluster analyses: job submission scripts (e.g., SLURM, PBS) are included and cluster environment specifications (node count, memory, walltime) are documented
- [ ] **[POMP]** Total computational cost is reported (CPU-hours or equivalent), so readers can assess feasibility of reproduction and reviewers can judge whether computational effort was adequate

---

## Documentation (README)

- [ ] Format: .txt, HTML, or PDF (not .docx)
- [ ] Software versions: OS, language versions, all package versions
- [ ] For R: `sessionInfo()` output included
- [ ] Reproducible environment option provided (Docker, renv, packrat)?
- [ ] GitHub packages: commit hash or release tag + installation instructions
- [ ] Clear instructions: which scripts, in what order, for which outputs
- [ ] Any manual steps documented with exact file/line/edit details
- [ ] Data documentation: provenance, licensing, data dictionaries
- [ ] File listing with folder structure and content descriptions
- [ ] **[POMP]** `pomp` and `spatPomp` package versions explicitly pinned — the API has changed substantially across versions and results may not reproduce on current CRAN releases without version locking (e.g., via `renv`)
- [ ] **[POMP]** Instructions distinguish between: (a) reproducing figures from archived parameter files (fast), (b) reproducing optimization from provided starting values (moderate), and (c) full replication from scratch (expensive) — readers should know which level is feasible

---

## Coding Standards

### Format
- [ ] ASCII/UTF-8 encoding
- [ ] English for all names, comments, documentation
- [ ] Consistent formatting: spacing, line lengths (≤80-100 chars), indentation
- [ ] Proper file extensions (.R, .py, .sas, not .txt or .pdf)

### Organization
- [ ] Code split by functionality with descriptive filenames
- [ ] Imports/dependencies at file top
- [ ] Sensible folder structure
- [ ] Functions documented (inputs, outputs, purpose)

### Quality
- [ ] No copy-paste code; reusable functions/loops instead
- [ ] Master scripts handle iteration over settings
- [ ] No repeated manual edits required
- [ ] Analysis code separated from function definitions
- [ ] No extraneous/commented-out code
- [ ] No global workspace modifications (no `rm(list=ls())`)
- [ ] No auto-installing packages without user consent
- [ ] Relative paths only (no `C:/Users/...`); or absolute paths documented

### Platform Independence
- [ ] Avoid OS-specific commands (`windows()`, `windowsFonts()`)
- [ ] Use `file.path()` or similar for cross-platform paths
- [ ] R packages as source (.tar.gz), not Windows binaries (.zip)
- [ ] Case-sensitive path names verified

### Compiled Code
- [ ] Source code + Makefiles/build instructions provided
- [ ] Pre-compiled executables included

---

## Red Flags

**General:**
- "Run script1.R, then manually change line 47, then run script2.R..."
- Hard-coded paths to author's local filesystem
- Missing package versions or `sessionInfo()`
- Code in Word documents or PDFs
- Results only reproducible on author's machine
- Intermediate results missing for expensive computations
- Simulation code absent from supplement

**POMP-specific:**
- Final MLE parameter vectors not archived separately — readers cannot evaluate results without re-running expensive optimization
- `pomp`/`spatPomp` version not pinned — silent API changes may break reproduction
- Particle count and IF2 iteration count not recorded — stochastic results cannot be exactly reproduced
- Measurement model in code differs from text description (Wheeler et al. 2024 document this as a concrete reproducibility failure in one of their evaluated models)
- No HPC job scripts for cluster-based analyses — reproduction is nominally possible but practically infeasible
- Auxiliary data files (covariate matrices, spatial structure) missing — model cannot be run even if main code is present
- No distinction between fast (parameter-file-based) and slow (full optimization) reproduction paths

---

## Key References
- Wheeler J, Rosengart A, Jiang Z, Tan K, Treutle N, Ionides EL (2024). Informing policy via dynamic models: Cholera in Haiti. *PLOS Computational Biology* 20(4): e1012032.
- Biometrical Journal reproducibility standards for computational supplements.
