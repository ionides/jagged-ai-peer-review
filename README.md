# Jagged AI in Scientific Peer Review: Evidence from POMP Data Analysis

This folder is a self-contained record of the experiment and the paper. It includes the manuscript, all agent definitions, skill files, input data, AI-generated reviews, comparison outputs, and analysis scripts.

---

## Paper

The manuscript is `ms.qmd`. To compile:

```bash
quarto render ms.qmd --to pdf
```

**Requirements:** Quarto, Python 3, `pandas`, `numpy`, `scipy`, `matplotlib`.

**Model:** All AI reviews were generated using `claude-sonnet-4-6` (April–May 2026).

---

## Folder Structure

```
submission/
├── ms.qmd / ms.pdf / bib-ai.bib   — manuscript and bibliography
├── agent-descriptions/             — agent definition files
├── skills/                         — skill files loaded by agents
├── data/                           — human peer reviews (input data)
├── results/
│   ├── alex/                       — Baseline reviews
│   ├── charlie/                    — 531-References reviews
│   ├── doug/                       — Meta-Skill reviews
│   ├── evan/                       — Orchestrator reviews
│   └── comparator/                 — Comparator comparison files
└── analysis/                       — Python scripts, figures, and results CSV
```

---

## Experiment Workflow

### 1. Data Collection

Student projects were downloaded manually from the public STATS 531 GitHub repositories:

