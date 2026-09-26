---
name: core-move-lesson
description: Build a focused Math Academy-style study lesson from a homework problem by identifying the problem's core move, decomposing it into a controlled step progression, writing worked examples and required Obsidian quiz-block practice variants, and validating the generated quiz blocks.
---

# Core Move Lesson

## Use This Skill When

Use this skill when the user provides a homework problem, assignment problem, quiz item, or problem excerpt and wants a focused study lesson that teaches the one core move needed for that problem. The usual output is a standalone Markdown lesson file in a `Lessons/` folder next to the source assignment or problem file.

## Required References

Before planning or writing any quiz block, invoke `$quiz-block-factory` at
`/Users/jake/Developer/study/util/skills/quiz-block-factory`. Its canonical schemas,
feedback standard, and validator are authoritative for every quiz type.

Read these references before writing a lesson:

- `references/core-move-identification.md`
- `references/math-academy-lesson-principles.md`
- `references/step-progression.md`
- `references/lesson-writing-format.md`
- `references/practice-question-rules.md`

Read `references/validation-rubric.md` before final verification. Do not maintain a
second quiz schema in this skill; use the factory references whenever you need field,
type, feedback-placement, or compatibility details.

## Workflow

1. Resolve the problem source.
   - If the user gives a file path, read the relevant problem from disk.
   - Preserve the exact givens, notation, answer type, answer options, and correct answer if provided.
   - Keep the target problem atomic; do not turn a whole assignment into one lesson unless asked.

2. Resolve the lesson destination.
   - If the user gives an explicit target path, write the finalized lesson there.
   - Otherwise, create or use a `Lessons/` directory in the source file's parent directory.
   - For a numbered problem, write `Lessons/Problem-N.md`, where `N` is the source problem number.
   - If there is no problem number, use a short hyphen-case filename based on the core move.

3. Identify the core move.
   - Write one sentence beginning with a concrete action verb.
   - Name the recognition cue, the exact task, prerequisite floor, likely mistakes, and variant axes.
   - Keep the move narrower than the course topic.

4. Plan the lesson progression.
   - Use one tutorial introduction, then example sections that deepen the same move.
   - Each example section should change one local dimension: numbers, representation, direction, condition, edge case, or common trap.
   - Do not introduce a second method or downstream topic inside practice.

5. Write the lesson.
   - Use the Markdown shape from `references/lesson-writing-format.md`.
   - Put every practice item in a fenced `quiz` block.
   - Use `type: radio` for multiple-choice practice unless the task genuinely requires another supported quiz type.
   - Follow `$quiz-block-factory` for canonical fields and feedback placement.
   - Give every generated radio or checkbox option substantive corrective feedback: explain why the correct response follows, and diagnose the specific error represented by each distractor.
   - Do not leave raw checklist questions such as `- [ ] A.` in final output.

6. Validate quiz blocks.
   - Run the bundled validator on the final Markdown.
   - For normal core-move lessons, require quiz blocks, require radio practice, and require ids:

```bash
python3 /Users/jake/Developer/study/util/skills/quiz-block-factory/scripts/validate_quiz_blocks.py \
  /path/to/Lessons/Problem-N.md \
  --require-radio-practice \
  --strict-ids \
  --require-feedback \
  --lint-feedback
```

7. Fix and revalidate.
   - If validation fails, edit the lesson and rerun the validator.
   - Final response should say where the file was written and whether validation passed.

## Output Contract

A finished lesson should include:

- Title
- Table of contents
- Prerequisites
- Introduction naming the problem's core move
- 3-6 focused sections unless the task is unusually small or broad
- Worked examples with concise explanations
- Obsidian quiz-block practice immediately after the matching example section
- Substantive response-specific feedback in the canonical location for every generated practice response
- Summary that compresses the rule, cue, and main trap

The output should be practical study material, not a discussion of pedagogy or pipeline design.
