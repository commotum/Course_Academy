# Diagram-based Cartesian coordinate generator

Implementation: ../17592186092273.py. Local review data only; steps 3–7, no database operations.

```sh
.venv/bin/python generate/scratch/17592186092273/validate.py
.venv/bin/python generate/scratch/17592186092273.py --difficulty all --seed 3 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186092273.py --difficulty hard --profile observed-q-120593 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Parameters have exactly radius (SymPy string), alpha/delta (integer degrees), direction (±1), units (degree/radian). Field types are radio or two ordered blank fields. Source masks have fixed original field layouts. Normal bank profile authored-method is eligible for learning; observed-q-* profiles preserve complete original banks and absent source attributes and are explicitly evidence-only. Their angle family is fixed, radius scaling is parameterized, and their wrong-option intent is unresolved. Original bank strings and correct-reference presence are replayed exactly, with generated UUID ownership.

classification.md documents authored easy/moderate and harder default bounds. template-extraction.md includes all four extraction stages and every source bank recipe. plot-extraction.md, source-geometry.json and canonical-geometry.json describe every diagram. The eleven files under images/ are byte-identical source copies so original relative references render in the review. review.md/review.json include originals, each scaled opaque-bank evidence variant, each normal source-family variant, and six extra variants per level. validation.json separates exact source fidelity, native grading, displayed mathematics, finite-domain variety and measured raster checks. Two absent source correct references are inferred only in normal authored completion; two absent source solutions/ratings stay absent publicly in observed replay.
