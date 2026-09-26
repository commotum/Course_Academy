---
name: setup-lessons
description: Populate an assignment skeleton's local Lessons, Prerequisites, and Source folders from verified Math Academy matches, then generate targeted core-move lessons for problems with no genuine Math Academy equivalent. Use when the user provides a study-vault assignment markdown file with many `## Problem N` sections and wants Codex to match each problem, copy verified MA lessons and prerequisites without duplicates, route unmatched problems through `lesson-pipeline`, normalize local names and metadata, and refresh course-level progress indices.
---

# Setup Lessons

## Overview

Use this skill to set up lesson context for an assignment markdown file. Process one problem at a time, use `match-ma-lesson` for the judgment step, copy genuine Math Academy matches with the bundled helper, and run `lesson-pipeline` only for the explicitly unmatched problem numbers. This preserves real MA lessons while ensuring every problem still receives focused lesson coverage.

## Workflow

1. Resolve the assignment markdown file.
   - Work from `/Users/jake/Developer/study` unless the user provides an absolute path.
   - Confirm the file has sibling `Lessons`, `Prerequisites`, and `Source` folders. Create missing folders only if the assignment skeleton is otherwise clearly valid.
   - Inspect the top `## Lessons` and `## Prerequisites` sections before edits.

2. Split the assignment into individual problems.
   - Use the bundled script to list problem blocks:

```bash
python3 util/skills/setup-lessons/scripts/list_problems.py vault/252/M1/WHW-1/2026-07-06-WHW-1.md
```

   - For a targeted pass, print one problem:

```bash
python3 util/skills/setup-lessons/scripts/list_problems.py vault/252/M1/WHW-1/2026-07-06-WHW-1.md --problem 1
```

3. Match lessons one problem at a time.
   - For each `## Problem N` block, use the `match-ma-lesson` skill workflow.
   - If `match-ma-lesson` has not already been loaded in the current turn, read `/Users/jake/Developer/study/util/skills/match-ma-lesson/SKILL.md` and follow it.
   - Keep the per-problem result explicit: main lessons go to `Lessons`; prerequisite or supporting background goes to `Prerequisites`.
   - Require the matcher to return one status per problem: `Equivalent Math Academy lesson found` or `No equivalent Math Academy lesson`.
   - Maintain two explicit lists while processing: `matched_problem_numbers` and `unmatched_problem_numbers`. Every problem number must appear in exactly one list.
   - Put a problem in `matched_problem_numbers` only when a verified lesson question/example teaches the same core move and task shape. Prerequisites, near misses, shared vocabulary, or a broadly related lesson do not count as an equivalent.
   - Put a problem in `unmatched_problem_numbers` when no genuine equivalent exists. Supporting MA prerequisites may still be copied, but do not promote them to a main match merely to avoid the fallback.
   - Prefer original Math Academy `md-path` values from `util/Mathematical-Foundations/topics.csv`; these let the helper find the matching `src-path`.
   - Do not manually chase prerequisite chains. The copy helper adds direct prerequisites from `util/Mathematical-Foundations/prerequisites.csv` and stops there.

4. Copy each matched lesson and its source folder locally.
   - Use the helper instead of manual `cp` when possible.
   - Run helper invocations sequentially for the same assignment file because each run rewrites `Source/topics.csv` and the assignment's top links.
   - Pass `--kind lesson` for main lesson matches and `--kind prerequisite` for prerequisite matches.
   - Repeat `--lesson-md` for multiple lessons of the same kind.
   - The helper copies the lesson `.md`, copies its indexed source folder into the assignment `Source` folder, copies each explicit lesson's direct prerequisites into `Prerequisites`, records every copied topic in `Source/topics.csv`, skips existing files/folders, removes skeleton placeholder links, and rewrites local markdown links in sorted layer order.
   - Local lesson markdown files and copied source folders are canonicalized as `Topic Name - TOPIC-ID.md` and `Source/Topic Name - TOPIC-ID`. Existing local copies with older names are renamed instead of duplicated.
   - After each run, the helper refreshes the course-level `topics.csv`, `prerequisites.csv`, `0. Table of Contents/TOC.md`, and `Home.md`, and ensures the course is configured in `obsidian-update-progress` with `queuePrerequisiteScope: "course"`.

