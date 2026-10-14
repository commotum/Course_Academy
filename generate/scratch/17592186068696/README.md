# Identifying Points of Discontinuity — scratch generator

This private draft implements easy, moderate and hard graphical recognition only. All 17 frozen originals and all complete banks replay through public `observed:q-ID` profiles. Moderate/hard labels are authored; source omissions and malformed legacy values are preserved as ineligible raw evidence.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186068696/validate.py
.venv/bin/python generate/scratch/17592186068696.py --difficulty all --seed 3 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186068696.py --difficulty easy --profile observed:q-48080 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`; individual easy/moderate/hard entry points expose the same keyword parameters. Easy parameters are `scale` (1 or 2), `shift` (integer -3…3), optional unit `grid`. Moderate/hard require three `coordinates` and `orientation` ±1, with guarded workload bounds documented in extraction. Explicit invalid inputs fail without silent resampling.

`validation.json` distinguishes source fidelity, independent displayed-coordinate/graph/raster checks and the real `course_academy_engine::learning::grade_field` native checks. `review.md` and `review.json` show every original bank beside parameterized observed evidence and normal variants, plus two authored examples for each absent level. `source.json` is the unmodified frozen wrapper. `source-bank-map.json`, `source-cases.json` and `plot-spec.json` expose all mappings. No database, registry, shared engine or transaction files were edited. Parent QA remains required; root approval is not claimed.

Parent QA correction: version `graph-discontinuity-2-zero-axes` includes the actual origin in every generated viewport. `zero-axes-review.json` contains all source-family boundary cases at scale2/shift±3, with PNG sidecars and actual raster origin checks. Old assets are retained; no fallback origin is used.
