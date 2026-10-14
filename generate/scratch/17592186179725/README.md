# Draft: scalar line integrals on 3D segments

Immutable math basis2275. Local generator only; no registration, DB transaction, engine change, or plot required. Parent independent review is pending.

```bash
.venv/bin/python generate/scratch/17592186179725/validate.py
.venv/bin/python generate/scratch/17592186179725.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186179725.py --difficulty hard --template exponential --profile source-q-123434 --seed 93
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters are integer endpoint triples `a` and `b`. Supported families are sum/quotient/radical at easy, polynomial at moderate, exponential/cosine/sine at hard. Original unrated sum/sine are explicitly assigned for API routing; faithful historical output preserves omitted rating/key/solution. `source-cases.json` supplies exact anchors and public historical profiles.

Historical complete banks have opaque intent and four invalid real integral choices. All are evidence-only, never default learning records. Normal defaults sample all seven families with separate method-derived complete banks and fixed per-level workload. See classification, four-stage extraction, fidelity map, rendered Markdown/JSON review, validator, native fixture/report and validation summary for counts and limitations.
