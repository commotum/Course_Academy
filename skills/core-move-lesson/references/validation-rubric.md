# Validation Rubric

Use this before final response.

## Lesson Quality

- The lesson teaches one core move.
- Unless the user provided an explicit target path, the finalized lesson is written under `Lessons/` next to the source file.
- The recognition cue is visible early.
- Prerequisites are minimal.
- The first example is canonical.
- Each later section changes one wrinkle.
- Practice is attached to the relevant section.
- Summary gives a reusable procedure.

## Quiz-Block Quality

- Every practice item is inside a fenced `quiz` block.
- No raw checklist MCQ remains, such as `- [ ] A.`.
- Normal multiple-choice practice uses `type: radio`.
- Every radio block has exactly one `correct: true`.
- Every generated quiz block has an `id`.
- Every generated radio option has an `id`.
- Distractors represent real mistakes.
- Every generated radio and checkbox option has nonempty feedback.
- Correct feedback states the governing idea, applies it to this prompt, and reaches
  the requested conclusion.
- Each distractor's feedback repairs the specific misconception encoded by that
  response instead of repeating generic rejection or the same solution.
- Feedback uses the canonical location defined by `$quiz-block-factory` for the quiz
  type.

## Required Command

For ordinary generated lessons, run:

```bash
python3 /Users/jake/Developer/study/util/skills/quiz-block-factory/scripts/validate_quiz_blocks.py \
  /path/to/lesson.md \
  --require-radio-practice \
  --strict-ids \
  --require-feedback \
  --lint-feedback
```

Fix every error before reporting completion. Then inspect feedback manually: the
validator can prove presence and flag shallow patterns, but it cannot prove physical,
mathematical, or misconception-level correctness.

## Optional Math Academy Comparison

When the user asks for refinement, compare against 3-4 random files from `/Users/jake/Developer/MA/DATA/Lessons/*/*.md` and look for:

- table of contents and prerequisites
- example/explanation/question loops
- section-level practice
- controlled progression
- representation/image use
- concise worked-example language

Incorporate structural improvements, not topic-specific content.
