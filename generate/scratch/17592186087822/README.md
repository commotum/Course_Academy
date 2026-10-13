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
