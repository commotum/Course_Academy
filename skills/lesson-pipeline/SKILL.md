---
name: lesson-pipeline
description: Generate all or an explicit subset of missing core-move lessons for a single Markdown assignment file by detecting problem sections, skipping existing associated lessons, and launching same-model sub-agents to run core-move-lesson, core-move-refiner, and llm-deodorizer in sequence before final validation. Use when the user wants every problem covered or when an assignment workflow such as `setup-lessons` supplies exact unmatched problem numbers that need generated fallback lessons without replacing genuine Math Academy matches.
---

# Lesson Pipeline

## Overview

Take one assignment Markdown file and create missing core-move lessons by delegating one problem per same-model worker sub-agent. In full mode, process every problem. In targeted mode, process only an explicit list of problem numbers supplied by the caller; this mode is the required fallback for problems that `setup-lessons` classified as having no equivalent Math Academy lesson.

Required local skills:

```text
/Users/jake/Developer/study/util/skills/core-move-lesson
/Users/jake/Developer/study/util/skills/core-move-refiner
/Users/jake/Developer/study/util/skills/llm-deodorizer
/Users/jake/Developer/study/util/skills/quiz-block-factory
```

## Assignment Contract

- Input must be one Markdown assignment file, such as `.../HW-1/HW-1.md`.
- Input may also include an explicit target list such as `Problems 2, 5, and 7 only`.
- Problems are normally headed `## Problem N`.
- The lesson directory is `Lessons/` next to the assignment file.
- The expected lesson for problem `N` is `Lessons/Problem-N.md`.
- A problem is considered already associated when its expected lesson file exists and is non-empty.
- Do not overwrite, delete, rename, or regenerate existing associated lesson files unless the user explicitly asks for that.
- Full mode targets every detected problem. Targeted mode targets only the supplied problem numbers, even when other problems lack `Lessons/Problem-N.md`.
- Never infer extra targets from missing `Problem-N.md` files when the caller supplied an explicit target list.

## Workflow

1. Resolve and inspect the assignment.
   - Confirm the provided path is a file.
   - Read the assignment enough to identify all `## Problem N` headings.
   - Preserve problem numbering exactly as written.
   - If no `## Problem N` headings exist, stop and ask for clarification instead of guessing.
   - If the caller supplied target problem numbers, normalize duplicates, preserve their assignment order, and verify every target corresponds to a detected heading. Stop and report any nonexistent target instead of silently substituting another problem.

Useful commands from the study repo root:

```bash
rg -n '^## Problem [0-9]+' /path/to/assignment.md
find /path/to/assignment-parent/Lessons -maxdepth 1 -type f -name 'Problem-*.md'
```

2. Determine missing lessons.
   - Set `assignment_dir` to the assignment file's parent directory.
   - Set `lesson_dir` to `assignment_dir/Lessons`.
   - Create `lesson_dir` if it does not exist.
   - In full mode, use all detected problem numbers. In targeted mode, use only the verified target problem numbers.
   - For each in-scope problem number `N`, compute `lesson_dir/Problem-N.md`.
   - Skip any expected lesson file that exists and is non-empty.
   - Treat a missing or zero-byte expected lesson file as work to do.
   - Report the assignment's total problem count, the in-scope target count, skipped count, and missing count before launching workers.
   - If no lessons are missing, do not launch sub-agents; proceed directly to the completion check.

3. Launch one worker sub-agent per missing problem.
   - If multi-agent tools are not currently exposed, use tool discovery with a query such as `multi-agent spawn subagent wait`.
   - Use `multi_agent_v1.spawn_agent` with `agent_type: "worker"`.
   - Omit the `model` field. Spawned agents inherit the parent model by default; this is the required same-model behavior.
   - Do not set `model` to a smaller or cheaper model such as mini or spark.
   - Use `fork_context: false` unless the current thread contains essential context that is not in the prompt.
   - Pass all four local skills as skill items when the tool supports structured items.
   - Give each worker ownership of exactly one expected lesson file, such as `Lessons/Problem-7.md`.
   - Tell each worker that other agents may be editing different lesson files and that it must not revert unrelated files.

Example worker prompt:

