---
name: lesson-cleanup
description: Clean and normalize study-vault homework, practice-quiz, assignment, and daily lecture-quiz Markdown after questions or screenshots have been added. Use when an assignment skeleton or lecture PRE/LEC source note contains rough text; images need canonical placement, semantic names, deduplication, or reuse; multipart questions need structure; raw questions need an Obsidian quiz type selected; numerical answers need significant-figure verification; or a dated lecture note should compose canonical PRE and LEC notes without duplicating their quiz content.
---

# Lesson Cleanup

Polish one study document in place without changing its academic substance. Normalize its Markdown, choose quiz types by task shape, verify numerical precision, and make its document-owned image set canonical and minimal.

## Required references

Before editing any quiz block, invoke `$quiz-block-factory` and read its complete `SKILL.md` plus both required references. Quiz Block Factory is authoritative for supported quiz types, canonical fields, correctness encoding, feedback placement and quality, and quiz validation.

Then read [references/cleanup-standard.md](references/cleanup-standard.md) for cleanup-specific policy: source fidelity, Markdown layout, multipart structure, images, typed-input conventions, and significant figures. Do not duplicate or override Quiz Block Factory's representation rules here.

## Workflow

1. Resolve the document kind.
   - Accept a Markdown file or its containing folder.
   - Treat homework, practice quizzes, and similar folders as assignments when the root Markdown owns `## Problem N` sections and sibling `Lessons`, `Prerequisites`, or `Source/<assignment-name>/Images`.
   - Treat a dated folder such as `2026-06-24-M1-1` as a daily lecture folder when its `Source` directory contains `<module-code>-PRE.md` or `<module-code>-LEC.md`.
   - In a daily lecture folder, make PRE and LEC notes canonical and make the dated root note a composition of those sources.
   - If more than one plausible target exists and the document kind is unclear, stop and ask.

2. Establish fidelity and scope before editing.
   - Read every target Markdown file completely.
   - For assignments, count and map every `## Problem N` section and multipart prompt.
   - For daily lectures, count quiz blocks separately in PRE and LEC, and confirm the root note contains no unique quiz content before replacing duplication with embeds.
   - Inspect one or two already-cleaned assignments in the same course when available.
   - Preserve problem order, givens, variables, units, answer choices, known correct answers, and shared source context.
   - For every numerical answer, record the precision of the givens, whether any quantities are exact, and whether the source specifies a rounding rule or tolerance.
   - Do not silently remove a repeated answer choice merely because its text is duplicated. If the source genuinely contains it, preserve it and report any resulting ambiguity.
   - Do not run lesson-generation or lesson-matching workflows. Preserve the contents of `Lessons`, `Prerequisites`, transcripts, lecture notes, and unrelated source folders.

3. Audit images before moving anything.

```bash
uv run --with pillow python util/skills/lesson-cleanup/scripts/audit_images.py path/to/Assignment.md
```

   - Review every referenced, missing, loose, unreferenced, exact-duplicate, decoded-pixel-duplicate, and visually similar candidate reported.
   - If `uv` or Pillow is unavailable, run the script with `python3`; exact-file checks still work, but manually inspect visual-duplicate candidates.
   - Visually inspect uncertain duplicate candidates.
   - For assignments, treat `Source/<assignment-name>/Images` and loose assignment images as cleanup scope.
   - For daily lectures, treat the shared `Source/Images` folder and loose PRE/LEC images as cleanup scope.
   - Treat `Source/<other-topic>/...`, `Lessons/...`, and `Prerequisites/...` as protected.

4. Canonicalize document images.
   - Move assignment images to `Source/<assignment-name>/Images`.
   - Move daily lecture PRE/LEC images to the lecture folder's shared `Source/Images` directory and reference them as `Images/<name>` from source notes.
   - Use concise, descriptive, lowercase kebab-case filenames such as `simple-harmonic-motion-position-time-graph.png`.
   - Prefer content-based names over upload names, hashes, dates, or `image-1`.
   - Keep one file when multiple questions use the same source image and point every relevant question to that file.
   - Preserve distinct crops, annotations, diagrams, or resolutions when they convey different information.
   - Never overwrite a different existing file. Compare first, choose a distinct semantic name if needed, and update references.
   - Delete a redundant file only after confirming equivalence and confirming that all references use the retained file.

5. Normalize assignment Markdown.
   - Begin every Markdown file created or modified in the cleanup scope with exactly one empty line, so substantive content starts on line 2. Collapse multiple leading empty lines to one. Represent an otherwise empty placeholder `.md` file as a single newline.
   - Preserve real `## Prerequisites` and `## Lessons` links and preserve skeleton placeholders in those two sections until the lesson-setup workflow replaces them.
   - Remove skeleton prompt text and raw answer scaffolding from problem sections once real content exists.
   - Do not add an H1 that merely repeats the Markdown filename; Obsidian already displays the note title.
   - Use `## Problem N` as the section anchor.
   - For a single quiz block, place `**Question N**` as the first line of the block's `content` instead of repeating it above the block.
   - For multipart work, label each block inside `content` with `**Question N — Part A**`, `**Part A**`, or another concise part label.
   - Separate problem sections consistently with `---`.
   - Put a single-question image inside that quiz block's `content`, after the stem and before options.
   - Put shared multipart context and its image once before the part-specific quiz blocks.
   - Keep equations, symbols, variables, and units in LaTeX. Repair obvious OCR spacing and line-break damage without changing meaning.

6. Normalize daily lecture Markdown.
   - Apply the same exactly-one-leading-empty-line rule to PRE, LEC, and composed dated root notes.
   - Remove H1 headings that repeat PRE, LEC, or dated filenames.
   - Do not use `## Problem N` in PRE or LEC notes.
   - For a single-step source question, begin quiz `content` with `**Question N**`.
   - For multipart source questions, use `## Question N` once for shared context and label the blocks inside `content` with `**Part A**`, `**Part B**`, and so on.
   - Separate source quiz blocks consistently with `---`.
   - Replace duplicated root-note quiz content with source-note embeds:

