# Shift identification generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186087822/validate.py
.venv/bin/python generate/scratch/17592186087822.py --difficulty all --seed 19 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087822.py --difficulty moderate --profile source:q-170593 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individually documented easy/moderate/hard entrypoints. Parameters use exact rational strings `b`, `c`, optional `step`. Level templates: labelled_integer, labelled_fraction, read_fraction_grid. Default bank profiles: signed_intercept, confuse_shift_stretch, intercept_offset, and (hard only) axis_reading. `source:q-N` profiles preserve complete historical banks and raw key presence as evidence-only; two originals lack correct refs and cannot be graded natively without inventing evidence.

Scope: read c from y=b^x+c and select its complete equation. Hard fractional-axis reading is authored; there is no source hard label. No unknown stretch/base, graph selection or horizontal shift. Basis1356 provenance, exact original replay, independent displayed-expression checks, exact finite task counts, renderer sidecars and real `learning::grade_field` checks are in validation.json. Review distinguishes originals from generated variants and contains each original complete bank plus changed-parameter replay and two examples per default bank per level. All artifacts are local review data; no EDB writes.

Renderer uses Matplotlib via cached read-only Python3.10 wheels when unavailable in the primary Python3.13 venv. Both runtimes' exact versions are recorded. Cache assets and fresh concurrency artifacts are kept for active reviewers; no pruning or shared environment changes.


## Replenishment deployment decision (2026-10-14)

Only easy `labelled_integer` and moderate `labelled_fraction` are supported for database replenishment. Both retain the source’s explicitly labelled asymptote and direct read. The historical draft hard `read_fraction_grid` and `axis_reading` bank remain review evidence; they are excluded from deployment because suppressing the label adds an axis-inference stage absent from the source backbone. `capabilities.json` records the hard shortage as unfilled. This decision supersedes the draft hard-support claim above.


## Verified replenishment

At math basis 2225, registered generator `1bc96f04-7c3b-5132-9c14-ab3d317e5ede` at `generate/scratch/17592186087822.py` and added one easy plus four moderate questions. Inventory was rechecked at basis 2224 while holding `api.lock`, which remained held through submission and exact receipt/readback verification. Validated distinct availability is five easy and five moderate; hard remains unsupported with shortage five. Eight source questions and the canonical example are unchanged; only additive scoped content datoms were committed through `application/ca-engine`.

Exact request, preview, receipt, grading report, assets and readback: `reference/replenishment/basis-2224/`. Plot review: `reference/visual-review.json`. Repeat transaction preparation adds no content. The source and generator snapshots and their hashes are retained.
