# Plane polar derivatives

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124594/validate.py
.venv/bin/python generate/scratch/17592186124594/build_review.py
.venv/bin/python generate/scratch/17592186124594.py --difficulty all --seed 23 --count 2 --format markdown
```

Scope: Cartesian-given symbolic function → r/theta derivative through the two-term chain rule. Seven source families, all radio, no plots. Source cases include eight raw banks covering seven questions (one duplicated legacy field). Every missing reference is explicitly derived, not counted as matched. Default operation banks and absent moderate/hard levels are authored; exact observed banks remain profile options. See classification, extraction, review and validation.json for bounds, provenance and denominators. Source.json preserves raw basis-1356 capture. No EDB writes, registration, engine modifications or database-preparation artifacts.

The validator independently parses actual printed prompt formulas, all choices and every solution row, verifies full banks/stage order and formatting, exercises function renaming, explicit domain guards, deterministic content identity and mathematical deduplication, and invokes the shared real native grader in memory. No blank fields: no algebraic entry-equivalence claim. The output UUIDs and colon-key schema are local review records.

Replenishment entry point (uses the existing configured math EDB writer):

```sh
.venv/bin/python generate/scratch/17592186124594/replenish.py
```

It rechecks inventory before generation and under the application `api.lock`,
validates distinct mathematical tasks and actual grading, registers the stable
generator UUID and repository-relative script, then holds the lock through the
basis-guarded submission and exact-basis readback. All requests, receipts,
source-quality exclusions, provenance checks and inventory counts are saved in
`reference/replenishment/`. The dated classification appendices supersede the
original README's statement that no database-preparation artifacts exist.
The generator script and its frozen identity have not changed.
