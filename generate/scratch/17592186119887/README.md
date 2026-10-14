# Fundamental vector product draft

Local generator and evidence at math basis 2275. No registration/database writes. Awaiting parent independent review; this is not approval.

Run:

```bash
.venv/bin/python generate/scratch/17592186119887/validate.py
.venv/bin/python generate/scratch/17592186119887.py --difficulty all --seed 3 --count 2 --format json
.venv/bin/python generate/scratch/17592186119887.py --difficulty easy --template q-105606 --profile observed:q-105606 --parameters '{"a":1,"b":1,"c":1}'
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus easy/moderate/hard entrypoints. `TEMPLATES` exposes all observed shapes and authored level aliases. Source-cases use raw `observed:<source-id>` complete profiles; these preserve raw missing keys/labels/solutions and duplicated fields, and are ineligible for learning. Normal defaults use a complete method bank and one supported field; existing norm family remains an expression blank with supplied prior product.

Review contains all originals, all changed raw banks, all normal easy families, and two boundary examples for every moderate/hard family. Classification and extraction document original bank opacity, repaired layout, bounds, arithmetic-only authored labels, exact source provenance and unknown calculator policy. `source-components.json` lists every field/option recipe. `validation.json` separates fidelity, math, native grading, capacity and unresolved interpretation/provenance limits.
