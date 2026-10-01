# Analysis pipeline

## 1. Comparator assembly & raw metrics

Builds the per-project comparator reports, then the flat metrics table that everything else in this directory reads from.

1. **`assemble_comparator.py`**: Assembles each project's final `results/comparator/comparator-{SEM}_PROJECT{NN}.md` from the human-issues list and the four sub-reports. Copies each sub-report verbatim. Computes a combined summary table and per-reviewer metrics. Generates a `Cross-Reviewer Aggregation` section, which contains consensus misses and unique finds per reviewer. Run by the Comparator agent during step 3 of its workflow.
2. **`parse_comparator.py`**: Regex-parses the Counts tables and Coverage records directly out of the 72 assembled `comparator-*.md` files, producing `comparator_results.csv`.

**Output**: `comparator_results.csv`: one row per (semester, project, reviewer), 288 rows, with the A-F counts and derived metrics (Human Overlap, AI-Unique Rate). `ms.qmd` read this file for all figures and statistics.

## 2. Figure 3: consensus-miss theme categorization

Produces the five-theme breakdown of human issues that every one of the four AI reviewers missed (`fig-themes`).

1. **`extract_consensus_misses.py`**: Scans all 72 assembled `comparator-*.md` files and pulls every human issue marked as missed by all four reviewers into `consensus_misses.txt`.
2. **Categorization**: `consensus_misses.txt` is classified into the five themes (Statistical interpretation, Model improvement direction, Argumentation / narrative, Presentation / visualization, Domain / data context) in a single pass by Claude, producing `categorized_misses.txt`. These five themes were preset from the first pass and kept fixed for consistency as different passes are not guaranteed to reproduce identical themes. We checked that the categorization was reasonable by verifying specific examples, which are listed as case studies in the paper. 
3. **`count_themes.py`**: Counts the total for `categorized_misses.txt`'s per-finding theme labels into `theme_counts.csv`.

**Output**: `theme_counts.csv`: Used to generate `ms.qmd`'s Figure 3 (`fig-themes`).


## 3. Figure 4: AI-unique findings matrix

Produces the per-agent matrix of AI-unique (A/C) findings (`fig-matrix`)

1. **`extract_ac_findings.py`**: Pulls every AI-unique (A/C) finding into `ac_findings.txt` for preliminary anecdote-hunting.
2. **`matrix_comparison.py`**: Generates `matrix_comparison.png`. Per-agent "X.X/proj" counts (blocks 2-4) are computed directly from `comparator_results.csv`. The specific labels shown in each row are hard-coded rather than regenerated per run, since repeated LLM categorization are not guaranteed to reproduce identical groupings. 

**Output**: `matrix_comparison.png`: `ms.qmd`'s Figure 4 (`fig-matrix`)

## 4. Comparator Validation

Five projects were selected at random from each semester where matches made by the Comparator were manually read and evaluated as clear, disputable, or incorrect. **`Comparator_Validation_Results.md`** records these per-reviewer counts with matches specifically cited for every disputable or incorrect matches. 
