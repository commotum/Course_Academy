---
name: core-move-refiner
description: Refine an existing core-move lesson by comparing it against lessons in the local Math Academy Mathematical Foundations vault. Use when Codex has already generated or edited a focused lesson and the user asks to compare it to Math Academy lessons, extract pedagogical insights, improve structure or practice, or make the lesson feel more Math Academy-like.
---

# Core Move Refiner

## Overview

Improve a generated core-move lesson by studying real Math Academy lesson patterns, identifying transferable pedagogy, and editing the generated lesson accordingly. The skill should produce a better lesson, not just a critique.

Before creating or changing any quiz block, invoke `$quiz-block-factory` at
`/Users/jake/Developer/study/util/skills/quiz-block-factory`. Its schema, feedback
standard, and validator are authoritative.

Primary comparison folder:

```text
/Users/jake/Developer/study/vault/MA/Mathematical-Foundations
```

## Workflow

1. Resolve the generated lesson.
   - If the user gives a path, read that file.
   - If the user gives an assignment/problem path and a problem number, infer the lesson path as `Lessons/Problem-N.md` next to the source file.
   - Preserve the original problem's givens, answer form, answer choices, and correct answer.
   - Do not modify Math Academy source lessons.

2. Select comparison lessons.
   - Compare against 4 Math Academy lessons unless the user requests another count.
   - If the user asks for random comparisons, sample random `.md` files under the Mathematical Foundations folder.
   - If the user asks for targeted refinement or the generated lesson has an obvious topic, prefer 2-4 relevant Math Academy lessons found by searching lesson titles, examples, and questions.
   - Avoid table-of-contents files and non-lesson notes when sampling.

Useful commands from the study repo root:

```bash
find vault/MA/Mathematical-Foundations -path '*/Lessons/*.md' -type f
python3 -c "import pathlib, random; files=list(pathlib.Path('vault/MA/Mathematical-Foundations').glob('**/Lessons/*.md')); print('\n'.join(map(str, random.sample(files, 4))))"
rg -n -i "keyword|synonym|notation" vault/MA/Mathematical-Foundations
```

3. Read for structure, not topic content.
   - Table of contents: section count, naming, and progression.
   - Prerequisites: whether they are minimal and linked to readiness.
   - Introduction: how quickly it states the reusable rule, cue, representation, or procedure.
   - Worked examples: whether they are concise, canonical first, and split into digestible algebra or reasoning steps.
   - Question placement: whether practice appears immediately after the matching explanation.
   - Practice density: whether a section uses one or multiple near-transfer questions.
   - Variation: what changes between sections, such as numbers, signs, representation, direction, condition, or a common trap.
   - Distractors: whether wrong answers encode real mistakes.
   - Summary: whether it compresses the cue, rule, procedure, and trap into a reusable checklist.
   - Media/representation: whether diagrams, tables, or visual representations make the reasoning easier; do not add images unless the generated lesson genuinely needs them and assets exist or can be created.

4. Extract transferable insights.
   - Report concrete observations from the sampled lessons before editing.
   - Translate each observation into an actionable change for the generated lesson.
   - Use structural and pedagogical patterns only; do not copy Math Academy wording or proprietary question content.
   - Prefer changes that make the lesson more usable: clearer cue, tighter rule statement, better staged examples, more near-transfer practice, stronger distractors, or a sharper summary.

5. Edit the generated lesson.
   - Keep the lesson focused on the same single core move.
   - Preserve the existing Markdown contract used by `core-move-lesson`: title, table of contents, prerequisites, introduction, focused sections, worked examples, quiz blocks, and summary.
   - Put every practice item in a fenced `quiz` block.
   - Use `type: radio` for ordinary multiple-choice practice.
   - Keep quiz ids and option ids unique and stable within the file.
   - Preserve or improve substantive corrective feedback for every generated radio or
     checkbox option, following `$quiz-block-factory`; correct responses need a
     rule-to-conclusion explanation, while distractors need option-specific diagnosis
     and repair.
   - Do not introduce unrelated downstream topics just because a sampled lesson is broader.

6. Validate.
   - If the lesson contains quiz blocks, run the quiz validator:

```bash
python3 /Users/jake/Developer/study/util/skills/quiz-block-factory/scripts/validate_quiz_blocks.py \
  /path/to/lesson.md \
  --require-radio-practice \
  --strict-ids \
  --require-feedback \
  --lint-feedback
```

   - Run `git diff --check -- /path/to/lesson.md`.
   - Fix every validation or whitespace error before reporting completion.

## Output Shape

In the final response, include:

- The generated lesson path that was modified.
- The 4 Math Academy lesson files compared.
- The main transferable insights.
- The concrete edits made.
- Whether quiz validation and `git diff --check` passed.

Keep the comparison concise. The useful output is the improved lesson plus enough evidence to show why the edits were made.
