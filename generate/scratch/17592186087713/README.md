# Identifying a Matrix by Its Description

Generator: `../17592186087713.py`. Source: math basis 1356. Scope: choose the exact matching subset of three displayed matrices by ordered row/column counts. No entry arithmetic, index notation, route modeling, images or database writes.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186087713.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186087713.py --difficulty hard --seed 42 --format json
.venv/bin/python generate/scratch/17592186087713/validate.py
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Explicit arrays/target/labels and original profiles replay all source cases through ordinary parameterized rendering. Original templates require explicit parameters. Replay examples are in `source-cases.json`; field type is always radio. Invalid explicit data fail instead of being changed.

Validation independently parses **the actual displayed arrays and all choices**, verifies every solution's ordered counting stages, full source bank/prose fidelity, deterministic identity, workload guards, and the finite shape catalogs. Native fixtures exercise the real `learning::grade_field` on every correct and incorrect option. Reports retain exact versus derived denominators. `review.md`/`review.json` show all eight original parameter replays, two variants per source profile, and two examples per authored level. `artifact-hashes.json` freezes final files after validation.

Evidence limitations: two unrated sources lack correct refs/solutions, which are independently derived and authored; easy/hard are explicitly authored contextual difficulty assignments. The canonical example omits two matrices even in the authoritative capture; absent entries are not fabricated. The shape task domain is finite (12 easy, 1920 moderate, 25 hard), and numerical entries/label aliases do not inflate it.

## Current checkbox layout and inventory registration

The default generator now produces three field-owned checkbox banks, one per
matrix label, each containing exactly `false` and `true`. Explicit
`field_type='radio'` replays the retained historical radio layout. Run
`validate_checkbox.py` for the current layout and `validate.py` for historical
source-bank fidelity. Current checkbox validation checks all eight source banks,
360 seeded peer instances, deterministic identities, independently parsed
arrays and worked solutions, and the actual learner grader (1,104 accepted and
1,104 rejected checks). The two repaired legacy source prompts use `\times`
and short authored explanations; the generator preserves their historical
`\cdot` replay and labels its longer explanations as authored.

Registered generator UUID: `21139754-3f24-5ec9-9924-df6d03a89dcd`.
Repository script: `generate/scratch/17592186087713.py`.

`replenish.py` uses the existing EDB integration and application contributor
`:application/ca-engine`. It holds `.local/learning/requests/math/api.lock`
through a fresh native inventory read, basis-guarded submission and exact-basis
readback. Requests, preview, receipt, generation parameters, grading results and
verification live in `reference/replenishment/`. The verified basis-1836 → 1837
commit added five easy and five hard tasks; existing moderate inventory met the
minimum. Its inventory recheck has no remaining job for this KP.

The mathematical task catalog remains finite: 12 easy, 1,920 moderate and 25
hard shape tasks. The moderate catalog overlaps the easy and hard catalogs;
these counts are not additive. Deduplicate across all levels and against all
existing practice shapes, including unrated and already-seen source questions.
Entries, labels, array ordering, seed changes and answer-bank changes cannot
replenish an exhausted structural task. Easy and hard remain explicitly authored
contextual difficulty assignments. Exhaustion must produce a bounded finite-limit
exception with its residual shortage, rather than reusing an assessed shape.
