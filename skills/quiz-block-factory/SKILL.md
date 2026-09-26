---
name: quiz-block-factory
description: Create, convert, repair, revise, and validate canonical fenced Obsidian quiz blocks for the local quiz-blocks plugin. Use for radio, checkbox, select, multi-select, noodle, free, or blank questions; for choosing a quiz type from a task's response shape; for adding option-specific or question-level corrective feedback; and whenever another study-vault skill generates or cleans quiz blocks.
---

# Quiz Block Factory

Build quiz blocks that are structurally accepted by the installed plugin and pedagogically useful after a student answers.

## Required references

Before creating or changing a quiz block:

1. Read [references/quiz-block-schema.md](references/quiz-block-schema.md) for the type being used.
2. Read [references/feedback-standard.md](references/feedback-standard.md) whenever the block includes feedback or belongs to generated study material.

The references distinguish plugin runtime compatibility from the stricter canonical authoring format. Always emit the canonical format.

## Workflow

1. Preserve the source task.
   - Keep givens, notation, units, diagrams, response instructions, supplied options, and known answer keys.
   - Do not infer correctness from option order or from an unsupported guess.

2. Select the type from the response shape.
   - `radio`: exactly one correct fixed option.
   - `checkbox`: multiple independently correct fixed options.
   - `select`: several prompts sharing one option bank.
   - `multi-select`: several prompts with separate option banks.
   - `noodle`: one-to-one matching.
   - `free`: a drawing, derivation, proof, explanation, or other open response.
   - `blank`: one or more short determinate typed responses. Preserve the source response shape: keep distinct source answer slots distinct, and do not invent extra slots or merge them into one.

3. Build only canonical fields.
   - Use `content`, never legacy aliases such as `text`, `question`, `answer`, or `option`.
   - Preserve supplied non-null scalar numbers or booleans in `content`; the runtime converts them to display text. Keep IDs as text.
   - Use `correct_option`, never `correct`, inside select-style or noodle questions.
   - Give every block and every selectable option an explicit stable text `id`; quote an ID that looks like a number, boolean, or null value.
   - Give every grouped question an explicit stable text `id`.
   - Put `feedback` at the level where the plugin displays it: individual radio/checkbox options, individual select-style/noodle questions, or the root of `free` and `blank`.
   - Set `shuffle: true` on every `radio` block so the correct multiple-choice answer does not stay in a predictable position. Do not rely on authored option order for meaning.
   - Do not add undocumented fields. Root schemas are strict.

4. Encode correctness.
   - Mark exactly one radio option `correct: true`.
   - Mark every correct checkbox option and at least one.
   - Point each `correct_option` to an option ID in the applicable bank.
   - Put a useful reference answer in `free.correct`.
   - Put answers inside `==...==`. With exact grading enabled, use literal keyboard-enterable text; `require_exact: false` may reveal display markup without grading it.
   - For symbolic or numerical mathematics that benefits from live notation, set `input_mode: math`. Keep its hidden answers keyboard-friendly, such as `(x+3)^2-2`, `sqrt(x+1)`, or `2pi/5`; the field converts them to visual math while the learner types.
   - Display math may contain multiple live blanks on the same LaTeX row or across `\\` row breaks. Keep each `==...==` marker outside LaTeX brace groups that must remain syntactically indivisible.
   - Treat exact math grading as structural, not algebraic: equivalent but differently structured expressions need not pass. Use `require_exact: false` when the task permits many equivalent forms and should reveal rather than grade.

5. Write corrective feedback.
   - For generated radio and checkbox practice, give every option nonempty feedback.
   - For generated select, multi-select, and noodle practice, give every question item nonempty feedback; option-bank feedback is ignored by those renderers.
   - For generated free responses, include both a reference answer in `correct` and strategy or self-check guidance in root `feedback`.
   - For generated blanks, include root `feedback` that reconstructs the governing reasoning or calculation.
   - For correct answers, use physical or conceptual rule → concrete interpretation → requested symbolic or numerical conclusion.
   - For distractors, identify the exact misconception, state what the selected quantity or operation actually controls, contrast it with what controls the answer, and apply that distinction here.
   - State boundary conditions or the circumstance in which a tempting choice would be valid when useful.
   - Use the shortest explanation that fully reconstructs the reasoning. Correct feedback is usually a compact rule → interpretation → conclusion chain; do not append algebra that adds no explanatory value after the physics or concept settles the result. Let distractor feedback be longer only when diagnosis and repair require it.
   - If a supplied distractor's origin is unclear, explain the objective reason it fails without inventing a student's thought process.
   - Verify arithmetic, signs, units, precision, graphs, and physical direction independently.

6. Validate the result.

```bash
python3 /Users/jake/Developer/study/util/skills/quiz-block-factory/scripts/validate_quiz_blocks.py \
  /path/to/file.md \
  --require-radio-shuffle \
  --strict-ids \
  --require-feedback \
  --lint-feedback
```

For ordinary core-move lessons, also require radio practice:

```bash
python3 /Users/jake/Developer/study/util/skills/quiz-block-factory/scripts/validate_quiz_blocks.py \
  /path/to/Lessons/Problem-N.md \
  --require-radio-practice \
  --require-radio-shuffle \
  --strict-ids \
  --require-feedback \
  --lint-feedback
```

7. Inspect what deterministic validation cannot prove.
   - Confirm each explanation matches its exact option rather than merely repeating the correct answer.
   - Confirm natural-language intuition and symbols agree.
   - Confirm feedback remains transferable to a nearby variant.
   - Run `git diff --check` and inspect the scoped diff.

## Editing contract

When asked to revise feedback only, change only feedback fields. Prove this by comparing the original and revised files after removing feedback fields. Never change prompts, option text, IDs, correct flags, answer order, lesson prose, or navigation unless the user separately requests it.

The validator proves structure and feedback presence. It does not certify conceptual quality; use the feedback rubric and an independent content review for that judgment.
