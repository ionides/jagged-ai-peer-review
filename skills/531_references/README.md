# references/

## Files

### `531-conventions.md`
**Role: False positive suppressor**

Documents STATS 531 course conventions that differ from publication-standard expectations. When the AI reviewer encounters something that looks like a problem but is actually standard course practice, this file prevents it from being flagged.

Contents:
- ACF residual diagnostic standards (the 1/18 lag rule, mild heteroskedasticity)
- The run_level framework: expected Np / Nmif / Nreps values at each computational level
- POMP likelihood evaluation conventions (replicated pfilter required; mif2 internal loglik not reliable)
- mif2 convergence standards (weak identifiability is expected; what good loglik convergence looks like)
- Profile likelihood conventions (acceptable point counts, envelope interpretation)
- Compartment model standards (Euler method acceptable; conservation requirement)
- Benchmark comparison norms (losing to ARMA is not automatically a failure; likelihoods across model classes are comparable)
- ESS interpretation (low ESS has multiple causes, not always model misspecification)
- Genuine review points: what to flag despite the course context

Sources: slides Ch 09, 10, 11, 12, 13, 15, 16, 17; MT2. Version 0.3.0, updated 2026-03-25.

---

### `531-weakness-reference.md`
**Role: True positive amplifier**

Documents errors that STATS 531 students were explicitly taught and assessed on. When one of these errors appears in a project, it should be flagged with higher confidence than general methodological concerns.

Contents:
- 31 course-confirmed (CC-Yes) student errors in two groups:
  - POMP errors (1.1–1.15): 8 Major, 7 Minor
  - ARMA errors (2.1–2.16): 2 Major, 14 Minor
- Severity labels: Major or Minor only (no Moderate)
- Each error includes: description, why it's wrong, and the quiz/exam source

Sources: W25 quizzes Q1–Q13, W26 quizzes Class 01–20, MT1, MT2. Version 0.2.0, updated 2026-03-25.

---

## How the two files relate

```
531-conventions.md        531-weakness-reference.md
      |                           |
suppress false positives    amplify true positives
      |                           |
 "don't flag this"          "flag this with confidence"
```

A student practice that appears in `531-conventions.md` should not be flagged even if it looks unusual.

An error that appears in `531-weakness-reference.md` should be flagged even if the AI reviewer is uncertain, because the student had direct instruction on the topic.

