---
name: meta-skill
description: Reflect after completing complex tasks to identify reusable methods and propose new skills. Trigger only when you improvised a novel multi-step workflow — not for routine tasks. Best suited for POMP analysis, statistical evaluation, reproducibility audits, and manuscript review.
---

# Meta-Skill: Skill Acquisition

## Purpose

This skill converts task-specific reasoning into reusable skills.

When a task reveals a novel method or workflow, this skill proposes a structured skill that can be reused in similar tasks and added to the repository.

The goal is to gradually build a library of skills that improve efficiency, consistency, and reproducibility across complex analytical and review tasks.

# When This Skill Should Activate

Use this skill after completing a task if one or more of the following occurred:

- You developed a new multi-step procedure
- You performed structured reasoning or evaluation
- You improvised a workflow that worked well
- You noticed a missing capability that would improve future tasks
- You solved a problem that is likely to recur in similar contexts

Common contexts include:

- reviewing research projects
- evaluating statistical models
- auditing reproducibility
- analyzing code or data
- synthesizing literature
- refereeing a manuscript
- designing workflows

**Do not activate** if the task was routine and involved no novel reasoning. Stop without producing a proposal.


# Goal

Produce a meta-skill reflection that proposes a candidate skill capturing the reusable method discovered during the task.

The proposed skill should describe:

- the capability
- the reusable method
- its limitations and edge cases
- when it should activate in the future


# Procedure

## 1. Identify a Skill Opportunity

Reflect on the completed task.

Ask:

- Did I create or adapt a method to solve the task?
- Would this approach improve future tasks of the same type?
- Could the reasoning be converted into a repeatable workflow?
- Could these methods be novelly introduced to another context?

If no — the task was routine and required no novel reasoning — **stop here. Do not produce a skill proposal.**

If yes, continue.


## 2. Check the Existing Skill Library

Before proposing a new skill, read the SKILL.md file of every existing skill in the repository.

For each existing skill, ask:

- Does its **trigger condition** already cover the pattern I observed?
- Does its **procedure** already describe the steps I improvised?
- Is my candidate skill a narrow variant or special case of an existing skill?

If an existing skill already covers the pattern — even partially — **do not create a new skill.** Instead, note which existing skill applies and stop here.

If the pattern is genuinely absent from all existing skills, continue to Step 3.

If the pattern is partially covered but the existing skill has a meaningful gap (e.g., it handles the epidemiological case but not the political science case), consider whether the better fix is to **extend the existing skill** rather than create a new one. Only create a new skill if the extension would make the existing skill's trigger condition too broad or its procedure too complex to follow.


## 3. Define the Skill

Provide the following elements.

### Skill Name

Create a concise capability name.

Good examples:

- `stats-project-review`
- `pomp-model-check`
- `reproducibility-audit`
- `literature-synthesis`

Avoid vague names such as:

- `analysis-helper`
- `review-tool`


### Core Value

In one sentence: what future task does this skill make meaningfully easier or more consistent? This sentence becomes the `description` field in the skill's frontmatter — make it precise and discriminating, not a general summary.


## 4. Extract the Core Method

Describe the reusable procedure that defines the skill.

Use clear operational steps.

Example structure:

1. Identify task type
2. Apply evaluation or analysis procedure
3. Extract key findings
4. Document conclusions

Focus on the steps that made the approach effective.


## 5. Define Limitations and Edge Cases

Describe conditions where this skill would break down, produce unreliable output, or should not be applied.

Ask:

- What inputs would cause this method to fail?
- What assumptions does the method rely on?
- Is there a task that looks similar but where this skill would give bad results?

This section forces honest scoping and prevents overuse.


## 6. Define the Trigger

Specify when the new skill should activate.

The trigger description is what Claude Code uses to decide whether to invoke the skill — it must be precise and discriminating, not general. Prefer specificity over breadth.

Examples:

- when reviewing a POMP model fit report that includes likelihood profiles and residual diagnostics
- when evaluating whether a statistical model's assumptions are met prior to inference
- when auditing an R Markdown document for computational reproducibility

Avoid triggers like "when analyzing data" — too broad to be reliable.


# Self-Check

Before saving the skill file, verify each of the following. If any check fails, revise before saving.

- [ ] **Description discriminates**: would the `description` frontmatter avoid firing on a routine review that doesn't involve this specific error pattern?
- [ ] **"Do not use when" is present**: does "When to Activate" include at least one explicit exclusion condition?
- [ ] **Procedure is operational**: are the steps numbered and concrete enough that a different reviewer could follow them without additional context?
- [ ] **Library check was completed**: was every existing skill file in Skills/ read before deciding to create this skill?
- [ ] **Not a duplicate or narrow variant**: does this skill catch something that no existing skill (including host skills with folded steps) already covers?

If all checks pass, save the skill file. If any fail, either revise the skill or — if the pattern turns out to be covered after all — do not save.

# Quality Guidelines

Proposed skills should be:

- reusable across similar tasks
- operational rather than abstract
- narrowly scoped enough to be reliable

Do not propose a skill if the task did not reveal a meaningful reusable method.


# Output

If the proposed skill appears useful, write the full skill as a ready-to-copy `.md` file using the format below.

The `description` field in the frontmatter is what Claude Code reads to decide whether to trigger the skill. It must be a precise, discriminating one-sentence description — not a general summary.

```markdown
---
name: <skill-name>
description: <one sentence: when to trigger, what it does, and what distinguishes it from similar tasks>
---

# <Skill Title>

## Purpose

<What this skill does and why it helps.>

## When to Activate

<Precise trigger conditions — what must be true for this skill to apply.>

Do not use this skill when:
- <Condition under which this skill does not apply>
- <A task that looks similar but where this skill gives bad or redundant results>

## Procedure

### 1. <Step>
...

### N. <Step>
...

## Limitations

<When this skill should not be used or may produce poor results.>
```

Make the output block clearly delimited so it can be copied and pasted directly into a new SKILL.md file.
