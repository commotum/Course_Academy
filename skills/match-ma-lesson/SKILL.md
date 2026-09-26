---
name: match-ma-lesson
description: Find and verify the Math Academy lesson or lessons that best match a given math problem, classify whether a genuine question-level equivalent exists, and explicitly signal when the problem needs a generated core-move fallback. Use when the user gives a single math problem, assignment problem, or problem excerpt and asks which Math Academy lessons cover the same skills, knowledge, or question type, including assignment workflows that must distinguish true matches from unmatched problems.
---

# Match MA Lesson

## Overview

Match a given math problem to Math Academy lessons in the study vault. Use the scoped indices to find candidate lessons, but choose matches only after inspecting the candidate lesson markdown and comparing its examples/questions to the given problem.

## Workflow

1. Identify the problem's mathematical task.
   - Extract the topic, operation, requested output, givens, constraints, notation, and needed prerequisite facts.
   - If the user provides a file path, inspect the exact problem text and cite the line number.
   - Keep the problem atomic; do not broaden to nearby assignment problems unless the user asks for a whole assignment.

2. Search the scoped Math Academy indices first.
   - For MTH-252/MTH-253 review matching, start with `vault/MA/Mathematical-Foundations/catalog.csv`.
   - For MTH-253 sequences, series, integration techniques, and other Calculus II material, also search `vault/MA/Single-Variable-Calculus/catalog.csv` and the course-local `vault/MA/Single-Variable-Calculus/CA2/topics.csv`.
   - The useful group catalog columns are `layer`, `topic-id`, `topic-code`, `topic-name`, `lesson-path`, and `source-path`.
   - The useful course topics columns are `topic-id`, `topic-code`, `topic-number`, `topic-name`, `unit`, `module`, `lesson-path`, `source-path`, and `layer`.
   - Use `layer` for study-order and prerequisite-readiness decisions. Unit/module order is structural navigation, not the study queue order.
   - In course-local `topics.csv`, `lesson-path` and `source-path` are relative to that course folder. For CA2, prefix them with `vault/MA/Single-Variable-Calculus/CA2/`.
   - Search topic names with the problem's core concepts and synonyms.
   - Prefer `rg` for local search.

```bash
rg -n -i "right riemann|riemann sum|definite integral" vault/MA/Mathematical-Foundations/catalog.csv vault/MA/Single-Variable-Calculus/catalog.csv
rg -n -i "geometric series|taylor|maclaurin|power series" vault/MA/Single-Variable-Calculus/catalog.csv vault/MA/Single-Variable-Calculus/CA2/topics.csv
```

3. Expand the candidate set when the index is too broad or too sparse.
   - Search lesson markdown under the relevant scoped course folders for exact terms, notation, and distinctive objects from the problem.
   - Use the global `vault/MA/catalog.csv` only as a broad fallback when Mathematical Foundations plus the relevant course/group index is clearly missing the topic.
   - Include prerequisite candidates when the problem requires a separate skill, such as special-angle trig values, exponent rules, factoring, or interpreting a graph.
   - Keep the working candidate list small enough to inspect carefully, usually 5-12 lessons.

```bash
rg -n -i "Question|Example|right Riemann|cos" vault/MA/Mathematical-Foundations/*/**/Lessons/*.md vault/MA/Single-Variable-Calculus/CA2/**/Lessons/*.md
```

4. Inspect candidate lesson questions and examples.
   - Open each candidate `lesson-path`; only use `source-path` if images, tables, or source assets are needed to understand a prompt.
   - Search inside each lesson for `**Question`, `**Example`, `Problem`, and the problem's key terms.
   - Read enough surrounding lines to understand the actual question type.

```bash
rg -n "Question|Example|Problem|right Riemann|cos" "vault/MA/path/to/Lesson.md"
nl -ba "vault/MA/path/to/Lesson.md" | sed -n '80,140p'
```

5. Rank by question-level similarity.
   - Treat matching lesson questions/examples as stronger evidence than a matching lesson title.
   - Prefer lessons that match the same mathematical action, such as compute, solve, estimate, graph, simplify, prove, or interpret.
   - Prefer lessons with the same representation, such as equation, table, graph, interval, sigma notation, word problem, or exact value.
   - Prefer lessons with the same answer form and constraints, such as exact value, decimal approximation, interval notation, multiple choice, or "do not compute X".
   - Mark prerequisite lessons separately from the main lesson; do not present a prerequisite as the best match unless it is the main task.
   - Mark nearby but weaker lessons as secondary when they teach related notation or a more advanced/later version of the idea.
   - Count a problem as matched only when at least one lesson question/example teaches the same core move and has substantially the same task shape. A shared topic name, prerequisite skill, or nearby technique is not enough.
   - If every candidate is only a prerequisite, near miss, broader survey, or different question type, classify the result as `No equivalent Math Academy lesson` instead of forcing a weak main match.

6. Report the result with evidence.
   - Start with exactly one match status: `Equivalent Math Academy lesson found` or `No equivalent Math Academy lesson`.
   - Give the best match first.
   - Include supporting/prerequisite lessons only when needed to do the problem.
   - Include line-linked file references for the index entry and for the matching lesson question/example.
   - Explain the match in terms of the task shape, not just keywords.
   - If useful, include a brief solution scaffold to show why the selected skills are necessary.
   - Do not claim an exact match unless a lesson question/example closely resembles the given problem.
   - For `No equivalent Math Academy lesson`, keep useful prerequisites and near misses clearly separated, and do not label either as the main lesson.
   - When the caller supplies an assignment file and problem number, include a fallback directive naming both: run `lesson-pipeline` in targeted mode for that problem. The assignment-level caller, normally `setup-lessons`, owns that invocation; do not run the full-assignment pipeline from this single-problem matcher.

## Output Shape

Use this structure unless the user asks for a different format:

```markdown
Match status: Equivalent Math Academy lesson found

Best match: [lesson title](absolute path with line)

Why: ...
Evidence: the lesson question/example at line ... asks students to ...

Prerequisite/supporting lessons:
- [lesson title](absolute path with line): why it is needed

Near misses:
- [lesson title](absolute path with line): why it is related but not the best match
```

For an unmatched problem, use:

```markdown
Match status: No equivalent Math Academy lesson

Why: ...

Prerequisite/supporting lessons:
- [lesson title](absolute path with line): why it is useful but not equivalent

Near misses:
- [lesson title](absolute path with line): the task-shape mismatch

Fallback: Run $lesson-pipeline in targeted mode for Problem N in /absolute/path/to/assignment.md.
```

## Local Paths

- Study repo root: `/Users/jake/Developer/study`
- Primary Mathematical Foundations catalog: `vault/MA/Mathematical-Foundations/catalog.csv`
- Calculus II course-local topics: `vault/MA/Single-Variable-Calculus/CA2/topics.csv`
- Single Variable Calculus group catalog: `vault/MA/Single-Variable-Calculus/catalog.csv`
- Broad fallback catalog: `vault/MA/catalog.csv`
- Group-local catalogs: `vault/MA/<Group>/catalog.csv`
- Course-local topics/prerequisites: `vault/MA/<Group>/<Course>/topics.csv` and `vault/MA/<Group>/<Course>/prerequisites.csv`
- Math Academy vault root: `vault/MA`

If a command is run from another working directory, resolve these paths relative to the study repo root.
