# Square-matrix entry generator

`../17592186100989.py` exposes generate_easy/moderate/hard and the standard generate API and CLI. It stops after steps3–7; no EDB writes, registration, shared changes or image assets.

Verify:

```sh
.venv/bin/python generate/scratch/17592186100989/validate.py
.venv/bin/python generate/scratch/17592186100989.py --difficulty all --seed 42 --count 2 --format markdown
```

Raw public replay uses `source-cases.json` and `raw_q-*` profiles, preserving all six banks and raw omissions. Raw replay is evidence-only. Normal q-13506 completion and q-125593 name repair are explicit. The opaque q-13490 historical5/4 slots have no recovered method and stay evidence-only; an authored neighboring-index bank serves its normal layout.

Missing moderate/hard are authored5x5/6x6 visual-search workloads with depth thresholds4/5; all number forms already occur at easy. These labels are design claims. Scope remains one square-matrix entry lookup. See extraction for finite meaningful-task counts excluding unrelated cells and aliases. `validation.json` records actual runtime, source fidelity, independent mathematics and actual engine checks. `review.md`/`review.json` show originals, observed-bank parameter variants and two normal examples per level.

Pre-existing `reference/`, `evidence/`, `replenish.py`, `db_support.py`, older local `check-engine*`, `native-*`, `previews.json`, `inventory-initial.json`, and `source.edn` are retained legacy artifacts, outside this frozen basis1356 rebuild. They were not run or modified. Current grading evidence is `engine-input.json`/`engine-report.json`; current replay is `source-cases.json`/`source-components.json` and `validation.json`. No legacy database-preparation workflow is part of this generator.