```text
Use $core-move-lesson at /Users/jake/Developer/study/util/skills/core-move-lesson, $core-move-refiner at /Users/jake/Developer/study/util/skills/core-move-refiner, $llm-deodorizer at /Users/jake/Developer/study/util/skills/llm-deodorizer, and $quiz-block-factory at /Users/jake/Developer/study/util/skills/quiz-block-factory.

Assignment file: /absolute/path/to/assignment.md
Problem number: N
Target lesson file: /absolute/path/to/Lessons/Problem-N.md

Create the missing lesson for only Problem N. First run the core-move-lesson workflow for Problem N. Next, run the core-move-refiner workflow on the lesson you created. Then run the llm-deodorizer workflow on that refined lesson: read its failure-point reference, scan before revising, perform the full semantic audit, make only warranted in-place prose edits, scan again, and review the diff. Preserve the problem's facts, numerical values, math, correct answers, quiz-block schema and IDs, links, citation targets, frontmatter, progress metadata, headings, explicit anchors, table of contents, and lesson-navigation blocks. Use quiz-block-factory as the authoritative schema and feedback standard throughout. Do not edit any other lesson file. Do not overwrite existing non-empty files. After deodorizing, validate the final quiz blocks with the quiz-block-factory validator, including strict ids, required feedback, and feedback lint, then run git diff --check for your target file. In your final response, list the target file, the main prose fixes, the before-and-after scan status, whether quiz validation passed, and any issue that prevented completion.
```

When using structured `items`, include the four skill paths explicitly:

```text
type=skill name=core-move-lesson path=/Users/jake/Developer/study/util/skills/core-move-lesson
type=skill name=core-move-refiner path=/Users/jake/Developer/study/util/skills/core-move-refiner
type=skill name=llm-deodorizer path=/Users/jake/Developer/study/util/skills/llm-deodorizer
type=skill name=quiz-block-factory path=/Users/jake/Developer/study/util/skills/quiz-block-factory
```

4. Manage concurrency.
   - Launch workers in parallel when the missing set is modest.
   - For large assignments, batch workers in manageable groups so tool limits and merge review stay practical.
   - Keep write scopes disjoint: one worker owns one `Problem-N.md`.
   - While workers run, do not locally edit the same target files.

5. Collect results and verify.
   - Wait for all worker agents to finish.
   - Close completed agents after collecting their final statuses.
   - For each worker, inspect whether its expected lesson file now exists and is non-empty.
   - Confirm each worker ran llm-deodorizer after core-move-refiner, reviewed the scanner's findings semantically, and reported its before-and-after scan status. A clean scanner result does not replace the semantic audit.
   - Run the llm-deodorizer scanner on each newly created lesson and review any remaining findings in context:

```bash
python3 /Users/jake/Developer/study/util/skills/llm-deodorizer/scripts/scan_prose.py \
  /path/to/Lessons/Problem-N.md
```

   - Run the core-move lesson quiz validator on each newly created lesson:

```bash
python3 /Users/jake/Developer/study/util/skills/quiz-block-factory/scripts/validate_quiz_blocks.py \
  /path/to/Lessons/Problem-N.md \
  --require-radio-practice \
  --strict-ids \
  --require-feedback \
  --lint-feedback
```

   - Run `git diff --check -- /path/to/Lessons/Problem-N.md` for each new lesson, or for all new files together.
   - If a worker failed or a lesson is still missing, relaunch a worker for that problem or complete that single problem locally with the same `core-move-lesson`, `core-move-refiner`, then `llm-deodorizer` sequence. After any relaunch or local fallback, repeat the post-deodorizer scanner review, strict quiz validation, and diff check before evaluating completion.

6. Completion condition.
   - Recompute the problem-to-lesson map from the assignment file.
   - In full mode, the task is not complete until every `## Problem N` has a non-empty `Lessons/Problem-N.md`.
   - In targeted mode, the task is not complete until every explicitly targeted problem has a non-empty `Lessons/Problem-N.md`. Out-of-scope problems must remain untouched and do not affect targeted completion.
   - Existing skipped lessons count toward completion, but do not silently claim they were newly generated.

## Final Response

Report:

- Assignment path.
- Number of problems found.
- Processing mode and targeted problem numbers, when applicable.
- Existing lesson files skipped.
- New lesson files created.
- Any problems that could not be completed.
- Deodorizer scan and semantic-audit status for new lessons.
- Quiz validation status for new lessons.

Keep the response focused on the pipeline outcome. Do not paste full lesson contents.
