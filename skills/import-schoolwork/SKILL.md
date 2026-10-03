---
name: import-schoolwork
description: Import school assignments from study-vault Markdown into Course Academy's EDB database and Assignments page, preserving original problems, shared context, diagrams, deadlines, and verified topic mappings. Use for adding schoolwork to the application; use the existing matching or lesson-generation skills separately when coverage needs investigation or new lessons.
---

# Import schoolwork

Work from the Course Academy repository. Read the assignment completely, its source PDF or problem source when available, and any accompanying `Math Academy Matches.md`. The original assignment is the content to import; linked Math Academy lessons remain shared database content.

## Content model

Use the current files in `schema/content` and `schema/learner` as the authority:

- `learner/assignments` references assignment activities.
- An `activity.type/assignment` owns ordered steps through `activity/steps`, `activity/first-step`, and `step/next`.
- A problem step references an `assigned-problem`. Its `topic-coverage` holds verified preparation topics; its `content` references a question or a multistep problem.
- A multistep retains shared setup and diagrams in `multistep/context`, with its own ordered steps for the parts. Preserve subpart labels and givens. Do not move a diagram out of a particular part unless it actually applies to the shared problem.
- Assignment instructions and original source links can occupy an introductory tutorial step. Strip vault navigation and matching commentary from the actual prompts.

Do not turn proofs, sketches, or unkeyed school problems into multiple-choice practice merely to satisfy the grader. They can be ordinary fieldless questions displayed through assigned-problem. Such prompts cannot be automatically graded or award mastery. Preserve existing answer fields, correct answers, and feedback when a source actually supplies them; the current plain-Markdown importer deliberately rejects quiz blocks until a reviewed conversion is added.

`activity/due` is already an optional instant. Worksheet dates, import dates, and week-folder names are not deadlines. Leave it absent without evidence or a user-provided deadline. For an explicit date with no time, the helper uses the end of that day in America/Los_Angeles; disclose that convention. Never replace the learner's current course to import schoolwork.

## Coverage

Prefer verified per-problem mappings in the source's match report. Do not attach the entire assignment's Lessons or Prerequisites list to every problem. Derive prerequisite traversal from `topic/next`; do not copy prerequisite edges into the assignment.

Keep direct, partial, and supporting-only judgments explicit in the import manifest. `topic-coverage` means preparation for the problem, not proof that every part has an equivalent lesson. If mappings are absent, leave them empty or investigate with the sibling `match-ma-lesson` skill. Do not automatically invoke `setup-lessons` or `lesson-pipeline`: they write vault copies or generated lessons and are separate work.

## Prepare and import

`scripts/import_school_assignments.py` is a nonmutating builder tested on the four F26 week-one assignments. It supports Markdown headed `## Problem N`, with optional `**(a)**` subparts, images, source links, and instructions. Its default manifest is those four reviewed assignments. For another assignment, supply a reviewed JSON array using `--manifest`:

```json
[
  {
    "path": "F26/256/W2/HW-2/HW-2.md",
    "problems": {
      "1": {
        "direct": [877],
        "supporting": [],
        "coverage": "direct",
        "note": "Verified integrating-factor problem."
      }
    }
  }
]
```

Paths are relative to the study vault. Topic numbers are verified Math Academy topic IDs, resolved against existing database topics. Do not invent IDs for new curriculum. Use stable source paths and problem/part labels; changing these changes the derived UUIDs and requires identity reconciliation.

Set `shared_images: true` on a reviewed problem mapping only when all its diagrams apply to every subpart; this moves trailing diagrams into the multistep's shared context. Otherwise the importer preserves their original positions.

1. Capture a current `EntitySnapshot` using the native learning helper's local `export-test-snapshot` action (`LEARNING_SNAPSHOT_PATH` sets its output), as supported by `scripts/learning_api.rs`. Keep this large private snapshot under `.local`, not in the skill or git. Confirm the learner and database explicitly from the running app configuration.
2. Run the builder with that snapshot:

   ```bash
   python3 scripts/import_school_assignments.py \
     --snapshot .local/edb/school-assignments/before.json \
     --manifest /tmp/reviewed-assignments.json \
     --output .local/edb/school-assignments
   ```

   Optional `--due-dates` accepts a JSON object from vault-relative paths to ISO dates or timestamps with timezones. The builder writes `assignments.edn`, `entities.json`, and `audit.json`. It preserves unrelated existing data, emits nothing for unchanged imported facts, and refuses changed managed content that needs a reviewed reconciliation.
3. Check every problem and part against the source, resolve all assets, render the LaTeX, and inspect partial mappings. The helper's regex parser does not replace this source comparison. For unfamiliar formatting, adapt the conversion or prepare explicit entities rather than silently dropping content.
4. Preview the EDN with EDB `with`, then transact the requested import through the configured durable writer with a stable request key and the reviewed database basis. An import request authorizes this step; do not introduce another approval checkpoint. If a write response is uncertain, inspect/replay the same request instead of generating a new request key.
5. Read `/api/assignments` and each `/api/assignment?assignment=UUID`. Confirm counts, order, math, diagrams, source links, and preparation-topic refs. Viewing is read-only. Rebuild against a fresh snapshot and expect zero forms for an unchanged reimport.

The Assignments page is separate from Study. It sorts real deadlines first and undated work last. In self-directed mode the Study planner already consumes assignment topic coverage and deadlines; reconcile the existing queue after importing. Do not manufacture completed work, XP, correctness, or progress just because an assignment was imported or viewed.

Report what was imported, unavailable deadlines, and meaningful coverage gaps. A reusable prompt is: “Import this school assignment into Course Academy, preserving its problems and existing verified topic matches: [path]. Its deadline is [date/time, if known].”