```bash
python3 util/skills/setup-lessons/scripts/copy_ma_lesson.py \
  vault/252/M1/WHW-1/2026-07-06-WHW-1.md \
  --kind lesson \
  --lesson-md 'vault/MA/Mathematical-Foundations/MF3/9. Definite Integrals/9.1. Approximating Areas with Riemann Sums/Lessons/9.1.2. Approximating Areas With the Right Riemann Sum.md'
```

```bash
python3 util/skills/setup-lessons/scripts/copy_ma_lesson.py \
  vault/252/M1/WHW-1/2026-07-06-WHW-1.md \
  --kind prerequisite \
  --lesson-md 'vault/MA/Mathematical-Foundations/MF2/9. Trigonometry/9.4. Special Trigonometric Ratios/Lessons/9.4.3. Finding Trigonometric Ratios of Special Angles Using the Unit Circle.md'
```

5. Generate targeted lessons for unmatched problems.
   - After all Math Academy copy-helper invocations finish, inspect `unmatched_problem_numbers`.
   - Unless the user explicitly requested an MA-only pass, read and invoke `/Users/jake/Developer/study/util/skills/lesson-pipeline/SKILL.md` in targeted mode with the assignment path and the exact unmatched problem numbers.
   - Do not invoke the pipeline's full-assignment mode from this workflow. Math Academy lesson files use topic-title filenames rather than `Problem-N.md`, so full mode would incorrectly generate replacements for matched problems.
   - Targeted mode must create or reuse only `Lessons/Problem-N.md` for numbers in `unmatched_problem_numbers`. It must not create, overwrite, rename, or refine files for `matched_problem_numbers`.
   - A pre-existing non-empty `Lessons/Problem-N.md` satisfies the fallback for that unmatched problem and must be skipped unless the user explicitly asks to regenerate it.
   - If the user requested MA-only matching, report unmatched problem numbers without generating fallback lessons.

6. Avoid duplicates.
   - Do not copy the same lesson markdown twice.
   - Do not copy the same source folder twice.
   - Do not add duplicate top links to the assignment markdown.
   - Do not add duplicate `topic-id` rows to `Source/topics.csv`; if a topic is later selected as a core lesson, let its role upgrade from `prerequisite` to `lesson`.
   - If the same lesson is matched by several problems, record it once and mention the repeated coverage in the final summary if useful.

7. Refresh or normalize without copying when needed.
   - Use `--refresh-only` to normalize existing local filenames/source folders and rebuild the assignment/course indices without adding a new lesson:

```bash
python3 util/skills/setup-lessons/scripts/copy_ma_lesson.py \
  vault/252/M1/WHW-1/2026-07-06-WHW-1.md \
  --refresh-only
```

8. Verify the local setup.
   - Inspect the top of the assignment markdown and confirm links point to local `Lessons/...` and `Prerequisites/...` paths.
   - Confirm `Source/topics.csv` exists and includes all copied topic IDs.
   - Confirm top-section links are sorted separately within `## Prerequisites` and `## Lessons` by the `layer` values from the original Math Academy `topics.csv`.
   - Confirm the course-level `topics.csv`, `prerequisites.csv`, TOC, and Home page have been refreshed under the course folder, for example `vault/252/topics.csv` and `vault/252/0. Table of Contents/TOC.md`.
   - List copied files:

```bash
find vault/252/M1/WHW-1/Lessons vault/252/M1/WHW-1/Prerequisites -maxdepth 1 -type f -name '*.md' -print | sort
find vault/252/M1/WHW-1/Source -maxdepth 2 -type d -print | sort
cat vault/252/M1/WHW-1/Source/topics.csv
```

   - Spot-check that copied lesson image links such as `../Source/<lesson>/Images/...` resolve under the assignment folder.
   - Confirm every problem classified as matched has its selected MA lesson copied locally.
   - Confirm every problem classified as unmatched has a non-empty `Lessons/Problem-N.md`, unless the user explicitly requested an MA-only pass.
   - Use the validation results required by `lesson-pipeline` for every newly generated fallback lesson.

## Reporting

Keep the final response concise:

- State the assignment file processed.
- List the copied `Lessons` and `Prerequisites`.
- List problem numbers covered by equivalent Math Academy lessons.
- List problem numbers handled by generated core-move fallback lessons.
- Mention direct prerequisites added and duplicates skipped.
- Mention any problem that still lacks coverage and why.

Do not rewrite the assignment problems unless the user explicitly asks.