```markdown

## Pre-Lecture Quiz

![[Source/M1-1-PRE]]

## Lecture Quiz

![[Source/M1-1-LEC]]
```

   - Omit a PRE or LEC section when that source file is missing or empty.
   - For the established simple source-note shape, use the bundled normalizer in preview mode first, then write:

```bash
python3 util/skills/lesson-cleanup/scripts/normalize_lecture_folder.py path/to/dated-lecture-folder
python3 util/skills/lesson-cleanup/scripts/normalize_lecture_folder.py path/to/dated-lecture-folder --write
```

7. Choose and build quiz blocks.
   - Follow `$quiz-block-factory` for type selection, canonical fields, IDs, correctness encoding, and feedback placement. Any type documented there is allowed.
   - Within cleanup scope, prefer document-wide block IDs such as `q-1`, `q-2`, and multipart forms such as `q-4a` while satisfying the factory's stable-ID requirements.
   - Set `shuffle: true` only for `radio` or `checkbox` choices whose order carries no meaning.
   - Encode correctness only when the answer key is established from the source or reliable local context. Do not infer correctness from option order, prior shuffle order, or a plausible guess. Do not expose the answer in prose immediately before a graded choice.
   - When the answer key is known, apply the factory's corrective-feedback standard at the renderer-supported level. In particular, every `radio` or `checkbox` option needs option-specific feedback; select-style and noodle items need question-level feedback; and `free` or `blank` uses root feedback.
   - For supplied distractors, diagnose a misconception only when the option itself or source context supports that diagnosis. Otherwise explain the option's objective failure, state the governing distinction, and apply it here without inventing a student's psychology.
   - If the answer key is genuinely unknown, preserve the prompt and choices without invented correct flags, explanations, or distractor psychology. Run structural validation anyway, leave any resulting correctness failure visible, and report the unknown-key exception explicitly rather than claiming the block is complete.
   - Create separate blocks only for parts that require independently answerable responses.
   - If a prompt has one answerable result plus a required supporting drawing, derivation, or explanation, keep one block using the answerable result's type and include the supporting-work requirements in its feedback or reference answer.
   - Use `free` when the drawing, proof, or explanation is itself the answerable response; provide a useful reference answer.
   - Use `blank` for short determinate values, expressions, labels, or multipart calculation results.
   - Make every answer inside `==...==` the literal plain-text response a student can type on a standard keyboard. Never put Markdown, `$...$`, LaTeX commands, equation labels, or decorative mathematical formatting inside an answer marker.
   - Set `require_exact: true` when an authoritative answer and one canonical keyboard-enterable response are known. Use `require_exact: false` only when the block is intentionally reveal-only or legitimately equivalent responses cannot be represented by one exact string.
   - Keep units outside the answer marker when the prompt asks for a number only. Put polished notation, units, equations, and significant-figure explanations in surrounding prose or `feedback`.
   - Check every calculated numerical answer for significant figures using the policy in `references/cleanup-standard.md`. Keep guard digits through intermediate work and round only the displayed final result.

8. Verify the result.
   - Re-run the image audit and confirm every assignment image reference resolves.
   - Confirm every expected problem, source question, and subpart remains present.
   - Recalculate or independently check every numerical answer, confirm its units, and confirm its final significant figures follow the supplied givens or explicit source instruction.
   - Inspect every `blank` answer marker and confirm it contains only the intended keyboard-enterable response, with no `$`, LaTeX command, variable label, appended unit, or explanatory text unless that literal text is explicitly required from the student.
   - For daily lectures, confirm PRE and LEC retain their original quiz-block counts and the root note embeds each non-empty source exactly once.
   - Confirm reused diagrams point to one canonical file and no verified redundant files remain.
   - Validate all quiz types without forcing radio:

```bash
python3 util/skills/quiz-block-factory/scripts/validate_quiz_blocks.py \
  path/to/Assignment.md \
  --strict-ids
```

   - Require and lint feedback for every block whose answer key is known. When all keys in the document are known, this command must pass:

```bash
python3 util/skills/quiz-block-factory/scripts/validate_quiz_blocks.py \
  path/to/Assignment.md \
  --strict-ids \
  --require-feedback \
  --lint-feedback
```

   - For a mixed document, run the feedback command after completing all known-key feedback and report failures confined to genuinely unknown-key blocks as explicit exceptions; do not weaken feedback on the known-key blocks. If every key is unknown, do not use feedback requirements to pressure a guess. In all cases, report every unresolved structural-validation issue, including a missing canonical correctness marker.

   - Scan for raw checklist MCQs, unfinished skeleton text inside problem sections, duplicate quiz IDs, and trailing whitespace.
   - Confirm every Markdown file created or modified in scope starts with exactly one empty line, including otherwise empty placeholders.
   - Run `git diff --check` and inspect the scoped diff.

## Safety

- Work only inside the requested document or lecture folder.
- Never delete based only on a similar filename.
- Never alter protected lesson-source images to deduplicate an assignment image.
- Never invent missing questions, choices, diagrams, or answer keys.
- If answer correctness cannot be established from the supplied material or reliable local context, preserve the content, omit unsupported correctness claims, and report the uncertainty and any consequent validation failure explicitly.

## Reporting

Report the documents processed, quiz types used, images moved or renamed, duplicates removed or reused, root-note embeds created, significant-figure corrections or unresolved precision ambiguities, feedback validation, and structural validation results. Name any unknown-key exception and its unresolved validator issue. Keep the report concise.
