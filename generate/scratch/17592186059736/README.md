# Cross-product generator

Local script: `../17592186059736.py`. Fixed database snapshot: math basis 1356. No database access or transactions; no plots.

Verify:

```sh
.venv/bin/python generate/scratch/17592186059736/validate.py
.venv/bin/python generate/scratch/17592186059736.py --difficulty all --seed 31 --count 2 --format json
```

Public API: `generate`, `generate_easy`, `generate_moderate`, `generate_hard`. Four normal templates: `tuple_radio`, `basis_radio`, `tuple_blank`, `basis_blank`. Every captured source appears in `source-cases.json` and can be replayed using its named recipe and original `observed:` profile. Public raw profiles append `:raw`; these preserve explicitly documented malformed source evidence and are never normal output.

The normal complete five-operation bank is authored. Observed full banks use explicit opaque covariance profiles, whose error intention remains unknown. Moderate and hard definitions are authored within the same determinant arithmetic and response layouts. See `classification.md` and `template-extraction.md` for curriculum boundaries and source-format repairs.

`review.md` / `review.json` show every original bank and a changed-input variant, plus two examples of each normal template at each difficulty. `validate.py` reads actual printed inputs, formal matrices, minors and every subsequent arithmetic stage using an independent recursive-descent parser, checks all complete vectors and blank fragment signs, source-stage fidelity, workload guards, collision rejection, identities and real native grading. The read-only parser dependency is `generate/runs/current/vector-math-parser.py`; generator rendering uses a separate converter. The engine fixture executes `course_academy_engine::learning::grade_field` in memory.

`freeze.json` records SHA-256 hashes of final artifacts, plus the read-only native grader/parser and exact dependency versions. Raw source evidence remains unchanged. Work stops at generator creation and verification.

Supplemental `raw-engine-input.json` / `raw-engine-report.json` verify all six original raw components in q-281976/977: the native grader accepts the exact original single-slash TeX scalar values. Serialized JSON escaping is not a source anomaly.
