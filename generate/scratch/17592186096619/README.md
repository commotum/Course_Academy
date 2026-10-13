# Product-rule slope generator

Scope: KP17592186096619, math basis 1356; stops after steps 3–7. No database transactions, registration, commits or plot assets.

Run the full independent validation and real learner grader:

```bash
.venv/bin/python generate/scratch/17592186096619/validate.py
```

Preview all levels:

```bash
.venv/bin/python generate/scratch/17592186096619.py --difficulty all --seed 42 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual easy/moderate/hard entrypoints. Templates/profiles and exact original parameter maps are in source-cases.json. `observed` and `observed_raw` are explicit replay profiles; normal radio defaults use one whole authored operation bank. JSON is local review data, not transaction EDN.

13 source cases, 12 observed banks (36 values/24 radio distractors), 10 observed correct designations. Easy/hard difficulty and two unrated assignments are authored claims. Source mathematical notation is normalized: raw exact solution reproduction is not claimed. Missing named-function context, fieldless source and absent correct refs are preserved in raw evidence and explicitly repaired. Bank intent for sparse opaque scalar banks remains unresolved; they are not normal default banks. See classification/template-extraction and validation for precise denominators and limits.

The native grader does not support a full `y=…` equation submitted to a scalar blank; this observed invalid-response-shape limitation is retained in native-limitations.json and is not counted as a grading pass. Canonical scalar slopes, unreduced product-rule equivalent entries and wrong scalar slopes are tested with the real grader.
