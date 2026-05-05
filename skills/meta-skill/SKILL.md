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


## 2. Define the Skill

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


### Task Context

Describe the task that revealed the need for the skill.

Include:

- the task type
- what made it difficult
- what reasoning was required


### Core Value

In one sentence: what future task does this skill make meaningfully easier or more consistent?


## 3. Extract the Core Method

Describe the reusable procedure that defines the skill.

Use clear operational steps.

Example structure:

1. Identify task type
2. Apply evaluation or analysis procedure
3. Extract key findings
4. Document conclusions

Focus on the steps that made the approach effective.


## 4. Define Limitations and Edge Cases

Describe conditions where this skill would break down, produce unreliable output, or should not be applied.

Ask:

- What inputs would cause this method to fail?
- What assumptions does the method rely on?
- Is there a task that looks similar but where this skill would give bad results?

This section forces honest scoping and prevents overuse.


## 5. Define the Trigger

Specify when the new skill should activate.

The trigger description is what Claude Code uses to decide whether to invoke the skill — it must be precise and discriminating, not general. Prefer specificity over breadth.

Examples:

- when reviewing a POMP model fit report that includes likelihood profiles and residual diagnostics
- when evaluating whether a statistical model's assumptions are met prior to inference
- when auditing an R Markdown document for computational reproducibility

Avoid triggers like "when analyzing data" — too broad to be reliable.


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

<Precise trigger conditions.>

## Procedure

### 1. <Step>
...

### N. <Step>
...

## Limitations

<When this skill should not be used or may produce poor results.>
```

Make the output block clearly delimited so it can be copied and pasted directly into a new SKILL.md file.
