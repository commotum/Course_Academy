# Non-pivot columns in row echelon form

Generator `generate/scratch/17592186124478.py` version 1.1.0 emits one checkbox for each displayed matrix column, named `Column 1`, `Column 2`, and so on. Every field owns text answers `false` and `true`; the correct selections are precisely the non-pivot columns. The prompt adds “Select all that apply.” once. The existing registered generator UUID and script path are retained.

Run `.venv/bin/python generate/scratch/17592186124478/validate.py` for all 16 historical source replays, all 888 profile/column mappings, 1,920 normal seeded samples, exact row-reduction checks, stable identities, malformed-output controls, and native `grade_field` checks of both owned Boolean choices. Current evidence is in `checkbox-update-2026-10-16/verification.json`, with source option mappings, coverage, native inputs/results, and readable previews beside it. Earlier top-level validation/review files describe the historical radio version.

Only easy is supported. The observed shape/rank families have one or two non-pivot columns and 40 distinct structural tasks. Neither empty nor full **correct** non-pivot subsets occurs in this scope. Empty and full learner selections are both expressible and are checked along with every other response subset. Novelty depends on shape and pivot positions; coefficients, seeds, labels, and former radio-bank profiles do not create new structural tasks.

`source.json`, `snapshot.json`, and the original evidence under `reference/` remain historical captures. Replay preserves their matrices, keys, difficulty, and solution text except for two documented singular/plural repairs: q-73618 ends in “columns” and q-73621 ends in “column.” The old duplicate unkeyed field for q-35391 is historical evidence, not an assumption about its current database state.

`replenish.py` uses the checkbox-aware validator for fresh inventory and remains a separate database-writing operation. It was not run for this generator update. No plots or new assets are required.
