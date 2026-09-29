# Skills

This directory contains the skill files provided to the review agents. Skill files are
Markdown documents loaded into an agent's context before it begins a task.

The contents correspond to the review run, performed on 9–13 April 2026, which produced the
agent reviews in `results/`.

---

## Skill configurations by agent

### Baseline (Alex)
No skill files. The agent is instructed not to access any, and reads only the project files.

### CourseGuided (Charlie)
- `guided-pomp-review/` — POMP review checklist covering likelihood inference, benchmark
  comparisons, convergence diagnostics, profile likelihood validity, and IF2 configuration.
  Charlie reads the whole directory, including `references/` and `assets/`.
- `531_references/` — course-specific context: `531-conventions.md` (documents accepted
  STATS 531 practices, to suppress false positives) and `531-weakness-reference.md`
  (confirmed student errors from past quizzes and exams, to amplify true positives).

Charlie is restricted to these two and may not use any other skills.

### MetaSkill (Doug)
- `guided-pomp-review/`: same directory as Charlie. Doug is required to read
  `SKILL_pomp.md` and both files under `references/`.
- `meta-skill/SKILL.md`: after each review, instructs the agent to reflect on what it
  found and, if a reusable audit pattern emerged, write a new skill file into this directory.
- `pomp-*/`, plus `hp-filter-lambda-misspecification/`,
  `ode-compartment-observation-mismatch/`, `sarima-baseline-audit/` and
  `stationarity-test-conclusion-audit/`: the 58 skills Doug created autonomously during
  the run. Each is a subdirectory containing a single `SKILL.md`.

Doug is also instructed to consult the generated skills from previous reviews as relevant.

### Orchestrator (Evan)
- `guided-pomp-review/SKILL_pomp.md`: read before Step 1 and applied throughout.
  The remainder of Evan's pipeline is defined in its agent description rather than here.

---

## Run order and skill accumulation

MetaSkill was run sequentially so that skills generated during earlier reviews were
available to later ones. The order was not by semester number:

| Order | Semester | Projects | Generated skills available at start |
|---|---|--:|---|--:|
| 1 | W24 | 16 | 0 |
| 2 | W25 | 17 | 13 |
| 3 | W21 | 16 | 31 |
| 4 | W22 | 23 | 44 |

58 skills were generated across the 72 reviews (0.81 per review); 19 reviews produced none.

Each review ends with a list of files the agent reports having consulted. Counting the
generated skills on those lists against the number available at that point:

---

# Note

The MetaSkill agent's instructions direct it to consult skill files in `Skills/` excluding `guided-pomp-review/` and `meta-skill/`. `531_references/` is not on that exclusion list, so it was visible to MetaSkill as well as
to CourseGuided. One MetaSkill review — `W21_PROJECT04` lists both `531_references` files as consulted. No other
MetaSkill review does.