- [531w21](https://github.com/ionides/531w21/tree/main/final_project) — 16 projects
- [531w22](https://github.com/ionides/531w22/tree/main/final_project) — 23 projects
- [531w24](https://github.com/ionides/531w24/tree/main/final_project) — 16 projects
- [531w25](https://github.com/ionides/531w25/tree/main/final_project) — 17 projects

Each project report is named `blinded.Rmd` / `blinded.html` following the course's file naming convention.

Human peer reviews (`comments.md` files) were extracted from the project repositories using Claude Code and stored in `data/human-reviews/`.

### 2. AI Reviews

Four Claude agents reviewed each of the 72 projects independently using `claude-sonnet-4-6`. The agent definitions are in `agent-descriptions/`. Each agent was instructed to produce a structured review of up to 15 major and minor weaknesses. This cap was set slightly above the observed average human review length of 10–12 points to keep the total volume of findings comparable between agents and human reviewers.

**Baseline (Alex)**
No skill files. Reads the project writeup (`blinded.Rmd`, `blinded.html`) and any other files in the folder. It then produces a structured peer review of up to 15 major and minor weaknesses. Has no access to the human reviews. Reviews saved to `results/alex/`. Ran in parallel across projects.

**CourseGuided (Charlie)**
Loads `skills/guided-pomp-review/` and `skills/531_references/` before reviewing. Otherwise follows the same process as Alex. Reviews saved to `results/charlie/`. Ran in parallel across projects.

**Meta-Skill (Doug)**
Loads `skills/guided-pomp-review/` and any previously generated skills in `skills/`. After each review, performs a meta-skill reflection and writes a new skill file to `skills/` if a reusable pattern was found. Must be run sequentially — each run may generate skill files that subsequent runs depend on. Reviews saved to `results/doug/`.

**Orchestrator (Evan)**
Runs a self-contained 4-step pipeline: first-pass review → dual audit → challenge-judge → final review. All instructions are embedded in `agent-descriptions/evan.md`. Reviews saved to `results/evan/`.

#### Skill Files

All skill files used in the experiment are in `skills/`. The mapping from agent to skill files is:

| Agent | Skill files loaded | Tools |
|:------|:-------------------|:------|
| Baseline | none | Bash, Glob, Grep, Read, Write |
| CourseGuided | `skills/guided-pomp-review/`, `skills/531_references/` | Bash, Glob, Grep, Read, Write |
| Meta-Skill | `skills/guided-pomp-review/`, all `skills/pomp-*/` files present at runtime | Bash, Edit, Glob, Grep, Read, Write |
| Orchestrator | `skills/guided-pomp-review/` (pipeline instructions embedded in `agent-descriptions/evan.md`) | Bash, Glob, Grep, Read, Write |

The `skills/pomp-*/` files were generated incrementally by the Meta-Skill agent during its sequential run. Each file represents a reusable pattern discovered during a prior review. These files are included in `skills/` in the order they were created, and reproduce the exact skill context available to the agent at each step of the sequential run.

#### Skill File Construction

**`skills/guided-pomp-review/`**: Using Claude, skill file was compiled based on the Wheeler et al. cholera paper [@wheeler2024cholera], then reviewed and fleshed out manually. It provides a 13-item checklist for evaluating POMP manuscripts covering likelihood inference, benchmark comparisons, convergence diagnostics, and related criteria.

**`skills/531_references/`**: Drafted by Claude from STATS 531 midterm materials ([mt1](https://github.com/ionides/531w26/tree/main/mt1), [mt2](https://github.com/ionides/531w26/tree/main/mt2)), then reviewed and fleshed out manually. The midterms are compilations of common mistakes the professor has observed in past student projects, along with course conventions and pointers students are expected to keep in mind. It contains two files: one suppressing false positives by documenting course conventions that differ from publication standards, and one amplifying true positives by listing errors students were explicitly taught and assessed on.

**`skills/pomp-*/`**: Auto-generated by the Meta-Skill agent during its sequential run. After completing each review, the agent reflected on whether a reusable pattern had been identified and, if so, wrote a new skill file to `skills/`. No manual editing was done on these files.

#### Invocation

Agents were registered as Claude Code agents using the definitions in `agent-descriptions/`. Each agent was invoked through a Claude Code session with a natural-language prompt identifying the target semester and project, for example:

> "Alex, I want you to review projects in W21."

Claude Code matches the name to the corresponding agent definition and begins the review. No additional workflow instructions were given in the prompt and the agent definition was treated as the authoritative spec. Each agent definition includes instructions to extract the semester and project number from the prompt and use them to navigate to the corresponding project folder and access the relevant files.

- **Baseline, CourseGuided, and Orchestrator** were invoked semester by semester and ran in parallel across projects within each batch.
- **Meta-Skill** was invoked one project at a time in a fixed sequential order, so that skill files generated during earlier reviews were available as context for later ones.

Each agent definition included an instruction to list the files it accessed at the end of its review. After the runs were complete, these file lists were manually checked to confirm that each agent had not accessed incorrect or unrelated files. No such violations were found. However, agents frequently exercised their own discretion in selecting which files to read among those they were instructed to consider, reading some skill files while skipping others. This selective reading behavior was consistent across agents and could not be controlled through prompting alone. 

This was intentionally allowed for the Meta-Skill agent: as the sequential run accumulated more `pomp-*` skill files, loading all of them before each review would have consumed a large portion of the context window, leaving less room for the project itself. The agent definition therefore explicitly instructed Meta-Skill to use its judgment about which generated skill files to consult, rather than reading all of them. Even when all skill files were loaded, LLMs tend to pay less attention to content in the middle of a long context, meaning irrelevant skill files would dilute rather than reinforce the ones that actually applied to the project at hand.

### 3. Permissions

The `.claude/settings.json` file documents the permissions granted to the agents during the experiment: read access to project files and skill files, write access to the results and skills directories.

### 4. Comparison

After all AI reviews were complete, the Comparator agent compared each AI review against the human review for the same project. It uses a three-agent system in addition to a python script that assembles the sub reports at the end:

- `Comparator.md`: orchestrator (tools: Agent, Bash). Holds no file-reading tool itself; it calls `HumanExtractor` once, then calls `ComparatorReviewer` once per reviewer, then runs the assembly script.
- `HumanExtractor.md`: sub-agent that reads the human peer review file, extracts and standardizes the issues list, and writes it to disk (tools: Read, Write, Grep).
- `ComparatorReviewer.md`: sub-agent that classifies one reviewer's findings into categories A–F against the extracted human issues list, and writes its own sub-report to disk (tools: Read, Write, Grep).
- `analysis/assemble_comparator.py`: deterministic script, run by the orchestrator as the final step. It copies the human issues list and each sub-report verbatim, then computes the Combined Summary Table, per-reviewer metrics, consensus misses, and unique finds from the counts and coverage records those files already contain.


Calling `ComparatorReviewer` as a separate agent instance for each reviewer, in a fresh context with no memory of the other reviewers, was done to prevent any cross reviewer contamination or hallucination issues that could arise. Extraction of the human issue list is likewise handled by its own sub-agent (`HumanExtractor`), reading only the human review and no AI review, so the reference list every agent is scored against cannot be influenced by AI phrasing.

Comparator is invoked once per project (semester + project number), from the `submission/` directory. For example:

> "Comparator, W21 PROJECT01."

Comparison outputs are in `results/comparator/`.

| Code | Definition |
|:----:|:-----------|
| A | AI major finding — human did not raise |
| B | AI major finding — human also raised |
| C | AI minor finding — human did not raise |
| D | AI minor finding — human also raised |
| E | Human raised — AI did not address |
| F | Direct contradiction — excluded from Human Overlap denominator |

The two headline metrics, chosen to treat AI-unique and human-unique findings symmetrically (an issue is either raised or not raised in peer review), are:

**Human Overlap** = 1 − E / (total human issues), computed per project from each sub-report's Coverage record. 
**AI-Unique Rate** = A + C / (total AI findings) = A + C / (A + B + C + D), computed per project from each sub-report's Findings classification.

The two labels A and E used for computing the two measures given above are explored further in @fig-themes (Figure 3) and @fig-matrix (Figure 4) in the paper.

#### Classification Rules

Each `ComparatorReviewer` invocation receives (1) the AI reviewer's file and (2) the numbered human issues list extracted by the orchestrator. The agent reads the AI review and assigns every finding to a category using the following rules:

**Matching (B/D vs. A/C/E):** Two issues are treated as matching when they refer to substantially the same underlying concern, even if phrased differently or pointing to a different specific manifestation of the same error. The deciding question is whether both identify the same logical or methodological error. Superficial topic overlap is not sufficient and issues on the same general theme that make different specific claims are not matched.

Examples from the agent definition:
- MATCH: "likelihood profiles are not shown" ↔ "no profile likelihoods are computed"
- MATCH: "model equations do not match the code" ↔ "inconsistency between the reported model and the implementation"
- NO MATCH: "model equations do not match the code" ↔ "notation collision in the equations" — related topic, different specific claim
- NO MATCH: "log-likelihood comparisons are invalid across different data scales" ↔ "AIC values are not reported" — same general topic, distinct claims

**Major/Minor (A vs. C, B vs. D):** Determined solely by the AI reviewer's own label. If the AI reviewer called a finding Major, it maps to A or B; if Minor, to C or D. The human review does not use Major/Minor labels, so severity is never inferred from the human side.

**Counting rule:** If several AI findings each match the same human issue, every one of them is labeled B or D and each names the human issue it matches. A or C is used only for a finding that matches no human issue at all. Note that there are cases where a single AI point matches two or more human issues at once and there are cases where multiple AI points match to a single human issue. Because of this, the number of B/D labeled findings need not equal the number of covered human issues.  



