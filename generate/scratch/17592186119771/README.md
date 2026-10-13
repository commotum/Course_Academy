# Describing a Triangular Matrix

Current scratch generator: `../17592186119771.py`, database math basis **1356**. All three entrypoints are implemented: observed 2×2/3×3 easy strict upper/lower, observed 3×3 moderate nonidentity diagonal, and explicitly authored 4×4 hard instances of the same classification method. There are no matrix operations, database calls, registration or writes in this work.

```sh
.venv/bin/python generate/scratch/17592186119771/validate.py
.venv/bin/python generate/scratch/17592186119771.py --difficulty all --count 2 --seed 42 --format markdown
.venv/bin/python generate/scratch/17592186119771.py --difficulty easy --profile raw:q-13769 --parameters '{"matrix":[[3,0,0],[6,8,0],[4,5,1]],"letter":"A","layout":"bmatrix"}'
```

`generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` accepts family lower/upper/diagonal and radio fields. `five-labels` is the normal complete bank. `raw:q-N` is public parameterized evidence replay, preserving source duplicate fields and omissions; it requires explicit parameters and is marked evidence-only/ineligible. `source:q-N` completes the same source recipe for normal practice. Raw enum maps/correct objects are converted to the established enum-string/owned-lookup-ref representation, with capture attributes retained. `source-cases.json` records exact replay arguments.

Validation passes 10 raw question replays, 11 full original banks / 55 values, all nine original solutions and all nine present correct designations. Source-format repairs are separate: q-13759 has one intended widget but two captured fields; q-13769 lacks a key, solution and rating. Native grading tests every choice in all 164 finite catalog tasks, nine keyed source-bank fixtures and ten completed source banks: **183 accepted, 732 rejected, zero unresolved**. The two raw unkeyed fields cannot be native graded as captured; no designation is fabricated in those public raw records. Both completed normal source questions grade correctly.

Meaningful finite catalog: **16 easy / 7 moderate / 141 hard**. Strict fingerprints ignore every diagonal value and all nonzero magnitudes/signs; diagonal fingerprints retain unit/nonunit positions for the identity distinction. Numerical changes only vary presentation. Normal prompts explicitly define most-specific listed description; square zero matrices count as diagonal in this bank, and normal families exclude Identity/Other as correct answers. Hard is an authored six-cell triangular or twelve-cell diagonal scan, justified by the tutorial's square-matrix definition and prerequisite MA862, not a recovered source rating.

`review.md`/`review.json` show all original public raw records and changed source-family variants, plus four normal examples per level. `classification.md`, `template-extraction.md`, `plot-extraction.md` record source mapping, definitions, level rationale and inspected canonical rasters. `validation.json` records runtime versions, hashes, fidelity denominators and limitations.

Historical files under `reference/replenishment`, `reference/inventory-initial.json`, and the pre-existing `replenish.py` belong to an earlier workflow and are **not current validation or authorized execution instructions**. They were not executed or modified by this basis-1356 generator task. Current work stops after steps 3–7; do not run the legacy replenishment script.
